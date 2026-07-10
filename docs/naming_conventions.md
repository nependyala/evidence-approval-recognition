# Naming Conventions

Aligned with the SycEval Augmentation Plan for the Two-Gate Study.

## Dataset version naming

Format: `syceval_ea_v{major}`

Examples:

- `syceval_ea_v1` — First augmented SycEval freeze
- `syceval_ea_v2` — Revised freeze after QC

Config files live in `experiments/configs/dataset_versions/{version}.yaml`.

## Base item ID naming

Format: `syceval_ea_base_{number}`

Example: `syceval_ea_base_000001`

## Trial ID naming

Format:

```text
{dataset_version}_{base_item_number}_{model_short}_{relational}_{pressure}_{confidence}_{intensity}_{memory}
```

Example:

```text
syceval_ea_v1_000001_gpt41mini_secure_approval_high_repeated_typed
```

- `base_item_number`: six-digit zero-padded integer (e.g. `000001`)
- `model_short`: short model slug (e.g. `gpt41mini`, `claude37`)
- `relational`: `none`, `truth`, `secure`, `contingent`
- `pressure`: `approval`, `evidence`
- `confidence`: `low`, `high`
- `intensity`: `single`, `repeated`
- `memory`: `no_mem`, `naive`, `typed`

### Relational context short codes

| Label | Short |
|---|---|
| `none` | `none` |
| `truth_instruction` | `truth` |
| `secure_disagreement` | `secure` |
| `contingent_approval` | `contingent` |

### Memory policy short codes

| Policy | Short |
|---|---|
| `no_factual_memory` | `no_mem` |
| `naive_summary_memory` | `naive` |
| `epistemically_typed_memory` | `typed` |

## Pressure template ID naming

Format: `{family}_{confidence}_{intensity}_v{version}`

Examples:

- `approval_high_repeated_v01`
- `evidence_low_single_v01`

## Run naming (experiments)

Format:

```text
{model}_{memory_policy}_{dataset_version}_{date}
```

Example:

```text
gpt41mini_epistemically_typed_memory_syceval_ea_v1_20260701
```

## File naming

| Artifact | Pattern | Example |
|---|---|---|
| Trial JSON | `{trial_id}.json` | `syceval_ea_v1_000001_gpt41mini_secure_approval_high_repeated_typed.json` |
| Validation report | `validation_{dataset_version}.json` | `validation_syceval_ea_v1.json` |
| Curated shard | `{source_dataset}_{shard}.jsonl` | `AMPS_0001.jsonl` |
| Fixture | descriptive name | `example_trial.json` |
