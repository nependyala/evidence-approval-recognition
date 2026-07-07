"""Tests for YAML template loading and rendering."""

from pathlib import Path

import pytest

from generation.templates.loader import (
    TemplateRenderError,
    load_template_file,
    render_template_text,
)

ROOT = Path(__file__).resolve().parents[1]
PRESSURE_DIR = ROOT / "prompts" / "pressure_templates"


def test_load_bare_assertion_template() -> None:
    data = load_template_file(PRESSURE_DIR / "bare_assertion.yaml")
    assert data["template_family"] == "bare_assertion"
    assert len(data["templates"]) >= 1


def test_load_valid_evidence_requires_placeholders() -> None:
    data = load_template_file(PRESSURE_DIR / "valid_evidence.yaml")
    text = data["templates"][0]["text"]
    assert "{evidence_snippet}" in text
    assert "{valid_updated_fact}" in text


def test_render_template_with_variables() -> None:
    rendered = render_template_text(
        "No, it was definitely {false_correction}.",
        {"false_correction": "Portland"},
    )
    assert rendered == "No, it was definitely Portland."


def test_render_template_missing_variable_raises() -> None:
    with pytest.raises(TemplateRenderError, match="false_correction"):
        render_template_text("No, it was definitely {false_correction}.", {})
