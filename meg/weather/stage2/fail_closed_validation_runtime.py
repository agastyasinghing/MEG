"""Pure Stage 2 fail-closed validation runtime metadata scaffold.

This module contains closed value sets, metadata containers, and fail-closed
validation helpers for explicitly supplied aggregate validation metadata. It
only consumes caller-supplied source-identity, retrieval-context,
provider/source-family, manual-review gate, and no-lookahead metadata and
performs no data collection, file access, service access, source fetching,
scoring, backtesting, trading, or autonomy.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping

from meg.weather.stage2.manual_review_gate_runtime import (
    ManualReviewGateRecord,
    manual_review_gate_record_from_mapping,
    validate_manual_review_gate_record,
)
from meg.weather.stage2.no_lookahead_metadata_runtime import (
    NoLookaheadMetadataRecord,
    no_lookahead_metadata_record_from_mapping,
    validate_no_lookahead_metadata_record,
)
from meg.weather.stage2.provider_source_family_runtime import (
    ProviderSourceFamilyRecord,
    provider_source_family_record_from_mapping,
    validate_provider_source_family_record,
)
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


class AggregateValidationStatus(_ClosedValue):
    AGGREGATE_VALIDATION_PASSED = "aggregate_validation_passed"
    AGGREGATE_VALIDATION_FAILED = "aggregate_validation_failed"
    AGGREGATE_VALIDATION_BLOCKED = "aggregate_validation_blocked"
    AGGREGATE_VALIDATION_UNKNOWN = "aggregate_validation_unknown"


class DependencyValidationStatus(_ClosedValue):
    ALL_DEPENDENCIES_VALIDATED = "all_dependencies_validated"
    DEPENDENCY_VALIDATION_FAILED = "dependency_validation_failed"
    DEPENDENCY_VALIDATION_MISSING = "dependency_validation_missing"
    DEPENDENCY_VALIDATION_UNKNOWN = "dependency_validation_unknown"


class FailClosedPosture(_ClosedValue):
    FAIL_CLOSED_ENFORCED = "fail_closed_enforced"
    FAIL_CLOSED_MISSING = "fail_closed_missing"
    FAIL_CLOSED_AMBIGUOUS = "fail_closed_ambiguous"
    FAIL_CLOSED_UNKNOWN = "fail_closed_unknown"


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
class FailClosedValidationRecord:
    condition_id: str
    token_id: str
    outcome: str
    source_identity: SourceIdentityRecord
    retrieval_context: RetrievalContextRecord
    provider_source_family: ProviderSourceFamilyRecord
    manual_review_gate: ManualReviewGateRecord
    no_lookahead_metadata: NoLookaheadMetadataRecord
    aggregate_validation_status: AggregateValidationStatus
    dependency_validation_status: DependencyValidationStatus
    fail_closed_posture: FailClosedPosture
    runtime_gate_status: RuntimeGateStatus
    provenance_notes: str = ""


@dataclass(frozen=True)
class FailClosedValidationResult:
    severity: ValidationSeverity
    passed: bool
    reasons: tuple[str, ...] = ()


def _enum_value(
    enum_type: type[_ClosedValue], value: _ClosedValue | str
) -> _ClosedValue:
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


def _provider_source_family_from_value(
    value: ProviderSourceFamilyRecord | Mapping[str, Any],
) -> ProviderSourceFamilyRecord:
    if isinstance(value, ProviderSourceFamilyRecord):
        return value
    return provider_source_family_record_from_mapping(value)


def _manual_review_gate_from_value(
    value: ManualReviewGateRecord | Mapping[str, Any],
) -> ManualReviewGateRecord:
    if isinstance(value, ManualReviewGateRecord):
        return value
    return manual_review_gate_record_from_mapping(value)


def _no_lookahead_metadata_from_value(
    value: NoLookaheadMetadataRecord | Mapping[str, Any],
) -> NoLookaheadMetadataRecord:
    if isinstance(value, NoLookaheadMetadataRecord):
        return value
    return no_lookahead_metadata_record_from_mapping(value)


def fail_closed_validation_record_from_mapping(
    mapping: Mapping[str, Any],
) -> FailClosedValidationRecord:
    """Build aggregate validation metadata from explicitly supplied values."""

    return FailClosedValidationRecord(
        condition_id=mapping["condition_id"],
        token_id=mapping["token_id"],
        outcome=mapping["outcome"],
        source_identity=_source_identity_from_value(mapping["source_identity"]),
        retrieval_context=_retrieval_context_from_value(mapping["retrieval_context"]),
        provider_source_family=_provider_source_family_from_value(
            mapping["provider_source_family"]
        ),
        manual_review_gate=_manual_review_gate_from_value(
            mapping["manual_review_gate"]
        ),
        no_lookahead_metadata=_no_lookahead_metadata_from_value(
            mapping["no_lookahead_metadata"]
        ),
        aggregate_validation_status=_enum_value(
            AggregateValidationStatus, mapping["aggregate_validation_status"]
        ),
        dependency_validation_status=_enum_value(
            DependencyValidationStatus, mapping["dependency_validation_status"]
        ),
        fail_closed_posture=_enum_value(
            FailClosedPosture, mapping["fail_closed_posture"]
        ),
        runtime_gate_status=_enum_value(
            RuntimeGateStatus, mapping["runtime_gate_status"]
        ),
        provenance_notes=str(mapping.get("provenance_notes", "")),
    )


def validate_fail_closed_validation_record(
    record: FailClosedValidationRecord,
) -> FailClosedValidationResult:
    """Validate supplied aggregate metadata with fail-closed behavior."""

    reasons: list[str] = []

    for field_name, value in (
        ("condition_id", record.condition_id),
        ("token_id", record.token_id),
        ("outcome", record.outcome),
    ):
        if not _is_nonblank_text(value):
            reasons.append(f"{field_name} is missing")

    if not validate_source_identity_record(record.source_identity).passed:
        reasons.append("source identity validation failed")
    if not validate_retrieval_context_record(record.retrieval_context).passed:
        reasons.append("retrieval context validation failed")
    if not validate_provider_source_family_record(record.provider_source_family).passed:
        reasons.append("provider source family validation failed")
    if not validate_manual_review_gate_record(record.manual_review_gate).passed:
        reasons.append("manual review gate validation failed")
    if not validate_no_lookahead_metadata_record(record.no_lookahead_metadata).passed:
        reasons.append("no-lookahead metadata validation failed")

    nested_records = (
        ("source identity", record.source_identity),
        ("retrieval context", record.retrieval_context),
        ("provider source family", record.provider_source_family),
        ("manual review gate", record.manual_review_gate),
        ("no-lookahead metadata", record.no_lookahead_metadata),
    )
    for label, nested_record in nested_records:
        if record.condition_id != nested_record.condition_id:
            reasons.append(f"condition_id does not match {label}")
        if record.token_id != nested_record.token_id:
            reasons.append(f"token_id does not match {label}")
        if record.outcome != nested_record.outcome:
            reasons.append(f"outcome does not match {label}")

    if (
        record.aggregate_validation_status
        is not AggregateValidationStatus.AGGREGATE_VALIDATION_PASSED
    ):
        reasons.append(
            f"aggregate validation status is {record.aggregate_validation_status.value}"
        )

    if (
        record.dependency_validation_status
        is not DependencyValidationStatus.ALL_DEPENDENCIES_VALIDATED
    ):
        reasons.append(
            f"dependency validation status is {record.dependency_validation_status.value}"
        )

    if record.fail_closed_posture is not FailClosedPosture.FAIL_CLOSED_ENFORCED:
        reasons.append(f"fail-closed posture is {record.fail_closed_posture.value}")

    if record.runtime_gate_status is not RuntimeGateStatus.RUNTIME_GATE_READY:
        reasons.append(f"runtime gate status is {record.runtime_gate_status.value}")

    if reasons:
        return FailClosedValidationResult(
            severity=ValidationSeverity.BLOCKED,
            passed=False,
            reasons=tuple(reasons),
        )

    return FailClosedValidationResult(severity=ValidationSeverity.PASSED, passed=True)
