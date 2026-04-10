"""
Presentation figures + brief findings from HH tradeoff summaries.

Reads outputs/hh_tradeoff_summary.csv (from build_tradeoff_tables.py).
Optionally enriches bullets with outputs/detox_integrity_analysis.csv if present.

Writes:
  outputs/hh_tradeoff_scatter.png  — mean toxicity vs mean helpfulness (Jaccard) by condition
  outputs/presentation_tradeoff_findings.txt — bullets for slides (supported / not supported)
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
os.chdir(ROOT)

OUTPUTS = ROOT / "outputs"
SUMMARY_CSV = OUTPUTS / "hh_tradeoff_summary.csv"
DETOX_ANALYSIS_CSV = OUTPUTS / "detox_integrity_analysis.csv"
OUT_PNG = OUTPUTS / "hh_tradeoff_scatter.png"
OUT_FINDINGS = OUTPUTS / "presentation_tradeoff_findings.txt"


def _short_label(cond: str) -> str:
    return cond.replace("high_", "H.").replace("low_", "L.").replace("_", " ")[:18]


def write_findings(summary: pd.DataFrame, detox_extra: pd.DataFrame | None) -> str:
    lines: list[str] = []
    lines.append("Toxicity vs helpfulness (tradeoff) — auto summary from hh_tradeoff_summary.csv")
    lines.append("Edit wording for your voice; numbers are from the CSV.")
    lines.append("")

    base = summary.loc[summary["personality_condition"].str.lower() == "baseline"]
    if base.empty:
        lines.append("No baseline row in summary — add baseline condition or fix CSV.")
        return "\n".join(lines)

    b = base.iloc[0]
    bt, bj = float(b["mean_detoxify_toxicity"]), float(b["mean_helpfulness_token_jaccard"])
    rest = summary.loc[summary["personality_condition"].str.lower() != "baseline"].copy()

    lines.append("Key numbers (means across prompts)")
    lines.append(f"- Baseline: mean Detoxify toxicity = {bt:.4f}; mean token Jaccard = {bj:.4f}")
    lines.append("")

    lower_tox = (rest["mean_detoxify_toxicity"] < bt).sum()
    higher_help = (rest["mean_helpfulness_token_jaccard"] > bj).sum()
    n = len(rest)
    lines.append("Supported by this aggregate table (vs baseline row)")
    lines.append(
        f"- Personality conditions with lower mean toxicity than baseline: {lower_tox} / {n}"
    )
    lines.append(
        f"- Personality conditions with higher mean Jaccard than baseline: {higher_help} / {n}"
    )
    lines.append(
        "- Interpretation: if most points sit northeast of baseline on the scatter, "
        "the run shows higher toxicity and higher overlap-with-reference together vs baseline "
        "(not a simple 'less toxic' win at the means)."
    )
    lines.append("")

    lines.append("Not supported / caveats (always mention)")
    lines.append("- Token Jaccard vs reference is a proxy for helpfulness, not human ratings.")
    lines.append("- Detoxify scores are model-based and sensitive to wording; use as a relative signal.")
    lines.append("")

    if detox_extra is not None and not detox_extra.empty:
        lines.append("Cross-check: detox_integrity_analysis.csv (prompt-level vs same baseline gens)")
        for _, row in detox_extra.iterrows():
            m = str(row.get("detox_method", ""))
            pct_win = row.get("pct_win_win", "")
            pct_td = row.get("pct_tradeoff_tox_down_integrity_hit", "")
            lines.append(
                f"- {m}: prompt-level 'toxicity down + integrity preserved' style rate ≈ {pct_td}%; "
                f"win-win rate ≈ {pct_win}% (see analysis config thresholds)."
            )
        lines.append("")

    lines.append("Evidence to show")
    lines.append(f"- Figure: {OUT_PNG.name} (mean toxicity × mean Jaccard per condition).")
    lines.append(f"- Table: {SUMMARY_CSV.name} and project README / work logs for setup.")
    return "\n".join(lines)


def plot_scatter(summary: pd.DataFrame) -> None:
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(9, 6), dpi=150)
    base_mask = summary["personality_condition"].str.lower() == "baseline"
    base = summary.loc[base_mask]
    rest = summary.loc[~base_mask]

    ax.scatter(
        rest["mean_detoxify_toxicity"],
        rest["mean_helpfulness_token_jaccard"],
        s=120,
        alpha=0.85,
        c="#2c7bb6",
        edgecolors="white",
        linewidths=0.5,
        label="Personality conditions",
        zorder=2,
    )
    if not base.empty:
        ax.scatter(
            base["mean_detoxify_toxicity"],
            base["mean_helpfulness_token_jaccard"],
            s=220,
            marker="*",
            c="#d7191c",
            edgecolors="white",
            linewidths=0.8,
            label="Baseline",
            zorder=3,
        )

    for _, row in summary.iterrows():
        ax.annotate(
            _short_label(str(row["personality_condition"])),
            (
                float(row["mean_detoxify_toxicity"]),
                float(row["mean_helpfulness_token_jaccard"]),
            ),
            textcoords="offset points",
            xytext=(4, 4),
            fontsize=7,
            alpha=0.9,
        )

    ax.set_xlabel("Mean Detoxify toxicity (lower is better)")
    ax.set_ylabel("Mean helpfulness token Jaccard vs reference (higher = more overlap)")
    ax.set_title("HH runs: toxicity vs helpfulness proxy (by personality condition)")
    ax.grid(True, alpha=0.3, linestyle="--")
    ax.legend(loc="best")
    fig.tight_layout()
    OUT_PNG.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT_PNG, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {OUT_PNG}")


def main() -> None:
    if not SUMMARY_CSV.is_file():
        print(f"Missing {SUMMARY_CSV}. Run: python src/build_tradeoff_tables.py")
        sys.exit(1)

    summary = pd.read_csv(SUMMARY_CSV)
    need = {"mean_detoxify_toxicity", "mean_helpfulness_token_jaccard", "personality_condition"}
    if not need.issubset(set(summary.columns)):
        print(f"Expected columns {need} in {SUMMARY_CSV}")
        sys.exit(1)

    detox_extra: pd.DataFrame | None = None
    if DETOX_ANALYSIS_CSV.is_file():
        detox_extra = pd.read_csv(DETOX_ANALYSIS_CSV)

    text = write_findings(summary, detox_extra)
    OUT_FINDINGS.write_text(text, encoding="utf-8")
    print(f"Saved: {OUT_FINDINGS}")

    try:
        plot_scatter(summary)
    except ImportError:
        print(
            "matplotlib not installed. Install with: pip install matplotlib\n"
            f"Findings file was still written to {OUT_FINDINGS}"
        )
        sys.exit(0)


if __name__ == "__main__":
    main()
