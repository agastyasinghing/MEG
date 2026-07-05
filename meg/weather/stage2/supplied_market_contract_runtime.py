"""Pure supplied-input market-contract runtime scaffold.

This module consumes only caller-supplied values for market-contract metadata.
It performs no data collection, file access, service access, source fetching,
scoring, backtesting, paper trading, trading, autonomy, or production behavior.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping


class _ClosedValue(str, Enum):
    """String enum base for closed, machine-checkable Stage 2 values."""

    @classmethod
    def values(cls) -> frozenset[str]:
        return frozenset(member.value for member in cls)


class SettlementRuleStatus(_ClosedValue):
    SETTLEMENT_RULE_RECORDED = "settlement_rule_recorded"
    SETTLEMENT_RULE_MISSING = "settlement_rule_missing"
    SETTLEMENT_RULE_AMBIGUOUS = "settlement_rule_ambiguous"
    SETTLEMENT_RULE_UNSUPPORTED = "settlement_rule_unsupported"
    SETTLEMENT_RULE_UNKNOWN = "settlement_rule_unknown"


class MarketContractStatus(_ClosedValue):
    MARKET_CONTRACT_RECORDED = "market_contract_recorded"
    MARKET_CONTRACT_MISSING = "market_contract_missing"
    MARKET_CONTRACT_AMBIGUOUS = "market_contract_ambiguous"
    MARKET_CONTRACT_UNSUPPORTED = "market_contract_unsupported"
    MARKET_CONTRACT_UNKNOWN = "market_contract_unknown"


class EventTimingStatus(_ClosedValue):
    EVENT_TIMING_RECORDED = "event_timing_recorded"
    EVENT_TIMING_MISSING = "event_timing_missing"
    EVENT_TIMING_AMBIGUOUS = "event_timing_ambiguous"
    EVENT_TIMING_UNSUPPORTED = "event_timing_unsupported"
    EVENT_TIMING_UNKNOWN = "event_timing_unknown"


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
class SuppliedMarketContractRecord:
    condition_id: str
    token_id: str
    outcome: str
    market_title: str
    settlement_rule: str
    event_start_utc: str
    event_end_utc: str
    settlement_rule_status: SettlementRuleStatus
    market_contract_status: MarketContractStatus
    event_timing_status: EventTimingStatus
    runtime_gate_status: RuntimeGateStatus
    provenance_notes: str = ""


@dataclass(frozen=True)
class SuppliedMarketContractValidationResult:
    severity: ValidationSeverity
    passed: bool
    reasons: tuple[str, ...] = ()


def _enum_value(enum_type: type[_ClosedValue], value: _ClosedValue | str) -> _ClosedValue:
    if isinstance(value, enum_type):
        return value
    return enum_type(value)


def _is_nonblank_text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def supplied_market_contract_record_from_mapping(
    mapping: Mapping[str, Any],
) -> SuppliedMarketContractRecord:
    """Build market-contract metadata from explicitly supplied values."""

    return SuppliedMarketContractRecord(
        condition_id=mapping["condition_id"],
        token_id=mapping["token_id"],
        outcome=mapping["outcome"],
        market_title=mapping["market_title"],
        settlement_rule=mapping["settlement_rule"],
        event_start_utc=mapping["event_start_utc"],
        event_end_utc=mapping["event_end_utc"],
        settlement_rule_status=_enum_value(
            SettlementRuleStatus, mapping["settlement_rule_status"]
        ),
        market_contract_status=_enum_value(
            MarketContractStatus, mapping["market_contract_status"]
        ),
        event_timing_status=_enum_value(EventTimingStatus, mapping["event_timing_status"]),
        runtime_gate_status=_enum_value(RuntimeGateStatus, mapping["runtime_gate_status"]),
        provenance_notes=str(mapping.get("provenance_notes", "")),
    )


def validate_supplied_market_contract_record(
    record: SuppliedMarketContractRecord,
) -> SuppliedMarketContractValidationResult:
    """Validate supplied market-contract metadata with fail-closed behavior."""

    reasons: list[str] = []

    for field_name, value in (
        ("condition_id", record.condition_id),
        ("token_id", record.token_id),
        ("outcome", record.outcome),
        ("market_title", record.market_title),
        ("settlement_rule", record.settlement_rule),
        ("event_start_utc", record.event_start_utc),
        ("event_end_utc", record.event_end_utc),
    ):
        if not _is_nonblank_text(value):
            reasons.append(f"{field_name} is missing")

    if record.settlement_rule_status is not SettlementRuleStatus.SETTLEMENT_RULE_RECORDED:
        reasons.append(f"settlement rule status is {record.settlement_rule_status.value}")

    if record.market_contract_status is not MarketContractStatus.MARKET_CONTRACT_RECORDED:
        reasons.append(f"market contract status is {record.market_contract_status.value}")

    if record.event_timing_status is not EventTimingStatus.EVENT_TIMING_RECORDED:
        reasons.append(f"event timing status is {record.event_timing_status.value}")

    if record.runtime_gate_status is not RuntimeGateStatus.RUNTIME_GATE_READY:
        reasons.append(f"runtime gate status is {record.runtime_gate_status.value}")

    if reasons:
        return SuppliedMarketContractValidationResult(
            severity=ValidationSeverity.BLOCKED,
            passed=False,
            reasons=tuple(reasons),
        )

    return SuppliedMarketContractValidationResult(
        severity=ValidationSeverity.PASSED,
        passed=True,
    )
