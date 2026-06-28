"""Pure Stage 2 static audit surface runtime metadata scaffold.

This module contains closed value sets, metadata containers, deterministic
read-only summary helpers, and fail-closed validation helpers for explicitly
supplied static audit metadata. It only consumes caller-supplied
source-identity, retrieval-context, provider/source-family, manual-review gate,
no-lookahead metadata, and fail-closed validation metadata and performs no data
collection, file access, service access, source fetching, scoring, backtesting,
trading, or autonomy.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping

from meg.weather.stage2.fail_closed_validation_runtime import (
    FailClosedValidationRecord,
    fail_closed_validation_record_from_mapping,
    validate_fail_closed_validation_record,
)
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


class StaticAuditSurfaceStatus(_ClosedValue):
    STATIC_AUDIT_SURFACE_RECORDED = "static_audit_surface_recorded"
    STATIC_AUDIT_SURFACE_MISSING = "static_audit_surface_missing"
    STATIC_AUDIT_SURFACE_AMBIGUOUS = "static_audit_surface_ambiguous"
    STATIC_AUDIT_SURFACE_UNKNOWN = "static_audit_surface_unknown"


class AuditPresentationMode(_ClosedValue):
    READ_ONLY_SUMMARY = "read_only_summary"
    READ_ONLY_DETAIL = "read_only_detail"
    WRITE_REPORT_NOT_APPROVED = "write_report_not_approved"
    EXTERNAL_EXPORT_NOT_APPROVED = "external_export_not_approved"
    UNKNOWN_REQUIRES_REVIEW = "unknown_requires_review"


class AuditEvidenceStatus(_ClosedValue):
    ALL_REQUIRED_METADATA_VALIDATED = "all_required_metadata_validated"
    METADATA_VALIDATION_FAILED = "metadata_validation_failed"
    METADATA_VALIDATION_MISSING = "metadata_validation_missing"
    METADATA_VALIDATION_UNKNOWN = "metadata_validation_unknown"


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
class StaticAuditSurfaceRecord:
    condition_id: str
    token_id: str
    outcome: str
    source_identity: SourceIdentityRecord
    retrieval_context: RetrievalContextRecord
    provider_source_family: ProviderSourceFamilyRecord
    manual_review_gate: ManualReviewGateRecord
    no_lookahead_metadata: NoLookaheadMetadataRecord
    fail_closed_validation: FailClosedValidationRecord
    static_audit_surface_status: StaticAuditSurfaceStatus
    audit_presentation_mode: AuditPresentationMode
    audit_evidence_status: AuditEvidenceStatus
    runtime_gate_status: RuntimeGateStatus
    provenance_notes: str = ""


@dataclass(frozen=True)
class StaticAuditSurfaceValidationResult:
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


def _fail_closed_validation_from_value(
    value: FailClosedValidationRecord | Mapping[str, Any],
) -> FailClosedValidationRecord:
    if isinstance(value, FailClosedValidationRecord):
        return value
    return fail_closed_validation_record_from_mapping(value)


def static_audit_surface_record_from_mapping(
    mapping: Mapping[str, Any],
) -> StaticAuditSurfaceRecord:
    """Build static audit surface metadata from explicitly supplied values."""

    return StaticAuditSurfaceRecord(
        condition_id=mapping["condition_id"],
        token_id=mapping["token_id"],
        outcome=mapping["outcome"],
        source_identity=_source_identity_from_value(mapping["source_identity"]),
        retrieval_context=_retrieval_context_from_value(mapping["retrieval_context"]),
        provider_source_family=_provider_source_family_from_value(
            mapping["provider_source_family"]
        ),
        manual_review_gate=_manual_review_gate_from_value(mapping["manual_review_gate"]),
        no_lookahead_metadata=_no_lookahead_metadata_from_value(
            mapping["no_lookahead_metadata"]
        ),
        fail_closed_validation=_fail_closed_validation_from_value(
            mapping["fail_closed_validation"]
        ),
        static_audit_surface_status=_enum_value(
            StaticAuditSurfaceStatus, mapping["static_audit_surface_status"]
        ),
        audit_presentation_mode=_enum_value(
            AuditPresentationMode, mapping["audit_presentation_mode"]
        ),
        audit_evidence_status=_enum_value(
            AuditEvidenceStatus, mapping["audit_evidence_status"]
        ),
        runtime_gate_status=_enum_value(RuntimeGateStatus, mapping["runtime_gate_status"]),
        provenance_notes=str(mapping.get("provenance_notes", "")),
    )


def validate_static_audit_surface_record(
    record: StaticAuditSurfaceRecord,
) -> StaticAuditSurfaceValidationResult:
    """Validate supplied static audit metadata with fail-closed behavior."""

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
    if not validate_fail_closed_validation_record(record.fail_closed_validation).passed:
        reasons.append("fail-closed validation failed")

    nested_records = (
        ("source identity", record.source_identity),
        ("retrieval context", record.retrieval_context),
        ("provider source family", record.provider_source_family),
        ("manual review gate", record.manual_review_gate),
        ("no-lookahead metadata", record.no_lookahead_metadata),
        ("fail-closed validation", record.fail_closed_validation),
    )
    for label, nested_record in nested_records:
        if record.condition_id != nested_record.condition_id:
            reasons.append(f"condition_id does not match {label}")
        if record.token_id != nested_record.token_id:
            reasons.append(f"token_id does not match {label}")
        if record.outcome != nested_record.outcome:
            reasons.append(f"outcome does not match {label}")

    if (
        record.static_audit_surface_status
        is not StaticAuditSurfaceStatus.STATIC_AUDIT_SURFACE_RECORDED
    ):
        reasons.append(
            f"static audit surface status is {record.static_audit_surface_status.value}"
        )

    if record.audit_presentation_mode not in {
        AuditPresentationMode.READ_ONLY_SUMMARY,
        AuditPresentationMode.READ_ONLY_DETAIL,
    }:
        reasons.append(
            f"audit presentation mode is {record.audit_presentation_mode.value}"
        )

    if (
        record.audit_evidence_status
        is not AuditEvidenceStatus.ALL_REQUIRED_METADATA_VALIDATED
    ):
        reasons.append(f"audit evidence status is {record.audit_evidence_status.value}")

    if record.runtime_gate_status is not RuntimeGateStatus.RUNTIME_GATE_READY:
        reasons.append(f"runtime gate status is {record.runtime_gate_status.value}")

    if reasons:
        return StaticAuditSurfaceValidationResult(
            severity=ValidationSeverity.BLOCKED,
            passed=False,
            reasons=tuple(reasons),
        )

    return StaticAuditSurfaceValidationResult(
        severity=ValidationSeverity.PASSED, passed=True
    )


def static_audit_summary(record: StaticAuditSurfaceRecord) -> tuple[str, ...]:
    """Return a deterministic read-only static audit summary."""

    return (
        f"condition_id={record.condition_id}",
        f"token_id={record.token_id}",
        f"outcome={record.outcome}",
        f"static_audit_surface_status={record.static_audit_surface_status.value}",
        f"audit_presentation_mode={record.audit_presentation_mode.value}",
        f"audit_evidence_status={record.audit_evidence_status.value}",
        f"runtime_gate_status={record.runtime_gate_status.value}",
    )
