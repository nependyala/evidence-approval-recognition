# Naming Conventions

## Dataset version naming

Format: `v{major}.{minor}`

Examples:

- `v0.1` — Initial scaffolding / draft schema
- `v1.0` — First frozen public release

Config files live in `experiments/configs/dataset_versions/{version}.yaml`.

## Template version naming

Format: `templates_v{major}.{minor}`

Examples:

- `templates_v0.1`

Config files live in `experiments/configs/template_versions/{version}.yaml`.

## Trial ID naming

Format:

```text
{domain_short}_{entity_number}_{relational_short}_{pushback_short}_{memory_short}
```

Example:

```text
bio_0042_secure_bare_assertion_naive
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

### Relational context short codes

| Context | Short |
|---|---|
| `none` | `none` |
| `truth_instruction` | `truth` |
| `secure_disagreement` | `secure` |
| `contingent_approval` | `contingent` |

### Pushback condition short codes

| Condition | Short |
|---|---|
| `no_pressure` | `no_pressure` |
| `bare_assertion` | `bare_assertion` |
| `approval` | `approval` |
| `fabricated_evidence` | `fabricated_evidence` |
| `valid_evidence` | `valid_evidence` |
| `weak_evidence` | `weak_evidence` |
| `ambiguous_evidence` | `ambiguous_evidence` |
| `authority` | `authority` |

### Memory policy short codes

| Policy | Short |
|---|---|
| `no_memory` | `no_mem` |
| `naive_summary` | `naive` |
| `epistemically_typed_memory` | `typed` |

`entity_number` is a four-digit zero-padded integer (e.g., `0042`).

Modifiers (`user_confidence`, `intensity`) are intentionally **not** encoded in the trial_id; they live in `hidden_metadata`. The id stays a stable key rather than a serialization of every attribute.

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
| Trial JSON | `{trial_id}.json` | `bio_0042_secure_bare_assertion_naive.json` |
| Validation report | `validation_{dataset_version}.json` | `validation_v0.1.json` |
| Curated shard | `{domain}_{shard}.jsonl` | `bio_0001.jsonl` |
| Fixture | descriptive name | `example_trial.json` |
