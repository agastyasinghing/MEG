"""Pure fixture-only Weather Bot Stage 2 source/provider operator-review acknowledgement bridge runtime scaffold.

This module consumes only caller-supplied fixture-only operator-review handoff
bridge and supplied runtime operator-review ack packet values. It is an in-memory
record only. It performs no live source fetching, no live provider clients, no
API calls, no scraping, no downloads, no SDK usage, no credentials/config
loading, no live ingestion, no evidence generation, no dry-run execution, no
simulation engine, no report generation, no smoke execution, no trace execution,
no handoff delivery, no acknowledgement delivery, no queue/service/scheduler/
broker behavior, no owner-decision capture, no operator decision execution, no
persistence/export writing, no paper trading, no trading/execution, no autonomy,
and no production behavior.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping

from meg.weather.stage2.fixture_only_source_provider_operator_review_handoff_bridge_runtime import (
    FixtureOnlySourceProviderOperatorReviewHandoffBridgeRecord,
    fixture_only_source_provider_operator_review_handoff_bridge_record_from_mapping,
    validate_fixture_only_source_provider_operator_review_handoff_bridge_record,
)
from meg.weather.stage2.supplied_runtime_operator_review_ack_packet import (
    SuppliedRuntimeOperatorReviewAckPacketRecord,
    supplied_runtime_operator_review_ack_packet_record_from_mapping,
    validate_supplied_runtime_operator_review_ack_packet_record,
)


class _ClosedValue(str, Enum):
    """String enum base for closed, machine-checkable Stage 2 values."""

    @classmethod
    def values(cls) -> frozenset[str]:
        return frozenset(member.value for member in cls)


class FixtureOnlyOperatorReviewAckBridgeStatus(_ClosedValue):
    FIXTURE_ONLY_OPERATOR_REVIEW_ACK_BRIDGE_RECORDED = "fixture_only_operator_review_ack_bridge_recorded"
    FIXTURE_ONLY_OPERATOR_REVIEW_ACK_BRIDGE_MISSING = "fixture_only_operator_review_ack_bridge_missing"
    FIXTURE_ONLY_OPERATOR_REVIEW_ACK_BRIDGE_AMBIGUOUS = "fixture_only_operator_review_ack_bridge_ambiguous"
    FIXTURE_ONLY_OPERATOR_REVIEW_ACK_BRIDGE_UNSUPPORTED = "fixture_only_operator_review_ack_bridge_unsupported"
    FIXTURE_ONLY_OPERATOR_REVIEW_ACK_BRIDGE_UNKNOWN = "fixture_only_operator_review_ack_bridge_unknown"


class FixtureOnlyOperatorReviewAckBridgePosture(_ClosedValue):
    FIXTURE_ONLY_OPERATOR_REVIEW_ACK_BRIDGE_IN_MEMORY_ONLY = "fixture_only_operator_review_ack_bridge_in_memory_only"
    FIXTURE_ONLY_OPERATOR_REVIEW_ACK_BRIDGE_MISSING = "fixture_only_operator_review_ack_bridge_missing"
    FIXTURE_ONLY_OPERATOR_REVIEW_ACK_BRIDGE_AMBIGUOUS = "fixture_only_operator_review_ack_bridge_ambiguous"
    FIXTURE_ONLY_OPERATOR_REVIEW_ACK_BRIDGE_UNSUPPORTED = "fixture_only_operator_review_ack_bridge_unsupported"
    FIXTURE_ONLY_OPERATOR_REVIEW_ACK_BRIDGE_UNKNOWN = "fixture_only_operator_review_ack_bridge_unknown"


class OperatorReviewAckBridgeAlignmentStatus(_ClosedValue):
    OPERATOR_REVIEW_ACK_BRIDGE_ALIGNED = "operator_review_ack_bridge_aligned"
    OPERATOR_REVIEW_ACK_BRIDGE_MISMATCH = "operator_review_ack_bridge_mismatch"
    OPERATOR_REVIEW_ACK_BRIDGE_MISSING = "operator_review_ack_bridge_missing"
    OPERATOR_REVIEW_ACK_BRIDGE_AMBIGUOUS = "operator_review_ack_bridge_ambiguous"
    OPERATOR_REVIEW_ACK_BRIDGE_UNKNOWN = "operator_review_ack_bridge_unknown"


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
class FixtureOnlySourceProviderOperatorReviewAckBridgeRecord:
    condition_id: str
    token_id: str
    outcome: str
    fixture_only_source_provider_operator_review_handoff_bridge: FixtureOnlySourceProviderOperatorReviewHandoffBridgeRecord
    supplied_runtime_operator_review_ack_packet: SuppliedRuntimeOperatorReviewAckPacketRecord
    operator_review_ack_bridge_id: str
    operator_review_ack_bridge_summary: str
    fixture_handoff_bridge_summary: str
    supplied_ack_summary: str
    operator_review_summary: str
    blocked_reason_summary: str
    fixture_only_operator_review_ack_bridge_status: FixtureOnlyOperatorReviewAckBridgeStatus
    fixture_only_operator_review_ack_bridge_posture: FixtureOnlyOperatorReviewAckBridgePosture
    operator_review_ack_bridge_alignment_status: OperatorReviewAckBridgeAlignmentStatus
    no_lookahead_status: NoLookaheadStatus
    operator_review_status: OperatorReviewStatus
    runtime_gate_status: RuntimeGateStatus
    provenance_notes: str = ""


@dataclass(frozen=True)
class FixtureOnlySourceProviderOperatorReviewAckBridgeValidationResult:
    severity: ValidationSeverity
    passed: bool
    reasons: tuple[str, ...] = ()


def _enum_value(enum_type: type[_ClosedValue], value: _ClosedValue | str) -> _ClosedValue:
    if isinstance(value, enum_type):
        return value
    return enum_type(value)


def _is_nonblank_text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _fixture_only_source_provider_operator_review_handoff_bridge_from_value(
    value: FixtureOnlySourceProviderOperatorReviewHandoffBridgeRecord | Mapping[str, Any],
) -> FixtureOnlySourceProviderOperatorReviewHandoffBridgeRecord:
    if isinstance(value, FixtureOnlySourceProviderOperatorReviewHandoffBridgeRecord):
        return value
    return fixture_only_source_provider_operator_review_handoff_bridge_record_from_mapping(value)


def _supplied_runtime_operator_review_ack_packet_from_value(
    value: SuppliedRuntimeOperatorReviewAckPacketRecord | Mapping[str, Any],
) -> SuppliedRuntimeOperatorReviewAckPacketRecord:
    if isinstance(value, SuppliedRuntimeOperatorReviewAckPacketRecord):
        return value
    return supplied_runtime_operator_review_ack_packet_record_from_mapping(value)


def fixture_only_source_provider_operator_review_ack_bridge_record_from_mapping(
    mapping: Mapping[str, Any],
) -> FixtureOnlySourceProviderOperatorReviewAckBridgeRecord:
    """Build operator-review acknowledgement bridge metadata from supplied values."""

    return FixtureOnlySourceProviderOperatorReviewAckBridgeRecord(
        condition_id=mapping["condition_id"],
        token_id=mapping["token_id"],
        outcome=mapping["outcome"],
        fixture_only_source_provider_operator_review_handoff_bridge=(
            _fixture_only_source_provider_operator_review_handoff_bridge_from_value(
                mapping["fixture_only_source_provider_operator_review_handoff_bridge"]
            )
        ),
        supplied_runtime_operator_review_ack_packet=(
            _supplied_runtime_operator_review_ack_packet_from_value(
                mapping["supplied_runtime_operator_review_ack_packet"]
            )
        ),
        operator_review_ack_bridge_id=mapping["operator_review_ack_bridge_id"],
        operator_review_ack_bridge_summary=mapping["operator_review_ack_bridge_summary"],
        fixture_handoff_bridge_summary=mapping["fixture_handoff_bridge_summary"],
        supplied_ack_summary=mapping["supplied_ack_summary"],
        operator_review_summary=mapping["operator_review_summary"],
        blocked_reason_summary=mapping["blocked_reason_summary"],
        fixture_only_operator_review_ack_bridge_status=_enum_value(
            FixtureOnlyOperatorReviewAckBridgeStatus,
            mapping["fixture_only_operator_review_ack_bridge_status"],
        ),
        fixture_only_operator_review_ack_bridge_posture=_enum_value(
            FixtureOnlyOperatorReviewAckBridgePosture,
            mapping["fixture_only_operator_review_ack_bridge_posture"],
        ),
        operator_review_ack_bridge_alignment_status=_enum_value(
            OperatorReviewAckBridgeAlignmentStatus,
            mapping["operator_review_ack_bridge_alignment_status"],
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


def validate_fixture_only_source_provider_operator_review_ack_bridge_record(
    record: FixtureOnlySourceProviderOperatorReviewAckBridgeRecord,
) -> FixtureOnlySourceProviderOperatorReviewAckBridgeValidationResult:
    """Validate fixture-only operator-review acknowledgement bridge metadata fail-closed."""

    reasons: list[str] = []

    for field_name, value in (
        ("condition_id", record.condition_id),
        ("token_id", record.token_id),
        ("outcome", record.outcome),
        ("operator_review_ack_bridge_id", record.operator_review_ack_bridge_id),
        ("operator_review_ack_bridge_summary", record.operator_review_ack_bridge_summary),
        ("fixture_handoff_bridge_summary", record.fixture_handoff_bridge_summary),
        ("supplied_ack_summary", record.supplied_ack_summary),
        ("operator_review_summary", record.operator_review_summary),
    ):
        if not _is_nonblank_text(value):
            reasons.append(f"{field_name} is missing")

    handoff_bridge = record.fixture_only_source_provider_operator_review_handoff_bridge
    ack_packet = record.supplied_runtime_operator_review_ack_packet
    bridge_handoff = handoff_bridge.supplied_runtime_operator_review_handoff
    ack_handoff = ack_packet.supplied_runtime_operator_review_handoff
    bridge_trace = bridge_handoff.supplied_runtime_trace_packet
    ack_trace = ack_handoff.supplied_runtime_trace_packet
    bridge_smoke = bridge_trace.supplied_runtime_end_to_end_smoke
    ack_smoke = ack_trace.supplied_runtime_end_to_end_smoke
    bridge_report = bridge_smoke.supplied_runtime_dry_run_report
    ack_report = ack_smoke.supplied_runtime_dry_run_report
    bridge_dry_run = bridge_report.supplied_runtime_dry_run_packet
    ack_dry_run = ack_report.supplied_runtime_dry_run_packet
    bridge_bundle = bridge_dry_run.supplied_runtime_validation_bundle
    ack_bundle = ack_dry_run.supplied_runtime_validation_bundle
    bridge_evidence = bridge_bundle.supplied_evidence_packet
    ack_evidence = ack_bundle.supplied_evidence_packet

    if not validate_fixture_only_source_provider_operator_review_handoff_bridge_record(handoff_bridge).passed:
        reasons.append("fixture-only source provider operator-review handoff bridge is invalid")
    if not validate_supplied_runtime_operator_review_ack_packet_record(ack_packet).passed:
        reasons.append("supplied runtime operator-review ack packet is invalid")

    if record.condition_id != handoff_bridge.condition_id:
        reasons.append("condition_id does not match fixture-only operator-review handoff bridge")
    if record.token_id != handoff_bridge.token_id:
        reasons.append("token_id does not match fixture-only operator-review handoff bridge")
    if record.outcome != handoff_bridge.outcome:
        reasons.append("outcome does not match fixture-only operator-review handoff bridge")

    if record.condition_id != ack_packet.condition_id:
        reasons.append("condition_id does not match supplied runtime operator-review ack packet")
    if record.token_id != ack_packet.token_id:
        reasons.append("token_id does not match supplied runtime operator-review ack packet")
    if record.outcome != ack_packet.outcome:
        reasons.append("outcome does not match supplied runtime operator-review ack packet")

    if not _same_route(handoff_bridge, ack_packet):
        reasons.append(
            "nested fixture-only operator-review handoff bridge and supplied runtime operator-review ack packet routes do not match"
        )
    if not _same_route(bridge_handoff, ack_handoff):
        reasons.append("nested supplied runtime operator-review handoffs do not match")
    if not _same_route(bridge_trace, ack_trace):
        reasons.append("nested supplied runtime trace packets do not match")
    if not _same_route(bridge_smoke, ack_smoke):
        reasons.append("nested supplied runtime end-to-end smokes do not match")
    if not _same_route(bridge_report, ack_report):
        reasons.append("nested supplied runtime dry-run reports do not match")
    if not _same_route(bridge_dry_run, ack_dry_run) or not _same_route(bridge_bundle, ack_bundle):
        reasons.append("nested supplied runtime dry-run packets do not match")
    if not _same_route(bridge_evidence, ack_evidence) or not _same_route(
        bridge_evidence.supplied_market_contract,
        ack_evidence.supplied_market_contract,
    ):
        reasons.append("nested supplied evidence packets do not match")

    if record.fixture_handoff_bridge_summary != handoff_bridge.operator_review_handoff_bridge_summary:
        reasons.append("fixture handoff bridge summary does not match fixture-only operator-review handoff bridge")
    if record.supplied_ack_summary != ack_packet.ack_summary:
        reasons.append("supplied ack summary does not match supplied runtime operator-review ack packet")
    if record.operator_review_summary != ack_packet.operator_review_summary:
        reasons.append("operator review summary does not match supplied runtime operator-review ack packet")
    if record.operator_review_summary != handoff_bridge.operator_review_summary:
        reasons.append("operator review summary does not match fixture-only operator-review handoff bridge")

    if record.fixture_only_operator_review_ack_bridge_status is not FixtureOnlyOperatorReviewAckBridgeStatus.FIXTURE_ONLY_OPERATOR_REVIEW_ACK_BRIDGE_RECORDED:
        reasons.append(
            "fixture-only operator-review ack bridge status is "
            f"{record.fixture_only_operator_review_ack_bridge_status.value}"
        )
    if record.fixture_only_operator_review_ack_bridge_posture is not FixtureOnlyOperatorReviewAckBridgePosture.FIXTURE_ONLY_OPERATOR_REVIEW_ACK_BRIDGE_IN_MEMORY_ONLY:
        reasons.append(
            "fixture-only operator-review ack bridge posture is "
            f"{record.fixture_only_operator_review_ack_bridge_posture.value}"
        )
    if record.operator_review_ack_bridge_alignment_status is not OperatorReviewAckBridgeAlignmentStatus.OPERATOR_REVIEW_ACK_BRIDGE_ALIGNED:
        reasons.append(
            "operator-review ack bridge alignment status is "
            f"{record.operator_review_ack_bridge_alignment_status.value}"
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
        return FixtureOnlySourceProviderOperatorReviewAckBridgeValidationResult(
            severity=ValidationSeverity.BLOCKED,
            passed=False,
            reasons=tuple(reasons),
        )

    return FixtureOnlySourceProviderOperatorReviewAckBridgeValidationResult(
        severity=ValidationSeverity.PASSED,
        passed=True,
    )
