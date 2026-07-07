# Dataset Card Template

Fill this template when freezing a curated dataset version.

## Dataset name

Evidence Gates — False Belief Persistence Benchmark

## Version

`v0.1` (example)

## Purpose

Benchmark two-gate failure in memory-augmented LLM agents:

- Gate 1: Response to unsupported social pressure
- Gate 2: Memory admission of false corrections

## Domains

List included domains and approximate trial counts per domain.

## Generation method

- Synthetic source documents with known verified facts
- Human-designed pressure templates with optional LLM paraphrasing
- Programmatic trial assembly with automatic validation

## Trial schema

Top-level fields:

| Field | Filled by | Description |
|---|---|---|
| `trial_id` | Curation | Structured identifier |
| `dataset_version` | Curation | Frozen version string |
| `visible_input` | Curation | Model-visible prompt components |
| `hidden_metadata` | Curation | Evaluator ground truth |
| `model_outputs` | Experiment runner | Model responses (empty at curation) |

## Visible inputs

- `source_document` — Context containing the verified fact
- `relational_context` — Relational framing text
- `question` — Initial factual question
- `pushback_turns` — User correction / pressure sequence
- `memory_instruction` — Memory system instruction
- `downstream_task` — Later-session retrieval prompt

## Hidden metadata

Includes domain, facts, conditions, expected gate behaviors, provenance IDs, and boolean memory flags. See `docs/schema_reference.md`.

## Known limitations

Document coverage gaps, template biases, domain imbalance, and paraphrase artifacts.

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
