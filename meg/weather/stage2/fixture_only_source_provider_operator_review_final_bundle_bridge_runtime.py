"""Pure fixture-only Weather Bot Stage 2 source/provider operator-review final-bundle bridge runtime scaffold.

This module consumes only caller-supplied fixture-only final-packet bridge and
supplied final-bundle values. It is an in-memory record only. It performs no
live providers or live source fetching, API clients or API calls, scraping,
forecast pulls, downloads, provider SDK usage, credentials, secrets,
environment or configuration loading, live ingestion, file or network I/O,
evidence generation or mutation, scoring or backtesting, dry-run execution,
simulation, report generation, smoke or trace execution, delivery of handoff,
acknowledgement, queue-packet, queue-entry, queue-summary, final-packet, or
final-bundle values, generated-packet, generated-bundle, or generated-summary
behavior, real queue services, enqueue/dequeue/publish/subscribe behavior,
scheduling or broker behavior, persistence or export writing, owner-decision
capture, operator-decision execution, paper trading, trading or execution,
autonomy, or production behavior.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping

from meg.weather.stage2.fixture_only_source_provider_operator_review_final_packet_bridge_runtime import (
    FixtureOnlySourceProviderOperatorReviewFinalPacketBridgeRecord,
    fixture_only_source_provider_operator_review_final_packet_bridge_record_from_mapping,
    validate_fixture_only_source_provider_operator_review_final_packet_bridge_record,
)
from meg.weather.stage2.supplied_runtime_operator_review_final_bundle import (
    SuppliedRuntimeOperatorReviewFinalBundleRecord,
    supplied_runtime_operator_review_final_bundle_record_from_mapping,
    validate_supplied_runtime_operator_review_final_bundle_record,
)


class _ClosedValue(str, Enum):
    """String enum base for closed, machine-checkable Stage 2 values."""

    @classmethod
    def values(cls) -> frozenset[str]:
        return frozenset(member.value for member in cls)


class FixtureOnlyOperatorReviewFinalBundleBridgeStatus(_ClosedValue):
    FIXTURE_ONLY_OPERATOR_REVIEW_FINAL_BUNDLE_BRIDGE_RECORDED = "fixture_only_operator_review_final_bundle_bridge_recorded"
    FIXTURE_ONLY_OPERATOR_REVIEW_FINAL_BUNDLE_BRIDGE_MISSING = "fixture_only_operator_review_final_bundle_bridge_missing"
    FIXTURE_ONLY_OPERATOR_REVIEW_FINAL_BUNDLE_BRIDGE_AMBIGUOUS = "fixture_only_operator_review_final_bundle_bridge_ambiguous"
    FIXTURE_ONLY_OPERATOR_REVIEW_FINAL_BUNDLE_BRIDGE_UNSUPPORTED = "fixture_only_operator_review_final_bundle_bridge_unsupported"
    FIXTURE_ONLY_OPERATOR_REVIEW_FINAL_BUNDLE_BRIDGE_UNKNOWN = "fixture_only_operator_review_final_bundle_bridge_unknown"


class FixtureOnlyOperatorReviewFinalBundleBridgePosture(_ClosedValue):
    FIXTURE_ONLY_OPERATOR_REVIEW_FINAL_BUNDLE_BRIDGE_IN_MEMORY_ONLY = "fixture_only_operator_review_final_bundle_bridge_in_memory_only"
    FIXTURE_ONLY_OPERATOR_REVIEW_FINAL_BUNDLE_BRIDGE_MISSING = "fixture_only_operator_review_final_bundle_bridge_missing"
    FIXTURE_ONLY_OPERATOR_REVIEW_FINAL_BUNDLE_BRIDGE_AMBIGUOUS = "fixture_only_operator_review_final_bundle_bridge_ambiguous"
    FIXTURE_ONLY_OPERATOR_REVIEW_FINAL_BUNDLE_BRIDGE_UNSUPPORTED = "fixture_only_operator_review_final_bundle_bridge_unsupported"
    FIXTURE_ONLY_OPERATOR_REVIEW_FINAL_BUNDLE_BRIDGE_UNKNOWN = "fixture_only_operator_review_final_bundle_bridge_unknown"


class OperatorReviewFinalBundleBridgeAlignmentStatus(_ClosedValue):
    OPERATOR_REVIEW_FINAL_BUNDLE_BRIDGE_ALIGNED = "operator_review_final_bundle_bridge_aligned"
    OPERATOR_REVIEW_FINAL_BUNDLE_BRIDGE_MISMATCH = "operator_review_final_bundle_bridge_mismatch"
    OPERATOR_REVIEW_FINAL_BUNDLE_BRIDGE_MISSING = "operator_review_final_bundle_bridge_missing"
    OPERATOR_REVIEW_FINAL_BUNDLE_BRIDGE_AMBIGUOUS = "operator_review_final_bundle_bridge_ambiguous"
    OPERATOR_REVIEW_FINAL_BUNDLE_BRIDGE_UNKNOWN = "operator_review_final_bundle_bridge_unknown"


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
class FixtureOnlySourceProviderOperatorReviewFinalBundleBridgeRecord:
    condition_id: str
    token_id: str
    outcome: str
    fixture_only_source_provider_operator_review_final_packet_bridge: FixtureOnlySourceProviderOperatorReviewFinalPacketBridgeRecord
    supplied_runtime_operator_review_final_bundle: SuppliedRuntimeOperatorReviewFinalBundleRecord
    operator_review_final_bundle_bridge_id: str
    operator_review_final_bundle_bridge_summary: str
    fixture_final_packet_bridge_summary: str
    supplied_final_bundle_summary: str
    operator_review_summary: str
    blocked_reason_summary: str
    fixture_only_operator_review_final_bundle_bridge_status: FixtureOnlyOperatorReviewFinalBundleBridgeStatus
    fixture_only_operator_review_final_bundle_bridge_posture: FixtureOnlyOperatorReviewFinalBundleBridgePosture
    operator_review_final_bundle_bridge_alignment_status: OperatorReviewFinalBundleBridgeAlignmentStatus
    no_lookahead_status: NoLookaheadStatus
    operator_review_status: OperatorReviewStatus
    runtime_gate_status: RuntimeGateStatus
    provenance_notes: str = ""


@dataclass(frozen=True)
class FixtureOnlySourceProviderOperatorReviewFinalBundleBridgeValidationResult:
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


def _fixture_only_source_provider_operator_review_final_packet_bridge_from_value(
    value: FixtureOnlySourceProviderOperatorReviewFinalPacketBridgeRecord | Mapping[str, Any],
) -> FixtureOnlySourceProviderOperatorReviewFinalPacketBridgeRecord:
    if isinstance(value, FixtureOnlySourceProviderOperatorReviewFinalPacketBridgeRecord):
        return value
    return fixture_only_source_provider_operator_review_final_packet_bridge_record_from_mapping(value)


def _supplied_runtime_operator_review_final_bundle_from_value(
    value: SuppliedRuntimeOperatorReviewFinalBundleRecord | Mapping[str, Any],
) -> SuppliedRuntimeOperatorReviewFinalBundleRecord:
    if isinstance(value, SuppliedRuntimeOperatorReviewFinalBundleRecord):
        return value
    return supplied_runtime_operator_review_final_bundle_record_from_mapping(value)


def fixture_only_source_provider_operator_review_final_bundle_bridge_record_from_mapping(
    mapping: Mapping[str, Any],
) -> FixtureOnlySourceProviderOperatorReviewFinalBundleBridgeRecord:
    """Build operator-review final-bundle bridge metadata from supplied values."""

    return FixtureOnlySourceProviderOperatorReviewFinalBundleBridgeRecord(
        condition_id=mapping["condition_id"],
        token_id=mapping["token_id"],
        outcome=mapping["outcome"],
        fixture_only_source_provider_operator_review_final_packet_bridge=(
            _fixture_only_source_provider_operator_review_final_packet_bridge_from_value(
                mapping["fixture_only_source_provider_operator_review_final_packet_bridge"]
            )
        ),
        supplied_runtime_operator_review_final_bundle=(
            _supplied_runtime_operator_review_final_bundle_from_value(
                mapping["supplied_runtime_operator_review_final_bundle"]
            )
        ),
        operator_review_final_bundle_bridge_id=mapping["operator_review_final_bundle_bridge_id"],
        operator_review_final_bundle_bridge_summary=mapping[
            "operator_review_final_bundle_bridge_summary"
        ],
        fixture_final_packet_bridge_summary=mapping["fixture_final_packet_bridge_summary"],
        supplied_final_bundle_summary=mapping["supplied_final_bundle_summary"],
        operator_review_summary=mapping["operator_review_summary"],
        blocked_reason_summary=mapping["blocked_reason_summary"],
        fixture_only_operator_review_final_bundle_bridge_status=_enum_value(
            FixtureOnlyOperatorReviewFinalBundleBridgeStatus,
            mapping["fixture_only_operator_review_final_bundle_bridge_status"],
        ),
        fixture_only_operator_review_final_bundle_bridge_posture=_enum_value(
            FixtureOnlyOperatorReviewFinalBundleBridgePosture,
            mapping["fixture_only_operator_review_final_bundle_bridge_posture"],
        ),
        operator_review_final_bundle_bridge_alignment_status=_enum_value(
            OperatorReviewFinalBundleBridgeAlignmentStatus,
            mapping["operator_review_final_bundle_bridge_alignment_status"],
        ),
        no_lookahead_status=_enum_value(NoLookaheadStatus, mapping["no_lookahead_status"]),
        operator_review_status=_enum_value(OperatorReviewStatus, mapping["operator_review_status"]),
        runtime_gate_status=_enum_value(RuntimeGateStatus, mapping["runtime_gate_status"]),
        provenance_notes=str(mapping.get("provenance_notes", "")),
    )


def validate_fixture_only_source_provider_operator_review_final_bundle_bridge_record(
    record: FixtureOnlySourceProviderOperatorReviewFinalBundleBridgeRecord,
) -> FixtureOnlySourceProviderOperatorReviewFinalBundleBridgeValidationResult:
    """Validate fixture-only operator-review final-bundle bridge metadata fail-closed."""

    reasons: list[str] = []
    for field_name, value in (
        ("condition_id", record.condition_id),
        ("token_id", record.token_id),
        ("outcome", record.outcome),
        ("operator_review_final_bundle_bridge_id", record.operator_review_final_bundle_bridge_id),
        ("operator_review_final_bundle_bridge_summary", record.operator_review_final_bundle_bridge_summary),
        ("fixture_final_packet_bridge_summary", record.fixture_final_packet_bridge_summary),
        ("supplied_final_bundle_summary", record.supplied_final_bundle_summary),
        ("operator_review_summary", record.operator_review_summary),
    ):
        if not _is_nonblank_text(value):
            reasons.append(f"{field_name} is missing")

    packet_bridge = record.fixture_only_source_provider_operator_review_final_packet_bridge
    final_bundle = record.supplied_runtime_operator_review_final_bundle
    bridge_final_packet = packet_bridge.supplied_runtime_operator_review_final_packet
    bundle_final_packet = final_bundle.supplied_runtime_operator_review_final_packet
    bridge_summary = bridge_final_packet.supplied_runtime_operator_review_queue_summary
    bundle_summary = bundle_final_packet.supplied_runtime_operator_review_queue_summary
    bridge_entry = bridge_summary.supplied_runtime_operator_review_queue_entry
    bundle_entry = bundle_summary.supplied_runtime_operator_review_queue_entry
    bridge_queue = bridge_entry.supplied_runtime_operator_review_queue_packet
    bundle_queue = bundle_entry.supplied_runtime_operator_review_queue_packet
    bridge_ack = bridge_queue.supplied_runtime_operator_review_ack_packet
    bundle_ack = bundle_queue.supplied_runtime_operator_review_ack_packet
    bridge_handoff = bridge_ack.supplied_runtime_operator_review_handoff
    bundle_handoff = bundle_ack.supplied_runtime_operator_review_handoff
    bridge_trace = bridge_handoff.supplied_runtime_trace_packet
    bundle_trace = bundle_handoff.supplied_runtime_trace_packet
    bridge_smoke = bridge_trace.supplied_runtime_end_to_end_smoke
    bundle_smoke = bundle_trace.supplied_runtime_end_to_end_smoke
    bridge_report = bridge_smoke.supplied_runtime_dry_run_report
    bundle_report = bundle_smoke.supplied_runtime_dry_run_report
    bridge_dry = bridge_report.supplied_runtime_dry_run_packet
    bundle_dry = bundle_report.supplied_runtime_dry_run_packet
    bridge_validation = bridge_dry.supplied_runtime_validation_bundle
    bundle_validation = bundle_dry.supplied_runtime_validation_bundle
    bridge_evidence = bridge_validation.supplied_evidence_packet
    bundle_evidence = bundle_validation.supplied_evidence_packet

    if not validate_fixture_only_source_provider_operator_review_final_packet_bridge_record(
        packet_bridge
    ).passed:
        reasons.append("fixture-only source provider operator-review final-packet bridge is invalid")
    if not validate_supplied_runtime_operator_review_final_bundle_record(final_bundle).passed:
        reasons.append("supplied runtime operator-review final bundle is invalid")

    if record.condition_id != packet_bridge.condition_id:
        reasons.append("condition_id does not match fixture-only operator-review final-packet bridge")
    if record.token_id != packet_bridge.token_id:
        reasons.append("token_id does not match fixture-only operator-review final-packet bridge")
    if record.outcome != packet_bridge.outcome:
        reasons.append("outcome does not match fixture-only operator-review final-packet bridge")
    if record.condition_id != final_bundle.condition_id:
        reasons.append("condition_id does not match supplied runtime operator-review final bundle")
    if record.token_id != final_bundle.token_id:
        reasons.append("token_id does not match supplied runtime operator-review final bundle")
    if record.outcome != final_bundle.outcome:
        reasons.append("outcome does not match supplied runtime operator-review final bundle")

    if not _same_route(packet_bridge, final_bundle):
        reasons.append("nested fixture-only operator-review final-packet bridge and supplied runtime operator-review final bundle routes do not match")
    if not _same_route(bridge_final_packet, bundle_final_packet):
        reasons.append("nested supplied runtime operator-review final packets do not match")
    if not _same_route(bridge_summary, bundle_summary):
        reasons.append("nested supplied runtime operator-review queue summaries do not match")
    if not _same_route(bridge_entry, bundle_entry):
        reasons.append("nested supplied runtime operator-review queue entries do not match")
    if not _same_route(bridge_queue, bundle_queue):
        reasons.append("nested supplied runtime operator-review queue packets do not match")
    if not _same_route(bridge_ack, bundle_ack):
        reasons.append("nested supplied runtime operator-review ack packets do not match")
    if not _same_route(bridge_handoff, bundle_handoff):
        reasons.append("nested supplied runtime operator-review handoffs do not match")
    if not _same_route(bridge_trace, bundle_trace):
        reasons.append("nested supplied runtime trace packets do not match")
    if not _same_route(bridge_smoke, bundle_smoke):
        reasons.append("nested supplied runtime end-to-end smokes do not match")
    if not _same_route(bridge_report, bundle_report):
        reasons.append("nested supplied runtime dry-run reports do not match")
    if not _same_route(bridge_dry, bundle_dry) or not _same_route(bridge_validation, bundle_validation):
        reasons.append("nested supplied runtime dry-run packets do not match")
    if not _same_route(bridge_evidence, bundle_evidence) or not _same_route(
        bridge_evidence.supplied_market_contract,
        bundle_evidence.supplied_market_contract,
    ):
        reasons.append("nested supplied evidence packets do not match")

    if record.fixture_final_packet_bridge_summary != packet_bridge.operator_review_final_packet_bridge_summary:
        reasons.append("fixture final-packet bridge summary does not match fixture-only operator-review final-packet bridge")
    if record.supplied_final_bundle_summary != final_bundle.final_bundle_summary:
        reasons.append("supplied final bundle summary does not match supplied runtime operator-review final bundle")
    if record.operator_review_summary != final_bundle.operator_review_summary:
        reasons.append("operator review summary does not match supplied runtime operator-review final bundle")
    if record.operator_review_summary != packet_bridge.operator_review_summary:
        reasons.append("operator review summary does not match fixture-only operator-review final-packet bridge")

    if record.fixture_only_operator_review_final_bundle_bridge_status is not FixtureOnlyOperatorReviewFinalBundleBridgeStatus.FIXTURE_ONLY_OPERATOR_REVIEW_FINAL_BUNDLE_BRIDGE_RECORDED:
        reasons.append(f"fixture-only operator-review final-bundle bridge status is {record.fixture_only_operator_review_final_bundle_bridge_status.value}")
    if record.fixture_only_operator_review_final_bundle_bridge_posture is not FixtureOnlyOperatorReviewFinalBundleBridgePosture.FIXTURE_ONLY_OPERATOR_REVIEW_FINAL_BUNDLE_BRIDGE_IN_MEMORY_ONLY:
        reasons.append(f"fixture-only operator-review final-bundle bridge posture is {record.fixture_only_operator_review_final_bundle_bridge_posture.value}")
    if record.operator_review_final_bundle_bridge_alignment_status is not OperatorReviewFinalBundleBridgeAlignmentStatus.OPERATOR_REVIEW_FINAL_BUNDLE_BRIDGE_ALIGNED:
        reasons.append(f"operator-review final-bundle bridge alignment status is {record.operator_review_final_bundle_bridge_alignment_status.value}")
    if record.no_lookahead_status is not NoLookaheadStatus.NO_LOOKAHEAD_RECORDED:
        reasons.append(f"no-lookahead status is {record.no_lookahead_status.value}")
    if record.operator_review_status is not OperatorReviewStatus.OPERATOR_REVIEW_REQUIRED:
        reasons.append(f"operator review status is {record.operator_review_status.value}")
    if record.runtime_gate_status is not RuntimeGateStatus.RUNTIME_GATE_READY:
        reasons.append(f"runtime gate status is {record.runtime_gate_status.value}")

    if reasons and not _is_nonblank_text(record.blocked_reason_summary):
        reasons.append("blocked_reason_summary is missing")
    if reasons:
        return FixtureOnlySourceProviderOperatorReviewFinalBundleBridgeValidationResult(
            severity=ValidationSeverity.BLOCKED,
            passed=False,
            reasons=tuple(reasons),
        )
    return FixtureOnlySourceProviderOperatorReviewFinalBundleBridgeValidationResult(
        severity=ValidationSeverity.PASSED,
        passed=True,
        reasons=(),
    )
