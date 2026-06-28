"""Static checks for Static Audit Surface Runtime Static Integration Review."""
from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CANONICAL_ID = "STATIC-AUDIT-SURFACE-RUNTIME-STATIC-INTEGRATION-REVIEW-01"
ARTIFACT_PATH = REPO_ROOT / f"docs/prd/{CANONICAL_ID}.md"
MACHINE_HEADING = (
    "## Machine-checkable static audit surface runtime static integration-review assignments"
)

REQUIRED_SECTIONS = (
    "Status and scope",
    "Relationship to static audit surface runtime scaffold",
    "Relationship to fail-closed validation runtime scaffold",
    "Relationship to no-lookahead metadata runtime scaffold",
    "Relationship to manual review gate runtime scaffold",
    "Relationship to provider/source-family runtime scaffold",
    "Relationship to retrieval context runtime scaffold",
    "Relationship to source identity runtime scaffold",
    "Relationship to Weather Bot PRD and architecture alignment",
    "Integration review objective",
    "Static audit surface record summary",
    "Safe future consumer surfaces",
    "Read-only audit boundary",
    "Runtime boundary",
    "Provider/source execution boundary",
    "Credential/config boundary",
    "Generated-data and fixture boundary",
    "Scoring/backtesting boundary",
    "Trading/autonomy/production boundary",
    "Audit report and export boundary",
    "Canonical identifier posture",
    "Blocked integration work",
    "Recommended next ticket",
    "Machine-checkable static audit surface runtime static integration-review assignments",
    "Acceptance criteria",
)
RELATIONSHIP_REFERENCES = {
    CANONICAL_ID,
    "meg/weather/stage2/static_audit_surface_runtime.py",
    "StaticAuditSurfaceRecord",
    "StaticAuditSurfaceValidationResult",
    "validate_static_audit_surface_record",
    "static_audit_summary",
    "meg/weather/stage2/fail_closed_validation_runtime.py",
    "FailClosedValidationRecord",
    "meg/weather/stage2/no_lookahead_metadata_runtime.py",
    "NoLookaheadMetadataRecord",
    "meg/weather/stage2/manual_review_gate_runtime.py",
    "ManualReviewGateRecord",
    "meg/weather/stage2/provider_source_family_runtime.py",
    "ProviderSourceFamilyRecord",
    "meg/weather/stage2/retrieval_context_runtime.py",
    "RetrievalContextRecord",
    "meg/weather/stage2/source_identity_runtime.py",
    "SourceIdentityRecord",
    "PRD-P1-WX-STAGE2-WEATHER-BOT-RETURN-TO-PLANNING-01",
    "PRD-P1-WX-STANDALONE_WEATHER_BOT_PRD",
}
STATIC_AUDIT_SURFACE_RECORD_FIELDS = {
    "condition_id",
    "token_id",
    "outcome",
    "source_identity",
    "retrieval_context",
    "provider_source_family",
    "manual_review_gate",
    "no_lookahead_metadata",
    "fail_closed_validation",
    "static_audit_surface_status",
    "audit_presentation_mode",
    "audit_evidence_status",
    "runtime_gate_status",
    "provenance_notes",
}
SAFE_FUTURE_CONSUMER_SURFACES = {
    "stage2_runtime_closeout_review",
    "source_fetching_runtime_readiness_review",
    "paper_trade_readiness_review",
    "static_audit_surface_closeout",
}
ALLOWED_FUTURE_CONSUMPTION_POSTURES = {
    "read_static_audit_surface_record_only",
    "require_validated_static_audit_surface",
    "fail_closed_on_invalid_static_audit_surface",
    "preserve_condition_id_token_id_outcome",
    "read_only_summary_or_detail_only",
    "no_report_writing",
    "no_external_export",
    "no_persistence",
    "no_provider_execution",
    "no_live_fetching",
    "no_credentials_config_loading",
    "no_generated_data",
    "no_fixture_change",
    "no_scoring_backtesting",
    "no_trading_autonomy_production",
}
BLOCKED_INTEGRATION_WORK = {
    "downstream_runtime_implementation",
    "source_fetching_implementation",
    "provider_connector_implementation",
    "provider_client_creation",
    "live_provider_source_fetching",
    "forecast_pull_execution",
    "api_call_execution",
    "scraping_execution",
    "file_download_execution",
    "provider_sdk_execution",
    "credentials_config_loading",
    "generated_data_creation",
    "fixture_data_modification",
    "scoring_implementation",
    "backtesting_implementation",
    "runtime_trading_behavior",
    "order_placement",
    "autonomy_behavior",
    "production_behavior",
    "audit_report_generation",
    "audit_output_persistence",
    "external_export_behavior",
}
ALLOWED_ASSIGNMENTS = {
    "weather bot planning stage": {"static_audit_surface_runtime_static_integration_review"},
    "integration review status": {
        "docs_static_test_only",
        "review_only",
        "post_pr_271_static_audit_surface_runtime_scaffold",
    },
    "current state posture": {
        "static_audit_surface_runtime_scaffold_landed",
        "downstream_integration_not_implemented",
    },
    "static audit surface artifact": {
        "static_audit_surface_runtime_py",
        "StaticAuditSurfaceRecord",
        "StaticAuditSurfaceValidationResult",
        "validate_static_audit_surface_record",
        "static_audit_summary",
    },
    "static audit surface record field": STATIC_AUDIT_SURFACE_RECORD_FIELDS,
    "safe future consumer surface": SAFE_FUTURE_CONSUMER_SURFACES,
    "allowed future consumption posture": ALLOWED_FUTURE_CONSUMPTION_POSTURES,
    "blocked integration work": BLOCKED_INTEGRATION_WORK,
    "provider source posture": {
        "provider_connectors_not_approved",
        "provider_clients_not_created",
        "live_provider_source_fetching_not_approved",
        "integration_review_only",
    },
    "credential config posture": {"unknown_requires_review"},
    "generated data fixture posture": {"no_generated_data", "no_fixture_change"},
    "audit output posture": {"no_report_writing", "no_external_export", "no_persistence"},
    "implementation posture": {
        "docs_static_test_only",
        "review_only",
        "no_runtime_code_change",
        "no_source_fetching",
        "no_provider_connector",
        "no_provider_client",
        "no_live_provider_fetching",
        "no_credential_config_loading",
        "no_generated_data",
        "no_fixture_change",
        "no_scoring_backtesting",
        "no_trading_autonomy_production",
        "no_report_writing",
        "no_external_export",
        "no_persistence",
    },
    "recommended next track": {"stage2_runtime_closeout_review"},
    "conditional next track": {
        "static_audit_surface_integration_review_revision_if_scope_too_broad",
        "hold_checkpoint_if_runtime_integration_not_desired",
    },
    "evidence status": {"integration_review_recorded"},
    "label confidence": {"confirmed"},
}
ASSIGNMENT_RE = re.compile(r"^- (?P<field>[^:]+): (?P<value>\S+)\s*$", re.MULTILINE)


def _read() -> str:
    return ARTIFACT_PATH.read_text(encoding="utf-8")


def _section(text: str, heading: str) -> str:
    match = re.search(
        rf"^## {re.escape(heading)}\n(?P<section>.*?)(?:\n## |\Z)",
        text,
        re.MULTILINE | re.DOTALL,
    )
    assert match, f"Missing section: {heading}"
    assert match.group("section").strip(), f"Section is empty: {heading}"
    return match.group("section")


def _machine_section(text: str) -> str:
    return _section(text, MACHINE_HEADING.removeprefix("## "))


def _assignments(text: str) -> dict[str, set[str]]:
    result: dict[str, set[str]] = {}
    for match in ASSIGNMENT_RE.finditer(_machine_section(text)):
        result.setdefault(match.group("field"), set()).add(match.group("value"))
    return result


def test_document_exists_canonical_sections_and_relationships() -> None:
    assert ARTIFACT_PATH.exists()
    text = _read()
    assert f"Canonical ID: {CANONICAL_ID}" in text
    for heading in REQUIRED_SECTIONS:
        _section(text, heading)
    for reference in RELATIONSHIP_REFERENCES:
        assert reference in text


def test_required_docs_static_review_posture_and_scope_boundaries() -> None:
    text = _read()
    required_phrases = [
        "docs/static-test-only/review-only",
        "PR #271 added `meg/weather/stage2/static_audit_surface_runtime.py`",
        "PR #271 added `StaticAuditSurfaceRecord`",
        "PR #271 added `StaticAuditSurfaceValidationResult`",
        "PR #271 added `validate_static_audit_surface_record`",
        "PR #271 added deterministic read-only `static_audit_summary`",
        "does not modify `meg/`",
        "does not implement downstream runtime behavior",
        "does not fetch sources",
        "does not call providers",
        "does not create provider connectors",
        "does not create provider clients",
        "does not approve live provider/source fetching",
        "does not approve forecast pulls",
        "does not approve API calls",
        "does not approve scraping",
        "does not approve file downloads",
        "does not approve provider SDK usage",
        "does not approve credentials/secrets/config loading",
        "does not approve generated data",
        "does not approve fixture changes",
        "does not approve scoring",
        "does not approve backtesting",
        "does not approve runtime trading",
        "does not approve order placement",
        "does not approve autonomy",
        "does not approve production behavior",
        "does not approve report writing",
        "does not approve audit output persistence",
        "does not approve external export",
        "Weather Bot models the market settlement rule, not generic weather",
        "No routing on `market_id` is introduced or approved",
        "Recommended next track: `stage2_runtime_closeout_review`",
    ]
    for phrase in required_phrases:
        assert phrase in text


def test_fields_surfaces_postures_and_blocked_work_are_present() -> None:
    text = _read()
    for value in (
        STATIC_AUDIT_SURFACE_RECORD_FIELDS
        | SAFE_FUTURE_CONSUMER_SURFACES
        | ALLOWED_FUTURE_CONSUMPTION_POSTURES
        | BLOCKED_INTEGRATION_WORK
    ):
        assert f"`{value}`" in text


def test_canonical_identifier_contract_preserved_without_noncanonical_routing() -> None:
    text = _read()
    for identifier in ("condition_id", "token_id", "outcome"):
        assert f"`{identifier}`" in text
    assert "No routing on `market_id` is introduced or approved" in text


def test_machine_checkable_assignments_are_section_scoped_and_allowed() -> None:
    assignments = _assignments(_read())
    assert set(assignments) == set(ALLOWED_ASSIGNMENTS)
    for field, allowed_values in ALLOWED_ASSIGNMENTS.items():
        assert assignments[field]
        assert assignments[field] <= allowed_values
        assert allowed_values <= assignments[field]
    assert assignments["static audit surface record field"] == STATIC_AUDIT_SURFACE_RECORD_FIELDS
    assert assignments["safe future consumer surface"] == SAFE_FUTURE_CONSUMER_SURFACES
    assert assignments["allowed future consumption posture"] == ALLOWED_FUTURE_CONSUMPTION_POSTURES
    assert assignments["blocked integration work"] == BLOCKED_INTEGRATION_WORK
    assert assignments["recommended next track"] == {"stage2_runtime_closeout_review"}


def test_synthetic_parser_scoping_ignores_assignments_after_next_heading() -> None:
    synthetic = (
        f"{MACHINE_HEADING}\n"
        "- recommended next track: stage2_runtime_closeout_review\n"
        "## Later heading\n"
        "- recommended next track: source_fetching_implementation\n"
    )
    assert _assignments(synthetic) == {
        "recommended next track": {"stage2_runtime_closeout_review"}
    }


def test_document_does_not_assert_provider_credentials_data_execution_or_export_approval() -> None:
    text = _read().lower()
    forbidden_positive_patterns = [
        r"provider connector is " + r"approved",
        r"provider client is " + r"created",
        r"source fetching is " + r"approved",
        r"live provider source fetching is " + r"approved",
        r"forecast pull is " + r"approved",
        r"api call is " + r"approved",
        r"scraping is " + r"approved",
        r"file download is " + r"approved",
        r"provider sdk is " + r"approved",
        r"credentials.*loading is " + r"approved",
        r"generated data is " + r"approved",
        r"fixture change is " + r"approved",
        r"scoring is " + r"approved",
        r"backtesting is " + r"approved",
        r"trading is " + r"approved",
        r"order placement is " + r"approved",
        r"autonomy is " + r"approved",
        r"production behavior is " + r"approved",
        r"report writing is " + r"approved",
        r"external export is " + r"approved",
        r"persistence is " + r"approved",
    ]
    for pattern in forbidden_positive_patterns:
        assert not re.search(pattern, text)
