# Memory writer prompts

Full prompts used to elicit a **memory record** from a model after a Gate 1
interaction, one per Gate 2 memory policy.

These are distinct from `prompts/memory_instructions/`, which holds the short
in-trial instruction line placed in `visible_input.memory_instruction`. The
files here are the standalone writer prompts a runner sends to the model at the
memory-write step.

| Policy | Writer prompt | Output |
|---|---|---|
| `no_memory` | (none) | No memory is written |
| `naive_summary` | `naive_summary_writer.txt` | Free text |
| `epistemically_typed_memory` | `typed_memory_writer.txt` | JSON: a typed memory record whose shape is defined by the prompt itself |

> **Note:** the earlier Gate-2 memory implementation under `src/memory/`
> (`audit.py`, `policies.py`, `retrieval.py`, `schema.py`) — including the
> `TypedMemoryRecord` schema this prompt used to reference — was removed when the
> Evidence/Approval regrounding dropped the `verified_fact` / `MemoryPolicy.NO_MEMORY`
> concepts it depended on. The `typed_memory_writer.txt` prompt is self-contained
> (it specifies its own JSON fields) and does not import that schema. Re-porting a
> typed-memory schema/validator onto the new taxonomy is tracked separately in
> issue #11.

Placeholders use `{name}` and are rendered with the same
`generation.templates.loader.render_template_text` helper used for pressure
templates. Available placeholders: `{source_document}`, `{question}`,
`{conversation_transcript}`.
