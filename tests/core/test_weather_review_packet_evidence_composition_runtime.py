import ast
from dataclasses import asdict
from pathlib import Path

import pytest

from meg.weather.stage2 import review_packet_evidence_composition_runtime as rpecr
from meg.weather.stage2 import supplied_evidence_packet_runtime as sepr
from meg.weather.stage2 import supplied_market_contract_runtime as smcr
from meg.weather.stage2 import supplied_market_review_packet_runtime as smrpr


MODULE_PATH = Path("meg/weather/stage2/review_packet_evidence_composition_runtime.py")
TEST_PATH = Path("tests/core/test_weather_review_packet_evidence_composition_runtime.py")


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


def _valid_review_packet(**overrides: object) -> smrpr.SuppliedMarketReviewPacketRecord:
    values = {
        "condition_id": "condition-1",
        "token_id": "token-1",
        "outcome": "Yes",
        "supplied_market_contract": _valid_contract(),
        "review_packet_id": "review-packet-1",
        "review_summary": "Caller supplied review summary text.",
        "evidence_summary": "Caller supplied evidence summary text.",
        "blocked_reason_summary": "",
        "review_packet_status": smrpr.ReviewPacketStatus.REVIEW_PACKET_RECORDED,
        "review_recommendation_status": (
            smrpr.ReviewRecommendationStatus.REVIEW_RECOMMENDATION_READY
        ),
        "evidence_summary_status": smrpr.EvidenceSummaryStatus.EVIDENCE_SUMMARY_RECORDED,
        "runtime_gate_status": smrpr.RuntimeGateStatus.RUNTIME_GATE_READY,
    }
    values.update(overrides)
    return smrpr.SuppliedMarketReviewPacketRecord(**values)


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


def _valid_composition(
    **overrides: object,
) -> rpecr.ReviewPacketEvidenceCompositionRecord:
    values = {
        "condition_id": "condition-1",
        "token_id": "token-1",
        "outcome": "Yes",
        "supplied_market_review_packet": _valid_review_packet(),
        "supplied_evidence_packet": _valid_evidence_packet(),
        "composition_id": "composition-1",
        "composition_summary": "Caller supplied composition summary text.",
        "composition_status": rpecr.CompositionStatus.COMPOSITION_RECORDED,
        "evidence_review_alignment_status": (
            rpecr.EvidenceReviewAlignmentStatus.EVIDENCE_REVIEW_ALIGNED
        ),
        "runtime_gate_status": rpecr.RuntimeGateStatus.RUNTIME_GATE_READY,
    }
    values.update(overrides)
    return rpecr.ReviewPacketEvidenceCompositionRecord(**values)


def _assert_blocked_with_reason(
    record: rpecr.ReviewPacketEvidenceCompositionRecord,
    reason: str,
) -> None:
    result = rpecr.validate_review_packet_evidence_composition_record(record)
    assert result.passed is False
    assert result.severity is rpecr.ValidationSeverity.BLOCKED
    assert reason in result.reasons


def test_enums_are_closed_sets() -> None:
    assert rpecr.CompositionStatus.values() == frozenset(
        {
            "composition_recorded",
            "composition_missing",
            "composition_ambiguous",
            "composition_unsupported",
            "composition_unknown",
        }
    )
    assert rpecr.EvidenceReviewAlignmentStatus.values() == frozenset(
        {
            "evidence_review_aligned",
            "evidence_review_mismatch",
            "evidence_review_missing",
            "evidence_review_ambiguous",
            "evidence_review_unknown",
        }
    )
    assert rpecr.RuntimeGateStatus.values() == frozenset(
        {
            "runtime_gate_ready",
            "runtime_gate_blocked",
            "runtime_gate_requires_manual_review",
            "runtime_gate_unknown",
        }
    )
    assert rpecr.ValidationSeverity.values() == frozenset(
        {"passed", "caution", "failed", "blocked"}
    )


def test_dataclass_construction() -> None:
    record = _valid_composition(provenance_notes="operator supplied composition")

    assert record.condition_id == "condition-1"
    assert record.token_id == "token-1"
    assert record.outcome == "Yes"
    assert isinstance(
        record.supplied_market_review_packet,
        smrpr.SuppliedMarketReviewPacketRecord,
    )
    assert isinstance(record.supplied_evidence_packet, sepr.SuppliedEvidencePacketRecord)
    assert record.composition_status is rpecr.CompositionStatus.COMPOSITION_RECORDED
    assert record.provenance_notes == "operator supplied composition"


def test_mapping_construction_coerces_string_enums_and_nested_packet_mappings() -> None:
    review_packet = asdict(
        _valid_review_packet(
            outcome="No",
            supplied_market_contract=_valid_contract(outcome="No"),
        )
    )
    evidence_packet = asdict(
        _valid_evidence_packet(
            outcome="No",
            supplied_market_contract=_valid_contract(outcome="No"),
        )
    )

    record = rpecr.review_packet_evidence_composition_record_from_mapping(
        {
            "condition_id": "condition-1",
            "token_id": "token-1",
            "outcome": "No",
            "supplied_market_review_packet": review_packet,
            "supplied_evidence_packet": evidence_packet,
            "composition_id": "composition-2",
            "composition_summary": "Caller supplied composition summary text.",
            "composition_status": "composition_recorded",
            "evidence_review_alignment_status": "evidence_review_aligned",
            "runtime_gate_status": "runtime_gate_ready",
            "provenance_notes": "composition note",
        }
    )

    assert record.supplied_market_review_packet.outcome == "No"
    assert record.supplied_evidence_packet.outcome == "No"
    assert record.composition_status is rpecr.CompositionStatus.COMPOSITION_RECORDED
    assert record.evidence_review_alignment_status is (
        rpecr.EvidenceReviewAlignmentStatus.EVIDENCE_REVIEW_ALIGNED
    )
    assert record.runtime_gate_status is rpecr.RuntimeGateStatus.RUNTIME_GATE_READY
    assert record.provenance_notes == "composition note"


def test_minimal_valid_composition_passes() -> None:
    result = rpecr.validate_review_packet_evidence_composition_record(_valid_composition())

    assert result.passed is True
    assert result.severity is rpecr.ValidationSeverity.PASSED
    assert result.reasons == ()


@pytest.mark.parametrize(
    ("field_name", "reason"),
    (
        ("condition_id", "condition_id is missing"),
        ("token_id", "token_id is missing"),
        ("outcome", "outcome is missing"),
        ("composition_id", "composition_id is missing"),
        ("composition_summary", "composition_summary is missing"),
    ),
)
def test_blank_required_text_fields_fail_closed(field_name: str, reason: str) -> None:
    _assert_blocked_with_reason(_valid_composition(**{field_name: "  "}), reason)


def test_nested_invalid_supplied_market_review_packet_fails_closed() -> None:
    _assert_blocked_with_reason(
        _valid_composition(
            supplied_market_review_packet=_valid_review_packet(review_summary="  ")
        ),
        "supplied market review packet validation failed",
    )


def test_nested_invalid_supplied_evidence_packet_fails_closed() -> None:
    _assert_blocked_with_reason(
        _valid_composition(
            supplied_evidence_packet=_valid_evidence_packet(evidence_summary="  ")
        ),
        "supplied evidence packet validation failed",
    )


def test_condition_id_mismatch_with_supplied_market_review_packet_fails_closed() -> None:
    _assert_blocked_with_reason(
        _valid_composition(
            supplied_market_review_packet=_valid_review_packet(condition_id="condition-2")
        ),
        "condition_id does not match supplied market review packet",
    )


def test_token_id_mismatch_with_supplied_market_review_packet_fails_closed() -> None:
    _assert_blocked_with_reason(
        _valid_composition(
            supplied_market_review_packet=_valid_review_packet(token_id="token-2")
        ),
        "token_id does not match supplied market review packet",
    )


def test_outcome_mismatch_with_supplied_market_review_packet_fails_closed() -> None:
    _assert_blocked_with_reason(
        _valid_composition(
            supplied_market_review_packet=_valid_review_packet(outcome="No")
        ),
        "outcome does not match supplied market review packet",
    )


def test_condition_id_mismatch_with_supplied_evidence_packet_fails_closed() -> None:
    _assert_blocked_with_reason(
        _valid_composition(
            supplied_evidence_packet=_valid_evidence_packet(condition_id="condition-2")
        ),
        "condition_id does not match supplied evidence packet",
    )


def test_token_id_mismatch_with_supplied_evidence_packet_fails_closed() -> None:
    _assert_blocked_with_reason(
        _valid_composition(
            supplied_evidence_packet=_valid_evidence_packet(token_id="token-2")
        ),
        "token_id does not match supplied evidence packet",
    )


def test_outcome_mismatch_with_supplied_evidence_packet_fails_closed() -> None:
    _assert_blocked_with_reason(
        _valid_composition(
            supplied_evidence_packet=_valid_evidence_packet(outcome="No")
        ),
        "outcome does not match supplied evidence packet",
    )


def test_supplied_market_review_packet_and_supplied_evidence_packet_id_mismatch_fails_closed() -> None:
    _assert_blocked_with_reason(
        _valid_composition(
            supplied_market_review_packet=_valid_review_packet(condition_id="condition-2"),
            supplied_evidence_packet=_valid_evidence_packet(condition_id="condition-3"),
        ),
        "supplied market review packet does not match supplied evidence packet",
    )


def test_nested_supplied_market_contracts_mismatch_fails_closed() -> None:
    review_packet = _valid_review_packet(
        supplied_market_contract=_valid_contract(condition_id="condition-2")
    )
    evidence_packet = _valid_evidence_packet(
        supplied_market_contract=_valid_contract(condition_id="condition-3")
    )

    _assert_blocked_with_reason(
        _valid_composition(
            supplied_market_review_packet=review_packet,
            supplied_evidence_packet=evidence_packet,
        ),
        "nested supplied market contracts do not match",
    )


def test_evidence_summary_mismatch_fails_closed() -> None:
    _assert_blocked_with_reason(
        _valid_composition(
            supplied_market_review_packet=_valid_review_packet(
                evidence_summary="review evidence"
            ),
            supplied_evidence_packet=_valid_evidence_packet(
                evidence_summary="packet evidence"
            ),
        ),
        "evidence_summary does not match supplied evidence packet",
    )


@pytest.mark.parametrize(
    "composition_status",
    (
        rpecr.CompositionStatus.COMPOSITION_MISSING,
        rpecr.CompositionStatus.COMPOSITION_AMBIGUOUS,
        rpecr.CompositionStatus.COMPOSITION_UNSUPPORTED,
        rpecr.CompositionStatus.COMPOSITION_UNKNOWN,
    ),
)
def test_non_recorded_composition_statuses_fail_closed(
    composition_status: rpecr.CompositionStatus,
) -> None:
    _assert_blocked_with_reason(
        _valid_composition(composition_status=composition_status),
        f"composition status is {composition_status.value}",
    )


@pytest.mark.parametrize(
    "evidence_review_alignment_status",
    (
        rpecr.EvidenceReviewAlignmentStatus.EVIDENCE_REVIEW_MISMATCH,
        rpecr.EvidenceReviewAlignmentStatus.EVIDENCE_REVIEW_MISSING,
        rpecr.EvidenceReviewAlignmentStatus.EVIDENCE_REVIEW_AMBIGUOUS,
        rpecr.EvidenceReviewAlignmentStatus.EVIDENCE_REVIEW_UNKNOWN,
    ),
)
def test_non_aligned_evidence_review_alignment_statuses_fail_closed(
    evidence_review_alignment_status: rpecr.EvidenceReviewAlignmentStatus,
) -> None:
    _assert_blocked_with_reason(
        _valid_composition(
            evidence_review_alignment_status=evidence_review_alignment_status
        ),
        f"evidence review alignment status is {evidence_review_alignment_status.value}",
    )


@pytest.mark.parametrize(
    "runtime_gate_status",
    (
        rpecr.RuntimeGateStatus.RUNTIME_GATE_BLOCKED,
        rpecr.RuntimeGateStatus.RUNTIME_GATE_REQUIRES_MANUAL_REVIEW,
        rpecr.RuntimeGateStatus.RUNTIME_GATE_UNKNOWN,
    ),
)
def test_non_ready_runtime_gate_statuses_fail_closed(
    runtime_gate_status: rpecr.RuntimeGateStatus,
) -> None:
    _assert_blocked_with_reason(
        _valid_composition(runtime_gate_status=runtime_gate_status),
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
