from __future__ import annotations

import ast
import dataclasses
from dataclasses import FrozenInstanceError
from decimal import Decimal
from enum import StrEnum
from pathlib import Path

import pytest

import meg.weather.stage3 as stage3
from meg.weather.stage3 import binary_probability_record as mod
from meg.weather.stage3.binary_probability_record import (
    BinaryOutcomeProbabilityRecord,
    PredictionRepresentation,
    ProbabilityRecordValidationCode as Code,
    ProbabilityRecordValidationResult,
    ProbabilityRecordValidationSeverity,
    binary_outcome_probability_record_from_mapping,
    validate_binary_outcome_probability_record,
)

NON_ROUTING_MARKET_KEY = "market" + "_id"

REQUIRED_KEYS = (
    "prediction_record_id", "condition_id", "token_id", "outcome",
    "settlement_rule_id", "settlement_rule_version", "prediction_as_of",
    "input_publication_available_at", "market_family", "threshold", "unit",
    "comparator", "measurement_window", "source_compatibility_posture",
    "station_compatibility_posture", "archive_finality_layer",
    "prediction_representation", "probability", "method_id", "method_version",
    "provenance_refs", "created_at", "record_version",
)
TEXT_FIELDS = (
    "prediction_record_id", "condition_id", "token_id", "outcome",
    "settlement_rule_id", "settlement_rule_version", "market_family", "threshold",
    "unit", "comparator", "measurement_window", "source_compatibility_posture",
    "station_compatibility_posture", "archive_finality_layer", "method_id",
    "method_version", "record_version",
)


def valid_mapping() -> dict[str, object]:
    return {
        "prediction_record_id": "pred-1",
        "condition_id": "cond-1",
        "token_id": "tok-yes",
        "outcome": "YES",
        "settlement_rule_id": "rule-1",
        "settlement_rule_version": "v1",
        "prediction_as_of": "2026-01-02T03:04:05+00:00",
        "input_publication_available_at": "2026-01-02T03:04:05+00:00",
        "market_family": "weather",
        "threshold": "10",
        "unit": "mm",
        "comparator": ">=",
        "measurement_window": "2026-01-02",
        "source_compatibility_posture": "compatible",
        "station_compatibility_posture": "compatible",
        "archive_finality_layer": "final",
        "prediction_representation": "binary_outcome_probability",
        "probability": "0.500",
        "method_id": "method-1",
        "method_version": "v1",
        "provenance_refs": ["ref-b", "ref-a", "ref-b"],
        "created_at": "2026-01-02T03:04:05+00:00",
        "record_version": "v1",
        "supersedes_prediction_record_id": "pred-0",
    }


def result_codes(mapping):
    record, result = binary_outcome_probability_record_from_mapping(mapping)
    assert record is None
    assert result.severity is ProbabilityRecordValidationSeverity.BLOCKED
    assert result.passed is False
    return result.codes


def test_public_api_package_boundary_and_imports():
    assert mod.__all__ == (
        "PredictionRepresentation", "ProbabilityRecordValidationSeverity",
        "ProbabilityRecordValidationCode", "BinaryOutcomeProbabilityRecord",
        "ProbabilityRecordValidationResult", "binary_outcome_probability_record_from_mapping",
        "validate_binary_outcome_probability_record",
    )
    assert [m.value for m in PredictionRepresentation] == ["binary_outcome_probability"]
    assert [m.value for m in ProbabilityRecordValidationSeverity] == ["passed", "blocked"]
    assert [m.value for m in Code] == [
        "missing_required_field", "unexpected_field", "blank_required_text",
        "invalid_prediction_representation", "invalid_probability_type",
        "non_finite_probability", "probability_out_of_range", "invalid_timestamp",
        "input_available_after_prediction", "created_before_prediction",
        "empty_provenance_refs", "invalid_provenance_ref", "self_supersession",
    ]
    for symbol in mod.__all__:
        assert not hasattr(stage3, symbol)
    tree = ast.parse(Path(mod.__file__).read_text())
    imports = {alias.name for node in tree.body if isinstance(node, ast.Import) for alias in node.names}
    froms = {node.module for node in tree.body if isinstance(node, ast.ImportFrom)}
    assert imports == {"re"}
    assert froms == {"__future__", "collections.abc", "dataclasses", "datetime", "decimal", "enum"}
    assert not any((name or "").startswith("meg.") for name in imports | froms)


def test_dataclass_contracts_and_frozen_defaults():
    assert [f.name for f in dataclasses.fields(BinaryOutcomeProbabilityRecord)] == list(REQUIRED_KEYS) + ["supersedes_prediction_record_id"]
    assert [f.name for f in dataclasses.fields(ProbabilityRecordValidationResult)] == ["severity", "passed", "codes"]
    assert BinaryOutcomeProbabilityRecord.__dataclass_params__.frozen
    assert ProbabilityRecordValidationResult.__dataclass_params__.frozen
    defaults = {f.name: f.default for f in dataclasses.fields(BinaryOutcomeProbabilityRecord)}
    assert defaults["supersedes_prediction_record_id"] is None
    for key in REQUIRED_KEYS:
        assert defaults[key] is dataclasses.MISSING
    assert dataclasses.fields(ProbabilityRecordValidationResult)[2].default == ()
    record, result = binary_outcome_probability_record_from_mapping(valid_mapping())
    assert result.passed and record is not None
    with pytest.raises(FrozenInstanceError):
        record.outcome = "NO"
    with pytest.raises(FrozenInstanceError):
        result.passed = False


def test_accepted_mapping_and_typed_inputs_preserve_caller_values():
    source = valid_mapping()
    record, result = binary_outcome_probability_record_from_mapping(source)
    assert result == ProbabilityRecordValidationResult(ProbabilityRecordValidationSeverity.PASSED, True)
    assert record is not None
    assert record.prediction_representation is PredictionRepresentation.BINARY_OUTCOME_PROBABILITY
    assert record.probability == Decimal("0.500")
    assert record.provenance_refs == ("ref-b", "ref-a", "ref-b")
    assert record.prediction_as_of == source["prediction_as_of"]
    assert record.condition_id == "cond-1" and record.token_id == "tok-yes" and record.outcome == "YES"
    typed = valid_mapping() | {
        "prediction_representation": PredictionRepresentation.BINARY_OUTCOME_PROBABILITY,
        "probability": Decimal("1"),
        "provenance_refs": ("ref-1",),
    }
    typed_record, typed_result = binary_outcome_probability_record_from_mapping(typed)
    assert typed_result.passed and typed_record is not None
    assert typed_record.probability == Decimal("1")
    assert typed_record.provenance_refs == ("ref-1",)


def test_mapping_shape_failures_and_optional_supersession():
    assert result_codes(object()) == (Code.MISSING_REQUIRED_FIELD,) * len(REQUIRED_KEYS)
    for key in REQUIRED_KEYS:
        data = valid_mapping(); data.pop(key)
        assert result_codes(data) == (Code.MISSING_REQUIRED_FIELD,)
    data = valid_mapping(); data.pop("prediction_record_id"); data.pop("token_id")
    assert result_codes(data) == (Code.MISSING_REQUIRED_FIELD, Code.MISSING_REQUIRED_FIELD)
    assert result_codes(valid_mapping() | {"z": 1}) == (Code.UNEXPECTED_FIELD,)
    assert result_codes(valid_mapping() | {"z": 1, "a": 2}) == (Code.UNEXPECTED_FIELD, Code.UNEXPECTED_FIELD)
    assert result_codes(valid_mapping() | {NON_ROUTING_MARKET_KEY: "x"}) == (Code.UNEXPECTED_FIELD,)
    assert result_codes(valid_mapping() | {"token_outcome_pair": "x"}) == (Code.UNEXPECTED_FIELD,)
    data = valid_mapping(); data.pop("outcome"); data["extra"] = 1
    assert result_codes(data) == (Code.MISSING_REQUIRED_FIELD, Code.UNEXPECTED_FIELD)
    for optional in (False, True):
        data = valid_mapping()
        if optional:
            data["supersedes_prediction_record_id"] = None
        else:
            data.pop("supersedes_prediction_record_id")
        assert binary_outcome_probability_record_from_mapping(data)[1].passed


@pytest.mark.parametrize("bad", ["", "   ", 7])
def test_required_text_fields_and_optional_supersession(bad):
    for field in TEXT_FIELDS:
        data = valid_mapping(); data[field] = bad
        assert result_codes(data) == (Code.BLANK_REQUIRED_TEXT,)
    data = valid_mapping(); data["prediction_record_id"] = " "; data["condition_id"] = 7
    assert result_codes(data) == (Code.BLANK_REQUIRED_TEXT, Code.BLANK_REQUIRED_TEXT)
    data = valid_mapping(); data["supersedes_prediction_record_id"] = bad
    assert result_codes(data) == (Code.BLANK_REQUIRED_TEXT,)


class OtherEnum(StrEnum):
    VALUE = "binary_outcome_probability"


@pytest.mark.parametrize("value", [PredictionRepresentation.BINARY_OUTCOME_PROBABILITY, "binary_outcome_probability"])
def test_representation_accepted(value):
    assert binary_outcome_probability_record_from_mapping(valid_mapping() | {"prediction_representation": value})[1].passed


@pytest.mark.parametrize("value", ["unknown", "binary_outcome_probability:v2", OtherEnum.VALUE])
def test_representation_rejected(value):
    assert result_codes(valid_mapping() | {"prediction_representation": value}) == (Code.INVALID_PREDICTION_REPRESENTATION,)


@pytest.mark.parametrize("value", [Decimal("0"), Decimal("1"), Decimal("0.123456789123456789"), "0.5", "0.00", "1.000"])
def test_probability_passes(value):
    assert binary_outcome_probability_record_from_mapping(valid_mapping() | {"probability": value})[1].passed


@pytest.mark.parametrize(("value", "code"), [
    (Decimal("-0.000000000000000001"), Code.PROBABILITY_OUT_OF_RANGE),
    (Decimal("1.000000000000000001"), Code.PROBABILITY_OUT_OF_RANGE),
    (True, Code.INVALID_PROBABILITY_TYPE), (1, Code.INVALID_PROBABILITY_TYPE),
    (0.5, Code.INVALID_PROBABILITY_TYPE), ("abc", Code.INVALID_PROBABILITY_TYPE),
    (" 0.5", Code.INVALID_PROBABILITY_TYPE), ("0.5 ", Code.INVALID_PROBABILITY_TYPE),
    ("1e-2", Code.INVALID_PROBABILITY_TYPE), ("+0.5", Code.INVALID_PROBABILITY_TYPE),
    (".5", Code.INVALID_PROBABILITY_TYPE), ("1.", Code.INVALID_PROBABILITY_TYPE),
    ("00.5", Code.INVALID_PROBABILITY_TYPE), (Decimal("NaN"), Code.NON_FINITE_PROBABILITY),
    ("NaN", Code.NON_FINITE_PROBABILITY), (Decimal("Infinity"), Code.NON_FINITE_PROBABILITY),
    ("Infinity", Code.NON_FINITE_PROBABILITY), ("-Infinity", Code.NON_FINITE_PROBABILITY),
])
def test_probability_rejections_are_exact(value, code):
    assert result_codes(valid_mapping() | {"probability": value}) == (code,)


def test_timestamps_validation_and_chronology():
    assert binary_outcome_probability_record_from_mapping(valid_mapping() | {
        "prediction_as_of": "2026-01-02T03:04:05+05:30",
        "input_publication_available_at": "2026-01-01T21:34:05-00:00",
        "created_at": "2026-01-01T21:34:05-04:00",
    })[1].passed
    assert result_codes(valid_mapping() | {"prediction_as_of": "bad", "input_publication_available_at": "2026-01-02T03:04:05", "created_at": 3}) == (Code.INVALID_TIMESTAMP, Code.INVALID_TIMESTAMP, Code.INVALID_TIMESTAMP)
    assert result_codes(valid_mapping() | {"input_publication_available_at": "2026-01-02T03:04:06+00:00"}) == (Code.INPUT_AVAILABLE_AFTER_PREDICTION,)
    assert result_codes(valid_mapping() | {"created_at": "2026-01-02T03:04:04+00:00"}) == (Code.CREATED_BEFORE_PREDICTION,)
    assert result_codes(valid_mapping() | {"prediction_as_of": "bad", "input_publication_available_at": "2999-01-02T03:04:06+00:00", "created_at": "1999-01-02T03:04:04+00:00"}) == (Code.INVALID_TIMESTAMP,)


def test_provenance_validation_preserves_order_and_duplicates():
    for value in [("a", "b"), ["b", "a", "b"]]:
        record, result = binary_outcome_probability_record_from_mapping(valid_mapping() | {"provenance_refs": value})
        assert result.passed and record is not None
        assert record.provenance_refs == tuple(value)
    for value in [(), []]:
        assert result_codes(valid_mapping() | {"provenance_refs": value}) == (Code.EMPTY_PROVENANCE_REFS,)
    assert result_codes(valid_mapping() | {"provenance_refs": "ref"}) == (Code.INVALID_PROVENANCE_REF,)
    assert result_codes(valid_mapping() | {"provenance_refs": ["", 1, "ok", " "]}) == (Code.INVALID_PROVENANCE_REF, Code.INVALID_PROVENANCE_REF, Code.INVALID_PROVENANCE_REF)


def test_supersession_rules():
    assert binary_outcome_probability_record_from_mapping(valid_mapping() | {"supersedes_prediction_record_id": "other"})[1].passed
    assert result_codes(valid_mapping() | {"supersedes_prediction_record_id": "pred-1"}) == (Code.SELF_SUPERSESSION,)


def test_deterministic_combined_failures_for_mapping_and_direct_record():
    data = valid_mapping() | {
        "prediction_record_id": " ", "prediction_representation": "bad",
        "probability": "1e-2", "prediction_as_of": "bad", "input_publication_available_at": "bad2",
        "created_at": "bad3", "provenance_refs": ["", 2], "supersedes_prediction_record_id": " ",
    }
    expected = (
        Code.BLANK_REQUIRED_TEXT, Code.BLANK_REQUIRED_TEXT,
        Code.INVALID_PREDICTION_REPRESENTATION,
        Code.INVALID_PROBABILITY_TYPE, Code.INVALID_TIMESTAMP, Code.INVALID_TIMESTAMP,
        Code.INVALID_TIMESTAMP, Code.INVALID_PROVENANCE_REF, Code.INVALID_PROVENANCE_REF,
        Code.SELF_SUPERSESSION,
    )
    for _ in range(3):
        assert result_codes(data) == expected
    record = BinaryOutcomeProbabilityRecord(**(valid_mapping() | {
        "prediction_representation": PredictionRepresentation.BINARY_OUTCOME_PROBABILITY,
        "probability": Decimal("2"),
        "provenance_refs": tuple(),
        "created_at": "2026-01-02T03:04:04+00:00",
    }))
    assert validate_binary_outcome_probability_record(record).codes == (Code.PROBABILITY_OUT_OF_RANGE, Code.CREATED_BEFORE_PREDICTION, Code.EMPTY_PROVENANCE_REFS)


def test_source_audit_non_goals():
    tree = ast.parse(Path(mod.__file__).read_text())
    forbidden_import_roots = {"os", "socket", "http", "urllib", "requests", "subprocess", "sqlite3", "duckdb", "psycopg", "json", "csv", "meg.weather.stage2"}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            assert not any(alias.name.split(".")[0] in forbidden_import_roots for alias in node.names)
        if isinstance(node, ast.ImportFrom):
            assert (node.module or "").split(".")[0] not in forbidden_import_roots
        if isinstance(node, ast.Name):
            assert node.id not in {"Path", "open", "exec", "eval"}
        if isinstance(node, ast.FunctionDef):
            lowered = node.name.lower()
            forbidden_terms = ("generate", "score", "model", "join", "persist", "report", "export", "simulate", "trade", "schedule", "queue", "orchestrat")
            assert not any(term in lowered for term in forbidden_terms)
