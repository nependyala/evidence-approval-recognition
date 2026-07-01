"""Individual validation check functions for trial records."""

import re
from typing import Any

from coding.enums import (
    EvidenceStatus,
    ExpectedEvidenceLevel,
    ExpectedVerificationStatus,
    MemoryPolicy,
    TurnStructure,
)
from coding.trial import Trial
from generation.ids import (
    DOMAIN_SHORT,
    MEMORY_POLICY_SHORT,
    PUSHBACK_SHORT,
    RELATIONAL_SHORT,
    validate_trial_id_format,
)

HIDDEN_LABEL_FIELDS = frozenset(
    {
        "domain",
        "verified_fact",
        "false_correction",
        "evidence_status",
        "pushback_condition",
        "relational_condition",
        "memory_policy",
        "expected_gate_1_behavior",
        "expected_gate_2_behavior",
    }
)

EVIDENCE_PHRASES = (
    "updated source",
    "verified record",
    "evidence",
    "audit",
    "new record",
    "documentation shows",
)

EVIDENCE_BEARING_PATTERNS = (
    r"\bevidence\b",
    r"\bverified record\b",
    r"\bupdated source\b",
    r"\bnew record\b",
    r"\baudit\b",
    r"\bdocumentation shows\b",
)

MVP_MEMORY_POLICIES = frozenset(
    {
        MemoryPolicy.NO_MEMORY,
        MemoryPolicy.NAIVE_SUMMARY,
        MemoryPolicy.EPISTEMICALLY_TYPED_MEMORY,
    }
)

REQUIRED_TOP_LEVEL_FIELDS = ("trial_id", "dataset_version", "visible_input", "hidden_metadata")


def check_required_top_level_fields(data: dict[str, Any]) -> list[str]:
    """Ensure curation-stage required top-level fields exist."""
    errors: list[str] = []
    for field in REQUIRED_TOP_LEVEL_FIELDS:
        if field not in data:
            errors.append(f"Missing required top-level field: {field}")
    return errors


def check_visible_input_no_label_leak(visible_input: dict[str, Any]) -> list[str]:
    """Ensure visible_input does not contain hidden evaluator labels."""
    errors: list[str] = []
    for key in visible_input:
        if key in HIDDEN_LABEL_FIELDS:
            errors.append(f"visible_input leaks hidden label field: {key}")
    for turn in visible_input.get("pushback_turns", []):
        lowered = turn.lower()
        for label in HIDDEN_LABEL_FIELDS:
            if label in lowered:
                errors.append(
                    f"visible_input.pushback_turns contains hidden label reference: {label}"
                )
    return errors


def check_verified_fact_in_source(trial: Trial) -> list[str]:
    """Ensure verified_fact appears in the source document."""
    if trial.hidden_metadata.verified_fact not in trial.visible_input.source_document:
        return ["verified_fact does not appear in visible_input.source_document"]
    return []


def check_false_correction_differs(trial: Trial) -> list[str]:
    """Ensure false_correction differs from verified_fact."""
    if trial.hidden_metadata.false_correction == trial.hidden_metadata.verified_fact:
        return ["false_correction must differ from verified_fact"]
    return []


def _contains_evidence_phrase(text: str, allowed_phrases: list[str] | None = None) -> bool:
    lowered = text.lower()
    allowed = {phrase.lower() for phrase in (allowed_phrases or [])}
    for phrase in EVIDENCE_PHRASES:
        if phrase in allowed:
            continue
        if phrase in lowered:
            return True
    return False


def check_unsupported_trial_constraints(
    trial: Trial,
    allowed_evidence_phrases: list[str] | None = None,
) -> list[str]:
    """Validate constraints for unsupported-evidence trials."""
    if trial.hidden_metadata.evidence_status != EvidenceStatus.UNSUPPORTED:
        return []

    errors: list[str] = []
    meta = trial.hidden_metadata

    if meta.valid_updated_fact is not None:
        errors.append("Unsupported trial must have valid_updated_fact = null")

    for index, turn in enumerate(trial.visible_input.pushback_turns):
        if _contains_evidence_phrase(turn, allowed_evidence_phrases):
            errors.append(
                f"Unsupported trial pushback_turns[{index}] contains disallowed evidence language"
            )

    if meta.should_update_answer:
        errors.append("Unsupported trial must have should_update_answer = false")

    if meta.should_overwrite_verified_fact:
        errors.append("Unsupported trial must have should_overwrite_verified_fact = false")

    return errors


def check_valid_evidence_trial_constraints(trial: Trial) -> list[str]:
    """Validate constraints for valid-evidence trials."""
    if trial.hidden_metadata.evidence_status != EvidenceStatus.VALID_EVIDENCE:
        return []

    errors: list[str] = []
    meta = trial.hidden_metadata

    if meta.valid_updated_fact is None:
        errors.append("Valid-evidence trial must have non-null valid_updated_fact")

    has_evidence_language = any(
        re.search(pattern, turn, re.IGNORECASE)
        for turn in trial.visible_input.pushback_turns
        for pattern in EVIDENCE_BEARING_PATTERNS
    )
    if not has_evidence_language:
        errors.append("Valid-evidence trial pushback_turns must contain evidence-bearing language")

    if not meta.should_update_answer:
        errors.append("Valid-evidence trial must have should_update_answer = true")

    if meta.expected_evidence_level != ExpectedEvidenceLevel.VALID_EVIDENCE:
        errors.append("Valid-evidence trial must have expected_evidence_level = valid_evidence")

    if meta.expected_verification_status != ExpectedVerificationStatus.VERIFIED:
        errors.append("Valid-evidence trial must have expected_verification_status = verified")

    return errors


def check_pressure_turn_count(trial: Trial) -> list[str]:
    """Ensure pressure_turn_count matches pushback_turns length."""
    actual = len(trial.visible_input.pushback_turns)
    expected = trial.hidden_metadata.pressure_turn_count
    if expected != actual:
        return [f"pressure_turn_count ({expected}) must equal len(pushback_turns) ({actual})"]
    return []


def check_turn_structure(trial: Trial) -> list[str]:
    """Ensure turn_structure matches pushback turn count."""
    count = len(trial.visible_input.pushback_turns)
    expected = TurnStructure.SINGLE_TURN if count == 1 else TurnStructure.MULTI_TURN
    if trial.hidden_metadata.turn_structure != expected:
        return [
            f"turn_structure must be {expected.value} for {count} pushback turn(s), "
            f"got {trial.hidden_metadata.turn_structure.value}"
        ]
    return []


def check_memory_policy_supported(trial: Trial) -> list[str]:
    """Ensure memory_policy is a supported MVP policy."""
    if trial.hidden_metadata.memory_policy not in MVP_MEMORY_POLICIES:
        return [f"Unsupported memory_policy: {trial.hidden_metadata.memory_policy.value}"]
    return []


def check_downstream_task_nonempty(trial: Trial) -> list[str]:
    """Ensure downstream_task is non-empty."""
    if not trial.visible_input.downstream_task.strip():
        return ["visible_input.downstream_task must be non-empty"]
    return []


def check_provenance_fields(trial: Trial) -> list[str]:
    """Ensure template and generator provenance fields are present."""
    errors: list[str] = []
    meta = trial.hidden_metadata
    for field_name in ("template_id", "paraphrase_id", "generator_id", "random_seed"):
        value = getattr(meta, field_name)
        if not str(value).strip():
            errors.append(f"hidden_metadata.{field_name} must be present")
    return errors


def check_trial_id_pattern(trial: Trial) -> list[str]:
    """Ensure trial_id follows the naming convention."""
    if not validate_trial_id_format(trial.trial_id):
        return [
            "trial_id must match pattern "
            "{domain_short}_{entity_number}_{relational_short}_{pushback_short}_{memory_short}"
        ]

    meta = trial.hidden_metadata
    expected_domain = DOMAIN_SHORT[meta.domain]
    expected_relational = RELATIONAL_SHORT[meta.relational_condition]
    expected_pushback = PUSHBACK_SHORT[meta.pushback_condition]
    expected_memory = MEMORY_POLICY_SHORT[meta.memory_policy]

    parts = trial.trial_id.split("_")
    memory_short = parts[-1]
    relational_short = parts[2]
    domain_short = parts[0]
    entity_part = parts[1]
    pushback_short = "_".join(parts[3:-1])

    mismatches: list[str] = []
    if domain_short != expected_domain:
        mismatches.append(f"domain segment expected {expected_domain}, got {domain_short}")
    if relational_short != expected_relational:
        mismatches.append(
            f"relational segment expected {expected_relational}, got {relational_short}"
        )
    if pushback_short != expected_pushback:
        mismatches.append(f"pushback segment expected {expected_pushback}, got {pushback_short}")
    if memory_short != expected_memory:
        mismatches.append(f"memory segment expected {expected_memory}, got {memory_short}")
    if not re.fullmatch(r"\d{4}", entity_part):
        mismatches.append(f"entity segment must be four digits, got {entity_part}")

    if mismatches:
        return ["trial_id components do not match hidden_metadata: " + "; ".join(mismatches)]
    return []
