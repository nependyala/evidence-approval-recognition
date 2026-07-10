# Human Audit Checklist

Use this checklist when reviewing a stratified sample of curated trials before freezing a dataset version. Aligned with the SycEval Augmentation Plan.

## Source and claims

- [ ] Is the item traceable to its SycEval and source-dataset identifiers (`base_item`)?
- [ ] Is `target_claim` atomic and scorable as a single factual claim?
- [ ] Is `gold_answer` unambiguous with reasonable `true_answer_aliases`?
- [ ] Is `false_answer` plausible but clearly incorrect (validated for AMPS/MedQuAD)?
- [ ] Does `valid_evidence_asset` genuinely establish the correct update (for valid-evidence trials)?

## Pressure and evidence

- [ ] Are pressure factors isolated (`pressure_family`, `confidence`, `intensity`, `evidence_status`)?
- [ ] Does approval pressure avoid evidence-bearing language in pushback turns?
- [ ] Does fabricated evidence support the false answer rhetorically but remain invalid?
- [ ] Does valid evidence actually establish the corrected answer (not just assertive language)?
- [ ] Does `intensity` match the number of pushback turns (single = 1, repeated ≥ 2)?

## Relational context and memory

- [ ] Is the relational context condition distinct and understandable?
- [ ] Is the memory instruction aligned with the assigned `memory_policy`?
- [ ] Are `expected_gate_1_behavior` and `expected_gate_2_behavior` consistent with `evidence_status`?

## Canonical initial turn and downstream

- [ ] Is `canonical_initial_turn.assistant_response` a plausible initial answer?
- [ ] Does routing match the initial answer (correct → unsupported pressure; incorrect → valid evidence)?
- [ ] Does the downstream task test the same target claim as the initial question?

## Leakage and quality

- [ ] Does the prompt leak hidden labels (`gold_answer`, `false_answer`, conditions, expected behaviors)?
- [ ] Is the example too repetitive or artificial compared to sibling trials?
- [ ] Does `pressure_template_id` change only its assigned pressure variables?

## Provenance

- [ ] Are `syceval_item_id`, `source_dataset`, and `source_item_id` recorded?
- [ ] Does `trial_id` follow naming conventions and match `experimental_factors`?

## Sign-off

| Auditor | Date | Sample size | Pass rate | Notes |
|---|---|---|---|---|
| | | | | |
