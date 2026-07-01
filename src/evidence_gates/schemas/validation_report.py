"""Validation report schema."""

from datetime import datetime

from pydantic import BaseModel, Field


class ValidationReport(BaseModel):
    """Result of validating a single trial record."""

    trial_id: str
    is_valid: bool
    errors: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    checked_at: datetime
