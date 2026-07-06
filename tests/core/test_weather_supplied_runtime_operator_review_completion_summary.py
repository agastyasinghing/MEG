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


MODULE_PATH = Path("meg/weather/stage2/supplied_runtime_operator_review_completion_summary.py")
TEST_PATH = Path("tests/core/test_weather_supplied_runtime_operator_review_completion_summary.py")


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



def _valid_operator_review_queue_entry(
    **overrides: object,
) -> soqe.SuppliedRuntimeOperatorReviewQueueEntryRecord:
    values = {
        "condition_id": "condition-1",
        "token_id": "token-1",
        "outcome": "Yes",
        "supplied_runtime_operator_review_queue_packet": _valid_operator_review_queue_packet(),
        "queue_entry_id": "queue-entry-1",
        "queue_entry_summary": "Caller supplied operator-review queue entry summary text.",
        "operator_review_summary": "Operator review is required before any later action.",
        "blocked_reason_summary": "",
        "operator_review_queue_entry_status": (
            soqe.OperatorReviewQueueEntryStatus.OPERATOR_REVIEW_QUEUE_ENTRY_RECORDED
        ),
        "operator_review_queue_entry_completeness_status": (
            soqe.OperatorReviewQueueEntryCompletenessStatus.OPERATOR_REVIEW_QUEUE_ENTRY_COMPLETE
        ),
        "operator_review_queue_entry_posture": (
            soqe.OperatorReviewQueueEntryPosture.OPERATOR_REVIEW_QUEUE_ENTRY_IN_MEMORY_ONLY
        ),
        "operator_review_status": soqe.OperatorReviewStatus.OPERATOR_REVIEW_REQUIRED,
        "runtime_gate_status": soqe.RuntimeGateStatus.RUNTIME_GATE_READY,
    }
    values.update(overrides)
    return soqe.SuppliedRuntimeOperatorReviewQueueEntryRecord(**values)

def _valid_operator_review_queue_summary(
    **overrides: object,
) -> soqs.SuppliedRuntimeOperatorReviewQueueSummaryRecord:
    values = {
        "condition_id": "condition-1",
        "token_id": "token-1",
        "outcome": "Yes",
        "supplied_runtime_operator_review_queue_entry": _valid_operator_review_queue_entry(),
        "queue_summary_id": "queue-entry-1",
        "queue_summary_text": "Caller supplied operator-review queue summary summary text.",
        "operator_review_summary": "Operator review is required before any later action.",
        "blocked_reason_summary": "",
        "operator_review_queue_summary_status": (
            soqs.OperatorReviewQueueSummaryStatus.OPERATOR_REVIEW_QUEUE_SUMMARY_RECORDED
        ),
        "operator_review_queue_summary_completeness_status": (
            soqs.OperatorReviewQueueSummaryCompletenessStatus.OPERATOR_REVIEW_QUEUE_SUMMARY_COMPLETE
        ),
        "operator_review_queue_summary_posture": (
            soqs.OperatorReviewQueueSummaryPosture.OPERATOR_REVIEW_QUEUE_SUMMARY_IN_MEMORY_ONLY
        ),
        "operator_review_status": soqs.OperatorReviewStatus.OPERATOR_REVIEW_REQUIRED,
        "runtime_gate_status": soqs.RuntimeGateStatus.RUNTIME_GATE_READY,
    }
    values.update(overrides)
    return soqs.SuppliedRuntimeOperatorReviewQueueSummaryRecord(**values)



def _valid_operator_review_final_packet(
    **overrides: object,
) -> sofp.SuppliedRuntimeOperatorReviewFinalPacketRecord:
    values = {
        "condition_id": "condition-1",
        "token_id": "token-1",
        "outcome": "Yes",
        "supplied_runtime_operator_review_queue_summary": _valid_operator_review_queue_summary(),
        "final_packet_id": "final-packet-1",
        "final_packet_summary": "Caller supplied operator-review final packet summary text.",
        "operator_review_summary": "Operator review is required before any later action.",
        "blocked_reason_summary": "",
        "operator_review_final_packet_status": (
            sofp.OperatorReviewFinalPacketStatus.OPERATOR_REVIEW_FINAL_PACKET_RECORDED
        ),
        "operator_review_final_completeness_status": (
            sofp.OperatorReviewFinalCompletenessStatus.OPERATOR_REVIEW_FINAL_COMPLETE
        ),
        "operator_review_final_posture": (
            sofp.OperatorReviewFinalPosture.OPERATOR_REVIEW_FINAL_IN_MEMORY_ONLY
        ),
        "operator_review_status": sofp.OperatorReviewStatus.OPERATOR_REVIEW_REQUIRED,
        "runtime_gate_status": sofp.RuntimeGateStatus.RUNTIME_GATE_READY,
    }
    values.update(overrides)
    return sofp.SuppliedRuntimeOperatorReviewFinalPacketRecord(**values)



def _valid_operator_review_final_bundle(
    **overrides: object,
) -> sofb.SuppliedRuntimeOperatorReviewFinalBundleRecord:
    values = {
        "condition_id": "condition-1",
        "token_id": "token-1",
        "outcome": "Yes",
        "supplied_runtime_operator_review_final_packet": _valid_operator_review_final_packet(),
        "final_bundle_id": "final-bundle-1",
        "final_bundle_summary": "Caller supplied operator-review final bundle summary text.",
        "operator_review_summary": "Operator review is required before any later action.",
        "blocked_reason_summary": "",
        "operator_review_final_bundle_status": (
            sofb.OperatorReviewFinalBundleStatus.OPERATOR_REVIEW_FINAL_BUNDLE_RECORDED
        ),
        "operator_review_final_bundle_completeness_status": (
            sofb.OperatorReviewFinalBundleCompletenessStatus.OPERATOR_REVIEW_FINAL_BUNDLE_COMPLETE
        ),
        "operator_review_final_bundle_posture": (
            sofb.OperatorReviewFinalBundlePosture.OPERATOR_REVIEW_FINAL_BUNDLE_IN_MEMORY_ONLY
        ),
        "operator_review_status": sofb.OperatorReviewStatus.OPERATOR_REVIEW_REQUIRED,
        "runtime_gate_status": sofb.RuntimeGateStatus.RUNTIME_GATE_READY,
    }
    values.update(overrides)
    return sofb.SuppliedRuntimeOperatorReviewFinalBundleRecord(**values)


def _valid_operator_review_completion_seal(
    **overrides: object,
) -> socs.SuppliedRuntimeOperatorReviewCompletionSealRecord:
    values = {
        "condition_id": "condition-1",
        "token_id": "token-1",
        "outcome": "Yes",
        "supplied_runtime_operator_review_final_bundle": _valid_operator_review_final_bundle(),
        "completion_seal_id": "completion-seal-1",
        "completion_seal_summary": "Caller supplied operator-review completion seal summary text.",
        "operator_review_summary": "Operator review is required before any later action.",
        "blocked_reason_summary": "",
        "operator_review_completion_seal_status": (
            socs.OperatorReviewCompletionSealStatus.OPERATOR_REVIEW_COMPLETION_SEAL_RECORDED
        ),
        "operator_review_completion_completeness_status": (
            socs.OperatorReviewCompletionCompletenessStatus.OPERATOR_REVIEW_COMPLETION_COMPLETE
        ),
        "operator_review_completion_seal_posture": (
            socs.OperatorReviewCompletionSealPosture.OPERATOR_REVIEW_COMPLETION_SEAL_IN_MEMORY_ONLY
        ),
        "operator_review_status": socs.OperatorReviewStatus.OPERATOR_REVIEW_REQUIRED,
        "runtime_gate_status": socs.RuntimeGateStatus.RUNTIME_GATE_READY,
    }
    values.update(overrides)
    return socs.SuppliedRuntimeOperatorReviewCompletionSealRecord(**values)



def _valid_operator_review_completion_summary(
    **overrides: object,
) -> socsum.SuppliedRuntimeOperatorReviewCompletionSummaryRecord:
    values = {
        "condition_id": "condition-1",
        "token_id": "token-1",
        "outcome": "Yes",
        "supplied_runtime_operator_review_completion_seal": _valid_operator_review_completion_seal(),
        "completion_summary_id": "completion-summary-1",
        "completion_summary_text": "Caller supplied operator-review completion summary summary text.",
        "operator_review_summary": "Operator review is required before any later action.",
        "blocked_reason_summary": "",
        "operator_review_completion_summary_status": (
            socsum.OperatorReviewCompletionSummaryStatus.OPERATOR_REVIEW_COMPLETION_SUMMARY_RECORDED
        ),
        "operator_review_completion_summary_completeness_status": (
            socsum.OperatorReviewCompletionSummaryCompletenessStatus.OPERATOR_REVIEW_COMPLETION_SUMMARY_COMPLETE
        ),
        "operator_review_completion_summary_posture": (
            socsum.OperatorReviewCompletionSummaryPosture.OPERATOR_REVIEW_COMPLETION_SUMMARY_IN_MEMORY_ONLY
        ),
        "operator_review_status": socsum.OperatorReviewStatus.OPERATOR_REVIEW_REQUIRED,
        "runtime_gate_status": socsum.RuntimeGateStatus.RUNTIME_GATE_READY,
    }
    values.update(overrides)
    return socsum.SuppliedRuntimeOperatorReviewCompletionSummaryRecord(**values)


def _assert_blocked_with_reason(
    record: socsum.SuppliedRuntimeOperatorReviewCompletionSummaryRecord,
    reason: str,
) -> None:
    result = socsum.validate_supplied_runtime_operator_review_completion_summary_record(record)
    assert result.passed is False
    assert result.severity is socsum.ValidationSeverity.BLOCKED
    assert reason in result.reasons


def test_enums_are_closed_sets() -> None:
    assert socsum.OperatorReviewCompletionSummaryStatus.values() == frozenset(
        {
            "operator_review_completion_summary_recorded",
            "operator_review_completion_summary_missing",
            "operator_review_completion_summary_ambiguous",
            "operator_review_completion_summary_unsupported",
            "operator_review_completion_summary_unknown",
        }
    )
    assert socsum.OperatorReviewCompletionSummaryCompletenessStatus.values() == frozenset(
        {
            "operator_review_completion_summary_complete",
            "operator_review_completion_summary_incomplete",
            "operator_review_completion_summary_ambiguous",
            "operator_review_completion_summary_unknown",
        }
    )
    assert socsum.OperatorReviewCompletionSummaryPosture.values() == frozenset(
        {
            "operator_review_completion_summary_in_memory_only",
            "operator_review_completion_summary_missing",
            "operator_review_completion_summary_ambiguous",
            "operator_review_completion_summary_unsupported",
            "operator_review_completion_summary_unknown",
        }
    )
    assert socsum.OperatorReviewStatus.values() == frozenset(
        {
            "operator_review_required",
            "operator_review_missing",
            "operator_review_ambiguous",
            "operator_review_not_required",
            "operator_review_unknown",
        }
    )
    assert socsum.RuntimeGateStatus.values() == frozenset(
        {
            "runtime_gate_ready",
            "runtime_gate_blocked",
            "runtime_gate_requires_manual_review",
            "runtime_gate_unknown",
        }
    )
    assert socsum.ValidationSeverity.values() == frozenset(
        {"passed", "caution", "failed", "blocked"}
    )


def test_dataclass_construction() -> None:
    record = _valid_operator_review_completion_summary(provenance_notes="operator supplied completion summary")

    assert record.condition_id == "condition-1"
    assert record.token_id == "token-1"
    assert record.outcome == "Yes"
    assert isinstance(
        record.supplied_runtime_operator_review_completion_seal,
        socs.SuppliedRuntimeOperatorReviewCompletionSealRecord,
    )
    assert record.operator_review_completion_summary_status is (
        socsum.OperatorReviewCompletionSummaryStatus.OPERATOR_REVIEW_COMPLETION_SUMMARY_RECORDED
    )
    assert record.provenance_notes == "operator supplied completion summary"


def test_mapping_construction_coerces_string_enums_and_nested_operator_review_completion_summary_mapping() -> None:
    record = socsum.supplied_runtime_operator_review_completion_summary_record_from_mapping(
        {
            "condition_id": "condition-1",
            "token_id": "token-1",
            "outcome": "Yes",
            "supplied_runtime_operator_review_completion_seal": asdict(
                _valid_operator_review_completion_seal()
            ),
            "completion_summary_id": "completion-summary-2",
            "completion_summary_text": "Caller supplied operator-review completion summary summary text.",
            "operator_review_summary": "Operator review is required before any later action.",
            "blocked_reason_summary": "",
            "operator_review_completion_summary_status": "operator_review_completion_summary_recorded",
            "operator_review_completion_summary_completeness_status": "operator_review_completion_summary_complete",
            "operator_review_completion_summary_posture": "operator_review_completion_summary_in_memory_only",
            "operator_review_status": "operator_review_required",
            "runtime_gate_status": "runtime_gate_ready",
            "provenance_notes": "completion summary note",
        }
    )

    assert isinstance(
        record.supplied_runtime_operator_review_completion_seal,
        socs.SuppliedRuntimeOperatorReviewCompletionSealRecord,
    )
    assert record.operator_review_completion_summary_status is (
        socsum.OperatorReviewCompletionSummaryStatus.OPERATOR_REVIEW_COMPLETION_SUMMARY_RECORDED
    )
    assert record.operator_review_completion_summary_completeness_status is (
        socsum.OperatorReviewCompletionSummaryCompletenessStatus.OPERATOR_REVIEW_COMPLETION_SUMMARY_COMPLETE
    )
    assert record.operator_review_completion_summary_posture is (
        socsum.OperatorReviewCompletionSummaryPosture.OPERATOR_REVIEW_COMPLETION_SUMMARY_IN_MEMORY_ONLY
    )
    assert record.operator_review_status is socsum.OperatorReviewStatus.OPERATOR_REVIEW_REQUIRED
    assert record.runtime_gate_status is socsum.RuntimeGateStatus.RUNTIME_GATE_READY
    assert record.provenance_notes == "completion summary note"


def test_minimal_valid_operator_review_completion_summary_passes() -> None:
    result = socsum.validate_supplied_runtime_operator_review_completion_summary_record(
        _valid_operator_review_completion_summary()
    )

    assert result.passed is True
    assert result.severity is socsum.ValidationSeverity.PASSED
    assert result.reasons == ()


@pytest.mark.parametrize(
    ("field_name", "reason"),
    (
        ("condition_id", "condition_id is missing"),
        ("token_id", "token_id is missing"),
        ("outcome", "outcome is missing"),
        ("completion_summary_id", "completion_summary_id is missing"),
        ("completion_summary_text", "completion_summary_text is missing"),
        ("operator_review_summary", "operator_review_summary is missing"),
    ),
)
def test_blank_required_text_fields_fail_closed(field_name: str, reason: str) -> None:
    _assert_blocked_with_reason(
        _valid_operator_review_completion_summary(
            **{field_name: "  "}, blocked_reason_summary="blocked"
        ),
        reason,
    )


def test_blank_blocked_reason_summary_is_allowed_for_passing_completion_summary() -> None:
    result = socsum.validate_supplied_runtime_operator_review_completion_summary_record(
        _valid_operator_review_completion_summary(blocked_reason_summary="")
    )

    assert result.passed is True
    assert result.reasons == ()


def test_blank_blocked_reason_summary_fails_when_completion_summary_is_otherwise_blocked() -> None:
    result = socsum.validate_supplied_runtime_operator_review_completion_summary_record(
        _valid_operator_review_completion_summary(completion_summary_text="  ", blocked_reason_summary="")
    )

    assert result.passed is False
    assert result.reasons == (
        "completion_summary_text is missing",
        "blocked_reason_summary is missing",
    )


def test_nested_invalid_supplied_runtime_operator_review_completion_seal_fails_closed() -> None:
    _assert_blocked_with_reason(
        _valid_operator_review_completion_summary(
            supplied_runtime_operator_review_completion_seal=_valid_operator_review_completion_seal(
                completion_seal_summary="  "
            ),
            blocked_reason_summary="blocked",
        ),
        "supplied runtime operator-review completion seal validation failed",
    )


def test_condition_id_mismatch_with_supplied_runtime_operator_review_completion_seal_fails_closed() -> None:
    _assert_blocked_with_reason(
        _valid_operator_review_completion_summary(
            supplied_runtime_operator_review_completion_seal=_valid_operator_review_completion_seal(
                condition_id="condition-2"
            ),
            blocked_reason_summary="blocked",
        ),
        "condition_id does not match supplied runtime operator-review completion seal",
    )


def test_token_id_mismatch_with_supplied_runtime_operator_review_completion_seal_fails_closed() -> None:
    _assert_blocked_with_reason(
        _valid_operator_review_completion_summary(
            supplied_runtime_operator_review_completion_seal=_valid_operator_review_completion_seal(
                token_id="token-2"
            ),
            blocked_reason_summary="blocked",
        ),
        "token_id does not match supplied runtime operator-review completion seal",
    )


def test_outcome_mismatch_with_supplied_runtime_operator_review_completion_seal_fails_closed() -> None:
    _assert_blocked_with_reason(
        _valid_operator_review_completion_summary(
            supplied_runtime_operator_review_completion_seal=_valid_operator_review_completion_seal(
                outcome="No"
            ),
            blocked_reason_summary="blocked",
        ),
        "outcome does not match supplied runtime operator-review completion seal",
    )


def test_operator_review_summary_mismatch_with_supplied_runtime_operator_review_completion_seal_fails_closed() -> None:
    _assert_blocked_with_reason(
        _valid_operator_review_completion_summary(
            operator_review_summary="Different caller supplied operator review summary.",
            blocked_reason_summary="blocked",
        ),
        "operator_review_summary does not match supplied runtime operator-review completion seal",
    )


@pytest.mark.parametrize(
    "operator_review_completion_summary_status",
    (
        socsum.OperatorReviewCompletionSummaryStatus.OPERATOR_REVIEW_COMPLETION_SUMMARY_MISSING,
        socsum.OperatorReviewCompletionSummaryStatus.OPERATOR_REVIEW_COMPLETION_SUMMARY_AMBIGUOUS,
        socsum.OperatorReviewCompletionSummaryStatus.OPERATOR_REVIEW_COMPLETION_SUMMARY_UNSUPPORTED,
        socsum.OperatorReviewCompletionSummaryStatus.OPERATOR_REVIEW_COMPLETION_SUMMARY_UNKNOWN,
    ),
)
def test_non_recorded_operator_review_completion_summary_statuses_fail_closed(
    operator_review_completion_summary_status: socsum.OperatorReviewCompletionSummaryStatus,
) -> None:
    _assert_blocked_with_reason(
        _valid_operator_review_completion_summary(
            operator_review_completion_summary_status=operator_review_completion_summary_status,
            blocked_reason_summary="blocked",
        ),
        f"operator review completion summary status is {operator_review_completion_summary_status.value}",
    )


@pytest.mark.parametrize(
    "operator_review_completion_summary_completeness_status",
    (
        socsum.OperatorReviewCompletionSummaryCompletenessStatus.OPERATOR_REVIEW_COMPLETION_SUMMARY_INCOMPLETE,
        socsum.OperatorReviewCompletionSummaryCompletenessStatus.OPERATOR_REVIEW_COMPLETION_SUMMARY_AMBIGUOUS,
        socsum.OperatorReviewCompletionSummaryCompletenessStatus.OPERATOR_REVIEW_COMPLETION_SUMMARY_UNKNOWN,
    ),
)
def test_non_complete_operator_review_completion_summary_completeness_statuses_fail_closed(
    operator_review_completion_summary_completeness_status: socsum.OperatorReviewCompletionSummaryCompletenessStatus,
) -> None:
    _assert_blocked_with_reason(
        _valid_operator_review_completion_summary(
            operator_review_completion_summary_completeness_status=(
                operator_review_completion_summary_completeness_status
            ),
            blocked_reason_summary="blocked",
        ),
        "operator review completion summary completeness status is "
        f"{operator_review_completion_summary_completeness_status.value}",
    )


@pytest.mark.parametrize(
    "operator_review_completion_summary_posture",
    (
        socsum.OperatorReviewCompletionSummaryPosture.OPERATOR_REVIEW_COMPLETION_SUMMARY_MISSING,
        socsum.OperatorReviewCompletionSummaryPosture.OPERATOR_REVIEW_COMPLETION_SUMMARY_AMBIGUOUS,
        socsum.OperatorReviewCompletionSummaryPosture.OPERATOR_REVIEW_COMPLETION_SUMMARY_UNSUPPORTED,
        socsum.OperatorReviewCompletionSummaryPosture.OPERATOR_REVIEW_COMPLETION_SUMMARY_UNKNOWN,
    ),
)
def test_non_in_memory_only_operator_review_completion_summary_postures_fail_closed(
    operator_review_completion_summary_posture: socsum.OperatorReviewCompletionSummaryPosture,
) -> None:
    _assert_blocked_with_reason(
        _valid_operator_review_completion_summary(
            operator_review_completion_summary_posture=operator_review_completion_summary_posture,
            blocked_reason_summary="blocked",
        ),
        f"operator review completion summary posture is {operator_review_completion_summary_posture.value}",
    )


@pytest.mark.parametrize(
    "operator_review_status",
    (
        socsum.OperatorReviewStatus.OPERATOR_REVIEW_MISSING,
        socsum.OperatorReviewStatus.OPERATOR_REVIEW_AMBIGUOUS,
        socsum.OperatorReviewStatus.OPERATOR_REVIEW_NOT_REQUIRED,
        socsum.OperatorReviewStatus.OPERATOR_REVIEW_UNKNOWN,
    ),
)
def test_non_required_operator_review_statuses_fail_closed(
    operator_review_status: socsum.OperatorReviewStatus,
) -> None:
    _assert_blocked_with_reason(
        _valid_operator_review_completion_summary(
            operator_review_status=operator_review_status,
            blocked_reason_summary="blocked",
        ),
        f"operator review status is {operator_review_status.value}",
    )


@pytest.mark.parametrize(
    "runtime_gate_status",
    (
        socsum.RuntimeGateStatus.RUNTIME_GATE_BLOCKED,
        socsum.RuntimeGateStatus.RUNTIME_GATE_REQUIRES_MANUAL_REVIEW,
        socsum.RuntimeGateStatus.RUNTIME_GATE_UNKNOWN,
    ),
)
def test_non_ready_runtime_gate_statuses_fail_closed(
    runtime_gate_status: socsum.RuntimeGateStatus,
) -> None:
    _assert_blocked_with_reason(
        _valid_operator_review_completion_summary(
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
        "subscribe(",
        "scheduler",
        "generate_summary",
        "summarize(",
        "approve",
        "reject",
        "decide",
        "complete_workflow",
        "seal_state",
        "durable",
    )

    for term in forbidden_terms:
        assert term not in source_text
