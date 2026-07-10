"""Trial record schemas for the SycEval augmentation benchmark."""

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from coding.enums import (
    Confidence,
    EvidenceStatus,
    ExpectedGate1Behavior,
    ExpectedGate2Behavior,
    Gate1Label,
    Intensity,
    LegacyContextMode,
    MemoryAdmissionLabel,
    MemoryPolicy,
    PressureFamily,
    RelationalContextLabel,
    SourceDataset,
)


class BaseItem(BaseModel):
    """Normalized SycEval source item with legacy provenance."""

    model_config = ConfigDict(extra="forbid")

    base_item_id: str
    syceval_item_id: str
    source_dataset: SourceDataset
    source_item_id: str
    domain: str
    legacy_context_mode: LegacyContextMode
    legacy_rebuttal_tier: str


class ExperimentalFactors(BaseModel):
    """Independent experimental manipulations for one trial run."""

    model_config = ConfigDict(extra="forbid")

    model_id: str | None = None
    relational_context_label: RelationalContextLabel
    condition: str
    pressure_family: PressureFamily
    confidence: Confidence
    intensity: Intensity
    evidence_status: EvidenceStatus
    memory_policy: MemoryPolicy
    pressure_template_id: str


class CanonicalInitialTurn(BaseModel):
    """Frozen canonical assistant answer reused across conditions."""

    model_config = ConfigDict(extra="forbid")

    assistant_response: str


class PushbackTurn(BaseModel):
    """One user pressure or evidence turn."""

    model_config = ConfigDict(extra="forbid")

    turn_index: int
    user_text: str


class ResponseFormatInstruction(BaseModel):
    """Per-turn JSON response schema shown to the model."""

    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    format: str = "json"
    response_schema: dict[str, str] = Field(alias="schema")


class VisibleInput(BaseModel):
    """Model-visible prompt components for one Gate 1 + Gate 2 run."""

    model_config = ConfigDict(extra="forbid")

    question: str
    relational_context: str
    canonical_initial_turn: CanonicalInitialTurn
    pushback_turns: list[PushbackTurn]
    response_format_instruction: ResponseFormatInstruction
    memory_instruction: str
    downstream_task: str


class HiddenMetadata(BaseModel):
    """Evaluator-only ground truth and expected behaviors."""

    model_config = ConfigDict(extra="forbid")

    target_claim: str
    gold_answer: str
    true_answer_aliases: list[str]
    false_answer: str
    valid_evidence_asset: str | None = None
    fabricated_evidence_asset: str | None = None
    should_update_answer: bool
    expected_gate_1_behavior: ExpectedGate1Behavior
    expected_gate_2_behavior: ExpectedGate2Behavior


class ModelOutputs(BaseModel):
    """Filled by experiment runners after model inference."""

    model_config = ConfigDict(extra="forbid")

    initial_answer: Any | None = None
    gate1_responses_by_turn: list[Any] = Field(default_factory=list)
    final_answer: Any | None = None
    extracted_answer: str | None = None
    gate1_label: Gate1Label | None = None
    discourse_label: str | None = None
    memory_write: Any | None = None
    retrieved_claim: str | None = None
    downstream_answer: Any | None = None
    false_memory_used: bool | None = None
    downstream_correct: bool | None = None


class Evaluation(BaseModel):
    """Filled by the grading pipeline after model outputs are recorded."""

    model_config = ConfigDict(extra="forbid")

    answer_state_by_turn: list[Any] = Field(default_factory=list)
    turn_of_flip: int | None = None
    number_of_flips: int | None = None
    memory_admission_label: MemoryAdmissionLabel | None = None
    source_preserved: bool | None = None
    contradiction_preserved: bool | None = None
    verification_preserved: bool | None = None
    downstream_contamination: bool | None = None
    requires_human_review: bool = False
    review_notes: str | None = None


class Trial(BaseModel):
    """Top-level trial record: one model x item x factor combination."""

    model_config = ConfigDict(extra="forbid")

    trial_id: str
    dataset_version: str
    base_item: BaseItem
    experimental_factors: ExperimentalFactors
    visible_input: VisibleInput
    hidden_metadata: HiddenMetadata
    model_outputs: ModelOutputs = Field(default_factory=ModelOutputs)
    evaluation: Evaluation = Field(default_factory=Evaluation)
