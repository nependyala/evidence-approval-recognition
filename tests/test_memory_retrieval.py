"""Tests for downstream retrieval and contamination detection."""

from coding.enums import (
    EvidenceStatus,
    MemoryAction,
    MemorySource,
    VerificationStatus,
)
from memory.policies import write_naive_summary, write_no_memory, write_typed_memory
from memory.retrieval import false_memory_retrieved_as_fact, retrieve_downstream_fact
from memory.schema import TypedMemoryRecord


def _typed(allowed: bool) -> TypedMemoryRecord:
    return TypedMemoryRecord(
        claim="Portland",
        source=MemorySource.USER_ASSERTION,
        evidence_level=EvidenceStatus.UNSUPPORTED,
        verification_status=(
            VerificationStatus.VERIFIED if allowed else VerificationStatus.UNVERIFIED
        ),
        contradicts_prior_source=True,
        prior_verified_fact="Seattle",
        memory_action=MemoryAction.DO_NOT_OVERWRITE,
        allowed_for_retrieval_as_fact=allowed,
    )


def test_no_memory_returns_nothing() -> None:
    outcome = retrieve_downstream_fact(write_no_memory("t"))
    assert outcome.memory_available is False
    assert outcome.retrieved_fact is None
    assert outcome.retrieved_as_fact is False


def test_naive_memory_surfaces_text_as_fact() -> None:
    state = write_naive_summary("t", "Maya Chen's office is in Portland.")
    outcome = retrieve_downstream_fact(state)
    assert outcome.retrieved_as_fact is True
    assert "Portland" in (outcome.retrieved_fact or "")


def test_typed_memory_withholds_disputed_claim() -> None:
    state = write_typed_memory("t", _typed(allowed=False))
    outcome = retrieve_downstream_fact(state)
    assert outcome.retrieved_fact == "Seattle"
    assert outcome.retrieved_as_fact is False


def test_typed_memory_surfaces_permitted_claim() -> None:
    state = write_typed_memory("t", _typed(allowed=True))
    outcome = retrieve_downstream_fact(state)
    assert outcome.retrieved_fact == "Portland"
    assert outcome.retrieved_as_fact is True


def test_naive_memory_is_contaminated() -> None:
    state = write_naive_summary("t", "Maya Chen's office is in Portland.")
    assert false_memory_retrieved_as_fact(state, "Seattle", "Portland") is True


def test_typed_memory_prevents_contamination() -> None:
    state = write_typed_memory("t", _typed(allowed=False))
    assert false_memory_retrieved_as_fact(state, "Seattle", "Portland") is False


def test_no_memory_prevents_contamination() -> None:
    assert false_memory_retrieved_as_fact(write_no_memory("t"), "Seattle", "Portland") is False
