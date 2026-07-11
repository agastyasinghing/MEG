"""Pure fixture-only Weather Bot Stage 2 source/provider operator-review queue-summary bridge runtime scaffold.

This module consumes only caller-supplied fixture-only queue-entry bridge and
supplied queue-summary values. It is an in-memory record only. It performs no
live providers or fetching, no API calls, scraping, downloads, SDKs,
credentials, or live ingestion, no evidence generation, no execution,
simulation, report generation, smoke execution, or trace execution, no handoff,
acknowledgement, queue-packet, queue-entry, or queue-summary delivery, no
generated-summary behavior, no real queue service, no enqueue/dequeue/
publish/subscribe behavior, no scheduler or broker, no owner-decision capture,
no operator-decision execution, no persistence or export writing, and no paper
trading, trading, autonomy, or production behavior.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping

from meg.weather.stage2.fixture_only_source_provider_operator_review_queue_entry_bridge_runtime import (
    FixtureOnlySourceProviderOperatorReviewQueueEntryBridgeRecord,
    fixture_only_source_provider_operator_review_queue_entry_bridge_record_from_mapping,
    validate_fixture_only_source_provider_operator_review_queue_entry_bridge_record,
)
from meg.weather.stage2.supplied_runtime_operator_review_queue_summary import (
    SuppliedRuntimeOperatorReviewQueueSummaryRecord,
    supplied_runtime_operator_review_queue_summary_record_from_mapping,
    validate_supplied_runtime_operator_review_queue_summary_record,
)


class _ClosedValue(str, Enum):
    """String enum base for closed, machine-checkable Stage 2 values."""

    @classmethod
    def values(cls) -> frozenset[str]:
        return frozenset(member.value for member in cls)


class FixtureOnlyOperatorReviewQueueSummaryBridgeStatus(_ClosedValue):
    FIXTURE_ONLY_OPERATOR_REVIEW_QUEUE_SUMMARY_BRIDGE_RECORDED = "fixture_only_operator_review_queue_summary_bridge_recorded"
    FIXTURE_ONLY_OPERATOR_REVIEW_QUEUE_SUMMARY_BRIDGE_MISSING = "fixture_only_operator_review_queue_summary_bridge_missing"
    FIXTURE_ONLY_OPERATOR_REVIEW_QUEUE_SUMMARY_BRIDGE_AMBIGUOUS = "fixture_only_operator_review_queue_summary_bridge_ambiguous"
    FIXTURE_ONLY_OPERATOR_REVIEW_QUEUE_SUMMARY_BRIDGE_UNSUPPORTED = "fixture_only_operator_review_queue_summary_bridge_unsupported"
    FIXTURE_ONLY_OPERATOR_REVIEW_QUEUE_SUMMARY_BRIDGE_UNKNOWN = "fixture_only_operator_review_queue_summary_bridge_unknown"


class FixtureOnlyOperatorReviewQueueSummaryBridgePosture(_ClosedValue):
    FIXTURE_ONLY_OPERATOR_REVIEW_QUEUE_SUMMARY_BRIDGE_IN_MEMORY_ONLY = "fixture_only_operator_review_queue_summary_bridge_in_memory_only"
    FIXTURE_ONLY_OPERATOR_REVIEW_QUEUE_SUMMARY_BRIDGE_MISSING = "fixture_only_operator_review_queue_summary_bridge_missing"
    FIXTURE_ONLY_OPERATOR_REVIEW_QUEUE_SUMMARY_BRIDGE_AMBIGUOUS = "fixture_only_operator_review_queue_summary_bridge_ambiguous"
    FIXTURE_ONLY_OPERATOR_REVIEW_QUEUE_SUMMARY_BRIDGE_UNSUPPORTED = "fixture_only_operator_review_queue_summary_bridge_unsupported"
    FIXTURE_ONLY_OPERATOR_REVIEW_QUEUE_SUMMARY_BRIDGE_UNKNOWN = "fixture_only_operator_review_queue_summary_bridge_unknown"


class OperatorReviewQueueSummaryBridgeAlignmentStatus(_ClosedValue):
    OPERATOR_REVIEW_QUEUE_SUMMARY_BRIDGE_ALIGNED = "operator_review_queue_summary_bridge_aligned"
    OPERATOR_REVIEW_QUEUE_SUMMARY_BRIDGE_MISMATCH = "operator_review_queue_summary_bridge_mismatch"
    OPERATOR_REVIEW_QUEUE_SUMMARY_BRIDGE_MISSING = "operator_review_queue_summary_bridge_missing"
    OPERATOR_REVIEW_QUEUE_SUMMARY_BRIDGE_AMBIGUOUS = "operator_review_queue_summary_bridge_ambiguous"
    OPERATOR_REVIEW_QUEUE_SUMMARY_BRIDGE_UNKNOWN = "operator_review_queue_summary_bridge_unknown"


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
class FixtureOnlySourceProviderOperatorReviewQueueSummaryBridgeRecord:
    condition_id: str
    token_id: str
    outcome: str
    fixture_only_source_provider_operator_review_queue_entry_bridge: FixtureOnlySourceProviderOperatorReviewQueueEntryBridgeRecord
    supplied_runtime_operator_review_queue_summary: SuppliedRuntimeOperatorReviewQueueSummaryRecord
    operator_review_queue_summary_bridge_id: str
    operator_review_queue_summary_bridge_summary: str
    fixture_queue_entry_bridge_summary: str
    supplied_queue_summary_text: str
    operator_review_summary: str
    blocked_reason_summary: str
    fixture_only_operator_review_queue_summary_bridge_status: FixtureOnlyOperatorReviewQueueSummaryBridgeStatus
    fixture_only_operator_review_queue_summary_bridge_posture: FixtureOnlyOperatorReviewQueueSummaryBridgePosture
    operator_review_queue_summary_bridge_alignment_status: OperatorReviewQueueSummaryBridgeAlignmentStatus
    no_lookahead_status: NoLookaheadStatus
    operator_review_status: OperatorReviewStatus
    runtime_gate_status: RuntimeGateStatus
    provenance_notes: str = ""


@dataclass(frozen=True)
class FixtureOnlySourceProviderOperatorReviewQueueSummaryBridgeValidationResult:
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


def _fixture_only_source_provider_operator_review_queue_entry_bridge_from_value(
    value: FixtureOnlySourceProviderOperatorReviewQueueEntryBridgeRecord | Mapping[str, Any],
) -> FixtureOnlySourceProviderOperatorReviewQueueEntryBridgeRecord:
    if isinstance(value, FixtureOnlySourceProviderOperatorReviewQueueEntryBridgeRecord):
        return value
    return fixture_only_source_provider_operator_review_queue_entry_bridge_record_from_mapping(value)


def _supplied_runtime_operator_review_queue_summary_from_value(
    value: SuppliedRuntimeOperatorReviewQueueSummaryRecord | Mapping[str, Any],
) -> SuppliedRuntimeOperatorReviewQueueSummaryRecord:
    if isinstance(value, SuppliedRuntimeOperatorReviewQueueSummaryRecord):
        return value
    return supplied_runtime_operator_review_queue_summary_record_from_mapping(value)


def fixture_only_source_provider_operator_review_queue_summary_bridge_record_from_mapping(
    mapping: Mapping[str, Any],
) -> FixtureOnlySourceProviderOperatorReviewQueueSummaryBridgeRecord:
    """Build operator-review queue-summary bridge metadata from supplied values."""

    return FixtureOnlySourceProviderOperatorReviewQueueSummaryBridgeRecord(
        condition_id=mapping["condition_id"],
        token_id=mapping["token_id"],
        outcome=mapping["outcome"],
        fixture_only_source_provider_operator_review_queue_entry_bridge=(
            _fixture_only_source_provider_operator_review_queue_entry_bridge_from_value(
                mapping["fixture_only_source_provider_operator_review_queue_entry_bridge"]
            )
        ),
        supplied_runtime_operator_review_queue_summary=(
            _supplied_runtime_operator_review_queue_summary_from_value(
                mapping["supplied_runtime_operator_review_queue_summary"]
            )
        ),
        operator_review_queue_summary_bridge_id=mapping["operator_review_queue_summary_bridge_id"],
        operator_review_queue_summary_bridge_summary=mapping[
            "operator_review_queue_summary_bridge_summary"
        ],
        fixture_queue_entry_bridge_summary=mapping["fixture_queue_entry_bridge_summary"],
        supplied_queue_summary_text=mapping["supplied_queue_summary_text"],
        operator_review_summary=mapping["operator_review_summary"],
        blocked_reason_summary=mapping["blocked_reason_summary"],
        fixture_only_operator_review_queue_summary_bridge_status=_enum_value(
            FixtureOnlyOperatorReviewQueueSummaryBridgeStatus,
            mapping["fixture_only_operator_review_queue_summary_bridge_status"],
        ),
        fixture_only_operator_review_queue_summary_bridge_posture=_enum_value(
            FixtureOnlyOperatorReviewQueueSummaryBridgePosture,
            mapping["fixture_only_operator_review_queue_summary_bridge_posture"],
        ),
        operator_review_queue_summary_bridge_alignment_status=_enum_value(
            OperatorReviewQueueSummaryBridgeAlignmentStatus,
            mapping["operator_review_queue_summary_bridge_alignment_status"],
        ),
        no_lookahead_status=_enum_value(NoLookaheadStatus, mapping["no_lookahead_status"]),
        operator_review_status=_enum_value(OperatorReviewStatus, mapping["operator_review_status"]),
        runtime_gate_status=_enum_value(RuntimeGateStatus, mapping["runtime_gate_status"]),
        provenance_notes=str(mapping.get("provenance_notes", "")),
    )


def validate_fixture_only_source_provider_operator_review_queue_summary_bridge_record(
    record: FixtureOnlySourceProviderOperatorReviewQueueSummaryBridgeRecord,
) -> FixtureOnlySourceProviderOperatorReviewQueueSummaryBridgeValidationResult:
    """Validate fixture-only operator-review queue-summary bridge metadata fail-closed."""

    reasons: list[str] = []

    for field_name, value in (
        ("condition_id", record.condition_id),
        ("token_id", record.token_id),
        ("outcome", record.outcome),
        ("operator_review_queue_summary_bridge_id", record.operator_review_queue_summary_bridge_id),
        ("operator_review_queue_summary_bridge_summary", record.operator_review_queue_summary_bridge_summary),
        ("fixture_queue_entry_bridge_summary", record.fixture_queue_entry_bridge_summary),
        ("supplied_queue_summary_text", record.supplied_queue_summary_text),
        ("operator_review_summary", record.operator_review_summary),
    ):
        if not _is_nonblank_text(value):
            reasons.append(f"{field_name} is missing")

    entry_bridge = record.fixture_only_source_provider_operator_review_queue_entry_bridge
    queue_summary = record.supplied_runtime_operator_review_queue_summary
    bridge_queue_entry = entry_bridge.supplied_runtime_operator_review_queue_entry
    summary_queue_entry = queue_summary.supplied_runtime_operator_review_queue_entry
    bridge_queue_packet = bridge_queue_entry.supplied_runtime_operator_review_queue_packet
    summary_queue_packet = summary_queue_entry.supplied_runtime_operator_review_queue_packet
    bridge_ack_packet = bridge_queue_packet.supplied_runtime_operator_review_ack_packet
    summary_ack_packet = summary_queue_packet.supplied_runtime_operator_review_ack_packet
    bridge_handoff = bridge_ack_packet.supplied_runtime_operator_review_handoff
    summary_handoff = summary_ack_packet.supplied_runtime_operator_review_handoff
    bridge_trace = bridge_handoff.supplied_runtime_trace_packet
    summary_trace = summary_handoff.supplied_runtime_trace_packet
    bridge_smoke = bridge_trace.supplied_runtime_end_to_end_smoke
    summary_smoke = summary_trace.supplied_runtime_end_to_end_smoke
    bridge_report = bridge_smoke.supplied_runtime_dry_run_report
    summary_report = summary_smoke.supplied_runtime_dry_run_report
    bridge_dry_run = bridge_report.supplied_runtime_dry_run_packet
    summary_dry_run = summary_report.supplied_runtime_dry_run_packet
    bridge_bundle = bridge_dry_run.supplied_runtime_validation_bundle
    summary_bundle = summary_dry_run.supplied_runtime_validation_bundle
    bridge_evidence = bridge_bundle.supplied_evidence_packet
    summary_evidence = summary_bundle.supplied_evidence_packet

    if not validate_fixture_only_source_provider_operator_review_queue_entry_bridge_record(
        entry_bridge
    ).passed:
        reasons.append("fixture-only source provider operator-review queue-entry bridge is invalid")
    if not validate_supplied_runtime_operator_review_queue_summary_record(queue_summary).passed:
        reasons.append("supplied runtime operator-review queue summary is invalid")

    if record.condition_id != entry_bridge.condition_id:
        reasons.append("condition_id does not match fixture-only operator-review queue-entry bridge")
    if record.token_id != entry_bridge.token_id:
        reasons.append("token_id does not match fixture-only operator-review queue-entry bridge")
    if record.outcome != entry_bridge.outcome:
        reasons.append("outcome does not match fixture-only operator-review queue-entry bridge")
    if record.condition_id != queue_summary.condition_id:
        reasons.append("condition_id does not match supplied runtime operator-review queue summary")
    if record.token_id != queue_summary.token_id:
        reasons.append("token_id does not match supplied runtime operator-review queue summary")
    if record.outcome != queue_summary.outcome:
        reasons.append("outcome does not match supplied runtime operator-review queue summary")

    if not _same_route(entry_bridge, queue_summary):
        reasons.append(
            "nested fixture-only operator-review queue-entry bridge and supplied runtime operator-review queue summary routes do not match"
        )
    if not _same_route(bridge_queue_entry, summary_queue_entry):
        reasons.append("nested supplied runtime operator-review queue entries do not match")
    if not _same_route(bridge_queue_packet, summary_queue_packet):
        reasons.append("nested supplied runtime operator-review queue packets do not match")
    if not _same_route(bridge_ack_packet, summary_ack_packet):
        reasons.append("nested supplied runtime operator-review ack packets do not match")
    if not _same_route(bridge_handoff, summary_handoff):
        reasons.append("nested supplied runtime operator-review handoffs do not match")
    if not _same_route(bridge_trace, summary_trace):
        reasons.append("nested supplied runtime trace packets do not match")
    if not _same_route(bridge_smoke, summary_smoke):
        reasons.append("nested supplied runtime end-to-end smokes do not match")
    if not _same_route(bridge_report, summary_report):
        reasons.append("nested supplied runtime dry-run reports do not match")
    if not _same_route(bridge_dry_run, summary_dry_run) or not _same_route(
        bridge_bundle,
        summary_bundle,
    ):
        reasons.append("nested supplied runtime dry-run packets do not match")
    if not _same_route(bridge_evidence, summary_evidence) or not _same_route(
        bridge_evidence.supplied_market_contract,
        summary_evidence.supplied_market_contract,
    ):
        reasons.append("nested supplied evidence packets do not match")

    if (
        record.fixture_queue_entry_bridge_summary
        != entry_bridge.operator_review_queue_entry_bridge_summary
    ):
        reasons.append(
            "fixture queue-entry bridge summary does not match fixture-only operator-review queue-entry bridge"
        )
    if record.supplied_queue_summary_text != queue_summary.queue_summary_text:
        reasons.append(
            "supplied queue summary text does not match supplied runtime operator-review queue summary"
        )
    if record.operator_review_summary != queue_summary.operator_review_summary:
        reasons.append("operator review summary does not match supplied runtime operator-review queue summary")
    if record.operator_review_summary != entry_bridge.operator_review_summary:
        reasons.append("operator review summary does not match fixture-only operator-review queue-entry bridge")

    if record.fixture_only_operator_review_queue_summary_bridge_status is not FixtureOnlyOperatorReviewQueueSummaryBridgeStatus.FIXTURE_ONLY_OPERATOR_REVIEW_QUEUE_SUMMARY_BRIDGE_RECORDED:
        reasons.append(
            "fixture-only operator-review queue-summary bridge status is "
            f"{record.fixture_only_operator_review_queue_summary_bridge_status.value}"
        )
    if record.fixture_only_operator_review_queue_summary_bridge_posture is not FixtureOnlyOperatorReviewQueueSummaryBridgePosture.FIXTURE_ONLY_OPERATOR_REVIEW_QUEUE_SUMMARY_BRIDGE_IN_MEMORY_ONLY:
        reasons.append(
            "fixture-only operator-review queue-summary bridge posture is "
            f"{record.fixture_only_operator_review_queue_summary_bridge_posture.value}"
        )
    if record.operator_review_queue_summary_bridge_alignment_status is not OperatorReviewQueueSummaryBridgeAlignmentStatus.OPERATOR_REVIEW_QUEUE_SUMMARY_BRIDGE_ALIGNED:
        reasons.append(
            "operator-review queue-summary bridge alignment status is "
            f"{record.operator_review_queue_summary_bridge_alignment_status.value}"
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
        return FixtureOnlySourceProviderOperatorReviewQueueSummaryBridgeValidationResult(
            severity=ValidationSeverity.BLOCKED,
            passed=False,
            reasons=tuple(reasons),
        )

    return FixtureOnlySourceProviderOperatorReviewQueueSummaryBridgeValidationResult(
        severity=ValidationSeverity.PASSED,
        passed=True,
    )
