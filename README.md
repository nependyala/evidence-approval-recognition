# Evidence Gates

Data-curation infrastructure for a **SycEval-augmented** research benchmark on **false belief persistence** in memory-augmented LLM agents.

Repository: [evidence-approval-recognition](https://github.com/nependyala/evidence-approval-recognition)

This project is built on two source-of-truth planning documents:

- **SycEval Augmentation Plan for the Two-Gate Study** — dataset construction, experimental factors, and run sequence (already reflected in this repo's schema, templates, and curation docs).
- **SycEval Two-Gate Judging and Grading Plan** — how Gate 1, Gate 2, and retrieval fields are produced (see `docs/reference/judging_architecture.md`). **Spec only — grading is not implemented yet.**

## Research framing: two-gate failure pipeline

1. **Gate 1 — Response gate:** Does the model cave to unsupported social pressure and revise a verified correct answer to a false user correction?
2. **Gate 2 — Memory admission gate:** Does a memory system store the unsupported false correction as fact, overwrite the verified fact, and later contaminate downstream responses?

Each trial separates what the model sees (`visible_input`) from evaluator-only ground truth (`hidden_metadata`). Experiment runners fill `model_outputs`; the grading pipeline fills `evaluation`.

## Setup

Requires Python 3.11+.

```bash
cd ~/Downloads/evidence-approval-recognition
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## How to regenerate, run, and judge trials

**Full walkthrough:** [`data/README.md`](data/README.md) (regenerate → where files live → how to run one → how to judge without a pipeline).

### Regenerate the 28,800-trial dump

Trial JSON files are **not** in git. They are written locally to `data/curated/syceval_ea_v1/trials/`:

```bash
python scripts/assemble_trials.py \
  --version syceval_ea_v1 \
  --out data/curated/syceval_ea_v1/trials

eg validate-dir data/curated/syceval_ea_v1/trials   # expect 28,800 / 28,800 VALID
```

Inputs: tracked `data/interim/base_items_200.json` + `prompts/`. Assembly is deterministic.

### Run a trial

**There is no experiment runner yet** (`src/runners/` is empty). A curated trial only has inputs filled; `model_outputs` is empty.

Until a runner exists, drive the model yourself using `visible_input` only:

1. **Gate 1** — question + relational context + canonical initial turn + pushback(s) → structured JSON per `response_format_instruction`
2. **Gate 2** — write memory under `memory_instruction` / `memory_policy`
3. **Downstream** — fresh session with memory + `downstream_task` only

Write completed runs under `results/raw/` (suggested). Details in [`data/README.md`](data/README.md) §3.

### Judge / grade

**There is no grading pipeline yet** — no `eg grade-trial`, and `src/evaluation/` is curation validation only. Metrics code (`src/analysis/`) is also a stub.

Use the **spec** for pilots or when implementing:

- [`docs/reference/judging_architecture.md`](docs/reference/judging_architecture.md) — stages, labels, routing
- [`docs/flowcharts/03-grading-pipeline.md`](docs/flowcharts/03-grading-pipeline.md)
- Interim scoring guidance: [`data/README.md`](data/README.md) §4

Primary metrics once labels exist: SCR, RRR, UDS, FMAR, UOR, DCR.

## What this repo does (v0.2)

- Pydantic schemas, enums, curation validators (`eg validate-*`)
- Pressure / relational / memory templates
- 200 base items at `data/interim/base_items_200.json`
- Deterministic assembly → 28,800 trials (`scripts/assemble_trials.py`)
- Dataset card + manifest under `data/curated/syceval_ea_v1/`
- Docs: curation, judging **spec**, audit checklist (human sign-off 2026-07-21)
- Tests for schema, validation, templates, IDs

Dataset card / limitations: [`data/curated/syceval_ea_v1/DATASET_CARD.md`](data/curated/syceval_ea_v1/DATASET_CARD.md). Doc index: [`docs/README.md`](docs/README.md).

## What this repo intentionally does **not** do yet

- Call model APIs / run experiments (`src/runners/`)
- Grade model outputs (`eg grade-*` / full `src/evaluation/` grader)
- Compute study metrics (`src/analysis/`)

## CLI (curation / validation only)

```bash
eg validate-trial data/fixtures/example_trial.json
eg validate-dir data/fixtures/
eg print-schema trial
eg render-template --template prompts/pressure_templates/confident_false.yaml --vars /path/to/vars.json
eg make-example-trial
```

## Directory structure

```text
evidence-approval-recognition/
  data/             # raw / interim / curated / fixtures — see data/README.md
  prompts/          # pressure, relational, memory templates
  src/
    coding/         # Trial schemas, enums
    generation/     # Assembly helpers, templates, versioning
    runners/        # Model experiment runners (future)
    memory/         # Memory admission logic (future)
    evaluation/     # Curation validator today; grading future
    analysis/       # Metrics (future)
  experiments/      # Run configs (future)
  results/          # Model outputs / graded runs (future)
  docs/             # reference / theory / audit / findings / flowcharts
  tests/
```

## Licensing

- **Code:** MIT (see `LICENSE`)
- **Dataset:** Expected CC BY 4.0 when published; see the dataset card for AMPS/MedQuAD upstream notes.

## Development

```bash
python -m pytest
python -m ruff check .
```
