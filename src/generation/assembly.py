"""Trial assembly helpers for curation scaffolding."""

from coding.trial import BaseItem, ExperimentalFactors, HiddenMetadata, Trial, VisibleInput


def assemble_trial(
    trial_id: str,
    dataset_version: str,
    base_item: BaseItem,
    experimental_factors: ExperimentalFactors,
    visible_input: VisibleInput,
    hidden_metadata: HiddenMetadata,
) -> Trial:
    """Assemble a curation-stage trial without model outputs or evaluation."""
    return Trial(
        trial_id=trial_id,
        dataset_version=dataset_version,
        base_item=base_item,
        experimental_factors=experimental_factors,
        visible_input=visible_input,
        hidden_metadata=hidden_metadata,
    )
