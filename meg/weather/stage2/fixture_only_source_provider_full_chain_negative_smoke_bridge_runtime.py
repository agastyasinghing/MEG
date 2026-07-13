"""Pure fixture-only Weather Bot Stage 2 source/provider full-chain negative-smoke bridge runtime scaffold.

This module consumes only caller-supplied fixture-only positive
integration-smoke bridge and supplied negative-smoke values. It is an in-memory
metadata record only. It confirms supplied expected fail-closed metadata without
executing or generating a smoke. A valid negative-smoke bridge remains
runtime-gate blocked. It has no live providers or fetching, no APIs, scraping,
downloads, SDKs, credentials, config loading, or live ingestion, and no file or
network I/O. It performs no evidence generation, scoring, backtesting, dry-run
execution, simulation, report generation, smoke execution, integration-smoke
execution, negative-smoke execution, or trace execution. It performs no failure
injection or generated failure behavior, no generated packet, bundle, seal,
summary, or smoke behavior, no delivery behavior, no real queue service,
scheduler, or broker, no durable-seal or workflow-completion side effects, no
persistence/export writing, no owner-decision capture, no operator-decision
execution, and no paper trading, trading, autonomy, or production behavior.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping

from meg.weather.stage2.fixture_only_source_provider_full_chain_integration_smoke_bridge_runtime import (
    FixtureOnlySourceProviderFullChainIntegrationSmokeBridgeRecord,
    fixture_only_source_provider_full_chain_integration_smoke_bridge_record_from_mapping,
    validate_fixture_only_source_provider_full_chain_integration_smoke_bridge_record,
)
from meg.weather.stage2.supplied_runtime_full_chain_negative_smoke import (
    SuppliedRuntimeFullChainNegativeSmokeRecord,
    supplied_runtime_full_chain_negative_smoke_record_from_mapping,
    validate_supplied_runtime_full_chain_negative_smoke_record,
)


class _ClosedValue(str, Enum):
    """String enum base for closed, machine-checkable Stage 2 values."""

    @classmethod
    def values(cls) -> frozenset[str]:
        return frozenset(member.value for member in cls)


class FixtureOnlyFullChainNegativeSmokeBridgeStatus(_ClosedValue):
    FIXTURE_ONLY_FULL_CHAIN_NEGATIVE_SMOKE_BRIDGE_RECORDED = "fixture_only_full_chain_negative_smoke_bridge_recorded"
    FIXTURE_ONLY_FULL_CHAIN_NEGATIVE_SMOKE_BRIDGE_MISSING = "fixture_only_full_chain_negative_smoke_bridge_missing"
    FIXTURE_ONLY_FULL_CHAIN_NEGATIVE_SMOKE_BRIDGE_AMBIGUOUS = "fixture_only_full_chain_negative_smoke_bridge_ambiguous"
    FIXTURE_ONLY_FULL_CHAIN_NEGATIVE_SMOKE_BRIDGE_UNSUPPORTED = "fixture_only_full_chain_negative_smoke_bridge_unsupported"
    FIXTURE_ONLY_FULL_CHAIN_NEGATIVE_SMOKE_BRIDGE_UNKNOWN = "fixture_only_full_chain_negative_smoke_bridge_unknown"


class FixtureOnlyFullChainNegativeSmokeBridgePosture(_ClosedValue):
    FIXTURE_ONLY_FULL_CHAIN_NEGATIVE_SMOKE_BRIDGE_IN_MEMORY_ONLY = "fixture_only_full_chain_negative_smoke_bridge_in_memory_only"
    FIXTURE_ONLY_FULL_CHAIN_NEGATIVE_SMOKE_BRIDGE_MISSING = "fixture_only_full_chain_negative_smoke_bridge_missing"
    FIXTURE_ONLY_FULL_CHAIN_NEGATIVE_SMOKE_BRIDGE_AMBIGUOUS = "fixture_only_full_chain_negative_smoke_bridge_ambiguous"
    FIXTURE_ONLY_FULL_CHAIN_NEGATIVE_SMOKE_BRIDGE_UNSUPPORTED = "fixture_only_full_chain_negative_smoke_bridge_unsupported"
    FIXTURE_ONLY_FULL_CHAIN_NEGATIVE_SMOKE_BRIDGE_UNKNOWN = "fixture_only_full_chain_negative_smoke_bridge_unknown"


class FullChainNegativeSmokeBridgeAlignmentStatus(_ClosedValue):
    FULL_CHAIN_NEGATIVE_SMOKE_BRIDGE_ALIGNED = "full_chain_negative_smoke_bridge_aligned"
    FULL_CHAIN_NEGATIVE_SMOKE_BRIDGE_MISMATCH = "full_chain_negative_smoke_bridge_mismatch"
    FULL_CHAIN_NEGATIVE_SMOKE_BRIDGE_MISSING = "full_chain_negative_smoke_bridge_missing"
    FULL_CHAIN_NEGATIVE_SMOKE_BRIDGE_AMBIGUOUS = "full_chain_negative_smoke_bridge_ambiguous"
    FULL_CHAIN_NEGATIVE_SMOKE_BRIDGE_UNKNOWN = "full_chain_negative_smoke_bridge_unknown"


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
    RUNTIME_GATE_BLOCKED = "runtime_gate_blocked"
    RUNTIME_GATE_READY = "runtime_gate_ready"
    RUNTIME_GATE_REQUIRES_MANUAL_REVIEW = "runtime_gate_requires_manual_review"
    RUNTIME_GATE_UNKNOWN = "runtime_gate_unknown"


class ValidationSeverity(_ClosedValue):
    PASSED = "passed"
    CAUTION = "caution"
    FAILED = "failed"
    BLOCKED = "blocked"


@dataclass(frozen=True)
class FixtureOnlySourceProviderFullChainNegativeSmokeBridgeRecord:
    condition_id: str
    token_id: str
    outcome: str
    fixture_only_source_provider_full_chain_integration_smoke_bridge: FixtureOnlySourceProviderFullChainIntegrationSmokeBridgeRecord
    supplied_runtime_full_chain_negative_smoke: SuppliedRuntimeFullChainNegativeSmokeRecord
    full_chain_negative_smoke_bridge_id: str
    full_chain_negative_smoke_bridge_summary: str
    fixture_integration_smoke_bridge_summary: str
    supplied_negative_smoke_summary: str
    expected_failure_reason_summary: str
    observed_failure_reason_summary: str
    operator_review_summary: str
    blocked_reason_summary: str
    fixture_only_full_chain_negative_smoke_bridge_status: FixtureOnlyFullChainNegativeSmokeBridgeStatus
    fixture_only_full_chain_negative_smoke_bridge_posture: FixtureOnlyFullChainNegativeSmokeBridgePosture
    full_chain_negative_smoke_bridge_alignment_status: FullChainNegativeSmokeBridgeAlignmentStatus
    no_lookahead_status: NoLookaheadStatus
    operator_review_status: OperatorReviewStatus
    runtime_gate_status: RuntimeGateStatus
    provenance_notes: str = ""


@dataclass(frozen=True)
class FixtureOnlySourceProviderFullChainNegativeSmokeBridgeValidationResult:
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


def _fixture_only_source_provider_full_chain_integration_smoke_bridge_from_value(
    value: FixtureOnlySourceProviderFullChainIntegrationSmokeBridgeRecord | Mapping[str, Any],
) -> FixtureOnlySourceProviderFullChainIntegrationSmokeBridgeRecord:
    if isinstance(value, FixtureOnlySourceProviderFullChainIntegrationSmokeBridgeRecord):
        return value
    return fixture_only_source_provider_full_chain_integration_smoke_bridge_record_from_mapping(value)


def _supplied_runtime_full_chain_negative_smoke_from_value(
    value: SuppliedRuntimeFullChainNegativeSmokeRecord | Mapping[str, Any],
) -> SuppliedRuntimeFullChainNegativeSmokeRecord:
    if isinstance(value, SuppliedRuntimeFullChainNegativeSmokeRecord):
        return value
    return supplied_runtime_full_chain_negative_smoke_record_from_mapping(value)


def fixture_only_source_provider_full_chain_negative_smoke_bridge_record_from_mapping(
    mapping: Mapping[str, Any],
) -> FixtureOnlySourceProviderFullChainNegativeSmokeBridgeRecord:
    """Build full-chain negative-smoke bridge metadata from supplied values."""

    return FixtureOnlySourceProviderFullChainNegativeSmokeBridgeRecord(
        condition_id=mapping["condition_id"],
        token_id=mapping["token_id"],
        outcome=mapping["outcome"],
        fixture_only_source_provider_full_chain_integration_smoke_bridge=(
            _fixture_only_source_provider_full_chain_integration_smoke_bridge_from_value(
                mapping["fixture_only_source_provider_full_chain_integration_smoke_bridge"]
            )
        ),
        supplied_runtime_full_chain_negative_smoke=_supplied_runtime_full_chain_negative_smoke_from_value(
            mapping["supplied_runtime_full_chain_negative_smoke"]
        ),
        full_chain_negative_smoke_bridge_id=mapping["full_chain_negative_smoke_bridge_id"],
        full_chain_negative_smoke_bridge_summary=mapping["full_chain_negative_smoke_bridge_summary"],
        fixture_integration_smoke_bridge_summary=mapping["fixture_integration_smoke_bridge_summary"],
        supplied_negative_smoke_summary=mapping["supplied_negative_smoke_summary"],
        expected_failure_reason_summary=mapping["expected_failure_reason_summary"],
        observed_failure_reason_summary=mapping["observed_failure_reason_summary"],
        operator_review_summary=mapping["operator_review_summary"],
        blocked_reason_summary=mapping["blocked_reason_summary"],
        fixture_only_full_chain_negative_smoke_bridge_status=_enum_value(
            FixtureOnlyFullChainNegativeSmokeBridgeStatus,
            mapping["fixture_only_full_chain_negative_smoke_bridge_status"],
        ),
        fixture_only_full_chain_negative_smoke_bridge_posture=_enum_value(
            FixtureOnlyFullChainNegativeSmokeBridgePosture,
            mapping["fixture_only_full_chain_negative_smoke_bridge_posture"],
        ),
        full_chain_negative_smoke_bridge_alignment_status=_enum_value(
            FullChainNegativeSmokeBridgeAlignmentStatus,
            mapping["full_chain_negative_smoke_bridge_alignment_status"],
        ),
        no_lookahead_status=_enum_value(NoLookaheadStatus, mapping["no_lookahead_status"]),
        operator_review_status=_enum_value(OperatorReviewStatus, mapping["operator_review_status"]),
        runtime_gate_status=_enum_value(RuntimeGateStatus, mapping["runtime_gate_status"]),
        provenance_notes=str(mapping.get("provenance_notes", "")),
    )


def validate_fixture_only_source_provider_full_chain_negative_smoke_bridge_record(
    record: FixtureOnlySourceProviderFullChainNegativeSmokeBridgeRecord,
) -> FixtureOnlySourceProviderFullChainNegativeSmokeBridgeValidationResult:
    """Validate fixture-only full-chain negative-smoke bridge metadata fail-closed."""

    reasons: list[str] = []
    for field_name, value in (
        ("condition_id", record.condition_id),
        ("token_id", record.token_id),
        ("outcome", record.outcome),
        ("full_chain_negative_smoke_bridge_id", record.full_chain_negative_smoke_bridge_id),
        ("full_chain_negative_smoke_bridge_summary", record.full_chain_negative_smoke_bridge_summary),
        ("fixture_integration_smoke_bridge_summary", record.fixture_integration_smoke_bridge_summary),
        ("supplied_negative_smoke_summary", record.supplied_negative_smoke_summary),
        ("expected_failure_reason_summary", record.expected_failure_reason_summary),
        ("observed_failure_reason_summary", record.observed_failure_reason_summary),
        ("operator_review_summary", record.operator_review_summary),
        ("blocked_reason_summary", record.blocked_reason_summary),
    ):
        if not _is_nonblank_text(value):
            reasons.append(f"{field_name} is missing")

    positive_bridge = record.fixture_only_source_provider_full_chain_integration_smoke_bridge
    negative_smoke = record.supplied_runtime_full_chain_negative_smoke
    positive_integration_smoke = positive_bridge.supplied_runtime_full_chain_integration_smoke
    negative_integration_smoke = negative_smoke.supplied_runtime_full_chain_integration_smoke

    positive_result = validate_fixture_only_source_provider_full_chain_integration_smoke_bridge_record(
        positive_bridge
    )
    negative_result = validate_supplied_runtime_full_chain_negative_smoke_record(negative_smoke)
    if not positive_result.passed:
        reasons.append("fixture-only source provider full-chain integration-smoke bridge is invalid")
    if not negative_result.passed:
        reasons.append("supplied runtime full-chain negative smoke is invalid")

    for field_name in ("condition_id", "token_id", "outcome"):
        if getattr(record, field_name) != getattr(positive_bridge, field_name):
            reasons.append(f"{field_name} does not match fixture-only full-chain integration-smoke bridge")
        if getattr(record, field_name) != getattr(negative_smoke, field_name):
            reasons.append(f"{field_name} does not match supplied runtime full-chain negative smoke")

    positive_summary = positive_integration_smoke.supplied_runtime_operator_review_completion_summary
    negative_summary = negative_integration_smoke.supplied_runtime_operator_review_completion_summary
    positive_seal = positive_summary.supplied_runtime_operator_review_completion_seal
    negative_seal = negative_summary.supplied_runtime_operator_review_completion_seal
    positive_bundle = positive_seal.supplied_runtime_operator_review_final_bundle
    negative_bundle = negative_seal.supplied_runtime_operator_review_final_bundle
    positive_packet = positive_bundle.supplied_runtime_operator_review_final_packet
    negative_packet = negative_bundle.supplied_runtime_operator_review_final_packet
    positive_queue_summary = positive_packet.supplied_runtime_operator_review_queue_summary
    negative_queue_summary = negative_packet.supplied_runtime_operator_review_queue_summary
    positive_entry = positive_queue_summary.supplied_runtime_operator_review_queue_entry
    negative_entry = negative_queue_summary.supplied_runtime_operator_review_queue_entry
    positive_queue = positive_entry.supplied_runtime_operator_review_queue_packet
    negative_queue = negative_entry.supplied_runtime_operator_review_queue_packet
    positive_ack = positive_queue.supplied_runtime_operator_review_ack_packet
    negative_ack = negative_queue.supplied_runtime_operator_review_ack_packet
    positive_handoff = positive_ack.supplied_runtime_operator_review_handoff
    negative_handoff = negative_ack.supplied_runtime_operator_review_handoff
    positive_trace = positive_handoff.supplied_runtime_trace_packet
    negative_trace = negative_handoff.supplied_runtime_trace_packet
    positive_smoke = positive_trace.supplied_runtime_end_to_end_smoke
    negative_smoke_record = negative_trace.supplied_runtime_end_to_end_smoke
    positive_report = positive_smoke.supplied_runtime_dry_run_report
    negative_report = negative_smoke_record.supplied_runtime_dry_run_report
    positive_dry = positive_report.supplied_runtime_dry_run_packet
    negative_dry = negative_report.supplied_runtime_dry_run_packet
    positive_validation = positive_dry.supplied_runtime_validation_bundle
    negative_validation = negative_dry.supplied_runtime_validation_bundle
    positive_evidence = positive_validation.supplied_evidence_packet
    negative_evidence = negative_validation.supplied_evidence_packet

    route_checks = (
        (positive_bridge, negative_smoke, "nested fixture-only full-chain integration-smoke bridge and supplied runtime full-chain negative smoke routes do not match"),
        (positive_integration_smoke, negative_integration_smoke, "nested supplied runtime full-chain integration smokes do not match"),
        (positive_summary, negative_summary, "nested supplied runtime operator-review completion summaries do not match"),
        (positive_seal, negative_seal, "nested supplied runtime operator-review completion seals do not match"),
        (positive_bundle, negative_bundle, "nested supplied runtime operator-review final bundles do not match"),
        (positive_packet, negative_packet, "nested supplied runtime operator-review final packets do not match"),
        (positive_queue_summary, negative_queue_summary, "nested supplied runtime operator-review queue summaries do not match"),
        (positive_entry, negative_entry, "nested supplied runtime operator-review queue entries do not match"),
        (positive_queue, negative_queue, "nested supplied runtime operator-review queue packets do not match"),
        (positive_ack, negative_ack, "nested supplied runtime operator-review ack packets do not match"),
        (positive_handoff, negative_handoff, "nested supplied runtime operator-review handoffs do not match"),
        (positive_trace, negative_trace, "nested supplied runtime trace packets do not match"),
        (positive_smoke, negative_smoke_record, "nested supplied runtime end-to-end smokes do not match"),
        (positive_report, negative_report, "nested supplied runtime dry-run reports do not match"),
    )
    for left, right, reason in route_checks:
        if not _same_route(left, right):
            reasons.append(reason)
    if not _same_route(positive_dry, negative_dry) or not _same_route(positive_validation, negative_validation):
        reasons.append("nested supplied runtime dry-run packets do not match")
    if not _same_route(positive_evidence, negative_evidence) or not _same_route(
        positive_evidence.supplied_market_contract,
        negative_evidence.supplied_market_contract,
    ):
        reasons.append("nested supplied evidence packets do not match")

    if record.fixture_integration_smoke_bridge_summary != positive_bridge.full_chain_integration_smoke_bridge_summary:
        reasons.append("fixture integration-smoke bridge summary does not match fixture-only full-chain integration-smoke bridge")
    if record.supplied_negative_smoke_summary != negative_smoke.negative_smoke_summary:
        reasons.append("supplied negative smoke summary does not match supplied runtime full-chain negative smoke")
    if record.expected_failure_reason_summary != negative_smoke.expected_failure_reason_summary:
        reasons.append("expected failure reason summary does not match supplied runtime full-chain negative smoke")
    if record.observed_failure_reason_summary != negative_smoke.observed_failure_reason_summary:
        reasons.append("observed failure reason summary does not match supplied runtime full-chain negative smoke")
    if record.operator_review_summary != positive_bridge.operator_review_summary:
        reasons.append("operator review summary does not match fixture-only full-chain integration-smoke bridge")
    if record.blocked_reason_summary != negative_smoke.blocked_reason_summary:
        reasons.append("blocked reason summary does not match supplied runtime full-chain negative smoke")

    if record.fixture_only_full_chain_negative_smoke_bridge_status is not FixtureOnlyFullChainNegativeSmokeBridgeStatus.FIXTURE_ONLY_FULL_CHAIN_NEGATIVE_SMOKE_BRIDGE_RECORDED:
        reasons.append(f"fixture-only full-chain negative-smoke bridge status is {record.fixture_only_full_chain_negative_smoke_bridge_status.value}")
    if record.fixture_only_full_chain_negative_smoke_bridge_posture is not FixtureOnlyFullChainNegativeSmokeBridgePosture.FIXTURE_ONLY_FULL_CHAIN_NEGATIVE_SMOKE_BRIDGE_IN_MEMORY_ONLY:
        reasons.append(f"fixture-only full-chain negative-smoke bridge posture is {record.fixture_only_full_chain_negative_smoke_bridge_posture.value}")
    if record.full_chain_negative_smoke_bridge_alignment_status is not FullChainNegativeSmokeBridgeAlignmentStatus.FULL_CHAIN_NEGATIVE_SMOKE_BRIDGE_ALIGNED:
        reasons.append(f"full-chain negative-smoke bridge alignment status is {record.full_chain_negative_smoke_bridge_alignment_status.value}")
    if record.no_lookahead_status is not NoLookaheadStatus.NO_LOOKAHEAD_RECORDED:
        reasons.append(f"no-lookahead status is {record.no_lookahead_status.value}")
    if record.operator_review_status is not OperatorReviewStatus.OPERATOR_REVIEW_REQUIRED:
        reasons.append(f"operator review status is {record.operator_review_status.value}")
    if record.runtime_gate_status is not RuntimeGateStatus.RUNTIME_GATE_BLOCKED:
        reasons.append(f"runtime gate status is {record.runtime_gate_status.value}")

    if reasons:
        return FixtureOnlySourceProviderFullChainNegativeSmokeBridgeValidationResult(
            severity=ValidationSeverity.BLOCKED,
            passed=False,
            reasons=tuple(reasons),
        )
    return FixtureOnlySourceProviderFullChainNegativeSmokeBridgeValidationResult(
        severity=ValidationSeverity.PASSED,
        passed=True,
        reasons=(),
    )
