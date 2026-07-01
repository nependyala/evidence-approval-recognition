"""Trial ID generation and parsing utilities."""

import re

from evidence_gates.schemas.enums import (
    Domain,
    MemoryPolicy,
    PushbackCondition,
    RelationalCondition,
)

DOMAIN_SHORT: dict[Domain, str] = {
    Domain.SYNTHETIC_BIOGRAPHY: "bio",
    Domain.COMPANY_POLICY_RECORDS: "policy",
    Domain.CALENDAR_SCHEDULING_FACTS: "calendar",
    Domain.USER_PROFILE_FACTS: "profile",
    Domain.TABLE_BASED_RECORDS: "table",
    Domain.TASK_RULES: "rules",
    Domain.ORGANIZATIONAL_RECORDS: "org",
}

RELATIONAL_SHORT: dict[RelationalCondition, str] = {
    RelationalCondition.NO_MEMORY: "no_mem",
    RelationalCondition.TRUTH_INSTRUCTION: "truth",
    RelationalCondition.SECURE_DISAGREEMENT_MEMORY: "secure",
    RelationalCondition.CONTINGENT_APPROVAL_MEMORY: "contingent",
}

PUSHBACK_SHORT: dict[PushbackCondition, str] = {
    PushbackCondition.NEUTRAL_FALSE: "neutral_false",
    PushbackCondition.CONFIDENT_FALSE: "confident_false",
    PushbackCondition.AUTHORITY_FALSE: "authority_false",
    PushbackCondition.EMOTIONAL_FALSE: "emotional_false",
    PushbackCondition.REPEATED_FALSE: "repeated_false",
    PushbackCondition.SOCIAL_PROOF_FALSE: "social_proof_false",
    PushbackCondition.WEAK_EVIDENCE: "weak_evidence",
    PushbackCondition.STRONG_EVIDENCE: "strong_evidence",
    PushbackCondition.AMBIGUOUS_EVIDENCE: "ambiguous_evidence",
}

MEMORY_POLICY_SHORT: dict[MemoryPolicy, str] = {
    MemoryPolicy.NO_MEMORY: "no_mem",
    MemoryPolicy.NAIVE_SUMMARY: "naive",
    MemoryPolicy.EPISTEMICALLY_TYPED_MEMORY: "typed",
}

TRIAL_ID_PATTERN = re.compile(
    r"^(?P<domain>[a-z]+)_(?P<entity>\d{4})_"
    r"(?P<relational>no_mem|truth|secure|contingent)_"
    r"(?P<pushback>neutral_false|confident_false|authority_false|emotional_false|"
    r"repeated_false|social_proof_false|weak_evidence|strong_evidence|ambiguous_evidence)_"
    r"(?P<memory>no_mem|naive|typed)$"
)


def build_trial_id(
    domain: Domain,
    entity_number: int,
    relational_condition: RelationalCondition,
    pushback_condition: PushbackCondition,
    memory_policy: MemoryPolicy,
) -> str:
    """Build a trial ID from structured components."""
    domain_short = DOMAIN_SHORT[domain]
    entity_part = f"{entity_number:04d}"
    relational_short = RELATIONAL_SHORT[relational_condition]
    pushback_short = PUSHBACK_SHORT[pushback_condition]
    memory_short = MEMORY_POLICY_SHORT[memory_policy]
    return f"{domain_short}_{entity_part}_{relational_short}_{pushback_short}_{memory_short}"


def validate_trial_id_format(trial_id: str) -> bool:
    """Return True if trial_id matches the expected naming pattern."""
    return TRIAL_ID_PATTERN.match(trial_id) is not None
