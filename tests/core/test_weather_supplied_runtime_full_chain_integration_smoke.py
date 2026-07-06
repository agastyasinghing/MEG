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
from meg.weather.stage2 import supplied_runtime_full_chain_integration_smoke as sfcis
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


MODULE_PATH = Path("meg/weather/stage2/supplied_runtime_full_chain_integration_smoke.py")
TEST_PATH = Path("tests/core/test_weather_supplied_runtime_full_chain_integration_smoke.py")


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




def _valid_full_chain_integration_smoke(
    **overrides: object,
) -> sfcis.SuppliedRuntimeFullChainIntegrationSmokeRecord:
    values = {
        "condition_id": "condition-1",
        "token_id": "token-1",
        "outcome": "Yes",
        "supplied_runtime_operator_review_completion_summary": _valid_operator_review_completion_summary(),
        "integration_smoke_id": "integration-smoke-1",
        "integration_smoke_summary": "Caller supplied full-chain integration smoke summary text.",
        "operator_review_summary": "Operator review is required before any later action.",
        "blocked_reason_summary": "",
        "full_chain_integration_smoke_status": (
            sfcis.FullChainIntegrationSmokeStatus.FULL_CHAIN_INTEGRATION_SMOKE_RECORDED
        ),
        "full_chain_integration_completeness_status": (
            sfcis.FullChainIntegrationCompletenessStatus.FULL_CHAIN_INTEGRATION_COMPLETE
        ),
        "full_chain_integration_posture": (
            sfcis.FullChainIntegrationPosture.FULL_CHAIN_INTEGRATION_IN_MEMORY_ONLY
        ),
        "operator_review_status": sfcis.OperatorReviewStatus.OPERATOR_REVIEW_REQUIRED,
        "runtime_gate_status": sfcis.RuntimeGateStatus.RUNTIME_GATE_READY,
    }
    values.update(overrides)
    return sfcis.SuppliedRuntimeFullChainIntegrationSmokeRecord(**values)


def _assert_blocked_with_reason(
    record: sfcis.SuppliedRuntimeFullChainIntegrationSmokeRecord,
    reason: str,
) -> None:
    result = sfcis.validate_supplied_runtime_full_chain_integration_smoke_record(record)
    assert result.passed is False
    assert result.severity is sfcis.ValidationSeverity.BLOCKED
    assert reason in result.reasons


def test_enums_are_closed_sets() -> None:
    assert sfcis.FullChainIntegrationSmokeStatus.values() == frozenset(
        {
            "full_chain_integration_smoke_recorded",
            "full_chain_integration_smoke_missing",
            "full_chain_integration_smoke_ambiguous",
            "full_chain_integration_smoke_unsupported",
            "full_chain_integration_smoke_unknown",
        }
    )
    assert sfcis.FullChainIntegrationCompletenessStatus.values() == frozenset(
        {
            "full_chain_integration_complete",
            "full_chain_integration_incomplete",
            "full_chain_integration_ambiguous",
            "full_chain_integration_unknown",
        }
    )
    assert sfcis.FullChainIntegrationPosture.values() == frozenset(
        {
            "full_chain_integration_in_memory_only",
            "full_chain_integration_missing",
            "full_chain_integration_ambiguous",
            "full_chain_integration_unsupported",
            "full_chain_integration_unknown",
        }
    )
    assert sfcis.OperatorReviewStatus.values() == frozenset(
        {
            "operator_review_required",
            "operator_review_missing",
            "operator_review_ambiguous",
            "operator_review_not_required",
            "operator_review_unknown",
        }
    )
    assert sfcis.RuntimeGateStatus.values() == frozenset(
        {
            "runtime_gate_ready",
            "runtime_gate_blocked",
            "runtime_gate_requires_manual_review",
            "runtime_gate_unknown",
        }
    )
    assert sfcis.ValidationSeverity.values() == frozenset({"passed", "caution", "failed", "blocked"})


def test_dataclass_construction() -> None:
    record = _valid_full_chain_integration_smoke(provenance_notes="operator supplied smoke")

    assert record.condition_id == "condition-1"
    assert record.token_id == "token-1"
    assert record.outcome == "Yes"
    assert isinstance(
        record.supplied_runtime_operator_review_completion_summary,
        socsum.SuppliedRuntimeOperatorReviewCompletionSummaryRecord,
    )
    assert record.full_chain_integration_smoke_status is (
        sfcis.FullChainIntegrationSmokeStatus.FULL_CHAIN_INTEGRATION_SMOKE_RECORDED
    )
    assert record.provenance_notes == "operator supplied smoke"


def test_mapping_construction_coerces_string_enums_and_nested_operator_review_completion_summary_mapping() -> None:
    record = sfcis.supplied_runtime_full_chain_integration_smoke_record_from_mapping(
        {
            "condition_id": "condition-1",
            "token_id": "token-1",
            "outcome": "Yes",
            "supplied_runtime_operator_review_completion_summary": asdict(
                _valid_operator_review_completion_summary()
            ),
            "integration_smoke_id": "integration-smoke-2",
            "integration_smoke_summary": "Caller supplied full-chain integration smoke summary text.",
            "operator_review_summary": "Operator review is required before any later action.",
            "blocked_reason_summary": "",
            "full_chain_integration_smoke_status": "full_chain_integration_smoke_recorded",
            "full_chain_integration_completeness_status": "full_chain_integration_complete",
            "full_chain_integration_posture": "full_chain_integration_in_memory_only",
            "operator_review_status": "operator_review_required",
            "runtime_gate_status": "runtime_gate_ready",
            "provenance_notes": "integration smoke note",
        }
    )

    assert isinstance(
        record.supplied_runtime_operator_review_completion_summary,
        socsum.SuppliedRuntimeOperatorReviewCompletionSummaryRecord,
    )
    assert record.full_chain_integration_smoke_status is (
        sfcis.FullChainIntegrationSmokeStatus.FULL_CHAIN_INTEGRATION_SMOKE_RECORDED
    )
    assert record.full_chain_integration_completeness_status is (
        sfcis.FullChainIntegrationCompletenessStatus.FULL_CHAIN_INTEGRATION_COMPLETE
    )
    assert record.full_chain_integration_posture is (
        sfcis.FullChainIntegrationPosture.FULL_CHAIN_INTEGRATION_IN_MEMORY_ONLY
    )
    assert record.operator_review_status is sfcis.OperatorReviewStatus.OPERATOR_REVIEW_REQUIRED
    assert record.runtime_gate_status is sfcis.RuntimeGateStatus.RUNTIME_GATE_READY
    assert record.provenance_notes == "integration smoke note"


def test_minimal_valid_full_chain_integration_smoke_passes() -> None:
    result = sfcis.validate_supplied_runtime_full_chain_integration_smoke_record(
        _valid_full_chain_integration_smoke()
    )

    assert result.passed is True
    assert result.severity is sfcis.ValidationSeverity.PASSED
    assert result.reasons == ()


@pytest.mark.parametrize(
    ("field_name", "reason"),
    (
        ("condition_id", "condition_id is missing"),
        ("token_id", "token_id is missing"),
        ("outcome", "outcome is missing"),
        ("integration_smoke_id", "integration_smoke_id is missing"),
        ("integration_smoke_summary", "integration_smoke_summary is missing"),
        ("operator_review_summary", "operator_review_summary is missing"),
    ),
)
def test_blank_required_text_fields_fail_closed(field_name: str, reason: str) -> None:
    _assert_blocked_with_reason(_valid_full_chain_integration_smoke(**{field_name: " "}), reason)


def test_blank_blocked_reason_summary_is_allowed_for_passing_integration_smoke() -> None:
    result = sfcis.validate_supplied_runtime_full_chain_integration_smoke_record(
        _valid_full_chain_integration_smoke(blocked_reason_summary="")
    )

    assert result.passed is True
    assert result.reasons == ()


def test_blank_blocked_reason_summary_fails_when_integration_smoke_is_otherwise_blocked() -> None:
    _assert_blocked_with_reason(
        _valid_full_chain_integration_smoke(
            integration_smoke_id="",
            blocked_reason_summary="",
        ),
        "blocked_reason_summary is missing",
    )


def test_nested_invalid_supplied_runtime_operator_review_completion_summary_fails_closed() -> None:
    _assert_blocked_with_reason(
        _valid_full_chain_integration_smoke(
            supplied_runtime_operator_review_completion_summary=_valid_operator_review_completion_summary(
                completion_summary_id="",
                blocked_reason_summary="nested blocked",
            ),
            blocked_reason_summary="top blocked",
        ),
        "supplied runtime operator-review completion summary validation failed",
    )


def test_condition_id_mismatch_with_supplied_runtime_operator_review_completion_summary_fails_closed() -> None:
    _assert_blocked_with_reason(
        _valid_full_chain_integration_smoke(condition_id="condition-2", blocked_reason_summary="blocked"),
        "condition_id does not match supplied runtime operator-review completion summary",
    )


def test_token_id_mismatch_with_supplied_runtime_operator_review_completion_summary_fails_closed() -> None:
    _assert_blocked_with_reason(
        _valid_full_chain_integration_smoke(token_id="token-2", blocked_reason_summary="blocked"),
        "token_id does not match supplied runtime operator-review completion summary",
    )


def test_outcome_mismatch_with_supplied_runtime_operator_review_completion_summary_fails_closed() -> None:
    _assert_blocked_with_reason(
        _valid_full_chain_integration_smoke(outcome="No", blocked_reason_summary="blocked"),
        "outcome does not match supplied runtime operator-review completion summary",
    )


def test_operator_review_summary_mismatch_with_supplied_runtime_operator_review_completion_summary_fails_closed() -> None:
    _assert_blocked_with_reason(
        _valid_full_chain_integration_smoke(
            operator_review_summary="Different supplied operator review summary.",
            blocked_reason_summary="blocked",
        ),
        "operator_review_summary does not match supplied runtime operator-review completion summary",
    )


@pytest.mark.parametrize(
    "status",
    [
        status
        for status in sfcis.FullChainIntegrationSmokeStatus
        if status is not sfcis.FullChainIntegrationSmokeStatus.FULL_CHAIN_INTEGRATION_SMOKE_RECORDED
    ],
)
def test_non_recorded_full_chain_integration_smoke_statuses_fail_closed(
    status: sfcis.FullChainIntegrationSmokeStatus,
) -> None:
    _assert_blocked_with_reason(
        _valid_full_chain_integration_smoke(
            full_chain_integration_smoke_status=status,
            blocked_reason_summary="blocked",
        ),
        f"full chain integration smoke status is {status.value}",
    )


@pytest.mark.parametrize(
    "status",
    [
        status
        for status in sfcis.FullChainIntegrationCompletenessStatus
        if status is not sfcis.FullChainIntegrationCompletenessStatus.FULL_CHAIN_INTEGRATION_COMPLETE
    ],
)
def test_non_complete_full_chain_integration_completeness_statuses_fail_closed(
    status: sfcis.FullChainIntegrationCompletenessStatus,
) -> None:
    _assert_blocked_with_reason(
        _valid_full_chain_integration_smoke(
            full_chain_integration_completeness_status=status,
            blocked_reason_summary="blocked",
        ),
        f"full chain integration completeness status is {status.value}",
    )


@pytest.mark.parametrize(
    "posture",
    [
        posture
        for posture in sfcis.FullChainIntegrationPosture
        if posture is not sfcis.FullChainIntegrationPosture.FULL_CHAIN_INTEGRATION_IN_MEMORY_ONLY
    ],
)
def test_non_in_memory_only_full_chain_integration_postures_fail_closed(
    posture: sfcis.FullChainIntegrationPosture,
) -> None:
    _assert_blocked_with_reason(
        _valid_full_chain_integration_smoke(
            full_chain_integration_posture=posture,
            blocked_reason_summary="blocked",
        ),
        f"full chain integration posture is {posture.value}",
    )


@pytest.mark.parametrize(
    "status",
    [
        status
        for status in sfcis.OperatorReviewStatus
        if status is not sfcis.OperatorReviewStatus.OPERATOR_REVIEW_REQUIRED
    ],
)
def test_non_required_operator_review_statuses_fail_closed(
    status: sfcis.OperatorReviewStatus,
) -> None:
    _assert_blocked_with_reason(
        _valid_full_chain_integration_smoke(
            operator_review_status=status,
            blocked_reason_summary="blocked",
        ),
        f"operator review status is {status.value}",
    )


@pytest.mark.parametrize(
    "status",
    [
        status
        for status in sfcis.RuntimeGateStatus
        if status is not sfcis.RuntimeGateStatus.RUNTIME_GATE_READY
    ],
)
def test_non_ready_runtime_gate_statuses_fail_closed(status: sfcis.RuntimeGateStatus) -> None:
    _assert_blocked_with_reason(
        _valid_full_chain_integration_smoke(
            runtime_gate_status=status,
            blocked_reason_summary="blocked",
        ),
        f"runtime gate status is {status.value}",
    )


def _source_without_docstrings(path: Path) -> str:
    tree = ast.parse(path.read_text())
    for node in ast.walk(tree):
        if not isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            continue
        if not node.body:
            continue
        first = node.body[0]
        if isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant) and isinstance(first.value.value, str):
            first.value = ast.Constant(value="")
    return ast.unparse(tree)


def test_static_sources_do_not_contain_noncanonical_identifier_literal() -> None:
    assert "market" + "_id" not in MODULE_PATH.read_text()
    assert "market" + "_id" not in TEST_PATH.read_text()


def test_source_has_no_forbidden_runtime_or_side_effect_terms() -> None:
    source = _source_without_docstrings(MODULE_PATH)
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
        assert term not in source


def test_deep_nested_invalid_supplied_market_contract_fails_top_level_smoke_closed() -> None:
    invalid_contract = _valid_contract(condition_id="", runtime_gate_status=smcr.RuntimeGateStatus.RUNTIME_GATE_BLOCKED)
    review_packet = _valid_review_packet(supplied_market_contract=invalid_contract)
    evidence_packet = _valid_evidence_packet(supplied_market_contract=invalid_contract)
    composition = _valid_composition(
        supplied_market_review_packet=review_packet,
        supplied_evidence_packet=evidence_packet,
    )
    bundle = _valid_bundle(
        supplied_market_contract=invalid_contract,
        supplied_market_review_packet=review_packet,
        supplied_evidence_packet=evidence_packet,
        review_packet_evidence_composition=composition,
    )
    dry_run_packet = _valid_dry_run_packet(supplied_runtime_validation_bundle=bundle)
    dry_run_report = _valid_dry_run_report(supplied_runtime_dry_run_packet=dry_run_packet)
    smoke = _valid_end_to_end_smoke(supplied_runtime_dry_run_report=dry_run_report)
    trace_packet = _valid_trace_packet(supplied_runtime_end_to_end_smoke=smoke)
    handoff = _valid_operator_review_handoff(supplied_runtime_trace_packet=trace_packet)
    ack_packet = _valid_operator_review_ack_packet(supplied_runtime_operator_review_handoff=handoff)
    queue_packet = _valid_operator_review_queue_packet(supplied_runtime_operator_review_ack_packet=ack_packet)
    queue_entry = _valid_operator_review_queue_entry(supplied_runtime_operator_review_queue_packet=queue_packet)
    queue_summary = _valid_operator_review_queue_summary(supplied_runtime_operator_review_queue_entry=queue_entry)
    final_packet = _valid_operator_review_final_packet(supplied_runtime_operator_review_queue_summary=queue_summary)
    final_bundle = _valid_operator_review_final_bundle(supplied_runtime_operator_review_final_packet=final_packet)
    completion_seal = _valid_operator_review_completion_seal(supplied_runtime_operator_review_final_bundle=final_bundle)
    completion_summary = _valid_operator_review_completion_summary(
        supplied_runtime_operator_review_completion_seal=completion_seal,
        blocked_reason_summary="nested blocked",
    )

    _assert_blocked_with_reason(
        _valid_full_chain_integration_smoke(
            supplied_runtime_operator_review_completion_summary=completion_summary,
            blocked_reason_summary="top blocked",
        ),
        "supplied runtime operator-review completion summary validation failed",
    )
