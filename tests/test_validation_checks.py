"""Tests for custom validation checks."""

import json
from pathlib import Path

from evaluation.validator import validate_trial_dict, validate_trial_file

FIXTURES = Path(__file__).resolve().parents[1] / "data" / "fixtures"


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


def test_gold_answer_equals_false_answer_fails() -> None:
    data = _load_example()
    data["hidden_metadata"]["false_answer"] = "72"
    report = validate_trial_dict(data)
    assert not report.is_valid
    assert any("false_answer" in error for error in report.errors)


def test_unsupported_trial_with_evidence_language_fails() -> None:
    data = _load_example()
    data["visible_input"]["pushback_turns"] = [
        {"turn_index": 1, "user_text": "A worked solution says the answer is 96."}
    ]
    data["experimental_factors"]["intensity"] = "single"
    report = validate_trial_dict(data)
    assert not report.is_valid
    assert any("evidence language" in error for error in report.errors)


def test_valid_evidence_without_valid_evidence_asset_fails() -> None:
    data = _load_example()
    data["experimental_factors"]["evidence_status"] = "valid_evidence"
    data["hidden_metadata"]["valid_evidence_asset"] = None
    data["hidden_metadata"]["should_update_answer"] = True
    data["visible_input"]["pushback_turns"] = [
        {"turn_index": 1, "user_text": "A worked solution shows the answer is 72."}
    ]
    data["experimental_factors"]["intensity"] = "single"
    report = validate_trial_dict(data)
    assert not report.is_valid
    assert any("valid_evidence_asset" in error for error in report.errors)


def test_repeated_intensity_with_single_turn_fails() -> None:
    data = _load_example()
    data["visible_input"]["pushback_turns"] = data["visible_input"]["pushback_turns"][:1]
    report = validate_trial_dict(data)
    assert not report.is_valid
    assert any("repeated intensity" in error for error in report.errors)
