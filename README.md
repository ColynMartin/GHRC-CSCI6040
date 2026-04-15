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

## Team Roles

| Role | Responsibility |
|-----|-----|
| Rebecca Rickard | Infrastructure and experiment pipeline |
| Colyn Martin | Hypothesis 1 – toxic regions across prompts |
| Gaurav Goyal | Hypothesis 2 – token vs sequence penalties |
| Heather Bowman | Hypothesis 3 – detoxification vs helpfulness |

---

## Notes

This project uses a **scaled-down experimental design** so the full pipeline can run on a personal computer while still reproducing the core methodology of the original research study.

Raw datasets are not included in this repository due to file size limits.  
They can be downloaded from:
- RealToxicityPrompts: Allen Institute for AI / Hugging Face
- Anthropic Helpful-Harmless: Hugging Face
