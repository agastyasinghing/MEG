"""Pure fixture-only Weather Bot Stage 2 source/provider trace bridge runtime scaffold.

This module consumes only caller-supplied fixture-only end-to-end smoke bridge
and supplied runtime trace packet values. It is an in-memory record only. It
performs no live source fetching, no live provider clients, no API calls, no
scraping, no downloads, no SDK usage, no credentials/config loading, no live
ingestion, no evidence generation, no dry-run execution, no simulation engine,
no report generation, no smoke execution, no trace execution, no
persistence/export writing, no paper trading, no trading/execution, no
autonomy, and no production behavior.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping

from meg.weather.stage2.fixture_only_source_provider_end_to_end_smoke_bridge_runtime import (
    FixtureOnlySourceProviderEndToEndSmokeBridgeRecord,
    fixture_only_source_provider_end_to_end_smoke_bridge_record_from_mapping,
    validate_fixture_only_source_provider_end_to_end_smoke_bridge_record,
)
from meg.weather.stage2.supplied_runtime_trace_packet import (
    SuppliedRuntimeTracePacketRecord,
    supplied_runtime_trace_packet_record_from_mapping,
    validate_supplied_runtime_trace_packet_record,
)


class _ClosedValue(str, Enum):
    """String enum base for closed, machine-checkable Stage 2 values."""

    @classmethod
    def values(cls) -> frozenset[str]:
        return frozenset(member.value for member in cls)


class FixtureOnlyTraceBridgeStatus(_ClosedValue):
    FIXTURE_ONLY_TRACE_BRIDGE_RECORDED = "fixture_only_trace_bridge_recorded"
    FIXTURE_ONLY_TRACE_BRIDGE_MISSING = "fixture_only_trace_bridge_missing"
    FIXTURE_ONLY_TRACE_BRIDGE_AMBIGUOUS = "fixture_only_trace_bridge_ambiguous"
    FIXTURE_ONLY_TRACE_BRIDGE_UNSUPPORTED = "fixture_only_trace_bridge_unsupported"
    FIXTURE_ONLY_TRACE_BRIDGE_UNKNOWN = "fixture_only_trace_bridge_unknown"


class FixtureOnlyTraceBridgePosture(_ClosedValue):
    FIXTURE_ONLY_TRACE_BRIDGE_IN_MEMORY_ONLY = "fixture_only_trace_bridge_in_memory_only"
    FIXTURE_ONLY_TRACE_BRIDGE_MISSING = "fixture_only_trace_bridge_missing"
    FIXTURE_ONLY_TRACE_BRIDGE_AMBIGUOUS = "fixture_only_trace_bridge_ambiguous"
    FIXTURE_ONLY_TRACE_BRIDGE_UNSUPPORTED = "fixture_only_trace_bridge_unsupported"
    FIXTURE_ONLY_TRACE_BRIDGE_UNKNOWN = "fixture_only_trace_bridge_unknown"


class TraceBridgeAlignmentStatus(_ClosedValue):
    TRACE_BRIDGE_ALIGNED = "trace_bridge_aligned"
    TRACE_BRIDGE_MISMATCH = "trace_bridge_mismatch"
    TRACE_BRIDGE_MISSING = "trace_bridge_missing"
    TRACE_BRIDGE_AMBIGUOUS = "trace_bridge_ambiguous"
    TRACE_BRIDGE_UNKNOWN = "trace_bridge_unknown"


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
class FixtureOnlySourceProviderTraceBridgeRecord:
    condition_id: str
    token_id: str
    outcome: str
    fixture_only_source_provider_end_to_end_smoke_bridge: FixtureOnlySourceProviderEndToEndSmokeBridgeRecord
    supplied_runtime_trace_packet: SuppliedRuntimeTracePacketRecord
    trace_bridge_id: str
    trace_bridge_summary: str
    fixture_end_to_end_smoke_bridge_summary: str
    supplied_trace_summary: str
    operator_review_summary: str
    blocked_reason_summary: str
    fixture_only_trace_bridge_status: FixtureOnlyTraceBridgeStatus
    fixture_only_trace_bridge_posture: FixtureOnlyTraceBridgePosture
    trace_bridge_alignment_status: TraceBridgeAlignmentStatus
    no_lookahead_status: NoLookaheadStatus
    operator_review_status: OperatorReviewStatus
    runtime_gate_status: RuntimeGateStatus
    provenance_notes: str = ""


@dataclass(frozen=True)
class FixtureOnlySourceProviderTraceBridgeValidationResult:
    severity: ValidationSeverity
    passed: bool
    reasons: tuple[str, ...] = ()


def _enum_value(enum_type: type[_ClosedValue], value: _ClosedValue | str) -> _ClosedValue:
    if isinstance(value, enum_type):
        return value
    return enum_type(value)


def _is_nonblank_text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _fixture_only_source_provider_end_to_end_smoke_bridge_from_value(
    value: FixtureOnlySourceProviderEndToEndSmokeBridgeRecord | Mapping[str, Any],
) -> FixtureOnlySourceProviderEndToEndSmokeBridgeRecord:
    if isinstance(value, FixtureOnlySourceProviderEndToEndSmokeBridgeRecord):
        return value
    return fixture_only_source_provider_end_to_end_smoke_bridge_record_from_mapping(value)


def _supplied_runtime_trace_packet_from_value(
    value: SuppliedRuntimeTracePacketRecord | Mapping[str, Any],
) -> SuppliedRuntimeTracePacketRecord:
    if isinstance(value, SuppliedRuntimeTracePacketRecord):
        return value
    return supplied_runtime_trace_packet_record_from_mapping(value)


def fixture_only_source_provider_trace_bridge_record_from_mapping(
    mapping: Mapping[str, Any],
) -> FixtureOnlySourceProviderTraceBridgeRecord:
    """Build trace bridge metadata from explicitly supplied values."""

    return FixtureOnlySourceProviderTraceBridgeRecord(
        condition_id=mapping["condition_id"],
        token_id=mapping["token_id"],
        outcome=mapping["outcome"],
        fixture_only_source_provider_end_to_end_smoke_bridge=(
            _fixture_only_source_provider_end_to_end_smoke_bridge_from_value(
                mapping["fixture_only_source_provider_end_to_end_smoke_bridge"]
            )
        ),
        supplied_runtime_trace_packet=_supplied_runtime_trace_packet_from_value(
            mapping["supplied_runtime_trace_packet"]
        ),
        trace_bridge_id=mapping["trace_bridge_id"],
        trace_bridge_summary=mapping["trace_bridge_summary"],
        fixture_end_to_end_smoke_bridge_summary=mapping[
            "fixture_end_to_end_smoke_bridge_summary"
        ],
        supplied_trace_summary=mapping["supplied_trace_summary"],
        operator_review_summary=mapping["operator_review_summary"],
        blocked_reason_summary=mapping["blocked_reason_summary"],
        fixture_only_trace_bridge_status=_enum_value(
            FixtureOnlyTraceBridgeStatus,
            mapping["fixture_only_trace_bridge_status"],
        ),
        fixture_only_trace_bridge_posture=_enum_value(
            FixtureOnlyTraceBridgePosture,
            mapping["fixture_only_trace_bridge_posture"],
        ),
        trace_bridge_alignment_status=_enum_value(
            TraceBridgeAlignmentStatus,
            mapping["trace_bridge_alignment_status"],
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


def validate_fixture_only_source_provider_trace_bridge_record(
    record: FixtureOnlySourceProviderTraceBridgeRecord,
) -> FixtureOnlySourceProviderTraceBridgeValidationResult:
    """Validate fixture-only trace bridge metadata fail-closed."""

    reasons: list[str] = []

    for field_name, value in (
        ("condition_id", record.condition_id),
        ("token_id", record.token_id),
        ("outcome", record.outcome),
        ("trace_bridge_id", record.trace_bridge_id),
        ("trace_bridge_summary", record.trace_bridge_summary),
        ("fixture_end_to_end_smoke_bridge_summary", record.fixture_end_to_end_smoke_bridge_summary),
        ("supplied_trace_summary", record.supplied_trace_summary),
        ("operator_review_summary", record.operator_review_summary),
    ):
        if not _is_nonblank_text(value):
            reasons.append(f"{field_name} is missing")

    fixture_bridge = record.fixture_only_source_provider_end_to_end_smoke_bridge
    trace_packet = record.supplied_runtime_trace_packet
    fixture_smoke = fixture_bridge.supplied_runtime_end_to_end_smoke
    trace_smoke = trace_packet.supplied_runtime_end_to_end_smoke
    fixture_report = fixture_smoke.supplied_runtime_dry_run_report
    trace_report = trace_smoke.supplied_runtime_dry_run_report
    fixture_packet = fixture_report.supplied_runtime_dry_run_packet
    trace_dry_run_packet = trace_report.supplied_runtime_dry_run_packet
    fixture_bundle = fixture_packet.supplied_runtime_validation_bundle
    trace_bundle = trace_dry_run_packet.supplied_runtime_validation_bundle
    fixture_evidence = fixture_bundle.supplied_evidence_packet
    trace_evidence = trace_bundle.supplied_evidence_packet

    if not validate_fixture_only_source_provider_end_to_end_smoke_bridge_record(fixture_bridge).passed:
        reasons.append("fixture-only source provider end-to-end smoke bridge is invalid")
    if not validate_supplied_runtime_trace_packet_record(trace_packet).passed:
        reasons.append("supplied runtime trace packet is invalid")

    if record.condition_id != fixture_bridge.condition_id:
        reasons.append("condition_id does not match fixture-only end-to-end smoke bridge")
    if record.token_id != fixture_bridge.token_id:
        reasons.append("token_id does not match fixture-only end-to-end smoke bridge")
    if record.outcome != fixture_bridge.outcome:
        reasons.append("outcome does not match fixture-only end-to-end smoke bridge")

    if record.condition_id != trace_packet.condition_id:
        reasons.append("condition_id does not match supplied runtime trace packet")
    if record.token_id != trace_packet.token_id:
        reasons.append("token_id does not match supplied runtime trace packet")
    if record.outcome != trace_packet.outcome:
        reasons.append("outcome does not match supplied runtime trace packet")

    if not _same_route(fixture_bridge, trace_packet):
        reasons.append(
            "nested fixture-only end-to-end smoke bridge and supplied runtime trace packet routes do not match"
        )
    if not _same_route(fixture_smoke, trace_smoke):
        reasons.append("nested supplied runtime end-to-end smokes do not match")
    if not _same_route(fixture_report, trace_report):
        reasons.append("nested supplied runtime dry-run reports do not match")
    if not _same_route(fixture_packet, trace_dry_run_packet) or not _same_route(
        fixture_bundle,
        trace_bundle,
    ):
        reasons.append("nested supplied runtime dry-run packets do not match")
    if not _same_route(fixture_evidence, trace_evidence) or not _same_route(
        fixture_evidence.supplied_market_contract,
        trace_evidence.supplied_market_contract,
    ):
        reasons.append("nested supplied evidence packets do not match")

    if record.fixture_end_to_end_smoke_bridge_summary != fixture_bridge.end_to_end_smoke_bridge_summary:
        reasons.append(
            "fixture end-to-end smoke bridge summary does not match fixture-only end-to-end smoke bridge"
        )
    if record.supplied_trace_summary != trace_packet.trace_summary:
        reasons.append("supplied trace summary does not match supplied runtime trace packet")
    if record.operator_review_summary != trace_packet.operator_review_summary:
        reasons.append("operator review summary does not match supplied runtime trace packet")
    if record.operator_review_summary != fixture_bridge.operator_review_summary:
        reasons.append("operator review summary does not match fixture-only end-to-end smoke bridge")

    if record.fixture_only_trace_bridge_status is not FixtureOnlyTraceBridgeStatus.FIXTURE_ONLY_TRACE_BRIDGE_RECORDED:
        reasons.append(f"fixture-only trace bridge status is {record.fixture_only_trace_bridge_status.value}")
    if record.fixture_only_trace_bridge_posture is not FixtureOnlyTraceBridgePosture.FIXTURE_ONLY_TRACE_BRIDGE_IN_MEMORY_ONLY:
        reasons.append(f"fixture-only trace bridge posture is {record.fixture_only_trace_bridge_posture.value}")
    if record.trace_bridge_alignment_status is not TraceBridgeAlignmentStatus.TRACE_BRIDGE_ALIGNED:
        reasons.append(f"trace bridge alignment status is {record.trace_bridge_alignment_status.value}")
    if record.no_lookahead_status is not NoLookaheadStatus.NO_LOOKAHEAD_RECORDED:
        reasons.append(f"no-lookahead status is {record.no_lookahead_status.value}")
    if record.operator_review_status is not OperatorReviewStatus.OPERATOR_REVIEW_REQUIRED:
        reasons.append(f"operator review status is {record.operator_review_status.value}")
    if record.runtime_gate_status is not RuntimeGateStatus.RUNTIME_GATE_READY:
        reasons.append(f"runtime gate status is {record.runtime_gate_status.value}")

    if reasons and not _is_nonblank_text(record.blocked_reason_summary):
        reasons.append("blocked_reason_summary is missing")

    if reasons:
        return FixtureOnlySourceProviderTraceBridgeValidationResult(
            severity=ValidationSeverity.BLOCKED,
            passed=False,
            reasons=tuple(reasons),
        )

    return FixtureOnlySourceProviderTraceBridgeValidationResult(
        severity=ValidationSeverity.PASSED,
        passed=True,
    )
