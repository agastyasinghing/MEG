import ast
from dataclasses import asdict, replace
from pathlib import Path

import pytest

from meg.weather.stage2 import fixture_only_source_provider_full_chain_negative_smoke_bridge_runtime as bridge
from meg.weather.stage2 import fixture_only_source_provider_full_chain_integration_smoke_bridge_runtime as positive_bridge_module
from meg.weather.stage2 import supplied_runtime_full_chain_negative_smoke as negative_smoke_module
from meg.weather.stage2 import supplied_runtime_full_chain_integration_smoke as integration_smoke_module
from tests.core import test_weather_stage2_fixture_only_source_provider_full_chain_integration_smoke_bridge_runtime as integration_bridge_base
from tests.core import test_weather_supplied_runtime_full_chain_negative_smoke as negative_base
from tests.core import test_weather_supplied_runtime_full_chain_integration_smoke as integration_base

MODULE_PATH = Path("meg/weather/stage2/fixture_only_source_provider_full_chain_negative_smoke_bridge_runtime.py")
TEST_PATH = Path("tests/core/test_weather_stage2_fixture_only_source_provider_full_chain_negative_smoke_bridge_runtime.py")


def _valid_integration_smoke_bridge(**overrides: object) -> positive_bridge_module.FixtureOnlySourceProviderFullChainIntegrationSmokeBridgeRecord:
    return integration_bridge_base._valid_bridge_record(**overrides)


def _valid_supplied_negative_smoke(**overrides: object) -> negative_smoke_module.SuppliedRuntimeFullChainNegativeSmokeRecord:
    return negative_base._valid_full_chain_negative_smoke(**overrides)


def _valid_bridge_record(**overrides: object) -> bridge.FixtureOnlySourceProviderFullChainNegativeSmokeBridgeRecord:
    positive = _valid_integration_smoke_bridge()
    negative = _valid_supplied_negative_smoke()
    values = {
        "condition_id": "condition-1",
        "token_id": "token-1",
        "outcome": "Yes",
        "fixture_only_source_provider_full_chain_integration_smoke_bridge": positive,
        "supplied_runtime_full_chain_negative_smoke": negative,
        "full_chain_negative_smoke_bridge_id": "full-chain-negative-smoke-bridge-1",
        "full_chain_negative_smoke_bridge_summary": "Fixture-only positive integration-smoke bridge linked to supplied negative smoke.",
        "fixture_integration_smoke_bridge_summary": positive.full_chain_integration_smoke_bridge_summary,
        "supplied_negative_smoke_summary": negative.negative_smoke_summary,
        "expected_failure_reason_summary": negative.expected_failure_reason_summary,
        "observed_failure_reason_summary": negative.observed_failure_reason_summary,
        "operator_review_summary": positive.operator_review_summary,
        "blocked_reason_summary": negative.blocked_reason_summary,
        "fixture_only_full_chain_negative_smoke_bridge_status": bridge.FixtureOnlyFullChainNegativeSmokeBridgeStatus.FIXTURE_ONLY_FULL_CHAIN_NEGATIVE_SMOKE_BRIDGE_RECORDED,
        "fixture_only_full_chain_negative_smoke_bridge_posture": bridge.FixtureOnlyFullChainNegativeSmokeBridgePosture.FIXTURE_ONLY_FULL_CHAIN_NEGATIVE_SMOKE_BRIDGE_IN_MEMORY_ONLY,
        "full_chain_negative_smoke_bridge_alignment_status": bridge.FullChainNegativeSmokeBridgeAlignmentStatus.FULL_CHAIN_NEGATIVE_SMOKE_BRIDGE_ALIGNED,
        "no_lookahead_status": bridge.NoLookaheadStatus.NO_LOOKAHEAD_RECORDED,
        "operator_review_status": bridge.OperatorReviewStatus.OPERATOR_REVIEW_REQUIRED,
        "runtime_gate_status": bridge.RuntimeGateStatus.RUNTIME_GATE_BLOCKED,
    }
    values.update(overrides)
    return bridge.FixtureOnlySourceProviderFullChainNegativeSmokeBridgeRecord(**values)


def _assert_blocked_with_reason(record, reason: str) -> None:
    result = bridge.validate_fixture_only_source_provider_full_chain_negative_smoke_bridge_record(record)
    assert result.passed is False
    assert result.severity is bridge.ValidationSeverity.BLOCKED
    assert reason in result.reasons


def _negative_with_nested(nested: integration_smoke_module.SuppliedRuntimeFullChainIntegrationSmokeRecord) -> negative_smoke_module.SuppliedRuntimeFullChainNegativeSmokeRecord:
    nested_result = integration_smoke_module.validate_supplied_runtime_full_chain_integration_smoke_record(nested)
    observed = nested_result.reasons[0] if nested_result.reasons else "no nested reason"
    return _valid_supplied_negative_smoke(
        supplied_runtime_full_chain_integration_smoke=nested,
        observed_failure_reason_summary=f"Observed nested reason: {observed}",
    )


def _negative_nested_smoke() -> integration_smoke_module.SuppliedRuntimeFullChainIntegrationSmokeRecord:
    return _valid_supplied_negative_smoke().supplied_runtime_full_chain_integration_smoke


def _with_summary(summary):
    return replace(_negative_nested_smoke(), supplied_runtime_operator_review_completion_summary=summary)


def _summary_with_seal(seal):
    return replace(_negative_nested_smoke().supplied_runtime_operator_review_completion_summary, supplied_runtime_operator_review_completion_seal=seal)


def _seal_with_bundle(bundle):
    summary = _negative_nested_smoke().supplied_runtime_operator_review_completion_summary
    return replace(summary.supplied_runtime_operator_review_completion_seal, supplied_runtime_operator_review_final_bundle=bundle)


def _bundle_with_packet(packet):
    seal = _negative_nested_smoke().supplied_runtime_operator_review_completion_summary.supplied_runtime_operator_review_completion_seal
    return replace(seal.supplied_runtime_operator_review_final_bundle, supplied_runtime_operator_review_final_packet=packet)


def _packet_with_summary(summary):
    bundle = _negative_nested_smoke().supplied_runtime_operator_review_completion_summary.supplied_runtime_operator_review_completion_seal.supplied_runtime_operator_review_final_bundle
    return replace(bundle.supplied_runtime_operator_review_final_packet, supplied_runtime_operator_review_queue_summary=summary)


def _queue_summary_with_entry(entry):
    packet = _negative_nested_smoke().supplied_runtime_operator_review_completion_summary.supplied_runtime_operator_review_completion_seal.supplied_runtime_operator_review_final_bundle.supplied_runtime_operator_review_final_packet
    return replace(packet.supplied_runtime_operator_review_queue_summary, supplied_runtime_operator_review_queue_entry=entry)


def _entry_with_queue(queue):
    summary = _negative_nested_smoke().supplied_runtime_operator_review_completion_summary.supplied_runtime_operator_review_completion_seal.supplied_runtime_operator_review_final_bundle.supplied_runtime_operator_review_final_packet.supplied_runtime_operator_review_queue_summary
    return replace(summary.supplied_runtime_operator_review_queue_entry, supplied_runtime_operator_review_queue_packet=queue)


def _queue_with_ack(ack):
    entry = _negative_nested_smoke().supplied_runtime_operator_review_completion_summary.supplied_runtime_operator_review_completion_seal.supplied_runtime_operator_review_final_bundle.supplied_runtime_operator_review_final_packet.supplied_runtime_operator_review_queue_summary.supplied_runtime_operator_review_queue_entry
    return replace(entry.supplied_runtime_operator_review_queue_packet, supplied_runtime_operator_review_ack_packet=ack)


def _ack_with_handoff(handoff):
    queue = _negative_nested_smoke().supplied_runtime_operator_review_completion_summary.supplied_runtime_operator_review_completion_seal.supplied_runtime_operator_review_final_bundle.supplied_runtime_operator_review_final_packet.supplied_runtime_operator_review_queue_summary.supplied_runtime_operator_review_queue_entry.supplied_runtime_operator_review_queue_packet
    return replace(queue.supplied_runtime_operator_review_ack_packet, supplied_runtime_operator_review_handoff=handoff)


def _handoff_with_trace(trace):
    ack = _negative_nested_smoke().supplied_runtime_operator_review_completion_summary.supplied_runtime_operator_review_completion_seal.supplied_runtime_operator_review_final_bundle.supplied_runtime_operator_review_final_packet.supplied_runtime_operator_review_queue_summary.supplied_runtime_operator_review_queue_entry.supplied_runtime_operator_review_queue_packet.supplied_runtime_operator_review_ack_packet
    return replace(ack.supplied_runtime_operator_review_handoff, supplied_runtime_trace_packet=trace)


def _trace_with_smoke(smoke):
    handoff = _negative_nested_smoke().supplied_runtime_operator_review_completion_summary.supplied_runtime_operator_review_completion_seal.supplied_runtime_operator_review_final_bundle.supplied_runtime_operator_review_final_packet.supplied_runtime_operator_review_queue_summary.supplied_runtime_operator_review_queue_entry.supplied_runtime_operator_review_queue_packet.supplied_runtime_operator_review_ack_packet.supplied_runtime_operator_review_handoff
    return replace(handoff.supplied_runtime_trace_packet, supplied_runtime_end_to_end_smoke=smoke)


def _smoke_with_report(report):
    trace = _negative_nested_smoke().supplied_runtime_operator_review_completion_summary.supplied_runtime_operator_review_completion_seal.supplied_runtime_operator_review_final_bundle.supplied_runtime_operator_review_final_packet.supplied_runtime_operator_review_queue_summary.supplied_runtime_operator_review_queue_entry.supplied_runtime_operator_review_queue_packet.supplied_runtime_operator_review_ack_packet.supplied_runtime_operator_review_handoff.supplied_runtime_trace_packet
    return replace(trace.supplied_runtime_end_to_end_smoke, supplied_runtime_dry_run_report=report)


def _report_with_dry(dry):
    smoke = _negative_nested_smoke().supplied_runtime_operator_review_completion_summary.supplied_runtime_operator_review_completion_seal.supplied_runtime_operator_review_final_bundle.supplied_runtime_operator_review_final_packet.supplied_runtime_operator_review_queue_summary.supplied_runtime_operator_review_queue_entry.supplied_runtime_operator_review_queue_packet.supplied_runtime_operator_review_ack_packet.supplied_runtime_operator_review_handoff.supplied_runtime_trace_packet.supplied_runtime_end_to_end_smoke
    return replace(smoke.supplied_runtime_dry_run_report, supplied_runtime_dry_run_packet=dry)


def _dry_with_validation(validation):
    report = _negative_nested_smoke().supplied_runtime_operator_review_completion_summary.supplied_runtime_operator_review_completion_seal.supplied_runtime_operator_review_final_bundle.supplied_runtime_operator_review_final_packet.supplied_runtime_operator_review_queue_summary.supplied_runtime_operator_review_queue_entry.supplied_runtime_operator_review_queue_packet.supplied_runtime_operator_review_ack_packet.supplied_runtime_operator_review_handoff.supplied_runtime_trace_packet.supplied_runtime_end_to_end_smoke.supplied_runtime_dry_run_report
    return replace(report.supplied_runtime_dry_run_packet, supplied_runtime_validation_bundle=validation)


def _validation_with_evidence(evidence):
    dry = _negative_nested_smoke().supplied_runtime_operator_review_completion_summary.supplied_runtime_operator_review_completion_seal.supplied_runtime_operator_review_final_bundle.supplied_runtime_operator_review_final_packet.supplied_runtime_operator_review_queue_summary.supplied_runtime_operator_review_queue_entry.supplied_runtime_operator_review_queue_packet.supplied_runtime_operator_review_ack_packet.supplied_runtime_operator_review_handoff.supplied_runtime_trace_packet.supplied_runtime_end_to_end_smoke.supplied_runtime_dry_run_report.supplied_runtime_dry_run_packet
    return replace(dry.supplied_runtime_validation_bundle, supplied_evidence_packet=evidence)


def _nested_from_bundle(bundle):
    return _with_summary(_summary_with_seal(_seal_with_bundle(bundle)))


def test_enums_are_closed_sets() -> None:
    assert bridge.FixtureOnlyFullChainNegativeSmokeBridgeStatus.values() == frozenset({"fixture_only_full_chain_negative_smoke_bridge_recorded", "fixture_only_full_chain_negative_smoke_bridge_missing", "fixture_only_full_chain_negative_smoke_bridge_ambiguous", "fixture_only_full_chain_negative_smoke_bridge_unsupported", "fixture_only_full_chain_negative_smoke_bridge_unknown"})
    assert bridge.FixtureOnlyFullChainNegativeSmokeBridgePosture.values() == frozenset({"fixture_only_full_chain_negative_smoke_bridge_in_memory_only", "fixture_only_full_chain_negative_smoke_bridge_missing", "fixture_only_full_chain_negative_smoke_bridge_ambiguous", "fixture_only_full_chain_negative_smoke_bridge_unsupported", "fixture_only_full_chain_negative_smoke_bridge_unknown"})
    assert bridge.FullChainNegativeSmokeBridgeAlignmentStatus.values() == frozenset({"full_chain_negative_smoke_bridge_aligned", "full_chain_negative_smoke_bridge_mismatch", "full_chain_negative_smoke_bridge_missing", "full_chain_negative_smoke_bridge_ambiguous", "full_chain_negative_smoke_bridge_unknown"})
    assert bridge.NoLookaheadStatus.values() == frozenset({"no_lookahead_recorded", "no_lookahead_missing", "no_lookahead_ambiguous", "no_lookahead_unknown"})
    assert bridge.OperatorReviewStatus.values() == frozenset({"operator_review_required", "operator_review_missing", "operator_review_ambiguous", "operator_review_not_required", "operator_review_unknown"})
    assert bridge.RuntimeGateStatus.values() == frozenset({"runtime_gate_blocked", "runtime_gate_ready", "runtime_gate_requires_manual_review", "runtime_gate_unknown"})
    assert bridge.ValidationSeverity.values() == frozenset({"passed", "caution", "failed", "blocked"})


def test_frozen_dataclass_construction() -> None:
    record = _valid_bridge_record(provenance_notes="caller supplied")
    assert isinstance(record.fixture_only_source_provider_full_chain_integration_smoke_bridge, positive_bridge_module.FixtureOnlySourceProviderFullChainIntegrationSmokeBridgeRecord)
    assert isinstance(record.supplied_runtime_full_chain_negative_smoke, negative_smoke_module.SuppliedRuntimeFullChainNegativeSmokeRecord)
    assert record.provenance_notes == "caller supplied"
    with pytest.raises(Exception):
        record.condition_id = "changed"


def test_mapping_construction_with_nested_mappings_and_string_enums() -> None:
    record = bridge.fixture_only_source_provider_full_chain_negative_smoke_bridge_record_from_mapping(asdict(_valid_bridge_record()))
    assert isinstance(record.fixture_only_source_provider_full_chain_integration_smoke_bridge, positive_bridge_module.FixtureOnlySourceProviderFullChainIntegrationSmokeBridgeRecord)
    assert isinstance(record.supplied_runtime_full_chain_negative_smoke, negative_smoke_module.SuppliedRuntimeFullChainNegativeSmokeRecord)
    assert record.runtime_gate_status is bridge.RuntimeGateStatus.RUNTIME_GATE_BLOCKED
    assert record.provenance_notes == ""


def test_correct_expected_failure_bridge_passes_while_gate_blocked() -> None:
    record = _valid_bridge_record()
    result = bridge.validate_fixture_only_source_provider_full_chain_negative_smoke_bridge_record(record)
    assert record.runtime_gate_status is bridge.RuntimeGateStatus.RUNTIME_GATE_BLOCKED
    assert result.passed is True
    assert result.severity is bridge.ValidationSeverity.PASSED
    assert result.reasons == ()


@pytest.mark.parametrize("field_name", ["condition_id", "token_id", "outcome", "full_chain_negative_smoke_bridge_id", "full_chain_negative_smoke_bridge_summary", "fixture_integration_smoke_bridge_summary", "supplied_negative_smoke_summary", "expected_failure_reason_summary", "observed_failure_reason_summary", "operator_review_summary", "blocked_reason_summary"])
def test_blank_required_text_fields_fail_closed(field_name: str) -> None:
    _assert_blocked_with_reason(_valid_bridge_record(**{field_name: "  "}), f"{field_name} is missing")


def test_invalid_positive_integration_smoke_bridge_fails_closed() -> None:
    invalid = _valid_integration_smoke_bridge(full_chain_integration_smoke_bridge_summary="")
    _assert_blocked_with_reason(_valid_bridge_record(fixture_only_source_provider_full_chain_integration_smoke_bridge=invalid), "fixture-only source provider full-chain integration-smoke bridge is invalid")


def test_invalid_supplied_negative_smoke_record_fails_closed() -> None:
    invalid = _valid_supplied_negative_smoke(negative_smoke_summary="")
    _assert_blocked_with_reason(_valid_bridge_record(supplied_runtime_full_chain_negative_smoke=invalid), "supplied runtime full-chain negative smoke is invalid")


def test_negative_smoke_with_unexpectedly_passing_nested_integration_smoke_fails_closed() -> None:
    passing = integration_base._valid_full_chain_integration_smoke()
    invalid_negative = _valid_supplied_negative_smoke(supplied_runtime_full_chain_integration_smoke=passing)
    _assert_blocked_with_reason(_valid_bridge_record(supplied_runtime_full_chain_negative_smoke=invalid_negative), "supplied runtime full-chain negative smoke is invalid")


@pytest.mark.parametrize(("field_name", "reason"), [("condition_id", "condition_id does not match fixture-only full-chain integration-smoke bridge"), ("token_id", "token_id does not match fixture-only full-chain integration-smoke bridge"), ("outcome", "outcome does not match fixture-only full-chain integration-smoke bridge")])
def test_top_level_route_mismatch_against_positive_bridge_fails_closed(field_name: str, reason: str) -> None:
    _assert_blocked_with_reason(_valid_bridge_record(**{field_name: "different"}), reason)


@pytest.mark.parametrize(("field_name", "reason"), [("condition_id", "condition_id does not match supplied runtime full-chain negative smoke"), ("token_id", "token_id does not match supplied runtime full-chain negative smoke"), ("outcome", "outcome does not match supplied runtime full-chain negative smoke")])
def test_top_level_route_mismatch_against_negative_smoke_fails_closed(field_name: str, reason: str) -> None:
    _assert_blocked_with_reason(_valid_bridge_record(supplied_runtime_full_chain_negative_smoke=_valid_supplied_negative_smoke(**{field_name: "different"})), reason)


def test_parent_positive_bridge_versus_negative_smoke_route_mismatch_fails_closed() -> None:
    _assert_blocked_with_reason(_valid_bridge_record(condition_id="different", supplied_runtime_full_chain_negative_smoke=_valid_supplied_negative_smoke(condition_id="different")), "nested fixture-only full-chain integration-smoke bridge and supplied runtime full-chain negative smoke routes do not match")


def test_positive_versus_negative_supplied_integration_smoke_route_mismatch_fails_closed() -> None:
    nested = replace(_negative_nested_smoke(), condition_id="different")
    _assert_blocked_with_reason(_valid_bridge_record(condition_id="different", supplied_runtime_full_chain_negative_smoke=_negative_with_nested(nested)), "nested supplied runtime full-chain integration smokes do not match")


@pytest.mark.parametrize(("nested", "reason"), [
    (_with_summary(integration_base._valid_operator_review_completion_summary(condition_id="different")), "nested supplied runtime operator-review completion summaries do not match"),
    (_with_summary(_summary_with_seal(integration_base._valid_operator_review_completion_seal(condition_id="different"))), "nested supplied runtime operator-review completion seals do not match"),
    (_nested_from_bundle(integration_base._valid_operator_review_final_bundle(condition_id="different")), "nested supplied runtime operator-review final bundles do not match"),
    (_nested_from_bundle(_bundle_with_packet(integration_base._valid_operator_review_final_packet(condition_id="different"))), "nested supplied runtime operator-review final packets do not match"),
    (_nested_from_bundle(_bundle_with_packet(_packet_with_summary(integration_base._valid_operator_review_queue_summary(condition_id="different")))), "nested supplied runtime operator-review queue summaries do not match"),
    (_nested_from_bundle(_bundle_with_packet(_packet_with_summary(_queue_summary_with_entry(integration_base._valid_operator_review_queue_entry(condition_id="different"))))), "nested supplied runtime operator-review queue entries do not match"),
    (_nested_from_bundle(_bundle_with_packet(_packet_with_summary(_queue_summary_with_entry(_entry_with_queue(integration_base._valid_operator_review_queue_packet(condition_id="different")))))), "nested supplied runtime operator-review queue packets do not match"),
    (_nested_from_bundle(_bundle_with_packet(_packet_with_summary(_queue_summary_with_entry(_entry_with_queue(_queue_with_ack(integration_base._valid_operator_review_ack_packet(condition_id="different"))))))), "nested supplied runtime operator-review ack packets do not match"),
    (_nested_from_bundle(_bundle_with_packet(_packet_with_summary(_queue_summary_with_entry(_entry_with_queue(_queue_with_ack(_ack_with_handoff(integration_base._valid_operator_review_handoff(condition_id="different")))))))), "nested supplied runtime operator-review handoffs do not match"),
    (_nested_from_bundle(_bundle_with_packet(_packet_with_summary(_queue_summary_with_entry(_entry_with_queue(_queue_with_ack(_ack_with_handoff(_handoff_with_trace(integration_base._valid_trace_packet(condition_id="different"))))))))), "nested supplied runtime trace packets do not match"),
    (_nested_from_bundle(_bundle_with_packet(_packet_with_summary(_queue_summary_with_entry(_entry_with_queue(_queue_with_ack(_ack_with_handoff(_handoff_with_trace(_trace_with_smoke(integration_base._valid_end_to_end_smoke(condition_id="different")))))))))), "nested supplied runtime end-to-end smokes do not match"),
    (_nested_from_bundle(_bundle_with_packet(_packet_with_summary(_queue_summary_with_entry(_entry_with_queue(_queue_with_ack(_ack_with_handoff(_handoff_with_trace(_trace_with_smoke(_smoke_with_report(integration_base._valid_dry_run_report(condition_id="different"))))))))))), "nested supplied runtime dry-run reports do not match"),
])
def test_nested_route_mismatches_fail_closed(nested, reason: str) -> None:
    _assert_blocked_with_reason(_valid_bridge_record(condition_id="different", supplied_runtime_full_chain_negative_smoke=_negative_with_nested(nested)), reason)


def _nested_with_validation(validation):
    dry = _dry_with_validation(validation)
    report = _report_with_dry(dry)
    end_smoke = _smoke_with_report(report)
    trace = _trace_with_smoke(end_smoke)
    handoff = _handoff_with_trace(trace)
    ack = _ack_with_handoff(handoff)
    queue = _queue_with_ack(ack)
    entry = _entry_with_queue(queue)
    queue_summary = _queue_summary_with_entry(entry)
    packet = _packet_with_summary(queue_summary)
    bundle = _bundle_with_packet(packet)
    return _nested_from_bundle(bundle)


def test_nested_dry_run_packet_and_validation_bundle_mismatch_fails_closed() -> None:
    validation = integration_base._valid_bundle(condition_id="different")
    nested = _nested_with_validation(validation)
    _assert_blocked_with_reason(_valid_bridge_record(condition_id="different", supplied_runtime_full_chain_negative_smoke=_negative_with_nested(nested)), "nested supplied runtime dry-run packets do not match")


def test_nested_evidence_packet_and_evidence_contract_mismatch_fails_closed() -> None:
    evidence = integration_base._valid_evidence_packet(condition_id="different", supplied_market_contract=integration_base._valid_contract(condition_id="different"))
    validation = _validation_with_evidence(evidence)
    nested = _nested_with_validation(validation)
    _assert_blocked_with_reason(_valid_bridge_record(condition_id="different", supplied_runtime_full_chain_negative_smoke=_negative_with_nested(nested)), "nested supplied evidence packets do not match")


def test_established_negative_smoke_fixture_with_intentional_nested_failure_passes_bridge() -> None:
    assert bridge.validate_fixture_only_source_provider_full_chain_negative_smoke_bridge_record(_valid_bridge_record()).passed is True


@pytest.mark.parametrize(("field_name", "reason"), [
    ("fixture_integration_smoke_bridge_summary", "fixture integration-smoke bridge summary does not match fixture-only full-chain integration-smoke bridge"),
    ("supplied_negative_smoke_summary", "supplied negative smoke summary does not match supplied runtime full-chain negative smoke"),
    ("expected_failure_reason_summary", "expected failure reason summary does not match supplied runtime full-chain negative smoke"),
    ("observed_failure_reason_summary", "observed failure reason summary does not match supplied runtime full-chain negative smoke"),
    ("operator_review_summary", "operator review summary does not match fixture-only full-chain integration-smoke bridge"),
    ("blocked_reason_summary", "blocked reason summary does not match supplied runtime full-chain negative smoke"),
])
def test_summary_mismatches_fail_closed(field_name: str, reason: str) -> None:
    _assert_blocked_with_reason(_valid_bridge_record(**{field_name: "different"}), reason)


@pytest.mark.parametrize("status", [value for value in bridge.FixtureOnlyFullChainNegativeSmokeBridgeStatus if value is not bridge.FixtureOnlyFullChainNegativeSmokeBridgeStatus.FIXTURE_ONLY_FULL_CHAIN_NEGATIVE_SMOKE_BRIDGE_RECORDED])
def test_every_non_recorded_bridge_status_fails_closed(status) -> None:
    _assert_blocked_with_reason(_valid_bridge_record(fixture_only_full_chain_negative_smoke_bridge_status=status), f"fixture-only full-chain negative-smoke bridge status is {status.value}")


@pytest.mark.parametrize("posture", [value for value in bridge.FixtureOnlyFullChainNegativeSmokeBridgePosture if value is not bridge.FixtureOnlyFullChainNegativeSmokeBridgePosture.FIXTURE_ONLY_FULL_CHAIN_NEGATIVE_SMOKE_BRIDGE_IN_MEMORY_ONLY])
def test_every_non_in_memory_bridge_posture_fails_closed(posture) -> None:
    _assert_blocked_with_reason(_valid_bridge_record(fixture_only_full_chain_negative_smoke_bridge_posture=posture), f"fixture-only full-chain negative-smoke bridge posture is {posture.value}")


@pytest.mark.parametrize("alignment", [value for value in bridge.FullChainNegativeSmokeBridgeAlignmentStatus if value is not bridge.FullChainNegativeSmokeBridgeAlignmentStatus.FULL_CHAIN_NEGATIVE_SMOKE_BRIDGE_ALIGNED])
def test_every_non_aligned_status_fails_closed(alignment) -> None:
    _assert_blocked_with_reason(_valid_bridge_record(full_chain_negative_smoke_bridge_alignment_status=alignment), f"full-chain negative-smoke bridge alignment status is {alignment.value}")


@pytest.mark.parametrize("status", [value for value in bridge.NoLookaheadStatus if value is not bridge.NoLookaheadStatus.NO_LOOKAHEAD_RECORDED])
def test_every_non_recorded_no_lookahead_status_fails_closed(status) -> None:
    _assert_blocked_with_reason(_valid_bridge_record(no_lookahead_status=status), f"no-lookahead status is {status.value}")


@pytest.mark.parametrize("status", [value for value in bridge.OperatorReviewStatus if value is not bridge.OperatorReviewStatus.OPERATOR_REVIEW_REQUIRED])
def test_every_non_required_operator_review_status_fails_closed(status) -> None:
    _assert_blocked_with_reason(_valid_bridge_record(operator_review_status=status), f"operator review status is {status.value}")


@pytest.mark.parametrize("status", [value for value in bridge.RuntimeGateStatus if value is not bridge.RuntimeGateStatus.RUNTIME_GATE_BLOCKED])
def test_every_runtime_gate_status_other_than_blocked_fails_closed(status) -> None:
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
        "requests", "httpx", "url" + "lib", "aiohttp", "boto3", "polymarket", "kalshi", "duckdb", "pandas", "sub" + "process", "open(", ".read" + "_text(", ".write" + "_text(", "socket", "os.environ", "dotenv", "place" + "_order", "paper" + "_trade", "trade", "back" + "test", "score", "execute" + "_order", "submit" + "_order", "persist", "data" + "base", "post" + "gres", "redis", "export", "write", "save", "owner" + "_decision", "capture" + "_decision", "operator" + "_decision", "execute" + "_decision", "celery", "rabbitmq", "sqs", "enqueue(", "dequeue(", "publish(", "subscribe(", "scheduler", "broker", "provider" + "_client", "api" + "_call", "scrape", "download", "credentials", "production", "simulate", "simulation", "generate" + "_report", "report" + "_writer", "generate" + "_summary", "summary" + "_writer", "finalize" + "_summary", "generate" + "_packet", "packet" + "_writer", "finalize" + "_packet", "generate" + "_bundle", "bundle" + "_writer", "finalize" + "_bundle", "generate" + "_seal", "seal" + "_writer", "finalize" + "_seal", "durable" + "_seal", "workflow" + "_completion", "complete" + "_workflow", "mark" + "_complete", "inject" + "_failure", "failure" + "_injection", "generate" + "_failure", "create" + "_failure", "generate" + "_smoke", "smoke" + "_generator", "execute" + "_smoke", "run" + "_smoke", "execute" + "_integration" + "_smoke", "run" + "_integration" + "_smoke", "integration" + "_smoke" + "_runner", "execute" + "_negative" + "_smoke", "run" + "_negative" + "_smoke", "negative" + "_smoke" + "_runner", "deliver" + "_integration" + "_smoke", "send" + "_integration" + "_smoke", "deliver" + "_negative" + "_smoke", "send" + "_negative" + "_smoke", "execute" + "_trace", "run" + "_trace", "deliver" + "_handoff", "send" + "_handoff", "deliver" + "_ack", "send" + "_ack", "deliver" + "_queue", "send" + "_queue", "deliver" + "_queue" + "_entry", "send" + "_queue" + "_entry", "deliver" + "_queue" + "_summary", "send" + "_queue" + "_summary", "deliver" + "_final" + "_packet", "send" + "_final" + "_packet", "deliver" + "_final" + "_bundle", "send" + "_final" + "_bundle", "deliver" + "_completion" + "_seal", "send" + "_completion" + "_seal", "deliver" + "_completion" + "_summary", "send" + "_completion" + "_summary", "queue" + "_service", "notification", "notify",
    ]
    assert {term for term in terms if term in source} == set()
