"""Tests for invalid trial schema parsing."""

import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from coding.trial import Trial

FIXTURES = Path(__file__).resolve().parents[1] / "data" / "fixtures"


def test_missing_hidden_metadata_fails_schema() -> None:
    data = json.loads(
        (FIXTURES / "invalid_trial_missing_hidden_field.json").read_text(encoding="utf-8")
    )
    with pytest.raises(ValidationError):
        Trial.model_validate(data)
