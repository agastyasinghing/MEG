import ast
from dataclasses import asdict
from pathlib import Path

import pytest

from meg.weather.stage2 import fixture_only_source_provider_evidence_bridge_runtime as evidence_bridge
from meg.weather.stage2 import fixture_only_source_provider_runtime as fspr
from meg.weather.stage2 import fixture_only_source_provider_validation_bundle_bridge_runtime as bridge
from meg.weather.stage2 import review_packet_evidence_composition_runtime as rpecr
from meg.weather.stage2 import supplied_evidence_packet_runtime as sepr
from meg.weather.stage2 import supplied_market_contract_runtime as smcr
from meg.weather.stage2 import supplied_market_review_packet_runtime as smrpr
from meg.weather.stage2 import supplied_runtime_validation_bundle as srvb


MODULE_PATH = Path(
    "meg/weather/stage2/fixture_only_source_provider_validation_bundle_bridge_runtime.py"
)
TEST_PATH = Path(
    "tests/core/test_weather_stage2_fixture_only_source_provider_validation_bundle_bridge_runtime.py"
)


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


def _valid_fixture_only_source_provider(**overrides: object) -> fspr.FixtureOnlySourceProviderRecord:
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


def _valid_supplied_evidence_packet(**overrides: object) -> sepr.SuppliedEvidencePacketRecord:
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


def _valid_fixture_evidence_bridge(
    **overrides: object,
) -> evidence_bridge.FixtureOnlySourceProviderEvidenceBridgeRecord:
    values = {
        "condition_id": "condition-1",
        "token_id": "token-1",
        "outcome": "Yes",
        "fixture_only_source_provider": _valid_fixture_only_source_provider(),
        "supplied_evidence_packet": _valid_supplied_evidence_packet(),
        "evidence_bridge_id": "fixture-evidence-bridge-1",
        "evidence_bridge_summary": "Fixture-only source/provider linked to supplied evidence.",
        "fixture_source_descriptor_summary": "Caller supplied static source label",
        "evidence_source_descriptor_summary": "Caller supplied manual evidence descriptor.",
        "no_lookahead_summary": "Available time is supplied before decision time.",
        "operator_review_summary": "Operator review remains required before any action.",
        "blocked_reason_summary": "No blocker for this valid bridge record.",
        "fixture_only_evidence_bridge_status": (
            evidence_bridge.FixtureOnlyEvidenceBridgeStatus.FIXTURE_ONLY_EVIDENCE_BRIDGE_RECORDED
        ),
        "fixture_only_evidence_bridge_posture": (
            evidence_bridge.FixtureOnlyEvidenceBridgePosture.FIXTURE_ONLY_EVIDENCE_BRIDGE_IN_MEMORY_ONLY
        ),
        "evidence_bridge_alignment_status": (
            evidence_bridge.EvidenceBridgeAlignmentStatus.EVIDENCE_BRIDGE_ALIGNED
        ),
        "no_lookahead_status": evidence_bridge.NoLookaheadStatus.NO_LOOKAHEAD_RECORDED,
        "operator_review_status": evidence_bridge.OperatorReviewStatus.OPERATOR_REVIEW_REQUIRED,
        "runtime_gate_status": evidence_bridge.RuntimeGateStatus.RUNTIME_GATE_READY,
    }
    values.update(overrides)
    return evidence_bridge.FixtureOnlySourceProviderEvidenceBridgeRecord(**values)


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
        "review_recommendation_status": smrpr.ReviewRecommendationStatus.REVIEW_RECOMMENDATION_READY,
        "evidence_summary_status": smrpr.EvidenceSummaryStatus.EVIDENCE_SUMMARY_RECORDED,
        "runtime_gate_status": smrpr.RuntimeGateStatus.RUNTIME_GATE_READY,
    }
    values.update(overrides)
    return smrpr.SuppliedMarketReviewPacketRecord(**values)


def _valid_composition(**overrides: object) -> rpecr.ReviewPacketEvidenceCompositionRecord:
    values = {
        "condition_id": "condition-1",
        "token_id": "token-1",
        "outcome": "Yes",
        "supplied_market_review_packet": _valid_review_packet(),
        "supplied_evidence_packet": _valid_supplied_evidence_packet(),
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


def _valid_supplied_runtime_validation_bundle(
    **overrides: object,
) -> srvb.SuppliedRuntimeValidationBundleRecord:
    values = {
        "condition_id": "condition-1",
        "token_id": "token-1",
        "outcome": "Yes",
        "supplied_market_contract": _valid_contract(),
        "supplied_market_review_packet": _valid_review_packet(),
        "supplied_evidence_packet": _valid_supplied_evidence_packet(),
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


def _valid_bridge_record(
    **overrides: object,
) -> bridge.FixtureOnlySourceProviderValidationBundleBridgeRecord:
    values = {
        "condition_id": "condition-1",
        "token_id": "token-1",
        "outcome": "Yes",
        "fixture_only_source_provider_evidence_bridge": _valid_fixture_evidence_bridge(),
        "supplied_runtime_validation_bundle": _valid_supplied_runtime_validation_bundle(),
        "validation_bundle_bridge_id": "validation-bundle-bridge-1",
        "validation_bundle_bridge_summary": "Fixture-only evidence bridge linked to validation bundle.",
        "fixture_evidence_bridge_summary": "Fixture-only source/provider linked to supplied evidence.",
        "supplied_validation_summary": "Caller supplied validation summary text.",
        "no_lookahead_summary": "Available time is supplied before decision time.",
        "operator_review_summary": "Operator review remains required before any action.",
        "blocked_reason_summary": "No blocker for this valid validation-bundle bridge.",
        "fixture_only_validation_bundle_bridge_status": (
            bridge.FixtureOnlyValidationBundleBridgeStatus.FIXTURE_ONLY_VALIDATION_BUNDLE_BRIDGE_RECORDED
        ),
        "fixture_only_validation_bundle_bridge_posture": (
            bridge.FixtureOnlyValidationBundleBridgePosture.FIXTURE_ONLY_VALIDATION_BUNDLE_BRIDGE_IN_MEMORY_ONLY
        ),
        "validation_bundle_bridge_alignment_status": (
            bridge.ValidationBundleBridgeAlignmentStatus.VALIDATION_BUNDLE_BRIDGE_ALIGNED
        ),
        "no_lookahead_status": bridge.NoLookaheadStatus.NO_LOOKAHEAD_RECORDED,
        "operator_review_status": bridge.OperatorReviewStatus.OPERATOR_REVIEW_REQUIRED,
        "runtime_gate_status": bridge.RuntimeGateStatus.RUNTIME_GATE_READY,
    }
    values.update(overrides)
    return bridge.FixtureOnlySourceProviderValidationBundleBridgeRecord(**values)


def _assert_blocked_with_reason(record, reason: str) -> None:
    result = bridge.validate_fixture_only_source_provider_validation_bundle_bridge_record(record)
    assert result.passed is False
    assert result.severity is bridge.ValidationSeverity.BLOCKED
    assert reason in result.reasons


def test_enums_are_closed_sets() -> None:
    assert bridge.FixtureOnlyValidationBundleBridgeStatus.values() == frozenset(
        {
            "fixture_only_validation_bundle_bridge_recorded",
            "fixture_only_validation_bundle_bridge_missing",
            "fixture_only_validation_bundle_bridge_ambiguous",
            "fixture_only_validation_bundle_bridge_unsupported",
            "fixture_only_validation_bundle_bridge_unknown",
        }
    )
    assert bridge.FixtureOnlyValidationBundleBridgePosture.values() == frozenset(
        {
            "fixture_only_validation_bundle_bridge_in_memory_only",
            "fixture_only_validation_bundle_bridge_missing",
            "fixture_only_validation_bundle_bridge_ambiguous",
            "fixture_only_validation_bundle_bridge_unsupported",
            "fixture_only_validation_bundle_bridge_unknown",
        }
    )
    assert bridge.ValidationBundleBridgeAlignmentStatus.values() == frozenset(
        {
            "validation_bundle_bridge_aligned",
            "validation_bundle_bridge_mismatch",
            "validation_bundle_bridge_missing",
            "validation_bundle_bridge_ambiguous",
            "validation_bundle_bridge_unknown",
        }
    )
    assert bridge.NoLookaheadStatus.values() == frozenset(
        {"no_lookahead_recorded", "no_lookahead_missing", "no_lookahead_ambiguous", "no_lookahead_unknown"}
    )
    assert bridge.OperatorReviewStatus.values() == frozenset(
        {
            "operator_review_required",
            "operator_review_missing",
            "operator_review_ambiguous",
            "operator_review_not_required",
            "operator_review_unknown",
        }
    )
    assert bridge.RuntimeGateStatus.values() == frozenset(
        {"runtime_gate_ready", "runtime_gate_blocked", "runtime_gate_requires_manual_review", "runtime_gate_unknown"}
    )
    assert bridge.ValidationSeverity.values() == frozenset({"passed", "caution", "failed", "blocked"})


def test_dataclass_construction() -> None:
    record = _valid_bridge_record(provenance_notes="caller supplied")
    assert record.condition_id == "condition-1"
    assert isinstance(record.fixture_only_source_provider_evidence_bridge, evidence_bridge.FixtureOnlySourceProviderEvidenceBridgeRecord)
    assert isinstance(record.supplied_runtime_validation_bundle, srvb.SuppliedRuntimeValidationBundleRecord)
    assert record.fixture_only_validation_bundle_bridge_status is bridge.FixtureOnlyValidationBundleBridgeStatus.FIXTURE_ONLY_VALIDATION_BUNDLE_BRIDGE_RECORDED
    assert record.provenance_notes == "caller supplied"


def test_mapping_construction_coerces_string_enums_and_nested_mappings() -> None:
    record = bridge.fixture_only_source_provider_validation_bundle_bridge_record_from_mapping(
        {
            **asdict(_valid_bridge_record()),
            "fixture_only_source_provider_evidence_bridge": asdict(_valid_fixture_evidence_bridge()),
            "supplied_runtime_validation_bundle": asdict(_valid_supplied_runtime_validation_bundle()),
            "fixture_only_validation_bundle_bridge_status": "fixture_only_validation_bundle_bridge_recorded",
            "fixture_only_validation_bundle_bridge_posture": "fixture_only_validation_bundle_bridge_in_memory_only",
            "validation_bundle_bridge_alignment_status": "validation_bundle_bridge_aligned",
            "no_lookahead_status": "no_lookahead_recorded",
            "operator_review_status": "operator_review_required",
            "runtime_gate_status": "runtime_gate_ready",
        }
    )
    assert isinstance(record.fixture_only_source_provider_evidence_bridge, evidence_bridge.FixtureOnlySourceProviderEvidenceBridgeRecord)
    assert isinstance(record.supplied_runtime_validation_bundle, srvb.SuppliedRuntimeValidationBundleRecord)
    assert record.runtime_gate_status is bridge.RuntimeGateStatus.RUNTIME_GATE_READY


def test_valid_record_passes() -> None:
    result = bridge.validate_fixture_only_source_provider_validation_bundle_bridge_record(_valid_bridge_record())
    assert result.passed is True
    assert result.severity is bridge.ValidationSeverity.PASSED
    assert result.reasons == ()


@pytest.mark.parametrize(
    "field_name",
    [
        "condition_id",
        "token_id",
        "outcome",
        "validation_bundle_bridge_id",
        "validation_bundle_bridge_summary",
        "fixture_evidence_bridge_summary",
        "supplied_validation_summary",
        "no_lookahead_summary",
        "operator_review_summary",
    ],
)
def test_blank_required_text_fields_fail_closed(field_name: str) -> None:
    _assert_blocked_with_reason(_valid_bridge_record(**{field_name: " "}), f"{field_name} is missing")


def test_blank_blocked_reason_summary_is_allowed_when_otherwise_valid() -> None:
    result = bridge.validate_fixture_only_source_provider_validation_bundle_bridge_record(
        _valid_bridge_record(blocked_reason_summary="")
    )
    assert result.passed is True


def test_blank_blocked_reason_summary_fails_when_another_validation_failure_exists() -> None:
    _assert_blocked_with_reason(
        _valid_bridge_record(condition_id="", blocked_reason_summary=""),
        "blocked_reason_summary is missing",
    )


def test_invalid_nested_fixture_only_source_provider_evidence_bridge_fails_closed() -> None:
    nested = _valid_fixture_evidence_bridge(evidence_bridge_id="")
    _assert_blocked_with_reason(
        _valid_bridge_record(fixture_only_source_provider_evidence_bridge=nested),
        "fixture-only source provider evidence bridge is invalid",
    )


def test_invalid_nested_supplied_runtime_validation_bundle_fails_closed() -> None:
    nested = _valid_supplied_runtime_validation_bundle(validation_bundle_id="")
    _assert_blocked_with_reason(
        _valid_bridge_record(supplied_runtime_validation_bundle=nested),
        "supplied runtime validation bundle is invalid",
    )


@pytest.mark.parametrize(
    ("field_name", "reason"),
    [
        ("condition_id", "condition_id does not match fixture-only evidence bridge"),
        ("token_id", "token_id does not match fixture-only evidence bridge"),
        ("outcome", "outcome does not match fixture-only evidence bridge"),
    ],
)
def test_top_level_route_mismatch_with_fixture_bridge_fails_closed(field_name: str, reason: str) -> None:
    _assert_blocked_with_reason(_valid_bridge_record(**{field_name: "different"}), reason)


@pytest.mark.parametrize(
    ("field_name", "reason"),
    [
        ("condition_id", "condition_id does not match supplied runtime validation bundle"),
        ("token_id", "token_id does not match supplied runtime validation bundle"),
        ("outcome", "outcome does not match supplied runtime validation bundle"),
    ],
)
def test_top_level_route_mismatch_with_supplied_bundle_fails_closed(field_name: str, reason: str) -> None:
    _assert_blocked_with_reason(_valid_bridge_record(**{field_name: "different"}), reason)


def test_nested_fixture_bridge_and_supplied_bundle_route_mismatch_fails_closed() -> None:
    nested = _valid_supplied_runtime_validation_bundle(condition_id="condition-2")
    _assert_blocked_with_reason(
        _valid_bridge_record(supplied_runtime_validation_bundle=nested),
        "nested fixture-only evidence bridge and supplied runtime validation bundle routes do not match",
    )


def test_nested_supplied_market_contract_mismatch_fails_closed() -> None:
    fixture_record = _valid_fixture_only_source_provider(supplied_market_contract=_valid_contract(token_id="token-2"))
    nested = _valid_fixture_evidence_bridge(fixture_only_source_provider=fixture_record)
    _assert_blocked_with_reason(
        _valid_bridge_record(fixture_only_source_provider_evidence_bridge=nested),
        "nested supplied market contracts do not match",
    )


def test_nested_supplied_evidence_packet_mismatch_fails_closed() -> None:
    nested = _valid_fixture_evidence_bridge(supplied_evidence_packet=_valid_supplied_evidence_packet(token_id="token-2"))
    _assert_blocked_with_reason(
        _valid_bridge_record(fixture_only_source_provider_evidence_bridge=nested),
        "nested supplied evidence packets do not match",
    )


def test_fixture_evidence_bridge_summary_mismatch_fails_closed() -> None:
    _assert_blocked_with_reason(
        _valid_bridge_record(fixture_evidence_bridge_summary="different"),
        "fixture evidence bridge summary does not match fixture-only evidence bridge",
    )


def test_supplied_validation_summary_mismatch_fails_closed() -> None:
    _assert_blocked_with_reason(
        _valid_bridge_record(supplied_validation_summary="different"),
        "supplied validation summary does not match supplied runtime validation bundle",
    )


def test_no_lookahead_summary_mismatch_fails_closed() -> None:
    _assert_blocked_with_reason(
        _valid_bridge_record(no_lookahead_summary="different"),
        "no-lookahead summary does not match fixture-only evidence bridge",
    )


@pytest.mark.parametrize(
    "status",
    [s for s in bridge.FixtureOnlyValidationBundleBridgeStatus if s is not bridge.FixtureOnlyValidationBundleBridgeStatus.FIXTURE_ONLY_VALIDATION_BUNDLE_BRIDGE_RECORDED],
)
def test_non_recorded_bridge_statuses_fail_closed(status) -> None:
    _assert_blocked_with_reason(_valid_bridge_record(fixture_only_validation_bundle_bridge_status=status), f"fixture-only validation bundle bridge status is {status.value}")


@pytest.mark.parametrize(
    "posture",
    [p for p in bridge.FixtureOnlyValidationBundleBridgePosture if p is not bridge.FixtureOnlyValidationBundleBridgePosture.FIXTURE_ONLY_VALIDATION_BUNDLE_BRIDGE_IN_MEMORY_ONLY],
)
def test_non_in_memory_bridge_postures_fail_closed(posture) -> None:
    _assert_blocked_with_reason(_valid_bridge_record(fixture_only_validation_bundle_bridge_posture=posture), f"fixture-only validation bundle bridge posture is {posture.value}")


@pytest.mark.parametrize(
    "alignment",
    [a for a in bridge.ValidationBundleBridgeAlignmentStatus if a is not bridge.ValidationBundleBridgeAlignmentStatus.VALIDATION_BUNDLE_BRIDGE_ALIGNED],
)
def test_non_aligned_bridge_alignment_statuses_fail_closed(alignment) -> None:
    _assert_blocked_with_reason(_valid_bridge_record(validation_bundle_bridge_alignment_status=alignment), f"validation bundle bridge alignment status is {alignment.value}")


@pytest.mark.parametrize("status", [s for s in bridge.NoLookaheadStatus if s is not bridge.NoLookaheadStatus.NO_LOOKAHEAD_RECORDED])
def test_non_recorded_no_lookahead_statuses_fail_closed(status) -> None:
    _assert_blocked_with_reason(_valid_bridge_record(no_lookahead_status=status), f"no-lookahead status is {status.value}")


@pytest.mark.parametrize("status", [s for s in bridge.OperatorReviewStatus if s is not bridge.OperatorReviewStatus.OPERATOR_REVIEW_REQUIRED])
def test_non_required_operator_review_statuses_fail_closed(status) -> None:
    _assert_blocked_with_reason(_valid_bridge_record(operator_review_status=status), f"operator review status is {status.value}")


@pytest.mark.parametrize("status", [s for s in bridge.RuntimeGateStatus if s is not bridge.RuntimeGateStatus.RUNTIME_GATE_READY])
def test_non_ready_runtime_gates_fail_closed(status) -> None:
    _assert_blocked_with_reason(_valid_bridge_record(runtime_gate_status=status), f"runtime gate status is {status.value}")


def _source_without_docstrings(path: Path) -> str:
    tree = ast.parse(path.read_text())
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            if (
                node.body
                and isinstance(node.body[0], ast.Expr)
                and isinstance(node.body[0].value, ast.Constant)
                and isinstance(node.body[0].value.value, str)
            ):
                node.body[0] = ast.Pass()
    return ast.unparse(tree)


def test_no_disallowed_market_route_dataclass_or_input_field() -> None:
    for path in (MODULE_PATH, TEST_PATH):
        source = _source_without_docstrings(path)
        for forbidden in ("market" + "_id", "market" + "_id:"):
            assert forbidden not in source


def test_source_module_has_no_live_io_or_runtime_behavior_terms() -> None:
    source = _source_without_docstrings(MODULE_PATH).lower()
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
    assert [term for term in forbidden_terms if term in source] == []
