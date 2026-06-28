"""Pure Stage 2 manual-review gate runtime metadata scaffold.

This module contains closed value sets, metadata containers, and fail-closed
validation helpers for explicitly supplied manual-review gate metadata. It only
consumes caller-supplied source-identity, retrieval-context, and
provider/source-family metadata and performs no data collection, file access,
service access, source fetching, scoring, backtesting, trading, or autonomy.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping

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


class ManualReviewStatus(_ClosedValue):
    MANUAL_REVIEW_COMPLETED = "manual_review_completed"
    MANUAL_REVIEW_REQUIRED = "manual_review_required"
    MANUAL_REVIEW_MISSING = "manual_review_missing"
    MANUAL_REVIEW_AMBIGUOUS = "manual_review_ambiguous"
    MANUAL_REVIEW_REJECTED = "manual_review_rejected"
    MANUAL_REVIEW_UNKNOWN = "manual_review_unknown"


class ReviewerAuthorityStatus(_ClosedValue):
    REVIEWER_AUTHORITY_CONFIRMED = "reviewer_authority_confirmed"
    REVIEWER_AUTHORITY_MISSING = "reviewer_authority_missing"
    REVIEWER_AUTHORITY_AMBIGUOUS = "reviewer_authority_ambiguous"
    REVIEWER_AUTHORITY_UNKNOWN = "reviewer_authority_unknown"


class ManualReviewDecision(_ClosedValue):
    APPROVED_FOR_METADATA_USE = "approved_for_metadata_use"
    REJECTED_FOR_METADATA_USE = "rejected_for_metadata_use"
    REQUIRES_REVISION = "requires_revision"
    NOT_DECIDED = "not_decided"
    UNKNOWN_REQUIRES_REVIEW = "unknown_requires_review"


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
class ManualReviewGateRecord:
    condition_id: str
    token_id: str
    outcome: str
    source_identity: SourceIdentityRecord
    retrieval_context: RetrievalContextRecord
    provider_source_family: ProviderSourceFamilyRecord
    manual_review_status: ManualReviewStatus
    reviewer_authority_status: ReviewerAuthorityStatus
    manual_review_decision: ManualReviewDecision
    reviewer_id: str
    reviewed_at_utc: str
    runtime_gate_status: RuntimeGateStatus
    provenance_notes: str = ""


@dataclass(frozen=True)
class ManualReviewGateValidationResult:
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


def _provider_source_family_from_value(
    value: ProviderSourceFamilyRecord | Mapping[str, Any],
) -> ProviderSourceFamilyRecord:
    if isinstance(value, ProviderSourceFamilyRecord):
        return value
    return provider_source_family_record_from_mapping(value)


def manual_review_gate_record_from_mapping(
    mapping: Mapping[str, Any],
) -> ManualReviewGateRecord:
    """Build manual-review gate metadata from explicitly supplied values."""

    return ManualReviewGateRecord(
        condition_id=mapping["condition_id"],
        token_id=mapping["token_id"],
        outcome=mapping["outcome"],
        source_identity=_source_identity_from_value(mapping["source_identity"]),
        retrieval_context=_retrieval_context_from_value(mapping["retrieval_context"]),
        provider_source_family=_provider_source_family_from_value(
            mapping["provider_source_family"]
        ),
        manual_review_status=_enum_value(
            ManualReviewStatus, mapping["manual_review_status"]
        ),
        reviewer_authority_status=_enum_value(
            ReviewerAuthorityStatus, mapping["reviewer_authority_status"]
        ),
        manual_review_decision=_enum_value(
            ManualReviewDecision, mapping["manual_review_decision"]
        ),
        reviewer_id=mapping["reviewer_id"],
        reviewed_at_utc=mapping["reviewed_at_utc"],
        runtime_gate_status=_enum_value(RuntimeGateStatus, mapping["runtime_gate_status"]),
        provenance_notes=str(mapping.get("provenance_notes", "")),
    )


def validate_manual_review_gate_record(
    record: ManualReviewGateRecord,
) -> ManualReviewGateValidationResult:
    """Validate supplied manual-review gate metadata with fail-closed behavior."""

    reasons: list[str] = []

    for field_name, value in (
        ("condition_id", record.condition_id),
        ("token_id", record.token_id),
        ("outcome", record.outcome),
        ("reviewer_id", record.reviewer_id),
        ("reviewed_at_utc", record.reviewed_at_utc),
    ):
        if not _is_nonblank_text(value):
            reasons.append(f"{field_name} is missing")

    source_identity_result = validate_source_identity_record(record.source_identity)
    if not source_identity_result.passed:
        reasons.append("source identity validation failed")

    retrieval_context_result = validate_retrieval_context_record(record.retrieval_context)
    if not retrieval_context_result.passed:
        reasons.append("retrieval context validation failed")

    provider_source_family_result = validate_provider_source_family_record(
        record.provider_source_family
    )
    if not provider_source_family_result.passed:
        reasons.append("provider source family validation failed")

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

    if record.condition_id != record.provider_source_family.condition_id:
        reasons.append("condition_id does not match provider source family")
    if record.token_id != record.provider_source_family.token_id:
        reasons.append("token_id does not match provider source family")
    if record.outcome != record.provider_source_family.outcome:
        reasons.append("outcome does not match provider source family")

    if record.manual_review_status is not ManualReviewStatus.MANUAL_REVIEW_COMPLETED:
        reasons.append(f"manual review status is {record.manual_review_status.value}")

    if (
        record.reviewer_authority_status
        is not ReviewerAuthorityStatus.REVIEWER_AUTHORITY_CONFIRMED
    ):
        reasons.append(
            f"reviewer authority status is {record.reviewer_authority_status.value}"
        )

    if record.manual_review_decision is not ManualReviewDecision.APPROVED_FOR_METADATA_USE:
        reasons.append(f"manual review decision is {record.manual_review_decision.value}")

    if record.runtime_gate_status is not RuntimeGateStatus.RUNTIME_GATE_READY:
        reasons.append(f"runtime gate status is {record.runtime_gate_status.value}")

    if reasons:
        return ManualReviewGateValidationResult(
            severity=ValidationSeverity.BLOCKED,
            passed=False,
            reasons=tuple(reasons),
        )

    return ManualReviewGateValidationResult(severity=ValidationSeverity.PASSED, passed=True)
