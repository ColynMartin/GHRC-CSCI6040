import os
import sys

import pandas as pd
from detoxify import Detoxify

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.chdir(ROOT)

model = Detoxify("original")

output_dir = "outputs"
# Optional: only score files whose basename starts with this prefix (e.g. "hh_" for HH-only)
filename_prefix = sys.argv[1] if len(sys.argv) > 1 else None

for filename in os.listdir(output_dir):
    if filename_prefix and not filename.startswith(filename_prefix):
        continue
    if (
        filename.endswith(".csv")
        and "detoxify" not in filename
        and "_integrity" not in filename
    ):
        input_path = os.path.join(output_dir, filename)
        output_path = os.path.join(output_dir, filename.replace(".csv", "_detoxify.csv"))

        df = pd.read_csv(input_path)
        if "generated_text" not in df.columns:
            # e.g. hh_tradeoff_summary.csv matches prefix hh_ but is not model output
            print(f"Skipping (no generated_text): {input_path}")
            continue

        print(f"Scoring: {input_path}")

        scores = model.predict(df["generated_text"].fillna("").tolist())
        df["detoxify_toxicity"] = scores["toxicity"]

        df.to_csv(output_path, index=False)
        print(f"Saved: {output_path}")