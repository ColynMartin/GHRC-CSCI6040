import pandas as pd
import os
import torch
import sys
import yaml
from transformers import pipeline

# Add project root so Python can find prompts/
sys.path.append(os.path.abspath("."))

from prompts.personality_prompts import build_prompt

# ---------------------------
# Load config
# ---------------------------
with open("configs/base.yaml", "r") as file:
    config = yaml.safe_load(file)

model_name = config["model_name"]
dataset_file = config["dataset_file"]
dataset_name = config["dataset"]
n_samples = config["n_samples"]
personality_conditions = config["personality_conditions"]
max_new_tokens = config["max_new_tokens"]
output_dir = config["output_dir"]

# Make sure output folder exists
os.makedirs(output_dir, exist_ok=True)

# ---------------------------
# Load dataset
# ---------------------------
df = pd.read_csv(dataset_file)
df = df.head(n_samples)

print(f"Loaded {len(df)} prompts from {dataset_name}")
print(f"Using model: {model_name}")
print(f"Running personality conditions: {personality_conditions}")

# ---------------------------
# Load model once
# ---------------------------
device = 0 if torch.cuda.is_available() else -1

if device == 0:
    print("Using GPU for generation")
else:
    print("GPU not found, using CPU")

generator = pipeline("text-generation", model=model_name, device=device)

# ---------------------------
# Run one condition at a time
# ---------------------------
for personality_condition in personality_conditions:
    print(f"\nRunning condition: {personality_condition}")

    results = []

    for _, row in df.iterrows():
        user_prompt = row["prompt_text"]
        full_prompt = build_prompt(personality_condition, user_prompt)

        output = generator(
            full_prompt,
            max_new_tokens=max_new_tokens,
            do_sample=False
        )

        full_generated_text = output[0]["generated_text"]

        # Remove the prompt from the output so only the new generated part remains
        if full_generated_text.startswith(full_prompt):
            generated_text = full_generated_text[len(full_prompt):].strip()
        else:
            generated_text = full_generated_text

        results.append({
            "prompt_id": row["prompt_id"],
            "dataset": dataset_name,
            "personality_condition": personality_condition,
            "prompt_text": user_prompt,
            "full_prompt": full_prompt,
            "generated_text": generated_text
        })

    results_df = pd.DataFrame(results)

    output_file = os.path.join(
        output_dir,
        f"{dataset_name.lower()}_{personality_condition}.csv"
    )

    results_df.to_csv(output_file, index=False)
    print(f"Saved: {output_file}")