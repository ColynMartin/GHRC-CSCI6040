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
rtp_clean["reference_reply"] = ""
rtp_clean["dataset"] = "RTP"
rtp_clean["prompt_id"] = range(len(rtp_clean))
rtp_clean = rtp_clean[["prompt_text", "reference_reply", "dataset", "prompt_id"]]

rtp_clean.to_csv("data/rtp_clean.csv", index=False)

print("Saved RTP cleaned dataset")

# -----------------------
# Clean Anthropic HH
# -----------------------

hh = pd.read_csv("data/hh_full.csv")

# Extract the first human turn (same convention as before)
def extract_prompt(text):
    if not isinstance(text, str):
        return ""
    if "Human:" in text:
        return text.split("Human:")[1].split("Assistant:")[0].strip()
    return text


# Preferred assistant completion in `chosen` (final "Assistant:" segment)
def extract_reference_reply(text):
    if not isinstance(text, str) or "Assistant:" not in text:
        return ""
    return text.rsplit("Assistant:", 1)[-1].strip()


hh["prompt_text"] = hh["chosen"].apply(extract_prompt)
hh["reference_reply"] = hh["chosen"].apply(extract_reference_reply)

hh_clean = hh[["prompt_text", "reference_reply"]].copy()
hh_clean["dataset"] = "HH"
hh_clean["prompt_id"] = range(len(hh_clean))

hh_clean.to_csv("data/hh_clean.csv", index=False)

print("Saved HH cleaned dataset")