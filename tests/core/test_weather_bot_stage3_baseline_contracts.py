from __future__ import annotations

import ast
import dataclasses
import inspect
import pathlib
import types
import typing
from collections.abc import Iterator, Mapping
from enum import StrEnum

import pytest

import meg.weather.stage3.baseline_contracts as module
from meg.weather.stage3.baseline_contracts import (
    BaselineContractDefinition,
    BaselineContractValidationResult,
    BaselineDefinitionStatus,
    BaselineType,
    BaselineValidationCode as Code,
    BaselineValidationSeverity,
    baseline_contract_definition_from_mapping,
    validate_baseline_contract_definition,
)

SOURCE_PATH = pathlib.Path(module.__file__)
EXPECTED_PUBLIC = (
    "BaselineType", "BaselineDefinitionStatus", "BaselineValidationSeverity",
    "BaselineValidationCode", "BaselineContractDefinition",
    "BaselineContractValidationResult", "baseline_contract_definition_from_mapping",
    "validate_baseline_contract_definition",
)
EXPECTED_CODES = (
    ("MISSING_REQUIRED_FIELD", "missing_required_field"), ("UNEXPECTED_FIELD", "unexpected_field"),
    ("BLANK_REQUIRED_TEXT", "blank_required_text"), ("INVALID_BASELINE_TYPE", "invalid_baseline_type"),
    ("INVALID_DEFINITION_STATUS", "invalid_definition_status"), ("INVALID_INTEGER_FIELD", "invalid_integer_field"),
    ("INVALID_FIXED_POSTURE", "invalid_fixed_posture"), ("INVALID_TIMESTAMP", "invalid_timestamp"),
    ("INPUT_AVAILABLE_AFTER_PREDICTION", "input_available_after_prediction"),
    ("PREDICTION_AFTER_FOLD_CUTOFF", "prediction_after_fold_cutoff"),
    ("DEFINITION_DECLARED_AFTER_PREDICTION", "definition_declared_after_prediction"),
    ("INVALID_CONDITIONING_DIMENSIONS", "invalid_conditioning_dimensions"),
    ("EMPTY_AVAILABILITY_EVIDENCE_REFS", "empty_availability_evidence_refs"),
    ("INVALID_AVAILABILITY_EVIDENCE_REF", "invalid_availability_evidence_ref"),
    ("EMPTY_PROVENANCE_REFS", "empty_provenance_refs"), ("INVALID_PROVENANCE_REF", "invalid_provenance_ref"),
    ("CLIMATOLOGY_INVALID_INPUT_POSTURE", "climatology_invalid_input_posture"),
    ("CLIMATOLOGY_MISSING_HISTORY_WINDOW", "climatology_missing_history_window"),
    ("CLIMATOLOGY_PERSISTENCE_FIELDS_PRESENT", "climatology_persistence_fields_present"),
    ("PERSISTENCE_INVALID_INPUT_POSTURE", "persistence_invalid_input_posture"),
    ("PERSISTENCE_CONDITIONING_FIELDS_PRESENT", "persistence_conditioning_fields_present"),
    ("PERSISTENCE_MISSING_QUANTITY", "persistence_missing_quantity"),
    ("PERSISTENCE_MISSING_CONVERSION_RULE", "persistence_missing_conversion_rule"),
    ("ACTIVE_WITH_EXCLUSION_REASON", "active_with_exclusion_reason"),
    ("BLOCKED_WITHOUT_EXCLUSION_REASON", "blocked_without_exclusion_reason"),
    ("SELF_SUPERSESSION", "self_supersession"),
)
REQUIRED = (
    "baseline_definition_id", "baseline_type", "definition_status", "baseline_version", "method_id",
    "method_version", "split_id", "split_version", "fold_id", "fold_index", "fold_cutoff",
    "prediction_as_of", "input_publication_available_at", "definition_declared_at", "condition_id",
    "token_id", "outcome", "settlement_rule_id", "settlement_rule_version",
    "source_compatibility_posture", "station_compatibility_posture", "threshold", "unit", "comparator",
    "measurement_window", "archive_finality_layer", "scoring_target_posture", "baseline_input_posture",
    "conditioning_dimensions", "smoothing_definition_id", "history_window_definition_id",
    "hierarchy_definition_id", "fallback_definition_id", "persisted_quantity_id", "conversion_rule_id",
    "split_parity_posture", "paired_comparison_posture", "availability_posture", "fallback_posture",
    "tuning_posture", "output_contract_posture", "market_price_posture", "baseline_execution_posture",
    "scoring_execution_posture", "storage_persistence_posture", "availability_evidence_refs",
    "provenance_refs", "exclusion_reason",
)
OPTIONAL = ("supersedes_baseline_definition_id",)
REQUIRED_TEXT = (
    "baseline_definition_id", "baseline_version", "method_id", "method_version", "split_id", "split_version",
    "fold_id", "condition_id", "token_id", "outcome", "settlement_rule_id", "settlement_rule_version",
    "source_compatibility_posture", "station_compatibility_posture", "threshold", "unit", "comparator",
    "measurement_window", "archive_finality_layer", "scoring_target_posture", "baseline_input_posture",
    "split_parity_posture", "paired_comparison_posture", "availability_posture", "fallback_posture",
    "tuning_posture", "output_contract_posture", "market_price_posture", "baseline_execution_posture",
    "scoring_execution_posture", "storage_persistence_posture",
)
NULLABLE_TEXT = (
    "smoothing_definition_id", "history_window_definition_id", "hierarchy_definition_id",
    "fallback_definition_id", "persisted_quantity_id", "conversion_rule_id", "exclusion_reason",
    "supersedes_baseline_definition_id",
)
TIMESTAMPS = ("fold_cutoff", "prediction_as_of", "input_publication_available_at", "definition_declared_at")
FIXED = (
    ("scoring_target_posture", "venue_defined_settlement_outcome"),
    ("split_parity_posture", "same_folds_cutoffs_eligibility_and_test_records_required"),
    ("paired_comparison_posture", "common_test_record_set_required"),
    ("availability_posture", "point_in_time_required"),
    ("fallback_posture", "predeclared_compatible_or_fail_closed"),
    ("tuning_posture", "train_or_calibration_only"),
    ("output_contract_posture", "probability_record_contract_required"),
    ("market_price_posture", "not_approved_as_baseline"),
    ("baseline_execution_posture", "not_approved"),
    ("scoring_execution_posture", "not_approved"),
    ("storage_persistence_posture", "not_approved"),
)
DEFINITION_TYPES = (
    str, BaselineType, BaselineDefinitionStatus, str, str, str, str, str, str, int,
    str, str, str, str, str, str, str, str, str, str, str, str, str, str, str, str, str, str,
    tuple[str, ...], str | None, str | None, str | None, str | None, str | None, str | None,
    str, str, str, str, str, str, str, str, str, str, tuple[str, ...], tuple[str, ...], str | None,
    str | None,
)


def valid(**changes: object) -> dict[str, object]:
    values: dict[str, object] = {
        "baseline_definition_id": "baseline-1", "baseline_type": "climatology", "definition_status": "active",
        "baseline_version": "v1", "method_id": "method", "method_version": "v1", "split_id": "split",
        "split_version": "v1", "fold_id": "fold", "fold_index": 0,
        "fold_cutoff": "2025-01-03T00:00:00+00:00", "prediction_as_of": "2025-01-02T00:00:00+00:00",
        "input_publication_available_at": "2025-01-01T00:00:00+00:00",
        "definition_declared_at": "2025-01-02T00:00:00+00:00", "condition_id": "condition",
        "token_id": "token", "outcome": "yes", "settlement_rule_id": "rule", "settlement_rule_version": "v1",
        "source_compatibility_posture": "compatible", "station_compatibility_posture": "compatible",
        "threshold": "10", "unit": "C", "comparator": ">=", "measurement_window": "day",
        "archive_finality_layer": "as_of", "scoring_target_posture": "venue_defined_settlement_outcome",
        "baseline_input_posture": "train_only_as_of_history", "conditioning_dimensions": (),
        "smoothing_definition_id": None, "history_window_definition_id": "history-v1",
        "hierarchy_definition_id": None, "fallback_definition_id": None, "persisted_quantity_id": None,
        "conversion_rule_id": None, "split_parity_posture": "same_folds_cutoffs_eligibility_and_test_records_required",
        "paired_comparison_posture": "common_test_record_set_required", "availability_posture": "point_in_time_required",
        "fallback_posture": "predeclared_compatible_or_fail_closed", "tuning_posture": "train_or_calibration_only",
        "output_contract_posture": "probability_record_contract_required",
        "market_price_posture": "not_approved_as_baseline", "baseline_execution_posture": "not_approved",
        "scoring_execution_posture": "not_approved", "storage_persistence_posture": "not_approved",
        "availability_evidence_refs": ("e1",), "provenance_refs": ("p1",), "exclusion_reason": None,
    }
    values.update(changes)
    return values


def persistence(**changes: object) -> dict[str, object]:
    values = valid(baseline_type="persistence", baseline_input_posture="latest_legitimately_available_compatible_prior_state",
                   history_window_definition_id=None, persisted_quantity_id="quantity", conversion_rule_id="conversion")
    values.update(changes)
    return values


def adapt(values: object):
    return baseline_contract_definition_from_mapping(values)


def codes(values: object) -> tuple[Code, ...]:
    return adapt(values)[1].codes


def direct(values: dict[str, object]) -> tuple[Code, ...]:
    supplied = values.copy()
    if supplied["baseline_type"] == "climatology" and type(supplied["baseline_type"]) is str:
        supplied["baseline_type"] = BaselineType.CLIMATOLOGY
    elif supplied["baseline_type"] == "persistence" and type(supplied["baseline_type"]) is str:
        supplied["baseline_type"] = BaselineType.PERSISTENCE
    if supplied["definition_status"] == "active" and type(supplied["definition_status"]) is str:
        supplied["definition_status"] = BaselineDefinitionStatus.ACTIVE
    elif supplied["definition_status"] == "blocked" and type(supplied["definition_status"]) is str:
        supplied["definition_status"] = BaselineDefinitionStatus.BLOCKED
    definition = BaselineContractDefinition(**supplied)
    return validate_baseline_contract_definition(definition).codes


class Text(str):
    pass


class Integer(int):
    pass


class OtherEnum(StrEnum):
    CLIMATOLOGY = "climatology"
    ACTIVE = "active"


class Hostile(Mapping):
    def __init__(self, mode: str): self.mode = mode
    def __len__(self): return 1
    def __iter__(self): return iter(())
    def __getitem__(self, key): raise KeyError(key)
    def items(self):
        if self.mode == "call": raise RuntimeError("call")
        if self.mode == "iterate":
            class Broken:
                def __iter__(self): raise RuntimeError("iterate")
            return Broken()
        if self.mode == "short": return [("field",)]
        if self.mode == "long": return [("field", 1, 2)]
        if self.mode == "noniterable": return [1]
        class BadHash:
            def __hash__(self): raise RuntimeError("hash")
        return [(BadHash(), 1)]


def test_exact_structure_and_private_contract():
    tree = ast.parse(SOURCE_PATH.read_text())
    public = tuple(node.name for node in tree.body if isinstance(node, (ast.ClassDef, ast.FunctionDef)) and not node.name.startswith("_"))
    imports = tuple((type(node).__name__, ast.unparse(node)) for node in tree.body if isinstance(node, (ast.Import, ast.ImportFrom)))
    assert module.__all__ == EXPECTED_PUBLIC
    assert public == EXPECTED_PUBLIC
    assert imports == (
        ("ImportFrom", "from __future__ import annotations"),
        ("ImportFrom", "from collections.abc import Mapping"),
        ("ImportFrom", "from dataclasses import dataclass"),
        ("ImportFrom", "from datetime import datetime"),
        ("ImportFrom", "from enum import StrEnum"),
    )
    assert tuple((item.name, item.value) for item in BaselineType) == (("CLIMATOLOGY", "climatology"), ("PERSISTENCE", "persistence"))
    assert tuple((item.name, item.value) for item in BaselineDefinitionStatus) == (("ACTIVE", "active"), ("BLOCKED", "blocked"))
    assert tuple((item.name, item.value) for item in BaselineValidationSeverity) == (("PASSED", "passed"), ("BLOCKED", "blocked"))
    assert tuple((item.name, item.value) for item in Code) == EXPECTED_CODES
    assert module._REQUIRED_MAPPING_KEYS == REQUIRED
    assert module._OPTIONAL_MAPPING_KEYS == OPTIONAL
    assert module._REQUIRED_TEXT_FIELDS == REQUIRED_TEXT
    assert module._NULLABLE_TEXT_FIELDS == NULLABLE_TEXT
    assert module._TIMESTAMP_FIELDS == TIMESTAMPS
    assert module._FIXED_POSTURES == FIXED


def test_exact_dataclass_shapes_and_signatures():
    definition_fields = dataclasses.fields(BaselineContractDefinition)
    result_fields = dataclasses.fields(BaselineContractValidationResult)
    assert tuple(field.name for field in definition_fields) == REQUIRED + OPTIONAL
    assert tuple(typing.get_type_hints(BaselineContractDefinition).values()) == DEFINITION_TYPES
    assert tuple(field.default for field in definition_fields[:-1]) == (dataclasses.MISSING,) * 48
    assert definition_fields[-1].default is None
    assert BaselineContractDefinition.__dataclass_params__.frozen is True
    assert tuple(field.name for field in result_fields) == ("severity", "passed", "codes")
    assert tuple(typing.get_type_hints(BaselineContractValidationResult).values()) == (BaselineValidationSeverity, bool, tuple[Code, ...])
    assert tuple(field.default for field in result_fields) == (dataclasses.MISSING, dataclasses.MISSING, ())
    assert BaselineContractValidationResult.__dataclass_params__.frozen is True
    mapping_signature = inspect.signature(baseline_contract_definition_from_mapping)
    direct_signature = inspect.signature(validate_baseline_contract_definition)
    assert tuple(mapping_signature.parameters) == ("mapping",)
    assert typing.get_type_hints(baseline_contract_definition_from_mapping) == {
        "mapping": object, "return": tuple[BaselineContractDefinition | None, BaselineContractValidationResult]
    }
    assert tuple(direct_signature.parameters) == ("definition",)
    assert typing.get_type_hints(validate_baseline_contract_definition) == {
        "definition": BaselineContractDefinition, "return": BaselineContractValidationResult
    }


@pytest.mark.parametrize("root", [None, 1, [], (), "mapping", object()])
def test_non_mapping_roots_fail_closed(root):
    assert codes(root) == (Code.MISSING_REQUIRED_FIELD,) * 48


@pytest.mark.parametrize("mode", ["call", "iterate", "short", "long", "noniterable", "hash"])
def test_hostile_mappings_fail_closed(mode):
    assert codes(Hostile(mode)) == (Code.MISSING_REQUIRED_FIELD,) * 48


@pytest.mark.parametrize("field", REQUIRED)
def test_every_required_key_missing_independently(field):
    values = valid()
    del values[field]
    expected = [Code.MISSING_REQUIRED_FIELD]
    if field == "history_window_definition_id": expected = [Code.MISSING_REQUIRED_FIELD]
    assert codes(values) == tuple(expected)


def test_mapping_shape_complete_order_and_no_partial_definition():
    values = valid(baseline_version="")
    del values["method_id"]
    del values["fold_id"]
    values["z-extra"] = 1
    values["a-extra"] = 2
    definition, result = adapt(values)
    assert definition is None
    assert result.codes == (
        Code.MISSING_REQUIRED_FIELD, Code.MISSING_REQUIRED_FIELD,
        Code.UNEXPECTED_FIELD, Code.UNEXPECTED_FIELD, Code.BLANK_REQUIRED_TEXT,
    )


def test_string_subclass_key_is_missing_and_unexpected():
    values = valid()
    value = values.pop("method_id")
    values[Text("method_id")] = value
    assert codes(values) == (Code.MISSING_REQUIRED_FIELD, Code.UNEXPECTED_FIELD)


@pytest.mark.parametrize("bad", ["", 1, Text("valid")])
@pytest.mark.parametrize("field", REQUIRED_TEXT)
def test_every_required_text_field_exact_type(field, bad):
    expected = [Code.BLANK_REQUIRED_TEXT]
    if field in dict(FIXED): expected.append(Code.INVALID_FIXED_POSTURE)
    if field == "baseline_input_posture": expected.append(Code.CLIMATOLOGY_INVALID_INPUT_POSTURE)
    assert codes(valid(**{field: bad})) == tuple(expected)


@pytest.mark.parametrize("field", NULLABLE_TEXT)
@pytest.mark.parametrize("value, generic", [(None, ()), ("valid", ()), ("", (Code.BLANK_REQUIRED_TEXT,)), (1, (Code.BLANK_REQUIRED_TEXT,)), (Text("valid"), (Code.BLANK_REQUIRED_TEXT,))])
def test_nullable_text_matrix(field, value, generic):
    values = valid(**{field: value})
    expected = generic
    if field == "history_window_definition_id" and value is not None and generic:
        expected += (Code.CLIMATOLOGY_MISSING_HISTORY_WINDOW,)
    elif field == "history_window_definition_id" and value is None:
        expected = (Code.CLIMATOLOGY_MISSING_HISTORY_WINDOW,)
    elif field in ("persisted_quantity_id", "conversion_rule_id") and value is not None:
        expected += (Code.CLIMATOLOGY_PERSISTENCE_FIELDS_PRESENT,)
    elif field == "exclusion_reason" and value is not None:
        expected += (Code.ACTIVE_WITH_EXCLUSION_REASON,)
    elif field == "supersedes_baseline_definition_id" and value == "valid":
        expected = generic
    assert codes(values) == expected


@pytest.mark.parametrize("field, member, raw", [("baseline_type", BaselineType.CLIMATOLOGY, "climatology"), ("definition_status", BaselineDefinitionStatus.ACTIVE, "active")])
def test_enum_mapping_and_direct_exactness(field, member, raw):
    definition, result = adapt(valid(**{field: member}))
    assert result.codes == () and definition is not None and getattr(definition, field) is member
    definition, result = adapt(valid(**{field: raw}))
    assert result.codes == () and definition is not None and getattr(definition, field) is member
    invalid_code = Code.INVALID_BASELINE_TYPE if field == "baseline_type" else Code.INVALID_DEFINITION_STATUS
    for bad in (Text(raw), OtherEnum(raw), "invalid", object()):
        assert codes(valid(**{field: bad})) == (invalid_code,)
        assert direct(valid(**{field: bad})) == (invalid_code,)
    raw_values = valid(**{field: raw})
    if field == "baseline_type": raw_values["definition_status"] = BaselineDefinitionStatus.ACTIVE
    else: raw_values["baseline_type"] = BaselineType.CLIMATOLOGY
    raw_definition = BaselineContractDefinition(**raw_values)
    assert validate_baseline_contract_definition(raw_definition).codes == (invalid_code,)


@pytest.mark.parametrize("value, expected", [(0, ()), (2, ()), (-1, (Code.INVALID_INTEGER_FIELD,)), (True, (Code.INVALID_INTEGER_FIELD,)), (Integer(1), (Code.INVALID_INTEGER_FIELD,)), (1.0, (Code.INVALID_INTEGER_FIELD,)), ("1", (Code.INVALID_INTEGER_FIELD,)), (None, (Code.INVALID_INTEGER_FIELD,))])
def test_fold_index_matrix(value, expected):
    if expected:
        assert codes(valid(fold_index=value)) == expected
    else:
        assert adapt(valid(fold_index=value))[1].codes == expected


@pytest.mark.parametrize("field, expected", FIXED)
def test_each_fixed_posture_and_double_categories(field, expected):
    assert codes(valid(**{field: "wrong"})) == (Code.INVALID_FIXED_POSTURE,)
    for bad in ("", 1, Text(expected)):
        assert codes(valid(**{field: bad})) == (Code.BLANK_REQUIRED_TEXT, Code.INVALID_FIXED_POSTURE)


@pytest.mark.parametrize("field", TIMESTAMPS)
@pytest.mark.parametrize("bad", ["bad", "2025-01-01T00:00:00", 1, Text("2025-01-01T00:00:00+00:00")])
def test_each_timestamp_exact_validation(field, bad):
    assert codes(valid(**{field: bad})) == (Code.INVALID_TIMESTAMP,)


def test_timestamp_order_temporal_boundaries_offsets_and_suppression():
    assert codes(valid(fold_cutoff="bad", prediction_as_of="bad", input_publication_available_at="bad", definition_declared_at="bad")) == (Code.INVALID_TIMESTAMP,) * 4
    offset = valid(fold_cutoff="2025-01-02T01:00:00+01:00", prediction_as_of="2025-01-02T00:00:00+00:00",
                   input_publication_available_at="2025-01-01T19:00:00-05:00", definition_declared_at="2025-01-02T00:00:00Z")
    definition, result = adapt(offset)
    assert result.codes == () and definition is not None
    assert definition.fold_cutoff == offset["fold_cutoff"]
    assert codes(valid(fold_cutoff="2025-01-01T00:00:00+00:00", prediction_as_of="2025-01-02T00:00:00+00:00",
                       input_publication_available_at="2025-01-03T00:00:00+00:00", definition_declared_at="2025-01-04T00:00:00+00:00")) == (
        Code.INPUT_AVAILABLE_AFTER_PREDICTION, Code.PREDICTION_AFTER_FOLD_CUTOFF, Code.DEFINITION_DECLARED_AFTER_PREDICTION,
    )
    equal = "2025-01-02T00:00:00+00:00"
    assert adapt(valid(fold_cutoff=equal, prediction_as_of=equal, input_publication_available_at=equal, definition_declared_at=equal))[1].codes == ()
    assert codes(valid(prediction_as_of="bad", input_publication_available_at="2025-01-04T00:00:00+00:00")) == (Code.INVALID_TIMESTAMP,)


@pytest.mark.parametrize("bad", [[], {}, "month", ("",), (1,), (Text("month"),), ("month", "month")])
def test_conditioning_malformed_once_direct(bad):
    assert direct(valid(conditioning_dimensions=bad)) == (Code.INVALID_CONDITIONING_DIMENSIONS,)


def test_conditioning_mapping_adaptation_and_order():
    for value in ((), ("month",), ["season", "month"]):
        original = value.copy() if isinstance(value, list) else value
        definition, result = adapt(valid(conditioning_dimensions=value))
        assert result.codes == () and definition is not None
        assert definition.conditioning_dimensions == tuple(value)
        assert value == original


@pytest.mark.parametrize("field, empty, invalid", [("availability_evidence_refs", Code.EMPTY_AVAILABILITY_EVIDENCE_REFS, Code.INVALID_AVAILABILITY_EVIDENCE_REF), ("provenance_refs", Code.EMPTY_PROVENANCE_REFS, Code.INVALID_PROVENANCE_REF)])
def test_reference_contracts(field, empty, invalid):
    assert direct(valid(**{field: ["a"]})) == (invalid,)
    assert codes(valid(**{field: {"a"}})) == (invalid,)
    assert codes(valid(**{field: ()})) == (empty,)
    assert codes(valid(**{field: (None, "", Text("a"))})) == (invalid, invalid, invalid)
    supplied = ["b", "a", "b"]
    before = supplied.copy()
    definition, result = adapt(valid(**{field: supplied}))
    assert result.codes == () and definition is not None
    assert getattr(definition, field) == ("b", "a", "b")
    assert supplied == before


def test_climatology_complete_role_matrix():
    assert adapt(valid())[1].codes == ()
    assert codes(valid(baseline_input_posture="wrong")) == (Code.CLIMATOLOGY_INVALID_INPUT_POSTURE,)
    for bad, generic in ((None, ()), ("", (Code.BLANK_REQUIRED_TEXT,)), (Text("h"), (Code.BLANK_REQUIRED_TEXT,)), (1, (Code.BLANK_REQUIRED_TEXT,))):
        assert codes(valid(history_window_definition_id=bad)) == generic + (Code.CLIMATOLOGY_MISSING_HISTORY_WINDOW,)
    for field in ("smoothing_definition_id", "hierarchy_definition_id", "fallback_definition_id"):
        assert adapt(valid(**{field: "declared"}))[1].codes == ()
    for changes in ({"persisted_quantity_id": "q"}, {"conversion_rule_id": "c"}, {"persisted_quantity_id": "q", "conversion_rule_id": "c"}):
        assert codes(valid(**changes)) == (Code.CLIMATOLOGY_PERSISTENCE_FIELDS_PRESENT,)
    values = valid()
    del values["history_window_definition_id"]
    assert codes(values) == (Code.MISSING_REQUIRED_FIELD,)
    assert codes(valid(history_window_definition_id="", persisted_quantity_id="q")) == (
        Code.BLANK_REQUIRED_TEXT, Code.CLIMATOLOGY_MISSING_HISTORY_WINDOW, Code.CLIMATOLOGY_PERSISTENCE_FIELDS_PRESENT,
    )


def test_persistence_complete_role_matrix():
    assert adapt(persistence())[1].codes == ()
    assert codes(persistence(baseline_input_posture="wrong")) == (Code.PERSISTENCE_INVALID_INPUT_POSTURE,)
    for changes in ({"conditioning_dimensions": ("month",)}, {"smoothing_definition_id": "s"},
                    {"history_window_definition_id": "h"}, {"hierarchy_definition_id": "h"},
                    {"fallback_definition_id": "f"}, {"smoothing_definition_id": "s", "fallback_definition_id": "f"}):
        assert codes(persistence(**changes)) == (Code.PERSISTENCE_CONDITIONING_FIELDS_PRESENT,)
    for field, role in (("persisted_quantity_id", Code.PERSISTENCE_MISSING_QUANTITY), ("conversion_rule_id", Code.PERSISTENCE_MISSING_CONVERSION_RULE)):
        for bad, generic in ((None, ()), ("", (Code.BLANK_REQUIRED_TEXT,)), (Text("x"), (Code.BLANK_REQUIRED_TEXT,)), (1, (Code.BLANK_REQUIRED_TEXT,))):
            assert codes(persistence(**{field: bad})) == generic + (role,)
        values = persistence(); del values[field]
        assert codes(values) == (Code.MISSING_REQUIRED_FIELD,)
    assert codes(persistence(conditioning_dimensions=("m",), persisted_quantity_id=None, conversion_rule_id=None)) == (
        Code.PERSISTENCE_CONDITIONING_FIELDS_PRESENT, Code.PERSISTENCE_MISSING_QUANTITY, Code.PERSISTENCE_MISSING_CONVERSION_RULE,
    )


def test_status_and_supersession_complete_matrix():
    assert adapt(valid(exclusion_reason=None))[1].codes == ()
    for value, expected in (("reason", (Code.ACTIVE_WITH_EXCLUSION_REASON,)),
                            ("", (Code.BLANK_REQUIRED_TEXT, Code.ACTIVE_WITH_EXCLUSION_REASON)),
                            (1, (Code.BLANK_REQUIRED_TEXT, Code.ACTIVE_WITH_EXCLUSION_REASON)),
                            (Text("reason"), (Code.BLANK_REQUIRED_TEXT, Code.ACTIVE_WITH_EXCLUSION_REASON))):
        assert codes(valid(exclusion_reason=value)) == expected
    assert adapt(valid(definition_status="blocked", exclusion_reason="reason"))[1].codes == ()
    for value, expected in ((None, (Code.BLOCKED_WITHOUT_EXCLUSION_REASON,)),
                            ("", (Code.BLANK_REQUIRED_TEXT, Code.BLOCKED_WITHOUT_EXCLUSION_REASON)),
                            (1, (Code.BLANK_REQUIRED_TEXT, Code.BLOCKED_WITHOUT_EXCLUSION_REASON)),
                            (Text("reason"), (Code.BLANK_REQUIRED_TEXT, Code.BLOCKED_WITHOUT_EXCLUSION_REASON))):
        assert codes(valid(definition_status="blocked", exclusion_reason=value)) == expected
    for status in ("active", "blocked"):
        values = valid(definition_status=status); del values["exclusion_reason"]
        assert codes(values) == (Code.MISSING_REQUIRED_FIELD,)
    assert codes(valid(definition_status="invalid", exclusion_reason="reason")) == (Code.INVALID_DEFINITION_STATUS,)
    for value in (None, "other"):
        assert adapt(valid(supersedes_baseline_definition_id=value))[1].codes == ()
    assert codes(valid(supersedes_baseline_definition_id="baseline-1")) == (Code.SELF_SUPERSESSION,)
    for value in ("", 1, Text("baseline-1")):
        assert codes(valid(supersedes_baseline_definition_id=value)) == (Code.BLANK_REQUIRED_TEXT,)
    assert codes(valid(baseline_definition_id="", supersedes_baseline_definition_id="")) == (
        Code.BLANK_REQUIRED_TEXT, Code.BLANK_REQUIRED_TEXT,
    )


def test_combined_order_and_duplicate_occurrences():
    assert codes(valid(baseline_version="", baseline_type="bad")) == (Code.BLANK_REQUIRED_TEXT, Code.INVALID_BASELINE_TYPE)
    assert codes(valid(fold_index=-1, scoring_target_posture="bad")) == (Code.INVALID_INTEGER_FIELD, Code.INVALID_FIXED_POSTURE)
    assert codes(valid(prediction_as_of="2025-01-02T00:00:00+00:00", fold_cutoff="2025-01-01T00:00:00+00:00", conditioning_dimensions=("",))) == (
        Code.PREDICTION_AFTER_FOLD_CUTOFF, Code.INVALID_CONDITIONING_DIMENSIONS,
    )
    assert codes(valid(availability_evidence_refs=(None, ""), provenance_refs=(None, ""))) == (
        Code.INVALID_AVAILABILITY_EVIDENCE_REF, Code.INVALID_AVAILABILITY_EVIDENCE_REF,
        Code.INVALID_PROVENANCE_REF, Code.INVALID_PROVENANCE_REF,
    )
    assert codes(valid(exclusion_reason="reason", supersedes_baseline_definition_id="baseline-1")) == (
        Code.ACTIVE_WITH_EXCLUSION_REASON, Code.SELF_SUPERSESSION,
    )


def test_immutability_purity_determinism_and_canonical_surface():
    caller = valid(conditioning_dimensions=["month"], availability_evidence_refs=["e", "e"], provenance_refs=("p2", "p1"))
    before = {key: value.copy() if isinstance(value, list) else value for key, value in caller.items()}
    first = adapt(caller); second = adapt(caller)
    assert first == second
    assert caller == before
    definition, result = first
    assert definition is not None and type(definition.conditioning_dimensions) is tuple
    assert type(definition.availability_evidence_refs) is tuple and type(definition.provenance_refs) is tuple
    assert type(result.codes) is tuple
    with pytest.raises(dataclasses.FrozenInstanceError): definition.fold_index = 2
    with pytest.raises(dataclasses.FrozenInstanceError): result.passed = False
    assert tuple(name for name in REQUIRED if name in ("condition_id", "token_id", "outcome")) == ("condition_id", "token_id", "outcome")
    prohibited = "market" + "_id"
    assert prohibited not in REQUIRED + OPTIONAL
    tree = ast.parse(SOURCE_PATH.read_text())
    forbidden_import_roots = ("os", "subprocess", "socket", "sqlite3", "duckdb", "requests", "urllib", "http", "time")
    observed = tuple(alias.name.split(".")[0] for node in ast.walk(tree) if isinstance(node, (ast.Import, ast.ImportFrom)) for alias in node.names)
    assert all(root not in forbidden_import_roots for root in observed)
    forbidden_calls = ("open", "exec", "eval", "compile", "system", "popen")
    calls = tuple(node.func.id for node in ast.walk(tree) if isinstance(node, ast.Call) and isinstance(node.func, ast.Name))
    assert all(name not in forbidden_calls for name in calls)
