import ast
from dataclasses import asdict, replace
from pathlib import Path

import pytest

from meg.weather.stage2 import fixture_only_source_provider_operator_review_final_packet_bridge_runtime as bridge
from meg.weather.stage2 import fixture_only_source_provider_operator_review_queue_summary_bridge_runtime as summary_bridge
from meg.weather.stage2 import supplied_runtime_operator_review_final_packet as sofp
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
from tests.core import test_weather_stage2_fixture_only_source_provider_operator_review_queue_summary_bridge_runtime as qsb_base
from tests.core import test_weather_supplied_runtime_operator_review_final_packet as final_base

MODULE_PATH = Path("meg/weather/stage2/fixture_only_source_provider_operator_review_final_packet_bridge_runtime.py")
TEST_PATH = Path("tests/core/test_weather_stage2_fixture_only_source_provider_operator_review_final_packet_bridge_runtime.py")


def _valid_queue_summary_bridge(**overrides: object) -> summary_bridge.FixtureOnlySourceProviderOperatorReviewQueueSummaryBridgeRecord:
    return qsb_base._valid_bridge_record(**overrides)


def _valid_final_packet(**overrides: object) -> sofp.SuppliedRuntimeOperatorReviewFinalPacketRecord:
    base_summary_bridge = _valid_queue_summary_bridge()
    values = {
        "supplied_runtime_operator_review_queue_summary": base_summary_bridge.supplied_runtime_operator_review_queue_summary,
        "operator_review_summary": base_summary_bridge.operator_review_summary,
    }
    values.update(overrides)
    return final_base._valid_operator_review_final_packet(**values)


def _valid_bridge_record(**overrides: object) -> bridge.FixtureOnlySourceProviderOperatorReviewFinalPacketBridgeRecord:
    values = {
        "condition_id": "condition-1",
        "token_id": "token-1",
        "outcome": "Yes",
        "fixture_only_source_provider_operator_review_queue_summary_bridge": _valid_queue_summary_bridge(),
        "supplied_runtime_operator_review_final_packet": _valid_final_packet(),
        "operator_review_final_packet_bridge_id": "final-packet-bridge-1",
        "operator_review_final_packet_bridge_summary": "Fixture-only queue-summary bridge linked to supplied final packet.",
        "fixture_queue_summary_bridge_summary": "Fixture-only queue-entry bridge linked to supplied queue summary.",
        "supplied_final_packet_summary": "Caller supplied operator-review final packet summary text.",
        "operator_review_summary": "Operator review remains required before any action.",
        "blocked_reason_summary": "No blocker for this valid final-packet bridge.",
        "fixture_only_operator_review_final_packet_bridge_status": bridge.FixtureOnlyOperatorReviewFinalPacketBridgeStatus.FIXTURE_ONLY_OPERATOR_REVIEW_FINAL_PACKET_BRIDGE_RECORDED,
        "fixture_only_operator_review_final_packet_bridge_posture": bridge.FixtureOnlyOperatorReviewFinalPacketBridgePosture.FIXTURE_ONLY_OPERATOR_REVIEW_FINAL_PACKET_BRIDGE_IN_MEMORY_ONLY,
        "operator_review_final_packet_bridge_alignment_status": bridge.OperatorReviewFinalPacketBridgeAlignmentStatus.OPERATOR_REVIEW_FINAL_PACKET_BRIDGE_ALIGNED,
        "no_lookahead_status": bridge.NoLookaheadStatus.NO_LOOKAHEAD_RECORDED,
        "operator_review_status": bridge.OperatorReviewStatus.OPERATOR_REVIEW_REQUIRED,
        "runtime_gate_status": bridge.RuntimeGateStatus.RUNTIME_GATE_READY,
    }
    values.update(overrides)
    return bridge.FixtureOnlySourceProviderOperatorReviewFinalPacketBridgeRecord(**values)


def _assert_blocked_with_reason(record, reason: str) -> None:
    result = bridge.validate_fixture_only_source_provider_operator_review_final_packet_bridge_record(record)
    assert result.passed is False
    assert result.severity is bridge.ValidationSeverity.BLOCKED
    assert reason in result.reasons


def _final_with_summary(summary: soqs.SuppliedRuntimeOperatorReviewQueueSummaryRecord, **overrides: object):
    values = {"condition_id": summary.condition_id, "token_id": summary.token_id, "outcome": summary.outcome, "supplied_runtime_operator_review_queue_summary": summary}
    values.update(overrides)
    return _valid_final_packet(**values)


def _summary_with_entry(entry: soqe.SuppliedRuntimeOperatorReviewQueueEntryRecord):
    return final_base._valid_operator_review_queue_summary(condition_id=entry.condition_id, token_id=entry.token_id, outcome=entry.outcome, supplied_runtime_operator_review_queue_entry=entry)


def _entry_with_packet(packet: soqp.SuppliedRuntimeOperatorReviewQueuePacketRecord):
    return final_base._valid_operator_review_queue_entry(condition_id=packet.condition_id, token_id=packet.token_id, outcome=packet.outcome, supplied_runtime_operator_review_queue_packet=packet)


def _packet_with_ack(ack: soap.SuppliedRuntimeOperatorReviewAckPacketRecord):
    return final_base._valid_operator_review_queue_packet(condition_id=ack.condition_id, token_id=ack.token_id, outcome=ack.outcome, supplied_runtime_operator_review_ack_packet=ack)


def _ack_with_handoff(handoff: sroh.SuppliedRuntimeOperatorReviewHandoffRecord):
    return final_base._valid_operator_review_ack_packet(condition_id=handoff.condition_id, token_id=handoff.token_id, outcome=handoff.outcome, supplied_runtime_operator_review_handoff=handoff)


def _handoff_with_trace(trace: srtp.SuppliedRuntimeTracePacketRecord):
    return final_base._valid_operator_review_handoff(condition_id=trace.condition_id, token_id=trace.token_id, outcome=trace.outcome, supplied_runtime_trace_packet=trace)


def _trace_with_smoke(smoke: sees.SuppliedRuntimeEndToEndSmokeRecord):
    return final_base._valid_trace_packet(condition_id=smoke.condition_id, token_id=smoke.token_id, outcome=smoke.outcome, supplied_runtime_end_to_end_smoke=smoke)


def _smoke_with_report(report: srdr.SuppliedRuntimeDryRunReportRecord):
    return final_base._valid_end_to_end_smoke(condition_id=report.condition_id, token_id=report.token_id, outcome=report.outcome, supplied_runtime_dry_run_report=report)


def _report_with_dry(dry: srdp.SuppliedRuntimeDryRunPacketRecord):
    return final_base._valid_dry_run_report(condition_id=dry.condition_id, token_id=dry.token_id, outcome=dry.outcome, supplied_runtime_dry_run_packet=dry)


def _dry_with_bundle(bundle: srvb.SuppliedRuntimeValidationBundleRecord):
    return final_base._valid_dry_run_packet(condition_id=bundle.condition_id, token_id=bundle.token_id, outcome=bundle.outcome, supplied_runtime_validation_bundle=bundle)


def _bundle_with_evidence(evidence: sepr.SuppliedEvidencePacketRecord):
    return final_base._valid_bundle(condition_id=evidence.condition_id, token_id=evidence.token_id, outcome=evidence.outcome, supplied_evidence_packet=evidence)


def test_enums_are_closed_sets() -> None:
    assert bridge.FixtureOnlyOperatorReviewFinalPacketBridgeStatus.values() == frozenset({"fixture_only_operator_review_final_packet_bridge_recorded", "fixture_only_operator_review_final_packet_bridge_missing", "fixture_only_operator_review_final_packet_bridge_ambiguous", "fixture_only_operator_review_final_packet_bridge_unsupported", "fixture_only_operator_review_final_packet_bridge_unknown"})
    assert bridge.FixtureOnlyOperatorReviewFinalPacketBridgePosture.values() == frozenset({"fixture_only_operator_review_final_packet_bridge_in_memory_only", "fixture_only_operator_review_final_packet_bridge_missing", "fixture_only_operator_review_final_packet_bridge_ambiguous", "fixture_only_operator_review_final_packet_bridge_unsupported", "fixture_only_operator_review_final_packet_bridge_unknown"})
    assert bridge.OperatorReviewFinalPacketBridgeAlignmentStatus.values() == frozenset({"operator_review_final_packet_bridge_aligned", "operator_review_final_packet_bridge_mismatch", "operator_review_final_packet_bridge_missing", "operator_review_final_packet_bridge_ambiguous", "operator_review_final_packet_bridge_unknown"})
    assert bridge.NoLookaheadStatus.values() == frozenset({"no_lookahead_recorded", "no_lookahead_missing", "no_lookahead_ambiguous", "no_lookahead_unknown"})
    assert bridge.OperatorReviewStatus.values() == frozenset({"operator_review_required", "operator_review_missing", "operator_review_ambiguous", "operator_review_not_required", "operator_review_unknown"})
    assert bridge.RuntimeGateStatus.values() == frozenset({"runtime_gate_ready", "runtime_gate_blocked", "runtime_gate_requires_manual_review", "runtime_gate_unknown"})
    assert bridge.ValidationSeverity.values() == frozenset({"passed", "caution", "failed", "blocked"})


def test_frozen_dataclass_construction() -> None:
    record = _valid_bridge_record(provenance_notes="caller supplied")
    assert isinstance(record.fixture_only_source_provider_operator_review_queue_summary_bridge, summary_bridge.FixtureOnlySourceProviderOperatorReviewQueueSummaryBridgeRecord)
    assert isinstance(record.supplied_runtime_operator_review_final_packet, sofp.SuppliedRuntimeOperatorReviewFinalPacketRecord)
    assert record.provenance_notes == "caller supplied"
    with pytest.raises(Exception):
        record.condition_id = "changed"


def test_mapping_construction_coerces_string_enums_and_nested_mappings() -> None:
    record = bridge.fixture_only_source_provider_operator_review_final_packet_bridge_record_from_mapping(asdict(_valid_bridge_record()))
    assert isinstance(record.fixture_only_source_provider_operator_review_queue_summary_bridge, summary_bridge.FixtureOnlySourceProviderOperatorReviewQueueSummaryBridgeRecord)
    assert isinstance(record.supplied_runtime_operator_review_final_packet, sofp.SuppliedRuntimeOperatorReviewFinalPacketRecord)
    assert record.fixture_only_operator_review_final_packet_bridge_status is bridge.FixtureOnlyOperatorReviewFinalPacketBridgeStatus.FIXTURE_ONLY_OPERATOR_REVIEW_FINAL_PACKET_BRIDGE_RECORDED
    assert record.provenance_notes == ""


def test_valid_record_passes() -> None:
    result = bridge.validate_fixture_only_source_provider_operator_review_final_packet_bridge_record(_valid_bridge_record())
    assert result.passed is True
    assert result.severity is bridge.ValidationSeverity.PASSED
    assert result.reasons == ()


@pytest.mark.parametrize("field_name", ["condition_id", "token_id", "outcome", "operator_review_final_packet_bridge_id", "operator_review_final_packet_bridge_summary", "fixture_queue_summary_bridge_summary", "supplied_final_packet_summary", "operator_review_summary"])
def test_blank_required_text_fields_fail_closed(field_name: str) -> None:
    _assert_blocked_with_reason(_valid_bridge_record(**{field_name: "  "}), f"{field_name} is missing")


def test_blank_blocked_reason_summary_is_allowed_when_otherwise_valid() -> None:
    assert bridge.validate_fixture_only_source_provider_operator_review_final_packet_bridge_record(_valid_bridge_record(blocked_reason_summary="")).passed is True


def test_blank_blocked_reason_summary_is_required_when_another_failure_exists() -> None:
    _assert_blocked_with_reason(_valid_bridge_record(condition_id="wrong", blocked_reason_summary=""), "blocked_reason_summary is missing")


def test_invalid_nested_fixture_queue_summary_bridge_fails_closed() -> None:
    bad = _valid_queue_summary_bridge(operator_review_queue_summary_bridge_summary="")
    _assert_blocked_with_reason(_valid_bridge_record(fixture_only_source_provider_operator_review_queue_summary_bridge=bad), "fixture-only source provider operator-review queue-summary bridge is invalid")


def test_invalid_nested_supplied_final_packet_fails_closed() -> None:
    _assert_blocked_with_reason(_valid_bridge_record(supplied_runtime_operator_review_final_packet=_valid_final_packet(final_packet_summary="")), "supplied runtime operator-review final packet is invalid")


@pytest.mark.parametrize(("field_name", "reason"), [("condition_id", "condition_id does not match fixture-only operator-review queue-summary bridge"), ("token_id", "token_id does not match fixture-only operator-review queue-summary bridge"), ("outcome", "outcome does not match fixture-only operator-review queue-summary bridge")])
def test_top_level_route_mismatch_with_fixture_summary_bridge_fails_closed(field_name: str, reason: str) -> None:
    _assert_blocked_with_reason(_valid_bridge_record(**{field_name: "different"}), reason)


@pytest.mark.parametrize(("field_name", "reason"), [("condition_id", "condition_id does not match supplied runtime operator-review final packet"), ("token_id", "token_id does not match supplied runtime operator-review final packet"), ("outcome", "outcome does not match supplied runtime operator-review final packet")])
def test_top_level_route_mismatch_with_supplied_final_packet_fails_closed(field_name: str, reason: str) -> None:
    _assert_blocked_with_reason(_valid_bridge_record(supplied_runtime_operator_review_final_packet=_valid_final_packet(**{field_name: "different"})), reason)


def test_fixture_summary_bridge_versus_supplied_final_packet_route_mismatch_fails_closed() -> None:
    final = _valid_final_packet(condition_id="different")
    _assert_blocked_with_reason(_valid_bridge_record(condition_id="different", supplied_runtime_operator_review_final_packet=final), "nested fixture-only operator-review queue-summary bridge and supplied runtime operator-review final packet routes do not match")


def test_nested_supplied_queue_summary_mismatch_fails_closed() -> None:
    final = _final_with_summary(final_base._valid_operator_review_queue_summary(condition_id="different"))
    _assert_blocked_with_reason(_valid_bridge_record(condition_id="different", supplied_runtime_operator_review_final_packet=final), "nested supplied runtime operator-review queue summaries do not match")


def test_nested_supplied_queue_entry_mismatch_fails_closed() -> None:
    final = _final_with_summary(_summary_with_entry(final_base._valid_operator_review_queue_entry(condition_id="different")))
    _assert_blocked_with_reason(_valid_bridge_record(condition_id="different", supplied_runtime_operator_review_final_packet=final), "nested supplied runtime operator-review queue entries do not match")


def test_nested_queue_packet_mismatch_fails_closed() -> None:
    packet = final_base._valid_operator_review_queue_packet(condition_id="different")
    final = _final_with_summary(_summary_with_entry(_entry_with_packet(packet)))
    _assert_blocked_with_reason(_valid_bridge_record(condition_id="different", supplied_runtime_operator_review_final_packet=final), "nested supplied runtime operator-review queue packets do not match")


def test_nested_ack_packet_mismatch_fails_closed() -> None:
    ack = final_base._valid_operator_review_ack_packet(condition_id="different")
    final = _final_with_summary(_summary_with_entry(_entry_with_packet(_packet_with_ack(ack))))
    _assert_blocked_with_reason(_valid_bridge_record(condition_id="different", supplied_runtime_operator_review_final_packet=final), "nested supplied runtime operator-review ack packets do not match")


def test_nested_handoff_mismatch_fails_closed() -> None:
    handoff = final_base._valid_operator_review_handoff(condition_id="different")
    final = _final_with_summary(_summary_with_entry(_entry_with_packet(_packet_with_ack(_ack_with_handoff(handoff)))))
    _assert_blocked_with_reason(_valid_bridge_record(condition_id="different", supplied_runtime_operator_review_final_packet=final), "nested supplied runtime operator-review handoffs do not match")


def test_nested_trace_mismatch_fails_closed() -> None:
    trace = final_base._valid_trace_packet(condition_id="different")
    final = _final_with_summary(_summary_with_entry(_entry_with_packet(_packet_with_ack(_ack_with_handoff(_handoff_with_trace(trace))))))
    _assert_blocked_with_reason(_valid_bridge_record(condition_id="different", supplied_runtime_operator_review_final_packet=final), "nested supplied runtime trace packets do not match")


def test_nested_end_to_end_smoke_mismatch_fails_closed() -> None:
    smoke = final_base._valid_end_to_end_smoke(condition_id="different")
    final = _final_with_summary(_summary_with_entry(_entry_with_packet(_packet_with_ack(_ack_with_handoff(_handoff_with_trace(_trace_with_smoke(smoke)))))))
    _assert_blocked_with_reason(_valid_bridge_record(condition_id="different", supplied_runtime_operator_review_final_packet=final), "nested supplied runtime end-to-end smokes do not match")


def test_nested_dry_run_report_mismatch_fails_closed() -> None:
    report = final_base._valid_dry_run_report(condition_id="different")
    final = _final_with_summary(_summary_with_entry(_entry_with_packet(_packet_with_ack(_ack_with_handoff(_handoff_with_trace(_trace_with_smoke(_smoke_with_report(report))))))))
    _assert_blocked_with_reason(_valid_bridge_record(condition_id="different", supplied_runtime_operator_review_final_packet=final), "nested supplied runtime dry-run reports do not match")


def test_nested_dry_run_packet_validation_bundle_mismatch_fails_closed() -> None:
    dry = final_base._valid_dry_run_packet(condition_id="different")
    final = _final_with_summary(_summary_with_entry(_entry_with_packet(_packet_with_ack(_ack_with_handoff(_handoff_with_trace(_trace_with_smoke(_smoke_with_report(_report_with_dry(dry)))))))))
    _assert_blocked_with_reason(_valid_bridge_record(condition_id="different", supplied_runtime_operator_review_final_packet=final), "nested supplied runtime dry-run packets do not match")


def test_nested_evidence_packet_contract_mismatch_fails_closed() -> None:
    contract = final_base._valid_contract(condition_id="different")
    evidence = final_base._valid_evidence_packet(condition_id="different", supplied_market_contract=contract)
    final = _final_with_summary(_summary_with_entry(_entry_with_packet(_packet_with_ack(_ack_with_handoff(_handoff_with_trace(_trace_with_smoke(_smoke_with_report(_report_with_dry(_dry_with_bundle(_bundle_with_evidence(evidence)))))))))))
    _assert_blocked_with_reason(_valid_bridge_record(condition_id="different", supplied_runtime_operator_review_final_packet=final), "nested supplied evidence packets do not match")


def test_summary_alignment_failures() -> None:
    _assert_blocked_with_reason(_valid_bridge_record(fixture_queue_summary_bridge_summary="different"), "fixture queue-summary bridge summary does not match fixture-only operator-review queue-summary bridge")
    _assert_blocked_with_reason(_valid_bridge_record(supplied_final_packet_summary="different"), "supplied final packet summary does not match supplied runtime operator-review final packet")


def test_operator_review_summary_mismatch_against_each_nested_record_fails_closed() -> None:
    _assert_blocked_with_reason(_valid_bridge_record(operator_review_summary="different"), "operator review summary does not match supplied runtime operator-review final packet")
    _assert_blocked_with_reason(_valid_bridge_record(operator_review_summary="different"), "operator review summary does not match fixture-only operator-review queue-summary bridge")


@pytest.mark.parametrize("status", [value for value in bridge.FixtureOnlyOperatorReviewFinalPacketBridgeStatus if value is not bridge.FixtureOnlyOperatorReviewFinalPacketBridgeStatus.FIXTURE_ONLY_OPERATOR_REVIEW_FINAL_PACKET_BRIDGE_RECORDED])
def test_every_non_recorded_bridge_status_fails_closed(status) -> None:
    _assert_blocked_with_reason(_valid_bridge_record(fixture_only_operator_review_final_packet_bridge_status=status), f"fixture-only operator-review final-packet bridge status is {status.value}")


@pytest.mark.parametrize("posture", [value for value in bridge.FixtureOnlyOperatorReviewFinalPacketBridgePosture if value is not bridge.FixtureOnlyOperatorReviewFinalPacketBridgePosture.FIXTURE_ONLY_OPERATOR_REVIEW_FINAL_PACKET_BRIDGE_IN_MEMORY_ONLY])
def test_every_non_in_memory_posture_fails_closed(posture) -> None:
    _assert_blocked_with_reason(_valid_bridge_record(fixture_only_operator_review_final_packet_bridge_posture=posture), f"fixture-only operator-review final-packet bridge posture is {posture.value}")


@pytest.mark.parametrize("alignment", [value for value in bridge.OperatorReviewFinalPacketBridgeAlignmentStatus if value is not bridge.OperatorReviewFinalPacketBridgeAlignmentStatus.OPERATOR_REVIEW_FINAL_PACKET_BRIDGE_ALIGNED])
def test_every_non_aligned_alignment_status_fails_closed(alignment) -> None:
    _assert_blocked_with_reason(_valid_bridge_record(operator_review_final_packet_bridge_alignment_status=alignment), f"operator-review final-packet bridge alignment status is {alignment.value}")


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
        "requests", "httpx", "url" + "lib", "aiohttp", "boto3", "polymarket", "kalshi", "duckdb", "pandas", "sub" + "process", "open(", ".read" + "_text(", ".write" + "_text(", "socket", "os.environ", "dotenv", "place" + "_order", "paper" + "_trade", "trade", "back" + "test", "score", "execute" + "_order", "submit" + "_order", "persist", "data" + "base", "post" + "gres", "redis", "export", "write", "save", "owner" + "_decision", "capture" + "_decision", "operator" + "_decision", "execute" + "_decision", "celery", "rabbitmq", "sqs", "enqueue(", "dequeue(", "publish(", "subscribe(", "scheduler", "broker", "provider" + "_client", "api" + "_call", "scrape", "download", "credentials", "production", "simulate", "simulation", "generate" + "_report", "report" + "_writer", "generate" + "_summary", "summary" + "_writer", "generate" + "_packet", "packet" + "_writer", "finalize" + "_packet", "execute" + "_smoke", "run" + "_smoke", "execute" + "_trace", "run" + "_trace", "deliver" + "_handoff", "send" + "_handoff", "deliver" + "_ack", "send" + "_ack", "deliver" + "_queue", "send" + "_queue", "deliver" + "_queue" + "_entry", "send" + "_queue" + "_entry", "deliver" + "_queue" + "_summary", "send" + "_queue" + "_summary", "deliver" + "_final" + "_packet", "send" + "_final" + "_packet", "queue" + "_service", "notification", "notify",
    ]
    assert {term for term in terms if term in source} == set()
