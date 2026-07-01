# Human Audit Checklist

Use this checklist when reviewing a stratified sample of curated trials before freezing a dataset version.

## Source and facts

- [ ] Is the source document clear and self-contained?
- [ ] Is the verified fact explicit and unambiguous in the source document?
- [ ] Is the false correction plausible but clearly unsupported (for unsupported conditions)?
- [ ] Does `valid_updated_fact` differ from both `verified_fact` and `false_correction` (for evidence conditions)?

## Pressure and evidence

- [ ] Is the pressure cue isolated (social confidence, authority, emotion, etc.) without confounds?
- [ ] Does the unsupported condition avoid evidence-bearing language in pushback turns?
- [ ] Does the evidence condition actually provide evidence (not just assertive language)?
- [ ] Is `pressure_turn_count` consistent with the number of pushback turns?

## Relational and memory context

- [ ] Is the relational-memory condition understandable and distinct from pushback condition?
- [ ] Is the memory instruction aligned with the assigned `memory_policy`?
- [ ] Are expected memory behavior flags (`should_*`) consistent with `evidence_status`?

## Leakage and quality

- [ ] Does the prompt leak hidden labels (domain, verified_fact, conditions, expected behaviors)?
- [ ] Is the example too repetitive or artificial compared to sibling trials?
- [ ] Does the downstream task test the same target fact as the initial question?

## Provenance

- [ ] Are `template_id`, `paraphrase_id`, `generator_id`, and `random_seed` recorded?
- [ ] Does `trial_id` follow naming conventions and match hidden metadata?

## Sign-off

| Auditor | Date | Sample size | Pass rate | Notes |
|---|---|---|---|---|
| | | | | |
