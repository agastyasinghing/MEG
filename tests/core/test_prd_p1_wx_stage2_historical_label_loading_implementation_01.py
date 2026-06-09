"""Static tests for the Stage 2 historical-label fixture loader ticket."""
from __future__ import annotations

import ast
import hashlib
import json
import py_compile
from pathlib import Path
from typing import Any

import pytest

from meg.weather.stage2.historical_label import HistoricalLabelMetadata, ValidationResult
from meg.weather.stage2.historical_label_loader import (
    FixtureLoadError,
    LoadedHistoricalLabelFixture,
    load_historical_label_fixture,
    load_historical_label_fixture_directory,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
CANONICAL_ID = "PRD-P1-WX-STAGE2-HISTORICAL-LABEL-LOADING-IMPLEMENTATION-01"
PRD_PATH = REPO_ROOT / "docs/prd/PRD-P1-WX-STAGE2-HISTORICAL-LABEL-LOADING-IMPLEMENTATION-01_STATIC_HISTORICAL_LABEL_LOADING_VALIDATION_IMPLEMENTATION.md"
SOURCE_PATH = REPO_ROOT / "meg/weather/stage2/historical_label_loader.py"
THIS_TEST_PATH = REPO_ROOT / "tests/core/test_prd_p1_wx_stage2_historical_label_loading_implementation_01.py"
SYNTHETIC_DIR = REPO_ROOT / "tests/fixtures/weather/stage2_historical_labels"
REAL_DIR = REPO_ROOT / "tests/fixtures/weather/stage2_real_source_backed_labels"
SYNTHETIC_FIXTURE_FILES = {
    "synthetic_blocked_missing_provenance.json",
    "synthetic_unclear_requires_adjudication.json",
    "synthetic_valid_source_backed_confirmed.json",
}
REAL_FIXTURE_FILES = {
    "polymarket_nyc_may_12_2026_temperature_conflict.json",
    "polymarket_nyc_may_2026_precipitation_less_than_2_no.json",
}
EXPECTED_FIXTURE_HASHES = {
    "tests/fixtures/weather/stage2_historical_labels/README.md": "0d04e9e3928e07d90f660c6b258d11920e8ad75d6c580d4a83b41e0dd66dac72",
    "tests/fixtures/weather/stage2_historical_labels/synthetic_blocked_missing_provenance.json": "df9c2b9f10cb267c75aa803d943224349c19d30a10ae3ca0ec84131a4ede2bb7",
    "tests/fixtures/weather/stage2_historical_labels/synthetic_unclear_requires_adjudication.json": "78afe3a038fbc15aeda6a5e508ddf3f741a6786ded9cba25be39843df698d0ec",
    "tests/fixtures/weather/stage2_historical_labels/synthetic_valid_source_backed_confirmed.json": "507e498bfbc45be2dd165a237c63ca7b490ad5f6af2325f4049a0ab16aee6ef8",
    "tests/fixtures/weather/stage2_real_source_backed_labels/README.md": "cf79ba2926b75228fd44b1998a1d491f40a3dec93de28cc468734310c95e85c9",
    "tests/fixtures/weather/stage2_real_source_backed_labels/polymarket_nyc_may_12_2026_temperature_conflict.json": "a920fa12697094465c980141f040b313e1e72267af9bca17372219eb5ede0046",
    "tests/fixtures/weather/stage2_real_source_backed_labels/polymarket_nyc_may_2026_precipitation_less_than_2_no.json": "462554c95055bde501779244e5db87c916fed7777bd7f353b7befb462ebeaacb",
}


def _forbidden_fragments() -> tuple[str, ...]:
    return (
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
        "json." + "load",
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
        "write_" + "text",
        "write_" + "bytes",
        "to" + "uch(",
    )


def _observed_posture(loaded: LoadedHistoricalLabelFixture) -> str:
    if loaded.validation_result.passed:
        return "pass"
    return loaded.validation_result.severity.value


def _read_json(path: Path) -> dict[str, Any]:
    parsed = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(parsed, dict)
    return parsed


def _make_fixture_file(path: Path, payload: Any) -> None:
    with path.open("w", encoding="utf-8") as handle:
        handle.write(json.dumps(payload))


def _make_text_file(path: Path, text: str) -> None:
    with path.open("w", encoding="utf-8") as handle:
        handle.write(text)


def _tmp_allowed_dir(tmp_path: Path, directory_name: str = "stage2_historical_labels") -> Path:
    allowed_dir = tmp_path / "tests" / "fixtures" / "weather" / directory_name
    allowed_dir.mkdir(parents=True)
    return allowed_dir


def _valid_fixture_payload() -> dict[str, Any]:
    return _read_json(SYNTHETIC_DIR / "synthetic_valid_source_backed_confirmed.json")


def test_implementation_prd_exists_and_includes_canonical_id() -> None:
    assert PRD_PATH.is_file()
    assert CANONICAL_ID in PRD_PATH.read_text(encoding="utf-8")


def test_source_module_exists_and_compiles() -> None:
    assert SOURCE_PATH.is_file()
    py_compile.compile(str(SOURCE_PATH), doraise=True)


def test_source_module_uses_standard_library_plus_existing_validator_only() -> None:
    tree = ast.parse(SOURCE_PATH.read_text(encoding="utf-8"))
    import_roots: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            import_roots.update(alias.name.split(".")[0] for alias in node.names)
        if isinstance(node, ast.ImportFrom) and node.module:
            import_roots.add(node.module.split(".")[0])

    assert import_roots <= {"__future__", "dataclasses", "json", "pathlib", "typing", "meg"}


def test_source_module_avoids_forbidden_runtime_fragments_except_static_json_loads() -> None:
    source_text = SOURCE_PATH.read_text(encoding="utf-8")
    allowed_static_parse_fragment = "json." + "loads"
    unexpected = [
        fragment
        for fragment in _forbidden_fragments()
        if fragment in source_text and fragment != "json." + "load"
    ]

    assert allowed_static_parse_fragment in source_text
    assert unexpected == []


def test_implementation_test_avoids_forbidden_runtime_fragments_except_static_json_loads() -> None:
    test_text = THIS_TEST_PATH.read_text(encoding="utf-8")
    unexpected = [
        fragment
        for fragment in _forbidden_fragments()
        if fragment in test_text and fragment != "json." + "load"
    ]

    assert "json." + "loads" in test_text
    assert unexpected == []


def test_fixture_json_and_readme_files_are_unchanged() -> None:
    observed_files = {
        path.relative_to(REPO_ROOT).as_posix()
        for fixture_dir in (SYNTHETIC_DIR, REAL_DIR)
        for path in fixture_dir.iterdir()
        if path.is_file()
    }
    assert observed_files == set(EXPECTED_FIXTURE_HASHES)

    for rel_path, expected_hash in EXPECTED_FIXTURE_HASHES.items():
        digest = hashlib.sha256((REPO_ROOT / rel_path).read_bytes()).hexdigest()
        assert digest == expected_hash


def test_loader_reads_all_synthetic_fixtures() -> None:
    loaded = load_historical_label_fixture_directory(SYNTHETIC_DIR, repo_root=REPO_ROOT)

    assert len(loaded) == 3
    assert {fixture.path.name for fixture in loaded} == SYNTHETIC_FIXTURE_FILES
    assert {fixture.synthetic_or_real for fixture in loaded} == {"synthetic"}


def test_loader_reads_both_real_source_backed_fixtures() -> None:
    loaded = load_historical_label_fixture_directory(REAL_DIR, repo_root=REPO_ROOT)

    assert len(loaded) == 2
    assert {fixture.path.name for fixture in loaded} == REAL_FIXTURE_FILES
    assert {fixture.synthetic_or_real for fixture in loaded} == {"real_source_backed"}


def test_directory_loader_returns_files_sorted_by_filename() -> None:
    for fixture_dir in (SYNTHETIC_DIR, REAL_DIR):
        loaded = load_historical_label_fixture_directory(fixture_dir, repo_root=REPO_ROOT)
        assert [fixture.path.name for fixture in loaded] == sorted(fixture.path.name for fixture in loaded)


def test_loaded_fixtures_include_expected_fields_and_matching_postures() -> None:
    loaded = load_historical_label_fixture_directory(SYNTHETIC_DIR, repo_root=REPO_ROOT) + load_historical_label_fixture_directory(REAL_DIR, repo_root=REPO_ROOT)

    for fixture in loaded:
        assert fixture.fixture_id
        assert fixture.synthetic_or_real in {"synthetic", "real_source_backed"}
        assert fixture.expected_validation_posture in {"pass", "blocked", "caution"}
        assert fixture.raw_fixture["fixture_id"] == fixture.fixture_id
        assert isinstance(fixture.metadata, HistoricalLabelMetadata)
        assert isinstance(fixture.validation_result, ValidationResult)
        assert _observed_posture(fixture) == fixture.expected_validation_posture


def test_expected_valid_and_blocked_postures_are_preserved() -> None:
    synthetic_valid = load_historical_label_fixture(
        SYNTHETIC_DIR / "synthetic_valid_source_backed_confirmed.json", repo_root=REPO_ROOT
    )
    real_precipitation = load_historical_label_fixture(
        REAL_DIR / "polymarket_nyc_may_2026_precipitation_less_than_2_no.json", repo_root=REPO_ROOT
    )
    synthetic_blocked = load_historical_label_fixture(
        SYNTHETIC_DIR / "synthetic_blocked_missing_provenance.json", repo_root=REPO_ROOT
    )
    synthetic_unclear = load_historical_label_fixture(
        SYNTHETIC_DIR / "synthetic_unclear_requires_adjudication.json", repo_root=REPO_ROOT
    )
    real_conflict = load_historical_label_fixture(
        REAL_DIR / "polymarket_nyc_may_12_2026_temperature_conflict.json", repo_root=REPO_ROOT
    )

    assert _observed_posture(synthetic_valid) == "pass"
    assert _observed_posture(real_precipitation) == "pass"
    assert _observed_posture(synthetic_blocked) == synthetic_blocked.expected_validation_posture == "blocked"
    assert _observed_posture(synthetic_unclear) == synthetic_unclear.expected_validation_posture == "blocked"
    assert _observed_posture(real_conflict) == real_conflict.expected_validation_posture == "blocked"


def test_non_allowlisted_missing_and_non_json_paths_fail_closed(tmp_path: Path) -> None:
    outside = tmp_path / "outside.json"
    _make_fixture_file(outside, _valid_fixture_payload())
    with pytest.raises(FixtureLoadError):
        load_historical_label_fixture(outside, repo_root=REPO_ROOT)

    missing_allowed_path = (
        tmp_path
        / "tests"
        / "fixtures"
        / "weather"
        / "stage2_historical_labels"
        / "missing.json"
    )
    with pytest.raises(FixtureLoadError):
        load_historical_label_fixture(missing_allowed_path, repo_root=tmp_path)

    allowed_dir = _tmp_allowed_dir(tmp_path)
    non_json = allowed_dir / "fixture.txt"
    _make_text_file(non_json, json.dumps(_valid_fixture_payload()))
    with pytest.raises(FixtureLoadError):
        load_historical_label_fixture(non_json, repo_root=tmp_path)


def test_malformed_and_non_object_json_fail_closed(tmp_path: Path) -> None:
    allowed_dir = _tmp_allowed_dir(tmp_path)
    malformed = allowed_dir / "malformed.json"
    _make_text_file(malformed, "{")
    with pytest.raises(FixtureLoadError):
        load_historical_label_fixture(malformed, repo_root=tmp_path)

    non_object = allowed_dir / "non_object.json"
    _make_fixture_file(non_object, ["not", "an", "object"])
    with pytest.raises(FixtureLoadError):
        load_historical_label_fixture(non_object, repo_root=tmp_path)


def test_missing_required_and_unexpected_closed_values_fail_closed(tmp_path: Path) -> None:
    allowed_dir = _tmp_allowed_dir(tmp_path)

    missing_required = _valid_fixture_payload()
    del missing_required["condition_id"]
    missing_path = allowed_dir / "missing_required.json"
    _make_fixture_file(missing_path, missing_required)
    with pytest.raises(FixtureLoadError):
        load_historical_label_fixture(missing_path, repo_root=tmp_path)

    unexpected_kind = _valid_fixture_payload()
    unexpected_kind["synthetic_or_real"] = "hybrid"
    unexpected_kind_path = allowed_dir / "unexpected_kind.json"
    _make_fixture_file(unexpected_kind_path, unexpected_kind)
    with pytest.raises(FixtureLoadError):
        load_historical_label_fixture(unexpected_kind_path, repo_root=tmp_path)

    unexpected_posture = _valid_fixture_payload()
    unexpected_posture["expected_validation_posture"] = "maybe"
    unexpected_posture_path = allowed_dir / "unexpected_posture.json"
    _make_fixture_file(unexpected_posture_path, unexpected_posture)
    with pytest.raises(FixtureLoadError):
        load_historical_label_fixture(unexpected_posture_path, repo_root=tmp_path)


def test_directory_loader_fails_closed_for_non_allowlisted_empty_and_nonrecursive_dirs(tmp_path: Path) -> None:
    outside_dir = tmp_path / "outside"
    outside_dir.mkdir()
    with pytest.raises(FixtureLoadError):
        load_historical_label_fixture_directory(outside_dir, repo_root=tmp_path)

    empty_allowed_dir = _tmp_allowed_dir(tmp_path)
    with pytest.raises(FixtureLoadError):
        load_historical_label_fixture_directory(empty_allowed_dir, repo_root=tmp_path)

    nested = empty_allowed_dir / "nested"
    nested.mkdir()
    _make_fixture_file(nested / "nested_fixture.json", _valid_fixture_payload())
    with pytest.raises(FixtureLoadError):
        load_historical_label_fixture_directory(empty_allowed_dir, repo_root=tmp_path)


def test_loader_source_does_not_use_environment_network_or_file_writes() -> None:
    source_text = SOURCE_PATH.read_text(encoding="utf-8")
    assert "Path.read_text" not in source_text
    assert ".read_text(" in source_text
    assert ".open(" not in source_text
    assert ".write(" not in source_text
    assert "iterdir(" in source_text


def test_prd_states_all_explicit_non_approval_boundaries() -> None:
    prd_text = PRD_PATH.read_text(encoding="utf-8")
    required_phrases = (
        "static historical-label loading/validation implementation only",
        "limited to explicit static fixture validation",
        "no ingestion was created",
        "no provider/API connectors were created",
        "no external API calls were created",
        "no credentials/secrets/config loading was created",
        "no forecast pulls were created",
        "no scoring/probability scoring was created",
        "no " + "back" + "testing/paper " + "simulation was created",
        "no runtime observation was created",
        "no trading/" + "order " + "placement/position sizing/autonomy was created",
        "no production behavior was created",
        "no C++/Rust runtime components were created",
        "no fixture JSON/README files were created or modified",
        "no historical-label data files or generated data were created",
        "future ingestion requires separate explicit approval",
        "future scoring/" + "back" + "testing requires separate explicit approval",
        "future runtime/trading requires separate explicit approval",
        "does not imply ingestion readiness, scoring readiness, runtime readiness, production readiness, "
        "or trading readiness",
    )

    for phrase in required_phrases:
        assert phrase in prd_text
