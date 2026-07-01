"""Tests for custom validation checks."""

import json
from pathlib import Path

from evaluation.validator import validate_trial_dict, validate_trial_file

FIXTURES = Path(__file__).resolve().parents[1] / "data" / "fixtures"
ROOT = Path(__file__).resolve().parents[1]


def _load_example() -> dict:
    return json.loads((FIXTURES / "example_trial.json").read_text(encoding="utf-8"))


def test_valid_example_passes_custom_checks() -> None:
    report = validate_trial_file(FIXTURES / "example_trial.json")
    assert report.is_valid, report.errors


def test_missing_hidden_metadata_fails() -> None:
    report = validate_trial_file(FIXTURES / "invalid_trial_missing_hidden_field.json")
    assert not report.is_valid
    assert any("hidden_metadata" in error for error in report.errors)


def test_label_leak_fails() -> None:
    report = validate_trial_file(FIXTURES / "invalid_trial_label_leak.json")
    assert not report.is_valid
    assert any("leak" in error.lower() or "label" in error.lower() for error in report.errors)


def test_verified_fact_missing_from_source_fails() -> None:
    data = _load_example()
    data["hidden_metadata"]["verified_fact"] = "Austin"
    report = validate_trial_dict(data)
    assert not report.is_valid
    assert any("verified_fact" in error for error in report.errors)


def test_unsupported_trial_with_evidence_language_fails() -> None:
    data = _load_example()
    data["visible_input"]["pushback_turns"] = [
        "The verified record shows Portland."
    ]
    data["hidden_metadata"]["pressure_turn_count"] = 1
    data["hidden_metadata"]["turn_structure"] = "single_turn"
    report = validate_trial_dict(data)
    assert not report.is_valid
    assert any("evidence language" in error for error in report.errors)


def test_valid_evidence_without_valid_updated_fact_fails() -> None:
    data = _load_example()
    data["hidden_metadata"]["evidence_status"] = "valid_evidence"
    data["hidden_metadata"]["valid_updated_fact"] = None
    data["hidden_metadata"]["should_update_answer"] = True
    data["hidden_metadata"]["expected_evidence_level"] = "valid_evidence"
    data["hidden_metadata"]["expected_verification_status"] = "verified"
    data["visible_input"]["pushback_turns"] = [
        "The verified record shows Portland."
    ]
    data["hidden_metadata"]["pressure_turn_count"] = 1
    data["hidden_metadata"]["turn_structure"] = "single_turn"
    report = validate_trial_dict(data)
    assert not report.is_valid
    assert any("valid_updated_fact" in error for error in report.errors)


def test_pressure_turn_count_mismatch_fails() -> None:
    data = _load_example()
    data["hidden_metadata"]["pressure_turn_count"] = 5
    report = validate_trial_dict(data)
    assert not report.is_valid
    assert any("pressure_turn_count" in error for error in report.errors)
