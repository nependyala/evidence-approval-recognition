"""Tests for deterministic Gate 2 memory-policy logic."""

import json
from pathlib import Path

import pytest

from coding.enums import (
    EvidenceStatus,
    MemoryAction,
    MemoryPolicy,
    MemorySource,
    VerificationStatus,
)
from coding.trial import Trial
from memory.policies import (
    build_reference_memory_state,
    build_reference_typed_memory,
    facts_conflict,
    write_naive_summary,
    write_no_memory,
)

FIXTURES = Path(__file__).resolve().parents[1] / "data" / "fixtures"


def _load_example() -> dict:
    return json.loads((FIXTURES / "example_trial.json").read_text(encoding="utf-8"))


def _valid_evidence_example() -> dict:
    data = _load_example()
    data["hidden_metadata"]["evidence_status"] = "valid_evidence"
    data["hidden_metadata"]["valid_updated_fact"] = "Portland"
    data["hidden_metadata"]["should_update_answer"] = True
    data["hidden_metadata"]["should_overwrite_verified_fact"] = True
    data["hidden_metadata"]["expected_evidence_level"] = "valid_evidence"
    data["hidden_metadata"]["expected_verification_status"] = "verified"
    return data


def test_facts_conflict_detects_contradiction() -> None:
    assert facts_conflict("Portland", "Seattle") is True


def test_facts_conflict_ignores_substring_and_case() -> None:
    assert facts_conflict("Seattle", "Seattle, WA") is False
    assert facts_conflict("seattle", "Seattle") is False


def test_facts_conflict_empty_is_false() -> None:
    assert facts_conflict("", "Seattle") is False


def test_reference_typed_memory_for_unsupported_trial() -> None:
    trial = Trial.model_validate(_load_example())
    record = build_reference_typed_memory(trial)
    assert record.claim == "Portland"
    assert record.source == MemorySource.USER_ASSERTION
    assert record.evidence_level == EvidenceStatus.UNSUPPORTED
    assert record.verification_status == VerificationStatus.UNVERIFIED
    assert record.contradicts_prior_source is True
    assert record.prior_verified_fact == "Seattle"
    assert record.memory_action == MemoryAction.DO_NOT_OVERWRITE
    assert record.allowed_for_retrieval_as_fact is False


def test_reference_typed_memory_for_valid_evidence_trial() -> None:
    trial = Trial.model_validate(_valid_evidence_example())
    record = build_reference_typed_memory(trial)
    assert record.claim == "Portland"
    assert record.source == MemorySource.EVIDENCE_UPDATE
    assert record.evidence_level == EvidenceStatus.VALID_EVIDENCE
    assert record.verification_status == VerificationStatus.VERIFIED
    assert record.memory_action == MemoryAction.STORE_VERIFIED_UPDATE
    assert record.allowed_for_retrieval_as_fact is True


def test_write_no_memory_is_empty() -> None:
    state = write_no_memory("bio_0042_secure_bare_assertion_no_mem")
    assert state.memory_policy == MemoryPolicy.NO_MEMORY
    assert state.naive_record is None
    assert state.typed_record is None


def test_write_naive_summary_wraps_text() -> None:
    state = write_naive_summary("bio_0042_secure_bare_assertion_naive", "note")
    assert state.naive_record is not None
    assert state.naive_record.summary_text == "note"


def test_build_reference_memory_state_rejects_naive_policy() -> None:
    data = _load_example()
    data["hidden_metadata"]["memory_policy"] = "naive_summary"
    trial = Trial.model_validate(data)
    with pytest.raises(ValueError, match="naive_summary"):
        build_reference_memory_state(trial)


def test_build_reference_memory_state_typed_policy() -> None:
    data = _load_example()
    data["hidden_metadata"]["memory_policy"] = "epistemically_typed_memory"
    trial = Trial.model_validate(data)
    state = build_reference_memory_state(trial)
    assert state.memory_policy == MemoryPolicy.EPISTEMICALLY_TYPED_MEMORY
    assert state.typed_record is not None
