import ast
from pathlib import Path

import pytest

from meg.weather.stage2 import fixture_only_source_provider_evidence_bridge_runtime as bridge
from meg.weather.stage2 import fixture_only_source_provider_runtime as fspr
from meg.weather.stage2 import supplied_evidence_packet_runtime as sepr
from meg.weather.stage2 import supplied_market_contract_runtime as smcr


MODULE_PATH = Path("meg/weather/stage2/fixture_only_source_provider_evidence_bridge_runtime.py")
TEST_PATH = Path("tests/core/test_weather_stage2_fixture_only_source_provider_evidence_bridge_runtime.py")


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


def _valid_fixture_only_source_provider(
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


def _valid_supplied_evidence_packet(
    **overrides: object,
) -> sepr.SuppliedEvidencePacketRecord:
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


def _valid_bridge_record(
    **overrides: object,
) -> bridge.FixtureOnlySourceProviderEvidenceBridgeRecord:
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
            bridge.FixtureOnlyEvidenceBridgeStatus.FIXTURE_ONLY_EVIDENCE_BRIDGE_RECORDED
        ),
        "fixture_only_evidence_bridge_posture": (
            bridge.FixtureOnlyEvidenceBridgePosture.FIXTURE_ONLY_EVIDENCE_BRIDGE_IN_MEMORY_ONLY
        ),
        "evidence_bridge_alignment_status": (
            bridge.EvidenceBridgeAlignmentStatus.EVIDENCE_BRIDGE_ALIGNED
        ),
        "no_lookahead_status": bridge.NoLookaheadStatus.NO_LOOKAHEAD_RECORDED,
        "operator_review_status": bridge.OperatorReviewStatus.OPERATOR_REVIEW_REQUIRED,
        "runtime_gate_status": bridge.RuntimeGateStatus.RUNTIME_GATE_READY,
    }
    values.update(overrides)
    return bridge.FixtureOnlySourceProviderEvidenceBridgeRecord(**values)


def _assert_blocked_with_reason(
    record: bridge.FixtureOnlySourceProviderEvidenceBridgeRecord,
    reason: str,
) -> None:
    result = bridge.validate_fixture_only_source_provider_evidence_bridge_record(record)
    assert result.passed is False
    assert result.severity is bridge.ValidationSeverity.BLOCKED
    assert reason in result.reasons


def test_enums_are_closed_sets() -> None:
    assert bridge.FixtureOnlyEvidenceBridgeStatus.values() == frozenset({
        "fixture_only_evidence_bridge_recorded", "fixture_only_evidence_bridge_missing",
        "fixture_only_evidence_bridge_ambiguous", "fixture_only_evidence_bridge_unsupported",
        "fixture_only_evidence_bridge_unknown"})
    assert bridge.FixtureOnlyEvidenceBridgePosture.values() == frozenset({
        "fixture_only_evidence_bridge_in_memory_only", "fixture_only_evidence_bridge_missing",
        "fixture_only_evidence_bridge_ambiguous", "fixture_only_evidence_bridge_unsupported",
        "fixture_only_evidence_bridge_unknown"})
    assert bridge.EvidenceBridgeAlignmentStatus.values() == frozenset({
        "evidence_bridge_aligned", "evidence_bridge_mismatch", "evidence_bridge_missing",
        "evidence_bridge_ambiguous", "evidence_bridge_unknown"})
    assert bridge.NoLookaheadStatus.values() == frozenset({
        "no_lookahead_recorded", "no_lookahead_missing", "no_lookahead_ambiguous",
        "no_lookahead_unknown"})
    assert bridge.OperatorReviewStatus.values() == frozenset({
        "operator_review_required", "operator_review_missing", "operator_review_ambiguous",
        "operator_review_not_required", "operator_review_unknown"})
    assert bridge.RuntimeGateStatus.values() == frozenset({
        "runtime_gate_ready", "runtime_gate_blocked", "runtime_gate_requires_manual_review",
        "runtime_gate_unknown"})
    assert bridge.ValidationSeverity.values() == frozenset({"passed", "caution", "failed", "blocked"})


def test_dataclass_construction() -> None:
    record = _valid_bridge_record(provenance_notes="review note")
    assert record.condition_id == "condition-1"
    assert record.fixture_only_source_provider.fixture_source_name == record.fixture_source_descriptor_summary
    assert record.supplied_evidence_packet.evidence_source_descriptor == record.evidence_source_descriptor_summary
    assert record.provenance_notes == "review note"


def test_mapping_construction_coerces_string_enums_and_nested_mappings() -> None:
    contract = _valid_contract().__dict__ | {
        "settlement_rule_status": "settlement_rule_recorded",
        "market_contract_status": "market_contract_recorded",
        "event_timing_status": "event_timing_recorded",
        "runtime_gate_status": "runtime_gate_ready",
    }
    fixture = _valid_fixture_only_source_provider().__dict__ | {
        "supplied_market_contract": contract,
        "fixture_only_source_provider_status": "fixture_only_source_provider_recorded",
        "fixture_only_source_provider_posture": "fixture_only_local_static_caller_supplied",
        "fixture_only_source_provider_freshness_status": "fixture_only_freshness_recorded",
        "no_lookahead_status": "no_lookahead_recorded",
        "operator_review_status": "operator_review_required",
        "runtime_gate_status": "runtime_gate_ready",
    }
    evidence = _valid_supplied_evidence_packet().__dict__ | {
        "supplied_market_contract": contract,
        "evidence_packet_status": "evidence_packet_recorded",
        "evidence_freshness_status": "evidence_freshness_recorded",
        "evidence_availability_status": "evidence_available_before_decision",
        "evidence_source_posture": "caller_supplied_static_evidence",
        "runtime_gate_status": "runtime_gate_ready",
    }
    record = bridge.fixture_only_source_provider_evidence_bridge_record_from_mapping({
        **_valid_bridge_record().__dict__,
        "fixture_only_source_provider": fixture,
        "supplied_evidence_packet": evidence,
        "fixture_only_evidence_bridge_status": "fixture_only_evidence_bridge_recorded",
        "fixture_only_evidence_bridge_posture": "fixture_only_evidence_bridge_in_memory_only",
        "evidence_bridge_alignment_status": "evidence_bridge_aligned",
        "no_lookahead_status": "no_lookahead_recorded",
        "operator_review_status": "operator_review_required",
        "runtime_gate_status": "runtime_gate_ready",
    })
    assert isinstance(record.fixture_only_source_provider, fspr.FixtureOnlySourceProviderRecord)
    assert isinstance(record.supplied_evidence_packet, sepr.SuppliedEvidencePacketRecord)
    assert record.fixture_only_evidence_bridge_status is bridge.FixtureOnlyEvidenceBridgeStatus.FIXTURE_ONLY_EVIDENCE_BRIDGE_RECORDED
    assert record.provenance_notes == ""


def test_valid_record_passes() -> None:
    result = bridge.validate_fixture_only_source_provider_evidence_bridge_record(_valid_bridge_record())
    assert result.passed is True
    assert result.severity is bridge.ValidationSeverity.PASSED
    assert result.reasons == ()


@pytest.mark.parametrize("field_name", [
    "condition_id", "token_id", "outcome", "evidence_bridge_id", "evidence_bridge_summary",
    "fixture_source_descriptor_summary", "evidence_source_descriptor_summary",
    "no_lookahead_summary", "operator_review_summary",
])
def test_blank_required_text_fields_fail_closed(field_name: str) -> None:
    _assert_blocked_with_reason(_valid_bridge_record(**{field_name: "  "}), f"{field_name} is missing")


def test_blank_blocked_reason_summary_is_allowed_when_otherwise_valid() -> None:
    result = bridge.validate_fixture_only_source_provider_evidence_bridge_record(
        _valid_bridge_record(blocked_reason_summary="  ")
    )
    assert result.passed is True
    assert result.reasons == ()


def test_blank_blocked_reason_summary_fails_when_another_validation_failure_exists() -> None:
    result = bridge.validate_fixture_only_source_provider_evidence_bridge_record(
        _valid_bridge_record(evidence_bridge_id="  ", blocked_reason_summary="  ")
    )
    assert result.reasons == ("evidence_bridge_id is missing", "blocked_reason_summary is missing")


def test_invalid_nested_fixture_only_source_provider_fails_closed() -> None:
    _assert_blocked_with_reason(
        _valid_bridge_record(fixture_only_source_provider=_valid_fixture_only_source_provider(fixture_provider_name="  ")),
        "fixture-only source provider is invalid",
    )


def test_invalid_nested_supplied_evidence_packet_fails_closed() -> None:
    _assert_blocked_with_reason(
        _valid_bridge_record(supplied_evidence_packet=_valid_supplied_evidence_packet(evidence_summary="  ")),
        "supplied evidence packet is invalid",
    )


@pytest.mark.parametrize(("field_name", "reason"), [
    ("condition_id", "condition_id does not match fixture-only source provider"),
    ("token_id", "token_id does not match fixture-only source provider"),
    ("outcome", "outcome does not match fixture-only source provider"),
])
def test_top_level_route_mismatch_with_fixture_only_source_provider_fails_closed(field_name: str, reason: str) -> None:
    _assert_blocked_with_reason(_valid_bridge_record(**{field_name: "different"}), reason)


@pytest.mark.parametrize(("field_name", "reason"), [
    ("condition_id", "condition_id does not match supplied evidence packet"),
    ("token_id", "token_id does not match supplied evidence packet"),
    ("outcome", "outcome does not match supplied evidence packet"),
])
def test_top_level_route_mismatch_with_supplied_evidence_packet_fails_closed(field_name: str, reason: str) -> None:
    fixture = _valid_fixture_only_source_provider(**{field_name: "different"})
    _assert_blocked_with_reason(
        _valid_bridge_record(**{field_name: "different", "fixture_only_source_provider": fixture}),
        reason,
    )


def test_nested_fixture_only_source_provider_and_supplied_evidence_packet_route_mismatch_fails_closed() -> None:
    _assert_blocked_with_reason(
        _valid_bridge_record(supplied_evidence_packet=_valid_supplied_evidence_packet(token_id="token-2")),
        "nested fixture-only source provider and supplied evidence packet routes do not match",
    )


def test_nested_supplied_market_contract_mismatch_fails_closed() -> None:
    _assert_blocked_with_reason(
        _valid_bridge_record(supplied_evidence_packet=_valid_supplied_evidence_packet(supplied_market_contract=_valid_contract(outcome="No"))),
        "nested supplied market contracts do not match",
    )


def test_fixture_source_descriptor_summary_mismatch_fails_closed() -> None:
    _assert_blocked_with_reason(
        _valid_bridge_record(fixture_source_descriptor_summary="Different source"),
        "fixture source descriptor summary does not match fixture-only source provider",
    )


def test_evidence_source_descriptor_summary_mismatch_fails_closed() -> None:
    _assert_blocked_with_reason(
        _valid_bridge_record(evidence_source_descriptor_summary="Different evidence source"),
        "evidence source descriptor summary does not match supplied evidence packet",
    )


def test_no_lookahead_summary_mismatch_fails_closed() -> None:
    _assert_blocked_with_reason(
        _valid_bridge_record(no_lookahead_summary="Different no-lookahead summary"),
        "no-lookahead summary does not match fixture-only source provider",
    )


@pytest.mark.parametrize("status", [s for s in bridge.FixtureOnlyEvidenceBridgeStatus if s is not bridge.FixtureOnlyEvidenceBridgeStatus.FIXTURE_ONLY_EVIDENCE_BRIDGE_RECORDED])
def test_non_recorded_fixture_only_evidence_bridge_statuses_fail_closed(status: bridge.FixtureOnlyEvidenceBridgeStatus) -> None:
    _assert_blocked_with_reason(_valid_bridge_record(fixture_only_evidence_bridge_status=status), f"fixture-only evidence bridge status is {status.value}")


@pytest.mark.parametrize("posture", [p for p in bridge.FixtureOnlyEvidenceBridgePosture if p is not bridge.FixtureOnlyEvidenceBridgePosture.FIXTURE_ONLY_EVIDENCE_BRIDGE_IN_MEMORY_ONLY])
def test_non_in_memory_bridge_postures_fail_closed(posture: bridge.FixtureOnlyEvidenceBridgePosture) -> None:
    _assert_blocked_with_reason(_valid_bridge_record(fixture_only_evidence_bridge_posture=posture), f"fixture-only evidence bridge posture is {posture.value}")


@pytest.mark.parametrize("status", [s for s in bridge.EvidenceBridgeAlignmentStatus if s is not bridge.EvidenceBridgeAlignmentStatus.EVIDENCE_BRIDGE_ALIGNED])
def test_non_aligned_bridge_alignment_statuses_fail_closed(status: bridge.EvidenceBridgeAlignmentStatus) -> None:
    _assert_blocked_with_reason(_valid_bridge_record(evidence_bridge_alignment_status=status), f"evidence bridge alignment status is {status.value}")


@pytest.mark.parametrize("status", [s for s in bridge.NoLookaheadStatus if s is not bridge.NoLookaheadStatus.NO_LOOKAHEAD_RECORDED])
def test_non_recorded_no_lookahead_statuses_fail_closed(status: bridge.NoLookaheadStatus) -> None:
    _assert_blocked_with_reason(_valid_bridge_record(no_lookahead_status=status), f"no-lookahead status is {status.value}")


@pytest.mark.parametrize("status", [s for s in bridge.OperatorReviewStatus if s is not bridge.OperatorReviewStatus.OPERATOR_REVIEW_REQUIRED])
def test_non_required_operator_review_statuses_fail_closed(status: bridge.OperatorReviewStatus) -> None:
    _assert_blocked_with_reason(_valid_bridge_record(operator_review_status=status), f"operator review status is {status.value}")


@pytest.mark.parametrize("status", [s for s in bridge.RuntimeGateStatus if s is not bridge.RuntimeGateStatus.RUNTIME_GATE_READY])
def test_non_ready_runtime_gates_fail_closed(status: bridge.RuntimeGateStatus) -> None:
    _assert_blocked_with_reason(_valid_bridge_record(runtime_gate_status=status), f"runtime gate status is {status.value}")


def _without_docstrings(path: Path) -> str:
    tree = ast.parse(path.read_text())
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.body and isinstance(node.body[0], ast.Expr) and isinstance(node.body[0].value, ast.Constant) and isinstance(node.body[0].value.value, str):
                node.body[0] = ast.Pass()
    return ast.unparse(tree)


def test_static_no_noncanonical_identifier_dataclass_or_input_field() -> None:
    forbidden = "market" + "_id"
    assert forbidden not in _without_docstrings(MODULE_PATH)
    assert forbidden not in _without_docstrings(TEST_PATH)


def test_static_source_module_has_no_forbidden_runtime_terms() -> None:
    source = _without_docstrings(MODULE_PATH)
    forbidden_terms = (
        "requests", "httpx", "urllib", "aiohttp", "boto3", "polymarket", "kalshi",
        "duckdb", "pandas", "subprocess", "open(", ".read_text(", ".write_text(",
        "socket", "os.environ", "dotenv", "place_order", "paper_trade", "trade",
        "backtest", "score", "execute_order", "submit_order", "persist", "database",
        "postgres", "redis", "export", "write", "save", "owner_decision",
        "capture_decision", "celery", "rabbitmq", "sqs", "enqueue(", "dequeue(",
        "publish(", "subscribe(", "scheduler", "provider_client", "api_call", "scrape",
        "download", "credentials", "production",
    )
    for term in forbidden_terms:
        assert term not in source
