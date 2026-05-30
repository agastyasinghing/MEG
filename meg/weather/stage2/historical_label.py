"""Supplied-metadata Stage 2 historical-label validation skeleton.

This module contains closed value sets, metadata containers, and pure validation
helpers for source-compatible weather-label metadata. It performs no data
collection, file access, service access, scoring, event monitoring, or execution.
The target is not P(weather variable crosses threshold). The target is P(the
venue-defined source/station/window/threshold/revision/classification rule
resolves Yes).
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping


class _ClosedValue(str, Enum):
    """String enum base for closed, machine-checkable Stage 2 values."""

    @classmethod
    def values(cls) -> frozenset[str]:
        return frozenset(member.value for member in cls)


class SourceResolutionStatus(_ClosedValue):
    SOURCE_RESOLVED = "source_resolved"
    SOURCE_UNRESOLVED = "source_unresolved"
    SOURCE_CONFLICTING = "source_conflicting"
    SOURCE_UNKNOWN = "source_unknown"
    REQUIRES_ADJUDICATION = "requires_adjudication"


class PointInTimeAvailabilityStatus(_ClosedValue):
    AVAILABLE_AS_OF = "available_as_of"
    UNAVAILABLE_AS_OF = "unavailable_as_of"
    AMBIGUOUS_AS_OF = "ambiguous_as_of"
    NOT_APPLICABLE = "not_applicable"
    DESIGN_ONLY = "design_only"


class LabelUsabilityPosture(_ClosedValue):
    DESIGN_ONLY = "design_only"
    USABLE_AFTER_STAGE_2_APPROVAL = "usable_after_stage_2_approval"
    BLOCKED_PENDING_SOURCE_MATCH = "blocked_pending_source_match"
    BLOCKED_PENDING_PROVENANCE = "blocked_pending_provenance"
    BLOCKED_PENDING_ADJUDICATION = "blocked_pending_adjudication"


class EvidenceStatus(_ClosedValue):
    SOURCE_BACKED = "source_backed"
    REVIEWER_INFERRED = "reviewer_inferred"
    MISSING = "missing"
    CONFLICTING = "conflicting"
    NOT_APPLICABLE = "not_applicable"


class LabelConfidence(_ClosedValue):
    CONFIRMED = "confirmed"
    UNCLEAR = "unclear"
    UNKNOWN = "unknown"


class ValidationSeverity(_ClosedValue):
    PASSED = "passed"
    CAUTION = "caution"
    FAILED = "failed"
    BLOCKED = "blocked"


@dataclass(frozen=True)
class SourceResolutionMetadata:
    resolver_source_identity: str | None
    status: SourceResolutionStatus
    evidence_status: EvidenceStatus
    reviewer_note: str = ""


@dataclass(frozen=True)
class PointInTimeProvenanceMetadata:
    availability_status: PointInTimeAvailabilityStatus
    evidence_status: EvidenceStatus
    as_of_timestamp: str | None = None
    reviewer_note: str = ""


@dataclass(frozen=True)
class LabelUsabilityMetadata:
    posture: LabelUsabilityPosture
    evidence_status: EvidenceStatus
    label_confidence: LabelConfidence
    reviewer_note: str = ""


@dataclass(frozen=True)
class HistoricalLabelMetadata:
    condition_id: str
    token_id: str
    outcome: str
    source_resolution: SourceResolutionMetadata
    point_in_time_provenance: PointInTimeProvenanceMetadata
    label_usability: LabelUsabilityMetadata
    venue_rule_summary: str = ""


@dataclass(frozen=True)
class ValidationResult:
    severity: ValidationSeverity
    passed: bool
    reasons: tuple[str, ...] = ()


_BLOCKING_SOURCE_STATUSES = frozenset(
    {
        SourceResolutionStatus.SOURCE_UNRESOLVED,
        SourceResolutionStatus.SOURCE_CONFLICTING,
        SourceResolutionStatus.SOURCE_UNKNOWN,
        SourceResolutionStatus.REQUIRES_ADJUDICATION,
    }
)
_BLOCKING_POINT_IN_TIME_STATUSES = frozenset(
    {
        PointInTimeAvailabilityStatus.UNAVAILABLE_AS_OF,
        PointInTimeAvailabilityStatus.AMBIGUOUS_AS_OF,
        PointInTimeAvailabilityStatus.NOT_APPLICABLE,
        PointInTimeAvailabilityStatus.DESIGN_ONLY,
    }
)
_BLOCKING_EVIDENCE_STATUSES = frozenset(
    {
        EvidenceStatus.REVIEWER_INFERRED,
        EvidenceStatus.MISSING,
        EvidenceStatus.CONFLICTING,
        EvidenceStatus.NOT_APPLICABLE,
    }
)
_BLOCKING_USABILITY_POSTURES = frozenset(
    {
        LabelUsabilityPosture.DESIGN_ONLY,
        LabelUsabilityPosture.BLOCKED_PENDING_SOURCE_MATCH,
        LabelUsabilityPosture.BLOCKED_PENDING_PROVENANCE,
        LabelUsabilityPosture.BLOCKED_PENDING_ADJUDICATION,
    }
)


def _enum_value(enum_type: type[_ClosedValue], value: _ClosedValue | str) -> _ClosedValue:
    if isinstance(value, enum_type):
        return value
    return enum_type(value)


def _is_nonblank_text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def source_resolution_metadata_from_mapping(metadata: Mapping[str, Any]) -> SourceResolutionMetadata:
    """Build source-resolution metadata from explicitly supplied values."""

    return SourceResolutionMetadata(
        resolver_source_identity=metadata["resolver_source_identity"],
        status=_enum_value(SourceResolutionStatus, metadata["status"]),
        evidence_status=_enum_value(EvidenceStatus, metadata["evidence_status"]),
        reviewer_note=str(metadata.get("reviewer_note", "")),
    )


def point_in_time_provenance_metadata_from_mapping(
    metadata: Mapping[str, Any],
) -> PointInTimeProvenanceMetadata:
    """Build point-in-time provenance metadata from explicitly supplied values."""

    return PointInTimeProvenanceMetadata(
        availability_status=_enum_value(
            PointInTimeAvailabilityStatus,
            metadata["availability_status"],
        ),
        evidence_status=_enum_value(EvidenceStatus, metadata["evidence_status"]),
        as_of_timestamp=metadata.get("as_of_timestamp"),
        reviewer_note=str(metadata.get("reviewer_note", "")),
    )


def label_usability_metadata_from_mapping(metadata: Mapping[str, Any]) -> LabelUsabilityMetadata:
    """Build label-usability metadata from explicitly supplied values."""

    return LabelUsabilityMetadata(
        posture=_enum_value(LabelUsabilityPosture, metadata["posture"]),
        evidence_status=_enum_value(EvidenceStatus, metadata["evidence_status"]),
        label_confidence=_enum_value(LabelConfidence, metadata["label_confidence"]),
        reviewer_note=str(metadata.get("reviewer_note", "")),
    )


def historical_label_metadata_from_mapping(metadata: Mapping[str, Any]) -> HistoricalLabelMetadata:
    """Build historical-label metadata from explicitly supplied nested values."""

    return HistoricalLabelMetadata(
        condition_id=metadata["condition_id"],
        token_id=metadata["token_id"],
        outcome=metadata["outcome"],
        source_resolution=source_resolution_metadata_from_mapping(metadata["source_resolution"]),
        point_in_time_provenance=point_in_time_provenance_metadata_from_mapping(
            metadata["point_in_time_provenance"]
        ),
        label_usability=label_usability_metadata_from_mapping(metadata["label_usability"]),
        venue_rule_summary=metadata["venue_rule_summary"],
    )


def validate_historical_label_metadata(metadata: HistoricalLabelMetadata) -> ValidationResult:
    """Validate supplied Stage 2 metadata with fail-closed behavior."""

    reasons: list[str] = []

    required_text_fields = (
        ("condition_id", metadata.condition_id),
        ("token_id", metadata.token_id),
        ("outcome", metadata.outcome),
        ("venue_rule_summary", metadata.venue_rule_summary),
    )
    for field_name, field_value in required_text_fields:
        if not _is_nonblank_text(field_value):
            reasons.append(f"{field_name} is missing")

    if not _is_nonblank_text(metadata.source_resolution.resolver_source_identity):
        reasons.append("resolver source identity is missing")

    if metadata.source_resolution.status in _BLOCKING_SOURCE_STATUSES:
        reasons.append(f"source-resolution status is {metadata.source_resolution.status.value}")

    if metadata.point_in_time_provenance.availability_status in _BLOCKING_POINT_IN_TIME_STATUSES:
        reasons.append(
            "point-in-time availability status is "
            f"{metadata.point_in_time_provenance.availability_status.value}"
        )

    evidence_fields = (
        ("source-resolution evidence", metadata.source_resolution.evidence_status),
        ("point-in-time provenance evidence", metadata.point_in_time_provenance.evidence_status),
        ("label-usability evidence", metadata.label_usability.evidence_status),
    )
    for field_name, status in evidence_fields:
        if status in _BLOCKING_EVIDENCE_STATUSES:
            reasons.append(f"{field_name} status is {status.value}")

    if metadata.label_usability.label_confidence in (
        LabelConfidence.UNCLEAR,
        LabelConfidence.UNKNOWN,
    ):
        reasons.append(f"label confidence is {metadata.label_usability.label_confidence.value}")

    if metadata.label_usability.posture in _BLOCKING_USABILITY_POSTURES:
        reasons.append(f"label usability posture is {metadata.label_usability.posture.value}")

    if reasons:
        return ValidationResult(
            severity=ValidationSeverity.BLOCKED,
            passed=False,
            reasons=tuple(reasons),
        )

    if (
        metadata.source_resolution.status is SourceResolutionStatus.SOURCE_RESOLVED
        and metadata.source_resolution.evidence_status is EvidenceStatus.SOURCE_BACKED
        and metadata.point_in_time_provenance.availability_status
        is PointInTimeAvailabilityStatus.AVAILABLE_AS_OF
        and metadata.point_in_time_provenance.evidence_status is EvidenceStatus.SOURCE_BACKED
        and metadata.label_usability.evidence_status is EvidenceStatus.SOURCE_BACKED
        and metadata.label_usability.label_confidence is LabelConfidence.CONFIRMED
        and metadata.label_usability.posture
        is LabelUsabilityPosture.USABLE_AFTER_STAGE_2_APPROVAL
    ):
        return ValidationResult(severity=ValidationSeverity.PASSED, passed=True)

    return ValidationResult(
        severity=ValidationSeverity.CAUTION,
        passed=False,
        reasons=("metadata is not explicitly source-backed, confirmed, and unblocked",),
    )
