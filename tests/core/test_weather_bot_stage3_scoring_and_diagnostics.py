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

# Independent literal oracles: these deliberately do not derive expectations from subject.
EXPECTED_ALL = (
    "ScoringArtifact", "ScoringPredictionRepresentation", "ScoringDefinitionStatus",
    "ScoringValidationSeverity", "ScoringValidationCode", "ScoringDiagnosticDefinition",
    "ScoringDiagnosticValidationResult", "scoring_diagnostic_definition_from_mapping",
    "validate_scoring_diagnostic_definition",
)
EXPECTED_CODES = (
    "missing_required_field", "unexpected_field", "blank_required_text",
    "invalid_scoring_artifact", "invalid_prediction_representation", "invalid_definition_status",
    "invalid_fixed_posture", "invalid_stratification_axes", "invalid_required_baseline_types",
    "empty_provenance_refs", "invalid_provenance_ref", "representation_mismatch",
    "direction_mismatch", "log_score_missing_boundary_policy",
    "reliability_missing_binning_policy", "brier_decomposition_missing_policy",
    "pit_missing_treatment_policy", "rank_missing_tie_policy",
    "threshold_weighted_crps_missing_weight_policy",
    "threshold_weighted_crps_missing_claim_justification",
    "inapplicable_policy_fields_present", "active_with_exclusion_reason",
    "blocked_without_exclusion_reason", "self_supersession",
)
EXPECTED_REQUIRED_KEYS = (
    "scoring_definition_id", "scoring_artifact", "definition_status", "definition_version",
    "method_id", "method_version", "prediction_representation", "aggregation_rule_id",
    "weighting_rule_id", "sample_support_policy_id", "uncertainty_method_id",
    "uncertainty_level_id", "supported_stratification_axes", "required_baseline_types",
    "probability_boundary_policy_id", "binning_policy_id", "decomposition_policy_id",
    "pit_treatment_policy_id", "tie_treatment_policy_id", "threshold_weight_policy_id",
    "claim_justification_id", "scoring_target_posture", "proper_score_direction_posture",
    "paired_comparison_posture", "applicability_posture", "availability_posture",
    "predeclaration_posture", "tuning_posture", "sparse_bucket_posture",
    "interpretation_posture", "market_price_posture", "scoring_execution_posture",
    "diagnostic_execution_posture", "storage_persistence_posture", "provenance_refs",
    "exclusion_reason",
)
EXPECTED_REQUIRED_TEXT = (
    "scoring_definition_id", "definition_version", "method_id", "method_version",
    "aggregation_rule_id", "weighting_rule_id", "sample_support_policy_id",
    "uncertainty_method_id", "uncertainty_level_id", "scoring_target_posture",
    "proper_score_direction_posture", "paired_comparison_posture", "applicability_posture",
    "availability_posture", "predeclaration_posture", "tuning_posture",
    "sparse_bucket_posture", "interpretation_posture", "market_price_posture",
    "scoring_execution_posture", "diagnostic_execution_posture", "storage_persistence_posture",
)
EXPECTED_NULLABLE_TEXT = (
    "probability_boundary_policy_id", "binning_policy_id", "decomposition_policy_id",
    "pit_treatment_policy_id", "tie_treatment_policy_id", "threshold_weight_policy_id",
    "claim_justification_id", "exclusion_reason", "supersedes_scoring_definition_id",
)
EXPECTED_FIXED = (
    ("scoring_target_posture", "venue_defined_settlement_outcome"),
    ("paired_comparison_posture", "same_split_fold_cutoff_eligible_records_labels_metric_aggregation_weighting_and_stratum_required"),
    ("applicability_posture", "representation_gated"),
    ("availability_posture", "point_in_time_required"),
    ("predeclaration_posture", "before_test_inspection_required"),
    ("tuning_posture", "train_or_calibration_only"),
    ("sparse_bucket_posture", "blocked_or_insufficient_not_silently_pooled"),
    ("interpretation_posture", "no_economic_edge_or_executability_inference"),
    ("market_price_posture", "not_approved_as_baseline_or_truth"),
    ("scoring_execution_posture", "not_approved"),
    ("diagnostic_execution_posture", "not_approved"),
    ("storage_persistence_posture", "not_approved"),
)
EXPECTED_AXES = (
    "market_family", "threshold_distance", "forecast_horizon", "station_source_compatibility",
    "trap_category", "season_or_regime_when_supported", "archive_layer",
)
ARTIFACT_CASES = (
    ("brier_score", "binary_outcome_probability", "lower_is_better", (), ()),
    ("log_score", "binary_outcome_probability", "lower_is_better", ("probability_boundary_policy_id",), (subject.ScoringValidationCode.LOG_SCORE_MISSING_BOUNDARY_POLICY,)),
    ("reliability_diagram", "binary_outcome_probability", "diagnostic_only_not_scalar_ranking", ("binning_policy_id",), (subject.ScoringValidationCode.RELIABILITY_MISSING_BINNING_POLICY,)),
    ("brier_decomposition", "binary_outcome_probability", "diagnostic_only_not_scalar_ranking", ("decomposition_policy_id",), (subject.ScoringValidationCode.BRIER_DECOMPOSITION_MISSING_POLICY,)),
    ("crps", "full_predictive_distribution", "lower_is_better", (), ()),
    ("pit_histogram", "full_predictive_distribution", "diagnostic_only_not_scalar_ranking", ("pit_treatment_policy_id",), (subject.ScoringValidationCode.PIT_MISSING_TREATMENT_POLICY,)),
    ("rank_histogram", "finite_comparable_ensemble", "diagnostic_only_not_scalar_ranking", ("tie_treatment_policy_id",), (subject.ScoringValidationCode.RANK_MISSING_TIE_POLICY,)),
    ("threshold_weighted_crps", "full_predictive_distribution", "lower_is_better", ("threshold_weight_policy_id", "claim_justification_id"), (subject.ScoringValidationCode.THRESHOLD_WEIGHTED_CRPS_MISSING_WEIGHT_POLICY, subject.ScoringValidationCode.THRESHOLD_WEIGHTED_CRPS_MISSING_CLAIM_JUSTIFICATION)),
)


def _definition(**changes):
    value, result = subject.scoring_diagnostic_definition_from_mapping(valid_mapping())
    assert result.codes == () and value is not None
    for name, replacement in changes.items():
        object.__setattr__(value, name, replacement)
    return value


def _direct_codes(**changes):
    return subject.validate_scoring_diagnostic_definition(_definition(**changes)).codes


def test_independent_ast_surface_imports_source_order_and_literal_enums():
    import ast
    import pathlib

    tree = ast.parse(pathlib.Path(subject.__file__).read_text(encoding="utf-8"))
    imports = []
    for node in tree.body:
        if isinstance(node, ast.ImportFrom):
            imports.append((node.module, tuple(alias.name for alias in node.names)))
        elif isinstance(node, ast.Import):
            imports.append((None, tuple(alias.name for alias in node.names)))
    assert imports == [
        ("__future__", ("annotations",)), ("collections.abc", ("Mapping",)),
        ("dataclasses", ("dataclass",)), ("enum", ("StrEnum",)),
        ("meg.weather.stage3.baseline_contracts", ("BaselineType",)),
    ]
    public = tuple(node.name for node in tree.body if isinstance(node, (ast.ClassDef, ast.FunctionDef)) and not node.name.startswith("_"))
    assert public == EXPECTED_ALL
    assert subject.__all__ == EXPECTED_ALL
    assert tuple((x.name, x.value) for x in subject.ScoringArtifact) == (
        ("BRIER_SCORE", "brier_score"), ("LOG_SCORE", "log_score"),
        ("RELIABILITY_DIAGRAM", "reliability_diagram"), ("BRIER_DECOMPOSITION", "brier_decomposition"),
        ("CRPS", "crps"), ("PIT_HISTOGRAM", "pit_histogram"),
        ("RANK_HISTOGRAM", "rank_histogram"), ("THRESHOLD_WEIGHTED_CRPS", "threshold_weighted_crps"),
    )
    assert tuple((x.name, x.value) for x in subject.ScoringPredictionRepresentation) == (
        ("BINARY_OUTCOME_PROBABILITY", "binary_outcome_probability"),
        ("FULL_PREDICTIVE_DISTRIBUTION", "full_predictive_distribution"),
        ("FINITE_COMPARABLE_ENSEMBLE", "finite_comparable_ensemble"),
    )
    assert tuple((x.name, x.value) for x in subject.ScoringDefinitionStatus) == (("ACTIVE", "active"), ("BLOCKED", "blocked"))
    assert tuple((x.name, x.value) for x in subject.ScoringValidationSeverity) == (("PASSED", "passed"), ("BLOCKED", "blocked"))
    assert tuple(x.value for x in subject.ScoringValidationCode) == EXPECTED_CODES


def test_independent_fields_signatures_annotations_defaults_and_private_literals():
    import types
    from dataclasses import MISSING

    definition_fields = fields(subject.ScoringDiagnosticDefinition)
    expected_names = EXPECTED_REQUIRED_KEYS + ("supersedes_scoring_definition_id",)
    expected_types = (
        str, subject.ScoringArtifact, subject.ScoringDefinitionStatus, str, str, str,
        subject.ScoringPredictionRepresentation, str, str, str, str, str, tuple[str, ...],
        tuple[BaselineType, ...], str | None, str | None, str | None, str | None, str | None,
        str | None, str | None, str, str, str, str, str, str, str, str, str, str, str, str,
        str, tuple[str, ...], str | None, str | None,
    )
    hints = get_type_hints(subject.ScoringDiagnosticDefinition)
    assert tuple((f.name, hints[f.name], f.default) for f in definition_fields) == tuple(
        (name, annotation, None if name == "supersedes_scoring_definition_id" else MISSING)
        for name, annotation in zip(expected_names, expected_types)
    )
    result_fields = fields(subject.ScoringDiagnosticValidationResult)
    result_hints = get_type_hints(subject.ScoringDiagnosticValidationResult)
    assert tuple((f.name, result_hints[f.name], f.default) for f in result_fields) == (
        ("severity", subject.ScoringValidationSeverity, MISSING), ("passed", bool, MISSING),
        ("codes", tuple[subject.ScoringValidationCode, ...], ()),
    )
    mapping_sig = inspect.signature(subject.scoring_diagnostic_definition_from_mapping)
    validation_sig = inspect.signature(subject.validate_scoring_diagnostic_definition)
    mapping_hints = get_type_hints(subject.scoring_diagnostic_definition_from_mapping)
    validation_hints = get_type_hints(subject.validate_scoring_diagnostic_definition)
    assert tuple(mapping_sig.parameters) == ("mapping",) and mapping_hints["mapping"] is object
    assert mapping_hints["return"] == tuple[subject.ScoringDiagnosticDefinition | None, subject.ScoringDiagnosticValidationResult]
    assert tuple(validation_sig.parameters) == ("definition",) and validation_hints == {
        "definition": subject.ScoringDiagnosticDefinition, "return": subject.ScoringDiagnosticValidationResult
    }
    assert subject._REQUIRED_MAPPING_KEYS == EXPECTED_REQUIRED_KEYS
    assert subject._OPTIONAL_MAPPING_KEYS == ("supersedes_scoring_definition_id",)
    assert subject._REQUIRED_TEXT_FIELDS == EXPECTED_REQUIRED_TEXT
    assert subject._NULLABLE_TEXT_FIELDS == EXPECTED_NULLABLE_TEXT
    assert subject._FIXED_POSTURES == EXPECTED_FIXED
    assert subject._PERMITTED_STRATIFICATION_AXES == EXPECTED_AXES
    assert subject._REQUIRED_BASELINE_TYPES == (BaselineType.CLIMATOLOGY, BaselineType.PERSISTENCE)
    expected_representation = {
        subject.ScoringArtifact.BRIER_SCORE: (subject.ScoringPredictionRepresentation.BINARY_OUTCOME_PROBABILITY, "lower_is_better"),
        subject.ScoringArtifact.LOG_SCORE: (subject.ScoringPredictionRepresentation.BINARY_OUTCOME_PROBABILITY, "lower_is_better"),
        subject.ScoringArtifact.RELIABILITY_DIAGRAM: (subject.ScoringPredictionRepresentation.BINARY_OUTCOME_PROBABILITY, "diagnostic_only_not_scalar_ranking"),
        subject.ScoringArtifact.BRIER_DECOMPOSITION: (subject.ScoringPredictionRepresentation.BINARY_OUTCOME_PROBABILITY, "diagnostic_only_not_scalar_ranking"),
        subject.ScoringArtifact.CRPS: (subject.ScoringPredictionRepresentation.FULL_PREDICTIVE_DISTRIBUTION, "lower_is_better"),
        subject.ScoringArtifact.PIT_HISTOGRAM: (subject.ScoringPredictionRepresentation.FULL_PREDICTIVE_DISTRIBUTION, "diagnostic_only_not_scalar_ranking"),
        subject.ScoringArtifact.RANK_HISTOGRAM: (subject.ScoringPredictionRepresentation.FINITE_COMPARABLE_ENSEMBLE, "diagnostic_only_not_scalar_ranking"),
        subject.ScoringArtifact.THRESHOLD_WEIGHTED_CRPS: (subject.ScoringPredictionRepresentation.FULL_PREDICTIVE_DISTRIBUTION, "lower_is_better"),
    }
    assert subject._REPRESENTATION_MATRIX == expected_representation
    assert subject._POLICY_FIELDS == ("probability_boundary_policy_id", "binning_policy_id", "decomposition_policy_id", "pit_treatment_policy_id", "tie_treatment_policy_id", "threshold_weight_policy_id", "claim_justification_id")
    assert subject._ARTIFACT_POLICY_MATRIX == {subject.ScoringArtifact(value): required for value, _, _, required, _ in ARTIFACT_CASES}
    assert subject._MISSING_POLICY_CODES == {
        "probability_boundary_policy_id": subject.ScoringValidationCode.LOG_SCORE_MISSING_BOUNDARY_POLICY,
        "binning_policy_id": subject.ScoringValidationCode.RELIABILITY_MISSING_BINNING_POLICY,
        "decomposition_policy_id": subject.ScoringValidationCode.BRIER_DECOMPOSITION_MISSING_POLICY,
        "pit_treatment_policy_id": subject.ScoringValidationCode.PIT_MISSING_TREATMENT_POLICY,
        "tie_treatment_policy_id": subject.ScoringValidationCode.RANK_MISSING_TIE_POLICY,
        "threshold_weight_policy_id": subject.ScoringValidationCode.THRESHOLD_WEIGHTED_CRPS_MISSING_WEIGHT_POLICY,
        "claim_justification_id": subject.ScoringValidationCode.THRESHOLD_WEIGHTED_CRPS_MISSING_CLAIM_JUSTIFICATION,
    }


class _ItemsMapping(__import__("collections.abc").abc.Mapping):
    def __init__(self, items_or_error): self.items_or_error = items_or_error
    def __getitem__(self, key): raise KeyError(key)
    def __iter__(self): return iter(())
    def __len__(self): return 0
    def items(self):
        if isinstance(self.items_or_error, Exception): raise self.items_or_error
        return self.items_or_error


@pytest.mark.parametrize("root", [None, [], object(), _ItemsMapping(RuntimeError("items")), _ItemsMapping(iter([(1, 2), RuntimeError("unused")])), _ItemsMapping([(1,)]), _ItemsMapping([(1, 2, 3)]), _ItemsMapping([1])])
def test_hostile_mapping_fail_closed_matrix(root):
    definition, result = subject.scoring_diagnostic_definition_from_mapping(root)
    assert definition is None
    assert (result.severity, result.passed, result.codes) == (
        subject.ScoringValidationSeverity.BLOCKED, False,
        (subject.ScoringValidationCode.MISSING_REQUIRED_FIELD,) * 36,
    )


def test_hostile_iteration_unpack_and_baseexception_boundaries():
    class BrokenIterator:
        def __iter__(self): return self
        def __next__(self): raise RuntimeError("iteration")
    assert codes(_ItemsMapping(BrokenIterator())) == (subject.ScoringValidationCode.MISSING_REQUIRED_FIELD,) * 36

    class BrokenItem:
        def __iter__(self): raise RuntimeError("unpack")
    assert codes(_ItemsMapping([BrokenItem()])) == (subject.ScoringValidationCode.MISSING_REQUIRED_FIELD,) * 36

    class FatalMapping(_ItemsMapping):
        def items(self): raise KeyboardInterrupt
    with pytest.raises(KeyboardInterrupt):
        subject.scoring_diagnostic_definition_from_mapping(FatalMapping(None))


@pytest.mark.parametrize("missing", EXPECTED_REQUIRED_KEYS)
def test_each_required_key_missing_has_complete_tuple(missing):
    mapping = valid_mapping(); del mapping[missing]
    expected = (subject.ScoringValidationCode.MISSING_REQUIRED_FIELD,)
    assert subject.scoring_diagnostic_definition_from_mapping(mapping) == (None, subject.ScoringDiagnosticValidationResult(subject.ScoringValidationSeverity.BLOCKED, False, expected))


def test_shape_order_aggregation_and_no_partial_definition():
    class Text(str): pass
    mapping = valid_mapping(supported_stratification_axes=("bad-axis",))
    del mapping["scoring_definition_id"]; del mapping["method_id"]
    mapping["zeta"] = 1; mapping["alpha"] = 2; mapping[Text("method_id")] = "method"; mapping[7] = 1; mapping[(1, 2)] = 2
    definition, result = subject.scoring_diagnostic_definition_from_mapping(mapping)
    assert definition is None
    assert result.codes == (
        subject.ScoringValidationCode.MISSING_REQUIRED_FIELD,
        subject.ScoringValidationCode.MISSING_REQUIRED_FIELD,
        subject.ScoringValidationCode.UNEXPECTED_FIELD,
        subject.ScoringValidationCode.UNEXPECTED_FIELD,
        subject.ScoringValidationCode.UNEXPECTED_FIELD,
        subject.ScoringValidationCode.UNEXPECTED_FIELD,
        subject.ScoringValidationCode.UNEXPECTED_FIELD,
        subject.ScoringValidationCode.INVALID_STRATIFICATION_AXES,
    )


class _Text(str): pass


@pytest.mark.parametrize("field", EXPECTED_REQUIRED_TEXT)
@pytest.mark.parametrize("bad", ["", 3, _Text("valid")])
def test_required_text_complete_matrix(field, bad):
    result = codes(valid_mapping(**{field: bad}))
    expected = [subject.ScoringValidationCode.BLANK_REQUIRED_TEXT]
    fixed = dict(EXPECTED_FIXED)
    if field in fixed: expected.append(subject.ScoringValidationCode.INVALID_FIXED_POSTURE)
    if field == "proper_score_direction_posture" and bad == "": pass
    assert result == tuple(expected)


@pytest.mark.parametrize("field", EXPECTED_NULLABLE_TEXT)
def test_nullable_text_complete_matrix(field):
    assert subject.ScoringValidationCode.BLANK_REQUIRED_TEXT not in codes(valid_mapping(**{field: None}))
    valid_result = codes(valid_mapping(**{field: "valid"}))
    assert subject.ScoringValidationCode.BLANK_REQUIRED_TEXT not in valid_result
    for bad in ("", 4, _Text("valid")):
        assert codes(valid_mapping(**{field: bad}))[0] is subject.ScoringValidationCode.BLANK_REQUIRED_TEXT


@pytest.mark.parametrize("field,expected", EXPECTED_FIXED)
def test_every_fixed_posture_complete_matrix(field, expected):
    assert codes(valid_mapping(**{field: expected})) == ()
    assert codes(valid_mapping(**{field: "wrong"})) == (subject.ScoringValidationCode.INVALID_FIXED_POSTURE,)
    for bad in ("", 4, _Text(expected)):
        assert codes(valid_mapping(**{field: bad})) == (subject.ScoringValidationCode.BLANK_REQUIRED_TEXT, subject.ScoringValidationCode.INVALID_FIXED_POSTURE)


@pytest.mark.parametrize("artifact,representation,direction,required,missing_codes", ARTIFACT_CASES)
def test_representation_direction_complete_matrix(artifact, representation, direction, required, missing_codes):
    policies = {field: "policy" for field in required}
    base = dict(scoring_artifact=artifact, prediction_representation=representation, proper_score_direction_posture=direction, **policies)
    assert codes(valid_mapping(**base)) == ()
    wrong_rep = "finite_comparable_ensemble" if representation != "finite_comparable_ensemble" else "binary_outcome_probability"
    assert codes(valid_mapping(**(base | {"prediction_representation": wrong_rep}))) == (subject.ScoringValidationCode.REPRESENTATION_MISMATCH,)
    assert codes(valid_mapping(**(base | {"proper_score_direction_posture": "wrong"}))) == (subject.ScoringValidationCode.DIRECTION_MISMATCH,)
    assert codes(valid_mapping(**(base | {"prediction_representation": wrong_rep, "proper_score_direction_posture": "wrong"}))) == (subject.ScoringValidationCode.REPRESENTATION_MISMATCH, subject.ScoringValidationCode.DIRECTION_MISMATCH)
    assert subject.ScoringValidationCode.REPRESENTATION_MISMATCH not in codes(valid_mapping(**(base | {"scoring_artifact": "invalid"})))
    invalid_rep = codes(valid_mapping(**(base | {"prediction_representation": "invalid"})))
    assert invalid_rep == (subject.ScoringValidationCode.INVALID_PREDICTION_REPRESENTATION,)
    assert subject.ScoringValidationCode.DIRECTION_MISMATCH not in codes(valid_mapping(**(base | {"proper_score_direction_posture": 1})))


@pytest.mark.parametrize("artifact,representation,direction,required,missing_codes", ARTIFACT_CASES)
def test_artifact_policy_exhaustive_matrix(artifact, representation, direction, required, missing_codes):
    base = {"scoring_artifact": artifact, "prediction_representation": representation, "proper_score_direction_posture": direction}
    base.update({field: "policy" for field in required})
    assert codes(valid_mapping(**base)) == ()
    for index, field in enumerate(required):
        mapping = valid_mapping(**base); del mapping[field]
        assert codes(mapping) == (subject.ScoringValidationCode.MISSING_REQUIRED_FIELD,)
        expected_code = missing_codes[index]
        assert codes(valid_mapping(**(base | {field: None}))) == (expected_code,)
        for bad in ("", 8, _Text("policy")):
            assert codes(valid_mapping(**(base | {field: bad}))) == (subject.ScoringValidationCode.BLANK_REQUIRED_TEXT, expected_code)
    inapplicable = [field for field in ("probability_boundary_policy_id", "binning_policy_id", "decomposition_policy_id", "pit_treatment_policy_id", "tie_treatment_policy_id", "threshold_weight_policy_id", "claim_justification_id") if field not in required]
    for field in inapplicable:
        assert codes(valid_mapping(**(base | {field: "supplied"}))) == (subject.ScoringValidationCode.INAPPLICABLE_POLICY_FIELDS_PRESENT,)
    if len(inapplicable) > 1:
        assert codes(valid_mapping(**(base | {inapplicable[0]: "a", inapplicable[1]: "b"}))) == (subject.ScoringValidationCode.INAPPLICABLE_POLICY_FIELDS_PRESENT,)
    invalid = codes(valid_mapping(**(base | {"scoring_artifact": "invalid", inapplicable[0]: "supplied"})))
    assert invalid == (subject.ScoringValidationCode.INVALID_SCORING_ARTIFACT,)


@pytest.mark.parametrize("value", [("market_family",), ["market_family"], (), EXPECTED_AXES, ("archive_layer", "market_family")])
def test_stratification_mapping_valid_preserves_values(value):
    original = value.copy() if isinstance(value, list) else value
    definition, result = subject.scoring_diagnostic_definition_from_mapping(valid_mapping(supported_stratification_axes=value))
    assert result.codes == () and definition is not None
    assert definition.supported_stratification_axes == tuple(value)
    assert value == original


@pytest.mark.parametrize("bad", [["market_family"], ("market_family", "market_family"), ("unsupported",), ("",), (3,), (_Text("market_family"),), {"market_family"}])
def test_stratification_direct_and_mapping_invalid_matrix(bad):
    direct = _direct_codes(supported_stratification_axes=bad)
    assert direct == (subject.ScoringValidationCode.INVALID_STRATIFICATION_AXES,)
    if type(bad) is not list or bad == ["market_family"]:
        mapped = codes(valid_mapping(supported_stratification_axes=bad))
        expected = () if bad == ["market_family"] else (subject.ScoringValidationCode.INVALID_STRATIFICATION_AXES,)
        assert mapped == expected


@pytest.mark.parametrize("bad", [
    (BaselineType.PERSISTENCE, BaselineType.CLIMATOLOGY), (BaselineType.CLIMATOLOGY,),
    (BaselineType.CLIMATOLOGY, BaselineType.CLIMATOLOGY),
    (BaselineType.CLIMATOLOGY, BaselineType.PERSISTENCE, BaselineType.CLIMATOLOGY),
    (_Text("climatology"), "persistence"), ("invalid", "persistence"), {"climatology", "persistence"},
])
def test_baseline_invalid_matrix(bad):
    assert codes(valid_mapping(required_baseline_types=bad)) == (subject.ScoringValidationCode.INVALID_REQUIRED_BASELINE_TYPES,)
    assert _direct_codes(required_baseline_types=bad) == (subject.ScoringValidationCode.INVALID_REQUIRED_BASELINE_TYPES,)


def test_baseline_mapping_adaptation_direct_tuple_only_and_unrelated_enum():
    class Other(StrEnum): CLIMATOLOGY = "climatology"
    for value in (["climatology", "persistence"], ("climatology", "persistence"), (BaselineType.CLIMATOLOGY, BaselineType.PERSISTENCE)):
        definition, result = subject.scoring_diagnostic_definition_from_mapping(valid_mapping(required_baseline_types=value))
        assert result.codes == () and definition.required_baseline_types == (BaselineType.CLIMATOLOGY, BaselineType.PERSISTENCE)
    assert _direct_codes(required_baseline_types=[BaselineType.CLIMATOLOGY, BaselineType.PERSISTENCE]) == (subject.ScoringValidationCode.INVALID_REQUIRED_BASELINE_TYPES,)
    assert codes(valid_mapping(required_baseline_types=(Other.CLIMATOLOGY, BaselineType.PERSISTENCE))) == (subject.ScoringValidationCode.INVALID_REQUIRED_BASELINE_TYPES,)


@pytest.mark.parametrize("bad,expected", [
    ([], (subject.ScoringValidationCode.EMPTY_PROVENANCE_REFS,)),
    ({"ref"}, (subject.ScoringValidationCode.INVALID_PROVENANCE_REF,)),
    ([""], (subject.ScoringValidationCode.INVALID_PROVENANCE_REF,)),
    ([4], (subject.ScoringValidationCode.INVALID_PROVENANCE_REF,)),
    ([_Text("ref")], (subject.ScoringValidationCode.INVALID_PROVENANCE_REF,)),
    (["", 4, _Text("ref")], (subject.ScoringValidationCode.INVALID_PROVENANCE_REF,) * 3),
])
def test_provenance_invalid_complete_matrix(bad, expected):
    assert codes(valid_mapping(provenance_refs=bad)) == expected
    assert subject.ScoringValidationCode.BLANK_REQUIRED_TEXT not in expected


def test_provenance_adaptation_preservation_and_direct_tuple_only():
    supplied = ["z", "a", "z"]
    definition, result = subject.scoring_diagnostic_definition_from_mapping(valid_mapping(provenance_refs=supplied))
    assert result.codes == () and definition.provenance_refs == ("z", "a", "z") and supplied == ["z", "a", "z"]
    assert _direct_codes(provenance_refs=["ref"]) == (subject.ScoringValidationCode.INVALID_PROVENANCE_REF,)
    assert _direct_codes(provenance_refs=("ref", "ref")) == ()


def test_status_and_supersession_complete_matrix():
    assert codes(valid_mapping(definition_status="active", exclusion_reason=None)) == ()
    assert codes(valid_mapping(definition_status="active", exclusion_reason="reason")) == (subject.ScoringValidationCode.ACTIVE_WITH_EXCLUSION_REASON,)
    for bad in ("", 4, _Text("reason")):
        assert codes(valid_mapping(definition_status="active", exclusion_reason=bad)) == (subject.ScoringValidationCode.BLANK_REQUIRED_TEXT, subject.ScoringValidationCode.ACTIVE_WITH_EXCLUSION_REASON)
    assert codes(valid_mapping(definition_status="blocked", exclusion_reason="reason")) == ()
    assert codes(valid_mapping(definition_status="blocked", exclusion_reason=None)) == (subject.ScoringValidationCode.BLOCKED_WITHOUT_EXCLUSION_REASON,)
    for bad in ("", 4, _Text("reason")):
        assert codes(valid_mapping(definition_status="blocked", exclusion_reason=bad)) == (subject.ScoringValidationCode.BLANK_REQUIRED_TEXT, subject.ScoringValidationCode.BLOCKED_WITHOUT_EXCLUSION_REASON)
    mapping = valid_mapping(); del mapping["exclusion_reason"]
    assert codes(mapping) == (subject.ScoringValidationCode.MISSING_REQUIRED_FIELD,)
    assert codes(valid_mapping(definition_status="invalid", exclusion_reason=None)) == (subject.ScoringValidationCode.INVALID_DEFINITION_STATUS,)
    for supersedes, expected in ((None, ()), ("different", ()), ("score-1", (subject.ScoringValidationCode.SELF_SUPERSESSION,)), ("", (subject.ScoringValidationCode.BLANK_REQUIRED_TEXT,)), (4, (subject.ScoringValidationCode.BLANK_REQUIRED_TEXT,)), (_Text("score-1"), (subject.ScoringValidationCode.BLANK_REQUIRED_TEXT,))):
        assert codes(valid_mapping(supersedes_scoring_definition_id=supersedes)) == expected


def test_combined_full_order_repetition_and_all_groups():
    mapping = valid_mapping(
        scoring_definition_id="", scoring_artifact="log_score", definition_status="blocked",
        prediction_representation="full_predictive_distribution", scoring_target_posture="wrong",
        proper_score_direction_posture="wrong", supported_stratification_axes=("bad",),
        required_baseline_types=(BaselineType.PERSISTENCE,), provenance_refs=("", 4),
        probability_boundary_policy_id="", binning_policy_id="supplied", exclusion_reason=None,
        supersedes_scoring_definition_id="",
    )
    mapping["unexpected"] = True
    assert codes(mapping) == (
        subject.ScoringValidationCode.UNEXPECTED_FIELD,
        subject.ScoringValidationCode.BLANK_REQUIRED_TEXT,
        subject.ScoringValidationCode.BLANK_REQUIRED_TEXT,
        subject.ScoringValidationCode.BLANK_REQUIRED_TEXT,
        subject.ScoringValidationCode.INVALID_FIXED_POSTURE,
        subject.ScoringValidationCode.INVALID_STRATIFICATION_AXES,
        subject.ScoringValidationCode.INVALID_REQUIRED_BASELINE_TYPES,
        subject.ScoringValidationCode.INVALID_PROVENANCE_REF,
        subject.ScoringValidationCode.INVALID_PROVENANCE_REF,
        subject.ScoringValidationCode.REPRESENTATION_MISMATCH,
        subject.ScoringValidationCode.DIRECTION_MISMATCH,
        subject.ScoringValidationCode.LOG_SCORE_MISSING_BOUNDARY_POLICY,
        subject.ScoringValidationCode.INAPPLICABLE_POLICY_FIELDS_PRESENT,
        subject.ScoringValidationCode.BLOCKED_WITHOUT_EXCLUSION_REASON,
    )


def test_result_tuple_coercion_caller_preservation_determinism_and_purity_ast():
    import ast
    import pathlib

    supplied_codes = [subject.ScoringValidationCode.UNEXPECTED_FIELD]
    result = subject.ScoringDiagnosticValidationResult(subject.ScoringValidationSeverity.PASSED, True, supplied_codes)
    supplied_codes.append(subject.ScoringValidationCode.SELF_SUPERSESSION)
    assert (result.severity, result.passed, result.codes) == (subject.ScoringValidationSeverity.BLOCKED, False, (subject.ScoringValidationCode.UNEXPECTED_FIELD,))
    passed = subject.ScoringDiagnosticValidationResult(subject.ScoringValidationSeverity.BLOCKED, False, [])
    assert (passed.severity, passed.passed, passed.codes) == (subject.ScoringValidationSeverity.PASSED, True, ())
    mapping = valid_mapping(provenance_refs=["b", "a", "b"], supported_stratification_axes=["archive_layer", "market_family"])
    before = repr(mapping)
    assert subject.scoring_diagnostic_definition_from_mapping(mapping) == subject.scoring_diagnostic_definition_from_mapping(mapping)
    assert repr(mapping) == before
    tree = ast.parse(pathlib.Path(subject.__file__).read_text(encoding="utf-8"))
    forbidden_import_roots = {"os", "sys", "pathlib", "subprocess", "socket", "time", "datetime", "requests", "http", "sqlite3", "duckdb"}
    roots = {node.module.split(".")[0] for node in ast.walk(tree) if isinstance(node, ast.ImportFrom) and node.module}
    roots |= {alias.name.split(".")[0] for node in ast.walk(tree) if isinstance(node, ast.Import) for alias in node.names}
    assert not roots & forbidden_import_roots
    forbidden_calls = {"open", "exec", "eval", "compile", "__import__", "system", "popen", "run", "check_call", "check_output", "getenv"}
    calls = {node.func.id for node in ast.walk(tree) if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)}
    assert not calls & forbidden_calls
