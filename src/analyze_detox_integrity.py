"""
Compare baseline HH runs to configured "detox" personality conditions:
quantitative integrity/toxicity deltas and qualitative example export.

Inputs: outputs/hh_<condition>_integrity.csv + hh_<condition>_detoxify.csv
Config: configs/detox_conditions.yaml
Outputs: outputs/detox_integrity_analysis.csv, .md, outputs/qualitative_examples.md
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import pandas as pd
import yaml

ROOT = Path(__file__).resolve().parent.parent
os.chdir(ROOT)

OUTPUTS = ROOT / "outputs"
CONFIG_PATH = ROOT / "configs" / "detox_conditions.yaml"
OUT_SUMMARY_CSV = OUTPUTS / "detox_integrity_analysis.csv"
OUT_SUMMARY_MD = OUTPUTS / "detox_integrity_analysis.md"
OUT_QUALITATIVE = OUTPUTS / "qualitative_examples.md"


def clip(s: str, n: int) -> str:
    s = (s or "").replace("\r", " ").replace("\n", " ").strip()
    if len(s) <= n:
        return s
    return s[: n - 3] + "..."


def md_cell(s: str) -> str:
    return (s or "").replace("|", "\\|").replace("\n", " ")


def dataframe_to_markdown_table(df: pd.DataFrame) -> str:
    cols = df.columns.tolist()
    header = "| " + " | ".join(cols) + " |"
    sep = "| " + " | ".join("---" for _ in cols) + " |"
    lines = [header, sep]
    for _, row in df.iterrows():
        cells = []
        for c in cols:
            v = row[c]
            if isinstance(v, float) and pd.notna(v):
                cells.append(f"{v:.6f}")
            elif pd.isna(v):
                cells.append("")
            else:
                cells.append(str(v))
        lines.append("| " + " | ".join(md_cell(x) for x in cells) + " |")
    return "\n".join(lines)


def load_integrity_plus_tox(condition: str) -> pd.DataFrame | None:
    ip = OUTPUTS / f"hh_{condition}_integrity.csv"
    tp = OUTPUTS / f"hh_{condition}_detoxify.csv"
    if not ip.is_file() or not tp.is_file():
        return None
    i = pd.read_csv(ip)
    t = pd.read_csv(tp)
    if "detoxify_toxicity" not in t.columns:
        return None
    m = i.merge(t[["prompt_id", "detoxify_toxicity"]], on="prompt_id", how="inner")
    return m


def compare_to_baseline(
    base: pd.DataFrame, cond: pd.DataFrame, method: str
) -> pd.DataFrame:
    b = base[
        [
            "prompt_id",
            "prompt_text",
            "reference_reply",
            "generated_text",
            "helpfulness_token_jaccard",
            "refusal_rule_based",
            "detoxify_toxicity",
        ]
    ].rename(
        columns={
            "generated_text": "gen_baseline",
            "helpfulness_token_jaccard": "jac_baseline",
            "refusal_rule_based": "ref_baseline",
            "detoxify_toxicity": "tox_baseline",
        }
    )
    c = cond[
        [
            "prompt_id",
            "generated_text",
            "helpfulness_token_jaccard",
            "refusal_rule_based",
            "detoxify_toxicity",
        ]
    ].rename(
        columns={
            "generated_text": f"gen_{method}",
            "helpfulness_token_jaccard": f"jac_{method}",
            "refusal_rule_based": f"ref_{method}",
            "detoxify_toxicity": f"tox_{method}",
        }
    )
    return b.merge(c, on="prompt_id", how="inner")


def main() -> None:
    if not CONFIG_PATH.is_file():
        print(f"Missing {CONFIG_PATH}")
        sys.exit(1)

    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    baseline_name = cfg.get("baseline", "baseline")
    methods: list[str] = cfg.get("detox_methods") or []
    tox_improve = float(cfg.get("toxicity_improvement_min", 0.0005))
    jac_tol = float(cfg.get("integrity_drop_tolerance", 0.02))
    ex_per_cat = int(cfg.get("examples_per_category", 2))
    max_ch = int(cfg.get("max_chars_per_field", 450))

    base = load_integrity_plus_tox(baseline_name)
    if base is None:
        print(
            f"Missing baseline outputs for '{baseline_name}'. "
            "Run HH generation + `python src/score_detoxify.py hh_` + `python src/run_integrity_all_hh.py`."
        )
        sys.exit(1)

    summary_rows: list[dict] = []
    qualitative_sections: list[str] = []

    intro = (
        "# Qualitative examples: detox personality vs baseline (HH)\n\n"
        "Each block lists **prompt_id**, short **prompt**, **reference** (HH chosen), "
        "**baseline** generation, and **condition** generation. "
        "Use these in your report alongside `detox_integrity_analysis.csv`.\n\n"
    )

    for method in methods:
        cond_df = load_integrity_plus_tox(method)
        if cond_df is None:
            summary_rows.append(
                {
                    "detox_method": method,
                    "n_matched_prompts": 0,
                    "note": "missing integrity or detoxify file",
                }
            )
            qualitative_sections.append(f"## {method}\n\n_Skipped — outputs not found._\n\n")
            continue

        m = compare_to_baseline(base, cond_df, method)
        jac_c = f"jac_{method}"
        tox_c = f"tox_{method}"
        ref_c = f"ref_{method}"
        gen_c = f"gen_{method}"

        m["delta_jaccard"] = m[jac_c] - m["jac_baseline"]
        m["delta_toxicity"] = m[tox_c] - m["tox_baseline"]
        m["toxicity_down"] = m["delta_toxicity"] <= -tox_improve
        m["integrity_preserved"] = m["delta_jaccard"] >= -jac_tol
        m["tradeoff"] = m["toxicity_down"] & (~m["integrity_preserved"])
        m["win_win"] = m["toxicity_down"] & m["integrity_preserved"]

        n = len(m)
        summary_rows.append(
            {
                "detox_method": method,
                "n_matched_prompts": n,
                "mean_delta_jaccard": m["delta_jaccard"].mean(),
                "mean_delta_toxicity": m["delta_toxicity"].mean(),
                "pct_toxicity_down": m["toxicity_down"].mean() * 100,
                "pct_integrity_preserved": m["integrity_preserved"].mean() * 100,
                "pct_tradeoff_tox_down_integrity_hit": m["tradeoff"].mean() * 100,
                "pct_win_win": m["win_win"].mean() * 100,
                "mean_jaccard_baseline": m["jac_baseline"].mean(),
                "mean_jaccard_method": m[jac_c].mean(),
                "mean_tox_baseline": m["tox_baseline"].mean(),
                "mean_tox_method": m[tox_c].mean(),
            }
        )

        # --- qualitative buckets ---
        qual_parts = [f"## Condition: `{method}`\n\n"]

        def pick_examples(mask: pd.Series, title: str) -> None:
            sub = m.loc[mask].copy()
            if sub.empty:
                qual_parts.append(f"### {title}\n\n_No prompts matched._\n\n")
                return
            sub = sub.sort_values("delta_toxicity", ascending=True)
            take = sub.head(ex_per_cat)
            qual_parts.append(f"### {title}\n\n")
            for _, r in take.iterrows():
                pid = int(r["prompt_id"])
                qual_parts.append(f"#### prompt_id {pid}\n\n")
                qual_parts.append(
                    f"- **Prompt:** {clip(str(r['prompt_text']), max_ch)}\n"
                    f"- **Reference reply:** {clip(str(r['reference_reply']), max_ch)}\n"
                    f"- **Baseline gen** (jaccard={r['jac_baseline']:.4f}, tox={r['tox_baseline']:.4f}): "
                    f"{clip(str(r['gen_baseline']), max_ch)}\n"
                    f"- **{method} gen** (jaccard={r[jac_c]:.4f}, tox={r[tox_c]:.4f}): "
                    f"{clip(str(r[gen_c]), max_ch)}\n"
                    f"- **Δ jaccard / Δ tox:** {r['delta_jaccard']:.4f} / {r['delta_toxicity']:.4f}\n\n"
                )

        pick_examples(m["win_win"], "Win–win (toxicity down, integrity within tolerance)")
        pick_examples(m["tradeoff"], "Tradeoff (toxicity down, integrity drop beyond tolerance)")
        loss = ~m["toxicity_down"] & (~m["integrity_preserved"])
        pick_examples(loss, "Integrity loss without clear toxicity gain")
        qual_parts.append("\n---\n\n")
        qualitative_sections.append("".join(qual_parts))

    OUTPUTS.mkdir(parents=True, exist_ok=True)
    sum_df = pd.DataFrame(summary_rows)
    sum_df.to_csv(OUT_SUMMARY_CSV, index=False)
    print(f"Wrote {OUT_SUMMARY_CSV}")

    md_lines = [
        "# Detox vs integrity — summary (vs baseline)\n\n",
        "Per **detox_method**: matched prompts, mean Δ in token Jaccard (helpfulness proxy) and Δ in Detoxify toxicity, "
        "and rough prompt-level rates. **integrity_preserved** = Jaccard did not fall more than "
        f"`integrity_drop_tolerance` ({jac_tol}) vs baseline. **toxicity_down** = toxicity lower by at least "
        f"`toxicity_improvement_min` ({tox_improve}).\n\n",
    ]
    if not sum_df.empty:
        md_lines.append(dataframe_to_markdown_table(sum_df))
    md_lines.append("\n")
    OUT_SUMMARY_MD.write_text("".join(md_lines), encoding="utf-8")
    print(f"Wrote {OUT_SUMMARY_MD}")

    OUT_QUALITATIVE.write_text(intro + "".join(qualitative_sections), encoding="utf-8")
    print(f"Wrote {OUT_QUALITATIVE}")


if __name__ == "__main__":
    main()
