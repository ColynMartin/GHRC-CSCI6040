# Week 5 work log: synthesis and presentation

**Milestone:** Final analyses, communicate **tradeoff** findings (toxicity vs helpfulness / integrity), and state **final integrity conclusions** for Hypothesis 3 (detox / personality prompting vs helpfulness).

**Last updated:** 2026-04-07  
**Owner:** Heather Bowman  

---

## 1. Prerequisites (Weeks 1–4)

| Week | Log | What you need for Week 5 |
|------|-----|---------------------------|
| 1 | [`week1_integrity_framework_metrics_work_log.md`](week1_integrity_framework_metrics_work_log.md) | Vocabulary: helpfulness retention, refusal, semantic consistency; toxicity vs integrity framework ([`docs/integrity_evaluation_plan.md`](../docs/integrity_evaluation_plan.md)). |
| 2 | [`week2_hh_baseline_helpfulness_validation_work_log.md`](week2_hh_baseline_helpfulness_validation_work_log.md) | Baseline HH generations + pre-detox integrity metrics + validation narrative. |
| 3 | [`week3_integrity_all_methods_tradeoff_work_log.md`](week3_integrity_all_methods_tradeoff_work_log.md) | `hh_tradeoff_summary.csv` / `.md` — per-condition toxicity, Jaccard, refusal. |
| 4 | [`week4_integrity_qualitative_work_log.md`](week4_integrity_qualitative_work_log.md) | `detox_integrity_analysis.*`, `qualitative_examples.md` — deltas vs baseline, win–win vs tradeoff, excerpts. |

If any file is missing, re-run the commands in the corresponding week log before finalizing slides or the report.

---

## 2. Goals (Week 5)

### 2.1 Final analyses

- **Integrate** Week 3 tradeoff table with Week 4 detox-vs-baseline aggregates: which personality conditions move toxicity and helpfulness together vs in opposition?
- **Ground numbers** with 2–3 **qualitative** blocks from `qualitative_examples.md` (cite `prompt_id` / condition).
- **State limits:** token Jaccard proxy, rule-based refusal, small `n_samples`, model size — align conclusions with [`docs/detox_integrity_analysis_guide.md`](../docs/detox_integrity_analysis_guide.md).

### 2.2 Communicate tradeoff analysis

- **One primary figure** (recommended): mean Detoxify toxicity (x or y) vs mean helpfulness Jaccard (y or x) **per condition**, or bar chart with error bars if you bootstrap or subset.
- **Stratify** if you defined benign vs harmful subsets (per integrity plan): avoid one aggregate story that hides over-refusal on benign prompts.
- **Verbal frame:** “lower toxicity with retained helpfulness” vs “toxicity down but integrity / alignment to HH `chosen` drops” (tradeoff).

### 2.3 Final integrity conclusions

- **Answer** the Hypothesis 3–style question: Do HEXACO / “detox-oriented” personality prompts **preserve** integrity (vs `reference_reply` and vs baseline) while changing toxicity?
- **Bullet 3–5 takeaways** for the audience (what you’d put on a summary slide).
- **Honest caveats:** what you did **not** measure (e.g. full embedding semantic consistency across all conditions if still using Jaccard only).

---

## 3. Suggested deliverables checklist

- [ ] **Slide deck** or report section: methods one-pager, tradeoff figure, qualitative example slide, conclusions + limitations.  
- [ ] **Spoken narrative** (2–3 min): walk through one tradeoff example and one “win–win” or “integrity preserved” example if present in your numbers.  
- [ ] **Upload** final PDF / slides and any **frozen** CSV exports to OneDrive **`week5/`** (e.g. `week5/analysis/`, `week5/presentation/`) per README Data Storage.  
- [ ] **Append** [`logs/experiment_log.csv`](experiment_log.csv) rows for any **new** frozen files you share (e.g. `hh_tradeoff_summary_vfinal.csv`, `presentation_integrity_h3_v1.pdf`) with date and short note.  

---

## 4. Primary files to cite in the presentation

| Artifact | Role in story |
|----------|----------------|
| `outputs/hh_tradeoff_summary.md` (or `.csv`) | All-conditions toxicity vs helpfulness snapshot. |
| `outputs/detox_integrity_analysis.md` (or `.csv`) | Baseline-relative detox comparison, % tradeoff / win–win. |
| `outputs/qualitative_examples.md` | Human-readable evidence. |
| `configs/hh_all_conditions.yaml`, `configs/detox_conditions.yaml` | Reproducibility footnote. |

---

## 5. Related documentation

- [`docs/integrity_evaluation_plan.md`](../docs/integrity_evaluation_plan.md) — definitions and framework.  
- [`docs/detox_integrity_analysis_guide.md`](../docs/detox_integrity_analysis_guide.md) — how to read aggregates and qualitative buckets.  

---

## 6. No new pipeline command required

Week 5 is **synthesis**: unless you re-run experiments for a final sweep, you do not need a new `src/*.py` entrypoint. If you regenerate all HH outputs, follow [`week3_integrity_all_methods_tradeoff_work_log.md`](week3_integrity_all_methods_tradeoff_work_log.md) and [`week4_integrity_qualitative_work_log.md`](week4_integrity_qualitative_work_log.md) first, then return here.
