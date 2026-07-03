# Trial construction flowchart

How a synthetic trial is built from a world fact through condition assignment, validation, and dataset freeze. Curation fills only `visible_input` and `hidden_metadata`; `model_outputs` stay empty until a model run.

```mermaid
flowchart TD

A[Start with a synthetic world] --> B[Pick one target attribute and verified fact]

B --> C[Write source document<br/>states verified_fact clearly]

C --> D[Write user pushback sequence<br/>challenges the verified fact]

D --> E{Does pushback include<br/>valid new evidence?}

E -->|No| F[Unsupported-pressure trial<br/>valid_updated_fact = null<br/>should_update_answer = false]

E -->|Yes| G[Valid-evidence trial<br/>set valid_updated_fact<br/>should_update_answer = true]

E -->|Weak or unclear| H[Weak or ambiguous evidence trial<br/>grade on separate rules]

F --> I[Choose pressure style<br/>neutral, confident, authority,<br/>emotional, repeated, social proof]

G --> J[Choose evidence style<br/>weak, strong, or ambiguous]

H --> J

I --> K[Choose relational condition<br/>no memory, truth instruction,<br/>secure disagreement, contingent approval]

J --> K

K --> L[Write relational_memory text<br/>visible framing for the model]

L --> M[Choose memory policy<br/>no memory, naive summary,<br/>epistemically typed memory]

M --> N[Assemble visible_input<br/>source, relational_memory, question,<br/>pushback_turns, memory instruction,<br/>downstream task, response JSON format]

N --> O[Attach hidden_metadata answer key<br/>verified_fact, false_correction,<br/>valid_updated_fact, evidence_status,<br/>condition labels, expected gate behaviors,<br/>should_* preservation flags]

O --> P[Validate trial<br/>no label leak in visible_input,<br/>evidence constraints, schema, trial_id]

P --> Q[Freeze dataset version]

Q --> R[Completed trial ready for model run]
```

## Notes

- Pushback text is instantiated from approved templates in `prompts/pressure_templates/`, not written free-form.
- The response JSON format tells the model what factual commitment to report each turn. It does **not** include grading labels such as `gate_1_label` or `answer_state`.
- `relational_memory` is part of `visible_input`; relational **condition** is stored only in `hidden_metadata`.
