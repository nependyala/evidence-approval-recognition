# Data directory

This directory holds dataset artifacts across the curation lifecycle.

| Subdirectory | Purpose |
|---|---|
| `raw/` | Unprocessed source artifacts (documents, seeds) |
| `interim/` | Partially assembled trials pending validation |
| `curated/` | Frozen, validated trial records for a dataset version |
| `fixtures/` | Toy examples for schema and validation testing |

**Note:** `curated/syceval_ea_v1/` contains the frozen, validated 28,800-trial
dataset (200 base items x 4 relational contexts x 12 pressure conditions x 3
memory policies). See `curated/syceval_ea_v1/DATASET_CARD.md` and
`manifest.json`. `raw/` and `interim/` hold intermediate build artifacts
(sampled source pools, normalized base items) and are not tracked in git — the
scripts in `scripts/` regenerate them deterministically from `data/raw/*.json`.
