import ast
from dataclasses import asdict, replace
from pathlib import Path

import pytest

from meg.weather.stage2 import fixture_only_source_provider_operator_review_queue_summary_bridge_runtime as bridge
from meg.weather.stage2 import fixture_only_source_provider_operator_review_queue_entry_bridge_runtime as entry_bridge
from meg.weather.stage2 import supplied_runtime_operator_review_queue_summary as soqs
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
from tests.core import test_weather_stage2_fixture_only_source_provider_operator_review_queue_entry_bridge_runtime as eb_base
from tests.core import test_weather_supplied_runtime_operator_review_queue_summary as summary_base

MODULE_PATH = Path("meg/weather/stage2/fixture_only_source_provider_operator_review_queue_summary_bridge_runtime.py")
TEST_PATH = Path("tests/core/test_weather_stage2_fixture_only_source_provider_operator_review_queue_summary_bridge_runtime.py")


def _valid_entry_bridge(**overrides: object) -> entry_bridge.FixtureOnlySourceProviderOperatorReviewQueueEntryBridgeRecord:
    return eb_base._valid_bridge_record(**overrides)


def _valid_summary(**overrides: object) -> soqs.SuppliedRuntimeOperatorReviewQueueSummaryRecord:
    values = {
        "condition_id": "condition-1",
        "token_id": "token-1",
        "outcome": "Yes",
        "supplied_runtime_operator_review_queue_entry": eb_base._valid_supplied_queue_entry(),
        "queue_summary_id": "queue-summary-1",
        "queue_summary_text": "Caller supplied queue summary text.",
        "operator_review_summary": "Operator review remains required before any action.",
        "blocked_reason_summary": "No blocker for this valid queue summary.",
        "operator_review_queue_summary_status": soqs.OperatorReviewQueueSummaryStatus.OPERATOR_REVIEW_QUEUE_SUMMARY_RECORDED,
        "operator_review_queue_summary_completeness_status": soqs.OperatorReviewQueueSummaryCompletenessStatus.OPERATOR_REVIEW_QUEUE_SUMMARY_COMPLETE,
        "operator_review_queue_summary_posture": soqs.OperatorReviewQueueSummaryPosture.OPERATOR_REVIEW_QUEUE_SUMMARY_IN_MEMORY_ONLY,
        "operator_review_status": soqs.OperatorReviewStatus.OPERATOR_REVIEW_REQUIRED,
        "runtime_gate_status": soqs.RuntimeGateStatus.RUNTIME_GATE_READY,
    }
    values.update(overrides)
    return soqs.SuppliedRuntimeOperatorReviewQueueSummaryRecord(**values)


def _valid_bridge_record(**overrides: object) -> bridge.FixtureOnlySourceProviderOperatorReviewQueueSummaryBridgeRecord:
    values = {
        "condition_id": "condition-1",
        "token_id": "token-1",
        "outcome": "Yes",
        "fixture_only_source_provider_operator_review_queue_entry_bridge": _valid_entry_bridge(),
        "supplied_runtime_operator_review_queue_summary": _valid_summary(),
        "operator_review_queue_summary_bridge_id": "queue-summary-bridge-1",
        "operator_review_queue_summary_bridge_summary": "Fixture-only queue-entry bridge linked to supplied queue summary.",
        "fixture_queue_entry_bridge_summary": "Fixture-only queue bridge linked to supplied queue entry.",
        "supplied_queue_summary_text": "Caller supplied queue summary text.",
        "operator_review_summary": "Operator review remains required before any action.",
        "blocked_reason_summary": "No blocker for this valid queue-summary bridge.",
        "fixture_only_operator_review_queue_summary_bridge_status": bridge.FixtureOnlyOperatorReviewQueueSummaryBridgeStatus.FIXTURE_ONLY_OPERATOR_REVIEW_QUEUE_SUMMARY_BRIDGE_RECORDED,
        "fixture_only_operator_review_queue_summary_bridge_posture": bridge.FixtureOnlyOperatorReviewQueueSummaryBridgePosture.FIXTURE_ONLY_OPERATOR_REVIEW_QUEUE_SUMMARY_BRIDGE_IN_MEMORY_ONLY,
        "operator_review_queue_summary_bridge_alignment_status": bridge.OperatorReviewQueueSummaryBridgeAlignmentStatus.OPERATOR_REVIEW_QUEUE_SUMMARY_BRIDGE_ALIGNED,
        "no_lookahead_status": bridge.NoLookaheadStatus.NO_LOOKAHEAD_RECORDED,
        "operator_review_status": bridge.OperatorReviewStatus.OPERATOR_REVIEW_REQUIRED,
        "runtime_gate_status": bridge.RuntimeGateStatus.RUNTIME_GATE_READY,
    }
    values.update(overrides)
    return bridge.FixtureOnlySourceProviderOperatorReviewQueueSummaryBridgeRecord(**values)


def _assert_blocked_with_reason(record, reason: str) -> None:
    result = bridge.validate_fixture_only_source_provider_operator_review_queue_summary_bridge_record(record)
    assert result.passed is False
    assert result.severity is bridge.ValidationSeverity.BLOCKED
    assert reason in result.reasons


def _summary_with_entry(entry: soqe.SuppliedRuntimeOperatorReviewQueueEntryRecord, **overrides: object):
    values = {"condition_id": entry.condition_id, "token_id": entry.token_id, "outcome": entry.outcome, "supplied_runtime_operator_review_queue_entry": entry}
    values.update(overrides)
    return _valid_summary(**values)


def _entry_with_packet(packet: soqp.SuppliedRuntimeOperatorReviewQueuePacketRecord):
    return eb_base._valid_supplied_queue_entry(condition_id=packet.condition_id, token_id=packet.token_id, outcome=packet.outcome, supplied_runtime_operator_review_queue_packet=packet)


def _queue_packet_with_ack(ack: soap.SuppliedRuntimeOperatorReviewAckPacketRecord):
    return replace(eb_base._valid_supplied_queue_entry().supplied_runtime_operator_review_queue_packet, condition_id=ack.condition_id, token_id=ack.token_id, outcome=ack.outcome, supplied_runtime_operator_review_ack_packet=ack)


def test_enums_are_closed_sets() -> None:
    assert bridge.FixtureOnlyOperatorReviewQueueSummaryBridgeStatus.values() == frozenset({"fixture_only_operator_review_queue_summary_bridge_recorded", "fixture_only_operator_review_queue_summary_bridge_missing", "fixture_only_operator_review_queue_summary_bridge_ambiguous", "fixture_only_operator_review_queue_summary_bridge_unsupported", "fixture_only_operator_review_queue_summary_bridge_unknown"})
    assert bridge.FixtureOnlyOperatorReviewQueueSummaryBridgePosture.values() == frozenset({"fixture_only_operator_review_queue_summary_bridge_in_memory_only", "fixture_only_operator_review_queue_summary_bridge_missing", "fixture_only_operator_review_queue_summary_bridge_ambiguous", "fixture_only_operator_review_queue_summary_bridge_unsupported", "fixture_only_operator_review_queue_summary_bridge_unknown"})
    assert bridge.OperatorReviewQueueSummaryBridgeAlignmentStatus.values() == frozenset({"operator_review_queue_summary_bridge_aligned", "operator_review_queue_summary_bridge_mismatch", "operator_review_queue_summary_bridge_missing", "operator_review_queue_summary_bridge_ambiguous", "operator_review_queue_summary_bridge_unknown"})
    assert bridge.NoLookaheadStatus.values() == frozenset({"no_lookahead_recorded", "no_lookahead_missing", "no_lookahead_ambiguous", "no_lookahead_unknown"})
    assert bridge.OperatorReviewStatus.values() == frozenset({"operator_review_required", "operator_review_missing", "operator_review_ambiguous", "operator_review_not_required", "operator_review_unknown"})
    assert bridge.RuntimeGateStatus.values() == frozenset({"runtime_gate_ready", "runtime_gate_blocked", "runtime_gate_requires_manual_review", "runtime_gate_unknown"})
    assert bridge.ValidationSeverity.values() == frozenset({"passed", "caution", "failed", "blocked"})


def test_dataclass_construction() -> None:
    record = _valid_bridge_record(provenance_notes="caller supplied")
    assert isinstance(record.fixture_only_source_provider_operator_review_queue_entry_bridge, entry_bridge.FixtureOnlySourceProviderOperatorReviewQueueEntryBridgeRecord)
    assert isinstance(record.supplied_runtime_operator_review_queue_summary, soqs.SuppliedRuntimeOperatorReviewQueueSummaryRecord)
    assert record.provenance_notes == "caller supplied"


def test_mapping_construction_coerces_string_enums_and_nested_mappings() -> None:
    record = bridge.fixture_only_source_provider_operator_review_queue_summary_bridge_record_from_mapping(asdict(_valid_bridge_record()))
    assert isinstance(record.fixture_only_source_provider_operator_review_queue_entry_bridge, entry_bridge.FixtureOnlySourceProviderOperatorReviewQueueEntryBridgeRecord)
    assert isinstance(record.supplied_runtime_operator_review_queue_summary, soqs.SuppliedRuntimeOperatorReviewQueueSummaryRecord)
    assert record.fixture_only_operator_review_queue_summary_bridge_status is bridge.FixtureOnlyOperatorReviewQueueSummaryBridgeStatus.FIXTURE_ONLY_OPERATOR_REVIEW_QUEUE_SUMMARY_BRIDGE_RECORDED
    assert record.provenance_notes == ""


def test_valid_record_passes() -> None:
    result = bridge.validate_fixture_only_source_provider_operator_review_queue_summary_bridge_record(_valid_bridge_record())
    assert result.passed is True
    assert result.severity is bridge.ValidationSeverity.PASSED
    assert result.reasons == ()


@pytest.mark.parametrize("field_name", ["condition_id", "token_id", "outcome", "operator_review_queue_summary_bridge_id", "operator_review_queue_summary_bridge_summary", "fixture_queue_entry_bridge_summary", "supplied_queue_summary_text", "operator_review_summary"])
def test_blank_required_text_fields_fail_closed(field_name: str) -> None:
    _assert_blocked_with_reason(_valid_bridge_record(**{field_name: "  "}), f"{field_name} is missing")


def test_blank_blocked_reason_summary_is_allowed_when_otherwise_valid() -> None:
    assert bridge.validate_fixture_only_source_provider_operator_review_queue_summary_bridge_record(_valid_bridge_record(blocked_reason_summary="")).passed is True


def test_blank_blocked_reason_summary_fails_when_another_validation_failure_exists() -> None:
    _assert_blocked_with_reason(_valid_bridge_record(condition_id="wrong", blocked_reason_summary=""), "blocked_reason_summary is missing")


def test_invalid_nested_fixture_queue_entry_bridge_fails_closed() -> None:
    _assert_blocked_with_reason(_valid_bridge_record(fixture_only_source_provider_operator_review_queue_entry_bridge=_valid_entry_bridge(operator_review_queue_entry_bridge_summary="")), "fixture-only source provider operator-review queue-entry bridge is invalid")


def test_invalid_nested_supplied_queue_summary_fails_closed() -> None:
    _assert_blocked_with_reason(_valid_bridge_record(supplied_runtime_operator_review_queue_summary=_valid_summary(queue_summary_text="")), "supplied runtime operator-review queue summary is invalid")


@pytest.mark.parametrize(("field_name", "reason"), [("condition_id", "condition_id does not match fixture-only operator-review queue-entry bridge"), ("token_id", "token_id does not match fixture-only operator-review queue-entry bridge"), ("outcome", "outcome does not match fixture-only operator-review queue-entry bridge")])
def test_top_level_route_mismatch_with_fixture_entry_bridge_fails_closed(field_name: str, reason: str) -> None:
    _assert_blocked_with_reason(_valid_bridge_record(**{field_name: "different"}), reason)


@pytest.mark.parametrize(("field_name", "reason"), [("condition_id", "condition_id does not match supplied runtime operator-review queue summary"), ("token_id", "token_id does not match supplied runtime operator-review queue summary"), ("outcome", "outcome does not match supplied runtime operator-review queue summary")])
def test_top_level_route_mismatch_with_supplied_summary_fails_closed(field_name: str, reason: str) -> None:
    summary = _valid_summary(**{field_name: "different"})
    _assert_blocked_with_reason(_valid_bridge_record(supplied_runtime_operator_review_queue_summary=summary), reason)


def test_fixture_entry_bridge_versus_supplied_summary_route_mismatch_fails_closed() -> None:
    summary = _valid_summary(condition_id="different")
    _assert_blocked_with_reason(_valid_bridge_record(condition_id="different", supplied_runtime_operator_review_queue_summary=summary), "nested fixture-only operator-review queue-entry bridge and supplied runtime operator-review queue summary routes do not match")


def test_nested_supplied_queue_entry_mismatch_fails_closed() -> None:
    summary = _summary_with_entry(eb_base._valid_supplied_queue_entry(condition_id="different"))
    _assert_blocked_with_reason(_valid_bridge_record(condition_id="different", supplied_runtime_operator_review_queue_summary=summary), "nested supplied runtime operator-review queue entries do not match")


def test_nested_queue_packet_mismatch_fails_closed() -> None:
    packet = replace(eb_base._valid_supplied_queue_entry().supplied_runtime_operator_review_queue_packet, condition_id="different")
    summary = _summary_with_entry(_entry_with_packet(packet))
    _assert_blocked_with_reason(_valid_bridge_record(condition_id="different", supplied_runtime_operator_review_queue_summary=summary), "nested supplied runtime operator-review queue packets do not match")


def test_nested_ack_packet_mismatch_fails_closed() -> None:
    ack = eb_base.qb_base._valid_supplied_runtime_operator_review_ack_packet(condition_id="different")
    summary = _summary_with_entry(_entry_with_packet(_queue_packet_with_ack(ack)))
    _assert_blocked_with_reason(_valid_bridge_record(condition_id="different", supplied_runtime_operator_review_queue_summary=summary), "nested supplied runtime operator-review ack packets do not match")


def test_nested_handoff_mismatch_fails_closed() -> None:
    handoff = eb_base.qb_base._valid_supplied_runtime_operator_review_handoff(condition_id="different")
    ack = eb_base.qb_base._valid_supplied_runtime_operator_review_ack_packet(condition_id="different", supplied_runtime_operator_review_handoff=handoff)
    summary = _summary_with_entry(_entry_with_packet(_queue_packet_with_ack(ack)))
    _assert_blocked_with_reason(_valid_bridge_record(condition_id="different", supplied_runtime_operator_review_queue_summary=summary), "nested supplied runtime operator-review handoffs do not match")


def test_nested_trace_mismatch_fails_closed() -> None:
    trace = eb_base.qb_base._valid_supplied_runtime_trace_packet(condition_id="different")
    handoff = eb_base.qb_base._valid_supplied_runtime_operator_review_handoff(condition_id="different", supplied_runtime_trace_packet=trace)
    ack = eb_base.qb_base._valid_supplied_runtime_operator_review_ack_packet(condition_id="different", supplied_runtime_operator_review_handoff=handoff)
    summary = _summary_with_entry(_entry_with_packet(_queue_packet_with_ack(ack)))
    _assert_blocked_with_reason(_valid_bridge_record(condition_id="different", supplied_runtime_operator_review_queue_summary=summary), "nested supplied runtime trace packets do not match")


def test_nested_end_to_end_smoke_mismatch_fails_closed() -> None:
    smoke = eb_base.qb_base._valid_supplied_runtime_end_to_end_smoke(condition_id="different")
    trace = eb_base.qb_base._valid_supplied_runtime_trace_packet(condition_id="different", supplied_runtime_end_to_end_smoke=smoke)
    handoff = eb_base.qb_base._valid_supplied_runtime_operator_review_handoff(condition_id="different", supplied_runtime_trace_packet=trace)
    ack = eb_base.qb_base._valid_supplied_runtime_operator_review_ack_packet(condition_id="different", supplied_runtime_operator_review_handoff=handoff)
    summary = _summary_with_entry(_entry_with_packet(_queue_packet_with_ack(ack)))
    _assert_blocked_with_reason(_valid_bridge_record(condition_id="different", supplied_runtime_operator_review_queue_summary=summary), "nested supplied runtime end-to-end smokes do not match")


def test_nested_dry_run_report_mismatch_fails_closed() -> None:
    report = eb_base.qb_base._valid_supplied_runtime_dry_run_report(condition_id="different")
    smoke = eb_base.qb_base._valid_supplied_runtime_end_to_end_smoke(condition_id="different", supplied_runtime_dry_run_report=report)
    trace = eb_base.qb_base._valid_supplied_runtime_trace_packet(condition_id="different", supplied_runtime_end_to_end_smoke=smoke)
    handoff = eb_base.qb_base._valid_supplied_runtime_operator_review_handoff(condition_id="different", supplied_runtime_trace_packet=trace)
    ack = eb_base.qb_base._valid_supplied_runtime_operator_review_ack_packet(condition_id="different", supplied_runtime_operator_review_handoff=handoff)
    summary = _summary_with_entry(_entry_with_packet(_queue_packet_with_ack(ack)))
    _assert_blocked_with_reason(_valid_bridge_record(condition_id="different", supplied_runtime_operator_review_queue_summary=summary), "nested supplied runtime dry-run reports do not match")


def test_nested_dry_run_packet_validation_bundle_mismatch_fails_closed() -> None:
    dry = eb_base.qb_base._valid_supplied_runtime_dry_run_packet(condition_id="different")
    report = eb_base.qb_base._valid_supplied_runtime_dry_run_report(condition_id="different", supplied_runtime_dry_run_packet=dry)
    smoke = eb_base.qb_base._valid_supplied_runtime_end_to_end_smoke(condition_id="different", supplied_runtime_dry_run_report=report)
    trace = eb_base.qb_base._valid_supplied_runtime_trace_packet(condition_id="different", supplied_runtime_end_to_end_smoke=smoke)
    handoff = eb_base.qb_base._valid_supplied_runtime_operator_review_handoff(condition_id="different", supplied_runtime_trace_packet=trace)
    ack = eb_base.qb_base._valid_supplied_runtime_operator_review_ack_packet(condition_id="different", supplied_runtime_operator_review_handoff=handoff)
    summary = _summary_with_entry(_entry_with_packet(_queue_packet_with_ack(ack)))
    _assert_blocked_with_reason(_valid_bridge_record(condition_id="different", supplied_runtime_operator_review_queue_summary=summary), "nested supplied runtime dry-run packets do not match")


def test_nested_evidence_packet_contract_mismatch_fails_closed() -> None:
    contract = summary_base._valid_contract(condition_id="different")
    evidence = summary_base._valid_evidence_packet(condition_id="different", supplied_market_contract=contract)
    bundle = summary_base._valid_bundle(condition_id="different", supplied_market_contract=contract, supplied_evidence_packet=evidence)
    dry = eb_base.qb_base._valid_supplied_runtime_dry_run_packet(condition_id="different", supplied_runtime_validation_bundle=bundle)
    report = eb_base.qb_base._valid_supplied_runtime_dry_run_report(condition_id="different", supplied_runtime_dry_run_packet=dry)
    smoke = eb_base.qb_base._valid_supplied_runtime_end_to_end_smoke(condition_id="different", supplied_runtime_dry_run_report=report)
    trace = eb_base.qb_base._valid_supplied_runtime_trace_packet(condition_id="different", supplied_runtime_end_to_end_smoke=smoke)
    handoff = eb_base.qb_base._valid_supplied_runtime_operator_review_handoff(condition_id="different", supplied_runtime_trace_packet=trace)
    ack = eb_base.qb_base._valid_supplied_runtime_operator_review_ack_packet(condition_id="different", supplied_runtime_operator_review_handoff=handoff)
    summary = _summary_with_entry(_entry_with_packet(_queue_packet_with_ack(ack)))
    _assert_blocked_with_reason(_valid_bridge_record(condition_id="different", supplied_runtime_operator_review_queue_summary=summary), "nested supplied evidence packets do not match")


@pytest.mark.parametrize(("field_name", "value", "reason"), [("fixture_queue_entry_bridge_summary", "different", "fixture queue-entry bridge summary does not match fixture-only operator-review queue-entry bridge"), ("supplied_queue_summary_text", "different", "supplied queue summary text does not match supplied runtime operator-review queue summary")])
def test_summary_mismatches_fail_closed(field_name: str, value: str, reason: str) -> None:
    _assert_blocked_with_reason(_valid_bridge_record(**{field_name: value}), reason)


def test_operator_review_summary_mismatch_with_supplied_summary_fails_closed() -> None:
    _assert_blocked_with_reason(_valid_bridge_record(supplied_runtime_operator_review_queue_summary=_valid_summary(operator_review_summary="different")), "operator review summary does not match supplied runtime operator-review queue summary")


def test_operator_review_summary_mismatch_with_fixture_entry_bridge_fails_closed() -> None:
    _assert_blocked_with_reason(_valid_bridge_record(fixture_only_source_provider_operator_review_queue_entry_bridge=_valid_entry_bridge(operator_review_summary="different")), "operator review summary does not match fixture-only operator-review queue-entry bridge")


@pytest.mark.parametrize("status", [item for item in bridge.FixtureOnlyOperatorReviewQueueSummaryBridgeStatus if item is not bridge.FixtureOnlyOperatorReviewQueueSummaryBridgeStatus.FIXTURE_ONLY_OPERATOR_REVIEW_QUEUE_SUMMARY_BRIDGE_RECORDED])
def test_non_recorded_bridge_status_fails_closed(status) -> None:
    _assert_blocked_with_reason(_valid_bridge_record(fixture_only_operator_review_queue_summary_bridge_status=status), f"fixture-only operator-review queue-summary bridge status is {status.value}")


@pytest.mark.parametrize("posture", [item for item in bridge.FixtureOnlyOperatorReviewQueueSummaryBridgePosture if item is not bridge.FixtureOnlyOperatorReviewQueueSummaryBridgePosture.FIXTURE_ONLY_OPERATOR_REVIEW_QUEUE_SUMMARY_BRIDGE_IN_MEMORY_ONLY])
def test_non_in_memory_posture_fails_closed(posture) -> None:
    _assert_blocked_with_reason(_valid_bridge_record(fixture_only_operator_review_queue_summary_bridge_posture=posture), f"fixture-only operator-review queue-summary bridge posture is {posture.value}")


@pytest.mark.parametrize("status", [item for item in bridge.OperatorReviewQueueSummaryBridgeAlignmentStatus if item is not bridge.OperatorReviewQueueSummaryBridgeAlignmentStatus.OPERATOR_REVIEW_QUEUE_SUMMARY_BRIDGE_ALIGNED])
def test_non_aligned_alignment_status_fails_closed(status) -> None:
    _assert_blocked_with_reason(_valid_bridge_record(operator_review_queue_summary_bridge_alignment_status=status), f"operator-review queue-summary bridge alignment status is {status.value}")


@pytest.mark.parametrize("status", [item for item in bridge.NoLookaheadStatus if item is not bridge.NoLookaheadStatus.NO_LOOKAHEAD_RECORDED])
def test_non_recorded_no_lookahead_status_fails_closed(status) -> None:
    _assert_blocked_with_reason(_valid_bridge_record(no_lookahead_status=status), f"no-lookahead status is {status.value}")


@pytest.mark.parametrize("status", [item for item in bridge.OperatorReviewStatus if item is not bridge.OperatorReviewStatus.OPERATOR_REVIEW_REQUIRED])
def test_non_required_operator_review_status_fails_closed(status) -> None:
    _assert_blocked_with_reason(_valid_bridge_record(operator_review_status=status), f"operator review status is {status.value}")


@pytest.mark.parametrize("status", [item for item in bridge.RuntimeGateStatus if item is not bridge.RuntimeGateStatus.RUNTIME_GATE_READY])
def test_non_ready_runtime_gate_status_fails_closed(status) -> None:
    _assert_blocked_with_reason(_valid_bridge_record(runtime_gate_status=status), f"runtime gate status is {status.value}")


def test_no_legacy_market_key_or_pair_dataclass_or_mapping_input() -> None:
    legacy_identifier = "market" + "_id"
    derived_pair = "token" + "_outcome_pair"
    assert legacy_identifier not in bridge.FixtureOnlySourceProviderOperatorReviewQueueSummaryBridgeRecord.__dataclass_fields__
    assert derived_pair not in bridge.FixtureOnlySourceProviderOperatorReviewQueueSummaryBridgeRecord.__dataclass_fields__
    source = MODULE_PATH.read_text()
    test_source = TEST_PATH.read_text()
    tree = ast.parse(source)
    dataclass_fields = [node.target.id for node in ast.walk(tree) if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name)]
    assert legacy_identifier not in dataclass_fields
    assert derived_pair not in dataclass_fields
    assert f'mapping["{legacy_identifier}"]' not in source
    assert f"mapping['{legacy_identifier}']" not in source
    assert f'mapping["{derived_pair}"]' not in source
    assert f"mapping['{derived_pair}']" not in source
    assert legacy_identifier not in test_source
    assert derived_pair not in test_source


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
    forbidden_terms = ["requests", "httpx", "urllib", "aiohttp", "boto3", "polymarket", "kalshi", "duckdb", "pandas", "subprocess", "open(", ".read_text(", ".write_text(", "socket", "os.environ", "dotenv", "place_order", "paper_trade", "trade", "backtest", "score", "execute_order", "submit_order", "persist", "database", "postgres", "redis", "export", "write", "save", "owner_decision", "capture_decision", "operator_decision", "execute_decision", "celery", "rabbitmq", "sqs", "enqueue(", "dequeue(", "publish(", "subscribe(", "scheduler", "broker", "provider_client", "api_call", "scrape", "download", "credentials", "production", "simulate", "simulation", "generate_report", "report_writer", "generate_summary", "summary_writer", "execute_smoke", "run_smoke", "execute_trace", "run_trace", "deliver_handoff", "send_handoff", "deliver_ack", "send_ack", "deliver_queue", "send_queue", "deliver_queue_entry", "send_queue_entry", "deliver_queue_summary", "send_queue_summary", "queue_service", "notification", "notify"]
    assert [term for term in forbidden_terms if term in source] == []
