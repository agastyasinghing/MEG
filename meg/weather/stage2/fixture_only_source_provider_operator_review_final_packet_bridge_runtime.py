"""Pure fixture-only Weather Bot Stage 2 source/provider operator-review final-packet bridge runtime scaffold.

This module consumes only caller-supplied fixture-only queue-summary bridge and
supplied final-packet values. It is an in-memory record only. It performs no
live providers or fetching, no API calls, scraping, downloads, SDKs,
credentials, or live ingestion, no evidence generation or mutation, no scoring
or backtesting, no dry-run execution, simulation, report generation, smoke
execution, or trace execution, no handoff, acknowledgement, queue-packet,
queue-entry, queue-summary, or final-packet delivery, no generated-packet or
generated-summary behavior, no real queue service, no enqueue/dequeue/
publish/subscribe behavior, no scheduler or broker, no persistence or export
writing, no owner-decision capture, no operator-decision execution, and no
paper trading, trading, autonomy, or production behavior.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping

from meg.weather.stage2.fixture_only_source_provider_operator_review_queue_summary_bridge_runtime import (
    FixtureOnlySourceProviderOperatorReviewQueueSummaryBridgeRecord,
    fixture_only_source_provider_operator_review_queue_summary_bridge_record_from_mapping,
    validate_fixture_only_source_provider_operator_review_queue_summary_bridge_record,
)
from meg.weather.stage2.supplied_runtime_operator_review_final_packet import (
    SuppliedRuntimeOperatorReviewFinalPacketRecord,
    supplied_runtime_operator_review_final_packet_record_from_mapping,
    validate_supplied_runtime_operator_review_final_packet_record,
)


class _ClosedValue(str, Enum):
    """String enum base for closed, machine-checkable Stage 2 values."""

    @classmethod
    def values(cls) -> frozenset[str]:
        return frozenset(member.value for member in cls)


class FixtureOnlyOperatorReviewFinalPacketBridgeStatus(_ClosedValue):
    FIXTURE_ONLY_OPERATOR_REVIEW_FINAL_PACKET_BRIDGE_RECORDED = "fixture_only_operator_review_final_packet_bridge_recorded"
    FIXTURE_ONLY_OPERATOR_REVIEW_FINAL_PACKET_BRIDGE_MISSING = "fixture_only_operator_review_final_packet_bridge_missing"
    FIXTURE_ONLY_OPERATOR_REVIEW_FINAL_PACKET_BRIDGE_AMBIGUOUS = "fixture_only_operator_review_final_packet_bridge_ambiguous"
    FIXTURE_ONLY_OPERATOR_REVIEW_FINAL_PACKET_BRIDGE_UNSUPPORTED = "fixture_only_operator_review_final_packet_bridge_unsupported"
    FIXTURE_ONLY_OPERATOR_REVIEW_FINAL_PACKET_BRIDGE_UNKNOWN = "fixture_only_operator_review_final_packet_bridge_unknown"


class FixtureOnlyOperatorReviewFinalPacketBridgePosture(_ClosedValue):
    FIXTURE_ONLY_OPERATOR_REVIEW_FINAL_PACKET_BRIDGE_IN_MEMORY_ONLY = "fixture_only_operator_review_final_packet_bridge_in_memory_only"
    FIXTURE_ONLY_OPERATOR_REVIEW_FINAL_PACKET_BRIDGE_MISSING = "fixture_only_operator_review_final_packet_bridge_missing"
    FIXTURE_ONLY_OPERATOR_REVIEW_FINAL_PACKET_BRIDGE_AMBIGUOUS = "fixture_only_operator_review_final_packet_bridge_ambiguous"
    FIXTURE_ONLY_OPERATOR_REVIEW_FINAL_PACKET_BRIDGE_UNSUPPORTED = "fixture_only_operator_review_final_packet_bridge_unsupported"
    FIXTURE_ONLY_OPERATOR_REVIEW_FINAL_PACKET_BRIDGE_UNKNOWN = "fixture_only_operator_review_final_packet_bridge_unknown"


class OperatorReviewFinalPacketBridgeAlignmentStatus(_ClosedValue):
    OPERATOR_REVIEW_FINAL_PACKET_BRIDGE_ALIGNED = "operator_review_final_packet_bridge_aligned"
    OPERATOR_REVIEW_FINAL_PACKET_BRIDGE_MISMATCH = "operator_review_final_packet_bridge_mismatch"
    OPERATOR_REVIEW_FINAL_PACKET_BRIDGE_MISSING = "operator_review_final_packet_bridge_missing"
    OPERATOR_REVIEW_FINAL_PACKET_BRIDGE_AMBIGUOUS = "operator_review_final_packet_bridge_ambiguous"
    OPERATOR_REVIEW_FINAL_PACKET_BRIDGE_UNKNOWN = "operator_review_final_packet_bridge_unknown"


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
class FixtureOnlySourceProviderOperatorReviewFinalPacketBridgeRecord:
    condition_id: str
    token_id: str
    outcome: str
    fixture_only_source_provider_operator_review_queue_summary_bridge: FixtureOnlySourceProviderOperatorReviewQueueSummaryBridgeRecord
    supplied_runtime_operator_review_final_packet: SuppliedRuntimeOperatorReviewFinalPacketRecord
    operator_review_final_packet_bridge_id: str
    operator_review_final_packet_bridge_summary: str
    fixture_queue_summary_bridge_summary: str
    supplied_final_packet_summary: str
    operator_review_summary: str
    blocked_reason_summary: str
    fixture_only_operator_review_final_packet_bridge_status: FixtureOnlyOperatorReviewFinalPacketBridgeStatus
    fixture_only_operator_review_final_packet_bridge_posture: FixtureOnlyOperatorReviewFinalPacketBridgePosture
    operator_review_final_packet_bridge_alignment_status: OperatorReviewFinalPacketBridgeAlignmentStatus
    no_lookahead_status: NoLookaheadStatus
    operator_review_status: OperatorReviewStatus
    runtime_gate_status: RuntimeGateStatus
    provenance_notes: str = ""


@dataclass(frozen=True)
class FixtureOnlySourceProviderOperatorReviewFinalPacketBridgeValidationResult:
    severity: ValidationSeverity
    passed: bool
    reasons: tuple[str, ...] = ()


def _enum_value(enum_type: type[_ClosedValue], value: _ClosedValue | str) -> _ClosedValue:
    if isinstance(value, enum_type):
        return value
    return enum_type(value)


def _is_nonblank_text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _same_route(left: object, right: object) -> bool:
    return (
        getattr(left, "condition_id") == getattr(right, "condition_id")
        and getattr(left, "token_id") == getattr(right, "token_id")
        and getattr(left, "outcome") == getattr(right, "outcome")
    )


def _fixture_only_source_provider_operator_review_queue_summary_bridge_from_value(
    value: FixtureOnlySourceProviderOperatorReviewQueueSummaryBridgeRecord | Mapping[str, Any],
) -> FixtureOnlySourceProviderOperatorReviewQueueSummaryBridgeRecord:
    if isinstance(value, FixtureOnlySourceProviderOperatorReviewQueueSummaryBridgeRecord):
        return value
    return fixture_only_source_provider_operator_review_queue_summary_bridge_record_from_mapping(value)


def _supplied_runtime_operator_review_final_packet_from_value(
    value: SuppliedRuntimeOperatorReviewFinalPacketRecord | Mapping[str, Any],
) -> SuppliedRuntimeOperatorReviewFinalPacketRecord:
    if isinstance(value, SuppliedRuntimeOperatorReviewFinalPacketRecord):
        return value
    return supplied_runtime_operator_review_final_packet_record_from_mapping(value)


def fixture_only_source_provider_operator_review_final_packet_bridge_record_from_mapping(
    mapping: Mapping[str, Any],
) -> FixtureOnlySourceProviderOperatorReviewFinalPacketBridgeRecord:
    """Build operator-review final-packet bridge metadata from supplied values."""

    return FixtureOnlySourceProviderOperatorReviewFinalPacketBridgeRecord(
        condition_id=mapping["condition_id"],
        token_id=mapping["token_id"],
        outcome=mapping["outcome"],
        fixture_only_source_provider_operator_review_queue_summary_bridge=(
            _fixture_only_source_provider_operator_review_queue_summary_bridge_from_value(
                mapping["fixture_only_source_provider_operator_review_queue_summary_bridge"]
            )
        ),
        supplied_runtime_operator_review_final_packet=(
            _supplied_runtime_operator_review_final_packet_from_value(
                mapping["supplied_runtime_operator_review_final_packet"]
            )
        ),
        operator_review_final_packet_bridge_id=mapping["operator_review_final_packet_bridge_id"],
        operator_review_final_packet_bridge_summary=mapping[
            "operator_review_final_packet_bridge_summary"
        ],
        fixture_queue_summary_bridge_summary=mapping["fixture_queue_summary_bridge_summary"],
        supplied_final_packet_summary=mapping["supplied_final_packet_summary"],
        operator_review_summary=mapping["operator_review_summary"],
        blocked_reason_summary=mapping["blocked_reason_summary"],
        fixture_only_operator_review_final_packet_bridge_status=_enum_value(
            FixtureOnlyOperatorReviewFinalPacketBridgeStatus,
            mapping["fixture_only_operator_review_final_packet_bridge_status"],
        ),
        fixture_only_operator_review_final_packet_bridge_posture=_enum_value(
            FixtureOnlyOperatorReviewFinalPacketBridgePosture,
            mapping["fixture_only_operator_review_final_packet_bridge_posture"],
        ),
        operator_review_final_packet_bridge_alignment_status=_enum_value(
            OperatorReviewFinalPacketBridgeAlignmentStatus,
            mapping["operator_review_final_packet_bridge_alignment_status"],
        ),
        no_lookahead_status=_enum_value(NoLookaheadStatus, mapping["no_lookahead_status"]),
        operator_review_status=_enum_value(OperatorReviewStatus, mapping["operator_review_status"]),
        runtime_gate_status=_enum_value(RuntimeGateStatus, mapping["runtime_gate_status"]),
        provenance_notes=str(mapping.get("provenance_notes", "")),
    )


def validate_fixture_only_source_provider_operator_review_final_packet_bridge_record(
    record: FixtureOnlySourceProviderOperatorReviewFinalPacketBridgeRecord,
) -> FixtureOnlySourceProviderOperatorReviewFinalPacketBridgeValidationResult:
    """Validate fixture-only operator-review final-packet bridge metadata fail-closed."""

    reasons: list[str] = []

    for field_name, value in (
        ("condition_id", record.condition_id),
        ("token_id", record.token_id),
        ("outcome", record.outcome),
        ("operator_review_final_packet_bridge_id", record.operator_review_final_packet_bridge_id),
        ("operator_review_final_packet_bridge_summary", record.operator_review_final_packet_bridge_summary),
        ("fixture_queue_summary_bridge_summary", record.fixture_queue_summary_bridge_summary),
        ("supplied_final_packet_summary", record.supplied_final_packet_summary),
        ("operator_review_summary", record.operator_review_summary),
    ):
        if not _is_nonblank_text(value):
            reasons.append(f"{field_name} is missing")

    summary_bridge = record.fixture_only_source_provider_operator_review_queue_summary_bridge
    final_packet = record.supplied_runtime_operator_review_final_packet
    bridge_summary = summary_bridge.supplied_runtime_operator_review_queue_summary
    final_summary = final_packet.supplied_runtime_operator_review_queue_summary
    bridge_entry = bridge_summary.supplied_runtime_operator_review_queue_entry
    final_entry = final_summary.supplied_runtime_operator_review_queue_entry
    bridge_packet = bridge_entry.supplied_runtime_operator_review_queue_packet
    final_packet_queue = final_entry.supplied_runtime_operator_review_queue_packet
    bridge_ack = bridge_packet.supplied_runtime_operator_review_ack_packet
    final_ack = final_packet_queue.supplied_runtime_operator_review_ack_packet
    bridge_handoff = bridge_ack.supplied_runtime_operator_review_handoff
    final_handoff = final_ack.supplied_runtime_operator_review_handoff
    bridge_trace = bridge_handoff.supplied_runtime_trace_packet
    final_trace = final_handoff.supplied_runtime_trace_packet
    bridge_smoke = bridge_trace.supplied_runtime_end_to_end_smoke
    final_smoke = final_trace.supplied_runtime_end_to_end_smoke
    bridge_report = bridge_smoke.supplied_runtime_dry_run_report
    final_report = final_smoke.supplied_runtime_dry_run_report
    bridge_dry = bridge_report.supplied_runtime_dry_run_packet
    final_dry = final_report.supplied_runtime_dry_run_packet
    bridge_bundle = bridge_dry.supplied_runtime_validation_bundle
    final_bundle = final_dry.supplied_runtime_validation_bundle
    bridge_evidence = bridge_bundle.supplied_evidence_packet
    final_evidence = final_bundle.supplied_evidence_packet

    if not validate_fixture_only_source_provider_operator_review_queue_summary_bridge_record(
        summary_bridge
    ).passed:
        reasons.append("fixture-only source provider operator-review queue-summary bridge is invalid")
    if not validate_supplied_runtime_operator_review_final_packet_record(final_packet).passed:
        reasons.append("supplied runtime operator-review final packet is invalid")

    if record.condition_id != summary_bridge.condition_id:
        reasons.append("condition_id does not match fixture-only operator-review queue-summary bridge")
    if record.token_id != summary_bridge.token_id:
        reasons.append("token_id does not match fixture-only operator-review queue-summary bridge")
    if record.outcome != summary_bridge.outcome:
        reasons.append("outcome does not match fixture-only operator-review queue-summary bridge")
    if record.condition_id != final_packet.condition_id:
        reasons.append("condition_id does not match supplied runtime operator-review final packet")
    if record.token_id != final_packet.token_id:
        reasons.append("token_id does not match supplied runtime operator-review final packet")
    if record.outcome != final_packet.outcome:
        reasons.append("outcome does not match supplied runtime operator-review final packet")

    if not _same_route(summary_bridge, final_packet):
        reasons.append(
            "nested fixture-only operator-review queue-summary bridge and supplied runtime operator-review final packet routes do not match"
        )
    if not _same_route(bridge_summary, final_summary):
        reasons.append("nested supplied runtime operator-review queue summaries do not match")
    if not _same_route(bridge_entry, final_entry):
        reasons.append("nested supplied runtime operator-review queue entries do not match")
    if not _same_route(bridge_packet, final_packet_queue):
        reasons.append("nested supplied runtime operator-review queue packets do not match")
    if not _same_route(bridge_ack, final_ack):
        reasons.append("nested supplied runtime operator-review ack packets do not match")
    if not _same_route(bridge_handoff, final_handoff):
        reasons.append("nested supplied runtime operator-review handoffs do not match")
    if not _same_route(bridge_trace, final_trace):
        reasons.append("nested supplied runtime trace packets do not match")
    if not _same_route(bridge_smoke, final_smoke):
        reasons.append("nested supplied runtime end-to-end smokes do not match")
    if not _same_route(bridge_report, final_report):
        reasons.append("nested supplied runtime dry-run reports do not match")
    if not _same_route(bridge_dry, final_dry) or not _same_route(bridge_bundle, final_bundle):
        reasons.append("nested supplied runtime dry-run packets do not match")
    if not _same_route(bridge_evidence, final_evidence) or not _same_route(
        bridge_evidence.supplied_market_contract,
        final_evidence.supplied_market_contract,
    ):
        reasons.append("nested supplied evidence packets do not match")

    if (
        record.fixture_queue_summary_bridge_summary
        != summary_bridge.operator_review_queue_summary_bridge_summary
    ):
        reasons.append(
            "fixture queue-summary bridge summary does not match fixture-only operator-review queue-summary bridge"
        )
    if record.supplied_final_packet_summary != final_packet.final_packet_summary:
        reasons.append("supplied final packet summary does not match supplied runtime operator-review final packet")
    if record.operator_review_summary != final_packet.operator_review_summary:
        reasons.append("operator review summary does not match supplied runtime operator-review final packet")
    if record.operator_review_summary != summary_bridge.operator_review_summary:
        reasons.append("operator review summary does not match fixture-only operator-review queue-summary bridge")

    if record.fixture_only_operator_review_final_packet_bridge_status is not FixtureOnlyOperatorReviewFinalPacketBridgeStatus.FIXTURE_ONLY_OPERATOR_REVIEW_FINAL_PACKET_BRIDGE_RECORDED:
        reasons.append(
            "fixture-only operator-review final-packet bridge status is "
            f"{record.fixture_only_operator_review_final_packet_bridge_status.value}"
        )
    if record.fixture_only_operator_review_final_packet_bridge_posture is not FixtureOnlyOperatorReviewFinalPacketBridgePosture.FIXTURE_ONLY_OPERATOR_REVIEW_FINAL_PACKET_BRIDGE_IN_MEMORY_ONLY:
        reasons.append(
            "fixture-only operator-review final-packet bridge posture is "
            f"{record.fixture_only_operator_review_final_packet_bridge_posture.value}"
        )
    if record.operator_review_final_packet_bridge_alignment_status is not OperatorReviewFinalPacketBridgeAlignmentStatus.OPERATOR_REVIEW_FINAL_PACKET_BRIDGE_ALIGNED:
        reasons.append(
            "operator-review final-packet bridge alignment status is "
            f"{record.operator_review_final_packet_bridge_alignment_status.value}"
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
        return FixtureOnlySourceProviderOperatorReviewFinalPacketBridgeValidationResult(
            severity=ValidationSeverity.BLOCKED,
            passed=False,
            reasons=tuple(reasons),
        )

    return FixtureOnlySourceProviderOperatorReviewFinalPacketBridgeValidationResult(
        severity=ValidationSeverity.PASSED,
        passed=True,
    )
