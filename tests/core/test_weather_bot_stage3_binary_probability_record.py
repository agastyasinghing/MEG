from __future__ import annotations

import ast
import dataclasses
import inspect
from dataclasses import FrozenInstanceError
from decimal import Decimal
from enum import StrEnum
from pathlib import Path
from typing import get_type_hints

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
OPTIONAL_KEYS = ("supersedes_prediction_record_id",)
TEXT_FIELDS = (
    "prediction_record_id", "condition_id", "token_id", "outcome",
    "settlement_rule_id", "settlement_rule_version", "market_family", "threshold",
    "unit", "comparator", "measurement_window", "source_compatibility_posture",
    "station_compatibility_posture", "archive_finality_layer", "method_id",
    "method_version", "record_version",
)
TIMESTAMP_FIELDS = ("prediction_as_of", "input_publication_available_at", "created_at")
PUBLIC_SYMBOLS = (
    "PredictionRepresentation", "ProbabilityRecordValidationSeverity",
    "ProbabilityRecordValidationCode", "BinaryOutcomeProbabilityRecord",
    "ProbabilityRecordValidationResult", "binary_outcome_probability_record_from_mapping",
    "validate_binary_outcome_probability_record",
)


def valid_mapping() -> dict[str, object]:
    return {
        "prediction_record_id": "pred-1", "condition_id": "cond-1", "token_id": "tok-yes",
        "outcome": "YES", "settlement_rule_id": "rule-1", "settlement_rule_version": "v1",
        "prediction_as_of": "2026-01-02T03:04:05+00:00",
        "input_publication_available_at": "2026-01-02T03:04:05+00:00",
        "market_family": "weather", "threshold": "10", "unit": "mm", "comparator": ">=",
        "measurement_window": "2026-01-02", "source_compatibility_posture": "compatible",
        "station_compatibility_posture": "compatible", "archive_finality_layer": "final",
        "prediction_representation": "binary_outcome_probability", "probability": "0.500",
        "method_id": "method-1", "method_version": "v1",
        "provenance_refs": ["ref-b", "ref-a", "ref-b"],
        "created_at": "2026-01-02T03:04:05+00:00", "record_version": "v1",
        "supersedes_prediction_record_id": "pred-0",
    }


def valid_record(**overrides: object) -> BinaryOutcomeProbabilityRecord:
    data = valid_mapping() | {
        "prediction_representation": PredictionRepresentation.BINARY_OUTCOME_PROBABILITY,
        "probability": Decimal("0.500"),
        "provenance_refs": ("ref-b", "ref-a", "ref-b"),
    }
    data.update(overrides)
    return BinaryOutcomeProbabilityRecord(**data)


def assert_blocked(result: ProbabilityRecordValidationResult, codes: tuple[Code, ...]) -> None:
    assert result == ProbabilityRecordValidationResult(ProbabilityRecordValidationSeverity.BLOCKED, False, codes)


def mapping_codes(mapping: object) -> tuple[Code, ...]:
    record, result = binary_outcome_probability_record_from_mapping(mapping)
    assert record is None
    assert result.severity is ProbabilityRecordValidationSeverity.BLOCKED
    assert result.passed is False
    assert result.codes
    return result.codes


def direct_codes(record: BinaryOutcomeProbabilityRecord) -> tuple[Code, ...]:
    result = validate_binary_outcome_probability_record(record)
    assert result.severity is ProbabilityRecordValidationSeverity.BLOCKED
    assert result.passed is False
    assert result.codes
    return result.codes


def test_package_file_ast_boundary():
    tree = ast.parse(Path(stage3.__file__).read_text())
    assert len(tree.body) == 2
    assert isinstance(tree.body[0], ast.Expr)
    assert isinstance(tree.body[0].value, ast.Constant)
    assert isinstance(tree.body[1], ast.ImportFrom)
    assert tree.body[1].module == "__future__"
    assert [alias.name for alias in tree.body[1].names] == ["annotations"]
    for symbol in PUBLIC_SYMBOLS:
        assert not hasattr(stage3, symbol)


def test_public_definitions_all_and_imports_are_exact():
    assert mod.__all__ == PUBLIC_SYMBOLS
    tree = ast.parse(Path(mod.__file__).read_text())
    public_defs = tuple(
        node.name for node in tree.body
        if isinstance(node, (ast.ClassDef, ast.FunctionDef)) and not node.name.startswith("_")
    )
    assert public_defs == PUBLIC_SYMBOLS
    imports = []
    for node in tree.body:
        if isinstance(node, ast.ImportFrom):
            imports.append((node.module, tuple(alias.name for alias in node.names)))
        elif isinstance(node, ast.Import):
            imports.append(("", tuple(alias.name for alias in node.names)))
    assert imports == [
        ("__future__", ("annotations",)),
        ("collections.abc", ("Mapping",)),
        ("dataclasses", ("dataclass",)),
        ("datetime", ("datetime",)),
        ("decimal", ("Decimal", "InvalidOperation")),
        ("enum", ("StrEnum",)),
    ]


def test_enum_contracts_are_exact():
    assert tuple(PredictionRepresentation.__members__) == ("BINARY_OUTCOME_PROBABILITY",)
    assert tuple(ProbabilityRecordValidationSeverity.__members__) == ("PASSED", "BLOCKED")
    assert tuple(Code.__members__) == (
        "MISSING_REQUIRED_FIELD", "UNEXPECTED_FIELD", "BLANK_REQUIRED_TEXT",
        "INVALID_PREDICTION_REPRESENTATION", "INVALID_PROBABILITY_TYPE",
        "NON_FINITE_PROBABILITY", "PROBABILITY_OUT_OF_RANGE", "INVALID_TIMESTAMP",
        "INPUT_AVAILABLE_AFTER_PREDICTION", "CREATED_BEFORE_PREDICTION",
        "EMPTY_PROVENANCE_REFS", "INVALID_PROVENANCE_REF", "SELF_SUPERSESSION",
    )
    assert [member.value for member in PredictionRepresentation] == ["binary_outcome_probability"]
    assert [member.value for member in ProbabilityRecordValidationSeverity] == ["passed", "blocked"]
    assert [member.value for member in Code] == [
        "missing_required_field", "unexpected_field", "blank_required_text",
        "invalid_prediction_representation", "invalid_probability_type", "non_finite_probability",
        "probability_out_of_range", "invalid_timestamp", "input_available_after_prediction",
        "created_before_prediction", "empty_provenance_refs", "invalid_provenance_ref",
        "self_supersession",
    ]


def test_dataclass_contracts_types_defaults_and_frozen():
    record_fields = dataclasses.fields(BinaryOutcomeProbabilityRecord)
    result_fields = dataclasses.fields(ProbabilityRecordValidationResult)
    assert [field.name for field in record_fields] == list(REQUIRED_KEYS) + ["supersedes_prediction_record_id"]
    assert [field.name for field in result_fields] == ["severity", "passed", "codes"]
    record_hints = get_type_hints(BinaryOutcomeProbabilityRecord)
    expected_record_types = {
        **{name: str for name in REQUIRED_KEYS if name not in {"prediction_representation", "probability", "provenance_refs"}},
        "prediction_representation": PredictionRepresentation,
        "probability": Decimal,
        "provenance_refs": tuple[str, ...],
        "supersedes_prediction_record_id": str | None,
    }
    assert record_hints == expected_record_types
    assert get_type_hints(ProbabilityRecordValidationResult) == {
        "severity": ProbabilityRecordValidationSeverity,
        "passed": bool,
        "codes": tuple[Code, ...],
    }
    assert BinaryOutcomeProbabilityRecord.__dataclass_params__.frozen
    assert ProbabilityRecordValidationResult.__dataclass_params__.frozen
    defaults = {field.name: field.default for field in record_fields}
    for key in REQUIRED_KEYS:
        assert defaults[key] is dataclasses.MISSING
    assert defaults["supersedes_prediction_record_id"] is None
    assert result_fields[2].default == ()
    record = valid_record()
    result = ProbabilityRecordValidationResult(ProbabilityRecordValidationSeverity.PASSED, True)
    with pytest.raises(FrozenInstanceError):
        record.outcome = "NO"
    with pytest.raises(FrozenInstanceError):
        result.passed = False


def test_function_signatures_and_private_declarations_are_exact():
    mapping_signature = inspect.signature(binary_outcome_probability_record_from_mapping)
    direct_signature = inspect.signature(validate_binary_outcome_probability_record)
    assert tuple(mapping_signature.parameters) == ("mapping",)
    assert mapping_signature.parameters["mapping"].kind is inspect.Parameter.POSITIONAL_OR_KEYWORD
    assert mapping_signature.parameters["mapping"].default is inspect.Parameter.empty
    assert tuple(direct_signature.parameters) == ("record",)
    assert direct_signature.parameters["record"].kind is inspect.Parameter.POSITIONAL_OR_KEYWORD
    assert direct_signature.parameters["record"].default is inspect.Parameter.empty
    mapping_hints = get_type_hints(binary_outcome_probability_record_from_mapping)
    direct_hints = get_type_hints(validate_binary_outcome_probability_record)
    assert mapping_hints == {
        "mapping": object,
        "return": tuple[BinaryOutcomeProbabilityRecord | None, ProbabilityRecordValidationResult],
    }
    assert direct_hints == {
        "record": BinaryOutcomeProbabilityRecord,
        "return": ProbabilityRecordValidationResult,
    }
    assert mod._REQUIRED_KEYS == REQUIRED_KEYS
    assert mod._OPTIONAL_KEYS == OPTIONAL_KEYS
    assert mod._TEXT_FIELDS == TEXT_FIELDS
    assert mod._TIMESTAMP_FIELDS == TIMESTAMP_FIELDS


def test_mapping_accepted_forms_preserve_caller_values():
    record, result = binary_outcome_probability_record_from_mapping(valid_mapping())
    assert record is not None
    assert result == ProbabilityRecordValidationResult(ProbabilityRecordValidationSeverity.PASSED, True)
    assert record.prediction_representation is PredictionRepresentation.BINARY_OUTCOME_PROBABILITY
    assert record.probability == Decimal("0.500")
    assert record.provenance_refs == ("ref-b", "ref-a", "ref-b")
    assert record.prediction_as_of == "2026-01-02T03:04:05+00:00"
    assert record.input_publication_available_at == "2026-01-02T03:04:05+00:00"
    assert record.created_at == "2026-01-02T03:04:05+00:00"
    assert record.prediction_record_id == "pred-1"
    assert record.condition_id == "cond-1"
    assert record.token_id == "tok-yes"
    assert record.outcome == "YES"
    typed_record, typed_result = binary_outcome_probability_record_from_mapping(valid_mapping() | {
        "prediction_representation": PredictionRepresentation.BINARY_OUTCOME_PROBABILITY,
        "probability": Decimal("1"), "provenance_refs": ("ref-1", "ref-1"),
    })
    assert typed_result.passed and typed_record is not None
    assert typed_record.probability == Decimal("1")
    assert typed_record.provenance_refs == ("ref-1", "ref-1")


def test_mapping_shape_aggregates_with_present_value_failures():
    assert mapping_codes(object()) == (Code.MISSING_REQUIRED_FIELD,) * len(REQUIRED_KEYS)
    for key in REQUIRED_KEYS:
        data = valid_mapping(); data.pop(key)
        assert mapping_codes(data) == (Code.MISSING_REQUIRED_FIELD,)
    data = valid_mapping(); data.update({"unexpected": 1, "probability": 0.5, "created_at": "bad"})
    assert mapping_codes(data) == (Code.UNEXPECTED_FIELD, Code.INVALID_PROBABILITY_TYPE, Code.INVALID_TIMESTAMP)
    data = valid_mapping(); data.pop("outcome"); data.update({
        "condition_id": " ", "prediction_representation": "bad", "probability": Decimal("2"),
        "provenance_refs": [],
    })
    assert mapping_codes(data) == (
        Code.MISSING_REQUIRED_FIELD, Code.BLANK_REQUIRED_TEXT,
        Code.INVALID_PREDICTION_REPRESENTATION, Code.PROBABILITY_OUT_OF_RANGE,
        Code.EMPTY_PROVENANCE_REFS,
    )
    data = valid_mapping(); data.pop("prediction_record_id"); data.pop("token_id")
    data.update({"z": 1, "a": 2, "condition_id": "", "settlement_rule_id": 3,
                 "prediction_as_of": "bad", "input_publication_available_at": "bad2",
                 "provenance_refs": ["", 1]})
    assert mapping_codes(data) == (
        Code.MISSING_REQUIRED_FIELD, Code.MISSING_REQUIRED_FIELD,
        Code.UNEXPECTED_FIELD, Code.UNEXPECTED_FIELD,
        Code.BLANK_REQUIRED_TEXT, Code.BLANK_REQUIRED_TEXT,
        Code.INVALID_TIMESTAMP, Code.INVALID_TIMESTAMP,
        Code.INVALID_PROVENANCE_REF, Code.INVALID_PROVENANCE_REF,
    )
    assert mapping_codes(valid_mapping() | {NON_ROUTING_MARKET_KEY: "x"}) == (Code.UNEXPECTED_FIELD,)
    assert mapping_codes(valid_mapping() | {"token_outcome_pair": "x"}) == (Code.UNEXPECTED_FIELD,)
    for replacement in ({}, {"supersedes_prediction_record_id": None}):
        data = valid_mapping(); data.pop("supersedes_prediction_record_id"); data.update(replacement)
        assert binary_outcome_probability_record_from_mapping(data)[1].passed


@pytest.mark.parametrize("bad", ["", "   ", 7])
def test_mapping_required_text_fields_and_optional_supersession(bad):
    for field in TEXT_FIELDS:
        assert mapping_codes(valid_mapping() | {field: bad}) == (Code.BLANK_REQUIRED_TEXT,)
    data = valid_mapping() | {"prediction_record_id": "", "condition_id": 7, "token_id": " "}
    assert mapping_codes(data) == (Code.BLANK_REQUIRED_TEXT, Code.BLANK_REQUIRED_TEXT, Code.BLANK_REQUIRED_TEXT)
    assert mapping_codes(valid_mapping() | {"supersedes_prediction_record_id": bad}) == (Code.BLANK_REQUIRED_TEXT,)


class OtherEnum(StrEnum):
    VALUE = "binary_outcome_probability"


class StringSubclass(str):
    pass


@pytest.mark.parametrize("value", [PredictionRepresentation.BINARY_OUTCOME_PROBABILITY, "binary_outcome_probability"])
def test_mapping_representation_accepted(value):
    assert binary_outcome_probability_record_from_mapping(valid_mapping() | {"prediction_representation": value})[1].passed


@pytest.mark.parametrize("value", ["unknown", "binary_outcome_probability:v2", OtherEnum.VALUE, StringSubclass("binary_outcome_probability")])
def test_mapping_representation_rejected(value):
    assert mapping_codes(valid_mapping() | {"prediction_representation": value}) == (Code.INVALID_PREDICTION_REPRESENTATION,)


@pytest.mark.parametrize("value", [Decimal("0"), Decimal("1"), Decimal("0.123456789123456789"), "0", "1", "0.5", "0.00", "1.000", "-0"])
def test_mapping_probability_passes(value):
    assert binary_outcome_probability_record_from_mapping(valid_mapping() | {"probability": value})[1].passed


@pytest.mark.parametrize(("value", "code"), [
    (Decimal("-0.000000000000000001"), Code.PROBABILITY_OUT_OF_RANGE),
    (Decimal("1.000000000000000001"), Code.PROBABILITY_OUT_OF_RANGE),
    (True, Code.INVALID_PROBABILITY_TYPE), (1, Code.INVALID_PROBABILITY_TYPE),
    (0.5, Code.INVALID_PROBABILITY_TYPE), ("abc", Code.INVALID_PROBABILITY_TYPE),
    (" 0.5", Code.INVALID_PROBABILITY_TYPE), ("0.5 ", Code.INVALID_PROBABILITY_TYPE),
    ("1e-2", Code.INVALID_PROBABILITY_TYPE), ("+0.5", Code.INVALID_PROBABILITY_TYPE),
    (".5", Code.INVALID_PROBABILITY_TYPE), ("1.", Code.INVALID_PROBABILITY_TYPE),
    ("00.5", Code.INVALID_PROBABILITY_TYPE), ("１", Code.INVALID_PROBABILITY_TYPE),
    ("١", Code.INVALID_PROBABILITY_TYPE), ("1٢", Code.INVALID_PROBABILITY_TYPE),
    ("0٫5", Code.INVALID_PROBABILITY_TYPE), ("1_0", Code.INVALID_PROBABILITY_TYPE),
    (StringSubclass("0.5"), Code.INVALID_PROBABILITY_TYPE), (OtherEnum.VALUE, Code.INVALID_PROBABILITY_TYPE),
    (Decimal("NaN"), Code.NON_FINITE_PROBABILITY), (Decimal("-NaN"), Code.NON_FINITE_PROBABILITY),
    (Decimal("sNaN"), Code.NON_FINITE_PROBABILITY), ("NaN", Code.NON_FINITE_PROBABILITY),
    ("-NaN", Code.NON_FINITE_PROBABILITY), ("sNaN", Code.NON_FINITE_PROBABILITY),
    (Decimal("Infinity"), Code.NON_FINITE_PROBABILITY), (Decimal("-Infinity"), Code.NON_FINITE_PROBABILITY),
    ("Infinity", Code.NON_FINITE_PROBABILITY), ("+Infinity", Code.NON_FINITE_PROBABILITY),
    ("-Infinity", Code.NON_FINITE_PROBABILITY),
])
def test_mapping_probability_rejections_are_exact(value, code):
    assert mapping_codes(valid_mapping() | {"probability": value}) == (code,)


def test_mapping_timestamps_and_chronology():
    assert binary_outcome_probability_record_from_mapping(valid_mapping() | {
        "prediction_as_of": "2026-01-02T03:04:05+05:30",
        "input_publication_available_at": "2026-01-01T21:34:05+00:00",
        "created_at": "2026-01-01T21:34:05-04:00",
    })[1].passed
    for field in TIMESTAMP_FIELDS:
        assert mapping_codes(valid_mapping() | {field: "bad"}) == (Code.INVALID_TIMESTAMP,)
        assert mapping_codes(valid_mapping() | {field: "2026-01-02T03:04:05"}) == (Code.INVALID_TIMESTAMP,)
        assert mapping_codes(valid_mapping() | {field: 3}) == (Code.INVALID_TIMESTAMP,)
    assert mapping_codes(valid_mapping() | {"prediction_as_of": "bad", "input_publication_available_at": "bad2", "created_at": 3}) == (
        Code.INVALID_TIMESTAMP, Code.INVALID_TIMESTAMP, Code.INVALID_TIMESTAMP,
    )
    assert mapping_codes(valid_mapping() | {"input_publication_available_at": "2026-01-02T03:04:06+00:00"}) == (Code.INPUT_AVAILABLE_AFTER_PREDICTION,)
    assert mapping_codes(valid_mapping() | {"created_at": "2026-01-02T03:04:04+00:00"}) == (Code.CREATED_BEFORE_PREDICTION,)
    assert mapping_codes(valid_mapping() | {"prediction_as_of": "bad", "input_publication_available_at": "2999-01-02T03:04:06+00:00", "created_at": "1999-01-02T03:04:04+00:00"}) == (Code.INVALID_TIMESTAMP,)


def test_mapping_provenance_and_supersession():
    for value in [("a", "b"), ["b", "a", "b"]]:
        record, result = binary_outcome_probability_record_from_mapping(valid_mapping() | {"provenance_refs": value})
        assert result.passed and record is not None
        assert record.provenance_refs == tuple(value)
    for value in [(), []]:
        assert mapping_codes(valid_mapping() | {"provenance_refs": value}) == (Code.EMPTY_PROVENANCE_REFS,)
    assert mapping_codes(valid_mapping() | {"provenance_refs": "ref"}) == (Code.INVALID_PROVENANCE_REF,)
    assert mapping_codes(valid_mapping() | {"provenance_refs": ["", 1, "ok", " "]}) == (Code.INVALID_PROVENANCE_REF, Code.INVALID_PROVENANCE_REF, Code.INVALID_PROVENANCE_REF)
    assert binary_outcome_probability_record_from_mapping(valid_mapping() | {"supersedes_prediction_record_id": "other"})[1].passed
    assert mapping_codes(valid_mapping() | {"supersedes_prediction_record_id": "pred-1"}) == (Code.SELF_SUPERSESSION,)


@pytest.mark.parametrize("bad", ["", "   ", 7])
def test_direct_required_text_fields_and_optional_supersession(bad):
    for field in TEXT_FIELDS:
        assert direct_codes(valid_record(**{field: bad})) == (Code.BLANK_REQUIRED_TEXT,)
    assert direct_codes(valid_record(prediction_record_id="", condition_id=7, token_id=" ")) == (
        Code.BLANK_REQUIRED_TEXT, Code.BLANK_REQUIRED_TEXT, Code.BLANK_REQUIRED_TEXT,
    )
    assert direct_codes(valid_record(supersedes_prediction_record_id=bad)) == (Code.BLANK_REQUIRED_TEXT,)


@pytest.mark.parametrize("value", ["binary_outcome_probability", "unknown", OtherEnum.VALUE, object()])
def test_direct_representation_rejected(value):
    assert direct_codes(valid_record(prediction_representation=value)) == (Code.INVALID_PREDICTION_REPRESENTATION,)


@pytest.mark.parametrize("value", [Decimal("0"), Decimal("1"), Decimal("0.123456789123456789")])
def test_direct_decimal_probability_passes(value):
    assert validate_binary_outcome_probability_record(valid_record(probability=value)).passed


@pytest.mark.parametrize(("value", "code"), [
    (True, Code.INVALID_PROBABILITY_TYPE), (1, Code.INVALID_PROBABILITY_TYPE),
    (0.5, Code.INVALID_PROBABILITY_TYPE), ("0.5", Code.INVALID_PROBABILITY_TYPE),
    ("bad", Code.INVALID_PROBABILITY_TYPE), (object(), Code.INVALID_PROBABILITY_TYPE),
    (Decimal("-0.1"), Code.PROBABILITY_OUT_OF_RANGE), (Decimal("1.1"), Code.PROBABILITY_OUT_OF_RANGE),
    (Decimal("NaN"), Code.NON_FINITE_PROBABILITY), (Decimal("Infinity"), Code.NON_FINITE_PROBABILITY),
    (Decimal("-Infinity"), Code.NON_FINITE_PROBABILITY),
])
def test_direct_probability_failures(value, code):
    assert direct_codes(valid_record(probability=value)) == (code,)


def test_direct_timestamps_chronology_and_suppression():
    for field in TIMESTAMP_FIELDS:
        assert direct_codes(valid_record(**{field: "bad"})) == (Code.INVALID_TIMESTAMP,)
        assert direct_codes(valid_record(**{field: "2026-01-02T03:04:05"})) == (Code.INVALID_TIMESTAMP,)
        assert direct_codes(valid_record(**{field: 3})) == (Code.INVALID_TIMESTAMP,)
    assert direct_codes(valid_record(prediction_as_of="bad", input_publication_available_at="bad2", created_at=3)) == (
        Code.INVALID_TIMESTAMP, Code.INVALID_TIMESTAMP, Code.INVALID_TIMESTAMP,
    )
    assert direct_codes(valid_record(input_publication_available_at="2026-01-02T03:04:06+00:00")) == (Code.INPUT_AVAILABLE_AFTER_PREDICTION,)
    assert direct_codes(valid_record(created_at="2026-01-02T03:04:04+00:00")) == (Code.CREATED_BEFORE_PREDICTION,)
    assert direct_codes(valid_record(prediction_as_of="bad", input_publication_available_at="2999-01-02T03:04:06+00:00", created_at="1999-01-02T03:04:04+00:00")) == (Code.INVALID_TIMESTAMP,)


def test_direct_provenance_and_supersession():
    assert direct_codes(valid_record(provenance_refs=["a", "b"])) == (Code.INVALID_PROVENANCE_REF,)
    assert direct_codes(valid_record(provenance_refs=[])) == (Code.INVALID_PROVENANCE_REF,)
    assert direct_codes(valid_record(provenance_refs="ref")) == (Code.INVALID_PROVENANCE_REF,)
    assert direct_codes(valid_record(provenance_refs=())) == (Code.EMPTY_PROVENANCE_REFS,)
    assert direct_codes(valid_record(provenance_refs=("", 1, "ok", " "))) == (Code.INVALID_PROVENANCE_REF, Code.INVALID_PROVENANCE_REF, Code.INVALID_PROVENANCE_REF)
    assert validate_binary_outcome_probability_record(valid_record(supersedes_prediction_record_id="other")).passed
    assert direct_codes(valid_record(supersedes_prediction_record_id="pred-1")) == (Code.SELF_SUPERSESSION,)


def test_deterministic_combined_mapping_and_direct_failures():
    mapping = valid_mapping(); mapping.pop("outcome"); mapping.pop("token_id")
    mapping.update({"z": 1, "a": 2, "prediction_record_id": "", "condition_id": 7,
                    "prediction_representation": "bad", "probability": "1e-2",
                    "prediction_as_of": "bad", "input_publication_available_at": "bad2",
                    "created_at": "bad3", "provenance_refs": ["", 2]})
    expected_mapping = (
        Code.MISSING_REQUIRED_FIELD, Code.MISSING_REQUIRED_FIELD,
        Code.UNEXPECTED_FIELD, Code.UNEXPECTED_FIELD,
        Code.BLANK_REQUIRED_TEXT, Code.BLANK_REQUIRED_TEXT,
        Code.INVALID_PREDICTION_REPRESENTATION, Code.INVALID_PROBABILITY_TYPE,
        Code.INVALID_TIMESTAMP, Code.INVALID_TIMESTAMP, Code.INVALID_TIMESTAMP,
        Code.INVALID_PROVENANCE_REF, Code.INVALID_PROVENANCE_REF,
    )
    direct = valid_record(prediction_record_id="", condition_id=7, prediction_representation="bad",
                          probability="1e-2", prediction_as_of="bad",
                          input_publication_available_at="bad2", created_at="bad3",
                          provenance_refs=("", 2), supersedes_prediction_record_id="")
    expected_direct = (
        Code.BLANK_REQUIRED_TEXT, Code.BLANK_REQUIRED_TEXT, Code.BLANK_REQUIRED_TEXT,
        Code.INVALID_PREDICTION_REPRESENTATION, Code.INVALID_PROBABILITY_TYPE,
        Code.INVALID_TIMESTAMP, Code.INVALID_TIMESTAMP, Code.INVALID_TIMESTAMP,
        Code.INVALID_PROVENANCE_REF, Code.INVALID_PROVENANCE_REF,
    )
    for _ in range(3):
        assert mapping_codes(mapping) == expected_mapping
        assert direct_codes(direct) == expected_direct


def test_static_safety_audits_for_production_and_test_modules():
    production_tree = ast.parse(Path(mod.__file__).read_text())
    test_tree = ast.parse(Path(__file__).read_text())
    forbidden_names = {"open", "PathLike", "exec", "eval", "__import__"}
    forbidden_attrs = {"now", "utcnow", "today", "insert", "remove", "sort"}
    for tree in (production_tree, test_tree):
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    assert alias.name.split(".")[0] not in {"os", "socket", "http", "urllib", "requests", "subprocess", "sqlite3", "duckdb", "psycopg"}
            if isinstance(node, ast.ImportFrom):
                root = (node.module or "").split(".")[0]
                if tree is production_tree:
                    assert root != "meg"
                assert root not in {"os", "socket", "http", "urllib", "requests", "subprocess", "sqlite3", "duckdb", "psycopg"}
            if isinstance(node, ast.Name):
                assert node.id not in forbidden_names
            if isinstance(node, ast.Attribute):
                assert node.attr not in forbidden_attrs
    direct_node = next(node for node in production_tree.body if isinstance(node, ast.FunctionDef) and node.name == "validate_binary_outcome_probability_record")
    for node in ast.walk(direct_node):
        assert not isinstance(node, ast.Set)
        assert not (isinstance(node, ast.ListComp) and isinstance(node.elt, ast.Name) and node.elt.id == "c")
        assert not (isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "sorted")
