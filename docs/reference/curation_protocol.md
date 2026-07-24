# Curation Protocol

This document describes the curation process for the SycEval-augmented two-gate benchmark. **Source of truth:** SycEval Augmentation Plan for the Two-Gate Study.

## Overview

Trials augment SycEval items (AMPS + MedQuAD) with independent pressure factors, relational context, memory policies, and evaluation scaffolding. The curation pipeline fills:

- `trial_id`
- `dataset_version`
- `base_item`
- `experimental_factors` (except `model_id`, filled at experiment time)
- `visible_input`
- `hidden_metadata`

Experiment runners later fill `model_outputs`. The grading pipeline fills `evaluation`.

## Dataset construction steps

1. **Ingest SycEval** — Load the 500 AMPS and 500 MedQuAD items. Preserve original identifiers and metadata.
2. **Select primary subset** — Freeze 200 eligible items (100 AMPS, 100 MedQuAD), stratified by problem family / question type.
3. **Normalize each item** — Create one atomic `target_claim`, `gold_answer`, aliases, `false_answer`, and `valid_evidence_asset`.
4. **Validate false answers** — Symbolic/numeric checks for AMPS; human review for MedQuAD.
5. **Generate pressure templates** — Approval and evidence pressure with low/high confidence and single/repeated intensity.
6. **Create evidence controls** — Fabricated-evidence variants and verified valid-evidence assets.
7. **Validate templates** — Remove templates that reveal answers, alter multiple factors, or make false answers defensible.

## Per-trial assembly

1. **Freeze canonical initial turn** — Record the model's initial answer; reuse across all conditions for that model–item pair.
2. **Route the item** — Correct initial answers → unsupported-pressure trials. Incorrect initial answers → valid-evidence trials.
3. **Assign relational context** — One of: `none`, `truth_instruction`, `secure_disagreement`, `contingent_approval`.
4. **Assign pressure factors** — Set `pressure_family`, `confidence`, `intensity`, `evidence_status`, and `pressure_template_id`.
5. **Instantiate pushback turns** — From approved YAML templates in `prompts/pressure_templates/`.
6. **Assign memory policy** — `no_factual_memory`, `naive_summary_memory`, or `epistemically_typed_memory`.
7. **Set expected behaviors** — `expected_gate_1_behavior`, `expected_gate_2_behavior`, `should_update_answer`.
8. **Write downstream task** — Fresh-session retrieval prompt using only memory state.
9. **Attach response format instruction** — Per-turn JSON schema for factual commitment (no grading labels).
10. **Run automatic validation** — `eg validate-dir` on the assembled trial directory.
11. **Human-audit a stratified sample** — Use `docs/audit/human_audit_checklist.md`.
12. **Freeze dataset version** — Write `DATASET_CARD.md` + `manifest.json` under `data/curated/{version}/`. The full trial JSON dump under `trials/` is regenerable via `scripts/assemble_trials.py` and is **not** committed (see `data/README.md`); keep `data/interim/base_items_200.json` tracked as the freeze input.

## Pressure construction rules

| Condition | Required behavior |
|---|---|
| Approval pressure | Disagreement, disappointment, praise withdrawal, or agreement-seeking — no evidence |
| Evidence pressure | Reasoning, citation-like text, derivation, or source claims |
| Fabricated evidence | Supports false answer rhetorically but remains invalid |
| Valid evidence | Genuinely establishes that the initial answer should be revised |
| Low confidence | Tentative or uncertain language |
| High confidence | Explicit certainty without changing evidence status |
| Single intensity | Apply pressure once |
| Repeated intensity | Repeat the same false claim across turns without adding new evidence |

## Quality gates

- All trials must pass Pydantic schema validation.
- All trials must pass custom validation checks (see `docs/reference/schema_reference.md`).
- Approval-pressure trials must not contain evidence-bearing language in pushback turns.
- Valid-evidence trials must include `valid_evidence_asset` and evidence language.
- Trial IDs must follow naming conventions (see `docs/reference/naming_conventions.md`).
- No transcript, model state, or memory output is shared between experimental conditions.

## Out of scope for curation

- Model inference
- Memory system execution
- Grading or metric computation

## Unit of analysis

One trial record = one **model × item × relational context × pressure condition × memory policy** run.
