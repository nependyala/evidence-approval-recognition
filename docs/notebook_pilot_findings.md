# Notebook Pilot Findings and Open Items

Status: working notes on the `notebooks/two_gate_probe.ipynb` pilot pushed to `origin/main`. This is pre-dataset scaffolding validation, not a result from the frozen 200-item curated set. Written to decide what to do about the H5 discrepancy below before we call the augmented dataset (schema + templates + memory policies + grading) usable end to end.

## Where this notebook actually lives

`notebooks/two_gate_probe.ipynb` and its raw output (`notebooks/quick_probe_outputs/`) exist **only on `origin/main`**, pushed directly by Ancil in two commits with no PR:

- `245d740` — "ad hoc experiment & hypothesis testing" (Run 1: single model, Qwen2.5-7B-Instruct, 100 items x 4 conditions, n=400)
- `11e65c9` — "updated notebook for comparing multiple models" (Run 2: qwen-2.5-7b-instruct, qwen3-235b-a22b, gemma-3-27b-it:nitro, 400 rows/probes per model, n=1200)

Local branches (`main`, `neil/docs`, `neil/dataset-construction`) are behind `origin/main` and do not have this notebook checked out. Pull it with:

```bash
git fetch origin
git checkout origin/main -- notebooks/
```

**Nathan's branches/PRs were checked and do not contain a notebook or H5 analysis.** Nathan's GitHub handle is `FedExodus`; his work in this repo is `nathan/approval-pressure-taxonomy` (PR #1, merged), `nathan/secure-base-wording` (PR #4, merged), `nathan/flowchart-taxonomy` (PR #3, open), and `nathan/enums-taxonomy` (no PR yet) — all taxonomy/flowchart/enum docs, none touch `notebooks/`. If Nathan has his own H5 analysis, it has not been pushed anywhere in this repo yet. **Action: sync with Nathan directly before treating "his approach" as an input to the decision below** — until then this doc only has Ancil's two runs to compare.

## What the pilot was for

Stress-test the augmentation plan's hypotheses (H1-H5) and the schema/prompt/grading pipeline against generated examples before the real AMPS+MedQuAD subset is curated. Full H1-H4 recap is in the [syceval-pilot-results canvas](/Users/neilpendyala/.cursor/projects/Users-neilpendyala-Downloads-evidence-approval-recognition/canvases/syceval-pilot-results.canvas.tsx) from the Slack thread. This doc focuses specifically on H5, since it's the one hypothesis that has not held up and blocks a clean "all augmentations validated" story.

## The H5 discrepancy

**H5 claim:** `secure_disagreement` + `epistemically_typed_memory` gives the lowest downstream contamination rate of all `(relational_context, memory_policy)` combinations.

**Run 1 (single model, Qwen2.5-7B, n=400):** contingent_approval+typed was lowest (5.4%), not secure_disagreement+typed (10.0%); RD of secure_disagreement+typed vs. all other combos pooled was only -0.02.

**Run 2 (3 models, n=400 each), recomputed directly from `notebooks/quick_probe_outputs/summary_two_gate_20260715_160648.csv` using the notebook's own `print_hypothesis_report` groupby/sort logic:**

| Model | Winning combo | Winning rate | Where secure_disagreement+typed ranks | RD (secure_disagreement+typed vs. all others, downstream) |
|---|---|---|---|---|
| qwen-2.5-7b-instruct | none+typed | 3.3% | 3rd (8.7%) | -0.022 |
| gemma-3-27b-it:nitro | secure_disagreement+naive (tied with contingent_approval+typed) | 19.6% | 3rd (20.0%) | -0.053 |
| qwen3-235b-a22b | secure_disagreement+naive | 1.8% | 3rd (5.0%) | -0.012 |

Two separate problems, not one:

1. **secure_disagreement+typed has never won outright**, in either run, for any model. It is close to the top every time, but something else is consistently at least as good.
2. **The same model's numbers moved between runs.** Qwen2.5-7B's secure_disagreement+typed downstream-contamination rate was 10.0% in Run 1 and 8.7% in Run 2 — different enough that we should not treat either as "the" number for that combo without knowing what changed (prompt/grading fixes landed between the two commits; see the Slack recap's "Problems Hit & Fixes" section). We have not yet re-run the same model twice under otherwise-identical conditions to know how much of that drift is pipeline changes vs. run-to-run API variance.

## What needs to be ironed out

To call the augmented dataset "fully usable" we need a position on H5, not just a shrug. Concretely:

- [ ] **Decide the primary contamination metric now, not per-analysis.** The notebook computes both `downstream_contamination` and `memory_only_contamination`, and they disagree (e.g. gemma's secure_disagreement+typed: 20.0% downstream vs. 33.8% memory-only). The Augmentation Plan's primary metrics list (`Retrieval Downstream Contamination Rate`) already answers this — downstream contamination is primary, memory-only is diagnostic. Say so explicitly in `docs/schema_reference.md` / the metrics section so nobody re-litigates it per analysis.
- [ ] **Do not encode "secure_disagreement+typed is best" anywhere in curation or schema defaults.** Nothing in `src/coding/enums.py` or the templates currently assumes this, and it should stay that way — the whole point of keeping all four relational contexts × both memory policies in the real 200-item design (`docs/curation_protocol.md`) is to let the frozen dataset answer H5, not to bake in an assumed answer.
- [ ] **Get Nathan's input before finalizing.** He's referenced as having "handled H5" somewhere, but nothing in his branches or PRs shows it. Either he has unpushed local work, or this is a mix-up — confirm which before assuming there's a second analysis to reconcile against.
- [ ] **Set a statistical bar for "confirmed" before the real run, not after.** Both pilot runs report point estimates on convenience-sized cells (n=56-88 per combo); at those sizes a couple of items flipping changes the ranking. Decide up front (e.g. in `docs/human_audit_checklist.md` or a new analysis-plan doc) what CI width / bootstrap procedure over item-level pairs is required before H5 is called confirmed, rejected, or genuinely inconclusive — not just "lowest point estimate wins."
- [ ] **Pin model version, temperature, and seed before comparing runs again.** The 10.0% vs 8.7% drift for the same model/combo is currently unexplained (pipeline fix vs. noise). Re-run one model under frozen settings twice and diff before trusting any future H5 number.
- [ ] **Update `docs/pressure_taxonomy.md`'s "Open questions for the team" section** to log H5 as tested-and-not-confirmed twice, so it doesn't quietly get treated as settled in the paper draft.

## Decision for now

Given the above, and until Nathan's input changes the picture:

- **Treat H5 as open, not confirmed and not rejected.** Two independent runs (one model, then three models) both fail to show secure_disagreement+typed winning outright, but the effect direction (small, negative RD vs. other combos, i.e. mildly protective) is consistent across all 4 models tested so far. That's a real but modest signal, not the clean "best pairing" claim.
- **This does not block calling the dataset augmentation-complete.** Per Ancil's read of the pilot, H4 (typed memory reduces false admission) alone carries the primary claim; H5 is upside, not load-bearing. Ship the full factorial design (all relational contexts x both memory policies) as planned so the real dataset can settle H5 empirically, and report it as an open/exploratory finding rather than a confirmed result in the paper.
- **Re-open this decision once:** (a) Nathan's H5 work, if it exists, is located and reconciled, and (b) the real curated-dataset run produces item-level-paired H5 numbers with a pre-registered significance bar.
