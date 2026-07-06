"""Memory record schemas for the three Gate 2 mechanisms.

Gate 2 asks whether an unsupported false correction is admitted into persistent
memory as fact. Three memory policies are represented here:

* ``no_memory`` -- persistence control; nothing is written and nothing can be
  retrieved in a later session.
* ``naive_summary`` -- a free-text summary with no forced epistemic structure.
  Vulnerable to storing unsupported claims as fact.
* ``epistemically_typed_memory`` -- a structured record that preserves source,
  evidence level, verification status, contradiction status, and an explicit
  retrieval-permission flag.
"""

from pydantic import BaseModel, ConfigDict, model_validator

from coding.enums import (
    EvidenceStatus,
    MemoryAction,
    MemoryPolicy,
    MemorySource,
    VerificationStatus,
)


class NaiveMemoryRecord(BaseModel):
    """Free-text memory summary with no forced epistemic metadata."""

    model_config = ConfigDict(extra="forbid")

    summary_text: str


class TypedMemoryRecord(BaseModel):
    """Epistemically typed memory record (Gate 2 intervention).

    ``evidence_level`` reuses :class:`~coding.enums.EvidenceStatus` so that
    dataset evidence conditions and stored evidence levels share one vocabulary.
    """

    model_config = ConfigDict(extra="forbid")

    claim: str
    source: MemorySource
    evidence_level: EvidenceStatus
    verification_status: VerificationStatus
    contradicts_prior_source: bool
    prior_verified_fact: str
    memory_action: MemoryAction
    allowed_for_retrieval_as_fact: bool


class MemoryState(BaseModel):
    """Persisted memory state for a single trial under one memory policy."""

    model_config = ConfigDict(extra="forbid")

    trial_id: str
    memory_policy: MemoryPolicy
    naive_record: NaiveMemoryRecord | None = None
    typed_record: TypedMemoryRecord | None = None

    @model_validator(mode="after")
    def _check_policy_record_consistency(self) -> "MemoryState":
        if self.memory_policy == MemoryPolicy.NO_MEMORY:
            if self.naive_record is not None or self.typed_record is not None:
                msg = "no_memory policy must not carry a naive or typed record"
                raise ValueError(msg)
        elif self.memory_policy == MemoryPolicy.NAIVE_SUMMARY:
            if self.naive_record is None:
                msg = "naive_summary policy requires a naive_record"
                raise ValueError(msg)
            if self.typed_record is not None:
                msg = "naive_summary policy must not carry a typed_record"
                raise ValueError(msg)
        elif self.memory_policy == MemoryPolicy.EPISTEMICALLY_TYPED_MEMORY:
            if self.typed_record is None:
                msg = "epistemically_typed_memory policy requires a typed_record"
                raise ValueError(msg)
            if self.naive_record is not None:
                msg = "epistemically_typed_memory policy must not carry a naive_record"
                raise ValueError(msg)
        return self
