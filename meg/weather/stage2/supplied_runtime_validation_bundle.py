"""Pure supplied-input runtime validation bundle scaffold.

This module consumes only caller-supplied values for runtime validation bundle
metadata. It performs no data collection, file access, service access, source
fetching, scoring, backtesting, paper trading, trading, autonomy, or production
behavior.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping

from meg.weather.stage2.review_packet_evidence_composition_runtime import (
    ReviewPacketEvidenceCompositionRecord,
    review_packet_evidence_composition_record_from_mapping,
    validate_review_packet_evidence_composition_record,
)
from meg.weather.stage2.supplied_evidence_packet_runtime import (
    SuppliedEvidencePacketRecord,
    supplied_evidence_packet_record_from_mapping,
    validate_supplied_evidence_packet_record,
)
from meg.weather.stage2.supplied_market_contract_runtime import (
    SuppliedMarketContractRecord,
    supplied_market_contract_record_from_mapping,
    validate_supplied_market_contract_record,
)
from meg.weather.stage2.supplied_market_review_packet_runtime import (
    SuppliedMarketReviewPacketRecord,
    supplied_market_review_packet_record_from_mapping,
    validate_supplied_market_review_packet_record,
)


class _ClosedValue(str, Enum):
    """String enum base for closed, machine-checkable Stage 2 values."""

    @classmethod
    def values(cls) -> frozenset[str]:
        return frozenset(member.value for member in cls)


class RuntimeValidationBundleStatus(_ClosedValue):
    RUNTIME_VALIDATION_BUNDLE_RECORDED = "runtime_validation_bundle_recorded"
    RUNTIME_VALIDATION_BUNDLE_MISSING = "runtime_validation_bundle_missing"
    RUNTIME_VALIDATION_BUNDLE_AMBIGUOUS = "runtime_validation_bundle_ambiguous"
    RUNTIME_VALIDATION_BUNDLE_UNSUPPORTED = "runtime_validation_bundle_unsupported"
    RUNTIME_VALIDATION_BUNDLE_UNKNOWN = "runtime_validation_bundle_unknown"


class RuntimeValidationCompletenessStatus(_ClosedValue):
    RUNTIME_VALIDATION_COMPLETE = "runtime_validation_complete"
    RUNTIME_VALIDATION_INCOMPLETE = "runtime_validation_incomplete"
    RUNTIME_VALIDATION_AMBIGUOUS = "runtime_validation_ambiguous"
    RUNTIME_VALIDATION_UNKNOWN = "runtime_validation_unknown"


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
class SuppliedRuntimeValidationBundleRecord:
    condition_id: str
    token_id: str
    outcome: str
    supplied_market_contract: SuppliedMarketContractRecord
    supplied_market_review_packet: SuppliedMarketReviewPacketRecord
    supplied_evidence_packet: SuppliedEvidencePacketRecord
    review_packet_evidence_composition: ReviewPacketEvidenceCompositionRecord
    validation_bundle_id: str
    validation_summary: str
    runtime_validation_bundle_status: RuntimeValidationBundleStatus
    runtime_validation_completeness_status: RuntimeValidationCompletenessStatus
    runtime_gate_status: RuntimeGateStatus
    provenance_notes: str = ""


@dataclass(frozen=True)
class SuppliedRuntimeValidationBundleValidationResult:
    severity: ValidationSeverity
    passed: bool
    reasons: tuple[str, ...] = ()


def _enum_value(enum_type: type[_ClosedValue], value: _ClosedValue | str) -> _ClosedValue:
    if isinstance(value, enum_type):
        return value
    return enum_type(value)


def _is_nonblank_text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _supplied_market_contract_from_value(
    value: SuppliedMarketContractRecord | Mapping[str, Any],
) -> SuppliedMarketContractRecord:
    if isinstance(value, SuppliedMarketContractRecord):
        return value
    return supplied_market_contract_record_from_mapping(value)


def _supplied_market_review_packet_from_value(
    value: SuppliedMarketReviewPacketRecord | Mapping[str, Any],
) -> SuppliedMarketReviewPacketRecord:
    if isinstance(value, SuppliedMarketReviewPacketRecord):
        return value
    return supplied_market_review_packet_record_from_mapping(value)


def _supplied_evidence_packet_from_value(
    value: SuppliedEvidencePacketRecord | Mapping[str, Any],
) -> SuppliedEvidencePacketRecord:
    if isinstance(value, SuppliedEvidencePacketRecord):
        return value
    return supplied_evidence_packet_record_from_mapping(value)


def _review_packet_evidence_composition_from_value(
    value: ReviewPacketEvidenceCompositionRecord | Mapping[str, Any],
) -> ReviewPacketEvidenceCompositionRecord:
    if isinstance(value, ReviewPacketEvidenceCompositionRecord):
        return value
    return review_packet_evidence_composition_record_from_mapping(value)


def supplied_runtime_validation_bundle_record_from_mapping(
    mapping: Mapping[str, Any],
) -> SuppliedRuntimeValidationBundleRecord:
    """Build runtime validation bundle metadata from explicitly supplied values."""

    return SuppliedRuntimeValidationBundleRecord(
        condition_id=mapping["condition_id"],
        token_id=mapping["token_id"],
        outcome=mapping["outcome"],
        supplied_market_contract=_supplied_market_contract_from_value(
            mapping["supplied_market_contract"]
        ),
        supplied_market_review_packet=_supplied_market_review_packet_from_value(
            mapping["supplied_market_review_packet"]
        ),
        supplied_evidence_packet=_supplied_evidence_packet_from_value(
            mapping["supplied_evidence_packet"]
        ),
        review_packet_evidence_composition=_review_packet_evidence_composition_from_value(
            mapping["review_packet_evidence_composition"]
        ),
        validation_bundle_id=mapping["validation_bundle_id"],
        validation_summary=mapping["validation_summary"],
        runtime_validation_bundle_status=_enum_value(
            RuntimeValidationBundleStatus,
            mapping["runtime_validation_bundle_status"],
        ),
        runtime_validation_completeness_status=_enum_value(
            RuntimeValidationCompletenessStatus,
            mapping["runtime_validation_completeness_status"],
        ),
        runtime_gate_status=_enum_value(RuntimeGateStatus, mapping["runtime_gate_status"]),
        provenance_notes=str(mapping.get("provenance_notes", "")),
    )


def _same_route(left: object, right: object) -> bool:
    return (
        getattr(left, "condition_id") == getattr(right, "condition_id")
        and getattr(left, "token_id") == getattr(right, "token_id")
        and getattr(left, "outcome") == getattr(right, "outcome")
    )


def validate_supplied_runtime_validation_bundle_record(
    record: SuppliedRuntimeValidationBundleRecord,
) -> SuppliedRuntimeValidationBundleValidationResult:
    """Validate a supplied runtime validation bundle with fail-closed behavior."""

    reasons: list[str] = []

    for field_name, value in (
        ("condition_id", record.condition_id),
        ("token_id", record.token_id),
        ("outcome", record.outcome),
        ("validation_bundle_id", record.validation_bundle_id),
        ("validation_summary", record.validation_summary),
    ):
        if not _is_nonblank_text(value):
            reasons.append(f"{field_name} is missing")

    contract_result = validate_supplied_market_contract_record(record.supplied_market_contract)
    if not contract_result.passed:
        reasons.append("supplied market contract validation failed")

    review_result = validate_supplied_market_review_packet_record(
        record.supplied_market_review_packet
    )
    if not review_result.passed:
        reasons.append("supplied market review packet validation failed")

    evidence_result = validate_supplied_evidence_packet_record(record.supplied_evidence_packet)
    if not evidence_result.passed:
        reasons.append("supplied evidence packet validation failed")

    composition_result = validate_review_packet_evidence_composition_record(
        record.review_packet_evidence_composition
    )
    if not composition_result.passed:
        reasons.append("review packet evidence composition validation failed")

    for field_name in ("condition_id", "token_id", "outcome"):
        if getattr(record, field_name) != getattr(record.supplied_market_contract, field_name):
            reasons.append(f"{field_name} does not match supplied market contract")
        if getattr(record, field_name) != getattr(record.supplied_market_review_packet, field_name):
            reasons.append(f"{field_name} does not match supplied market review packet")
        if getattr(record, field_name) != getattr(record.supplied_evidence_packet, field_name):
            reasons.append(f"{field_name} does not match supplied evidence packet")
        if getattr(record, field_name) != getattr(
            record.review_packet_evidence_composition,
            field_name,
        ):
            reasons.append(f"{field_name} does not match review packet evidence composition")

    if not _same_route(
        record.supplied_market_review_packet.supplied_market_contract,
        record.supplied_market_contract,
    ):
        reasons.append(
            "supplied market review packet contract does not match supplied market contract"
        )

    if not _same_route(
        record.supplied_evidence_packet.supplied_market_contract,
        record.supplied_market_contract,
    ):
        reasons.append(
            "supplied evidence packet contract does not match supplied market contract"
        )

    composition = record.review_packet_evidence_composition
    if not _same_route(
        composition.supplied_market_review_packet,
        record.supplied_market_review_packet,
    ):
        reasons.append("composition review packet does not match supplied market review packet")

    if not _same_route(composition.supplied_evidence_packet, record.supplied_evidence_packet):
        reasons.append("composition evidence packet does not match supplied evidence packet")

    if (
        not _same_route(
            composition.supplied_market_review_packet.supplied_market_contract,
            record.supplied_market_contract,
        )
        or not _same_route(
            composition.supplied_evidence_packet.supplied_market_contract,
            record.supplied_market_contract,
        )
    ):
        reasons.append("composition nested contracts do not match supplied market contract")

    if (
        record.runtime_validation_bundle_status
        is not RuntimeValidationBundleStatus.RUNTIME_VALIDATION_BUNDLE_RECORDED
    ):
        reasons.append(
            f"runtime validation bundle status is "
            f"{record.runtime_validation_bundle_status.value}"
        )

    if (
        record.runtime_validation_completeness_status
        is not RuntimeValidationCompletenessStatus.RUNTIME_VALIDATION_COMPLETE
    ):
        reasons.append(
            f"runtime validation completeness status is "
            f"{record.runtime_validation_completeness_status.value}"
        )

    if record.runtime_gate_status is not RuntimeGateStatus.RUNTIME_GATE_READY:
        reasons.append(f"runtime gate status is {record.runtime_gate_status.value}")

    if reasons:
        return SuppliedRuntimeValidationBundleValidationResult(
            severity=ValidationSeverity.BLOCKED,
            passed=False,
            reasons=tuple(reasons),
        )

    return SuppliedRuntimeValidationBundleValidationResult(
        severity=ValidationSeverity.PASSED,
        passed=True,
    )
