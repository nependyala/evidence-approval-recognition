"""Tests for valid trial schema parsing."""

import json
from pathlib import Path

from coding.trial import Trial

FIXTURES = Path(__file__).resolve().parents[1] / "data" / "fixtures"


def test_valid_example_trial_passes_schema() -> None:
    data = json.loads((FIXTURES / "example_trial.json").read_text(encoding="utf-8"))
    trial = Trial.model_validate(data)
    assert trial.trial_id == "bio_0042_secure_bare_assertion_naive"
    assert trial.model_outputs == {}
    assert trial.hidden_metadata.verified_fact == "Seattle"


def test_model_outputs_defaults_to_empty() -> None:
    data = json.loads((FIXTURES / "example_trial.json").read_text(encoding="utf-8"))
    del data["model_outputs"]
    trial = Trial.model_validate(data)
    assert trial.model_outputs == {}
