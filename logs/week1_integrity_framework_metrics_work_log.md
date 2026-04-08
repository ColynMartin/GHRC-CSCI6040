# Week 1 work log: integrity metrics (HH) and toxicity vs integrity framework

This log captures **Week 1** planning for **Hypothesis 3–style** evaluation on **Anthropic HH**: defining **integrity metrics** (helpfulness retention, refusal rate, semantic consistency) and the **toxicity vs integrity** evaluation framework. The canonical write-up is **[`docs/integrity_evaluation_plan.md`](../docs/integrity_evaluation_plan.md)**.

**Last updated:** 2026-04-07  
**Owner:** Heather Bowman  

---

## 1. Week 1 deliverables (mapped to goals)

| Goal | Where it is specified | § in `integrity_evaluation_plan.md` |
|------|------------------------|--------------------------------------|
| **Helpfulness retention** (vs HH `chosen` / `reference_reply`) | Operational definition; benign subset; report vs baseline | §2.1 |
| **Refusal rate** (calibrated harmful vs benign; vs reference refusal) | Definitions, subsets, alignment / over-refusal | §2.2 |
| **Semantic consistency** (cross-condition + reference-anchored) | Embedding-based formulation; variance across conditions | §2.3 |
| **Toxicity vs integrity framework** | Two axes, summary table, tradeoff plot, stratification | §3 |
| **Data + implementation bridge** | `reference_reply` in `hh_clean`; later scoring scripts | §1, §4, §5 |

---

## 2. Metric definitions (summary)

Details and formulas remain in the plan document; this log records the **intent** for Week 1 sign-off.

### 2.1 Helpfulness retention

- Compare generation \(g_{i,c}\) to human-preferred **`reference_reply`** \(r_i\) for the same `prompt_id`.
- **Planned primary:** embedding cosine similarity on a **benign** HH subset; report **relative to baseline** (delta or ratio), not only raw similarity.
- **Course-scale proxy (implemented later in code):** token-set **Jaccard** in `score_integrity_hh.py` as a lightweight stand-in until embeddings are added (see plan §4 dependencies).

### 2.2 Refusal rate

- **Harmful subset:** prompts where policy-safe behavior implies refusal; compare model **refusal** to a **reference refusal** indicator from `reference_reply` (same rules or labels).
- **Not** “higher refusal is always better”: track **appropriate alignment** on harmful prompts and **over-refusal** on benign prompts.
- **Implemented later:** phrase / keyword heuristic `refusal_rule_based` in `score_integrity_hh.py` (plan §2.2).

### 2.3 Semantic consistency

- **Cross-condition:** stability of answers for the **same** `prompt_id` across personality conditions (e.g. embedding spread or pairwise similarity).
- **Reference-anchored:** variance across conditions of similarity to \(r_i\) (large variance ⇒ unstable / integrity risk).
- **Implementation note:** full embedding pipeline optional for the course; cross-condition analysis appears in later tooling (e.g. `analyze_detox_integrity.py` for baseline-vs-method pairs). Broader multi-condition consistency can be added as a follow-up.

---

## 3. Toxicity vs integrity evaluation framework (plan)

From **§3** of the plan:

| Layer | Description |
|-------|-------------|
| **Toxicity axis** | `detoxify_toxicity` on `generated_text` (HH `*_detoxify.csv`), same family as RTP scoring. |
| **Integrity axis** | Helpfulness / refusal / (eventually) consistency metrics per condition and prompt. |
| **Joint reporting** | (1) Condition-level summary table, (2) tradeoff visualization (e.g. toxicity vs helpfulness), (3) **stratified** benign vs harmful so effects do not cancel in a single average. |
| **Hypothesis 3 anchor** | Link **reduced toxicity** to **helpfulness retention** and **refusal calibration** on HH. |

---

## 4. Primary artifact (Week 1)

| Path | Description |
|------|-------------|
| [`docs/integrity_evaluation_plan.md`](../docs/integrity_evaluation_plan.md) | Full definitions, subsets, framework, minimal success criteria, and pointers to later scripts. |

Optional for Week 1 folder on **OneDrive** (`week1/analysis/` or `week1/docs/`): export or snapshot this Markdown file and any slides that summarize §2–§3.

---

## 5. Traceability: plan → later implementation

| Plan concept | Repo implementation (later weeks) |
|--------------|-----------------------------------|
| `reference_reply` for HH | `src/clean_datasets.py` |
| Helpfulness (proxy) | `helpfulness_token_jaccard` in `src/score_integrity_hh.py` |
| Refusal (rule-based) | `refusal_rule_based` in `src/score_integrity_hh.py` |
| Metric validation output | `validate_integrity_metrics()` in `src/score_integrity_hh.py` |
| Per-condition toxicity + helpfulness table | `src/build_tradeoff_tables.py` → `hh_tradeoff_summary.*` |
| Baseline-first HH run | [`logs/week2_hh_baseline_helpfulness_validation_work_log.md`](week2_hh_baseline_helpfulness_validation_work_log.md) |
| All conditions + tradeoff (Week 3) | [`logs/week3_integrity_all_methods_tradeoff_work_log.md`](week3_integrity_all_methods_tradeoff_work_log.md) |
| Detox vs baseline + qualitative (Week 4) | [`logs/week4_integrity_qualitative_work_log.md`](week4_integrity_qualitative_work_log.md) |

---

## 6. `experiment_log.csv`

A row for the planning document is recorded in [`experiment_log.csv`](experiment_log.csv) (`file_name` = `docs/integrity_evaluation_plan.md` or basename as in other rows — use `integrity_evaluation_plan.md` for consistency with file-based tracking).

---

## 7. Next steps (post–Week 1)

- Confirm **benign** vs **harmful** HH subsets (even a small labeled list) for stratified reporting.
- Run **Week 2** baseline pipeline and validate metrics (see Week 2 log).
- Optionally add **embeddings** for helpfulness retention and semantic consistency per §2.1 and §2.3.
