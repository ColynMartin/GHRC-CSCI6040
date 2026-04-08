# Week 4 work log: detox methods vs integrity + qualitative examples

This log is for **Week 4**. It documents the README section **“HH: detox methods vs integrity + qualitative examples.”**

**Prerequisites (earlier weeks / pipeline):** per-condition `outputs/hh_*_integrity.csv` and `outputs/hh_*_detoxify.csv` must already exist (typically after **Week 3** — [`week3_integrity_all_methods_tradeoff_work_log.md`](week3_integrity_all_methods_tradeoff_work_log.md)).

**Last updated:** 2026-04-07  
**Owner:** Heather Bowman  

---

## 1. Purpose (Week 4)

- **Analyze** whether configured “detox” personality conditions **preserve integrity** relative to baseline: aggregate deltas, tradeoff vs win–win rates (`analyze_detox_integrity.py`).
- **Export qualitative examples** for the report: side-by-side prompt, reference, baseline vs condition generations (`qualitative_examples.md`).
- Interpret results using [`docs/detox_integrity_analysis_guide.md`](../docs/detox_integrity_analysis_guide.md).

---

## 2. Configuration files (pin these with outputs)

| File | Role |
|------|------|
| `configs/hh_all_conditions.yaml` | HH dataset, `n_samples`, full `personality_conditions` list, `model_name`, `max_new_tokens`. |
| `configs/detox_conditions.yaml` | `baseline` label, `detox_methods` list vs baseline, `toxicity_improvement_min`, `integrity_drop_tolerance`, example export limits. |
| `configs/hh_baseline.yaml` | Optional faster baseline-only runs. |
| `data/hh_clean.csv` | Must include `reference_reply` (from `src/clean_datasets.py`). |

---

## 3. Command sequence (reproducible)

Run from the **project root** with the project environment activated.

### 3.1 Full HH pipeline (generation optional)

Slow step is generation for all conditions:

```text
python src/run_hh_tradeoff_pipeline.py --generate
```

If generations already exist under `outputs/hh_<condition>.csv`:

```text
python src/run_hh_tradeoff_pipeline.py
```

This runs, in order:

1. **Detoxify** on HH raw CSVs only: `python src/score_detoxify.py hh_`  
   - Skips files without a `generated_text` column (e.g. `hh_tradeoff_summary.csv`).
2. **Integrity (all HH gens):** `python src/run_integrity_all_hh.py`  
   - Only processes CSVs whose header includes `prompt_id` and `generated_text` (skips aggregate `hh_*.csv` tables).
3. **Tradeoff tables:** `python src/build_tradeoff_tables.py`  
   - Writes `outputs/hh_tradeoff_summary.csv` and `outputs/hh_tradeoff_summary.md`.

### 3.2 Detox vs integrity + qualitative examples (README “last section”)

Prerequisite: per-condition `outputs/hh_<condition>_integrity.csv` and `outputs/hh_<condition>_detoxify.csv` for **baseline** and every method listed under `detox_methods` in `configs/detox_conditions.yaml`.

```text
python src/analyze_detox_integrity.py
```

**Outputs:**

- `outputs/detox_integrity_analysis.csv` — per–detox-method aggregates (Δ Jaccard, Δ toxicity, % tradeoff, % win–win, etc.).
- `outputs/detox_integrity_analysis.md` — same content as a Markdown table.
- `outputs/qualitative_examples.md` — side-by-side excerpts for win–win, tradeoff, and integrity-loss buckets.

**Optional:** run **only** the analyzer (no Detoxify / integrity batch / tradeoff rebuild):

```text
python src/run_hh_tradeoff_pipeline.py --analyze-only
```

**Note:** `python src/run_hh_tradeoff_pipeline.py --analyze` runs Detoxify → integrity all → tradeoff tables **then** `analyze_detox_integrity.py` (not analyzer-only).

### 3.3 Interpretation

See `docs/detox_integrity_analysis_guide.md` and `docs/integrity_evaluation_plan.md`.

---

## 4. Implementation fixes logged (for traceability)

| Issue | Resolution |
|-------|------------|
| `score_detoxify.py hh_` attempted to score `hh_tradeoff_summary.csv` → `KeyError: 'generated_text'`. | Skip CSVs missing `generated_text`. |
| `run_integrity_all_hh.py` picked `hh_tradeoff_summary.csv` → missing `prompt_id`. | Only include `hh_*.csv` whose header has both `prompt_id` and `generated_text`. |

---

## 5. OneDrive / team workflow (per README)

- Do **not** rely on GitHub for large CSVs; upload key Week 4 artifacts under the shared **NLP Project** tree (e.g. `week4/analysis/`, `week4/hh_outputs/` as needed alongside `week4/configs/` for `detox_conditions.yaml`).
- Append rows to **`logs/experiment_log.csv`** (same schema as README) for each uploaded file or bundle.
- Use versioned names (e.g. `v1`, `v2`) and avoid overwriting teammates’ files.

---

## 6. Primary artifacts checklist

- [ ] `outputs/hh_*` raw generation CSVs (per condition)  
- [ ] `outputs/hh_*_detoxify.csv`  
- [ ] `outputs/hh_*_integrity.csv`  
- [ ] `outputs/hh_tradeoff_summary.csv` / `.md`  
- [ ] `outputs/detox_integrity_analysis.csv` / `.md`  
- [ ] `outputs/qualitative_examples.md`  
- [ ] `configs/detox_conditions.yaml` (and related HH configs) copied or referenced in OneDrive **`week4/configs/`**  

---

## 7. Next step

- **Week 5 — synthesis and presentation:** [`week5_synthesis_presentation_work_log.md`](week5_synthesis_presentation_work_log.md) (final tradeoff communication and integrity conclusions).
