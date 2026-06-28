"""Static checks for Source Identity Runtime Static Integration Review."""
from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CANONICAL_ID = "SOURCE-IDENTITY-RUNTIME-STATIC-INTEGRATION-REVIEW-01"
ARTIFACT_PATH = REPO_ROOT / f"docs/prd/{CANONICAL_ID}.md"
MACHINE_HEADING = "## Machine-checkable source-identity runtime static integration-review assignments"

REQUIRED_SECTIONS = (
    "Status and scope",
    "Relationship to source identity runtime scaffold",
    "Relationship to runtime static scaffold",
    "Relationship to Weather Bot PRD and architecture alignment",
    "Integration review objective",
    "Source identity record summary",
    "Safe future consumer surfaces",
    "Retrieval context consumption boundary",
    "Provider/source family consumption boundary",
    "Manual review gate consumption boundary",
    "No-lookahead metadata gate consumption boundary",
    "Fail-closed validation consumption boundary",
    "Static audit surface consumption boundary",
    "Runtime boundary",
    "Provider/source execution boundary",
    "Credential/config boundary",
    "Generated-data and fixture boundary",
    "Scoring/backtesting boundary",
    "Trading/autonomy/production boundary",
    "Canonical identifier posture",
    "Blocked integration work",
    "Recommended next ticket",
    "Machine-checkable source-identity runtime static integration-review assignments",
    "Acceptance criteria",
)
RELATIONSHIP_REFERENCES = {
    CANONICAL_ID,
    "meg/weather/stage2/source_identity_runtime.py",
    "SourceIdentityRecord",
    "SourceIdentityValidationResult",
    "validate_source_identity_record",
    "PRD-P1-WX-STAGE2-SOURCE-FETCHING-RUNTIME-STATIC-SCAFFOLD-01",
    "PRD-P1-WX-STAGE2-SOURCE-FETCHING-RUNTIME-IMPLEMENTATION-PLAN-01",
    "PRD-P1-WX-STAGE2-WEATHER-BOT-RETURN-TO-PLANNING-01",
    "PRD-P1-WX-STANDALONE_WEATHER_BOT_PRD",
}
SOURCE_IDENTITY_RECORD_FIELDS = {
    "condition_id",
    "token_id",
    "outcome",
    "source_id",
    "source_family",
    "source_uri_descriptor",
    "source_access_method",
    "source_identity_status",
    "runtime_gate_status",
    "provenance_notes",
}
SAFE_FUTURE_CONSUMER_SURFACES = {
    "retrieval_context_runtime",
    "provider_source_family_runtime",
    "manual_review_gate_runtime",
    "no_lookahead_metadata_runtime",
    "fail_closed_validation_runtime",
    "static_audit_surface_runtime",
}
ALLOWED_FUTURE_CONSUMPTION_POSTURES = {
    "read_source_identity_record_only",
    "require_validated_source_identity",
    "fail_closed_on_invalid_source_identity",
    "preserve_condition_id_token_id_outcome",
    "manual_review_or_static_reference_only",
    "no_provider_execution",
    "no_live_fetching",
    "no_credentials_config_loading",
    "no_generated_data",
    "no_fixture_change",
    "no_scoring_backtesting",
    "no_trading_autonomy_production",
}
BLOCKED_INTEGRATION_WORK = {
    "retrieval_context_runtime_implementation",
    "provider_source_family_runtime_implementation",
    "manual_review_gate_runtime_implementation",
    "no_lookahead_metadata_runtime_implementation",
    "fail_closed_validation_runtime_implementation",
    "static_audit_surface_runtime_implementation",
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
}
ALLOWED_ASSIGNMENTS = {
    "weather bot planning stage": {"source_identity_runtime_static_integration_review"},
    "integration review status": {
        "docs_static_test_only",
        "review_only",
        "post_pr_263_source_identity_runtime_scaffold",
    },
    "current state posture": {"source_identity_runtime_scaffold_landed", "integration_not_implemented"},
    "source identity artifact": {
        "source_identity_runtime_py",
        "SourceIdentityRecord",
        "SourceIdentityValidationResult",
        "validate_source_identity_record",
    },
    "source identity record field": SOURCE_IDENTITY_RECORD_FIELDS,
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
    },
    "recommended next track": {"retrieval_context_runtime_scaffold"},
    "conditional next track": {
        "source_identity_integration_review_revision_if_scope_too_broad",
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
        "PR #263 added `meg/weather/stage2/source_identity_runtime.py`",
        "PR #263 added `SourceIdentityRecord`",
        "PR #263 added `SourceIdentityValidationResult`",
        "PR #263 added fail-closed validation through `validate_source_identity_record`",
        "does not modify `meg/`",
        "does not implement retrieval context code",
        "does not implement provider/source family code",
        "does not implement manual review gate code",
        "does not implement no-lookahead metadata gate code",
        "does not implement fail-closed validation gate code beyond review/planning",
        "does not implement static audit runtime code",
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
        "Weather Bot models the market settlement rule, not generic weather",
        "No routing on `market_id` is introduced or approved",
        "Recommended next track: `retrieval_context_runtime_scaffold`",
    ]
    for phrase in required_phrases:
        assert phrase in text


def test_fields_surfaces_postures_and_blocked_work_are_present() -> None:
    text = _read()
    for value in (
        SOURCE_IDENTITY_RECORD_FIELDS
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
    assert assignments["source identity record field"] == SOURCE_IDENTITY_RECORD_FIELDS
    assert assignments["safe future consumer surface"] == SAFE_FUTURE_CONSUMER_SURFACES
    assert assignments["allowed future consumption posture"] == ALLOWED_FUTURE_CONSUMPTION_POSTURES
    assert assignments["blocked integration work"] == BLOCKED_INTEGRATION_WORK
    assert assignments["recommended next track"] == {"retrieval_context_runtime_scaffold"}


def test_synthetic_parser_scoping_ignores_assignments_after_next_heading() -> None:
    synthetic = (
        f"{MACHINE_HEADING}\n"
        "- recommended next track: retrieval_context_runtime_scaffold\n"
        "## Later heading\n"
        "- recommended next track: source_fetching_implementation\n"
    )
    assert _assignments(synthetic) == {
        "recommended next track": {"retrieval_context_runtime_scaffold"}
    }


def test_document_does_not_assert_provider_credentials_data_or_execution_approval() -> None:
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
    ]
    for pattern in forbidden_positive_patterns:
        assert not re.search(pattern, text)
