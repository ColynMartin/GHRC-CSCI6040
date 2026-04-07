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

### HH: integrity across all methods + toxicity vs helpfulness tables

1. Generate for **every** personality condition using `configs/hh_all_conditions.yaml` (or use the bundled pipeline below).
2. **Integrity on all HH runs:** `python src/run_integrity_all_hh.py` — scores every `outputs/hh_<condition>.csv` (skips `*_detoxify*` and `*_integrity*`).
3. **Detoxify on HH generations:** `python src/score_detoxify.py hh_` — optional `hh_` prefix limits scoring to files starting with `hh_` (omit the argument to score all raw output CSVs as before).
4. **Tradeoff tables:** `python src/build_tradeoff_tables.py` — writes `outputs/hh_tradeoff_summary.csv` and `outputs/hh_tradeoff_summary.md` (mean toxicity, mean/median helpfulness Jaccard, refusal rate per condition).

One-shot (add `--generate` to include the slow generation step):

```
python src/run_hh_tradeoff_pipeline.py --generate
```

---

## Project Structure

```
llm-personality-project
│
├── configs
│   ├── base.yaml
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

## Team Roles

| Role | Responsibility |
|-----|-----|
| Rebecca Rickard | Infrastructure and experiment pipeline |
| Colyn Martin | Hypothesis 1 – toxic regions across prompts |
| Gaurav Goyal | Hypothesis 2 – token vs sequence penalties |
| Heather Bowman | Hypothesis 3 – detoxification vs helpfulness |

**Integrity / tradeoff evaluation (HH):** metric definitions, subsets, and toxicity-vs-integrity reporting are in [`docs/integrity_evaluation_plan.md`](docs/integrity_evaluation_plan.md).

---

## Notes

This project uses a **scaled-down experimental design** so the full pipeline can run on a personal computer while still reproducing the core methodology of the original research study.

Raw datasets are not included in this repository due to file size limits.  
They can be downloaded from:
- RealToxicityPrompts: Allen Institute for AI / Hugging Face
- Anthropic Helpful-Harmless: Hugging Face
