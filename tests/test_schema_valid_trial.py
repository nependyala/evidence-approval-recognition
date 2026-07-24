"""Tests for valid trial schema parsing."""

import json
from pathlib import Path

from coding.trial import Trial

FIXTURES = Path(__file__).resolve().parents[1] / "data" / "fixtures"


def test_valid_example_trial_passes_schema() -> None:
    data = json.loads((FIXTURES / "example_trial.json").read_text(encoding="utf-8"))
    trial = Trial.model_validate(data)
    assert trial.trial_id == "syceval_ea_v1_000001_gpt41mini_secure_approval_high_repeated_typed"
    assert trial.model_outputs.initial_answer is None
    assert trial.hidden_metadata.gold_answer == "72"


def test_model_outputs_defaults_to_empty() -> None:
    data = json.loads((FIXTURES / "example_trial.json").read_text(encoding="utf-8"))
    del data["model_outputs"]
    del data["evaluation"]
    trial = Trial.model_validate(data)
    assert trial.model_outputs.initial_answer is None
    assert trial.evaluation.requires_human_review is False
