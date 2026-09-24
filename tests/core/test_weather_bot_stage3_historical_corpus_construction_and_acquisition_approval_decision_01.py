"""Static oracle for the Stage 3 historical-corpus approval decision."""

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DOC_PATH = ROOT / "docs/prd/WEATHER-BOT-STAGE3-HISTORICAL-CORPUS-CONSTRUCTION-AND-ACQUISITION-APPROVAL-DECISION-01.md"
TEXT = DOC_PATH.read_text(encoding="utf-8")

HEADINGS = [
    "Status and scope", "Immediate predecessor and merge verification", "Decision basis",
    "Selected decision", "Decision effect", "Approved future path",
    "Historical/offline acquisition boundary", "Access-method posture",
    "Point-in-time/no-lookahead requirements", "Storage/artifact posture",
    "Current corpus/evidence posture", "Explicit non-approvals",
    "Stage 3 / Stage 4 separation", "Canonical routing posture",
    "Recommended next ticket", "Machine-checkable assignments", "Acceptance criteria",
]

DECISION_OPTIONS = [
    "approve_narrow_historical_corpus_construction_and_acquisition",
    "request_approval_request_revision",
    "hold",
    "block",
]

ACCESS_METHODS = [
    "manual_source_review",
    "static_public_reference",
    "offline_public_file_acquisition",
    "offline_public_api_acquisition",
    "source_specific_credentials_required",
    "scraping_requires_separate_approval",
    "live_runtime_provider_requires_separate_approval",
]


def assignments(key: str) -> list[str]:
    return re.findall(rf"^{re.escape(key)}: (\S+)$", TEXT, re.MULTILINE)


def section(heading: str, next_heading: str) -> str:
    return TEXT.split(f"## {heading}\n", 1)[1].split(f"## {next_heading}\n", 1)[0]


def backtick_bullets(body: str) -> list[str]:
    return re.findall(r"^- `([^`]+)`$", body, re.MULTILINE)


def test_exact_path_predecessor_and_heading_order() -> None:
    assert DOC_PATH.is_file()
    assert "PR #387" in TEXT
    assert assignments("actual_merge_sha") == ["6901845cfea86670b1b7fed82fa2db976fbfa627"]
    assert re.findall(r"^## (.+)$", TEXT, re.MULTILINE) == HEADINGS


def test_closed_decision_set_and_exact_selection() -> None:
    assert backtick_bullets(section("Selected decision", "Decision effect")) == DECISION_OPTIONS
    assert assignments("decision_option") == DECISION_OPTIONS
    assert assignments("selected_decision") == [
        "approve_narrow_historical_corpus_construction_and_acquisition"
    ]
    assert assignments("decision_status") == ["decision_recorded"]


def test_only_planning_paths_open_and_no_execution_authority() -> None:
    assert assignments("historical_corpus_path") == ["approved_for_narrow_implementation_planning"]
    assert assignments("historical_acquisition_path") == ["approved_for_narrow_implementation_planning"]
    assert assignments("execution_authority") == ["not_granted_by_decision_artifact"]
    assert assignments("access_method_authority") == ["none_individually_approved"]
    assert assignments("live_provider_runtime_authority") == ["not_approved"]
    access_section = section("Access-method posture", "Point-in-time/no-lookahead requirements")
    assert backtick_bullets(access_section) == ACCESS_METHODS
    assert "No access method in this set is individually authorized" in access_section
    acquisition_section = section("Historical/offline acquisition boundary", "Access-method posture")
    for deferred_boundary in (
        "providers", "source families", "endpoints", "access methods", "credentials", "storage"
    ):
        assert deferred_boundary in acquisition_section


def test_evidence_and_storage_posture_remain_unresolved() -> None:
    expected = {
        "current_corpus": "five_static_stage2_examples_only", "synthetic_example_count": "3",
        "real_source_backed_example_count": "2", "corpus_coverage": "not_established",
        "sample_sufficiency": "not_established", "strict_oos_feasibility": "not_demonstrated",
        "stage3_scoring_readiness": "not_ready", "storage_path": "not_selected",
        "file_format": "not_selected", "database": "not_selected", "dataset_size": "not_selected",
    }
    assert all(assignments(key) == [value] for key, value in expected.items())
    evidence_section = section("Current corpus/evidence posture", "Explicit non-approvals")
    assert "exactly 3 synthetic examples and 2 real source-backed examples" in evidence_section
    assert "not promoted into a historical corpus" in evidence_section


def test_no_lookahead_and_non_approval_boundaries_are_explicit() -> None:
    required = [
        "substitute final archives into earlier as-of views", "future revisions before availability",
        "labels before legitimate resolution availability", "future forecasts",
        "with hindsight", "test outcomes", "modern values", "silently mix archive/finality layers",
        "Observation/event time and publication/availability time must remain distinct",
        "Stage 4 remains separate and not approved", "trading", "production runtime", "autonomy",
    ]
    assert all(value in TEXT for value in required)
    assert "arbitrary scraping or API access" in section(
        "Explicit non-approvals", "Stage 3 / Stage 4 separation"
    )
    assert "Large datasets are not authorized for Git by default" in section(
        "Storage/artifact posture", "Current corpus/evidence posture"
    )


def test_canonical_routing_and_single_successor() -> None:
    assert assignments("canonical_routing_field") == ["condition_id", "token_id", "outcome"]
    assert assignments("non_routing_legacy_identifier") == ["market_id"]
    assert assignments("derived_identifier") == ["token_outcome_pair"]
    assert assignments("recommended_next_ticket") == [
        "WEATHER-BOT-STAGE3-HISTORICAL-CORPUS-CONSTRUCTION-AND-ACQUISITION-IMPLEMENTATION-PLAN-01"
    ]
