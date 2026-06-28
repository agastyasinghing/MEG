"""Pure Stage 2 no-lookahead metadata runtime scaffold.

This module contains closed value sets, metadata containers, and fail-closed
validation helpers for explicitly supplied no-lookahead metadata. It only
consumes caller-supplied source-identity, retrieval-context,
provider/source-family, and manual-review gate metadata and performs no data
collection, file access, service access, source fetching, scoring,
backtesting, trading, or autonomy.
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


class NoLookaheadVerificationStatus(_ClosedValue):
    NO_LOOKAHEAD_VERIFIED = "no_lookahead_verified"
    NO_LOOKAHEAD_MISSING = "no_lookahead_missing"
    NO_LOOKAHEAD_AMBIGUOUS = "no_lookahead_ambiguous"
    NO_LOOKAHEAD_FAILED = "no_lookahead_failed"
    NO_LOOKAHEAD_UNKNOWN = "no_lookahead_unknown"


class AvailabilityTimingStatus(_ClosedValue):
    AVAILABILITY_BEFORE_DECISION = "availability_before_decision"
    AVAILABILITY_AT_DECISION = "availability_at_decision"
    AVAILABILITY_AFTER_DECISION = "availability_after_decision"
    AVAILABILITY_MISSING = "availability_missing"
    AVAILABILITY_AMBIGUOUS = "availability_ambiguous"
    AVAILABILITY_UNKNOWN = "availability_unknown"


class DecisionTimingStatus(_ClosedValue):
    DECISION_TIME_RECORDED = "decision_time_recorded"
    DECISION_TIME_MISSING = "decision_time_missing"
    DECISION_TIME_AMBIGUOUS = "decision_time_ambiguous"
    DECISION_TIME_UNKNOWN = "decision_time_unknown"


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
class NoLookaheadMetadataRecord:
    condition_id: str
    token_id: str
    outcome: str
    source_identity: SourceIdentityRecord
    retrieval_context: RetrievalContextRecord
    provider_source_family: ProviderSourceFamilyRecord
    manual_review_gate: ManualReviewGateRecord
    available_at_utc: str
    decision_time_utc: str
    no_lookahead_verification_status: NoLookaheadVerificationStatus
    availability_timing_status: AvailabilityTimingStatus
    decision_timing_status: DecisionTimingStatus
    runtime_gate_status: RuntimeGateStatus
    provenance_notes: str = ""


@dataclass(frozen=True)
class NoLookaheadMetadataValidationResult:
    severity: ValidationSeverity
    passed: bool
    reasons: tuple[str, ...] = ()


_ALLOWED_AVAILABILITY_TIMING_STATUSES = frozenset(
    {
        AvailabilityTimingStatus.AVAILABILITY_BEFORE_DECISION,
        AvailabilityTimingStatus.AVAILABILITY_AT_DECISION,
    }
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


def no_lookahead_metadata_record_from_mapping(
    mapping: Mapping[str, Any],
) -> NoLookaheadMetadataRecord:
    """Build no-lookahead metadata from explicitly supplied values."""

    return NoLookaheadMetadataRecord(
        condition_id=mapping["condition_id"],
        token_id=mapping["token_id"],
        outcome=mapping["outcome"],
        source_identity=_source_identity_from_value(mapping["source_identity"]),
        retrieval_context=_retrieval_context_from_value(mapping["retrieval_context"]),
        provider_source_family=_provider_source_family_from_value(
            mapping["provider_source_family"]
        ),
        manual_review_gate=_manual_review_gate_from_value(mapping["manual_review_gate"]),
        available_at_utc=mapping["available_at_utc"],
        decision_time_utc=mapping["decision_time_utc"],
        no_lookahead_verification_status=_enum_value(
            NoLookaheadVerificationStatus,
            mapping["no_lookahead_verification_status"],
        ),
        availability_timing_status=_enum_value(
            AvailabilityTimingStatus, mapping["availability_timing_status"]
        ),
        decision_timing_status=_enum_value(
            DecisionTimingStatus, mapping["decision_timing_status"]
        ),
        runtime_gate_status=_enum_value(RuntimeGateStatus, mapping["runtime_gate_status"]),
        provenance_notes=str(mapping.get("provenance_notes", "")),
    )


def validate_no_lookahead_metadata_record(
    record: NoLookaheadMetadataRecord,
) -> NoLookaheadMetadataValidationResult:
    """Validate supplied no-lookahead metadata with fail-closed behavior."""

    reasons: list[str] = []

    for field_name, value in (
        ("condition_id", record.condition_id),
        ("token_id", record.token_id),
        ("outcome", record.outcome),
        ("available_at_utc", record.available_at_utc),
        ("decision_time_utc", record.decision_time_utc),
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

    nested_records = (
        ("source identity", record.source_identity),
        ("retrieval context", record.retrieval_context),
        ("provider source family", record.provider_source_family),
        ("manual review gate", record.manual_review_gate),
    )
    for label, nested_record in nested_records:
        if record.condition_id != nested_record.condition_id:
            reasons.append(f"condition_id does not match {label}")
        if record.token_id != nested_record.token_id:
            reasons.append(f"token_id does not match {label}")
        if record.outcome != nested_record.outcome:
            reasons.append(f"outcome does not match {label}")

    if record.available_at_utc != record.retrieval_context.available_at_utc:
        reasons.append("available_at_utc does not match retrieval context")
    if record.decision_time_utc != record.retrieval_context.decision_time_utc:
        reasons.append("decision_time_utc does not match retrieval context")

    if (
        record.no_lookahead_verification_status
        is not NoLookaheadVerificationStatus.NO_LOOKAHEAD_VERIFIED
    ):
        reasons.append(
            "no-lookahead verification status is "
            f"{record.no_lookahead_verification_status.value}"
        )

    if record.availability_timing_status not in _ALLOWED_AVAILABILITY_TIMING_STATUSES:
        reasons.append(
            f"availability timing status is {record.availability_timing_status.value}"
        )

    if record.decision_timing_status is not DecisionTimingStatus.DECISION_TIME_RECORDED:
        reasons.append(f"decision timing status is {record.decision_timing_status.value}")

    if record.runtime_gate_status is not RuntimeGateStatus.RUNTIME_GATE_READY:
        reasons.append(f"runtime gate status is {record.runtime_gate_status.value}")

    if reasons:
        return NoLookaheadMetadataValidationResult(
            severity=ValidationSeverity.BLOCKED,
            passed=False,
            reasons=tuple(reasons),
        )

    return NoLookaheadMetadataValidationResult(
        severity=ValidationSeverity.PASSED, passed=True
    )
