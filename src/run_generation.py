from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional

import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    LogitsProcessorList,
)

from src.detox_methods import ToxicTokenPenaltyProcessor, load_toxic_lexicon
from src.score_detoxify import DetoxifyScorer
from src.utils import resolve_device


@dataclass
class GenerationConfig:
    model_name: str
    max_new_tokens: int = 64
    temperature: float = 0.8
    top_p: float = 0.95
    do_sample: bool = True
    repetition_penalty: float = 1.05
    num_candidates_sequence_penalty: int = 4
    sequence_penalty_strength: float = 1.0
    token_penalty_strength: float = 2.0
    toxic_token_lexicon_path: str = "configs/toxic_lexicon.txt"
    bad_words_blocklist_only: bool = False
    toxic_threshold: float = 0.5
    device: str = "auto"
    torch_dtype: str = "auto"


class TextGenerator:
    def __init__(
        self,
        cfg: GenerationConfig,
        detoxify_scorer: Optional[DetoxifyScorer] = None,
    ) -> None:
        self.cfg = cfg
        self.device = resolve_device(cfg.device)
        self.tokenizer = AutoTokenizer.from_pretrained(cfg.model_name)
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token

        dtype = torch.float16 if self.device == "cuda" and cfg.torch_dtype == "auto" else None
        self.model = AutoModelForCausalLM.from_pretrained(cfg.model_name, torch_dtype=dtype)
        self.model.to(self.device)
        self.model.eval()
        self.detoxify_scorer = detoxify_scorer
        self._toxic_terms = load_toxic_lexicon(cfg.toxic_token_lexicon_path)

    def _decode_only_new_tokens(self, input_ids: torch.Tensor, outputs: torch.Tensor) -> List[str]:
        prompt_len = input_ids.shape[1]
        new_tokens = outputs[:, prompt_len:]
        return self.tokenizer.batch_decode(new_tokens, skip_special_tokens=True)

    def _common_generate_kwargs(self) -> Dict:
        return {
            "max_new_tokens": self.cfg.max_new_tokens,
            "temperature": self.cfg.temperature,
            "top_p": self.cfg.top_p,
            "do_sample": self.cfg.do_sample,
            "repetition_penalty": self.cfg.repetition_penalty,
            "pad_token_id": self.tokenizer.eos_token_id,
        }

    @torch.no_grad()
    def generate(self, prompt: str, method: str = "baseline") -> Dict:
        encoded = self.tokenizer(prompt, return_tensors="pt", truncation=True).to(self.device)

        if method == "baseline":
            outputs = self.model.generate(**encoded, **self._common_generate_kwargs())
            text = self._decode_only_new_tokens(encoded["input_ids"], outputs)[0].strip()
            return {"response_text": text, "selected_candidate_index": 0, "candidate_texts": [text]}

        if method == "sequence_penalty":
            outputs = self.model.generate(
                **encoded,
                num_return_sequences=self.cfg.num_candidates_sequence_penalty,
                **self._common_generate_kwargs(),
            )
            candidates = [t.strip() for t in self._decode_only_new_tokens(encoded["input_ids"], outputs)]
            if not self.detoxify_scorer:
                raise ValueError("Sequence penalty requires a DetoxifyScorer.")
            scores = self.detoxify_scorer.score_texts(candidates)
            ranked = []
            for idx, (cand, sc) in enumerate(zip(candidates, scores)):
                toxicity = float(sc.get("toxicity", 0.0))
                utility_bonus = min(0.5, len(cand.split()) / 100.0)
                objective = toxicity * self.cfg.sequence_penalty_strength - utility_bonus
                ranked.append((objective, idx, cand, toxicity))
            ranked.sort(key=lambda x: x[0])
            _, best_idx, best_text, best_toxicity = ranked[0]
            return {
                "response_text": best_text,
                "selected_candidate_index": int(best_idx),
                "candidate_texts": candidates,
                "candidate_toxicity": [float(s.get("toxicity", 0.0)) for s in scores],
                "selected_candidate_toxicity": float(best_toxicity),
            }

        if method == "token_penalty":
            processor = ToxicTokenPenaltyProcessor(
                tokenizer=self.tokenizer,
                toxic_terms=self._toxic_terms,
                penalty_strength=self.cfg.token_penalty_strength,
                blocklist_only=self.cfg.bad_words_blocklist_only,
            )
            logits_processor = LogitsProcessorList([processor])
            outputs = self.model.generate(
                **encoded,
                logits_processor=logits_processor,
                **self._common_generate_kwargs(),
            )
            text = self._decode_only_new_tokens(encoded["input_ids"], outputs)[0].strip()
            return {"response_text": text, "selected_candidate_index": 0, "candidate_texts": [text]}

        raise ValueError(f"Unsupported method: {method}")
