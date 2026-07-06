"""Pure supplied-input runtime full-chain integration smoke scaffold.

This module consumes only caller-supplied values. The integration smoke is an
in-memory record only. It validates the supplied-input chain from market
contract through operator-review completion summary. It performs no data
collection, file access, service access, source fetching, scoring, backtesting,
paper trading, trading, autonomy, persistence, export writing, owner-decision
capture, decision execution, queue service, scheduler, broker,
generated-summary behavior, durable seal, workflow-completion side effect, or
production behavior.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping

from meg.weather.stage2.supplied_runtime_operator_review_completion_summary import (
    SuppliedRuntimeOperatorReviewCompletionSummaryRecord,
    supplied_runtime_operator_review_completion_summary_record_from_mapping,
    validate_supplied_runtime_operator_review_completion_summary_record,
)


class _ClosedValue(str, Enum):
    """String enum base for closed, machine-checkable Stage 2 values."""

    @classmethod
    def values(cls) -> frozenset[str]:
        return frozenset(member.value for member in cls)


class FullChainIntegrationSmokeStatus(_ClosedValue):
    FULL_CHAIN_INTEGRATION_SMOKE_RECORDED = "full_chain_integration_smoke_recorded"
    FULL_CHAIN_INTEGRATION_SMOKE_MISSING = "full_chain_integration_smoke_missing"
    FULL_CHAIN_INTEGRATION_SMOKE_AMBIGUOUS = "full_chain_integration_smoke_ambiguous"
    FULL_CHAIN_INTEGRATION_SMOKE_UNSUPPORTED = "full_chain_integration_smoke_unsupported"
    FULL_CHAIN_INTEGRATION_SMOKE_UNKNOWN = "full_chain_integration_smoke_unknown"


class FullChainIntegrationCompletenessStatus(_ClosedValue):
    FULL_CHAIN_INTEGRATION_COMPLETE = "full_chain_integration_complete"
    FULL_CHAIN_INTEGRATION_INCOMPLETE = "full_chain_integration_incomplete"
    FULL_CHAIN_INTEGRATION_AMBIGUOUS = "full_chain_integration_ambiguous"
    FULL_CHAIN_INTEGRATION_UNKNOWN = "full_chain_integration_unknown"


class FullChainIntegrationPosture(_ClosedValue):
    FULL_CHAIN_INTEGRATION_IN_MEMORY_ONLY = "full_chain_integration_in_memory_only"
    FULL_CHAIN_INTEGRATION_MISSING = "full_chain_integration_missing"
    FULL_CHAIN_INTEGRATION_AMBIGUOUS = "full_chain_integration_ambiguous"
    FULL_CHAIN_INTEGRATION_UNSUPPORTED = "full_chain_integration_unsupported"
    FULL_CHAIN_INTEGRATION_UNKNOWN = "full_chain_integration_unknown"


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
class SuppliedRuntimeFullChainIntegrationSmokeRecord:
    condition_id: str
    token_id: str
    outcome: str
    supplied_runtime_operator_review_completion_summary: (
        SuppliedRuntimeOperatorReviewCompletionSummaryRecord
    )
    integration_smoke_id: str
    integration_smoke_summary: str
    operator_review_summary: str
    blocked_reason_summary: str
    full_chain_integration_smoke_status: FullChainIntegrationSmokeStatus
    full_chain_integration_completeness_status: FullChainIntegrationCompletenessStatus
    full_chain_integration_posture: FullChainIntegrationPosture
    operator_review_status: OperatorReviewStatus
    runtime_gate_status: RuntimeGateStatus
    provenance_notes: str = ""


@dataclass(frozen=True)
class SuppliedRuntimeFullChainIntegrationSmokeValidationResult:
    severity: ValidationSeverity
    passed: bool
    reasons: tuple[str, ...] = ()


def _enum_value(enum_type: type[_ClosedValue], value: _ClosedValue | str) -> _ClosedValue:
    if isinstance(value, enum_type):
        return value
    return enum_type(value)


def _is_nonblank_text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _supplied_runtime_operator_review_completion_summary_from_value(
    value: SuppliedRuntimeOperatorReviewCompletionSummaryRecord | Mapping[str, Any],
) -> SuppliedRuntimeOperatorReviewCompletionSummaryRecord:
    if isinstance(value, SuppliedRuntimeOperatorReviewCompletionSummaryRecord):
        return value
    return supplied_runtime_operator_review_completion_summary_record_from_mapping(value)


def supplied_runtime_full_chain_integration_smoke_record_from_mapping(
    mapping: Mapping[str, Any],
) -> SuppliedRuntimeFullChainIntegrationSmokeRecord:
    """Build full-chain integration smoke metadata from supplied values."""

    return SuppliedRuntimeFullChainIntegrationSmokeRecord(
        condition_id=mapping["condition_id"],
        token_id=mapping["token_id"],
        outcome=mapping["outcome"],
        supplied_runtime_operator_review_completion_summary=(
            _supplied_runtime_operator_review_completion_summary_from_value(
                mapping["supplied_runtime_operator_review_completion_summary"]
            )
        ),
        integration_smoke_id=mapping["integration_smoke_id"],
        integration_smoke_summary=mapping["integration_smoke_summary"],
        operator_review_summary=mapping["operator_review_summary"],
        blocked_reason_summary=mapping["blocked_reason_summary"],
        full_chain_integration_smoke_status=_enum_value(
            FullChainIntegrationSmokeStatus,
            mapping["full_chain_integration_smoke_status"],
        ),
        full_chain_integration_completeness_status=_enum_value(
            FullChainIntegrationCompletenessStatus,
            mapping["full_chain_integration_completeness_status"],
        ),
        full_chain_integration_posture=_enum_value(
            FullChainIntegrationPosture,
            mapping["full_chain_integration_posture"],
        ),
        operator_review_status=_enum_value(OperatorReviewStatus, mapping["operator_review_status"]),
        runtime_gate_status=_enum_value(RuntimeGateStatus, mapping["runtime_gate_status"]),
        provenance_notes=str(mapping.get("provenance_notes", "")),
    )


def validate_supplied_runtime_full_chain_integration_smoke_record(
    record: SuppliedRuntimeFullChainIntegrationSmokeRecord,
) -> SuppliedRuntimeFullChainIntegrationSmokeValidationResult:
    """Validate a supplied full-chain integration smoke with fail-closed behavior."""

    reasons: list[str] = []

    for field_name, value in (
        ("condition_id", record.condition_id),
        ("token_id", record.token_id),
        ("outcome", record.outcome),
        ("integration_smoke_id", record.integration_smoke_id),
        ("integration_smoke_summary", record.integration_smoke_summary),
        ("operator_review_summary", record.operator_review_summary),
    ):
        if not _is_nonblank_text(value):
            reasons.append(f"{field_name} is missing")

    completion_summary_result = validate_supplied_runtime_operator_review_completion_summary_record(
        record.supplied_runtime_operator_review_completion_summary
    )
    if not completion_summary_result.passed:
        reasons.append("supplied runtime operator-review completion summary validation failed")

    for field_name in ("condition_id", "token_id", "outcome"):
        if getattr(record, field_name) != getattr(
            record.supplied_runtime_operator_review_completion_summary,
            field_name,
        ):
            reasons.append(
                f"{field_name} does not match supplied runtime operator-review completion summary"
            )

    if (
        record.operator_review_summary
        != record.supplied_runtime_operator_review_completion_summary.operator_review_summary
    ):
        reasons.append(
            "operator_review_summary does not match supplied runtime operator-review completion summary"
        )

    if (
        record.full_chain_integration_smoke_status
        is not FullChainIntegrationSmokeStatus.FULL_CHAIN_INTEGRATION_SMOKE_RECORDED
    ):
        reasons.append(
            "full chain integration smoke status is "
            f"{record.full_chain_integration_smoke_status.value}"
        )

    if (
        record.full_chain_integration_completeness_status
        is not FullChainIntegrationCompletenessStatus.FULL_CHAIN_INTEGRATION_COMPLETE
    ):
        reasons.append(
            "full chain integration completeness status is "
            f"{record.full_chain_integration_completeness_status.value}"
        )

    if (
        record.full_chain_integration_posture
        is not FullChainIntegrationPosture.FULL_CHAIN_INTEGRATION_IN_MEMORY_ONLY
    ):
        reasons.append(
            f"full chain integration posture is {record.full_chain_integration_posture.value}"
        )

    if record.operator_review_status is not OperatorReviewStatus.OPERATOR_REVIEW_REQUIRED:
        reasons.append(f"operator review status is {record.operator_review_status.value}")

    if record.runtime_gate_status is not RuntimeGateStatus.RUNTIME_GATE_READY:
        reasons.append(f"runtime gate status is {record.runtime_gate_status.value}")

    if reasons and not _is_nonblank_text(record.blocked_reason_summary):
        reasons.append("blocked_reason_summary is missing")

    if reasons:
        return SuppliedRuntimeFullChainIntegrationSmokeValidationResult(
            severity=ValidationSeverity.BLOCKED,
            passed=False,
            reasons=tuple(reasons),
        )

    return SuppliedRuntimeFullChainIntegrationSmokeValidationResult(
        severity=ValidationSeverity.PASSED,
        passed=True,
        reasons=(),
    )
