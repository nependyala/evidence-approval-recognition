"""Trial record schemas."""

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from coding.enums import (
    Domain,
    EvidenceStatus,
    ExpectedEvidenceLevel,
    ExpectedGate1Behavior,
    ExpectedGate2Behavior,
    ExpectedVerificationStatus,
    MemoryPolicy,
    PushbackCondition,
    RelationalCondition,
    TurnStructure,
)


class VisibleInput(BaseModel):
    """Natural input shown to the tested model."""

    model_config = ConfigDict(extra="forbid")

    source_document: str
    relational_memory: str
    question: str
    pushback_turns: list[str]
    memory_instruction: str
    downstream_task: str


class HiddenMetadata(BaseModel):
    """Evaluator-only ground-truth metadata."""

    model_config = ConfigDict(extra="forbid")

    domain: Domain
    entity_id: str
    target_attribute: str
    verified_fact: str
    false_correction: str
    valid_updated_fact: str | None
    evidence_status: EvidenceStatus
    pushback_condition: PushbackCondition
    relational_condition: RelationalCondition
    memory_policy: MemoryPolicy
    turn_structure: TurnStructure
    pressure_turn_count: int
    expected_gate_1_behavior: ExpectedGate1Behavior
    expected_gate_2_behavior: ExpectedGate2Behavior
    should_update_answer: bool
    should_store_user_claim: bool
    should_overwrite_verified_fact: bool
    should_preserve_source: bool
    should_preserve_contradiction: bool
    should_preserve_uncertainty: bool
    expected_verification_status: ExpectedVerificationStatus
    expected_evidence_level: ExpectedEvidenceLevel
    template_id: str
    paraphrase_id: str
    generator_id: str
    random_seed: str


class Trial(BaseModel):
    """Top-level trial record for curation and experimentation."""

    model_config = ConfigDict(extra="forbid")

    trial_id: str
    dataset_version: str
    visible_input: VisibleInput
    hidden_metadata: HiddenMetadata
    model_outputs: dict[str, Any] = Field(default_factory=dict)
