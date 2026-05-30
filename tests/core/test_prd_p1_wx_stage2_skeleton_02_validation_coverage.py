from dataclasses import replace
from pathlib import Path

import pytest

from meg.weather.stage2 import historical_label as hl


PRD_PATH = Path("docs/prd/PRD-P1-WX-STAGE2-SKELETON-02_VALIDATION_COVERAGE_REFINEMENT.md")
SOURCE_PATH = Path("meg/weather/stage2/historical_label.py")
SKELETON_01_TEST_PATH = Path("tests/core/test_prd_p1_wx_stage2_skeleton_01_historical_label.py")
THIS_TEST_PATH = Path(__file__)
CANONICAL_ID = "PRD-P1-WX-STAGE2-SKELETON-02"


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
            as_of_timestamp="2026-05-29T00:00:00Z",
        ),
        label_usability=hl.LabelUsabilityMetadata(
            posture=hl.LabelUsabilityPosture.USABLE_AFTER_STAGE_2_APPROVAL,
            evidence_status=hl.EvidenceStatus.SOURCE_BACKED,
            label_confidence=hl.LabelConfidence.CONFIRMED,
        ),
        venue_rule_summary="supplied venue-defined rule metadata only",
    )


def _assert_does_not_pass(result: hl.ValidationResult) -> None:
    assert result.passed is False
    assert result.severity in {hl.ValidationSeverity.BLOCKED, hl.ValidationSeverity.CAUTION}


def test_prd_guard_doc_exists_with_canonical_id() -> None:
    assert PRD_PATH.exists()
    text = PRD_PATH.read_text(encoding="utf-8")
    assert CANONICAL_ID in text


def test_source_module_imports() -> None:
    assert hl.HistoricalLabelMetadata.__name__ == "HistoricalLabelMetadata"


def test_enum_values_remain_exactly_unchanged() -> None:
    assert hl.SourceResolutionStatus.values() == frozenset(
        {
            "source_resolved",
            "source_unresolved",
            "source_conflicting",
            "source_unknown",
            "requires_adjudication",
        }
    )
    assert hl.PointInTimeAvailabilityStatus.values() == frozenset(
        {
            "available_as_of",
            "unavailable_as_of",
            "ambiguous_as_of",
            "not_applicable",
            "design_only",
        }
    )
    assert hl.LabelUsabilityPosture.values() == frozenset(
        {
            "design_only",
            "usable_after_stage_2_approval",
            "blocked_pending_source_match",
            "blocked_pending_provenance",
            "blocked_pending_adjudication",
        }
    )
    assert hl.EvidenceStatus.values() == frozenset(
        {"source_backed", "reviewer_inferred", "missing", "conflicting", "not_applicable"}
    )
    assert hl.LabelConfidence.values() == frozenset({"confirmed", "unclear", "unknown"})
    assert hl.ValidationSeverity.values() == frozenset({"passed", "caution", "failed", "blocked"})


def test_valid_supplied_metadata_still_passes() -> None:
    result = hl.validate_historical_label_metadata(_valid_metadata())

    assert result.passed is True
    assert result.severity is hl.ValidationSeverity.PASSED
    assert result.reasons == ()


@pytest.mark.parametrize(
    ("field_name", "reason"),
    (
        ("condition_id", "condition_id is missing"),
        ("token_id", "token_id is missing"),
        ("outcome", "outcome is missing"),
        ("venue_rule_summary", "venue_rule_summary is missing"),
    ),
)
def test_missing_required_text_fields_do_not_pass(field_name: str, reason: str) -> None:
    metadata = replace(_valid_metadata(), **{field_name: "  "})

    result = hl.validate_historical_label_metadata(metadata)

    _assert_does_not_pass(result)
    assert reason in result.reasons


@pytest.mark.parametrize(
    ("field_name", "field_value", "reason"),
    (
        ("condition_id", None, "condition_id is missing"),
        ("token_id", None, "token_id is missing"),
        ("outcome", None, "outcome is missing"),
        ("venue_rule_summary", None, "venue_rule_summary is missing"),
        ("condition_id", 123, "condition_id is missing"),
        ("token_id", 123, "token_id is missing"),
    ),
)
def test_none_or_non_string_required_text_fields_do_not_pass(
    field_name: str,
    field_value: object,
    reason: str,
) -> None:
    metadata = replace(_valid_metadata(), **{field_name: field_value})

    result = hl.validate_historical_label_metadata(metadata)

    _assert_does_not_pass(result)
    assert reason in result.reasons


def test_none_resolver_source_identity_does_not_pass() -> None:
    metadata = _valid_metadata()
    result = hl.validate_historical_label_metadata(
        replace(
            metadata,
            source_resolution=replace(
                metadata.source_resolution,
                resolver_source_identity=None,
            ),
        )
    )

    _assert_does_not_pass(result)
    assert "resolver source identity is missing" in result.reasons


@pytest.mark.parametrize(
    "status",
    (
        hl.PointInTimeAvailabilityStatus.NOT_APPLICABLE,
        hl.PointInTimeAvailabilityStatus.DESIGN_ONLY,
    ),
)
def test_conservative_point_in_time_statuses_do_not_pass(
    status: hl.PointInTimeAvailabilityStatus,
) -> None:
    metadata = _valid_metadata()
    result = hl.validate_historical_label_metadata(
        replace(
            metadata,
            point_in_time_provenance=replace(
                metadata.point_in_time_provenance,
                availability_status=status,
            ),
        )
    )

    _assert_does_not_pass(result)
    assert f"point-in-time availability status is {status.value}" in result.reasons


@pytest.mark.parametrize(
    "status",
    (hl.EvidenceStatus.REVIEWER_INFERRED, hl.EvidenceStatus.NOT_APPLICABLE),
)
def test_conservative_evidence_statuses_do_not_pass(status: hl.EvidenceStatus) -> None:
    metadata = _valid_metadata()
    result = hl.validate_historical_label_metadata(
        replace(
            metadata,
            source_resolution=replace(metadata.source_resolution, evidence_status=status),
        )
    )

    _assert_does_not_pass(result)
    assert f"source-resolution evidence status is {status.value}" in result.reasons


def test_unclear_confidence_does_not_pass() -> None:
    metadata = _valid_metadata()
    result = hl.validate_historical_label_metadata(
        replace(
            metadata,
            label_usability=replace(
                metadata.label_usability,
                label_confidence=hl.LabelConfidence.UNCLEAR,
            ),
        )
    )

    _assert_does_not_pass(result)
    assert "label confidence is unclear" in result.reasons


def test_design_only_label_usability_does_not_pass() -> None:
    metadata = _valid_metadata()
    result = hl.validate_historical_label_metadata(
        replace(
            metadata,
            label_usability=replace(
                metadata.label_usability,
                posture=hl.LabelUsabilityPosture.DESIGN_ONLY,
            ),
        )
    )

    _assert_does_not_pass(result)
    assert "label usability posture is design_only" in result.reasons


@pytest.mark.parametrize(
    ("builder", "metadata"),
    (
        (
            hl.source_resolution_metadata_from_mapping,
            {
                "resolver_source_identity": "venue resolver source",
                "status": "not_a_source_status",
                "evidence_status": "source_backed",
            },
        ),
        (
            hl.point_in_time_provenance_metadata_from_mapping,
            {"availability_status": "not_an_availability_status", "evidence_status": "source_backed"},
        ),
        (
            hl.label_usability_metadata_from_mapping,
            {
                "posture": "not_a_posture",
                "evidence_status": "source_backed",
                "label_confidence": "confirmed",
            },
        ),
        (
            hl.label_usability_metadata_from_mapping,
            {
                "posture": "usable_after_stage_2_approval",
                "evidence_status": "not_an_evidence_status",
                "label_confidence": "confirmed",
            },
        ),
        (
            hl.label_usability_metadata_from_mapping,
            {
                "posture": "usable_after_stage_2_approval",
                "evidence_status": "source_backed",
                "label_confidence": "not_a_confidence",
            },
        ),
    ),
)
def test_invalid_enum_strings_raise_value_error(builder: object, metadata: dict[str, str]) -> None:
    with pytest.raises(ValueError):
        builder(metadata)


@pytest.mark.parametrize(
    ("builder", "metadata", "missing_key"),
    (
        (
            hl.source_resolution_metadata_from_mapping,
            {"resolver_source_identity": "venue resolver source", "status": "source_resolved"},
            "evidence_status",
        ),
        (
            hl.point_in_time_provenance_metadata_from_mapping,
            {"evidence_status": "source_backed"},
            "availability_status",
        ),
        (
            hl.label_usability_metadata_from_mapping,
            {"evidence_status": "source_backed", "label_confidence": "confirmed"},
            "posture",
        ),
        (
            hl.historical_label_metadata_from_mapping,
            {
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
                },
                "label_usability": {
                    "posture": "usable_after_stage_2_approval",
                    "evidence_status": "source_backed",
                    "label_confidence": "confirmed",
                },
            },
            "venue_rule_summary",
        ),
    ),
)
def test_missing_required_mapping_keys_raise_key_error(
    builder: object,
    metadata: dict[str, object],
    missing_key: str,
) -> None:
    with pytest.raises(KeyError) as exc_info:
        builder(metadata)

    assert exc_info.value.args == (missing_key,)


def test_mapping_builder_preserves_invalid_required_text_for_fail_closed_validation() -> None:
    metadata = hl.historical_label_metadata_from_mapping(
        {
            "condition_id": None,
            "token_id": 123,
            "outcome": "Yes",
            "source_resolution": {
                "resolver_source_identity": None,
                "status": "source_resolved",
                "evidence_status": "source_backed",
            },
            "point_in_time_provenance": {
                "availability_status": "available_as_of",
                "evidence_status": "source_backed",
            },
            "label_usability": {
                "posture": "usable_after_stage_2_approval",
                "evidence_status": "source_backed",
                "label_confidence": "confirmed",
            },
            "venue_rule_summary": None,
        }
    )

    result = hl.validate_historical_label_metadata(metadata)

    _assert_does_not_pass(result)
    assert "condition_id is missing" in result.reasons
    assert "token_id is missing" in result.reasons
    assert "venue_rule_summary is missing" in result.reasons
    assert "resolver source identity is missing" in result.reasons


def test_validators_are_supplied_metadata_only_and_do_not_mutate_inputs() -> None:
    metadata = _valid_metadata()

    first_result = hl.validate_historical_label_metadata(metadata)
    second_result = hl.validate_historical_label_metadata(metadata)

    assert first_result == second_result
    assert metadata == _valid_metadata()


def test_tests_do_not_create_files_or_call_network() -> None:
    for path in (THIS_TEST_PATH, SKELETON_01_TEST_PATH):
        text = path.read_text(encoding="utf-8")
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


def test_source_and_tests_avoid_forbidden_implementation_tokens() -> None:
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
    for path in (SOURCE_PATH, SKELETON_01_TEST_PATH, THIS_TEST_PATH):
        text = path.read_text(encoding="utf-8")
        assert all(token not in text for token in forbidden_tokens)
