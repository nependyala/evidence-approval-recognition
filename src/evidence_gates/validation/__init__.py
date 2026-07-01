"""Trial validation package."""

from evidence_gates.validation.validator import (
    validate_trial_dict,
    validate_trial_directory,
    validate_trial_file,
)

__all__ = [
    "validate_trial_dict",
    "validate_trial_directory",
    "validate_trial_file",
]
