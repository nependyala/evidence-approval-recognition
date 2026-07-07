"""Trial ID generation and parsing utilities."""

import re

from coding.enums import (
    Domain,
    MemoryPolicy,
    PushbackCondition,
    RelationalContext,
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

RELATIONAL_SHORT: dict[RelationalContext, str] = {
    RelationalContext.NONE: "none",
    RelationalContext.TRUTH_INSTRUCTION: "truth",
    RelationalContext.SECURE_DISAGREEMENT: "secure",
    RelationalContext.CONTINGENT_APPROVAL: "contingent",
}

PUSHBACK_SHORT: dict[PushbackCondition, str] = {
    PushbackCondition.NO_PRESSURE: "no_pressure",
    PushbackCondition.BARE_ASSERTION: "bare_assertion",
    PushbackCondition.APPROVAL: "approval",
    PushbackCondition.FABRICATED_EVIDENCE: "fabricated_evidence",
    PushbackCondition.VALID_EVIDENCE: "valid_evidence",
    PushbackCondition.WEAK_EVIDENCE: "weak_evidence",
    PushbackCondition.AMBIGUOUS_EVIDENCE: "ambiguous_evidence",
    PushbackCondition.AUTHORITY: "authority",
}

MEMORY_POLICY_SHORT: dict[MemoryPolicy, str] = {
    MemoryPolicy.NO_MEMORY: "no_mem",
    MemoryPolicy.NAIVE_SUMMARY: "naive",
    MemoryPolicy.EPISTEMICALLY_TYPED_MEMORY: "typed",
}

# Modifiers (user_confidence, intensity) are intentionally NOT encoded in the
# trial_id; they live in hidden_metadata. The id stays a stable key rather than a
# serialization of every attribute.
TRIAL_ID_PATTERN = re.compile(
    r"^(?P<domain>[a-z]+)_(?P<entity>\d{4})_"
    r"(?P<relational>none|truth|secure|contingent)_"
    r"(?P<pushback>no_pressure|bare_assertion|approval|fabricated_evidence|"
    r"valid_evidence|weak_evidence|ambiguous_evidence|authority)_"
    r"(?P<memory>no_mem|naive|typed)$"
)


def build_trial_id(
    domain: Domain,
    entity_number: int,
    relational_context: RelationalContext,
    pushback_condition: PushbackCondition,
    memory_policy: MemoryPolicy,
) -> str:
    """Build a trial ID from structured components."""
    domain_short = DOMAIN_SHORT[domain]
    entity_part = f"{entity_number:04d}"
    relational_short = RELATIONAL_SHORT[relational_context]
    pushback_short = PUSHBACK_SHORT[pushback_condition]
    memory_short = MEMORY_POLICY_SHORT[memory_policy]
    return f"{domain_short}_{entity_part}_{relational_short}_{pushback_short}_{memory_short}"


def validate_trial_id_format(trial_id: str) -> bool:
    """Return True if trial_id matches the expected naming pattern."""
    return TRIAL_ID_PATTERN.match(trial_id) is not None
