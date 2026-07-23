from __future__ import annotations

import ast
import dataclasses
import inspect
from collections.abc import Mapping
from dataclasses import FrozenInstanceError
from enum import Enum
from pathlib import Path
from typing import get_type_hints

import pytest

from meg.weather.stage3.strict_oos_split import (
    OverlapControlPosture,
    SplitApplicabilityMode,
    SplitAssignmentStatus,
    SplitRole,
    SplitValidationCode,
    SplitValidationSeverity,
    StrictOOSSplitAssignment,
    StrictOOSSplitValidationResult,
    strict_oos_split_assignment_from_mapping,
    validate_strict_oos_split_assignment,
    validate_strict_oos_split_assignments,
)
import meg.weather.stage3.strict_oos_split as module

C = SplitValidationCode

API = (
    "SplitRole", "SplitApplicabilityMode", "SplitAssignmentStatus", "OverlapControlPosture",
    "SplitValidationSeverity", "SplitValidationCode", "StrictOOSSplitAssignment",
    "StrictOOSSplitValidationResult", "strict_oos_split_assignment_from_mapping",
    "validate_strict_oos_split_assignment", "validate_strict_oos_split_assignments",
)
REQUIRED_KEYS = (
    "split_assignment_id", "split_id", "split_version", "fold_id", "fold_index",
    "prediction_record_id", "condition_id", "token_id", "outcome", "settlement_rule_id",
    "settlement_rule_version", "split_role", "applicability_modes", "assignment_status",
    "fold_cutoff", "prediction_as_of", "input_publication_available_at", "target_start_at",
    "target_end_at", "label_available_at", "leakage_group_id", "overlap_control_posture",
    "primary_split_posture", "tuning_posture", "calibration_posture", "baseline_parity_posture",
    "exclusion_reason", "provenance_refs", "created_at",
)
REQUIRED_TEXT = (
    "split_assignment_id", "split_id", "split_version", "fold_id", "prediction_record_id",
    "condition_id", "token_id", "outcome", "settlement_rule_id", "settlement_rule_version",
    "leakage_group_id", "primary_split_posture", "tuning_posture", "calibration_posture",
    "baseline_parity_posture",
)
TIMES = (
    "fold_cutoff", "prediction_as_of", "input_publication_available_at", "target_start_at",
    "target_end_at", "label_available_at", "created_at",
)
FIXED = (("primary_split_posture", "rolling_origin_or_walk_forward_required"), ("tuning_posture", "train_or_calibration_only"), ("calibration_posture", "separate_when_required"), ("baseline_parity_posture", "same_folds_and_eligibility_required"))


def good(**overrides):
    data = {
        "split_assignment_id": "assign-1", "split_id": "split-1", "split_version": "v1", "fold_id": "fold-1", "fold_index": 0,
        "prediction_record_id": "pred-1", "condition_id": "cond-1", "token_id": "tok-1", "outcome": "yes", "settlement_rule_id": "rule-1",
        "settlement_rule_version": "rv1", "split_role": SplitRole.TEST, "applicability_modes": (SplitApplicabilityMode.PRIMARY_TEMPORAL, SplitApplicabilityMode.LEAVE_YEAR_OUT),
        "assignment_status": SplitAssignmentStatus.ASSIGNED, "fold_cutoff": "2025-01-01T00:00:00+00:00", "prediction_as_of": "2025-01-01T00:00:00+00:00",
        "input_publication_available_at": "2025-01-01T00:00:00+00:00", "target_start_at": "2025-01-02T00:00:00+00:00", "target_end_at": "2025-01-03T00:00:00+00:00",
        "label_available_at": None, "leakage_group_id": "lg-1", "overlap_control_posture": OverlapControlPosture.SATISFIED,
        "primary_split_posture": "rolling_origin_or_walk_forward_required", "tuning_posture": "train_or_calibration_only", "calibration_posture": "separate_when_required",
        "baseline_parity_posture": "same_folds_and_eligibility_required", "exclusion_reason": None, "provenance_refs": ("prd:369", "ticket:strict"),
        "created_at": "2025-01-01T00:00:00+00:00", "supersedes_split_assignment_id": None,
    }
    data.update(overrides)
    return StrictOOSSplitAssignment(**data)


def mapping(**overrides):
    data = good().__dict__.copy()
    data.update(overrides)
    return data


def assert_codes(subject, expected):
    result = subject if isinstance(subject, StrictOOSSplitValidationResult) else validate_strict_oos_split_assignment(subject)
    assert result.codes == expected
    assert result.passed is (expected == ())
    assert result.severity is (SplitValidationSeverity.PASSED if expected == () else SplitValidationSeverity.BLOCKED)


def test_public_contract_is_frozen_completely():
    assert module.__all__ == API
    tree = ast.parse(Path(module.__file__).read_text())
    public_defs = [n.name for n in tree.body if isinstance(n, (ast.ClassDef, ast.FunctionDef)) and not n.name.startswith("_")]
    assert public_defs == list(API)
    assert [(m.name, m.value) for m in SplitRole] == [("TRAIN", "train"), ("CALIBRATION", "calibration"), ("TEST", "test")]
    assert [(m.name, m.value) for m in SplitApplicabilityMode] == [("PRIMARY_TEMPORAL", "primary_temporal"), ("LEAVE_STATION_OUT", "leave_station_out"), ("LEAVE_YEAR_OUT", "leave_year_out"), ("FAMILY_STRATIFIED", "family_stratified"), ("SEASON_OR_REGIME_STRATIFIED", "season_or_regime_stratified")]
    assert [(m.name, m.value) for m in SplitAssignmentStatus] == [("ASSIGNED", "assigned"), ("BLOCKED", "blocked")]
    assert [(m.name, m.value) for m in OverlapControlPosture] == [("NOT_REQUIRED", "not_required"), ("SATISFIED", "satisfied"), ("UNSATISFIED", "unsatisfied")]
    assert [(m.name, m.value) for m in SplitValidationSeverity] == [("PASSED", "passed"), ("BLOCKED", "blocked")]
    assert [(m.name, m.value) for m in SplitValidationCode] == [("MISSING_REQUIRED_FIELD", "missing_required_field"), ("UNEXPECTED_FIELD", "unexpected_field"), ("BLANK_REQUIRED_TEXT", "blank_required_text"), ("INVALID_SPLIT_ROLE", "invalid_split_role"), ("INVALID_APPLICABILITY_MODES", "invalid_applicability_modes"), ("INVALID_ASSIGNMENT_STATUS", "invalid_assignment_status"), ("INVALID_OVERLAP_CONTROL_POSTURE", "invalid_overlap_control_posture"), ("INVALID_INTEGER_FIELD", "invalid_integer_field"), ("INVALID_FIXED_POSTURE", "invalid_fixed_posture"), ("INVALID_TIMESTAMP", "invalid_timestamp"), ("INPUT_AVAILABLE_AFTER_PREDICTION", "input_available_after_prediction"), ("PREDICTION_AFTER_FOLD_CUTOFF", "prediction_after_fold_cutoff"), ("INVALID_TARGET_WINDOW", "invalid_target_window"), ("TRAIN_OR_CALIBRATION_AFTER_CUTOFF", "train_or_calibration_after_cutoff"), ("TRAIN_OR_CALIBRATION_LABEL_UNAVAILABLE_BY_CUTOFF", "train_or_calibration_label_unavailable_by_cutoff"), ("TEST_NOT_STRICTLY_AFTER_CUTOFF", "test_not_strictly_after_cutoff"), ("TEST_LABEL_AVAILABLE_BY_CUTOFF", "test_label_available_by_cutoff"), ("ASSIGNED_WITH_EXCLUSION_REASON", "assigned_with_exclusion_reason"), ("BLOCKED_WITHOUT_EXCLUSION_REASON", "blocked_without_exclusion_reason"), ("UNSATISFIED_OVERLAP_CONTROL_ASSIGNED", "unsatisfied_overlap_control_assigned"), ("EMPTY_PROVENANCE_REFS", "empty_provenance_refs"), ("INVALID_PROVENANCE_REF", "invalid_provenance_ref"), ("SELF_SUPERSESSION", "self_supersession"), ("INVALID_ASSIGNMENT_COLLECTION_TYPE", "invalid_assignment_collection_type"), ("EMPTY_ASSIGNMENT_COLLECTION", "empty_assignment_collection"), ("DUPLICATE_ASSIGNMENT_ID", "duplicate_assignment_id"), ("DUPLICATE_FOLD_RECORD_ASSIGNMENT", "duplicate_fold_record_assignment"), ("DUPLICATE_TEST_RECORD", "duplicate_test_record"), ("INCONSISTENT_SPLIT_ID", "inconsistent_split_id"), ("INCONSISTENT_SPLIT_VERSION", "inconsistent_split_version"), ("INCONSISTENT_FOLD_DEFINITION", "inconsistent_fold_definition"), ("NON_MONOTONIC_FOLD_CUTOFF", "non_monotonic_fold_cutoff"), ("LEAKAGE_GROUP_ROLE_CONFLICT", "leakage_group_role_conflict")]
    assert [f.name for f in dataclasses.fields(StrictOOSSplitAssignment)] == list(REQUIRED_KEYS) + ["supersedes_split_assignment_id"]
    hints = get_type_hints(StrictOOSSplitAssignment)
    assert hints["fold_index"] is int
    assert hints["split_role"] is SplitRole
    assert hints["applicability_modes"] == tuple[SplitApplicabilityMode, ...]
    assert dataclasses.fields(StrictOOSSplitAssignment)[-1].default is None
    assert [f.name for f in dataclasses.fields(StrictOOSSplitValidationResult)] == ["severity", "passed", "codes"]
    assert get_type_hints(StrictOOSSplitValidationResult)["codes"] == tuple[SplitValidationCode, ...]
    assert dataclasses.fields(StrictOOSSplitValidationResult)[2].default == ()
    with pytest.raises(FrozenInstanceError):
        good().split_id = "new"
    with pytest.raises(FrozenInstanceError):
        StrictOOSSplitValidationResult(SplitValidationSeverity.PASSED, True).passed = False
    sig = inspect.signature(strict_oos_split_assignment_from_mapping)
    assert list(sig.parameters) == ["mapping"]
    assert sig.return_annotation == "tuple[StrictOOSSplitAssignment | None, StrictOOSSplitValidationResult]"
    assert inspect.signature(validate_strict_oos_split_assignment).return_annotation == "StrictOOSSplitValidationResult"
    assert inspect.signature(validate_strict_oos_split_assignments).return_annotation == "StrictOOSSplitValidationResult"
    assert module._REQUIRED_MAPPING_KEYS == REQUIRED_KEYS
    assert module._OPTIONAL_MAPPING_KEYS == ("supersedes_split_assignment_id",)
    assert module._REQUIRED_TEXT_FIELDS == REQUIRED_TEXT
    assert module._NULLABLE_TEXT_FIELDS == ("exclusion_reason", "supersedes_split_assignment_id")
    assert module._TIMESTAMP_FIELDS == TIMES
    assert module._FIXED_POSTURES == FIXED


def test_mapping_root_shape_and_hostile_fail_closed():
    expected = (C.MISSING_REQUIRED_FIELD,) * 29
    for value in (None, "x", [], (), object()):
        record, result = strict_oos_split_assignment_from_mapping(value)
        assert record is None
        assert result.codes == expected

    class Hostile(Mapping):
        def __init__(self, mode): self.mode = mode
        def items(self):
            if self.mode == "items": raise RuntimeError("items")
            if self.mode == "iter": return BrokenIter()
            if self.mode == "three": return [("a", "b", "c")]
            if self.mode == "scalar": return [1]
            return [BadEntry()]
        def __iter__(self): return iter(())
        def __len__(self): return 0
        def __getitem__(self, key): raise RuntimeError("get")
    class BrokenIter:
        def __iter__(self): raise RuntimeError("iter")
    class BadEntry:
        def __iter__(self): raise RuntimeError("entry")

    for mode in ("items", "iter", "three", "scalar", "key"):
        record, result = strict_oos_split_assignment_from_mapping(Hostile(mode))
        assert record is None
        assert result.codes == expected

    assert strict_oos_split_assignment_from_mapping({})[1].codes == expected
    for missing in REQUIRED_KEYS:
        d = mapping()
        d.pop(missing)
        assert strict_oos_split_assignment_from_mapping(d)[1].codes == (C.MISSING_REQUIRED_FIELD,)
    d = mapping(); d.pop("split_id"); d.pop("fold_id")
    assert strict_oos_split_assignment_from_mapping(d)[1].codes == (C.MISSING_REQUIRED_FIELD, C.MISSING_REQUIRED_FIELD)
    forbidden = "mar" + "ket" + "_" + "id"
    assert strict_oos_split_assignment_from_mapping({**mapping(), forbidden: "x"})[1].codes == (C.UNEXPECTED_FIELD,)
    assert strict_oos_split_assignment_from_mapping({**mapping(), "z": 1, "a": 2, 9: 3, (1,): 4})[1].codes == (C.UNEXPECTED_FIELD, C.UNEXPECTED_FIELD, C.UNEXPECTED_FIELD, C.UNEXPECTED_FIELD)

    class S(str): pass
    d = mapping(); d.pop("condition_id"); d[S("condition_id")] = "x"
    assert strict_oos_split_assignment_from_mapping(d)[1].codes == (C.MISSING_REQUIRED_FIELD, C.UNEXPECTED_FIELD)


def test_mapping_adaptation_success_and_direct_non_adaptation():
    data = mapping(split_role="test", assignment_status="assigned", overlap_control_posture="satisfied", applicability_modes=["primary_temporal", "leave_year_out"], provenance_refs=["a", "a"])
    record, result = strict_oos_split_assignment_from_mapping(data)
    assert result.codes == ()
    assert record.split_role is SplitRole.TEST
    assert record.applicability_modes == (SplitApplicabilityMode.PRIMARY_TEMPORAL, SplitApplicabilityMode.LEAVE_YEAR_OUT)
    assert record.provenance_refs == ("a", "a")
    assert data["applicability_modes"] == ["primary_temporal", "leave_year_out"]
    assert_codes(good(split_role="test"), (C.INVALID_SPLIT_ROLE,))
    assert_codes(good(applicability_modes=[SplitApplicabilityMode.PRIMARY_TEMPORAL]), (C.INVALID_APPLICABILITY_MODES,))
    assert_codes(good(provenance_refs=["a"]), (C.INVALID_PROVENANCE_REF,))


def test_direct_required_text_fields_individually_and_fixed_exactness():
    class S(str): pass
    for field in REQUIRED_TEXT:
        if field in dict(FIXED):
            expected = (C.BLANK_REQUIRED_TEXT, C.INVALID_FIXED_POSTURE)
        else:
            expected = (C.BLANK_REQUIRED_TEXT,)
        assert_codes(good(**{field: " "}), expected)
        assert_codes(good(**{field: 4}), expected)
        value = S(dict(FIXED).get(field, "valid"))
        assert_codes(good(**{field: value}), expected)
    assert_codes(good(fold_cutoff=""), (C.INVALID_TIMESTAMP,))
    assert_codes(good(created_at=4), (C.INVALID_TIMESTAMP,))
    assert_codes(good(primary_split_posture="wrong", tuning_posture="wrong"), (C.INVALID_FIXED_POSTURE, C.INVALID_FIXED_POSTURE))


def test_enums_applicability_integer_and_provenance_failures():
    class S(str): pass
    class I(int): pass
    class Other(Enum): TEST = "test"
    assert_codes(good(split_role=S("test")), (C.INVALID_SPLIT_ROLE,))
    assert_codes(good(assignment_status=Other.TEST), (C.INVALID_ASSIGNMENT_STATUS,))
    assert_codes(good(overlap_control_posture=S("satisfied")), (C.INVALID_OVERLAP_CONTROL_POSTURE,))
    for value in ([], (), ["leave_year_out"], ["primary_temporal", "primary_temporal"], (SplitApplicabilityMode.PRIMARY_TEMPORAL, "leave_year_out"), "primary_temporal"):
        assert_codes(good(applicability_modes=value), (C.INVALID_APPLICABILITY_MODES,))
    for value in (False, I(1), -1, "1"):
        assert_codes(good(fold_index=value), (C.INVALID_INTEGER_FIELD,))
    assert_codes(good(provenance_refs={"x"}), (C.INVALID_PROVENANCE_REF,))
    assert_codes(good(provenance_refs=()), (C.EMPTY_PROVENANCE_REFS,))
    assert_codes(good(provenance_refs=("", 3, "ok", "ok")), (C.INVALID_PROVENANCE_REF, C.INVALID_PROVENANCE_REF))


def test_timestamp_temporal_role_label_status_and_supersession_order():
    for field in TIMES:
        value = None if field == "label_available_at" else "bad"
        if field == "label_available_at":
            assert_codes(good(split_role=SplitRole.TRAIN, label_available_at=None), (C.TRAIN_OR_CALIBRATION_AFTER_CUTOFF, C.TRAIN_OR_CALIBRATION_LABEL_UNAVAILABLE_BY_CUTOFF))
        else:
            assert_codes(good(**{field: value}), (C.INVALID_TIMESTAMP,))
        assert_codes(good(**{field: "2025-01-01T00:00:00"}), (C.INVALID_TIMESTAMP,))
    assert_codes(good(input_publication_available_at="2025-01-01T00:00:01+00:00", prediction_as_of="2025-01-01T00:00:00+00:00", target_start_at="2025-01-04T00:00:00+00:00", target_end_at="2025-01-03T00:00:00+00:00"), (C.INPUT_AVAILABLE_AFTER_PREDICTION, C.INVALID_TARGET_WINDOW))
    assert_codes(good(fold_cutoff="2024-12-31T23:59:59+00:00"), (C.PREDICTION_AFTER_FOLD_CUTOFF,))
    assert_codes(good(fold_cutoff="bad", prediction_as_of="2026-01-01T00:00:00+00:00"), (C.INVALID_TIMESTAMP,))
    assert validate_strict_oos_split_assignment(good(fold_cutoff="2024-12-31T22:00:00+00:00", prediction_as_of="2024-12-31T22:00:00+00:00", input_publication_available_at="2024-12-31T22:00:00+00:00", target_start_at="2025-01-01T00:00:00+01:00", target_end_at="2024-12-31T23:00:00+00:00")).codes == ()
    assert_codes(good(split_role=SplitRole.TRAIN, label_available_at="bad"), (C.INVALID_TIMESTAMP, C.TRAIN_OR_CALIBRATION_AFTER_CUTOFF, C.TRAIN_OR_CALIBRATION_LABEL_UNAVAILABLE_BY_CUTOFF))
    assert_codes(good(split_role=SplitRole.CALIBRATION, label_available_at="2025-01-01T00:00:00+00:00", target_start_at="2025-01-01T00:00:00+00:00", target_end_at="2025-01-01T00:00:00+00:00"), ())
    assert_codes(good(split_role=SplitRole.TEST, target_start_at="2025-01-01T00:00:00+00:00", label_available_at="2025-01-01T00:00:00+00:00", exclusion_reason="x", overlap_control_posture=OverlapControlPosture.UNSATISFIED), (C.TEST_NOT_STRICTLY_AFTER_CUTOFF, C.TEST_LABEL_AVAILABLE_BY_CUTOFF, C.ASSIGNED_WITH_EXCLUSION_REASON, C.UNSATISFIED_OVERLAP_CONTROL_ASSIGNED))
    assert_codes(good(assignment_status=SplitAssignmentStatus.BLOCKED, target_start_at="2025-01-01T00:00:00+00:00", exclusion_reason=None, overlap_control_posture=OverlapControlPosture.UNSATISFIED), (C.BLOCKED_WITHOUT_EXCLUSION_REASON,))
    assert_codes(good(exclusion_reason=" "), (C.BLANK_REQUIRED_TEXT, C.ASSIGNED_WITH_EXCLUSION_REASON))
    assert_codes(good(supersedes_split_assignment_id="assign-1"), (C.SELF_SUPERSESSION,))
    assert_codes(good(split_assignment_id=" ", supersedes_split_assignment_id=" "), (C.BLANK_REQUIRED_TEXT, C.BLANK_REQUIRED_TEXT))


def test_mapping_combined_exact_ordering_cases():
    assert strict_oos_split_assignment_from_mapping(mapping(extra="x", fold_cutoff="bad", created_at="bad", provenance_refs=["", 3]))[1].codes == (C.UNEXPECTED_FIELD, C.INVALID_TIMESTAMP, C.INVALID_TIMESTAMP, C.INVALID_PROVENANCE_REF, C.INVALID_PROVENANCE_REF)
    d = mapping(primary_split_posture="", tuning_posture="wrong", input_publication_available_at="2025-01-01T00:00:01+00:00")
    d.pop("split_id"); d.pop("fold_id")
    assert strict_oos_split_assignment_from_mapping(d)[1].codes == (C.MISSING_REQUIRED_FIELD, C.MISSING_REQUIRED_FIELD, C.BLANK_REQUIRED_TEXT, C.INVALID_FIXED_POSTURE, C.INVALID_FIXED_POSTURE, C.INPUT_AVAILABLE_AFTER_PREDICTION)
    assert strict_oos_split_assignment_from_mapping(mapping(exclusion_reason=" "))[1].codes == (C.BLANK_REQUIRED_TEXT, C.ASSIGNED_WITH_EXCLUSION_REASON)
    assert strict_oos_split_assignment_from_mapping(mapping(unexpected="x", supersedes_split_assignment_id="assign-1"))[1].codes == (C.UNEXPECTED_FIELD, C.SELF_SUPERSESSION)
    assert strict_oos_split_assignment_from_mapping(mapping(applicability_modes=[], fold_index=-1))[1].codes == (C.INVALID_APPLICABILITY_MODES, C.INVALID_INTEGER_FIELD)
    assert strict_oos_split_assignment_from_mapping(mapping(split_role="bad", assignment_status="bad", overlap_control_posture="bad"))[1].codes == (C.INVALID_SPLIT_ROLE, C.INVALID_ASSIGNMENT_STATUS, C.INVALID_OVERLAP_CONTROL_POSTURE)


def test_collection_all_categories_repeated_and_ordered():
    assert validate_strict_oos_split_assignments([]).codes == (C.INVALID_ASSIGNMENT_COLLECTION_TYPE,)
    assert validate_strict_oos_split_assignments(()).codes == (C.EMPTY_ASSIGNMENT_COLLECTION,)
    r1 = good(split_assignment_id="a1", fold_id="f1", fold_index=0, prediction_record_id="p1", split_role=SplitRole.TEST)
    r2 = good(split_assignment_id="a1", fold_id="f2", fold_index=1, prediction_record_id="p1", split_role=SplitRole.TEST, fold_cutoff="2025-01-02T00:00:00+00:00", target_start_at="2025-01-03T00:00:00+00:00", target_end_at="2025-01-04T00:00:00+00:00")
    r3 = good(split_assignment_id="a1", fold_id="f2", fold_index=1, prediction_record_id="p1", split_id="split-2", split_version="v2", split_role=SplitRole.TRAIN, fold_cutoff="2025-01-02T00:00:00+00:00", target_start_at="2025-01-01T00:00:00+00:00", target_end_at="2025-01-01T00:00:00+00:00", label_available_at="2025-01-01T00:00:00+00:00")
    assert validate_strict_oos_split_assignments(("bad", r1, r2, r3)).codes == (C.INVALID_ASSIGNMENT_COLLECTION_TYPE, C.DUPLICATE_ASSIGNMENT_ID, C.DUPLICATE_ASSIGNMENT_ID, C.DUPLICATE_FOLD_RECORD_ASSIGNMENT, C.DUPLICATE_TEST_RECORD, C.INCONSISTENT_SPLIT_ID, C.INCONSISTENT_SPLIT_VERSION, C.LEAKAGE_GROUP_ROLE_CONFLICT)
    same_fold = good(split_assignment_id="a2", fold_id="f1", prediction_record_id="p1")
    assert validate_strict_oos_split_assignments((r1, same_fold)).codes == (C.DUPLICATE_FOLD_RECORD_ASSIGNMENT,)
    conflict_fold = good(split_assignment_id="a3", fold_id="f1", fold_index=2, prediction_record_id="p3", fold_cutoff="2025-01-01T00:00:00+01:00", prediction_as_of="2024-12-31T23:00:00+00:00", input_publication_available_at="2024-12-31T23:00:00+00:00")
    conflict_index = good(split_assignment_id="a4", fold_id="f4", fold_index=0, prediction_record_id="p4", fold_cutoff="2025-01-01T00:00:00+01:00", prediction_as_of="2024-12-31T23:00:00+00:00", input_publication_available_at="2024-12-31T23:00:00+00:00")
    assert validate_strict_oos_split_assignments((r1, conflict_fold, conflict_index)).codes == (C.INCONSISTENT_FOLD_DEFINITION, C.INCONSISTENT_FOLD_DEFINITION)
    equal_cutoff = good(split_assignment_id="a5", fold_id="f3", fold_index=3, prediction_record_id="p5", fold_cutoff="2025-01-01T00:00:00+00:00", target_start_at="2025-01-04T00:00:00+00:00", target_end_at="2025-01-05T00:00:00+00:00")
    reverse = good(split_assignment_id="a6", fold_id="f4", fold_index=4, prediction_record_id="p6", fold_cutoff="2024-12-31T00:00:00+00:00", prediction_as_of="2024-12-31T00:00:00+00:00", input_publication_available_at="2024-12-31T00:00:00+00:00", target_start_at="2025-01-05T00:00:00+00:00", target_end_at="2025-01-06T00:00:00+00:00")
    assert validate_strict_oos_split_assignments((r1, equal_cutoff, reverse)).codes == (C.NON_MONOTONIC_FOLD_CUTOFF, C.NON_MONOTONIC_FOLD_CUTOFF)
    unrelated_bad = good(split_assignment_id="a7", prediction_record_id="p7", split_role=SplitRole.TRAIN, target_end_at="2025-01-02T00:00:00+00:00", label_available_at="2025-01-01T00:00:00+00:00")
    duplicate_bad = good(split_assignment_id="a7", prediction_record_id="p8", leakage_group_id="lg-2")
    assert validate_strict_oos_split_assignments((unrelated_bad, duplicate_bad)).codes == (C.TRAIN_OR_CALIBRATION_AFTER_CUTOFF, C.DUPLICATE_ASSIGNMENT_ID)
    assert validate_strict_oos_split_assignments((unrelated_bad, duplicate_bad)).codes == (C.TRAIN_OR_CALIBRATION_AFTER_CUTOFF, C.DUPLICATE_ASSIGNMENT_ID)


def test_source_audit_static_boundaries_and_canonical_token_absence():
    prod = Path("meg/weather/stage3/strict_oos_split.py").read_text()
    test = Path("tests/core/test_weather_bot_stage3_strict_oos_split.py").read_text()
    assert "mar" + "ket" + "_" + "id" not in prod
    assert "mar" + "ket" + "_" + "id" not in test
    tree = ast.parse(prod)
    imports = []
    public_defs = []
    forbidden_names = {"open", "exec", "eval", "compile", "__import__", "print"}
    forbidden_attrs = {"now", "utcnow", "today", "read", "write", "connect", "request", "dump", "dumps", "load", "loads", "run", "Popen"}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)
        if isinstance(node, ast.ImportFrom):
            imports.append((node.module, tuple(alias.name for alias in node.names)))
        if isinstance(node, (ast.ClassDef, ast.FunctionDef)) and not node.name.startswith("_"):
            public_defs.append(node.name)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            assert node.func.id not in forbidden_names
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            assert node.func.attr not in forbidden_attrs
    assert imports == [("__future__", ("annotations",)), ("collections.abc", ("Mapping",)), ("dataclasses", ("dataclass",)), ("datetime", ("datetime",)), ("enum", ("StrEnum",))]
    assert public_defs == list(API)
