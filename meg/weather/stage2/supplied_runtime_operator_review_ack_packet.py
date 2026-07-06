"""Pure supplied-input runtime operator-review acknowledgement packet scaffold.

This module consumes only caller-supplied values for runtime operator-review
acknowledgement packet metadata. The acknowledgement packet is an in-memory
record only. It performs no data collection, file access, service access,
source fetching, scoring, backtesting, paper trading, trading, autonomy,
persistence, export writing, owner-decision capture, decision execution, or
production behavior.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping

from meg.weather.stage2.supplied_runtime_operator_review_handoff import (
    SuppliedRuntimeOperatorReviewHandoffRecord,
    supplied_runtime_operator_review_handoff_record_from_mapping,
    validate_supplied_runtime_operator_review_handoff_record,
)


class _ClosedValue(str, Enum):
    """String enum base for closed, machine-checkable Stage 2 values."""

    @classmethod
    def values(cls) -> frozenset[str]:
        return frozenset(member.value for member in cls)


class OperatorReviewAckPacketStatus(_ClosedValue):
    OPERATOR_REVIEW_ACK_PACKET_RECORDED = "operator_review_ack_packet_recorded"
    OPERATOR_REVIEW_ACK_PACKET_MISSING = "operator_review_ack_packet_missing"
    OPERATOR_REVIEW_ACK_PACKET_AMBIGUOUS = "operator_review_ack_packet_ambiguous"
    OPERATOR_REVIEW_ACK_PACKET_UNSUPPORTED = "operator_review_ack_packet_unsupported"
    OPERATOR_REVIEW_ACK_PACKET_UNKNOWN = "operator_review_ack_packet_unknown"


class OperatorReviewAckCompletenessStatus(_ClosedValue):
    OPERATOR_REVIEW_ACK_COMPLETE = "operator_review_ack_complete"
    OPERATOR_REVIEW_ACK_INCOMPLETE = "operator_review_ack_incomplete"
    OPERATOR_REVIEW_ACK_AMBIGUOUS = "operator_review_ack_ambiguous"
    OPERATOR_REVIEW_ACK_UNKNOWN = "operator_review_ack_unknown"


class OperatorReviewStatus(_ClosedValue):
    OPERATOR_REVIEW_REQUIRED = "operator_review_required"
    OPERATOR_REVIEW_MISSING = "operator_review_missing"
    OPERATOR_REVIEW_AMBIGUOUS = "operator_review_ambiguous"
    OPERATOR_REVIEW_NOT_REQUIRED = "operator_review_not_required"
    OPERATOR_REVIEW_UNKNOWN = "operator_review_unknown"


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
class SuppliedRuntimeOperatorReviewAckPacketRecord:
    condition_id: str
    token_id: str
    outcome: str
    supplied_runtime_operator_review_handoff: SuppliedRuntimeOperatorReviewHandoffRecord
    ack_packet_id: str
    ack_summary: str
    operator_review_summary: str
    blocked_reason_summary: str
    operator_review_ack_packet_status: OperatorReviewAckPacketStatus
    operator_review_ack_completeness_status: OperatorReviewAckCompletenessStatus
    operator_review_status: OperatorReviewStatus
    runtime_gate_status: RuntimeGateStatus
    provenance_notes: str = ""


@dataclass(frozen=True)
class SuppliedRuntimeOperatorReviewAckPacketValidationResult:
    severity: ValidationSeverity
    passed: bool
    reasons: tuple[str, ...] = ()


def _enum_value(enum_type: type[_ClosedValue], value: _ClosedValue | str) -> _ClosedValue:
    if isinstance(value, enum_type):
        return value
    return enum_type(value)


def _is_nonblank_text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _supplied_runtime_operator_review_handoff_from_value(
    value: SuppliedRuntimeOperatorReviewHandoffRecord | Mapping[str, Any],
) -> SuppliedRuntimeOperatorReviewHandoffRecord:
    if isinstance(value, SuppliedRuntimeOperatorReviewHandoffRecord):
        return value
    return supplied_runtime_operator_review_handoff_record_from_mapping(value)


def supplied_runtime_operator_review_ack_packet_record_from_mapping(
    mapping: Mapping[str, Any],
) -> SuppliedRuntimeOperatorReviewAckPacketRecord:
    """Build operator-review acknowledgement metadata from supplied values."""

    return SuppliedRuntimeOperatorReviewAckPacketRecord(
        condition_id=mapping["condition_id"],
        token_id=mapping["token_id"],
        outcome=mapping["outcome"],
        supplied_runtime_operator_review_handoff=(
            _supplied_runtime_operator_review_handoff_from_value(
                mapping["supplied_runtime_operator_review_handoff"]
            )
        ),
        ack_packet_id=mapping["ack_packet_id"],
        ack_summary=mapping["ack_summary"],
        operator_review_summary=mapping["operator_review_summary"],
        blocked_reason_summary=mapping["blocked_reason_summary"],
        operator_review_ack_packet_status=_enum_value(
            OperatorReviewAckPacketStatus,
            mapping["operator_review_ack_packet_status"],
        ),
        operator_review_ack_completeness_status=_enum_value(
            OperatorReviewAckCompletenessStatus,
            mapping["operator_review_ack_completeness_status"],
        ),
        operator_review_status=_enum_value(
            OperatorReviewStatus,
            mapping["operator_review_status"],
        ),
        runtime_gate_status=_enum_value(RuntimeGateStatus, mapping["runtime_gate_status"]),
        provenance_notes=str(mapping.get("provenance_notes", "")),
    )


def validate_supplied_runtime_operator_review_ack_packet_record(
    record: SuppliedRuntimeOperatorReviewAckPacketRecord,
) -> SuppliedRuntimeOperatorReviewAckPacketValidationResult:
    """Validate a supplied operator-review ack packet with fail-closed behavior."""

    reasons: list[str] = []

    for field_name, value in (
        ("condition_id", record.condition_id),
        ("token_id", record.token_id),
        ("outcome", record.outcome),
        ("ack_packet_id", record.ack_packet_id),
        ("ack_summary", record.ack_summary),
        ("operator_review_summary", record.operator_review_summary),
    ):
        if not _is_nonblank_text(value):
            reasons.append(f"{field_name} is missing")

    handoff_result = validate_supplied_runtime_operator_review_handoff_record(
        record.supplied_runtime_operator_review_handoff
    )
    if not handoff_result.passed:
        reasons.append("supplied runtime operator-review handoff validation failed")

    for field_name in ("condition_id", "token_id", "outcome"):
        if getattr(record, field_name) != getattr(
            record.supplied_runtime_operator_review_handoff,
            field_name,
        ):
            reasons.append(
                f"{field_name} does not match supplied runtime operator-review handoff"
            )

    if (
        record.operator_review_summary
        != record.supplied_runtime_operator_review_handoff.operator_review_summary
    ):
        reasons.append(
            "operator_review_summary does not match supplied runtime operator-review handoff"
        )

    if (
        record.operator_review_ack_packet_status
        is not OperatorReviewAckPacketStatus.OPERATOR_REVIEW_ACK_PACKET_RECORDED
    ):
        reasons.append(
            "operator review ack packet status is "
            f"{record.operator_review_ack_packet_status.value}"
        )

    if (
        record.operator_review_ack_completeness_status
        is not OperatorReviewAckCompletenessStatus.OPERATOR_REVIEW_ACK_COMPLETE
    ):
        reasons.append(
            "operator review ack completeness status is "
            f"{record.operator_review_ack_completeness_status.value}"
        )

    if record.operator_review_status is not OperatorReviewStatus.OPERATOR_REVIEW_REQUIRED:
        reasons.append(f"operator review status is {record.operator_review_status.value}")

    if record.runtime_gate_status is not RuntimeGateStatus.RUNTIME_GATE_READY:
        reasons.append(f"runtime gate status is {record.runtime_gate_status.value}")

    if reasons and not _is_nonblank_text(record.blocked_reason_summary):
        reasons.append("blocked_reason_summary is missing")

    if reasons:
        return SuppliedRuntimeOperatorReviewAckPacketValidationResult(
            severity=ValidationSeverity.BLOCKED,
            passed=False,
            reasons=tuple(reasons),
        )

    return SuppliedRuntimeOperatorReviewAckPacketValidationResult(
        severity=ValidationSeverity.PASSED,
        passed=True,
    )
