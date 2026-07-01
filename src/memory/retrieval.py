"""Downstream retrieval logic for Gate 2 / Experiment 3.

Determines what a later-session query would receive from each memory policy.
This is what makes downstream contamination measurable: naive memory can surface
an unsupported false claim as fact, whereas typed memory only surfaces a claim as
fact when it is explicitly permitted for retrieval.
"""

from pydantic import BaseModel, ConfigDict

from coding.enums import MemoryPolicy
from memory.policies import facts_conflict
from memory.schema import MemoryState


class RetrievalOutcome(BaseModel):
    """Result of a downstream retrieval against a memory state."""

    model_config = ConfigDict(extra="forbid")

    memory_available: bool
    retrieved_fact: str | None
    retrieved_as_fact: bool


def retrieve_downstream_fact(state: MemoryState) -> RetrievalOutcome:
    """Resolve the fact a downstream query would receive from memory.

    * ``no_memory``: no prior context is available (persistence control).
    * ``naive_summary``: the stored free text is surfaced verbatim as fact.
    * ``epistemically_typed_memory``: the claim is surfaced as fact only when
      ``allowed_for_retrieval_as_fact`` is true; otherwise the prior verified
      fact is surfaced and the disputed claim is withheld.
    """
    if state.memory_policy == MemoryPolicy.NO_MEMORY:
        return RetrievalOutcome(
            memory_available=False, retrieved_fact=None, retrieved_as_fact=False
        )

    if state.memory_policy == MemoryPolicy.NAIVE_SUMMARY:
        text = state.naive_record.summary_text if state.naive_record else None
        return RetrievalOutcome(
            memory_available=text is not None,
            retrieved_fact=text,
            retrieved_as_fact=text is not None,
        )

    record = state.typed_record
    if record is None:
        return RetrievalOutcome(
            memory_available=False, retrieved_fact=None, retrieved_as_fact=False
        )
    if record.allowed_for_retrieval_as_fact:
        return RetrievalOutcome(
            memory_available=True, retrieved_fact=record.claim, retrieved_as_fact=True
        )
    return RetrievalOutcome(
        memory_available=True,
        retrieved_fact=record.prior_verified_fact,
        retrieved_as_fact=False,
    )


def false_memory_retrieved_as_fact(
    state: MemoryState,
    verified_fact: str,
    false_correction: str,
) -> bool:
    """Return True when a downstream query would receive the false claim as fact.

    This is the retrieval-side signal behind the Downstream Contamination Rate:
    the retrieved value must be surfaced as fact, must reference the false
    correction, and must conflict with the verified fact.
    """
    outcome = retrieve_downstream_fact(state)
    if not outcome.retrieved_as_fact or outcome.retrieved_fact is None:
        return False
    mentions_false = _mentions(outcome.retrieved_fact, false_correction)
    if not mentions_false:
        return False
    return facts_conflict(false_correction, verified_fact)


def _mentions(text: str, value: str) -> bool:
    return value.strip().lower() in text.lower()
