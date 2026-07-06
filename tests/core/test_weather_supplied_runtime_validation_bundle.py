import ast
from dataclasses import asdict
from pathlib import Path

import pytest

from meg.weather.stage2 import review_packet_evidence_composition_runtime as rpecr
from meg.weather.stage2 import supplied_evidence_packet_runtime as sepr
from meg.weather.stage2 import supplied_market_contract_runtime as smcr
from meg.weather.stage2 import supplied_market_review_packet_runtime as smrpr
from meg.weather.stage2 import supplied_runtime_validation_bundle as srvb


MODULE_PATH = Path("meg/weather/stage2/supplied_runtime_validation_bundle.py")
TEST_PATH = Path("tests/core/test_weather_supplied_runtime_validation_bundle.py")


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


def _valid_bundle(**overrides: object) -> srvb.SuppliedRuntimeValidationBundleRecord:
    values = {
        "condition_id": "condition-1",
        "token_id": "token-1",
        "outcome": "Yes",
        "supplied_market_contract": _valid_contract(),
        "supplied_market_review_packet": _valid_review_packet(),
        "supplied_evidence_packet": _valid_evidence_packet(),
        "review_packet_evidence_composition": _valid_composition(),
        "validation_bundle_id": "validation-bundle-1",
        "validation_summary": "Caller supplied validation summary text.",
        "runtime_validation_bundle_status": (
            srvb.RuntimeValidationBundleStatus.RUNTIME_VALIDATION_BUNDLE_RECORDED
        ),
        "runtime_validation_completeness_status": (
            srvb.RuntimeValidationCompletenessStatus.RUNTIME_VALIDATION_COMPLETE
        ),
        "runtime_gate_status": srvb.RuntimeGateStatus.RUNTIME_GATE_READY,
    }
    values.update(overrides)
    return srvb.SuppliedRuntimeValidationBundleRecord(**values)


def _assert_blocked_with_reason(
    record: srvb.SuppliedRuntimeValidationBundleRecord,
    reason: str,
) -> None:
    result = srvb.validate_supplied_runtime_validation_bundle_record(record)
    assert result.passed is False
    assert result.severity is srvb.ValidationSeverity.BLOCKED
    assert reason in result.reasons


def test_enums_are_closed_sets() -> None:
    assert srvb.RuntimeValidationBundleStatus.values() == frozenset(
        {
            "runtime_validation_bundle_recorded",
            "runtime_validation_bundle_missing",
            "runtime_validation_bundle_ambiguous",
            "runtime_validation_bundle_unsupported",
            "runtime_validation_bundle_unknown",
        }
    )
    assert srvb.RuntimeValidationCompletenessStatus.values() == frozenset(
        {
            "runtime_validation_complete",
            "runtime_validation_incomplete",
            "runtime_validation_ambiguous",
            "runtime_validation_unknown",
        }
    )
    assert srvb.RuntimeGateStatus.values() == frozenset(
        {
            "runtime_gate_ready",
            "runtime_gate_blocked",
            "runtime_gate_requires_manual_review",
            "runtime_gate_unknown",
        }
    )
    assert srvb.ValidationSeverity.values() == frozenset(
        {"passed", "caution", "failed", "blocked"}
    )


def test_dataclass_construction() -> None:
    record = _valid_bundle(provenance_notes="operator supplied validation")

    assert record.condition_id == "condition-1"
    assert record.token_id == "token-1"
    assert record.outcome == "Yes"
    assert isinstance(record.supplied_market_contract, smcr.SuppliedMarketContractRecord)
    assert isinstance(
        record.supplied_market_review_packet,
        smrpr.SuppliedMarketReviewPacketRecord,
    )
    assert isinstance(record.supplied_evidence_packet, sepr.SuppliedEvidencePacketRecord)
    assert isinstance(
        record.review_packet_evidence_composition,
        rpecr.ReviewPacketEvidenceCompositionRecord,
    )
    assert record.runtime_validation_bundle_status is (
        srvb.RuntimeValidationBundleStatus.RUNTIME_VALIDATION_BUNDLE_RECORDED
    )
    assert record.provenance_notes == "operator supplied validation"


def test_mapping_construction_coerces_string_enums_and_nested_record_mappings() -> None:
    record = srvb.supplied_runtime_validation_bundle_record_from_mapping(
        {
            "condition_id": "condition-1",
            "token_id": "token-1",
            "outcome": "Yes",
            "supplied_market_contract": asdict(_valid_contract()),
            "supplied_market_review_packet": asdict(_valid_review_packet()),
            "supplied_evidence_packet": asdict(_valid_evidence_packet()),
            "review_packet_evidence_composition": asdict(_valid_composition()),
            "validation_bundle_id": "validation-bundle-2",
            "validation_summary": "Caller supplied validation summary text.",
            "runtime_validation_bundle_status": "runtime_validation_bundle_recorded",
            "runtime_validation_completeness_status": "runtime_validation_complete",
            "runtime_gate_status": "runtime_gate_ready",
            "provenance_notes": "validation note",
        }
    )

    assert isinstance(record.supplied_market_contract, smcr.SuppliedMarketContractRecord)
    assert isinstance(
        record.supplied_market_review_packet,
        smrpr.SuppliedMarketReviewPacketRecord,
    )
    assert isinstance(record.supplied_evidence_packet, sepr.SuppliedEvidencePacketRecord)
    assert isinstance(
        record.review_packet_evidence_composition,
        rpecr.ReviewPacketEvidenceCompositionRecord,
    )
    assert record.runtime_validation_bundle_status is (
        srvb.RuntimeValidationBundleStatus.RUNTIME_VALIDATION_BUNDLE_RECORDED
    )
    assert record.runtime_validation_completeness_status is (
        srvb.RuntimeValidationCompletenessStatus.RUNTIME_VALIDATION_COMPLETE
    )
    assert record.runtime_gate_status is srvb.RuntimeGateStatus.RUNTIME_GATE_READY
    assert record.provenance_notes == "validation note"


def test_minimal_valid_validation_bundle_passes() -> None:
    result = srvb.validate_supplied_runtime_validation_bundle_record(_valid_bundle())

    assert result.passed is True
    assert result.severity is srvb.ValidationSeverity.PASSED
    assert result.reasons == ()


@pytest.mark.parametrize(
    ("field_name", "reason"),
    (
        ("condition_id", "condition_id is missing"),
        ("token_id", "token_id is missing"),
        ("outcome", "outcome is missing"),
        ("validation_bundle_id", "validation_bundle_id is missing"),
        ("validation_summary", "validation_summary is missing"),
    ),
)
def test_blank_required_text_fields_fail_closed(field_name: str, reason: str) -> None:
    _assert_blocked_with_reason(_valid_bundle(**{field_name: "  "}), reason)


def test_nested_invalid_supplied_market_contract_fails_closed() -> None:
    _assert_blocked_with_reason(
        _valid_bundle(supplied_market_contract=_valid_contract(market_title="  ")),
        "supplied market contract validation failed",
    )


def test_nested_invalid_supplied_market_review_packet_fails_closed() -> None:
    _assert_blocked_with_reason(
        _valid_bundle(
            supplied_market_review_packet=_valid_review_packet(review_summary="  ")
        ),
        "supplied market review packet validation failed",
    )


def test_nested_invalid_supplied_evidence_packet_fails_closed() -> None:
    _assert_blocked_with_reason(
        _valid_bundle(supplied_evidence_packet=_valid_evidence_packet(evidence_summary="  ")),
        "supplied evidence packet validation failed",
    )


def test_nested_invalid_review_packet_evidence_composition_fails_closed() -> None:
    _assert_blocked_with_reason(
        _valid_bundle(
            review_packet_evidence_composition=_valid_composition(composition_summary="  ")
        ),
        "review packet evidence composition validation failed",
    )


@pytest.mark.parametrize(
    ("field_name", "value", "reason"),
    (
        ("condition_id", "condition-2", "condition_id does not match supplied market contract"),
        ("token_id", "token-2", "token_id does not match supplied market contract"),
        ("outcome", "No", "outcome does not match supplied market contract"),
    ),
)
def test_route_mismatch_with_supplied_market_contract_fails_closed(
    field_name: str,
    value: str,
    reason: str,
) -> None:
    _assert_blocked_with_reason(
        _valid_bundle(supplied_market_contract=_valid_contract(**{field_name: value})),
        reason,
    )


@pytest.mark.parametrize(
    ("field_name", "value", "reason"),
    (
        (
            "condition_id",
            "condition-2",
            "condition_id does not match supplied market review packet",
        ),
        ("token_id", "token-2", "token_id does not match supplied market review packet"),
        ("outcome", "No", "outcome does not match supplied market review packet"),
    ),
)
def test_route_mismatch_with_supplied_market_review_packet_fails_closed(
    field_name: str,
    value: str,
    reason: str,
) -> None:
    _assert_blocked_with_reason(
        _valid_bundle(
            supplied_market_review_packet=_valid_review_packet(**{field_name: value})
        ),
        reason,
    )


@pytest.mark.parametrize(
    ("field_name", "value", "reason"),
    (
        ("condition_id", "condition-2", "condition_id does not match supplied evidence packet"),
        ("token_id", "token-2", "token_id does not match supplied evidence packet"),
        ("outcome", "No", "outcome does not match supplied evidence packet"),
    ),
)
def test_route_mismatch_with_supplied_evidence_packet_fails_closed(
    field_name: str,
    value: str,
    reason: str,
) -> None:
    _assert_blocked_with_reason(
        _valid_bundle(supplied_evidence_packet=_valid_evidence_packet(**{field_name: value})),
        reason,
    )


@pytest.mark.parametrize(
    ("field_name", "value", "reason"),
    (
        (
            "condition_id",
            "condition-2",
            "condition_id does not match review packet evidence composition",
        ),
        ("token_id", "token-2", "token_id does not match review packet evidence composition"),
        ("outcome", "No", "outcome does not match review packet evidence composition"),
    ),
)
def test_route_mismatch_with_review_packet_evidence_composition_fails_closed(
    field_name: str,
    value: str,
    reason: str,
) -> None:
    _assert_blocked_with_reason(
        _valid_bundle(review_packet_evidence_composition=_valid_composition(**{field_name: value})),
        reason,
    )


def test_supplied_market_review_packet_contract_mismatch_with_supplied_market_contract_fails_closed() -> None:
    _assert_blocked_with_reason(
        _valid_bundle(
            supplied_market_review_packet=_valid_review_packet(
                supplied_market_contract=_valid_contract(condition_id="condition-2")
            )
        ),
        "supplied market review packet contract does not match supplied market contract",
    )


def test_supplied_evidence_packet_contract_mismatch_with_supplied_market_contract_fails_closed() -> None:
    _assert_blocked_with_reason(
        _valid_bundle(
            supplied_evidence_packet=_valid_evidence_packet(
                supplied_market_contract=_valid_contract(condition_id="condition-2")
            )
        ),
        "supplied evidence packet contract does not match supplied market contract",
    )


def test_composition_review_packet_mismatch_with_supplied_market_review_packet_fails_closed() -> None:
    _assert_blocked_with_reason(
        _valid_bundle(
            review_packet_evidence_composition=_valid_composition(
                supplied_market_review_packet=_valid_review_packet(condition_id="condition-2")
            )
        ),
        "composition review packet does not match supplied market review packet",
    )


def test_composition_evidence_packet_mismatch_with_supplied_evidence_packet_fails_closed() -> None:
    _assert_blocked_with_reason(
        _valid_bundle(
            review_packet_evidence_composition=_valid_composition(
                supplied_evidence_packet=_valid_evidence_packet(condition_id="condition-2")
            )
        ),
        "composition evidence packet does not match supplied evidence packet",
    )


def test_composition_nested_contracts_mismatch_with_supplied_market_contract_fails_closed() -> None:
    _assert_blocked_with_reason(
        _valid_bundle(
            review_packet_evidence_composition=_valid_composition(
                supplied_market_review_packet=_valid_review_packet(
                    supplied_market_contract=_valid_contract(condition_id="condition-2")
                )
            )
        ),
        "composition nested contracts do not match supplied market contract",
    )


@pytest.mark.parametrize(
    "runtime_validation_bundle_status",
    (
        srvb.RuntimeValidationBundleStatus.RUNTIME_VALIDATION_BUNDLE_MISSING,
        srvb.RuntimeValidationBundleStatus.RUNTIME_VALIDATION_BUNDLE_AMBIGUOUS,
        srvb.RuntimeValidationBundleStatus.RUNTIME_VALIDATION_BUNDLE_UNSUPPORTED,
        srvb.RuntimeValidationBundleStatus.RUNTIME_VALIDATION_BUNDLE_UNKNOWN,
    ),
)
def test_non_recorded_runtime_validation_bundle_statuses_fail_closed(
    runtime_validation_bundle_status: srvb.RuntimeValidationBundleStatus,
) -> None:
    _assert_blocked_with_reason(
        _valid_bundle(runtime_validation_bundle_status=runtime_validation_bundle_status),
        f"runtime validation bundle status is {runtime_validation_bundle_status.value}",
    )


@pytest.mark.parametrize(
    "runtime_validation_completeness_status",
    (
        srvb.RuntimeValidationCompletenessStatus.RUNTIME_VALIDATION_INCOMPLETE,
        srvb.RuntimeValidationCompletenessStatus.RUNTIME_VALIDATION_AMBIGUOUS,
        srvb.RuntimeValidationCompletenessStatus.RUNTIME_VALIDATION_UNKNOWN,
    ),
)
def test_non_complete_runtime_validation_completeness_statuses_fail_closed(
    runtime_validation_completeness_status: srvb.RuntimeValidationCompletenessStatus,
) -> None:
    _assert_blocked_with_reason(
        _valid_bundle(
            runtime_validation_completeness_status=runtime_validation_completeness_status
        ),
        f"runtime validation completeness status is {runtime_validation_completeness_status.value}",
    )


@pytest.mark.parametrize(
    "runtime_gate_status",
    (
        srvb.RuntimeGateStatus.RUNTIME_GATE_BLOCKED,
        srvb.RuntimeGateStatus.RUNTIME_GATE_REQUIRES_MANUAL_REVIEW,
        srvb.RuntimeGateStatus.RUNTIME_GATE_UNKNOWN,
    ),
)
def test_non_ready_runtime_gate_statuses_fail_closed(
    runtime_gate_status: srvb.RuntimeGateStatus,
) -> None:
    _assert_blocked_with_reason(
        _valid_bundle(runtime_gate_status=runtime_gate_status),
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
