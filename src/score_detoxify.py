import os

import pandas as pd
from detoxify import Detoxify

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.chdir(ROOT)

model = Detoxify("original")

output_dir = "outputs"

for filename in os.listdir(output_dir):
    if (
        filename.endswith(".csv")
        and "detoxify" not in filename
        and "_integrity" not in filename
    ):
        input_path = os.path.join(output_dir, filename)
        output_path = os.path.join(output_dir, filename.replace(".csv", "_detoxify.csv"))

        print(f"Scoring: {input_path}")

        df = pd.read_csv(input_path)
        scores = model.predict(df["generated_text"].fillna("").tolist())
        df["detoxify_toxicity"] = scores["toxicity"]

        df.to_csv(output_path, index=False)
        print(f"Saved: {output_path}")