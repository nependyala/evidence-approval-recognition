# Schema Reference

Source of truth: **SycEval Augmentation Plan for the Two-Gate Study**. This document describes the trial JSON schema used for curation, experiment logging, and grading.

## Trial (top-level)

```json
{
  "trial_id": "string",
  "dataset_version": "string",
  "base_item": {},
  "experimental_factors": {},
  "visible_input": {},
  "hidden_metadata": {},
  "model_outputs": {},
  "evaluation": {}
}
```

`model_outputs` and `evaluation` default to empty/null at curation time.

## base_item

| Field | Type | Description |
|---|---|---|
| `base_item_id` | string | Normalized item identifier in this dataset |
| `syceval_item_id` | string | Original SycEval item identifier |
| `source_dataset` | enum | `AMPS` or `MedQuAD` |
| `source_item_id` | string | Original source-dataset identifier |
| `domain` | string | Item domain (e.g. `math_word_problem`) |
| `legacy_context_mode` | enum | `in_context` or `preemptive` |
| `legacy_rebuttal_tier` | string | Original SycEval rebuttal level (legacy only) |

## experimental_factors

| Field | Type | Description |
|---|---|---|
| `model_id` | string \| null | Model under test (filled at experiment time) |
| `relational_context_label` | enum | `none`, `truth_instruction`, `secure_disagreement`, `contingent_approval` |
| `condition` | string | High-level condition label (e.g. `approval_pressure`) |
| `pressure_family` | enum | `approval` or `evidence` |
| `confidence` | enum | `low` or `high` |
| `intensity` | enum | `single` or `repeated` |
| `evidence_status` | enum | `unsupported_assertion`, `fabricated_evidence`, `valid_evidence` |
| `memory_policy` | enum | `no_factual_memory`, `naive_summary_memory`, `epistemically_typed_memory` |
| `pressure_template_id` | string | Pressure wording template identifier |

## visible_input

| Field | Type | Description |
|---|---|---|
| `question` | string | Original or normalized SycEval question |
| `relational_context` | string | Relational framing text shown before pressure |
| `canonical_initial_turn` | object | Frozen assistant answer (`assistant_response`) |
| `pushback_turns` | list[object] | User pressure turns (`turn_index`, `user_text`) |
| `response_format_instruction` | object | Per-turn JSON response schema |
| `memory_instruction` | string | Gate 2 memory-write instruction |
| `downstream_task` | string | Fresh-session retrieval prompt |

### Gate 1 transcript order

1. Question
2. Canonical initial assistant answer (frozen)
3. Relational context
4. User pressure or valid-evidence correction
5+. Additional turns for `repeated` intensity
6. Final model response (recorded in `model_outputs`)

## hidden_metadata

| Field | Type | Description |
|---|---|---|
| `target_claim` | string | Single atomic factual claim under evaluation |
| `gold_answer` | string | Verified correct answer |
| `true_answer_aliases` | list[string] | Accepted equivalent answers |
| `false_answer` | string | Validated incorrect answer |
| `valid_evidence_asset` | string \| null | Verified evidence establishing correct update |
| `fabricated_evidence_asset` | string \| null | Invalid but rhetorically supportive false evidence |
| `should_update_answer` | bool | Whether the model should revise its answer |
| `expected_gate_1_behavior` | enum | Expected response-gate behavior |
| `expected_gate_2_behavior` | enum | Expected memory-gate behavior |

## model_outputs

Filled by experiment runners after inference.

| Field | Type | Description |
|---|---|---|
| `initial_answer` | any \| null | Parsed initial response |
| `gate1_responses_by_turn` | list | Per-turn Gate 1 response JSON |
| `final_answer` | any \| null | Final Gate 1 response JSON |
| `extracted_answer` | string \| null | Extracted factual value |
| `gate1_label` | enum \| null | Objective Gate 1 label |
| `discourse_label` | string \| null | Secondary discourse behavior label |
| `memory_write` | any \| null | Gate 2 memory record |
| `retrieved_claim` | string \| null | Claim retrieved in downstream session |
| `downstream_answer` | any \| null | Fresh-session response |
| `false_memory_used` | bool \| null | Whether false memory was used as fact |
| `downstream_correct` | bool \| null | Whether downstream answer matches gold |

## evaluation

Filled by the grading pipeline.

| Field | Type | Description |
|---|---|---|
| `answer_state_by_turn` | list | Per-turn extracted answer states |
| `turn_of_flip` | int \| null | Turn where answer first changed |
| `number_of_flips` | int \| null | Count of answer changes |
| `memory_admission_label` | enum \| null | Gate 2 memory admission outcome |
| `source_preserved` | bool \| null | Whether claim origin was preserved |
| `contradiction_preserved` | bool \| null | Whether conflict with prior fact was preserved |
| `verification_preserved` | bool \| null | Whether verification state was preserved |
| `downstream_contamination` | bool \| null | Whether false memory contaminated downstream answer |
| `requires_human_review` | bool | Flag for ambiguous cases |
| `review_notes` | string \| null | Human reviewer notes |

## Enums

### Gate 1 labels

`hold`, `cave`, `elicitation_non_cave`, `rational_revision`, `stubborn`, `ambiguous`

### Gate 2 memory-admission labels

`false_claim_not_stored`, `stored_as_user_assertion`, `stored_as_disputed`, `stored_as_unverified`, `stored_as_fact`, `verified_fact_overwritten`, `not_retrievable_as_fact`

### Typed-memory fields (epistemically_typed_memory)

| Field | Example |
|---|---|
| `claim` | Factual claim text |
| `source` | `user_assertion`, `question`, `provided_evidence`, etc. |
| `evidence_status` | `unsupported`, `valid`, etc. |
| `verification_status` | `verified`, `unverified`, `disputed` |
| `contradiction_status` | e.g. `contradicts_prior_verified_fact` |
| `prior_verified_fact` | Previously verified fact |
| `memory_action` | e.g. `do_not_overwrite` |
| `retrievable_as_fact` | boolean |

## Validation rules (summary)

1. Required top-level curation fields present
2. No hidden labels in `visible_input`
3. `false_answer` ≠ `gold_answer`
4. Unsupported-pressure trials: `valid_evidence_asset` null, `should_update_answer` false; approval pressure must not contain evidence language
5. Fabricated-evidence trials: `fabricated_evidence_asset` required
6. Valid-evidence trials: `valid_evidence_asset` set, evidence language in pushback, `should_update_answer` true
7. `single` intensity → 1 pushback turn; `repeated` intensity → ≥ 2 turns
8. Pushback `turn_index` values are 1-indexed and contiguous
9. `memory_policy` in supported set
10. `downstream_task` and `canonical_initial_turn.assistant_response` non-empty
11. `trial_id` matches naming pattern and `experimental_factors`

## Sample fixture

See `data/fixtures/example_trial.json` for a complete synthetic trial with empty `model_outputs` and `evaluation`.
