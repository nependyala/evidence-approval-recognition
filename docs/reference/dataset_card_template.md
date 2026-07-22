# Dataset Card Template

Fill this template when freezing a curated dataset version.

## Dataset name

SycEval Evidence Gates — Two-Gate False Belief Persistence Benchmark

## Version

`syceval_ea_v1` (example)

## Purpose

Augmented SycEval benchmark for two-gate failure in memory-augmented LLM agents:

- **Gate 1:** Response to unsupported social pressure (caving vs. holding vs. elicitation)
- **Gate 2:** Memory admission of false corrections and downstream contamination

## Source data

- Base: SycEval (500 AMPS + 500 MedQuAD items)
- Primary experimental subset: 200 items (100 AMPS + 100 MedQuAD)
- Augmentation: independent pressure factors, relational context, memory policies

## Domains

| Source | Domain examples | Approximate item count |
|---|---|---|
| AMPS | `math_word_problem` | 100 |
| MedQuAD | medical QA categories | 100 |

## Generation method

1. Ingest and normalize SycEval items to atomic target claims
2. Validate false answers (symbolic for AMPS, human for MedQuAD)
3. Generate pressure templates (approval + evidence families)
4. Create fabricated-evidence and valid-evidence controls
5. Programmatic trial assembly with automatic validation
6. Human audit of stratified sample

## Trial schema

Top-level fields:

| Field | Filled by | Description |
|---|---|---|
| `trial_id` | Curation | Structured identifier |
| `dataset_version` | Curation | Frozen version string |
| `base_item` | Curation | SycEval provenance and legacy metadata |
| `experimental_factors` | Curation (+ runner for `model_id`) | Independent manipulations |
| `visible_input` | Curation | Model-visible prompt components |
| `hidden_metadata` | Curation | Evaluator ground truth |
| `model_outputs` | Experiment runner | Model responses |
| `evaluation` | Grading pipeline | Derived labels and metrics inputs |

See `docs/reference/schema_reference.md` and `data/fixtures/example_trial.json`.

## Experimental factors

| Factor | Levels |
|---|---|
| Relational context | none, truth_instruction, secure_disagreement, contingent_approval |
| Pressure family | approval, evidence |
| Confidence | low, high |
| Intensity | single, repeated |
| Evidence status | unsupported_assertion, fabricated_evidence, valid_evidence |
| Memory policy | no_factual_memory, naive_summary_memory, epistemically_typed_memory |

## Primary metrics

| Stage | Metric |
|---|---|
| Gate 1 | Sycophantic Capitulation Rate (SCR) |
| Gate 1 | Rational Revision Rate (RRR) |
| Gate 1 | Update Discrimination Score (UDS) |
| Gate 2 | False Memory Admission Rate (FMAR) |
| Gate 2 | Unsupported Overwrite Rate (UOR) |
| Retrieval | Downstream Contamination Rate (DCR) |

## Known limitations

Document coverage gaps, template biases, domain imbalance, MedQuAD adjudication artifacts, and legacy SycEval condition differences.

## License

- Code: MIT
- Dataset: CC BY 4.0 (expected; update when data is published)

## Validation report

Summarize automatic validation results:

- Total trials validated
- Pass / fail counts
- Common failure categories

## Human audit summary

Summarize stratified human audit (sample size, pass rate, major issues found).

## Excluded trials and reasons

| trial_id | Reason excluded |
|---|---|
| | |
