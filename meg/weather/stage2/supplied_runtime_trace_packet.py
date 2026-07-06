"""Pure supplied-input runtime trace packet scaffold.

This module consumes only caller-supplied values for runtime trace packet
metadata. The trace packet is an in-memory record only. It performs no data
collection, file access, service access, source fetching, scoring,
backtesting, paper trading, trading, autonomy, persistence, export writing,
or production behavior.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping

from meg.weather.stage2.supplied_runtime_end_to_end_smoke import (
    SuppliedRuntimeEndToEndSmokeRecord,
    supplied_runtime_end_to_end_smoke_record_from_mapping,
    validate_supplied_runtime_end_to_end_smoke_record,
)


class _ClosedValue(str, Enum):
    """String enum base for closed, machine-checkable Stage 2 values."""

    @classmethod
    def values(cls) -> frozenset[str]:
        return frozenset(member.value for member in cls)


class RuntimeTracePacketStatus(_ClosedValue):
    RUNTIME_TRACE_PACKET_RECORDED = "runtime_trace_packet_recorded"
    RUNTIME_TRACE_PACKET_MISSING = "runtime_trace_packet_missing"
    RUNTIME_TRACE_PACKET_AMBIGUOUS = "runtime_trace_packet_ambiguous"
    RUNTIME_TRACE_PACKET_UNSUPPORTED = "runtime_trace_packet_unsupported"
    RUNTIME_TRACE_PACKET_UNKNOWN = "runtime_trace_packet_unknown"


class RuntimeTraceCompletenessStatus(_ClosedValue):
    RUNTIME_TRACE_COMPLETE = "runtime_trace_complete"
    RUNTIME_TRACE_INCOMPLETE = "runtime_trace_incomplete"
    RUNTIME_TRACE_AMBIGUOUS = "runtime_trace_ambiguous"
    RUNTIME_TRACE_UNKNOWN = "runtime_trace_unknown"


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
class SuppliedRuntimeTracePacketRecord:
    condition_id: str
    token_id: str
    outcome: str
    supplied_runtime_end_to_end_smoke: SuppliedRuntimeEndToEndSmokeRecord
    trace_packet_id: str
    trace_summary: str
    operator_review_summary: str
    blocked_reason_summary: str
    runtime_trace_packet_status: RuntimeTracePacketStatus
    runtime_trace_completeness_status: RuntimeTraceCompletenessStatus
    operator_review_status: OperatorReviewStatus
    runtime_gate_status: RuntimeGateStatus
    provenance_notes: str = ""


@dataclass(frozen=True)
class SuppliedRuntimeTracePacketValidationResult:
    severity: ValidationSeverity
    passed: bool
    reasons: tuple[str, ...] = ()


def _enum_value(enum_type: type[_ClosedValue], value: _ClosedValue | str) -> _ClosedValue:
    if isinstance(value, enum_type):
        return value
    return enum_type(value)


def _is_nonblank_text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _supplied_runtime_end_to_end_smoke_from_value(
    value: SuppliedRuntimeEndToEndSmokeRecord | Mapping[str, Any],
) -> SuppliedRuntimeEndToEndSmokeRecord:
    if isinstance(value, SuppliedRuntimeEndToEndSmokeRecord):
        return value
    return supplied_runtime_end_to_end_smoke_record_from_mapping(value)


def supplied_runtime_trace_packet_record_from_mapping(
    mapping: Mapping[str, Any],
) -> SuppliedRuntimeTracePacketRecord:
    """Build runtime trace packet metadata from explicitly supplied values."""

    return SuppliedRuntimeTracePacketRecord(
        condition_id=mapping["condition_id"],
        token_id=mapping["token_id"],
        outcome=mapping["outcome"],
        supplied_runtime_end_to_end_smoke=_supplied_runtime_end_to_end_smoke_from_value(
            mapping["supplied_runtime_end_to_end_smoke"]
        ),
        trace_packet_id=mapping["trace_packet_id"],
        trace_summary=mapping["trace_summary"],
        operator_review_summary=mapping["operator_review_summary"],
        blocked_reason_summary=mapping["blocked_reason_summary"],
        runtime_trace_packet_status=_enum_value(
            RuntimeTracePacketStatus,
            mapping["runtime_trace_packet_status"],
        ),
        runtime_trace_completeness_status=_enum_value(
            RuntimeTraceCompletenessStatus,
            mapping["runtime_trace_completeness_status"],
        ),
        operator_review_status=_enum_value(
            OperatorReviewStatus,
            mapping["operator_review_status"],
        ),
        runtime_gate_status=_enum_value(RuntimeGateStatus, mapping["runtime_gate_status"]),
        provenance_notes=str(mapping.get("provenance_notes", "")),
    )


def validate_supplied_runtime_trace_packet_record(
    record: SuppliedRuntimeTracePacketRecord,
) -> SuppliedRuntimeTracePacketValidationResult:
    """Validate a supplied runtime trace packet with fail-closed behavior."""

    reasons: list[str] = []

    for field_name, value in (
        ("condition_id", record.condition_id),
        ("token_id", record.token_id),
        ("outcome", record.outcome),
        ("trace_packet_id", record.trace_packet_id),
        ("trace_summary", record.trace_summary),
        ("operator_review_summary", record.operator_review_summary),
    ):
        if not _is_nonblank_text(value):
            reasons.append(f"{field_name} is missing")

    smoke_result = validate_supplied_runtime_end_to_end_smoke_record(
        record.supplied_runtime_end_to_end_smoke
    )
    if not smoke_result.passed:
        reasons.append("supplied runtime end-to-end smoke validation failed")

    for field_name in ("condition_id", "token_id", "outcome"):
        if getattr(record, field_name) != getattr(
            record.supplied_runtime_end_to_end_smoke,
            field_name,
        ):
            reasons.append(
                f"{field_name} does not match supplied runtime end-to-end smoke"
            )

    if (
        record.operator_review_summary
        != record.supplied_runtime_end_to_end_smoke.operator_review_summary
    ):
        reasons.append(
            "operator_review_summary does not match supplied runtime end-to-end smoke"
        )

    if (
        record.runtime_trace_packet_status
        is not RuntimeTracePacketStatus.RUNTIME_TRACE_PACKET_RECORDED
    ):
        reasons.append(
            f"runtime trace packet status is {record.runtime_trace_packet_status.value}"
        )

    if (
        record.runtime_trace_completeness_status
        is not RuntimeTraceCompletenessStatus.RUNTIME_TRACE_COMPLETE
    ):
        reasons.append(
            f"runtime trace completeness status is "
            f"{record.runtime_trace_completeness_status.value}"
        )

    if record.operator_review_status is not OperatorReviewStatus.OPERATOR_REVIEW_REQUIRED:
        reasons.append(f"operator review status is {record.operator_review_status.value}")

    if record.runtime_gate_status is not RuntimeGateStatus.RUNTIME_GATE_READY:
        reasons.append(f"runtime gate status is {record.runtime_gate_status.value}")

    if reasons and not _is_nonblank_text(record.blocked_reason_summary):
        reasons.append("blocked_reason_summary is missing")

    if reasons:
        return SuppliedRuntimeTracePacketValidationResult(
            severity=ValidationSeverity.BLOCKED,
            passed=False,
            reasons=tuple(reasons),
        )

    return SuppliedRuntimeTracePacketValidationResult(
        severity=ValidationSeverity.PASSED,
        passed=True,
    )
