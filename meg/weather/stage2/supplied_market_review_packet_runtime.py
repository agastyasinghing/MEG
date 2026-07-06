"""Pure supplied-input review-packet runtime scaffold.

This module consumes only caller-supplied values for review-packet metadata.
It performs no data collection, file access, service access, source fetching,
scoring, backtesting, paper trading, trading, autonomy, or production behavior.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping

from meg.weather.stage2.supplied_market_contract_runtime import (
    SuppliedMarketContractRecord,
    supplied_market_contract_record_from_mapping,
    validate_supplied_market_contract_record,
)


class _ClosedValue(str, Enum):
    """String enum base for closed, machine-checkable Stage 2 values."""

    @classmethod
    def values(cls) -> frozenset[str]:
        return frozenset(member.value for member in cls)


class ReviewPacketStatus(_ClosedValue):
    REVIEW_PACKET_RECORDED = "review_packet_recorded"
    REVIEW_PACKET_MISSING = "review_packet_missing"
    REVIEW_PACKET_AMBIGUOUS = "review_packet_ambiguous"
    REVIEW_PACKET_UNSUPPORTED = "review_packet_unsupported"
    REVIEW_PACKET_UNKNOWN = "review_packet_unknown"


class ReviewRecommendationStatus(_ClosedValue):
    REVIEW_RECOMMENDATION_READY = "review_recommendation_ready"
    REVIEW_RECOMMENDATION_BLOCKED = "review_recommendation_blocked"
    REVIEW_RECOMMENDATION_REQUIRES_MANUAL_REVIEW = (
        "review_recommendation_requires_manual_review"
    )
    REVIEW_RECOMMENDATION_UNKNOWN = "review_recommendation_unknown"


class EvidenceSummaryStatus(_ClosedValue):
    EVIDENCE_SUMMARY_RECORDED = "evidence_summary_recorded"
    EVIDENCE_SUMMARY_MISSING = "evidence_summary_missing"
    EVIDENCE_SUMMARY_AMBIGUOUS = "evidence_summary_ambiguous"
    EVIDENCE_SUMMARY_UNSUPPORTED = "evidence_summary_unsupported"
    EVIDENCE_SUMMARY_UNKNOWN = "evidence_summary_unknown"


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
class SuppliedMarketReviewPacketRecord:
    condition_id: str
    token_id: str
    outcome: str
    supplied_market_contract: SuppliedMarketContractRecord
    review_packet_id: str
    review_summary: str
    evidence_summary: str
    blocked_reason_summary: str
    review_packet_status: ReviewPacketStatus
    review_recommendation_status: ReviewRecommendationStatus
    evidence_summary_status: EvidenceSummaryStatus
    runtime_gate_status: RuntimeGateStatus
    provenance_notes: str = ""


@dataclass(frozen=True)
class SuppliedMarketReviewPacketValidationResult:
    severity: ValidationSeverity
    passed: bool
    reasons: tuple[str, ...] = ()


def _enum_value(enum_type: type[_ClosedValue], value: _ClosedValue | str) -> _ClosedValue:
    if isinstance(value, enum_type):
        return value
    return enum_type(value)


def _is_nonblank_text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _supplied_market_contract_from_value(
    value: SuppliedMarketContractRecord | Mapping[str, Any],
) -> SuppliedMarketContractRecord:
    if isinstance(value, SuppliedMarketContractRecord):
        return value
    return supplied_market_contract_record_from_mapping(value)


def supplied_market_review_packet_record_from_mapping(
    mapping: Mapping[str, Any],
) -> SuppliedMarketReviewPacketRecord:
    """Build review-packet metadata from explicitly supplied values."""

    return SuppliedMarketReviewPacketRecord(
        condition_id=mapping["condition_id"],
        token_id=mapping["token_id"],
        outcome=mapping["outcome"],
        supplied_market_contract=_supplied_market_contract_from_value(
            mapping["supplied_market_contract"]
        ),
        review_packet_id=mapping["review_packet_id"],
        review_summary=mapping["review_summary"],
        evidence_summary=mapping["evidence_summary"],
        blocked_reason_summary=mapping["blocked_reason_summary"],
        review_packet_status=_enum_value(
            ReviewPacketStatus, mapping["review_packet_status"]
        ),
        review_recommendation_status=_enum_value(
            ReviewRecommendationStatus, mapping["review_recommendation_status"]
        ),
        evidence_summary_status=_enum_value(
            EvidenceSummaryStatus, mapping["evidence_summary_status"]
        ),
        runtime_gate_status=_enum_value(RuntimeGateStatus, mapping["runtime_gate_status"]),
        provenance_notes=str(mapping.get("provenance_notes", "")),
    )


def validate_supplied_market_review_packet_record(
    record: SuppliedMarketReviewPacketRecord,
) -> SuppliedMarketReviewPacketValidationResult:
    """Validate supplied review-packet metadata with fail-closed behavior."""

    reasons: list[str] = []

    for field_name, value in (
        ("condition_id", record.condition_id),
        ("token_id", record.token_id),
        ("outcome", record.outcome),
        ("review_packet_id", record.review_packet_id),
        ("review_summary", record.review_summary),
        ("evidence_summary", record.evidence_summary),
    ):
        if not _is_nonblank_text(value):
            reasons.append(f"{field_name} is missing")

    contract_result = validate_supplied_market_contract_record(
        record.supplied_market_contract
    )
    if not contract_result.passed:
        reasons.append("supplied market contract validation failed")

    if record.condition_id != record.supplied_market_contract.condition_id:
        reasons.append("condition_id does not match supplied market contract")

    if record.token_id != record.supplied_market_contract.token_id:
        reasons.append("token_id does not match supplied market contract")

    if record.outcome != record.supplied_market_contract.outcome:
        reasons.append("outcome does not match supplied market contract")

    if record.review_packet_status is not ReviewPacketStatus.REVIEW_PACKET_RECORDED:
        reasons.append(f"review packet status is {record.review_packet_status.value}")

    if (
        record.review_recommendation_status
        is not ReviewRecommendationStatus.REVIEW_RECOMMENDATION_READY
    ):
        reasons.append(
            f"review recommendation status is {record.review_recommendation_status.value}"
        )

    if record.evidence_summary_status is not EvidenceSummaryStatus.EVIDENCE_SUMMARY_RECORDED:
        reasons.append(f"evidence summary status is {record.evidence_summary_status.value}")

    if record.runtime_gate_status is not RuntimeGateStatus.RUNTIME_GATE_READY:
        reasons.append(f"runtime gate status is {record.runtime_gate_status.value}")

    if reasons and not _is_nonblank_text(record.blocked_reason_summary):
        reasons.append("blocked_reason_summary is missing")

    if reasons:
        return SuppliedMarketReviewPacketValidationResult(
            severity=ValidationSeverity.BLOCKED,
            passed=False,
            reasons=tuple(reasons),
        )

    return SuppliedMarketReviewPacketValidationResult(
        severity=ValidationSeverity.PASSED,
        passed=True,
    )
