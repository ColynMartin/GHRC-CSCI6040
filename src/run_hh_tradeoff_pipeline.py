"""
End-to-end HH path: optional generation for all conditions, Detoxify, integrity on all HH gens, tradeoff tables.

Example:
  python src/run_hh_tradeoff_pipeline.py --generate   # full run (slow)
  python src/run_hh_tradeoff_pipeline.py              # use existing outputs/hh_*.csv
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
    args = parser.parse_args()

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
    print("\nDone. See outputs/hh_tradeoff_summary.csv and outputs/hh_tradeoff_summary.md")


if __name__ == "__main__":
    main()
