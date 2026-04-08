# Week 2 work log: HH baseline, helpfulness before detox, metric validation

This log documents the **Week 2** milestone aligned with the README subsection **“HH baseline: helpfulness before Detoxify”** and the three deliverables:

1. **Run HH prompts through baseline** — generate completions under the baseline personality condition only.  
2. **Measure helpfulness before detox** — score integrity **before** Detoxify (helpfulness proxy + refusal heuristic vs HH `reference_reply`).  
3. **Validate evaluation metrics** — review the printed validation block (coverage, ranges, refusal rate sanity checks).

**Last updated:** 2026-04-07  
**Owner:** Heather Bowman  

**Prerequisite:** Week 1 metric definitions and toxicity-vs-integrity framework: [`week1_integrity_framework_metrics_work_log.md`](week1_integrity_framework_metrics_work_log.md) and [`docs/integrity_evaluation_plan.md`](../docs/integrity_evaluation_plan.md).

---

## 1. Prerequisites

| Requirement | Notes |
|-------------|--------|
| `data/hh_clean.csv` with **`reference_reply`** | Produced by `src/clean_datasets.py` from `data/hh_full.csv`. Without `reference_reply`, `score_integrity_hh.py` exits with an error. |
| Model + dependencies | Same as main pipeline (`requirements.txt`); `configs/hh_baseline.yaml` defaults to `distilgpt2`. |
| Project environment | Activate venv or Conda (see README Quick Start). |

---

## 2. Configuration to save with Week 2 outputs

| File | Role |
|------|------|
| `configs/hh_baseline.yaml` | HH dataset path, `personality_conditions: [baseline]`, `n_samples`, `max_new_tokens`, `model_name`. |

Copy this YAML into OneDrive **`week2/configs/`** (or your team’s naming) next to the outputs you upload.

---

## 3. Commands (project root)

### One command (generation + integrity, no Detoxify)

```text
python src/run_hh_baseline_eval.py
```

This runs:

1. `python src/run_generation.py configs/hh_baseline.yaml`  
   - Writes **`outputs/hh_baseline.csv`** (columns include `prompt_id`, `prompt_text`, `generated_text`, `personality_condition`, etc.).

2. For each condition in the config (default: **baseline** only), `python src/score_integrity_hh.py outputs/hh_<condition>.csv`  
   - Writes **`outputs/hh_baseline_integrity.csv`** (adds `reference_reply`, `helpfulness_token_jaccard`, `refusal_rule_based`).  
   - Prints **metric validation** to the terminal (see §4).

### Equivalent manual steps

```text
python src/run_generation.py configs/hh_baseline.yaml
python src/score_integrity_hh.py outputs/hh_baseline.csv
```

### Optional: toxicity **after** Week 2 integrity pass

Detoxify is intentionally **not** part of the “before detox” helpfulness step. When you want toxicity on the same raw generations:

```text
python src/score_detoxify.py hh_
```

(Scores `hh_baseline.csv` among other `hh_*.csv` files; `*_integrity.csv` files are skipped.)

---

## 4. “Validate evaluation metrics” — what to check

After `score_integrity_hh.py` runs, the script prints a **Metric validation** section. Use it for Week 2 sign-off:

| Check | What to look for |
|-------|------------------|
| Row count | `Rows: N` should match `n_samples` from `hh_baseline.yaml` (unless generation failed on some rows). |
| Empty generations | `empty generated_text` — high counts may indicate pipeline or model issues; note in your report. |
| `reference_reply` coverage | `Empty reference_reply` should be **0** if `hh_clean.csv` was built with current `clean_datasets.py`. |
| `helpfulness_token_jaccard` | Values in **[0, 1]**; min/max/mean reported. Low absolute values are common for small LMs; focus on whether the metric is **finite** and the distribution is plausible. |
| Warnings | Script warns if >5% missing `reference_reply` or if Jaccard is out of range / NaN. |

**Helpfulness before detox:** at this stage, **only** `helpfulness_token_jaccard` and `refusal_rule_based` are computed on `generated_text` vs `reference_reply` — **no** `detoxify_toxicity` column until you run Detoxify separately.

---

## 5. Primary artifacts (Week 2)

| Path | Description |
|------|-------------|
| `outputs/hh_baseline.csv` | Baseline-only HH generations. |
| `outputs/hh_baseline_integrity.csv` | Same + reference + helpfulness Jaccard + refusal flags. |

Suggested OneDrive locations (per README Data Storage):

- `week2/hh_outputs/` — CSVs above  
- `week2/configs/` — copy of `hh_baseline.yaml`  
- `week2/logs/` — paste terminal validation output or reference this file  

---

## 6. `experiment_log.csv` rows

Add or keep rows in [`experiment_log.csv`](experiment_log.csv) for `hh_baseline.csv` and `hh_baseline_integrity.csv` (see appended entries). Use your actual run date and owner name if different.

---

## 7. Related documentation

- [`docs/integrity_evaluation_plan.md`](../docs/integrity_evaluation_plan.md) — definitions of helpfulness, refusal, consistency.  
- [`logs/week3_integrity_all_methods_tradeoff_work_log.md`](week3_integrity_all_methods_tradeoff_work_log.md) — **Week 3:** all personality conditions + tradeoff tables.  
