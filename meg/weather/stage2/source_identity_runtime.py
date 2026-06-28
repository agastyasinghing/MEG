"""Pure Stage 2 source-identity runtime metadata scaffold.

This module contains closed value sets, metadata containers, and fail-closed
validation helpers for explicitly supplied source-identity metadata. It performs
no data collection, file access, service access, source fetching, scoring,
backtesting, trading, autonomy, or production behavior.
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


class SourceFamily(_ClosedValue):
    FORECAST_PROVIDER_FAMILY = "forecast_provider_family"
    HISTORICAL_OBSERVATION_PROVIDER_FAMILY = "historical_observation_provider_family"
    OFFICIAL_RESOLUTION_SOURCE_FAMILY = "official_resolution_source_family"
    MARKET_METADATA_SOURCE_FAMILY = "market_metadata_source_family"
    MANUAL_HUMAN_REVIEW_SOURCE_FAMILY = "manual_human_review_source_family"
    UNSUPPORTED_SOURCE_FAMILY = "unsupported_source_family"
    UNKNOWN_SOURCE_FAMILY = "unknown_source_family"


class SourceAccessMethod(_ClosedValue):
    MANUAL_REVIEW = "manual_review"
    STATIC_REFERENCE = "static_reference"
    API_CALL = "api_call"
    SCRAPING = "scraping"
    FILE_DOWNLOAD = "file_download"
    PROVIDER_SDK = "provider_sdk"
    UNKNOWN_REQUIRES_REVIEW = "unknown_requires_review"


class SourceIdentityStatus(_ClosedValue):
    SOURCE_IDENTITY_RECORDED = "source_identity_recorded"
    SOURCE_IDENTITY_MISSING = "source_identity_missing"
    SOURCE_IDENTITY_AMBIGUOUS = "source_identity_ambiguous"
    SOURCE_IDENTITY_UNSUPPORTED = "source_identity_unsupported"
    SOURCE_IDENTITY_UNKNOWN = "source_identity_unknown"


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
class SourceIdentityRecord:
    condition_id: str
    token_id: str
    outcome: str
    source_id: str
    source_family: SourceFamily
    source_uri_descriptor: str
    source_access_method: SourceAccessMethod
    source_identity_status: SourceIdentityStatus
    runtime_gate_status: RuntimeGateStatus
    provenance_notes: str = ""


@dataclass(frozen=True)
class SourceIdentityValidationResult:
    severity: ValidationSeverity
    passed: bool
    reasons: tuple[str, ...] = ()


_ALLOWED_SOURCE_FAMILIES = frozenset(
    {
        SourceFamily.FORECAST_PROVIDER_FAMILY,
        SourceFamily.HISTORICAL_OBSERVATION_PROVIDER_FAMILY,
        SourceFamily.OFFICIAL_RESOLUTION_SOURCE_FAMILY,
        SourceFamily.MARKET_METADATA_SOURCE_FAMILY,
        SourceFamily.MANUAL_HUMAN_REVIEW_SOURCE_FAMILY,
    }
)
_ALLOWED_SOURCE_ACCESS_METHODS = frozenset(
    {SourceAccessMethod.MANUAL_REVIEW, SourceAccessMethod.STATIC_REFERENCE}
)


def _enum_value(enum_type: type[_ClosedValue], value: _ClosedValue | str) -> _ClosedValue:
    if isinstance(value, enum_type):
        return value
    return enum_type(value)


def _is_nonblank_text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def source_identity_record_from_mapping(mapping: Mapping[str, Any]) -> SourceIdentityRecord:
    """Build source-identity metadata from explicitly supplied values."""

    return SourceIdentityRecord(
        condition_id=mapping["condition_id"],
        token_id=mapping["token_id"],
        outcome=mapping["outcome"],
        source_id=mapping["source_id"],
        source_family=_enum_value(SourceFamily, mapping["source_family"]),
        source_uri_descriptor=mapping["source_uri_descriptor"],
        source_access_method=_enum_value(SourceAccessMethod, mapping["source_access_method"]),
        source_identity_status=_enum_value(
            SourceIdentityStatus, mapping["source_identity_status"]
        ),
        runtime_gate_status=_enum_value(RuntimeGateStatus, mapping["runtime_gate_status"]),
        provenance_notes=str(mapping.get("provenance_notes", "")),
    )


def validate_source_identity_record(
    record: SourceIdentityRecord,
) -> SourceIdentityValidationResult:
    """Validate supplied source-identity metadata with fail-closed behavior."""

    reasons: list[str] = []

    required_text_fields = (
        ("condition_id", record.condition_id),
        ("token_id", record.token_id),
        ("outcome", record.outcome),
        ("source_id", record.source_id),
        ("source_uri_descriptor", record.source_uri_descriptor),
    )
    for field_name, value in required_text_fields:
        if not _is_nonblank_text(value):
            reasons.append(f"{field_name} is missing")

    if record.source_family not in _ALLOWED_SOURCE_FAMILIES:
        reasons.append(f"source family is {record.source_family.value}")

    if record.source_access_method not in _ALLOWED_SOURCE_ACCESS_METHODS:
        reasons.append(f"source access method is {record.source_access_method.value}")

    if record.source_identity_status is not SourceIdentityStatus.SOURCE_IDENTITY_RECORDED:
        reasons.append(f"source identity status is {record.source_identity_status.value}")

    if record.runtime_gate_status is not RuntimeGateStatus.RUNTIME_GATE_READY:
        reasons.append(f"runtime gate status is {record.runtime_gate_status.value}")

    if reasons:
        return SourceIdentityValidationResult(
            severity=ValidationSeverity.BLOCKED,
            passed=False,
            reasons=tuple(reasons),
        )

    return SourceIdentityValidationResult(severity=ValidationSeverity.PASSED, passed=True)
