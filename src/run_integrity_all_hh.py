"""
Score integrity metrics for every raw HH generation file in outputs/
(hh_<condition>.csv, excluding *_detoxify* and *_integrity*).
"""
import glob
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, "src"))

from score_integrity_hh import process_integrity_csv


def iter_hh_generation_csvs() -> list[str]:
    paths = []
    for p in sorted(glob.glob(os.path.join("outputs", "hh_*.csv"))):
        base = os.path.basename(p)
        if "detoxify" in base or "integrity" in base:
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
