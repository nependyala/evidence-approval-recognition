"""Pressure-condition manifest: maps each of the 12 (pressure_family,
evidence_status, confidence, intensity) combinations in the Augmentation
Plan's experimental-factors table to concrete YAML pressure templates,
a `pressure_template_id` (docs/reference/naming_conventions.md format), and the
closest legacy SycEval rebuttal-tier analog (preserved as legacy metadata
per the Augmentation Plan's "Rebuttal-strength ladder" row).

Approval-pressure wording rotates across five unsupported-assertion template
families (by base_item_number) for stylistic diversity across items; evidence
conditions use the dedicated valid/fabricated x confidence template pairs.
"""

from __future__ import annotations

from pathlib import Path

PROMPTS_DIR = Path(__file__).resolve().parent.parent / "prompts" / "pressure_templates"

APPROVAL_HIGH_FAMILIES = [
    "confident_false",
    "authority_false",
    "emotional_false",
    "social_proof_false",
    "repeated_false",
]


def _family_file(family: str) -> Path:
    return PROMPTS_DIR / f"{family}.yaml"


def approval_low_family(_item_number: int) -> str:
    return "neutral_false"


def approval_high_family(item_number: int) -> str:
    return APPROVAL_HIGH_FAMILIES[item_number % len(APPROVAL_HIGH_FAMILIES)]


PRESSURE_CONDITIONS = [
    {
        "key": "approval_low_single",
        "pressure_family": "approval",
        "evidence_status": "unsupported_assertion",
        "confidence": "low",
        "intensity": "single",
        "condition_label": "approval_pressure",
        "pressure_template_id": "approval_low_single_v01",
        "legacy_rebuttal_tier": "simple",
        "family_fn": approval_low_family,
        "num_turns": 1,
    },
    {
        "key": "approval_low_repeated",
        "pressure_family": "approval",
        "evidence_status": "unsupported_assertion",
        "confidence": "low",
        "intensity": "repeated",
        "condition_label": "approval_pressure",
        "pressure_template_id": "approval_low_repeated_v01",
        "legacy_rebuttal_tier": "simple",
        "family_fn": approval_low_family,
        "num_turns": 3,
    },
    {
        "key": "approval_high_single",
        "pressure_family": "approval",
        "evidence_status": "unsupported_assertion",
        "confidence": "high",
        "intensity": "single",
        "condition_label": "approval_pressure",
        "pressure_template_id": "approval_high_single_v01",
        "legacy_rebuttal_tier": "ethos",
        "family_fn": approval_high_family,
        "num_turns": 1,
    },
    {
        "key": "approval_high_repeated",
        "pressure_family": "approval",
        "evidence_status": "unsupported_assertion",
        "confidence": "high",
        "intensity": "repeated",
        "condition_label": "approval_pressure",
        "pressure_template_id": "approval_high_repeated_v01",
        "legacy_rebuttal_tier": "ethos",
        "family_fn": approval_high_family,
        "num_turns": 3,
    },
    {
        "key": "fabricated_low_single",
        "pressure_family": "evidence",
        "evidence_status": "fabricated_evidence",
        "confidence": "low",
        "intensity": "single",
        "condition_label": "fabricated_evidence_pressure",
        "pressure_template_id": "evidence_fabricated_low_single_v01",
        "legacy_rebuttal_tier": "justification",
        "family_fn": lambda _n: "fabricated_uncertain",
        "num_turns": 1,
    },
    {
        "key": "fabricated_low_repeated",
        "pressure_family": "evidence",
        "evidence_status": "fabricated_evidence",
        "confidence": "low",
        "intensity": "repeated",
        "condition_label": "fabricated_evidence_pressure",
        "pressure_template_id": "evidence_fabricated_low_repeated_v01",
        "legacy_rebuttal_tier": "justification",
        "family_fn": lambda _n: "fabricated_uncertain",
        "num_turns": 3,
    },
    {
        "key": "fabricated_high_single",
        "pressure_family": "evidence",
        "evidence_status": "fabricated_evidence",
        "confidence": "high",
        "intensity": "single",
        "condition_label": "fabricated_evidence_pressure",
        "pressure_template_id": "evidence_fabricated_high_single_v01",
        "legacy_rebuttal_tier": "justification",
        "family_fn": lambda _n: "fabricated_confident",
        "num_turns": 1,
    },
    {
        "key": "fabricated_high_repeated",
        "pressure_family": "evidence",
        "evidence_status": "fabricated_evidence",
        "confidence": "high",
        "intensity": "repeated",
        "condition_label": "fabricated_evidence_pressure",
        "pressure_template_id": "evidence_fabricated_high_repeated_v01",
        "legacy_rebuttal_tier": "justification",
        "family_fn": lambda _n: "fabricated_confident",
        "num_turns": 3,
    },
    {
        "key": "valid_low_single",
        "pressure_family": "evidence",
        "evidence_status": "valid_evidence",
        "confidence": "low",
        "intensity": "single",
        "condition_label": "valid_evidence_pressure",
        "pressure_template_id": "evidence_valid_low_single_v01",
        "legacy_rebuttal_tier": "citation",
        "family_fn": lambda _n: "weak_evidence",
        "num_turns": 1,
    },
    {
        "key": "valid_low_repeated",
        "pressure_family": "evidence",
        "evidence_status": "valid_evidence",
        "confidence": "low",
        "intensity": "repeated",
        "condition_label": "valid_evidence_pressure",
        "pressure_template_id": "evidence_valid_low_repeated_v01",
        "legacy_rebuttal_tier": "citation",
        "family_fn": lambda _n: "weak_evidence",
        "num_turns": 3,
    },
    {
        "key": "valid_high_single",
        "pressure_family": "evidence",
        "evidence_status": "valid_evidence",
        "confidence": "high",
        "intensity": "single",
        "condition_label": "valid_evidence_pressure",
        "pressure_template_id": "evidence_valid_high_single_v01",
        "legacy_rebuttal_tier": "citation",
        "family_fn": lambda _n: "strong_evidence",
        "num_turns": 1,
    },
    {
        "key": "valid_high_repeated",
        "pressure_family": "evidence",
        "evidence_status": "valid_evidence",
        "confidence": "high",
        "intensity": "repeated",
        "condition_label": "valid_evidence_pressure",
        "pressure_template_id": "evidence_valid_high_repeated_v01",
        "legacy_rebuttal_tier": "citation",
        "family_fn": lambda _n: "strong_evidence",
        "num_turns": 3,
    },
]


def build_pushback_texts(condition: dict, item_number: int, base_item: dict) -> list[str]:
    """Render `condition["num_turns"]` pushback-turn texts for one base item."""
    from generation.templates.renderer import render_template_from_file  # noqa: PLC0415

    family = condition["family_fn"](item_number)
    template_path = _family_file(family)
    evidence_status = condition["evidence_status"]

    if evidence_status == "valid_evidence":
        variables = {
            "valid_updated_fact": base_item["gold_answer"],
            "evidence_snippet": base_item["valid_evidence_asset"],
        }
    elif evidence_status == "fabricated_evidence":
        variables = {
            "false_correction": base_item["false_answer"],
            "fabricated_evidence_snippet": base_item["fabricated_evidence_asset"],
        }
    else:
        variables = {"false_correction": base_item["false_answer"]}

    texts = []
    for turn_offset in range(condition["num_turns"]):
        if condition["num_turns"] == 1:
            variant = (item_number % 3) + 1
        else:
            variant = turn_offset + 1
        template_id = f"{family}_{variant:03d}"
        texts.append(render_template_from_file(template_path, template_id, variables))
    return texts
