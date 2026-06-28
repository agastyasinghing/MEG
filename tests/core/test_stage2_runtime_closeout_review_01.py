"""Static checks for Stage 2 Runtime Closeout Review."""
from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CANONICAL_ID = "STAGE2-RUNTIME-CLOSEOUT-REVIEW-01"
ARTIFACT_PATH = REPO_ROOT / f"docs/prd/{CANONICAL_ID}.md"
MACHINE_HEADING = "## Machine-checkable Stage 2 runtime closeout assignments"

REQUIRED_SECTIONS = (
    "Status and scope",
    "Relationship to Weather Bot PRD and architecture alignment",
    "Closeout objective",
    "Landed Stage 2 runtime metadata artifacts",
    "Validation dependency chain",
    "Source identity runtime closeout",
    "Retrieval context runtime closeout",
    "Provider/source-family runtime closeout",
    "Manual review gate runtime closeout",
    "No-lookahead metadata runtime closeout",
    "Fail-closed validation runtime closeout",
    "Static audit surface runtime closeout",
    "Static integration review artifacts",
    "Supplied-metadata-only boundary",
    "Runtime boundary",
    "Provider/source execution boundary",
    "Credential/config boundary",
    "Generated-data and fixture boundary",
    "Scoring/backtesting boundary",
    "Trading/autonomy/production boundary",
    "Audit report and export boundary",
    "Canonical identifier posture",
    "Blocked work after closeout",
    "Recommended next ticket",
    "Machine-checkable Stage 2 runtime closeout assignments",
    "Acceptance criteria",
)
RUNTIME_MODULE_PATHS = {
    "meg/weather/stage2/source_identity_runtime.py",
    "meg/weather/stage2/retrieval_context_runtime.py",
    "meg/weather/stage2/provider_source_family_runtime.py",
    "meg/weather/stage2/manual_review_gate_runtime.py",
    "meg/weather/stage2/no_lookahead_metadata_runtime.py",
    "meg/weather/stage2/fail_closed_validation_runtime.py",
    "meg/weather/stage2/static_audit_surface_runtime.py",
}
RUNTIME_RECORDS = {
    "SourceIdentityRecord",
    "RetrievalContextRecord",
    "ProviderSourceFamilyRecord",
    "ManualReviewGateRecord",
    "NoLookaheadMetadataRecord",
    "FailClosedValidationRecord",
    "StaticAuditSurfaceRecord",
}
RUNTIME_VALIDATORS = {
    "validate_source_identity_record",
    "validate_retrieval_context_record",
    "validate_provider_source_family_record",
    "validate_manual_review_gate_record",
    "validate_no_lookahead_metadata_record",
    "validate_fail_closed_validation_record",
    "validate_static_audit_surface_record",
}
VALIDATION_DEPENDENCY_ORDER = {
    "source_identity_runtime",
    "retrieval_context_runtime",
    "provider_source_family_runtime",
    "manual_review_gate_runtime",
    "no_lookahead_metadata_runtime",
    "fail_closed_validation_runtime",
    "static_audit_surface_runtime",
}
ALLOWED_FUTURE_CONSUMPTION_POSTURES = {
    "read_landed_stage2_runtime_metadata_only",
    "require_validated_upstream_metadata",
    "fail_closed_on_invalid_stage2_metadata",
    "preserve_condition_id_token_id_outcome",
    "supplied_metadata_only",
    "no_source_fetching",
    "no_provider_execution",
    "no_live_fetching",
    "no_credentials_config_loading",
    "no_generated_data",
    "no_fixture_change",
    "no_scoring_backtesting",
    "no_trading_autonomy_production",
    "no_report_writing",
    "no_external_export",
    "no_persistence",
}
BLOCKED_WORK_AFTER_CLOSEOUT = {
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
    "weather bot planning stage": {"stage2_runtime_closeout_review"},
    "closeout status": {
        "docs_static_test_only",
        "closeout_only",
        "post_pr_272_static_audit_surface_integration_review",
    },
    "current state posture": {
        "stage2_runtime_metadata_scaffold_sequence_landed",
        "source_fetching_not_implemented",
        "downstream_runtime_integration_not_implemented",
    },
    "landed runtime artifact": {
        "source_identity_runtime_py",
        "retrieval_context_runtime_py",
        "provider_source_family_runtime_py",
        "manual_review_gate_runtime_py",
        "no_lookahead_metadata_runtime_py",
        "fail_closed_validation_runtime_py",
        "static_audit_surface_runtime_py",
    },
    "landed runtime record": RUNTIME_RECORDS,
    "landed runtime validator": RUNTIME_VALIDATORS,
    "validation dependency order": VALIDATION_DEPENDENCY_ORDER,
    "static integration review artifact": {
        "SOURCE-IDENTITY-RUNTIME-STATIC-INTEGRATION-REVIEW-01",
        "PROVIDER-SOURCE-FAMILY-RUNTIME-STATIC-INTEGRATION-REVIEW-01",
        "STATIC-AUDIT-SURFACE-RUNTIME-STATIC-INTEGRATION-REVIEW-01",
    },
    "allowed future consumption posture": ALLOWED_FUTURE_CONSUMPTION_POSTURES,
    "blocked work after closeout": BLOCKED_WORK_AFTER_CLOSEOUT,
    "provider source posture": {
        "provider_connectors_not_approved",
        "provider_clients_not_created",
        "live_provider_source_fetching_not_approved",
        "closeout_review_only",
    },
    "credential config posture": {"unknown_requires_review"},
    "generated data fixture posture": {"no_generated_data", "no_fixture_change"},
    "audit output posture": {"no_report_writing", "no_external_export", "no_persistence"},
    "implementation posture": {
        "docs_static_test_only",
        "closeout_only",
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
    "recommended next track": {"source_fetching_runtime_readiness_review"},
    "conditional next track": {
        "stage2_runtime_closeout_revision_if_scope_too_broad",
        "hold_checkpoint_if_source_fetching_readiness_not_desired",
    },
    "evidence status": {"closeout_review_recorded"},
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
    references = {
        CANONICAL_ID,
        "PRD-P1-WX-STAGE2-WEATHER-BOT-RETURN-TO-PLANNING-01",
        "PRD-P1-WX-STANDALONE_WEATHER_BOT_PRD",
        "SOURCE-IDENTITY-RUNTIME-STATIC-INTEGRATION-REVIEW-01",
        "PROVIDER-SOURCE-FAMILY-RUNTIME-STATIC-INTEGRATION-REVIEW-01",
        "STATIC-AUDIT-SURFACE-RUNTIME-STATIC-INTEGRATION-REVIEW-01",
        "static_audit_summary",
    }
    for reference in references | RUNTIME_MODULE_PATHS | RUNTIME_RECORDS | RUNTIME_VALIDATORS:
        assert reference in text


def test_required_docs_static_closeout_posture_and_scope_boundaries() -> None:
    text = _read()
    required_phrases = [
        "docs/static-test-only/closeout-only",
        "does not modify `meg/`",
        "does not implement new runtime behavior",
        "closes out the current Stage 2 runtime metadata scaffold sequence",
        "Weather Bot models the market settlement rule, not generic weather",
        "All Stage 2 runtime metadata artifacts remain supplied-metadata-only and fail-closed",
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
        "No routing on `market_id` is introduced or approved",
    ]
    for phrase in required_phrases:
        assert phrase in text


def test_landed_artifacts_dependency_order_and_postures_appear() -> None:
    text = _read()
    for value in (
        RUNTIME_MODULE_PATHS
        | RUNTIME_RECORDS
        | RUNTIME_VALIDATORS
        | VALIDATION_DEPENDENCY_ORDER
        | ALLOWED_FUTURE_CONSUMPTION_POSTURES
        | BLOCKED_WORK_AFTER_CLOSEOUT
    ):
        assert value in text


def test_no_forbidden_execution_or_output_approval_phrases() -> None:
    text = _read().lower()
    forbidden_pattern_parts = [
        ("provider connector", "is approved"),
        ("provider client", "is created"),
        ("source fetching", "is approved"),
        ("source fetching implementation", "is approved"),
        ("live provider source fetching", "is approved"),
        ("forecast pull", "is approved"),
        ("api call", "is approved"),
        ("scraping", "is approved"),
        ("file download", "is approved"),
        ("provider sdk", "is approved"),
        ("credentials", r".*loading " + "is approved"),
        ("generated data", "is approved"),
        ("fixture change", "is approved"),
        ("scoring", "is approved"),
        ("backtesting", "is approved"),
        ("trading", "is approved"),
        ("order placement", "is approved"),
        ("autonomy", "is approved"),
        ("production behavior", "is approved"),
        ("report writing", "is approved"),
        ("external export", "is approved"),
        ("persistence", "is approved"),
    ]
    forbidden_patterns = [f"{prefix} {suffix}" for prefix, suffix in forbidden_pattern_parts]
    for pattern in forbidden_patterns:
        assert not re.search(pattern, text), pattern


def test_canonical_identifier_contract_and_no_market_id_routing() -> None:
    text = _read()
    canonical_section = _section(text, "Canonical identifier posture")
    for identifier in ("condition_id", "token_id", "outcome"):
        assert f"`{identifier}`" in canonical_section
    assert "No routing on `market_id` is introduced or approved" in canonical_section


def test_machine_checkable_assignments_are_complete_and_allowed() -> None:
    assignments = _assignments(_read())
    assert set(assignments) == set(ALLOWED_ASSIGNMENTS)
    for field, allowed_values in ALLOWED_ASSIGNMENTS.items():
        assert assignments[field] == allowed_values


def test_machine_checkable_parser_is_section_scoped() -> None:
    text = _read()
    machine_section = _machine_section(text)
    assert "Acceptance criteria" not in machine_section

    synthetic = (
        "# Example\n\n"
        f"{MACHINE_HEADING}\n\n"
        "- evidence status: closeout_review_recorded\n\n"
        "## Acceptance criteria\n\n"
        "- evidence status: forged_after_next_heading\n"
    )
    parsed = _assignments(synthetic)
    assert parsed == {"evidence status": {"closeout_review_recorded"}}


def test_recommended_next_track_is_readiness_only_not_implementation_approval() -> None:
    text = _read()
    recommended = _section(text, "Recommended next ticket")
    assert "Recommended next track: `source_fetching_runtime_readiness_review`" in recommended
    assert "readiness review only, not implementation approval" in recommended
    assert "must not itself approve source fetching implementation" in recommended
    assignments = _assignments(text)
    assert assignments["recommended next track"] == {"source_fetching_runtime_readiness_review"}
