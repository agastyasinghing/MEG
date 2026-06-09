"""Static Stage 2 historical-label fixture loading helpers.

The helpers in this module are intentionally limited to caller-supplied fixture
paths under a closed allowlist. They adapt existing static fixture mappings into
the Stage 2 historical-label metadata validator and return deterministic results.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from meg.weather.stage2.historical_label import (
    HistoricalLabelMetadata,
    ValidationResult,
    historical_label_metadata_from_mapping,
    validate_historical_label_metadata,
)

ALLOWED_FIXTURE_DIRECTORY_PARTS: tuple[tuple[str, ...], ...] = (
    ("tests", "fixtures", "weather", "stage2_historical_labels"),
    ("tests", "fixtures", "weather", "stage2_real_source_backed_labels"),
)

_ALLOWED_SYNTHETIC_OR_REAL = frozenset({"synthetic", "real_source_backed"})
_ALLOWED_EXPECTED_VALIDATION_POSTURES = frozenset({"pass", "blocked", "caution"})
_REQUIRED_TOP_LEVEL_FIELDS = frozenset(
    {
        "fixture_id",
        "synthetic_or_real",
        "expected_validation_posture",
        "condition_id",
        "token_id",
        "outcome",
        "source_resolution",
        "point_in_time_provenance",
        "label_usability",
        "venue_rule_summary",
    }
)
_METADATA_FIELDS = (
    "condition_id",
    "token_id",
    "outcome",
    "source_resolution",
    "point_in_time_provenance",
    "label_usability",
    "venue_rule_summary",
)


class FixtureLoadError(ValueError):
    """Raised when a static historical-label fixture fails closed."""


@dataclass(frozen=True)
class LoadedHistoricalLabelFixture:
    """Loaded static fixture plus adapted Stage 2 validation artifacts."""

    path: Path
    fixture_id: str
    synthetic_or_real: str
    expected_validation_posture: str
    raw_fixture: Mapping[str, Any]
    metadata: HistoricalLabelMetadata
    validation_result: ValidationResult


def _resolved_repo_root(repo_root: Path) -> Path:
    return repo_root.resolve(strict=True)


def _allowed_directories(repo_root: Path) -> tuple[Path, ...]:
    return tuple(
        repo_root.joinpath(*parts).resolve(strict=False)
        for parts in ALLOWED_FIXTURE_DIRECTORY_PARTS
    )


def _is_relative_to(path: Path, directory: Path) -> bool:
    try:
        path.relative_to(directory)
    except ValueError:
        return False
    return True


def _require_allowed_file_path(path: Path, *, repo_root: Path) -> Path:
    resolved_root = _resolved_repo_root(repo_root)
    try:
        resolved_path = path.resolve(strict=True)
    except FileNotFoundError as exc:
        raise FixtureLoadError("fixture file is missing") from exc

    if resolved_path.suffix != ".json":
        raise FixtureLoadError("fixture path must be a .json file")

    if not any(
        _is_relative_to(resolved_path, directory)
        for directory in _allowed_directories(resolved_root)
    ):
        raise FixtureLoadError("fixture path is outside the static allowlist")

    return resolved_path


def _require_allowed_directory_path(directory: Path, *, repo_root: Path) -> Path:
    resolved_root = _resolved_repo_root(repo_root)
    try:
        resolved_directory = directory.resolve(strict=True)
    except FileNotFoundError as exc:
        raise FixtureLoadError("fixture directory is missing") from exc

    if resolved_directory not in _allowed_directories(resolved_root):
        raise FixtureLoadError("fixture directory is outside the static allowlist")

    return resolved_directory


def _read_fixture_mapping(path: Path) -> Mapping[str, Any]:
    try:
        parsed = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise FixtureLoadError("fixture JSON is malformed") from exc

    if not isinstance(parsed, dict):
        raise FixtureLoadError("fixture JSON root must be an object")

    return parsed


def _require_text_field(fixture: Mapping[str, Any], field_name: str) -> str:
    value = fixture.get(field_name)
    if not isinstance(value, str) or not value.strip():
        raise FixtureLoadError(f"fixture field {field_name} is missing")
    return value


def _metadata_mapping_from_fixture(fixture: Mapping[str, Any]) -> Mapping[str, Any]:
    return {field_name: fixture[field_name] for field_name in _METADATA_FIELDS}


def _validation_posture(result: ValidationResult) -> str:
    if result.passed:
        return "pass"
    return result.severity.value


def load_historical_label_fixture(path: Path, *, repo_root: Path) -> LoadedHistoricalLabelFixture:
    """Load and validate one explicitly supplied static historical-label fixture."""

    resolved_path = _require_allowed_file_path(path, repo_root=repo_root)
    fixture = _read_fixture_mapping(resolved_path)

    missing_fields = sorted(_REQUIRED_TOP_LEVEL_FIELDS - set(fixture))
    if missing_fields:
        raise FixtureLoadError("fixture is missing required fields: " + ", ".join(missing_fields))

    fixture_id = _require_text_field(fixture, "fixture_id")
    synthetic_or_real = _require_text_field(fixture, "synthetic_or_real")
    if synthetic_or_real not in _ALLOWED_SYNTHETIC_OR_REAL:
        raise FixtureLoadError("fixture synthetic_or_real value is not allowed")

    expected_validation_posture = _require_text_field(fixture, "expected_validation_posture")
    if expected_validation_posture not in _ALLOWED_EXPECTED_VALIDATION_POSTURES:
        raise FixtureLoadError("fixture expected_validation_posture value is not allowed")

    try:
        metadata = historical_label_metadata_from_mapping(_metadata_mapping_from_fixture(fixture))
    except (KeyError, TypeError, ValueError) as exc:
        raise FixtureLoadError("fixture metadata cannot be adapted for Stage 2 validation") from exc

    validation_result = validate_historical_label_metadata(metadata)
    observed_validation_posture = _validation_posture(validation_result)
    if observed_validation_posture != expected_validation_posture:
        raise FixtureLoadError("fixture expected validation posture does not match observed posture")

    return LoadedHistoricalLabelFixture(
        path=resolved_path,
        fixture_id=fixture_id,
        synthetic_or_real=synthetic_or_real,
        expected_validation_posture=expected_validation_posture,
        raw_fixture=fixture,
        metadata=metadata,
        validation_result=validation_result,
    )


def load_historical_label_fixture_directory(
    directory: Path, *, repo_root: Path
) -> tuple[LoadedHistoricalLabelFixture, ...]:
    """Load non-recursive .json fixtures from one exact allowlisted directory."""

    resolved_directory = _require_allowed_directory_path(directory, repo_root=repo_root)
    fixture_paths = tuple(
        sorted(
            (path for path in resolved_directory.iterdir() if path.suffix == ".json"),
            key=lambda path: path.name,
        )
    )
    if not fixture_paths:
        raise FixtureLoadError("fixture directory contains no .json files")

    return tuple(
        load_historical_label_fixture(fixture_path, repo_root=repo_root) for fixture_path in fixture_paths
    )
