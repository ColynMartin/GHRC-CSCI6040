# LLM Personality Detoxification Project

A scaled-down reproduction of a research study investigating how **HEXACO-based personality prompts** influence **toxicity in large language model outputs**.

---

## Quick Start

Activate the environment:

```
venv\Scripts\activate
```


Run the full experiment pipeline:

```
python src/run_experiment.py
```

This command will:

1. Generate model responses using personality prompts
2. Score toxicity using Detoxify
3. Save results to the `outputs/` folder

⚠️ Note:  
All important experiment outputs should be uploaded to the shared OneDrive folder (see Data Storage section below).

---

## Project Structure

```
llm-personality-project
│
├── configs
│   └── base.yaml
│
├── data
│   ├── rtp_clean.csv
│   └── hh_clean.csv
│
├── prompts
│   └── personality_prompts.py
│
├── src
│   ├── run_experiment.py
│   ├── run_generation.py
│   └── score_detoxify.py
│
├── outputs
│
└── README.md
```

---

## Pipeline

```
Dataset
   ↓
Personality Prompt Injection
   ↓
LLM Generation
   ↓
Toxicity Scoring (Detoxify)
   ↓
CSV Results
```

---

## Datasets

- **RealToxicityPrompts (RTP)** – used for generating text and measuring toxicity.
- **Anthropic Helpful-Harmless (HH)** – used to test whether detoxification affects helpfulness.

---

## Data Storage

All large datasets and experiment outputs are stored in OneDrive:

https://studentsecuedu66932-my.sharepoint.com/:f:/r/personal/rickardr25_students_ecu_edu/Documents/NLP%20Project?csf=1&web=1&e=ik1K7j

### Folder Structure
```
nlp_project
│
├── week1/
│
├── week2/
│
├── week3/
│
├── week4/
│
├── week5/
│
├── final_results
│
└── archive
```

Each week contains:
```
rtp_outputs/
hh_outputs/
detox_scores/
analysis/
configs/
logs/
```

### Guidelines

- Do **not** upload large output files to GitHub  
- Upload all experiment results to the appropriate OneDrive folder  
- Do **not overwrite files** — create new versions (`v1`, `v2`, etc.)  
- Use consistent file naming  

### File Naming Convention
```
dataset_model_method_v#.csv
```
Examples:
```
rtp_llama_baseline_v1.csv
rtp_gpt4_tokenpenalty_v2.csv
hh_llama_sequence_v1.csv
```

---

## Reproducibility

To ensure experiments can be reproduced:

Each output must include:
- a corresponding config file (`.yaml`)
- an entry in the experiment log (`logs/experiment_log.csv`)

### Reproducing an Experiment

1. Download the required dataset/output from OneDrive  
2. Locate the corresponding config file  
3. Run:
```
python src/run_experiment.py --config configs/base.yaml
```

---

## Team Workflow (Pipeline-Specific)

This workflow is tailored to how `run_experiment.py` works.

---

### Step 1 — Pull Latest Code
```
git pull origin main
```
### Step 2 — Run the Pipeline
```
python src/run_experiment.py
```

This will:
- load RTP or HH dataset  
- apply personality prompts  
- generate outputs  
- score toxicity with Detoxify  
- save results to `outputs/`

### Step 3 — Rename Output File

Before uploading, rename your file:
```
dataset_model_method_v#.csv
```

Example:
```
rtp_llama_baseline_v1.csv
```
### Step 4 — Upload to OneDrive

Upload to:
```
weekX/rtp_outputs/
weekX/hh_outputs/
weekX/detox_scores/
```
### Step 5 — Save Config

Save your config file to:
```
weekX/configs/
```
Example:
```
rtp_llama_baseline_v1_config.yaml
```
### Step 6 — Update Experiment Log

Open:
```
weekX/logs/experiment_log.csv
```
Add:
```
file_name,model,method,dataset,date,owner,notes
rtp_llama_baseline_v1.csv,llama,baseline,rtp,2026-04-01,YourName,initial run
```
### Step 7 — Notify Team

Example message:
```
Uploaded Week 1 RTP baseline (llama)
- rtp_llama_baseline_v1.csv
- config included
- log updated
```

---

### Folder Responsibilities

| Task | Folder |
|------|--------|
| RTP outputs | `rtp_outputs/` |
| HH outputs | `hh_outputs/` |
| Detox scores | `detox_scores/` |
| Analysis | `analysis/` |
| Configs | `configs/` |
| Logs | `logs/` |

---

### Final Checklist

- [ ] File named correctly  
- [ ] Uploaded to correct folder  
- [ ] Config saved  
- [ ] Log updated  
- [ ] Team notified  

---

## Common Mistakes (Read This First)

### ❌ Uploading to GitHub instead of OneDrive
✔ Fix: All outputs go in OneDrive, not GitHub

---

### ❌ Overwriting files
✔ Fix: Always increment version
```
v1 → v2 → v3
```
---

### ❌ Bad file names
❌ `results.csv`  
❌ `final_new.csv`  

✔ Use:
```
rtp_llama_tokenpenalty_v1.csv
```

---

### ❌ Forgetting config files
✔ Every output must have a matching `.yaml`

---

### ❌ Not updating experiment log
✔ If it’s not logged, it didn’t happen

---

### ❌ Uploading to wrong folder
✔ Check:
- RTP → `rtp_outputs`
- HH → `hh_outputs`

---

### ❌ Not pulling latest code
✔ Always run:
```
git pull origin main
```
---

### ❌ OneDrive not synced
✔ Check sync icon before assuming upload worked

---

## Team Roles

| Role | Responsibility |
|-----|-----|
| Rebecca Rickard | Infrastructure and experiment pipeline |
| Colyn Martin | Hypothesis 1 – toxic regions |
| Gaurav Goyal | Hypothesis 2 – detox methods |
| Heather Bowman | Hypothesis 3 – integrity vs helpfulness |

---

## Notes

This project uses a **scaled-down experimental design** so the full pipeline can run on a personal computer while still reproducing core research behavior.

Raw datasets are not included due to file size limits.

Download from:
- RealToxicityPrompts – Allen Institute for AI / Hugging Face  
- Anthropic Helpful-Harmless – Hugging Face  
