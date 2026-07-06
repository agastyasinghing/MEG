"""Pure supplied-input review/evidence composition runtime scaffold.

This module consumes only caller-supplied values for review/evidence composition.
It performs no data collection, file access, service access, source fetching,
scoring, backtesting, paper trading, trading, autonomy, or production behavior.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping

from meg.weather.stage2.supplied_evidence_packet_runtime import (
    SuppliedEvidencePacketRecord,
    supplied_evidence_packet_record_from_mapping,
    validate_supplied_evidence_packet_record,
)
from meg.weather.stage2.supplied_market_review_packet_runtime import (
    SuppliedMarketReviewPacketRecord,
    supplied_market_review_packet_record_from_mapping,
    validate_supplied_market_review_packet_record,
)


class _ClosedValue(str, Enum):
    """String enum base for closed, machine-checkable Stage 2 values."""

    @classmethod
    def values(cls) -> frozenset[str]:
        return frozenset(member.value for member in cls)


class CompositionStatus(_ClosedValue):
    COMPOSITION_RECORDED = "composition_recorded"
    COMPOSITION_MISSING = "composition_missing"
    COMPOSITION_AMBIGUOUS = "composition_ambiguous"
    COMPOSITION_UNSUPPORTED = "composition_unsupported"
    COMPOSITION_UNKNOWN = "composition_unknown"


class EvidenceReviewAlignmentStatus(_ClosedValue):
    EVIDENCE_REVIEW_ALIGNED = "evidence_review_aligned"
    EVIDENCE_REVIEW_MISMATCH = "evidence_review_mismatch"
    EVIDENCE_REVIEW_MISSING = "evidence_review_missing"
    EVIDENCE_REVIEW_AMBIGUOUS = "evidence_review_ambiguous"
    EVIDENCE_REVIEW_UNKNOWN = "evidence_review_unknown"


class RuntimeGateStatus(_ClosedValue):
    RUNTIME_GATE_READY = "runtime_gate_ready"
    RUNTIME_GATE_BLOCKED = "runtime_gate_blocked"
    RUNTIME_GATE_REQUIRES_MANUAL_REVIEW = "runtime_gate_requires_manual_review"
    RUNTIME_GATE_UNKNOWN = "runtime_gate_unknown"


class ValidationSeverity(_ClosedValue):
    PASSED = "passed"
    CAUTION = "caution"
    FAILED = "failed"
    BLOCKED = "blocked"


@dataclass(frozen=True)
class ReviewPacketEvidenceCompositionRecord:
    condition_id: str
    token_id: str
    outcome: str
    supplied_market_review_packet: SuppliedMarketReviewPacketRecord
    supplied_evidence_packet: SuppliedEvidencePacketRecord
    composition_id: str
    composition_summary: str
    composition_status: CompositionStatus
    evidence_review_alignment_status: EvidenceReviewAlignmentStatus
    runtime_gate_status: RuntimeGateStatus
    provenance_notes: str = ""


@dataclass(frozen=True)
class ReviewPacketEvidenceCompositionValidationResult:
    severity: ValidationSeverity
    passed: bool
    reasons: tuple[str, ...] = ()


def _enum_value(enum_type: type[_ClosedValue], value: _ClosedValue | str) -> _ClosedValue:
    if isinstance(value, enum_type):
        return value
    return enum_type(value)


def _is_nonblank_text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _supplied_market_review_packet_from_value(
    value: SuppliedMarketReviewPacketRecord | Mapping[str, Any],
) -> SuppliedMarketReviewPacketRecord:
    if isinstance(value, SuppliedMarketReviewPacketRecord):
        return value
    return supplied_market_review_packet_record_from_mapping(value)


def _supplied_evidence_packet_from_value(
    value: SuppliedEvidencePacketRecord | Mapping[str, Any],
) -> SuppliedEvidencePacketRecord:
    if isinstance(value, SuppliedEvidencePacketRecord):
        return value
    return supplied_evidence_packet_record_from_mapping(value)


def review_packet_evidence_composition_record_from_mapping(
    mapping: Mapping[str, Any],
) -> ReviewPacketEvidenceCompositionRecord:
    """Build review/evidence composition metadata from explicitly supplied values."""

    return ReviewPacketEvidenceCompositionRecord(
        condition_id=mapping["condition_id"],
        token_id=mapping["token_id"],
        outcome=mapping["outcome"],
        supplied_market_review_packet=_supplied_market_review_packet_from_value(
            mapping["supplied_market_review_packet"]
        ),
        supplied_evidence_packet=_supplied_evidence_packet_from_value(
            mapping["supplied_evidence_packet"]
        ),
        composition_id=mapping["composition_id"],
        composition_summary=mapping["composition_summary"],
        composition_status=_enum_value(CompositionStatus, mapping["composition_status"]),
        evidence_review_alignment_status=_enum_value(
            EvidenceReviewAlignmentStatus,
            mapping["evidence_review_alignment_status"],
        ),
        runtime_gate_status=_enum_value(RuntimeGateStatus, mapping["runtime_gate_status"]),
        provenance_notes=str(mapping.get("provenance_notes", "")),
    )


def validate_review_packet_evidence_composition_record(
    record: ReviewPacketEvidenceCompositionRecord,
) -> ReviewPacketEvidenceCompositionValidationResult:
    """Validate supplied review/evidence composition with fail-closed behavior."""

    reasons: list[str] = []

    for field_name, value in (
        ("condition_id", record.condition_id),
        ("token_id", record.token_id),
        ("outcome", record.outcome),
        ("composition_id", record.composition_id),
        ("composition_summary", record.composition_summary),
    ):
        if not _is_nonblank_text(value):
            reasons.append(f"{field_name} is missing")

    review_result = validate_supplied_market_review_packet_record(
        record.supplied_market_review_packet
    )
    if not review_result.passed:
        reasons.append("supplied market review packet validation failed")

    evidence_result = validate_supplied_evidence_packet_record(record.supplied_evidence_packet)
    if not evidence_result.passed:
        reasons.append("supplied evidence packet validation failed")

    if record.condition_id != record.supplied_market_review_packet.condition_id:
        reasons.append("condition_id does not match supplied market review packet")
    if record.token_id != record.supplied_market_review_packet.token_id:
        reasons.append("token_id does not match supplied market review packet")
    if record.outcome != record.supplied_market_review_packet.outcome:
        reasons.append("outcome does not match supplied market review packet")

    if record.condition_id != record.supplied_evidence_packet.condition_id:
        reasons.append("condition_id does not match supplied evidence packet")
    if record.token_id != record.supplied_evidence_packet.token_id:
        reasons.append("token_id does not match supplied evidence packet")
    if record.outcome != record.supplied_evidence_packet.outcome:
        reasons.append("outcome does not match supplied evidence packet")

    review_packet = record.supplied_market_review_packet
    evidence_packet = record.supplied_evidence_packet
    if (
        review_packet.condition_id != evidence_packet.condition_id
        or review_packet.token_id != evidence_packet.token_id
        or review_packet.outcome != evidence_packet.outcome
    ):
        reasons.append("supplied market review packet does not match supplied evidence packet")

    review_contract = review_packet.supplied_market_contract
    evidence_contract = evidence_packet.supplied_market_contract
    if (
        review_contract.condition_id != evidence_contract.condition_id
        or review_contract.token_id != evidence_contract.token_id
        or review_contract.outcome != evidence_contract.outcome
    ):
        reasons.append("nested supplied market contracts do not match")

    if review_packet.evidence_summary != evidence_packet.evidence_summary:
        reasons.append("evidence_summary does not match supplied evidence packet")

    if record.composition_status is not CompositionStatus.COMPOSITION_RECORDED:
        reasons.append(f"composition status is {record.composition_status.value}")

    if (
        record.evidence_review_alignment_status
        is not EvidenceReviewAlignmentStatus.EVIDENCE_REVIEW_ALIGNED
    ):
        reasons.append(
            f"evidence review alignment status is "
            f"{record.evidence_review_alignment_status.value}"
        )

    if record.runtime_gate_status is not RuntimeGateStatus.RUNTIME_GATE_READY:
        reasons.append(f"runtime gate status is {record.runtime_gate_status.value}")

    if reasons:
        return ReviewPacketEvidenceCompositionValidationResult(
            severity=ValidationSeverity.BLOCKED,
            passed=False,
            reasons=tuple(reasons),
        )

    return ReviewPacketEvidenceCompositionValidationResult(
        severity=ValidationSeverity.PASSED,
        passed=True,
    )
