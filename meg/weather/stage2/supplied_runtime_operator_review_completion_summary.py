"""Pure supplied-input runtime operator-review completion summary scaffold.

This module consumes only caller-supplied values. The completion summary is an
in-memory record only. It performs no data collection, file access, service
access, source fetching, scoring, backtesting, paper trading, trading, autonomy,
persistence, export writing, owner-decision capture, decision execution, queue
service, scheduler, broker, generated-summary behavior, durable seal,
workflow-completion side effect, or production behavior.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping

from meg.weather.stage2.supplied_runtime_operator_review_completion_seal import (
    SuppliedRuntimeOperatorReviewCompletionSealRecord,
    supplied_runtime_operator_review_completion_seal_record_from_mapping,
    validate_supplied_runtime_operator_review_completion_seal_record,
)


class _ClosedValue(str, Enum):
    """String enum base for closed, machine-checkable Stage 2 values."""

    @classmethod
    def values(cls) -> frozenset[str]:
        return frozenset(member.value for member in cls)


class OperatorReviewCompletionSummaryStatus(_ClosedValue):
    OPERATOR_REVIEW_COMPLETION_SUMMARY_RECORDED = "operator_review_completion_summary_recorded"
    OPERATOR_REVIEW_COMPLETION_SUMMARY_MISSING = "operator_review_completion_summary_missing"
    OPERATOR_REVIEW_COMPLETION_SUMMARY_AMBIGUOUS = "operator_review_completion_summary_ambiguous"
    OPERATOR_REVIEW_COMPLETION_SUMMARY_UNSUPPORTED = "operator_review_completion_summary_unsupported"
    OPERATOR_REVIEW_COMPLETION_SUMMARY_UNKNOWN = "operator_review_completion_summary_unknown"


class OperatorReviewCompletionSummaryCompletenessStatus(_ClosedValue):
    OPERATOR_REVIEW_COMPLETION_SUMMARY_COMPLETE = "operator_review_completion_summary_complete"
    OPERATOR_REVIEW_COMPLETION_SUMMARY_INCOMPLETE = "operator_review_completion_summary_incomplete"
    OPERATOR_REVIEW_COMPLETION_SUMMARY_AMBIGUOUS = "operator_review_completion_summary_ambiguous"
    OPERATOR_REVIEW_COMPLETION_SUMMARY_UNKNOWN = "operator_review_completion_summary_unknown"


class OperatorReviewCompletionSummaryPosture(_ClosedValue):
    OPERATOR_REVIEW_COMPLETION_SUMMARY_IN_MEMORY_ONLY = "operator_review_completion_summary_in_memory_only"
    OPERATOR_REVIEW_COMPLETION_SUMMARY_MISSING = "operator_review_completion_summary_missing"
    OPERATOR_REVIEW_COMPLETION_SUMMARY_AMBIGUOUS = "operator_review_completion_summary_ambiguous"
    OPERATOR_REVIEW_COMPLETION_SUMMARY_UNSUPPORTED = "operator_review_completion_summary_unsupported"
    OPERATOR_REVIEW_COMPLETION_SUMMARY_UNKNOWN = "operator_review_completion_summary_unknown"


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
class SuppliedRuntimeOperatorReviewCompletionSummaryRecord:
    condition_id: str
    token_id: str
    outcome: str
    supplied_runtime_operator_review_completion_seal: SuppliedRuntimeOperatorReviewCompletionSealRecord
    completion_summary_id: str
    completion_summary_text: str
    operator_review_summary: str
    blocked_reason_summary: str
    operator_review_completion_summary_status: OperatorReviewCompletionSummaryStatus
    operator_review_completion_summary_completeness_status: OperatorReviewCompletionSummaryCompletenessStatus
    operator_review_completion_summary_posture: OperatorReviewCompletionSummaryPosture
    operator_review_status: OperatorReviewStatus
    runtime_gate_status: RuntimeGateStatus
    provenance_notes: str = ""


@dataclass(frozen=True)
class SuppliedRuntimeOperatorReviewCompletionSummaryValidationResult:
    severity: ValidationSeverity
    passed: bool
    reasons: tuple[str, ...] = ()


def _enum_value(enum_type: type[_ClosedValue], value: _ClosedValue | str) -> _ClosedValue:
    if isinstance(value, enum_type):
        return value
    return enum_type(value)


def _is_nonblank_text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _supplied_runtime_operator_review_completion_seal_from_value(
    value: SuppliedRuntimeOperatorReviewCompletionSealRecord | Mapping[str, Any],
) -> SuppliedRuntimeOperatorReviewCompletionSealRecord:
    if isinstance(value, SuppliedRuntimeOperatorReviewCompletionSealRecord):
        return value
    return supplied_runtime_operator_review_completion_seal_record_from_mapping(value)


def supplied_runtime_operator_review_completion_summary_record_from_mapping(
    mapping: Mapping[str, Any],
) -> SuppliedRuntimeOperatorReviewCompletionSummaryRecord:
    """Build operator-review completion summary metadata from supplied values."""

    return SuppliedRuntimeOperatorReviewCompletionSummaryRecord(
        condition_id=mapping["condition_id"],
        token_id=mapping["token_id"],
        outcome=mapping["outcome"],
        supplied_runtime_operator_review_completion_seal=(
            _supplied_runtime_operator_review_completion_seal_from_value(
                mapping["supplied_runtime_operator_review_completion_seal"]
            )
        ),
        completion_summary_id=mapping["completion_summary_id"],
        completion_summary_text=mapping["completion_summary_text"],
        operator_review_summary=mapping["operator_review_summary"],
        blocked_reason_summary=mapping["blocked_reason_summary"],
        operator_review_completion_summary_status=_enum_value(
            OperatorReviewCompletionSummaryStatus,
            mapping["operator_review_completion_summary_status"],
        ),
        operator_review_completion_summary_completeness_status=_enum_value(
            OperatorReviewCompletionSummaryCompletenessStatus,
            mapping["operator_review_completion_summary_completeness_status"],
        ),
        operator_review_completion_summary_posture=_enum_value(
            OperatorReviewCompletionSummaryPosture,
            mapping["operator_review_completion_summary_posture"],
        ),
        operator_review_status=_enum_value(OperatorReviewStatus, mapping["operator_review_status"]),
        runtime_gate_status=_enum_value(RuntimeGateStatus, mapping["runtime_gate_status"]),
        provenance_notes=str(mapping.get("provenance_notes", "")),
    )


def validate_supplied_runtime_operator_review_completion_summary_record(
    record: SuppliedRuntimeOperatorReviewCompletionSummaryRecord,
) -> SuppliedRuntimeOperatorReviewCompletionSummaryValidationResult:
    """Validate a supplied operator-review completion summary with fail-closed behavior."""

    reasons: list[str] = []

    for field_name, value in (
        ("condition_id", record.condition_id),
        ("token_id", record.token_id),
        ("outcome", record.outcome),
        ("completion_summary_id", record.completion_summary_id),
        ("completion_summary_text", record.completion_summary_text),
        ("operator_review_summary", record.operator_review_summary),
    ):
        if not _is_nonblank_text(value):
            reasons.append(f"{field_name} is missing")

    completion_seal_result = validate_supplied_runtime_operator_review_completion_seal_record(
        record.supplied_runtime_operator_review_completion_seal
    )
    if not completion_seal_result.passed:
        reasons.append("supplied runtime operator-review completion seal validation failed")

    for field_name in ("condition_id", "token_id", "outcome"):
        if getattr(record, field_name) != getattr(
            record.supplied_runtime_operator_review_completion_seal,
            field_name,
        ):
            reasons.append(
                f"{field_name} does not match supplied runtime operator-review completion seal"
            )

    if (
        record.operator_review_summary
        != record.supplied_runtime_operator_review_completion_seal.operator_review_summary
    ):
        reasons.append(
            "operator_review_summary does not match supplied runtime operator-review completion seal"
        )

    if (
        record.operator_review_completion_summary_status
        is not OperatorReviewCompletionSummaryStatus.OPERATOR_REVIEW_COMPLETION_SUMMARY_RECORDED
    ):
        reasons.append(
            "operator review completion summary status is "
            f"{record.operator_review_completion_summary_status.value}"
        )

    if (
        record.operator_review_completion_summary_completeness_status
        is not OperatorReviewCompletionSummaryCompletenessStatus.OPERATOR_REVIEW_COMPLETION_SUMMARY_COMPLETE
    ):
        reasons.append(
            "operator review completion summary completeness status is "
            f"{record.operator_review_completion_summary_completeness_status.value}"
        )

    if (
        record.operator_review_completion_summary_posture
        is not OperatorReviewCompletionSummaryPosture.OPERATOR_REVIEW_COMPLETION_SUMMARY_IN_MEMORY_ONLY
    ):
        reasons.append(
            "operator review completion summary posture is "
            f"{record.operator_review_completion_summary_posture.value}"
        )

    if record.operator_review_status is not OperatorReviewStatus.OPERATOR_REVIEW_REQUIRED:
        reasons.append(f"operator review status is {record.operator_review_status.value}")

    if record.runtime_gate_status is not RuntimeGateStatus.RUNTIME_GATE_READY:
        reasons.append(f"runtime gate status is {record.runtime_gate_status.value}")

    if reasons and not _is_nonblank_text(record.blocked_reason_summary):
        reasons.append("blocked_reason_summary is missing")

    if reasons:
        return SuppliedRuntimeOperatorReviewCompletionSummaryValidationResult(
            severity=ValidationSeverity.BLOCKED,
            passed=False,
            reasons=tuple(reasons),
        )

    return SuppliedRuntimeOperatorReviewCompletionSummaryValidationResult(
        severity=ValidationSeverity.PASSED,
        passed=True,
        reasons=(),
    )
