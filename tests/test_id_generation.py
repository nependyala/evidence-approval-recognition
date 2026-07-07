"""Tests for trial ID generation."""

from coding.enums import (
    Domain,
    MemoryPolicy,
    PushbackCondition,
    RelationalContext,
)
from generation.ids import build_trial_id, validate_trial_id_format


def test_build_example_trial_id() -> None:
    trial_id = build_trial_id(
        Domain.SYNTHETIC_BIOGRAPHY,
        42,
        RelationalContext.SECURE_DISAGREEMENT,
        PushbackCondition.BARE_ASSERTION,
        MemoryPolicy.NAIVE_SUMMARY,
    )
    assert trial_id == "bio_0042_secure_bare_assertion_naive"


def test_validate_trial_id_format() -> None:
    assert validate_trial_id_format("bio_0042_secure_bare_assertion_naive")
    assert not validate_trial_id_format("invalid_trial_id")
