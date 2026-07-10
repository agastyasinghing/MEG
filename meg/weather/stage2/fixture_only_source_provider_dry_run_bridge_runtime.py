"""Pure fixture-only Weather Bot Stage 2 source/provider dry-run bridge runtime scaffold.

This module consumes only caller-supplied fixture-only validation-bundle bridge
and supplied runtime dry-run packet values. It keeps an in-memory record only.
It performs no live source fetching, no live provider clients, no API calls, no
scraping, no downloads, no SDK usage, no credentials/config loading, no live
ingestion, no evidence generation, no dry-run execution, no simulation engine,
no persistence/export writing, no paper trading, no trading/execution, no
autonomy, and no production behavior.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping

from meg.weather.stage2.fixture_only_source_provider_validation_bundle_bridge_runtime import (
    FixtureOnlySourceProviderValidationBundleBridgeRecord,
    fixture_only_source_provider_validation_bundle_bridge_record_from_mapping,
    validate_fixture_only_source_provider_validation_bundle_bridge_record,
)
from meg.weather.stage2.supplied_runtime_dry_run_packet import (
    SuppliedRuntimeDryRunPacketRecord,
    supplied_runtime_dry_run_packet_record_from_mapping,
    validate_supplied_runtime_dry_run_packet_record,
)


class _ClosedValue(str, Enum):
    """String enum base for closed, machine-checkable Stage 2 values."""

    @classmethod
    def values(cls) -> frozenset[str]:
        return frozenset(member.value for member in cls)


class FixtureOnlyDryRunBridgeStatus(_ClosedValue):
    FIXTURE_ONLY_DRY_RUN_BRIDGE_RECORDED = "fixture_only_dry_run_bridge_recorded"
    FIXTURE_ONLY_DRY_RUN_BRIDGE_MISSING = "fixture_only_dry_run_bridge_missing"
    FIXTURE_ONLY_DRY_RUN_BRIDGE_AMBIGUOUS = "fixture_only_dry_run_bridge_ambiguous"
    FIXTURE_ONLY_DRY_RUN_BRIDGE_UNSUPPORTED = "fixture_only_dry_run_bridge_unsupported"
    FIXTURE_ONLY_DRY_RUN_BRIDGE_UNKNOWN = "fixture_only_dry_run_bridge_unknown"


class FixtureOnlyDryRunBridgePosture(_ClosedValue):
    FIXTURE_ONLY_DRY_RUN_BRIDGE_IN_MEMORY_ONLY = "fixture_only_dry_run_bridge_in_memory_only"
    FIXTURE_ONLY_DRY_RUN_BRIDGE_MISSING = "fixture_only_dry_run_bridge_missing"
    FIXTURE_ONLY_DRY_RUN_BRIDGE_AMBIGUOUS = "fixture_only_dry_run_bridge_ambiguous"
    FIXTURE_ONLY_DRY_RUN_BRIDGE_UNSUPPORTED = "fixture_only_dry_run_bridge_unsupported"
    FIXTURE_ONLY_DRY_RUN_BRIDGE_UNKNOWN = "fixture_only_dry_run_bridge_unknown"


class DryRunBridgeAlignmentStatus(_ClosedValue):
    DRY_RUN_BRIDGE_ALIGNED = "dry_run_bridge_aligned"
    DRY_RUN_BRIDGE_MISMATCH = "dry_run_bridge_mismatch"
    DRY_RUN_BRIDGE_MISSING = "dry_run_bridge_missing"
    DRY_RUN_BRIDGE_AMBIGUOUS = "dry_run_bridge_ambiguous"
    DRY_RUN_BRIDGE_UNKNOWN = "dry_run_bridge_unknown"


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
class FixtureOnlySourceProviderDryRunBridgeRecord:
    condition_id: str
    token_id: str
    outcome: str
    fixture_only_source_provider_validation_bundle_bridge: FixtureOnlySourceProviderValidationBundleBridgeRecord
    supplied_runtime_dry_run_packet: SuppliedRuntimeDryRunPacketRecord
    dry_run_bridge_id: str
    dry_run_bridge_summary: str
    fixture_validation_bridge_summary: str
    supplied_dry_run_summary: str
    no_lookahead_summary: str
    operator_review_summary: str
    blocked_reason_summary: str
    fixture_only_dry_run_bridge_status: FixtureOnlyDryRunBridgeStatus
    fixture_only_dry_run_bridge_posture: FixtureOnlyDryRunBridgePosture
    dry_run_bridge_alignment_status: DryRunBridgeAlignmentStatus
    no_lookahead_status: NoLookaheadStatus
    operator_review_status: OperatorReviewStatus
    runtime_gate_status: RuntimeGateStatus
    provenance_notes: str = ""


@dataclass(frozen=True)
class FixtureOnlySourceProviderDryRunBridgeValidationResult:
    severity: ValidationSeverity
    passed: bool
    reasons: tuple[str, ...] = ()


def _enum_value(enum_type: type[_ClosedValue], value: _ClosedValue | str) -> _ClosedValue:
    if isinstance(value, enum_type):
        return value
    return enum_type(value)


def _is_nonblank_text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _fixture_only_source_provider_validation_bundle_bridge_from_value(
    value: FixtureOnlySourceProviderValidationBundleBridgeRecord | Mapping[str, Any],
) -> FixtureOnlySourceProviderValidationBundleBridgeRecord:
    if isinstance(value, FixtureOnlySourceProviderValidationBundleBridgeRecord):
        return value
    return fixture_only_source_provider_validation_bundle_bridge_record_from_mapping(value)


def _supplied_runtime_dry_run_packet_from_value(
    value: SuppliedRuntimeDryRunPacketRecord | Mapping[str, Any],
) -> SuppliedRuntimeDryRunPacketRecord:
    if isinstance(value, SuppliedRuntimeDryRunPacketRecord):
        return value
    return supplied_runtime_dry_run_packet_record_from_mapping(value)


def fixture_only_source_provider_dry_run_bridge_record_from_mapping(
    mapping: Mapping[str, Any],
) -> FixtureOnlySourceProviderDryRunBridgeRecord:
    """Build dry-run bridge metadata from explicitly supplied values."""

    return FixtureOnlySourceProviderDryRunBridgeRecord(
        condition_id=mapping["condition_id"],
        token_id=mapping["token_id"],
        outcome=mapping["outcome"],
        fixture_only_source_provider_validation_bundle_bridge=(
            _fixture_only_source_provider_validation_bundle_bridge_from_value(
                mapping["fixture_only_source_provider_validation_bundle_bridge"]
            )
        ),
        supplied_runtime_dry_run_packet=_supplied_runtime_dry_run_packet_from_value(
            mapping["supplied_runtime_dry_run_packet"]
        ),
        dry_run_bridge_id=mapping["dry_run_bridge_id"],
        dry_run_bridge_summary=mapping["dry_run_bridge_summary"],
        fixture_validation_bridge_summary=mapping["fixture_validation_bridge_summary"],
        supplied_dry_run_summary=mapping["supplied_dry_run_summary"],
        no_lookahead_summary=mapping["no_lookahead_summary"],
        operator_review_summary=mapping["operator_review_summary"],
        blocked_reason_summary=mapping["blocked_reason_summary"],
        fixture_only_dry_run_bridge_status=_enum_value(
            FixtureOnlyDryRunBridgeStatus,
            mapping["fixture_only_dry_run_bridge_status"],
        ),
        fixture_only_dry_run_bridge_posture=_enum_value(
            FixtureOnlyDryRunBridgePosture,
            mapping["fixture_only_dry_run_bridge_posture"],
        ),
        dry_run_bridge_alignment_status=_enum_value(
            DryRunBridgeAlignmentStatus,
            mapping["dry_run_bridge_alignment_status"],
        ),
        no_lookahead_status=_enum_value(NoLookaheadStatus, mapping["no_lookahead_status"]),
        operator_review_status=_enum_value(OperatorReviewStatus, mapping["operator_review_status"]),
        runtime_gate_status=_enum_value(RuntimeGateStatus, mapping["runtime_gate_status"]),
        provenance_notes=str(mapping.get("provenance_notes", "")),
    )


def _same_route(left: object, right: object) -> bool:
    return (
        getattr(left, "condition_id") == getattr(right, "condition_id")
        and getattr(left, "token_id") == getattr(right, "token_id")
        and getattr(left, "outcome") == getattr(right, "outcome")
    )


def validate_fixture_only_source_provider_dry_run_bridge_record(
    record: FixtureOnlySourceProviderDryRunBridgeRecord,
) -> FixtureOnlySourceProviderDryRunBridgeValidationResult:
    """Validate fixture-only dry-run bridge metadata fail-closed."""

    reasons: list[str] = []

    for field_name, value in (
        ("condition_id", record.condition_id),
        ("token_id", record.token_id),
        ("outcome", record.outcome),
        ("dry_run_bridge_id", record.dry_run_bridge_id),
        ("dry_run_bridge_summary", record.dry_run_bridge_summary),
        ("fixture_validation_bridge_summary", record.fixture_validation_bridge_summary),
        ("supplied_dry_run_summary", record.supplied_dry_run_summary),
        ("no_lookahead_summary", record.no_lookahead_summary),
        ("operator_review_summary", record.operator_review_summary),
    ):
        if not _is_nonblank_text(value):
            reasons.append(f"{field_name} is missing")

    validation_bridge = record.fixture_only_source_provider_validation_bundle_bridge
    dry_run_packet = record.supplied_runtime_dry_run_packet
    validation_bundle = validation_bridge.supplied_runtime_validation_bundle
    dry_run_bundle = dry_run_packet.supplied_runtime_validation_bundle

    if not validate_fixture_only_source_provider_validation_bundle_bridge_record(validation_bridge).passed:
        reasons.append("fixture-only source provider validation-bundle bridge is invalid")
    if not validate_supplied_runtime_dry_run_packet_record(dry_run_packet).passed:
        reasons.append("supplied runtime dry-run packet is invalid")

    if record.condition_id != validation_bridge.condition_id:
        reasons.append("condition_id does not match fixture-only validation-bundle bridge")
    if record.token_id != validation_bridge.token_id:
        reasons.append("token_id does not match fixture-only validation-bundle bridge")
    if record.outcome != validation_bridge.outcome:
        reasons.append("outcome does not match fixture-only validation-bundle bridge")

    if record.condition_id != dry_run_packet.condition_id:
        reasons.append("condition_id does not match supplied runtime dry-run packet")
    if record.token_id != dry_run_packet.token_id:
        reasons.append("token_id does not match supplied runtime dry-run packet")
    if record.outcome != dry_run_packet.outcome:
        reasons.append("outcome does not match supplied runtime dry-run packet")

    if not _same_route(validation_bridge, dry_run_packet):
        reasons.append(
            "nested fixture-only validation-bundle bridge and supplied runtime dry-run packet routes do not match"
        )

    if not _same_route(validation_bundle, dry_run_bundle) or not _same_route(
        validation_bundle.supplied_market_contract,
        dry_run_bundle.supplied_market_contract,
    ):
        reasons.append("nested supplied runtime validation bundles do not match")

    if not _same_route(
        validation_bundle.supplied_evidence_packet,
        dry_run_bundle.supplied_evidence_packet,
    ) or not _same_route(
        validation_bundle.supplied_evidence_packet.supplied_market_contract,
        dry_run_bundle.supplied_evidence_packet.supplied_market_contract,
    ):
        reasons.append("nested supplied evidence packets do not match")

    if validation_bridge.validation_bundle_bridge_summary != record.fixture_validation_bridge_summary:
        reasons.append(
            "fixture validation bridge summary does not match fixture-only validation-bundle bridge"
        )
    if dry_run_packet.dry_run_summary != record.supplied_dry_run_summary:
        reasons.append("supplied dry-run summary does not match supplied runtime dry-run packet")
    if validation_bridge.no_lookahead_summary != record.no_lookahead_summary:
        reasons.append("no-lookahead summary does not match fixture-only validation-bundle bridge")

    if record.fixture_only_dry_run_bridge_status is not FixtureOnlyDryRunBridgeStatus.FIXTURE_ONLY_DRY_RUN_BRIDGE_RECORDED:
        reasons.append(f"fixture-only dry-run bridge status is {record.fixture_only_dry_run_bridge_status.value}")
    if record.fixture_only_dry_run_bridge_posture is not FixtureOnlyDryRunBridgePosture.FIXTURE_ONLY_DRY_RUN_BRIDGE_IN_MEMORY_ONLY:
        reasons.append(f"fixture-only dry-run bridge posture is {record.fixture_only_dry_run_bridge_posture.value}")
    if record.dry_run_bridge_alignment_status is not DryRunBridgeAlignmentStatus.DRY_RUN_BRIDGE_ALIGNED:
        reasons.append(f"dry-run bridge alignment status is {record.dry_run_bridge_alignment_status.value}")
    if record.no_lookahead_status is not NoLookaheadStatus.NO_LOOKAHEAD_RECORDED:
        reasons.append(f"no-lookahead status is {record.no_lookahead_status.value}")
    if record.operator_review_status is not OperatorReviewStatus.OPERATOR_REVIEW_REQUIRED:
        reasons.append(f"operator review status is {record.operator_review_status.value}")
    if record.runtime_gate_status is not RuntimeGateStatus.RUNTIME_GATE_READY:
        reasons.append(f"runtime gate status is {record.runtime_gate_status.value}")

    if reasons and not _is_nonblank_text(record.blocked_reason_summary):
        reasons.append("blocked_reason_summary is missing")

    if reasons:
        return FixtureOnlySourceProviderDryRunBridgeValidationResult(
            severity=ValidationSeverity.BLOCKED,
            passed=False,
            reasons=tuple(reasons),
        )

    return FixtureOnlySourceProviderDryRunBridgeValidationResult(
        severity=ValidationSeverity.PASSED,
        passed=True,
    )
