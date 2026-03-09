import pandas as pd
import os
from detoxify import Detoxify

model = Detoxify("original")

output_dir = "outputs"

for filename in os.listdir(output_dir):
    if filename.endswith(".csv") and "detoxify" not in filename:
        input_path = os.path.join(output_dir, filename)
        output_path = os.path.join(output_dir, filename.replace(".csv", "_detoxify.csv"))

        print(f"Scoring: {input_path}")

        df = pd.read_csv(input_path)
        scores = model.predict(df["generated_text"].fillna("").tolist())
        df["detoxify_toxicity"] = scores["toxicity"]

        df.to_csv(output_path, index=False)
        print(f"Saved: {output_path}")