"""Pure supplied-input runtime operator-review final bundle scaffold.

This module consumes only caller-supplied values for runtime operator-review
final bundle metadata. The final bundle is an in-memory record only. It
performs no data collection, file access, service access, source fetching,
scoring, backtesting, paper trading, trading, autonomy, persistence, export
writing, owner-decision capture, decision execution, queue service, scheduler,
broker, generated-summary behavior, or production behavior.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping

from meg.weather.stage2.supplied_runtime_operator_review_final_packet import (
    SuppliedRuntimeOperatorReviewFinalPacketRecord,
    supplied_runtime_operator_review_final_packet_record_from_mapping,
    validate_supplied_runtime_operator_review_final_packet_record,
)


class _ClosedValue(str, Enum):
    """String enum base for closed, machine-checkable Stage 2 values."""

    @classmethod
    def values(cls) -> frozenset[str]:
        return frozenset(member.value for member in cls)


class OperatorReviewFinalBundleStatus(_ClosedValue):
    OPERATOR_REVIEW_FINAL_BUNDLE_RECORDED = "operator_review_final_bundle_recorded"
    OPERATOR_REVIEW_FINAL_BUNDLE_MISSING = "operator_review_final_bundle_missing"
    OPERATOR_REVIEW_FINAL_BUNDLE_AMBIGUOUS = "operator_review_final_bundle_ambiguous"
    OPERATOR_REVIEW_FINAL_BUNDLE_UNSUPPORTED = "operator_review_final_bundle_unsupported"
    OPERATOR_REVIEW_FINAL_BUNDLE_UNKNOWN = "operator_review_final_bundle_unknown"


class OperatorReviewFinalBundleCompletenessStatus(_ClosedValue):
    OPERATOR_REVIEW_FINAL_BUNDLE_COMPLETE = "operator_review_final_bundle_complete"
    OPERATOR_REVIEW_FINAL_BUNDLE_INCOMPLETE = "operator_review_final_bundle_incomplete"
    OPERATOR_REVIEW_FINAL_BUNDLE_AMBIGUOUS = "operator_review_final_bundle_ambiguous"
    OPERATOR_REVIEW_FINAL_BUNDLE_UNKNOWN = "operator_review_final_bundle_unknown"


class OperatorReviewFinalBundlePosture(_ClosedValue):
    OPERATOR_REVIEW_FINAL_BUNDLE_IN_MEMORY_ONLY = "operator_review_final_bundle_in_memory_only"
    OPERATOR_REVIEW_FINAL_BUNDLE_MISSING = "operator_review_final_bundle_missing"
    OPERATOR_REVIEW_FINAL_BUNDLE_AMBIGUOUS = "operator_review_final_bundle_ambiguous"
    OPERATOR_REVIEW_FINAL_BUNDLE_UNSUPPORTED = "operator_review_final_bundle_unsupported"
    OPERATOR_REVIEW_FINAL_BUNDLE_UNKNOWN = "operator_review_final_bundle_unknown"


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
class SuppliedRuntimeOperatorReviewFinalBundleRecord:
    condition_id: str
    token_id: str
    outcome: str
    supplied_runtime_operator_review_final_packet: SuppliedRuntimeOperatorReviewFinalPacketRecord
    final_bundle_id: str
    final_bundle_summary: str
    operator_review_summary: str
    blocked_reason_summary: str
    operator_review_final_bundle_status: OperatorReviewFinalBundleStatus
    operator_review_final_bundle_completeness_status: OperatorReviewFinalBundleCompletenessStatus
    operator_review_final_bundle_posture: OperatorReviewFinalBundlePosture
    operator_review_status: OperatorReviewStatus
    runtime_gate_status: RuntimeGateStatus
    provenance_notes: str = ""


@dataclass(frozen=True)
class SuppliedRuntimeOperatorReviewFinalBundleValidationResult:
    severity: ValidationSeverity
    passed: bool
    reasons: tuple[str, ...] = ()


def _enum_value(enum_type: type[_ClosedValue], value: _ClosedValue | str) -> _ClosedValue:
    if isinstance(value, enum_type):
        return value
    return enum_type(value)


def _is_nonblank_text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _supplied_runtime_operator_review_final_packet_from_value(
    value: SuppliedRuntimeOperatorReviewFinalPacketRecord | Mapping[str, Any],
) -> SuppliedRuntimeOperatorReviewFinalPacketRecord:
    if isinstance(value, SuppliedRuntimeOperatorReviewFinalPacketRecord):
        return value
    return supplied_runtime_operator_review_final_packet_record_from_mapping(value)


def supplied_runtime_operator_review_final_bundle_record_from_mapping(
    mapping: Mapping[str, Any],
) -> SuppliedRuntimeOperatorReviewFinalBundleRecord:
    """Build operator-review final bundle metadata from supplied values."""

    return SuppliedRuntimeOperatorReviewFinalBundleRecord(
        condition_id=mapping["condition_id"],
        token_id=mapping["token_id"],
        outcome=mapping["outcome"],
        supplied_runtime_operator_review_final_packet=(
            _supplied_runtime_operator_review_final_packet_from_value(
                mapping["supplied_runtime_operator_review_final_packet"]
            )
        ),
        final_bundle_id=mapping["final_bundle_id"],
        final_bundle_summary=mapping["final_bundle_summary"],
        operator_review_summary=mapping["operator_review_summary"],
        blocked_reason_summary=mapping["blocked_reason_summary"],
        operator_review_final_bundle_status=_enum_value(
            OperatorReviewFinalBundleStatus,
            mapping["operator_review_final_bundle_status"],
        ),
        operator_review_final_bundle_completeness_status=_enum_value(
            OperatorReviewFinalBundleCompletenessStatus,
            mapping["operator_review_final_bundle_completeness_status"],
        ),
        operator_review_final_bundle_posture=_enum_value(
            OperatorReviewFinalBundlePosture,
            mapping["operator_review_final_bundle_posture"],
        ),
        operator_review_status=_enum_value(OperatorReviewStatus, mapping["operator_review_status"]),
        runtime_gate_status=_enum_value(RuntimeGateStatus, mapping["runtime_gate_status"]),
        provenance_notes=str(mapping.get("provenance_notes", "")),
    )


def validate_supplied_runtime_operator_review_final_bundle_record(
    record: SuppliedRuntimeOperatorReviewFinalBundleRecord,
) -> SuppliedRuntimeOperatorReviewFinalBundleValidationResult:
    """Validate a supplied operator-review final bundle with fail-closed behavior."""

    reasons: list[str] = []

    for field_name, value in (
        ("condition_id", record.condition_id),
        ("token_id", record.token_id),
        ("outcome", record.outcome),
        ("final_bundle_id", record.final_bundle_id),
        ("final_bundle_summary", record.final_bundle_summary),
        ("operator_review_summary", record.operator_review_summary),
    ):
        if not _is_nonblank_text(value):
            reasons.append(f"{field_name} is missing")

    final_packet_result = validate_supplied_runtime_operator_review_final_packet_record(
        record.supplied_runtime_operator_review_final_packet
    )
    if not final_packet_result.passed:
        reasons.append("supplied runtime operator-review final packet validation failed")

    for field_name in ("condition_id", "token_id", "outcome"):
        if getattr(record, field_name) != getattr(
            record.supplied_runtime_operator_review_final_packet,
            field_name,
        ):
            reasons.append(
                f"{field_name} does not match supplied runtime operator-review final packet"
            )

    if (
        record.operator_review_summary
        != record.supplied_runtime_operator_review_final_packet.operator_review_summary
    ):
        reasons.append(
            "operator_review_summary does not match supplied runtime operator-review final packet"
        )

    if (
        record.operator_review_final_bundle_status
        is not OperatorReviewFinalBundleStatus.OPERATOR_REVIEW_FINAL_BUNDLE_RECORDED
    ):
        reasons.append(
            "operator review final bundle status is "
            f"{record.operator_review_final_bundle_status.value}"
        )

    if (
        record.operator_review_final_bundle_completeness_status
        is not OperatorReviewFinalBundleCompletenessStatus.OPERATOR_REVIEW_FINAL_BUNDLE_COMPLETE
    ):
        reasons.append(
            "operator review final bundle completeness status is "
            f"{record.operator_review_final_bundle_completeness_status.value}"
        )

    if (
        record.operator_review_final_bundle_posture
        is not OperatorReviewFinalBundlePosture.OPERATOR_REVIEW_FINAL_BUNDLE_IN_MEMORY_ONLY
    ):
        reasons.append(
            "operator review final bundle posture is "
            f"{record.operator_review_final_bundle_posture.value}"
        )

    if record.operator_review_status is not OperatorReviewStatus.OPERATOR_REVIEW_REQUIRED:
        reasons.append(f"operator review status is {record.operator_review_status.value}")

    if record.runtime_gate_status is not RuntimeGateStatus.RUNTIME_GATE_READY:
        reasons.append(f"runtime gate status is {record.runtime_gate_status.value}")

    if reasons and not _is_nonblank_text(record.blocked_reason_summary):
        reasons.append("blocked_reason_summary is missing")

    if reasons:
        return SuppliedRuntimeOperatorReviewFinalBundleValidationResult(
            severity=ValidationSeverity.BLOCKED,
            passed=False,
            reasons=tuple(reasons),
        )

    return SuppliedRuntimeOperatorReviewFinalBundleValidationResult(
        severity=ValidationSeverity.PASSED,
        passed=True,
        reasons=(),
    )
