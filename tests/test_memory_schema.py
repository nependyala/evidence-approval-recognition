"""Tests for memory record schemas and policy/record consistency."""

import pytest
from pydantic import ValidationError

from coding.enums import (
    EvidenceStatus,
    MemoryAction,
    MemoryPolicy,
    MemorySource,
    VerificationStatus,
)
from memory.schema import MemoryState, NaiveMemoryRecord, TypedMemoryRecord


def _typed_record() -> TypedMemoryRecord:
    return TypedMemoryRecord(
        claim="Portland",
        source=MemorySource.USER_ASSERTION,
        evidence_level=EvidenceStatus.UNSUPPORTED,
        verification_status=VerificationStatus.UNVERIFIED,
        contradicts_prior_source=True,
        prior_verified_fact="Seattle",
        memory_action=MemoryAction.DO_NOT_OVERWRITE,
        allowed_for_retrieval_as_fact=False,
    )


def test_typed_record_rejects_unknown_source() -> None:
    with pytest.raises(ValidationError):
        TypedMemoryRecord.model_validate(
            {
                "claim": "Portland",
                "source": "wikipedia",
                "evidence_level": "unsupported",
                "verification_status": "unverified",
                "contradicts_prior_source": True,
                "prior_verified_fact": "Seattle",
                "memory_action": "do_not_overwrite",
                "allowed_for_retrieval_as_fact": False,
            }
        )


def test_typed_record_forbids_extra_fields() -> None:
    with pytest.raises(ValidationError):
        TypedMemoryRecord.model_validate(
            {
                "claim": "Portland",
                "source": "user assertion",
                "evidence_level": "unsupported",
                "verification_status": "unverified",
                "contradicts_prior_source": True,
                "prior_verified_fact": "Seattle",
                "memory_action": "do_not_overwrite",
                "allowed_for_retrieval_as_fact": False,
                "confidence": 0.9,
            }
        )


def test_no_memory_state_rejects_records() -> None:
    with pytest.raises(ValidationError):
        MemoryState(
            trial_id="bio_0042_secure_bare_assertion_no_mem",
            memory_policy=MemoryPolicy.NO_MEMORY,
            naive_record=NaiveMemoryRecord(summary_text="x"),
        )


def test_naive_state_requires_naive_record() -> None:
    with pytest.raises(ValidationError):
        MemoryState(
            trial_id="bio_0042_secure_bare_assertion_naive",
            memory_policy=MemoryPolicy.NAIVE_SUMMARY,
        )


def test_typed_state_requires_typed_record() -> None:
    with pytest.raises(ValidationError):
        MemoryState(
            trial_id="bio_0042_secure_bare_assertion_typed",
            memory_policy=MemoryPolicy.EPISTEMICALLY_TYPED_MEMORY,
        )


def test_typed_state_round_trip() -> None:
    state = MemoryState(
        trial_id="bio_0042_secure_bare_assertion_typed",
        memory_policy=MemoryPolicy.EPISTEMICALLY_TYPED_MEMORY,
        typed_record=_typed_record(),
    )
    restored = MemoryState.model_validate_json(state.model_dump_json())
    assert restored == state
