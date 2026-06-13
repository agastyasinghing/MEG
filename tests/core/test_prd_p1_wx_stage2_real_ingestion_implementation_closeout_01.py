"""Static checks for the offline real-ingestion implementation closeout PRD."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PRD_REL = "docs/prd/PRD-P1-WX-STAGE2-REAL-INGESTION-IMPLEMENTATION-CLOSEOUT-01_OFFLINE_REAL_INGESTION_IMPLEMENTATION_SKELETON_CLOSEOUT.md"
PRD_PATH = REPO_ROOT / PRD_REL
CANONICAL_ID = "PRD-P1-WX-STAGE2-REAL-INGESTION-IMPLEMENTATION-CLOSEOUT-01"
MACHINE_HEADING = "Machine-checkable real ingestion implementation closeout assignments"

REQUIRED_SECTIONS = (
    "Status and scope",
    "Strategic framing",
    "Predecessor chain",
    "Implementation artifact inventory",
    "Offline skeleton summary",
    "Drift-guard hardening summary",
    "Closed-set validation summary",
    "Caller-supplied descriptor boundary",
    "Explicit non-approval boundaries",
    "Provider/API connector boundary",
    "Source-fetching boundary",
    "External API boundary",
    "Credentials/secrets/config boundary",
    "Forecast-pull boundary",
    "Scoring/backtesting boundary",
    "Runtime/trading/autonomy boundary",
    "Fixture/data/generated-artifact boundary",
    "Test coverage summary",
    "Known limitations",
    "Later-ticket handoff",
    MACHINE_HEADING,
    "Acceptance criteria",
)

PREDECESSORS = (
    "PRD-P1-WX-STAGE2-REAL-INGESTION-PLANNING-APPROVAL-01",
    "PRD-P1-WX-STAGE2-REAL-INGESTION-PLAN-01",
    "PRD-P1-WX-STAGE2-REAL-INGESTION-PLAN-CLOSEOUT-01",
    "MEG-OPS-WX-ACTIVE-STATE-07",
    "PRD-P1-WX-STAGE2-REAL-INGESTION-IMPLEMENTATION-APPROVAL-01",
    "PRD-P1-WX-STAGE2-REAL-INGESTION-IMPLEMENTATION-01",
    "PRD-P1-WX-STAGE2-INGESTION-IMPLEMENTATION-CLOSEOUT-01",
)

ARTIFACTS = (
    "meg/weather/stage2/real_ingestion.py",
    "tests/unit/weather/stage2/test_real_ingestion.py",
    "docs/prd/PRD-P1-WX-STAGE2-REAL-INGESTION-IMPLEMENTATION-01_OFFLINE_REAL_INGESTION_IMPLEMENTATION_SKELETON.md",
    "tests/core/test_prd_p1_wx_stage2_real_ingestion_implementation_01.py",
)

ALLOWED_ASSIGNMENTS = {
    "real ingestion implementation closeout stage": {
        "stage_2_offline_real_ingestion_implementation_skeleton_closeout",
    },
    "implementation artifact status": {
        "skeleton_present",
        "unit_tests_present",
        "static_tests_present",
        "prd_present",
    },
    "drift guard status": {
        "expanded_connector_api_source_fetching_scraping_forecast_guards_present",
        "expanded_runtime_polling_streaming_scheduling_job_guards_present",
        "expanded_secrets_config_credentials_guards_present",
        "expanded_scoring_backtesting_paper_simulation_guards_present",
        "expanded_trading_autonomy_production_guards_present",
    },
    "source boundary status": {
        "caller_supplied_descriptors_only",
        "already_reviewed_values_only",
        "offline_static_validation_only",
        "no_runtime_source_acquisition",
    },
    "non approval status": {
        "provider_connectors_not_approved",
        "source_fetching_not_approved",
        "external_api_calls_not_approved",
        "credentials_secrets_config_not_approved",
        "forecast_pulls_not_approved",
        "scoring_backtesting_not_approved",
        "runtime_trading_autonomy_not_approved",
        "production_behavior_not_approved",
    },
    "data posture": {
        "no_fixture_files_modified",
        "no_fixture_files_read_by_runtime",
        "no_historical_label_data_created",
        "no_generated_data_created",
    },
    "later gate posture": {
        "hold_checkpoint",
        "architecture_alignment_planning_before_feature_expansion",
        "provider_connector_requires_later_approval",
        "source_fetching_requires_later_approval",
        "scoring_backtesting_requires_later_approval",
        "runtime_trading_requires_later_approval",
    },
    "evidence status": {
        "source_backed",
        "reviewer_inferred",
        "missing",
        "conflicting",
        "not_applicable",
    },
    "label confidence": {
        "confirmed",
        "unclear",
        "unknown",
    },
}


def _read() -> str:
    return PRD_PATH.read_text(encoding="utf-8")


def _section(text: str, heading: str) -> str:
    marker = "## " + heading
    start = text.index(marker)
    next_start = text.find("\n## ", start + len(marker))
    if next_start == -1:
        return text[start:]
    return text[start:next_start]


def _assignments(text: str) -> dict[str, list[str]]:
    section = _section(text, MACHINE_HEADING)
    parsed: dict[str, list[str]] = {}
    for line in section.splitlines():
        if not line.startswith("- ") or ": " not in line:
            continue
        key, value = line[2:].split(": ", 1)
        parsed.setdefault(key, []).append(value)
    return parsed


def test_closeout_prd_exists_and_contains_canonical_id() -> None:
    assert PRD_PATH.is_file()
    assert CANONICAL_ID in _read()


def test_all_required_sections_appear_in_order() -> None:
    text = _read()
    cursor = -1
    for section in REQUIRED_SECTIONS:
        next_cursor = text.find("## " + section)
        assert next_cursor > cursor, section
        cursor = next_cursor


def test_predecessor_references_and_artifact_inventory_paths_appear() -> None:
    text = _read()
    for required in PREDECESSORS + ARTIFACTS:
        assert required in text


def test_closeout_checkpoint_offline_stdlib_and_descriptor_boundary_are_stated() -> None:
    text = _read()
    required_phrases = (
        "This is a closeout/checkpoint only",
        "The offline real-ingestion implementation skeleton exists.",
        "The skeleton is standard-library only",
        "validating caller-supplied, already-reviewed source descriptor mappings only",
        "PR #228 created the offline real-ingestion implementation skeleton",
        "PR #229 expanded/hardened drift-guard coverage",
        "expanded/hardened drift-guard coverage after PR #228",
    )
    for phrase in required_phrases:
        assert phrase in text


def test_explicit_non_approval_boundaries_are_stated() -> None:
    text = _read()
    required_fragments = (
        "no source fetching",
        "no provider/API connector behavior",
        "no external API calls",
        "no credential/secret/config loading",
        "no forecast pulls",
        "no scraping/polling/streaming/scheduling/jobs behavior",
        "no scoring/backtesting/paper simulation behavior",
        "no runtime market observation",
        "no trading/order placement/autonomy behavior",
        "no production behavior",
        "does not read or write fixture README/JSON files",
        "does not create historical-label data",
        "does not create generated data",
    )
    for fragment in required_fragments:
        assert fragment in text


def test_future_later_approval_and_next_posture_are_stated() -> None:
    text = _read()
    required_phrases = (
        "Future provider connector implementation requires later approval",
        "Future source fetching requires later approval",
        "Future scoring/backtesting requires later approval",
        "Future runtime/trading/autonomy requires later approval",
        "Future production behavior requires later approval",
        "hold/checkpoint or broader architecture-alignment planning before feature expansion",
        "not provider/source/scoring/runtime/trading work by default",
        "MEG-ARCH-ALIGN-01",
    )
    for phrase in required_phrases:
        assert phrase in text


def test_machine_checkable_assignment_section_exists_and_parser_is_section_scoped() -> None:
    text = _read()
    assert "## " + MACHINE_HEADING in text
    assignments = _assignments(text)
    assert set(assignments) == set(ALLOWED_ASSIGNMENTS)
    assert "not_an_assignment" not in assignments


def test_every_allowed_closed_set_value_appears_as_assignment_value() -> None:
    assignments = _assignments(_read())
    for key, allowed_values in ALLOWED_ASSIGNMENTS.items():
        assert set(assignments[key]) == allowed_values


def test_no_unapproved_actual_assignment_values_appear() -> None:
    assignments = _assignments(_read())
    offenders = {
        key: sorted(set(values) - ALLOWED_ASSIGNMENTS.get(key, set()))
        for key, values in assignments.items()
    }
    offenders = {key: values for key, values in offenders.items() if values}
    assert offenders == {}
