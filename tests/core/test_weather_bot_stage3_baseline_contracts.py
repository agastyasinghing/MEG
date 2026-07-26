from dataclasses import FrozenInstanceError, fields

import pytest

from meg.weather.stage3.baseline_contracts import (
    BaselineContractDefinition,
    BaselineContractValidationResult,
    BaselineDefinitionStatus,
    BaselineType,
    BaselineValidationCode,
    BaselineValidationSeverity,
    baseline_contract_definition_from_mapping,
    validate_baseline_contract_definition,
)


def _valid(**updates):
    values = {
        "baseline_definition_id": "baseline-1", "baseline_type": "climatology",
        "definition_status": "active", "baseline_version": "v1", "method_id": "method",
        "method_version": "v1", "split_id": "split", "split_version": "v1",
        "fold_id": "fold", "fold_index": 0, "fold_cutoff": "2025-01-03T00:00:00+00:00",
        "prediction_as_of": "2025-01-02T00:00:00+00:00",
        "input_publication_available_at": "2025-01-01T00:00:00+00:00",
        "definition_declared_at": "2025-01-02T00:00:00+00:00", "condition_id": "condition",
        "token_id": "token", "outcome": "yes", "settlement_rule_id": "rule",
        "settlement_rule_version": "v1", "source_compatibility_posture": "compatible",
        "station_compatibility_posture": "compatible", "threshold": "10", "unit": "C",
        "comparator": ">=", "measurement_window": "day", "archive_finality_layer": "as_of",
        "scoring_target_posture": "venue_defined_settlement_outcome",
        "baseline_input_posture": "train_only_as_of_history", "conditioning_dimensions": (),
        "smoothing_definition_id": None, "history_window_definition_id": "history-v1",
        "hierarchy_definition_id": None, "fallback_definition_id": None,
        "persisted_quantity_id": None, "conversion_rule_id": None,
        "split_parity_posture": "same_folds_cutoffs_eligibility_and_test_records_required",
        "paired_comparison_posture": "common_test_record_set_required",
        "availability_posture": "point_in_time_required",
        "fallback_posture": "predeclared_compatible_or_fail_closed",
        "tuning_posture": "train_or_calibration_only",
        "output_contract_posture": "probability_record_contract_required",
        "market_price_posture": "not_approved_as_baseline",
        "baseline_execution_posture": "not_approved", "scoring_execution_posture": "not_approved",
        "storage_persistence_posture": "not_approved", "availability_evidence_refs": ("e1",),
        "provenance_refs": ("p1",), "exclusion_reason": None,
    }
    values.update(updates)
    return values


def _codes(mapping):
    definition, result = baseline_contract_definition_from_mapping(mapping)
    assert definition is None
    return result.codes


def test_public_contract_shapes_and_valid_mapping_round_trip():
    assert tuple(BaselineType) == (BaselineType.CLIMATOLOGY, BaselineType.PERSISTENCE)
    assert len(BaselineValidationCode) == 26
    assert len(fields(BaselineContractDefinition)) == 49
    assert tuple(field.name for field in fields(BaselineContractValidationResult)) == ("severity", "passed", "codes")
    definition, result = baseline_contract_definition_from_mapping(_valid())
    assert result == BaselineContractValidationResult(BaselineValidationSeverity.PASSED, True, ())
    assert definition is not None
    assert type(definition.baseline_type) is BaselineType
    assert type(definition.definition_status) is BaselineDefinitionStatus
    assert validate_baseline_contract_definition(definition) == result
    with pytest.raises(FrozenInstanceError):
        definition.fold_index = 1


def test_shape_errors_aggregate_without_early_return_or_unrelated_suppression():
    values = _valid(baseline_version="", fold_index=True, scoring_target_posture="wrong")
    del values["method_id"]
    values["z-extra"] = 1
    assert _codes(values) == (
        BaselineValidationCode.MISSING_REQUIRED_FIELD,
        BaselineValidationCode.UNEXPECTED_FIELD,
        BaselineValidationCode.BLANK_REQUIRED_TEXT,
        BaselineValidationCode.INVALID_INTEGER_FIELD,
        BaselineValidationCode.INVALID_FIXED_POSTURE,
    )


def test_missing_prerequisites_suppress_only_dependent_diagnostics():
    values = _valid()
    del values["baseline_input_posture"]
    del values["history_window_definition_id"]
    del values["exclusion_reason"]
    assert _codes(values) == (BaselineValidationCode.MISSING_REQUIRED_FIELD,) * 3


class _Hostile(dict):
    def items(self):
        raise RuntimeError("hostile")


def test_non_mapping_and_hostile_mapping_fail_with_exact_missing_sequence():
    expected = (BaselineValidationCode.MISSING_REQUIRED_FIELD,) * 48
    assert _codes(object()) == expected
    assert _codes(_Hostile()) == expected


def test_exact_builtin_types_are_required():
    class Text(str):
        pass

    assert _codes(_valid(baseline_version=Text("v1"), fold_index=True)) == (
        BaselineValidationCode.BLANK_REQUIRED_TEXT,
        BaselineValidationCode.INVALID_INTEGER_FIELD,
    )


def test_duplicate_conditioning_dimensions_fail_exactly_once():
    assert _codes(_valid(conditioning_dimensions=("month", "month"))) == (
        BaselineValidationCode.INVALID_CONDITIONING_DIMENSIONS,
    )


def test_evidence_and_provenance_preserve_valid_order_and_duplicates():
    definition, result = baseline_contract_definition_from_mapping(
        _valid(availability_evidence_refs=["b", "a", "b"], provenance_refs=["p2", "p1", "p2"])
    )
    assert result.codes == ()
    assert definition is not None
    assert definition.availability_evidence_refs == ("b", "a", "b")
    assert definition.provenance_refs == ("p2", "p1", "p2")


def test_climatology_and_persistence_codes_retain_exact_order():
    assert _codes(_valid(
        baseline_input_posture="wrong", history_window_definition_id=None,
        persisted_quantity_id="quantity", conversion_rule_id="rule",
    )) == (
        BaselineValidationCode.CLIMATOLOGY_INVALID_INPUT_POSTURE,
        BaselineValidationCode.CLIMATOLOGY_MISSING_HISTORY_WINDOW,
        BaselineValidationCode.CLIMATOLOGY_PERSISTENCE_FIELDS_PRESENT,
    )
    assert _codes(_valid(
        baseline_type="persistence", baseline_input_posture="wrong",
        conditioning_dimensions=("month",), smoothing_definition_id="smooth",
        history_window_definition_id=None, persisted_quantity_id=None, conversion_rule_id=None,
    )) == (
        BaselineValidationCode.PERSISTENCE_INVALID_INPUT_POSTURE,
        BaselineValidationCode.PERSISTENCE_CONDITIONING_FIELDS_PRESENT,
        BaselineValidationCode.PERSISTENCE_MISSING_QUANTITY,
        BaselineValidationCode.PERSISTENCE_MISSING_CONVERSION_RULE,
    )


def test_diagnostics_are_not_sorted_or_deduplicated():
    assert _codes(_valid(
        availability_evidence_refs=(None, "", 1), provenance_refs=(None, ""),
    )) == (
        BaselineValidationCode.INVALID_AVAILABILITY_EVIDENCE_REF,
        BaselineValidationCode.INVALID_AVAILABILITY_EVIDENCE_REF,
        BaselineValidationCode.INVALID_AVAILABILITY_EVIDENCE_REF,
        BaselineValidationCode.INVALID_PROVENANCE_REF,
        BaselineValidationCode.INVALID_PROVENANCE_REF,
    )
