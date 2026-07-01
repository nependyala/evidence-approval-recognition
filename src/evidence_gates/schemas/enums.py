"""Enumerations for trial metadata and expected behaviors."""

from enum import StrEnum


class Domain(StrEnum):
    SYNTHETIC_BIOGRAPHY = "synthetic_biography"
    COMPANY_POLICY_RECORDS = "company_policy_records"
    CALENDAR_SCHEDULING_FACTS = "calendar_scheduling_facts"
    USER_PROFILE_FACTS = "user_profile_facts"
    TABLE_BASED_RECORDS = "table_based_records"
    TASK_RULES = "task_rules"
    ORGANIZATIONAL_RECORDS = "organizational_records"


class RelationalCondition(StrEnum):
    NO_MEMORY = "no_memory"
    TRUTH_INSTRUCTION = "truth_instruction"
    SECURE_DISAGREEMENT_MEMORY = "secure_disagreement_memory"
    CONTINGENT_APPROVAL_MEMORY = "contingent_approval_memory"


class PushbackCondition(StrEnum):
    NEUTRAL_FALSE = "neutral_false"
    CONFIDENT_FALSE = "confident_false"
    AUTHORITY_FALSE = "authority_false"
    EMOTIONAL_FALSE = "emotional_false"
    REPEATED_FALSE = "repeated_false"
    SOCIAL_PROOF_FALSE = "social_proof_false"
    WEAK_EVIDENCE = "weak_evidence"
    STRONG_EVIDENCE = "strong_evidence"
    AMBIGUOUS_EVIDENCE = "ambiguous_evidence"


class EvidenceStatus(StrEnum):
    UNSUPPORTED = "unsupported"
    WEAK_EVIDENCE = "weak_evidence"
    VALID_EVIDENCE = "valid_evidence"
    AMBIGUOUS_EVIDENCE = "ambiguous_evidence"


class MemoryPolicy(StrEnum):
    NO_MEMORY = "no_memory"
    NAIVE_SUMMARY = "naive_summary"
    EPISTEMICALLY_TYPED_MEMORY = "epistemically_typed_memory"


class TurnStructure(StrEnum):
    SINGLE_TURN = "single_turn"
    MULTI_TURN = "multi_turn"


class ExpectedGate1Behavior(StrEnum):
    HOLD = "hold"
    REVISE = "revise"
    UNCERTAIN_OR_ASK_FOR_EVIDENCE = "uncertain_or_ask_for_evidence"


class ExpectedGate2Behavior(StrEnum):
    REJECT_OR_STORE_DISPUTED = "reject_or_store_disputed"
    STORE_VERIFIED_UPDATE = "store_verified_update"
    NO_MEMORY_WRITE = "no_memory_write"


class ExpectedVerificationStatus(StrEnum):
    VERIFIED = "verified"
    UNVERIFIED = "unverified"
    DISPUTED = "disputed"
    NOT_APPLICABLE = "not_applicable"


class ExpectedEvidenceLevel(StrEnum):
    UNSUPPORTED = "unsupported"
    WEAK_EVIDENCE = "weak_evidence"
    VALID_EVIDENCE = "valid_evidence"
    AMBIGUOUS_EVIDENCE = "ambiguous_evidence"
    NOT_APPLICABLE = "not_applicable"


class MemoryAction(StrEnum):
    DO_NOT_OVERWRITE = "do_not_overwrite"
    STORE_AS_DISPUTED_CLAIM = "store_as_disputed_claim"
    STORE_VERIFIED_UPDATE = "store_verified_update"
    NO_ACTION = "no_action"
