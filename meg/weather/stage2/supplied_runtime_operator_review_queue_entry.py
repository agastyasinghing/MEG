"""Pure supplied-input runtime operator-review queue entry scaffold.

This module consumes only caller-supplied values for runtime operator-review
queue entry metadata. The queue entry is an in-memory record only. It performs
no data collection, file access, service access, source fetching, scoring,
backtesting, paper trading, trading, autonomy, persistence, export writing,
owner-decision capture, decision execution, queue service, scheduler, broker,
or production behavior.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping

from meg.weather.stage2.supplied_runtime_operator_review_queue_packet import (
    SuppliedRuntimeOperatorReviewQueuePacketRecord,
    supplied_runtime_operator_review_queue_packet_record_from_mapping,
    validate_supplied_runtime_operator_review_queue_packet_record,
)


class _ClosedValue(str, Enum):
    """String enum base for closed, machine-checkable Stage 2 values."""

    @classmethod
    def values(cls) -> frozenset[str]:
        return frozenset(member.value for member in cls)


class OperatorReviewQueueEntryStatus(_ClosedValue):
    OPERATOR_REVIEW_QUEUE_ENTRY_RECORDED = "operator_review_queue_entry_recorded"
    OPERATOR_REVIEW_QUEUE_ENTRY_MISSING = "operator_review_queue_entry_missing"
    OPERATOR_REVIEW_QUEUE_ENTRY_AMBIGUOUS = "operator_review_queue_entry_ambiguous"
    OPERATOR_REVIEW_QUEUE_ENTRY_UNSUPPORTED = "operator_review_queue_entry_unsupported"
    OPERATOR_REVIEW_QUEUE_ENTRY_UNKNOWN = "operator_review_queue_entry_unknown"


class OperatorReviewQueueEntryCompletenessStatus(_ClosedValue):
    OPERATOR_REVIEW_QUEUE_ENTRY_COMPLETE = "operator_review_queue_entry_complete"
    OPERATOR_REVIEW_QUEUE_ENTRY_INCOMPLETE = "operator_review_queue_entry_incomplete"
    OPERATOR_REVIEW_QUEUE_ENTRY_AMBIGUOUS = "operator_review_queue_entry_ambiguous"
    OPERATOR_REVIEW_QUEUE_ENTRY_UNKNOWN = "operator_review_queue_entry_unknown"


class OperatorReviewQueueEntryPosture(_ClosedValue):
    OPERATOR_REVIEW_QUEUE_ENTRY_IN_MEMORY_ONLY = "operator_review_queue_entry_in_memory_only"
    OPERATOR_REVIEW_QUEUE_ENTRY_MISSING = "operator_review_queue_entry_missing"
    OPERATOR_REVIEW_QUEUE_ENTRY_AMBIGUOUS = "operator_review_queue_entry_ambiguous"
    OPERATOR_REVIEW_QUEUE_ENTRY_UNSUPPORTED = "operator_review_queue_entry_unsupported"
    OPERATOR_REVIEW_QUEUE_ENTRY_UNKNOWN = "operator_review_queue_entry_unknown"


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
class SuppliedRuntimeOperatorReviewQueueEntryRecord:
    condition_id: str
    token_id: str
    outcome: str
    supplied_runtime_operator_review_queue_packet: SuppliedRuntimeOperatorReviewQueuePacketRecord
    queue_entry_id: str
    queue_entry_summary: str
    operator_review_summary: str
    blocked_reason_summary: str
    operator_review_queue_entry_status: OperatorReviewQueueEntryStatus
    operator_review_queue_entry_completeness_status: OperatorReviewQueueEntryCompletenessStatus
    operator_review_queue_entry_posture: OperatorReviewQueueEntryPosture
    operator_review_status: OperatorReviewStatus
    runtime_gate_status: RuntimeGateStatus
    provenance_notes: str = ""


@dataclass(frozen=True)
class SuppliedRuntimeOperatorReviewQueueEntryValidationResult:
    severity: ValidationSeverity
    passed: bool
    reasons: tuple[str, ...] = ()


def _enum_value(enum_type: type[_ClosedValue], value: _ClosedValue | str) -> _ClosedValue:
    if isinstance(value, enum_type):
        return value
    return enum_type(value)


def _is_nonblank_text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _supplied_runtime_operator_review_queue_packet_from_value(
    value: SuppliedRuntimeOperatorReviewQueuePacketRecord | Mapping[str, Any],
) -> SuppliedRuntimeOperatorReviewQueuePacketRecord:
    if isinstance(value, SuppliedRuntimeOperatorReviewQueuePacketRecord):
        return value
    return supplied_runtime_operator_review_queue_packet_record_from_mapping(value)


def supplied_runtime_operator_review_queue_entry_record_from_mapping(
    mapping: Mapping[str, Any],
) -> SuppliedRuntimeOperatorReviewQueueEntryRecord:
    """Build operator-review queue entry metadata from supplied values."""

    return SuppliedRuntimeOperatorReviewQueueEntryRecord(
        condition_id=mapping["condition_id"],
        token_id=mapping["token_id"],
        outcome=mapping["outcome"],
        supplied_runtime_operator_review_queue_packet=(
            _supplied_runtime_operator_review_queue_packet_from_value(
                mapping["supplied_runtime_operator_review_queue_packet"]
            )
        ),
        queue_entry_id=mapping["queue_entry_id"],
        queue_entry_summary=mapping["queue_entry_summary"],
        operator_review_summary=mapping["operator_review_summary"],
        blocked_reason_summary=mapping["blocked_reason_summary"],
        operator_review_queue_entry_status=_enum_value(
            OperatorReviewQueueEntryStatus,
            mapping["operator_review_queue_entry_status"],
        ),
        operator_review_queue_entry_completeness_status=_enum_value(
            OperatorReviewQueueEntryCompletenessStatus,
            mapping["operator_review_queue_entry_completeness_status"],
        ),
        operator_review_queue_entry_posture=_enum_value(
            OperatorReviewQueueEntryPosture,
            mapping["operator_review_queue_entry_posture"],
        ),
        operator_review_status=_enum_value(
            OperatorReviewStatus,
            mapping["operator_review_status"],
        ),
        runtime_gate_status=_enum_value(RuntimeGateStatus, mapping["runtime_gate_status"]),
        provenance_notes=str(mapping.get("provenance_notes", "")),
    )


def validate_supplied_runtime_operator_review_queue_entry_record(
    record: SuppliedRuntimeOperatorReviewQueueEntryRecord,
) -> SuppliedRuntimeOperatorReviewQueueEntryValidationResult:
    """Validate a supplied operator-review queue entry with fail-closed behavior."""

    reasons: list[str] = []

    for field_name, value in (
        ("condition_id", record.condition_id),
        ("token_id", record.token_id),
        ("outcome", record.outcome),
        ("queue_entry_id", record.queue_entry_id),
        ("queue_entry_summary", record.queue_entry_summary),
        ("operator_review_summary", record.operator_review_summary),
    ):
        if not _is_nonblank_text(value):
            reasons.append(f"{field_name} is missing")

    queue_packet_result = validate_supplied_runtime_operator_review_queue_packet_record(
        record.supplied_runtime_operator_review_queue_packet
    )
    if not queue_packet_result.passed:
        reasons.append("supplied runtime operator-review queue packet validation failed")

    for field_name in ("condition_id", "token_id", "outcome"):
        if getattr(record, field_name) != getattr(
            record.supplied_runtime_operator_review_queue_packet,
            field_name,
        ):
            reasons.append(
                f"{field_name} does not match supplied runtime operator-review queue packet"
            )

    if (
        record.operator_review_summary
        != record.supplied_runtime_operator_review_queue_packet.operator_review_summary
    ):
        reasons.append(
            "operator_review_summary does not match supplied runtime operator-review queue packet"
        )

    if (
        record.operator_review_queue_entry_status
        is not OperatorReviewQueueEntryStatus.OPERATOR_REVIEW_QUEUE_ENTRY_RECORDED
    ):
        reasons.append(
            "operator review queue entry status is "
            f"{record.operator_review_queue_entry_status.value}"
        )

    if (
        record.operator_review_queue_entry_completeness_status
        is not OperatorReviewQueueEntryCompletenessStatus.OPERATOR_REVIEW_QUEUE_ENTRY_COMPLETE
    ):
        reasons.append(
            "operator review queue entry completeness status is "
            f"{record.operator_review_queue_entry_completeness_status.value}"
        )

    if (
        record.operator_review_queue_entry_posture
        is not OperatorReviewQueueEntryPosture.OPERATOR_REVIEW_QUEUE_ENTRY_IN_MEMORY_ONLY
    ):
        reasons.append(
            "operator review queue entry posture is "
            f"{record.operator_review_queue_entry_posture.value}"
        )

    if record.operator_review_status is not OperatorReviewStatus.OPERATOR_REVIEW_REQUIRED:
        reasons.append(f"operator review status is {record.operator_review_status.value}")

    if record.runtime_gate_status is not RuntimeGateStatus.RUNTIME_GATE_READY:
        reasons.append(f"runtime gate status is {record.runtime_gate_status.value}")

    if reasons and not _is_nonblank_text(record.blocked_reason_summary):
        reasons.append("blocked_reason_summary is missing")

    if reasons:
        return SuppliedRuntimeOperatorReviewQueueEntryValidationResult(
            severity=ValidationSeverity.BLOCKED,
            passed=False,
            reasons=tuple(reasons),
        )

    return SuppliedRuntimeOperatorReviewQueueEntryValidationResult(
        severity=ValidationSeverity.PASSED,
        passed=True,
    )
