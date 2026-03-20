"""
Run HH prompts from a config, then score helpfulness/refusal (pre-Detoxify).
Default config is baseline-only on HH (`configs/hh_baseline.yaml`).
"""
import os
import subprocess
import sys

import yaml

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.chdir(ROOT)


def main() -> None:
    config_path = sys.argv[1] if len(sys.argv) > 1 else "configs/hh_baseline.yaml"
    print("Step 1: Generation\n")
    subprocess.run(
        [sys.executable, "src/run_generation.py", config_path],
        check=True,
    )

    with open(config_path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    dataset = str(cfg["dataset"]).lower()
    conditions = cfg["personality_conditions"]

    print("\nStep 2: Integrity metrics (before Detoxify)\n")
    for cond in conditions:
        gen_csv = os.path.join("outputs", f"{dataset}_{cond}.csv")
        subprocess.run(
            [sys.executable, "src/score_integrity_hh.py", gen_csv],
            check=True,
        )
    print("\nDone. See outputs/<dataset>_<condition>_integrity.csv")
    print("Optional: python src/score_detoxify.py  (adds toxicity when you are ready)")


if __name__ == "__main__":
    main()
