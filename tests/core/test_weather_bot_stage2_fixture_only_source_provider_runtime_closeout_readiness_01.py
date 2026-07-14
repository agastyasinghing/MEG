"""Static tests for Weather Bot Stage 2 fixture-only runtime closeout readiness."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "docs/prd/WEATHER-BOT-STAGE2-FIXTURE-ONLY-SOURCE-PROVIDER-RUNTIME-CLOSEOUT-READINESS-01.md"
CANONICAL_ID = "WEATHER-BOT-STAGE2-FIXTURE-ONLY-SOURCE-PROVIDER-RUNTIME-CLOSEOUT-READINESS-01"
NEXT_TICKET = "WEATHER-BOT-STAGE2-PHASE-SUMMARY-AND-HANDOFF-REFRESH-01"

SECTIONS = [
    "Status and scope",
    "Immediate predecessor and merge verification",
    "Closeout objective",
    "Approval relationship and controlling boundaries",
    "Complete fixture-only runtime-chain inventory",
    "Validation dependency order",
    "Positive full-chain integration-smoke posture",
    "Negative fail-closed smoke posture",
    "Canonical routing posture",
    "No-lookahead and fail-closed posture",
    "Operator-review and runtime-gate posture",
    "Stage 2 approved-scope completion conclusion",
    "Live provider and source-fetching boundary",
    "Stage 3 scoring and evaluation boundary",
    "Paper-simulation, runtime-observation, and execution boundary",
    "Persistence, export, queue, and workflow side-effect boundary",
    "Remaining blockers and explicit non-approvals",
    "Handoff-refresh requirement",
    "Recommended next ticket",
    "Machine-checkable Weather Bot Stage 2 fixture-only runtime closeout assignments",
    "Acceptance criteria",
]

MODULES = [
    ("meg/weather/stage2/fixture_only_source_provider_runtime.py", "FixtureOnlySourceProviderRecord", "FixtureOnlySourceProviderValidationResult", "fixture_only_source_provider_record_from_mapping", "validate_fixture_only_source_provider_record"),
    ("meg/weather/stage2/fixture_only_source_provider_evidence_bridge_runtime.py", "FixtureOnlySourceProviderEvidenceBridgeRecord", "FixtureOnlySourceProviderEvidenceBridgeValidationResult", "fixture_only_source_provider_evidence_bridge_record_from_mapping", "validate_fixture_only_source_provider_evidence_bridge_record"),
    ("meg/weather/stage2/fixture_only_source_provider_validation_bundle_bridge_runtime.py", "FixtureOnlySourceProviderValidationBundleBridgeRecord", "FixtureOnlySourceProviderValidationBundleBridgeValidationResult", "fixture_only_source_provider_validation_bundle_bridge_record_from_mapping", "validate_fixture_only_source_provider_validation_bundle_bridge_record"),
    ("meg/weather/stage2/fixture_only_source_provider_dry_run_bridge_runtime.py", "FixtureOnlySourceProviderDryRunBridgeRecord", "FixtureOnlySourceProviderDryRunBridgeValidationResult", "fixture_only_source_provider_dry_run_bridge_record_from_mapping", "validate_fixture_only_source_provider_dry_run_bridge_record"),
    ("meg/weather/stage2/fixture_only_source_provider_dry_run_report_bridge_runtime.py", "FixtureOnlySourceProviderDryRunReportBridgeRecord", "FixtureOnlySourceProviderDryRunReportBridgeValidationResult", "fixture_only_source_provider_dry_run_report_bridge_record_from_mapping", "validate_fixture_only_source_provider_dry_run_report_bridge_record"),
    ("meg/weather/stage2/fixture_only_source_provider_end_to_end_smoke_bridge_runtime.py", "FixtureOnlySourceProviderEndToEndSmokeBridgeRecord", "FixtureOnlySourceProviderEndToEndSmokeBridgeValidationResult", "fixture_only_source_provider_end_to_end_smoke_bridge_record_from_mapping", "validate_fixture_only_source_provider_end_to_end_smoke_bridge_record"),
    ("meg/weather/stage2/fixture_only_source_provider_trace_bridge_runtime.py", "FixtureOnlySourceProviderTraceBridgeRecord", "FixtureOnlySourceProviderTraceBridgeValidationResult", "fixture_only_source_provider_trace_bridge_record_from_mapping", "validate_fixture_only_source_provider_trace_bridge_record"),
    ("meg/weather/stage2/fixture_only_source_provider_operator_review_handoff_bridge_runtime.py", "FixtureOnlySourceProviderOperatorReviewHandoffBridgeRecord", "FixtureOnlySourceProviderOperatorReviewHandoffBridgeValidationResult", "fixture_only_source_provider_operator_review_handoff_bridge_record_from_mapping", "validate_fixture_only_source_provider_operator_review_handoff_bridge_record"),
    ("meg/weather/stage2/fixture_only_source_provider_operator_review_ack_bridge_runtime.py", "FixtureOnlySourceProviderOperatorReviewAckBridgeRecord", "FixtureOnlySourceProviderOperatorReviewAckBridgeValidationResult", "fixture_only_source_provider_operator_review_ack_bridge_record_from_mapping", "validate_fixture_only_source_provider_operator_review_ack_bridge_record"),
    ("meg/weather/stage2/fixture_only_source_provider_operator_review_queue_bridge_runtime.py", "FixtureOnlySourceProviderOperatorReviewQueueBridgeRecord", "FixtureOnlySourceProviderOperatorReviewQueueBridgeValidationResult", "fixture_only_source_provider_operator_review_queue_bridge_record_from_mapping", "validate_fixture_only_source_provider_operator_review_queue_bridge_record"),
    ("meg/weather/stage2/fixture_only_source_provider_operator_review_queue_entry_bridge_runtime.py", "FixtureOnlySourceProviderOperatorReviewQueueEntryBridgeRecord", "FixtureOnlySourceProviderOperatorReviewQueueEntryBridgeValidationResult", "fixture_only_source_provider_operator_review_queue_entry_bridge_record_from_mapping", "validate_fixture_only_source_provider_operator_review_queue_entry_bridge_record"),
    ("meg/weather/stage2/fixture_only_source_provider_operator_review_queue_summary_bridge_runtime.py", "FixtureOnlySourceProviderOperatorReviewQueueSummaryBridgeRecord", "FixtureOnlySourceProviderOperatorReviewQueueSummaryBridgeValidationResult", "fixture_only_source_provider_operator_review_queue_summary_bridge_record_from_mapping", "validate_fixture_only_source_provider_operator_review_queue_summary_bridge_record"),
    ("meg/weather/stage2/fixture_only_source_provider_operator_review_final_packet_bridge_runtime.py", "FixtureOnlySourceProviderOperatorReviewFinalPacketBridgeRecord", "FixtureOnlySourceProviderOperatorReviewFinalPacketBridgeValidationResult", "fixture_only_source_provider_operator_review_final_packet_bridge_record_from_mapping", "validate_fixture_only_source_provider_operator_review_final_packet_bridge_record"),
    ("meg/weather/stage2/fixture_only_source_provider_operator_review_final_bundle_bridge_runtime.py", "FixtureOnlySourceProviderOperatorReviewFinalBundleBridgeRecord", "FixtureOnlySourceProviderOperatorReviewFinalBundleBridgeValidationResult", "fixture_only_source_provider_operator_review_final_bundle_bridge_record_from_mapping", "validate_fixture_only_source_provider_operator_review_final_bundle_bridge_record"),
    ("meg/weather/stage2/fixture_only_source_provider_operator_review_completion_seal_bridge_runtime.py", "FixtureOnlySourceProviderOperatorReviewCompletionSealBridgeRecord", "FixtureOnlySourceProviderOperatorReviewCompletionSealBridgeValidationResult", "fixture_only_source_provider_operator_review_completion_seal_bridge_record_from_mapping", "validate_fixture_only_source_provider_operator_review_completion_seal_bridge_record"),
    ("meg/weather/stage2/fixture_only_source_provider_operator_review_completion_summary_bridge_runtime.py", "FixtureOnlySourceProviderOperatorReviewCompletionSummaryBridgeRecord", "FixtureOnlySourceProviderOperatorReviewCompletionSummaryBridgeValidationResult", "fixture_only_source_provider_operator_review_completion_summary_bridge_record_from_mapping", "validate_fixture_only_source_provider_operator_review_completion_summary_bridge_record"),
    ("meg/weather/stage2/fixture_only_source_provider_full_chain_integration_smoke_bridge_runtime.py", "FixtureOnlySourceProviderFullChainIntegrationSmokeBridgeRecord", "FixtureOnlySourceProviderFullChainIntegrationSmokeBridgeValidationResult", "fixture_only_source_provider_full_chain_integration_smoke_bridge_record_from_mapping", "validate_fixture_only_source_provider_full_chain_integration_smoke_bridge_record"),
    ("meg/weather/stage2/fixture_only_source_provider_full_chain_negative_smoke_bridge_runtime.py", "FixtureOnlySourceProviderFullChainNegativeSmokeBridgeRecord", "FixtureOnlySourceProviderFullChainNegativeSmokeBridgeValidationResult", "fixture_only_source_provider_full_chain_negative_smoke_bridge_record_from_mapping", "validate_fixture_only_source_provider_full_chain_negative_smoke_bridge_record"),
]


def _text() -> str:
    return DOC.read_text(encoding="utf-8")


def _section(text: str, name: str) -> str:
    marker = f"## {name}\n"
    assert marker in text
    rest = text.split(marker, 1)[1]
    return rest.split("\n## ", 1)[0].strip()


def _assignments(text: str) -> dict[str, set[str]]:
    section = _section(text, "Machine-checkable Weather Bot Stage 2 fixture-only runtime closeout assignments")
    assert section.startswith("```assignments")
    assert section.endswith("```")
    parsed: dict[str, set[str]] = {}
    for line in section.splitlines()[1:-1]:
        key, value = line.split(": ", 1)
        parsed.setdefault(key, set()).add(value)
    return parsed


def test_document_title_id_sections_and_predecessor() -> None:
    assert DOC.exists()
    text = _text()
    assert text.startswith(f"# {CANONICAL_ID}\n")
    assert f"Canonical ID: {CANONICAL_ID}" in text
    for section in SECTIONS:
        assert _section(text, section)
    predecessor = _section(text, "Immediate predecessor and merge verification")
    assert "PR #354" in predecessor
    assert "immediate merged predecessor" in predecessor
    assert "Merge pull request #354" in predecessor


def test_inventory_names_and_dependency_order() -> None:
    text = _text()
    inventory = _section(text, "Complete fixture-only runtime-chain inventory")
    order = _section(text, "Validation dependency order")
    last = -1
    for module, record, result, constructor, validator in MODULES:
        for expected in (module, record, result, constructor, validator):
            assert expected in inventory
        pos = order.index(module)
        assert pos > last
        last = pos


def test_positive_and_negative_smoke_semantics() -> None:
    text = _text()
    positive = _section(text, "Positive full-chain integration-smoke posture")
    assert "fully valid supplied chain" in positive
    assert "metadata validation only" in positive
    assert "does not execute or generate a smoke" in positive
    assert "runtime_gate_ready" in positive
    negative = _section(text, "Negative fail-closed smoke posture")
    assert "expected fail-closed result" in negative
    assert "positive bridge must pass validation" in negative
    assert "supplied negative-smoke record must pass validation" in negative
    assert "intentionally failing nested integration smoke is not directly required to pass" in negative
    assert "`ValidationSeverity.PASSED`" in negative
    assert "`passed=True`" in negative
    assert "`RuntimeGateStatus.RUNTIME_GATE_BLOCKED`" in negative
    assert "`runtime_gate_status` at `runtime_gate_blocked`" in negative
    assert "does not authorize progression, execution, smoke execution, or delivery" in negative
    assert "No failure is injected or generated" in negative
    assert "nested integration smoke must pass" not in negative.lower()


def test_domain_canonical_and_boundary_posture() -> None:
    text = _text()
    assert "Weather Bot models market settlement rules, not generic weather" in text
    canonical = _section(text, "Canonical routing posture")
    for field in ("condition_id", "token_id", "outcome"):
        assert field in canonical
    assert "`market_id` is non-routing only" in canonical
    assert "`token_outcome_pair` is derived only" in canonical
    assert "No timestamp parsing or comparison is approved" in canonical
    for section in (
        "Stage 3 scoring and evaluation boundary",
        "Paper-simulation, runtime-observation, and execution boundary",
        "Live provider and source-fetching boundary",
        "Persistence, export, queue, and workflow side-effect boundary",
    ):
        content = _section(text, section)
        assert "does not approve or implement" in content
    assert NEXT_TICKET in _section(text, "Recommended next ticket")


def test_assignment_parser_is_section_scoped_and_closed() -> None:
    text = _text() + "\noutside key: outside_value\n"
    assignments = _assignments(text)
    assert "outside key" not in assignments
    expected = {
        "weather bot planning stage": {"weather_bot_stage2_fixture_only_source_provider_runtime_closeout_readiness"},
        "immediate predecessor pr": {"pr_354"},
        "closeout lifecycle status": {"docs_static_test_only", "closeout_readiness_only", "no_runtime_code_change"},
        "approved scope status": {"fixture_only_source_provider_runtime_chain_complete", "local_static_caller_supplied_only", "positive_full_chain_validation_recorded", "expected_fail_closed_negative_smoke_recorded", "stage2_approved_scope_code_complete"},
        "runtime chain module": {m[0] for m in MODULES},
        "canonical routing field": {"condition_id", "token_id", "outcome"},
        "non routing field": {"market_id"},
        "derived identifier field": {"token_outcome_pair"},
        "positive smoke posture": {"supplied_metadata_validation_only", "no_smoke_execution", "runtime_gate_ready_required"},
        "negative smoke posture": {"expected_fail_closed_representation", "nested_integration_smoke_expected_to_fail", "bridge_validation_passed", "runtime_gate_blocked", "no_failure_injection"},
        "live runtime posture": {"live_provider_runtime_not_approved", "live_source_fetching_not_approved"},
        "stage3 posture": {"stage3_not_approved", "scoring_not_approved", "evaluation_execution_not_approved"},
        "later stage posture": {"paper_simulation_not_approved", "runtime_observation_not_approved", "trading_execution_not_approved"},
        "persistence posture": {"no_persistence", "no_export_writing"},
        "service posture": {"no_real_queue_service", "no_scheduler", "no_broker"},
        "workflow posture": {"no_owner_decision_capture", "no_operator_decision_execution", "no_durable_completion_side_effect"},
        "recommended next ticket": {"weather_bot_stage2_phase_summary_and_handoff_refresh_01"},
        "fresh chat posture": {"handoff_refresh_required_before_new_chat"},
        "evidence status": {"closeout_readiness_recorded"},
        "label confidence": {"confirmed"},
    }
    assert assignments == expected


def test_no_prohibited_positive_approval_claims() -> None:
    text = _text().lower()
    prohibited_subjects = (
        "live provider", "live source fetching", "stage 3", "stage3", "scoring",
        "evaluation", "paper", "runtime observation", "trading", "execution",
        "persistence", "export", "queue", "scheduler", "broker", "workflow-completion",
        "production", "autonomy",
    )
    for subject in prohibited_subjects:
        assert f"{subject} is approved" not in text
        assert f"{subject} is enabled" not in text
        assert f"{subject} is production ready" not in text
    assert "no later stage begins automatically" in text
    assert "stage 3 begins automatically" not in text
