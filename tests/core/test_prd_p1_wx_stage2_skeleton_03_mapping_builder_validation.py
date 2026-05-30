"""Targeted PRD-P1-WX-STAGE2-SKELETON-03 mapping-builder coverage."""
from __future__ import annotations

import importlib
from dataclasses import replace
from pathlib import Path
from typing import Any

import pytest

from meg.weather.stage2 import historical_label as hl

REPO_ROOT = Path(__file__).resolve().parents[2]
SOURCE_PATH = REPO_ROOT / "meg" / "weather" / "stage2" / "historical_label.py"
THIS_TEST_PATH = Path(__file__)
PRD_GUARD_PATH = (
    REPO_ROOT
    / "docs"
    / "prd"
    / "PRD-P1-WX-STAGE2-SKELETON-03_TARGETED_MAPPING_BUILDER_VALIDATION_COVERAGE.md"
)
CANONICAL_ID = "PRD-P1-WX-STAGE2-SKELETON-03"


def _valid_metadata() -> hl.HistoricalLabelMetadata:
    return hl.HistoricalLabelMetadata(
        condition_id="condition-1",
        token_id="token-1",
        outcome="Yes",
        source_resolution=hl.SourceResolutionMetadata(
            resolver_source_identity="venue resolver source",
            status=hl.SourceResolutionStatus.SOURCE_RESOLVED,
            evidence_status=hl.EvidenceStatus.SOURCE_BACKED,
        ),
        point_in_time_provenance=hl.PointInTimeProvenanceMetadata(
            availability_status=hl.PointInTimeAvailabilityStatus.AVAILABLE_AS_OF,
            evidence_status=hl.EvidenceStatus.SOURCE_BACKED,
            as_of_timestamp="2026-01-01T00:00:00Z",
        ),
        label_usability=hl.LabelUsabilityMetadata(
            posture=hl.LabelUsabilityPosture.USABLE_AFTER_STAGE_2_APPROVAL,
            evidence_status=hl.EvidenceStatus.SOURCE_BACKED,
            label_confidence=hl.LabelConfidence.CONFIRMED,
        ),
        venue_rule_summary="Venue rule summary supplied by reviewer.",
    )


def _valid_mapping() -> dict[str, Any]:
    return {
        "condition_id": "condition-1",
        "token_id": "token-1",
        "outcome": "Yes",
        "source_resolution": {
            "resolver_source_identity": "venue resolver source",
            "status": "source_resolved",
            "evidence_status": "source_backed",
        },
        "point_in_time_provenance": {
            "availability_status": "available_as_of",
            "evidence_status": "source_backed",
            "as_of_timestamp": "2026-01-01T00:00:00Z",
        },
        "label_usability": {
            "posture": "usable_after_stage_2_approval",
            "evidence_status": "source_backed",
            "label_confidence": "confirmed",
        },
        "venue_rule_summary": "Venue rule summary supplied by reviewer.",
    }


def _assert_does_not_pass(result: hl.ValidationResult) -> None:
    assert result.passed is False
    assert result.severity in (hl.ValidationSeverity.BLOCKED, hl.ValidationSeverity.CAUTION)
    assert result.reasons


def test_prd_guard_doc_exists_and_contains_canonical_id() -> None:
    assert PRD_GUARD_PATH.is_file()
    assert CANONICAL_ID in PRD_GUARD_PATH.read_text(encoding="utf-8")


def test_source_module_imports() -> None:
    module = importlib.import_module("meg.weather.stage2.historical_label")

    assert module is hl


def test_valid_supplied_metadata_still_passes() -> None:
    result = hl.validate_historical_label_metadata(_valid_metadata())

    assert result.passed is True
    assert result.severity is hl.ValidationSeverity.PASSED
    assert result.reasons == ()


@pytest.mark.parametrize(
    ("field_name", "field_value", "reason"),
    (
        ("outcome", 123, "outcome is missing"),
        ("venue_rule_summary", 123, "venue_rule_summary is missing"),
    ),
)
def test_non_string_required_historical_label_text_fields_do_not_pass(
    field_name: str,
    field_value: object,
    reason: str,
) -> None:
    metadata = replace(_valid_metadata(), **{field_name: field_value})

    result = hl.validate_historical_label_metadata(metadata)

    _assert_does_not_pass(result)
    assert reason in result.reasons


@pytest.mark.parametrize("resolver_source_identity", (123, "   \t\n"))
def test_invalid_resolver_source_identity_does_not_pass(
    resolver_source_identity: object,
) -> None:
    metadata = _valid_metadata()

    result = hl.validate_historical_label_metadata(
        replace(
            metadata,
            source_resolution=replace(
                metadata.source_resolution,
                resolver_source_identity=resolver_source_identity,
            ),
        )
    )

    _assert_does_not_pass(result)
    assert "resolver source identity is missing" in result.reasons


@pytest.mark.parametrize(
    "missing_key",
    ("source_resolution", "point_in_time_provenance", "label_usability"),
)
def test_historical_label_mapping_builder_missing_nested_metadata_keys_fail_closed(
    missing_key: str,
) -> None:
    metadata = _valid_mapping()
    del metadata[missing_key]

    with pytest.raises(KeyError) as exc_info:
        hl.historical_label_metadata_from_mapping(metadata)

    assert exc_info.value.args == (missing_key,)


@pytest.mark.parametrize(
    "nested_key",
    ("source_resolution", "point_in_time_provenance", "label_usability"),
)
def test_historical_label_mapping_builder_non_mapping_nested_metadata_fails_closed(
    nested_key: str,
) -> None:
    metadata = _valid_mapping()
    metadata[nested_key] = "not supplied nested metadata"

    with pytest.raises((TypeError, AttributeError, ValueError, KeyError)):
        built_metadata = hl.historical_label_metadata_from_mapping(metadata)
        result = hl.validate_historical_label_metadata(built_metadata)
        assert result.passed is False


def test_tests_do_not_create_files_or_call_network() -> None:
    text = THIS_TEST_PATH.read_text(encoding="utf-8")
    forbidden_fragments = (
        ".write_" + "text",
        ".write_" + "bytes",
        ".to" + "uch(",
        "mk" + "stemp",
        "mk" + "dtemp",
        "so" + "cket.",
        "sub" + "process.",
        "url" + "open",
    )

    assert all(fragment not in text for fragment in forbidden_fragments)


def test_source_and_new_test_avoid_forbidden_implementation_tokens() -> None:
    forbidden_tokens = (
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
    )

    for path in (SOURCE_PATH, THIS_TEST_PATH):
        text = path.read_text(encoding="utf-8")
        assert all(token not in text for token in forbidden_tokens)
