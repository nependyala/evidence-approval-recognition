# Flowcharts

Mermaid flowcharts for the Evidence/Approval/Recognition study pipeline. These are schematic overviews with no trial-specific examples.

| File | Topic |
|------|-------|
| [01-trial-construction.md](01-trial-construction.md) | Building a trial from a synthetic world through validation and dataset freeze |
| [02-trial-record-structure.md](02-trial-record-structure.md) | Visible input, hidden metadata, and model outputs; what the model reports vs what the grader derives |
| [03-grading-pipeline.md](03-grading-pipeline.md) | Answer-state extraction, evidence-aware Gate 1 labels, Gate 2 memory audit, downstream grading |

These render in GitHub, many IDEs, and any Mermaid-compatible viewer.

## Alignment with the grading spec

- **Construction (01):** Includes `relational_memory`, per-turn response JSON format, and `hidden_metadata` flags (`valid_updated_fact`, `should_update_answer`, expected gate behaviors). Matches curation steps in `docs/curation_protocol.md`.
- **Record structure (02):** Separates model factual-commitment JSON from grader-derived labels (`answer_state`, `gate_1_label`). Matches the trial schema in `docs/schema_reference.md`.
- **Grading (03):** Adds the missing answer-state extraction step before Gate 1 mapping; makes downstream contamination conditional on `evidence_status`; aligns Gate 1 and Gate 2 label names with the grading specification.
