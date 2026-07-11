import ast
from dataclasses import asdict
from pathlib import Path

import pytest

from meg.weather.stage2 import fixture_only_source_provider_operator_review_queue_entry_bridge_runtime as bridge
from meg.weather.stage2 import fixture_only_source_provider_operator_review_queue_bridge_runtime as queue_bridge
from meg.weather.stage2 import supplied_runtime_operator_review_queue_entry as soqe
from meg.weather.stage2 import supplied_runtime_operator_review_queue_packet as soqp
from meg.weather.stage2 import supplied_runtime_operator_review_ack_packet as soap
from meg.weather.stage2 import supplied_runtime_operator_review_handoff as sroh
from meg.weather.stage2 import supplied_runtime_trace_packet as srtp
from meg.weather.stage2 import supplied_runtime_end_to_end_smoke as sees
from meg.weather.stage2 import supplied_runtime_dry_run_report as srdr
from meg.weather.stage2 import supplied_runtime_dry_run_packet as srdp
from meg.weather.stage2 import supplied_runtime_validation_bundle as srvb
from meg.weather.stage2 import supplied_evidence_packet_runtime as sepr
from meg.weather.stage2 import supplied_market_contract_runtime as smcr
from tests.core import test_weather_stage2_fixture_only_source_provider_operator_review_queue_bridge_runtime as qb_base
from tests.core import test_weather_supplied_runtime_operator_review_queue_entry as entry_base

MODULE_PATH = Path("meg/weather/stage2/fixture_only_source_provider_operator_review_queue_entry_bridge_runtime.py")
TEST_PATH = Path("tests/core/test_weather_stage2_fixture_only_source_provider_operator_review_queue_entry_bridge_runtime.py")


def _valid_fixture_queue_bridge(**overrides: object) -> queue_bridge.FixtureOnlySourceProviderOperatorReviewQueueBridgeRecord:
    return qb_base._valid_bridge_record(**overrides)


def _valid_supplied_queue_entry(**overrides: object) -> soqe.SuppliedRuntimeOperatorReviewQueueEntryRecord:
    values = {
        "condition_id": "condition-1",
        "token_id": "token-1",
        "outcome": "Yes",
        "supplied_runtime_operator_review_queue_packet": qb_base._valid_supplied_runtime_operator_review_queue_packet(),
        "queue_entry_id": "queue-entry-1",
        "queue_entry_summary": "Caller supplied queue entry summary text.",
        "operator_review_summary": "Operator review remains required before any action.",
        "blocked_reason_summary": "No blocker for this valid queue entry.",
        "operator_review_queue_entry_status": soqe.OperatorReviewQueueEntryStatus.OPERATOR_REVIEW_QUEUE_ENTRY_RECORDED,
        "operator_review_queue_entry_completeness_status": soqe.OperatorReviewQueueEntryCompletenessStatus.OPERATOR_REVIEW_QUEUE_ENTRY_COMPLETE,
        "operator_review_queue_entry_posture": soqe.OperatorReviewQueueEntryPosture.OPERATOR_REVIEW_QUEUE_ENTRY_IN_MEMORY_ONLY,
        "operator_review_status": soqe.OperatorReviewStatus.OPERATOR_REVIEW_REQUIRED,
        "runtime_gate_status": soqe.RuntimeGateStatus.RUNTIME_GATE_READY,
    }
    values.update(overrides)
    return soqe.SuppliedRuntimeOperatorReviewQueueEntryRecord(**values)


def _valid_bridge_record(**overrides: object) -> bridge.FixtureOnlySourceProviderOperatorReviewQueueEntryBridgeRecord:
    values = {
        "condition_id": "condition-1",
        "token_id": "token-1",
        "outcome": "Yes",
        "fixture_only_source_provider_operator_review_queue_bridge": _valid_fixture_queue_bridge(),
        "supplied_runtime_operator_review_queue_entry": _valid_supplied_queue_entry(),
        "operator_review_queue_entry_bridge_id": "queue-entry-bridge-1",
        "operator_review_queue_entry_bridge_summary": "Fixture-only queue bridge linked to supplied queue entry.",
        "fixture_queue_bridge_summary": "Fixture-only ack bridge linked to supplied queue packet.",
        "supplied_queue_entry_summary": "Caller supplied queue entry summary text.",
        "operator_review_summary": "Operator review remains required before any action.",
        "blocked_reason_summary": "No blocker for this valid queue-entry bridge.",
        "fixture_only_operator_review_queue_entry_bridge_status": bridge.FixtureOnlyOperatorReviewQueueEntryBridgeStatus.FIXTURE_ONLY_OPERATOR_REVIEW_QUEUE_ENTRY_BRIDGE_RECORDED,
        "fixture_only_operator_review_queue_entry_bridge_posture": bridge.FixtureOnlyOperatorReviewQueueEntryBridgePosture.FIXTURE_ONLY_OPERATOR_REVIEW_QUEUE_ENTRY_BRIDGE_IN_MEMORY_ONLY,
        "operator_review_queue_entry_bridge_alignment_status": bridge.OperatorReviewQueueEntryBridgeAlignmentStatus.OPERATOR_REVIEW_QUEUE_ENTRY_BRIDGE_ALIGNED,
        "no_lookahead_status": bridge.NoLookaheadStatus.NO_LOOKAHEAD_RECORDED,
        "operator_review_status": bridge.OperatorReviewStatus.OPERATOR_REVIEW_REQUIRED,
        "runtime_gate_status": bridge.RuntimeGateStatus.RUNTIME_GATE_READY,
    }
    values.update(overrides)
    return bridge.FixtureOnlySourceProviderOperatorReviewQueueEntryBridgeRecord(**values)


def _assert_blocked_with_reason(record, reason: str) -> None:
    result = bridge.validate_fixture_only_source_provider_operator_review_queue_entry_bridge_record(record)
    assert result.passed is False
    assert result.severity is bridge.ValidationSeverity.BLOCKED
    assert reason in result.reasons


def _entry_with_packet(packet: soqp.SuppliedRuntimeOperatorReviewQueuePacketRecord, **overrides: object):
    values = {"condition_id": packet.condition_id, "token_id": packet.token_id, "outcome": packet.outcome, "supplied_runtime_operator_review_queue_packet": packet}
    values.update(overrides)
    return _valid_supplied_queue_entry(**values)


def _queue_packet_with_ack(ack: soap.SuppliedRuntimeOperatorReviewAckPacketRecord):
    return qb_base._valid_supplied_runtime_operator_review_queue_packet(condition_id=ack.condition_id, token_id=ack.token_id, outcome=ack.outcome, supplied_runtime_operator_review_ack_packet=ack)


def test_enums_are_closed_sets() -> None:
    assert bridge.FixtureOnlyOperatorReviewQueueEntryBridgeStatus.values() == frozenset({"fixture_only_operator_review_queue_entry_bridge_recorded", "fixture_only_operator_review_queue_entry_bridge_missing", "fixture_only_operator_review_queue_entry_bridge_ambiguous", "fixture_only_operator_review_queue_entry_bridge_unsupported", "fixture_only_operator_review_queue_entry_bridge_unknown"})
    assert bridge.FixtureOnlyOperatorReviewQueueEntryBridgePosture.values() == frozenset({"fixture_only_operator_review_queue_entry_bridge_in_memory_only", "fixture_only_operator_review_queue_entry_bridge_missing", "fixture_only_operator_review_queue_entry_bridge_ambiguous", "fixture_only_operator_review_queue_entry_bridge_unsupported", "fixture_only_operator_review_queue_entry_bridge_unknown"})
    assert bridge.OperatorReviewQueueEntryBridgeAlignmentStatus.values() == frozenset({"operator_review_queue_entry_bridge_aligned", "operator_review_queue_entry_bridge_mismatch", "operator_review_queue_entry_bridge_missing", "operator_review_queue_entry_bridge_ambiguous", "operator_review_queue_entry_bridge_unknown"})
    assert bridge.NoLookaheadStatus.values() == frozenset({"no_lookahead_recorded", "no_lookahead_missing", "no_lookahead_ambiguous", "no_lookahead_unknown"})
    assert bridge.OperatorReviewStatus.values() == frozenset({"operator_review_required", "operator_review_missing", "operator_review_ambiguous", "operator_review_not_required", "operator_review_unknown"})
    assert bridge.RuntimeGateStatus.values() == frozenset({"runtime_gate_ready", "runtime_gate_blocked", "runtime_gate_requires_manual_review", "runtime_gate_unknown"})
    assert bridge.ValidationSeverity.values() == frozenset({"passed", "caution", "failed", "blocked"})


def test_dataclass_construction() -> None:
    record = _valid_bridge_record(provenance_notes="caller supplied")
    assert record.condition_id == "condition-1"
    assert isinstance(record.fixture_only_source_provider_operator_review_queue_bridge, queue_bridge.FixtureOnlySourceProviderOperatorReviewQueueBridgeRecord)
    assert isinstance(record.supplied_runtime_operator_review_queue_entry, soqe.SuppliedRuntimeOperatorReviewQueueEntryRecord)
    assert record.provenance_notes == "caller supplied"


def test_mapping_construction_coerces_string_enums_and_nested_mappings() -> None:
    record = bridge.fixture_only_source_provider_operator_review_queue_entry_bridge_record_from_mapping(asdict(_valid_bridge_record()))
    assert isinstance(record.fixture_only_source_provider_operator_review_queue_bridge, queue_bridge.FixtureOnlySourceProviderOperatorReviewQueueBridgeRecord)
    assert isinstance(record.supplied_runtime_operator_review_queue_entry, soqe.SuppliedRuntimeOperatorReviewQueueEntryRecord)
    assert record.fixture_only_operator_review_queue_entry_bridge_status is bridge.FixtureOnlyOperatorReviewQueueEntryBridgeStatus.FIXTURE_ONLY_OPERATOR_REVIEW_QUEUE_ENTRY_BRIDGE_RECORDED
    assert record.provenance_notes == ""


def test_valid_record_passes() -> None:
    result = bridge.validate_fixture_only_source_provider_operator_review_queue_entry_bridge_record(_valid_bridge_record())
    assert result.passed is True
    assert result.severity is bridge.ValidationSeverity.PASSED
    assert result.reasons == ()


@pytest.mark.parametrize("field_name", ["condition_id", "token_id", "outcome", "operator_review_queue_entry_bridge_id", "operator_review_queue_entry_bridge_summary", "fixture_queue_bridge_summary", "supplied_queue_entry_summary", "operator_review_summary"])
def test_blank_required_text_fields_fail_closed(field_name: str) -> None:
    _assert_blocked_with_reason(_valid_bridge_record(**{field_name: "  "}), f"{field_name} is missing")


def test_blank_blocked_reason_summary_is_allowed_when_otherwise_valid() -> None:
    assert bridge.validate_fixture_only_source_provider_operator_review_queue_entry_bridge_record(_valid_bridge_record(blocked_reason_summary="")).passed is True


def test_blank_blocked_reason_summary_fails_when_another_validation_failure_exists() -> None:
    _assert_blocked_with_reason(_valid_bridge_record(condition_id="wrong", blocked_reason_summary=""), "blocked_reason_summary is missing")


def test_invalid_nested_fixture_queue_bridge_fails_closed() -> None:
    _assert_blocked_with_reason(_valid_bridge_record(fixture_only_source_provider_operator_review_queue_bridge=_valid_fixture_queue_bridge(operator_review_queue_bridge_summary="")), "fixture-only source provider operator-review queue bridge is invalid")


def test_invalid_nested_supplied_queue_entry_fails_closed() -> None:
    _assert_blocked_with_reason(_valid_bridge_record(supplied_runtime_operator_review_queue_entry=_valid_supplied_queue_entry(queue_entry_summary="")), "supplied runtime operator-review queue entry is invalid")


@pytest.mark.parametrize(("field_name", "reason"), [("condition_id", "condition_id does not match fixture-only operator-review queue bridge"), ("token_id", "token_id does not match fixture-only operator-review queue bridge"), ("outcome", "outcome does not match fixture-only operator-review queue bridge")])
def test_top_level_route_mismatch_with_fixture_queue_bridge_fails_closed(field_name: str, reason: str) -> None:
    _assert_blocked_with_reason(_valid_bridge_record(**{field_name: "different"}), reason)


@pytest.mark.parametrize(("field_name", "reason"), [("condition_id", "condition_id does not match supplied runtime operator-review queue entry"), ("token_id", "token_id does not match supplied runtime operator-review queue entry"), ("outcome", "outcome does not match supplied runtime operator-review queue entry")])
def test_top_level_route_mismatch_with_supplied_queue_entry_fails_closed(field_name: str, reason: str) -> None:
    entry = _valid_supplied_queue_entry(**{field_name: "different"})
    _assert_blocked_with_reason(_valid_bridge_record(supplied_runtime_operator_review_queue_entry=entry), reason)


def test_nested_fixture_queue_bridge_and_supplied_queue_entry_route_mismatch_fails_closed() -> None:
    entry = _valid_supplied_queue_entry(condition_id="different")
    record = _valid_bridge_record(condition_id="different", supplied_runtime_operator_review_queue_entry=entry)
    _assert_blocked_with_reason(record, "nested fixture-only operator-review queue bridge and supplied runtime operator-review queue entry routes do not match")


def test_nested_supplied_runtime_operator_review_queue_packet_mismatch_fails_closed() -> None:
    packet = qb_base._valid_supplied_runtime_operator_review_queue_packet(condition_id="different")
    entry = _entry_with_packet(packet)
    record = _valid_bridge_record(condition_id="different", supplied_runtime_operator_review_queue_entry=entry)
    _assert_blocked_with_reason(record, "nested supplied runtime operator-review queue packets do not match")


def test_nested_ack_packet_mismatch_fails_closed() -> None:
    ack = qb_base._valid_supplied_runtime_operator_review_ack_packet(condition_id="different")
    packet = _queue_packet_with_ack(ack)
    entry = _entry_with_packet(packet)
    record = _valid_bridge_record(condition_id="different", supplied_runtime_operator_review_queue_entry=entry)
    _assert_blocked_with_reason(record, "nested supplied runtime operator-review ack packets do not match")


def test_nested_handoff_mismatch_fails_closed() -> None:
    handoff = qb_base._valid_supplied_runtime_operator_review_handoff(condition_id="different")
    ack = qb_base._valid_supplied_runtime_operator_review_ack_packet(condition_id="different", supplied_runtime_operator_review_handoff=handoff)
    entry = _entry_with_packet(_queue_packet_with_ack(ack))
    record = _valid_bridge_record(condition_id="different", supplied_runtime_operator_review_queue_entry=entry)
    _assert_blocked_with_reason(record, "nested supplied runtime operator-review handoffs do not match")


def test_nested_trace_mismatch_fails_closed() -> None:
    trace = qb_base._valid_supplied_runtime_trace_packet(condition_id="different")
    handoff = qb_base._valid_supplied_runtime_operator_review_handoff(condition_id="different", supplied_runtime_trace_packet=trace)
    ack = qb_base._valid_supplied_runtime_operator_review_ack_packet(condition_id="different", supplied_runtime_operator_review_handoff=handoff)
    entry = _entry_with_packet(_queue_packet_with_ack(ack))
    record = _valid_bridge_record(condition_id="different", supplied_runtime_operator_review_queue_entry=entry)
    _assert_blocked_with_reason(record, "nested supplied runtime trace packets do not match")


def test_nested_end_to_end_smoke_mismatch_fails_closed() -> None:
    smoke = qb_base._valid_supplied_runtime_end_to_end_smoke(condition_id="different")
    trace = qb_base._valid_supplied_runtime_trace_packet(condition_id="different", supplied_runtime_end_to_end_smoke=smoke)
    handoff = qb_base._valid_supplied_runtime_operator_review_handoff(condition_id="different", supplied_runtime_trace_packet=trace)
    ack = qb_base._valid_supplied_runtime_operator_review_ack_packet(condition_id="different", supplied_runtime_operator_review_handoff=handoff)
    entry = _entry_with_packet(_queue_packet_with_ack(ack))
    record = _valid_bridge_record(condition_id="different", supplied_runtime_operator_review_queue_entry=entry)
    _assert_blocked_with_reason(record, "nested supplied runtime end-to-end smokes do not match")


def test_nested_dry_run_report_mismatch_fails_closed() -> None:
    report = qb_base._valid_supplied_runtime_dry_run_report(condition_id="different")
    smoke = qb_base._valid_supplied_runtime_end_to_end_smoke(condition_id="different", supplied_runtime_dry_run_report=report)
    trace = qb_base._valid_supplied_runtime_trace_packet(condition_id="different", supplied_runtime_end_to_end_smoke=smoke)
    handoff = qb_base._valid_supplied_runtime_operator_review_handoff(condition_id="different", supplied_runtime_trace_packet=trace)
    ack = qb_base._valid_supplied_runtime_operator_review_ack_packet(condition_id="different", supplied_runtime_operator_review_handoff=handoff)
    entry = _entry_with_packet(_queue_packet_with_ack(ack))
    record = _valid_bridge_record(condition_id="different", supplied_runtime_operator_review_queue_entry=entry)
    _assert_blocked_with_reason(record, "nested supplied runtime dry-run reports do not match")


def test_nested_dry_run_packet_mismatch_fails_closed() -> None:
    dry = qb_base._valid_supplied_runtime_dry_run_packet(condition_id="different")
    report = qb_base._valid_supplied_runtime_dry_run_report(condition_id="different", supplied_runtime_dry_run_packet=dry)
    smoke = qb_base._valid_supplied_runtime_end_to_end_smoke(condition_id="different", supplied_runtime_dry_run_report=report)
    trace = qb_base._valid_supplied_runtime_trace_packet(condition_id="different", supplied_runtime_end_to_end_smoke=smoke)
    handoff = qb_base._valid_supplied_runtime_operator_review_handoff(condition_id="different", supplied_runtime_trace_packet=trace)
    ack = qb_base._valid_supplied_runtime_operator_review_ack_packet(condition_id="different", supplied_runtime_operator_review_handoff=handoff)
    entry = _entry_with_packet(_queue_packet_with_ack(ack))
    record = _valid_bridge_record(condition_id="different", supplied_runtime_operator_review_queue_entry=entry)
    _assert_blocked_with_reason(record, "nested supplied runtime dry-run packets do not match")


def test_nested_evidence_packet_contract_mismatch_fails_closed() -> None:
    contract = entry_base._valid_contract(condition_id="different")
    evidence = entry_base._valid_evidence_packet(condition_id="different", supplied_market_contract=contract)
    bundle = entry_base._valid_bundle(condition_id="different", supplied_market_contract=contract, supplied_evidence_packet=evidence)
    dry = qb_base._valid_supplied_runtime_dry_run_packet(condition_id="different", supplied_runtime_validation_bundle=bundle)
    report = qb_base._valid_supplied_runtime_dry_run_report(condition_id="different", supplied_runtime_dry_run_packet=dry)
    smoke = qb_base._valid_supplied_runtime_end_to_end_smoke(condition_id="different", supplied_runtime_dry_run_report=report)
    trace = qb_base._valid_supplied_runtime_trace_packet(condition_id="different", supplied_runtime_end_to_end_smoke=smoke)
    handoff = qb_base._valid_supplied_runtime_operator_review_handoff(condition_id="different", supplied_runtime_trace_packet=trace)
    ack = qb_base._valid_supplied_runtime_operator_review_ack_packet(condition_id="different", supplied_runtime_operator_review_handoff=handoff)
    entry = _entry_with_packet(_queue_packet_with_ack(ack))
    record = _valid_bridge_record(condition_id="different", supplied_runtime_operator_review_queue_entry=entry)
    _assert_blocked_with_reason(record, "nested supplied evidence packets do not match")


@pytest.mark.parametrize(("field_name", "value", "reason"), [("fixture_queue_bridge_summary", "different", "fixture queue bridge summary does not match fixture-only operator-review queue bridge"), ("supplied_queue_entry_summary", "different", "supplied queue entry summary does not match supplied runtime operator-review queue entry")])
def test_summary_mismatches_fail_closed(field_name: str, value: str, reason: str) -> None:
    _assert_blocked_with_reason(_valid_bridge_record(**{field_name: value}), reason)


def test_operator_review_summary_mismatch_with_supplied_queue_entry_fails_closed() -> None:
    entry = _valid_supplied_queue_entry(operator_review_summary="different")
    _assert_blocked_with_reason(_valid_bridge_record(supplied_runtime_operator_review_queue_entry=entry), "operator review summary does not match supplied runtime operator-review queue entry")


def test_operator_review_summary_mismatch_with_fixture_queue_bridge_fails_closed() -> None:
    nested = _valid_fixture_queue_bridge(operator_review_summary="different")
    _assert_blocked_with_reason(_valid_bridge_record(fixture_only_source_provider_operator_review_queue_bridge=nested), "operator review summary does not match fixture-only operator-review queue bridge")


@pytest.mark.parametrize("status", [item for item in bridge.FixtureOnlyOperatorReviewQueueEntryBridgeStatus if item is not bridge.FixtureOnlyOperatorReviewQueueEntryBridgeStatus.FIXTURE_ONLY_OPERATOR_REVIEW_QUEUE_ENTRY_BRIDGE_RECORDED])
def test_non_recorded_bridge_status_fails_closed(status) -> None:
    _assert_blocked_with_reason(_valid_bridge_record(fixture_only_operator_review_queue_entry_bridge_status=status), f"fixture-only operator-review queue-entry bridge status is {status.value}")


@pytest.mark.parametrize("posture", [item for item in bridge.FixtureOnlyOperatorReviewQueueEntryBridgePosture if item is not bridge.FixtureOnlyOperatorReviewQueueEntryBridgePosture.FIXTURE_ONLY_OPERATOR_REVIEW_QUEUE_ENTRY_BRIDGE_IN_MEMORY_ONLY])
def test_non_in_memory_posture_fails_closed(posture) -> None:
    _assert_blocked_with_reason(_valid_bridge_record(fixture_only_operator_review_queue_entry_bridge_posture=posture), f"fixture-only operator-review queue-entry bridge posture is {posture.value}")


@pytest.mark.parametrize("status", [item for item in bridge.OperatorReviewQueueEntryBridgeAlignmentStatus if item is not bridge.OperatorReviewQueueEntryBridgeAlignmentStatus.OPERATOR_REVIEW_QUEUE_ENTRY_BRIDGE_ALIGNED])
def test_non_aligned_alignment_status_fails_closed(status) -> None:
    _assert_blocked_with_reason(_valid_bridge_record(operator_review_queue_entry_bridge_alignment_status=status), f"operator-review queue-entry bridge alignment status is {status.value}")


@pytest.mark.parametrize("status", [item for item in bridge.NoLookaheadStatus if item is not bridge.NoLookaheadStatus.NO_LOOKAHEAD_RECORDED])
def test_non_recorded_no_lookahead_status_fails_closed(status) -> None:
    _assert_blocked_with_reason(_valid_bridge_record(no_lookahead_status=status), f"no-lookahead status is {status.value}")


@pytest.mark.parametrize("status", [item for item in bridge.OperatorReviewStatus if item is not bridge.OperatorReviewStatus.OPERATOR_REVIEW_REQUIRED])
def test_non_required_operator_review_status_fails_closed(status) -> None:
    _assert_blocked_with_reason(_valid_bridge_record(operator_review_status=status), f"operator review status is {status.value}")


@pytest.mark.parametrize("status", [item for item in bridge.RuntimeGateStatus if item is not bridge.RuntimeGateStatus.RUNTIME_GATE_READY])
def test_non_ready_runtime_gate_status_fails_closed(status) -> None:
    _assert_blocked_with_reason(_valid_bridge_record(runtime_gate_status=status), f"runtime gate status is {status.value}")


def test_no_legacy_market_key_dataclass_or_mapping_input() -> None:
    legacy_identifier = "market" + "_id"
    assert legacy_identifier not in bridge.FixtureOnlySourceProviderOperatorReviewQueueEntryBridgeRecord.__dataclass_fields__
    source = MODULE_PATH.read_text()
    tree = ast.parse(source)
    dataclass_fields = [node.target.id for node in ast.walk(tree) if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name)]
    assert legacy_identifier not in dataclass_fields
    assert f'mapping["{legacy_identifier}"]' not in source
    assert f"mapping['{legacy_identifier}']" not in source


def _strip_docstrings(source: str) -> str:
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if not isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        if node.body and isinstance(node.body[0], ast.Expr) and isinstance(node.body[0].value, ast.Constant) and isinstance(node.body[0].value.value, str):
            node.body[0] = ast.Pass()
    return ast.unparse(tree)


def test_static_no_side_effect_terms() -> None:
    source = _strip_docstrings(MODULE_PATH.read_text())
    forbidden_terms = ["requests", "httpx", "urllib", "aiohttp", "boto3", "polymarket", "kalshi", "duckdb", "pandas", "subprocess", "open(", ".read_text(", ".write_text(", "socket", "os.environ", "dotenv", "place_order", "paper_trade", "trade", "backtest", "score", "execute_order", "submit_order", "persist", "database", "postgres", "redis", "export", "write", "save", "owner_decision", "capture_decision", "operator_decision", "execute_decision", "celery", "rabbitmq", "sqs", "enqueue(", "dequeue(", "publish(", "subscribe(", "scheduler", "broker", "provider_client", "api_call", "scrape", "download", "credentials", "production", "simulate", "simulation", "generate_report", "report_writer", "execute_smoke", "run_smoke", "execute_trace", "run_trace", "deliver_handoff", "send_handoff", "deliver_ack", "send_ack", "deliver_queue", "send_queue", "deliver_queue_entry", "send_queue_entry", "queue_service", "notification", "notify"]
    assert [term for term in forbidden_terms if term in source] == []
