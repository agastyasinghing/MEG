"""Focused contract tests for Stage 3 scoring/diagnostic definitions."""

from dataclasses import FrozenInstanceError, fields
from enum import StrEnum
import inspect
from typing import get_type_hints

import pytest

from meg.weather.stage3.baseline_contracts import BaselineType
import meg.weather.stage3.scoring_and_diagnostics as subject


def valid_mapping(**changes):
    value = {
        "scoring_definition_id": "score-1",
        "scoring_artifact": "brier_score",
        "definition_status": "active",
        "definition_version": "v1",
        "method_id": "method",
        "method_version": "v1",
        "prediction_representation": "binary_outcome_probability",
        "aggregation_rule_id": "aggregation",
        "weighting_rule_id": "weighting",
        "sample_support_policy_id": "support",
        "uncertainty_method_id": "uncertainty",
        "uncertainty_level_id": "level",
        "supported_stratification_axes": ["market_family", "market_family"],
        "required_baseline_types": ["climatology", "persistence"],
        "probability_boundary_policy_id": None,
        "binning_policy_id": None,
        "decomposition_policy_id": None,
        "pit_treatment_policy_id": None,
        "tie_treatment_policy_id": None,
        "threshold_weight_policy_id": None,
        "claim_justification_id": None,
        "scoring_target_posture": "venue_defined_settlement_outcome",
        "proper_score_direction_posture": "lower_is_better",
        "paired_comparison_posture": "same_split_fold_cutoff_eligible_records_labels_metric_aggregation_weighting_and_stratum_required",
        "applicability_posture": "representation_gated",
        "availability_posture": "point_in_time_required",
        "predeclaration_posture": "before_test_inspection_required",
        "tuning_posture": "train_or_calibration_only",
        "sparse_bucket_posture": "blocked_or_insufficient_not_silently_pooled",
        "interpretation_posture": "no_economic_edge_or_executability_inference",
        "market_price_posture": "not_approved_as_baseline_or_truth",
        "scoring_execution_posture": "not_approved",
        "diagnostic_execution_posture": "not_approved",
        "storage_persistence_posture": "not_approved",
        "provenance_refs": ["caller-ref", "caller-ref"],
        "exclusion_reason": None,
    }
    value["supported_stratification_axes"] = []
    value.update(changes)
    return value


def codes(mapping):
    return subject.scoring_diagnostic_definition_from_mapping(mapping)[1].codes


def test_public_api_enum_members_and_private_matrices_are_frozen():
    assert subject.__all__ == (
        "ScoringArtifact", "ScoringPredictionRepresentation", "ScoringDefinitionStatus",
        "ScoringValidationSeverity", "ScoringValidationCode", "ScoringDiagnosticDefinition",
        "ScoringDiagnosticValidationResult", "scoring_diagnostic_definition_from_mapping",
        "validate_scoring_diagnostic_definition",
    )
    assert "BaselineType" not in subject.__all__
    assert [(x.name, x.value) for x in subject.ScoringArtifact] == [
        ("BRIER_SCORE", "brier_score"), ("LOG_SCORE", "log_score"),
        ("RELIABILITY_DIAGRAM", "reliability_diagram"),
        ("BRIER_DECOMPOSITION", "brier_decomposition"), ("CRPS", "crps"),
        ("PIT_HISTOGRAM", "pit_histogram"), ("RANK_HISTOGRAM", "rank_histogram"),
        ("THRESHOLD_WEIGHTED_CRPS", "threshold_weighted_crps"),
    ]
    assert [x.value for x in subject.ScoringPredictionRepresentation] == [
        "binary_outcome_probability", "full_predictive_distribution", "finite_comparable_ensemble"
    ]
    assert [x.value for x in subject.ScoringDefinitionStatus] == ["active", "blocked"]
    assert [x.value for x in subject.ScoringValidationSeverity] == ["passed", "blocked"]
    assert [x.value for x in subject.ScoringValidationCode] == [x.name.lower() for x in subject.ScoringValidationCode]
    assert len(subject.ScoringValidationCode) == 24
    assert tuple(subject._REPRESENTATION_MATRIX) == tuple(subject.ScoringArtifact)
    assert tuple(subject._ARTIFACT_POLICY_MATRIX) == tuple(subject.ScoringArtifact)
    assert subject._PERMITTED_STRATIFICATION_AXES == (
        "market_family", "threshold_distance", "forecast_horizon", "station_source_compatibility",
        "trap_category", "season_or_regime_when_supported", "archive_layer",
    )
    assert subject._REQUIRED_BASELINE_TYPES == (BaselineType.CLIMATOLOGY, BaselineType.PERSISTENCE)


def test_dataclasses_signatures_source_order_and_result_invariants():
    assert len(fields(subject.ScoringDiagnosticDefinition)) == 37
    assert [field.name for field in fields(subject.ScoringDiagnosticDefinition)] == list(subject._REQUIRED_MAPPING_KEYS) + list(subject._OPTIONAL_MAPPING_KEYS)
    assert fields(subject.ScoringDiagnosticDefinition)[-1].default is None
    hints = get_type_hints(subject.ScoringDiagnosticDefinition)
    assert hints["required_baseline_types"] == tuple[BaselineType, ...]
    assert hints["supersedes_scoring_definition_id"] == str | None
    assert list(inspect.signature(subject.scoring_diagnostic_definition_from_mapping).parameters) == ["mapping"]
    assert list(inspect.signature(subject.validate_scoring_diagnostic_definition).parameters) == ["definition"]
    source = inspect.getsource(subject)
    assert source.index("def scoring_diagnostic_definition_from_mapping") < source.index("def validate_scoring_diagnostic_definition")
    empty = subject.ScoringDiagnosticValidationResult(subject.ScoringValidationSeverity.BLOCKED, False)
    failed = subject.ScoringDiagnosticValidationResult(subject.ScoringValidationSeverity.PASSED, True, (subject.ScoringValidationCode.UNEXPECTED_FIELD,))
    assert (empty.severity, empty.passed, empty.codes) == (subject.ScoringValidationSeverity.PASSED, True, ())
    assert (failed.severity, failed.passed) == (subject.ScoringValidationSeverity.BLOCKED, False)
    with pytest.raises(FrozenInstanceError):
        empty.passed = False


def test_mapping_success_adapts_without_mutating_caller_and_is_deterministic():
    mapping = valid_mapping(supported_stratification_axes=["market_family"], provenance_refs=["r", "r"])
    original_axes = mapping["supported_stratification_axes"]
    first = subject.scoring_diagnostic_definition_from_mapping(mapping)
    second = subject.scoring_diagnostic_definition_from_mapping(mapping)
    assert first == second
    definition, result = first
    assert result.passed and definition is not None
    assert definition.scoring_artifact is subject.ScoringArtifact.BRIER_SCORE
    assert definition.required_baseline_types == (BaselineType.CLIMATOLOGY, BaselineType.PERSISTENCE)
    assert definition.provenance_refs == ("r", "r")
    assert mapping["supported_stratification_axes"] is original_axes
    with pytest.raises(FrozenInstanceError):
        definition.method_id = "changed"


def test_mapping_early_returns_hostile_roots_and_baseexception_boundary():
    expected = (subject.ScoringValidationCode.MISSING_REQUIRED_FIELD,) * 36
    assert codes(None) == expected

    class Hostile(dict):
        def items(self):
            raise RuntimeError("ordinary snapshot failure")

    assert codes(Hostile()) == expected

    class Interrupting(dict):
        def items(self):
            raise KeyboardInterrupt

    with pytest.raises(KeyboardInterrupt):
        subject.scoring_diagnostic_definition_from_mapping(Interrupting())


def test_shape_order_string_subclass_keys_and_aggregation():
    class Text(str):
        pass

    mapping = valid_mapping(supported_stratification_axes=["market_family", "market_family"])
    del mapping["method_id"]
    mapping["z"] = 1
    mapping["a"] = 2
    mapping[Text("method_id")] = "method"
    mapping[3] = "other"
    result = codes(mapping)
    assert result[:5] == (
        subject.ScoringValidationCode.MISSING_REQUIRED_FIELD,
        subject.ScoringValidationCode.UNEXPECTED_FIELD,
        subject.ScoringValidationCode.UNEXPECTED_FIELD,
        subject.ScoringValidationCode.UNEXPECTED_FIELD,
        subject.ScoringValidationCode.UNEXPECTED_FIELD,
    )
    assert result[-1] == subject.ScoringValidationCode.INVALID_STRATIFICATION_AXES


def test_exact_enum_adaptation_and_direct_validation_do_not_adapt():
    class Text(str):
        pass

    assert codes(valid_mapping(scoring_artifact=Text("brier_score"))) == (subject.ScoringValidationCode.INVALID_SCORING_ARTIFACT,)
    definition, _ = subject.scoring_diagnostic_definition_from_mapping(valid_mapping())
    assert definition is not None
    object.__setattr__(definition, "scoring_artifact", "brier_score")
    assert subject.validate_scoring_diagnostic_definition(definition).codes == (subject.ScoringValidationCode.INVALID_SCORING_ARTIFACT,)


@pytest.mark.parametrize("field", subject._REQUIRED_TEXT_FIELDS)
def test_every_required_text_field(field):
    result = codes(valid_mapping(**{field: " "}))
    assert result.count(subject.ScoringValidationCode.BLANK_REQUIRED_TEXT) == 1


@pytest.mark.parametrize("field", subject._NULLABLE_TEXT_FIELDS)
def test_every_nullable_text_field(field):
    result = codes(valid_mapping(**{field: " "}))
    assert result[0] is subject.ScoringValidationCode.BLANK_REQUIRED_TEXT


def test_fixed_posture_double_classification_and_dependency_suppression():
    assert codes(valid_mapping(scoring_target_posture=1))[:2] == (
        subject.ScoringValidationCode.BLANK_REQUIRED_TEXT,
        subject.ScoringValidationCode.INVALID_FIXED_POSTURE,
    )
    result = codes(valid_mapping(scoring_artifact="bad", prediction_representation="bad", proper_score_direction_posture=1))
    assert subject.ScoringValidationCode.REPRESENTATION_MISMATCH not in result
    assert subject.ScoringValidationCode.DIRECTION_MISMATCH not in result


@pytest.mark.parametrize("artifact,representation,direction,required", [
    ("brier_score", "binary_outcome_probability", "lower_is_better", ()),
    ("log_score", "binary_outcome_probability", "lower_is_better", ("probability_boundary_policy_id",)),
    ("reliability_diagram", "binary_outcome_probability", "diagnostic_only_not_scalar_ranking", ("binning_policy_id",)),
    ("brier_decomposition", "binary_outcome_probability", "diagnostic_only_not_scalar_ranking", ("decomposition_policy_id",)),
    ("crps", "full_predictive_distribution", "lower_is_better", ()),
    ("pit_histogram", "full_predictive_distribution", "diagnostic_only_not_scalar_ranking", ("pit_treatment_policy_id",)),
    ("rank_histogram", "finite_comparable_ensemble", "diagnostic_only_not_scalar_ranking", ("tie_treatment_policy_id",)),
    ("threshold_weighted_crps", "full_predictive_distribution", "lower_is_better", ("threshold_weight_policy_id", "claim_justification_id")),
])
def test_every_artifact_policy_combination(artifact, representation, direction, required):
    changes = {"scoring_artifact": artifact, "prediction_representation": representation, "proper_score_direction_posture": direction}
    for field in required:
        changes[field] = "caller-policy"
    assert codes(valid_mapping(**changes)) == ()
    if required:
        changes[required[0]] = None
        assert subject._MISSING_POLICY_CODES[required[0]] in codes(valid_mapping(**changes))
    inapplicable = next((field for field in subject._POLICY_FIELDS if field not in required), None)
    if inapplicable:
        changes = {"scoring_artifact": artifact, "prediction_representation": representation, "proper_score_direction_posture": direction, inapplicable: "supplied"}
        for field in required:
            changes[field] = "caller-policy"
        assert codes(valid_mapping(**changes)).count(subject.ScoringValidationCode.INAPPLICABLE_POLICY_FIELDS_PRESENT) == 1


def test_tuple_boundaries_repetitions_and_order():
    assert codes(valid_mapping(supported_stratification_axes=["market_family", "market_family"])) == (subject.ScoringValidationCode.INVALID_STRATIFICATION_AXES,)
    assert codes(valid_mapping(required_baseline_types=["persistence", "climatology"])) == (subject.ScoringValidationCode.INVALID_REQUIRED_BASELINE_TYPES,)
    assert codes(valid_mapping(provenance_refs=[1, " ", 2])) == (subject.ScoringValidationCode.INVALID_PROVENANCE_REF,) * 3
    assert codes(valid_mapping(provenance_refs=[])) == (subject.ScoringValidationCode.EMPTY_PROVENANCE_REFS,)


def test_missing_dependent_keys_status_supersession_and_repeated_codes():
    mapping = valid_mapping()
    del mapping["exclusion_reason"]
    assert codes(mapping) == (subject.ScoringValidationCode.MISSING_REQUIRED_FIELD,)
    assert codes(valid_mapping(definition_status="active", exclusion_reason="why")) == (subject.ScoringValidationCode.ACTIVE_WITH_EXCLUSION_REASON,)
    assert codes(valid_mapping(definition_status="blocked", exclusion_reason=None)) == (subject.ScoringValidationCode.BLOCKED_WITHOUT_EXCLUSION_REASON,)
    assert codes(valid_mapping(supersedes_scoring_definition_id="score-1")) == (subject.ScoringValidationCode.SELF_SUPERSESSION,)
    result = codes(valid_mapping(probability_boundary_policy_id=" ", binning_policy_id=" "))
    assert result[:2] == (subject.ScoringValidationCode.BLANK_REQUIRED_TEXT,) * 2
    assert result[-1] is subject.ScoringValidationCode.INAPPLICABLE_POLICY_FIELDS_PRESENT
