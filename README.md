# Evidence Gates

Data-curation infrastructure for a research benchmark on **false belief persistence** in memory-augmented LLM agents.

Repository: [evidence-approval-recognition](https://github.com/nependyala/evidence-approval-recognition)

## Research framing: two-gate failure pipeline

This benchmark studies where models fail when faced with unsupported social pressure and memory contamination:

1. **Gate 1 — Response gate:** Does the model cave to unsupported social pressure and revise a verified correct answer to a false user correction?
2. **Gate 2 — Memory admission gate:** Does a memory system store the unsupported false correction as fact, overwrite the verified fact, and later contaminate downstream responses?

Each trial separates what the model sees (`visible_input`) from evaluator-only ground truth (`hidden_metadata`). Experiment runners later fill `model_outputs`; grading pipelines are out of scope for this repo.

## What this repo does (v0.1 scaffolding)

This initial release provides **reproducible curation scaffolding only**:

- Pydantic v2 schemas for trial records
- Enum definitions for domains, conditions, and expected behaviors
- Custom validation checks (label-leak prevention, evidence constraints, ID naming)
- YAML pressure and memory template libraries (metadata + seed text, not instantiated trials)
- Gate 2 memory mechanisms (no-memory, naive summary, epistemically typed memory) with
  policy logic, downstream retrieval, and audit/validation (`src/memory/`)
- CLI commands for validation, schema export, template rendering, and memory tooling
- Documentation for curation protocol, audit checklist, and naming conventions
- Tests for schema parsing, validation, templates, ID generation, and memory mechanisms

## What this repo intentionally does **not** do yet

- Generate the full curated dataset
- Call any model APIs
- Run model experiments
- Grade Gate 1 responses
- Compute aggregate metrics (SCR, RRR, UDS, FMAR, DCR, UOR)
- Perform statistical analysis

## Gate 2 memory mechanisms (`src/memory/`)

The three MVP memory policies are implemented as deterministic, model-free logic:

- **`no_memory`** — persistence control; nothing is written or retrieved.
- **`naive_summary`** — stores model-produced free text; `audit_naive_summary`
  flags when an unsupported false correction is stored as fact.
- **`epistemically_typed_memory`** — structured record preserving source,
  evidence level, verification status, contradiction status, overwrite action,
  and retrieval permission.

Key building blocks:

- `policies.py` — contradiction detection, overwrite logic, retrieval-permission
  logic, and a reference typed-memory builder derived from ground truth.
- `retrieval.py` — resolves what a downstream query receives from each policy
  and detects false-memory contamination.
- `audit.py` — typed-memory schema validation, ground-truth validation against
  the reference, and naive-summary auditing.

See `docs/schema_reference.md` for the record schemas and derivation rules, and
`prompts/memory_writers/` for the model-facing writer prompts.

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

# Build the reference memory state for a trial's assigned memory policy
eg build-reference-memory data/fixtures/example_trial.json

# Validate a typed-memory record (schema + optional ground truth)
eg validate-typed-memory typed_record.json --trial data/fixtures/example_trial.json

# Audit a naive summary for storing the false correction as fact
eg audit-naive-memory data/fixtures/example_trial.json --summary "..."
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
| Curation | This repo | `trial_id`, `dataset_version`, `visible_input`, `hidden_metadata` |
| Experiment | Runner (future) | `model_outputs` |
| Evaluation | Judging pipeline (future) | Grading outputs |

Curation workflow (planned):

1. Define domain pool and target attributes
2. Generate synthetic source documents and corrections
3. Assign relational, pushback, and memory conditions
4. Instantiate trials from approved templates
5. Run automatic validation (`eg validate-dir`)
6. Human-audit a stratified sample
7. Freeze dataset version under `data/curated/`

## Licensing

- **Code:** MIT (see `LICENSE`)
- **Dataset (future):** Expected to be released under CC BY 4.0 when curated data is published. No dataset is included in this scaffolding release.

## Development

```bash
python -m pytest
python -m ruff check .
```
