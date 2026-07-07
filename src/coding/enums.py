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


class RelationalContext(StrEnum):
    """Relational framing delivered in the model's context at Gate 1 (renamed
    from RelationalCondition; 'memory' now refers only to the Gate-2 store).
    Approval and the secure base are the contingent and non-contingent forms of regard."""

    NONE = "none"  # no relational framing; baseline
    TRUTH_INSTRUCTION = "truth_instruction"  # plain honesty instruction; non-relational control
    SECURE_DISAGREEMENT = "secure_disagreement"  # non-contingent regard; the secure base
    CONTINGENT_APPROVAL = "contingent_approval"  # conditional approval; the insecure frame


class PushbackCondition(StrEnum):
    """Pressure conditions, sorted by the channel the pressure appeals to
    (Deutsch & Gerard 1955, informational vs normative). Conditions name the
    mechanism; legitimacy lives in ``should_update`` / ``EvidenceStatus``, not in
    the name, which is why the old ``*_false`` suffix is gone."""

    # Live conditions
    NO_PRESSURE = "no_pressure"  # baseline, no pushback; the flip reference
    BARE_ASSERTION = "bare_assertion"  # floor; neither channel
    APPROVAL = "approval"  # normative channel; the secure-base intervention target
    FABRICATED_EVIDENCE = "fabricated_evidence"  # informational in form, void in ground; confounded
    VALID_EVIDENCE = "valid_evidence"  # informational, legitimate; the control
    # Deferred for the MVP (real conditions, out of scope for now)
    WEAK_EVIDENCE = "weak_evidence"
    AMBIGUOUS_EVIDENCE = "ambiguous_evidence"
    AUTHORITY = "authority"  # pure credential appeals; future authority split


class Modifier(StrEnum):
    """Dosage knobs crossed with the pressure conditions, not conditions
    themselves. Applied as transforms on a base pushback at assembly time."""

    USER_CONFIDENCE = "user_confidence"  # how confident the user sounds
    INTENSITY = "intensity"  # how many times the push repeats


class EvidenceStatus(StrEnum):
    UNSUPPORTED = "unsupported"
    FABRICATED = "fabricated"  # fake evidence as real; grades like unsupported, tagged apart
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


class MemorySource(StrEnum):
    """Provenance of a claim recorded in typed memory."""

    SOURCE_DOCUMENT = "source document"
    USER_ASSERTION = "user assertion"
    MODEL_INFERENCE = "model inference"
    EVIDENCE_UPDATE = "evidence update"


class VerificationStatus(StrEnum):
    """Verification state assigned to a typed-memory claim."""

    VERIFIED = "verified"
    UNVERIFIED = "unverified"
    DISPUTED = "disputed"
