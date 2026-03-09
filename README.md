# LLM Personality Detoxification Project

A scaled-down reproduction of a research study investigating how **HEXACO-based personality prompts** influence **toxicity in large language model outputs**.

---

## Quick Start

Activate the environment:

```
venv\Scripts\activate
```

Run text generation:

```
python src/run_generation.py
```

Score toxicity:

```
python src/score_detoxify.py
```

Results will be saved in the `outputs/` folder.

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
