# Trial record structure flowchart

How one completed trial splits into source provenance, experimental factors, model-visible input, evaluator ground truth, model outputs, and grading results. The grader never infers ground truth from the conversation alone; it compares structured model outputs to `hidden_metadata`.

## 1. Top-level blocks and data flow

Who fills each block and how data moves from curation through experiment to grading.

```mermaid
flowchart LR
  subgraph curation["Curation — this repo"]
    BI[base_item]
    EF[experimental_factors]
    VI[visible_input]
    HM[hidden_metadata]
  end

  subgraph experiment["Experiment — runner"]
    MO[model_outputs]
  end

  subgraph grading["Evaluation — grader"]
    EV[evaluation]
  end

  TRIAL[trial_id + dataset_version]

  TRIAL --- BI
  TRIAL --- EF
  TRIAL --- VI
  TRIAL --- HM
  TRIAL --- MO
  TRIAL --- EV

  VI -->|prompts model| MO
  HM -->|ground truth for scoring| MO
  MO -->|raw responses to grade| EV
```

## 2. Provenance and experimental factors

Filled at curation time. `base_item` traces the trial back to SycEval; `experimental_factors` holds the independent manipulations for this run.

```mermaid
flowchart TB
  subgraph base_item["base_item"]
    direction TB
    B0[base_item_id]
    B1[syceval_item_id]
    B2[source_dataset · domain]
    B3[source_item_id]
    B4[legacy_context_mode · legacy_rebuttal_tier]
  end

  subgraph experimental_factors["experimental_factors"]
    direction TB
    C1[relational_context_label · condition]
    C2[pressure_family · confidence · intensity]
    C3[evidence_status · memory_policy]
    C4[pressure_template_id · model_id]
  end
```

## 3. Prompt and ground truth

`visible_input` is what the model sees; `hidden_metadata` is evaluator-only and never shown to the model.

```mermaid
flowchart LR
  subgraph visible_input["visible_input — model-visible"]
    direction TB
    D1[question]
    D2[relational_context]
    D3[canonical_initial_turn]
    D4[pushback_turns]
    D5[response_format_instruction]
    D6[memory_instruction]
    D7[downstream_task]
  end

  subgraph hidden_metadata["hidden_metadata — evaluator only"]
    direction TB
    E1[target_claim]
    E2[gold_answer · true_answer_aliases · false_answer]
    E3[valid_evidence_asset · fabricated_evidence_asset]
    E4[should_update_answer]
    E5[expected_gate_1_behavior · expected_gate_2_behavior]
  end
```

**`response_format_instruction`:** the model reports `final_answer`, `final_answer_type`, `source_used`, `accepted_user_correction`, `asked_for_evidence`, and `expressed_uncertainty` each turn. It does **not** output `gate1_label` or `answer_state` — those are assigned by the grader.

## 4. Model outputs and evaluation

Filled after the experiment run. The runner logs raw responses in `model_outputs`; the grader derives labels and writes `evaluation` (plus some fields back into `model_outputs`).

```mermaid
flowchart LR
  subgraph model_outputs["model_outputs — runner"]
    direction TB
    F1[initial_answer]
    F2[gate1_responses_by_turn]
    F3[final_answer]
    F4[extracted_answer · gate1_label · discourse_label]
    F5[generated memory output]
    F6[retrieved_claim · downstream_answer]
    F7[false_memory_used · downstream_correct]
  end

  subgraph evaluation["evaluation — grader"]
    direction TB
    G1[answer_state_by_turn]
    G2[turn_of_flip · number_of_flips]
    G3[gate2 block]
    G4[downstream_contamination]
    G5[requires_human_review · review_notes]
  end

  F3 --> G1
  F5 --> G3
  F6 --> G4
```

**`gate2` block:** `stored_claim`, `source`, `verification_status`, `contradiction_status`, `memory_action`, `retrievable_as_fact` — produced for every `memory_policy`.

## Lifecycle by stage

| Stage | Actor | Fills |
|---|---|---|
| Curation | This repo | `trial_id`, `dataset_version`, `base_item`, `experimental_factors`, `visible_input`, `hidden_metadata` |
| Experiment | Runner | `model_outputs` |
| Evaluation | Grading pipeline | `evaluation` (+ some `model_outputs` labels like `gate1_label`) |

## Notes

- During curation, `model_outputs` and `evaluation` are empty/null. Runners and graders fill them later.
- `condition` is a high-level, human-readable label derived from `evidence_status` at generation time (`approval_pressure`, `fabricated_evidence_pressure`, `valid_evidence_pressure`); it does not add information beyond `pressure_family`/`evidence_status`, but makes filtering trial files easier.
- Every trial ID also encodes `evidence_status` for the two `pressure_family=evidence` conditions specifically (`evidence-fab` vs. `evidence-valid`), not just `pressure_family`. Without this, `fabricated_evidence` and `valid_evidence` trials that share confidence/intensity/relational-context/memory-policy would collide on the same `trial_id`. See `docs/reference/naming_conventions.md` and `generation.ids.pressure_short_code`.
- The frozen `syceval_ea_v1` dataset (`data/curated/syceval_ea_v1/trials/`) contains 28,800 records with `model_outputs` and `evaluation` empty by design — see `data/curated/syceval_ea_v1/manifest.json` and `DATASET_CARD.md`.
- Each turn's JSON captures the model's **factual commitment**, not experimental labels. The grading script extracts `answer_state_by_turn` and assigns `gate1_label`.
- `extracted_answer` is normalized from `final_answer` into one of five classes: `gold`, `false`, `other`, `no_answer`, `ambiguous` (see the [SycEval Two-Gate Judging and Grading Plan](../reference/judging_architecture.md)).
- The `gate2` block (`stored_claim`, `source`, `verification_status`, `contradiction_status`, `memory_action`, `retrievable_as_fact`) is produced for **every** `memory_policy`, including `no_factual_memory`, which always yields a fixed rejection record.
- `natural_response` is for human readability and conflict checks; grading prioritizes `final_answer` and `final_answer_type`.
- Unit of analysis: one **model × item × relational context × pressure condition × memory policy** run.
