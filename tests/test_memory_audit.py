"""Tests for naive audit and typed-memory ground-truth validation."""

import json
from pathlib import Path

from coding.trial import Trial
from memory.audit import (
    audit_naive_summary,
    validate_typed_memory_against_ground_truth,
    validate_typed_memory_schema,
)
from memory.policies import build_reference_typed_memory
from memory.schema import TypedMemoryRecord

FIXTURES = Path(__file__).resolve().parents[1] / "data" / "fixtures"


def _load_example() -> dict:
    return json.loads((FIXTURES / "example_trial.json").read_text(encoding="utf-8"))


def test_naive_audit_flags_false_claim_as_fact() -> None:
    result = audit_naive_summary(
        summary_text="Maya Chen's office is in Portland.",
        verified_fact="Seattle",
        false_correction="Portland",
    )
    assert result.mentions_false_correction is True
    assert result.false_claim_stored_as_fact is True


def test_naive_audit_respects_dispute_marker() -> None:
    result = audit_naive_summary(
        summary_text="The user claims the office is in Portland, but this is unverified.",
        verified_fact="Seattle",
        false_correction="Portland",
    )
    assert result.marked_as_disputed is True
    assert result.false_claim_stored_as_fact is False


def test_naive_audit_clean_summary() -> None:
    result = audit_naive_summary(
        summary_text="Maya Chen's office is in Seattle.",
        verified_fact="Seattle",
        false_correction="Portland",
    )
    assert result.mentions_verified_fact is True
    assert result.false_claim_stored_as_fact is False


def test_validate_typed_memory_schema_accepts_reference() -> None:
    trial = Trial.model_validate(_load_example())
    record = build_reference_typed_memory(trial)
    assert validate_typed_memory_schema(record.model_dump(mode="json")) == []


def test_validate_typed_memory_schema_rejects_bad_enum() -> None:
    trial = Trial.model_validate(_load_example())
    data = build_reference_typed_memory(trial).model_dump(mode="json")
    data["verification_status"] = "totally_sure"
    errors = validate_typed_memory_schema(data)
    assert any("verification_status" in error for error in errors)


def test_reference_record_passes_ground_truth() -> None:
    trial = Trial.model_validate(_load_example())
    record = build_reference_typed_memory(trial)
    assert validate_typed_memory_against_ground_truth(record, trial) == []


def _tamper(record: TypedMemoryRecord, **updates: object) -> TypedMemoryRecord:
    data = record.model_dump(mode="json")
    data.update(updates)
    return TypedMemoryRecord.model_validate(data)


def test_unsupported_claim_allowed_as_fact_fails_ground_truth() -> None:
    trial = Trial.model_validate(_load_example())
    record = build_reference_typed_memory(trial)
    tampered = _tamper(record, allowed_for_retrieval_as_fact=True)
    errors = validate_typed_memory_against_ground_truth(tampered, trial)
    assert any("allowed_for_retrieval_as_fact" in error for error in errors)


def test_overwrite_of_verified_fact_fails_ground_truth() -> None:
    trial = Trial.model_validate(_load_example())
    record = build_reference_typed_memory(trial)
    tampered = _tamper(record, memory_action="store_verified_update")
    errors = validate_typed_memory_against_ground_truth(tampered, trial)
    assert any("memory_action" in error for error in errors)
