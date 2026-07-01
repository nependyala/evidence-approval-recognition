# Naming Conventions

## Dataset version naming

Format: `v{major}.{minor}`

Examples:

- `v0.1` — Initial scaffolding / draft schema
- `v1.0` — First frozen public release

Config files live in `configs/dataset_versions/{version}.yaml`.

## Template version naming

Format: `templates_v{major}.{minor}`

Examples:

- `templates_v0.1`

Config files live in `configs/template_versions/{version}.yaml`.

## Trial ID naming

Format:

```text
{domain_short}_{entity_number}_{relational_short}_{pushback_short}_{memory_short}
```

Example:

```text
bio_0042_secure_confident_false_naive
```

### Domain short codes

| Domain | Short |
|---|---|
| `synthetic_biography` | `bio` |
| `company_policy_records` | `policy` |
| `calendar_scheduling_facts` | `calendar` |
| `user_profile_facts` | `profile` |
| `table_based_records` | `table` |
| `task_rules` | `rules` |
| `organizational_records` | `org` |

### Relational condition short codes

| Condition | Short |
|---|---|
| `no_memory` | `no_mem` |
| `truth_instruction` | `truth` |
| `secure_disagreement_memory` | `secure` |
| `contingent_approval_memory` | `contingent` |

### Pushback condition short codes

| Condition | Short |
|---|---|
| `neutral_false` | `neutral_false` |
| `confident_false` | `confident_false` |
| `authority_false` | `authority_false` |
| `emotional_false` | `emotional_false` |
| `repeated_false` | `repeated_false` |
| `social_proof_false` | `social_proof_false` |
| `weak_evidence` | `weak_evidence` |
| `strong_evidence` | `strong_evidence` |
| `ambiguous_evidence` | `ambiguous_evidence` |

### Memory policy short codes

| Policy | Short |
|---|---|
| `no_memory` | `no_mem` |
| `naive_summary` | `naive` |
| `epistemically_typed_memory` | `typed` |

`entity_number` is a four-digit zero-padded integer (e.g., `0042`).

## Run naming (future experiments)

Format:

```text
{model}_{memory_system}_{dataset_version}_{date}
```

Example:

```text
gpt4o_naive_summary_v0.1_20260701
```

## File naming

| Artifact | Pattern | Example |
|---|---|---|
| Trial JSON | `{trial_id}.json` | `bio_0042_secure_confident_false_naive.json` |
| Validation report | `validation_{dataset_version}.json` | `validation_v0.1.json` |
| Curated shard | `{domain}_{shard}.jsonl` | `bio_0001.jsonl` |
| Fixture | descriptive name | `example_trial.json` |
