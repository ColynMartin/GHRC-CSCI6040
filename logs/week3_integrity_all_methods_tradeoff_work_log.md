# Week 3 work log: integrity across all methods + toxicity vs helpfulness tradeoff tables

This log is for **Week 3**. It matches the README section **“HH: integrity across all methods + toxicity vs helpfulness tables”**: measuring **integrity metrics** for every HH personality condition, then building **per-condition** summaries that pair **Detoxify toxicity** with **helpfulness** (token Jaccard vs `reference_reply`) and **refusal** rates.

**Last updated:** 2026-04-07  
**Owner:** Heather Bowman  

**Prerequisite:** Week 2 HH baseline + pre-detox helpfulness + metric validation is documented in [`week2_hh_baseline_helpfulness_validation_work_log.md`](week2_hh_baseline_helpfulness_validation_work_log.md).

---

## 1. Objectives (Week 3)

- Run (or reuse) **HH generations** for **each** personality condition in `configs/hh_all_conditions.yaml`.
- Compute **integrity** on every raw `outputs/hh_<condition>.csv`: `helpfulness_token_jaccard`, `refusal_rule_based`, plus merged `reference_reply` from `data/hh_clean.csv`.
- Score **toxicity** (Detoxify) on the same generations.
- Produce **tradeoff tables**: one row per condition with mean toxicity, mean/median Jaccard, refusal rate — for plots and narrative on toxicity vs helpfulness.

---

## 2. Configuration to archive with results

| File | Purpose |
|------|---------|
| `configs/hh_all_conditions.yaml` | `model_name`, `dataset_file` (`data/hh_clean.csv`), `n_samples`, `personality_conditions`, `max_new_tokens`, etc. |
| `data/hh_clean.csv` | Must include `prompt_id`, `prompt_text`, `reference_reply` (from `src/clean_datasets.py`). |

---

## 3. Commands (project root)

### Option A — one-shot pipeline

Includes optional **generation** (slow):

```text
python src/run_hh_tradeoff_pipeline.py --generate
```

If `outputs/hh_<condition>.csv` files already exist for all conditions:

```text
python src/run_hh_tradeoff_pipeline.py
```

This invokes, in order:

1. `python src/score_detoxify.py hh_` — Detoxify on each `hh_*.csv` that has `generated_text` (skips aggregate tables such as `hh_tradeoff_summary.csv`).
2. `python src/run_integrity_all_hh.py` — integrity scoring on each raw HH generation file (skips `*detoxify*`, `*integrity*`, and any `hh_*.csv` missing `prompt_id` / `generated_text`).
3. `python src/build_tradeoff_tables.py` — builds summary tables from `outputs/hh_*_integrity.csv` + matching `hh_*_detoxify.csv`.

### Option B — step-by-step (same outcome)

```text
python src/run_generation.py configs/hh_all_conditions.yaml
python src/score_detoxify.py hh_
python src/run_integrity_all_hh.py
python src/build_tradeoff_tables.py
```

---

## 4. Primary outputs

| Path | Description |
|------|-------------|
| `outputs/hh_<condition>.csv` | Raw generations per personality condition. |
| `outputs/hh_<condition>_detoxify.csv` | Same rows + `detoxify_toxicity`. |
| `outputs/hh_<condition>_integrity.csv` | Same + `reference_reply`, `helpfulness_token_jaccard`, `refusal_rule_based`. |
| `outputs/hh_tradeoff_summary.csv` | Machine-readable table: one row per condition. |
| `outputs/hh_tradeoff_summary.md` | Markdown table for slides or report. |

**Metrics in the tradeoff summary**

- `mean_detoxify_toxicity` — merged on `prompt_id` from each condition’s Detoxify file.
- `mean_helpfulness_token_jaccard` / `median_helpfulness_token_jaccard` — from integrity file.
- `refusal_rate_rule_based` — fraction of rule-based refusals in that condition.

---

## 5. Implementation notes (robustness)

- **`score_detoxify.py`:** CSVs without `generated_text` are skipped (avoids scoring `hh_tradeoff_summary.csv` when using prefix `hh_`).
- **`run_integrity_all_hh.py`:** Only files whose header includes both `prompt_id` and `generated_text` are processed (avoids summary CSVs).

---

## 6. OneDrive / team (README Data Storage)

- Upload primary CSV/MD outputs and a copy of `configs/hh_all_conditions.yaml` under **`week3/`** (e.g. `week3/hh_outputs/`, `week3/detox_scores/`, `week3/analysis/`, `week3/configs/`).
- Append rows to [`logs/experiment_log.csv`](experiment_log.csv) for `hh_tradeoff_summary.csv` and `hh_tradeoff_summary.md` (and optionally versioned copies).
- Do not commit large `outputs/*.csv` to Git if the team policy is OneDrive-only for artifacts.

---

## 7. Related docs

- [`docs/integrity_evaluation_plan.md`](../docs/integrity_evaluation_plan.md) — metric definitions and framework.
- [`logs/week4_integrity_qualitative_work_log.md`](week4_integrity_qualitative_work_log.md) — **Week 4** downstream **detox vs baseline** analysis and qualitative examples (separate README section).
- [`logs/week5_synthesis_presentation_work_log.md`](week5_synthesis_presentation_work_log.md) — **Week 5** synthesis and presentation after Week 4.
