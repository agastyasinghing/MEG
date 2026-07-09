"""Static tests for Stage 2 real source-backed fixture implementation."""
from __future__ import annotations

import json
import re
import subprocess
from datetime import date
from pathlib import Path

from meg.weather.stage2.historical_label import (
    historical_label_metadata_from_mapping,
    validate_historical_label_metadata,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
CANONICAL_ID = "PRD-P1-WX-STAGE2-REAL-FIXTURE-IMPLEMENTATION-01"
PRD_PATH = REPO_ROOT / "docs/prd/PRD-P1-WX-STAGE2-REAL-FIXTURE-IMPLEMENTATION-01_REAL_SOURCE_BACKED_FIXTURE_IMPLEMENTATION.md"
FIXTURE_DIR = REPO_ROOT / "tests/fixtures/weather/stage2_real_source_backed_labels"
README_PATH = FIXTURE_DIR / "README.md"
EXPECTED_FIXTURE_NAMES = {
    "polymarket_nyc_may_2026_precipitation_less_than_2_no.json",
    "polymarket_nyc_may_12_2026_temperature_conflict.json",
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
    "source_identity",
    "source_name",
    "source_locator",
    "access_date",
    "venue_rule_reference",
    "resolver_source_identity",
    "reviewer_notes",
    "provenance_notes",
    "no_lookahead_notes",
    "conflicting_source_notes",
    "non_approval_notes",
}
ALLOWED_FIXTURE_KINDS = {
    "real_source_backed_candidate",
    "venue_rule_edge_case",
    "provenance_edge_case",
    "no_lookahead_edge_case",
    "conflicting_source_case",
    "blocked_case",
    "unclear_case",
}
ALLOWED_POSTURES = {"pass", "blocked", "caution"}
ALLOWED_CONFIDENCE_STATUS = {"confirmed", "unclear", "unknown"}
DISALLOWED_CONFIDENCE_STATUS = {
    "confirmed/unclear",
    "confirmed/unknown",
    "unclear/unknown",
    "partial",
    "mixed",
    "likely_confirmed",
    "maybe",
    "supported",
    "approved",
}
NON_REVIEWABLE_SOURCE_PLACEHOLDERS = {
    "tbd",
    "todo",
    "unknown",
    "none",
    "n/a",
    "placeholder",
    "example.com",
}
SECRET_FRAGMENTS = (
    "api_" + "key",
    "secret_" + "key",
    "weather_" + "api_" + "key",
    "bearer token",
    "password=",
)
FORBIDDEN_TEST_FRAGMENTS = (
    "os." + "environ",
    "load_" + "dot" + "env",
    "dot" + "env",
    "requests" + ".",
    "http" + "x.",
    "aio" + "http",
    "urllib." + "request",
)
ALLOWED_CHANGED_PATHS = {
    "docs/prd/PRD-P1-WX-STAGE2-REAL-FIXTURE-IMPLEMENTATION-01_REAL_SOURCE_BACKED_FIXTURE_IMPLEMENTATION.md",
    # Later docs/meta approval-decision repairs may intentionally touch the
    # Weather Bot packet plus their focused static test while preserving the
    # no-runtime/source/provider/trading scope enforced below.
    "docs/meta/domain_packets/WEATHER_BOT_PACKET.md",
    "tests/core/test_prd_p1_wx_stage2_real_fixture_implementation_01.py",
    "tests/core/test_weather_stage2_source_provider_runtime_approval_decision.py",
    "tests/core/test_weather_stage2_source_provider_runtime_hold_closeout.py",
    "tests/core/canonical_id_allowlist.py",
    "tests/fixtures/weather/stage2_real_source_backed_labels/README.md",
    "tests/fixtures/weather/stage2_real_source_backed_labels/polymarket_nyc_may_2026_precipitation_less_than_2_no.json",
    "tests/fixtures/weather/stage2_real_source_backed_labels/polymarket_nyc_may_12_2026_temperature_conflict.json",
}


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _fixture_paths() -> list[Path]:
    if not FIXTURE_DIR.exists():
        return []
    return sorted(FIXTURE_DIR.glob("*.json"))


def _fixtures() -> list[dict[str, object]]:
    return [json.loads(_read_text(path)) for path in _fixture_paths()]


def _is_nonempty_string(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _assert_no_nested_key(value: object, forbidden_key: str) -> None:
    if isinstance(value, dict):
        assert forbidden_key not in value
        for nested_value in value.values():
            _assert_no_nested_key(nested_value, forbidden_key)
    elif isinstance(value, list):
        for nested_value in value:
            _assert_no_nested_key(nested_value, forbidden_key)


def _adapt_for_skeleton(fixture: dict[str, object]) -> dict[str, object]:
    return {
        "condition_id": fixture["condition_id"],
        "token_id": fixture["token_id"],
        "outcome": fixture["outcome"],
        "venue_rule_summary": fixture["venue_rule_summary"],
        "source_resolution": fixture["source_resolution"],
        "point_in_time_provenance": fixture["point_in_time_provenance"],
        "label_usability": fixture["label_usability"],
    }


def _posture_from_validation(fixture: dict[str, object]) -> str:
    metadata = historical_label_metadata_from_mapping(_adapt_for_skeleton(fixture))
    result = validate_historical_label_metadata(metadata)
    if result.passed:
        return "pass"
    if result.severity.value == "blocked":
        return "blocked"
    return "caution"


def test_prd_and_readme_exist_with_required_static_scope() -> None:
    assert PRD_PATH.is_file()
    assert README_PATH.is_file()
    prd_text = _read_text(PRD_PATH)
    readme_text = _read_text(README_PATH)
    assert CANONICAL_ID in prd_text
    for required in (
        "real source-backed fixture implementation only",
        "at most 3 real source-backed fixture JSON files",
        "no generated data was created",
        "future historical-label loading requires separate explicit approval",
        "future ingestion requires separate explicit approval",
        "future scoring/backtesting requires separate explicit approval",
        "future runtime/trading requires separate explicit approval",
    ):
        assert required in prd_text
    for required in (
        "purpose",
        "directory allowlist",
        "fixture count cap",
        "static-test-only rule",
        "These fixtures do not approve historical-label loading.",
    ):
        assert required.lower() in readme_text.lower()


def test_fixture_directory_inventory_is_capped_and_exact() -> None:
    prd_text = _read_text(PRD_PATH)
    if "BLOCKED:" in prd_text:
        assert not FIXTURE_DIR.exists() or not _fixture_paths()
        assert "real source-backed fixture implementation requires source-backed fixture evidence" in prd_text
        return

    assert FIXTURE_DIR.is_dir()
    fixture_paths = _fixture_paths()
    assert 1 <= len(fixture_paths) <= 3
    assert {path.name for path in fixture_paths} == EXPECTED_FIXTURE_NAMES
    for path in fixture_paths:
        assert path.name in _read_text(README_PATH)
        assert path.as_posix().replace(str(REPO_ROOT) + "/", "") in prd_text


def test_all_fixture_files_parse_and_include_required_keys() -> None:
    for fixture in _fixtures():
        assert REQUIRED_TOP_LEVEL_KEYS <= set(fixture)
        assert fixture["synthetic_or_real"] == "real_source_backed"
        assert fixture["fixture_kind"] in ALLOWED_FIXTURE_KINDS
        assert fixture["expected_validation_posture"] in ALLOWED_POSTURES


def test_fixture_identifiers_are_unique_prefixed_and_do_not_use_legacy_identifier() -> None:
    fixture_ids: set[str] = set()
    condition_ids: set[str] = set()
    token_ids: set[str] = set()
    for fixture in _fixtures():
        _assert_no_nested_key(fixture, "market_id")
        fixture_id = fixture["fixture_id"]
        condition_id = fixture["condition_id"]
        token_id = fixture["token_id"]
        assert isinstance(fixture_id, str) and fixture_id.startswith("real_fixture_stage2_")
        assert isinstance(condition_id, str) and condition_id.startswith("real_fixture_condition_stage2_")
        assert isinstance(token_id, str) and token_id.startswith("real_fixture_token_stage2_")
        fixture_ids.add(fixture_id)
        condition_ids.add(condition_id)
        token_ids.add(token_id)
    assert len(fixture_ids) == len(_fixtures())
    assert len(condition_ids) == len(_fixtures())
    assert len(token_ids) == len(_fixtures())


def test_fixture_source_evidence_is_reviewable_and_not_placeholder() -> None:
    for fixture in _fixtures():
        for key in (
            "source_identity",
            "source_name",
            "source_locator",
            "access_date",
            "venue_rule_reference",
            "resolver_source_identity",
            "reviewer_notes",
            "provenance_notes",
            "no_lookahead_notes",
            "non_approval_notes",
        ):
            assert _is_nonempty_string(fixture[key]), key
        date.fromisoformat(str(fixture["access_date"]))
        searchable_values = "\n".join(
            str(fixture[key]).lower()
            for key in (
                "source_identity",
                "source_name",
                "source_locator",
                "venue_rule_reference",
                "resolver_source_identity",
            )
        )
        assert not any(fragment in searchable_values for fragment in NON_REVIEWABLE_SOURCE_PLACEHOLDERS)
        assert str(fixture["source_locator"]).startswith(("https://", "http://"))


def test_fixtures_do_not_contain_secret_material_or_keys() -> None:
    for path in _fixture_paths():
        text = _read_text(path).lower()
        assert not any(fragment in text for fragment in SECRET_FRAGMENTS)


def test_fixtures_adapt_to_stage2_skeleton_and_match_expected_posture() -> None:
    observed_postures = set()
    for fixture in _fixtures():
        expected = fixture["expected_validation_posture"]
        observed = _posture_from_validation(fixture)
        assert observed == expected
        observed_postures.add(observed)
    assert "pass" in observed_postures
    assert "blocked" in observed_postures or "caution" in observed_postures


def test_prd_fixture_summary_confidence_status_uses_closed_values() -> None:
    prd_text = _read_text(PRD_PATH)
    rows = [line for line in prd_text.splitlines() if line.startswith("| `tests/fixtures/weather/stage2_real_source_backed_labels/")]
    assert rows
    for row in rows:
        cells = [cell.strip() for cell in row.strip().strip("|").split("|")]
        confidence_status = cells[-1]
        assert confidence_status in ALLOWED_CONFIDENCE_STATUS
        assert confidence_status not in DISALLOWED_CONFIDENCE_STATUS
    for disallowed in DISALLOWED_CONFIDENCE_STATUS:
        assert not re.search(rf"\|\s*{re.escape(disallowed)}\s*\|", prd_text)


def test_new_test_file_does_not_call_network_or_read_process_environment() -> None:
    text = _read_text(Path(__file__))
    assert not any(fragment in text for fragment in FORBIDDEN_TEST_FRAGMENTS)
    assert ("so" + "cket") not in text


def test_no_source_or_runtime_modules_modified_by_this_ticket() -> None:
    result = subprocess.run(
        ["git", "diff", "--name-only", "HEAD"],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    changed_paths = {line.strip() for line in result.stdout.splitlines() if line.strip()}
    assert changed_paths <= ALLOWED_CHANGED_PATHS
    assert not any(path.startswith("meg/") for path in changed_paths)
    assert not any(path.startswith(("connectors/", "ingestion/", "runtime/", "trading/")) for path in changed_paths)
