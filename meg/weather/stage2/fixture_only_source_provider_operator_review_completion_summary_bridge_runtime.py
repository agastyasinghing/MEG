"""Pure fixture-only Weather Bot Stage 2 source/provider operator-review completion-summary bridge runtime scaffold.

This module consumes only caller-supplied fixture-only completion-seal bridge and
supplied completion-summary values. It is an in-memory record only. It performs
no live provider or source-fetching behavior, APIs, scraping, downloads, SDKs,
credentials, config loading, or live ingestion, file or network I/O, evidence
generation, scoring, backtesting, execution, simulation, report generation,
smoke execution, trace execution, handoff delivery, ack delivery, queue delivery,
final-packet delivery, final-bundle delivery, completion-seal delivery, or
completion-summary delivery. It performs no generated packet, bundle, seal, or
summary behavior, durable-seal side effects, workflow-completion side effects,
real queue service, scheduler, broker, persistence/export writing,
owner-decision capture, operator-decision execution, paper trading, trading,
autonomy, or production behavior.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping

from meg.weather.stage2.fixture_only_source_provider_operator_review_completion_seal_bridge_runtime import (
    FixtureOnlySourceProviderOperatorReviewCompletionSealBridgeRecord,
    fixture_only_source_provider_operator_review_completion_seal_bridge_record_from_mapping,
    validate_fixture_only_source_provider_operator_review_completion_seal_bridge_record,
)
from meg.weather.stage2.supplied_runtime_operator_review_completion_summary import (
    SuppliedRuntimeOperatorReviewCompletionSummaryRecord,
    supplied_runtime_operator_review_completion_summary_record_from_mapping,
    validate_supplied_runtime_operator_review_completion_summary_record,
)


class _ClosedValue(str, Enum):
    """String enum base for closed, machine-checkable Stage 2 values."""

    @classmethod
    def values(cls) -> frozenset[str]:
        return frozenset(member.value for member in cls)


class FixtureOnlyOperatorReviewCompletionSummaryBridgeStatus(_ClosedValue):
    FIXTURE_ONLY_OPERATOR_REVIEW_COMPLETION_SUMMARY_BRIDGE_RECORDED = "fixture_only_operator_review_completion_summary_bridge_recorded"
    FIXTURE_ONLY_OPERATOR_REVIEW_COMPLETION_SUMMARY_BRIDGE_MISSING = "fixture_only_operator_review_completion_summary_bridge_missing"
    FIXTURE_ONLY_OPERATOR_REVIEW_COMPLETION_SUMMARY_BRIDGE_AMBIGUOUS = "fixture_only_operator_review_completion_summary_bridge_ambiguous"
    FIXTURE_ONLY_OPERATOR_REVIEW_COMPLETION_SUMMARY_BRIDGE_UNSUPPORTED = "fixture_only_operator_review_completion_summary_bridge_unsupported"
    FIXTURE_ONLY_OPERATOR_REVIEW_COMPLETION_SUMMARY_BRIDGE_UNKNOWN = "fixture_only_operator_review_completion_summary_bridge_unknown"


class FixtureOnlyOperatorReviewCompletionSummaryBridgePosture(_ClosedValue):
    FIXTURE_ONLY_OPERATOR_REVIEW_COMPLETION_SUMMARY_BRIDGE_IN_MEMORY_ONLY = "fixture_only_operator_review_completion_summary_bridge_in_memory_only"
    FIXTURE_ONLY_OPERATOR_REVIEW_COMPLETION_SUMMARY_BRIDGE_MISSING = "fixture_only_operator_review_completion_summary_bridge_missing"
    FIXTURE_ONLY_OPERATOR_REVIEW_COMPLETION_SUMMARY_BRIDGE_AMBIGUOUS = "fixture_only_operator_review_completion_summary_bridge_ambiguous"
    FIXTURE_ONLY_OPERATOR_REVIEW_COMPLETION_SUMMARY_BRIDGE_UNSUPPORTED = "fixture_only_operator_review_completion_summary_bridge_unsupported"
    FIXTURE_ONLY_OPERATOR_REVIEW_COMPLETION_SUMMARY_BRIDGE_UNKNOWN = "fixture_only_operator_review_completion_summary_bridge_unknown"


class OperatorReviewCompletionSummaryBridgeAlignmentStatus(_ClosedValue):
    OPERATOR_REVIEW_COMPLETION_SUMMARY_BRIDGE_ALIGNED = "operator_review_completion_summary_bridge_aligned"
    OPERATOR_REVIEW_COMPLETION_SUMMARY_BRIDGE_MISMATCH = "operator_review_completion_summary_bridge_mismatch"
    OPERATOR_REVIEW_COMPLETION_SUMMARY_BRIDGE_MISSING = "operator_review_completion_summary_bridge_missing"
    OPERATOR_REVIEW_COMPLETION_SUMMARY_BRIDGE_AMBIGUOUS = "operator_review_completion_summary_bridge_ambiguous"
    OPERATOR_REVIEW_COMPLETION_SUMMARY_BRIDGE_UNKNOWN = "operator_review_completion_summary_bridge_unknown"


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
class FixtureOnlySourceProviderOperatorReviewCompletionSummaryBridgeRecord:
    condition_id: str
    token_id: str
    outcome: str
    fixture_only_source_provider_operator_review_completion_seal_bridge: FixtureOnlySourceProviderOperatorReviewCompletionSealBridgeRecord
    supplied_runtime_operator_review_completion_summary: SuppliedRuntimeOperatorReviewCompletionSummaryRecord
    operator_review_completion_summary_bridge_id: str
    operator_review_completion_summary_bridge_summary: str
    fixture_completion_seal_bridge_summary: str
    supplied_completion_summary_text: str
    operator_review_summary: str
    blocked_reason_summary: str
    fixture_only_operator_review_completion_summary_bridge_status: FixtureOnlyOperatorReviewCompletionSummaryBridgeStatus
    fixture_only_operator_review_completion_summary_bridge_posture: FixtureOnlyOperatorReviewCompletionSummaryBridgePosture
    operator_review_completion_summary_bridge_alignment_status: OperatorReviewCompletionSummaryBridgeAlignmentStatus
    no_lookahead_status: NoLookaheadStatus
    operator_review_status: OperatorReviewStatus
    runtime_gate_status: RuntimeGateStatus
    provenance_notes: str = ""


@dataclass(frozen=True)
class FixtureOnlySourceProviderOperatorReviewCompletionSummaryBridgeValidationResult:
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


def _fixture_only_source_provider_operator_review_completion_seal_bridge_from_value(
    value: FixtureOnlySourceProviderOperatorReviewCompletionSealBridgeRecord | Mapping[str, Any],
) -> FixtureOnlySourceProviderOperatorReviewCompletionSealBridgeRecord:
    if isinstance(value, FixtureOnlySourceProviderOperatorReviewCompletionSealBridgeRecord):
        return value
    return fixture_only_source_provider_operator_review_completion_seal_bridge_record_from_mapping(value)


def _supplied_runtime_operator_review_completion_summary_from_value(
    value: SuppliedRuntimeOperatorReviewCompletionSummaryRecord | Mapping[str, Any],
) -> SuppliedRuntimeOperatorReviewCompletionSummaryRecord:
    if isinstance(value, SuppliedRuntimeOperatorReviewCompletionSummaryRecord):
        return value
    return supplied_runtime_operator_review_completion_summary_record_from_mapping(value)


def fixture_only_source_provider_operator_review_completion_summary_bridge_record_from_mapping(
    mapping: Mapping[str, Any],
) -> FixtureOnlySourceProviderOperatorReviewCompletionSummaryBridgeRecord:
    """Build operator-review completion-summary bridge metadata from supplied values."""

    return FixtureOnlySourceProviderOperatorReviewCompletionSummaryBridgeRecord(
        condition_id=mapping["condition_id"],
        token_id=mapping["token_id"],
        outcome=mapping["outcome"],
        fixture_only_source_provider_operator_review_completion_seal_bridge=(
            _fixture_only_source_provider_operator_review_completion_seal_bridge_from_value(
                mapping["fixture_only_source_provider_operator_review_completion_seal_bridge"]
            )
        ),
        supplied_runtime_operator_review_completion_summary=(
            _supplied_runtime_operator_review_completion_summary_from_value(
                mapping["supplied_runtime_operator_review_completion_summary"]
            )
        ),
        operator_review_completion_summary_bridge_id=mapping["operator_review_completion_summary_bridge_id"],
        operator_review_completion_summary_bridge_summary=mapping["operator_review_completion_summary_bridge_summary"],
        fixture_completion_seal_bridge_summary=mapping["fixture_completion_seal_bridge_summary"],
        supplied_completion_summary_text=mapping["supplied_completion_summary_text"],
        operator_review_summary=mapping["operator_review_summary"],
        blocked_reason_summary=mapping["blocked_reason_summary"],
        fixture_only_operator_review_completion_summary_bridge_status=_enum_value(
            FixtureOnlyOperatorReviewCompletionSummaryBridgeStatus,
            mapping["fixture_only_operator_review_completion_summary_bridge_status"],
        ),
        fixture_only_operator_review_completion_summary_bridge_posture=_enum_value(
            FixtureOnlyOperatorReviewCompletionSummaryBridgePosture,
            mapping["fixture_only_operator_review_completion_summary_bridge_posture"],
        ),
        operator_review_completion_summary_bridge_alignment_status=_enum_value(
            OperatorReviewCompletionSummaryBridgeAlignmentStatus,
            mapping["operator_review_completion_summary_bridge_alignment_status"],
        ),
        no_lookahead_status=_enum_value(NoLookaheadStatus, mapping["no_lookahead_status"]),
        operator_review_status=_enum_value(OperatorReviewStatus, mapping["operator_review_status"]),
        runtime_gate_status=_enum_value(RuntimeGateStatus, mapping["runtime_gate_status"]),
        provenance_notes=str(mapping.get("provenance_notes", "")),
    )


def validate_fixture_only_source_provider_operator_review_completion_summary_bridge_record(
    record: FixtureOnlySourceProviderOperatorReviewCompletionSummaryBridgeRecord,
) -> FixtureOnlySourceProviderOperatorReviewCompletionSummaryBridgeValidationResult:
    """Validate fixture-only operator-review completion-summary bridge metadata fail-closed."""

    reasons: list[str] = []
    for field_name, value in (
        ("condition_id", record.condition_id),
        ("token_id", record.token_id),
        ("outcome", record.outcome),
        ("operator_review_completion_summary_bridge_id", record.operator_review_completion_summary_bridge_id),
        ("operator_review_completion_summary_bridge_summary", record.operator_review_completion_summary_bridge_summary),
        ("fixture_completion_seal_bridge_summary", record.fixture_completion_seal_bridge_summary),
        ("supplied_completion_summary_text", record.supplied_completion_summary_text),
        ("operator_review_summary", record.operator_review_summary),
    ):
        if not _is_nonblank_text(value):
            reasons.append(f"{field_name} is missing")

    bridge = record.fixture_only_source_provider_operator_review_completion_seal_bridge
    summary = record.supplied_runtime_operator_review_completion_summary
    bridge_seal = bridge.supplied_runtime_operator_review_completion_seal
    summary_seal = summary.supplied_runtime_operator_review_completion_seal
    bridge_bundle = bridge_seal.supplied_runtime_operator_review_final_bundle
    summary_bundle = summary_seal.supplied_runtime_operator_review_final_bundle
    bridge_packet = bridge_bundle.supplied_runtime_operator_review_final_packet
    summary_packet = summary_bundle.supplied_runtime_operator_review_final_packet
    bridge_queue_summary = bridge_packet.supplied_runtime_operator_review_queue_summary
    summary_queue_summary = summary_packet.supplied_runtime_operator_review_queue_summary
    bridge_entry = bridge_queue_summary.supplied_runtime_operator_review_queue_entry
    summary_entry = summary_queue_summary.supplied_runtime_operator_review_queue_entry
    bridge_queue = bridge_entry.supplied_runtime_operator_review_queue_packet
    summary_queue = summary_entry.supplied_runtime_operator_review_queue_packet
    bridge_ack = bridge_queue.supplied_runtime_operator_review_ack_packet
    summary_ack = summary_queue.supplied_runtime_operator_review_ack_packet
    bridge_handoff = bridge_ack.supplied_runtime_operator_review_handoff
    summary_handoff = summary_ack.supplied_runtime_operator_review_handoff
    bridge_trace = bridge_handoff.supplied_runtime_trace_packet
    summary_trace = summary_handoff.supplied_runtime_trace_packet
    bridge_smoke = bridge_trace.supplied_runtime_end_to_end_smoke
    summary_smoke = summary_trace.supplied_runtime_end_to_end_smoke
    bridge_report = bridge_smoke.supplied_runtime_dry_run_report
    summary_report = summary_smoke.supplied_runtime_dry_run_report
    bridge_dry = bridge_report.supplied_runtime_dry_run_packet
    summary_dry = summary_report.supplied_runtime_dry_run_packet
    bridge_validation = bridge_dry.supplied_runtime_validation_bundle
    summary_validation = summary_dry.supplied_runtime_validation_bundle
    bridge_evidence = bridge_validation.supplied_evidence_packet
    summary_evidence = summary_validation.supplied_evidence_packet

    if not validate_fixture_only_source_provider_operator_review_completion_seal_bridge_record(bridge).passed:
        reasons.append("fixture-only source provider operator-review completion-seal bridge is invalid")
    if not validate_supplied_runtime_operator_review_completion_summary_record(summary).passed:
        reasons.append("supplied runtime operator-review completion summary is invalid")

    if record.condition_id != bridge.condition_id:
        reasons.append("condition_id does not match fixture-only operator-review completion-seal bridge")
    if record.token_id != bridge.token_id:
        reasons.append("token_id does not match fixture-only operator-review completion-seal bridge")
    if record.outcome != bridge.outcome:
        reasons.append("outcome does not match fixture-only operator-review completion-seal bridge")
    if record.condition_id != summary.condition_id:
        reasons.append("condition_id does not match supplied runtime operator-review completion summary")
    if record.token_id != summary.token_id:
        reasons.append("token_id does not match supplied runtime operator-review completion summary")
    if record.outcome != summary.outcome:
        reasons.append("outcome does not match supplied runtime operator-review completion summary")

    if not _same_route(bridge, summary):
        reasons.append("nested fixture-only operator-review completion-seal bridge and supplied runtime operator-review completion summary routes do not match")
    if not _same_route(bridge_seal, summary_seal):
        reasons.append("nested supplied runtime operator-review completion seals do not match")
    if not _same_route(bridge_bundle, summary_bundle):
        reasons.append("nested supplied runtime operator-review final bundles do not match")
    if not _same_route(bridge_packet, summary_packet):
        reasons.append("nested supplied runtime operator-review final packets do not match")
    if not _same_route(bridge_queue_summary, summary_queue_summary):
        reasons.append("nested supplied runtime operator-review queue summaries do not match")
    if not _same_route(bridge_entry, summary_entry):
        reasons.append("nested supplied runtime operator-review queue entries do not match")
    if not _same_route(bridge_queue, summary_queue):
        reasons.append("nested supplied runtime operator-review queue packets do not match")
    if not _same_route(bridge_ack, summary_ack):
        reasons.append("nested supplied runtime operator-review ack packets do not match")
    if not _same_route(bridge_handoff, summary_handoff):
        reasons.append("nested supplied runtime operator-review handoffs do not match")
    if not _same_route(bridge_trace, summary_trace):
        reasons.append("nested supplied runtime trace packets do not match")
    if not _same_route(bridge_smoke, summary_smoke):
        reasons.append("nested supplied runtime end-to-end smokes do not match")
    if not _same_route(bridge_report, summary_report):
        reasons.append("nested supplied runtime dry-run reports do not match")
    if not _same_route(bridge_dry, summary_dry) or not _same_route(bridge_validation, summary_validation):
        reasons.append("nested supplied runtime dry-run packets do not match")
    if not _same_route(bridge_evidence, summary_evidence) or not _same_route(
        bridge_evidence.supplied_market_contract,
        summary_evidence.supplied_market_contract,
    ):
        reasons.append("nested supplied evidence packets do not match")

    if record.fixture_completion_seal_bridge_summary != bridge.operator_review_completion_seal_bridge_summary:
        reasons.append("fixture completion-seal bridge summary does not match fixture-only operator-review completion-seal bridge")
    if record.supplied_completion_summary_text != summary.completion_summary_text:
        reasons.append("supplied completion summary text does not match supplied runtime operator-review completion summary")
    if record.operator_review_summary != bridge.operator_review_summary:
        reasons.append("operator review summary does not match fixture-only operator-review completion-seal bridge")
    if record.operator_review_summary != summary.operator_review_summary:
        reasons.append("operator review summary does not match supplied runtime operator-review completion summary")

    if record.fixture_only_operator_review_completion_summary_bridge_status is not FixtureOnlyOperatorReviewCompletionSummaryBridgeStatus.FIXTURE_ONLY_OPERATOR_REVIEW_COMPLETION_SUMMARY_BRIDGE_RECORDED:
        reasons.append(f"fixture-only operator-review completion-summary bridge status is {record.fixture_only_operator_review_completion_summary_bridge_status.value}")
    if record.fixture_only_operator_review_completion_summary_bridge_posture is not FixtureOnlyOperatorReviewCompletionSummaryBridgePosture.FIXTURE_ONLY_OPERATOR_REVIEW_COMPLETION_SUMMARY_BRIDGE_IN_MEMORY_ONLY:
        reasons.append(f"fixture-only operator-review completion-summary bridge posture is {record.fixture_only_operator_review_completion_summary_bridge_posture.value}")
    if record.operator_review_completion_summary_bridge_alignment_status is not OperatorReviewCompletionSummaryBridgeAlignmentStatus.OPERATOR_REVIEW_COMPLETION_SUMMARY_BRIDGE_ALIGNED:
        reasons.append(f"operator-review completion-summary bridge alignment status is {record.operator_review_completion_summary_bridge_alignment_status.value}")
    if record.no_lookahead_status is not NoLookaheadStatus.NO_LOOKAHEAD_RECORDED:
        reasons.append(f"no-lookahead status is {record.no_lookahead_status.value}")
    if record.operator_review_status is not OperatorReviewStatus.OPERATOR_REVIEW_REQUIRED:
        reasons.append(f"operator review status is {record.operator_review_status.value}")
    if record.runtime_gate_status is not RuntimeGateStatus.RUNTIME_GATE_READY:
        reasons.append(f"runtime gate status is {record.runtime_gate_status.value}")

    if reasons and not _is_nonblank_text(record.blocked_reason_summary):
        reasons.append("blocked_reason_summary is missing")
    if reasons:
        return FixtureOnlySourceProviderOperatorReviewCompletionSummaryBridgeValidationResult(
            severity=ValidationSeverity.BLOCKED,
            passed=False,
            reasons=tuple(reasons),
        )
    return FixtureOnlySourceProviderOperatorReviewCompletionSummaryBridgeValidationResult(
        severity=ValidationSeverity.PASSED,
        passed=True,
        reasons=(),
    )
