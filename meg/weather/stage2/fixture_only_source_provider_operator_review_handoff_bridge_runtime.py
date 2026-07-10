"""Pure fixture-only Weather Bot Stage 2 source/provider operator-review handoff bridge runtime scaffold.

This module consumes only caller-supplied fixture-only trace bridge and supplied
runtime operator-review handoff values. It is an in-memory record only. It
performs no live source fetching, no live provider clients, no API calls, no
scraping, no downloads, no SDK usage, no credentials/config loading, no live
ingestion, no evidence generation, no dry-run execution, no simulation engine,
no report generation, no smoke execution, no trace execution, no handoff
delivery, no queue/service/scheduler/broker behavior, no owner-decision capture,
no operator decision execution, no persistence/export writing, no paper trading,
no trading/execution, no autonomy, and no production behavior.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping

from meg.weather.stage2.fixture_only_source_provider_trace_bridge_runtime import (
    FixtureOnlySourceProviderTraceBridgeRecord,
    fixture_only_source_provider_trace_bridge_record_from_mapping,
    validate_fixture_only_source_provider_trace_bridge_record,
)
from meg.weather.stage2.supplied_runtime_operator_review_handoff import (
    SuppliedRuntimeOperatorReviewHandoffRecord,
    supplied_runtime_operator_review_handoff_record_from_mapping,
    validate_supplied_runtime_operator_review_handoff_record,
)


class _ClosedValue(str, Enum):
    """String enum base for closed, machine-checkable Stage 2 values."""

    @classmethod
    def values(cls) -> frozenset[str]:
        return frozenset(member.value for member in cls)


class FixtureOnlyOperatorReviewHandoffBridgeStatus(_ClosedValue):
    FIXTURE_ONLY_OPERATOR_REVIEW_HANDOFF_BRIDGE_RECORDED = "fixture_only_operator_review_handoff_bridge_recorded"
    FIXTURE_ONLY_OPERATOR_REVIEW_HANDOFF_BRIDGE_MISSING = "fixture_only_operator_review_handoff_bridge_missing"
    FIXTURE_ONLY_OPERATOR_REVIEW_HANDOFF_BRIDGE_AMBIGUOUS = "fixture_only_operator_review_handoff_bridge_ambiguous"
    FIXTURE_ONLY_OPERATOR_REVIEW_HANDOFF_BRIDGE_UNSUPPORTED = "fixture_only_operator_review_handoff_bridge_unsupported"
    FIXTURE_ONLY_OPERATOR_REVIEW_HANDOFF_BRIDGE_UNKNOWN = "fixture_only_operator_review_handoff_bridge_unknown"


class FixtureOnlyOperatorReviewHandoffBridgePosture(_ClosedValue):
    FIXTURE_ONLY_OPERATOR_REVIEW_HANDOFF_BRIDGE_IN_MEMORY_ONLY = "fixture_only_operator_review_handoff_bridge_in_memory_only"
    FIXTURE_ONLY_OPERATOR_REVIEW_HANDOFF_BRIDGE_MISSING = "fixture_only_operator_review_handoff_bridge_missing"
    FIXTURE_ONLY_OPERATOR_REVIEW_HANDOFF_BRIDGE_AMBIGUOUS = "fixture_only_operator_review_handoff_bridge_ambiguous"
    FIXTURE_ONLY_OPERATOR_REVIEW_HANDOFF_BRIDGE_UNSUPPORTED = "fixture_only_operator_review_handoff_bridge_unsupported"
    FIXTURE_ONLY_OPERATOR_REVIEW_HANDOFF_BRIDGE_UNKNOWN = "fixture_only_operator_review_handoff_bridge_unknown"


class OperatorReviewHandoffBridgeAlignmentStatus(_ClosedValue):
    OPERATOR_REVIEW_HANDOFF_BRIDGE_ALIGNED = "operator_review_handoff_bridge_aligned"
    OPERATOR_REVIEW_HANDOFF_BRIDGE_MISMATCH = "operator_review_handoff_bridge_mismatch"
    OPERATOR_REVIEW_HANDOFF_BRIDGE_MISSING = "operator_review_handoff_bridge_missing"
    OPERATOR_REVIEW_HANDOFF_BRIDGE_AMBIGUOUS = "operator_review_handoff_bridge_ambiguous"
    OPERATOR_REVIEW_HANDOFF_BRIDGE_UNKNOWN = "operator_review_handoff_bridge_unknown"


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
class FixtureOnlySourceProviderOperatorReviewHandoffBridgeRecord:
    condition_id: str
    token_id: str
    outcome: str
    fixture_only_source_provider_trace_bridge: FixtureOnlySourceProviderTraceBridgeRecord
    supplied_runtime_operator_review_handoff: SuppliedRuntimeOperatorReviewHandoffRecord
    operator_review_handoff_bridge_id: str
    operator_review_handoff_bridge_summary: str
    fixture_trace_bridge_summary: str
    supplied_handoff_summary: str
    operator_review_summary: str
    blocked_reason_summary: str
    fixture_only_operator_review_handoff_bridge_status: FixtureOnlyOperatorReviewHandoffBridgeStatus
    fixture_only_operator_review_handoff_bridge_posture: FixtureOnlyOperatorReviewHandoffBridgePosture
    operator_review_handoff_bridge_alignment_status: OperatorReviewHandoffBridgeAlignmentStatus
    no_lookahead_status: NoLookaheadStatus
    operator_review_status: OperatorReviewStatus
    runtime_gate_status: RuntimeGateStatus
    provenance_notes: str = ""


@dataclass(frozen=True)
class FixtureOnlySourceProviderOperatorReviewHandoffBridgeValidationResult:
    severity: ValidationSeverity
    passed: bool
    reasons: tuple[str, ...] = ()


def _enum_value(enum_type: type[_ClosedValue], value: _ClosedValue | str) -> _ClosedValue:
    if isinstance(value, enum_type):
        return value
    return enum_type(value)


def _is_nonblank_text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _fixture_only_source_provider_trace_bridge_from_value(
    value: FixtureOnlySourceProviderTraceBridgeRecord | Mapping[str, Any],
) -> FixtureOnlySourceProviderTraceBridgeRecord:
    if isinstance(value, FixtureOnlySourceProviderTraceBridgeRecord):
        return value
    return fixture_only_source_provider_trace_bridge_record_from_mapping(value)


def _supplied_runtime_operator_review_handoff_from_value(
    value: SuppliedRuntimeOperatorReviewHandoffRecord | Mapping[str, Any],
) -> SuppliedRuntimeOperatorReviewHandoffRecord:
    if isinstance(value, SuppliedRuntimeOperatorReviewHandoffRecord):
        return value
    return supplied_runtime_operator_review_handoff_record_from_mapping(value)


def fixture_only_source_provider_operator_review_handoff_bridge_record_from_mapping(
    mapping: Mapping[str, Any],
) -> FixtureOnlySourceProviderOperatorReviewHandoffBridgeRecord:
    """Build operator-review handoff bridge metadata from explicitly supplied values."""

    return FixtureOnlySourceProviderOperatorReviewHandoffBridgeRecord(
        condition_id=mapping["condition_id"],
        token_id=mapping["token_id"],
        outcome=mapping["outcome"],
        fixture_only_source_provider_trace_bridge=(
            _fixture_only_source_provider_trace_bridge_from_value(
                mapping["fixture_only_source_provider_trace_bridge"]
            )
        ),
        supplied_runtime_operator_review_handoff=(
            _supplied_runtime_operator_review_handoff_from_value(
                mapping["supplied_runtime_operator_review_handoff"]
            )
        ),
        operator_review_handoff_bridge_id=mapping["operator_review_handoff_bridge_id"],
        operator_review_handoff_bridge_summary=mapping["operator_review_handoff_bridge_summary"],
        fixture_trace_bridge_summary=mapping["fixture_trace_bridge_summary"],
        supplied_handoff_summary=mapping["supplied_handoff_summary"],
        operator_review_summary=mapping["operator_review_summary"],
        blocked_reason_summary=mapping["blocked_reason_summary"],
        fixture_only_operator_review_handoff_bridge_status=_enum_value(
            FixtureOnlyOperatorReviewHandoffBridgeStatus,
            mapping["fixture_only_operator_review_handoff_bridge_status"],
        ),
        fixture_only_operator_review_handoff_bridge_posture=_enum_value(
            FixtureOnlyOperatorReviewHandoffBridgePosture,
            mapping["fixture_only_operator_review_handoff_bridge_posture"],
        ),
        operator_review_handoff_bridge_alignment_status=_enum_value(
            OperatorReviewHandoffBridgeAlignmentStatus,
            mapping["operator_review_handoff_bridge_alignment_status"],
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


def validate_fixture_only_source_provider_operator_review_handoff_bridge_record(
    record: FixtureOnlySourceProviderOperatorReviewHandoffBridgeRecord,
) -> FixtureOnlySourceProviderOperatorReviewHandoffBridgeValidationResult:
    """Validate fixture-only operator-review handoff bridge metadata fail-closed."""

    reasons: list[str] = []

    for field_name, value in (
        ("condition_id", record.condition_id),
        ("token_id", record.token_id),
        ("outcome", record.outcome),
        ("operator_review_handoff_bridge_id", record.operator_review_handoff_bridge_id),
        ("operator_review_handoff_bridge_summary", record.operator_review_handoff_bridge_summary),
        ("fixture_trace_bridge_summary", record.fixture_trace_bridge_summary),
        ("supplied_handoff_summary", record.supplied_handoff_summary),
        ("operator_review_summary", record.operator_review_summary),
    ):
        if not _is_nonblank_text(value):
            reasons.append(f"{field_name} is missing")

    trace_bridge = record.fixture_only_source_provider_trace_bridge
    handoff = record.supplied_runtime_operator_review_handoff
    trace_packet = trace_bridge.supplied_runtime_trace_packet
    handoff_trace_packet = handoff.supplied_runtime_trace_packet
    trace_smoke = trace_packet.supplied_runtime_end_to_end_smoke
    handoff_smoke = handoff_trace_packet.supplied_runtime_end_to_end_smoke
    trace_report = trace_smoke.supplied_runtime_dry_run_report
    handoff_report = handoff_smoke.supplied_runtime_dry_run_report
    trace_dry_run_packet = trace_report.supplied_runtime_dry_run_packet
    handoff_dry_run_packet = handoff_report.supplied_runtime_dry_run_packet
    trace_bundle = trace_dry_run_packet.supplied_runtime_validation_bundle
    handoff_bundle = handoff_dry_run_packet.supplied_runtime_validation_bundle
    trace_evidence = trace_bundle.supplied_evidence_packet
    handoff_evidence = handoff_bundle.supplied_evidence_packet

    if not validate_fixture_only_source_provider_trace_bridge_record(trace_bridge).passed:
        reasons.append("fixture-only source provider trace bridge is invalid")
    if not validate_supplied_runtime_operator_review_handoff_record(handoff).passed:
        reasons.append("supplied runtime operator-review handoff is invalid")

    if record.condition_id != trace_bridge.condition_id:
        reasons.append("condition_id does not match fixture-only trace bridge")
    if record.token_id != trace_bridge.token_id:
        reasons.append("token_id does not match fixture-only trace bridge")
    if record.outcome != trace_bridge.outcome:
        reasons.append("outcome does not match fixture-only trace bridge")

    if record.condition_id != handoff.condition_id:
        reasons.append("condition_id does not match supplied runtime operator-review handoff")
    if record.token_id != handoff.token_id:
        reasons.append("token_id does not match supplied runtime operator-review handoff")
    if record.outcome != handoff.outcome:
        reasons.append("outcome does not match supplied runtime operator-review handoff")

    if not _same_route(trace_bridge, handoff):
        reasons.append(
            "nested fixture-only trace bridge and supplied runtime operator-review handoff routes do not match"
        )
    if not _same_route(trace_packet, handoff_trace_packet):
        reasons.append("nested supplied runtime trace packets do not match")
    if not _same_route(trace_smoke, handoff_smoke):
        reasons.append("nested supplied runtime end-to-end smokes do not match")
    if not _same_route(trace_report, handoff_report):
        reasons.append("nested supplied runtime dry-run reports do not match")
    if not _same_route(trace_dry_run_packet, handoff_dry_run_packet) or not _same_route(
        trace_bundle,
        handoff_bundle,
    ):
        reasons.append("nested supplied runtime dry-run packets do not match")
    if not _same_route(trace_evidence, handoff_evidence) or not _same_route(
        trace_evidence.supplied_market_contract,
        handoff_evidence.supplied_market_contract,
    ):
        reasons.append("nested supplied evidence packets do not match")

    if record.fixture_trace_bridge_summary != trace_bridge.trace_bridge_summary:
        reasons.append("fixture trace bridge summary does not match fixture-only trace bridge")
    if record.supplied_handoff_summary != handoff.handoff_summary:
        reasons.append("supplied handoff summary does not match supplied runtime operator-review handoff")
    if record.operator_review_summary != handoff.operator_review_summary:
        reasons.append("operator review summary does not match supplied runtime operator-review handoff")
    if record.operator_review_summary != trace_bridge.operator_review_summary:
        reasons.append("operator review summary does not match fixture-only trace bridge")

    if record.fixture_only_operator_review_handoff_bridge_status is not FixtureOnlyOperatorReviewHandoffBridgeStatus.FIXTURE_ONLY_OPERATOR_REVIEW_HANDOFF_BRIDGE_RECORDED:
        reasons.append(
            "fixture-only operator-review handoff bridge status is "
            f"{record.fixture_only_operator_review_handoff_bridge_status.value}"
        )
    if record.fixture_only_operator_review_handoff_bridge_posture is not FixtureOnlyOperatorReviewHandoffBridgePosture.FIXTURE_ONLY_OPERATOR_REVIEW_HANDOFF_BRIDGE_IN_MEMORY_ONLY:
        reasons.append(
            "fixture-only operator-review handoff bridge posture is "
            f"{record.fixture_only_operator_review_handoff_bridge_posture.value}"
        )
    if record.operator_review_handoff_bridge_alignment_status is not OperatorReviewHandoffBridgeAlignmentStatus.OPERATOR_REVIEW_HANDOFF_BRIDGE_ALIGNED:
        reasons.append(
            "operator-review handoff bridge alignment status is "
            f"{record.operator_review_handoff_bridge_alignment_status.value}"
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
        return FixtureOnlySourceProviderOperatorReviewHandoffBridgeValidationResult(
            severity=ValidationSeverity.BLOCKED,
            passed=False,
            reasons=tuple(reasons),
        )

    return FixtureOnlySourceProviderOperatorReviewHandoffBridgeValidationResult(
        severity=ValidationSeverity.PASSED,
        passed=True,
    )
