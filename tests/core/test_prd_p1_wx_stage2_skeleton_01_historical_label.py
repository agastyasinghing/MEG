from pathlib import Path

from meg.weather.stage2 import historical_label as hl


PRD_PATH = Path("docs/prd/PRD-P1-WX-STAGE2-SKELETON-01_HISTORICAL_LABEL_SKELETON_IMPLEMENTATION.md")
SOURCE_PATH = Path("meg/weather/stage2/historical_label.py")
CANONICAL_ID = "PRD-P1-WX-STAGE2-SKELETON-01"


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


def test_prd_doc_exists_with_canonical_id() -> None:
    assert PRD_PATH.exists()
    assert CANONICAL_ID in PRD_PATH.read_text(encoding="utf-8")


def test_module_imports_and_enums_are_closed_sets() -> None:
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


def test_dataclasses_can_be_instantiated_from_supplied_metadata() -> None:
    metadata = hl.historical_label_metadata_from_mapping(
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
                "as_of_timestamp": "2026-05-29T00:00:00Z",
            },
            "label_usability": {
                "posture": "usable_after_stage_2_approval",
                "evidence_status": "source_backed",
                "label_confidence": "confirmed",
            },
            "venue_rule_summary": "supplied rule metadata",
        }
    )

    assert metadata.condition_id == "condition-1"
    assert metadata.token_id == "token-1"
    assert metadata.outcome == "Yes"
    assert metadata.source_resolution.status is hl.SourceResolutionStatus.SOURCE_RESOLVED


def test_validation_passes_for_minimal_valid_supplied_metadata() -> None:
    result = hl.validate_historical_label_metadata(_valid_metadata())

    assert result.passed is True
    assert result.severity is hl.ValidationSeverity.PASSED
    assert result.reasons == ()


def test_validation_blocks_missing_resolver_source() -> None:
    metadata = _valid_metadata()
    result = hl.validate_historical_label_metadata(
        hl.HistoricalLabelMetadata(
            condition_id=metadata.condition_id,
            token_id=metadata.token_id,
            outcome=metadata.outcome,
            source_resolution=hl.SourceResolutionMetadata(
                resolver_source_identity="",
                status=hl.SourceResolutionStatus.SOURCE_RESOLVED,
                evidence_status=hl.EvidenceStatus.SOURCE_BACKED,
            ),
            point_in_time_provenance=metadata.point_in_time_provenance,
            label_usability=metadata.label_usability,
        )
    )

    assert result.passed is False
    assert result.severity is hl.ValidationSeverity.BLOCKED
    assert "resolver source identity is missing" in result.reasons


def test_validation_blocks_unresolved_conflicting_unknown_source_resolution_statuses() -> None:
    for status in (
        hl.SourceResolutionStatus.SOURCE_UNRESOLVED,
        hl.SourceResolutionStatus.SOURCE_CONFLICTING,
        hl.SourceResolutionStatus.SOURCE_UNKNOWN,
        hl.SourceResolutionStatus.REQUIRES_ADJUDICATION,
    ):
        metadata = _valid_metadata()
        result = hl.validate_historical_label_metadata(
            hl.HistoricalLabelMetadata(
                condition_id=metadata.condition_id,
                token_id=metadata.token_id,
                outcome=metadata.outcome,
                source_resolution=hl.SourceResolutionMetadata(
                    resolver_source_identity="venue resolver source",
                    status=status,
                    evidence_status=hl.EvidenceStatus.SOURCE_BACKED,
                ),
                point_in_time_provenance=metadata.point_in_time_provenance,
                label_usability=metadata.label_usability,
            )
        )
        assert result.passed is False
        assert result.severity is hl.ValidationSeverity.BLOCKED
        assert f"source-resolution status is {status.value}" in result.reasons


def test_validation_blocks_unavailable_or_ambiguous_point_in_time_availability() -> None:
    for status in (
        hl.PointInTimeAvailabilityStatus.UNAVAILABLE_AS_OF,
        hl.PointInTimeAvailabilityStatus.AMBIGUOUS_AS_OF,
    ):
        metadata = _valid_metadata()
        result = hl.validate_historical_label_metadata(
            hl.HistoricalLabelMetadata(
                condition_id=metadata.condition_id,
                token_id=metadata.token_id,
                outcome=metadata.outcome,
                source_resolution=metadata.source_resolution,
                point_in_time_provenance=hl.PointInTimeProvenanceMetadata(
                    availability_status=status,
                    evidence_status=hl.EvidenceStatus.SOURCE_BACKED,
                ),
                label_usability=metadata.label_usability,
            )
        )
        assert result.passed is False
        assert result.severity is hl.ValidationSeverity.BLOCKED
        assert f"point-in-time availability status is {status.value}" in result.reasons


def test_validation_blocks_missing_or_conflicting_evidence() -> None:
    for status in (hl.EvidenceStatus.MISSING, hl.EvidenceStatus.CONFLICTING):
        metadata = _valid_metadata()
        result = hl.validate_historical_label_metadata(
            hl.HistoricalLabelMetadata(
                condition_id=metadata.condition_id,
                token_id=metadata.token_id,
                outcome=metadata.outcome,
                source_resolution=hl.SourceResolutionMetadata(
                    resolver_source_identity="venue resolver source",
                    status=hl.SourceResolutionStatus.SOURCE_RESOLVED,
                    evidence_status=status,
                ),
                point_in_time_provenance=metadata.point_in_time_provenance,
                label_usability=metadata.label_usability,
            )
        )
        assert result.passed is False
        assert result.severity is hl.ValidationSeverity.BLOCKED
        assert f"source-resolution evidence status is {status.value}" in result.reasons


def test_validation_blocks_unknown_label_confidence() -> None:
    metadata = _valid_metadata()
    result = hl.validate_historical_label_metadata(
        hl.HistoricalLabelMetadata(
            condition_id=metadata.condition_id,
            token_id=metadata.token_id,
            outcome=metadata.outcome,
            source_resolution=metadata.source_resolution,
            point_in_time_provenance=metadata.point_in_time_provenance,
            label_usability=hl.LabelUsabilityMetadata(
                posture=hl.LabelUsabilityPosture.USABLE_AFTER_STAGE_2_APPROVAL,
                evidence_status=hl.EvidenceStatus.SOURCE_BACKED,
                label_confidence=hl.LabelConfidence.UNKNOWN,
            ),
        )
    )

    assert result.passed is False
    assert result.severity is hl.ValidationSeverity.BLOCKED
    assert "label confidence is unknown" in result.reasons


def test_validation_blocks_blocked_label_usability_postures() -> None:
    for posture in (
        hl.LabelUsabilityPosture.BLOCKED_PENDING_SOURCE_MATCH,
        hl.LabelUsabilityPosture.BLOCKED_PENDING_PROVENANCE,
        hl.LabelUsabilityPosture.BLOCKED_PENDING_ADJUDICATION,
    ):
        metadata = _valid_metadata()
        result = hl.validate_historical_label_metadata(
            hl.HistoricalLabelMetadata(
                condition_id=metadata.condition_id,
                token_id=metadata.token_id,
                outcome=metadata.outcome,
                source_resolution=metadata.source_resolution,
                point_in_time_provenance=metadata.point_in_time_provenance,
                label_usability=hl.LabelUsabilityMetadata(
                    posture=posture,
                    evidence_status=hl.EvidenceStatus.SOURCE_BACKED,
                    label_confidence=hl.LabelConfidence.CONFIRMED,
                ),
            )
        )
        assert result.passed is False
        assert result.severity is hl.ValidationSeverity.BLOCKED
        assert f"label usability posture is {posture.value}" in result.reasons


def test_test_file_does_not_create_files_or_call_services() -> None:
    text = Path(__file__).read_text(encoding="utf-8")
    forbidden_fragments = (
        ".write_" + "text",
        ".to" + "uch(",
        "so" + "cket.",
        "sub" + "process.",
    )
    assert all(fragment not in text for fragment in forbidden_fragments)


def test_source_module_text_avoids_forbidden_implementation_tokens() -> None:
    text = SOURCE_PATH.read_text(encoding="utf-8")
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
        "auto_" + "execute",
        "aut" + "onomous",
    )
    assert all(token not in text for token in forbidden_tokens)
