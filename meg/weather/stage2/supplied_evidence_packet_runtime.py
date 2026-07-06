"""Pure supplied-input evidence-packet runtime scaffold.

This module consumes only caller-supplied values for evidence-packet metadata.
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


class EvidencePacketStatus(_ClosedValue):
    EVIDENCE_PACKET_RECORDED = "evidence_packet_recorded"
    EVIDENCE_PACKET_MISSING = "evidence_packet_missing"
    EVIDENCE_PACKET_AMBIGUOUS = "evidence_packet_ambiguous"
    EVIDENCE_PACKET_UNSUPPORTED = "evidence_packet_unsupported"
    EVIDENCE_PACKET_UNKNOWN = "evidence_packet_unknown"


class EvidenceFreshnessStatus(_ClosedValue):
    EVIDENCE_FRESHNESS_RECORDED = "evidence_freshness_recorded"
    EVIDENCE_FRESHNESS_MISSING = "evidence_freshness_missing"
    EVIDENCE_FRESHNESS_AMBIGUOUS = "evidence_freshness_ambiguous"
    EVIDENCE_FRESHNESS_STALE = "evidence_freshness_stale"
    EVIDENCE_FRESHNESS_UNKNOWN = "evidence_freshness_unknown"


class EvidenceAvailabilityStatus(_ClosedValue):
    EVIDENCE_AVAILABLE_BEFORE_DECISION = "evidence_available_before_decision"
    EVIDENCE_AVAILABLE_AT_DECISION = "evidence_available_at_decision"
    EVIDENCE_AVAILABLE_AFTER_DECISION = "evidence_available_after_decision"
    EVIDENCE_AVAILABILITY_MISSING = "evidence_availability_missing"
    EVIDENCE_AVAILABILITY_AMBIGUOUS = "evidence_availability_ambiguous"
    EVIDENCE_AVAILABILITY_UNKNOWN = "evidence_availability_unknown"


class EvidenceSourcePosture(_ClosedValue):
    CALLER_SUPPLIED_STATIC_EVIDENCE = "caller_supplied_static_evidence"
    CALLER_SUPPLIED_MANUAL_REVIEW_EVIDENCE = "caller_supplied_manual_review_evidence"
    UNSUPPORTED_RUNTIME_SOURCE_EVIDENCE = "unsupported_runtime_source_evidence"
    UNKNOWN_SOURCE_POSTURE = "unknown_source_posture"


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
class SuppliedEvidencePacketRecord:
    condition_id: str
    token_id: str
    outcome: str
    supplied_market_contract: SuppliedMarketContractRecord
    evidence_packet_id: str
    evidence_summary: str
    evidence_source_descriptor: str
    evidence_observed_at_utc: str
    evidence_available_at_utc: str
    decision_time_utc: str
    evidence_packet_status: EvidencePacketStatus
    evidence_freshness_status: EvidenceFreshnessStatus
    evidence_availability_status: EvidenceAvailabilityStatus
    evidence_source_posture: EvidenceSourcePosture
    runtime_gate_status: RuntimeGateStatus
    provenance_notes: str = ""


@dataclass(frozen=True)
class SuppliedEvidencePacketValidationResult:
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


def supplied_evidence_packet_record_from_mapping(
    mapping: Mapping[str, Any],
) -> SuppliedEvidencePacketRecord:
    """Build evidence-packet metadata from explicitly supplied values."""

    return SuppliedEvidencePacketRecord(
        condition_id=mapping["condition_id"],
        token_id=mapping["token_id"],
        outcome=mapping["outcome"],
        supplied_market_contract=_supplied_market_contract_from_value(
            mapping["supplied_market_contract"]
        ),
        evidence_packet_id=mapping["evidence_packet_id"],
        evidence_summary=mapping["evidence_summary"],
        evidence_source_descriptor=mapping["evidence_source_descriptor"],
        evidence_observed_at_utc=mapping["evidence_observed_at_utc"],
        evidence_available_at_utc=mapping["evidence_available_at_utc"],
        decision_time_utc=mapping["decision_time_utc"],
        evidence_packet_status=_enum_value(
            EvidencePacketStatus, mapping["evidence_packet_status"]
        ),
        evidence_freshness_status=_enum_value(
            EvidenceFreshnessStatus, mapping["evidence_freshness_status"]
        ),
        evidence_availability_status=_enum_value(
            EvidenceAvailabilityStatus, mapping["evidence_availability_status"]
        ),
        evidence_source_posture=_enum_value(
            EvidenceSourcePosture, mapping["evidence_source_posture"]
        ),
        runtime_gate_status=_enum_value(RuntimeGateStatus, mapping["runtime_gate_status"]),
        provenance_notes=str(mapping.get("provenance_notes", "")),
    )


def validate_supplied_evidence_packet_record(
    record: SuppliedEvidencePacketRecord,
) -> SuppliedEvidencePacketValidationResult:
    """Validate supplied evidence-packet metadata with fail-closed behavior."""

    reasons: list[str] = []

    for field_name, value in (
        ("condition_id", record.condition_id),
        ("token_id", record.token_id),
        ("outcome", record.outcome),
        ("evidence_packet_id", record.evidence_packet_id),
        ("evidence_summary", record.evidence_summary),
        ("evidence_source_descriptor", record.evidence_source_descriptor),
        ("evidence_observed_at_utc", record.evidence_observed_at_utc),
        ("evidence_available_at_utc", record.evidence_available_at_utc),
        ("decision_time_utc", record.decision_time_utc),
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

    if record.evidence_packet_status is not EvidencePacketStatus.EVIDENCE_PACKET_RECORDED:
        reasons.append(f"evidence packet status is {record.evidence_packet_status.value}")

    if (
        record.evidence_freshness_status
        is not EvidenceFreshnessStatus.EVIDENCE_FRESHNESS_RECORDED
    ):
        reasons.append(
            f"evidence freshness status is {record.evidence_freshness_status.value}"
        )

    allowed_availability_statuses = frozenset(
        {
            EvidenceAvailabilityStatus.EVIDENCE_AVAILABLE_BEFORE_DECISION,
            EvidenceAvailabilityStatus.EVIDENCE_AVAILABLE_AT_DECISION,
        }
    )
    if record.evidence_availability_status not in allowed_availability_statuses:
        reasons.append(
            f"evidence availability status is {record.evidence_availability_status.value}"
        )

    allowed_source_postures = frozenset(
        {
            EvidenceSourcePosture.CALLER_SUPPLIED_STATIC_EVIDENCE,
            EvidenceSourcePosture.CALLER_SUPPLIED_MANUAL_REVIEW_EVIDENCE,
        }
    )
    if record.evidence_source_posture not in allowed_source_postures:
        reasons.append(f"evidence source posture is {record.evidence_source_posture.value}")

    if record.runtime_gate_status is not RuntimeGateStatus.RUNTIME_GATE_READY:
        reasons.append(f"runtime gate status is {record.runtime_gate_status.value}")

    if reasons:
        return SuppliedEvidencePacketValidationResult(
            severity=ValidationSeverity.BLOCKED,
            passed=False,
            reasons=tuple(reasons),
        )

    return SuppliedEvidencePacketValidationResult(
        severity=ValidationSeverity.PASSED,
        passed=True,
    )
