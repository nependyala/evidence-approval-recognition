"""Tests for YAML template loading and rendering."""

from pathlib import Path

import pytest
import yaml

from generation.templates.loader import (
    TemplateLoadError,
    TemplateRenderError,
    load_template_file,
    render_template_text,
)

ROOT = Path(__file__).resolve().parents[1]
PRESSURE_DIR = ROOT / "prompts" / "pressure_templates"


def test_load_confident_false_template() -> None:
    data = load_template_file(PRESSURE_DIR / "confident_false.yaml")
    assert data["template_family"] == "confident_false"
    assert len(data["templates"]) >= 1


def test_load_strong_evidence_requires_placeholders() -> None:
    data = load_template_file(PRESSURE_DIR / "strong_evidence.yaml")
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


def test_all_pressure_templates_load() -> None:
    yaml_files = sorted(PRESSURE_DIR.glob("*.yaml"))
    assert yaml_files, "expected pressure template files"
    for path in yaml_files:
        load_template_file(path)


def test_unknown_evidence_status_rejected(tmp_path: Path) -> None:
    bad = tmp_path / "bad.yaml"
    bad.write_text(
        yaml.safe_dump(
            {
                "template_family": "bad",
                "evidence_status": "not_a_real_status",
                "allowed_for_mvp": True,
                "templates": [{"template_id": "bad_001", "text": "It is {false_correction}."}],
            }
        ),
        encoding="utf-8",
    )
    with pytest.raises(TemplateLoadError, match="Invalid evidence_status"):
        load_template_file(bad)


def test_fabricated_template_requires_placeholders(tmp_path: Path) -> None:
    bad = tmp_path / "fab.yaml"
    bad.write_text(
        yaml.safe_dump(
            {
                "template_family": "fabricated_confident",
                "evidence_status": "fabricated_evidence",
                "allowed_for_mvp": True,
                # Missing {fabricated_evidence_snippet}.
                "templates": [{"template_id": "fab_001", "text": "It is {false_correction}."}],
            }
        ),
        encoding="utf-8",
    )
    with pytest.raises(TemplateLoadError, match="fabricated_evidence_snippet"):
        load_template_file(bad)
