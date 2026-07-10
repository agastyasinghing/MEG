"""Pure fixture-only Weather Bot Stage 2 source/provider validation-bundle bridge runtime scaffold.

This module consumes only caller-supplied fixture-only evidence bridge and
supplied runtime validation bundle values. It keeps an in-memory record only. It
performs no live source fetching, no live provider clients, no API calls, no
scraping, no downloads, no SDK usage, no credentials/config loading, no live
 ingestion, no evidence generation, no persistence/export writing, no paper
trading, no trading/execution, no autonomy, and no production behavior.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping

from meg.weather.stage2.fixture_only_source_provider_evidence_bridge_runtime import (
    FixtureOnlySourceProviderEvidenceBridgeRecord,
    fixture_only_source_provider_evidence_bridge_record_from_mapping,
    validate_fixture_only_source_provider_evidence_bridge_record,
)
from meg.weather.stage2.supplied_runtime_validation_bundle import (
    SuppliedRuntimeValidationBundleRecord,
    supplied_runtime_validation_bundle_record_from_mapping,
    validate_supplied_runtime_validation_bundle_record,
)


class _ClosedValue(str, Enum):
    """String enum base for closed, machine-checkable Stage 2 values."""

    @classmethod
    def values(cls) -> frozenset[str]:
        return frozenset(member.value for member in cls)


class FixtureOnlyValidationBundleBridgeStatus(_ClosedValue):
    FIXTURE_ONLY_VALIDATION_BUNDLE_BRIDGE_RECORDED = (
        "fixture_only_validation_bundle_bridge_recorded"
    )
    FIXTURE_ONLY_VALIDATION_BUNDLE_BRIDGE_MISSING = (
        "fixture_only_validation_bundle_bridge_missing"
    )
    FIXTURE_ONLY_VALIDATION_BUNDLE_BRIDGE_AMBIGUOUS = (
        "fixture_only_validation_bundle_bridge_ambiguous"
    )
    FIXTURE_ONLY_VALIDATION_BUNDLE_BRIDGE_UNSUPPORTED = (
        "fixture_only_validation_bundle_bridge_unsupported"
    )
    FIXTURE_ONLY_VALIDATION_BUNDLE_BRIDGE_UNKNOWN = (
        "fixture_only_validation_bundle_bridge_unknown"
    )


class FixtureOnlyValidationBundleBridgePosture(_ClosedValue):
    FIXTURE_ONLY_VALIDATION_BUNDLE_BRIDGE_IN_MEMORY_ONLY = (
        "fixture_only_validation_bundle_bridge_in_memory_only"
    )
    FIXTURE_ONLY_VALIDATION_BUNDLE_BRIDGE_MISSING = (
        "fixture_only_validation_bundle_bridge_missing"
    )
    FIXTURE_ONLY_VALIDATION_BUNDLE_BRIDGE_AMBIGUOUS = (
        "fixture_only_validation_bundle_bridge_ambiguous"
    )
    FIXTURE_ONLY_VALIDATION_BUNDLE_BRIDGE_UNSUPPORTED = (
        "fixture_only_validation_bundle_bridge_unsupported"
    )
    FIXTURE_ONLY_VALIDATION_BUNDLE_BRIDGE_UNKNOWN = (
        "fixture_only_validation_bundle_bridge_unknown"
    )


class ValidationBundleBridgeAlignmentStatus(_ClosedValue):
    VALIDATION_BUNDLE_BRIDGE_ALIGNED = "validation_bundle_bridge_aligned"
    VALIDATION_BUNDLE_BRIDGE_MISMATCH = "validation_bundle_bridge_mismatch"
    VALIDATION_BUNDLE_BRIDGE_MISSING = "validation_bundle_bridge_missing"
    VALIDATION_BUNDLE_BRIDGE_AMBIGUOUS = "validation_bundle_bridge_ambiguous"
    VALIDATION_BUNDLE_BRIDGE_UNKNOWN = "validation_bundle_bridge_unknown"


class NoLookaheadStatus(_ClosedValue):
    NO_LOOKAHEAD_RECORDED = "no_lookahead_recorded"
    NO_LOOKAHEAD_MISSING = "no_lookahead_missing"
    NO_LOOKAHEAD_AMBIGUOUS = "no_lookahead_ambiguous"
    NO_LOOKAHEAD_UNKNOWN = "no_lookahead_unknown"


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
class FixtureOnlySourceProviderValidationBundleBridgeRecord:
    condition_id: str
    token_id: str
    outcome: str
    fixture_only_source_provider_evidence_bridge: FixtureOnlySourceProviderEvidenceBridgeRecord
    supplied_runtime_validation_bundle: SuppliedRuntimeValidationBundleRecord
    validation_bundle_bridge_id: str
    validation_bundle_bridge_summary: str
    fixture_evidence_bridge_summary: str
    supplied_validation_summary: str
    no_lookahead_summary: str
    operator_review_summary: str
    blocked_reason_summary: str
    fixture_only_validation_bundle_bridge_status: FixtureOnlyValidationBundleBridgeStatus
    fixture_only_validation_bundle_bridge_posture: FixtureOnlyValidationBundleBridgePosture
    validation_bundle_bridge_alignment_status: ValidationBundleBridgeAlignmentStatus
    no_lookahead_status: NoLookaheadStatus
    operator_review_status: OperatorReviewStatus
    runtime_gate_status: RuntimeGateStatus
    provenance_notes: str = ""


@dataclass(frozen=True)
class FixtureOnlySourceProviderValidationBundleBridgeValidationResult:
    severity: ValidationSeverity
    passed: bool
    reasons: tuple[str, ...] = ()


def _enum_value(enum_type: type[_ClosedValue], value: _ClosedValue | str) -> _ClosedValue:
    if isinstance(value, enum_type):
        return value
    return enum_type(value)


def _is_nonblank_text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _fixture_only_source_provider_evidence_bridge_from_value(
    value: FixtureOnlySourceProviderEvidenceBridgeRecord | Mapping[str, Any],
) -> FixtureOnlySourceProviderEvidenceBridgeRecord:
    if isinstance(value, FixtureOnlySourceProviderEvidenceBridgeRecord):
        return value
    return fixture_only_source_provider_evidence_bridge_record_from_mapping(value)


def _supplied_runtime_validation_bundle_from_value(
    value: SuppliedRuntimeValidationBundleRecord | Mapping[str, Any],
) -> SuppliedRuntimeValidationBundleRecord:
    if isinstance(value, SuppliedRuntimeValidationBundleRecord):
        return value
    return supplied_runtime_validation_bundle_record_from_mapping(value)


def fixture_only_source_provider_validation_bundle_bridge_record_from_mapping(
    mapping: Mapping[str, Any],
) -> FixtureOnlySourceProviderValidationBundleBridgeRecord:
    """Build validation-bundle bridge metadata from explicitly supplied values."""

    return FixtureOnlySourceProviderValidationBundleBridgeRecord(
        condition_id=mapping["condition_id"],
        token_id=mapping["token_id"],
        outcome=mapping["outcome"],
        fixture_only_source_provider_evidence_bridge=(
            _fixture_only_source_provider_evidence_bridge_from_value(
                mapping["fixture_only_source_provider_evidence_bridge"]
            )
        ),
        supplied_runtime_validation_bundle=_supplied_runtime_validation_bundle_from_value(
            mapping["supplied_runtime_validation_bundle"]
        ),
        validation_bundle_bridge_id=mapping["validation_bundle_bridge_id"],
        validation_bundle_bridge_summary=mapping["validation_bundle_bridge_summary"],
        fixture_evidence_bridge_summary=mapping["fixture_evidence_bridge_summary"],
        supplied_validation_summary=mapping["supplied_validation_summary"],
        no_lookahead_summary=mapping["no_lookahead_summary"],
        operator_review_summary=mapping["operator_review_summary"],
        blocked_reason_summary=mapping["blocked_reason_summary"],
        fixture_only_validation_bundle_bridge_status=_enum_value(
            FixtureOnlyValidationBundleBridgeStatus,
            mapping["fixture_only_validation_bundle_bridge_status"],
        ),
        fixture_only_validation_bundle_bridge_posture=_enum_value(
            FixtureOnlyValidationBundleBridgePosture,
            mapping["fixture_only_validation_bundle_bridge_posture"],
        ),
        validation_bundle_bridge_alignment_status=_enum_value(
            ValidationBundleBridgeAlignmentStatus,
            mapping["validation_bundle_bridge_alignment_status"],
        ),
        no_lookahead_status=_enum_value(NoLookaheadStatus, mapping["no_lookahead_status"]),
        operator_review_status=_enum_value(
            OperatorReviewStatus,
            mapping["operator_review_status"],
        ),
        runtime_gate_status=_enum_value(RuntimeGateStatus, mapping["runtime_gate_status"]),
        provenance_notes=str(mapping.get("provenance_notes", "")),
    )


def _same_route(left: object, right: object) -> bool:
    return (
        getattr(left, "condition_id") == getattr(right, "condition_id")
        and getattr(left, "token_id") == getattr(right, "token_id")
        and getattr(left, "outcome") == getattr(right, "outcome")
    )


def validate_fixture_only_source_provider_validation_bundle_bridge_record(
    record: FixtureOnlySourceProviderValidationBundleBridgeRecord,
) -> FixtureOnlySourceProviderValidationBundleBridgeValidationResult:
    """Validate fixture-only validation-bundle bridge metadata fail-closed."""

    reasons: list[str] = []

    for field_name, value in (
        ("condition_id", record.condition_id),
        ("token_id", record.token_id),
        ("outcome", record.outcome),
        ("validation_bundle_bridge_id", record.validation_bundle_bridge_id),
        ("validation_bundle_bridge_summary", record.validation_bundle_bridge_summary),
        ("fixture_evidence_bridge_summary", record.fixture_evidence_bridge_summary),
        ("supplied_validation_summary", record.supplied_validation_summary),
        ("no_lookahead_summary", record.no_lookahead_summary),
        ("operator_review_summary", record.operator_review_summary),
    ):
        if not _is_nonblank_text(value):
            reasons.append(f"{field_name} is missing")

    fixture_bridge = record.fixture_only_source_provider_evidence_bridge
    supplied_bundle = record.supplied_runtime_validation_bundle

    fixture_result = validate_fixture_only_source_provider_evidence_bridge_record(
        fixture_bridge
    )
    if not fixture_result.passed:
        reasons.append("fixture-only source provider evidence bridge is invalid")

    supplied_result = validate_supplied_runtime_validation_bundle_record(supplied_bundle)
    if not supplied_result.passed:
        reasons.append("supplied runtime validation bundle is invalid")

    if record.condition_id != fixture_bridge.condition_id:
        reasons.append("condition_id does not match fixture-only evidence bridge")
    if record.token_id != fixture_bridge.token_id:
        reasons.append("token_id does not match fixture-only evidence bridge")
    if record.outcome != fixture_bridge.outcome:
        reasons.append("outcome does not match fixture-only evidence bridge")

    if record.condition_id != supplied_bundle.condition_id:
        reasons.append("condition_id does not match supplied runtime validation bundle")
    if record.token_id != supplied_bundle.token_id:
        reasons.append("token_id does not match supplied runtime validation bundle")
    if record.outcome != supplied_bundle.outcome:
        reasons.append("outcome does not match supplied runtime validation bundle")

    if not _same_route(fixture_bridge, supplied_bundle):
        reasons.append(
            "nested fixture-only evidence bridge and supplied runtime validation bundle routes do not match"
        )

    if not _same_route(
        fixture_bridge.fixture_only_source_provider.supplied_market_contract,
        supplied_bundle.supplied_market_contract,
    ):
        reasons.append("nested supplied market contracts do not match")

    if (
        not _same_route(fixture_bridge.supplied_evidence_packet, supplied_bundle.supplied_evidence_packet)
        or not _same_route(
            fixture_bridge.supplied_evidence_packet.supplied_market_contract,
            supplied_bundle.supplied_evidence_packet.supplied_market_contract,
        )
    ):
        reasons.append("nested supplied evidence packets do not match")

    if fixture_bridge.evidence_bridge_summary != record.fixture_evidence_bridge_summary:
        reasons.append(
            "fixture evidence bridge summary does not match fixture-only evidence bridge"
        )
    if supplied_bundle.validation_summary != record.supplied_validation_summary:
        reasons.append(
            "supplied validation summary does not match supplied runtime validation bundle"
        )
    if fixture_bridge.no_lookahead_summary != record.no_lookahead_summary:
        reasons.append("no-lookahead summary does not match fixture-only evidence bridge")

    if (
        record.fixture_only_validation_bundle_bridge_status
        is not FixtureOnlyValidationBundleBridgeStatus.FIXTURE_ONLY_VALIDATION_BUNDLE_BRIDGE_RECORDED
    ):
        reasons.append(
            "fixture-only validation bundle bridge status is "
            f"{record.fixture_only_validation_bundle_bridge_status.value}"
        )
    if (
        record.fixture_only_validation_bundle_bridge_posture
        is not FixtureOnlyValidationBundleBridgePosture.FIXTURE_ONLY_VALIDATION_BUNDLE_BRIDGE_IN_MEMORY_ONLY
    ):
        reasons.append(
            "fixture-only validation bundle bridge posture is "
            f"{record.fixture_only_validation_bundle_bridge_posture.value}"
        )
    if (
        record.validation_bundle_bridge_alignment_status
        is not ValidationBundleBridgeAlignmentStatus.VALIDATION_BUNDLE_BRIDGE_ALIGNED
    ):
        reasons.append(
            "validation bundle bridge alignment status is "
            f"{record.validation_bundle_bridge_alignment_status.value}"
        )
    if record.no_lookahead_status is not NoLookaheadStatus.NO_LOOKAHEAD_RECORDED:
        reasons.append(f"no-lookahead status is {record.no_lookahead_status.value}")
    if record.operator_review_status is not OperatorReviewStatus.OPERATOR_REVIEW_REQUIRED:
        reasons.append(f"operator review status is {record.operator_review_status.value}")
    if record.runtime_gate_status is not RuntimeGateStatus.RUNTIME_GATE_READY:
        reasons.append(f"runtime gate status is {record.runtime_gate_status.value}")

    if reasons and not _is_nonblank_text(record.blocked_reason_summary):
        reasons.append("blocked_reason_summary is missing")

    if reasons:
        return FixtureOnlySourceProviderValidationBundleBridgeValidationResult(
            severity=ValidationSeverity.BLOCKED,
            passed=False,
            reasons=tuple(reasons),
        )

    return FixtureOnlySourceProviderValidationBundleBridgeValidationResult(
        severity=ValidationSeverity.PASSED,
        passed=True,
    )
