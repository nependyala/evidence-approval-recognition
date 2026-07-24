"""Trial ID generation and parsing utilities."""

import re

from coding.enums import (
    Confidence,
    EvidenceStatus,
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

# pressure_family alone is ambiguous for PressureFamily.EVIDENCE, which spans
# two distinct evidence_status conditions (fabricated_evidence, valid_evidence)
# -- without this, both conditions would collide on the same trial_id (see
# docs/reference/naming_conventions.md). Bare "evidence" is kept only as a fallback for
# callers that do not pass evidence_status.
EVIDENCE_PRESSURE_SHORT: dict[EvidenceStatus, str] = {
    EvidenceStatus.FABRICATED_EVIDENCE: "evidence-fab",
    EvidenceStatus.VALID_EVIDENCE: "evidence-valid",
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
    r"(?P<pressure>approval|evidence-fab|evidence-valid|evidence)_"
    r"(?P<confidence>low|high)_"
    r"(?P<intensity>single|repeated)_"
    r"(?P<memory>no_mem|naive|typed)$"
)


def pressure_short_code(
    pressure_family: PressureFamily, evidence_status: EvidenceStatus | None = None
) -> str:
    """Return the trial_id short code for a (pressure_family, evidence_status)
    pair, disambiguating the two EVIDENCE-family conditions.
    """
    if pressure_family == PressureFamily.EVIDENCE and evidence_status in EVIDENCE_PRESSURE_SHORT:
        return EVIDENCE_PRESSURE_SHORT[evidence_status]
    return PRESSURE_FAMILY_SHORT[pressure_family]


def build_trial_id(
    dataset_version: str,
    base_item_number: int,
    model_short: str,
    relational_context_label: RelationalContextLabel,
    pressure_family: PressureFamily,
    confidence: Confidence,
    intensity: Intensity,
    memory_policy: MemoryPolicy,
    evidence_status: EvidenceStatus | None = None,
) -> str:
    """Build a trial ID from structured components."""
    item_part = f"{base_item_number:06d}"
    relational_short = RELATIONAL_SHORT[relational_context_label]
    pressure_short = pressure_short_code(pressure_family, evidence_status)
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
