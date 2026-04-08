"""
Build per-condition toxicity vs helpfulness summary from HH Detoxify + integrity outputs.

Reads outputs/hh_<condition>_integrity.csv and outputs/hh_<condition>_detoxify.csv,
merges on prompt_id, aggregates means, writes CSV + Markdown table.
"""
import glob
import os
import re
import sys

import pandas as pd

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.chdir(ROOT)

OUTPUTS = "outputs"
SUMMARY_CSV = os.path.join(OUTPUTS, "hh_tradeoff_summary.csv")
SUMMARY_MD = os.path.join(OUTPUTS, "hh_tradeoff_summary.md")


def condition_from_integrity_path(path: str) -> str | None:
    m = re.match(r"hh_(.+)_integrity\.csv$", os.path.basename(path))
    return m.group(1) if m else None


def dataframe_to_markdown_table(df: pd.DataFrame) -> str:
    cols = df.columns.tolist()
    header = "| " + " | ".join(cols) + " |"
    sep = "| " + " | ".join("---" for _ in cols) + " |"
    lines = [header, sep]
    for _, row in df.iterrows():
        cells = []
        for c in cols:
            v = row[c]
            if isinstance(v, float):
                cells.append(f"{v:.4f}" if pd.notna(v) else "")
            else:
                cells.append(str(v))
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def main() -> None:
    rows: list[dict] = []
    missing_tox: list[str] = []

    for int_path in sorted(glob.glob(os.path.join(OUTPUTS, "hh_*_integrity.csv"))):
        cond = condition_from_integrity_path(int_path)
        if not cond:
            continue

        int_df = pd.read_csv(int_path)
        if "helpfulness_token_jaccard" not in int_df.columns:
            continue

        if "detoxify_toxicity" in int_df.columns:
            mean_tox = int_df["detoxify_toxicity"].mean()
            merged_n = len(int_df)
        else:
            tox_path = os.path.join(OUTPUTS, f"hh_{cond}_detoxify.csv")
            if os.path.isfile(tox_path):
                tox_df = pd.read_csv(tox_path)
                if "detoxify_toxicity" not in tox_df.columns:
                    missing_tox.append(cond)
                    mean_tox = float("nan")
                    merged_n = len(int_df)
                else:
                    m = int_df.merge(
                        tox_df[["prompt_id", "detoxify_toxicity"]],
                        on="prompt_id",
                        how="left",
                    )
                    mean_tox = m["detoxify_toxicity"].mean()
                    merged_n = len(m)
            else:
                missing_tox.append(cond)
                mean_tox = float("nan")
                merged_n = len(int_df)

        refusal = int_df["refusal_rule_based"].astype(bool) if "refusal_rule_based" in int_df.columns else pd.Series([float("nan")] * len(int_df))

        rows.append(
            {
                "personality_condition": cond,
                "n_prompts": merged_n,
                "mean_detoxify_toxicity": mean_tox,
                "mean_helpfulness_token_jaccard": int_df["helpfulness_token_jaccard"].mean(),
                "median_helpfulness_token_jaccard": int_df["helpfulness_token_jaccard"].median(),
                "refusal_rate_rule_based": refusal.mean(),
            }
        )

    if not rows:
        print("No outputs/hh_*_integrity.csv files found. Run src/run_integrity_all_hh.py first.")
        sys.exit(1)

    out = pd.DataFrame(rows)
    # Baseline first, then alphabetical by condition
    out["_sort"] = out["personality_condition"].apply(
        lambda c: (0 if c == "baseline" else 1, c)
    )
    out = out.sort_values("_sort").drop(columns=["_sort"]).reset_index(drop=True)

    os.makedirs(OUTPUTS, exist_ok=True)
    out.to_csv(SUMMARY_CSV, index=False)
    print(f"Wrote {SUMMARY_CSV}")

    md = (
        "# HH toxicity vs helpfulness (by personality condition)\n\n"
        "Mean/median **helpfulness_token_jaccard** and **refusal_rate_rule_based** from integrity scoring; "
        "**mean_detoxify_toxicity** from merged Detoxify scores (same `prompt_id`).\n\n"
        + dataframe_to_markdown_table(out)
        + "\n"
    )
    with open(SUMMARY_MD, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"Wrote {SUMMARY_MD}")

    if missing_tox:
        n = len(set(missing_tox))
        print(
            f"\nNote: Missing Detoxify output for {n} condition(s). "
            "Run `python src/run_generation.py configs/hh_all_conditions.yaml` "
            "then `python src/score_detoxify.py hh_` so each `hh_<condition>_detoxify.csv` exists."
        )


if __name__ == "__main__":
    main()
