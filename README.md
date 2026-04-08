# LLM Personality Detoxification Project

A scaled-down reproduction of a research study investigating how **HEXACO-based personality prompts** influence **toxicity in large language model outputs**.

---

## Quick Start

Activate the environment.

**venv (Windows):**

```
venv\Scripts\activate
```

**Anaconda (PowerShell):** one-time setup is `conda init powershell` from **Anaconda Prompt**, then open a new terminal. In the project folder, either run `conda activate base` (or your env name), or dot-source the helper (must be dotted so it changes the current session):

```
. .\scripts\conda_activate.ps1
```

Optional: `. .\scripts\conda_activate.ps1 your_env_name`

In Cursor/VS Code, use **Python: Select Interpreter** and pick that environment’s `python.exe`.


Run the full experiment pipeline:

```
python src/run_experiment.py
```

Optional config (paths are relative to the project root):

```
python src/run_experiment.py configs/hh_baseline.yaml
```

This command will:

1. Generate model responses using personality prompts
2. Score toxicity using Detoxify
3. Save results to the `outputs/` folder

### HH baseline: helpfulness before Detoxify

After `data/hh_clean.csv` exists (with `reference_reply`; see `src/clean_datasets.py`):

```
python src/run_hh_baseline_eval.py
```

This runs generation from `configs/hh_baseline.yaml` (HH, baseline only by default), then `src/score_integrity_hh.py` for each condition, writing e.g. `outputs/hh_baseline_integrity.csv` and printing **metric validation** (coverage, score ranges, refusal rate). Run `python src/score_detoxify.py` afterward when you want toxicity on the raw generation files (integrity CSVs are skipped by Detoxify to avoid duplicate scoring).

**Week 2 work log** (baseline run, helpfulness before detox, validating metrics): [`logs/week2_hh_baseline_helpfulness_validation_work_log.md`](logs/week2_hh_baseline_helpfulness_validation_work_log.md).

### HH: integrity across all methods + toxicity vs helpfulness tables

1. Generate for **every** personality condition using `configs/hh_all_conditions.yaml` (or use the bundled pipeline below).
2. **Integrity on all HH runs:** `python src/run_integrity_all_hh.py` — scores every `outputs/hh_<condition>.csv` (skips `*_detoxify*` and `*_integrity*`).
3. **Detoxify on HH generations:** `python src/score_detoxify.py hh_` — optional `hh_` prefix limits scoring to files starting with `hh_` (omit the argument to score all raw output CSVs as before).
4. **Tradeoff tables:** `python src/build_tradeoff_tables.py` — writes `outputs/hh_tradeoff_summary.csv` and `outputs/hh_tradeoff_summary.md` (mean toxicity, mean/median helpfulness Jaccard, refusal rate per condition).

One-shot (add `--generate` to include the slow generation step):

```
python src/run_hh_tradeoff_pipeline.py --generate
```

**Week 3 work log** (integrity across all methods + tradeoff tables): [`logs/week3_integrity_all_methods_tradeoff_work_log.md`](logs/week3_integrity_all_methods_tradeoff_work_log.md). Log rows for summary artifacts: [`logs/experiment_log.csv`](logs/experiment_log.csv).

### HH: detox methods vs integrity + qualitative examples

After per-condition `hh_*_integrity.csv` and `hh_*_detoxify.csv` exist, edit **`configs/detox_conditions.yaml`** (which personality runs count as “detox” vs `baseline`), then:

```
python src/analyze_detox_integrity.py
```

This writes **`outputs/detox_integrity_analysis.csv`** / **`.md`** (aggregate Δ helpfulness Jaccard, Δ toxicity, tradeoff vs win–win rates) and **`outputs/qualitative_examples.md`** (side-by-side prompts, reference, baseline vs condition generations). Interpretation notes: [`docs/detox_integrity_analysis_guide.md`](docs/detox_integrity_analysis_guide.md).

**Week 4 work log** (detox vs integrity + qualitative examples — commands, configs, artifacts, OneDrive checklist): [`logs/week4_integrity_qualitative_work_log.md`](logs/week4_integrity_qualitative_work_log.md). **Experiment log rows** for this stream: [`logs/experiment_log.csv`](logs/experiment_log.csv).

- `python src/run_hh_tradeoff_pipeline.py --analyze` — reruns Detoxify (HH prefix), integrity-all, tradeoff tables, then `analyze_detox_integrity.py`.
- `python src/run_hh_tradeoff_pipeline.py --analyze-only` — runs **only** `analyze_detox_integrity.py` (expects per-condition integrity + Detoxify CSVs already on disk).

⚠️ **Note:** All important experiment outputs should be uploaded to the shared OneDrive folder (see Data Storage section below).

---

## Project Structure

```
llm-personality-project
│
├── configs
│   ├── base.yaml
│   ├── detox_conditions.yaml
│   ├── hh_all_conditions.yaml
│   └── hh_baseline.yaml
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
│   ├── run_hh_baseline_eval.py
│   ├── run_hh_tradeoff_pipeline.py
│   ├── run_integrity_all_hh.py
│   ├── build_tradeoff_tables.py
│   ├── analyze_detox_integrity.py
│   ├── score_detoxify.py
│   └── score_integrity_hh.py
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

**Integrity / tradeoff evaluation (HH):** metric definitions, subsets, and toxicity-vs-integrity reporting are in [`docs/integrity_evaluation_plan.md`](docs/integrity_evaluation_plan.md).

**Week 1 work log** (define helpfulness retention, refusal rate, semantic consistency; plan toxicity vs integrity framework): [`logs/week1_integrity_framework_metrics_work_log.md`](logs/week1_integrity_framework_metrics_work_log.md).

**Week 3 work log** (integrity across all methods + tradeoff tables): [`logs/week3_integrity_all_methods_tradeoff_work_log.md`](logs/week3_integrity_all_methods_tradeoff_work_log.md).

**Week 4 work log** (detox vs integrity analysis + qualitative examples): [`logs/week4_integrity_qualitative_work_log.md`](logs/week4_integrity_qualitative_work_log.md).

---

## Notes

This project uses a **scaled-down experimental design** so the full pipeline can run on a personal computer while still reproducing core research behavior.

Raw datasets are not included due to file size limits.

Download from:
- RealToxicityPrompts – Allen Institute for AI / Hugging Face  
- Anthropic Helpful-Harmless – Hugging Face  
