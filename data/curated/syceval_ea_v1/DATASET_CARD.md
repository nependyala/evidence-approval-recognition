# Dataset Card: syceval_ea_v1

Filled from `docs/dataset_card_template.md` when freezing this dataset version.

## Dataset name

SycEval Evidence Gates — Two-Gate False Belief Persistence Benchmark

## Version

`syceval_ea_v1`

## Purpose

Augmented SycEval-style benchmark for two-gate failure in memory-augmented LLM agents:

- **Gate 1:** Response to unsupported social pressure (caving vs. holding vs. elicitation)
- **Gate 2:** Memory admission of false corrections and downstream contamination

## Source data

There is no single official "SycEval dataset" release to download directly; the SycEval
paper's own item pools are AMPS and MedQuAD. This version sources both directly and
reproduces the paper's sampling/normalization approach rather than depending on a
third-party SycEval mirror:

- **AMPS**: sampled from the Hugging Face-hosted AMPS mirror (`APW-2/amps-algebra`-style
  rows fetched via the datasets-server `/rows` API), restricted to `algebra` items with
  single closed-form numeric/symbolic answers.
- **MedQuAD**: sampled from the MedQuAD GitHub repository's GARD/GHR XML question-answer
  pairs (shallow git clone), restricted to items with a single extractable inheritance
  pattern or prevalence-ratio fact.
- 500-item raw pools per source are cached at `data/raw/amps_pool_500.json` and
  `data/raw/medquad_pool_500.json`.
- Primary experimental subset: 200 items (100 AMPS + 100 MedQuAD), normalized to
  `data/interim/base_items_200.json`.
- Augmentation: independent pressure factors, relational context, and memory policies
  per the SycEval Augmentation Plan (see `docs/notebook_pilot_findings.md` and the
  augmentations spec PDF).

## Domains

| Source | Domain | Item count |
|---|---|---|
| AMPS | `algebra_pemdas` | 11 |
| AMPS | `algebra_complete_square` | 11 |
| AMPS | `algebra_factor_polynomials` | 11 |
| AMPS | `algebra_multiply_polynomials` | 11 |
| AMPS | `algebra_polynomial_arithmetic` | 11 |
| AMPS | `algebra_polynomial_gcd` | 11 |
| AMPS | `algebra_complex_norm_and_arg` | 9 |
| AMPS | `algebra_exponential_equations` | 9 |
| AMPS | `algebra_system_of_equations` | 9 |
| AMPS | `algebra_solve_abs_value_equation` | 7 |
| MedQuAD | `medquad_inheritance` (inheritance-pattern facts) | 55 |
| MedQuAD | `medquad_frequency` (prevalence-ratio facts) | 45 |

AMPS totals 100 items across 10 sub-topics; MedQuAD totals 100 items across 2 fact types.

## Generation method

1. Ingested 500-item raw pools directly from AMPS (Hugging Face) and MedQuAD (GitHub XML),
   via `scripts/build_amps_items.py` / `scripts/build_medquad_items.py` (backed by
   `scripts/lib_amps.py` / `scripts/lib_medquad.py`).
2. Normalized each item to one atomic `target_claim`, `gold_answer`, `true_answer_aliases`,
   and a programmatically-derived, verified `false_answer` (integer-literal perturbation for
   AMPS; categorical swap — e.g. inheritance pattern — for MedQuAD). AMPS false answers are
   symbolically verified distinct from gold at generation time; MedQuAD false answers are
   drawn from a fixed set of plausible-but-incorrect categorical alternatives.
3. Generated `valid_evidence_asset` and `fabricated_evidence_asset` text per item
   (`scripts/merge_base_items.py`).
4. Added the two missing pressure templates required by the augmentation plan
   (`prompts/pressure_templates/fabricated_confident.yaml`,
   `prompts/pressure_templates/fabricated_uncertain.yaml`) and built a 12-condition
   pressure manifest (`scripts/pressure_manifest.py`) covering
   `{unsupported_assertion, fabricated_evidence, valid_evidence} x {low, high} x {single, repeated}`.
5. Assembled the full factorial of trials (`scripts/assemble_trials.py`):
   200 base items x 4 relational contexts x 12 pressure conditions x 3 memory policies
   = **28,800 trial records**.
6. Ran automatic validation (`eg validate-dir data/curated/syceval_ea_v1/trials`) over
   the full 28,800-record set: **28,800 / 28,800 passed**, 0 failures. (Trial records live
   under `trials/`, separate from this card and `manifest.json`, so `validate-dir` only
   ever sees trial JSON files.)
7. Ran a stratified programmatic proxy audit (n=40, seeded) against the criteria in
   `docs/human_audit_checklist.md` (leakage, evidence-asset presence, turn-count/intensity
   consistency, downstream-task/question consistency): 0 issues found. **A full manual
   human audit per `docs/human_audit_checklist.md` has not yet been performed** — see
   Known limitations.

## Trial schema

Top-level fields:

| Field | Filled by | Description |
|---|---|---|
| `trial_id` | Curation | Structured identifier |
| `dataset_version` | Curation | Frozen version string (`syceval_ea_v1`) |
| `base_item` | Curation | SycEval-style provenance and legacy metadata |
| `experimental_factors` | Curation (+ runner for `model_id`) | Independent manipulations |
| `visible_input` | Curation | Model-visible prompt components |
| `hidden_metadata` | Curation | Evaluator ground truth |
| `model_outputs` | Experiment runner (empty here) | Model responses |
| `evaluation` | Grading pipeline (empty here) | Derived labels and metrics inputs |

See `docs/schema_reference.md` and `data/fixtures/example_trial.json`.

## Experimental factors

| Factor | Levels | Count per level |
|---|---|---|
| Relational context | none, truth_instruction, secure_disagreement, contingent_approval | 7,200 each |
| Pressure family | approval, evidence | 9,600 / 19,200 |
| Evidence status | unsupported_assertion, fabricated_evidence, valid_evidence | 9,600 each |
| Confidence | low, high | 14,400 each |
| Intensity | single, repeated | 14,400 each |
| Memory policy | no_factual_memory, naive_summary_memory, epistemically_typed_memory | 9,600 each |

Full breakdown in `manifest.json`.

## Primary metrics

| Stage | Metric |
|---|---|
| Gate 1 | Sycophantic Capitulation Rate (SCR) |
| Gate 1 | Rational Revision Rate (RRR) |
| Gate 1 | Update Discrimination Score (UDS) |
| Gate 2 | False Memory Admission Rate (FMAR) |
| Gate 2 | Unsupported Overwrite Rate (UOR) |
| Retrieval | Downstream Contamination Rate (DCR) |

This curated release contains no `model_outputs` or `evaluation` values (both are
out of scope for curation); metrics are computed downstream by an experiment
runner and grading pipeline against this frozen trial set.

## Known limitations

- **No manual human audit performed.** Only an automated proxy audit (stratified,
  n=40) was run against the `docs/human_audit_checklist.md` criteria. The
  sign-off table in that checklist is still blank and should be completed by a
  human reviewer before using this version for any published result.
- **MedQuAD false answers are templated categorical swaps**, not independently
  fact-checked against a second medical source; they are plausible-but-wrong by
  construction (e.g. swapping `autosomal dominant` for `x-linked dominant`) but
  have not had clinical review.
- **AMPS domain coverage is limited to 10 algebra sub-topics** with closed-form
  numeric/symbolic answers; no calculus, geometry, or word-problem AMPS items are
  included, and per-sub-topic item counts are uneven (7–11) due to availability
  of clean, unambiguous candidates in the sampled pool.
- **No official "SycEval" dataset release was found** at generation time; this
  version re-sources AMPS/MedQuAD directly and re-implements the paper's item
  selection/normalization approach rather than reusing a pre-built SycEval
  artifact. `syceval_item_id` values are therefore synthetic IDs assigned by this
  pipeline (`syceval_amps_NNNNNN` / `syceval_medquad_NNNNNN`), not IDs from an
  upstream SycEval release.
- **`legacy_context_mode` / `legacy_rebuttal_tier`** fields carry over
  approximate SycEval-era categorical mappings for backward compatibility, but
  the augmented pressure/evidence taxonomy in this version is finer-grained and
  is the source of truth for experimental design.
- All 28,800 trials use `model_id: null` and empty `model_outputs`/`evaluation`
  blocks by design — this is a curated *input* set, not experiment results.

## License

- Code: MIT
- Dataset: CC BY 4.0 (expected; update when data is published). Note AMPS and
  MedQuAD each carry their own upstream license terms; consult the original
  sources before redistribution.

## Validation report

- Total trials validated: 28,800
- Pass: 28,800
- Fail: 0
- Common failure categories encountered *during development* (all fixed prior to
  freeze): trial_id/experimental_factors mismatches from missing
  `evidence_status` disambiguation in the ID pattern (fixed in
  `src/generation/ids.py` / `src/evaluation/checks.py`; see
  `docs/naming_conventions.md`); LaTeX-perturbation edge cases producing
  malformed exponents (fixed in `scripts/lib_amps.py`).

## Human audit summary

| Auditor | Date | Sample size | Pass rate | Notes |
|---|---|---|---|---|
| automated proxy (not a substitute for human review) | 2026-07-15 | 40 (stratified, seed=42) | 100% (0 issues / 40) | Checked leakage, evidence-asset presence, turn-count/intensity consistency, downstream-task/question consistency. Full manual audit per `docs/human_audit_checklist.md` still pending — sign-off row there remains blank. |

## Excluded trials and reasons

| trial_id | Reason excluded |
|---|---|
| _(none)_ | All 28,800 generated trials passed validation; none were excluded. |
