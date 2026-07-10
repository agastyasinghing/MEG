"""Pure fixture-only Weather Bot Stage 2 source/provider operator-review queue bridge runtime scaffold.

This module consumes only caller-supplied fixture-only operator-review ack bridge
and supplied runtime operator-review queue packet values. It is an in-memory
record only. It performs no live source fetching, no live provider clients, no
API calls, no scraping, no downloads, no SDK usage, no credentials/config
loading, no live ingestion, no evidence generation, no dry-run execution, no
simulation engine, no report generation, no smoke execution, no trace execution,
no handoff delivery, no acknowledgement delivery, no real queue service, no
enqueue/dequeue/publish/subscribe behavior, no queue/service/scheduler/broker
behavior, no owner-decision capture, no operator decision execution, no
persistence/export writing, no paper trading, no trading/execution, no autonomy,
and no production behavior.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping

from meg.weather.stage2.fixture_only_source_provider_operator_review_ack_bridge_runtime import (
    FixtureOnlySourceProviderOperatorReviewAckBridgeRecord,
    fixture_only_source_provider_operator_review_ack_bridge_record_from_mapping,
    validate_fixture_only_source_provider_operator_review_ack_bridge_record,
)
from meg.weather.stage2.supplied_runtime_operator_review_queue_packet import (
    SuppliedRuntimeOperatorReviewQueuePacketRecord,
    supplied_runtime_operator_review_queue_packet_record_from_mapping,
    validate_supplied_runtime_operator_review_queue_packet_record,
)


class _ClosedValue(str, Enum):
    """String enum base for closed, machine-checkable Stage 2 values."""

    @classmethod
    def values(cls) -> frozenset[str]:
        return frozenset(member.value for member in cls)


class FixtureOnlyOperatorReviewQueueBridgeStatus(_ClosedValue):
    FIXTURE_ONLY_OPERATOR_REVIEW_QUEUE_BRIDGE_RECORDED = "fixture_only_operator_review_queue_bridge_recorded"
    FIXTURE_ONLY_OPERATOR_REVIEW_QUEUE_BRIDGE_MISSING = "fixture_only_operator_review_queue_bridge_missing"
    FIXTURE_ONLY_OPERATOR_REVIEW_QUEUE_BRIDGE_AMBIGUOUS = "fixture_only_operator_review_queue_bridge_ambiguous"
    FIXTURE_ONLY_OPERATOR_REVIEW_QUEUE_BRIDGE_UNSUPPORTED = "fixture_only_operator_review_queue_bridge_unsupported"
    FIXTURE_ONLY_OPERATOR_REVIEW_QUEUE_BRIDGE_UNKNOWN = "fixture_only_operator_review_queue_bridge_unknown"


class FixtureOnlyOperatorReviewQueueBridgePosture(_ClosedValue):
    FIXTURE_ONLY_OPERATOR_REVIEW_QUEUE_BRIDGE_IN_MEMORY_ONLY = "fixture_only_operator_review_queue_bridge_in_memory_only"
    FIXTURE_ONLY_OPERATOR_REVIEW_QUEUE_BRIDGE_MISSING = "fixture_only_operator_review_queue_bridge_missing"
    FIXTURE_ONLY_OPERATOR_REVIEW_QUEUE_BRIDGE_AMBIGUOUS = "fixture_only_operator_review_queue_bridge_ambiguous"
    FIXTURE_ONLY_OPERATOR_REVIEW_QUEUE_BRIDGE_UNSUPPORTED = "fixture_only_operator_review_queue_bridge_unsupported"
    FIXTURE_ONLY_OPERATOR_REVIEW_QUEUE_BRIDGE_UNKNOWN = "fixture_only_operator_review_queue_bridge_unknown"


class OperatorReviewQueueBridgeAlignmentStatus(_ClosedValue):
    OPERATOR_REVIEW_QUEUE_BRIDGE_ALIGNED = "operator_review_queue_bridge_aligned"
    OPERATOR_REVIEW_QUEUE_BRIDGE_MISMATCH = "operator_review_queue_bridge_mismatch"
    OPERATOR_REVIEW_QUEUE_BRIDGE_MISSING = "operator_review_queue_bridge_missing"
    OPERATOR_REVIEW_QUEUE_BRIDGE_AMBIGUOUS = "operator_review_queue_bridge_ambiguous"
    OPERATOR_REVIEW_QUEUE_BRIDGE_UNKNOWN = "operator_review_queue_bridge_unknown"


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
class FixtureOnlySourceProviderOperatorReviewQueueBridgeRecord:
    condition_id: str
    token_id: str
    outcome: str
    fixture_only_source_provider_operator_review_ack_bridge: FixtureOnlySourceProviderOperatorReviewAckBridgeRecord
    supplied_runtime_operator_review_queue_packet: SuppliedRuntimeOperatorReviewQueuePacketRecord
    operator_review_queue_bridge_id: str
    operator_review_queue_bridge_summary: str
    fixture_ack_bridge_summary: str
    supplied_queue_summary: str
    operator_review_summary: str
    blocked_reason_summary: str
    fixture_only_operator_review_queue_bridge_status: FixtureOnlyOperatorReviewQueueBridgeStatus
    fixture_only_operator_review_queue_bridge_posture: FixtureOnlyOperatorReviewQueueBridgePosture
    operator_review_queue_bridge_alignment_status: OperatorReviewQueueBridgeAlignmentStatus
    no_lookahead_status: NoLookaheadStatus
    operator_review_status: OperatorReviewStatus
    runtime_gate_status: RuntimeGateStatus
    provenance_notes: str = ""


@dataclass(frozen=True)
class FixtureOnlySourceProviderOperatorReviewQueueBridgeValidationResult:
    severity: ValidationSeverity
    passed: bool
    reasons: tuple[str, ...] = ()


def _enum_value(enum_type: type[_ClosedValue], value: _ClosedValue | str) -> _ClosedValue:
    if isinstance(value, enum_type):
        return value
    return enum_type(value)


def _is_nonblank_text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _fixture_only_source_provider_operator_review_ack_bridge_from_value(
    value: FixtureOnlySourceProviderOperatorReviewAckBridgeRecord | Mapping[str, Any],
) -> FixtureOnlySourceProviderOperatorReviewAckBridgeRecord:
    if isinstance(value, FixtureOnlySourceProviderOperatorReviewAckBridgeRecord):
        return value
    return fixture_only_source_provider_operator_review_ack_bridge_record_from_mapping(value)


def _supplied_runtime_operator_review_queue_packet_from_value(
    value: SuppliedRuntimeOperatorReviewQueuePacketRecord | Mapping[str, Any],
) -> SuppliedRuntimeOperatorReviewQueuePacketRecord:
    if isinstance(value, SuppliedRuntimeOperatorReviewQueuePacketRecord):
        return value
    return supplied_runtime_operator_review_queue_packet_record_from_mapping(value)


def fixture_only_source_provider_operator_review_queue_bridge_record_from_mapping(
    mapping: Mapping[str, Any],
) -> FixtureOnlySourceProviderOperatorReviewQueueBridgeRecord:
    """Build operator-review queue bridge metadata from supplied values."""

    return FixtureOnlySourceProviderOperatorReviewQueueBridgeRecord(
        condition_id=mapping["condition_id"],
        token_id=mapping["token_id"],
        outcome=mapping["outcome"],
        fixture_only_source_provider_operator_review_ack_bridge=(
            _fixture_only_source_provider_operator_review_ack_bridge_from_value(
                mapping["fixture_only_source_provider_operator_review_ack_bridge"]
            )
        ),
        supplied_runtime_operator_review_queue_packet=(
            _supplied_runtime_operator_review_queue_packet_from_value(
                mapping["supplied_runtime_operator_review_queue_packet"]
            )
        ),
        operator_review_queue_bridge_id=mapping["operator_review_queue_bridge_id"],
        operator_review_queue_bridge_summary=mapping["operator_review_queue_bridge_summary"],
        fixture_ack_bridge_summary=mapping["fixture_ack_bridge_summary"],
        supplied_queue_summary=mapping["supplied_queue_summary"],
        operator_review_summary=mapping["operator_review_summary"],
        blocked_reason_summary=mapping["blocked_reason_summary"],
        fixture_only_operator_review_queue_bridge_status=_enum_value(
            FixtureOnlyOperatorReviewQueueBridgeStatus,
            mapping["fixture_only_operator_review_queue_bridge_status"],
        ),
        fixture_only_operator_review_queue_bridge_posture=_enum_value(
            FixtureOnlyOperatorReviewQueueBridgePosture,
            mapping["fixture_only_operator_review_queue_bridge_posture"],
        ),
        operator_review_queue_bridge_alignment_status=_enum_value(
            OperatorReviewQueueBridgeAlignmentStatus,
            mapping["operator_review_queue_bridge_alignment_status"],
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


def validate_fixture_only_source_provider_operator_review_queue_bridge_record(
    record: FixtureOnlySourceProviderOperatorReviewQueueBridgeRecord,
) -> FixtureOnlySourceProviderOperatorReviewQueueBridgeValidationResult:
    """Validate fixture-only operator-review queue bridge metadata fail-closed."""

    reasons: list[str] = []

    for field_name, value in (
        ("condition_id", record.condition_id),
        ("token_id", record.token_id),
        ("outcome", record.outcome),
        ("operator_review_queue_bridge_id", record.operator_review_queue_bridge_id),
        ("operator_review_queue_bridge_summary", record.operator_review_queue_bridge_summary),
        ("fixture_ack_bridge_summary", record.fixture_ack_bridge_summary),
        ("supplied_queue_summary", record.supplied_queue_summary),
        ("operator_review_summary", record.operator_review_summary),
    ):
        if not _is_nonblank_text(value):
            reasons.append(f"{field_name} is missing")

    ack_bridge = record.fixture_only_source_provider_operator_review_ack_bridge
    queue_packet = record.supplied_runtime_operator_review_queue_packet
    bridge_ack_packet = ack_bridge.supplied_runtime_operator_review_ack_packet
    queue_ack_packet = queue_packet.supplied_runtime_operator_review_ack_packet
    bridge_handoff = bridge_ack_packet.supplied_runtime_operator_review_handoff
    queue_handoff = queue_ack_packet.supplied_runtime_operator_review_handoff
    bridge_trace = bridge_handoff.supplied_runtime_trace_packet
    queue_trace = queue_handoff.supplied_runtime_trace_packet
    bridge_smoke = bridge_trace.supplied_runtime_end_to_end_smoke
    queue_smoke = queue_trace.supplied_runtime_end_to_end_smoke
    bridge_report = bridge_smoke.supplied_runtime_dry_run_report
    queue_report = queue_smoke.supplied_runtime_dry_run_report
    bridge_dry_run = bridge_report.supplied_runtime_dry_run_packet
    queue_dry_run = queue_report.supplied_runtime_dry_run_packet
    bridge_bundle = bridge_dry_run.supplied_runtime_validation_bundle
    queue_bundle = queue_dry_run.supplied_runtime_validation_bundle
    bridge_evidence = bridge_bundle.supplied_evidence_packet
    queue_evidence = queue_bundle.supplied_evidence_packet

    if not validate_fixture_only_source_provider_operator_review_ack_bridge_record(ack_bridge).passed:
        reasons.append("fixture-only source provider operator-review ack bridge is invalid")
    if not validate_supplied_runtime_operator_review_queue_packet_record(queue_packet).passed:
        reasons.append("supplied runtime operator-review queue packet is invalid")

    if record.condition_id != ack_bridge.condition_id:
        reasons.append("condition_id does not match fixture-only operator-review ack bridge")
    if record.token_id != ack_bridge.token_id:
        reasons.append("token_id does not match fixture-only operator-review ack bridge")
    if record.outcome != ack_bridge.outcome:
        reasons.append("outcome does not match fixture-only operator-review ack bridge")

    if record.condition_id != queue_packet.condition_id:
        reasons.append("condition_id does not match supplied runtime operator-review queue packet")
    if record.token_id != queue_packet.token_id:
        reasons.append("token_id does not match supplied runtime operator-review queue packet")
    if record.outcome != queue_packet.outcome:
        reasons.append("outcome does not match supplied runtime operator-review queue packet")

    if not _same_route(ack_bridge, queue_packet):
        reasons.append(
            "nested fixture-only operator-review ack bridge and supplied runtime operator-review queue packet routes do not match"
        )
    if not _same_route(bridge_ack_packet, queue_ack_packet):
        reasons.append("nested supplied runtime operator-review ack packets do not match")
    if not _same_route(bridge_handoff, queue_handoff):
        reasons.append("nested supplied runtime operator-review handoffs do not match")
    if not _same_route(bridge_trace, queue_trace):
        reasons.append("nested supplied runtime trace packets do not match")
    if not _same_route(bridge_smoke, queue_smoke):
        reasons.append("nested supplied runtime end-to-end smokes do not match")
    if not _same_route(bridge_report, queue_report):
        reasons.append("nested supplied runtime dry-run reports do not match")
    if not _same_route(bridge_dry_run, queue_dry_run) or not _same_route(bridge_bundle, queue_bundle):
        reasons.append("nested supplied runtime dry-run packets do not match")
    if not _same_route(bridge_evidence, queue_evidence) or not _same_route(
        bridge_evidence.supplied_market_contract,
        queue_evidence.supplied_market_contract,
    ):
        reasons.append("nested supplied evidence packets do not match")

    if record.fixture_ack_bridge_summary != ack_bridge.operator_review_ack_bridge_summary:
        reasons.append("fixture ack bridge summary does not match fixture-only operator-review ack bridge")
    if record.supplied_queue_summary != queue_packet.queue_summary:
        reasons.append("supplied queue summary does not match supplied runtime operator-review queue packet")
    if record.operator_review_summary != queue_packet.operator_review_summary:
        reasons.append("operator review summary does not match supplied runtime operator-review queue packet")
    if record.operator_review_summary != ack_bridge.operator_review_summary:
        reasons.append("operator review summary does not match fixture-only operator-review ack bridge")

    if record.fixture_only_operator_review_queue_bridge_status is not FixtureOnlyOperatorReviewQueueBridgeStatus.FIXTURE_ONLY_OPERATOR_REVIEW_QUEUE_BRIDGE_RECORDED:
        reasons.append(
            "fixture-only operator-review queue bridge status is "
            f"{record.fixture_only_operator_review_queue_bridge_status.value}"
        )
    if record.fixture_only_operator_review_queue_bridge_posture is not FixtureOnlyOperatorReviewQueueBridgePosture.FIXTURE_ONLY_OPERATOR_REVIEW_QUEUE_BRIDGE_IN_MEMORY_ONLY:
        reasons.append(
            "fixture-only operator-review queue bridge posture is "
            f"{record.fixture_only_operator_review_queue_bridge_posture.value}"
        )
    if record.operator_review_queue_bridge_alignment_status is not OperatorReviewQueueBridgeAlignmentStatus.OPERATOR_REVIEW_QUEUE_BRIDGE_ALIGNED:
        reasons.append(
            "operator-review queue bridge alignment status is "
            f"{record.operator_review_queue_bridge_alignment_status.value}"
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
        return FixtureOnlySourceProviderOperatorReviewQueueBridgeValidationResult(
            severity=ValidationSeverity.BLOCKED,
            passed=False,
            reasons=tuple(reasons),
        )

    return FixtureOnlySourceProviderOperatorReviewQueueBridgeValidationResult(
        severity=ValidationSeverity.PASSED,
        passed=True,
    )
