import ast
from pathlib import Path

import pytest

from meg.weather.stage2 import supplied_market_contract_runtime as smcr


MODULE_PATH = Path("meg/weather/stage2/supplied_market_contract_runtime.py")
TEST_PATH = Path("tests/core/test_weather_supplied_market_contract_runtime.py")


def _valid_record(**overrides: object) -> smcr.SuppliedMarketContractRecord:
    values = {
        "condition_id": "condition-1",
        "token_id": "token-1",
        "outcome": "Yes",
        "market_title": "Will this settlement rule resolve yes?",
        "settlement_rule": "Resolves Yes if the supplied event condition is met.",
        "event_start_utc": "2026-01-01T00:00:00Z",
        "event_end_utc": "2026-01-02T00:00:00Z",
        "settlement_rule_status": smcr.SettlementRuleStatus.SETTLEMENT_RULE_RECORDED,
        "market_contract_status": smcr.MarketContractStatus.MARKET_CONTRACT_RECORDED,
        "event_timing_status": smcr.EventTimingStatus.EVENT_TIMING_RECORDED,
        "runtime_gate_status": smcr.RuntimeGateStatus.RUNTIME_GATE_READY,
    }
    values.update(overrides)
    return smcr.SuppliedMarketContractRecord(**values)


def _assert_blocked_with_reason(
    record: smcr.SuppliedMarketContractRecord,
    reason: str,
) -> None:
    result = smcr.validate_supplied_market_contract_record(record)
    assert result.passed is False
    assert result.severity is smcr.ValidationSeverity.BLOCKED
    assert reason in result.reasons


def test_enums_are_closed_sets() -> None:
    assert smcr.SettlementRuleStatus.values() == frozenset(
        {
            "settlement_rule_recorded",
            "settlement_rule_missing",
            "settlement_rule_ambiguous",
            "settlement_rule_unsupported",
            "settlement_rule_unknown",
        }
    )
    assert smcr.MarketContractStatus.values() == frozenset(
        {
            "market_contract_recorded",
            "market_contract_missing",
            "market_contract_ambiguous",
            "market_contract_unsupported",
            "market_contract_unknown",
        }
    )
    assert smcr.EventTimingStatus.values() == frozenset(
        {
            "event_timing_recorded",
            "event_timing_missing",
            "event_timing_ambiguous",
            "event_timing_unsupported",
            "event_timing_unknown",
        }
    )
    assert smcr.RuntimeGateStatus.values() == frozenset(
        {
            "runtime_gate_ready",
            "runtime_gate_blocked",
            "runtime_gate_requires_manual_review",
            "runtime_gate_unknown",
        }
    )
    assert smcr.ValidationSeverity.values() == frozenset(
        {"passed", "caution", "failed", "blocked"}
    )


def test_dataclass_construction() -> None:
    record = _valid_record(provenance_notes="operator supplied contract fields")

    assert record.condition_id == "condition-1"
    assert record.token_id == "token-1"
    assert record.outcome == "Yes"
    assert record.market_title == "Will this settlement rule resolve yes?"
    assert record.settlement_rule_status is smcr.SettlementRuleStatus.SETTLEMENT_RULE_RECORDED
    assert record.provenance_notes == "operator supplied contract fields"


def test_mapping_construction_coerces_string_enums() -> None:
    record = smcr.supplied_market_contract_record_from_mapping(
        {
            "condition_id": "condition-1",
            "token_id": "token-1",
            "outcome": "No",
            "market_title": "Will this settlement rule resolve no?",
            "settlement_rule": "Resolves No if the supplied event condition is not met.",
            "event_start_utc": "2026-01-01T00:00:00Z",
            "event_end_utc": "2026-01-02T00:00:00Z",
            "settlement_rule_status": "settlement_rule_recorded",
            "market_contract_status": "market_contract_recorded",
            "event_timing_status": "event_timing_recorded",
            "runtime_gate_status": "runtime_gate_ready",
            "provenance_notes": "review note",
        }
    )

    assert record.settlement_rule_status is smcr.SettlementRuleStatus.SETTLEMENT_RULE_RECORDED
    assert record.market_contract_status is smcr.MarketContractStatus.MARKET_CONTRACT_RECORDED
    assert record.event_timing_status is smcr.EventTimingStatus.EVENT_TIMING_RECORDED
    assert record.runtime_gate_status is smcr.RuntimeGateStatus.RUNTIME_GATE_READY
    assert record.provenance_notes == "review note"


def test_minimal_valid_record_passes() -> None:
    result = smcr.validate_supplied_market_contract_record(_valid_record())

    assert result.passed is True
    assert result.severity is smcr.ValidationSeverity.PASSED
    assert result.reasons == ()


@pytest.mark.parametrize(
    ("field_name", "reason"),
    (
        ("condition_id", "condition_id is missing"),
        ("token_id", "token_id is missing"),
        ("outcome", "outcome is missing"),
        ("market_title", "market_title is missing"),
        ("settlement_rule", "settlement_rule is missing"),
        ("event_start_utc", "event_start_utc is missing"),
        ("event_end_utc", "event_end_utc is missing"),
    ),
)
def test_blank_required_text_fields_fail_closed(field_name: str, reason: str) -> None:
    _assert_blocked_with_reason(_valid_record(**{field_name: "  "}), reason)


@pytest.mark.parametrize(
    "settlement_rule_status",
    (
        smcr.SettlementRuleStatus.SETTLEMENT_RULE_MISSING,
        smcr.SettlementRuleStatus.SETTLEMENT_RULE_AMBIGUOUS,
        smcr.SettlementRuleStatus.SETTLEMENT_RULE_UNSUPPORTED,
        smcr.SettlementRuleStatus.SETTLEMENT_RULE_UNKNOWN,
    ),
)
def test_non_recorded_settlement_rule_statuses_fail_closed(
    settlement_rule_status: smcr.SettlementRuleStatus,
) -> None:
    _assert_blocked_with_reason(
        _valid_record(settlement_rule_status=settlement_rule_status),
        f"settlement rule status is {settlement_rule_status.value}",
    )


@pytest.mark.parametrize(
    "market_contract_status",
    (
        smcr.MarketContractStatus.MARKET_CONTRACT_MISSING,
        smcr.MarketContractStatus.MARKET_CONTRACT_AMBIGUOUS,
        smcr.MarketContractStatus.MARKET_CONTRACT_UNSUPPORTED,
        smcr.MarketContractStatus.MARKET_CONTRACT_UNKNOWN,
    ),
)
def test_non_recorded_market_contract_statuses_fail_closed(
    market_contract_status: smcr.MarketContractStatus,
) -> None:
    _assert_blocked_with_reason(
        _valid_record(market_contract_status=market_contract_status),
        f"market contract status is {market_contract_status.value}",
    )


@pytest.mark.parametrize(
    "event_timing_status",
    (
        smcr.EventTimingStatus.EVENT_TIMING_MISSING,
        smcr.EventTimingStatus.EVENT_TIMING_AMBIGUOUS,
        smcr.EventTimingStatus.EVENT_TIMING_UNSUPPORTED,
        smcr.EventTimingStatus.EVENT_TIMING_UNKNOWN,
    ),
)
def test_non_recorded_event_timing_statuses_fail_closed(
    event_timing_status: smcr.EventTimingStatus,
) -> None:
    _assert_blocked_with_reason(
        _valid_record(event_timing_status=event_timing_status),
        f"event timing status is {event_timing_status.value}",
    )


@pytest.mark.parametrize(
    "gate_status",
    (
        smcr.RuntimeGateStatus.RUNTIME_GATE_BLOCKED,
        smcr.RuntimeGateStatus.RUNTIME_GATE_REQUIRES_MANUAL_REVIEW,
        smcr.RuntimeGateStatus.RUNTIME_GATE_UNKNOWN,
    ),
)
def test_non_ready_runtime_gate_statuses_fail_closed(gate_status: smcr.RuntimeGateStatus) -> None:
    _assert_blocked_with_reason(
        _valid_record(runtime_gate_status=gate_status),
        f"runtime gate status is {gate_status.value}",
    )


def test_new_files_do_not_contain_noncanonical_identifier_string() -> None:
    forbidden = "market" "_id"

    assert forbidden not in MODULE_PATH.read_text(encoding="utf-8")
    assert forbidden not in TEST_PATH.read_text(encoding="utf-8")


def _module_source_without_docstrings() -> str:
    source_text = MODULE_PATH.read_text(encoding="utf-8")
    parsed = ast.parse(source_text)
    for node in ast.walk(parsed):
        if not hasattr(node, "body") or not node.body:
            continue
        first_statement = node.body[0]
        if isinstance(first_statement, ast.Expr) and isinstance(
            first_statement.value,
            ast.Constant,
        ):
            if isinstance(first_statement.value.value, str):
                first_statement.value = ast.Constant(value="")
    return ast.unparse(parsed)


def test_module_source_has_no_network_provider_execution_or_file_io_calls() -> None:
    source_text = _module_source_without_docstrings()
    forbidden_terms = (
        "requests",
        "httpx",
        "urllib",
        "aiohttp",
        "boto3",
        "polymarket",
        "kalshi",
        "duckdb",
        "pandas",
        "subprocess",
        "open(",
        ".read_text(",
        ".write_text(",
        "socket",
        "os.environ",
        "dotenv",
        "place_order",
        "paper_trade",
        "trade",
        "backtest",
        "score",
    )

    for term in forbidden_terms:
        assert term not in source_text
