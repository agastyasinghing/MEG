import ast
from dataclasses import asdict
from pathlib import Path

import pytest

from meg.weather.stage2 import fixture_only_source_provider_dry_run_report_bridge_runtime as bridge
from meg.weather.stage2 import fixture_only_source_provider_dry_run_bridge_runtime as dry_run_bridge
from meg.weather.stage2 import fixture_only_source_provider_validation_bundle_bridge_runtime as validation_bridge
from meg.weather.stage2 import fixture_only_source_provider_evidence_bridge_runtime as evidence_bridge
from meg.weather.stage2 import fixture_only_source_provider_runtime as fspr
from meg.weather.stage2 import supplied_runtime_dry_run_report as srdr
from meg.weather.stage2 import supplied_runtime_dry_run_packet as srdp
from meg.weather.stage2 import supplied_runtime_validation_bundle as srvb
from meg.weather.stage2 import supplied_evidence_packet_runtime as sepr
from meg.weather.stage2 import supplied_market_contract_runtime as smcr
from tests.core import test_weather_stage2_fixture_only_source_provider_dry_run_bridge_runtime as base


MODULE_PATH = Path("meg/weather/stage2/fixture_only_source_provider_dry_run_report_bridge_runtime.py")
TEST_PATH = Path("tests/core/test_weather_stage2_fixture_only_source_provider_dry_run_report_bridge_runtime.py")


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
    return base._valid_bridge_record(**overrides)


def _valid_supplied_runtime_dry_run_report(**overrides: object) -> srdr.SuppliedRuntimeDryRunReportRecord:
    values = {
        "condition_id": "condition-1",
        "token_id": "token-1",
        "outcome": "Yes",
        "supplied_runtime_dry_run_packet": _valid_supplied_runtime_dry_run_packet(),
        "dry_run_report_id": "dry-run-report-1",
        "report_summary": "Caller supplied dry-run report summary text.",
        "operator_review_summary": "Operator review remains required before any action.",
        "blocked_reason_summary": "No blocker for this valid dry-run report.",
        "dry_run_report_status": srdr.DryRunReportStatus.DRY_RUN_REPORT_RECORDED,
        "dry_run_report_completeness_status": srdr.DryRunReportCompletenessStatus.DRY_RUN_REPORT_COMPLETE,
        "operator_review_status": srdr.OperatorReviewStatus.OPERATOR_REVIEW_REQUIRED,
        "runtime_gate_status": srdr.RuntimeGateStatus.RUNTIME_GATE_READY,
    }
    values.update(overrides)
    return srdr.SuppliedRuntimeDryRunReportRecord(**values)


def _valid_bridge_record(**overrides: object) -> bridge.FixtureOnlySourceProviderDryRunReportBridgeRecord:
    values = {
        "condition_id": "condition-1",
        "token_id": "token-1",
        "outcome": "Yes",
        "fixture_only_source_provider_dry_run_bridge": _valid_dry_run_bridge(),
        "supplied_runtime_dry_run_report": _valid_supplied_runtime_dry_run_report(),
        "dry_run_report_bridge_id": "dry-run-report-bridge-1",
        "dry_run_report_bridge_summary": "Fixture-only dry-run bridge linked to supplied report.",
        "fixture_dry_run_bridge_summary": "Fixture-only validation bridge linked to dry-run packet.",
        "supplied_report_summary": "Caller supplied dry-run report summary text.",
        "operator_review_summary": "Operator review remains required before any action.",
        "blocked_reason_summary": "No blocker for this valid dry-run report bridge.",
        "fixture_only_dry_run_report_bridge_status": bridge.FixtureOnlyDryRunReportBridgeStatus.FIXTURE_ONLY_DRY_RUN_REPORT_BRIDGE_RECORDED,
        "fixture_only_dry_run_report_bridge_posture": bridge.FixtureOnlyDryRunReportBridgePosture.FIXTURE_ONLY_DRY_RUN_REPORT_BRIDGE_IN_MEMORY_ONLY,
        "dry_run_report_bridge_alignment_status": bridge.DryRunReportBridgeAlignmentStatus.DRY_RUN_REPORT_BRIDGE_ALIGNED,
        "no_lookahead_status": bridge.NoLookaheadStatus.NO_LOOKAHEAD_RECORDED,
        "operator_review_status": bridge.OperatorReviewStatus.OPERATOR_REVIEW_REQUIRED,
        "runtime_gate_status": bridge.RuntimeGateStatus.RUNTIME_GATE_READY,
    }
    values.update(overrides)
    return bridge.FixtureOnlySourceProviderDryRunReportBridgeRecord(**values)


def _assert_blocked_with_reason(record, reason: str) -> None:
    result = bridge.validate_fixture_only_source_provider_dry_run_report_bridge_record(record)
    assert result.passed is False
    assert result.severity is bridge.ValidationSeverity.BLOCKED
    assert reason in result.reasons


def test_enums_are_closed_sets() -> None:
    assert bridge.FixtureOnlyDryRunReportBridgeStatus.values() == frozenset({"fixture_only_dry_run_report_bridge_recorded", "fixture_only_dry_run_report_bridge_missing", "fixture_only_dry_run_report_bridge_ambiguous", "fixture_only_dry_run_report_bridge_unsupported", "fixture_only_dry_run_report_bridge_unknown"})
    assert bridge.FixtureOnlyDryRunReportBridgePosture.values() == frozenset({"fixture_only_dry_run_report_bridge_in_memory_only", "fixture_only_dry_run_report_bridge_missing", "fixture_only_dry_run_report_bridge_ambiguous", "fixture_only_dry_run_report_bridge_unsupported", "fixture_only_dry_run_report_bridge_unknown"})
    assert bridge.DryRunReportBridgeAlignmentStatus.values() == frozenset({"dry_run_report_bridge_aligned", "dry_run_report_bridge_mismatch", "dry_run_report_bridge_missing", "dry_run_report_bridge_ambiguous", "dry_run_report_bridge_unknown"})
    assert bridge.NoLookaheadStatus.values() == frozenset({"no_lookahead_recorded", "no_lookahead_missing", "no_lookahead_ambiguous", "no_lookahead_unknown"})
    assert bridge.OperatorReviewStatus.values() == frozenset({"operator_review_required", "operator_review_missing", "operator_review_ambiguous", "operator_review_not_required", "operator_review_unknown"})
    assert bridge.RuntimeGateStatus.values() == frozenset({"runtime_gate_ready", "runtime_gate_blocked", "runtime_gate_requires_manual_review", "runtime_gate_unknown"})
    assert bridge.ValidationSeverity.values() == frozenset({"passed", "caution", "failed", "blocked"})


def test_dataclass_construction() -> None:
    record = _valid_bridge_record(provenance_notes="caller supplied")
    assert record.condition_id == "condition-1"
    assert isinstance(record.fixture_only_source_provider_dry_run_bridge, dry_run_bridge.FixtureOnlySourceProviderDryRunBridgeRecord)
    assert isinstance(record.supplied_runtime_dry_run_report, srdr.SuppliedRuntimeDryRunReportRecord)
    assert record.provenance_notes == "caller supplied"


def test_mapping_construction_coerces_string_enums_and_nested_mappings() -> None:
    record = bridge.fixture_only_source_provider_dry_run_report_bridge_record_from_mapping({
        **asdict(_valid_bridge_record()),
        "fixture_only_source_provider_dry_run_bridge": asdict(_valid_dry_run_bridge()),
        "supplied_runtime_dry_run_report": asdict(_valid_supplied_runtime_dry_run_report()),
        "fixture_only_dry_run_report_bridge_status": "fixture_only_dry_run_report_bridge_recorded",
        "fixture_only_dry_run_report_bridge_posture": "fixture_only_dry_run_report_bridge_in_memory_only",
        "dry_run_report_bridge_alignment_status": "dry_run_report_bridge_aligned",
        "no_lookahead_status": "no_lookahead_recorded",
        "operator_review_status": "operator_review_required",
        "runtime_gate_status": "runtime_gate_ready",
    })
    assert isinstance(record.fixture_only_source_provider_dry_run_bridge, dry_run_bridge.FixtureOnlySourceProviderDryRunBridgeRecord)
    assert isinstance(record.supplied_runtime_dry_run_report, srdr.SuppliedRuntimeDryRunReportRecord)
    assert record.runtime_gate_status is bridge.RuntimeGateStatus.RUNTIME_GATE_READY


def test_valid_record_passes() -> None:
    result = bridge.validate_fixture_only_source_provider_dry_run_report_bridge_record(_valid_bridge_record())
    assert result.passed is True
    assert result.severity is bridge.ValidationSeverity.PASSED
    assert result.reasons == ()


@pytest.mark.parametrize("field_name", ["condition_id", "token_id", "outcome", "dry_run_report_bridge_id", "dry_run_report_bridge_summary", "fixture_dry_run_bridge_summary", "supplied_report_summary", "operator_review_summary"])
def test_blank_required_text_fields_fail_closed(field_name: str) -> None:
    _assert_blocked_with_reason(_valid_bridge_record(**{field_name: " "}), f"{field_name} is missing")


def test_blank_blocked_reason_summary_is_allowed_when_otherwise_valid() -> None:
    assert bridge.validate_fixture_only_source_provider_dry_run_report_bridge_record(_valid_bridge_record(blocked_reason_summary="")).passed is True


def test_blank_blocked_reason_summary_fails_when_another_validation_failure_exists() -> None:
    _assert_blocked_with_reason(_valid_bridge_record(condition_id="", blocked_reason_summary=""), "blocked_reason_summary is missing")


def test_invalid_nested_fixture_only_dry_run_bridge_fails_closed() -> None:
    nested = _valid_dry_run_bridge(dry_run_bridge_id="")
    _assert_blocked_with_reason(_valid_bridge_record(fixture_only_source_provider_dry_run_bridge=nested), "fixture-only source provider dry-run bridge is invalid")


def test_invalid_nested_supplied_runtime_dry_run_report_fails_closed() -> None:
    nested = _valid_supplied_runtime_dry_run_report(dry_run_report_id="")
    _assert_blocked_with_reason(_valid_bridge_record(supplied_runtime_dry_run_report=nested), "supplied runtime dry-run report is invalid")


@pytest.mark.parametrize(("field_name", "reason"), [("condition_id", "condition_id does not match fixture-only dry-run bridge"), ("token_id", "token_id does not match fixture-only dry-run bridge"), ("outcome", "outcome does not match fixture-only dry-run bridge")])
def test_top_level_route_mismatch_with_fixture_dry_run_bridge_fails_closed(field_name: str, reason: str) -> None:
    _assert_blocked_with_reason(_valid_bridge_record(**{field_name: "different"}), reason)


@pytest.mark.parametrize(("field_name", "reason"), [("condition_id", "condition_id does not match supplied runtime dry-run report"), ("token_id", "token_id does not match supplied runtime dry-run report"), ("outcome", "outcome does not match supplied runtime dry-run report")])
def test_top_level_route_mismatch_with_supplied_runtime_dry_run_report_fails_closed(field_name: str, reason: str) -> None:
    _assert_blocked_with_reason(_valid_bridge_record(**{field_name: "different"}), reason)


def test_nested_fixture_only_dry_run_bridge_and_supplied_runtime_dry_run_report_route_mismatch_fails_closed() -> None:
    nested = _valid_supplied_runtime_dry_run_report(condition_id="condition-2")
    _assert_blocked_with_reason(_valid_bridge_record(supplied_runtime_dry_run_report=nested), "nested fixture-only dry-run bridge and supplied runtime dry-run report routes do not match")


def test_nested_supplied_runtime_dry_run_packet_mismatch_fails_closed() -> None:
    packet = _valid_supplied_runtime_dry_run_packet(supplied_runtime_validation_bundle=_valid_supplied_runtime_validation_bundle(token_id="token-2"))
    report = _valid_supplied_runtime_dry_run_report(supplied_runtime_dry_run_packet=packet)
    _assert_blocked_with_reason(_valid_bridge_record(supplied_runtime_dry_run_report=report), "nested supplied runtime dry-run packets do not match")


def test_nested_supplied_evidence_packet_mismatch_fails_closed() -> None:
    bundle = _valid_supplied_runtime_validation_bundle(supplied_evidence_packet=_valid_supplied_evidence_packet(token_id="token-2"))
    packet = _valid_supplied_runtime_dry_run_packet(supplied_runtime_validation_bundle=bundle)
    report = _valid_supplied_runtime_dry_run_report(supplied_runtime_dry_run_packet=packet)
    _assert_blocked_with_reason(_valid_bridge_record(supplied_runtime_dry_run_report=report), "nested supplied evidence packets do not match")


def test_fixture_dry_run_bridge_summary_mismatch_fails_closed() -> None:
    _assert_blocked_with_reason(_valid_bridge_record(fixture_dry_run_bridge_summary="different"), "fixture dry-run bridge summary does not match fixture-only dry-run bridge")


def test_supplied_report_summary_mismatch_fails_closed() -> None:
    _assert_blocked_with_reason(_valid_bridge_record(supplied_report_summary="different"), "supplied report summary does not match supplied runtime dry-run report")


def test_operator_review_summary_mismatch_with_supplied_runtime_dry_run_report_fails_closed() -> None:
    report = _valid_supplied_runtime_dry_run_report(operator_review_summary="different")
    _assert_blocked_with_reason(_valid_bridge_record(supplied_runtime_dry_run_report=report), "operator review summary does not match supplied runtime dry-run report")


def test_operator_review_summary_mismatch_with_fixture_only_dry_run_bridge_fails_closed() -> None:
    nested = _valid_dry_run_bridge(operator_review_summary="different")
    _assert_blocked_with_reason(_valid_bridge_record(fixture_only_source_provider_dry_run_bridge=nested), "operator review summary does not match fixture-only dry-run bridge")


@pytest.mark.parametrize("status", [s for s in bridge.FixtureOnlyDryRunReportBridgeStatus if s is not bridge.FixtureOnlyDryRunReportBridgeStatus.FIXTURE_ONLY_DRY_RUN_REPORT_BRIDGE_RECORDED])
def test_non_recorded_fixture_only_dry_run_report_bridge_statuses_fail_closed(status) -> None:
    _assert_blocked_with_reason(_valid_bridge_record(fixture_only_dry_run_report_bridge_status=status), f"fixture-only dry-run report bridge status is {status.value}")


@pytest.mark.parametrize("posture", [p for p in bridge.FixtureOnlyDryRunReportBridgePosture if p is not bridge.FixtureOnlyDryRunReportBridgePosture.FIXTURE_ONLY_DRY_RUN_REPORT_BRIDGE_IN_MEMORY_ONLY])
def test_non_in_memory_bridge_postures_fail_closed(posture) -> None:
    _assert_blocked_with_reason(_valid_bridge_record(fixture_only_dry_run_report_bridge_posture=posture), f"fixture-only dry-run report bridge posture is {posture.value}")


@pytest.mark.parametrize("status", [s for s in bridge.DryRunReportBridgeAlignmentStatus if s is not bridge.DryRunReportBridgeAlignmentStatus.DRY_RUN_REPORT_BRIDGE_ALIGNED])
def test_non_aligned_bridge_alignment_statuses_fail_closed(status) -> None:
    _assert_blocked_with_reason(_valid_bridge_record(dry_run_report_bridge_alignment_status=status), f"dry-run report bridge alignment status is {status.value}")


@pytest.mark.parametrize("status", [s for s in bridge.NoLookaheadStatus if s is not bridge.NoLookaheadStatus.NO_LOOKAHEAD_RECORDED])
def test_non_recorded_no_lookahead_statuses_fail_closed(status) -> None:
    _assert_blocked_with_reason(_valid_bridge_record(no_lookahead_status=status), f"no-lookahead status is {status.value}")


@pytest.mark.parametrize("status", [s for s in bridge.OperatorReviewStatus if s is not bridge.OperatorReviewStatus.OPERATOR_REVIEW_REQUIRED])
def test_non_required_operator_review_statuses_fail_closed(status) -> None:
    _assert_blocked_with_reason(_valid_bridge_record(operator_review_status=status), f"operator review status is {status.value}")


@pytest.mark.parametrize("status", [s for s in bridge.RuntimeGateStatus if s is not bridge.RuntimeGateStatus.RUNTIME_GATE_READY])
def test_non_ready_runtime_gates_fail_closed(status) -> None:
    _assert_blocked_with_reason(_valid_bridge_record(runtime_gate_status=status), f"runtime gate status is {status.value}")


def _without_docstrings(source: str) -> str:
    parsed = ast.parse(source)
    for node in ast.walk(parsed):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.body and isinstance(node.body[0], ast.Expr) and isinstance(getattr(node.body[0], "value", None), ast.Constant) and isinstance(node.body[0].value.value, str):
                node.body[0] = ast.Pass()
    return ast.unparse(parsed)


def test_no_legacy_route_identifier_dataclass_or_input_field() -> None:
    for path in (MODULE_PATH, TEST_PATH):
        source = path.read_text()
        assert "mar" + "ket" + "_" + "id:" not in source
        assert '"mar' + 'ket' + '_' + 'id"' not in source
        assert "'mar" + "ket" + "_" + "id'" not in source


def test_source_module_has_no_forbidden_runtime_calls_or_imports() -> None:
    source = _without_docstrings(MODULE_PATH.read_text())
    forbidden_terms = ["requests", "httpx", "urllib", "aiohttp", "boto3", "polymarket", "kalshi", "duckdb", "pandas", "subprocess", "open(", ".read_text(", ".write_text(", "socket", "os.environ", "dotenv", "place_order", "paper_trade", "trade", "backtest", "score", "execute_order", "submit_order", "persist", "database", "postgres", "redis", "export", "write", "save", "owner_decision", "capture_decision", "celery", "rabbitmq", "sqs", "enqueue(", "dequeue(", "publish(", "subscribe(", "scheduler", "provider_client", "api_call", "scrape", "download", "credentials", "production", "simulate", "simulation", "generate_report", "report_writer"]
    lowered = source.lower()
    assert not [term for term in forbidden_terms if term in lowered]
