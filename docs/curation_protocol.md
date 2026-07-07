# Curation Protocol

This document describes the intended future process for curating the Evidence Gates benchmark dataset. **No full dataset is generated in the scaffolding release.**

## Overview

Trials are synthetic with known ground truth. The curation pipeline fills only:

- `trial_id`
- `dataset_version`
- `visible_input`
- `hidden_metadata`

Experiment runners later fill `model_outputs`. Evaluation pipelines add grading outputs separately.

## Steps

1. **Define domain pool** — Select from supported domains (biography, policy records, scheduling, etc.).
2. **Define target attributes** — Choose fact attributes to query and potentially corrupt (e.g., office location).
3. **Generate synthetic source documents** — Create self-contained records containing verified facts.
4. **Generate plausible false corrections** — Produce believable but unsupported alternatives.
5. **Generate valid evidence corrections** — For evidence-bearing conditions, create `valid_updated_fact` and evidence snippets.
6. **Assign relational condition** — Select from `none`, `truth_instruction`, `secure_disagreement`, or `contingent_approval`.
7. **Assign pushback/evidence condition** — Select pressure template family (false correction or evidence-bearing).
8. **Use human-designed seed templates** — Start from approved YAML templates in `prompts/pressure_templates/`.
9. **Use LLMs only for paraphrasing approved templates** — No free-form trial generation; paraphrase within template constraints.
10. **Instantiate trials programmatically** — Assemble `visible_input` and `hidden_metadata` from components.
11. **Create multi-turn pushback sequences** — Build `pushback_turns` consistent with `pressure_turn_count` and `turn_structure`.
12. **Assign memory policy** — Select `no_memory`, `naive_summary`, or `epistemically_typed_memory`.
13. **Define expected memory behavior** — Set boolean flags (`should_update_answer`, `should_overwrite_verified_fact`, etc.).
14. **Create downstream retrieval tasks** — Write `downstream_task` prompts that test memory contamination.
15. **Generate visible model input** — Ensure no hidden labels leak into `visible_input`.
16. **Generate hidden evaluator metadata** — Record ground truth, conditions, and expected gate behaviors.
17. **Run automatic validation** — `eg validate-dir data/interim/`
18. **Human-audit a stratified sample** — Use `docs/human_audit_checklist.md`.
19. **Freeze dataset version** — Copy validated trials to `data/curated/{version}/` and update dataset card.

## Quality gates

- All trials must pass Pydantic schema validation.
- All trials must pass custom validation checks (see `docs/schema_reference.md`).
- Unsupported trials must not contain evidence-bearing language in pushback turns.
- Valid-evidence trials must include `valid_updated_fact` and evidence language.
- Trial IDs must follow naming conventions (see `docs/naming_conventions.md`).

## Out of scope for curation

- Model inference
- Memory system execution
- Grading or metric computation
