import ast
from dataclasses import asdict
from pathlib import Path

import pytest

from meg.weather.stage2 import fixture_only_source_provider_operator_review_ack_bridge_runtime as bridge
from meg.weather.stage2 import fixture_only_source_provider_operator_review_handoff_bridge_runtime as handoff_bridge
from meg.weather.stage2 import fixture_only_source_provider_trace_bridge_runtime as trace_bridge
from meg.weather.stage2 import fixture_only_source_provider_end_to_end_smoke_bridge_runtime as smoke_bridge
from meg.weather.stage2 import fixture_only_source_provider_dry_run_report_bridge_runtime as dry_run_report_bridge
from meg.weather.stage2 import fixture_only_source_provider_dry_run_bridge_runtime as dry_run_bridge
from meg.weather.stage2 import fixture_only_source_provider_validation_bundle_bridge_runtime as validation_bridge
from meg.weather.stage2 import fixture_only_source_provider_evidence_bridge_runtime as evidence_bridge
from meg.weather.stage2 import fixture_only_source_provider_runtime as fspr
from meg.weather.stage2 import supplied_runtime_operator_review_ack_packet as soack
from meg.weather.stage2 import supplied_runtime_operator_review_handoff as sorh
from meg.weather.stage2 import supplied_runtime_trace_packet as srtp
from meg.weather.stage2 import supplied_runtime_end_to_end_smoke as sees
from meg.weather.stage2 import supplied_runtime_dry_run_report as srdr
from meg.weather.stage2 import supplied_runtime_dry_run_packet as srdp
from meg.weather.stage2 import supplied_runtime_validation_bundle as srvb
from meg.weather.stage2 import supplied_evidence_packet_runtime as sepr
from meg.weather.stage2 import supplied_market_contract_runtime as smcr
from tests.core import test_weather_stage2_fixture_only_source_provider_operator_review_handoff_bridge_runtime as base

MODULE_PATH = Path("meg/weather/stage2/fixture_only_source_provider_operator_review_ack_bridge_runtime.py")
TEST_PATH = Path("tests/core/test_weather_stage2_fixture_only_source_provider_operator_review_ack_bridge_runtime.py")


def _valid_contract(**overrides: object) -> smcr.SuppliedMarketContractRecord:
    return base._valid_contract(**overrides)


def _valid_fixture_only_source_provider(**overrides: object) -> fspr.FixtureOnlySourceProviderRecord:
    return base._valid_fixture_only_source_provider(**overrides)


def _valid_supplied_evidence_packet(**overrides: object) -> sepr.SuppliedEvidencePacketRecord:
    return base._valid_supplied_evidence_packet(**overrides)


def _valid_fixture_evidence_bridge(**overrides: object) -> evidence_bridge.FixtureOnlySourceProviderEvidenceBridgeRecord:
    return base._valid_fixture_evidence_bridge(**overrides)


def _valid_supplied_runtime_validation_bundle(**overrides: object) -> srvb.SuppliedRuntimeValidationBundleRecord:
    return base._valid_supplied_runtime_validation_bundle(**overrides)


def _valid_validation_bundle_bridge(**overrides: object) -> validation_bridge.FixtureOnlySourceProviderValidationBundleBridgeRecord:
    return base._valid_validation_bundle_bridge(**overrides)


def _valid_supplied_runtime_dry_run_packet(**overrides: object) -> srdp.SuppliedRuntimeDryRunPacketRecord:
    return base._valid_supplied_runtime_dry_run_packet(**overrides)


def _valid_dry_run_bridge(**overrides: object) -> dry_run_bridge.FixtureOnlySourceProviderDryRunBridgeRecord:
    return base._valid_dry_run_bridge(**overrides)


def _valid_supplied_runtime_dry_run_report(**overrides: object) -> srdr.SuppliedRuntimeDryRunReportRecord:
    return base._valid_supplied_runtime_dry_run_report(**overrides)


def _valid_dry_run_report_bridge(**overrides: object) -> dry_run_report_bridge.FixtureOnlySourceProviderDryRunReportBridgeRecord:
    return base._valid_dry_run_report_bridge(**overrides)


def _valid_supplied_runtime_end_to_end_smoke(**overrides: object) -> sees.SuppliedRuntimeEndToEndSmokeRecord:
    return base._valid_supplied_runtime_end_to_end_smoke(**overrides)


def _valid_end_to_end_smoke_bridge(**overrides: object) -> smoke_bridge.FixtureOnlySourceProviderEndToEndSmokeBridgeRecord:
    return base._valid_end_to_end_smoke_bridge(**overrides)


def _valid_supplied_runtime_trace_packet(**overrides: object) -> srtp.SuppliedRuntimeTracePacketRecord:
    return base._valid_supplied_runtime_trace_packet(**overrides)


def _valid_trace_bridge(**overrides: object) -> trace_bridge.FixtureOnlySourceProviderTraceBridgeRecord:
    return base._valid_trace_bridge(**overrides)


def _valid_supplied_runtime_operator_review_handoff(**overrides: object) -> sorh.SuppliedRuntimeOperatorReviewHandoffRecord:
    return base._valid_supplied_runtime_operator_review_handoff(**overrides)


def _valid_operator_review_handoff_bridge(**overrides: object) -> handoff_bridge.FixtureOnlySourceProviderOperatorReviewHandoffBridgeRecord:
    return base._valid_bridge_record(**overrides)


def _valid_supplied_runtime_operator_review_ack_packet(**overrides: object) -> soack.SuppliedRuntimeOperatorReviewAckPacketRecord:
    values = {
        "condition_id": "condition-1",
        "token_id": "token-1",
        "outcome": "Yes",
        "supplied_runtime_operator_review_handoff": _valid_supplied_runtime_operator_review_handoff(),
        "ack_packet_id": "ack-packet-1",
        "ack_summary": "Caller supplied acknowledgement packet summary text.",
        "operator_review_summary": "Operator review remains required before any action.",
        "blocked_reason_summary": "No blocker for this valid acknowledgement packet.",
        "operator_review_ack_packet_status": soack.OperatorReviewAckPacketStatus.OPERATOR_REVIEW_ACK_PACKET_RECORDED,
        "operator_review_ack_completeness_status": soack.OperatorReviewAckCompletenessStatus.OPERATOR_REVIEW_ACK_COMPLETE,
        "operator_review_status": soack.OperatorReviewStatus.OPERATOR_REVIEW_REQUIRED,
        "runtime_gate_status": soack.RuntimeGateStatus.RUNTIME_GATE_READY,
    }
    values.update(overrides)
    return soack.SuppliedRuntimeOperatorReviewAckPacketRecord(**values)


def _valid_bridge_record(**overrides: object) -> bridge.FixtureOnlySourceProviderOperatorReviewAckBridgeRecord:
    values = {
        "condition_id": "condition-1",
        "token_id": "token-1",
        "outcome": "Yes",
        "fixture_only_source_provider_operator_review_handoff_bridge": _valid_operator_review_handoff_bridge(),
        "supplied_runtime_operator_review_ack_packet": _valid_supplied_runtime_operator_review_ack_packet(),
        "operator_review_ack_bridge_id": "operator-review-ack-bridge-1",
        "operator_review_ack_bridge_summary": "Fixture-only handoff bridge linked to supplied acknowledgement packet.",
        "fixture_handoff_bridge_summary": "Fixture-only trace bridge linked to supplied operator-review handoff.",
        "supplied_ack_summary": "Caller supplied acknowledgement packet summary text.",
        "operator_review_summary": "Operator review remains required before any action.",
        "blocked_reason_summary": "No blocker for this valid operator-review acknowledgement bridge.",
        "fixture_only_operator_review_ack_bridge_status": bridge.FixtureOnlyOperatorReviewAckBridgeStatus.FIXTURE_ONLY_OPERATOR_REVIEW_ACK_BRIDGE_RECORDED,
        "fixture_only_operator_review_ack_bridge_posture": bridge.FixtureOnlyOperatorReviewAckBridgePosture.FIXTURE_ONLY_OPERATOR_REVIEW_ACK_BRIDGE_IN_MEMORY_ONLY,
        "operator_review_ack_bridge_alignment_status": bridge.OperatorReviewAckBridgeAlignmentStatus.OPERATOR_REVIEW_ACK_BRIDGE_ALIGNED,
        "no_lookahead_status": bridge.NoLookaheadStatus.NO_LOOKAHEAD_RECORDED,
        "operator_review_status": bridge.OperatorReviewStatus.OPERATOR_REVIEW_REQUIRED,
        "runtime_gate_status": bridge.RuntimeGateStatus.RUNTIME_GATE_READY,
    }
    values.update(overrides)
    return bridge.FixtureOnlySourceProviderOperatorReviewAckBridgeRecord(**values)


def _assert_blocked_with_reason(record, reason: str) -> None:
    result = bridge.validate_fixture_only_source_provider_operator_review_ack_bridge_record(record)
    assert result.passed is False
    assert result.severity is bridge.ValidationSeverity.BLOCKED
    assert reason in result.reasons


def test_enums_are_closed_sets() -> None:
    assert bridge.FixtureOnlyOperatorReviewAckBridgeStatus.values() == frozenset({"fixture_only_operator_review_ack_bridge_recorded", "fixture_only_operator_review_ack_bridge_missing", "fixture_only_operator_review_ack_bridge_ambiguous", "fixture_only_operator_review_ack_bridge_unsupported", "fixture_only_operator_review_ack_bridge_unknown"})
    assert bridge.FixtureOnlyOperatorReviewAckBridgePosture.values() == frozenset({"fixture_only_operator_review_ack_bridge_in_memory_only", "fixture_only_operator_review_ack_bridge_missing", "fixture_only_operator_review_ack_bridge_ambiguous", "fixture_only_operator_review_ack_bridge_unsupported", "fixture_only_operator_review_ack_bridge_unknown"})
    assert bridge.OperatorReviewAckBridgeAlignmentStatus.values() == frozenset({"operator_review_ack_bridge_aligned", "operator_review_ack_bridge_mismatch", "operator_review_ack_bridge_missing", "operator_review_ack_bridge_ambiguous", "operator_review_ack_bridge_unknown"})
    assert bridge.NoLookaheadStatus.values() == frozenset({"no_lookahead_recorded", "no_lookahead_missing", "no_lookahead_ambiguous", "no_lookahead_unknown"})
    assert bridge.OperatorReviewStatus.values() == frozenset({"operator_review_required", "operator_review_missing", "operator_review_ambiguous", "operator_review_not_required", "operator_review_unknown"})
    assert bridge.RuntimeGateStatus.values() == frozenset({"runtime_gate_ready", "runtime_gate_blocked", "runtime_gate_requires_manual_review", "runtime_gate_unknown"})
    assert bridge.ValidationSeverity.values() == frozenset({"passed", "caution", "failed", "blocked"})


def test_dataclass_construction() -> None:
    record = _valid_bridge_record(provenance_notes="caller supplied")
    assert record.condition_id == "condition-1"
    assert isinstance(record.fixture_only_source_provider_operator_review_handoff_bridge, handoff_bridge.FixtureOnlySourceProviderOperatorReviewHandoffBridgeRecord)
    assert isinstance(record.supplied_runtime_operator_review_ack_packet, soack.SuppliedRuntimeOperatorReviewAckPacketRecord)
    assert record.provenance_notes == "caller supplied"


def test_mapping_construction_coerces_string_enums_and_nested_mappings() -> None:
    record = bridge.fixture_only_source_provider_operator_review_ack_bridge_record_from_mapping(asdict(_valid_bridge_record()))
    assert isinstance(record.fixture_only_source_provider_operator_review_handoff_bridge, handoff_bridge.FixtureOnlySourceProviderOperatorReviewHandoffBridgeRecord)
    assert isinstance(record.supplied_runtime_operator_review_ack_packet, soack.SuppliedRuntimeOperatorReviewAckPacketRecord)
    assert record.fixture_only_operator_review_ack_bridge_status is bridge.FixtureOnlyOperatorReviewAckBridgeStatus.FIXTURE_ONLY_OPERATOR_REVIEW_ACK_BRIDGE_RECORDED
    assert record.provenance_notes == ""


def test_valid_record_passes() -> None:
    result = bridge.validate_fixture_only_source_provider_operator_review_ack_bridge_record(_valid_bridge_record())
    assert result.passed is True
    assert result.severity is bridge.ValidationSeverity.PASSED
    assert result.reasons == ()


@pytest.mark.parametrize("field_name", ["condition_id", "token_id", "outcome", "operator_review_ack_bridge_id", "operator_review_ack_bridge_summary", "fixture_handoff_bridge_summary", "supplied_ack_summary", "operator_review_summary"])
def test_blank_required_text_fields_fail_closed(field_name: str) -> None:
    _assert_blocked_with_reason(_valid_bridge_record(**{field_name: "  "}), f"{field_name} is missing")


def test_blank_blocked_reason_summary_is_allowed_when_otherwise_valid() -> None:
    assert bridge.validate_fixture_only_source_provider_operator_review_ack_bridge_record(_valid_bridge_record(blocked_reason_summary="")).passed is True


def test_blank_blocked_reason_summary_fails_when_another_validation_failure_exists() -> None:
    _assert_blocked_with_reason(_valid_bridge_record(condition_id="wrong", blocked_reason_summary=""), "blocked_reason_summary is missing")


def test_invalid_nested_fixture_only_operator_review_handoff_bridge_fails_closed() -> None:
    nested = _valid_operator_review_handoff_bridge(operator_review_handoff_bridge_summary="")
    _assert_blocked_with_reason(_valid_bridge_record(fixture_only_source_provider_operator_review_handoff_bridge=nested), "fixture-only source provider operator-review handoff bridge is invalid")


def test_invalid_nested_supplied_runtime_operator_review_ack_packet_fails_closed() -> None:
    nested = _valid_supplied_runtime_operator_review_ack_packet(ack_summary="")
    _assert_blocked_with_reason(_valid_bridge_record(supplied_runtime_operator_review_ack_packet=nested), "supplied runtime operator-review ack packet is invalid")


@pytest.mark.parametrize(("field_name", "reason"), [("condition_id", "condition_id does not match fixture-only operator-review handoff bridge"), ("token_id", "token_id does not match fixture-only operator-review handoff bridge"), ("outcome", "outcome does not match fixture-only operator-review handoff bridge")])
def test_top_level_route_mismatch_with_fixture_handoff_bridge_fails_closed(field_name: str, reason: str) -> None:
    _assert_blocked_with_reason(_valid_bridge_record(**{field_name: "different"}), reason)


@pytest.mark.parametrize(("field_name", "reason"), [("condition_id", "condition_id does not match supplied runtime operator-review ack packet"), ("token_id", "token_id does not match supplied runtime operator-review ack packet"), ("outcome", "outcome does not match supplied runtime operator-review ack packet")])
def test_top_level_route_mismatch_with_supplied_ack_packet_fails_closed(field_name: str, reason: str) -> None:
    ack = _valid_supplied_runtime_operator_review_ack_packet(**{field_name: "different"})
    _assert_blocked_with_reason(_valid_bridge_record(supplied_runtime_operator_review_ack_packet=ack), reason)


def _ack_with_handoff(handoff: sorh.SuppliedRuntimeOperatorReviewHandoffRecord, **overrides: object) -> soack.SuppliedRuntimeOperatorReviewAckPacketRecord:
    values = {"condition_id": handoff.condition_id, "token_id": handoff.token_id, "outcome": handoff.outcome, "supplied_runtime_operator_review_handoff": handoff}
    values.update(overrides)
    return _valid_supplied_runtime_operator_review_ack_packet(**values)


def test_nested_fixture_handoff_bridge_and_supplied_ack_packet_route_mismatch_fails_closed() -> None:
    ack = _valid_supplied_runtime_operator_review_ack_packet(condition_id="different")
    record = _valid_bridge_record(condition_id="different", supplied_runtime_operator_review_ack_packet=ack)
    _assert_blocked_with_reason(record, "nested fixture-only operator-review handoff bridge and supplied runtime operator-review ack packet routes do not match")


def test_nested_supplied_runtime_operator_review_handoff_mismatch_fails_closed() -> None:
    handoff = _valid_supplied_runtime_operator_review_handoff(condition_id="different")
    ack = _ack_with_handoff(handoff)
    record = _valid_bridge_record(condition_id="different", supplied_runtime_operator_review_ack_packet=ack)
    _assert_blocked_with_reason(record, "nested supplied runtime operator-review handoffs do not match")


def test_nested_supplied_runtime_trace_packet_mismatch_fails_closed() -> None:
    packet = _valid_supplied_runtime_trace_packet(condition_id="different")
    handoff = _valid_supplied_runtime_operator_review_handoff(condition_id="different", supplied_runtime_trace_packet=packet)
    ack = _ack_with_handoff(handoff)
    record = _valid_bridge_record(condition_id="different", supplied_runtime_operator_review_ack_packet=ack)
    _assert_blocked_with_reason(record, "nested supplied runtime trace packets do not match")


def test_nested_supplied_runtime_end_to_end_smoke_mismatch_fails_closed() -> None:
    smoke = _valid_supplied_runtime_end_to_end_smoke(condition_id="different")
    packet = _valid_supplied_runtime_trace_packet(condition_id="different", supplied_runtime_end_to_end_smoke=smoke)
    handoff = _valid_supplied_runtime_operator_review_handoff(condition_id="different", supplied_runtime_trace_packet=packet)
    ack = _ack_with_handoff(handoff)
    record = _valid_bridge_record(condition_id="different", supplied_runtime_operator_review_ack_packet=ack)
    _assert_blocked_with_reason(record, "nested supplied runtime end-to-end smokes do not match")


def test_nested_supplied_runtime_dry_run_report_mismatch_fails_closed() -> None:
    report = _valid_supplied_runtime_dry_run_report(condition_id="different")
    smoke = _valid_supplied_runtime_end_to_end_smoke(condition_id="different", supplied_runtime_dry_run_report=report)
    packet = _valid_supplied_runtime_trace_packet(condition_id="different", supplied_runtime_end_to_end_smoke=smoke)
    handoff = _valid_supplied_runtime_operator_review_handoff(condition_id="different", supplied_runtime_trace_packet=packet)
    ack = _ack_with_handoff(handoff)
    record = _valid_bridge_record(condition_id="different", supplied_runtime_operator_review_ack_packet=ack)
    _assert_blocked_with_reason(record, "nested supplied runtime dry-run reports do not match")


def test_nested_supplied_runtime_dry_run_packet_mismatch_fails_closed() -> None:
    dry_packet = _valid_supplied_runtime_dry_run_packet(condition_id="different")
    report = _valid_supplied_runtime_dry_run_report(condition_id="different", supplied_runtime_dry_run_packet=dry_packet)
    smoke = _valid_supplied_runtime_end_to_end_smoke(condition_id="different", supplied_runtime_dry_run_report=report)
    packet = _valid_supplied_runtime_trace_packet(condition_id="different", supplied_runtime_end_to_end_smoke=smoke)
    handoff = _valid_supplied_runtime_operator_review_handoff(condition_id="different", supplied_runtime_trace_packet=packet)
    ack = _ack_with_handoff(handoff)
    record = _valid_bridge_record(condition_id="different", supplied_runtime_operator_review_ack_packet=ack)
    _assert_blocked_with_reason(record, "nested supplied runtime dry-run packets do not match")


def test_nested_supplied_evidence_packet_mismatch_fails_closed() -> None:
    contract = _valid_contract(condition_id="different")
    evidence = _valid_supplied_evidence_packet(condition_id="different", supplied_market_contract=contract)
    bundle = _valid_supplied_runtime_validation_bundle(condition_id="different", supplied_evidence_packet=evidence)
    dry_packet = _valid_supplied_runtime_dry_run_packet(condition_id="different", supplied_runtime_validation_bundle=bundle)
    report = _valid_supplied_runtime_dry_run_report(condition_id="different", supplied_runtime_dry_run_packet=dry_packet)
    smoke = _valid_supplied_runtime_end_to_end_smoke(condition_id="different", supplied_runtime_dry_run_report=report)
    packet = _valid_supplied_runtime_trace_packet(condition_id="different", supplied_runtime_end_to_end_smoke=smoke)
    handoff = _valid_supplied_runtime_operator_review_handoff(condition_id="different", supplied_runtime_trace_packet=packet)
    ack = _ack_with_handoff(handoff)
    record = _valid_bridge_record(condition_id="different", supplied_runtime_operator_review_ack_packet=ack)
    _assert_blocked_with_reason(record, "nested supplied evidence packets do not match")


def test_fixture_handoff_bridge_summary_mismatch_fails_closed() -> None:
    _assert_blocked_with_reason(_valid_bridge_record(fixture_handoff_bridge_summary="different"), "fixture handoff bridge summary does not match fixture-only operator-review handoff bridge")


def test_supplied_ack_summary_mismatch_fails_closed() -> None:
    _assert_blocked_with_reason(_valid_bridge_record(supplied_ack_summary="different"), "supplied ack summary does not match supplied runtime operator-review ack packet")


def test_operator_review_summary_mismatch_with_supplied_runtime_operator_review_ack_packet_fails_closed() -> None:
    ack = _valid_supplied_runtime_operator_review_ack_packet(operator_review_summary="different")
    _assert_blocked_with_reason(_valid_bridge_record(supplied_runtime_operator_review_ack_packet=ack), "operator review summary does not match supplied runtime operator-review ack packet")


def test_operator_review_summary_mismatch_with_fixture_handoff_bridge_fails_closed() -> None:
    fixture = _valid_operator_review_handoff_bridge(operator_review_summary="different")
    _assert_blocked_with_reason(_valid_bridge_record(fixture_only_source_provider_operator_review_handoff_bridge=fixture), "operator review summary does not match fixture-only operator-review handoff bridge")


@pytest.mark.parametrize("status", [s for s in bridge.FixtureOnlyOperatorReviewAckBridgeStatus if s is not bridge.FixtureOnlyOperatorReviewAckBridgeStatus.FIXTURE_ONLY_OPERATOR_REVIEW_ACK_BRIDGE_RECORDED])
def test_non_recorded_statuses_fail_closed(status) -> None:
    _assert_blocked_with_reason(_valid_bridge_record(fixture_only_operator_review_ack_bridge_status=status), f"fixture-only operator-review ack bridge status is {status.value}")


@pytest.mark.parametrize("posture", [p for p in bridge.FixtureOnlyOperatorReviewAckBridgePosture if p is not bridge.FixtureOnlyOperatorReviewAckBridgePosture.FIXTURE_ONLY_OPERATOR_REVIEW_ACK_BRIDGE_IN_MEMORY_ONLY])
def test_non_in_memory_postures_fail_closed(posture) -> None:
    _assert_blocked_with_reason(_valid_bridge_record(fixture_only_operator_review_ack_bridge_posture=posture), f"fixture-only operator-review ack bridge posture is {posture.value}")


@pytest.mark.parametrize("status", [s for s in bridge.OperatorReviewAckBridgeAlignmentStatus if s is not bridge.OperatorReviewAckBridgeAlignmentStatus.OPERATOR_REVIEW_ACK_BRIDGE_ALIGNED])
def test_non_aligned_statuses_fail_closed(status) -> None:
    _assert_blocked_with_reason(_valid_bridge_record(operator_review_ack_bridge_alignment_status=status), f"operator-review ack bridge alignment status is {status.value}")


@pytest.mark.parametrize("status", [s for s in bridge.NoLookaheadStatus if s is not bridge.NoLookaheadStatus.NO_LOOKAHEAD_RECORDED])
def test_non_recorded_no_lookahead_statuses_fail_closed(status) -> None:
    _assert_blocked_with_reason(_valid_bridge_record(no_lookahead_status=status), f"no-lookahead status is {status.value}")


@pytest.mark.parametrize("status", [s for s in bridge.OperatorReviewStatus if s is not bridge.OperatorReviewStatus.OPERATOR_REVIEW_REQUIRED])
def test_non_required_operator_review_statuses_fail_closed(status) -> None:
    _assert_blocked_with_reason(_valid_bridge_record(operator_review_status=status), f"operator review status is {status.value}")


@pytest.mark.parametrize("status", [s for s in bridge.RuntimeGateStatus if s is not bridge.RuntimeGateStatus.RUNTIME_GATE_READY])
def test_non_ready_runtime_gate_statuses_fail_closed(status) -> None:
    _assert_blocked_with_reason(_valid_bridge_record(runtime_gate_status=status), f"runtime gate status is {status.value}")


def _source_without_docstrings(path: Path) -> str:
    module = ast.parse(path.read_text())
    for node in ast.walk(module):
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if node.body and isinstance(node.body[0], ast.Expr) and isinstance(node.body[0].value, ast.Constant) and isinstance(node.body[0].value.value, str):
                node.body[0] = ast.Pass()
    return ast.unparse(module)


def test_no_legacy_identifier_dataclass_or_input_field() -> None:
    forbidden = "market" + "_" + "id"
    for path in (MODULE_PATH, TEST_PATH):
        source = path.read_text()
        assert f"{forbidden}:" not in source
        assert f'"{forbidden}"' not in source
        assert f"'{forbidden}'" not in source


def test_source_has_no_forbidden_runtime_or_side_effect_terms() -> None:
    source = _source_without_docstrings(MODULE_PATH)
    forbidden_terms = ["requests", "httpx", "urllib", "aiohttp", "boto3", "polymarket", "kalshi", "duckdb", "pandas", "subprocess", "open(", ".read_text(", ".write_text(", "socket", "os.environ", "dotenv", "place_order", "paper_trade", "trade", "backtest", "score", "execute_order", "submit_order", "persist", "database", "postgres", "redis", "export", "write", "save", "owner_decision", "capture_decision", "operator_decision", "execute_decision", "celery", "rabbitmq", "sqs", "enqueue(", "dequeue(", "publish(", "subscribe(", "scheduler", "provider_client", "api_call", "scrape", "download", "credentials", "production", "simulate", "simulation", "generate_report", "report_writer", "execute_smoke", "run_smoke", "execute_trace", "run_trace", "deliver_handoff", "send_handoff", "deliver_ack", "send_ack", "acknowledgement_delivery", "notification", "notify"]
    for term in forbidden_terms:
        assert term not in source
