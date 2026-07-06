"""Pure supplied-input runtime full-chain negative smoke scaffold.

This module consumes only caller-supplied values. The negative smoke is an
in-memory record only. It records an expected fail-closed supplied-input
full-chain integration smoke result. It performs no data collection, file
access, service access, source fetching, scoring, backtesting, paper trading,
trading, autonomy, persistence, export writing, owner-decision capture,
decision execution, queue service, scheduler, broker, generated-summary
behavior, durable seal, workflow-completion side effect, or production
behavior.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping

from meg.weather.stage2.supplied_runtime_full_chain_integration_smoke import (
    SuppliedRuntimeFullChainIntegrationSmokeRecord,
    ValidationSeverity as FullChainIntegrationSmokeValidationSeverity,
    supplied_runtime_full_chain_integration_smoke_record_from_mapping,
    validate_supplied_runtime_full_chain_integration_smoke_record,
)


class _ClosedValue(str, Enum):
    """String enum base for closed, machine-checkable Stage 2 values."""

    @classmethod
    def values(cls) -> frozenset[str]:
        return frozenset(member.value for member in cls)


class FullChainNegativeSmokeStatus(_ClosedValue):
    FULL_CHAIN_NEGATIVE_SMOKE_RECORDED = "full_chain_negative_smoke_recorded"
    FULL_CHAIN_NEGATIVE_SMOKE_MISSING = "full_chain_negative_smoke_missing"
    FULL_CHAIN_NEGATIVE_SMOKE_AMBIGUOUS = "full_chain_negative_smoke_ambiguous"
    FULL_CHAIN_NEGATIVE_SMOKE_UNSUPPORTED = "full_chain_negative_smoke_unsupported"
    FULL_CHAIN_NEGATIVE_SMOKE_UNKNOWN = "full_chain_negative_smoke_unknown"


class FullChainNegativeSmokeOutcomeStatus(_ClosedValue):
    EXPECTED_FAIL_CLOSED_OBSERVED = "expected_fail_closed_observed"
    EXPECTED_FAIL_CLOSED_MISSING = "expected_fail_closed_missing"
    EXPECTED_FAIL_CLOSED_AMBIGUOUS = "expected_fail_closed_ambiguous"
    EXPECTED_FAIL_CLOSED_UNSUPPORTED = "expected_fail_closed_unsupported"
    EXPECTED_FAIL_CLOSED_UNKNOWN = "expected_fail_closed_unknown"


class FullChainNegativeSmokePosture(_ClosedValue):
    FULL_CHAIN_NEGATIVE_SMOKE_IN_MEMORY_ONLY = "full_chain_negative_smoke_in_memory_only"
    FULL_CHAIN_NEGATIVE_SMOKE_MISSING = "full_chain_negative_smoke_missing"
    FULL_CHAIN_NEGATIVE_SMOKE_AMBIGUOUS = "full_chain_negative_smoke_ambiguous"
    FULL_CHAIN_NEGATIVE_SMOKE_UNSUPPORTED = "full_chain_negative_smoke_unsupported"
    FULL_CHAIN_NEGATIVE_SMOKE_UNKNOWN = "full_chain_negative_smoke_unknown"


class OperatorReviewStatus(_ClosedValue):
    OPERATOR_REVIEW_REQUIRED = "operator_review_required"
    OPERATOR_REVIEW_MISSING = "operator_review_missing"
    OPERATOR_REVIEW_AMBIGUOUS = "operator_review_ambiguous"
    OPERATOR_REVIEW_NOT_REQUIRED = "operator_review_not_required"
    OPERATOR_REVIEW_UNKNOWN = "operator_review_unknown"


class RuntimeGateStatus(_ClosedValue):
    RUNTIME_GATE_BLOCKED = "runtime_gate_blocked"
    RUNTIME_GATE_READY = "runtime_gate_ready"
    RUNTIME_GATE_REQUIRES_MANUAL_REVIEW = "runtime_gate_requires_manual_review"
    RUNTIME_GATE_UNKNOWN = "runtime_gate_unknown"


class ValidationSeverity(_ClosedValue):
    PASSED = "passed"
    CAUTION = "caution"
    FAILED = "failed"
    BLOCKED = "blocked"


@dataclass(frozen=True)
class SuppliedRuntimeFullChainNegativeSmokeRecord:
    condition_id: str
    token_id: str
    outcome: str
    supplied_runtime_full_chain_integration_smoke: SuppliedRuntimeFullChainIntegrationSmokeRecord
    negative_smoke_id: str
    negative_smoke_summary: str
    expected_failure_reason_summary: str
    observed_failure_reason_summary: str
    blocked_reason_summary: str
    full_chain_negative_smoke_status: FullChainNegativeSmokeStatus
    full_chain_negative_smoke_outcome_status: FullChainNegativeSmokeOutcomeStatus
    full_chain_negative_smoke_posture: FullChainNegativeSmokePosture
    operator_review_status: OperatorReviewStatus
    runtime_gate_status: RuntimeGateStatus
    provenance_notes: str = ""


@dataclass(frozen=True)
class SuppliedRuntimeFullChainNegativeSmokeValidationResult:
    severity: ValidationSeverity
    passed: bool
    reasons: tuple[str, ...] = ()


def _enum_value(enum_type: type[_ClosedValue], value: _ClosedValue | str) -> _ClosedValue:
    if isinstance(value, enum_type):
        return value
    return enum_type(value)


def _is_nonblank_text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _supplied_runtime_full_chain_integration_smoke_from_value(
    value: SuppliedRuntimeFullChainIntegrationSmokeRecord | Mapping[str, Any],
) -> SuppliedRuntimeFullChainIntegrationSmokeRecord:
    if isinstance(value, SuppliedRuntimeFullChainIntegrationSmokeRecord):
        return value
    return supplied_runtime_full_chain_integration_smoke_record_from_mapping(value)


def supplied_runtime_full_chain_negative_smoke_record_from_mapping(
    mapping: Mapping[str, Any],
) -> SuppliedRuntimeFullChainNegativeSmokeRecord:
    """Build full-chain negative smoke metadata from supplied values."""

    return SuppliedRuntimeFullChainNegativeSmokeRecord(
        condition_id=mapping["condition_id"],
        token_id=mapping["token_id"],
        outcome=mapping["outcome"],
        supplied_runtime_full_chain_integration_smoke=(
            _supplied_runtime_full_chain_integration_smoke_from_value(
                mapping["supplied_runtime_full_chain_integration_smoke"]
            )
        ),
        negative_smoke_id=mapping["negative_smoke_id"],
        negative_smoke_summary=mapping["negative_smoke_summary"],
        expected_failure_reason_summary=mapping["expected_failure_reason_summary"],
        observed_failure_reason_summary=mapping["observed_failure_reason_summary"],
        blocked_reason_summary=mapping["blocked_reason_summary"],
        full_chain_negative_smoke_status=_enum_value(
            FullChainNegativeSmokeStatus,
            mapping["full_chain_negative_smoke_status"],
        ),
        full_chain_negative_smoke_outcome_status=_enum_value(
            FullChainNegativeSmokeOutcomeStatus,
            mapping["full_chain_negative_smoke_outcome_status"],
        ),
        full_chain_negative_smoke_posture=_enum_value(
            FullChainNegativeSmokePosture,
            mapping["full_chain_negative_smoke_posture"],
        ),
        operator_review_status=_enum_value(OperatorReviewStatus, mapping["operator_review_status"]),
        runtime_gate_status=_enum_value(RuntimeGateStatus, mapping["runtime_gate_status"]),
        provenance_notes=str(mapping.get("provenance_notes", "")),
    )


def validate_supplied_runtime_full_chain_negative_smoke_record(
    record: SuppliedRuntimeFullChainNegativeSmokeRecord,
) -> SuppliedRuntimeFullChainNegativeSmokeValidationResult:
    """Validate a supplied full-chain negative smoke with fail-closed behavior."""

    reasons: list[str] = []

    for field_name, value in (
        ("condition_id", record.condition_id),
        ("token_id", record.token_id),
        ("outcome", record.outcome),
        ("negative_smoke_id", record.negative_smoke_id),
        ("negative_smoke_summary", record.negative_smoke_summary),
        ("expected_failure_reason_summary", record.expected_failure_reason_summary),
        ("observed_failure_reason_summary", record.observed_failure_reason_summary),
        ("blocked_reason_summary", record.blocked_reason_summary),
    ):
        if not _is_nonblank_text(value):
            reasons.append(f"{field_name} is missing")

    integration_result = validate_supplied_runtime_full_chain_integration_smoke_record(
        record.supplied_runtime_full_chain_integration_smoke
    )
    if integration_result.passed:
        reasons.append("supplied runtime full-chain integration smoke unexpectedly passed")
    if integration_result.severity is not FullChainIntegrationSmokeValidationSeverity.BLOCKED:
        reasons.append("supplied runtime full-chain integration smoke did not report blocked severity")
    if not integration_result.reasons:
        reasons.append("supplied runtime full-chain integration smoke did not report reasons")

    for field_name in ("condition_id", "token_id", "outcome"):
        if getattr(record, field_name) != getattr(
            record.supplied_runtime_full_chain_integration_smoke,
            field_name,
        ):
            reasons.append(f"{field_name} does not match supplied runtime full-chain integration smoke")

    if not any(
        nested_reason in record.observed_failure_reason_summary
        for nested_reason in integration_result.reasons
    ):
        reasons.append("observed_failure_reason_summary does not include a nested integration smoke reason")

    if (
        record.full_chain_negative_smoke_status
        is not FullChainNegativeSmokeStatus.FULL_CHAIN_NEGATIVE_SMOKE_RECORDED
    ):
        reasons.append(
            f"full chain negative smoke status is {record.full_chain_negative_smoke_status.value}"
        )

    if (
        record.full_chain_negative_smoke_outcome_status
        is not FullChainNegativeSmokeOutcomeStatus.EXPECTED_FAIL_CLOSED_OBSERVED
    ):
        reasons.append(
            "full chain negative smoke outcome status is "
            f"{record.full_chain_negative_smoke_outcome_status.value}"
        )

    if (
        record.full_chain_negative_smoke_posture
        is not FullChainNegativeSmokePosture.FULL_CHAIN_NEGATIVE_SMOKE_IN_MEMORY_ONLY
    ):
        reasons.append(
            f"full chain negative smoke posture is {record.full_chain_negative_smoke_posture.value}"
        )

    if record.operator_review_status is not OperatorReviewStatus.OPERATOR_REVIEW_REQUIRED:
        reasons.append(f"operator review status is {record.operator_review_status.value}")

    if record.runtime_gate_status is not RuntimeGateStatus.RUNTIME_GATE_BLOCKED:
        reasons.append(f"runtime gate status is {record.runtime_gate_status.value}")

    if reasons:
        return SuppliedRuntimeFullChainNegativeSmokeValidationResult(
            severity=ValidationSeverity.BLOCKED,
            passed=False,
            reasons=tuple(reasons),
        )

    return SuppliedRuntimeFullChainNegativeSmokeValidationResult(
        severity=ValidationSeverity.PASSED,
        passed=True,
        reasons=(),
    )
