# Evidence Gates

Data-curation infrastructure for a **SycEval-augmented** research benchmark on **false belief persistence** in memory-augmented LLM agents.

Repository: [evidence-approval-recognition](https://github.com/nependyala/evidence-approval-recognition)

This project is built on two source-of-truth planning documents:

- **SycEval Augmentation Plan for the Two-Gate Study** — dataset construction, experimental factors, and run sequence (already reflected in this repo's schema, templates, and curation docs).
- **SycEval Two-Gate Judging and Grading Plan** — how Gate 1, Gate 2, and retrieval fields are produced: answer extraction, label rules, judge routing (deterministic → LLM judge → second judge → human adjudication), and the final judged-record shape (see `docs/judging_architecture.md`).

## Research framing: two-gate failure pipeline

This benchmark augments SycEval (AMPS + MedQuAD) to study where models fail when faced with unsupported social pressure and memory contamination:

1. **Gate 1 — Response gate:** Does the model cave to unsupported social pressure and revise a verified correct answer to a false user correction?
2. **Gate 2 — Memory admission gate:** Does a memory system store the unsupported false correction as fact, overwrite the verified fact, and later contaminate downstream responses?

Each trial separates what the model sees (`visible_input`) from evaluator-only ground truth (`hidden_metadata`). Experiment runners fill `model_outputs`; the grading pipeline fills `evaluation`.

## What this repo does (v0.2: curated dataset frozen)

Beyond the v0.1 curation scaffolding, this release adds a **frozen, validated
28,800-trial curated dataset** (`data/curated/syceval_ea_v1/`):

- Pydantic v2 schemas for trial records
- Enum definitions for domains, conditions, and expected behaviors
- Custom validation checks (label-leak prevention, evidence constraints, ID naming)
- YAML pressure and memory template libraries, including `fabricated_confident` /
  `fabricated_uncertain` templates added to close a gap in evidence-status coverage
- CLI commands for validation, schema export, and template rendering
- 200 base items (100 AMPS + 100 MedQuAD) sourced and normalized directly from the
  upstream datasets (`scripts/build_amps_items.py`, `scripts/build_medquad_items.py`)
- The full `200 items x 4 relational contexts x 12 pressure conditions x 3 memory
  policies = 28,800` trial factorial (`scripts/assemble_trials.py`), 100% passing
  `eg validate-dir`
- `data/curated/syceval_ea_v1/DATASET_CARD.md` and `manifest.json` documenting
  provenance, stratification counts, and known limitations
- Documentation for curation protocol, judging architecture, audit checklist, and naming conventions
- Tests for schema parsing, validation, templates, and ID generation

See `data/curated/syceval_ea_v1/DATASET_CARD.md` for known limitations —
notably, **no manual human audit** has been performed yet (only an automated
proxy check), and MedQuAD false answers are templated categorical swaps rather
than independently fact-checked.

## What this repo intentionally does **not** do yet

- Call any model APIs
- Run model experiments
- Grade model outputs
- Compute metrics (SCR, RRR, UDS, FMAR, DCR, UOR)
- Perform statistical analysis
- Perform a manual human audit of the curated dataset (checklist exists, sign-off pending)

## Setup

Requires Python 3.11+.

```bash
cd ~/Downloads/evidence-approval-recognition
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## CLI usage

The CLI entry point is `eg`:

```bash
# Validate a single trial fixture
eg validate-trial data/fixtures/example_trial.json

# Validate all JSON trials in a directory
eg validate-dir data/fixtures/

# Print JSON Schema for the Trial model
eg print-schema trial

# Render a pressure template with variables
eg render-template \
  --template prompts/pressure_templates/confident_false.yaml \
  --vars /path/to/vars.json

# Regenerate the toy example fixture
eg make-example-trial
```

Example `vars.json` for template rendering:

```json
{
  "false_correction": "Portland"
}
```

## Directory structure

```text
evidence-approval-recognition/
  data/             # raw / interim / curated / fixtures
  prompts/          # Memory instructions, relational memory, pressure templates
  src/
    coding/         # Trial schemas, enums, coding rubrics
    generation/     # Synthetic trial assembly, templates, versioning
    runners/        # Model experiment runners (future)
    memory/         # Memory admission logic (future)
    evaluation/     # Trial validation and grading (future)
    analysis/       # Metrics and statistical analysis (future)
  experiments/      # Run configs, manifests, version pins
  results/          # Model outputs and aggregated metrics (future)
  notebooks/        # Exploratory analysis
  paper/            # Manuscript and figures
  docs/             # Curation protocol, judging architecture, schema reference
  tests/
```

## Data-curation lifecycle

| Stage | Actor | Fills |
|---|---|---|
| Curation | This repo | `trial_id`, `dataset_version`, `base_item`, `experimental_factors`, `visible_input`, `hidden_metadata` |
| Experiment | Runner (future) | `model_outputs` |
| Evaluation | Grading pipeline (future) | `evaluation` |

Curation workflow (see `docs/curation_protocol.md`):

1. Ingest SycEval and select 200-item primary subset
2. Normalize items to atomic target claims and answer keys
3. Generate and validate pressure templates and evidence controls
4. Assign relational context, pressure factors, and memory policy
5. Instantiate trials from approved templates
6. Run automatic validation (`eg validate-dir`)
7. Human-audit a stratified sample
8. Freeze dataset version under `data/curated/`

Sample trial: `data/fixtures/example_trial.json`

Frozen dataset: `data/curated/syceval_ea_v1/trials/` (28,800 trial JSON files), documented
by `data/curated/syceval_ea_v1/DATASET_CARD.md` and `manifest.json`

## Licensing

- **Code:** MIT (see `LICENSE`)
- **Dataset:** Expected to be released under CC BY 4.0 when published; see
  `data/curated/syceval_ea_v1/DATASET_CARD.md` for AMPS/MedQuAD upstream license notes.

## Development

```bash
python -m pytest
python -m ruff check .
```
