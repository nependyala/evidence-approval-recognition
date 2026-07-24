"""Enumerations for trial metadata and expected behaviors."""

from enum import StrEnum


class SourceDataset(StrEnum):
    AMPS = "AMPS"
    MEDQUAD = "MedQuAD"


class LegacyContextMode(StrEnum):
    IN_CONTEXT = "in_context"
    PREEMPTIVE = "preemptive"


class RelationalContextLabel(StrEnum):
    NONE = "none"
    TRUTH_INSTRUCTION = "truth_instruction"
    SECURE_DISAGREEMENT = "secure_disagreement"
    CONTINGENT_APPROVAL = "contingent_approval"


class PressureFamily(StrEnum):
    APPROVAL = "approval"
    EVIDENCE = "evidence"


class Confidence(StrEnum):
    LOW = "low"
    HIGH = "high"


class Intensity(StrEnum):
    SINGLE = "single"
    REPEATED = "repeated"


class EvidenceStatus(StrEnum):
    UNSUPPORTED_ASSERTION = "unsupported_assertion"
    FABRICATED_EVIDENCE = "fabricated_evidence"
    VALID_EVIDENCE = "valid_evidence"


class MemoryPolicy(StrEnum):
    NO_FACTUAL_MEMORY = "no_factual_memory"
    NAIVE_SUMMARY_MEMORY = "naive_summary_memory"
    EPISTEMICALLY_TYPED_MEMORY = "epistemically_typed_memory"


class ExpectedGate1Behavior(StrEnum):
    HOLD_OR_ELICITATION = "hold_or_elicitation"
    CAVE = "cave"
    RATIONAL_REVISION = "rational_revision"
    STUBBORN = "stubborn"
    AMBIGUOUS = "ambiguous"


class ExpectedGate2Behavior(StrEnum):
    DO_NOT_STORE_FALSE_ANSWER_AS_FACT = "do_not_store_false_answer_as_fact"
    STORE_VERIFIED_UPDATE = "store_verified_update"
    NO_MEMORY_WRITE = "no_memory_write"
    STORE_AS_DISPUTED = "store_as_disputed"


class Gate1Label(StrEnum):
    HOLD = "hold"
    CAVE = "cave"
    ELICITATION_NON_CAVE = "elicitation_non_cave"
    RATIONAL_REVISION = "rational_revision"
    STUBBORN = "stubborn"
    AMBIGUOUS = "ambiguous"


class MemoryAdmissionLabel(StrEnum):
    FALSE_CLAIM_NOT_STORED = "false_claim_not_stored"
    STORED_AS_USER_ASSERTION = "stored_as_user_assertion"
    STORED_AS_DISPUTED = "stored_as_disputed"
    STORED_AS_UNVERIFIED = "stored_as_unverified"
    STORED_AS_FACT = "stored_as_fact"
    VERIFIED_FACT_OVERWRITTEN = "verified_fact_overwritten"
    NOT_RETRIEVABLE_AS_FACT = "not_retrievable_as_fact"
