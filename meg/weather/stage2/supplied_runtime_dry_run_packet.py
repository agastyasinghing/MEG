"""Pure supplied-input runtime dry-run packet scaffold.

This module consumes only caller-supplied values for runtime dry-run packet
metadata. It performs no data collection, file access, service access, source
fetching, scoring, backtesting, paper trading, trading, autonomy, or production
behavior.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping

from meg.weather.stage2.supplied_runtime_validation_bundle import (
    SuppliedRuntimeValidationBundleRecord,
    supplied_runtime_validation_bundle_record_from_mapping,
    validate_supplied_runtime_validation_bundle_record,
)


class _ClosedValue(str, Enum):
    """String enum base for closed, machine-checkable Stage 2 values."""

    @classmethod
    def values(cls) -> frozenset[str]:
        return frozenset(member.value for member in cls)


class DryRunPacketStatus(_ClosedValue):
    DRY_RUN_PACKET_RECORDED = "dry_run_packet_recorded"
    DRY_RUN_PACKET_MISSING = "dry_run_packet_missing"
    DRY_RUN_PACKET_AMBIGUOUS = "dry_run_packet_ambiguous"
    DRY_RUN_PACKET_UNSUPPORTED = "dry_run_packet_unsupported"
    DRY_RUN_PACKET_UNKNOWN = "dry_run_packet_unknown"


class DryRunRecommendationStatus(_ClosedValue):
    DRY_RUN_RECOMMENDATION_READY = "dry_run_recommendation_ready"
    DRY_RUN_RECOMMENDATION_BLOCKED = "dry_run_recommendation_blocked"
    DRY_RUN_RECOMMENDATION_REQUIRES_MANUAL_REVIEW = (
        "dry_run_recommendation_requires_manual_review"
    )
    DRY_RUN_RECOMMENDATION_UNKNOWN = "dry_run_recommendation_unknown"


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
class SuppliedRuntimeDryRunPacketRecord:
    condition_id: str
    token_id: str
    outcome: str
    supplied_runtime_validation_bundle: SuppliedRuntimeValidationBundleRecord
    dry_run_packet_id: str
    dry_run_summary: str
    operator_review_summary: str
    blocked_reason_summary: str
    dry_run_packet_status: DryRunPacketStatus
    dry_run_recommendation_status: DryRunRecommendationStatus
    operator_review_status: OperatorReviewStatus
    runtime_gate_status: RuntimeGateStatus
    provenance_notes: str = ""


@dataclass(frozen=True)
class SuppliedRuntimeDryRunPacketValidationResult:
    severity: ValidationSeverity
    passed: bool
    reasons: tuple[str, ...] = ()


def _enum_value(enum_type: type[_ClosedValue], value: _ClosedValue | str) -> _ClosedValue:
    if isinstance(value, enum_type):
        return value
    return enum_type(value)


def _is_nonblank_text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _supplied_runtime_validation_bundle_from_value(
    value: SuppliedRuntimeValidationBundleRecord | Mapping[str, Any],
) -> SuppliedRuntimeValidationBundleRecord:
    if isinstance(value, SuppliedRuntimeValidationBundleRecord):
        return value
    return supplied_runtime_validation_bundle_record_from_mapping(value)


def supplied_runtime_dry_run_packet_record_from_mapping(
    mapping: Mapping[str, Any],
) -> SuppliedRuntimeDryRunPacketRecord:
    """Build dry-run packet metadata from explicitly supplied values."""

    return SuppliedRuntimeDryRunPacketRecord(
        condition_id=mapping["condition_id"],
        token_id=mapping["token_id"],
        outcome=mapping["outcome"],
        supplied_runtime_validation_bundle=_supplied_runtime_validation_bundle_from_value(
            mapping["supplied_runtime_validation_bundle"]
        ),
        dry_run_packet_id=mapping["dry_run_packet_id"],
        dry_run_summary=mapping["dry_run_summary"],
        operator_review_summary=mapping["operator_review_summary"],
        blocked_reason_summary=mapping["blocked_reason_summary"],
        dry_run_packet_status=_enum_value(
            DryRunPacketStatus,
            mapping["dry_run_packet_status"],
        ),
        dry_run_recommendation_status=_enum_value(
            DryRunRecommendationStatus,
            mapping["dry_run_recommendation_status"],
        ),
        operator_review_status=_enum_value(
            OperatorReviewStatus,
            mapping["operator_review_status"],
        ),
        runtime_gate_status=_enum_value(RuntimeGateStatus, mapping["runtime_gate_status"]),
        provenance_notes=str(mapping.get("provenance_notes", "")),
    )


def validate_supplied_runtime_dry_run_packet_record(
    record: SuppliedRuntimeDryRunPacketRecord,
) -> SuppliedRuntimeDryRunPacketValidationResult:
    """Validate a supplied runtime dry-run packet with fail-closed behavior."""

    reasons: list[str] = []

    for field_name, value in (
        ("condition_id", record.condition_id),
        ("token_id", record.token_id),
        ("outcome", record.outcome),
        ("dry_run_packet_id", record.dry_run_packet_id),
        ("dry_run_summary", record.dry_run_summary),
        ("operator_review_summary", record.operator_review_summary),
    ):
        if not _is_nonblank_text(value):
            reasons.append(f"{field_name} is missing")

    bundle_result = validate_supplied_runtime_validation_bundle_record(
        record.supplied_runtime_validation_bundle
    )
    if not bundle_result.passed:
        reasons.append("supplied runtime validation bundle validation failed")

    for field_name in ("condition_id", "token_id", "outcome"):
        if getattr(record, field_name) != getattr(
            record.supplied_runtime_validation_bundle,
            field_name,
        ):
            reasons.append(
                f"{field_name} does not match supplied runtime validation bundle"
            )

    if record.dry_run_packet_status is not DryRunPacketStatus.DRY_RUN_PACKET_RECORDED:
        reasons.append(f"dry run packet status is {record.dry_run_packet_status.value}")

    if (
        record.dry_run_recommendation_status
        is not DryRunRecommendationStatus.DRY_RUN_RECOMMENDATION_READY
    ):
        reasons.append(
            f"dry run recommendation status is "
            f"{record.dry_run_recommendation_status.value}"
        )

    if record.operator_review_status is not OperatorReviewStatus.OPERATOR_REVIEW_REQUIRED:
        reasons.append(f"operator review status is {record.operator_review_status.value}")

    if record.runtime_gate_status is not RuntimeGateStatus.RUNTIME_GATE_READY:
        reasons.append(f"runtime gate status is {record.runtime_gate_status.value}")

    if reasons and not _is_nonblank_text(record.blocked_reason_summary):
        reasons.append("blocked_reason_summary is missing")

    if reasons:
        return SuppliedRuntimeDryRunPacketValidationResult(
            severity=ValidationSeverity.BLOCKED,
            passed=False,
            reasons=tuple(reasons),
        )

    return SuppliedRuntimeDryRunPacketValidationResult(
        severity=ValidationSeverity.PASSED,
        passed=True,
    )
