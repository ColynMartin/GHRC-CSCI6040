"""
End-to-end HH path: optional generation for all conditions, Detoxify, integrity on all HH gens, tradeoff tables.

Example:
  python src/run_hh_tradeoff_pipeline.py --generate   # full run (slow)
  python src/run_hh_tradeoff_pipeline.py              # use existing outputs/hh_*.csv
  python src/run_hh_tradeoff_pipeline.py --analyze-only
"""
import argparse
import os
import subprocess
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.chdir(ROOT)


def main() -> None:
    parser = argparse.ArgumentParser(description="HH toxicity vs helpfulness pipeline")
    parser.add_argument(
        "--generate",
        action="store_true",
        help="Run run_generation.py with configs/hh_all_conditions.yaml first",
    )
    parser.add_argument(
        "--config",
        default="configs/hh_all_conditions.yaml",
        help="Config for --generate (default: hh_all_conditions.yaml)",
    )
    parser.add_argument(
        "--analyze",
        action="store_true",
        help="After tradeoff tables, run analyze_detox_integrity.py",
    )
    parser.add_argument(
        "--analyze-only",
        action="store_true",
        help="Only run analyze_detox_integrity.py (expects HH integrity+detoxify CSVs)",
    )
    args = parser.parse_args()

    if args.analyze_only:
        print("Running detox vs integrity analysis only\n")
        subprocess.run([sys.executable, "src/analyze_detox_integrity.py"], check=True)
        print("\nDone. See outputs/detox_integrity_analysis.* and qualitative_examples.md")
        return

    if args.generate:
        print("Step 1: Generation (all HH conditions)\n")
        subprocess.run(
            [sys.executable, "src/run_generation.py", args.config],
            check=True,
        )
    print("\nStep 2: Detoxify (HH raw generations only: prefix hh_)\n")
    subprocess.run([sys.executable, "src/score_detoxify.py", "hh_"], check=True)
    print("\nStep 3: Integrity metrics (all HH generation files)\n")
    subprocess.run([sys.executable, "src/run_integrity_all_hh.py"], check=True)
    print("\nStep 4: Tradeoff summary tables\n")
    subprocess.run([sys.executable, "src/build_tradeoff_tables.py"], check=True)
    print("\nStep 5: Presentation tradeoff figure + slide bullets\n")
    subprocess.run([sys.executable, "src/plot_hh_tradeoff.py"], check=True)
    print(
        "\nDone. See outputs/hh_tradeoff_summary.csv, outputs/hh_tradeoff_summary.md, "
        "outputs/hh_tradeoff_scatter.png, outputs/presentation_tradeoff_findings.txt"
    )
    if args.analyze:
        print("\nStep 6: Detox vs integrity analysis + qualitative examples\n")
        subprocess.run([sys.executable, "src/analyze_detox_integrity.py"], check=True)
        print("\nAlso see outputs/detox_integrity_analysis.* and qualitative_examples.md")


if __name__ == "__main__":
    main()
