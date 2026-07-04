from __future__ import annotations

import ast
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CANONICAL_ID = "WEATHER-BOT-PHASE0A-NON-OWNER-RUNTIME-GATE-HOLD-REFRESH-PLANNING-01"
PRD = ROOT / f"docs/prd/{CANONICAL_ID}.md"
TEST = ROOT / "tests/core/test_weather_bot_phase0a_non_owner_runtime_gate_hold_refresh_planning_01.py"
MACHINE_HEADING = "Machine-checkable Weather Bot Phase 0A non-owner runtime gate hold assignments"
REQUIRED_TITLE = f"# {CANONICAL_ID} — Weather Bot Phase 0A Non-Owner Runtime Gate Hold Refresh Planning"
REQUIRED_CANONICAL = f"Canonical ID: {CANONICAL_ID}"
REQUIRED_SECTIONS = (
    "Status and scope",
    "Predecessor and stop condition",
    "Purpose",
    "Non-owner runtime gate hold posture",
    "Non-goals and non-approval boundaries",
    "Source-of-truth relationship",
    "Canonical identifier posture",
    "Runtime hold summary",
    "Source-fetching and provider hold summary",
    "Paper-trade evaluation and trading hold summary",
    "Manual-review and operator runtime hold summary",
    "Gate blocker inventory",
    "Future lane boundaries",
    "Static-test expectations",
    MACHINE_HEADING,
    "Embedded self-review requirement",
    "Acceptance criteria",
    "Recommended next ticket",
)
ASSIGNMENT_RE = re.compile(r"^- (?P<category>[^:]+): (?P<value>\S+)\s*$", re.MULTILINE)
CLOSED_SETS = {
    "weather bot planning stage": ["weather_bot_phase0a_non_owner_runtime_gate_hold_refresh_planning"],
    "predecessor pr": ["pr_306"],
    "predecessor artifact": ["runtime_approval_request_packet_planning"],
    "excluded predecessor pr": ["pr_283_unmerged"],
    "gate posture": ["non_owner_runtime_gate_hold_refresh_only", "no_owner_decision_capture", "no_owner_capture_next_track", "runtime_gate_not_revised", "runtime_gate_required_before_runtime_use", "runtime_approval_not_granted"],
    "source fetching track posture": ["closed_held", "source_fetching_not_implemented", "implementation_approval_not_granted", "hold_source_fetching_runtime_track"],
    "canonical routing field": ["condition_id", "token_id", "outcome"],
    "derived identifier field": ["token_outcome_pair"],
    "non routing field": ["market_id"],
    "runtime hold status": ["not_runtime_ready", "runtime_approval_not_granted", "settlement_rule_interpreter_runtime_not_implemented", "no_lookahead_validation_runtime_not_implemented", "fail_closed_validation_runtime_not_implemented", "runtime_ingestion_not_implemented", "runtime_loading_not_implemented", "runtime_validation_not_implemented", "runtime_parser_interpreter_not_implemented"],
    "source provider hold status": ["source_fetching_not_approved", "provider_implementation_not_approved", "provider_connector_not_implemented", "provider_client_not_implemented", "api_calls_not_implemented", "forecast_pulls_not_implemented", "credentials_config_loading_not_implemented"],
    "evaluation trading hold status": ["not_evaluation_ready", "not_paper_trade_ready", "scoring_evaluation_execution_not_implemented", "metric_persistence_not_implemented", "backtesting_not_implemented", "paper_trading_not_implemented", "order_simulation_not_implemented", "trading_autonomy_production_not_implemented"],
    "manual operator hold status": ["manual_review_runtime_not_implemented", "manual_review_ui_not_implemented", "operator_workflow_runtime_not_implemented", "operator_decision_execution_not_implemented", "operator_decision_persistence_not_implemented"],
    "implementation posture": ["no_runtime_code_change", "no_meg_modification", "no_source_fetching", "no_provider_connector", "no_provider_client", "no_api_call", "no_scraping", "no_file_download", "no_forecast_pull", "no_sdk_usage", "no_credentials_config_loading", "no_generated_data", "no_fixture_change", "no_schema_change", "no_db_migration", "no_runtime_ingestion", "no_runtime_loading", "no_runtime_validation", "no_runtime_parser_interpreter", "no_manual_review_runtime_workflow", "no_manual_review_ui", "no_operator_decision_execution", "no_operator_decision_persistence", "no_scoring_evaluation_execution", "no_metric_persistence", "no_backtesting", "no_paper_trading", "no_order_simulation", "no_trading_autonomy_production", "no_reports", "no_persistence", "no_audit_output", "no_export", "no_runtime_gate_revision", "no_runtime_approval_granted", "no_source_fetching_approval_granted", "no_provider_source_approval_granted", "no_paper_trade_approval_granted"],
    "recommended next track": ["weather_bot_phase0a_static_planning_lane_closeout_refresh"],
    "conditional next track": ["weather_bot_phase0a_non_owner_runtime_gate_hold_refresh_revision_if_scope_too_broad"],
    "weather bot scope": ["market_settlement_rule_not_generic_weather"],
    "label confidence": ["confirmed"],
}
REQUIRED_ASSIGNMENTS = {(category, value) for category, values in CLOSED_SETS.items() for value in values}
SELF_REVIEW_FRAGMENTS = ("self_review", "self-review", "standalone_self_review", "standalone-self-review")
OWNER_CAPTURE_NEXT_TRACK_FRAGMENTS = (
    "owner_decision_capture",
    "owner_capture",
    "weather_bot_phase0a_owner_decision_capture_planning",
)


def _read(path: Path = PRD) -> str:
    return path.read_text(encoding="utf-8")


def _section(text: str, heading: str) -> str:
    match = re.search(rf"^## {re.escape(heading)}\n(?P<body>.*?)(?:\n## |\Z)", text, re.S | re.M)
    assert match, heading
    assert match.group("body").strip(), heading
    return match.group("body")


def _pairs_from_section(section: str) -> list[tuple[str, str]]:
    pairs = []
    for line in section.splitlines():
        if line.startswith("- "):
            match = ASSIGNMENT_RE.match(line)
            assert match, line
            pairs.append((match.group("category"), match.group("value")))
    return pairs


def _pairs(text: str) -> list[tuple[str, str]]:
    return _pairs_from_section(_section(text, MACHINE_HEADING))


def _assert_closed_sets(pairs: list[tuple[str, str]]) -> None:
    for category, allowed in CLOSED_SETS.items():
        actual = {value for field, value in pairs if field == category}
        assert actual == set(allowed), category
    assert set(pairs) == REQUIRED_ASSIGNMENTS


def test_prd_exists_title_canonical_id_and_required_sections() -> None:
    text = _read()
    assert text.startswith(REQUIRED_TITLE)
    assert REQUIRED_CANONICAL in text
    assert text.count(f"## {MACHINE_HEADING}") == 1
    for heading in REQUIRED_SECTIONS:
        _section(text, heading)


def test_test_file_uses_only_standard_library_imports() -> None:
    tree = ast.parse(TEST.read_text(encoding="utf-8"))
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.append(node.module)
    assert set(imports) <= {"__future__", "ast", "re", "pathlib"}


def test_machine_checkable_assignments_are_complete_and_closed_set_exact() -> None:
    pairs = _pairs(_read())
    _assert_closed_sets(pairs)


def test_predecessor_pr306_and_pr283_exclusion_are_recorded() -> None:
    pairs = _pairs(_read())
    assert ("predecessor pr", "pr_306") in pairs
    assert ("predecessor artifact", "runtime_approval_request_packet_planning") in pairs
    assert ("excluded predecessor pr", "pr_283_unmerged") in pairs


def test_canonical_market_and_token_outcome_assignments_are_scoped_correctly() -> None:
    pairs = _pairs(_read())
    assert {value for field, value in pairs if field == "canonical routing field"} == {"condition_id", "token_id", "outcome"}
    assert ("derived identifier field", "token_outcome_pair") in pairs
    assert ("canonical routing field", "token_outcome_pair") not in pairs
    assert ("non routing field", "market_id") in pairs
    assert ("canonical routing field", "market_id") not in pairs


def test_hold_statuses_are_present_for_all_blocked_lanes() -> None:
    pairs = _pairs(_read())
    for category in (
        "runtime hold status",
        "source provider hold status",
        "evaluation trading hold status",
        "manual operator hold status",
    ):
        for value in CLOSED_SETS[category]:
            assert (category, value) in pairs
    assert ("source fetching track posture", "hold_source_fetching_runtime_track") in pairs
    assert ("source fetching track posture", "closed_held") in pairs


def test_no_owner_capture_or_self_review_next_track_is_recommended() -> None:
    pairs = _pairs(_read())
    next_tracks = [value for field, value in pairs if field in {"recommended next track", "conditional next track"}]
    assert next_tracks == [
        "weather_bot_phase0a_static_planning_lane_closeout_refresh",
        "weather_bot_phase0a_non_owner_runtime_gate_hold_refresh_revision_if_scope_too_broad",
    ]
    for track in next_tracks:
        assert not any(fragment in track for fragment in OWNER_CAPTURE_NEXT_TRACK_FRAGMENTS)
        assert not any(fragment in track for fragment in SELF_REVIEW_FRAGMENTS)


def test_machine_section_has_required_non_owner_gate_hold_values() -> None:
    pairs = _pairs(_read())
    assert ("gate posture", "no_owner_decision_capture") in pairs
    assert ("gate posture", "no_owner_capture_next_track") in pairs
    assert ("gate posture", "runtime_gate_not_revised") in pairs
    assert ("gate posture", "runtime_gate_required_before_runtime_use") in pairs
    assert ("gate posture", "runtime_approval_not_granted") in pairs


def test_parser_rejects_artificial_hybrid_custom_assignment_values() -> None:
    sample = "- canonical routing field: condition_id_market_id_hybrid\n"
    sample_pairs = _pairs_from_section(sample)
    try:
        _assert_closed_sets(sample_pairs)
    except AssertionError:
        return
    raise AssertionError("hybrid/custom assignment value was accepted")
