import ast
from dataclasses import asdict
from pathlib import Path

import pytest

from meg.weather.stage2 import fixture_only_source_provider_operator_review_completion_seal_bridge_runtime as bridge
from meg.weather.stage2 import fixture_only_source_provider_operator_review_final_bundle_bridge_runtime as bundle_bridge
from meg.weather.stage2 import supplied_runtime_operator_review_completion_seal as socs
from tests.core import test_weather_stage2_fixture_only_source_provider_operator_review_final_bundle_bridge_runtime as bundle_base
from tests.core import test_weather_supplied_runtime_operator_review_completion_seal as seal_base

MODULE_PATH = Path("meg/weather/stage2/fixture_only_source_provider_operator_review_completion_seal_bridge_runtime.py")
TEST_PATH = Path("tests/core/test_weather_stage2_fixture_only_source_provider_operator_review_completion_seal_bridge_runtime.py")


def _valid_final_bundle_bridge(**overrides: object) -> bundle_bridge.FixtureOnlySourceProviderOperatorReviewFinalBundleBridgeRecord:
    return bundle_base._valid_bridge_record(**overrides)


def _valid_completion_seal(**overrides: object) -> socs.SuppliedRuntimeOperatorReviewCompletionSealRecord:
    base = _valid_final_bundle_bridge()
    values = {
        "supplied_runtime_operator_review_final_bundle": base.supplied_runtime_operator_review_final_bundle,
        "operator_review_summary": base.operator_review_summary,
    }
    values.update(overrides)
    return seal_base._valid_operator_review_completion_seal(**values)


def _valid_bridge_record(**overrides: object) -> bridge.FixtureOnlySourceProviderOperatorReviewCompletionSealBridgeRecord:
    values = {
        "condition_id": "condition-1",
        "token_id": "token-1",
        "outcome": "Yes",
        "fixture_only_source_provider_operator_review_final_bundle_bridge": _valid_final_bundle_bridge(),
        "supplied_runtime_operator_review_completion_seal": _valid_completion_seal(),
        "operator_review_completion_seal_bridge_id": "completion-seal-bridge-1",
        "operator_review_completion_seal_bridge_summary": "Fixture-only final-bundle bridge linked to supplied completion seal.",
        "fixture_final_bundle_bridge_summary": "Fixture-only final-packet bridge linked to supplied final bundle.",
        "supplied_completion_seal_summary": "Caller supplied operator-review completion seal summary text.",
        "operator_review_summary": "Operator review remains required before any action.",
        "blocked_reason_summary": "No blocker for this valid completion-seal bridge.",
        "fixture_only_operator_review_completion_seal_bridge_status": bridge.FixtureOnlyOperatorReviewCompletionSealBridgeStatus.FIXTURE_ONLY_OPERATOR_REVIEW_COMPLETION_SEAL_BRIDGE_RECORDED,
        "fixture_only_operator_review_completion_seal_bridge_posture": bridge.FixtureOnlyOperatorReviewCompletionSealBridgePosture.FIXTURE_ONLY_OPERATOR_REVIEW_COMPLETION_SEAL_BRIDGE_IN_MEMORY_ONLY,
        "operator_review_completion_seal_bridge_alignment_status": bridge.OperatorReviewCompletionSealBridgeAlignmentStatus.OPERATOR_REVIEW_COMPLETION_SEAL_BRIDGE_ALIGNED,
        "no_lookahead_status": bridge.NoLookaheadStatus.NO_LOOKAHEAD_RECORDED,
        "operator_review_status": bridge.OperatorReviewStatus.OPERATOR_REVIEW_REQUIRED,
        "runtime_gate_status": bridge.RuntimeGateStatus.RUNTIME_GATE_READY,
    }
    values.update(overrides)
    return bridge.FixtureOnlySourceProviderOperatorReviewCompletionSealBridgeRecord(**values)


def _assert_blocked_with_reason(record, reason: str) -> None:
    result = bridge.validate_fixture_only_source_provider_operator_review_completion_seal_bridge_record(record)
    assert result.passed is False
    assert result.severity is bridge.ValidationSeverity.BLOCKED
    assert reason in result.reasons


def test_enums_are_closed_sets() -> None:
    assert bridge.FixtureOnlyOperatorReviewCompletionSealBridgeStatus.values() == frozenset({"fixture_only_operator_review_completion_seal_bridge_recorded", "fixture_only_operator_review_completion_seal_bridge_missing", "fixture_only_operator_review_completion_seal_bridge_ambiguous", "fixture_only_operator_review_completion_seal_bridge_unsupported", "fixture_only_operator_review_completion_seal_bridge_unknown"})
    assert bridge.FixtureOnlyOperatorReviewCompletionSealBridgePosture.values() == frozenset({"fixture_only_operator_review_completion_seal_bridge_in_memory_only", "fixture_only_operator_review_completion_seal_bridge_missing", "fixture_only_operator_review_completion_seal_bridge_ambiguous", "fixture_only_operator_review_completion_seal_bridge_unsupported", "fixture_only_operator_review_completion_seal_bridge_unknown"})
    assert bridge.OperatorReviewCompletionSealBridgeAlignmentStatus.values() == frozenset({"operator_review_completion_seal_bridge_aligned", "operator_review_completion_seal_bridge_mismatch", "operator_review_completion_seal_bridge_missing", "operator_review_completion_seal_bridge_ambiguous", "operator_review_completion_seal_bridge_unknown"})
    assert bridge.NoLookaheadStatus.values() == frozenset({"no_lookahead_recorded", "no_lookahead_missing", "no_lookahead_ambiguous", "no_lookahead_unknown"})
    assert bridge.OperatorReviewStatus.values() == frozenset({"operator_review_required", "operator_review_missing", "operator_review_ambiguous", "operator_review_not_required", "operator_review_unknown"})
    assert bridge.RuntimeGateStatus.values() == frozenset({"runtime_gate_ready", "runtime_gate_blocked", "runtime_gate_requires_manual_review", "runtime_gate_unknown"})
    assert bridge.ValidationSeverity.values() == frozenset({"passed", "caution", "failed", "blocked"})


def test_frozen_dataclass_construction() -> None:
    record = _valid_bridge_record(provenance_notes="caller supplied")
    assert isinstance(record.fixture_only_source_provider_operator_review_final_bundle_bridge, bundle_bridge.FixtureOnlySourceProviderOperatorReviewFinalBundleBridgeRecord)
    assert isinstance(record.supplied_runtime_operator_review_completion_seal, socs.SuppliedRuntimeOperatorReviewCompletionSealRecord)
    assert record.provenance_notes == "caller supplied"
    with pytest.raises(Exception):
        record.condition_id = "changed"


def test_mapping_construction_coerces_string_enums_and_nested_mappings() -> None:
    record = bridge.fixture_only_source_provider_operator_review_completion_seal_bridge_record_from_mapping(asdict(_valid_bridge_record()))
    assert isinstance(record.fixture_only_source_provider_operator_review_final_bundle_bridge, bundle_bridge.FixtureOnlySourceProviderOperatorReviewFinalBundleBridgeRecord)
    assert isinstance(record.supplied_runtime_operator_review_completion_seal, socs.SuppliedRuntimeOperatorReviewCompletionSealRecord)
    assert record.fixture_only_operator_review_completion_seal_bridge_status is bridge.FixtureOnlyOperatorReviewCompletionSealBridgeStatus.FIXTURE_ONLY_OPERATOR_REVIEW_COMPLETION_SEAL_BRIDGE_RECORDED
    assert record.provenance_notes == ""


def test_valid_record_passes() -> None:
    result = bridge.validate_fixture_only_source_provider_operator_review_completion_seal_bridge_record(_valid_bridge_record())
    assert result.passed is True
    assert result.severity is bridge.ValidationSeverity.PASSED
    assert result.reasons == ()


@pytest.mark.parametrize("field_name", ["condition_id", "token_id", "outcome", "operator_review_completion_seal_bridge_id", "operator_review_completion_seal_bridge_summary", "fixture_final_bundle_bridge_summary", "supplied_completion_seal_summary", "operator_review_summary"])
def test_blank_required_text_fields_fail_closed(field_name: str) -> None:
    _assert_blocked_with_reason(_valid_bridge_record(**{field_name: "  "}), f"{field_name} is missing")


def test_blank_blocked_reason_summary_is_allowed_when_otherwise_valid() -> None:
    assert bridge.validate_fixture_only_source_provider_operator_review_completion_seal_bridge_record(_valid_bridge_record(blocked_reason_summary="")).passed is True


def test_blank_blocked_reason_summary_is_required_when_another_failure_exists() -> None:
    _assert_blocked_with_reason(_valid_bridge_record(condition_id="wrong", blocked_reason_summary=""), "blocked_reason_summary is missing")


def test_invalid_nested_records_fail_closed() -> None:
    _assert_blocked_with_reason(_valid_bridge_record(fixture_only_source_provider_operator_review_final_bundle_bridge=_valid_final_bundle_bridge(operator_review_final_bundle_bridge_summary="")), "fixture-only source provider operator-review final-bundle bridge is invalid")
    _assert_blocked_with_reason(_valid_bridge_record(supplied_runtime_operator_review_completion_seal=_valid_completion_seal(completion_seal_summary="")), "supplied runtime operator-review completion seal is invalid")


@pytest.mark.parametrize(("field_name", "reason"), [("condition_id", "condition_id does not match fixture-only operator-review final-bundle bridge"), ("token_id", "token_id does not match fixture-only operator-review final-bundle bridge"), ("outcome", "outcome does not match fixture-only operator-review final-bundle bridge")])
def test_top_level_route_mismatch_with_fixture_final_bundle_bridge_fails_closed(field_name: str, reason: str) -> None:
    _assert_blocked_with_reason(_valid_bridge_record(**{field_name: "different"}), reason)


@pytest.mark.parametrize(("field_name", "reason"), [("condition_id", "condition_id does not match supplied runtime operator-review completion seal"), ("token_id", "token_id does not match supplied runtime operator-review completion seal"), ("outcome", "outcome does not match supplied runtime operator-review completion seal")])
def test_top_level_route_mismatch_with_supplied_completion_seal_fails_closed(field_name: str, reason: str) -> None:
    _assert_blocked_with_reason(_valid_bridge_record(supplied_runtime_operator_review_completion_seal=_valid_completion_seal(**{field_name: "different"})), reason)


def test_fixture_final_bundle_bridge_versus_supplied_completion_seal_route_mismatch_fails_closed() -> None:
    _assert_blocked_with_reason(_valid_bridge_record(condition_id="different", supplied_runtime_operator_review_completion_seal=_valid_completion_seal(condition_id="different")), "nested fixture-only operator-review final-bundle bridge and supplied runtime operator-review completion seal routes do not match")


def test_nested_route_mismatches_fail_closed() -> None:
    other_bundle = seal_base._valid_operator_review_final_bundle(condition_id="different")
    seal = _valid_completion_seal(condition_id="different", supplied_runtime_operator_review_final_bundle=other_bundle)
    _assert_blocked_with_reason(_valid_bridge_record(condition_id="different", supplied_runtime_operator_review_completion_seal=seal), "nested supplied runtime operator-review final bundles do not match")
    other_packet = seal_base._valid_operator_review_final_packet(condition_id="different")
    seal = _valid_completion_seal(condition_id="different", supplied_runtime_operator_review_final_bundle=seal_base._valid_operator_review_final_bundle(condition_id="different", supplied_runtime_operator_review_final_packet=other_packet))
    _assert_blocked_with_reason(_valid_bridge_record(condition_id="different", supplied_runtime_operator_review_completion_seal=seal), "nested supplied runtime operator-review final packets do not match")
    summary = seal_base._valid_operator_review_queue_summary(condition_id="different")
    packet = seal_base._valid_operator_review_final_packet(condition_id="different", supplied_runtime_operator_review_queue_summary=summary)
    seal = _valid_completion_seal(condition_id="different", supplied_runtime_operator_review_final_bundle=seal_base._valid_operator_review_final_bundle(condition_id="different", supplied_runtime_operator_review_final_packet=packet))
    _assert_blocked_with_reason(_valid_bridge_record(condition_id="different", supplied_runtime_operator_review_completion_seal=seal), "nested supplied runtime operator-review queue summaries do not match")


def test_deeper_nested_route_mismatches_fail_closed() -> None:
    cases = [
        (
            bundle_base._bundle_with_packet(bundle_base._packet_with_summary(bundle_base._summary_with_entry(seal_base._valid_operator_review_queue_entry(condition_id="different")))),
            "nested supplied runtime operator-review queue entries do not match",
        ),
        (
            bundle_base._bundle_with_packet(bundle_base._packet_with_summary(bundle_base._summary_with_entry(bundle_base._entry_with_queue(seal_base._valid_operator_review_queue_packet(condition_id="different"))))),
            "nested supplied runtime operator-review queue packets do not match",
        ),
        (
            bundle_base._bundle_with_packet(bundle_base._packet_with_summary(bundle_base._summary_with_entry(bundle_base._entry_with_queue(bundle_base._queue_with_ack(seal_base._valid_operator_review_ack_packet(condition_id="different")))))),
            "nested supplied runtime operator-review ack packets do not match",
        ),
        (
            bundle_base._bundle_with_packet(bundle_base._packet_with_summary(bundle_base._summary_with_entry(bundle_base._entry_with_queue(bundle_base._queue_with_ack(bundle_base._ack_with_handoff(seal_base._valid_operator_review_handoff(condition_id="different"))))))),
            "nested supplied runtime operator-review handoffs do not match",
        ),
        (
            bundle_base._bundle_with_packet(bundle_base._packet_with_summary(bundle_base._summary_with_entry(bundle_base._entry_with_queue(bundle_base._queue_with_ack(bundle_base._ack_with_handoff(bundle_base._handoff_with_trace(seal_base._valid_trace_packet(condition_id="different")))))))),
            "nested supplied runtime trace packets do not match",
        ),
        (
            bundle_base._bundle_with_packet(bundle_base._packet_with_summary(bundle_base._summary_with_entry(bundle_base._entry_with_queue(bundle_base._queue_with_ack(bundle_base._ack_with_handoff(bundle_base._handoff_with_trace(bundle_base._trace_with_smoke(seal_base._valid_end_to_end_smoke(condition_id="different"))))))))),
            "nested supplied runtime end-to-end smokes do not match",
        ),
        (
            bundle_base._bundle_with_packet(bundle_base._packet_with_summary(bundle_base._summary_with_entry(bundle_base._entry_with_queue(bundle_base._queue_with_ack(bundle_base._ack_with_handoff(bundle_base._handoff_with_trace(bundle_base._trace_with_smoke(bundle_base._smoke_with_report(seal_base._valid_dry_run_report(condition_id="different")))))))))),
            "nested supplied runtime dry-run reports do not match",
        ),
    ]
    for final_bundle, reason in cases:
        seal = _valid_completion_seal(condition_id="different", supplied_runtime_operator_review_final_bundle=final_bundle)
        _assert_blocked_with_reason(_valid_bridge_record(condition_id="different", supplied_runtime_operator_review_completion_seal=seal), reason)

def test_dry_validation_evidence_route_mismatches_fail_closed() -> None:
    validation = seal_base._valid_bundle(condition_id="different")
    dry = seal_base._valid_dry_run_packet(condition_id="different", supplied_runtime_validation_bundle=validation)
    report = seal_base._valid_dry_run_report(condition_id="different", supplied_runtime_dry_run_packet=dry)
    smoke = seal_base._valid_end_to_end_smoke(condition_id="different", supplied_runtime_dry_run_report=report)
    trace = seal_base._valid_trace_packet(condition_id="different", supplied_runtime_end_to_end_smoke=smoke)
    handoff = seal_base._valid_operator_review_handoff(condition_id="different", supplied_runtime_trace_packet=trace)
    ack = seal_base._valid_operator_review_ack_packet(condition_id="different", supplied_runtime_operator_review_handoff=handoff)
    queue = seal_base._valid_operator_review_queue_packet(condition_id="different", supplied_runtime_operator_review_ack_packet=ack)
    entry = seal_base._valid_operator_review_queue_entry(condition_id="different", supplied_runtime_operator_review_queue_packet=queue)
    summary = seal_base._valid_operator_review_queue_summary(condition_id="different", supplied_runtime_operator_review_queue_entry=entry)
    packet = seal_base._valid_operator_review_final_packet(condition_id="different", supplied_runtime_operator_review_queue_summary=summary)
    seal = _valid_completion_seal(condition_id="different", supplied_runtime_operator_review_final_bundle=seal_base._valid_operator_review_final_bundle(condition_id="different", supplied_runtime_operator_review_final_packet=packet))
    _assert_blocked_with_reason(_valid_bridge_record(condition_id="different", supplied_runtime_operator_review_completion_seal=seal), "nested supplied runtime dry-run packets do not match")
    evidence = seal_base._valid_evidence_packet(condition_id="different", supplied_market_contract=seal_base._valid_contract(condition_id="different"))
    validation = seal_base._valid_bundle(condition_id="different", supplied_evidence_packet=evidence)
    dry = seal_base._valid_dry_run_packet(condition_id="different", supplied_runtime_validation_bundle=validation)
    report = seal_base._valid_dry_run_report(condition_id="different", supplied_runtime_dry_run_packet=dry)
    smoke = seal_base._valid_end_to_end_smoke(condition_id="different", supplied_runtime_dry_run_report=report)
    trace = seal_base._valid_trace_packet(condition_id="different", supplied_runtime_end_to_end_smoke=smoke)
    handoff = seal_base._valid_operator_review_handoff(condition_id="different", supplied_runtime_trace_packet=trace)
    ack = seal_base._valid_operator_review_ack_packet(condition_id="different", supplied_runtime_operator_review_handoff=handoff)
    queue = seal_base._valid_operator_review_queue_packet(condition_id="different", supplied_runtime_operator_review_ack_packet=ack)
    entry = seal_base._valid_operator_review_queue_entry(condition_id="different", supplied_runtime_operator_review_queue_packet=queue)
    summary = seal_base._valid_operator_review_queue_summary(condition_id="different", supplied_runtime_operator_review_queue_entry=entry)
    packet = seal_base._valid_operator_review_final_packet(condition_id="different", supplied_runtime_operator_review_queue_summary=summary)
    seal = _valid_completion_seal(condition_id="different", supplied_runtime_operator_review_final_bundle=seal_base._valid_operator_review_final_bundle(condition_id="different", supplied_runtime_operator_review_final_packet=packet))
    _assert_blocked_with_reason(_valid_bridge_record(condition_id="different", supplied_runtime_operator_review_completion_seal=seal), "nested supplied evidence packets do not match")


def test_summary_alignment_failures() -> None:
    _assert_blocked_with_reason(_valid_bridge_record(fixture_final_bundle_bridge_summary="different"), "fixture final-bundle bridge summary does not match fixture-only operator-review final-bundle bridge")
    _assert_blocked_with_reason(_valid_bridge_record(supplied_completion_seal_summary="different"), "supplied completion seal summary does not match supplied runtime operator-review completion seal")


def test_operator_review_summary_mismatch_against_each_nested_record_fails_closed() -> None:
    _assert_blocked_with_reason(_valid_bridge_record(operator_review_summary="different"), "operator review summary does not match supplied runtime operator-review completion seal")
    _assert_blocked_with_reason(_valid_bridge_record(operator_review_summary="different"), "operator review summary does not match fixture-only operator-review final-bundle bridge")


@pytest.mark.parametrize("status", [value for value in bridge.FixtureOnlyOperatorReviewCompletionSealBridgeStatus if value is not bridge.FixtureOnlyOperatorReviewCompletionSealBridgeStatus.FIXTURE_ONLY_OPERATOR_REVIEW_COMPLETION_SEAL_BRIDGE_RECORDED])
def test_every_non_recorded_bridge_status_fails_closed(status) -> None:
    _assert_blocked_with_reason(_valid_bridge_record(fixture_only_operator_review_completion_seal_bridge_status=status), f"fixture-only operator-review completion-seal bridge status is {status.value}")


@pytest.mark.parametrize("posture", [value for value in bridge.FixtureOnlyOperatorReviewCompletionSealBridgePosture if value is not bridge.FixtureOnlyOperatorReviewCompletionSealBridgePosture.FIXTURE_ONLY_OPERATOR_REVIEW_COMPLETION_SEAL_BRIDGE_IN_MEMORY_ONLY])
def test_every_non_in_memory_posture_fails_closed(posture) -> None:
    _assert_blocked_with_reason(_valid_bridge_record(fixture_only_operator_review_completion_seal_bridge_posture=posture), f"fixture-only operator-review completion-seal bridge posture is {posture.value}")


@pytest.mark.parametrize("alignment", [value for value in bridge.OperatorReviewCompletionSealBridgeAlignmentStatus if value is not bridge.OperatorReviewCompletionSealBridgeAlignmentStatus.OPERATOR_REVIEW_COMPLETION_SEAL_BRIDGE_ALIGNED])
def test_every_non_aligned_alignment_status_fails_closed(alignment) -> None:
    _assert_blocked_with_reason(_valid_bridge_record(operator_review_completion_seal_bridge_alignment_status=alignment), f"operator-review completion-seal bridge alignment status is {alignment.value}")


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
        "requests", "httpx", "url" + "lib", "aiohttp", "boto3", "polymarket", "kalshi", "duckdb", "pandas", "sub" + "process", "open(", ".read" + "_text(", ".write" + "_text(", "socket", "os.environ", "dotenv", "place" + "_order", "paper" + "_trade", "trade", "back" + "test", "score", "execute" + "_order", "submit" + "_order", "persist", "data" + "base", "post" + "gres", "redis", "export", "write", "save", "owner" + "_decision", "capture" + "_decision", "operator" + "_decision", "execute" + "_decision", "celery", "rabbitmq", "sqs", "enqueue(", "dequeue(", "publish(", "subscribe(", "scheduler", "broker", "provider" + "_client", "api" + "_call", "scrape", "download", "credentials", "production", "simulate", "simulation", "generate" + "_report", "report" + "_writer", "generate" + "_summary", "summary" + "_writer", "generate" + "_packet", "packet" + "_writer", "finalize" + "_packet", "generate" + "_bundle", "bundle" + "_writer", "finalize" + "_bundle", "generate" + "_seal", "seal" + "_writer", "finalize" + "_seal", "durable" + "_seal", "workflow" + "_completion", "complete" + "_workflow", "mark" + "_complete", "execute" + "_smoke", "run" + "_smoke", "execute" + "_trace", "run" + "_trace", "deliver" + "_handoff", "send" + "_handoff", "deliver" + "_ack", "send" + "_ack", "deliver" + "_queue", "send" + "_queue", "deliver" + "_queue" + "_entry", "send" + "_queue" + "_entry", "deliver" + "_queue" + "_summary", "send" + "_queue" + "_summary", "deliver" + "_final" + "_packet", "send" + "_final" + "_packet", "deliver" + "_final" + "_bundle", "send" + "_final" + "_bundle", "deliver" + "_completion" + "_seal", "send" + "_completion" + "_seal", "queue" + "_service", "notification", "notify",
    ]
    assert {term for term in terms if term in source} == set()
