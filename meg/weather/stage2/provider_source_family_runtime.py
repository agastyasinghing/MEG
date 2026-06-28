"""Pure Stage 2 provider/source-family runtime metadata scaffold.

This module contains closed value sets, metadata containers, and fail-closed
validation helpers for explicitly supplied provider/source-family metadata. It
only consumes caller-supplied source-identity and retrieval-context metadata and
performs no data collection, file access, service access, source fetching,
scoring, backtesting, trading, or autonomy.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping

from meg.weather.stage2.retrieval_context_runtime import (
    RetrievalContextRecord,
    retrieval_context_record_from_mapping,
    validate_retrieval_context_record,
)
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


class ProviderSourceFamilyStatus(_ClosedValue):
    PROVIDER_SOURCE_FAMILY_RECORDED = "provider_source_family_recorded"
    PROVIDER_SOURCE_FAMILY_MISSING = "provider_source_family_missing"
    PROVIDER_SOURCE_FAMILY_AMBIGUOUS = "provider_source_family_ambiguous"
    PROVIDER_SOURCE_FAMILY_UNSUPPORTED = "provider_source_family_unsupported"
    PROVIDER_SOURCE_FAMILY_UNKNOWN = "provider_source_family_unknown"


class ProviderExecutionPosture(_ClosedValue):
    NO_PROVIDER_EXECUTION = "no_provider_execution"
    PROVIDER_EXECUTION_NOT_APPROVED = "provider_execution_not_approved"
    PROVIDER_CONNECTOR_NOT_CREATED = "provider_connector_not_created"
    PROVIDER_CLIENT_NOT_CREATED = "provider_client_not_created"
    LIVE_PROVIDER_FETCHING_NOT_APPROVED = "live_provider_fetching_not_approved"
    UNKNOWN_REQUIRES_REVIEW = "unknown_requires_review"


class SourceFamilyCompatibilityStatus(_ClosedValue):
    SOURCE_FAMILY_COMPATIBLE = "source_family_compatible"
    SOURCE_FAMILY_INCOMPATIBLE = "source_family_incompatible"
    SOURCE_FAMILY_REQUIRES_MANUAL_REVIEW = "source_family_requires_manual_review"
    SOURCE_FAMILY_UNKNOWN = "source_family_unknown"


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
class ProviderSourceFamilyRecord:
    condition_id: str
    token_id: str
    outcome: str
    source_identity: SourceIdentityRecord
    retrieval_context: RetrievalContextRecord
    source_family: str
    provider_source_family_status: ProviderSourceFamilyStatus
    provider_execution_posture: ProviderExecutionPosture
    source_family_compatibility_status: SourceFamilyCompatibilityStatus
    runtime_gate_status: RuntimeGateStatus
    provenance_notes: str = ""


@dataclass(frozen=True)
class ProviderSourceFamilyValidationResult:
    severity: ValidationSeverity
    passed: bool
    reasons: tuple[str, ...] = ()


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


def _retrieval_context_from_value(
    value: RetrievalContextRecord | Mapping[str, Any],
) -> RetrievalContextRecord:
    if isinstance(value, RetrievalContextRecord):
        return value
    return retrieval_context_record_from_mapping(value)


def provider_source_family_record_from_mapping(
    mapping: Mapping[str, Any],
) -> ProviderSourceFamilyRecord:
    """Build provider/source-family metadata from explicitly supplied values."""

    return ProviderSourceFamilyRecord(
        condition_id=mapping["condition_id"],
        token_id=mapping["token_id"],
        outcome=mapping["outcome"],
        source_identity=_source_identity_from_value(mapping["source_identity"]),
        retrieval_context=_retrieval_context_from_value(mapping["retrieval_context"]),
        source_family=mapping["source_family"],
        provider_source_family_status=_enum_value(
            ProviderSourceFamilyStatus, mapping["provider_source_family_status"]
        ),
        provider_execution_posture=_enum_value(
            ProviderExecutionPosture, mapping["provider_execution_posture"]
        ),
        source_family_compatibility_status=_enum_value(
            SourceFamilyCompatibilityStatus, mapping["source_family_compatibility_status"]
        ),
        runtime_gate_status=_enum_value(RuntimeGateStatus, mapping["runtime_gate_status"]),
        provenance_notes=str(mapping.get("provenance_notes", "")),
    )


def validate_provider_source_family_record(
    record: ProviderSourceFamilyRecord,
) -> ProviderSourceFamilyValidationResult:
    """Validate supplied provider/source-family metadata with fail-closed behavior."""

    reasons: list[str] = []

    for field_name, value in (
        ("condition_id", record.condition_id),
        ("token_id", record.token_id),
        ("outcome", record.outcome),
        ("source_family", record.source_family),
    ):
        if not _is_nonblank_text(value):
            reasons.append(f"{field_name} is missing")

    source_identity_result = validate_source_identity_record(record.source_identity)
    if not source_identity_result.passed:
        reasons.append("source identity validation failed")

    retrieval_context_result = validate_retrieval_context_record(record.retrieval_context)
    if not retrieval_context_result.passed:
        reasons.append("retrieval context validation failed")

    if record.condition_id != record.source_identity.condition_id:
        reasons.append("condition_id does not match source identity")
    if record.token_id != record.source_identity.token_id:
        reasons.append("token_id does not match source identity")
    if record.outcome != record.source_identity.outcome:
        reasons.append("outcome does not match source identity")

    if record.condition_id != record.retrieval_context.condition_id:
        reasons.append("condition_id does not match retrieval context")
    if record.token_id != record.retrieval_context.token_id:
        reasons.append("token_id does not match retrieval context")
    if record.outcome != record.retrieval_context.outcome:
        reasons.append("outcome does not match retrieval context")

    if record.source_family != record.source_identity.source_family.value:
        reasons.append("source_family does not match source identity")

    if (
        record.provider_source_family_status
        is not ProviderSourceFamilyStatus.PROVIDER_SOURCE_FAMILY_RECORDED
    ):
        reasons.append(
            f"provider source family status is {record.provider_source_family_status.value}"
        )

    if record.provider_execution_posture is not ProviderExecutionPosture.NO_PROVIDER_EXECUTION:
        reasons.append(f"provider execution posture is {record.provider_execution_posture.value}")

    if (
        record.source_family_compatibility_status
        is not SourceFamilyCompatibilityStatus.SOURCE_FAMILY_COMPATIBLE
    ):
        reasons.append(
            "source family compatibility status is "
            f"{record.source_family_compatibility_status.value}"
        )

    if record.runtime_gate_status is not RuntimeGateStatus.RUNTIME_GATE_READY:
        reasons.append(f"runtime gate status is {record.runtime_gate_status.value}")

    if reasons:
        return ProviderSourceFamilyValidationResult(
            severity=ValidationSeverity.BLOCKED,
            passed=False,
            reasons=tuple(reasons),
        )

    return ProviderSourceFamilyValidationResult(severity=ValidationSeverity.PASSED, passed=True)
