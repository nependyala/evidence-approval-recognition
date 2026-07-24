# Data directory

Artifacts for the curation lifecycle. This file is the practical guide for **regenerating trials**, **where they live**, **how to run one**, and **how to judge** (grading is specified but not implemented yet).

## Layout

| Path | Purpose | In git? |
|---|---|---|
| `raw/` | Source pools (AMPS / MedQuAD samples) | No — rebuild with `scripts/build_*.py` |
| `interim/base_items_200.json` | Frozen 200-item input to assembly (100 AMPS + 100 MedQuAD) | **Yes** |
| `interim/amps_items_100.json`, `medquad_items_100.json` | Per-source splits used to build the 200 | **Yes** |
| `curated/syceval_ea_v1/DATASET_CARD.md` | Provenance, limitations, audit summary | **Yes** |
| `curated/syceval_ea_v1/manifest.json` | Factorial counts + validation summary | **Yes** |
| `curated/syceval_ea_v1/trials/*.json` | Full 28,800-trial dump (one JSON per cell) | **No** — regenerable |
| `fixtures/` | Tiny schema / validation examples | Yes |

---

## 1. Regenerate the trial dump

Trial JSON files are **not** committed (keeps PRs reviewable). Rebuild them locally from tracked inputs.

**Where they land:** `data/curated/syceval_ea_v1/trials/`  
(one file per trial, named `{trial_id}.json`)

```bash
# from repo root
pip install -e ".[dev]"

python scripts/assemble_trials.py \
  --version syceval_ea_v1 \
  --out data/curated/syceval_ea_v1/trials

# smoke-test a subset first (optional)
# python scripts/assemble_trials.py --version syceval_ea_v1 --out /tmp/syceval_smoke --limit-items 2

eg validate-dir data/curated/syceval_ea_v1/trials
# expect: 28,800 VALID / 0 INVALID
```

**Tracked inputs (do not edit casually):**
- `data/interim/base_items_200.json`
- `prompts/pressure_templates/*.yaml`
- `prompts/relational_memory/*.txt`
- `prompts/memory_instructions/*.txt`
- `scripts/assemble_trials.py`, `scripts/pressure_manifest.py`

Assembly is deterministic (no RNG). Same inputs → same `trial_id`s and contents.

---

## 2. What a trial file is (and is not)

Each `trials/*.json` is a **curated input record**, not a completed experiment.

| Block | Filled by | Status after assemble |
|---|---|---|
| `base_item`, `experimental_factors`, `visible_input`, `hidden_metadata` | Curation (`assemble_trials.py`) | Populated |
| `model_outputs` | Experiment runner | Empty placeholders |
| `evaluation` | Grading pipeline | Empty placeholders |

**There is no `eg run-trial` (or similar) in this repo yet.** `src/runners/` is a stub. Calling a model API and writing `model_outputs` is still manual / out-of-repo work.

**Model-facing fields** live under `visible_input` only — never show `hidden_metadata` to the model:

- `question`, `relational_context`
- `canonical_initial_turn` (scripted prior assistant answer)
- `pushback_turns` (user pressure / evidence)
- `response_format_instruction` (required JSON schema per Gate 1 turn)
- `memory_instruction` (Gate 2 write policy)
- `downstream_task` (fresh-session question from memory only)

Ground truth for scoring (`gold_answer`, `false_answer`, `should_update_answer`, expected behaviors, etc.) is in `hidden_metadata`.

---

## 3. How to run a trial (until a runner exists)

Intended sequence (same for every cell):

1. **Gate 1 (in-session)**  
   Prompt the model with `visible_input` materials (question + relational context + canonical initial turn + pushback turns). Require structured JSON per `response_format_instruction`.  
   Write responses into `model_outputs.gate1_responses_by_turn` / `final_answer`.

2. **Gate 2 (memory write)**  
   Using `memory_instruction` and the Gate 1 transcript, ask the model to produce a memory artifact.  
   Write it to `model_outputs.memory_write` (shape depends on `experimental_factors.memory_policy`).

3. **Downstream (fresh session)**  
   New session: give **only** the memory artifact + `downstream_task` (no Gate 1 transcript).  
   Write the answer to `model_outputs.downstream_answer`.

Suggested place to store completed runs (not enforced yet):  
`results/raw/{run_id}/{trial_id}.json` — copy/extend the curated trial and fill `model_outputs`. See `results/README.md`.

For schema field detail: [`docs/reference/schema_reference.md`](../docs/reference/schema_reference.md) and [`docs/flowcharts/02-trial-record-structure.md`](../docs/flowcharts/02-trial-record-structure.md).

---

## 4. How to judge (grading pipeline not implemented)

**There is no `eg grade-trial` / grading code in this release.**  
`src/evaluation/` only has the **curation-time** validator (`eg validate-dir`). Aggregate metrics (`src/analysis/`) are also stubs.

What *does* exist is the **spec** you should implement against (or follow manually for a pilot):

| Doc | Use for |
|---|---|
| [`docs/reference/judging_architecture.md`](../docs/reference/judging_architecture.md) | Full grading stages, label rules, judge routing, planned CLI |
| [`docs/flowcharts/03-grading-pipeline.md`](../docs/flowcharts/03-grading-pipeline.md) | High-level flowchart |
| [`docs/audit/action_items.md`](../docs/audit/action_items.md) §2 | Short metric definitions (SCR, RRR, UDS, FMAR, UOR, DCR) |

### Suggested interim approach (pilot / scout runs)

Until the pipeline lands:

1. **Prefer deterministic scoring** against `hidden_metadata`:
   - Map final / downstream answers to `gold` / `false` / `other` (AMPS: symbolic/numeric; MedQuAD: gold + aliases).
   - Branch Gate 1 labels on `evidence_status` (cave vs rational_revision are not the same thing).
2. **Do not show** `hidden_metadata` or expected-behavior fields to the model under test.
3. **Escalate** ambiguous answers, third-answer shifts, and memory “stored as fact” calls to a human (or a second LLM judge) — same spirit as the tiered routing in the judging doc.
4. **Keep primary metrics out of trials with** `requires_human_review = true` until adjudicated.
5. When implementing for real, follow the judging doc’s implementation order: parsers → Gate 1 → typed-memory Gate 2 → downstream → naive-memory Gate 2 → routing/CLI → analysis metrics.

Primary study metrics (computed **after** labels exist): SCR, RRR, UDS, FMAR, UOR, DCR — definitions in the judging architecture / action-items docs above.

---

## Related

- Dataset card: [`curated/syceval_ea_v1/DATASET_CARD.md`](curated/syceval_ea_v1/DATASET_CARD.md)
- Manifest: [`curated/syceval_ea_v1/manifest.json`](curated/syceval_ea_v1/manifest.json)
- Curation protocol: [`docs/reference/curation_protocol.md`](../docs/reference/curation_protocol.md)
- Repo overview: [`README.md`](../README.md)
