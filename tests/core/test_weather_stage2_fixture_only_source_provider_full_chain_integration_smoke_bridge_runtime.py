import ast
from dataclasses import asdict
from pathlib import Path

import pytest

from meg.weather.stage2 import fixture_only_source_provider_full_chain_integration_smoke_bridge_runtime as bridge
from meg.weather.stage2 import fixture_only_source_provider_operator_review_completion_summary_bridge_runtime as summary_bridge
from meg.weather.stage2 import supplied_runtime_full_chain_integration_smoke as smoke
from tests.core import test_weather_stage2_fixture_only_source_provider_operator_review_completion_summary_bridge_runtime as summary_bridge_base
from tests.core import test_weather_stage2_fixture_only_source_provider_operator_review_final_bundle_bridge_runtime as bundle_base
from tests.core import test_weather_supplied_runtime_full_chain_integration_smoke as smoke_base
from tests.core import test_weather_supplied_runtime_operator_review_completion_summary as supplied_summary_base

MODULE_PATH = Path("meg/weather/stage2/fixture_only_source_provider_full_chain_integration_smoke_bridge_runtime.py")
TEST_PATH = Path("tests/core/test_weather_stage2_fixture_only_source_provider_full_chain_integration_smoke_bridge_runtime.py")


def _valid_completion_summary_bridge(**overrides: object) -> summary_bridge.FixtureOnlySourceProviderOperatorReviewCompletionSummaryBridgeRecord:
    return summary_bridge_base._valid_bridge_record(**overrides)


def _valid_supplied_integration_smoke(**overrides: object) -> smoke.SuppliedRuntimeFullChainIntegrationSmokeRecord:
    base = _valid_completion_summary_bridge()
    values = {
        "supplied_runtime_operator_review_completion_summary": base.supplied_runtime_operator_review_completion_summary,
        "operator_review_summary": base.operator_review_summary,
    }
    values.update(overrides)
    return smoke_base._valid_full_chain_integration_smoke(**values)


def _valid_bridge_record(**overrides: object) -> bridge.FixtureOnlySourceProviderFullChainIntegrationSmokeBridgeRecord:
    completion_summary_bridge = _valid_completion_summary_bridge()
    supplied_integration_smoke = _valid_supplied_integration_smoke()
    values = {
        "condition_id": "condition-1",
        "token_id": "token-1",
        "outcome": "Yes",
        "fixture_only_source_provider_operator_review_completion_summary_bridge": completion_summary_bridge,
        "supplied_runtime_full_chain_integration_smoke": supplied_integration_smoke,
        "full_chain_integration_smoke_bridge_id": "full-chain-integration-smoke-bridge-1",
        "full_chain_integration_smoke_bridge_summary": "Fixture-only completion-summary bridge linked to supplied full-chain integration smoke.",
        "fixture_completion_summary_bridge_summary": completion_summary_bridge.operator_review_completion_summary_bridge_summary,
        "supplied_integration_smoke_summary": supplied_integration_smoke.integration_smoke_summary,
        "operator_review_summary": completion_summary_bridge.operator_review_summary,
        "blocked_reason_summary": "No blocker for this valid full-chain integration-smoke bridge.",
        "fixture_only_full_chain_integration_smoke_bridge_status": bridge.FixtureOnlyFullChainIntegrationSmokeBridgeStatus.FIXTURE_ONLY_FULL_CHAIN_INTEGRATION_SMOKE_BRIDGE_RECORDED,
        "fixture_only_full_chain_integration_smoke_bridge_posture": bridge.FixtureOnlyFullChainIntegrationSmokeBridgePosture.FIXTURE_ONLY_FULL_CHAIN_INTEGRATION_SMOKE_BRIDGE_IN_MEMORY_ONLY,
        "full_chain_integration_smoke_bridge_alignment_status": bridge.FullChainIntegrationSmokeBridgeAlignmentStatus.FULL_CHAIN_INTEGRATION_SMOKE_BRIDGE_ALIGNED,
        "no_lookahead_status": bridge.NoLookaheadStatus.NO_LOOKAHEAD_RECORDED,
        "operator_review_status": bridge.OperatorReviewStatus.OPERATOR_REVIEW_REQUIRED,
        "runtime_gate_status": bridge.RuntimeGateStatus.RUNTIME_GATE_READY,
    }
    values.update(overrides)
    return bridge.FixtureOnlySourceProviderFullChainIntegrationSmokeBridgeRecord(**values)


def _assert_blocked_with_reason(record, reason: str) -> None:
    result = bridge.validate_fixture_only_source_provider_full_chain_integration_smoke_bridge_record(record)
    assert result.passed is False
    assert result.severity is bridge.ValidationSeverity.BLOCKED
    assert reason in result.reasons


def test_enums_are_closed_sets() -> None:
    assert bridge.FixtureOnlyFullChainIntegrationSmokeBridgeStatus.values() == frozenset({"fixture_only_full_chain_integration_smoke_bridge_recorded", "fixture_only_full_chain_integration_smoke_bridge_missing", "fixture_only_full_chain_integration_smoke_bridge_ambiguous", "fixture_only_full_chain_integration_smoke_bridge_unsupported", "fixture_only_full_chain_integration_smoke_bridge_unknown"})
    assert bridge.FixtureOnlyFullChainIntegrationSmokeBridgePosture.values() == frozenset({"fixture_only_full_chain_integration_smoke_bridge_in_memory_only", "fixture_only_full_chain_integration_smoke_bridge_missing", "fixture_only_full_chain_integration_smoke_bridge_ambiguous", "fixture_only_full_chain_integration_smoke_bridge_unsupported", "fixture_only_full_chain_integration_smoke_bridge_unknown"})
    assert bridge.FullChainIntegrationSmokeBridgeAlignmentStatus.values() == frozenset({"full_chain_integration_smoke_bridge_aligned", "full_chain_integration_smoke_bridge_mismatch", "full_chain_integration_smoke_bridge_missing", "full_chain_integration_smoke_bridge_ambiguous", "full_chain_integration_smoke_bridge_unknown"})
    assert bridge.NoLookaheadStatus.values() == frozenset({"no_lookahead_recorded", "no_lookahead_missing", "no_lookahead_ambiguous", "no_lookahead_unknown"})
    assert bridge.OperatorReviewStatus.values() == frozenset({"operator_review_required", "operator_review_missing", "operator_review_ambiguous", "operator_review_not_required", "operator_review_unknown"})
    assert bridge.RuntimeGateStatus.values() == frozenset({"runtime_gate_ready", "runtime_gate_blocked", "runtime_gate_requires_manual_review", "runtime_gate_unknown"})
    assert bridge.ValidationSeverity.values() == frozenset({"passed", "caution", "failed", "blocked"})


def test_frozen_dataclass_construction() -> None:
    record = _valid_bridge_record(provenance_notes="caller supplied")
    assert isinstance(record.fixture_only_source_provider_operator_review_completion_summary_bridge, summary_bridge.FixtureOnlySourceProviderOperatorReviewCompletionSummaryBridgeRecord)
    assert isinstance(record.supplied_runtime_full_chain_integration_smoke, smoke.SuppliedRuntimeFullChainIntegrationSmokeRecord)
    assert record.provenance_notes == "caller supplied"
    with pytest.raises(Exception):
        record.condition_id = "changed"


def test_mapping_construction_coerces_string_enums_and_nested_mappings() -> None:
    record = bridge.fixture_only_source_provider_full_chain_integration_smoke_bridge_record_from_mapping(asdict(_valid_bridge_record()))
    assert isinstance(record.fixture_only_source_provider_operator_review_completion_summary_bridge, summary_bridge.FixtureOnlySourceProviderOperatorReviewCompletionSummaryBridgeRecord)
    assert isinstance(record.supplied_runtime_full_chain_integration_smoke, smoke.SuppliedRuntimeFullChainIntegrationSmokeRecord)
    assert record.fixture_only_full_chain_integration_smoke_bridge_status is bridge.FixtureOnlyFullChainIntegrationSmokeBridgeStatus.FIXTURE_ONLY_FULL_CHAIN_INTEGRATION_SMOKE_BRIDGE_RECORDED
    assert record.provenance_notes == ""


def test_valid_record_passes() -> None:
    result = bridge.validate_fixture_only_source_provider_full_chain_integration_smoke_bridge_record(_valid_bridge_record())
    assert result.passed is True
    assert result.severity is bridge.ValidationSeverity.PASSED
    assert result.reasons == ()


@pytest.mark.parametrize("field_name", ["condition_id", "token_id", "outcome", "full_chain_integration_smoke_bridge_id", "full_chain_integration_smoke_bridge_summary", "fixture_completion_summary_bridge_summary", "supplied_integration_smoke_summary", "operator_review_summary"])
def test_blank_required_text_fields_fail_closed(field_name: str) -> None:
    _assert_blocked_with_reason(_valid_bridge_record(**{field_name: "  "}), f"{field_name} is missing")


def test_blank_blocked_reason_summary_is_allowed_when_otherwise_valid() -> None:
    assert bridge.validate_fixture_only_source_provider_full_chain_integration_smoke_bridge_record(_valid_bridge_record(blocked_reason_summary="")).passed is True


def test_blank_blocked_reason_summary_is_required_when_another_failure_exists() -> None:
    _assert_blocked_with_reason(_valid_bridge_record(condition_id="wrong", blocked_reason_summary=""), "blocked_reason_summary is missing")


def test_invalid_nested_fixture_only_completion_summary_bridge_fails_closed() -> None:
    invalid = _valid_completion_summary_bridge(operator_review_completion_summary_bridge_summary="")
    _assert_blocked_with_reason(_valid_bridge_record(fixture_only_source_provider_operator_review_completion_summary_bridge=invalid), "fixture-only source provider operator-review completion-summary bridge is invalid")


def test_invalid_supplied_integration_smoke_fails_closed() -> None:
    invalid = _valid_supplied_integration_smoke(integration_smoke_summary="")
    _assert_blocked_with_reason(_valid_bridge_record(supplied_runtime_full_chain_integration_smoke=invalid), "supplied runtime full-chain integration smoke is invalid")


@pytest.mark.parametrize(("field_name", "reason"), [("condition_id", "condition_id does not match fixture-only operator-review completion-summary bridge"), ("token_id", "token_id does not match fixture-only operator-review completion-summary bridge"), ("outcome", "outcome does not match fixture-only operator-review completion-summary bridge")])
def test_top_level_route_mismatch_with_fixture_completion_summary_bridge_fails_closed(field_name: str, reason: str) -> None:
    _assert_blocked_with_reason(_valid_bridge_record(**{field_name: "different"}), reason)


@pytest.mark.parametrize(("field_name", "reason"), [("condition_id", "condition_id does not match supplied runtime full-chain integration smoke"), ("token_id", "token_id does not match supplied runtime full-chain integration smoke"), ("outcome", "outcome does not match supplied runtime full-chain integration smoke")])
def test_top_level_route_mismatch_with_supplied_integration_smoke_fails_closed(field_name: str, reason: str) -> None:
    _assert_blocked_with_reason(_valid_bridge_record(supplied_runtime_full_chain_integration_smoke=_valid_supplied_integration_smoke(**{field_name: "different"})), reason)


def _smoke_with_summary(summary):
    return _valid_supplied_integration_smoke(condition_id="different", supplied_runtime_operator_review_completion_summary=summary)


def _summary_with_seal(seal):
    return smoke_base._valid_operator_review_completion_summary(condition_id="different", supplied_runtime_operator_review_completion_seal=seal)


def _seal_with_bundle(bundle):
    return smoke_base._valid_operator_review_completion_seal(condition_id="different", supplied_runtime_operator_review_final_bundle=bundle)


def test_parent_bridge_versus_supplied_integration_smoke_route_mismatch_fails_closed() -> None:
    _assert_blocked_with_reason(_valid_bridge_record(condition_id="different", supplied_runtime_full_chain_integration_smoke=_valid_supplied_integration_smoke(condition_id="different")), "nested fixture-only operator-review completion-summary bridge and supplied runtime full-chain integration smoke routes do not match")


def test_nested_completion_summary_mismatch_fails_closed() -> None:
    _assert_blocked_with_reason(_valid_bridge_record(condition_id="different", supplied_runtime_full_chain_integration_smoke=_smoke_with_summary(smoke_base._valid_operator_review_completion_summary(condition_id="different"))), "nested supplied runtime operator-review completion summaries do not match")


def test_nested_completion_seal_mismatch_fails_closed() -> None:
    _assert_blocked_with_reason(_valid_bridge_record(condition_id="different", supplied_runtime_full_chain_integration_smoke=_smoke_with_summary(_summary_with_seal(smoke_base._valid_operator_review_completion_seal(condition_id="different")))), "nested supplied runtime operator-review completion seals do not match")


def test_nested_final_bundle_mismatch_fails_closed() -> None:
    _assert_blocked_with_reason(_valid_bridge_record(condition_id="different", supplied_runtime_full_chain_integration_smoke=_smoke_with_summary(_summary_with_seal(_seal_with_bundle(smoke_base._valid_operator_review_final_bundle(condition_id="different"))))), "nested supplied runtime operator-review final bundles do not match")


def test_nested_final_packet_mismatch_fails_closed() -> None:
    bundle = smoke_base._valid_operator_review_final_bundle(condition_id="different", supplied_runtime_operator_review_final_packet=smoke_base._valid_operator_review_final_packet(condition_id="different"))
    _assert_blocked_with_reason(_valid_bridge_record(condition_id="different", supplied_runtime_full_chain_integration_smoke=_smoke_with_summary(_summary_with_seal(_seal_with_bundle(bundle)))), "nested supplied runtime operator-review final packets do not match")


def test_nested_queue_summary_mismatch_fails_closed() -> None:
    packet = smoke_base._valid_operator_review_final_packet(condition_id="different", supplied_runtime_operator_review_queue_summary=smoke_base._valid_operator_review_queue_summary(condition_id="different"))
    bundle = smoke_base._valid_operator_review_final_bundle(condition_id="different", supplied_runtime_operator_review_final_packet=packet)
    _assert_blocked_with_reason(_valid_bridge_record(condition_id="different", supplied_runtime_full_chain_integration_smoke=_smoke_with_summary(_summary_with_seal(_seal_with_bundle(bundle)))), "nested supplied runtime operator-review queue summaries do not match")


@pytest.mark.parametrize(("final_bundle", "reason"), [
    (bundle_base._bundle_with_packet(bundle_base._packet_with_summary(bundle_base._summary_with_entry(smoke_base._valid_operator_review_queue_entry(condition_id="different")))), "nested supplied runtime operator-review queue entries do not match"),
    (bundle_base._bundle_with_packet(bundle_base._packet_with_summary(bundle_base._summary_with_entry(bundle_base._entry_with_queue(smoke_base._valid_operator_review_queue_packet(condition_id="different"))))), "nested supplied runtime operator-review queue packets do not match"),
    (bundle_base._bundle_with_packet(bundle_base._packet_with_summary(bundle_base._summary_with_entry(bundle_base._entry_with_queue(bundle_base._queue_with_ack(smoke_base._valid_operator_review_ack_packet(condition_id="different")))))), "nested supplied runtime operator-review ack packets do not match"),
    (bundle_base._bundle_with_packet(bundle_base._packet_with_summary(bundle_base._summary_with_entry(bundle_base._entry_with_queue(bundle_base._queue_with_ack(bundle_base._ack_with_handoff(smoke_base._valid_operator_review_handoff(condition_id="different"))))))), "nested supplied runtime operator-review handoffs do not match"),
    (bundle_base._bundle_with_packet(bundle_base._packet_with_summary(bundle_base._summary_with_entry(bundle_base._entry_with_queue(bundle_base._queue_with_ack(bundle_base._ack_with_handoff(bundle_base._handoff_with_trace(smoke_base._valid_trace_packet(condition_id="different")))))))), "nested supplied runtime trace packets do not match"),
    (bundle_base._bundle_with_packet(bundle_base._packet_with_summary(bundle_base._summary_with_entry(bundle_base._entry_with_queue(bundle_base._queue_with_ack(bundle_base._ack_with_handoff(bundle_base._handoff_with_trace(bundle_base._trace_with_smoke(smoke_base._valid_end_to_end_smoke(condition_id="different"))))))))), "nested supplied runtime end-to-end smokes do not match"),
    (bundle_base._bundle_with_packet(bundle_base._packet_with_summary(bundle_base._summary_with_entry(bundle_base._entry_with_queue(bundle_base._queue_with_ack(bundle_base._ack_with_handoff(bundle_base._handoff_with_trace(bundle_base._trace_with_smoke(bundle_base._smoke_with_report(smoke_base._valid_dry_run_report(condition_id="different")))))))))), "nested supplied runtime dry-run reports do not match"),
])
def test_deeper_nested_route_mismatches_fail_closed(final_bundle, reason: str) -> None:
    _assert_blocked_with_reason(_valid_bridge_record(condition_id="different", supplied_runtime_full_chain_integration_smoke=_smoke_with_summary(_summary_with_seal(_seal_with_bundle(final_bundle)))), reason)


def test_dry_run_packet_and_validation_bundle_mismatch_fails_closed() -> None:
    validation = smoke_base._valid_bundle(condition_id="different")
    dry = smoke_base._valid_dry_run_packet(condition_id="different", supplied_runtime_validation_bundle=validation)
    report = smoke_base._valid_dry_run_report(condition_id="different", supplied_runtime_dry_run_packet=dry)
    final_bundle = bundle_base._bundle_with_packet(bundle_base._packet_with_summary(bundle_base._summary_with_entry(bundle_base._entry_with_queue(bundle_base._queue_with_ack(bundle_base._ack_with_handoff(bundle_base._handoff_with_trace(bundle_base._trace_with_smoke(bundle_base._smoke_with_report(report)))))))))
    _assert_blocked_with_reason(_valid_bridge_record(condition_id="different", supplied_runtime_full_chain_integration_smoke=_smoke_with_summary(_summary_with_seal(_seal_with_bundle(final_bundle)))), "nested supplied runtime dry-run packets do not match")


def test_evidence_packet_and_market_contract_mismatch_fails_closed() -> None:
    evidence = smoke_base._valid_evidence_packet(condition_id="different", supplied_market_contract=smoke_base._valid_contract(condition_id="different"))
    validation = smoke_base._valid_bundle(condition_id="different", supplied_evidence_packet=evidence)
    dry = smoke_base._valid_dry_run_packet(condition_id="different", supplied_runtime_validation_bundle=validation)
    report = smoke_base._valid_dry_run_report(condition_id="different", supplied_runtime_dry_run_packet=dry)
    final_bundle = bundle_base._bundle_with_packet(bundle_base._packet_with_summary(bundle_base._summary_with_entry(bundle_base._entry_with_queue(bundle_base._queue_with_ack(bundle_base._ack_with_handoff(bundle_base._handoff_with_trace(bundle_base._trace_with_smoke(bundle_base._smoke_with_report(report)))))))))
    _assert_blocked_with_reason(_valid_bridge_record(condition_id="different", supplied_runtime_full_chain_integration_smoke=_smoke_with_summary(_summary_with_seal(_seal_with_bundle(final_bundle)))), "nested supplied evidence packets do not match")


def test_all_summary_mismatches_fail_closed() -> None:
    _assert_blocked_with_reason(_valid_bridge_record(fixture_completion_summary_bridge_summary="different"), "fixture completion-summary bridge summary does not match fixture-only operator-review completion-summary bridge")
    _assert_blocked_with_reason(_valid_bridge_record(supplied_integration_smoke_summary="different"), "supplied integration smoke summary does not match supplied runtime full-chain integration smoke")
    _assert_blocked_with_reason(_valid_bridge_record(operator_review_summary="different"), "operator review summary does not match fixture-only operator-review completion-summary bridge")
    _assert_blocked_with_reason(_valid_bridge_record(operator_review_summary="different"), "operator review summary does not match supplied runtime full-chain integration smoke")


@pytest.mark.parametrize("status", [value for value in bridge.FixtureOnlyFullChainIntegrationSmokeBridgeStatus if value is not bridge.FixtureOnlyFullChainIntegrationSmokeBridgeStatus.FIXTURE_ONLY_FULL_CHAIN_INTEGRATION_SMOKE_BRIDGE_RECORDED])
def test_every_non_recorded_bridge_status_fails_closed(status) -> None:
    _assert_blocked_with_reason(_valid_bridge_record(fixture_only_full_chain_integration_smoke_bridge_status=status), f"fixture-only full-chain integration-smoke bridge status is {status.value}")


@pytest.mark.parametrize("posture", [value for value in bridge.FixtureOnlyFullChainIntegrationSmokeBridgePosture if value is not bridge.FixtureOnlyFullChainIntegrationSmokeBridgePosture.FIXTURE_ONLY_FULL_CHAIN_INTEGRATION_SMOKE_BRIDGE_IN_MEMORY_ONLY])
def test_every_non_in_memory_posture_fails_closed(posture) -> None:
    _assert_blocked_with_reason(_valid_bridge_record(fixture_only_full_chain_integration_smoke_bridge_posture=posture), f"fixture-only full-chain integration-smoke bridge posture is {posture.value}")


@pytest.mark.parametrize("alignment", [value for value in bridge.FullChainIntegrationSmokeBridgeAlignmentStatus if value is not bridge.FullChainIntegrationSmokeBridgeAlignmentStatus.FULL_CHAIN_INTEGRATION_SMOKE_BRIDGE_ALIGNED])
def test_every_non_aligned_alignment_status_fails_closed(alignment) -> None:
    _assert_blocked_with_reason(_valid_bridge_record(full_chain_integration_smoke_bridge_alignment_status=alignment), f"full-chain integration-smoke bridge alignment status is {alignment.value}")


@pytest.mark.parametrize("status", [value for value in bridge.NoLookaheadStatus if value is not bridge.NoLookaheadStatus.NO_LOOKAHEAD_RECORDED])
def test_every_non_recorded_no_lookahead_status_fails_closed(status) -> None:
    _assert_blocked_with_reason(_valid_bridge_record(no_lookahead_status=status), f"no-lookahead status is {status.value}")


@pytest.mark.parametrize("status", [value for value in bridge.OperatorReviewStatus if value is not bridge.OperatorReviewStatus.OPERATOR_REVIEW_REQUIRED])
def test_every_non_required_operator_review_status_fails_closed(status) -> None:
    _assert_blocked_with_reason(_valid_bridge_record(operator_review_status=status), f"operator review status is {status.value}")


@pytest.mark.parametrize("status", [value for value in bridge.RuntimeGateStatus if value is not bridge.RuntimeGateStatus.RUNTIME_GATE_READY])
def test_every_non_ready_runtime_gate_fails_closed(status) -> None:
    _assert_blocked_with_reason(_valid_bridge_record(runtime_gate_status=status), f"runtime gate status is {status.value}")


def _without_docstrings(path: Path) -> str:
    tree = ast.parse(path.read_bytes().decode())
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)) and node.body and isinstance(node.body[0], ast.Expr) and isinstance(getattr(node.body[0], "value", None), ast.Constant) and isinstance(node.body[0].value.value, str):
            node.body[0] = ast.Pass()
    return ast.unparse(tree)


def test_static_no_noncanonical_route_inputs() -> None:
    combined = _without_docstrings(MODULE_PATH) + _without_docstrings(TEST_PATH)
    assert "market" + "_id" not in combined
    assert "token" + "_outcome" + "_pair" not in combined


def test_static_no_side_effects() -> None:
    source = _without_docstrings(MODULE_PATH)
    terms = [
        "requests", "httpx", "url" + "lib", "aiohttp", "boto3", "polymarket", "kalshi", "duckdb", "pandas", "sub" + "process", "open(", ".read" + "_text(", ".write" + "_text(", "socket", "os.environ", "dotenv", "place" + "_order", "paper" + "_trade", "trade", "back" + "test", "score", "execute" + "_order", "submit" + "_order", "persist", "data" + "base", "post" + "gres", "redis", "export", "write", "save", "owner" + "_decision", "capture" + "_decision", "operator" + "_decision", "execute" + "_decision", "celery", "rabbitmq", "sqs", "enqueue(", "dequeue(", "publish(", "subscribe(", "scheduler", "broker", "provider" + "_client", "api" + "_call", "scrape", "download", "credentials", "production", "simulate", "simulation", "generate" + "_report", "report" + "_writer", "generate" + "_summary", "summary" + "_writer", "finalize" + "_summary", "generate" + "_packet", "packet" + "_writer", "finalize" + "_packet", "generate" + "_bundle", "bundle" + "_writer", "finalize" + "_bundle", "generate" + "_seal", "seal" + "_writer", "finalize" + "_seal", "durable" + "_seal", "workflow" + "_completion", "complete" + "_workflow", "mark" + "_complete", "generate" + "_smoke", "smoke" + "_generator", "execute" + "_smoke", "run" + "_smoke", "execute" + "_integration" + "_smoke", "run" + "_integration" + "_smoke", "integration" + "_smoke" + "_runner", "deliver" + "_integration" + "_smoke", "send" + "_integration" + "_smoke", "execute" + "_trace", "run" + "_trace", "deliver" + "_handoff", "send" + "_handoff", "deliver" + "_ack", "send" + "_ack", "deliver" + "_queue", "send" + "_queue", "deliver" + "_queue" + "_entry", "send" + "_queue" + "_entry", "deliver" + "_queue" + "_summary", "send" + "_queue" + "_summary", "deliver" + "_final" + "_packet", "send" + "_final" + "_packet", "deliver" + "_final" + "_bundle", "send" + "_final" + "_bundle", "deliver" + "_completion" + "_seal", "send" + "_completion" + "_seal", "deliver" + "_completion" + "_summary", "send" + "_completion" + "_summary", "queue" + "_service", "notification", "notify",
    ]
    assert {term for term in terms if term in source} == set()
