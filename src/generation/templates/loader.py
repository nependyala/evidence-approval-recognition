"""YAML template loading utilities."""

import re
from pathlib import Path
from typing import Any

import yaml

PLACEHOLDER_PATTERN = re.compile(r"\{([a-zA-Z_][a-zA-Z0-9_]*)\}")

REQUIRED_TEMPLATE_FILE_FIELDS = (
    "template_family",
    "evidence_status",
    "allowed_for_mvp",
    "templates",
)

REQUIRED_TEMPLATE_ENTRY_FIELDS = ("template_id", "text")

VALID_EVIDENCE_STATUSES = frozenset({"valid_evidence", "weak_evidence", "ambiguous_evidence"})

VALID_EVIDENCE_REQUIRED_PLACEHOLDERS = frozenset({"evidence_snippet", "valid_updated_fact"})


class TemplateLoadError(ValueError):
    """Raised when a template file fails structural validation."""


class TemplateRenderError(ValueError):
    """Raised when template rendering fails due to missing variables."""


def load_template_file(path: Path) -> dict[str, Any]:
    """Load and validate a pressure template YAML file."""
    with path.open(encoding="utf-8") as handle:
        data = yaml.safe_load(handle)

    if not isinstance(data, dict):
        msg = f"Template file must be a mapping: {path}"
        raise TemplateLoadError(msg)

    for field in REQUIRED_TEMPLATE_FILE_FIELDS:
        if field not in data:
            raise TemplateLoadError(f"Missing required field '{field}' in {path}")

    templates = data.get("templates")
    if not isinstance(templates, list) or not templates:
        raise TemplateLoadError(f"'templates' must be a non-empty list in {path}")

    evidence_status = str(data["evidence_status"])
    for index, entry in enumerate(templates):
        if not isinstance(entry, dict):
            raise TemplateLoadError(f"templates[{index}] must be a mapping in {path}")
        for field in REQUIRED_TEMPLATE_ENTRY_FIELDS:
            if field not in entry:
                raise TemplateLoadError(f"templates[{index}] missing '{field}' in {path}")

        placeholders = extract_placeholders(str(entry["text"]))
        if evidence_status in VALID_EVIDENCE_STATUSES:
            missing = VALID_EVIDENCE_REQUIRED_PLACEHOLDERS - placeholders
            if missing:
                raise TemplateLoadError(
                    f"templates[{index}] missing required placeholders for evidence template: "
                    f"{sorted(missing)}"
                )

    return data


def extract_placeholders(text: str) -> set[str]:
    """Extract placeholder variable names from template text."""
    return set(PLACEHOLDER_PATTERN.findall(text))


def render_template_text(text: str, variables: dict[str, Any]) -> str:
    """Render a template string with the provided variables."""
    placeholders = extract_placeholders(text)
    missing = placeholders - set(variables.keys())
    if missing:
        raise TemplateRenderError(
            f"Missing required template variables: {sorted(missing)}"
        )

    def replace(match: re.Match[str]) -> str:
        key = match.group(1)
        return str(variables[key])

    return PLACEHOLDER_PATTERN.sub(replace, text)


def render_template_entry(entry: dict[str, Any], variables: dict[str, Any]) -> str:
    """Render a single template entry from a loaded template file."""
    return render_template_text(str(entry["text"]), variables)
