"""Pure fixture-only Weather Bot Stage 2 source/provider runtime scaffold.

This module consumes only caller-supplied fixture-like/static values and keeps
an in-memory record only. It performs no live source fetching, no live provider
clients, no API calls, no scraping, no downloads, no SDK usage, no
credentials/config loading, no live ingestion, no persistence/export writing,
no paper trading, no trading/execution, no autonomy, and no production behavior.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping

from meg.weather.stage2.supplied_market_contract_runtime import (
    SuppliedMarketContractRecord,
    supplied_market_contract_record_from_mapping,
    validate_supplied_market_contract_record,
)


class _ClosedValue(str, Enum):
    """String enum base for closed, machine-checkable Stage 2 values."""

    @classmethod
    def values(cls) -> frozenset[str]:
        return frozenset(member.value for member in cls)


class FixtureOnlySourceProviderStatus(_ClosedValue):
    FIXTURE_ONLY_SOURCE_PROVIDER_RECORDED = "fixture_only_source_provider_recorded"
    FIXTURE_ONLY_SOURCE_PROVIDER_MISSING = "fixture_only_source_provider_missing"
    FIXTURE_ONLY_SOURCE_PROVIDER_AMBIGUOUS = "fixture_only_source_provider_ambiguous"
    FIXTURE_ONLY_SOURCE_PROVIDER_UNSUPPORTED = "fixture_only_source_provider_unsupported"
    FIXTURE_ONLY_SOURCE_PROVIDER_UNKNOWN = "fixture_only_source_provider_unknown"


class FixtureOnlySourceProviderPosture(_ClosedValue):
    FIXTURE_ONLY_LOCAL_STATIC_CALLER_SUPPLIED = "fixture_only_local_static_caller_supplied"
    FIXTURE_ONLY_MISSING = "fixture_only_missing"
    FIXTURE_ONLY_AMBIGUOUS = "fixture_only_ambiguous"
    FIXTURE_ONLY_UNSUPPORTED = "fixture_only_unsupported"
    FIXTURE_ONLY_UNKNOWN = "fixture_only_unknown"


class FixtureOnlySourceProviderFreshnessStatus(_ClosedValue):
    FIXTURE_ONLY_FRESHNESS_RECORDED = "fixture_only_freshness_recorded"
    FIXTURE_ONLY_FRESHNESS_MISSING = "fixture_only_freshness_missing"
    FIXTURE_ONLY_FRESHNESS_AMBIGUOUS = "fixture_only_freshness_ambiguous"
    FIXTURE_ONLY_FRESHNESS_UNKNOWN = "fixture_only_freshness_unknown"


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
class FixtureOnlySourceProviderRecord:
    condition_id: str
    token_id: str
    outcome: str
    supplied_market_contract: SuppliedMarketContractRecord
    fixture_provider_record_id: str
    fixture_provider_name: str
    fixture_source_name: str
    fixture_snapshot_summary: str
    fixture_observed_at_utc: str
    fixture_available_at_utc: str
    decision_time_utc: str
    no_lookahead_summary: str
    operator_review_summary: str
    blocked_reason_summary: str
    fixture_only_source_provider_status: FixtureOnlySourceProviderStatus
    fixture_only_source_provider_posture: FixtureOnlySourceProviderPosture
    fixture_only_source_provider_freshness_status: FixtureOnlySourceProviderFreshnessStatus
    no_lookahead_status: NoLookaheadStatus
    operator_review_status: OperatorReviewStatus
    runtime_gate_status: RuntimeGateStatus
    provenance_notes: str = ""


@dataclass(frozen=True)
class FixtureOnlySourceProviderValidationResult:
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


def fixture_only_source_provider_record_from_mapping(
    mapping: Mapping[str, Any],
) -> FixtureOnlySourceProviderRecord:
    """Build fixture-only source/provider metadata from explicitly supplied values."""

    return FixtureOnlySourceProviderRecord(
        condition_id=mapping["condition_id"],
        token_id=mapping["token_id"],
        outcome=mapping["outcome"],
        supplied_market_contract=_supplied_market_contract_from_value(
            mapping["supplied_market_contract"]
        ),
        fixture_provider_record_id=mapping["fixture_provider_record_id"],
        fixture_provider_name=mapping["fixture_provider_name"],
        fixture_source_name=mapping["fixture_source_name"],
        fixture_snapshot_summary=mapping["fixture_snapshot_summary"],
        fixture_observed_at_utc=mapping["fixture_observed_at_utc"],
        fixture_available_at_utc=mapping["fixture_available_at_utc"],
        decision_time_utc=mapping["decision_time_utc"],
        no_lookahead_summary=mapping["no_lookahead_summary"],
        operator_review_summary=mapping["operator_review_summary"],
        blocked_reason_summary=mapping["blocked_reason_summary"],
        fixture_only_source_provider_status=_enum_value(
            FixtureOnlySourceProviderStatus,
            mapping["fixture_only_source_provider_status"],
        ),
        fixture_only_source_provider_posture=_enum_value(
            FixtureOnlySourceProviderPosture,
            mapping["fixture_only_source_provider_posture"],
        ),
        fixture_only_source_provider_freshness_status=_enum_value(
            FixtureOnlySourceProviderFreshnessStatus,
            mapping["fixture_only_source_provider_freshness_status"],
        ),
        no_lookahead_status=_enum_value(
            NoLookaheadStatus,
            mapping["no_lookahead_status"],
        ),
        operator_review_status=_enum_value(
            OperatorReviewStatus,
            mapping["operator_review_status"],
        ),
        runtime_gate_status=_enum_value(RuntimeGateStatus, mapping["runtime_gate_status"]),
        provenance_notes=str(mapping.get("provenance_notes", "")),
    )


def validate_fixture_only_source_provider_record(
    record: FixtureOnlySourceProviderRecord,
) -> FixtureOnlySourceProviderValidationResult:
    """Validate fixture-only source/provider metadata with fail-closed behavior."""

    reasons: list[str] = []

    for field_name, value in (
        ("condition_id", record.condition_id),
        ("token_id", record.token_id),
        ("outcome", record.outcome),
        ("fixture_provider_record_id", record.fixture_provider_record_id),
        ("fixture_provider_name", record.fixture_provider_name),
        ("fixture_source_name", record.fixture_source_name),
        ("fixture_snapshot_summary", record.fixture_snapshot_summary),
        ("fixture_observed_at_utc", record.fixture_observed_at_utc),
        ("fixture_available_at_utc", record.fixture_available_at_utc),
        ("decision_time_utc", record.decision_time_utc),
        ("no_lookahead_summary", record.no_lookahead_summary),
        ("operator_review_summary", record.operator_review_summary),
    ):
        if not _is_nonblank_text(value):
            reasons.append(f"{field_name} is missing")

    supplied_contract_result = validate_supplied_market_contract_record(
        record.supplied_market_contract
    )
    if not supplied_contract_result.passed:
        reasons.append("supplied market contract is invalid")

    if record.condition_id != record.supplied_market_contract.condition_id:
        reasons.append("condition_id does not match supplied market contract")

    if record.token_id != record.supplied_market_contract.token_id:
        reasons.append("token_id does not match supplied market contract")

    if record.outcome != record.supplied_market_contract.outcome:
        reasons.append("outcome does not match supplied market contract")

    if (
        record.fixture_only_source_provider_status
        is not FixtureOnlySourceProviderStatus.FIXTURE_ONLY_SOURCE_PROVIDER_RECORDED
    ):
        reasons.append(
            "fixture-only source provider status is "
            f"{record.fixture_only_source_provider_status.value}"
        )

    if (
        record.fixture_only_source_provider_posture
        is not FixtureOnlySourceProviderPosture.FIXTURE_ONLY_LOCAL_STATIC_CALLER_SUPPLIED
    ):
        reasons.append(
            "fixture-only source provider posture is "
            f"{record.fixture_only_source_provider_posture.value}"
        )

    if (
        record.fixture_only_source_provider_freshness_status
        is not FixtureOnlySourceProviderFreshnessStatus.FIXTURE_ONLY_FRESHNESS_RECORDED
    ):
        reasons.append(
            "fixture-only source provider freshness status is "
            f"{record.fixture_only_source_provider_freshness_status.value}"
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
        return FixtureOnlySourceProviderValidationResult(
            severity=ValidationSeverity.BLOCKED,
            passed=False,
            reasons=tuple(reasons),
        )

    return FixtureOnlySourceProviderValidationResult(
        severity=ValidationSeverity.PASSED,
        passed=True,
    )
