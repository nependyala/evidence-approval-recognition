"""Template rendering helpers."""

from pathlib import Path
from typing import Any

from evidence_gates.templates.loader import load_template_file, render_template_entry


def render_template_from_file(
    template_path: Path,
    template_id: str,
    variables: dict[str, Any],
) -> str:
    """Render a specific template entry from a YAML template file."""
    data = load_template_file(template_path)
    for entry in data["templates"]:
        if entry["template_id"] == template_id:
            return render_template_entry(entry, variables)
    msg = f"template_id '{template_id}' not found in {template_path}"
    raise ValueError(msg)


def render_first_template(template_path: Path, variables: dict[str, Any]) -> str:
    """Render the first template entry in a YAML template file."""
    data = load_template_file(template_path)
    return render_template_entry(data["templates"][0], variables)
