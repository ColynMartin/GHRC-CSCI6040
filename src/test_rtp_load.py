from datasets import load_dataset
import pandas as pd
import os

print("Loading dataset...")
dataset = load_dataset("allenai/real-toxicity-prompts")

print("Dataset loaded successfully.")
print(dataset)

# Convert the train split to a pandas DataFrame
df = pd.DataFrame(dataset["train"])

print("First few rows:")
print(df.head())

print("Columns:")
print(df.columns)

# Make sure the data folder exists
os.makedirs("data", exist_ok=True)

# Save the full dataset
output_path = "data/rtp_full.csv"
df.to_csv(output_path, index=False)

print(f"Saved dataset to: {output_path}")
print(f"Current working directory: {os.getcwd()}")