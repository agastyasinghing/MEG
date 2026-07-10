import ast
from dataclasses import asdict
from pathlib import Path

import pytest

from meg.weather.stage2 import fixture_only_source_provider_trace_bridge_runtime as bridge
from meg.weather.stage2 import fixture_only_source_provider_end_to_end_smoke_bridge_runtime as smoke_bridge
from meg.weather.stage2 import fixture_only_source_provider_dry_run_report_bridge_runtime as dry_run_report_bridge
from meg.weather.stage2 import fixture_only_source_provider_dry_run_bridge_runtime as dry_run_bridge
from meg.weather.stage2 import fixture_only_source_provider_validation_bundle_bridge_runtime as validation_bridge
from meg.weather.stage2 import fixture_only_source_provider_evidence_bridge_runtime as evidence_bridge
from meg.weather.stage2 import fixture_only_source_provider_runtime as fspr
from meg.weather.stage2 import supplied_runtime_trace_packet as srtp
from meg.weather.stage2 import supplied_runtime_end_to_end_smoke as sees
from meg.weather.stage2 import supplied_runtime_dry_run_report as srdr
from meg.weather.stage2 import supplied_runtime_dry_run_packet as srdp
from meg.weather.stage2 import supplied_runtime_validation_bundle as srvb
from meg.weather.stage2 import supplied_evidence_packet_runtime as sepr
from meg.weather.stage2 import supplied_market_contract_runtime as smcr
from tests.core import test_weather_stage2_fixture_only_source_provider_end_to_end_smoke_bridge_runtime as base

MODULE_PATH = Path("meg/weather/stage2/fixture_only_source_provider_trace_bridge_runtime.py")
TEST_PATH = Path("tests/core/test_weather_stage2_fixture_only_source_provider_trace_bridge_runtime.py")


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
    return base._valid_bridge_record(**overrides)


def _valid_supplied_runtime_trace_packet(**overrides: object) -> srtp.SuppliedRuntimeTracePacketRecord:
    values = {
        "condition_id": "condition-1",
        "token_id": "token-1",
        "outcome": "Yes",
        "supplied_runtime_end_to_end_smoke": _valid_supplied_runtime_end_to_end_smoke(),
        "trace_packet_id": "trace-packet-1",
        "trace_summary": "Caller supplied runtime trace summary text.",
        "operator_review_summary": "Operator review remains required before any action.",
        "blocked_reason_summary": "No blocker for this valid trace packet.",
        "runtime_trace_packet_status": srtp.RuntimeTracePacketStatus.RUNTIME_TRACE_PACKET_RECORDED,
        "runtime_trace_completeness_status": srtp.RuntimeTraceCompletenessStatus.RUNTIME_TRACE_COMPLETE,
        "operator_review_status": srtp.OperatorReviewStatus.OPERATOR_REVIEW_REQUIRED,
        "runtime_gate_status": srtp.RuntimeGateStatus.RUNTIME_GATE_READY,
    }
    values.update(overrides)
    return srtp.SuppliedRuntimeTracePacketRecord(**values)


def _valid_bridge_record(**overrides: object) -> bridge.FixtureOnlySourceProviderTraceBridgeRecord:
    values = {
        "condition_id": "condition-1",
        "token_id": "token-1",
        "outcome": "Yes",
        "fixture_only_source_provider_end_to_end_smoke_bridge": _valid_end_to_end_smoke_bridge(),
        "supplied_runtime_trace_packet": _valid_supplied_runtime_trace_packet(),
        "trace_bridge_id": "trace-bridge-1",
        "trace_bridge_summary": "Fixture-only smoke bridge linked to supplied trace.",
        "fixture_end_to_end_smoke_bridge_summary": "Fixture-only dry-run report bridge linked to supplied smoke.",
        "supplied_trace_summary": "Caller supplied runtime trace summary text.",
        "operator_review_summary": "Operator review remains required before any action.",
        "blocked_reason_summary": "No blocker for this valid trace bridge.",
        "fixture_only_trace_bridge_status": bridge.FixtureOnlyTraceBridgeStatus.FIXTURE_ONLY_TRACE_BRIDGE_RECORDED,
        "fixture_only_trace_bridge_posture": bridge.FixtureOnlyTraceBridgePosture.FIXTURE_ONLY_TRACE_BRIDGE_IN_MEMORY_ONLY,
        "trace_bridge_alignment_status": bridge.TraceBridgeAlignmentStatus.TRACE_BRIDGE_ALIGNED,
        "no_lookahead_status": bridge.NoLookaheadStatus.NO_LOOKAHEAD_RECORDED,
        "operator_review_status": bridge.OperatorReviewStatus.OPERATOR_REVIEW_REQUIRED,
        "runtime_gate_status": bridge.RuntimeGateStatus.RUNTIME_GATE_READY,
    }
    values.update(overrides)
    return bridge.FixtureOnlySourceProviderTraceBridgeRecord(**values)


def _assert_blocked_with_reason(record, reason: str) -> None:
    result = bridge.validate_fixture_only_source_provider_trace_bridge_record(record)
    assert result.passed is False
    assert result.severity is bridge.ValidationSeverity.BLOCKED
    assert reason in result.reasons


def test_enums_are_closed_sets() -> None:
    assert bridge.FixtureOnlyTraceBridgeStatus.values() == frozenset({"fixture_only_trace_bridge_recorded", "fixture_only_trace_bridge_missing", "fixture_only_trace_bridge_ambiguous", "fixture_only_trace_bridge_unsupported", "fixture_only_trace_bridge_unknown"})
    assert bridge.FixtureOnlyTraceBridgePosture.values() == frozenset({"fixture_only_trace_bridge_in_memory_only", "fixture_only_trace_bridge_missing", "fixture_only_trace_bridge_ambiguous", "fixture_only_trace_bridge_unsupported", "fixture_only_trace_bridge_unknown"})
    assert bridge.TraceBridgeAlignmentStatus.values() == frozenset({"trace_bridge_aligned", "trace_bridge_mismatch", "trace_bridge_missing", "trace_bridge_ambiguous", "trace_bridge_unknown"})
    assert bridge.NoLookaheadStatus.values() == frozenset({"no_lookahead_recorded", "no_lookahead_missing", "no_lookahead_ambiguous", "no_lookahead_unknown"})
    assert bridge.OperatorReviewStatus.values() == frozenset({"operator_review_required", "operator_review_missing", "operator_review_ambiguous", "operator_review_not_required", "operator_review_unknown"})
    assert bridge.RuntimeGateStatus.values() == frozenset({"runtime_gate_ready", "runtime_gate_blocked", "runtime_gate_requires_manual_review", "runtime_gate_unknown"})
    assert bridge.ValidationSeverity.values() == frozenset({"passed", "caution", "failed", "blocked"})


def test_dataclass_construction() -> None:
    record = _valid_bridge_record(provenance_notes="caller supplied")
    assert record.condition_id == "condition-1"
    assert isinstance(record.fixture_only_source_provider_end_to_end_smoke_bridge, smoke_bridge.FixtureOnlySourceProviderEndToEndSmokeBridgeRecord)
    assert isinstance(record.supplied_runtime_trace_packet, srtp.SuppliedRuntimeTracePacketRecord)
    assert record.provenance_notes == "caller supplied"


def test_mapping_construction_coerces_string_enums_and_nested_mappings() -> None:
    record = bridge.fixture_only_source_provider_trace_bridge_record_from_mapping(asdict(_valid_bridge_record()))
    assert isinstance(record.fixture_only_source_provider_end_to_end_smoke_bridge, smoke_bridge.FixtureOnlySourceProviderEndToEndSmokeBridgeRecord)
    assert isinstance(record.supplied_runtime_trace_packet, srtp.SuppliedRuntimeTracePacketRecord)
    assert record.fixture_only_trace_bridge_status is bridge.FixtureOnlyTraceBridgeStatus.FIXTURE_ONLY_TRACE_BRIDGE_RECORDED
    assert record.provenance_notes == ""


def test_valid_record_passes() -> None:
    result = bridge.validate_fixture_only_source_provider_trace_bridge_record(_valid_bridge_record())
    assert result.passed is True
    assert result.severity is bridge.ValidationSeverity.PASSED
    assert result.reasons == ()


@pytest.mark.parametrize("field_name", ["condition_id", "token_id", "outcome", "trace_bridge_id", "trace_bridge_summary", "fixture_end_to_end_smoke_bridge_summary", "supplied_trace_summary", "operator_review_summary"])
def test_blank_required_text_fields_fail_closed(field_name: str) -> None:
    _assert_blocked_with_reason(_valid_bridge_record(**{field_name: "  "}), f"{field_name} is missing")


def test_blank_blocked_reason_summary_is_allowed_when_otherwise_valid() -> None:
    assert bridge.validate_fixture_only_source_provider_trace_bridge_record(_valid_bridge_record(blocked_reason_summary="")).passed is True


def test_blank_blocked_reason_summary_fails_when_another_validation_failure_exists() -> None:
    _assert_blocked_with_reason(_valid_bridge_record(condition_id="wrong", blocked_reason_summary=""), "blocked_reason_summary is missing")


def test_invalid_nested_fixture_only_end_to_end_smoke_bridge_fails_closed() -> None:
    nested = _valid_end_to_end_smoke_bridge(end_to_end_smoke_bridge_summary="")
    _assert_blocked_with_reason(_valid_bridge_record(fixture_only_source_provider_end_to_end_smoke_bridge=nested), "fixture-only source provider end-to-end smoke bridge is invalid")


def test_invalid_nested_supplied_runtime_trace_packet_fails_closed() -> None:
    nested = _valid_supplied_runtime_trace_packet(trace_summary="")
    _assert_blocked_with_reason(_valid_bridge_record(supplied_runtime_trace_packet=nested), "supplied runtime trace packet is invalid")


@pytest.mark.parametrize(("field_name", "reason"), [("condition_id", "condition_id does not match fixture-only end-to-end smoke bridge"), ("token_id", "token_id does not match fixture-only end-to-end smoke bridge"), ("outcome", "outcome does not match fixture-only end-to-end smoke bridge")])
def test_top_level_route_mismatch_with_fixture_bridge_fails_closed(field_name: str, reason: str) -> None:
    _assert_blocked_with_reason(_valid_bridge_record(**{field_name: "different"}), reason)


@pytest.mark.parametrize(("field_name", "reason"), [("condition_id", "condition_id does not match supplied runtime trace packet"), ("token_id", "token_id does not match supplied runtime trace packet"), ("outcome", "outcome does not match supplied runtime trace packet")])
def test_top_level_route_mismatch_with_supplied_trace_packet_fails_closed(field_name: str, reason: str) -> None:
    packet = _valid_supplied_runtime_trace_packet(**{field_name: "different"})
    _assert_blocked_with_reason(_valid_bridge_record(supplied_runtime_trace_packet=packet), reason)


def test_nested_fixture_bridge_and_supplied_trace_packet_route_mismatch_fails_closed() -> None:
    packet = _valid_supplied_runtime_trace_packet(condition_id="different")
    record = _valid_bridge_record(condition_id="different", supplied_runtime_trace_packet=packet)
    _assert_blocked_with_reason(record, "nested fixture-only end-to-end smoke bridge and supplied runtime trace packet routes do not match")


def test_nested_supplied_runtime_end_to_end_smoke_mismatch_fails_closed() -> None:
    smoke = _valid_supplied_runtime_end_to_end_smoke(condition_id="different")
    packet = _valid_supplied_runtime_trace_packet(condition_id="different", supplied_runtime_end_to_end_smoke=smoke)
    record = _valid_bridge_record(condition_id="different", supplied_runtime_trace_packet=packet)
    _assert_blocked_with_reason(record, "nested supplied runtime end-to-end smokes do not match")


def test_nested_supplied_runtime_dry_run_report_mismatch_fails_closed() -> None:
    report = _valid_supplied_runtime_dry_run_report(condition_id="different")
    smoke = _valid_supplied_runtime_end_to_end_smoke(condition_id="different", supplied_runtime_dry_run_report=report)
    packet = _valid_supplied_runtime_trace_packet(condition_id="different", supplied_runtime_end_to_end_smoke=smoke)
    record = _valid_bridge_record(condition_id="different", supplied_runtime_trace_packet=packet)
    _assert_blocked_with_reason(record, "nested supplied runtime dry-run reports do not match")


def test_nested_supplied_runtime_dry_run_packet_mismatch_fails_closed() -> None:
    dry_packet = _valid_supplied_runtime_dry_run_packet(condition_id="different")
    report = _valid_supplied_runtime_dry_run_report(condition_id="different", supplied_runtime_dry_run_packet=dry_packet)
    smoke = _valid_supplied_runtime_end_to_end_smoke(condition_id="different", supplied_runtime_dry_run_report=report)
    trace_packet = _valid_supplied_runtime_trace_packet(condition_id="different", supplied_runtime_end_to_end_smoke=smoke)
    record = _valid_bridge_record(condition_id="different", supplied_runtime_trace_packet=trace_packet)
    _assert_blocked_with_reason(record, "nested supplied runtime dry-run packets do not match")


def test_nested_supplied_evidence_packet_mismatch_fails_closed() -> None:
    contract = _valid_contract(condition_id="different")
    evidence = _valid_supplied_evidence_packet(condition_id="different", supplied_market_contract=contract)
    bundle = _valid_supplied_runtime_validation_bundle(condition_id="different", supplied_evidence_packet=evidence)
    dry_packet = _valid_supplied_runtime_dry_run_packet(condition_id="different", supplied_runtime_validation_bundle=bundle)
    report = _valid_supplied_runtime_dry_run_report(condition_id="different", supplied_runtime_dry_run_packet=dry_packet)
    smoke = _valid_supplied_runtime_end_to_end_smoke(condition_id="different", supplied_runtime_dry_run_report=report)
    trace_packet = _valid_supplied_runtime_trace_packet(condition_id="different", supplied_runtime_end_to_end_smoke=smoke)
    record = _valid_bridge_record(condition_id="different", supplied_runtime_trace_packet=trace_packet)
    _assert_blocked_with_reason(record, "nested supplied evidence packets do not match")


def test_fixture_end_to_end_smoke_bridge_summary_mismatch_fails_closed() -> None:
    _assert_blocked_with_reason(_valid_bridge_record(fixture_end_to_end_smoke_bridge_summary="different"), "fixture end-to-end smoke bridge summary does not match fixture-only end-to-end smoke bridge")


def test_supplied_trace_summary_mismatch_fails_closed() -> None:
    _assert_blocked_with_reason(_valid_bridge_record(supplied_trace_summary="different"), "supplied trace summary does not match supplied runtime trace packet")


def test_operator_review_summary_mismatch_with_supplied_runtime_trace_packet_fails_closed() -> None:
    packet = _valid_supplied_runtime_trace_packet(operator_review_summary="different")
    _assert_blocked_with_reason(_valid_bridge_record(supplied_runtime_trace_packet=packet), "operator review summary does not match supplied runtime trace packet")


def test_operator_review_summary_mismatch_with_fixture_end_to_end_smoke_bridge_fails_closed() -> None:
    fixture = _valid_end_to_end_smoke_bridge(operator_review_summary="different")
    _assert_blocked_with_reason(_valid_bridge_record(fixture_only_source_provider_end_to_end_smoke_bridge=fixture), "operator review summary does not match fixture-only end-to-end smoke bridge")


@pytest.mark.parametrize("status", [s for s in bridge.FixtureOnlyTraceBridgeStatus if s is not bridge.FixtureOnlyTraceBridgeStatus.FIXTURE_ONLY_TRACE_BRIDGE_RECORDED])
def test_non_recorded_statuses_fail_closed(status) -> None:
    _assert_blocked_with_reason(_valid_bridge_record(fixture_only_trace_bridge_status=status), f"fixture-only trace bridge status is {status.value}")


@pytest.mark.parametrize("posture", [p for p in bridge.FixtureOnlyTraceBridgePosture if p is not bridge.FixtureOnlyTraceBridgePosture.FIXTURE_ONLY_TRACE_BRIDGE_IN_MEMORY_ONLY])
def test_non_in_memory_postures_fail_closed(posture) -> None:
    _assert_blocked_with_reason(_valid_bridge_record(fixture_only_trace_bridge_posture=posture), f"fixture-only trace bridge posture is {posture.value}")


@pytest.mark.parametrize("status", [s for s in bridge.TraceBridgeAlignmentStatus if s is not bridge.TraceBridgeAlignmentStatus.TRACE_BRIDGE_ALIGNED])
def test_non_aligned_statuses_fail_closed(status) -> None:
    _assert_blocked_with_reason(_valid_bridge_record(trace_bridge_alignment_status=status), f"trace bridge alignment status is {status.value}")


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
    forbidden_terms = ["requests", "httpx", "urllib", "aiohttp", "boto3", "polymarket", "kalshi", "duckdb", "pandas", "subprocess", "open(", ".read_text(", ".write_text(", "socket", "os.environ", "dotenv", "place_order", "paper_trade", "trade", "backtest", "score", "execute_order", "submit_order", "persist", "database", "postgres", "redis", "export", "write", "save", "owner_decision", "capture_decision", "celery", "rabbitmq", "sqs", "enqueue(", "dequeue(", "publish(", "subscribe(", "scheduler", "provider_client", "api_call", "scrape", "download", "credentials", "production", "simulate", "simulation", "generate_report", "report_writer", "execute_smoke", "run_smoke", "execute_trace", "run_trace"]
    for term in forbidden_terms:
        assert term not in source
