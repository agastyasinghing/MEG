"""Pure Stage 2 retrieval-context runtime metadata scaffold.

This module contains closed value sets, metadata containers, and fail-closed
validation helpers for explicitly supplied retrieval-context metadata. It only
consumes caller-supplied source-identity metadata and performs no data
collection, file access, service access, scoring, backtesting, trading,
or autonomy.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping

from meg.weather.stage2.source_identity_runtime import (
    SourceIdentityRecord,
    source_identity_record_from_mapping,
    validate_source_identity_record,
)


class _ClosedValue(str, Enum):
    """String enum base for closed, machine-checkable Stage 2 values."""

    @classmethod
    def values(cls) -> frozenset[str]:
        return frozenset(member.value for member in cls)


class RetrievalMode(_ClosedValue):
    MANUAL_DESCRIPTOR_ONLY = "manual_descriptor_only"
    STATIC_REFERENCE = "static_reference"
    LATER_SOURCE_FETCHING_REQUEST = "later_source_fetching_request"
    LATER_PROVIDER_CONNECTOR_REQUEST = "later_provider_connector_request"
    PROHIBITED_UNTIL_EXPLICIT_APPROVAL = "prohibited_until_explicit_approval"
    UNKNOWN_REQUIRES_REVIEW = "unknown_requires_review"


class RetrievalContextStatus(_ClosedValue):
    RETRIEVAL_CONTEXT_RECORDED = "retrieval_context_recorded"
    RETRIEVAL_CONTEXT_MISSING = "retrieval_context_missing"
    RETRIEVAL_CONTEXT_AMBIGUOUS = "retrieval_context_ambiguous"
    RETRIEVAL_CONTEXT_UNSUPPORTED = "retrieval_context_unsupported"
    RETRIEVAL_CONTEXT_UNKNOWN = "retrieval_context_unknown"


class RetrievalTimingStatus(_ClosedValue):
    RETRIEVAL_TIMING_RECORDED = "retrieval_timing_recorded"
    RETRIEVAL_TIMING_MISSING = "retrieval_timing_missing"
    RETRIEVAL_TIMING_AMBIGUOUS = "retrieval_timing_ambiguous"
    RETRIEVAL_TIMING_AFTER_DECISION = "retrieval_timing_after_decision"
    RETRIEVAL_TIMING_UNKNOWN = "retrieval_timing_unknown"


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
class RetrievalContextRecord:
    condition_id: str
    token_id: str
    outcome: str
    source_identity: SourceIdentityRecord
    retrieval_mode: RetrievalMode
    retrieval_context_status: RetrievalContextStatus
    retrieval_timing_status: RetrievalTimingStatus
    accessed_at_utc: str
    retrieved_at_utc: str
    available_at_utc: str
    decision_time_utc: str
    runtime_gate_status: RuntimeGateStatus
    provenance_notes: str = ""


@dataclass(frozen=True)
class RetrievalContextValidationResult:
    severity: ValidationSeverity
    passed: bool
    reasons: tuple[str, ...] = ()


_ALLOWED_RETRIEVAL_MODES = frozenset(
    {RetrievalMode.MANUAL_DESCRIPTOR_ONLY, RetrievalMode.STATIC_REFERENCE}
)


def _enum_value(enum_type: type[_ClosedValue], value: _ClosedValue | str) -> _ClosedValue:
    if isinstance(value, enum_type):
        return value
    return enum_type(value)


def _is_nonblank_text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _source_identity_from_value(
    value: SourceIdentityRecord | Mapping[str, Any],
) -> SourceIdentityRecord:
    if isinstance(value, SourceIdentityRecord):
        return value
    return source_identity_record_from_mapping(value)


def retrieval_context_record_from_mapping(mapping: Mapping[str, Any]) -> RetrievalContextRecord:
    """Build retrieval-context metadata from explicitly supplied values."""

    return RetrievalContextRecord(
        condition_id=mapping["condition_id"],
        token_id=mapping["token_id"],
        outcome=mapping["outcome"],
        source_identity=_source_identity_from_value(mapping["source_identity"]),
        retrieval_mode=_enum_value(RetrievalMode, mapping["retrieval_mode"]),
        retrieval_context_status=_enum_value(
            RetrievalContextStatus, mapping["retrieval_context_status"]
        ),
        retrieval_timing_status=_enum_value(
            RetrievalTimingStatus, mapping["retrieval_timing_status"]
        ),
        accessed_at_utc=mapping["accessed_at_utc"],
        retrieved_at_utc=mapping["retrieved_at_utc"],
        available_at_utc=mapping["available_at_utc"],
        decision_time_utc=mapping["decision_time_utc"],
        runtime_gate_status=_enum_value(RuntimeGateStatus, mapping["runtime_gate_status"]),
        provenance_notes=str(mapping.get("provenance_notes", "")),
    )


def validate_retrieval_context_record(
    record: RetrievalContextRecord,
) -> RetrievalContextValidationResult:
    """Validate supplied retrieval-context metadata with fail-closed behavior."""

    reasons: list[str] = []

    for field_name, value in (
        ("condition_id", record.condition_id),
        ("token_id", record.token_id),
        ("outcome", record.outcome),
    ):
        if not _is_nonblank_text(value):
            reasons.append(f"{field_name} is missing")

    source_identity_result = validate_source_identity_record(record.source_identity)
    if not source_identity_result.passed:
        reasons.append("source identity validation failed")

    if record.condition_id != record.source_identity.condition_id:
        reasons.append("condition_id does not match source identity")
    if record.token_id != record.source_identity.token_id:
        reasons.append("token_id does not match source identity")
    if record.outcome != record.source_identity.outcome:
        reasons.append("outcome does not match source identity")

    if record.retrieval_mode not in _ALLOWED_RETRIEVAL_MODES:
        reasons.append(f"retrieval mode is {record.retrieval_mode.value}")

    if (
        record.retrieval_context_status
        is not RetrievalContextStatus.RETRIEVAL_CONTEXT_RECORDED
    ):
        reasons.append(f"retrieval context status is {record.retrieval_context_status.value}")

    if (
        record.retrieval_timing_status
        is not RetrievalTimingStatus.RETRIEVAL_TIMING_RECORDED
    ):
        reasons.append(f"retrieval timing status is {record.retrieval_timing_status.value}")

    for field_name, value in (
        ("accessed_at_utc", record.accessed_at_utc),
        ("retrieved_at_utc", record.retrieved_at_utc),
        ("available_at_utc", record.available_at_utc),
        ("decision_time_utc", record.decision_time_utc),
    ):
        if not _is_nonblank_text(value):
            reasons.append(f"{field_name} is missing")

    if record.runtime_gate_status is not RuntimeGateStatus.RUNTIME_GATE_READY:
        reasons.append(f"runtime gate status is {record.runtime_gate_status.value}")

    if reasons:
        return RetrievalContextValidationResult(
            severity=ValidationSeverity.BLOCKED,
            passed=False,
            reasons=tuple(reasons),
        )

    return RetrievalContextValidationResult(severity=ValidationSeverity.PASSED, passed=True)
