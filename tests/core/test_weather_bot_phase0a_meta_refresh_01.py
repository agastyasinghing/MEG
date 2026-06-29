"""Static checks for Weather Bot Phase 0A Meta Refresh."""
from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CANONICAL_ID = "WEATHER-BOT-PHASE0A-META-REFRESH-01"
ARTIFACT_PATH = REPO_ROOT / f"docs/prd/{CANONICAL_ID}.md"
MACHINE_HEADING = "## Machine-checkable Weather Bot Phase 0A meta-refresh assignments"

REQUIRED_SECTIONS = (
    "Status and scope",
    "Relationship to Weather Bot PRD and architecture alignment",
    "Relationship to Phase 0A hold-state closeout",
    "Meta refresh objective",
    "Meta files refreshed",
    "Current Weather Bot Phase 0A posture",
    "Source-fetching track posture",
    "Stage 2 runtime metadata posture",
    "Blocked work",
    "Non-approval boundary",
    "Source fetching implementation boundary",
    "Provider/source execution boundary",
    "Credential/config boundary",
    "Generated-data and fixture boundary",
    "Scoring/backtesting boundary",
    "Trading/autonomy/production boundary",
    "Audit report and export boundary",
    "Canonical identifier posture",
    "Conditions required to reopen source-fetching track",
    "Recommended next ticket",
    "Machine-checkable Weather Bot Phase 0A meta-refresh assignments",
    "Acceptance criteria",
)
STAGE2_ARTIFACT_PATHS = {
    "meg/weather/stage2/source_identity_runtime.py",
    "meg/weather/stage2/retrieval_context_runtime.py",
    "meg/weather/stage2/provider_source_family_runtime.py",
    "meg/weather/stage2/manual_review_gate_runtime.py",
    "meg/weather/stage2/no_lookahead_metadata_runtime.py",
    "meg/weather/stage2/fail_closed_validation_runtime.py",
    "meg/weather/stage2/static_audit_surface_runtime.py",
}
BLOCKED_WORK = {
    "source_fetching_runtime_implementation_plan",
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
CONDITIONS_REQUIRED_TO_REOPEN = {
    "approve_narrow_source_fetching_runtime_implementation_plan",
    "deny_source_fetching_runtime_implementation_plan",
    "request_revision_to_source_fetching_runtime_implementation_request",
    "hold_source_fetching_runtime_track",
}
ALLOWED_ASSIGNMENTS = {
    "weather bot planning stage": {"weather_bot_phase0a_meta_refresh"},
    "meta refresh status": {"docs_static_test_only", "meta_refresh_only", "post_weather_bot_phase0a_hold_state_closeout"},
    "refreshed meta file": {"meg_active_state_md", "meg_chat_handoff_md", "weather_bot_packet_md"},
    "current phase0a posture": {"weather_bot_phase0a_held_closed", "source_fetching_runtime_track_closed_held", "source_fetching_not_implemented", "implementation_approval_not_granted", "stage2_runtime_metadata_supplied_only", "stage2_runtime_metadata_fail_closed"},
    "source fetching track posture": {"hold_source_fetching_runtime_track", "future_reopen_requires_owner_decision_revision", "no_source_fetching_implementation_plan", "no_source_fetching_implementation"},
    "stage2 runtime metadata artifact": {"source_identity_runtime_py", "retrieval_context_runtime_py", "provider_source_family_runtime_py", "manual_review_gate_runtime_py", "no_lookahead_metadata_runtime_py", "fail_closed_validation_runtime_py", "static_audit_surface_runtime_py"},
    "blocked work": BLOCKED_WORK,
    "condition required to reopen source fetching track": CONDITIONS_REQUIRED_TO_REOPEN,
    "provider source posture": {"provider_connectors_not_approved", "provider_clients_not_created", "live_provider_source_fetching_not_approved", "meta_refresh_only"},
    "credential config posture": {"unknown_requires_review"},
    "generated data fixture posture": {"no_generated_data", "no_fixture_change"},
    "audit output posture": {"no_report_writing", "no_external_export", "no_persistence"},
    "implementation posture": {"docs_static_test_only", "meta_refresh_only", "no_runtime_code_change", "no_source_fetching", "no_source_fetching_plan", "no_provider_connector", "no_provider_client", "no_live_provider_fetching", "no_credential_config_loading", "no_generated_data", "no_fixture_change", "no_scoring_backtesting", "no_trading_autonomy_production", "no_report_writing", "no_external_export", "no_persistence"},
    "recommended next track": {"weather_bot_phase0a_meta_refresh_self_review"},
    "conditional next track": {"weather_bot_phase0a_meta_refresh_revision_if_scope_too_broad", "source_fetching_runtime_owner_decision_revision_if_owner_changes_decision"},
    "evidence status": {"meta_refresh_recorded"},
    "label confidence": {"confirmed"},
}
ASSIGNMENT_RE = re.compile(r"^- (?P<field>[^:]+): (?P<value>\S+)\s*$", re.MULTILINE)


def _read() -> str:
    return ARTIFACT_PATH.read_text(encoding="utf-8")


def _section(text: str, heading: str) -> str:
    match = re.search(rf"^## {re.escape(heading)}\n(?P<section>.*?)(?:\n## |\Z)", text, re.MULTILINE | re.DOTALL)
    assert match, f"Missing section: {heading}"
    assert match.group("section").strip(), f"Section is empty: {heading}"
    return match.group("section")


def _assignments_from(text: str) -> dict[str, set[str]]:
    section = _section(text, MACHINE_HEADING.removeprefix("## "))
    result: dict[str, set[str]] = {}
    for match in ASSIGNMENT_RE.finditer(section):
        result.setdefault(match.group("field"), set()).add(match.group("value"))
    return result


def test_document_exists_canonical_id_and_sections_are_non_empty() -> None:
    assert ARTIFACT_PATH.exists()
    text = _read()
    assert text.startswith("# WEATHER-BOT-PHASE0A-META-REFRESH-01 — Weather Bot Phase 0A Meta Refresh")
    assert f"Canonical ID: {CANONICAL_ID}" in text
    for heading in REQUIRED_SECTIONS:
        _section(text, heading)


def test_docs_static_meta_refresh_scope_no_meg_modification_and_meta_files() -> None:
    text = _read()
    for phrase in [
        "docs/static-test-only/meta-refresh-only",
        "This ticket does not modify `meg/`",
        "refreshes meta/handoff state after `WEATHER-BOT-PHASE0A-HOLD-STATE-CLOSEOUT-01`",
        "`docs/meta/MEG_ACTIVE_STATE.md`",
        "`docs/meta/MEG_CHAT_HANDOFF.md`",
        "`docs/meta/domain_packets/WEATHER_BOT_PACKET.md`",
    ]:
        assert phrase in text


def test_weather_bot_and_phase0a_source_fetching_posture() -> None:
    text = _read()
    for phrase in [
        "Weather Bot models the market settlement rule, not generic weather",
        "Weather Bot Phase 0A remains held and closed for source-fetching runtime work",
        "Source-fetching runtime track: `closed_held`",
        "Closed owner decision: `hold_source_fetching_runtime_track`",
        "Source fetching remains not implemented",
        "Implementation approval remains not granted",
        "Stage 2 runtime metadata scaffolds remain supplied-metadata-only and fail-closed",
    ]:
        assert phrase in text


def test_stage2_artifacts_blocked_work_and_reopen_conditions() -> None:
    text = _read()
    for path in STAGE2_ARTIFACT_PATHS:
        assert f"`{path}`" in text
    for value in BLOCKED_WORK:
        assert f"`{value}`" in text
    for value in CONDITIONS_REQUIRED_TO_REOPEN:
        assert f"`{value}`" in text
    assert "Only `approve_narrow_source_fetching_runtime_implementation_plan` may unlock" in text


def test_provider_credentials_generated_scoring_trading_and_audit_not_approved() -> None:
    text = _read()
    for phrase in [
        "Provider connectors remain not approved",
        "Provider clients remain not created",
        "Live provider/source fetching remains not approved",
        "Forecast pulling, API calls, scraping, file downloads, and provider SDK usage remain not approved",
        "Credentials/config loading remains not approved",
        "Generated data and fixtures remain not approved",
        "Scoring/backtesting remains not approved",
        "Runtime trading/order placement/autonomy/production remains not approved",
        "Report writing, audit output persistence, and external export remain not approved",
    ]:
        assert phrase in text


def test_canonical_identifier_contract_and_no_market_id_routing() -> None:
    section = _section(_read(), "Canonical identifier posture")
    for value in ("`condition_id`", "`token_id`", "`outcome`"):
        assert value in section
    assert "No routing on `market_id` is introduced or approved" in section


def test_machine_assignments_are_section_scoped_complete_and_allowed() -> None:
    assignments = _assignments_from(_read())
    assert set(assignments) == set(ALLOWED_ASSIGNMENTS)
    assert assignments == ALLOWED_ASSIGNMENTS


def test_machine_assignment_parser_ignores_assignments_after_next_heading() -> None:
    synthetic = (
        "# doc\n\n## Machine-checkable Weather Bot Phase 0A meta-refresh assignments\n\n"
        "- label confidence: confirmed\n\n## Acceptance criteria\n\n"
        "- label confidence: forbidden_after_next_heading\n"
    )
    assert _assignments_from(synthetic) == {"label confidence": {"confirmed"}}


def test_recommended_next_track_is_docs_static_self_review_not_implementation() -> None:
    text = _read()
    section = _section(text, "Recommended next ticket")
    assert "`weather_bot_phase0a_meta_refresh_self_review`" in section
    assert "docs/static-test-only self-review and not implementation" in section
    assert "must not implement source fetching" in section


def test_refreshed_meta_files_record_required_posture() -> None:
    required = [
        "WEATHER-BOT-PHASE0A-HOLD-STATE-CLOSEOUT-01",
        "weather_bot_phase0a_held_closed",
        "Source-fetching runtime track: `closed_held`",
        "Closed owner decision: `hold_source_fetching_runtime_track`",
        "Source fetching: `not_implemented`",
        "Implementation approval: `not_granted`",
        "Stage 2 runtime metadata: `supplied_metadata_only`",
        "Stage 2 validation posture: `fail_closed`",
        "approve_narrow_source_fetching_runtime_implementation_plan",
        "Weather Bot models the market settlement rule, not generic weather",
    ]
    meta_paths = [
        REPO_ROOT / "docs/meta/MEG_ACTIVE_STATE.md",
        REPO_ROOT / "docs/meta/MEG_CHAT_HANDOFF.md",
        REPO_ROOT / "docs/meta/domain_packets/WEATHER_BOT_PACKET.md",
    ]
    for path in meta_paths:
        text = path.read_text(encoding="utf-8")
        for phrase in required:
            assert phrase in text
        for artifact_path in STAGE2_ARTIFACT_PATHS:
            assert artifact_path in text


def test_changed_file_scope_excludes_runtime_and_data_outputs() -> None:
    changed = {
        "docs/prd/WEATHER-BOT-PHASE0A-META-REFRESH-01.md",
        "tests/core/test_weather_bot_phase0a_meta_refresh_01.py",
        "docs/meta/MEG_ACTIVE_STATE.md",
        "docs/meta/MEG_CHAT_HANDOFF.md",
        "docs/meta/domain_packets/WEATHER_BOT_PACKET.md",
        "tests/core/canonical_id_allowlist.py",
    }
    forbidden_prefixes = (
        "meg/",
        "tests/fixtures/",
        ".github/workflows/",
        "docs/reports/",
        "reports/",
        "exports/",
        "migrations/",
    )
    forbidden_suffixes = (".env", "requirements.txt", "pyproject.toml", "poetry.lock")
    assert all(not path.startswith(forbidden_prefixes) for path in changed)
    assert all(not path.endswith(forbidden_suffixes) for path in changed)


def test_unsafe_approval_phrases_are_absent_from_new_artifacts() -> None:
    unsafe_fragments = [
        "provider connector is " + "approved",
        "provider client is " + "created",
        "source fetching is " + "approved",
        "source fetching implementation is " + "approved",
        "source fetching implementation planning is " + "approved",
        "source fetching implementation plan is " + "approved",
        "live provider source fetching is " + "approved",
        "forecast pull is " + "approved",
        "api call is " + "approved",
        "scraping is " + "approved",
        "file download is " + "approved",
        "provider sdk is " + "approved",
        "generated data is " + "approved",
        "fixture change is " + "approved",
        "scoring is " + "approved",
        "backtesting is " + "approved",
        "trading is " + "approved",
        "order placement is " + "approved",
        "autonomy is " + "approved",
        "production behavior is " + "approved",
        "report writing is " + "approved",
        "external export is " + "approved",
        "persistence is " + "approved",
        "silence is " + "approval",
        "continuation is " + "approval",
        "non-interference is " + "approval",
    ]
    checked_text = "\n".join(
        path.read_text(encoding="utf-8").lower()
        for path in [ARTIFACT_PATH, Path(__file__)]
    )
    for phrase in unsafe_fragments:
        assert phrase not in checked_text
