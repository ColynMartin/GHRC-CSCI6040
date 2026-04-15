from __future__ import annotations

from pathlib import Path
from typing import Iterable, List

import torch
from transformers import LogitsProcessor


def load_toxic_lexicon(path: str | Path) -> List[str]:
    with open(path, "r", encoding="utf-8") as f:
        items = [line.strip() for line in f if line.strip() and not line.startswith("#")]
    return items


class ToxicTokenPenaltyProcessor(LogitsProcessor):
    """Subtract a fixed penalty from logits associated with toxic lexicon token IDs."""

    def __init__(
        self,
        tokenizer,
        toxic_terms: Iterable[str],
        penalty_strength: float = 2.0,
        blocklist_only: bool = False,
    ) -> None:
        self.penalty_strength = float(penalty_strength)
        self.blocklist_only = bool(blocklist_only)
        token_ids = set()
        for term in toxic_terms:
            encoded = tokenizer.encode(term, add_special_tokens=False)
            token_ids.update(encoded)
        self.toxic_token_ids = sorted(token_ids)

    def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor) -> torch.FloatTensor:
        if not self.toxic_token_ids:
            return scores
        if self.blocklist_only:
            scores[:, self.toxic_token_ids] = -float("inf")
        else:
            scores[:, self.toxic_token_ids] -= self.penalty_strength
        return scores
