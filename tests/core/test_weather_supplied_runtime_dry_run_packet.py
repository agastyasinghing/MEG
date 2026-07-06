import ast
from dataclasses import asdict
from pathlib import Path

import pytest

from meg.weather.stage2 import review_packet_evidence_composition_runtime as rpecr
from meg.weather.stage2 import supplied_evidence_packet_runtime as sepr
from meg.weather.stage2 import supplied_market_contract_runtime as smcr
from meg.weather.stage2 import supplied_market_review_packet_runtime as smrpr
from meg.weather.stage2 import supplied_runtime_dry_run_packet as srdp
from meg.weather.stage2 import supplied_runtime_validation_bundle as srvb


MODULE_PATH = Path("meg/weather/stage2/supplied_runtime_dry_run_packet.py")
TEST_PATH = Path("tests/core/test_weather_supplied_runtime_dry_run_packet.py")


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


def _valid_dry_run_packet(
    **overrides: object,
) -> srdp.SuppliedRuntimeDryRunPacketRecord:
    values = {
        "condition_id": "condition-1",
        "token_id": "token-1",
        "outcome": "Yes",
        "supplied_runtime_validation_bundle": _valid_bundle(),
        "dry_run_packet_id": "dry-run-packet-1",
        "dry_run_summary": "Caller supplied dry-run summary text.",
        "operator_review_summary": "Operator review is required before any later action.",
        "blocked_reason_summary": "",
        "dry_run_packet_status": srdp.DryRunPacketStatus.DRY_RUN_PACKET_RECORDED,
        "dry_run_recommendation_status": (
            srdp.DryRunRecommendationStatus.DRY_RUN_RECOMMENDATION_READY
        ),
        "operator_review_status": srdp.OperatorReviewStatus.OPERATOR_REVIEW_REQUIRED,
        "runtime_gate_status": srdp.RuntimeGateStatus.RUNTIME_GATE_READY,
    }
    values.update(overrides)
    return srdp.SuppliedRuntimeDryRunPacketRecord(**values)


def _assert_blocked_with_reason(
    record: srdp.SuppliedRuntimeDryRunPacketRecord,
    reason: str,
) -> None:
    result = srdp.validate_supplied_runtime_dry_run_packet_record(record)
    assert result.passed is False
    assert result.severity is srdp.ValidationSeverity.BLOCKED
    assert reason in result.reasons


def test_enums_are_closed_sets() -> None:
    assert srdp.DryRunPacketStatus.values() == frozenset(
        {
            "dry_run_packet_recorded",
            "dry_run_packet_missing",
            "dry_run_packet_ambiguous",
            "dry_run_packet_unsupported",
            "dry_run_packet_unknown",
        }
    )
    assert srdp.DryRunRecommendationStatus.values() == frozenset(
        {
            "dry_run_recommendation_ready",
            "dry_run_recommendation_blocked",
            "dry_run_recommendation_requires_manual_review",
            "dry_run_recommendation_unknown",
        }
    )
    assert srdp.OperatorReviewStatus.values() == frozenset(
        {
            "operator_review_required",
            "operator_review_missing",
            "operator_review_ambiguous",
            "operator_review_not_required",
            "operator_review_unknown",
        }
    )
    assert srdp.RuntimeGateStatus.values() == frozenset(
        {
            "runtime_gate_ready",
            "runtime_gate_blocked",
            "runtime_gate_requires_manual_review",
            "runtime_gate_unknown",
        }
    )
    assert srdp.ValidationSeverity.values() == frozenset(
        {"passed", "caution", "failed", "blocked"}
    )


def test_dataclass_construction() -> None:
    record = _valid_dry_run_packet(provenance_notes="operator supplied dry-run packet")

    assert record.condition_id == "condition-1"
    assert record.token_id == "token-1"
    assert record.outcome == "Yes"
    assert isinstance(
        record.supplied_runtime_validation_bundle,
        srvb.SuppliedRuntimeValidationBundleRecord,
    )
    assert record.dry_run_packet_status is srdp.DryRunPacketStatus.DRY_RUN_PACKET_RECORDED
    assert record.provenance_notes == "operator supplied dry-run packet"


def test_mapping_construction_coerces_string_enums_and_nested_validation_bundle_mapping() -> None:
    record = srdp.supplied_runtime_dry_run_packet_record_from_mapping(
        {
            "condition_id": "condition-1",
            "token_id": "token-1",
            "outcome": "Yes",
            "supplied_runtime_validation_bundle": asdict(_valid_bundle()),
            "dry_run_packet_id": "dry-run-packet-2",
            "dry_run_summary": "Caller supplied dry-run summary text.",
            "operator_review_summary": "Operator review is required before any later action.",
            "blocked_reason_summary": "",
            "dry_run_packet_status": "dry_run_packet_recorded",
            "dry_run_recommendation_status": "dry_run_recommendation_ready",
            "operator_review_status": "operator_review_required",
            "runtime_gate_status": "runtime_gate_ready",
            "provenance_notes": "dry-run note",
        }
    )

    assert isinstance(
        record.supplied_runtime_validation_bundle,
        srvb.SuppliedRuntimeValidationBundleRecord,
    )
    assert record.dry_run_packet_status is srdp.DryRunPacketStatus.DRY_RUN_PACKET_RECORDED
    assert record.dry_run_recommendation_status is (
        srdp.DryRunRecommendationStatus.DRY_RUN_RECOMMENDATION_READY
    )
    assert record.operator_review_status is srdp.OperatorReviewStatus.OPERATOR_REVIEW_REQUIRED
    assert record.runtime_gate_status is srdp.RuntimeGateStatus.RUNTIME_GATE_READY
    assert record.provenance_notes == "dry-run note"


def test_minimal_valid_dry_run_packet_passes() -> None:
    result = srdp.validate_supplied_runtime_dry_run_packet_record(_valid_dry_run_packet())

    assert result.passed is True
    assert result.severity is srdp.ValidationSeverity.PASSED
    assert result.reasons == ()


@pytest.mark.parametrize(
    ("field_name", "reason"),
    (
        ("condition_id", "condition_id is missing"),
        ("token_id", "token_id is missing"),
        ("outcome", "outcome is missing"),
        ("dry_run_packet_id", "dry_run_packet_id is missing"),
        ("dry_run_summary", "dry_run_summary is missing"),
        ("operator_review_summary", "operator_review_summary is missing"),
    ),
)
def test_blank_required_text_fields_fail_closed(field_name: str, reason: str) -> None:
    _assert_blocked_with_reason(
        _valid_dry_run_packet(**{field_name: "  "}, blocked_reason_summary="blocked"),
        reason,
    )


def test_blank_blocked_reason_summary_is_allowed_for_passing_packet() -> None:
    result = srdp.validate_supplied_runtime_dry_run_packet_record(
        _valid_dry_run_packet(blocked_reason_summary="")
    )

    assert result.passed is True
    assert result.reasons == ()


def test_blank_blocked_reason_summary_fails_when_packet_is_otherwise_blocked() -> None:
    result = srdp.validate_supplied_runtime_dry_run_packet_record(
        _valid_dry_run_packet(dry_run_summary="  ", blocked_reason_summary="")
    )

    assert result.passed is False
    assert result.reasons == (
        "dry_run_summary is missing",
        "blocked_reason_summary is missing",
    )


def test_nested_invalid_supplied_runtime_validation_bundle_fails_closed() -> None:
    _assert_blocked_with_reason(
        _valid_dry_run_packet(
            supplied_runtime_validation_bundle=_valid_bundle(validation_summary="  "),
            blocked_reason_summary="blocked",
        ),
        "supplied runtime validation bundle validation failed",
    )


@pytest.mark.parametrize(
    ("field_name", "value", "reason"),
    (
        (
            "condition_id",
            "condition-2",
            "condition_id does not match supplied runtime validation bundle",
        ),
        ("token_id", "token-2", "token_id does not match supplied runtime validation bundle"),
        ("outcome", "No", "outcome does not match supplied runtime validation bundle"),
    ),
)
def test_route_mismatch_with_supplied_runtime_validation_bundle_fails_closed(
    field_name: str,
    value: str,
    reason: str,
) -> None:
    _assert_blocked_with_reason(
        _valid_dry_run_packet(
            supplied_runtime_validation_bundle=_valid_bundle(**{field_name: value}),
            blocked_reason_summary="blocked",
        ),
        reason,
    )


@pytest.mark.parametrize(
    "dry_run_packet_status",
    (
        srdp.DryRunPacketStatus.DRY_RUN_PACKET_MISSING,
        srdp.DryRunPacketStatus.DRY_RUN_PACKET_AMBIGUOUS,
        srdp.DryRunPacketStatus.DRY_RUN_PACKET_UNSUPPORTED,
        srdp.DryRunPacketStatus.DRY_RUN_PACKET_UNKNOWN,
    ),
)
def test_non_recorded_dry_run_packet_statuses_fail_closed(
    dry_run_packet_status: srdp.DryRunPacketStatus,
) -> None:
    _assert_blocked_with_reason(
        _valid_dry_run_packet(
            dry_run_packet_status=dry_run_packet_status,
            blocked_reason_summary="blocked",
        ),
        f"dry run packet status is {dry_run_packet_status.value}",
    )


@pytest.mark.parametrize(
    "dry_run_recommendation_status",
    (
        srdp.DryRunRecommendationStatus.DRY_RUN_RECOMMENDATION_BLOCKED,
        srdp.DryRunRecommendationStatus.DRY_RUN_RECOMMENDATION_REQUIRES_MANUAL_REVIEW,
        srdp.DryRunRecommendationStatus.DRY_RUN_RECOMMENDATION_UNKNOWN,
    ),
)
def test_non_ready_dry_run_recommendation_statuses_fail_closed(
    dry_run_recommendation_status: srdp.DryRunRecommendationStatus,
) -> None:
    _assert_blocked_with_reason(
        _valid_dry_run_packet(
            dry_run_recommendation_status=dry_run_recommendation_status,
            blocked_reason_summary="blocked",
        ),
        f"dry run recommendation status is {dry_run_recommendation_status.value}",
    )


@pytest.mark.parametrize(
    "operator_review_status",
    (
        srdp.OperatorReviewStatus.OPERATOR_REVIEW_MISSING,
        srdp.OperatorReviewStatus.OPERATOR_REVIEW_AMBIGUOUS,
        srdp.OperatorReviewStatus.OPERATOR_REVIEW_NOT_REQUIRED,
        srdp.OperatorReviewStatus.OPERATOR_REVIEW_UNKNOWN,
    ),
)
def test_non_required_operator_review_statuses_fail_closed(
    operator_review_status: srdp.OperatorReviewStatus,
) -> None:
    _assert_blocked_with_reason(
        _valid_dry_run_packet(
            operator_review_status=operator_review_status,
            blocked_reason_summary="blocked",
        ),
        f"operator review status is {operator_review_status.value}",
    )


@pytest.mark.parametrize(
    "runtime_gate_status",
    (
        srdp.RuntimeGateStatus.RUNTIME_GATE_BLOCKED,
        srdp.RuntimeGateStatus.RUNTIME_GATE_REQUIRES_MANUAL_REVIEW,
        srdp.RuntimeGateStatus.RUNTIME_GATE_UNKNOWN,
    ),
)
def test_non_ready_runtime_gate_statuses_fail_closed(
    runtime_gate_status: srdp.RuntimeGateStatus,
) -> None:
    _assert_blocked_with_reason(
        _valid_dry_run_packet(
            runtime_gate_status=runtime_gate_status,
            blocked_reason_summary="blocked",
        ),
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
        "execute_order",
        "submit_order",
        "persist",
        "database",
        "postgres",
        "redis",
    )

    for term in forbidden_terms:
        assert term not in source_text
