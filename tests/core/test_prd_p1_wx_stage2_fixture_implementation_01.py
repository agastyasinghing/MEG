from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from meg.weather.stage2 import historical_label as hl


PRD_PATH = Path(
    "docs/prd/PRD-P1-WX-STAGE2-FIXTURE-IMPLEMENTATION-01_STATIC_HISTORICAL_LABEL_FIXTURE_IMPLEMENTATION.md"
)
CANONICAL_ID = "PRD-P1-WX-STAGE2-FIXTURE-IMPLEMENTATION-01"
FIXTURE_DIR = Path("tests/fixtures/weather/stage2_historical_labels")
README_PATH = FIXTURE_DIR / "README.md"
THIS_TEST_PATH = Path("tests/core/test_prd_p1_wx_stage2_fixture_implementation_01.py")
SOURCE_PATH = Path("meg/weather/stage2/historical_label.py")
LEGACY_ID_FIELD = "market" + "_id"

ALLOWED_FIXTURE_FILES = {
    "synthetic_valid_source_backed_confirmed.json",
    "synthetic_blocked_missing_provenance.json",
    "synthetic_unclear_requires_adjudication.json",
}
REQUIRED_TOP_LEVEL_KEYS = {
    "fixture_id",
    "fixture_kind",
    "synthetic_or_real",
    "canonical_event_summary",
    "venue_rule_summary",
    "condition_id",
    "token_id",
    "outcome",
    "source_resolution",
    "point_in_time_provenance",
    "label_usability",
    "expected_validation_posture",
    "reviewer_notes",
    "provenance_notes",
    "no_lookahead_notes",
    "non_approval_notes",
}


def _fixture_paths() -> list[Path]:
    return sorted(FIXTURE_DIR.glob("*.json"))


def _read_fixture(path: Path) -> dict[str, Any]:
    parsed = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(parsed, dict)
    return parsed


def _fixtures() -> dict[str, dict[str, Any]]:
    return {path.name: _read_fixture(path) for path in _fixture_paths()}


def _validation_posture(fixture: dict[str, Any]) -> str:
    metadata = hl.historical_label_metadata_from_mapping(
        {
            "condition_id": fixture["condition_id"],
            "token_id": fixture["token_id"],
            "outcome": fixture["outcome"],
            "source_resolution": fixture["source_resolution"],
            "point_in_time_provenance": fixture["point_in_time_provenance"],
            "label_usability": fixture["label_usability"],
            "venue_rule_summary": fixture["venue_rule_summary"],
        }
    )
    result = hl.validate_historical_label_metadata(metadata)
    if result.passed:
        return "pass"
    return result.severity.value


def _walk_strings(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        strings: list[str] = []
        for key, nested in value.items():
            strings.extend(_walk_strings(key))
            strings.extend(_walk_strings(nested))
        return strings
    if isinstance(value, list):
        strings = []
        for nested in value:
            strings.extend(_walk_strings(nested))
        return strings
    return []


def test_implementation_prd_exists_with_canonical_id() -> None:
    assert PRD_PATH.is_file()
    assert CANONICAL_ID in PRD_PATH.read_text(encoding="utf-8")


def test_fixture_directory_readme_and_exact_json_inventory_exist() -> None:
    assert FIXTURE_DIR.is_dir()
    assert README_PATH.is_file()
    assert {path.name for path in _fixture_paths()} == ALLOWED_FIXTURE_FILES


def test_all_fixtures_parse_and_include_required_top_level_keys() -> None:
    for fixture in _fixtures().values():
        assert REQUIRED_TOP_LEVEL_KEYS <= set(fixture)


def test_fixtures_are_synthetic_unique_and_use_synthetic_canonical_ids() -> None:
    fixtures = _fixtures().values()
    fixture_ids = [fixture["fixture_id"] for fixture in fixtures]

    assert len(fixture_ids) == len(set(fixture_ids))
    for fixture in _fixtures().values():
        assert fixture["synthetic_or_real"] == "synthetic"
        assert fixture["condition_id"].startswith("synthetic_condition_stage2_")
        assert fixture["token_id"].startswith("synthetic_token_stage2_")


def test_fixture_payloads_avoid_legacy_identifier_fields_and_provider_urls() -> None:
    for fixture in _fixtures().values():
        assert LEGACY_ID_FIELD not in fixture
        for text in _walk_strings(fixture):
            assert LEGACY_ID_FIELD not in text
            assert "http://" not in text
            assert "https://" not in text


def test_fixture_review_provenance_no_lookahead_and_non_approval_notes_are_nonempty() -> None:
    required_note_fields = (
        "reviewer_notes",
        "provenance_notes",
        "no_lookahead_notes",
        "non_approval_notes",
    )
    for fixture in _fixtures().values():
        for field in required_note_fields:
            assert isinstance(fixture[field], str)
            assert fixture[field].strip()


def test_fixture_validation_postures_match_stage_2_skeleton_results() -> None:
    fixtures = _fixtures()

    assert _validation_posture(fixtures["synthetic_valid_source_backed_confirmed.json"]) == "pass"
    assert _validation_posture(fixtures["synthetic_blocked_missing_provenance.json"]) != "pass"
    assert _validation_posture(fixtures["synthetic_unclear_requires_adjudication.json"]) != "pass"

    for fixture in fixtures.values():
        expected = fixture["expected_validation_posture"]
        observed = _validation_posture(fixture)
        assert expected in {"pass", "blocked", "caution"}
        assert observed == expected


def test_valid_fixture_supplies_strict_confirmed_source_backed_metadata() -> None:
    fixture = _fixtures()["synthetic_valid_source_backed_confirmed.json"]

    assert fixture["source_resolution"]["status"] == "source_resolved"
    assert fixture["source_resolution"]["evidence_status"] == "source_backed"
    assert fixture["source_resolution"]["resolver_source_identity"].strip()
    assert fixture["point_in_time_provenance"]["availability_status"] == "available_as_of"
    assert fixture["point_in_time_provenance"]["evidence_status"] == "source_backed"
    assert fixture["label_usability"]["evidence_status"] == "source_backed"
    assert fixture["label_usability"]["label_confidence"] == "confirmed"
    assert fixture["label_usability"]["posture"] == "usable_after_stage_2_approval"
    assert fixture["venue_rule_summary"].strip()


def test_blocked_and_unclear_fixtures_fail_closed_for_expected_reasons() -> None:
    blocked = _fixtures()["synthetic_blocked_missing_provenance.json"]
    unclear = _fixtures()["synthetic_unclear_requires_adjudication.json"]

    assert blocked["source_resolution"]["evidence_status"] == "missing"
    assert blocked["point_in_time_provenance"]["availability_status"] == "unavailable_as_of"
    assert blocked["label_usability"]["posture"] == "blocked_pending_provenance"
    assert blocked["label_usability"]["label_confidence"] == "unknown"

    assert unclear["source_resolution"]["status"] == "requires_adjudication"
    assert unclear["label_usability"]["label_confidence"] == "unclear"
    assert unclear["label_usability"]["posture"] == "blocked_pending_adjudication"


def test_test_file_uses_static_reads_only_and_avoids_runtime_behaviors() -> None:
    text = THIS_TEST_PATH.read_text(encoding="utf-8")
    forbidden_fragments = (
        "os." + "environ",
        "load_" + "dot" + "env",
        "dot" + "env",
        "requests" + ".",
        "http" + "x.",
        "aio" + "http",
        "urllib." + "request",
        "api_" + "key",
        "secret_" + "key",
        "weather_" + "api_" + "key",
        "fast" + "api",
        "fl" + "ask",
        "sql" + "alchemy",
        "pan" + "das",
        "pol" + "ars",
        "duck" + "db",
        "read_" + "csv",
        "to_" + "csv",
        "json" + "lines",
        "par" + "quet",
        "pre" + "dict",
        "back" + "test",
        "paper " + "simulation",
        "order " + "placement",
        "trade" + "_ready",
        "auto_" + "execute",
        "aut" + "onomous",
        "so" + "cket.",
        "sub" + "process.",
        "url" + "open",
        ".write_" + "text",
        ".write_" + "bytes",
        ".to" + "uch(",
    )

    assert all(fragment not in text for fragment in forbidden_fragments)
    assert "Path" in text


def test_source_runtime_module_is_not_a_fixture_loader() -> None:
    source_text = SOURCE_PATH.read_text(encoding="utf-8")

    assert "stage2_historical_labels" not in source_text
    assert "synthetic_valid_source_backed_confirmed" not in source_text
