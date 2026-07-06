import ast
from dataclasses import asdict, replace
from pathlib import Path

import pytest

from meg.weather.stage2 import review_packet_evidence_composition_runtime as rpecr
from meg.weather.stage2 import supplied_evidence_packet_runtime as sepr
from meg.weather.stage2 import supplied_market_contract_runtime as smcr
from meg.weather.stage2 import supplied_market_review_packet_runtime as smrpr
from meg.weather.stage2 import supplied_runtime_dry_run_report as srdr
from meg.weather.stage2 import supplied_runtime_dry_run_packet as srdp
from meg.weather.stage2 import supplied_runtime_end_to_end_smoke as sees
from meg.weather.stage2 import supplied_runtime_full_chain_integration_smoke as sfcis
from meg.weather.stage2 import supplied_runtime_full_chain_negative_smoke as sfcns
from meg.weather.stage2 import supplied_runtime_operator_review_completion_summary as socsum
from meg.weather.stage2 import supplied_runtime_operator_review_completion_seal as socs
from meg.weather.stage2 import supplied_runtime_operator_review_final_bundle as sofb
from meg.weather.stage2 import supplied_runtime_operator_review_final_packet as sofp
from meg.weather.stage2 import supplied_runtime_operator_review_queue_summary as soqs
from meg.weather.stage2 import supplied_runtime_operator_review_queue_entry as soqe
from meg.weather.stage2 import supplied_runtime_operator_review_queue_packet as soqp
from meg.weather.stage2 import supplied_runtime_operator_review_ack_packet as soap
from meg.weather.stage2 import supplied_runtime_operator_review_handoff as sroh
from meg.weather.stage2 import supplied_runtime_trace_packet as srtp
from meg.weather.stage2 import supplied_runtime_validation_bundle as srvb
from tests.core import test_weather_supplied_runtime_full_chain_integration_smoke as base


MODULE_PATH = Path("meg/weather/stage2/supplied_runtime_full_chain_negative_smoke.py")
TEST_PATH = Path("tests/core/test_weather_supplied_runtime_full_chain_negative_smoke.py")


def _valid_contract(**overrides: object) -> smcr.SuppliedMarketContractRecord:
    return base._valid_contract(**overrides)


def _valid_review_packet(**overrides: object) -> smrpr.SuppliedMarketReviewPacketRecord:
    return base._valid_review_packet(**overrides)


def _valid_evidence_packet(**overrides: object) -> sepr.SuppliedEvidencePacketRecord:
    return base._valid_evidence_packet(**overrides)


def _valid_composition(**overrides: object) -> rpecr.ReviewPacketEvidenceCompositionRecord:
    return base._valid_composition(**overrides)


def _valid_bundle(**overrides: object) -> srvb.SuppliedRuntimeValidationBundleRecord:
    return base._valid_bundle(**overrides)


def _valid_dry_run_packet(**overrides: object) -> srdp.SuppliedRuntimeDryRunPacketRecord:
    return base._valid_dry_run_packet(**overrides)


def _valid_dry_run_report(**overrides: object) -> srdr.SuppliedRuntimeDryRunReportRecord:
    return base._valid_dry_run_report(**overrides)


def _valid_end_to_end_smoke(**overrides: object) -> sees.SuppliedRuntimeEndToEndSmokeRecord:
    return base._valid_end_to_end_smoke(**overrides)


def _valid_trace_packet(**overrides: object) -> srtp.SuppliedRuntimeTracePacketRecord:
    return base._valid_trace_packet(**overrides)


def _valid_operator_review_handoff(**overrides: object) -> sroh.SuppliedRuntimeOperatorReviewHandoffRecord:
    return base._valid_operator_review_handoff(**overrides)


def _valid_operator_review_ack_packet(**overrides: object) -> soap.SuppliedRuntimeOperatorReviewAckPacketRecord:
    return base._valid_operator_review_ack_packet(**overrides)


def _valid_operator_review_queue_packet(**overrides: object) -> soqp.SuppliedRuntimeOperatorReviewQueuePacketRecord:
    return base._valid_operator_review_queue_packet(**overrides)


def _valid_operator_review_queue_entry(**overrides: object) -> soqe.SuppliedRuntimeOperatorReviewQueueEntryRecord:
    return base._valid_operator_review_queue_entry(**overrides)


def _valid_operator_review_queue_summary(**overrides: object) -> soqs.SuppliedRuntimeOperatorReviewQueueSummaryRecord:
    return base._valid_operator_review_queue_summary(**overrides)


def _valid_operator_review_final_packet(**overrides: object) -> sofp.SuppliedRuntimeOperatorReviewFinalPacketRecord:
    return base._valid_operator_review_final_packet(**overrides)


def _valid_operator_review_final_bundle(**overrides: object) -> sofb.SuppliedRuntimeOperatorReviewFinalBundleRecord:
    return base._valid_operator_review_final_bundle(**overrides)


def _valid_operator_review_completion_seal(**overrides: object) -> socs.SuppliedRuntimeOperatorReviewCompletionSealRecord:
    return base._valid_operator_review_completion_seal(**overrides)


def _valid_operator_review_completion_summary(**overrides: object) -> socsum.SuppliedRuntimeOperatorReviewCompletionSummaryRecord:
    return base._valid_operator_review_completion_summary(**overrides)


def _valid_full_chain_integration_smoke(**overrides: object) -> sfcis.SuppliedRuntimeFullChainIntegrationSmokeRecord:
    return base._valid_full_chain_integration_smoke(**overrides)


def _invalid_full_chain_integration_smoke_with_nested_contract_failure() -> sfcis.SuppliedRuntimeFullChainIntegrationSmokeRecord:
    invalid_summary = _valid_operator_review_completion_summary(
        supplied_runtime_operator_review_completion_seal=_valid_operator_review_completion_seal(
            supplied_runtime_operator_review_final_bundle=_valid_operator_review_final_bundle(
                supplied_runtime_operator_review_final_packet=_valid_operator_review_final_packet(
                    supplied_runtime_operator_review_queue_summary=_valid_operator_review_queue_summary(
                        supplied_runtime_operator_review_queue_entry=_valid_operator_review_queue_entry(
                            supplied_runtime_operator_review_queue_packet=_valid_operator_review_queue_packet(
                                supplied_runtime_operator_review_ack_packet=_valid_operator_review_ack_packet(
                                    supplied_runtime_operator_review_handoff=_valid_operator_review_handoff(
                                        supplied_runtime_trace_packet=_valid_trace_packet(
                                            supplied_runtime_end_to_end_smoke=_valid_end_to_end_smoke(
                                                supplied_runtime_dry_run_report=_valid_dry_run_report(
                                                    supplied_runtime_dry_run_packet=_valid_dry_run_packet(
                                                        supplied_runtime_validation_bundle=_valid_bundle(
                                                            supplied_market_contract=_valid_contract(condition_id=" ")
                                                        )
                                                    )
                                                )
                                            )
                                        )
                                    )
                                )
                            )
                        )
                    )
                )
            )
        )
    )
    return _valid_full_chain_integration_smoke(
        supplied_runtime_operator_review_completion_summary=invalid_summary,
        blocked_reason_summary="Nested contract failure is expected for this negative smoke.",
    )


def _valid_full_chain_negative_smoke(**overrides: object) -> sfcns.SuppliedRuntimeFullChainNegativeSmokeRecord:
    nested = overrides.pop(
        "supplied_runtime_full_chain_integration_smoke",
        _invalid_full_chain_integration_smoke_with_nested_contract_failure(),
    )
    nested_result = sfcis.validate_supplied_runtime_full_chain_integration_smoke_record(nested)
    observed_reason = nested_result.reasons[0] if nested_result.reasons else "no nested reason"
    values = {
        "condition_id": "condition-1",
        "token_id": "token-1",
        "outcome": "Yes",
        "supplied_runtime_full_chain_integration_smoke": nested,
        "negative_smoke_id": "negative-smoke-1",
        "negative_smoke_summary": "Caller supplied negative smoke summary text.",
        "expected_failure_reason_summary": "Expected nested full-chain integration smoke to fail closed.",
        "observed_failure_reason_summary": f"Observed nested reason: {observed_reason}",
        "blocked_reason_summary": "Runtime gate remains blocked for the negative smoke.",
        "full_chain_negative_smoke_status": sfcns.FullChainNegativeSmokeStatus.FULL_CHAIN_NEGATIVE_SMOKE_RECORDED,
        "full_chain_negative_smoke_outcome_status": sfcns.FullChainNegativeSmokeOutcomeStatus.EXPECTED_FAIL_CLOSED_OBSERVED,
        "full_chain_negative_smoke_posture": sfcns.FullChainNegativeSmokePosture.FULL_CHAIN_NEGATIVE_SMOKE_IN_MEMORY_ONLY,
        "operator_review_status": sfcns.OperatorReviewStatus.OPERATOR_REVIEW_REQUIRED,
        "runtime_gate_status": sfcns.RuntimeGateStatus.RUNTIME_GATE_BLOCKED,
    }
    values.update(overrides)
    return sfcns.SuppliedRuntimeFullChainNegativeSmokeRecord(**values)


def _assert_blocked_with_reason(record: sfcns.SuppliedRuntimeFullChainNegativeSmokeRecord, reason: str) -> None:
    result = sfcns.validate_supplied_runtime_full_chain_negative_smoke_record(record)
    assert result.passed is False
    assert result.severity is sfcns.ValidationSeverity.BLOCKED
    assert reason in result.reasons


def test_enums_are_closed_sets() -> None:
    assert sfcns.FullChainNegativeSmokeStatus.values() == frozenset({
        "full_chain_negative_smoke_recorded",
        "full_chain_negative_smoke_missing",
        "full_chain_negative_smoke_ambiguous",
        "full_chain_negative_smoke_unsupported",
        "full_chain_negative_smoke_unknown",
    })
    assert sfcns.FullChainNegativeSmokeOutcomeStatus.values() == frozenset({
        "expected_fail_closed_observed",
        "expected_fail_closed_missing",
        "expected_fail_closed_ambiguous",
        "expected_fail_closed_unsupported",
        "expected_fail_closed_unknown",
    })
    assert sfcns.FullChainNegativeSmokePosture.values() == frozenset({
        "full_chain_negative_smoke_in_memory_only",
        "full_chain_negative_smoke_missing",
        "full_chain_negative_smoke_ambiguous",
        "full_chain_negative_smoke_unsupported",
        "full_chain_negative_smoke_unknown",
    })
    assert sfcns.OperatorReviewStatus.values() == frozenset({
        "operator_review_required",
        "operator_review_missing",
        "operator_review_ambiguous",
        "operator_review_not_required",
        "operator_review_unknown",
    })
    assert sfcns.RuntimeGateStatus.values() == frozenset({
        "runtime_gate_blocked",
        "runtime_gate_ready",
        "runtime_gate_requires_manual_review",
        "runtime_gate_unknown",
    })
    assert sfcns.ValidationSeverity.values() == frozenset({"passed", "caution", "failed", "blocked"})


def test_dataclass_construction() -> None:
    record = _valid_full_chain_negative_smoke(provenance_notes="operator supplied negative smoke")
    assert record.condition_id == "condition-1"
    assert record.token_id == "token-1"
    assert record.outcome == "Yes"
    assert isinstance(record.supplied_runtime_full_chain_integration_smoke, sfcis.SuppliedRuntimeFullChainIntegrationSmokeRecord)
    assert record.full_chain_negative_smoke_status is sfcns.FullChainNegativeSmokeStatus.FULL_CHAIN_NEGATIVE_SMOKE_RECORDED
    assert record.provenance_notes == "operator supplied negative smoke"


def test_mapping_construction_coerces_string_enums_and_nested_full_chain_integration_smoke_mapping() -> None:
    record = sfcns.supplied_runtime_full_chain_negative_smoke_record_from_mapping({
        "condition_id": "condition-1",
        "token_id": "token-1",
        "outcome": "Yes",
        "supplied_runtime_full_chain_integration_smoke": asdict(_invalid_full_chain_integration_smoke_with_nested_contract_failure()),
        "negative_smoke_id": "negative-smoke-2",
        "negative_smoke_summary": "Caller supplied negative smoke summary text.",
        "expected_failure_reason_summary": "Expected nested full-chain integration smoke to fail closed.",
        "observed_failure_reason_summary": "Observed nested reason: supplied runtime operator-review completion summary validation failed",
        "blocked_reason_summary": "Runtime gate remains blocked for the negative smoke.",
        "full_chain_negative_smoke_status": "full_chain_negative_smoke_recorded",
        "full_chain_negative_smoke_outcome_status": "expected_fail_closed_observed",
        "full_chain_negative_smoke_posture": "full_chain_negative_smoke_in_memory_only",
        "operator_review_status": "operator_review_required",
        "runtime_gate_status": "runtime_gate_blocked",
    })
    assert record.full_chain_negative_smoke_outcome_status is sfcns.FullChainNegativeSmokeOutcomeStatus.EXPECTED_FAIL_CLOSED_OBSERVED
    assert isinstance(record.supplied_runtime_full_chain_integration_smoke, sfcis.SuppliedRuntimeFullChainIntegrationSmokeRecord)


def test_valid_negative_smoke_passes_when_nested_full_chain_integration_smoke_fails_closed_as_expected() -> None:
    result = sfcns.validate_supplied_runtime_full_chain_negative_smoke_record(_valid_full_chain_negative_smoke())
    assert result.passed is True
    assert result.severity is sfcns.ValidationSeverity.PASSED
    assert result.reasons == ()


def test_negative_smoke_blocks_when_nested_full_chain_integration_smoke_unexpectedly_passes() -> None:
    _assert_blocked_with_reason(
        _valid_full_chain_negative_smoke(
            supplied_runtime_full_chain_integration_smoke=_valid_full_chain_integration_smoke(),
            observed_failure_reason_summary="No nested reason was observed.",
        ),
        "supplied runtime full-chain integration smoke unexpectedly passed",
    )


def test_negative_smoke_blocks_when_nested_full_chain_integration_smoke_has_no_reasons() -> None:
    record = _valid_full_chain_negative_smoke()
    nested = record.supplied_runtime_full_chain_integration_smoke
    nested = replace(nested, supplied_runtime_operator_review_completion_summary=_valid_operator_review_completion_summary())
    record = replace(record, supplied_runtime_full_chain_integration_smoke=nested)
    _assert_blocked_with_reason(record, "supplied runtime full-chain integration smoke did not report reasons")


@pytest.mark.parametrize("field_name", [
    "condition_id",
    "token_id",
    "outcome",
    "negative_smoke_id",
    "negative_smoke_summary",
    "expected_failure_reason_summary",
    "observed_failure_reason_summary",
    "blocked_reason_summary",
])
def test_blank_required_text_field_fails_closed(field_name: str) -> None:
    _assert_blocked_with_reason(replace(_valid_full_chain_negative_smoke(), **{field_name: " "}), f"{field_name} is missing")


def test_condition_id_mismatch_with_supplied_runtime_full_chain_integration_smoke_fails_closed() -> None:
    _assert_blocked_with_reason(replace(_valid_full_chain_negative_smoke(), condition_id="condition-2"), "condition_id does not match supplied runtime full-chain integration smoke")


def test_token_id_mismatch_with_supplied_runtime_full_chain_integration_smoke_fails_closed() -> None:
    _assert_blocked_with_reason(replace(_valid_full_chain_negative_smoke(), token_id="token-2"), "token_id does not match supplied runtime full-chain integration smoke")


def test_outcome_mismatch_with_supplied_runtime_full_chain_integration_smoke_fails_closed() -> None:
    _assert_blocked_with_reason(replace(_valid_full_chain_negative_smoke(), outcome="No"), "outcome does not match supplied runtime full-chain integration smoke")


def test_observed_failure_reason_summary_must_include_nested_integration_smoke_reason() -> None:
    _assert_blocked_with_reason(replace(_valid_full_chain_negative_smoke(), observed_failure_reason_summary="Different supplied observation."), "observed_failure_reason_summary does not include a nested integration smoke reason")


@pytest.mark.parametrize("status", [s for s in sfcns.FullChainNegativeSmokeStatus if s is not sfcns.FullChainNegativeSmokeStatus.FULL_CHAIN_NEGATIVE_SMOKE_RECORDED])
def test_non_recorded_full_chain_negative_smoke_statuses_fail_closed(status: sfcns.FullChainNegativeSmokeStatus) -> None:
    _assert_blocked_with_reason(replace(_valid_full_chain_negative_smoke(), full_chain_negative_smoke_status=status), f"full chain negative smoke status is {status.value}")


@pytest.mark.parametrize("status", [s for s in sfcns.FullChainNegativeSmokeOutcomeStatus if s is not sfcns.FullChainNegativeSmokeOutcomeStatus.EXPECTED_FAIL_CLOSED_OBSERVED])
def test_non_observed_expected_fail_closed_outcome_statuses_fail_closed(status: sfcns.FullChainNegativeSmokeOutcomeStatus) -> None:
    _assert_blocked_with_reason(replace(_valid_full_chain_negative_smoke(), full_chain_negative_smoke_outcome_status=status), f"full chain negative smoke outcome status is {status.value}")


@pytest.mark.parametrize("posture", [p for p in sfcns.FullChainNegativeSmokePosture if p is not sfcns.FullChainNegativeSmokePosture.FULL_CHAIN_NEGATIVE_SMOKE_IN_MEMORY_ONLY])
def test_non_in_memory_only_full_chain_negative_smoke_postures_fail_closed(posture: sfcns.FullChainNegativeSmokePosture) -> None:
    _assert_blocked_with_reason(replace(_valid_full_chain_negative_smoke(), full_chain_negative_smoke_posture=posture), f"full chain negative smoke posture is {posture.value}")


@pytest.mark.parametrize("status", [s for s in sfcns.OperatorReviewStatus if s is not sfcns.OperatorReviewStatus.OPERATOR_REVIEW_REQUIRED])
def test_non_required_operator_review_statuses_fail_closed(status: sfcns.OperatorReviewStatus) -> None:
    _assert_blocked_with_reason(replace(_valid_full_chain_negative_smoke(), operator_review_status=status), f"operator review status is {status.value}")


@pytest.mark.parametrize("status", [s for s in sfcns.RuntimeGateStatus if s is not sfcns.RuntimeGateStatus.RUNTIME_GATE_BLOCKED])
def test_non_blocked_runtime_gate_statuses_fail_closed(status: sfcns.RuntimeGateStatus) -> None:
    _assert_blocked_with_reason(replace(_valid_full_chain_negative_smoke(), runtime_gate_status=status), f"runtime gate status is {status.value}")


def _source_without_docstrings(source: str) -> str:
    parsed = ast.parse(source)
    for node in ast.walk(parsed):
        if not isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        if node.body and isinstance(node.body[0], ast.Expr) and isinstance(node.body[0].value, ast.Constant) and isinstance(node.body[0].value.value, str):
            node.body[0] = ast.Pass()
    return ast.unparse(parsed)


def test_new_module_and_new_test_do_not_contain_noncanonical_identifier_literal() -> None:
    forbidden = "market" + "_id"
    assert forbidden not in MODULE_PATH.read_text()
    assert forbidden not in TEST_PATH.read_text()


def test_new_module_source_has_no_forbidden_runtime_terms() -> None:
    source = _source_without_docstrings(MODULE_PATH.read_text())
    forbidden_terms = (
        "requests", "httpx", "urllib", "aiohttp", "boto3", "polymarket", "kalshi",
        "duckdb", "pandas", "subprocess", "open(", ".read_text(", ".write_text(",
        "socket", "os.environ", "dotenv", "place_order", "paper_trade", "trade",
        "backtest", "score", "execute_order", "submit_order", "persist", "database",
        "postgres", "redis", "export", "write", "save", "owner_decision",
        "capture_decision", "celery", "rabbitmq", "sqs", "enqueue(", "dequeue(",
        "publish(", "subscribe(", "scheduler", "generate_summary", "summarize(",
        "approve", "reject", "decide", "complete_workflow", "seal_state", "durable",
    )
    assert [term for term in forbidden_terms if term in source] == []
