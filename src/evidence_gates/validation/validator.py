"""Trial validation orchestration."""

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml
from pydantic import ValidationError

from evidence_gates.schemas.trial import Trial
from evidence_gates.schemas.validation_report import ValidationReport
from evidence_gates.validation import checks


def _load_validation_config(config_path: Path | None = None) -> dict[str, Any]:
    if config_path is None:
        config_path = Path("configs/validation.yaml")
    if not config_path.exists():
        return {}
    with config_path.open(encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    return data if isinstance(data, dict) else {}


def validate_trial_dict(
    data: dict[str, Any],
    config: dict[str, Any] | None = None,
) -> ValidationReport:
    """Validate a trial dictionary and return a structured report."""
    config = config or _load_validation_config()
    allowed_phrases = config.get("allowed_evidence_phrases_in_unsupported", [])

    trial_id = str(data.get("trial_id", "unknown"))
    errors: list[str] = []
    warnings: list[str] = []

    errors.extend(checks.check_required_top_level_fields(data))

    visible_input = data.get("visible_input")
    if isinstance(visible_input, dict):
        errors.extend(checks.check_visible_input_no_label_leak(visible_input))
    elif "visible_input" in data:
        errors.append("visible_input must be an object")

    try:
        trial = Trial.model_validate(data)
    except ValidationError as exc:
        for issue in exc.errors():
            location = ".".join(str(part) for part in issue["loc"])
            errors.append(f"{location}: {issue['msg']}")
        return ValidationReport(
            trial_id=trial_id,
            is_valid=False,
            errors=errors,
            warnings=warnings,
            checked_at=datetime.now(UTC),
        )

    check_functions = [
        checks.check_verified_fact_in_source,
        checks.check_false_correction_differs,
        lambda t: checks.check_unsupported_trial_constraints(t, allowed_phrases),
        checks.check_valid_evidence_trial_constraints,
        checks.check_pressure_turn_count,
        checks.check_turn_structure,
        checks.check_memory_policy_supported,
        checks.check_downstream_task_nonempty,
        checks.check_provenance_fields,
        checks.check_trial_id_pattern,
    ]

    for check_fn in check_functions:
        errors.extend(check_fn(trial))

    return ValidationReport(
        trial_id=trial.trial_id,
        is_valid=len(errors) == 0,
        errors=errors,
        warnings=warnings,
        checked_at=datetime.now(UTC),
    )


def validate_trial_file(path: Path, config: dict[str, Any] | None = None) -> ValidationReport:
    """Validate a trial JSON file."""
    with path.open(encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        return ValidationReport(
            trial_id=path.stem,
            is_valid=False,
            errors=["Trial file must contain a JSON object"],
            warnings=[],
            checked_at=datetime.now(UTC),
        )
    return validate_trial_dict(data, config=config)


def validate_trial_directory(
    directory: Path,
    config: dict[str, Any] | None = None,
) -> list[ValidationReport]:
    """Validate all JSON trial files in a directory."""
    reports: list[ValidationReport] = []
    for path in sorted(directory.glob("*.json")):
        reports.append(validate_trial_file(path, config=config))
    return reports
