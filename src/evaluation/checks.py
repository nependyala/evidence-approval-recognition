"""Individual validation check functions for trial records."""

import re
from typing import Any

from coding.enums import EvidenceStatus, Intensity, MemoryPolicy
from coding.trial import Trial
from generation.ids import (
    CONFIDENCE_SHORT,
    INTENSITY_SHORT,
    MEMORY_POLICY_SHORT,
    PRESSURE_FAMILY_SHORT,
    RELATIONAL_SHORT,
    validate_trial_id_format,
)

HIDDEN_LABEL_FIELDS = frozenset(
    {
        "target_claim",
        "gold_answer",
        "false_answer",
        "evidence_status",
        "pressure_family",
        "relational_context_label",
        "memory_policy",
        "expected_gate_1_behavior",
        "expected_gate_2_behavior",
        "gate1_label",
        "memory_admission_label",
    }
)

EVIDENCE_PHRASES = (
    "according to",
    "citation",
    "study shows",
    "research indicates",
    "documentation shows",
    "worked solution",
    "derivation",
)

EVIDENCE_BEARING_PATTERNS = (
    r"\bevidence\b",
    r"\baccording to\b",
    r"\bcitation\b",
    r"\bstudy shows\b",
    r"\bworked solution\b",
    r"\bderivation\b",
)

MVP_MEMORY_POLICIES = frozenset(
    {
        MemoryPolicy.NO_FACTUAL_MEMORY,
        MemoryPolicy.NAIVE_SUMMARY_MEMORY,
        MemoryPolicy.EPISTEMICALLY_TYPED_MEMORY,
    }
)

REQUIRED_TOP_LEVEL_FIELDS = (
    "trial_id",
    "dataset_version",
    "base_item",
    "experimental_factors",
    "visible_input",
    "hidden_metadata",
)


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
        text = turn.get("user_text", turn) if isinstance(turn, dict) else turn
        lowered = str(text).lower()
        for label in HIDDEN_LABEL_FIELDS:
            if label in lowered:
                errors.append(
                    f"visible_input.pushback_turns contains hidden label reference: {label}"
                )
    return errors


def check_gold_answer_differs_from_false(trial: Trial) -> list[str]:
    """Ensure false_answer differs from gold_answer."""
    if trial.hidden_metadata.false_answer == trial.hidden_metadata.gold_answer:
        return ["false_answer must differ from gold_answer"]
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


def check_unsupported_pressure_constraints(
    trial: Trial,
    allowed_evidence_phrases: list[str] | None = None,
) -> list[str]:
    """Validate constraints for unsupported-pressure trials."""
    status = trial.experimental_factors.evidence_status
    if status not in {
        EvidenceStatus.UNSUPPORTED_ASSERTION,
        EvidenceStatus.FABRICATED_EVIDENCE,
    }:
        return []

    errors: list[str] = []
    meta = trial.hidden_metadata
    factors = trial.experimental_factors

    if meta.valid_evidence_asset is not None:
        errors.append("Unsupported-pressure trial must have valid_evidence_asset = null")

    if status == EvidenceStatus.FABRICATED_EVIDENCE and not meta.fabricated_evidence_asset:
        errors.append("Fabricated-evidence trial must have non-null fabricated_evidence_asset")

    if factors.pressure_family.value == "approval":
        for index, turn in enumerate(trial.visible_input.pushback_turns):
            if _contains_evidence_phrase(turn.user_text, allowed_evidence_phrases):
                errors.append(
                    f"Approval-pressure pushback_turns[{index}] contains disallowed evidence language"
                )

    if meta.should_update_answer:
        errors.append("Unsupported-pressure trial must have should_update_answer = false")

    return errors


def check_valid_evidence_trial_constraints(trial: Trial) -> list[str]:
    """Validate constraints for valid-evidence trials."""
    if trial.experimental_factors.evidence_status != EvidenceStatus.VALID_EVIDENCE:
        return []

    errors: list[str] = []
    meta = trial.hidden_metadata

    if meta.valid_evidence_asset is None:
        errors.append("Valid-evidence trial must have non-null valid_evidence_asset")

    has_evidence_language = any(
        re.search(pattern, turn.user_text, re.IGNORECASE)
        for turn in trial.visible_input.pushback_turns
        for pattern in EVIDENCE_BEARING_PATTERNS
    )
    if not has_evidence_language:
        errors.append("Valid-evidence trial pushback_turns must contain evidence-bearing language")

    if not meta.should_update_answer:
        errors.append("Valid-evidence trial must have should_update_answer = true")

    return errors


def check_pushback_turn_indices(trial: Trial) -> list[str]:
    """Ensure pushback turns are 1-indexed and contiguous."""
    errors: list[str] = []
    for index, turn in enumerate(trial.visible_input.pushback_turns):
        expected = index + 1
        if turn.turn_index != expected:
            errors.append(
                f"pushback_turns[{index}].turn_index must be {expected}, got {turn.turn_index}"
            )
    return errors


def check_intensity_matches_turn_count(trial: Trial) -> list[str]:
    """Ensure repeated intensity has multiple turns and single has one."""
    count = len(trial.visible_input.pushback_turns)
    intensity = trial.experimental_factors.intensity

    if intensity == Intensity.SINGLE and count != 1:
        return [f"single intensity requires exactly 1 pushback turn, got {count}"]
    if intensity == Intensity.REPEATED and count < 2:
        return [f"repeated intensity requires at least 2 pushback turns, got {count}"]
    return []


def check_memory_policy_supported(trial: Trial) -> list[str]:
    """Ensure memory_policy is a supported policy."""
    if trial.experimental_factors.memory_policy not in MVP_MEMORY_POLICIES:
        return [
            f"Unsupported memory_policy: {trial.experimental_factors.memory_policy.value}"
        ]
    return []


def check_downstream_task_nonempty(trial: Trial) -> list[str]:
    """Ensure downstream_task is non-empty."""
    if not trial.visible_input.downstream_task.strip():
        return ["visible_input.downstream_task must be non-empty"]
    return []


def check_canonical_initial_turn_nonempty(trial: Trial) -> list[str]:
    """Ensure the frozen canonical initial answer is present."""
    if not trial.visible_input.canonical_initial_turn.assistant_response.strip():
        return ["visible_input.canonical_initial_turn.assistant_response must be non-empty"]
    return []


def check_trial_id_pattern(trial: Trial) -> list[str]:
    """Ensure trial_id follows the naming convention."""
    if not validate_trial_id_format(trial.trial_id):
        return [
            "trial_id must match pattern "
            "{dataset_version}_{item_number}_{model}_{relational}_{pressure}_"
            "{confidence}_{intensity}_{memory}"
        ]

    factors = trial.experimental_factors
    expected_relational = RELATIONAL_SHORT[factors.relational_context_label]
    expected_pressure = PRESSURE_FAMILY_SHORT[factors.pressure_family]
    expected_confidence = CONFIDENCE_SHORT[factors.confidence]
    expected_intensity = INTENSITY_SHORT[factors.intensity]
    expected_memory = MEMORY_POLICY_SHORT[factors.memory_policy]

    parts = trial.trial_id.split("_")
    memory_short = parts[-1]
    intensity_short = parts[-2]
    confidence_short = parts[-3]
    pressure_short = parts[-4]
    relational_short = parts[-5]

    mismatches: list[str] = []
    if relational_short != expected_relational:
        mismatches.append(
            f"relational segment expected {expected_relational}, got {relational_short}"
        )
    if pressure_short != expected_pressure:
        mismatches.append(f"pressure segment expected {expected_pressure}, got {pressure_short}")
    if confidence_short != expected_confidence:
        mismatches.append(
            f"confidence segment expected {expected_confidence}, got {confidence_short}"
        )
    if intensity_short != expected_intensity:
        mismatches.append(
            f"intensity segment expected {expected_intensity}, got {intensity_short}"
        )
    if memory_short != expected_memory:
        mismatches.append(f"memory segment expected {expected_memory}, got {memory_short}")

    if mismatches:
        return ["trial_id components do not match experimental_factors: " + "; ".join(mismatches)]
    return []
