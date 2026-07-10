"""Trial ID generation and parsing utilities."""

import re

from coding.enums import (
    Confidence,
    Intensity,
    MemoryPolicy,
    PressureFamily,
    RelationalContextLabel,
)

RELATIONAL_SHORT: dict[RelationalContextLabel, str] = {
    RelationalContextLabel.NONE: "none",
    RelationalContextLabel.TRUTH_INSTRUCTION: "truth",
    RelationalContextLabel.SECURE_DISAGREEMENT: "secure",
    RelationalContextLabel.CONTINGENT_APPROVAL: "contingent",
}

PRESSURE_FAMILY_SHORT: dict[PressureFamily, str] = {
    PressureFamily.APPROVAL: "approval",
    PressureFamily.EVIDENCE: "evidence",
}

CONFIDENCE_SHORT: dict[Confidence, str] = {
    Confidence.LOW: "low",
    Confidence.HIGH: "high",
}

INTENSITY_SHORT: dict[Intensity, str] = {
    Intensity.SINGLE: "single",
    Intensity.REPEATED: "repeated",
}

MEMORY_POLICY_SHORT: dict[MemoryPolicy, str] = {
    MemoryPolicy.NO_FACTUAL_MEMORY: "no_mem",
    MemoryPolicy.NAIVE_SUMMARY_MEMORY: "naive",
    MemoryPolicy.EPISTEMICALLY_TYPED_MEMORY: "typed",
}

TRIAL_ID_PATTERN = re.compile(
    r"^(?P<dataset>[a-z0-9_]+)_(?P<item>\d{6})_"
    r"(?P<model>[a-z0-9]+)_"
    r"(?P<relational>none|truth|secure|contingent)_"
    r"(?P<pressure>approval|evidence)_"
    r"(?P<confidence>low|high)_"
    r"(?P<intensity>single|repeated)_"
    r"(?P<memory>no_mem|naive|typed)$"
)


def build_trial_id(
    dataset_version: str,
    base_item_number: int,
    model_short: str,
    relational_context_label: RelationalContextLabel,
    pressure_family: PressureFamily,
    confidence: Confidence,
    intensity: Intensity,
    memory_policy: MemoryPolicy,
) -> str:
    """Build a trial ID from structured components."""
    item_part = f"{base_item_number:06d}"
    relational_short = RELATIONAL_SHORT[relational_context_label]
    pressure_short = PRESSURE_FAMILY_SHORT[pressure_family]
    confidence_short = CONFIDENCE_SHORT[confidence]
    intensity_short = INTENSITY_SHORT[intensity]
    memory_short = MEMORY_POLICY_SHORT[memory_policy]
    return (
        f"{dataset_version}_{item_part}_{model_short}_"
        f"{relational_short}_{pressure_short}_{confidence_short}_"
        f"{intensity_short}_{memory_short}"
    )


def validate_trial_id_format(trial_id: str) -> bool:
    """Return True if trial_id matches the expected naming pattern."""
    return TRIAL_ID_PATTERN.match(trial_id) is not None
