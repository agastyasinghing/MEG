"""Pure supplied-input runtime operator-review completion seal scaffold.

This module consumes only caller-supplied values for runtime operator-review
completion seal metadata. The completion seal is an in-memory record only. It
performs no data collection, file access, service access, source fetching,
scoring, backtesting, paper trading, trading, autonomy, persistence, export
writing, owner-decision capture, decision execution, queue service, scheduler,
broker, generated-summary behavior, or production behavior.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping

from meg.weather.stage2.supplied_runtime_operator_review_final_bundle import (
    SuppliedRuntimeOperatorReviewFinalBundleRecord,
    supplied_runtime_operator_review_final_bundle_record_from_mapping,
    validate_supplied_runtime_operator_review_final_bundle_record,
)


class _ClosedValue(str, Enum):
    """String enum base for closed, machine-checkable Stage 2 values."""

    @classmethod
    def values(cls) -> frozenset[str]:
        return frozenset(member.value for member in cls)


class OperatorReviewCompletionSealStatus(_ClosedValue):
    OPERATOR_REVIEW_COMPLETION_SEAL_RECORDED = "operator_review_completion_seal_recorded"
    OPERATOR_REVIEW_COMPLETION_SEAL_MISSING = "operator_review_completion_seal_missing"
    OPERATOR_REVIEW_COMPLETION_SEAL_AMBIGUOUS = "operator_review_completion_seal_ambiguous"
    OPERATOR_REVIEW_COMPLETION_SEAL_UNSUPPORTED = "operator_review_completion_seal_unsupported"
    OPERATOR_REVIEW_COMPLETION_SEAL_UNKNOWN = "operator_review_completion_seal_unknown"


class OperatorReviewCompletionCompletenessStatus(_ClosedValue):
    OPERATOR_REVIEW_COMPLETION_COMPLETE = "operator_review_completion_complete"
    OPERATOR_REVIEW_COMPLETION_INCOMPLETE = "operator_review_completion_incomplete"
    OPERATOR_REVIEW_COMPLETION_AMBIGUOUS = "operator_review_completion_ambiguous"
    OPERATOR_REVIEW_COMPLETION_UNKNOWN = "operator_review_completion_unknown"


class OperatorReviewCompletionSealPosture(_ClosedValue):
    OPERATOR_REVIEW_COMPLETION_SEAL_IN_MEMORY_ONLY = "operator_review_completion_seal_in_memory_only"
    OPERATOR_REVIEW_COMPLETION_SEAL_MISSING = "operator_review_completion_seal_missing"
    OPERATOR_REVIEW_COMPLETION_SEAL_AMBIGUOUS = "operator_review_completion_seal_ambiguous"
    OPERATOR_REVIEW_COMPLETION_SEAL_UNSUPPORTED = "operator_review_completion_seal_unsupported"
    OPERATOR_REVIEW_COMPLETION_SEAL_UNKNOWN = "operator_review_completion_seal_unknown"


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
class SuppliedRuntimeOperatorReviewCompletionSealRecord:
    condition_id: str
    token_id: str
    outcome: str
    supplied_runtime_operator_review_final_bundle: SuppliedRuntimeOperatorReviewFinalBundleRecord
    completion_seal_id: str
    completion_seal_summary: str
    operator_review_summary: str
    blocked_reason_summary: str
    operator_review_completion_seal_status: OperatorReviewCompletionSealStatus
    operator_review_completion_completeness_status: OperatorReviewCompletionCompletenessStatus
    operator_review_completion_seal_posture: OperatorReviewCompletionSealPosture
    operator_review_status: OperatorReviewStatus
    runtime_gate_status: RuntimeGateStatus
    provenance_notes: str = ""


@dataclass(frozen=True)
class SuppliedRuntimeOperatorReviewCompletionSealValidationResult:
    severity: ValidationSeverity
    passed: bool
    reasons: tuple[str, ...] = ()


def _enum_value(enum_type: type[_ClosedValue], value: _ClosedValue | str) -> _ClosedValue:
    if isinstance(value, enum_type):
        return value
    return enum_type(value)


def _is_nonblank_text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _supplied_runtime_operator_review_final_bundle_from_value(
    value: SuppliedRuntimeOperatorReviewFinalBundleRecord | Mapping[str, Any],
) -> SuppliedRuntimeOperatorReviewFinalBundleRecord:
    if isinstance(value, SuppliedRuntimeOperatorReviewFinalBundleRecord):
        return value
    return supplied_runtime_operator_review_final_bundle_record_from_mapping(value)


def supplied_runtime_operator_review_completion_seal_record_from_mapping(
    mapping: Mapping[str, Any],
) -> SuppliedRuntimeOperatorReviewCompletionSealRecord:
    """Build operator-review completion seal metadata from supplied values."""

    return SuppliedRuntimeOperatorReviewCompletionSealRecord(
        condition_id=mapping["condition_id"],
        token_id=mapping["token_id"],
        outcome=mapping["outcome"],
        supplied_runtime_operator_review_final_bundle=(
            _supplied_runtime_operator_review_final_bundle_from_value(
                mapping["supplied_runtime_operator_review_final_bundle"]
            )
        ),
        completion_seal_id=mapping["completion_seal_id"],
        completion_seal_summary=mapping["completion_seal_summary"],
        operator_review_summary=mapping["operator_review_summary"],
        blocked_reason_summary=mapping["blocked_reason_summary"],
        operator_review_completion_seal_status=_enum_value(
            OperatorReviewCompletionSealStatus,
            mapping["operator_review_completion_seal_status"],
        ),
        operator_review_completion_completeness_status=_enum_value(
            OperatorReviewCompletionCompletenessStatus,
            mapping["operator_review_completion_completeness_status"],
        ),
        operator_review_completion_seal_posture=_enum_value(
            OperatorReviewCompletionSealPosture,
            mapping["operator_review_completion_seal_posture"],
        ),
        operator_review_status=_enum_value(OperatorReviewStatus, mapping["operator_review_status"]),
        runtime_gate_status=_enum_value(RuntimeGateStatus, mapping["runtime_gate_status"]),
        provenance_notes=str(mapping.get("provenance_notes", "")),
    )


def validate_supplied_runtime_operator_review_completion_seal_record(
    record: SuppliedRuntimeOperatorReviewCompletionSealRecord,
) -> SuppliedRuntimeOperatorReviewCompletionSealValidationResult:
    """Validate a supplied operator-review completion seal with fail-closed behavior."""

    reasons: list[str] = []

    for field_name, value in (
        ("condition_id", record.condition_id),
        ("token_id", record.token_id),
        ("outcome", record.outcome),
        ("completion_seal_id", record.completion_seal_id),
        ("completion_seal_summary", record.completion_seal_summary),
        ("operator_review_summary", record.operator_review_summary),
    ):
        if not _is_nonblank_text(value):
            reasons.append(f"{field_name} is missing")

    final_bundle_result = validate_supplied_runtime_operator_review_final_bundle_record(
        record.supplied_runtime_operator_review_final_bundle
    )
    if not final_bundle_result.passed:
        reasons.append("supplied runtime operator-review final bundle validation failed")

    for field_name in ("condition_id", "token_id", "outcome"):
        if getattr(record, field_name) != getattr(
            record.supplied_runtime_operator_review_final_bundle,
            field_name,
        ):
            reasons.append(
                f"{field_name} does not match supplied runtime operator-review final bundle"
            )

    if (
        record.operator_review_summary
        != record.supplied_runtime_operator_review_final_bundle.operator_review_summary
    ):
        reasons.append(
            "operator_review_summary does not match supplied runtime operator-review final bundle"
        )

    if (
        record.operator_review_completion_seal_status
        is not OperatorReviewCompletionSealStatus.OPERATOR_REVIEW_COMPLETION_SEAL_RECORDED
    ):
        reasons.append(
            "operator review completion seal status is "
            f"{record.operator_review_completion_seal_status.value}"
        )

    if (
        record.operator_review_completion_completeness_status
        is not OperatorReviewCompletionCompletenessStatus.OPERATOR_REVIEW_COMPLETION_COMPLETE
    ):
        reasons.append(
            "operator review completion completeness status is "
            f"{record.operator_review_completion_completeness_status.value}"
        )

    if (
        record.operator_review_completion_seal_posture
        is not OperatorReviewCompletionSealPosture.OPERATOR_REVIEW_COMPLETION_SEAL_IN_MEMORY_ONLY
    ):
        reasons.append(
            "operator review completion seal posture is "
            f"{record.operator_review_completion_seal_posture.value}"
        )

    if record.operator_review_status is not OperatorReviewStatus.OPERATOR_REVIEW_REQUIRED:
        reasons.append(f"operator review status is {record.operator_review_status.value}")

    if record.runtime_gate_status is not RuntimeGateStatus.RUNTIME_GATE_READY:
        reasons.append(f"runtime gate status is {record.runtime_gate_status.value}")

    if reasons and not _is_nonblank_text(record.blocked_reason_summary):
        reasons.append("blocked_reason_summary is missing")

    if reasons:
        return SuppliedRuntimeOperatorReviewCompletionSealValidationResult(
            severity=ValidationSeverity.BLOCKED,
            passed=False,
            reasons=tuple(reasons),
        )

    return SuppliedRuntimeOperatorReviewCompletionSealValidationResult(
        severity=ValidationSeverity.PASSED,
        passed=True,
        reasons=(),
    )
