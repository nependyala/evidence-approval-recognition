# Data directory

This directory holds dataset artifacts across the curation lifecycle.

| Subdirectory | Purpose | Tracked in git? |
|---|---|---|
| `raw/` | Unprocessed source pools (AMPS / MedQuAD samples) | No — regenerable via `scripts/build_*.py` |
| `interim/` | Normalized base items pending / used for assembly | **Yes for** `base_items_200.json` (+ the 100-item splits); other interim outputs no |
| `curated/{version}/` | Frozen version metadata (`DATASET_CARD.md`, `manifest.json`) | **Yes** for card + manifest |
| `curated/{version}/trials/` | Full factorial trial JSON dump (28,800 files for v1) | **No** — regenerable (see below) |
| `fixtures/` | Toy examples for schema and validation testing | Yes |

## Regenerate `syceval_ea_v1` trials

The 28,800 trial JSON files are **not** stored in git. Rebuild them from the tracked base items + templates:

```bash
# from repo root, with the package installed (`pip install -e ".[dev]"`)
python scripts/assemble_trials.py \
  --version syceval_ea_v1 \
  --out data/curated/syceval_ea_v1/trials

# optional: confirm the freeze
eg validate-dir data/curated/syceval_ea_v1/trials
# expect: 28,800 VALID / 0 INVALID
```

**Inputs (tracked):**
- `data/interim/base_items_200.json` — 100 AMPS + 100 MedQuAD normalized items
- `prompts/pressure_templates/*.yaml`, `prompts/relational_memory/*.txt`, `prompts/memory_instructions/*.txt`
- `scripts/assemble_trials.py`, `scripts/pressure_manifest.py`

Assembly is deterministic (no RNG). Provenance and known limitations live in [`curated/syceval_ea_v1/DATASET_CARD.md`](curated/syceval_ea_v1/DATASET_CARD.md); counts in [`manifest.json`](curated/syceval_ea_v1/manifest.json).
