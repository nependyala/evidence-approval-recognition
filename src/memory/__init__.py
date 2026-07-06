"""Gate 2 memory mechanisms: no-memory, naive summary, and typed memory.

This package implements the three MVP memory policies together with the
deterministic policy logic (contradiction detection, overwrite decisions,
retrieval permission), downstream retrieval, and audit/validation used to score
memory admission and downstream contamination.
"""

from memory.audit import (
    NaiveAuditResult,
    audit_naive_summary,
    validate_typed_memory_against_ground_truth,
    validate_typed_memory_schema,
)
from memory.policies import (
    build_reference_memory_state,
    build_reference_typed_memory,
    derive_memory_action,
    derive_retrieval_permission,
    derive_source,
    derive_verification_status,
    facts_conflict,
    write_naive_summary,
    write_no_memory,
    write_typed_memory,
)
from memory.retrieval import (
    RetrievalOutcome,
    false_memory_retrieved_as_fact,
    retrieve_downstream_fact,
)
from memory.schema import (
    MemoryState,
    NaiveMemoryRecord,
    TypedMemoryRecord,
)

__all__ = [
    "MemoryState",
    "NaiveAuditResult",
    "NaiveMemoryRecord",
    "RetrievalOutcome",
    "TypedMemoryRecord",
    "audit_naive_summary",
    "build_reference_memory_state",
    "build_reference_typed_memory",
    "derive_memory_action",
    "derive_retrieval_permission",
    "derive_source",
    "derive_verification_status",
    "facts_conflict",
    "false_memory_retrieved_as_fact",
    "retrieve_downstream_fact",
    "validate_typed_memory_against_ground_truth",
    "validate_typed_memory_schema",
    "write_naive_summary",
    "write_no_memory",
    "write_typed_memory",
]
