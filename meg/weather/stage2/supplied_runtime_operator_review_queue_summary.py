"""Pure supplied-input runtime operator-review queue summary scaffold.

This module consumes only caller-supplied values for runtime operator-review
queue summary metadata. The queue summary is an in-memory record only. It
performs no data collection, file access, service access, source fetching,
scoring, backtesting, paper trading, trading, autonomy, persistence, export
writing, owner-decision capture, decision execution, queue service, scheduler,
broker, or production behavior.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping

from meg.weather.stage2.supplied_runtime_operator_review_queue_entry import (
    SuppliedRuntimeOperatorReviewQueueEntryRecord,
    supplied_runtime_operator_review_queue_entry_record_from_mapping,
    validate_supplied_runtime_operator_review_queue_entry_record,
)


class _ClosedValue(str, Enum):
    """String enum base for closed, machine-checkable Stage 2 values."""

    @classmethod
    def values(cls) -> frozenset[str]:
        return frozenset(member.value for member in cls)


class OperatorReviewQueueSummaryStatus(_ClosedValue):
    OPERATOR_REVIEW_QUEUE_SUMMARY_RECORDED = "operator_review_queue_summary_recorded"
    OPERATOR_REVIEW_QUEUE_SUMMARY_MISSING = "operator_review_queue_summary_missing"
    OPERATOR_REVIEW_QUEUE_SUMMARY_AMBIGUOUS = "operator_review_queue_summary_ambiguous"
    OPERATOR_REVIEW_QUEUE_SUMMARY_UNSUPPORTED = "operator_review_queue_summary_unsupported"
    OPERATOR_REVIEW_QUEUE_SUMMARY_UNKNOWN = "operator_review_queue_summary_unknown"


class OperatorReviewQueueSummaryCompletenessStatus(_ClosedValue):
    OPERATOR_REVIEW_QUEUE_SUMMARY_COMPLETE = "operator_review_queue_summary_complete"
    OPERATOR_REVIEW_QUEUE_SUMMARY_INCOMPLETE = "operator_review_queue_summary_incomplete"
    OPERATOR_REVIEW_QUEUE_SUMMARY_AMBIGUOUS = "operator_review_queue_summary_ambiguous"
    OPERATOR_REVIEW_QUEUE_SUMMARY_UNKNOWN = "operator_review_queue_summary_unknown"


class OperatorReviewQueueSummaryPosture(_ClosedValue):
    OPERATOR_REVIEW_QUEUE_SUMMARY_IN_MEMORY_ONLY = "operator_review_queue_summary_in_memory_only"
    OPERATOR_REVIEW_QUEUE_SUMMARY_MISSING = "operator_review_queue_summary_missing"
    OPERATOR_REVIEW_QUEUE_SUMMARY_AMBIGUOUS = "operator_review_queue_summary_ambiguous"
    OPERATOR_REVIEW_QUEUE_SUMMARY_UNSUPPORTED = "operator_review_queue_summary_unsupported"
    OPERATOR_REVIEW_QUEUE_SUMMARY_UNKNOWN = "operator_review_queue_summary_unknown"


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
class SuppliedRuntimeOperatorReviewQueueSummaryRecord:
    condition_id: str
    token_id: str
    outcome: str
    supplied_runtime_operator_review_queue_entry: SuppliedRuntimeOperatorReviewQueueEntryRecord
    queue_summary_id: str
    queue_summary_text: str
    operator_review_summary: str
    blocked_reason_summary: str
    operator_review_queue_summary_status: OperatorReviewQueueSummaryStatus
    operator_review_queue_summary_completeness_status: OperatorReviewQueueSummaryCompletenessStatus
    operator_review_queue_summary_posture: OperatorReviewQueueSummaryPosture
    operator_review_status: OperatorReviewStatus
    runtime_gate_status: RuntimeGateStatus
    provenance_notes: str = ""


@dataclass(frozen=True)
class SuppliedRuntimeOperatorReviewQueueSummaryValidationResult:
    severity: ValidationSeverity
    passed: bool
    reasons: tuple[str, ...] = ()


def _enum_value(enum_type: type[_ClosedValue], value: _ClosedValue | str) -> _ClosedValue:
    if isinstance(value, enum_type):
        return value
    return enum_type(value)


def _is_nonblank_text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _supplied_runtime_operator_review_queue_entry_from_value(
    value: SuppliedRuntimeOperatorReviewQueueEntryRecord | Mapping[str, Any],
) -> SuppliedRuntimeOperatorReviewQueueEntryRecord:
    if isinstance(value, SuppliedRuntimeOperatorReviewQueueEntryRecord):
        return value
    return supplied_runtime_operator_review_queue_entry_record_from_mapping(value)


def supplied_runtime_operator_review_queue_summary_record_from_mapping(
    mapping: Mapping[str, Any],
) -> SuppliedRuntimeOperatorReviewQueueSummaryRecord:
    """Build operator-review queue summary metadata from supplied values."""

    return SuppliedRuntimeOperatorReviewQueueSummaryRecord(
        condition_id=mapping["condition_id"],
        token_id=mapping["token_id"],
        outcome=mapping["outcome"],
        supplied_runtime_operator_review_queue_entry=(
            _supplied_runtime_operator_review_queue_entry_from_value(
                mapping["supplied_runtime_operator_review_queue_entry"]
            )
        ),
        queue_summary_id=mapping["queue_summary_id"],
        queue_summary_text=mapping["queue_summary_text"],
        operator_review_summary=mapping["operator_review_summary"],
        blocked_reason_summary=mapping["blocked_reason_summary"],
        operator_review_queue_summary_status=_enum_value(
            OperatorReviewQueueSummaryStatus,
            mapping["operator_review_queue_summary_status"],
        ),
        operator_review_queue_summary_completeness_status=_enum_value(
            OperatorReviewQueueSummaryCompletenessStatus,
            mapping["operator_review_queue_summary_completeness_status"],
        ),
        operator_review_queue_summary_posture=_enum_value(
            OperatorReviewQueueSummaryPosture,
            mapping["operator_review_queue_summary_posture"],
        ),
        operator_review_status=_enum_value(
            OperatorReviewStatus,
            mapping["operator_review_status"],
        ),
        runtime_gate_status=_enum_value(RuntimeGateStatus, mapping["runtime_gate_status"]),
        provenance_notes=str(mapping.get("provenance_notes", "")),
    )


def validate_supplied_runtime_operator_review_queue_summary_record(
    record: SuppliedRuntimeOperatorReviewQueueSummaryRecord,
) -> SuppliedRuntimeOperatorReviewQueueSummaryValidationResult:
    """Validate a supplied operator-review queue summary with fail-closed behavior."""

    reasons: list[str] = []

    for field_name, value in (
        ("condition_id", record.condition_id),
        ("token_id", record.token_id),
        ("outcome", record.outcome),
        ("queue_summary_id", record.queue_summary_id),
        ("queue_summary_text", record.queue_summary_text),
        ("operator_review_summary", record.operator_review_summary),
    ):
        if not _is_nonblank_text(value):
            reasons.append(f"{field_name} is missing")

    queue_entry_result = validate_supplied_runtime_operator_review_queue_entry_record(
        record.supplied_runtime_operator_review_queue_entry
    )
    if not queue_entry_result.passed:
        reasons.append("supplied runtime operator-review queue entry validation failed")

    for field_name in ("condition_id", "token_id", "outcome"):
        if getattr(record, field_name) != getattr(
            record.supplied_runtime_operator_review_queue_entry,
            field_name,
        ):
            reasons.append(
                f"{field_name} does not match supplied runtime operator-review queue entry"
            )

    if (
        record.operator_review_summary
        != record.supplied_runtime_operator_review_queue_entry.operator_review_summary
    ):
        reasons.append(
            "operator_review_summary does not match supplied runtime operator-review queue entry"
        )

    if (
        record.operator_review_queue_summary_status
        is not OperatorReviewQueueSummaryStatus.OPERATOR_REVIEW_QUEUE_SUMMARY_RECORDED
    ):
        reasons.append(
            "operator review queue summary status is "
            f"{record.operator_review_queue_summary_status.value}"
        )

    if (
        record.operator_review_queue_summary_completeness_status
        is not OperatorReviewQueueSummaryCompletenessStatus.OPERATOR_REVIEW_QUEUE_SUMMARY_COMPLETE
    ):
        reasons.append(
            "operator review queue summary completeness status is "
            f"{record.operator_review_queue_summary_completeness_status.value}"
        )

    if (
        record.operator_review_queue_summary_posture
        is not OperatorReviewQueueSummaryPosture.OPERATOR_REVIEW_QUEUE_SUMMARY_IN_MEMORY_ONLY
    ):
        reasons.append(
            "operator review queue summary posture is "
            f"{record.operator_review_queue_summary_posture.value}"
        )

    if record.operator_review_status is not OperatorReviewStatus.OPERATOR_REVIEW_REQUIRED:
        reasons.append(f"operator review status is {record.operator_review_status.value}")

    if record.runtime_gate_status is not RuntimeGateStatus.RUNTIME_GATE_READY:
        reasons.append(f"runtime gate status is {record.runtime_gate_status.value}")

    if reasons and not _is_nonblank_text(record.blocked_reason_summary):
        reasons.append("blocked_reason_summary is missing")

    if reasons:
        return SuppliedRuntimeOperatorReviewQueueSummaryValidationResult(
            severity=ValidationSeverity.BLOCKED,
            passed=False,
            reasons=tuple(reasons),
        )

    return SuppliedRuntimeOperatorReviewQueueSummaryValidationResult(
        severity=ValidationSeverity.PASSED,
        passed=True,
    )
