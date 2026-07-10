import ast
from pathlib import Path

import pytest

from meg.weather.stage2 import fixture_only_source_provider_runtime as fspr
from meg.weather.stage2 import supplied_market_contract_runtime as smcr


MODULE_PATH = Path("meg/weather/stage2/fixture_only_source_provider_runtime.py")
TEST_PATH = Path("tests/core/test_weather_stage2_fixture_only_source_provider_runtime.py")


def _valid_contract(**overrides: object) -> smcr.SuppliedMarketContractRecord:
    values = {
        "condition_id": "condition-1",
        "token_id": "token-1",
        "outcome": "Yes",
        "market_title": "Will this weather market settlement rule resolve yes?",
        "settlement_rule": "Resolves Yes if the supplied settlement condition is met.",
        "event_start_utc": "2026-01-01T00:00:00Z",
        "event_end_utc": "2026-01-02T00:00:00Z",
        "settlement_rule_status": smcr.SettlementRuleStatus.SETTLEMENT_RULE_RECORDED,
        "market_contract_status": smcr.MarketContractStatus.MARKET_CONTRACT_RECORDED,
        "event_timing_status": smcr.EventTimingStatus.EVENT_TIMING_RECORDED,
        "runtime_gate_status": smcr.RuntimeGateStatus.RUNTIME_GATE_READY,
    }
    values.update(overrides)
    return smcr.SuppliedMarketContractRecord(**values)


def _valid_fixture_only_source_provider_record(
    **overrides: object,
) -> fspr.FixtureOnlySourceProviderRecord:
    values = {
        "condition_id": "condition-1",
        "token_id": "token-1",
        "outcome": "Yes",
        "supplied_market_contract": _valid_contract(),
        "fixture_provider_record_id": "fixture-provider-record-1",
        "fixture_provider_name": "Caller supplied static provider label",
        "fixture_source_name": "Caller supplied static source label",
        "fixture_snapshot_summary": "Caller supplied static snapshot summary.",
        "fixture_observed_at_utc": "2026-01-01T12:00:00Z",
        "fixture_available_at_utc": "2026-01-01T12:05:00Z",
        "decision_time_utc": "2026-01-01T12:10:00Z",
        "no_lookahead_summary": "Available time is supplied before decision time.",
        "operator_review_summary": "Operator review remains required before any action.",
        "blocked_reason_summary": "No blocker for this valid fixture-only record.",
        "fixture_only_source_provider_status": (
            fspr.FixtureOnlySourceProviderStatus.FIXTURE_ONLY_SOURCE_PROVIDER_RECORDED
        ),
        "fixture_only_source_provider_posture": (
            fspr.FixtureOnlySourceProviderPosture.FIXTURE_ONLY_LOCAL_STATIC_CALLER_SUPPLIED
        ),
        "fixture_only_source_provider_freshness_status": (
            fspr.FixtureOnlySourceProviderFreshnessStatus.FIXTURE_ONLY_FRESHNESS_RECORDED
        ),
        "no_lookahead_status": fspr.NoLookaheadStatus.NO_LOOKAHEAD_RECORDED,
        "operator_review_status": fspr.OperatorReviewStatus.OPERATOR_REVIEW_REQUIRED,
        "runtime_gate_status": fspr.RuntimeGateStatus.RUNTIME_GATE_READY,
    }
    values.update(overrides)
    return fspr.FixtureOnlySourceProviderRecord(**values)


def _assert_blocked_with_reason(
    record: fspr.FixtureOnlySourceProviderRecord,
    reason: str,
) -> None:
    result = fspr.validate_fixture_only_source_provider_record(record)
    assert result.passed is False
    assert result.severity is fspr.ValidationSeverity.BLOCKED
    assert reason in result.reasons


def test_enums_are_closed_sets() -> None:
    assert fspr.FixtureOnlySourceProviderStatus.values() == frozenset(
        {
            "fixture_only_source_provider_recorded",
            "fixture_only_source_provider_missing",
            "fixture_only_source_provider_ambiguous",
            "fixture_only_source_provider_unsupported",
            "fixture_only_source_provider_unknown",
        }
    )
    assert fspr.FixtureOnlySourceProviderPosture.values() == frozenset(
        {
            "fixture_only_local_static_caller_supplied",
            "fixture_only_missing",
            "fixture_only_ambiguous",
            "fixture_only_unsupported",
            "fixture_only_unknown",
        }
    )
    assert fspr.FixtureOnlySourceProviderFreshnessStatus.values() == frozenset(
        {
            "fixture_only_freshness_recorded",
            "fixture_only_freshness_missing",
            "fixture_only_freshness_ambiguous",
            "fixture_only_freshness_unknown",
        }
    )
    assert fspr.NoLookaheadStatus.values() == frozenset(
        {
            "no_lookahead_recorded",
            "no_lookahead_missing",
            "no_lookahead_ambiguous",
            "no_lookahead_unknown",
        }
    )
    assert fspr.OperatorReviewStatus.values() == frozenset(
        {
            "operator_review_required",
            "operator_review_missing",
            "operator_review_ambiguous",
            "operator_review_not_required",
            "operator_review_unknown",
        }
    )
    assert fspr.RuntimeGateStatus.values() == frozenset(
        {
            "runtime_gate_ready",
            "runtime_gate_blocked",
            "runtime_gate_requires_manual_review",
            "runtime_gate_unknown",
        }
    )
    assert fspr.ValidationSeverity.values() == frozenset(
        {"passed", "caution", "failed", "blocked"}
    )


def test_dataclass_construction() -> None:
    record = _valid_fixture_only_source_provider_record(provenance_notes="review note")

    assert record.condition_id == "condition-1"
    assert record.token_id == "token-1"
    assert record.outcome == "Yes"
    assert record.supplied_market_contract.condition_id == "condition-1"
    assert record.fixture_provider_record_id == "fixture-provider-record-1"
    assert record.provenance_notes == "review note"


def test_mapping_construction_coerces_string_enums_and_nested_contract_mapping() -> None:
    contract_mapping = {
        "condition_id": "condition-1",
        "token_id": "token-1",
        "outcome": "Yes",
        "market_title": "Will this weather market settlement rule resolve yes?",
        "settlement_rule": "Resolves Yes if the supplied settlement condition is met.",
        "event_start_utc": "2026-01-01T00:00:00Z",
        "event_end_utc": "2026-01-02T00:00:00Z",
        "settlement_rule_status": "settlement_rule_recorded",
        "market_contract_status": "market_contract_recorded",
        "event_timing_status": "event_timing_recorded",
        "runtime_gate_status": "runtime_gate_ready",
    }
    record = fspr.fixture_only_source_provider_record_from_mapping(
        {
            "condition_id": "condition-1",
            "token_id": "token-1",
            "outcome": "Yes",
            "supplied_market_contract": contract_mapping,
            "fixture_provider_record_id": "fixture-provider-record-1",
            "fixture_provider_name": "Caller supplied static provider label",
            "fixture_source_name": "Caller supplied static source label",
            "fixture_snapshot_summary": "Caller supplied static snapshot summary.",
            "fixture_observed_at_utc": "2026-01-01T12:00:00Z",
            "fixture_available_at_utc": "2026-01-01T12:05:00Z",
            "decision_time_utc": "2026-01-01T12:10:00Z",
            "no_lookahead_summary": "Available time is supplied before decision time.",
            "operator_review_summary": "Operator review remains required.",
            "blocked_reason_summary": "No blocker.",
            "fixture_only_source_provider_status": "fixture_only_source_provider_recorded",
            "fixture_only_source_provider_posture": "fixture_only_local_static_caller_supplied",
            "fixture_only_source_provider_freshness_status": "fixture_only_freshness_recorded",
            "no_lookahead_status": "no_lookahead_recorded",
            "operator_review_status": "operator_review_required",
            "runtime_gate_status": "runtime_gate_ready",
        }
    )

    assert isinstance(record.supplied_market_contract, smcr.SuppliedMarketContractRecord)
    assert record.fixture_only_source_provider_status is (
        fspr.FixtureOnlySourceProviderStatus.FIXTURE_ONLY_SOURCE_PROVIDER_RECORDED
    )
    assert record.fixture_only_source_provider_posture is (
        fspr.FixtureOnlySourceProviderPosture.FIXTURE_ONLY_LOCAL_STATIC_CALLER_SUPPLIED
    )
    assert record.provenance_notes == ""


def test_valid_record_passes() -> None:
    result = fspr.validate_fixture_only_source_provider_record(
        _valid_fixture_only_source_provider_record()
    )

    assert result.passed is True
    assert result.severity is fspr.ValidationSeverity.PASSED
    assert result.reasons == ()


@pytest.mark.parametrize(
    ("field_name", "reason"),
    (
        ("condition_id", "condition_id is missing"),
        ("token_id", "token_id is missing"),
        ("outcome", "outcome is missing"),
        ("fixture_provider_record_id", "fixture_provider_record_id is missing"),
        ("fixture_provider_name", "fixture_provider_name is missing"),
        ("fixture_source_name", "fixture_source_name is missing"),
        ("fixture_snapshot_summary", "fixture_snapshot_summary is missing"),
        ("fixture_observed_at_utc", "fixture_observed_at_utc is missing"),
        ("fixture_available_at_utc", "fixture_available_at_utc is missing"),
        ("decision_time_utc", "decision_time_utc is missing"),
        ("no_lookahead_summary", "no_lookahead_summary is missing"),
        ("operator_review_summary", "operator_review_summary is missing"),
    ),
)
def test_blank_required_text_fields_fail_closed(field_name: str, reason: str) -> None:
    _assert_blocked_with_reason(
        _valid_fixture_only_source_provider_record(**{field_name: "  "}),
        reason,
    )


def test_blank_blocked_reason_summary_is_allowed_when_otherwise_valid() -> None:
    result = fspr.validate_fixture_only_source_provider_record(
        _valid_fixture_only_source_provider_record(blocked_reason_summary="  ")
    )

    assert result.passed is True
    assert result.reasons == ()


def test_blank_blocked_reason_summary_fails_when_another_failure_exists() -> None:
    result = fspr.validate_fixture_only_source_provider_record(
        _valid_fixture_only_source_provider_record(
            fixture_provider_name="  ",
            blocked_reason_summary="  ",
        )
    )

    assert result.passed is False
    assert result.reasons == (
        "fixture_provider_name is missing",
        "blocked_reason_summary is missing",
    )


def test_nested_invalid_supplied_market_contract_fails_closed() -> None:
    _assert_blocked_with_reason(
        _valid_fixture_only_source_provider_record(
            supplied_market_contract=_valid_contract(settlement_rule="  ")
        ),
        "supplied market contract is invalid",
    )


def test_condition_id_mismatch_with_supplied_market_contract_fails_closed() -> None:
    _assert_blocked_with_reason(
        _valid_fixture_only_source_provider_record(condition_id="condition-2"),
        "condition_id does not match supplied market contract",
    )


def test_token_id_mismatch_with_supplied_market_contract_fails_closed() -> None:
    _assert_blocked_with_reason(
        _valid_fixture_only_source_provider_record(token_id="token-2"),
        "token_id does not match supplied market contract",
    )


def test_outcome_mismatch_with_supplied_market_contract_fails_closed() -> None:
    _assert_blocked_with_reason(
        _valid_fixture_only_source_provider_record(outcome="No"),
        "outcome does not match supplied market contract",
    )


@pytest.mark.parametrize(
    "status",
    (
        fspr.FixtureOnlySourceProviderStatus.FIXTURE_ONLY_SOURCE_PROVIDER_MISSING,
        fspr.FixtureOnlySourceProviderStatus.FIXTURE_ONLY_SOURCE_PROVIDER_AMBIGUOUS,
        fspr.FixtureOnlySourceProviderStatus.FIXTURE_ONLY_SOURCE_PROVIDER_UNSUPPORTED,
        fspr.FixtureOnlySourceProviderStatus.FIXTURE_ONLY_SOURCE_PROVIDER_UNKNOWN,
    ),
)
def test_non_recorded_fixture_only_source_provider_statuses_fail_closed(
    status: fspr.FixtureOnlySourceProviderStatus,
) -> None:
    _assert_blocked_with_reason(
        _valid_fixture_only_source_provider_record(fixture_only_source_provider_status=status),
        f"fixture-only source provider status is {status.value}",
    )


@pytest.mark.parametrize(
    "posture",
    (
        fspr.FixtureOnlySourceProviderPosture.FIXTURE_ONLY_MISSING,
        fspr.FixtureOnlySourceProviderPosture.FIXTURE_ONLY_AMBIGUOUS,
        fspr.FixtureOnlySourceProviderPosture.FIXTURE_ONLY_UNSUPPORTED,
        fspr.FixtureOnlySourceProviderPosture.FIXTURE_ONLY_UNKNOWN,
    ),
)
def test_non_local_static_caller_supplied_postures_fail_closed(
    posture: fspr.FixtureOnlySourceProviderPosture,
) -> None:
    _assert_blocked_with_reason(
        _valid_fixture_only_source_provider_record(fixture_only_source_provider_posture=posture),
        f"fixture-only source provider posture is {posture.value}",
    )


@pytest.mark.parametrize(
    "freshness_status",
    (
        fspr.FixtureOnlySourceProviderFreshnessStatus.FIXTURE_ONLY_FRESHNESS_MISSING,
        fspr.FixtureOnlySourceProviderFreshnessStatus.FIXTURE_ONLY_FRESHNESS_AMBIGUOUS,
        fspr.FixtureOnlySourceProviderFreshnessStatus.FIXTURE_ONLY_FRESHNESS_UNKNOWN,
    ),
)
def test_non_recorded_freshness_statuses_fail_closed(
    freshness_status: fspr.FixtureOnlySourceProviderFreshnessStatus,
) -> None:
    _assert_blocked_with_reason(
        _valid_fixture_only_source_provider_record(
            fixture_only_source_provider_freshness_status=freshness_status
        ),
        f"fixture-only source provider freshness status is {freshness_status.value}",
    )


@pytest.mark.parametrize(
    "status",
    (
        fspr.NoLookaheadStatus.NO_LOOKAHEAD_MISSING,
        fspr.NoLookaheadStatus.NO_LOOKAHEAD_AMBIGUOUS,
        fspr.NoLookaheadStatus.NO_LOOKAHEAD_UNKNOWN,
    ),
)
def test_non_recorded_no_lookahead_statuses_fail_closed(
    status: fspr.NoLookaheadStatus,
) -> None:
    _assert_blocked_with_reason(
        _valid_fixture_only_source_provider_record(no_lookahead_status=status),
        f"no-lookahead status is {status.value}",
    )


@pytest.mark.parametrize(
    "status",
    (
        fspr.OperatorReviewStatus.OPERATOR_REVIEW_MISSING,
        fspr.OperatorReviewStatus.OPERATOR_REVIEW_AMBIGUOUS,
        fspr.OperatorReviewStatus.OPERATOR_REVIEW_NOT_REQUIRED,
        fspr.OperatorReviewStatus.OPERATOR_REVIEW_UNKNOWN,
    ),
)
def test_non_required_operator_review_statuses_fail_closed(
    status: fspr.OperatorReviewStatus,
) -> None:
    _assert_blocked_with_reason(
        _valid_fixture_only_source_provider_record(operator_review_status=status),
        f"operator review status is {status.value}",
    )


@pytest.mark.parametrize(
    "status",
    (
        fspr.RuntimeGateStatus.RUNTIME_GATE_BLOCKED,
        fspr.RuntimeGateStatus.RUNTIME_GATE_REQUIRES_MANUAL_REVIEW,
        fspr.RuntimeGateStatus.RUNTIME_GATE_UNKNOWN,
    ),
)
def test_non_ready_runtime_gates_fail_closed(status: fspr.RuntimeGateStatus) -> None:
    _assert_blocked_with_reason(
        _valid_fixture_only_source_provider_record(runtime_gate_status=status),
        f"runtime gate status is {status.value}",
    )


def test_new_files_do_not_contain_noncanonical_identifier_input_field() -> None:
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


def test_module_source_has_no_live_provider_source_fetching_or_side_effect_calls() -> None:
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
        "execute_order",
        "submit_order",
        "persist",
        "database",
        "postgres",
        "redis",
        "export",
        "write",
        "save",
        "owner_decision",
        "capture_decision",
        "celery",
        "rabbitmq",
        "sqs",
        "enqueue(",
        "dequeue(",
        "publish(",
        "subscribe(",
        "scheduler",
        "provider_client",
        "api_call",
        "scrape",
        "download",
        "credentials",
        "production",
    )

    for term in forbidden_terms:
        assert term not in source_text
