"""Pure fixture-only Weather Bot Stage 2 source/provider full-chain integration-smoke bridge runtime scaffold.

This module consumes only caller-supplied fixture-only completion-summary bridge
and supplied full-chain integration-smoke values. It is an in-memory metadata
record only. It validates supplied values but does not execute a smoke. It has
no live provider or source-fetching behavior, no APIs, scraping, downloads,
SDKs, credentials, config loading, or live ingestion, and no file or network
I/O. It performs no evidence generation, scoring, backtesting, execution,
simulation, report generation, smoke execution, integration-smoke execution, or
trace execution. It performs no handoff, acknowledgement, queue, final-packet,
final-bundle, completion-seal, completion-summary, or integration-smoke
delivery. It performs no generated packet, bundle, seal, summary, or smoke
behavior, no durable-seal or workflow-completion side effects, no real queue
service, scheduler, or broker, no persistence/export writing, no owner-decision
capture, no operator-decision execution, and no paper trading, trading,
autonomy, or production behavior.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping

from meg.weather.stage2.fixture_only_source_provider_operator_review_completion_summary_bridge_runtime import (
    FixtureOnlySourceProviderOperatorReviewCompletionSummaryBridgeRecord,
    fixture_only_source_provider_operator_review_completion_summary_bridge_record_from_mapping,
    validate_fixture_only_source_provider_operator_review_completion_summary_bridge_record,
)
from meg.weather.stage2.supplied_runtime_full_chain_integration_smoke import (
    SuppliedRuntimeFullChainIntegrationSmokeRecord,
    supplied_runtime_full_chain_integration_smoke_record_from_mapping,
    validate_supplied_runtime_full_chain_integration_smoke_record,
)


class _ClosedValue(str, Enum):
    """String enum base for closed, machine-checkable Stage 2 values."""

    @classmethod
    def values(cls) -> frozenset[str]:
        return frozenset(member.value for member in cls)


class FixtureOnlyFullChainIntegrationSmokeBridgeStatus(_ClosedValue):
    FIXTURE_ONLY_FULL_CHAIN_INTEGRATION_SMOKE_BRIDGE_RECORDED = "fixture_only_full_chain_integration_smoke_bridge_recorded"
    FIXTURE_ONLY_FULL_CHAIN_INTEGRATION_SMOKE_BRIDGE_MISSING = "fixture_only_full_chain_integration_smoke_bridge_missing"
    FIXTURE_ONLY_FULL_CHAIN_INTEGRATION_SMOKE_BRIDGE_AMBIGUOUS = "fixture_only_full_chain_integration_smoke_bridge_ambiguous"
    FIXTURE_ONLY_FULL_CHAIN_INTEGRATION_SMOKE_BRIDGE_UNSUPPORTED = "fixture_only_full_chain_integration_smoke_bridge_unsupported"
    FIXTURE_ONLY_FULL_CHAIN_INTEGRATION_SMOKE_BRIDGE_UNKNOWN = "fixture_only_full_chain_integration_smoke_bridge_unknown"


class FixtureOnlyFullChainIntegrationSmokeBridgePosture(_ClosedValue):
    FIXTURE_ONLY_FULL_CHAIN_INTEGRATION_SMOKE_BRIDGE_IN_MEMORY_ONLY = "fixture_only_full_chain_integration_smoke_bridge_in_memory_only"
    FIXTURE_ONLY_FULL_CHAIN_INTEGRATION_SMOKE_BRIDGE_MISSING = "fixture_only_full_chain_integration_smoke_bridge_missing"
    FIXTURE_ONLY_FULL_CHAIN_INTEGRATION_SMOKE_BRIDGE_AMBIGUOUS = "fixture_only_full_chain_integration_smoke_bridge_ambiguous"
    FIXTURE_ONLY_FULL_CHAIN_INTEGRATION_SMOKE_BRIDGE_UNSUPPORTED = "fixture_only_full_chain_integration_smoke_bridge_unsupported"
    FIXTURE_ONLY_FULL_CHAIN_INTEGRATION_SMOKE_BRIDGE_UNKNOWN = "fixture_only_full_chain_integration_smoke_bridge_unknown"


class FullChainIntegrationSmokeBridgeAlignmentStatus(_ClosedValue):
    FULL_CHAIN_INTEGRATION_SMOKE_BRIDGE_ALIGNED = "full_chain_integration_smoke_bridge_aligned"
    FULL_CHAIN_INTEGRATION_SMOKE_BRIDGE_MISMATCH = "full_chain_integration_smoke_bridge_mismatch"
    FULL_CHAIN_INTEGRATION_SMOKE_BRIDGE_MISSING = "full_chain_integration_smoke_bridge_missing"
    FULL_CHAIN_INTEGRATION_SMOKE_BRIDGE_AMBIGUOUS = "full_chain_integration_smoke_bridge_ambiguous"
    FULL_CHAIN_INTEGRATION_SMOKE_BRIDGE_UNKNOWN = "full_chain_integration_smoke_bridge_unknown"


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
class FixtureOnlySourceProviderFullChainIntegrationSmokeBridgeRecord:
    condition_id: str
    token_id: str
    outcome: str
    fixture_only_source_provider_operator_review_completion_summary_bridge: FixtureOnlySourceProviderOperatorReviewCompletionSummaryBridgeRecord
    supplied_runtime_full_chain_integration_smoke: SuppliedRuntimeFullChainIntegrationSmokeRecord
    full_chain_integration_smoke_bridge_id: str
    full_chain_integration_smoke_bridge_summary: str
    fixture_completion_summary_bridge_summary: str
    supplied_integration_smoke_summary: str
    operator_review_summary: str
    blocked_reason_summary: str
    fixture_only_full_chain_integration_smoke_bridge_status: FixtureOnlyFullChainIntegrationSmokeBridgeStatus
    fixture_only_full_chain_integration_smoke_bridge_posture: FixtureOnlyFullChainIntegrationSmokeBridgePosture
    full_chain_integration_smoke_bridge_alignment_status: FullChainIntegrationSmokeBridgeAlignmentStatus
    no_lookahead_status: NoLookaheadStatus
    operator_review_status: OperatorReviewStatus
    runtime_gate_status: RuntimeGateStatus
    provenance_notes: str = ""


@dataclass(frozen=True)
class FixtureOnlySourceProviderFullChainIntegrationSmokeBridgeValidationResult:
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


def _fixture_only_source_provider_operator_review_completion_summary_bridge_from_value(
    value: FixtureOnlySourceProviderOperatorReviewCompletionSummaryBridgeRecord | Mapping[str, Any],
) -> FixtureOnlySourceProviderOperatorReviewCompletionSummaryBridgeRecord:
    if isinstance(value, FixtureOnlySourceProviderOperatorReviewCompletionSummaryBridgeRecord):
        return value
    return fixture_only_source_provider_operator_review_completion_summary_bridge_record_from_mapping(value)


def _supplied_runtime_full_chain_integration_smoke_from_value(
    value: SuppliedRuntimeFullChainIntegrationSmokeRecord | Mapping[str, Any],
) -> SuppliedRuntimeFullChainIntegrationSmokeRecord:
    if isinstance(value, SuppliedRuntimeFullChainIntegrationSmokeRecord):
        return value
    return supplied_runtime_full_chain_integration_smoke_record_from_mapping(value)


def fixture_only_source_provider_full_chain_integration_smoke_bridge_record_from_mapping(
    mapping: Mapping[str, Any],
) -> FixtureOnlySourceProviderFullChainIntegrationSmokeBridgeRecord:
    """Build full-chain integration-smoke bridge metadata from supplied values."""

    return FixtureOnlySourceProviderFullChainIntegrationSmokeBridgeRecord(
        condition_id=mapping["condition_id"],
        token_id=mapping["token_id"],
        outcome=mapping["outcome"],
        fixture_only_source_provider_operator_review_completion_summary_bridge=(
            _fixture_only_source_provider_operator_review_completion_summary_bridge_from_value(
                mapping["fixture_only_source_provider_operator_review_completion_summary_bridge"]
            )
        ),
        supplied_runtime_full_chain_integration_smoke=(
            _supplied_runtime_full_chain_integration_smoke_from_value(
                mapping["supplied_runtime_full_chain_integration_smoke"]
            )
        ),
        full_chain_integration_smoke_bridge_id=mapping["full_chain_integration_smoke_bridge_id"],
        full_chain_integration_smoke_bridge_summary=mapping["full_chain_integration_smoke_bridge_summary"],
        fixture_completion_summary_bridge_summary=mapping["fixture_completion_summary_bridge_summary"],
        supplied_integration_smoke_summary=mapping["supplied_integration_smoke_summary"],
        operator_review_summary=mapping["operator_review_summary"],
        blocked_reason_summary=mapping["blocked_reason_summary"],
        fixture_only_full_chain_integration_smoke_bridge_status=_enum_value(
            FixtureOnlyFullChainIntegrationSmokeBridgeStatus,
            mapping["fixture_only_full_chain_integration_smoke_bridge_status"],
        ),
        fixture_only_full_chain_integration_smoke_bridge_posture=_enum_value(
            FixtureOnlyFullChainIntegrationSmokeBridgePosture,
            mapping["fixture_only_full_chain_integration_smoke_bridge_posture"],
        ),
        full_chain_integration_smoke_bridge_alignment_status=_enum_value(
            FullChainIntegrationSmokeBridgeAlignmentStatus,
            mapping["full_chain_integration_smoke_bridge_alignment_status"],
        ),
        no_lookahead_status=_enum_value(NoLookaheadStatus, mapping["no_lookahead_status"]),
        operator_review_status=_enum_value(OperatorReviewStatus, mapping["operator_review_status"]),
        runtime_gate_status=_enum_value(RuntimeGateStatus, mapping["runtime_gate_status"]),
        provenance_notes=str(mapping.get("provenance_notes", "")),
    )


def validate_fixture_only_source_provider_full_chain_integration_smoke_bridge_record(
    record: FixtureOnlySourceProviderFullChainIntegrationSmokeBridgeRecord,
) -> FixtureOnlySourceProviderFullChainIntegrationSmokeBridgeValidationResult:
    """Validate fixture-only full-chain integration-smoke bridge metadata fail-closed."""

    reasons: list[str] = []
    for field_name, value in (
        ("condition_id", record.condition_id),
        ("token_id", record.token_id),
        ("outcome", record.outcome),
        ("full_chain_integration_smoke_bridge_id", record.full_chain_integration_smoke_bridge_id),
        ("full_chain_integration_smoke_bridge_summary", record.full_chain_integration_smoke_bridge_summary),
        ("fixture_completion_summary_bridge_summary", record.fixture_completion_summary_bridge_summary),
        ("supplied_integration_smoke_summary", record.supplied_integration_smoke_summary),
        ("operator_review_summary", record.operator_review_summary),
    ):
        if not _is_nonblank_text(value):
            reasons.append(f"{field_name} is missing")

    bridge = record.fixture_only_source_provider_operator_review_completion_summary_bridge
    smoke = record.supplied_runtime_full_chain_integration_smoke
    bridge_summary = bridge.supplied_runtime_operator_review_completion_summary
    smoke_summary = smoke.supplied_runtime_operator_review_completion_summary
    bridge_seal = bridge_summary.supplied_runtime_operator_review_completion_seal
    smoke_seal = smoke_summary.supplied_runtime_operator_review_completion_seal
    bridge_bundle = bridge_seal.supplied_runtime_operator_review_final_bundle
    smoke_bundle = smoke_seal.supplied_runtime_operator_review_final_bundle
    bridge_packet = bridge_bundle.supplied_runtime_operator_review_final_packet
    smoke_packet = smoke_bundle.supplied_runtime_operator_review_final_packet
    bridge_queue_summary = bridge_packet.supplied_runtime_operator_review_queue_summary
    smoke_queue_summary = smoke_packet.supplied_runtime_operator_review_queue_summary
    bridge_entry = bridge_queue_summary.supplied_runtime_operator_review_queue_entry
    smoke_entry = smoke_queue_summary.supplied_runtime_operator_review_queue_entry
    bridge_queue = bridge_entry.supplied_runtime_operator_review_queue_packet
    smoke_queue = smoke_entry.supplied_runtime_operator_review_queue_packet
    bridge_ack = bridge_queue.supplied_runtime_operator_review_ack_packet
    smoke_ack = smoke_queue.supplied_runtime_operator_review_ack_packet
    bridge_handoff = bridge_ack.supplied_runtime_operator_review_handoff
    smoke_handoff = smoke_ack.supplied_runtime_operator_review_handoff
    bridge_trace = bridge_handoff.supplied_runtime_trace_packet
    smoke_trace = smoke_handoff.supplied_runtime_trace_packet
    bridge_smoke = bridge_trace.supplied_runtime_end_to_end_smoke
    smoke_smoke = smoke_trace.supplied_runtime_end_to_end_smoke
    bridge_report = bridge_smoke.supplied_runtime_dry_run_report
    smoke_report = smoke_smoke.supplied_runtime_dry_run_report
    bridge_dry = bridge_report.supplied_runtime_dry_run_packet
    smoke_dry = smoke_report.supplied_runtime_dry_run_packet
    bridge_validation = bridge_dry.supplied_runtime_validation_bundle
    smoke_validation = smoke_dry.supplied_runtime_validation_bundle
    bridge_evidence = bridge_validation.supplied_evidence_packet
    smoke_evidence = smoke_validation.supplied_evidence_packet

    if not validate_fixture_only_source_provider_operator_review_completion_summary_bridge_record(bridge).passed:
        reasons.append("fixture-only source provider operator-review completion-summary bridge is invalid")
    if not validate_supplied_runtime_full_chain_integration_smoke_record(smoke).passed:
        reasons.append("supplied runtime full-chain integration smoke is invalid")

    for field_name in ("condition_id", "token_id", "outcome"):
        if getattr(record, field_name) != getattr(bridge, field_name):
            reasons.append(f"{field_name} does not match fixture-only operator-review completion-summary bridge")
        if getattr(record, field_name) != getattr(smoke, field_name):
            reasons.append(f"{field_name} does not match supplied runtime full-chain integration smoke")

    if not _same_route(bridge, smoke):
        reasons.append("nested fixture-only operator-review completion-summary bridge and supplied runtime full-chain integration smoke routes do not match")
    if not _same_route(bridge_summary, smoke_summary):
        reasons.append("nested supplied runtime operator-review completion summaries do not match")
    if not _same_route(bridge_seal, smoke_seal):
        reasons.append("nested supplied runtime operator-review completion seals do not match")
    if not _same_route(bridge_bundle, smoke_bundle):
        reasons.append("nested supplied runtime operator-review final bundles do not match")
    if not _same_route(bridge_packet, smoke_packet):
        reasons.append("nested supplied runtime operator-review final packets do not match")
    if not _same_route(bridge_queue_summary, smoke_queue_summary):
        reasons.append("nested supplied runtime operator-review queue summaries do not match")
    if not _same_route(bridge_entry, smoke_entry):
        reasons.append("nested supplied runtime operator-review queue entries do not match")
    if not _same_route(bridge_queue, smoke_queue):
        reasons.append("nested supplied runtime operator-review queue packets do not match")
    if not _same_route(bridge_ack, smoke_ack):
        reasons.append("nested supplied runtime operator-review ack packets do not match")
    if not _same_route(bridge_handoff, smoke_handoff):
        reasons.append("nested supplied runtime operator-review handoffs do not match")
    if not _same_route(bridge_trace, smoke_trace):
        reasons.append("nested supplied runtime trace packets do not match")
    if not _same_route(bridge_smoke, smoke_smoke):
        reasons.append("nested supplied runtime end-to-end smokes do not match")
    if not _same_route(bridge_report, smoke_report):
        reasons.append("nested supplied runtime dry-run reports do not match")
    if not _same_route(bridge_dry, smoke_dry) or not _same_route(bridge_validation, smoke_validation):
        reasons.append("nested supplied runtime dry-run packets do not match")
    if not _same_route(bridge_evidence, smoke_evidence) or not _same_route(
        bridge_evidence.supplied_market_contract,
        smoke_evidence.supplied_market_contract,
    ):
        reasons.append("nested supplied evidence packets do not match")

    if record.fixture_completion_summary_bridge_summary != bridge.operator_review_completion_summary_bridge_summary:
        reasons.append("fixture completion-summary bridge summary does not match fixture-only operator-review completion-summary bridge")
    if record.supplied_integration_smoke_summary != smoke.integration_smoke_summary:
        reasons.append("supplied integration smoke summary does not match supplied runtime full-chain integration smoke")
    if record.operator_review_summary != bridge.operator_review_summary:
        reasons.append("operator review summary does not match fixture-only operator-review completion-summary bridge")
    if record.operator_review_summary != smoke.operator_review_summary:
        reasons.append("operator review summary does not match supplied runtime full-chain integration smoke")

    if record.fixture_only_full_chain_integration_smoke_bridge_status is not FixtureOnlyFullChainIntegrationSmokeBridgeStatus.FIXTURE_ONLY_FULL_CHAIN_INTEGRATION_SMOKE_BRIDGE_RECORDED:
        reasons.append(f"fixture-only full-chain integration-smoke bridge status is {record.fixture_only_full_chain_integration_smoke_bridge_status.value}")
    if record.fixture_only_full_chain_integration_smoke_bridge_posture is not FixtureOnlyFullChainIntegrationSmokeBridgePosture.FIXTURE_ONLY_FULL_CHAIN_INTEGRATION_SMOKE_BRIDGE_IN_MEMORY_ONLY:
        reasons.append(f"fixture-only full-chain integration-smoke bridge posture is {record.fixture_only_full_chain_integration_smoke_bridge_posture.value}")
    if record.full_chain_integration_smoke_bridge_alignment_status is not FullChainIntegrationSmokeBridgeAlignmentStatus.FULL_CHAIN_INTEGRATION_SMOKE_BRIDGE_ALIGNED:
        reasons.append(f"full-chain integration-smoke bridge alignment status is {record.full_chain_integration_smoke_bridge_alignment_status.value}")
    if record.no_lookahead_status is not NoLookaheadStatus.NO_LOOKAHEAD_RECORDED:
        reasons.append(f"no-lookahead status is {record.no_lookahead_status.value}")
    if record.operator_review_status is not OperatorReviewStatus.OPERATOR_REVIEW_REQUIRED:
        reasons.append(f"operator review status is {record.operator_review_status.value}")
    if record.runtime_gate_status is not RuntimeGateStatus.RUNTIME_GATE_READY:
        reasons.append(f"runtime gate status is {record.runtime_gate_status.value}")

    if reasons and not _is_nonblank_text(record.blocked_reason_summary):
        reasons.append("blocked_reason_summary is missing")
    if reasons:
        return FixtureOnlySourceProviderFullChainIntegrationSmokeBridgeValidationResult(
            severity=ValidationSeverity.BLOCKED,
            passed=False,
            reasons=tuple(reasons),
        )
    return FixtureOnlySourceProviderFullChainIntegrationSmokeBridgeValidationResult(
        severity=ValidationSeverity.PASSED,
        passed=True,
        reasons=(),
    )
