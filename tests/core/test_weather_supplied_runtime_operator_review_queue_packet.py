import ast
from dataclasses import asdict
from pathlib import Path

import pytest

from meg.weather.stage2 import review_packet_evidence_composition_runtime as rpecr
from meg.weather.stage2 import supplied_evidence_packet_runtime as sepr
from meg.weather.stage2 import supplied_market_contract_runtime as smcr
from meg.weather.stage2 import supplied_market_review_packet_runtime as smrpr
from meg.weather.stage2 import supplied_runtime_dry_run_report as srdr
from meg.weather.stage2 import supplied_runtime_dry_run_packet as srdp
from meg.weather.stage2 import supplied_runtime_end_to_end_smoke as sees
from meg.weather.stage2 import supplied_runtime_operator_review_queue_packet as soqp
from meg.weather.stage2 import supplied_runtime_operator_review_ack_packet as soap
from meg.weather.stage2 import supplied_runtime_operator_review_handoff as sroh
from meg.weather.stage2 import supplied_runtime_trace_packet as srtp
from meg.weather.stage2 import supplied_runtime_validation_bundle as srvb


MODULE_PATH = Path("meg/weather/stage2/supplied_runtime_operator_review_queue_packet.py")
TEST_PATH = Path("tests/core/test_weather_supplied_runtime_operator_review_queue_packet.py")


def _valid_contract(**overrides: object) -> smcr.SuppliedMarketContractRecord:
    values = {
        "condition_id": "condition-1",
        "token_id": "token-1",
        "outcome": "Yes",
        "market_title": "Will this settlement rule resolve yes?",
        "settlement_rule": "Resolves Yes if the supplied event condition is met.",
        "event_start_utc": "2026-01-01T00:00:00Z",
        "event_end_utc": "2026-01-02T00:00:00Z",
        "settlement_rule_status": smcr.SettlementRuleStatus.SETTLEMENT_RULE_RECORDED,
        "market_contract_status": smcr.MarketContractStatus.MARKET_CONTRACT_RECORDED,
        "event_timing_status": smcr.EventTimingStatus.EVENT_TIMING_RECORDED,
        "runtime_gate_status": smcr.RuntimeGateStatus.RUNTIME_GATE_READY,
    }
    values.update(overrides)
    return smcr.SuppliedMarketContractRecord(**values)


def _valid_review_packet(**overrides: object) -> smrpr.SuppliedMarketReviewPacketRecord:
    values = {
        "condition_id": "condition-1",
        "token_id": "token-1",
        "outcome": "Yes",
        "supplied_market_contract": _valid_contract(),
        "review_packet_id": "review-packet-1",
        "review_summary": "Caller supplied review summary text.",
        "evidence_summary": "Caller supplied evidence summary text.",
        "blocked_reason_summary": "",
        "review_packet_status": smrpr.ReviewPacketStatus.REVIEW_PACKET_RECORDED,
        "review_recommendation_status": (
            smrpr.ReviewRecommendationStatus.REVIEW_RECOMMENDATION_READY
        ),
        "evidence_summary_status": smrpr.EvidenceSummaryStatus.EVIDENCE_SUMMARY_RECORDED,
        "runtime_gate_status": smrpr.RuntimeGateStatus.RUNTIME_GATE_READY,
    }
    values.update(overrides)
    return smrpr.SuppliedMarketReviewPacketRecord(**values)


def _valid_evidence_packet(**overrides: object) -> sepr.SuppliedEvidencePacketRecord:
    values = {
        "condition_id": "condition-1",
        "token_id": "token-1",
        "outcome": "Yes",
        "supplied_market_contract": _valid_contract(),
        "evidence_packet_id": "evidence-packet-1",
        "evidence_summary": "Caller supplied evidence summary text.",
        "evidence_source_descriptor": "Caller supplied manual evidence descriptor.",
        "evidence_observed_at_utc": "2026-01-01T12:00:00Z",
        "evidence_available_at_utc": "2026-01-01T12:05:00Z",
        "decision_time_utc": "2026-01-01T12:10:00Z",
        "evidence_packet_status": sepr.EvidencePacketStatus.EVIDENCE_PACKET_RECORDED,
        "evidence_freshness_status": sepr.EvidenceFreshnessStatus.EVIDENCE_FRESHNESS_RECORDED,
        "evidence_availability_status": (
            sepr.EvidenceAvailabilityStatus.EVIDENCE_AVAILABLE_BEFORE_DECISION
        ),
        "evidence_source_posture": sepr.EvidenceSourcePosture.CALLER_SUPPLIED_STATIC_EVIDENCE,
        "runtime_gate_status": sepr.RuntimeGateStatus.RUNTIME_GATE_READY,
    }
    values.update(overrides)
    return sepr.SuppliedEvidencePacketRecord(**values)


def _valid_composition(
    **overrides: object,
) -> rpecr.ReviewPacketEvidenceCompositionRecord:
    values = {
        "condition_id": "condition-1",
        "token_id": "token-1",
        "outcome": "Yes",
        "supplied_market_review_packet": _valid_review_packet(),
        "supplied_evidence_packet": _valid_evidence_packet(),
        "composition_id": "composition-1",
        "composition_summary": "Caller supplied composition summary text.",
        "composition_status": rpecr.CompositionStatus.COMPOSITION_RECORDED,
        "evidence_review_alignment_status": (
            rpecr.EvidenceReviewAlignmentStatus.EVIDENCE_REVIEW_ALIGNED
        ),
        "runtime_gate_status": rpecr.RuntimeGateStatus.RUNTIME_GATE_READY,
    }
    values.update(overrides)
    return rpecr.ReviewPacketEvidenceCompositionRecord(**values)


def _valid_bundle(**overrides: object) -> srvb.SuppliedRuntimeValidationBundleRecord:
    values = {
        "condition_id": "condition-1",
        "token_id": "token-1",
        "outcome": "Yes",
        "supplied_market_contract": _valid_contract(),
        "supplied_market_review_packet": _valid_review_packet(),
        "supplied_evidence_packet": _valid_evidence_packet(),
        "review_packet_evidence_composition": _valid_composition(),
        "validation_bundle_id": "validation-bundle-1",
        "validation_summary": "Caller supplied validation summary text.",
        "runtime_validation_bundle_status": (
            srvb.RuntimeValidationBundleStatus.RUNTIME_VALIDATION_BUNDLE_RECORDED
        ),
        "runtime_validation_completeness_status": (
            srvb.RuntimeValidationCompletenessStatus.RUNTIME_VALIDATION_COMPLETE
        ),
        "runtime_gate_status": srvb.RuntimeGateStatus.RUNTIME_GATE_READY,
    }
    values.update(overrides)
    return srvb.SuppliedRuntimeValidationBundleRecord(**values)


def _valid_dry_run_packet(
    **overrides: object,
) -> srdp.SuppliedRuntimeDryRunPacketRecord:
    values = {
        "condition_id": "condition-1",
        "token_id": "token-1",
        "outcome": "Yes",
        "supplied_runtime_validation_bundle": _valid_bundle(),
        "dry_run_packet_id": "dry-run-packet-1",
        "dry_run_summary": "Caller supplied dry-run summary text.",
        "operator_review_summary": "Operator review is required before any later action.",
        "blocked_reason_summary": "",
        "dry_run_packet_status": srdp.DryRunPacketStatus.DRY_RUN_PACKET_RECORDED,
        "dry_run_recommendation_status": (
            srdp.DryRunRecommendationStatus.DRY_RUN_RECOMMENDATION_READY
        ),
        "operator_review_status": srdp.OperatorReviewStatus.OPERATOR_REVIEW_REQUIRED,
        "runtime_gate_status": srdp.RuntimeGateStatus.RUNTIME_GATE_READY,
    }
    values.update(overrides)
    return srdp.SuppliedRuntimeDryRunPacketRecord(**values)



def _valid_dry_run_report(
    **overrides: object,
) -> srdr.SuppliedRuntimeDryRunReportRecord:
    values = {
        "condition_id": "condition-1",
        "token_id": "token-1",
        "outcome": "Yes",
        "supplied_runtime_dry_run_packet": _valid_dry_run_packet(),
        "dry_run_report_id": "dry-run-report-1",
        "report_summary": "Caller supplied dry-run report summary text.",
        "operator_review_summary": "Operator review is required before any later action.",
        "blocked_reason_summary": "",
        "dry_run_report_status": srdr.DryRunReportStatus.DRY_RUN_REPORT_RECORDED,
        "dry_run_report_completeness_status": (
            srdr.DryRunReportCompletenessStatus.DRY_RUN_REPORT_COMPLETE
        ),
        "operator_review_status": srdr.OperatorReviewStatus.OPERATOR_REVIEW_REQUIRED,
        "runtime_gate_status": srdr.RuntimeGateStatus.RUNTIME_GATE_READY,
    }
    values.update(overrides)
    return srdr.SuppliedRuntimeDryRunReportRecord(**values)




def _valid_end_to_end_smoke(
    **overrides: object,
) -> sees.SuppliedRuntimeEndToEndSmokeRecord:
    values = {
        "condition_id": "condition-1",
        "token_id": "token-1",
        "outcome": "Yes",
        "supplied_runtime_dry_run_report": _valid_dry_run_report(),
        "smoke_id": "smoke-1",
        "smoke_summary": "Caller supplied end-to-end smoke summary text.",
        "operator_review_summary": "Operator review is required before any later action.",
        "blocked_reason_summary": "",
        "end_to_end_smoke_status": sees.EndToEndSmokeStatus.END_TO_END_SMOKE_RECORDED,
        "end_to_end_smoke_completeness_status": (
            sees.EndToEndSmokeCompletenessStatus.END_TO_END_SMOKE_COMPLETE
        ),
        "operator_review_status": sees.OperatorReviewStatus.OPERATOR_REVIEW_REQUIRED,
        "runtime_gate_status": sees.RuntimeGateStatus.RUNTIME_GATE_READY,
    }
    values.update(overrides)
    return sees.SuppliedRuntimeEndToEndSmokeRecord(**values)


def _valid_trace_packet(
    **overrides: object,
) -> srtp.SuppliedRuntimeTracePacketRecord:
    values = {
        "condition_id": "condition-1",
        "token_id": "token-1",
        "outcome": "Yes",
        "supplied_runtime_end_to_end_smoke": _valid_end_to_end_smoke(),
        "trace_packet_id": "trace-packet-1",
        "trace_summary": "Caller supplied runtime trace packet summary text.",
        "operator_review_summary": "Operator review is required before any later action.",
        "blocked_reason_summary": "",
        "runtime_trace_packet_status": (
            srtp.RuntimeTracePacketStatus.RUNTIME_TRACE_PACKET_RECORDED
        ),
        "runtime_trace_completeness_status": (
            srtp.RuntimeTraceCompletenessStatus.RUNTIME_TRACE_COMPLETE
        ),
        "operator_review_status": srtp.OperatorReviewStatus.OPERATOR_REVIEW_REQUIRED,
        "runtime_gate_status": srtp.RuntimeGateStatus.RUNTIME_GATE_READY,
    }
    values.update(overrides)
    return srtp.SuppliedRuntimeTracePacketRecord(**values)



def _valid_operator_review_handoff(
    **overrides: object,
) -> sroh.SuppliedRuntimeOperatorReviewHandoffRecord:
    values = {
        "condition_id": "condition-1",
        "token_id": "token-1",
        "outcome": "Yes",
        "supplied_runtime_trace_packet": _valid_trace_packet(),
        "handoff_id": "handoff-1",
        "handoff_summary": "Caller supplied operator-review handoff summary text.",
        "operator_review_summary": "Operator review is required before any later action.",
        "blocked_reason_summary": "",
        "operator_review_handoff_status": (
            sroh.OperatorReviewHandoffStatus.OPERATOR_REVIEW_HANDOFF_RECORDED
        ),
        "operator_review_handoff_completeness_status": (
            sroh.OperatorReviewHandoffCompletenessStatus.OPERATOR_REVIEW_HANDOFF_COMPLETE
        ),
        "operator_review_status": sroh.OperatorReviewStatus.OPERATOR_REVIEW_REQUIRED,
        "runtime_gate_status": sroh.RuntimeGateStatus.RUNTIME_GATE_READY,
    }
    values.update(overrides)
    return sroh.SuppliedRuntimeOperatorReviewHandoffRecord(**values)


def _valid_operator_review_ack_packet(
    **overrides: object,
) -> soap.SuppliedRuntimeOperatorReviewAckPacketRecord:
    values = {
        "condition_id": "condition-1",
        "token_id": "token-1",
        "outcome": "Yes",
        "supplied_runtime_operator_review_handoff": _valid_operator_review_handoff(),
        "ack_packet_id": "ack-packet-1",
        "ack_summary": "Caller supplied operator-review ack packet summary text.",
        "operator_review_summary": "Operator review is required before any later action.",
        "blocked_reason_summary": "",
        "operator_review_ack_packet_status": (
            soap.OperatorReviewAckPacketStatus.OPERATOR_REVIEW_ACK_PACKET_RECORDED
        ),
        "operator_review_ack_completeness_status": (
            soap.OperatorReviewAckCompletenessStatus.OPERATOR_REVIEW_ACK_COMPLETE
        ),
        "operator_review_status": soap.OperatorReviewStatus.OPERATOR_REVIEW_REQUIRED,
        "runtime_gate_status": soap.RuntimeGateStatus.RUNTIME_GATE_READY,
    }
    values.update(overrides)
    return soap.SuppliedRuntimeOperatorReviewAckPacketRecord(**values)



def _valid_operator_review_queue_packet(
    **overrides: object,
) -> soqp.SuppliedRuntimeOperatorReviewQueuePacketRecord:
    values = {
        "condition_id": "condition-1",
        "token_id": "token-1",
        "outcome": "Yes",
        "supplied_runtime_operator_review_ack_packet": _valid_operator_review_ack_packet(),
        "queue_packet_id": "queue-packet-1",
        "queue_summary": "Caller supplied operator-review queue packet summary text.",
        "operator_review_summary": "Operator review is required before any later action.",
        "blocked_reason_summary": "",
        "operator_review_queue_packet_status": (
            soqp.OperatorReviewQueuePacketStatus.OPERATOR_REVIEW_QUEUE_PACKET_RECORDED
        ),
        "operator_review_queue_completeness_status": (
            soqp.OperatorReviewQueueCompletenessStatus.OPERATOR_REVIEW_QUEUE_COMPLETE
        ),
        "operator_review_queue_posture": (
            soqp.OperatorReviewQueuePosture.OPERATOR_REVIEW_QUEUE_IN_MEMORY_ONLY
        ),
        "operator_review_status": soqp.OperatorReviewStatus.OPERATOR_REVIEW_REQUIRED,
        "runtime_gate_status": soqp.RuntimeGateStatus.RUNTIME_GATE_READY,
    }
    values.update(overrides)
    return soqp.SuppliedRuntimeOperatorReviewQueuePacketRecord(**values)


def _assert_blocked_with_reason(
    record: soqp.SuppliedRuntimeOperatorReviewQueuePacketRecord,
    reason: str,
) -> None:
    result = soqp.validate_supplied_runtime_operator_review_queue_packet_record(record)
    assert result.passed is False
    assert result.severity is soqp.ValidationSeverity.BLOCKED
    assert reason in result.reasons


def test_enums_are_closed_sets() -> None:
    assert soqp.OperatorReviewQueuePacketStatus.values() == frozenset(
        {
            "operator_review_queue_packet_recorded",
            "operator_review_queue_packet_missing",
            "operator_review_queue_packet_ambiguous",
            "operator_review_queue_packet_unsupported",
            "operator_review_queue_packet_unknown",
        }
    )
    assert soqp.OperatorReviewQueueCompletenessStatus.values() == frozenset(
        {
            "operator_review_queue_complete",
            "operator_review_queue_incomplete",
            "operator_review_queue_ambiguous",
            "operator_review_queue_unknown",
        }
    )
    assert soqp.OperatorReviewQueuePosture.values() == frozenset(
        {
            "operator_review_queue_in_memory_only",
            "operator_review_queue_missing",
            "operator_review_queue_ambiguous",
            "operator_review_queue_unsupported",
            "operator_review_queue_unknown",
        }
    )
    assert soqp.OperatorReviewStatus.values() == frozenset(
        {
            "operator_review_required",
            "operator_review_missing",
            "operator_review_ambiguous",
            "operator_review_not_required",
            "operator_review_unknown",
        }
    )
    assert soqp.RuntimeGateStatus.values() == frozenset(
        {
            "runtime_gate_ready",
            "runtime_gate_blocked",
            "runtime_gate_requires_manual_review",
            "runtime_gate_unknown",
        }
    )
    assert soqp.ValidationSeverity.values() == frozenset(
        {"passed", "caution", "failed", "blocked"}
    )


def test_dataclass_construction() -> None:
    record = _valid_operator_review_queue_packet(provenance_notes="operator supplied queue")

    assert record.condition_id == "condition-1"
    assert record.token_id == "token-1"
    assert record.outcome == "Yes"
    assert isinstance(
        record.supplied_runtime_operator_review_ack_packet,
        soap.SuppliedRuntimeOperatorReviewAckPacketRecord,
    )
    assert record.operator_review_queue_packet_status is (
        soqp.OperatorReviewQueuePacketStatus.OPERATOR_REVIEW_QUEUE_PACKET_RECORDED
    )
    assert record.provenance_notes == "operator supplied queue"


def test_mapping_construction_coerces_string_enums_and_nested_ack_packet_mapping() -> None:
    record = soqp.supplied_runtime_operator_review_queue_packet_record_from_mapping(
        {
            "condition_id": "condition-1",
            "token_id": "token-1",
            "outcome": "Yes",
            "supplied_runtime_operator_review_ack_packet": asdict(
                _valid_operator_review_ack_packet()
            ),
            "queue_packet_id": "queue-packet-2",
            "queue_summary": "Caller supplied operator-review queue packet summary text.",
            "operator_review_summary": "Operator review is required before any later action.",
            "blocked_reason_summary": "",
            "operator_review_queue_packet_status": "operator_review_queue_packet_recorded",
            "operator_review_queue_completeness_status": "operator_review_queue_complete",
            "operator_review_queue_posture": "operator_review_queue_in_memory_only",
            "operator_review_status": "operator_review_required",
            "runtime_gate_status": "runtime_gate_ready",
            "provenance_notes": "queue note",
        }
    )

    assert isinstance(
        record.supplied_runtime_operator_review_ack_packet,
        soap.SuppliedRuntimeOperatorReviewAckPacketRecord,
    )
    assert record.operator_review_queue_packet_status is (
        soqp.OperatorReviewQueuePacketStatus.OPERATOR_REVIEW_QUEUE_PACKET_RECORDED
    )
    assert record.operator_review_queue_completeness_status is (
        soqp.OperatorReviewQueueCompletenessStatus.OPERATOR_REVIEW_QUEUE_COMPLETE
    )
    assert record.operator_review_queue_posture is (
        soqp.OperatorReviewQueuePosture.OPERATOR_REVIEW_QUEUE_IN_MEMORY_ONLY
    )
    assert record.operator_review_status is soqp.OperatorReviewStatus.OPERATOR_REVIEW_REQUIRED
    assert record.runtime_gate_status is soqp.RuntimeGateStatus.RUNTIME_GATE_READY
    assert record.provenance_notes == "queue note"


def test_minimal_valid_operator_review_queue_packet_passes() -> None:
    result = soqp.validate_supplied_runtime_operator_review_queue_packet_record(
        _valid_operator_review_queue_packet()
    )

    assert result.passed is True
    assert result.severity is soqp.ValidationSeverity.PASSED
    assert result.reasons == ()


@pytest.mark.parametrize(
    ("field_name", "reason"),
    (
        ("condition_id", "condition_id is missing"),
        ("token_id", "token_id is missing"),
        ("outcome", "outcome is missing"),
        ("queue_packet_id", "queue_packet_id is missing"),
        ("queue_summary", "queue_summary is missing"),
        ("operator_review_summary", "operator_review_summary is missing"),
    ),
)
def test_blank_required_text_fields_fail_closed(field_name: str, reason: str) -> None:
    _assert_blocked_with_reason(
        _valid_operator_review_queue_packet(
            **{field_name: "  "}, blocked_reason_summary="blocked"
        ),
        reason,
    )


def test_blank_blocked_reason_summary_is_allowed_for_passing_queue_packet() -> None:
    result = soqp.validate_supplied_runtime_operator_review_queue_packet_record(
        _valid_operator_review_queue_packet(blocked_reason_summary="")
    )

    assert result.passed is True
    assert result.reasons == ()


def test_blank_blocked_reason_summary_fails_when_queue_packet_is_otherwise_blocked() -> None:
    result = soqp.validate_supplied_runtime_operator_review_queue_packet_record(
        _valid_operator_review_queue_packet(queue_summary="  ", blocked_reason_summary="")
    )

    assert result.passed is False
    assert result.reasons == (
        "queue_summary is missing",
        "blocked_reason_summary is missing",
    )


def test_nested_invalid_supplied_runtime_operator_review_ack_packet_fails_closed() -> None:
    _assert_blocked_with_reason(
        _valid_operator_review_queue_packet(
            supplied_runtime_operator_review_ack_packet=_valid_operator_review_ack_packet(
                ack_summary="  "
            ),
            blocked_reason_summary="blocked",
        ),
        "supplied runtime operator-review ack packet validation failed",
    )


def test_condition_id_mismatch_with_supplied_runtime_operator_review_ack_packet_fails_closed() -> None:
    _assert_blocked_with_reason(
        _valid_operator_review_queue_packet(
            supplied_runtime_operator_review_ack_packet=_valid_operator_review_ack_packet(
                condition_id="condition-2"
            ),
            blocked_reason_summary="blocked",
        ),
        "condition_id does not match supplied runtime operator-review ack packet",
    )


def test_token_id_mismatch_with_supplied_runtime_operator_review_ack_packet_fails_closed() -> None:
    _assert_blocked_with_reason(
        _valid_operator_review_queue_packet(
            supplied_runtime_operator_review_ack_packet=_valid_operator_review_ack_packet(
                token_id="token-2"
            ),
            blocked_reason_summary="blocked",
        ),
        "token_id does not match supplied runtime operator-review ack packet",
    )


def test_outcome_mismatch_with_supplied_runtime_operator_review_ack_packet_fails_closed() -> None:
    _assert_blocked_with_reason(
        _valid_operator_review_queue_packet(
            supplied_runtime_operator_review_ack_packet=_valid_operator_review_ack_packet(
                outcome="No"
            ),
            blocked_reason_summary="blocked",
        ),
        "outcome does not match supplied runtime operator-review ack packet",
    )


def test_operator_review_summary_mismatch_with_supplied_runtime_operator_review_ack_packet_fails_closed() -> None:
    _assert_blocked_with_reason(
        _valid_operator_review_queue_packet(
            operator_review_summary="Different caller supplied operator review summary.",
            blocked_reason_summary="blocked",
        ),
        "operator_review_summary does not match supplied runtime operator-review ack packet",
    )


@pytest.mark.parametrize(
    "operator_review_queue_packet_status",
    (
        soqp.OperatorReviewQueuePacketStatus.OPERATOR_REVIEW_QUEUE_PACKET_MISSING,
        soqp.OperatorReviewQueuePacketStatus.OPERATOR_REVIEW_QUEUE_PACKET_AMBIGUOUS,
        soqp.OperatorReviewQueuePacketStatus.OPERATOR_REVIEW_QUEUE_PACKET_UNSUPPORTED,
        soqp.OperatorReviewQueuePacketStatus.OPERATOR_REVIEW_QUEUE_PACKET_UNKNOWN,
    ),
)
def test_non_recorded_operator_review_queue_packet_statuses_fail_closed(
    operator_review_queue_packet_status: soqp.OperatorReviewQueuePacketStatus,
) -> None:
    _assert_blocked_with_reason(
        _valid_operator_review_queue_packet(
            operator_review_queue_packet_status=operator_review_queue_packet_status,
            blocked_reason_summary="blocked",
        ),
        f"operator review queue packet status is {operator_review_queue_packet_status.value}",
    )


@pytest.mark.parametrize(
    "operator_review_queue_completeness_status",
    (
        soqp.OperatorReviewQueueCompletenessStatus.OPERATOR_REVIEW_QUEUE_INCOMPLETE,
        soqp.OperatorReviewQueueCompletenessStatus.OPERATOR_REVIEW_QUEUE_AMBIGUOUS,
        soqp.OperatorReviewQueueCompletenessStatus.OPERATOR_REVIEW_QUEUE_UNKNOWN,
    ),
)
def test_non_complete_operator_review_queue_completeness_statuses_fail_closed(
    operator_review_queue_completeness_status: soqp.OperatorReviewQueueCompletenessStatus,
) -> None:
    _assert_blocked_with_reason(
        _valid_operator_review_queue_packet(
            operator_review_queue_completeness_status=operator_review_queue_completeness_status,
            blocked_reason_summary="blocked",
        ),
        "operator review queue completeness status is "
        f"{operator_review_queue_completeness_status.value}",
    )


@pytest.mark.parametrize(
    "operator_review_queue_posture",
    (
        soqp.OperatorReviewQueuePosture.OPERATOR_REVIEW_QUEUE_MISSING,
        soqp.OperatorReviewQueuePosture.OPERATOR_REVIEW_QUEUE_AMBIGUOUS,
        soqp.OperatorReviewQueuePosture.OPERATOR_REVIEW_QUEUE_UNSUPPORTED,
        soqp.OperatorReviewQueuePosture.OPERATOR_REVIEW_QUEUE_UNKNOWN,
    ),
)
def test_non_in_memory_only_operator_review_queue_postures_fail_closed(
    operator_review_queue_posture: soqp.OperatorReviewQueuePosture,
) -> None:
    _assert_blocked_with_reason(
        _valid_operator_review_queue_packet(
            operator_review_queue_posture=operator_review_queue_posture,
            blocked_reason_summary="blocked",
        ),
        f"operator review queue posture is {operator_review_queue_posture.value}",
    )


@pytest.mark.parametrize(
    "operator_review_status",
    (
        soqp.OperatorReviewStatus.OPERATOR_REVIEW_MISSING,
        soqp.OperatorReviewStatus.OPERATOR_REVIEW_AMBIGUOUS,
        soqp.OperatorReviewStatus.OPERATOR_REVIEW_NOT_REQUIRED,
        soqp.OperatorReviewStatus.OPERATOR_REVIEW_UNKNOWN,
    ),
)
def test_non_required_operator_review_statuses_fail_closed(
    operator_review_status: soqp.OperatorReviewStatus,
) -> None:
    _assert_blocked_with_reason(
        _valid_operator_review_queue_packet(
            operator_review_status=operator_review_status,
            blocked_reason_summary="blocked",
        ),
        f"operator review status is {operator_review_status.value}",
    )


@pytest.mark.parametrize(
    "runtime_gate_status",
    (
        soqp.RuntimeGateStatus.RUNTIME_GATE_BLOCKED,
        soqp.RuntimeGateStatus.RUNTIME_GATE_REQUIRES_MANUAL_REVIEW,
        soqp.RuntimeGateStatus.RUNTIME_GATE_UNKNOWN,
    ),
)
def test_non_ready_runtime_gate_statuses_fail_closed(
    runtime_gate_status: soqp.RuntimeGateStatus,
) -> None:
    _assert_blocked_with_reason(
        _valid_operator_review_queue_packet(
            runtime_gate_status=runtime_gate_status,
            blocked_reason_summary="blocked",
        ),
        f"runtime gate status is {runtime_gate_status.value}",
    )


def test_new_files_do_not_contain_noncanonical_identifier_string() -> None:
    forbidden = "market" "_id"

    assert forbidden not in MODULE_PATH.read_text(encoding="utf-8")
    assert forbidden not in TEST_PATH.read_text(encoding="utf-8")


def _module_source_without_docstrings() -> str:
    source_text = MODULE_PATH.read_text(encoding="utf-8")
    parsed = ast.parse(source_text)
    for node in ast.walk(parsed):
        if not hasattr(node, "body") or not node.body:
            continue
        first_statement = node.body[0]
        if isinstance(first_statement, ast.Expr) and isinstance(
            first_statement.value,
            ast.Constant,
        ):
            if isinstance(first_statement.value.value, str):
                first_statement.value = ast.Constant(value="")
    return ast.unparse(parsed)


def test_module_source_has_no_network_provider_execution_or_file_io_calls() -> None:
    source_text = _module_source_without_docstrings()
    forbidden_terms = (
        "requests",
        "httpx",
        "urllib",
        "aiohttp",
        "boto3",
        "polymarket",
        "kalshi",
        "duckdb",
        "pandas",
        "subprocess",
        "open(",
        ".read_text(",
        ".write_text(",
        "socket",
        "os.environ",
        "dotenv",
        "place_order",
        "paper_trade",
        "trade",
        "backtest",
        "score",
        "execute_order",
        "submit_order",
        "persist",
        "database",
        "postgres",
        "redis",
        "export",
        "write",
        "save",
        "owner_decision",
        "capture_decision",
        "celery",
        "rabbitmq",
        "sqs",
        "enqueue(",
        "dequeue(",
        "publish(",
    )

    for term in forbidden_terms:
        assert term not in source_text
