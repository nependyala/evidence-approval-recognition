# Documentation

Docs for the SycEval-augmented two-gate benchmark. Start here if you're looking for a specific note.

## Layout

| Folder | What's in it |
| --- | --- |
| [`reference/`](reference/) | Stable specs: schema, naming, curation protocol, judging architecture, dataset-card template |
| [`theory/`](theory/) | Design rationale: pressure taxonomy, relational interventions |
| [`audit/`](audit/) | Freeze-review process: action items, human audit checklist |
| [`findings/`](findings/) | Pilot / scout notes (not publication results) |
| [`flowcharts/`](flowcharts/) | Mermaid overviews of trial construction, record shape, and grading |

## Quick links

### Reference
- [Schema reference](reference/schema_reference.md) — trial JSON fields
- [Naming conventions](reference/naming_conventions.md) — IDs and version strings
- [Curation protocol](reference/curation_protocol.md) — how trials are built and frozen
- [Judging architecture](reference/judging_architecture.md) — grading pipeline implementation spec
- [Dataset card template](reference/dataset_card_template.md) — fill when freezing a curated version

### Theory
- [Pressure taxonomy](theory/pressure_taxonomy.md) — evidence vs approval channels at Gate 1
- [Relational interventions](theory/relational_interventions_and_the_dispositional_axis.md) — dispositional axis and secure-base framing

### Audit / freeze
- [Action items](audit/action_items.md) — `syceval_ea_v1` freeze-review brief
- [Human audit checklist](audit/human_audit_checklist.md) — pre-freeze review checklist + sign-off
- [Human audit sample trials](audit/human_audit_sample_trials.md) — 48-trial stratified rendered-trial reading list
- [Weekly summary (Jul 17–23, 2026)](audit/weekly_summary_2026-07-23.md) — one-pager on the freeze + hardening pass

### Findings
- [Authority deference finding](findings/authority_deference_finding.md) — scout result on authority as a dissociable channel
- [Notebook pilot findings](findings/notebook_pilot_findings.md) — pre-dataset probe notebook notes

### Flowcharts
- [Trial construction](flowcharts/01-trial-construction.md)
- [Trial record structure](flowcharts/02-trial-record-structure.md)
- [Grading pipeline](flowcharts/03-grading-pipeline.md)

## Related (outside `docs/`)

- Frozen dataset card: [`data/curated/syceval_ea_v1/DATASET_CARD.md`](../data/curated/syceval_ea_v1/DATASET_CARD.md)
- Repo overview: [`README.md`](../README.md)
