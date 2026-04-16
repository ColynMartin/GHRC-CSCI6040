"""
Week 5 synthesis visuals from Week 3–4 outputs (no new scoring).

Reads:
  - outputs/hh_tradeoff_summary.csv  (Week 3 aggregate: toxicity vs Jaccard per condition)
  - outputs/detox_integrity_analysis.csv  (Week 4: baseline-relative deltas and prompt-level rates)

Writes PNGs under outputs/week5_figures/ for slides and report.

Run from project root:
  python src/week5_synthesis_figures.py
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
os.chdir(ROOT)

OUTPUTS = ROOT / "outputs"
TRADEOFF_CSV = OUTPUTS / "hh_tradeoff_summary.csv"
DETOX_CSV = OUTPUTS / "detox_integrity_analysis.csv"


def _short_label(condition: str) -> str:
    if condition == "baseline":
        return "baseline"
    return condition.replace("_", "\n")


def figure_tradeoff_scatter(df: pd.DataFrame, out_dir: Path) -> Path:
    """Primary Week 5 figure: mean toxicity vs mean helpfulness Jaccard per condition."""
    x = df["mean_detoxify_toxicity"].to_numpy()
    y = df["mean_helpfulness_token_jaccard"].to_numpy()
    is_base = df["personality_condition"].eq("baseline")

    fig, ax = plt.subplots(figsize=(9, 6.5))
    ax.scatter(
        x[~is_base],
        y[~is_base],
        s=85,
        c="#2563eb",
        edgecolors="white",
        linewidths=0.8,
        zorder=3,
        label="Personality conditions",
    )
    ax.scatter(
        x[is_base],
        y[is_base],
        s=220,
        marker="*",
        c="#dc2626",
        edgecolors="white",
        linewidths=0.9,
        zorder=4,
        label="Baseline",
    )

    for _, row in df.iterrows():
        ax.annotate(
            _short_label(row["personality_condition"]),
            (row["mean_detoxify_toxicity"], row["mean_helpfulness_token_jaccard"]),
            textcoords="offset points",
            xytext=(4, 4),
            fontsize=7,
            alpha=0.92,
        )

    ax.set_xlabel("Mean Detoxify toxicity (lower is less toxic)")
    ax.set_ylabel("Mean helpfulness token Jaccard vs reference (higher ≈ more overlap)")
    ax.set_title("HH tradeoff snapshot: toxicity vs integrity proxy (per condition)")
    ax.grid(True, alpha=0.28, linestyle="--")
    ax.legend(loc="lower left", framealpha=0.95)
    fig.tight_layout()
    path = out_dir / "hh_tradeoff_scatter.png"
    fig.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(fig)
    return path


def figure_detox_integrity_rates(df: pd.DataFrame, out_dir: Path) -> Path | None:
    """Week 4 aggregates: win–win vs tradeoff-style rates (config-defined thresholds)."""
    if df.empty:
        return None
    methods = df["detox_method"].tolist()
    x = np.arange(len(methods))
    width = 0.35
    win = df["pct_win_win"].to_numpy(dtype=float)
    trade = df["pct_tradeoff_tox_down_integrity_hit"].to_numpy(dtype=float)

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar(x - width / 2, win, width, label="% win–win (tox ↓ & integrity preserved)", color="#059669")
    ax.bar(x + width / 2, trade, width, label="% tradeoff (tox ↓ but Jaccard hit vs baseline)", color="#d97706")
    ax.set_xticks(x)
    ax.set_xticklabels(methods, rotation=25, ha="right")
    ax.set_ylabel("Percent of matched prompts")
    ax.set_title("Week 4 detox vs baseline: prompt-level outcome rates (subset in detox_conditions.yaml)")
    ax.legend(loc="upper right", framealpha=0.95)
    ax.grid(True, axis="y", alpha=0.28, linestyle="--")
    ax.set_ylim(0, max(100, float(np.nanmax(np.r_[win, trade])) * 1.12))
    fig.tight_layout()
    path = out_dir / "detox_integrity_win_tradeoff_bars.png"
    fig.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(fig)
    return path


def figure_delta_scatter(df: pd.DataFrame, out_dir: Path) -> Path | None:
    """Aggregate Δ toxicity vs Δ Jaccard (Week 4 analysis vs same baseline generations)."""
    if df.empty:
        return None
    x = df["mean_delta_toxicity"].to_numpy()
    y = df["mean_delta_jaccard"].to_numpy()
    methods = df["detox_method"].tolist()

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.axhline(0, color="#94a3b8", linewidth=0.9, zorder=1)
    ax.axvline(0, color="#94a3b8", linewidth=0.9, zorder=1)
    ax.scatter(x, y, s=120, c="#7c3aed", edgecolors="white", linewidths=0.8, zorder=3)
    for i, m in enumerate(methods):
        ax.annotate(m.replace("_", "\n"), (x[i], y[i]), textcoords="offset points", xytext=(5, 5), fontsize=8)
    ax.set_xlabel("Mean Δ toxicity (method − baseline; positive = more toxic)")
    ax.set_ylabel("Mean Δ Jaccard (method − baseline; positive = higher overlap vs reference)")
    ax.set_title("Week 4: aggregate deltas vs shared baseline (matched prompts)")
    ax.grid(True, alpha=0.28, linestyle="--")
    fig.tight_layout()
    path = out_dir / "detox_integrity_delta_scatter.png"
    fig.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(fig)
    return path


def export_week5_table(tradeoff: pd.DataFrame, detox: pd.DataFrame, out_dir: Path) -> Path:
    """Single CSV merging mean-level tradeoff with Week 4 subset for citation."""
    t = tradeoff.rename(
        columns={
            "personality_condition": "condition",
            "mean_detoxify_toxicity": "mean_toxicity",
            "mean_helpfulness_token_jaccard": "mean_jaccard",
        }
    )[["condition", "n_prompts", "mean_toxicity", "mean_jaccard", "refusal_rate_rule_based"]]
    if not detox.empty:
        d = detox.rename(columns={"detox_method": "condition"})
        merged = t.merge(
            d[
                [
                    "condition",
                    "n_matched_prompts",
                    "mean_delta_jaccard",
                    "mean_delta_toxicity",
                    "pct_win_win",
                    "pct_tradeoff_tox_down_integrity_hit",
                ]
            ],
            on="condition",
            how="left",
        )
    else:
        merged = t.assign(
            n_matched_prompts=np.nan,
            mean_delta_jaccard=np.nan,
            mean_delta_toxicity=np.nan,
            pct_win_win=np.nan,
            pct_tradeoff_tox_down_integrity_hit=np.nan,
        )
    path = out_dir / "week5_synthesis_merged.csv"
    merged.to_csv(path, index=False)
    return path


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate Week 5 figures from Week 3–4 CSV outputs.")
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=OUTPUTS / "week5_figures",
        help="Directory for PNG exports (default: outputs/week5_figures)",
    )
    args = parser.parse_args()
    out_dir: Path = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    if not TRADEOFF_CSV.is_file():
        print(f"Missing {TRADEOFF_CSV}", file=sys.stderr)
        sys.exit(1)

    tradeoff = pd.read_csv(TRADEOFF_CSV)
    detox = pd.read_csv(DETOX_CSV) if DETOX_CSV.is_file() else pd.DataFrame()

    p1 = figure_tradeoff_scatter(tradeoff, out_dir)
    print(f"Wrote {p1}")

    p2 = figure_detox_integrity_rates(detox, out_dir)
    if p2:
        print(f"Wrote {p2}")
    else:
        print("Skipped detox_integrity bar chart (empty or missing detox_integrity_analysis.csv)")

    p3 = figure_delta_scatter(detox, out_dir)
    if p3:
        print(f"Wrote {p3}")
    else:
        print("Skipped delta scatter (empty or missing detox_integrity_analysis.csv)")

    merged = export_week5_table(tradeoff, detox, out_dir)
    print(f"Wrote {merged}")


if __name__ == "__main__":
    main()
