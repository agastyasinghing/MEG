import ast
from pathlib import Path

import pytest

from meg.weather.stage2 import supplied_evidence_packet_runtime as sepr
from meg.weather.stage2 import supplied_market_contract_runtime as smcr


MODULE_PATH = Path("meg/weather/stage2/supplied_evidence_packet_runtime.py")
TEST_PATH = Path("tests/core/test_weather_supplied_evidence_packet_runtime.py")


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


def _valid_evidence_packet(**overrides: object) -> sepr.SuppliedEvidencePacketRecord:
    values = {
        "condition_id": "condition-1",
        "token_id": "token-1",
        "outcome": "Yes",
        "supplied_market_contract": _valid_contract(),
        "evidence_packet_id": "evidence-packet-1",
        "evidence_summary": "Caller supplied evidence summary text.",
        "evidence_source_descriptor": "Caller supplied manual evidence descriptor.",
        "evidence_observed_at_utc": "2026-01-01T12:00:00Z",
        "evidence_available_at_utc": "2026-01-01T12:05:00Z",
        "decision_time_utc": "2026-01-01T12:10:00Z",
        "evidence_packet_status": sepr.EvidencePacketStatus.EVIDENCE_PACKET_RECORDED,
        "evidence_freshness_status": sepr.EvidenceFreshnessStatus.EVIDENCE_FRESHNESS_RECORDED,
        "evidence_availability_status": (
            sepr.EvidenceAvailabilityStatus.EVIDENCE_AVAILABLE_BEFORE_DECISION
        ),
        "evidence_source_posture": sepr.EvidenceSourcePosture.CALLER_SUPPLIED_STATIC_EVIDENCE,
        "runtime_gate_status": sepr.RuntimeGateStatus.RUNTIME_GATE_READY,
    }
    values.update(overrides)
    return sepr.SuppliedEvidencePacketRecord(**values)


def _assert_blocked_with_reason(
    record: sepr.SuppliedEvidencePacketRecord,
    reason: str,
) -> None:
    result = sepr.validate_supplied_evidence_packet_record(record)
    assert result.passed is False
    assert result.severity is sepr.ValidationSeverity.BLOCKED
    assert reason in result.reasons


def test_enums_are_closed_sets() -> None:
    assert sepr.EvidencePacketStatus.values() == frozenset(
        {
            "evidence_packet_recorded",
            "evidence_packet_missing",
            "evidence_packet_ambiguous",
            "evidence_packet_unsupported",
            "evidence_packet_unknown",
        }
    )
    assert sepr.EvidenceFreshnessStatus.values() == frozenset(
        {
            "evidence_freshness_recorded",
            "evidence_freshness_missing",
            "evidence_freshness_ambiguous",
            "evidence_freshness_stale",
            "evidence_freshness_unknown",
        }
    )
    assert sepr.EvidenceAvailabilityStatus.values() == frozenset(
        {
            "evidence_available_before_decision",
            "evidence_available_at_decision",
            "evidence_available_after_decision",
            "evidence_availability_missing",
            "evidence_availability_ambiguous",
            "evidence_availability_unknown",
        }
    )
    assert sepr.EvidenceSourcePosture.values() == frozenset(
        {
            "caller_supplied_static_evidence",
            "caller_supplied_manual_review_evidence",
            "unsupported_runtime_source_evidence",
            "unknown_source_posture",
        }
    )
    assert sepr.RuntimeGateStatus.values() == frozenset(
        {
            "runtime_gate_ready",
            "runtime_gate_blocked",
            "runtime_gate_requires_manual_review",
            "runtime_gate_unknown",
        }
    )
    assert sepr.ValidationSeverity.values() == frozenset(
        {"passed", "caution", "failed", "blocked"}
    )


def test_dataclass_construction() -> None:
    record = _valid_evidence_packet(provenance_notes="operator supplied evidence")

    assert record.condition_id == "condition-1"
    assert record.token_id == "token-1"
    assert record.outcome == "Yes"
    assert isinstance(record.supplied_market_contract, smcr.SuppliedMarketContractRecord)
    assert record.evidence_packet_id == "evidence-packet-1"
    assert record.evidence_packet_status is sepr.EvidencePacketStatus.EVIDENCE_PACKET_RECORDED
    assert record.provenance_notes == "operator supplied evidence"


def test_mapping_construction_coerces_string_enums_and_nested_contract_mapping() -> None:
    record = sepr.supplied_evidence_packet_record_from_mapping(
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
            "evidence_packet_id": "evidence-packet-2",
            "evidence_summary": "Caller supplied evidence summary text.",
            "evidence_source_descriptor": "Caller supplied static descriptor.",
            "evidence_observed_at_utc": "2026-01-01T12:00:00Z",
            "evidence_available_at_utc": "2026-01-01T12:05:00Z",
            "decision_time_utc": "2026-01-01T12:10:00Z",
            "evidence_packet_status": "evidence_packet_recorded",
            "evidence_freshness_status": "evidence_freshness_recorded",
            "evidence_availability_status": "evidence_available_at_decision",
            "evidence_source_posture": "caller_supplied_manual_review_evidence",
            "runtime_gate_status": "runtime_gate_ready",
            "provenance_notes": "evidence note",
        }
    )

    assert record.supplied_market_contract.outcome == "No"
    assert record.evidence_packet_status is sepr.EvidencePacketStatus.EVIDENCE_PACKET_RECORDED
    assert record.evidence_freshness_status is (
        sepr.EvidenceFreshnessStatus.EVIDENCE_FRESHNESS_RECORDED
    )
    assert record.evidence_availability_status is (
        sepr.EvidenceAvailabilityStatus.EVIDENCE_AVAILABLE_AT_DECISION
    )
    assert record.evidence_source_posture is (
        sepr.EvidenceSourcePosture.CALLER_SUPPLIED_MANUAL_REVIEW_EVIDENCE
    )
    assert record.runtime_gate_status is sepr.RuntimeGateStatus.RUNTIME_GATE_READY
    assert record.provenance_notes == "evidence note"


def test_minimal_valid_evidence_packet_passes() -> None:
    result = sepr.validate_supplied_evidence_packet_record(_valid_evidence_packet())

    assert result.passed is True
    assert result.severity is sepr.ValidationSeverity.PASSED
    assert result.reasons == ()


@pytest.mark.parametrize(
    ("field_name", "reason"),
    (
        ("condition_id", "condition_id is missing"),
        ("token_id", "token_id is missing"),
        ("outcome", "outcome is missing"),
        ("evidence_packet_id", "evidence_packet_id is missing"),
        ("evidence_summary", "evidence_summary is missing"),
        ("evidence_source_descriptor", "evidence_source_descriptor is missing"),
        ("evidence_observed_at_utc", "evidence_observed_at_utc is missing"),
        ("evidence_available_at_utc", "evidence_available_at_utc is missing"),
        ("decision_time_utc", "decision_time_utc is missing"),
    ),
)
def test_blank_required_text_fields_fail_closed(field_name: str, reason: str) -> None:
    _assert_blocked_with_reason(_valid_evidence_packet(**{field_name: "  "}), reason)


def test_nested_invalid_supplied_market_contract_fails_closed() -> None:
    _assert_blocked_with_reason(
        _valid_evidence_packet(supplied_market_contract=_valid_contract(settlement_rule="  ")),
        "supplied market contract validation failed",
    )


def test_condition_id_mismatch_fails_closed() -> None:
    _assert_blocked_with_reason(
        _valid_evidence_packet(condition_id="condition-2"),
        "condition_id does not match supplied market contract",
    )


def test_token_id_mismatch_fails_closed() -> None:
    _assert_blocked_with_reason(
        _valid_evidence_packet(token_id="token-2"),
        "token_id does not match supplied market contract",
    )


def test_outcome_mismatch_fails_closed() -> None:
    _assert_blocked_with_reason(
        _valid_evidence_packet(outcome="No"),
        "outcome does not match supplied market contract",
    )


@pytest.mark.parametrize(
    "evidence_packet_status",
    (
        sepr.EvidencePacketStatus.EVIDENCE_PACKET_MISSING,
        sepr.EvidencePacketStatus.EVIDENCE_PACKET_AMBIGUOUS,
        sepr.EvidencePacketStatus.EVIDENCE_PACKET_UNSUPPORTED,
        sepr.EvidencePacketStatus.EVIDENCE_PACKET_UNKNOWN,
    ),
)
def test_non_recorded_evidence_packet_statuses_fail_closed(
    evidence_packet_status: sepr.EvidencePacketStatus,
) -> None:
    _assert_blocked_with_reason(
        _valid_evidence_packet(evidence_packet_status=evidence_packet_status),
        f"evidence packet status is {evidence_packet_status.value}",
    )


@pytest.mark.parametrize(
    "evidence_freshness_status",
    (
        sepr.EvidenceFreshnessStatus.EVIDENCE_FRESHNESS_MISSING,
        sepr.EvidenceFreshnessStatus.EVIDENCE_FRESHNESS_AMBIGUOUS,
        sepr.EvidenceFreshnessStatus.EVIDENCE_FRESHNESS_STALE,
        sepr.EvidenceFreshnessStatus.EVIDENCE_FRESHNESS_UNKNOWN,
    ),
)
def test_non_recorded_evidence_freshness_statuses_fail_closed(
    evidence_freshness_status: sepr.EvidenceFreshnessStatus,
) -> None:
    _assert_blocked_with_reason(
        _valid_evidence_packet(evidence_freshness_status=evidence_freshness_status),
        f"evidence freshness status is {evidence_freshness_status.value}",
    )


@pytest.mark.parametrize(
    "evidence_availability_status",
    (
        sepr.EvidenceAvailabilityStatus.EVIDENCE_AVAILABLE_AFTER_DECISION,
        sepr.EvidenceAvailabilityStatus.EVIDENCE_AVAILABILITY_MISSING,
        sepr.EvidenceAvailabilityStatus.EVIDENCE_AVAILABILITY_AMBIGUOUS,
        sepr.EvidenceAvailabilityStatus.EVIDENCE_AVAILABILITY_UNKNOWN,
    ),
)
def test_disallowed_evidence_availability_statuses_fail_closed(
    evidence_availability_status: sepr.EvidenceAvailabilityStatus,
) -> None:
    _assert_blocked_with_reason(
        _valid_evidence_packet(evidence_availability_status=evidence_availability_status),
        f"evidence availability status is {evidence_availability_status.value}",
    )


@pytest.mark.parametrize(
    "evidence_source_posture",
    (
        sepr.EvidenceSourcePosture.UNSUPPORTED_RUNTIME_SOURCE_EVIDENCE,
        sepr.EvidenceSourcePosture.UNKNOWN_SOURCE_POSTURE,
    ),
)
def test_unsupported_or_unknown_source_postures_fail_closed(
    evidence_source_posture: sepr.EvidenceSourcePosture,
) -> None:
    _assert_blocked_with_reason(
        _valid_evidence_packet(evidence_source_posture=evidence_source_posture),
        f"evidence source posture is {evidence_source_posture.value}",
    )


@pytest.mark.parametrize(
    "runtime_gate_status",
    (
        sepr.RuntimeGateStatus.RUNTIME_GATE_BLOCKED,
        sepr.RuntimeGateStatus.RUNTIME_GATE_REQUIRES_MANUAL_REVIEW,
        sepr.RuntimeGateStatus.RUNTIME_GATE_UNKNOWN,
    ),
)
def test_non_ready_runtime_gate_statuses_fail_closed(
    runtime_gate_status: sepr.RuntimeGateStatus,
) -> None:
    _assert_blocked_with_reason(
        _valid_evidence_packet(runtime_gate_status=runtime_gate_status),
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
