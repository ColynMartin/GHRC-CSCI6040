import pandas as pd
import os

os.makedirs("data", exist_ok=True)

# -----------------------
# Clean RealToxicityPrompts
# -----------------------

rtp = pd.read_csv("data/rtp_full.csv")

# Extract the nested prompt text
rtp["prompt_text"] = rtp["prompt"].apply(lambda x: eval(x)["text"])

rtp_clean = rtp[["prompt_text"]].copy()
rtp_clean["dataset"] = "RTP"
rtp_clean["prompt_id"] = range(len(rtp_clean))

rtp_clean.to_csv("data/rtp_clean.csv", index=False)

print("Saved RTP cleaned dataset")

# -----------------------
# Clean Anthropic HH
# -----------------------

hh = pd.read_csv("data/hh_full.csv")

# Extract the human prompt
def extract_prompt(text):
    if "Human:" in text:
        return text.split("Human:")[1].split("Assistant:")[0].strip()
    return text

hh["prompt_text"] = hh["chosen"].apply(extract_prompt)

hh_clean = hh[["prompt_text"]].copy()
hh_clean["dataset"] = "HH"
hh_clean["prompt_id"] = range(len(hh_clean))

hh_clean.to_csv("data/hh_clean.csv", index=False)

print("Saved HH cleaned dataset")