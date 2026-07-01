"""Trial assembly helpers for curation scaffolding."""

from coding.trial import HiddenMetadata, Trial, VisibleInput


def assemble_trial(
    trial_id: str,
    dataset_version: str,
    visible_input: VisibleInput,
    hidden_metadata: HiddenMetadata,
) -> Trial:
    """Assemble a curation-stage trial without model outputs."""
    return Trial(
        trial_id=trial_id,
        dataset_version=dataset_version,
        visible_input=visible_input,
        hidden_metadata=hidden_metadata,
    )
