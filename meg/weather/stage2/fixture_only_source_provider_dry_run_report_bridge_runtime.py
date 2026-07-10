"""Pure fixture-only Weather Bot Stage 2 source/provider dry-run report bridge runtime scaffold.

This module consumes only caller-supplied fixture-only dry-run bridge and supplied
runtime dry-run report values. It is an in-memory record only. It performs no
live source fetching, no live provider clients, no API calls, no scraping, no
downloads, no SDK usage, no credentials/config loading, no live ingestion, no
evidence generation, no dry-run execution, no simulation engine, no
persistence/export writing, no paper trading, no trading/execution, no autonomy,
and no production behavior.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping

from meg.weather.stage2.fixture_only_source_provider_dry_run_bridge_runtime import (
    FixtureOnlySourceProviderDryRunBridgeRecord,
    fixture_only_source_provider_dry_run_bridge_record_from_mapping,
    validate_fixture_only_source_provider_dry_run_bridge_record,
)
from meg.weather.stage2.supplied_runtime_dry_run_report import (
    SuppliedRuntimeDryRunReportRecord,
    supplied_runtime_dry_run_report_record_from_mapping,
    validate_supplied_runtime_dry_run_report_record,
)


class _ClosedValue(str, Enum):
    """String enum base for closed, machine-checkable Stage 2 values."""

    @classmethod
    def values(cls) -> frozenset[str]:
        return frozenset(member.value for member in cls)


class FixtureOnlyDryRunReportBridgeStatus(_ClosedValue):
    FIXTURE_ONLY_DRY_RUN_REPORT_BRIDGE_RECORDED = "fixture_only_dry_run_report_bridge_recorded"
    FIXTURE_ONLY_DRY_RUN_REPORT_BRIDGE_MISSING = "fixture_only_dry_run_report_bridge_missing"
    FIXTURE_ONLY_DRY_RUN_REPORT_BRIDGE_AMBIGUOUS = "fixture_only_dry_run_report_bridge_ambiguous"
    FIXTURE_ONLY_DRY_RUN_REPORT_BRIDGE_UNSUPPORTED = "fixture_only_dry_run_report_bridge_unsupported"
    FIXTURE_ONLY_DRY_RUN_REPORT_BRIDGE_UNKNOWN = "fixture_only_dry_run_report_bridge_unknown"


class FixtureOnlyDryRunReportBridgePosture(_ClosedValue):
    FIXTURE_ONLY_DRY_RUN_REPORT_BRIDGE_IN_MEMORY_ONLY = "fixture_only_dry_run_report_bridge_in_memory_only"
    FIXTURE_ONLY_DRY_RUN_REPORT_BRIDGE_MISSING = "fixture_only_dry_run_report_bridge_missing"
    FIXTURE_ONLY_DRY_RUN_REPORT_BRIDGE_AMBIGUOUS = "fixture_only_dry_run_report_bridge_ambiguous"
    FIXTURE_ONLY_DRY_RUN_REPORT_BRIDGE_UNSUPPORTED = "fixture_only_dry_run_report_bridge_unsupported"
    FIXTURE_ONLY_DRY_RUN_REPORT_BRIDGE_UNKNOWN = "fixture_only_dry_run_report_bridge_unknown"


class DryRunReportBridgeAlignmentStatus(_ClosedValue):
    DRY_RUN_REPORT_BRIDGE_ALIGNED = "dry_run_report_bridge_aligned"
    DRY_RUN_REPORT_BRIDGE_MISMATCH = "dry_run_report_bridge_mismatch"
    DRY_RUN_REPORT_BRIDGE_MISSING = "dry_run_report_bridge_missing"
    DRY_RUN_REPORT_BRIDGE_AMBIGUOUS = "dry_run_report_bridge_ambiguous"
    DRY_RUN_REPORT_BRIDGE_UNKNOWN = "dry_run_report_bridge_unknown"


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
class FixtureOnlySourceProviderDryRunReportBridgeRecord:
    condition_id: str
    token_id: str
    outcome: str
    fixture_only_source_provider_dry_run_bridge: FixtureOnlySourceProviderDryRunBridgeRecord
    supplied_runtime_dry_run_report: SuppliedRuntimeDryRunReportRecord
    dry_run_report_bridge_id: str
    dry_run_report_bridge_summary: str
    fixture_dry_run_bridge_summary: str
    supplied_report_summary: str
    operator_review_summary: str
    blocked_reason_summary: str
    fixture_only_dry_run_report_bridge_status: FixtureOnlyDryRunReportBridgeStatus
    fixture_only_dry_run_report_bridge_posture: FixtureOnlyDryRunReportBridgePosture
    dry_run_report_bridge_alignment_status: DryRunReportBridgeAlignmentStatus
    no_lookahead_status: NoLookaheadStatus
    operator_review_status: OperatorReviewStatus
    runtime_gate_status: RuntimeGateStatus
    provenance_notes: str = ""


@dataclass(frozen=True)
class FixtureOnlySourceProviderDryRunReportBridgeValidationResult:
    severity: ValidationSeverity
    passed: bool
    reasons: tuple[str, ...] = ()


def _enum_value(enum_type: type[_ClosedValue], value: _ClosedValue | str) -> _ClosedValue:
    if isinstance(value, enum_type):
        return value
    return enum_type(value)


def _is_nonblank_text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _fixture_only_source_provider_dry_run_bridge_from_value(
    value: FixtureOnlySourceProviderDryRunBridgeRecord | Mapping[str, Any],
) -> FixtureOnlySourceProviderDryRunBridgeRecord:
    if isinstance(value, FixtureOnlySourceProviderDryRunBridgeRecord):
        return value
    return fixture_only_source_provider_dry_run_bridge_record_from_mapping(value)


def _supplied_runtime_dry_run_report_from_value(
    value: SuppliedRuntimeDryRunReportRecord | Mapping[str, Any],
) -> SuppliedRuntimeDryRunReportRecord:
    if isinstance(value, SuppliedRuntimeDryRunReportRecord):
        return value
    return supplied_runtime_dry_run_report_record_from_mapping(value)


def fixture_only_source_provider_dry_run_report_bridge_record_from_mapping(
    mapping: Mapping[str, Any],
) -> FixtureOnlySourceProviderDryRunReportBridgeRecord:
    """Build dry-run report bridge metadata from explicitly supplied values."""

    return FixtureOnlySourceProviderDryRunReportBridgeRecord(
        condition_id=mapping["condition_id"],
        token_id=mapping["token_id"],
        outcome=mapping["outcome"],
        fixture_only_source_provider_dry_run_bridge=(
            _fixture_only_source_provider_dry_run_bridge_from_value(
                mapping["fixture_only_source_provider_dry_run_bridge"]
            )
        ),
        supplied_runtime_dry_run_report=_supplied_runtime_dry_run_report_from_value(
            mapping["supplied_runtime_dry_run_report"]
        ),
        dry_run_report_bridge_id=mapping["dry_run_report_bridge_id"],
        dry_run_report_bridge_summary=mapping["dry_run_report_bridge_summary"],
        fixture_dry_run_bridge_summary=mapping["fixture_dry_run_bridge_summary"],
        supplied_report_summary=mapping["supplied_report_summary"],
        operator_review_summary=mapping["operator_review_summary"],
        blocked_reason_summary=mapping["blocked_reason_summary"],
        fixture_only_dry_run_report_bridge_status=_enum_value(
            FixtureOnlyDryRunReportBridgeStatus,
            mapping["fixture_only_dry_run_report_bridge_status"],
        ),
        fixture_only_dry_run_report_bridge_posture=_enum_value(
            FixtureOnlyDryRunReportBridgePosture,
            mapping["fixture_only_dry_run_report_bridge_posture"],
        ),
        dry_run_report_bridge_alignment_status=_enum_value(
            DryRunReportBridgeAlignmentStatus,
            mapping["dry_run_report_bridge_alignment_status"],
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


def validate_fixture_only_source_provider_dry_run_report_bridge_record(
    record: FixtureOnlySourceProviderDryRunReportBridgeRecord,
) -> FixtureOnlySourceProviderDryRunReportBridgeValidationResult:
    """Validate fixture-only dry-run report bridge metadata fail-closed."""

    reasons: list[str] = []

    for field_name, value in (
        ("condition_id", record.condition_id),
        ("token_id", record.token_id),
        ("outcome", record.outcome),
        ("dry_run_report_bridge_id", record.dry_run_report_bridge_id),
        ("dry_run_report_bridge_summary", record.dry_run_report_bridge_summary),
        ("fixture_dry_run_bridge_summary", record.fixture_dry_run_bridge_summary),
        ("supplied_report_summary", record.supplied_report_summary),
        ("operator_review_summary", record.operator_review_summary),
    ):
        if not _is_nonblank_text(value):
            reasons.append(f"{field_name} is missing")

    dry_run_bridge = record.fixture_only_source_provider_dry_run_bridge
    report = record.supplied_runtime_dry_run_report
    bridge_packet = dry_run_bridge.supplied_runtime_dry_run_packet
    report_packet = report.supplied_runtime_dry_run_packet
    bridge_bundle = bridge_packet.supplied_runtime_validation_bundle
    report_bundle = report_packet.supplied_runtime_validation_bundle
    bridge_evidence = bridge_bundle.supplied_evidence_packet
    report_evidence = report_bundle.supplied_evidence_packet

    if not validate_fixture_only_source_provider_dry_run_bridge_record(dry_run_bridge).passed:
        reasons.append("fixture-only source provider dry-run bridge is invalid")
    if not validate_supplied_runtime_dry_run_report_record(report).passed:
        reasons.append("supplied runtime dry-run report is invalid")

    if record.condition_id != dry_run_bridge.condition_id:
        reasons.append("condition_id does not match fixture-only dry-run bridge")
    if record.token_id != dry_run_bridge.token_id:
        reasons.append("token_id does not match fixture-only dry-run bridge")
    if record.outcome != dry_run_bridge.outcome:
        reasons.append("outcome does not match fixture-only dry-run bridge")

    if record.condition_id != report.condition_id:
        reasons.append("condition_id does not match supplied runtime dry-run report")
    if record.token_id != report.token_id:
        reasons.append("token_id does not match supplied runtime dry-run report")
    if record.outcome != report.outcome:
        reasons.append("outcome does not match supplied runtime dry-run report")

    if not _same_route(dry_run_bridge, report):
        reasons.append(
            "nested fixture-only dry-run bridge and supplied runtime dry-run report routes do not match"
        )

    if not _same_route(bridge_packet, report_packet) or not _same_route(bridge_bundle, report_bundle):
        reasons.append("nested supplied runtime dry-run packets do not match")

    if not _same_route(bridge_evidence, report_evidence) or not _same_route(
        bridge_evidence.supplied_market_contract,
        report_evidence.supplied_market_contract,
    ):
        reasons.append("nested supplied evidence packets do not match")

    if record.fixture_dry_run_bridge_summary != dry_run_bridge.dry_run_bridge_summary:
        reasons.append("fixture dry-run bridge summary does not match fixture-only dry-run bridge")
    if record.supplied_report_summary != report.report_summary:
        reasons.append("supplied report summary does not match supplied runtime dry-run report")
    if record.operator_review_summary != report.operator_review_summary:
        reasons.append("operator review summary does not match supplied runtime dry-run report")
    if record.operator_review_summary != dry_run_bridge.operator_review_summary:
        reasons.append("operator review summary does not match fixture-only dry-run bridge")

    if record.fixture_only_dry_run_report_bridge_status is not FixtureOnlyDryRunReportBridgeStatus.FIXTURE_ONLY_DRY_RUN_REPORT_BRIDGE_RECORDED:
        reasons.append(f"fixture-only dry-run report bridge status is {record.fixture_only_dry_run_report_bridge_status.value}")
    if record.fixture_only_dry_run_report_bridge_posture is not FixtureOnlyDryRunReportBridgePosture.FIXTURE_ONLY_DRY_RUN_REPORT_BRIDGE_IN_MEMORY_ONLY:
        reasons.append(f"fixture-only dry-run report bridge posture is {record.fixture_only_dry_run_report_bridge_posture.value}")
    if record.dry_run_report_bridge_alignment_status is not DryRunReportBridgeAlignmentStatus.DRY_RUN_REPORT_BRIDGE_ALIGNED:
        reasons.append(f"dry-run report bridge alignment status is {record.dry_run_report_bridge_alignment_status.value}")
    if record.no_lookahead_status is not NoLookaheadStatus.NO_LOOKAHEAD_RECORDED:
        reasons.append(f"no-lookahead status is {record.no_lookahead_status.value}")
    if record.operator_review_status is not OperatorReviewStatus.OPERATOR_REVIEW_REQUIRED:
        reasons.append(f"operator review status is {record.operator_review_status.value}")
    if record.runtime_gate_status is not RuntimeGateStatus.RUNTIME_GATE_READY:
        reasons.append(f"runtime gate status is {record.runtime_gate_status.value}")

    if reasons and not _is_nonblank_text(record.blocked_reason_summary):
        reasons.append("blocked_reason_summary is missing")

    if reasons:
        return FixtureOnlySourceProviderDryRunReportBridgeValidationResult(
            severity=ValidationSeverity.BLOCKED,
            passed=False,
            reasons=tuple(reasons),
        )

    return FixtureOnlySourceProviderDryRunReportBridgeValidationResult(
        severity=ValidationSeverity.PASSED,
        passed=True,
    )
