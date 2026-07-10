"""Pure fixture-only Weather Bot Stage 2 source/provider end-to-end smoke bridge runtime scaffold.

This module consumes only caller-supplied fixture-only dry-run report bridge and
supplied runtime end-to-end smoke values. It is an in-memory record only. It
performs no live source fetching, no live provider clients, no API calls, no
scraping, no downloads, no SDK usage, no credentials/config loading, no live
ingestion, no evidence generation, no dry-run execution, no simulation engine,
no smoke execution, no persistence/export writing, no paper trading, no
trading/execution, no autonomy, and no production behavior.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping

from meg.weather.stage2.fixture_only_source_provider_dry_run_report_bridge_runtime import (
    FixtureOnlySourceProviderDryRunReportBridgeRecord,
    fixture_only_source_provider_dry_run_report_bridge_record_from_mapping,
    validate_fixture_only_source_provider_dry_run_report_bridge_record,
)
from meg.weather.stage2.supplied_runtime_end_to_end_smoke import (
    SuppliedRuntimeEndToEndSmokeRecord,
    supplied_runtime_end_to_end_smoke_record_from_mapping,
    validate_supplied_runtime_end_to_end_smoke_record,
)


class _ClosedValue(str, Enum):
    """String enum base for closed, machine-checkable Stage 2 values."""

    @classmethod
    def values(cls) -> frozenset[str]:
        return frozenset(member.value for member in cls)


class FixtureOnlyEndToEndSmokeBridgeStatus(_ClosedValue):
    FIXTURE_ONLY_END_TO_END_SMOKE_BRIDGE_RECORDED = "fixture_only_end_to_end_smoke_bridge_recorded"
    FIXTURE_ONLY_END_TO_END_SMOKE_BRIDGE_MISSING = "fixture_only_end_to_end_smoke_bridge_missing"
    FIXTURE_ONLY_END_TO_END_SMOKE_BRIDGE_AMBIGUOUS = "fixture_only_end_to_end_smoke_bridge_ambiguous"
    FIXTURE_ONLY_END_TO_END_SMOKE_BRIDGE_UNSUPPORTED = "fixture_only_end_to_end_smoke_bridge_unsupported"
    FIXTURE_ONLY_END_TO_END_SMOKE_BRIDGE_UNKNOWN = "fixture_only_end_to_end_smoke_bridge_unknown"


class FixtureOnlyEndToEndSmokeBridgePosture(_ClosedValue):
    FIXTURE_ONLY_END_TO_END_SMOKE_BRIDGE_IN_MEMORY_ONLY = "fixture_only_end_to_end_smoke_bridge_in_memory_only"
    FIXTURE_ONLY_END_TO_END_SMOKE_BRIDGE_MISSING = "fixture_only_end_to_end_smoke_bridge_missing"
    FIXTURE_ONLY_END_TO_END_SMOKE_BRIDGE_AMBIGUOUS = "fixture_only_end_to_end_smoke_bridge_ambiguous"
    FIXTURE_ONLY_END_TO_END_SMOKE_BRIDGE_UNSUPPORTED = "fixture_only_end_to_end_smoke_bridge_unsupported"
    FIXTURE_ONLY_END_TO_END_SMOKE_BRIDGE_UNKNOWN = "fixture_only_end_to_end_smoke_bridge_unknown"


class EndToEndSmokeBridgeAlignmentStatus(_ClosedValue):
    END_TO_END_SMOKE_BRIDGE_ALIGNED = "end_to_end_smoke_bridge_aligned"
    END_TO_END_SMOKE_BRIDGE_MISMATCH = "end_to_end_smoke_bridge_mismatch"
    END_TO_END_SMOKE_BRIDGE_MISSING = "end_to_end_smoke_bridge_missing"
    END_TO_END_SMOKE_BRIDGE_AMBIGUOUS = "end_to_end_smoke_bridge_ambiguous"
    END_TO_END_SMOKE_BRIDGE_UNKNOWN = "end_to_end_smoke_bridge_unknown"


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
class FixtureOnlySourceProviderEndToEndSmokeBridgeRecord:
    condition_id: str
    token_id: str
    outcome: str
    fixture_only_source_provider_dry_run_report_bridge: FixtureOnlySourceProviderDryRunReportBridgeRecord
    supplied_runtime_end_to_end_smoke: SuppliedRuntimeEndToEndSmokeRecord
    end_to_end_smoke_bridge_id: str
    end_to_end_smoke_bridge_summary: str
    fixture_dry_run_report_bridge_summary: str
    supplied_smoke_summary: str
    operator_review_summary: str
    blocked_reason_summary: str
    fixture_only_end_to_end_smoke_bridge_status: FixtureOnlyEndToEndSmokeBridgeStatus
    fixture_only_end_to_end_smoke_bridge_posture: FixtureOnlyEndToEndSmokeBridgePosture
    end_to_end_smoke_bridge_alignment_status: EndToEndSmokeBridgeAlignmentStatus
    no_lookahead_status: NoLookaheadStatus
    operator_review_status: OperatorReviewStatus
    runtime_gate_status: RuntimeGateStatus
    provenance_notes: str = ""


@dataclass(frozen=True)
class FixtureOnlySourceProviderEndToEndSmokeBridgeValidationResult:
    severity: ValidationSeverity
    passed: bool
    reasons: tuple[str, ...] = ()


def _enum_value(enum_type: type[_ClosedValue], value: _ClosedValue | str) -> _ClosedValue:
    if isinstance(value, enum_type):
        return value
    return enum_type(value)


def _is_nonblank_text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _fixture_only_source_provider_dry_run_report_bridge_from_value(
    value: FixtureOnlySourceProviderDryRunReportBridgeRecord | Mapping[str, Any],
) -> FixtureOnlySourceProviderDryRunReportBridgeRecord:
    if isinstance(value, FixtureOnlySourceProviderDryRunReportBridgeRecord):
        return value
    return fixture_only_source_provider_dry_run_report_bridge_record_from_mapping(value)


def _supplied_runtime_end_to_end_smoke_from_value(
    value: SuppliedRuntimeEndToEndSmokeRecord | Mapping[str, Any],
) -> SuppliedRuntimeEndToEndSmokeRecord:
    if isinstance(value, SuppliedRuntimeEndToEndSmokeRecord):
        return value
    return supplied_runtime_end_to_end_smoke_record_from_mapping(value)


def fixture_only_source_provider_end_to_end_smoke_bridge_record_from_mapping(
    mapping: Mapping[str, Any],
) -> FixtureOnlySourceProviderEndToEndSmokeBridgeRecord:
    """Build end-to-end smoke bridge metadata from explicitly supplied values."""

    return FixtureOnlySourceProviderEndToEndSmokeBridgeRecord(
        condition_id=mapping["condition_id"],
        token_id=mapping["token_id"],
        outcome=mapping["outcome"],
        fixture_only_source_provider_dry_run_report_bridge=(
            _fixture_only_source_provider_dry_run_report_bridge_from_value(
                mapping["fixture_only_source_provider_dry_run_report_bridge"]
            )
        ),
        supplied_runtime_end_to_end_smoke=_supplied_runtime_end_to_end_smoke_from_value(
            mapping["supplied_runtime_end_to_end_smoke"]
        ),
        end_to_end_smoke_bridge_id=mapping["end_to_end_smoke_bridge_id"],
        end_to_end_smoke_bridge_summary=mapping["end_to_end_smoke_bridge_summary"],
        fixture_dry_run_report_bridge_summary=mapping["fixture_dry_run_report_bridge_summary"],
        supplied_smoke_summary=mapping["supplied_smoke_summary"],
        operator_review_summary=mapping["operator_review_summary"],
        blocked_reason_summary=mapping["blocked_reason_summary"],
        fixture_only_end_to_end_smoke_bridge_status=_enum_value(
            FixtureOnlyEndToEndSmokeBridgeStatus,
            mapping["fixture_only_end_to_end_smoke_bridge_status"],
        ),
        fixture_only_end_to_end_smoke_bridge_posture=_enum_value(
            FixtureOnlyEndToEndSmokeBridgePosture,
            mapping["fixture_only_end_to_end_smoke_bridge_posture"],
        ),
        end_to_end_smoke_bridge_alignment_status=_enum_value(
            EndToEndSmokeBridgeAlignmentStatus,
            mapping["end_to_end_smoke_bridge_alignment_status"],
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


def validate_fixture_only_source_provider_end_to_end_smoke_bridge_record(
    record: FixtureOnlySourceProviderEndToEndSmokeBridgeRecord,
) -> FixtureOnlySourceProviderEndToEndSmokeBridgeValidationResult:
    """Validate fixture-only end-to-end smoke bridge metadata fail-closed."""

    reasons: list[str] = []

    for field_name, value in (
        ("condition_id", record.condition_id),
        ("token_id", record.token_id),
        ("outcome", record.outcome),
        ("end_to_end_smoke_bridge_id", record.end_to_end_smoke_bridge_id),
        ("end_to_end_smoke_bridge_summary", record.end_to_end_smoke_bridge_summary),
        ("fixture_dry_run_report_bridge_summary", record.fixture_dry_run_report_bridge_summary),
        ("supplied_smoke_summary", record.supplied_smoke_summary),
        ("operator_review_summary", record.operator_review_summary),
    ):
        if not _is_nonblank_text(value):
            reasons.append(f"{field_name} is missing")

    bridge = record.fixture_only_source_provider_dry_run_report_bridge
    smoke = record.supplied_runtime_end_to_end_smoke
    bridge_report = bridge.supplied_runtime_dry_run_report
    smoke_report = smoke.supplied_runtime_dry_run_report
    bridge_packet = bridge_report.supplied_runtime_dry_run_packet
    smoke_packet = smoke_report.supplied_runtime_dry_run_packet
    bridge_bundle = bridge_packet.supplied_runtime_validation_bundle
    smoke_bundle = smoke_packet.supplied_runtime_validation_bundle
    bridge_evidence = bridge_bundle.supplied_evidence_packet
    smoke_evidence = smoke_bundle.supplied_evidence_packet

    if not validate_fixture_only_source_provider_dry_run_report_bridge_record(bridge).passed:
        reasons.append("fixture-only source provider dry-run report bridge is invalid")
    if not validate_supplied_runtime_end_to_end_smoke_record(smoke).passed:
        reasons.append("supplied runtime end-to-end smoke is invalid")

    if record.condition_id != bridge.condition_id:
        reasons.append("condition_id does not match fixture-only dry-run report bridge")
    if record.token_id != bridge.token_id:
        reasons.append("token_id does not match fixture-only dry-run report bridge")
    if record.outcome != bridge.outcome:
        reasons.append("outcome does not match fixture-only dry-run report bridge")

    if record.condition_id != smoke.condition_id:
        reasons.append("condition_id does not match supplied runtime end-to-end smoke")
    if record.token_id != smoke.token_id:
        reasons.append("token_id does not match supplied runtime end-to-end smoke")
    if record.outcome != smoke.outcome:
        reasons.append("outcome does not match supplied runtime end-to-end smoke")

    if not _same_route(bridge, smoke):
        reasons.append(
            "nested fixture-only dry-run report bridge and supplied runtime end-to-end smoke routes do not match"
        )

    if not _same_route(bridge_report, smoke_report):
        reasons.append("nested supplied runtime dry-run reports do not match")

    if not _same_route(bridge_packet, smoke_packet) or not _same_route(bridge_bundle, smoke_bundle):
        reasons.append("nested supplied runtime dry-run packets do not match")

    if not _same_route(bridge_evidence, smoke_evidence) or not _same_route(
        bridge_evidence.supplied_market_contract,
        smoke_evidence.supplied_market_contract,
    ):
        reasons.append("nested supplied evidence packets do not match")

    if record.fixture_dry_run_report_bridge_summary != bridge.dry_run_report_bridge_summary:
        reasons.append(
            "fixture dry-run report bridge summary does not match fixture-only dry-run report bridge"
        )
    if record.supplied_smoke_summary != smoke.smoke_summary:
        reasons.append("supplied smoke summary does not match supplied runtime end-to-end smoke")
    if record.operator_review_summary != smoke.operator_review_summary:
        reasons.append("operator review summary does not match supplied runtime end-to-end smoke")
    if record.operator_review_summary != bridge.operator_review_summary:
        reasons.append("operator review summary does not match fixture-only dry-run report bridge")

    if record.fixture_only_end_to_end_smoke_bridge_status is not FixtureOnlyEndToEndSmokeBridgeStatus.FIXTURE_ONLY_END_TO_END_SMOKE_BRIDGE_RECORDED:
        reasons.append(f"fixture-only end-to-end smoke bridge status is {record.fixture_only_end_to_end_smoke_bridge_status.value}")
    if record.fixture_only_end_to_end_smoke_bridge_posture is not FixtureOnlyEndToEndSmokeBridgePosture.FIXTURE_ONLY_END_TO_END_SMOKE_BRIDGE_IN_MEMORY_ONLY:
        reasons.append(f"fixture-only end-to-end smoke bridge posture is {record.fixture_only_end_to_end_smoke_bridge_posture.value}")
    if record.end_to_end_smoke_bridge_alignment_status is not EndToEndSmokeBridgeAlignmentStatus.END_TO_END_SMOKE_BRIDGE_ALIGNED:
        reasons.append(f"end-to-end smoke bridge alignment status is {record.end_to_end_smoke_bridge_alignment_status.value}")
    if record.no_lookahead_status is not NoLookaheadStatus.NO_LOOKAHEAD_RECORDED:
        reasons.append(f"no-lookahead status is {record.no_lookahead_status.value}")
    if record.operator_review_status is not OperatorReviewStatus.OPERATOR_REVIEW_REQUIRED:
        reasons.append(f"operator review status is {record.operator_review_status.value}")
    if record.runtime_gate_status is not RuntimeGateStatus.RUNTIME_GATE_READY:
        reasons.append(f"runtime gate status is {record.runtime_gate_status.value}")

    if reasons and not _is_nonblank_text(record.blocked_reason_summary):
        reasons.append("blocked_reason_summary is missing")

    if reasons:
        return FixtureOnlySourceProviderEndToEndSmokeBridgeValidationResult(
            severity=ValidationSeverity.BLOCKED,
            passed=False,
            reasons=tuple(reasons),
        )

    return FixtureOnlySourceProviderEndToEndSmokeBridgeValidationResult(
        severity=ValidationSeverity.PASSED,
        passed=True,
    )
