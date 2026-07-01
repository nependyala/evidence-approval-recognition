"""Tests for trial ID generation."""

from coding.enums import (
    Domain,
    MemoryPolicy,
    PushbackCondition,
    RelationalCondition,
)
from generation.ids import build_trial_id, validate_trial_id_format


def test_build_example_trial_id() -> None:
    trial_id = build_trial_id(
        Domain.SYNTHETIC_BIOGRAPHY,
        42,
        RelationalCondition.SECURE_DISAGREEMENT_MEMORY,
        PushbackCondition.CONFIDENT_FALSE,
        MemoryPolicy.NAIVE_SUMMARY,
    )
    assert trial_id == "bio_0042_secure_confident_false_naive"


def test_validate_trial_id_format() -> None:
    assert validate_trial_id_format("bio_0042_secure_confident_false_naive")
    assert not validate_trial_id_format("invalid_trial_id")
