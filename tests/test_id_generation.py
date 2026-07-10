"""Tests for trial ID generation."""

from coding.enums import (
    Confidence,
    Intensity,
    MemoryPolicy,
    PressureFamily,
    RelationalContextLabel,
)
from generation.ids import build_trial_id, validate_trial_id_format


def test_build_example_trial_id() -> None:
    trial_id = build_trial_id(
        "syceval_ea_v1",
        1,
        "gpt41mini",
        RelationalContextLabel.SECURE_DISAGREEMENT,
        PressureFamily.APPROVAL,
        Confidence.HIGH,
        Intensity.REPEATED,
        MemoryPolicy.EPISTEMICALLY_TYPED_MEMORY,
    )
    assert trial_id == "syceval_ea_v1_000001_gpt41mini_secure_approval_high_repeated_typed"


def test_validate_trial_id_format() -> None:
    assert validate_trial_id_format(
        "syceval_ea_v1_000001_gpt41mini_secure_approval_high_repeated_typed"
    )
    assert not validate_trial_id_format("invalid_trial_id")
