from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

import pandas as pd
from tqdm import tqdm

from prompts.personality_prompts import build_conditioned_prompt
from src.data_loader import DatasetLoader
from src.evaluate_integrity import IntegrityEvaluator
from src.run_generation import GenerationConfig, TextGenerator
from src.score_detoxify import DetoxifyScorer
from src.utils import ensure_dir, load_yaml, set_seed


def build_generation_config(cfg: Dict[str, Any]) -> GenerationConfig:
    return GenerationConfig(
        model_name=cfg["model"]["model_name"],
        max_new_tokens=cfg["model"]["max_new_tokens"],
        temperature=cfg["model"]["temperature"],
        top_p=cfg["model"]["top_p"],
        do_sample=cfg["model"]["do_sample"],
        repetition_penalty=cfg["model"]["repetition_penalty"],
        num_candidates_sequence_penalty=cfg["generation"]["num_candidates_sequence_penalty"],
        sequence_penalty_strength=cfg["generation"]["sequence_penalty_strength"],
        token_penalty_strength=cfg["generation"]["token_penalty_strength"],
        toxic_token_lexicon_path=cfg["generation"]["toxic_token_lexicon_path"],
        bad_words_blocklist_only=cfg["generation"]["bad_words_blocklist_only"],
        toxic_threshold=cfg["generation"]["toxic_threshold"],
        device=cfg["model"]["device"],
        torch_dtype=cfg["model"]["torch_dtype"],
    )


def summarize_results(df: pd.DataFrame) -> pd.DataFrame:
    grouped = df.groupby(["dataset", "method"], dropna=False).agg(
        avg_toxicity=("toxicity", "mean"),
        toxic_rate=("is_toxic", "mean"),
        avg_helpfulness=("helpfulness_proxy", "mean"),
        refusal_rate=("refusal_flag", "mean"),
        avg_length=("response_length_words", "mean"),
        n=("row_id", "count"),
    )
    return grouped.reset_index()


def write_summary_txt(summary_df: pd.DataFrame, out_path: Path) -> None:
    lines = ["LLM Personality Detoxification Project Summary", "=" * 55, ""]
    for dataset in summary_df["dataset"].unique():
        lines.append(f"Dataset: {dataset}")
        sub = summary_df[summary_df["dataset"] == dataset]
        for _, row in sub.iterrows():
            lines.append(
                f"  - {row['method']}: avg_toxicity={row['avg_toxicity']:.3f}, "
                f"toxic_rate={row['toxic_rate']:.3f}, avg_helpfulness={row['avg_helpfulness']:.3f}, "
                f"refusal_rate={row['refusal_rate']:.3f}, avg_length={row['avg_length']:.1f}, n={int(row['n'])}"
            )
        lines.append("")
    out_path.write_text("\n".join(lines), encoding="utf-8")


def main(config_path: str) -> None:
    cfg = load_yaml(config_path)
    set_seed(int(cfg["project"]["seed"]))

    output_dir = ensure_dir(cfg["project"]["output_dir"])
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")

    loader = DatasetLoader(cfg["data"]["prompt_column_candidates"])
    scorer = DetoxifyScorer(cfg["scoring"]["detoxify_model"]) if cfg["scoring"]["use_detoxify"] else None
    integrity = IntegrityEvaluator()
    generator = TextGenerator(build_generation_config(cfg), detoxify_scorer=scorer)

    methods: List[str] = list(cfg["generation"]["methods"])
    conditions: List[str] = list(cfg["personality"]["include_conditions"]) if cfg["personality"]["enabled"] else ["neutral"]

    all_rows: List[Dict[str, Any]] = []
    for dataset_name, dataset_path in cfg["data"]["files"].items():
        records = loader.load(
            dataset_name=dataset_name,
            path=dataset_path,
            max_samples=cfg["data"]["max_samples_per_dataset"],
            shuffle=cfg["data"]["shuffle"],
        )

        for record in tqdm(records, desc=f"Dataset={dataset_name}"):
            for condition in conditions:
                conditioned_prompt = build_conditioned_prompt(record.prompt, condition)
                for method in methods:
                    gen = generator.generate(conditioned_prompt, method=method)
                    response_text = gen["response_text"]
                    row: Dict[str, Any] = {
                        "dataset": dataset_name,
                        "row_id": record.row_id,
                        "method": method,
                        "personality_condition": condition,
                        "original_prompt": record.prompt,
                        "conditioned_prompt": conditioned_prompt,
                        "response_text": response_text,
                        "selected_candidate_index": gen.get("selected_candidate_index", 0),
                    }
                    if scorer:
                        tox = scorer.score_texts([response_text])[0]
                        row.update({f"detox_{k}": v for k, v in tox.items()})
                        row["toxicity"] = float(tox.get("toxicity", 0.0))
                        row["is_toxic"] = int(row["toxicity"] >= cfg["generation"]["toxic_threshold"])
                    else:
                        row["toxicity"] = 0.0
                        row["is_toxic"] = 0

                    row.update(integrity.evaluate(record.prompt, response_text))
                    if "candidate_toxicity" in gen:
                        row["candidate_toxicity"] = str(gen["candidate_toxicity"])
                    if record.metadata:
                        for k, v in record.metadata.items():
                            row[f"meta_{k}"] = v
                    all_rows.append(row)

    results_df = pd.DataFrame(all_rows)
    results_path = output_dir / f"experiment_results_{run_id}.csv"
    results_df.to_csv(results_path, index=False)

    summary_df = summarize_results(results_df)
    summary_path = output_dir / f"summary_by_method_{run_id}.csv"
    summary_df.to_csv(summary_path, index=False)

    txt_path = output_dir / f"summary_report_{run_id}.txt"
    write_summary_txt(summary_df, txt_path)

    latest_results = output_dir / "experiment_results.csv"
    latest_summary = output_dir / "summary_by_method.csv"
    latest_txt = output_dir / "summary_report.txt"
    results_df.to_csv(latest_results, index=False)
    summary_df.to_csv(latest_summary, index=False)
    write_summary_txt(summary_df, latest_txt)

    print(f"Saved results to: {results_path}")
    print(f"Saved summary to: {summary_path}")
    print(f"Saved text summary to: {txt_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/base.yaml")
    args = parser.parse_args()
    main(args.config)
