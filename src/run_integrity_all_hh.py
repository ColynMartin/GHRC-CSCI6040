"""
Score integrity metrics for every raw HH generation file in outputs/
(hh_<condition>.csv, excluding *_detoxify* and *_integrity*).
"""
import glob
import os
import sys

import pandas as pd

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, "src"))

from score_integrity_hh import process_integrity_csv


def _is_hh_generation_csv(path: str) -> bool:
    """True only for raw model output (e.g. not hh_tradeoff_summary.csv)."""
    try:
        cols = pd.read_csv(path, nrows=0).columns
    except (OSError, pd.errors.EmptyDataError, ValueError):
        return False
    return "prompt_id" in cols and "generated_text" in cols


def iter_hh_generation_csvs() -> list[str]:
    paths = []
    for p in sorted(glob.glob(os.path.join("outputs", "hh_*.csv"))):
        base = os.path.basename(p)
        if "detoxify" in base or "integrity" in base:
            continue
        if not _is_hh_generation_csv(p):
            continue
        paths.append(p)
    return paths


def main() -> None:
    paths = iter_hh_generation_csvs()
    if not paths:
        print("No outputs/hh_*.csv generation files found (skip *_detoxify*, *_integrity*).")
        sys.exit(0)
    for p in paths:
        print(f"\n=== {p} ===")
        try:
            process_integrity_csv(p, print_validation=True)
        except (FileNotFoundError, ValueError) as e:
            print(e)
            sys.exit(1)
    print(f"\nProcessed {len(paths)} file(s).")


if __name__ == "__main__":
    main()
