"""Pure supplied-input runtime end-to-end smoke scaffold.

This module consumes only caller-supplied values for runtime end-to-end smoke
metadata. The smoke result is an in-memory record only. It performs no data
collection, file access, service access, source fetching, scoring,
backtesting, paper trading, trading, autonomy, persistence, export writing,
or production behavior.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping

from meg.weather.stage2.supplied_runtime_dry_run_report import (
    SuppliedRuntimeDryRunReportRecord,
    supplied_runtime_dry_run_report_record_from_mapping,
    validate_supplied_runtime_dry_run_report_record,
)


class _ClosedValue(str, Enum):
    """String enum base for closed, machine-checkable Stage 2 values."""

    @classmethod
    def values(cls) -> frozenset[str]:
        return frozenset(member.value for member in cls)


class EndToEndSmokeStatus(_ClosedValue):
    END_TO_END_SMOKE_RECORDED = "end_to_end_smoke_recorded"
    END_TO_END_SMOKE_MISSING = "end_to_end_smoke_missing"
    END_TO_END_SMOKE_AMBIGUOUS = "end_to_end_smoke_ambiguous"
    END_TO_END_SMOKE_UNSUPPORTED = "end_to_end_smoke_unsupported"
    END_TO_END_SMOKE_UNKNOWN = "end_to_end_smoke_unknown"


class EndToEndSmokeCompletenessStatus(_ClosedValue):
    END_TO_END_SMOKE_COMPLETE = "end_to_end_smoke_complete"
    END_TO_END_SMOKE_INCOMPLETE = "end_to_end_smoke_incomplete"
    END_TO_END_SMOKE_AMBIGUOUS = "end_to_end_smoke_ambiguous"
    END_TO_END_SMOKE_UNKNOWN = "end_to_end_smoke_unknown"


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
class SuppliedRuntimeEndToEndSmokeRecord:
    condition_id: str
    token_id: str
    outcome: str
    supplied_runtime_dry_run_report: SuppliedRuntimeDryRunReportRecord
    smoke_id: str
    smoke_summary: str
    operator_review_summary: str
    blocked_reason_summary: str
    end_to_end_smoke_status: EndToEndSmokeStatus
    end_to_end_smoke_completeness_status: EndToEndSmokeCompletenessStatus
    operator_review_status: OperatorReviewStatus
    runtime_gate_status: RuntimeGateStatus
    provenance_notes: str = ""


@dataclass(frozen=True)
class SuppliedRuntimeEndToEndSmokeValidationResult:
    severity: ValidationSeverity
    passed: bool
    reasons: tuple[str, ...] = ()


def _enum_value(enum_type: type[_ClosedValue], value: _ClosedValue | str) -> _ClosedValue:
    if isinstance(value, enum_type):
        return value
    return enum_type(value)


def _is_nonblank_text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _supplied_runtime_dry_run_report_from_value(
    value: SuppliedRuntimeDryRunReportRecord | Mapping[str, Any],
) -> SuppliedRuntimeDryRunReportRecord:
    if isinstance(value, SuppliedRuntimeDryRunReportRecord):
        return value
    return supplied_runtime_dry_run_report_record_from_mapping(value)


def supplied_runtime_end_to_end_smoke_record_from_mapping(
    mapping: Mapping[str, Any],
) -> SuppliedRuntimeEndToEndSmokeRecord:
    """Build end-to-end smoke metadata from explicitly supplied values."""

    return SuppliedRuntimeEndToEndSmokeRecord(
        condition_id=mapping["condition_id"],
        token_id=mapping["token_id"],
        outcome=mapping["outcome"],
        supplied_runtime_dry_run_report=_supplied_runtime_dry_run_report_from_value(
            mapping["supplied_runtime_dry_run_report"]
        ),
        smoke_id=mapping["smoke_id"],
        smoke_summary=mapping["smoke_summary"],
        operator_review_summary=mapping["operator_review_summary"],
        blocked_reason_summary=mapping["blocked_reason_summary"],
        end_to_end_smoke_status=_enum_value(
            EndToEndSmokeStatus,
            mapping["end_to_end_smoke_status"],
        ),
        end_to_end_smoke_completeness_status=_enum_value(
            EndToEndSmokeCompletenessStatus,
            mapping["end_to_end_smoke_completeness_status"],
        ),
        operator_review_status=_enum_value(
            OperatorReviewStatus,
            mapping["operator_review_status"],
        ),
        runtime_gate_status=_enum_value(RuntimeGateStatus, mapping["runtime_gate_status"]),
        provenance_notes=str(mapping.get("provenance_notes", "")),
    )


def validate_supplied_runtime_end_to_end_smoke_record(
    record: SuppliedRuntimeEndToEndSmokeRecord,
) -> SuppliedRuntimeEndToEndSmokeValidationResult:
    """Validate a supplied runtime end-to-end smoke with fail-closed behavior."""

    reasons: list[str] = []

    for field_name, value in (
        ("condition_id", record.condition_id),
        ("token_id", record.token_id),
        ("outcome", record.outcome),
        ("smoke_id", record.smoke_id),
        ("smoke_summary", record.smoke_summary),
        ("operator_review_summary", record.operator_review_summary),
    ):
        if not _is_nonblank_text(value):
            reasons.append(f"{field_name} is missing")

    report_result = validate_supplied_runtime_dry_run_report_record(
        record.supplied_runtime_dry_run_report
    )
    if not report_result.passed:
        reasons.append("supplied runtime dry-run report validation failed")

    for field_name in ("condition_id", "token_id", "outcome"):
        if getattr(record, field_name) != getattr(
            record.supplied_runtime_dry_run_report,
            field_name,
        ):
            reasons.append(f"{field_name} does not match supplied runtime dry-run report")

    if (
        record.operator_review_summary
        != record.supplied_runtime_dry_run_report.operator_review_summary
    ):
        reasons.append("operator_review_summary does not match supplied runtime dry-run report")

    if (
        record.end_to_end_smoke_status
        is not EndToEndSmokeStatus.END_TO_END_SMOKE_RECORDED
    ):
        reasons.append(f"end-to-end smoke status is {record.end_to_end_smoke_status.value}")

    if (
        record.end_to_end_smoke_completeness_status
        is not EndToEndSmokeCompletenessStatus.END_TO_END_SMOKE_COMPLETE
    ):
        reasons.append(
            f"end-to-end smoke completeness status is "
            f"{record.end_to_end_smoke_completeness_status.value}"
        )

    if record.operator_review_status is not OperatorReviewStatus.OPERATOR_REVIEW_REQUIRED:
        reasons.append(f"operator review status is {record.operator_review_status.value}")

    if record.runtime_gate_status is not RuntimeGateStatus.RUNTIME_GATE_READY:
        reasons.append(f"runtime gate status is {record.runtime_gate_status.value}")

    if reasons and not _is_nonblank_text(record.blocked_reason_summary):
        reasons.append("blocked_reason_summary is missing")

    if reasons:
        return SuppliedRuntimeEndToEndSmokeValidationResult(
            severity=ValidationSeverity.BLOCKED,
            passed=False,
            reasons=tuple(reasons),
        )

    return SuppliedRuntimeEndToEndSmokeValidationResult(
        severity=ValidationSeverity.PASSED,
        passed=True,
    )
