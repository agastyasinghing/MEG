"""Pure supplied-input runtime dry-run report scaffold.

This module consumes only caller-supplied values for runtime dry-run report
metadata. The report is an in-memory record only. It performs no data
collection, file access, service access, source fetching, scoring,
backtesting, paper trading, trading, autonomy, persistence, export writing,
or production behavior.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping

from meg.weather.stage2.supplied_runtime_dry_run_packet import (
    SuppliedRuntimeDryRunPacketRecord,
    supplied_runtime_dry_run_packet_record_from_mapping,
    validate_supplied_runtime_dry_run_packet_record,
)


class _ClosedValue(str, Enum):
    """String enum base for closed, machine-checkable Stage 2 values."""

    @classmethod
    def values(cls) -> frozenset[str]:
        return frozenset(member.value for member in cls)


class DryRunReportStatus(_ClosedValue):
    DRY_RUN_REPORT_RECORDED = "dry_run_report_recorded"
    DRY_RUN_REPORT_MISSING = "dry_run_report_missing"
    DRY_RUN_REPORT_AMBIGUOUS = "dry_run_report_ambiguous"
    DRY_RUN_REPORT_UNSUPPORTED = "dry_run_report_unsupported"
    DRY_RUN_REPORT_UNKNOWN = "dry_run_report_unknown"


class DryRunReportCompletenessStatus(_ClosedValue):
    DRY_RUN_REPORT_COMPLETE = "dry_run_report_complete"
    DRY_RUN_REPORT_INCOMPLETE = "dry_run_report_incomplete"
    DRY_RUN_REPORT_AMBIGUOUS = "dry_run_report_ambiguous"
    DRY_RUN_REPORT_UNKNOWN = "dry_run_report_unknown"


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
class SuppliedRuntimeDryRunReportRecord:
    condition_id: str
    token_id: str
    outcome: str
    supplied_runtime_dry_run_packet: SuppliedRuntimeDryRunPacketRecord
    dry_run_report_id: str
    report_summary: str
    operator_review_summary: str
    blocked_reason_summary: str
    dry_run_report_status: DryRunReportStatus
    dry_run_report_completeness_status: DryRunReportCompletenessStatus
    operator_review_status: OperatorReviewStatus
    runtime_gate_status: RuntimeGateStatus
    provenance_notes: str = ""


@dataclass(frozen=True)
class SuppliedRuntimeDryRunReportValidationResult:
    severity: ValidationSeverity
    passed: bool
    reasons: tuple[str, ...] = ()


def _enum_value(enum_type: type[_ClosedValue], value: _ClosedValue | str) -> _ClosedValue:
    if isinstance(value, enum_type):
        return value
    return enum_type(value)


def _is_nonblank_text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _supplied_runtime_dry_run_packet_from_value(
    value: SuppliedRuntimeDryRunPacketRecord | Mapping[str, Any],
) -> SuppliedRuntimeDryRunPacketRecord:
    if isinstance(value, SuppliedRuntimeDryRunPacketRecord):
        return value
    return supplied_runtime_dry_run_packet_record_from_mapping(value)


def supplied_runtime_dry_run_report_record_from_mapping(
    mapping: Mapping[str, Any],
) -> SuppliedRuntimeDryRunReportRecord:
    """Build dry-run report metadata from explicitly supplied values."""

    return SuppliedRuntimeDryRunReportRecord(
        condition_id=mapping["condition_id"],
        token_id=mapping["token_id"],
        outcome=mapping["outcome"],
        supplied_runtime_dry_run_packet=_supplied_runtime_dry_run_packet_from_value(
            mapping["supplied_runtime_dry_run_packet"]
        ),
        dry_run_report_id=mapping["dry_run_report_id"],
        report_summary=mapping["report_summary"],
        operator_review_summary=mapping["operator_review_summary"],
        blocked_reason_summary=mapping["blocked_reason_summary"],
        dry_run_report_status=_enum_value(
            DryRunReportStatus,
            mapping["dry_run_report_status"],
        ),
        dry_run_report_completeness_status=_enum_value(
            DryRunReportCompletenessStatus,
            mapping["dry_run_report_completeness_status"],
        ),
        operator_review_status=_enum_value(
            OperatorReviewStatus,
            mapping["operator_review_status"],
        ),
        runtime_gate_status=_enum_value(RuntimeGateStatus, mapping["runtime_gate_status"]),
        provenance_notes=str(mapping.get("provenance_notes", "")),
    )


def validate_supplied_runtime_dry_run_report_record(
    record: SuppliedRuntimeDryRunReportRecord,
) -> SuppliedRuntimeDryRunReportValidationResult:
    """Validate a supplied runtime dry-run report with fail-closed behavior."""

    reasons: list[str] = []

    for field_name, value in (
        ("condition_id", record.condition_id),
        ("token_id", record.token_id),
        ("outcome", record.outcome),
        ("dry_run_report_id", record.dry_run_report_id),
        ("report_summary", record.report_summary),
        ("operator_review_summary", record.operator_review_summary),
    ):
        if not _is_nonblank_text(value):
            reasons.append(f"{field_name} is missing")

    packet_result = validate_supplied_runtime_dry_run_packet_record(
        record.supplied_runtime_dry_run_packet
    )
    if not packet_result.passed:
        reasons.append("supplied runtime dry-run packet validation failed")

    for field_name in ("condition_id", "token_id", "outcome"):
        if getattr(record, field_name) != getattr(
            record.supplied_runtime_dry_run_packet,
            field_name,
        ):
            reasons.append(f"{field_name} does not match supplied runtime dry-run packet")

    if (
        record.operator_review_summary
        != record.supplied_runtime_dry_run_packet.operator_review_summary
    ):
        reasons.append("operator_review_summary does not match supplied runtime dry-run packet")

    if record.dry_run_report_status is not DryRunReportStatus.DRY_RUN_REPORT_RECORDED:
        reasons.append(f"dry run report status is {record.dry_run_report_status.value}")

    if (
        record.dry_run_report_completeness_status
        is not DryRunReportCompletenessStatus.DRY_RUN_REPORT_COMPLETE
    ):
        reasons.append(
            f"dry run report completeness status is "
            f"{record.dry_run_report_completeness_status.value}"
        )

    if record.operator_review_status is not OperatorReviewStatus.OPERATOR_REVIEW_REQUIRED:
        reasons.append(f"operator review status is {record.operator_review_status.value}")

    if record.runtime_gate_status is not RuntimeGateStatus.RUNTIME_GATE_READY:
        reasons.append(f"runtime gate status is {record.runtime_gate_status.value}")

    if reasons and not _is_nonblank_text(record.blocked_reason_summary):
        reasons.append("blocked_reason_summary is missing")

    if reasons:
        return SuppliedRuntimeDryRunReportValidationResult(
            severity=ValidationSeverity.BLOCKED,
            passed=False,
            reasons=tuple(reasons),
        )

    return SuppliedRuntimeDryRunReportValidationResult(
        severity=ValidationSeverity.PASSED,
        passed=True,
    )
