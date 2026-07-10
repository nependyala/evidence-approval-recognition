# Flowcharts

Mermaid flowcharts for the SycEval-augmented two-gate study pipeline. These are schematic overviews aligned with the **SycEval Augmentation Plan for the Two-Gate Study** (source of truth for data curation).

| File | Topic |
|------|-------|
| [01-trial-construction.md](01-trial-construction.md) | Ingesting SycEval, normalizing items, assigning independent pressure factors, and freezing trials |
| [02-trial-record-structure.md](02-trial-record-structure.md) | `base_item`, `experimental_factors`, `visible_input`, `hidden_metadata`, `model_outputs`, `evaluation` |
| [03-grading-pipeline.md](03-grading-pipeline.md) | Answer-state extraction, Gate 1 labels, Gate 2 memory admission, downstream contamination |

These render in GitHub, many IDEs, and any Mermaid-compatible viewers.

## Alignment with the augmentation plan

- **Construction (01):** Follows the 7-step dataset construction procedure (ingest → subset → normalize → validate → templates → evidence controls → validate templates). Uses in-context trials with frozen `canonical_initial_turn`.
- **Record structure (02):** Matches the augmented item schema and run-sequence logging fields. Separates model factual-commitment JSON from grader-derived labels.
- **Grading (03):** Uses Gate 1 labels (`hold`, `cave`, `elicitation_non_cave`, `rational_revision`, `stubborn`, `ambiguous`), Gate 2 memory-admission labels, and evidence-aware downstream contamination rules.

See `docs/schema_reference.md` for the full trial JSON schema and `data/fixtures/example_trial.json` for a synthetic sample.
