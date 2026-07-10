# Evidence Gates

Data-curation infrastructure for a **SycEval-augmented** research benchmark on **false belief persistence** in memory-augmented LLM agents.

Repository: [evidence-approval-recognition](https://github.com/nependyala/evidence-approval-recognition)

## Research framing: two-gate failure pipeline

This benchmark augments SycEval (AMPS + MedQuAD) to study where models fail when faced with unsupported social pressure and memory contamination:

1. **Gate 1 — Response gate:** Does the model cave to unsupported social pressure and revise a verified correct answer to a false user correction?
2. **Gate 2 — Memory admission gate:** Does a memory system store the unsupported false correction as fact, overwrite the verified fact, and later contaminate downstream responses?

Each trial separates what the model sees (`visible_input`) from evaluator-only ground truth (`hidden_metadata`). Experiment runners fill `model_outputs`; the grading pipeline fills `evaluation`.

## What this repo does (v0.1 scaffolding)

This initial release provides **reproducible curation scaffolding only**:

- Pydantic v2 schemas for trial records
- Enum definitions for domains, conditions, and expected behaviors
- Custom validation checks (label-leak prevention, evidence constraints, ID naming)
- YAML pressure and memory template libraries (metadata + seed text, not instantiated trials)
- CLI commands for validation, schema export, and template rendering
- Documentation for curation protocol, audit checklist, and naming conventions
- Tests for schema parsing, validation, templates, and ID generation

## What this repo intentionally does **not** do yet

- Generate the full curated dataset
- Call any model APIs
- Run model experiments
- Grade model outputs
- Compute metrics (SCR, RRR, UDS, FMAR, DCR, UOR)
- Perform statistical analysis

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
  docs/             # Curation protocol, audit checklist, schema reference
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

## Licensing

- **Code:** MIT (see `LICENSE`)
- **Dataset (future):** Expected to be released under CC BY 4.0 when curated data is published. No dataset is included in this scaffolding release.

## Development

```bash
python -m pytest
python -m ruff check .
```
