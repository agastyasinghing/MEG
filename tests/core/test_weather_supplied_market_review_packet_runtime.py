import ast
from pathlib import Path

import pytest

from meg.weather.stage2 import supplied_market_contract_runtime as smcr
from meg.weather.stage2 import supplied_market_review_packet_runtime as smrpr


MODULE_PATH = Path("meg/weather/stage2/supplied_market_review_packet_runtime.py")
TEST_PATH = Path("tests/core/test_weather_supplied_market_review_packet_runtime.py")


def _valid_contract(**overrides: object) -> smcr.SuppliedMarketContractRecord:
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


def _valid_packet(**overrides: object) -> smrpr.SuppliedMarketReviewPacketRecord:
    values = {
        "condition_id": "condition-1",
        "token_id": "token-1",
        "outcome": "Yes",
        "supplied_market_contract": _valid_contract(),
        "review_packet_id": "review-packet-1",
        "review_summary": "Operator review packet is ready for manual review.",
        "evidence_summary": "Caller supplied evidence summary text.",
        "blocked_reason_summary": "No blocking reasons were supplied.",
        "review_packet_status": smrpr.ReviewPacketStatus.REVIEW_PACKET_RECORDED,
        "review_recommendation_status": (
            smrpr.ReviewRecommendationStatus.REVIEW_RECOMMENDATION_READY
        ),
        "evidence_summary_status": smrpr.EvidenceSummaryStatus.EVIDENCE_SUMMARY_RECORDED,
        "runtime_gate_status": smrpr.RuntimeGateStatus.RUNTIME_GATE_READY,
    }
    values.update(overrides)
    return smrpr.SuppliedMarketReviewPacketRecord(**values)


def _assert_blocked_with_reason(
    record: smrpr.SuppliedMarketReviewPacketRecord,
    reason: str,
) -> None:
    result = smrpr.validate_supplied_market_review_packet_record(record)
    assert result.passed is False
    assert result.severity is smrpr.ValidationSeverity.BLOCKED
    assert reason in result.reasons


def test_enums_are_closed_sets() -> None:
    assert smrpr.ReviewPacketStatus.values() == frozenset(
        {
            "review_packet_recorded",
            "review_packet_missing",
            "review_packet_ambiguous",
            "review_packet_unsupported",
            "review_packet_unknown",
        }
    )
    assert smrpr.ReviewRecommendationStatus.values() == frozenset(
        {
            "review_recommendation_ready",
            "review_recommendation_blocked",
            "review_recommendation_requires_manual_review",
            "review_recommendation_unknown",
        }
    )
    assert smrpr.EvidenceSummaryStatus.values() == frozenset(
        {
            "evidence_summary_recorded",
            "evidence_summary_missing",
            "evidence_summary_ambiguous",
            "evidence_summary_unsupported",
            "evidence_summary_unknown",
        }
    )
    assert smrpr.RuntimeGateStatus.values() == frozenset(
        {
            "runtime_gate_ready",
            "runtime_gate_blocked",
            "runtime_gate_requires_manual_review",
            "runtime_gate_unknown",
        }
    )
    assert smrpr.ValidationSeverity.values() == frozenset(
        {"passed", "caution", "failed", "blocked"}
    )


def test_dataclass_construction() -> None:
    record = _valid_packet(provenance_notes="operator supplied review packet")

    assert record.condition_id == "condition-1"
    assert record.token_id == "token-1"
    assert record.outcome == "Yes"
    assert isinstance(record.supplied_market_contract, smcr.SuppliedMarketContractRecord)
    assert record.review_packet_id == "review-packet-1"
    assert record.review_packet_status is smrpr.ReviewPacketStatus.REVIEW_PACKET_RECORDED
    assert record.provenance_notes == "operator supplied review packet"


def test_mapping_construction_coerces_string_enums_and_nested_contract_mapping() -> None:
    record = smrpr.supplied_market_review_packet_record_from_mapping(
        {
            "condition_id": "condition-1",
            "token_id": "token-1",
            "outcome": "No",
            "supplied_market_contract": {
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
            },
            "review_packet_id": "review-packet-2",
            "review_summary": "Operator review packet is ready.",
            "evidence_summary": "Caller supplied evidence summary text.",
            "blocked_reason_summary": "No blocking reasons were supplied.",
            "review_packet_status": "review_packet_recorded",
            "review_recommendation_status": "review_recommendation_ready",
            "evidence_summary_status": "evidence_summary_recorded",
            "runtime_gate_status": "runtime_gate_ready",
            "provenance_notes": "review note",
        }
    )

    assert record.supplied_market_contract.outcome == "No"
    assert record.review_packet_status is smrpr.ReviewPacketStatus.REVIEW_PACKET_RECORDED
    assert record.review_recommendation_status is (
        smrpr.ReviewRecommendationStatus.REVIEW_RECOMMENDATION_READY
    )
    assert record.evidence_summary_status is smrpr.EvidenceSummaryStatus.EVIDENCE_SUMMARY_RECORDED
    assert record.runtime_gate_status is smrpr.RuntimeGateStatus.RUNTIME_GATE_READY
    assert record.provenance_notes == "review note"


def test_minimal_valid_packet_passes() -> None:
    result = smrpr.validate_supplied_market_review_packet_record(_valid_packet())

    assert result.passed is True
    assert result.severity is smrpr.ValidationSeverity.PASSED
    assert result.reasons == ()


@pytest.mark.parametrize(
    ("field_name", "reason"),
    (
        ("condition_id", "condition_id is missing"),
        ("token_id", "token_id is missing"),
        ("outcome", "outcome is missing"),
        ("review_packet_id", "review_packet_id is missing"),
        ("review_summary", "review_summary is missing"),
        ("evidence_summary", "evidence_summary is missing"),
    ),
)
def test_blank_required_text_fields_fail_closed(field_name: str, reason: str) -> None:
    _assert_blocked_with_reason(_valid_packet(**{field_name: "  "}), reason)


def test_blank_blocked_reason_summary_is_allowed_for_passing_packet() -> None:
    result = smrpr.validate_supplied_market_review_packet_record(
        _valid_packet(blocked_reason_summary="  ")
    )

    assert result.passed is True
    assert result.severity is smrpr.ValidationSeverity.PASSED
    assert result.reasons == ()


def test_blank_blocked_reason_summary_fails_when_packet_is_otherwise_blocked() -> None:
    result = smrpr.validate_supplied_market_review_packet_record(
        _valid_packet(
            blocked_reason_summary="  ",
            review_packet_status=smrpr.ReviewPacketStatus.REVIEW_PACKET_MISSING,
        )
    )

    assert result.passed is False
    assert result.severity is smrpr.ValidationSeverity.BLOCKED
    assert result.reasons == (
        "review packet status is review_packet_missing",
        "blocked_reason_summary is missing",
    )


def test_nested_invalid_supplied_market_contract_fails_closed() -> None:
    _assert_blocked_with_reason(
        _valid_packet(supplied_market_contract=_valid_contract(settlement_rule="  ")),
        "supplied market contract validation failed",
    )


def test_condition_id_mismatch_fails_closed() -> None:
    _assert_blocked_with_reason(
        _valid_packet(condition_id="condition-2"),
        "condition_id does not match supplied market contract",
    )


def test_token_id_mismatch_fails_closed() -> None:
    _assert_blocked_with_reason(
        _valid_packet(token_id="token-2"),
        "token_id does not match supplied market contract",
    )


def test_outcome_mismatch_fails_closed() -> None:
    _assert_blocked_with_reason(
        _valid_packet(outcome="No"),
        "outcome does not match supplied market contract",
    )


@pytest.mark.parametrize(
    "review_packet_status",
    (
        smrpr.ReviewPacketStatus.REVIEW_PACKET_MISSING,
        smrpr.ReviewPacketStatus.REVIEW_PACKET_AMBIGUOUS,
        smrpr.ReviewPacketStatus.REVIEW_PACKET_UNSUPPORTED,
        smrpr.ReviewPacketStatus.REVIEW_PACKET_UNKNOWN,
    ),
)
def test_non_recorded_review_packet_statuses_fail_closed(
    review_packet_status: smrpr.ReviewPacketStatus,
) -> None:
    _assert_blocked_with_reason(
        _valid_packet(review_packet_status=review_packet_status),
        f"review packet status is {review_packet_status.value}",
    )


@pytest.mark.parametrize(
    "review_recommendation_status",
    (
        smrpr.ReviewRecommendationStatus.REVIEW_RECOMMENDATION_BLOCKED,
        smrpr.ReviewRecommendationStatus.REVIEW_RECOMMENDATION_REQUIRES_MANUAL_REVIEW,
        smrpr.ReviewRecommendationStatus.REVIEW_RECOMMENDATION_UNKNOWN,
    ),
)
def test_non_ready_review_recommendation_statuses_fail_closed(
    review_recommendation_status: smrpr.ReviewRecommendationStatus,
) -> None:
    _assert_blocked_with_reason(
        _valid_packet(review_recommendation_status=review_recommendation_status),
        f"review recommendation status is {review_recommendation_status.value}",
    )


@pytest.mark.parametrize(
    "evidence_summary_status",
    (
        smrpr.EvidenceSummaryStatus.EVIDENCE_SUMMARY_MISSING,
        smrpr.EvidenceSummaryStatus.EVIDENCE_SUMMARY_AMBIGUOUS,
        smrpr.EvidenceSummaryStatus.EVIDENCE_SUMMARY_UNSUPPORTED,
        smrpr.EvidenceSummaryStatus.EVIDENCE_SUMMARY_UNKNOWN,
    ),
)
def test_non_recorded_evidence_summary_statuses_fail_closed(
    evidence_summary_status: smrpr.EvidenceSummaryStatus,
) -> None:
    _assert_blocked_with_reason(
        _valid_packet(evidence_summary_status=evidence_summary_status),
        f"evidence summary status is {evidence_summary_status.value}",
    )


@pytest.mark.parametrize(
    "runtime_gate_status",
    (
        smrpr.RuntimeGateStatus.RUNTIME_GATE_BLOCKED,
        smrpr.RuntimeGateStatus.RUNTIME_GATE_REQUIRES_MANUAL_REVIEW,
        smrpr.RuntimeGateStatus.RUNTIME_GATE_UNKNOWN,
    ),
)
def test_non_ready_runtime_gate_statuses_fail_closed(
    runtime_gate_status: smrpr.RuntimeGateStatus,
) -> None:
    _assert_blocked_with_reason(
        _valid_packet(runtime_gate_status=runtime_gate_status),
        f"runtime gate status is {runtime_gate_status.value}",
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
