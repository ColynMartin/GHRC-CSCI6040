from datasets import load_dataset
import pandas as pd
import os

print("Loading Anthropic HH dataset...")

# load dataset from Hugging Face
dataset = load_dataset("Anthropic/hh-rlhf")

print("Dataset loaded!")
print(dataset)

# convert the train split to pandas
df = pd.DataFrame(dataset["train"])

print("First few rows:")
print(df.head())

print("Columns:")
print(df.columns)

# make sure the data folder exists
os.makedirs("data", exist_ok=True)

# save dataset locally
output_path = "data/hh_full.csv"
df.to_csv(output_path, index=False)

print(f"Saved dataset to: {output_path}")