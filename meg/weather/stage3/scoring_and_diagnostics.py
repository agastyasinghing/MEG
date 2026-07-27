"""Immutable Stage 3 scoring/diagnostic definitions and pure validation."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from enum import StrEnum

from meg.weather.stage3.baseline_contracts import BaselineType

__all__ = (
    "ScoringArtifact",
    "ScoringPredictionRepresentation",
    "ScoringDefinitionStatus",
    "ScoringValidationSeverity",
    "ScoringValidationCode",
    "ScoringDiagnosticDefinition",
    "ScoringDiagnosticValidationResult",
    "scoring_diagnostic_definition_from_mapping",
    "validate_scoring_diagnostic_definition",
)


class ScoringArtifact(StrEnum):
    BRIER_SCORE = "brier_score"
    LOG_SCORE = "log_score"
    RELIABILITY_DIAGRAM = "reliability_diagram"
    BRIER_DECOMPOSITION = "brier_decomposition"
    CRPS = "crps"
    PIT_HISTOGRAM = "pit_histogram"
    RANK_HISTOGRAM = "rank_histogram"
    THRESHOLD_WEIGHTED_CRPS = "threshold_weighted_crps"


class ScoringPredictionRepresentation(StrEnum):
    BINARY_OUTCOME_PROBABILITY = "binary_outcome_probability"
    FULL_PREDICTIVE_DISTRIBUTION = "full_predictive_distribution"
    FINITE_COMPARABLE_ENSEMBLE = "finite_comparable_ensemble"


class ScoringDefinitionStatus(StrEnum):
    ACTIVE = "active"
    BLOCKED = "blocked"


class ScoringValidationSeverity(StrEnum):
    PASSED = "passed"
    BLOCKED = "blocked"


class ScoringValidationCode(StrEnum):
    MISSING_REQUIRED_FIELD = "missing_required_field"
    UNEXPECTED_FIELD = "unexpected_field"
    BLANK_REQUIRED_TEXT = "blank_required_text"
    INVALID_SCORING_ARTIFACT = "invalid_scoring_artifact"
    INVALID_PREDICTION_REPRESENTATION = "invalid_prediction_representation"
    INVALID_DEFINITION_STATUS = "invalid_definition_status"
    INVALID_FIXED_POSTURE = "invalid_fixed_posture"
    INVALID_STRATIFICATION_AXES = "invalid_stratification_axes"
    INVALID_REQUIRED_BASELINE_TYPES = "invalid_required_baseline_types"
    EMPTY_PROVENANCE_REFS = "empty_provenance_refs"
    INVALID_PROVENANCE_REF = "invalid_provenance_ref"
    REPRESENTATION_MISMATCH = "representation_mismatch"
    DIRECTION_MISMATCH = "direction_mismatch"
    LOG_SCORE_MISSING_BOUNDARY_POLICY = "log_score_missing_boundary_policy"
    RELIABILITY_MISSING_BINNING_POLICY = "reliability_missing_binning_policy"
    BRIER_DECOMPOSITION_MISSING_POLICY = "brier_decomposition_missing_policy"
    PIT_MISSING_TREATMENT_POLICY = "pit_missing_treatment_policy"
    RANK_MISSING_TIE_POLICY = "rank_missing_tie_policy"
    THRESHOLD_WEIGHTED_CRPS_MISSING_WEIGHT_POLICY = "threshold_weighted_crps_missing_weight_policy"
    THRESHOLD_WEIGHTED_CRPS_MISSING_CLAIM_JUSTIFICATION = "threshold_weighted_crps_missing_claim_justification"
    INAPPLICABLE_POLICY_FIELDS_PRESENT = "inapplicable_policy_fields_present"
    ACTIVE_WITH_EXCLUSION_REASON = "active_with_exclusion_reason"
    BLOCKED_WITHOUT_EXCLUSION_REASON = "blocked_without_exclusion_reason"
    SELF_SUPERSESSION = "self_supersession"


@dataclass(frozen=True)
class ScoringDiagnosticDefinition:
    scoring_definition_id: str
    scoring_artifact: ScoringArtifact
    definition_status: ScoringDefinitionStatus
    definition_version: str
    method_id: str
    method_version: str
    prediction_representation: ScoringPredictionRepresentation
    aggregation_rule_id: str
    weighting_rule_id: str
    sample_support_policy_id: str
    uncertainty_method_id: str
    uncertainty_level_id: str
    supported_stratification_axes: tuple[str, ...]
    required_baseline_types: tuple[BaselineType, ...]
    probability_boundary_policy_id: str | None
    binning_policy_id: str | None
    decomposition_policy_id: str | None
    pit_treatment_policy_id: str | None
    tie_treatment_policy_id: str | None
    threshold_weight_policy_id: str | None
    claim_justification_id: str | None
    scoring_target_posture: str
    proper_score_direction_posture: str
    paired_comparison_posture: str
    applicability_posture: str
    availability_posture: str
    predeclaration_posture: str
    tuning_posture: str
    sparse_bucket_posture: str
    interpretation_posture: str
    market_price_posture: str
    scoring_execution_posture: str
    diagnostic_execution_posture: str
    storage_persistence_posture: str
    provenance_refs: tuple[str, ...]
    exclusion_reason: str | None
    supersedes_scoring_definition_id: str | None = None


@dataclass(frozen=True)
class ScoringDiagnosticValidationResult:
    severity: ScoringValidationSeverity
    passed: bool
    codes: tuple[ScoringValidationCode, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "codes", tuple(self.codes))
        if self.codes:
            object.__setattr__(self, "severity", ScoringValidationSeverity.BLOCKED)
            object.__setattr__(self, "passed", False)
        else:
            object.__setattr__(self, "severity", ScoringValidationSeverity.PASSED)
            object.__setattr__(self, "passed", True)
            object.__setattr__(self, "codes", ())


_REQUIRED_MAPPING_KEYS = (
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
_OPTIONAL_MAPPING_KEYS = ("supersedes_scoring_definition_id",)
_REQUIRED_TEXT_FIELDS = (
    "scoring_definition_id", "definition_version", "method_id", "method_version",
    "aggregation_rule_id", "weighting_rule_id", "sample_support_policy_id",
    "uncertainty_method_id", "uncertainty_level_id", "scoring_target_posture",
    "proper_score_direction_posture", "paired_comparison_posture", "applicability_posture",
    "availability_posture", "predeclaration_posture", "tuning_posture",
    "sparse_bucket_posture", "interpretation_posture", "market_price_posture",
    "scoring_execution_posture", "diagnostic_execution_posture", "storage_persistence_posture",
)
_NULLABLE_TEXT_FIELDS = (
    "probability_boundary_policy_id", "binning_policy_id", "decomposition_policy_id",
    "pit_treatment_policy_id", "tie_treatment_policy_id", "threshold_weight_policy_id",
    "claim_justification_id", "exclusion_reason", "supersedes_scoring_definition_id",
)
_FIXED_POSTURES = (
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
_PERMITTED_STRATIFICATION_AXES = (
    "market_family", "threshold_distance", "forecast_horizon", "station_source_compatibility",
    "trap_category", "season_or_regime_when_supported", "archive_layer",
)
_REQUIRED_BASELINE_TYPES = (BaselineType.CLIMATOLOGY, BaselineType.PERSISTENCE)
_REPRESENTATION_MATRIX = {
    ScoringArtifact.BRIER_SCORE: (ScoringPredictionRepresentation.BINARY_OUTCOME_PROBABILITY, "lower_is_better"),
    ScoringArtifact.LOG_SCORE: (ScoringPredictionRepresentation.BINARY_OUTCOME_PROBABILITY, "lower_is_better"),
    ScoringArtifact.RELIABILITY_DIAGRAM: (ScoringPredictionRepresentation.BINARY_OUTCOME_PROBABILITY, "diagnostic_only_not_scalar_ranking"),
    ScoringArtifact.BRIER_DECOMPOSITION: (ScoringPredictionRepresentation.BINARY_OUTCOME_PROBABILITY, "diagnostic_only_not_scalar_ranking"),
    ScoringArtifact.CRPS: (ScoringPredictionRepresentation.FULL_PREDICTIVE_DISTRIBUTION, "lower_is_better"),
    ScoringArtifact.PIT_HISTOGRAM: (ScoringPredictionRepresentation.FULL_PREDICTIVE_DISTRIBUTION, "diagnostic_only_not_scalar_ranking"),
    ScoringArtifact.RANK_HISTOGRAM: (ScoringPredictionRepresentation.FINITE_COMPARABLE_ENSEMBLE, "diagnostic_only_not_scalar_ranking"),
    ScoringArtifact.THRESHOLD_WEIGHTED_CRPS: (ScoringPredictionRepresentation.FULL_PREDICTIVE_DISTRIBUTION, "lower_is_better"),
}
_POLICY_FIELDS = (
    "probability_boundary_policy_id", "binning_policy_id", "decomposition_policy_id",
    "pit_treatment_policy_id", "tie_treatment_policy_id", "threshold_weight_policy_id",
    "claim_justification_id",
)
_ARTIFACT_POLICY_MATRIX = {
    ScoringArtifact.BRIER_SCORE: (),
    ScoringArtifact.LOG_SCORE: ("probability_boundary_policy_id",),
    ScoringArtifact.RELIABILITY_DIAGRAM: ("binning_policy_id",),
    ScoringArtifact.BRIER_DECOMPOSITION: ("decomposition_policy_id",),
    ScoringArtifact.CRPS: (),
    ScoringArtifact.PIT_HISTOGRAM: ("pit_treatment_policy_id",),
    ScoringArtifact.RANK_HISTOGRAM: ("tie_treatment_policy_id",),
    ScoringArtifact.THRESHOLD_WEIGHTED_CRPS: ("threshold_weight_policy_id", "claim_justification_id"),
}
_MISSING_POLICY_CODES = {
    "probability_boundary_policy_id": ScoringValidationCode.LOG_SCORE_MISSING_BOUNDARY_POLICY,
    "binning_policy_id": ScoringValidationCode.RELIABILITY_MISSING_BINNING_POLICY,
    "decomposition_policy_id": ScoringValidationCode.BRIER_DECOMPOSITION_MISSING_POLICY,
    "pit_treatment_policy_id": ScoringValidationCode.PIT_MISSING_TREATMENT_POLICY,
    "tie_treatment_policy_id": ScoringValidationCode.RANK_MISSING_TIE_POLICY,
    "threshold_weight_policy_id": ScoringValidationCode.THRESHOLD_WEIGHTED_CRPS_MISSING_WEIGHT_POLICY,
    "claim_justification_id": ScoringValidationCode.THRESHOLD_WEIGHTED_CRPS_MISSING_CLAIM_JUSTIFICATION,
}


def _result(codes: list[ScoringValidationCode] | tuple[ScoringValidationCode, ...]) -> ScoringDiagnosticValidationResult:
    values = tuple(codes)
    return ScoringDiagnosticValidationResult(ScoringValidationSeverity.BLOCKED, False, values)


def _missing_result() -> ScoringDiagnosticValidationResult:
    return _result((ScoringValidationCode.MISSING_REQUIRED_FIELD,) * 36)


def _valid_text(value: object) -> bool:
    return type(value) is str and bool(value.strip())


def _validate(values: Mapping[str, object], present: set[str]) -> list[ScoringValidationCode]:
    codes: list[ScoringValidationCode] = []
    for field in _REQUIRED_TEXT_FIELDS:
        if field in present and not _valid_text(values[field]):
            codes.append(ScoringValidationCode.BLANK_REQUIRED_TEXT)
    for field in _NULLABLE_TEXT_FIELDS:
        if field in present and values[field] is not None and not _valid_text(values[field]):
            codes.append(ScoringValidationCode.BLANK_REQUIRED_TEXT)

    artifact = values.get("scoring_artifact")
    valid_artifact = type(artifact) is ScoringArtifact
    if "scoring_artifact" in present and not valid_artifact:
        codes.append(ScoringValidationCode.INVALID_SCORING_ARTIFACT)
    representation = values.get("prediction_representation")
    valid_representation = type(representation) is ScoringPredictionRepresentation
    if "prediction_representation" in present and not valid_representation:
        codes.append(ScoringValidationCode.INVALID_PREDICTION_REPRESENTATION)
    status = values.get("definition_status")
    valid_status = type(status) is ScoringDefinitionStatus
    if "definition_status" in present and not valid_status:
        codes.append(ScoringValidationCode.INVALID_DEFINITION_STATUS)

    for field, expected in _FIXED_POSTURES:
        if field in present and (type(values[field]) is not str or values[field] != expected):
            codes.append(ScoringValidationCode.INVALID_FIXED_POSTURE)

    if "supported_stratification_axes" in present:
        axes = values["supported_stratification_axes"]
        valid_axes = type(axes) is tuple
        if valid_axes:
            valid_axes = all(_valid_text(axis) and axis in _PERMITTED_STRATIFICATION_AXES for axis in axes)
            valid_axes = valid_axes and len(set(axes)) == len(axes)
        if not valid_axes:
            codes.append(ScoringValidationCode.INVALID_STRATIFICATION_AXES)

    if "required_baseline_types" in present:
        baseline_types = values["required_baseline_types"]
        if type(baseline_types) is not tuple or len(baseline_types) != 2 or any(
            type(value) is not BaselineType for value in baseline_types
        ) or baseline_types != _REQUIRED_BASELINE_TYPES:
            codes.append(ScoringValidationCode.INVALID_REQUIRED_BASELINE_TYPES)

    if "provenance_refs" in present:
        refs = values["provenance_refs"]
        if type(refs) is not tuple:
            codes.append(ScoringValidationCode.INVALID_PROVENANCE_REF)
        elif not refs:
            codes.append(ScoringValidationCode.EMPTY_PROVENANCE_REFS)
        else:
            for ref in refs:
                if not _valid_text(ref):
                    codes.append(ScoringValidationCode.INVALID_PROVENANCE_REF)

    if valid_artifact and valid_representation and representation is not _REPRESENTATION_MATRIX[artifact][0]:
        codes.append(ScoringValidationCode.REPRESENTATION_MISMATCH)
    if valid_artifact and "proper_score_direction_posture" in present and _valid_text(values["proper_score_direction_posture"]):
        if values["proper_score_direction_posture"] != _REPRESENTATION_MATRIX[artifact][1]:
            codes.append(ScoringValidationCode.DIRECTION_MISMATCH)

    if valid_artifact:
        required_policies = _ARTIFACT_POLICY_MATRIX[artifact]
        for field in required_policies:
            if field in present and not _valid_text(values[field]):
                codes.append(_MISSING_POLICY_CODES[field])
        if any(field in present and values[field] is not None for field in _POLICY_FIELDS if field not in required_policies):
            codes.append(ScoringValidationCode.INAPPLICABLE_POLICY_FIELDS_PRESENT)

    if valid_status and "exclusion_reason" in present:
        exclusion = values["exclusion_reason"]
        if status is ScoringDefinitionStatus.ACTIVE and exclusion is not None:
            codes.append(ScoringValidationCode.ACTIVE_WITH_EXCLUSION_REASON)
        elif status is ScoringDefinitionStatus.BLOCKED and not _valid_text(exclusion):
            codes.append(ScoringValidationCode.BLOCKED_WITHOUT_EXCLUSION_REASON)

    if "scoring_definition_id" in present and "supersedes_scoring_definition_id" in present:
        identity = values["scoring_definition_id"]
        supersedes = values["supersedes_scoring_definition_id"]
        if _valid_text(identity) and _valid_text(supersedes) and identity == supersedes:
            codes.append(ScoringValidationCode.SELF_SUPERSESSION)
    return codes


def scoring_diagnostic_definition_from_mapping(
    mapping: object,
) -> tuple[
    ScoringDiagnosticDefinition | None,
    ScoringDiagnosticValidationResult,
]:
    if not isinstance(mapping, Mapping):
        return None, _missing_result()
    try:
        items = list(mapping.items())
        values: dict[str, object] = {}
        unexpected_strings: list[str] = []
        unexpected_other: list[object] = []
        allowed = _REQUIRED_MAPPING_KEYS + _OPTIONAL_MAPPING_KEYS
        for item in items:
            key, value = item
            if type(key) is str and key in allowed:
                values[key] = value
            elif type(key) is str:
                unexpected_strings.append(key)
            else:
                unexpected_other.append(key)
    except Exception:
        return None, _missing_result()

    present = set(values)
    codes = [ScoringValidationCode.MISSING_REQUIRED_FIELD for key in _REQUIRED_MAPPING_KEYS if key not in present]
    codes.extend(ScoringValidationCode.UNEXPECTED_FIELD for _ in sorted(unexpected_strings))
    codes.extend(ScoringValidationCode.UNEXPECTED_FIELD for _ in unexpected_other)

    for field, enum_type in (
        ("scoring_artifact", ScoringArtifact),
        ("prediction_representation", ScoringPredictionRepresentation),
        ("definition_status", ScoringDefinitionStatus),
    ):
        if field in present and type(values[field]) is str:
            try:
                values[field] = enum_type(values[field])
            except ValueError:
                pass
    if "supported_stratification_axes" in present and type(values["supported_stratification_axes"]) is list:
        values["supported_stratification_axes"] = tuple(values["supported_stratification_axes"])
    if "provenance_refs" in present and type(values["provenance_refs"]) is list:
        values["provenance_refs"] = tuple(values["provenance_refs"])
    if "required_baseline_types" in present and type(values["required_baseline_types"]) in (tuple, list):
        adapted = []
        for value in values["required_baseline_types"]:
            if type(value) is str:
                try:
                    value = BaselineType(value)
                except ValueError:
                    pass
            adapted.append(value)
        values["required_baseline_types"] = tuple(adapted)

    codes.extend(_validate(values, present))
    if codes:
        return None, _result(codes)
    definition = ScoringDiagnosticDefinition(**values)
    result = validate_scoring_diagnostic_definition(definition)
    return (definition if result.passed else None), result


def validate_scoring_diagnostic_definition(
    definition: ScoringDiagnosticDefinition,
) -> ScoringDiagnosticValidationResult:
    values = {field: getattr(definition, field) for field in _REQUIRED_MAPPING_KEYS + _OPTIONAL_MAPPING_KEYS}
    return _result(_validate(values, set(values)))
