"""Pure supplied-input runtime operator-review final packet scaffold.

This module consumes only caller-supplied values for runtime operator-review
final packet metadata. The final packet is an in-memory record only. It
performs no data collection, file access, service access, source fetching,
scoring, backtesting, paper trading, trading, autonomy, persistence, export
writing, owner-decision capture, decision execution, queue service, scheduler,
broker, generated-summary behavior, or production behavior.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping

from meg.weather.stage2.supplied_runtime_operator_review_queue_summary import (
    SuppliedRuntimeOperatorReviewQueueSummaryRecord,
    supplied_runtime_operator_review_queue_summary_record_from_mapping,
    validate_supplied_runtime_operator_review_queue_summary_record,
)


class _ClosedValue(str, Enum):
    """String enum base for closed, machine-checkable Stage 2 values."""

    @classmethod
    def values(cls) -> frozenset[str]:
        return frozenset(member.value for member in cls)


class OperatorReviewFinalPacketStatus(_ClosedValue):
    OPERATOR_REVIEW_FINAL_PACKET_RECORDED = "operator_review_final_packet_recorded"
    OPERATOR_REVIEW_FINAL_PACKET_MISSING = "operator_review_final_packet_missing"
    OPERATOR_REVIEW_FINAL_PACKET_AMBIGUOUS = "operator_review_final_packet_ambiguous"
    OPERATOR_REVIEW_FINAL_PACKET_UNSUPPORTED = "operator_review_final_packet_unsupported"
    OPERATOR_REVIEW_FINAL_PACKET_UNKNOWN = "operator_review_final_packet_unknown"


class OperatorReviewFinalCompletenessStatus(_ClosedValue):
    OPERATOR_REVIEW_FINAL_COMPLETE = "operator_review_final_complete"
    OPERATOR_REVIEW_FINAL_INCOMPLETE = "operator_review_final_incomplete"
    OPERATOR_REVIEW_FINAL_AMBIGUOUS = "operator_review_final_ambiguous"
    OPERATOR_REVIEW_FINAL_UNKNOWN = "operator_review_final_unknown"


class OperatorReviewFinalPosture(_ClosedValue):
    OPERATOR_REVIEW_FINAL_IN_MEMORY_ONLY = "operator_review_final_in_memory_only"
    OPERATOR_REVIEW_FINAL_MISSING = "operator_review_final_missing"
    OPERATOR_REVIEW_FINAL_AMBIGUOUS = "operator_review_final_ambiguous"
    OPERATOR_REVIEW_FINAL_UNSUPPORTED = "operator_review_final_unsupported"
    OPERATOR_REVIEW_FINAL_UNKNOWN = "operator_review_final_unknown"


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
class SuppliedRuntimeOperatorReviewFinalPacketRecord:
    condition_id: str
    token_id: str
    outcome: str
    supplied_runtime_operator_review_queue_summary: SuppliedRuntimeOperatorReviewQueueSummaryRecord
    final_packet_id: str
    final_packet_summary: str
    operator_review_summary: str
    blocked_reason_summary: str
    operator_review_final_packet_status: OperatorReviewFinalPacketStatus
    operator_review_final_completeness_status: OperatorReviewFinalCompletenessStatus
    operator_review_final_posture: OperatorReviewFinalPosture
    operator_review_status: OperatorReviewStatus
    runtime_gate_status: RuntimeGateStatus
    provenance_notes: str = ""


@dataclass(frozen=True)
class SuppliedRuntimeOperatorReviewFinalPacketValidationResult:
    severity: ValidationSeverity
    passed: bool
    reasons: tuple[str, ...] = ()


def _enum_value(enum_type: type[_ClosedValue], value: _ClosedValue | str) -> _ClosedValue:
    if isinstance(value, enum_type):
        return value
    return enum_type(value)


def _is_nonblank_text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _supplied_runtime_operator_review_queue_summary_from_value(
    value: SuppliedRuntimeOperatorReviewQueueSummaryRecord | Mapping[str, Any],
) -> SuppliedRuntimeOperatorReviewQueueSummaryRecord:
    if isinstance(value, SuppliedRuntimeOperatorReviewQueueSummaryRecord):
        return value
    return supplied_runtime_operator_review_queue_summary_record_from_mapping(value)


def supplied_runtime_operator_review_final_packet_record_from_mapping(
    mapping: Mapping[str, Any],
) -> SuppliedRuntimeOperatorReviewFinalPacketRecord:
    """Build operator-review final packet metadata from supplied values."""

    return SuppliedRuntimeOperatorReviewFinalPacketRecord(
        condition_id=mapping["condition_id"],
        token_id=mapping["token_id"],
        outcome=mapping["outcome"],
        supplied_runtime_operator_review_queue_summary=(
            _supplied_runtime_operator_review_queue_summary_from_value(
                mapping["supplied_runtime_operator_review_queue_summary"]
            )
        ),
        final_packet_id=mapping["final_packet_id"],
        final_packet_summary=mapping["final_packet_summary"],
        operator_review_summary=mapping["operator_review_summary"],
        blocked_reason_summary=mapping["blocked_reason_summary"],
        operator_review_final_packet_status=_enum_value(
            OperatorReviewFinalPacketStatus,
            mapping["operator_review_final_packet_status"],
        ),
        operator_review_final_completeness_status=_enum_value(
            OperatorReviewFinalCompletenessStatus,
            mapping["operator_review_final_completeness_status"],
        ),
        operator_review_final_posture=_enum_value(
            OperatorReviewFinalPosture,
            mapping["operator_review_final_posture"],
        ),
        operator_review_status=_enum_value(OperatorReviewStatus, mapping["operator_review_status"]),
        runtime_gate_status=_enum_value(RuntimeGateStatus, mapping["runtime_gate_status"]),
        provenance_notes=str(mapping.get("provenance_notes", "")),
    )


def validate_supplied_runtime_operator_review_final_packet_record(
    record: SuppliedRuntimeOperatorReviewFinalPacketRecord,
) -> SuppliedRuntimeOperatorReviewFinalPacketValidationResult:
    """Validate a supplied operator-review final packet with fail-closed behavior."""

    reasons: list[str] = []

    for field_name, value in (
        ("condition_id", record.condition_id),
        ("token_id", record.token_id),
        ("outcome", record.outcome),
        ("final_packet_id", record.final_packet_id),
        ("final_packet_summary", record.final_packet_summary),
        ("operator_review_summary", record.operator_review_summary),
    ):
        if not _is_nonblank_text(value):
            reasons.append(f"{field_name} is missing")

    queue_summary_result = validate_supplied_runtime_operator_review_queue_summary_record(
        record.supplied_runtime_operator_review_queue_summary
    )
    if not queue_summary_result.passed:
        reasons.append("supplied runtime operator-review queue summary validation failed")

    for field_name in ("condition_id", "token_id", "outcome"):
        if getattr(record, field_name) != getattr(
            record.supplied_runtime_operator_review_queue_summary,
            field_name,
        ):
            reasons.append(
                f"{field_name} does not match supplied runtime operator-review queue summary"
            )

    if (
        record.operator_review_summary
        != record.supplied_runtime_operator_review_queue_summary.operator_review_summary
    ):
        reasons.append(
            "operator_review_summary does not match supplied runtime operator-review queue summary"
        )

    if (
        record.operator_review_final_packet_status
        is not OperatorReviewFinalPacketStatus.OPERATOR_REVIEW_FINAL_PACKET_RECORDED
    ):
        reasons.append(
            "operator review final packet status is "
            f"{record.operator_review_final_packet_status.value}"
        )

    if (
        record.operator_review_final_completeness_status
        is not OperatorReviewFinalCompletenessStatus.OPERATOR_REVIEW_FINAL_COMPLETE
    ):
        reasons.append(
            "operator review final completeness status is "
            f"{record.operator_review_final_completeness_status.value}"
        )

    if (
        record.operator_review_final_posture
        is not OperatorReviewFinalPosture.OPERATOR_REVIEW_FINAL_IN_MEMORY_ONLY
    ):
        reasons.append(
            "operator review final posture is "
            f"{record.operator_review_final_posture.value}"
        )

    if record.operator_review_status is not OperatorReviewStatus.OPERATOR_REVIEW_REQUIRED:
        reasons.append(f"operator review status is {record.operator_review_status.value}")

    if record.runtime_gate_status is not RuntimeGateStatus.RUNTIME_GATE_READY:
        reasons.append(f"runtime gate status is {record.runtime_gate_status.value}")

    if reasons and not _is_nonblank_text(record.blocked_reason_summary):
        reasons.append("blocked_reason_summary is missing")

    if reasons:
        return SuppliedRuntimeOperatorReviewFinalPacketValidationResult(
            severity=ValidationSeverity.BLOCKED,
            passed=False,
            reasons=tuple(reasons),
        )

    return SuppliedRuntimeOperatorReviewFinalPacketValidationResult(
        severity=ValidationSeverity.PASSED,
        passed=True,
        reasons=(),
    )
