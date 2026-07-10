"""Pure fixture-only Weather Bot Stage 2 source/provider evidence bridge runtime scaffold.

This module consumes only caller-supplied fixture-only source/provider and
supplied evidence packet values. It keeps an in-memory record only. It performs
no live source fetching, no live provider clients, no API calls, no scraping,
no downloads, no SDK usage, no credentials/config loading, no live ingestion,
no evidence generation, no persistence/export writing, no paper trading, no
trading/execution, no autonomy, and no production behavior.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping

from meg.weather.stage2.fixture_only_source_provider_runtime import (
    FixtureOnlySourceProviderRecord,
    fixture_only_source_provider_record_from_mapping,
    validate_fixture_only_source_provider_record,
)
from meg.weather.stage2.supplied_evidence_packet_runtime import (
    SuppliedEvidencePacketRecord,
    supplied_evidence_packet_record_from_mapping,
    validate_supplied_evidence_packet_record,
)


class _ClosedValue(str, Enum):
    """String enum base for closed, machine-checkable Stage 2 values."""

    @classmethod
    def values(cls) -> frozenset[str]:
        return frozenset(member.value for member in cls)


class FixtureOnlyEvidenceBridgeStatus(_ClosedValue):
    FIXTURE_ONLY_EVIDENCE_BRIDGE_RECORDED = "fixture_only_evidence_bridge_recorded"
    FIXTURE_ONLY_EVIDENCE_BRIDGE_MISSING = "fixture_only_evidence_bridge_missing"
    FIXTURE_ONLY_EVIDENCE_BRIDGE_AMBIGUOUS = "fixture_only_evidence_bridge_ambiguous"
    FIXTURE_ONLY_EVIDENCE_BRIDGE_UNSUPPORTED = "fixture_only_evidence_bridge_unsupported"
    FIXTURE_ONLY_EVIDENCE_BRIDGE_UNKNOWN = "fixture_only_evidence_bridge_unknown"


class FixtureOnlyEvidenceBridgePosture(_ClosedValue):
    FIXTURE_ONLY_EVIDENCE_BRIDGE_IN_MEMORY_ONLY = (
        "fixture_only_evidence_bridge_in_memory_only"
    )
    FIXTURE_ONLY_EVIDENCE_BRIDGE_MISSING = "fixture_only_evidence_bridge_missing"
    FIXTURE_ONLY_EVIDENCE_BRIDGE_AMBIGUOUS = "fixture_only_evidence_bridge_ambiguous"
    FIXTURE_ONLY_EVIDENCE_BRIDGE_UNSUPPORTED = "fixture_only_evidence_bridge_unsupported"
    FIXTURE_ONLY_EVIDENCE_BRIDGE_UNKNOWN = "fixture_only_evidence_bridge_unknown"


class EvidenceBridgeAlignmentStatus(_ClosedValue):
    EVIDENCE_BRIDGE_ALIGNED = "evidence_bridge_aligned"
    EVIDENCE_BRIDGE_MISMATCH = "evidence_bridge_mismatch"
    EVIDENCE_BRIDGE_MISSING = "evidence_bridge_missing"
    EVIDENCE_BRIDGE_AMBIGUOUS = "evidence_bridge_ambiguous"
    EVIDENCE_BRIDGE_UNKNOWN = "evidence_bridge_unknown"


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
class FixtureOnlySourceProviderEvidenceBridgeRecord:
    condition_id: str
    token_id: str
    outcome: str
    fixture_only_source_provider: FixtureOnlySourceProviderRecord
    supplied_evidence_packet: SuppliedEvidencePacketRecord
    evidence_bridge_id: str
    evidence_bridge_summary: str
    fixture_source_descriptor_summary: str
    evidence_source_descriptor_summary: str
    no_lookahead_summary: str
    operator_review_summary: str
    blocked_reason_summary: str
    fixture_only_evidence_bridge_status: FixtureOnlyEvidenceBridgeStatus
    fixture_only_evidence_bridge_posture: FixtureOnlyEvidenceBridgePosture
    evidence_bridge_alignment_status: EvidenceBridgeAlignmentStatus
    no_lookahead_status: NoLookaheadStatus
    operator_review_status: OperatorReviewStatus
    runtime_gate_status: RuntimeGateStatus
    provenance_notes: str = ""


@dataclass(frozen=True)
class FixtureOnlySourceProviderEvidenceBridgeValidationResult:
    severity: ValidationSeverity
    passed: bool
    reasons: tuple[str, ...] = ()


def _enum_value(enum_type: type[_ClosedValue], value: _ClosedValue | str) -> _ClosedValue:
    if isinstance(value, enum_type):
        return value
    return enum_type(value)


def _is_nonblank_text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _fixture_only_source_provider_from_value(
    value: FixtureOnlySourceProviderRecord | Mapping[str, Any],
) -> FixtureOnlySourceProviderRecord:
    if isinstance(value, FixtureOnlySourceProviderRecord):
        return value
    return fixture_only_source_provider_record_from_mapping(value)


def _supplied_evidence_packet_from_value(
    value: SuppliedEvidencePacketRecord | Mapping[str, Any],
) -> SuppliedEvidencePacketRecord:
    if isinstance(value, SuppliedEvidencePacketRecord):
        return value
    return supplied_evidence_packet_record_from_mapping(value)


def fixture_only_source_provider_evidence_bridge_record_from_mapping(
    mapping: Mapping[str, Any],
) -> FixtureOnlySourceProviderEvidenceBridgeRecord:
    """Build bridge metadata from explicitly supplied in-memory values."""

    return FixtureOnlySourceProviderEvidenceBridgeRecord(
        condition_id=mapping["condition_id"],
        token_id=mapping["token_id"],
        outcome=mapping["outcome"],
        fixture_only_source_provider=_fixture_only_source_provider_from_value(
            mapping["fixture_only_source_provider"]
        ),
        supplied_evidence_packet=_supplied_evidence_packet_from_value(
            mapping["supplied_evidence_packet"]
        ),
        evidence_bridge_id=mapping["evidence_bridge_id"],
        evidence_bridge_summary=mapping["evidence_bridge_summary"],
        fixture_source_descriptor_summary=mapping["fixture_source_descriptor_summary"],
        evidence_source_descriptor_summary=mapping["evidence_source_descriptor_summary"],
        no_lookahead_summary=mapping["no_lookahead_summary"],
        operator_review_summary=mapping["operator_review_summary"],
        blocked_reason_summary=mapping["blocked_reason_summary"],
        fixture_only_evidence_bridge_status=_enum_value(
            FixtureOnlyEvidenceBridgeStatus,
            mapping["fixture_only_evidence_bridge_status"],
        ),
        fixture_only_evidence_bridge_posture=_enum_value(
            FixtureOnlyEvidenceBridgePosture,
            mapping["fixture_only_evidence_bridge_posture"],
        ),
        evidence_bridge_alignment_status=_enum_value(
            EvidenceBridgeAlignmentStatus,
            mapping["evidence_bridge_alignment_status"],
        ),
        no_lookahead_status=_enum_value(NoLookaheadStatus, mapping["no_lookahead_status"]),
        operator_review_status=_enum_value(
            OperatorReviewStatus,
            mapping["operator_review_status"],
        ),
        runtime_gate_status=_enum_value(RuntimeGateStatus, mapping["runtime_gate_status"]),
        provenance_notes=str(mapping.get("provenance_notes", "")),
    )


def validate_fixture_only_source_provider_evidence_bridge_record(
    record: FixtureOnlySourceProviderEvidenceBridgeRecord,
) -> FixtureOnlySourceProviderEvidenceBridgeValidationResult:
    """Validate fixture-only source/provider evidence bridge metadata fail-closed."""

    reasons: list[str] = []

    for field_name, value in (
        ("condition_id", record.condition_id),
        ("token_id", record.token_id),
        ("outcome", record.outcome),
        ("evidence_bridge_id", record.evidence_bridge_id),
        ("evidence_bridge_summary", record.evidence_bridge_summary),
        ("fixture_source_descriptor_summary", record.fixture_source_descriptor_summary),
        ("evidence_source_descriptor_summary", record.evidence_source_descriptor_summary),
        ("no_lookahead_summary", record.no_lookahead_summary),
        ("operator_review_summary", record.operator_review_summary),
    ):
        if not _is_nonblank_text(value):
            reasons.append(f"{field_name} is missing")

    fixture_result = validate_fixture_only_source_provider_record(
        record.fixture_only_source_provider
    )
    if not fixture_result.passed:
        reasons.append("fixture-only source provider is invalid")

    evidence_result = validate_supplied_evidence_packet_record(record.supplied_evidence_packet)
    if not evidence_result.passed:
        reasons.append("supplied evidence packet is invalid")

    if record.condition_id != record.fixture_only_source_provider.condition_id:
        reasons.append("condition_id does not match fixture-only source provider")
    if record.token_id != record.fixture_only_source_provider.token_id:
        reasons.append("token_id does not match fixture-only source provider")
    if record.outcome != record.fixture_only_source_provider.outcome:
        reasons.append("outcome does not match fixture-only source provider")

    if record.condition_id != record.supplied_evidence_packet.condition_id:
        reasons.append("condition_id does not match supplied evidence packet")
    if record.token_id != record.supplied_evidence_packet.token_id:
        reasons.append("token_id does not match supplied evidence packet")
    if record.outcome != record.supplied_evidence_packet.outcome:
        reasons.append("outcome does not match supplied evidence packet")

    fixture_route = (
        record.fixture_only_source_provider.condition_id,
        record.fixture_only_source_provider.token_id,
        record.fixture_only_source_provider.outcome,
    )
    evidence_route = (
        record.supplied_evidence_packet.condition_id,
        record.supplied_evidence_packet.token_id,
        record.supplied_evidence_packet.outcome,
    )
    if fixture_route != evidence_route:
        reasons.append(
            "nested fixture-only source provider and supplied evidence packet routes do not match"
        )

    fixture_contract_route = (
        record.fixture_only_source_provider.supplied_market_contract.condition_id,
        record.fixture_only_source_provider.supplied_market_contract.token_id,
        record.fixture_only_source_provider.supplied_market_contract.outcome,
    )
    evidence_contract_route = (
        record.supplied_evidence_packet.supplied_market_contract.condition_id,
        record.supplied_evidence_packet.supplied_market_contract.token_id,
        record.supplied_evidence_packet.supplied_market_contract.outcome,
    )
    if fixture_contract_route != evidence_contract_route:
        reasons.append("nested supplied market contracts do not match")

    if (
        record.fixture_source_descriptor_summary
        != record.fixture_only_source_provider.fixture_source_name
    ):
        reasons.append(
            "fixture source descriptor summary does not match fixture-only source provider"
        )
    if (
        record.evidence_source_descriptor_summary
        != record.supplied_evidence_packet.evidence_source_descriptor
    ):
        reasons.append(
            "evidence source descriptor summary does not match supplied evidence packet"
        )
    if record.no_lookahead_summary != record.fixture_only_source_provider.no_lookahead_summary:
        reasons.append("no-lookahead summary does not match fixture-only source provider")

    if (
        record.fixture_only_evidence_bridge_status
        is not FixtureOnlyEvidenceBridgeStatus.FIXTURE_ONLY_EVIDENCE_BRIDGE_RECORDED
    ):
        reasons.append(
            "fixture-only evidence bridge status is "
            f"{record.fixture_only_evidence_bridge_status.value}"
        )
    if (
        record.fixture_only_evidence_bridge_posture
        is not FixtureOnlyEvidenceBridgePosture.FIXTURE_ONLY_EVIDENCE_BRIDGE_IN_MEMORY_ONLY
    ):
        reasons.append(
            "fixture-only evidence bridge posture is "
            f"{record.fixture_only_evidence_bridge_posture.value}"
        )
    if (
        record.evidence_bridge_alignment_status
        is not EvidenceBridgeAlignmentStatus.EVIDENCE_BRIDGE_ALIGNED
    ):
        reasons.append(
            f"evidence bridge alignment status is {record.evidence_bridge_alignment_status.value}"
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
        return FixtureOnlySourceProviderEvidenceBridgeValidationResult(
            severity=ValidationSeverity.BLOCKED,
            passed=False,
            reasons=tuple(reasons),
        )

    return FixtureOnlySourceProviderEvidenceBridgeValidationResult(
        severity=ValidationSeverity.PASSED,
        passed=True,
    )
