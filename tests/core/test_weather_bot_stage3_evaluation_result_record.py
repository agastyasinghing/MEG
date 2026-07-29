from __future__ import annotations

import ast
from collections.abc import Mapping
from dataclasses import FrozenInstanceError, MISSING, fields, is_dataclass, replace
from enum import StrEnum
import inspect
from pathlib import Path
import typing

import pytest

from meg.weather.stage3.baseline_contracts import BaselineType
from meg.weather.stage3.evaluation_result_record import (
    CalibrationBinResultPayload,
    DecompositionResultPayload,
    DistributionDiagnosticResultPayload,
    EnsembleDiagnosticResultPayload,
    EvaluationResultKind,
    EvaluationResultMethodRole,
    EvaluationResultRecord,
    EvaluationResultSupportStatus,
    EvaluationResultValidationCode,
    EvaluationResultValidationResult,
    EvaluationResultValidationSeverity,
    PairedComparisonResultPayload,
    ScalarScoreResultPayload,
    evaluation_result_record_from_mapping,
    validate_evaluation_result_record,
)
from meg.weather.stage3.scoring_and_diagnostics import (
    ScoringArtifact,
    ScoringPredictionRepresentation,
)

import meg.weather.stage3.evaluation_result_record as module


SOURCE = Path(module.__file__).read_text(encoding="utf-8")
C = EvaluationResultValidationCode


class TextSubclass(str):
    pass


class IntSubclass(int):
    pass


class TupleSubclass(tuple):
    pass


class UnrelatedEnum(StrEnum):
    VALUE = "scalar_score_result"


def _payload() -> ScalarScoreResultPayload:
    return ScalarScoreResultPayload(0.25, "lower_is_better", "artifact_specific_domain_validated")


def _values(**changes: object) -> dict[str, object]:
    values: dict[str, object] = {
        "evaluation_result_id": "result-1", "result_kind": EvaluationResultKind.SCALAR_SCORE_RESULT,
        "artifact_id": ScoringArtifact.BRIER_SCORE, "artifact_version": "1",
        "evaluation_definition_id": "definition-1", "evaluation_definition_version": "1",
        "evaluation_run_id": "run-1", "method_role": EvaluationResultMethodRole.CANDIDATE,
        "method_id": "method-1", "method_version": "1",
        "prediction_representation": ScoringPredictionRepresentation.BINARY_OUTCOME_PROBABILITY,
        "target_posture": "venue_defined_settlement_outcome", "split_id": "split-1",
        "split_version": "1", "fold_id": "fold-1", "cutoff_identity": "cutoff-1",
        "paired_test_record_set_id": "set-1", "eligibility_policy_id": "eligible-1",
        "aggregation_rule_id": "aggregate-1", "weighting_rule_id": "weight-1",
        "stratum_id": "all", "eligible_record_count": 2, "excluded_record_count": 0,
        "blocked_record_count": 0, "total_considered_record_count": 2,
        "exclusion_block_reason_summary": (), "uncertainty_method_id": None,
        "uncertainty_level_id": None, "support_status": EvaluationResultSupportStatus.SUPPORTED,
        "result_payload": _payload(), "provenance": ("source-1",),
        "result_created_at": "2026-07-27T12:00:00Z",
        "supersedes_result_id_when_applicable": None,
    }
    values.update(changes)
    return values


def _codes(**changes: object) -> tuple[EvaluationResultValidationCode, ...]:
    return validate_evaluation_result_record(EvaluationResultRecord(**_values(**changes))).codes


def test_public_contract_and_frozen_shapes() -> None:
    import meg.weather.stage3.evaluation_result_record as module

    assert module.__all__ == (
        "EvaluationResultKind", "EvaluationResultSupportStatus", "EvaluationResultMethodRole",
        "EvaluationResultValidationSeverity", "EvaluationResultValidationCode",
        "ScalarScoreResultPayload", "CalibrationBinResultPayload", "DecompositionResultPayload",
        "DistributionDiagnosticResultPayload", "EnsembleDiagnosticResultPayload",
        "PairedComparisonResultPayload", "EvaluationResultRecord",
        "EvaluationResultValidationResult", "evaluation_result_record_from_mapping",
        "validate_evaluation_result_record",
    )
    assert len(EvaluationResultValidationCode) == 30
    assert tuple(member.value for member in EvaluationResultValidationCode) == tuple(
        name.lower() for name in (
            "MISSING_REQUIRED_FIELD", "UNEXPECTED_FIELD", "BLANK_REQUIRED_TEXT",
            "INVALID_RESULT_KIND", "INVALID_ARTIFACT", "INVALID_METHOD_ROLE",
            "INVALID_PREDICTION_REPRESENTATION", "INVALID_SUPPORT_STATUS",
            "INVALID_FIXED_POSTURE", "INVALID_RECORD_COUNT", "SAMPLE_ACCOUNTING_MISMATCH",
            "INVALID_REASON_SUMMARY", "MISSING_REQUIRED_REASON", "UNCERTAINTY_FIELDS_MISMATCH",
            "EMPTY_PROVENANCE", "INVALID_PROVENANCE_REF", "INVALID_RESULT_CREATED_AT",
            "RESULT_KIND_ARTIFACT_MISMATCH", "REPRESENTATION_MISMATCH", "METHOD_ROLE_MISMATCH",
            "INVALID_PAYLOAD_TYPE", "INVALID_SCALAR_SCORE_PAYLOAD",
            "INVALID_CALIBRATION_BIN_PAYLOAD", "INVALID_DECOMPOSITION_PAYLOAD",
            "INVALID_DISTRIBUTION_DIAGNOSTIC_PAYLOAD", "INVALID_ENSEMBLE_DIAGNOSTIC_PAYLOAD",
            "INVALID_PAIRED_COMPARISON_PAYLOAD", "PAIR_BASELINE_NOT_APPROVED",
            "PAIR_RESULT_IDENTITY_COLLISION", "SELF_SUPERSESSION",
        )
    )
    assert len(fields(EvaluationResultRecord)) == 33
    record = EvaluationResultRecord(**_values())
    with pytest.raises(FrozenInstanceError):
        record.method_id = "changed"  # type: ignore[misc]
    assert tuple(inspect.signature(evaluation_result_record_from_mapping).parameters) == ("mapping",)
    assert tuple(inspect.signature(validate_evaluation_result_record).parameters) == ("record",)


def test_validation_result_forces_invariants() -> None:
    passed = EvaluationResultValidationResult(EvaluationResultValidationSeverity.BLOCKED, False)
    blocked = EvaluationResultValidationResult(
        EvaluationResultValidationSeverity.PASSED, True,
        [EvaluationResultValidationCode.INVALID_ARTIFACT],  # type: ignore[arg-type]
    )
    assert (passed.severity, passed.passed, passed.codes) == (EvaluationResultValidationSeverity.PASSED, True, ())
    assert (blocked.severity, blocked.passed, blocked.codes) == (
        EvaluationResultValidationSeverity.BLOCKED, False,
        (EvaluationResultValidationCode.INVALID_ARTIFACT,),
    )


def test_valid_direct_and_mapping_records() -> None:
    record = EvaluationResultRecord(**_values())
    assert validate_evaluation_result_record(record).passed
    mapping = _values(result_kind="scalar_score_result", artifact_id="brier_score", method_role="candidate", prediction_representation="binary_outcome_probability", support_status="supported", exclusion_block_reason_summary=[], provenance=["source-1"])
    original = {key: value.copy() if type(value) is list else value for key, value in mapping.items()}
    adapted, result = evaluation_result_record_from_mapping(mapping)
    assert result.passed and adapted == record
    assert mapping == original


@pytest.mark.parametrize("root", [None, 1, [], object()])
def test_non_mapping_is_fail_closed(root: object) -> None:
    record, result = evaluation_result_record_from_mapping(root)
    assert record is None
    assert result.codes == (EvaluationResultValidationCode.MISSING_REQUIRED_FIELD,) * 32


class _DuplicateMapping(Mapping):
    def __getitem__(self, key: object) -> object:
        return "unused"

    def __iter__(self):
        return iter(())

    def __len__(self) -> int:
        return 2

    def items(self):
        return [("evaluation_result_id", "one"), ("evaluation_result_id", "two")]


class _BaseExceptionMapping(_DuplicateMapping):
    def items(self):
        raise KeyboardInterrupt


def test_duplicate_snapshot_is_unreadable_and_baseexception_propagates() -> None:
    assert evaluation_result_record_from_mapping(_DuplicateMapping())[1].codes == (
        EvaluationResultValidationCode.MISSING_REQUIRED_FIELD,
    ) * 32
    with pytest.raises(KeyboardInterrupt):
        evaluation_result_record_from_mapping(_BaseExceptionMapping())


def test_complete_group_order_and_repeated_codes() -> None:
    changes = _values(
        evaluation_result_id=" ", result_kind="bad", artifact_id="bad", method_role="bad",
        prediction_representation="bad", support_status="bad", target_posture=" ",
        eligible_record_count=-1, excluded_record_count=-1, blocked_record_count=-1,
        total_considered_record_count=-1, exclusion_block_reason_summary=("",),
        uncertainty_method_id="method", uncertainty_level_id=None, provenance=("", 1),
        result_created_at=" ", supersedes_result_id_when_applicable=" ",
    )
    _, result = evaluation_result_record_from_mapping(changes)
    assert result.codes == (
        EvaluationResultValidationCode.BLANK_REQUIRED_TEXT,
        EvaluationResultValidationCode.BLANK_REQUIRED_TEXT,
        EvaluationResultValidationCode.BLANK_REQUIRED_TEXT,
        EvaluationResultValidationCode.BLANK_REQUIRED_TEXT,
        EvaluationResultValidationCode.INVALID_RESULT_KIND,
        EvaluationResultValidationCode.INVALID_ARTIFACT,
        EvaluationResultValidationCode.INVALID_METHOD_ROLE,
        EvaluationResultValidationCode.INVALID_PREDICTION_REPRESENTATION,
        EvaluationResultValidationCode.INVALID_SUPPORT_STATUS,
        EvaluationResultValidationCode.INVALID_FIXED_POSTURE,
        EvaluationResultValidationCode.INVALID_RECORD_COUNT,
        EvaluationResultValidationCode.INVALID_RECORD_COUNT,
        EvaluationResultValidationCode.INVALID_RECORD_COUNT,
        EvaluationResultValidationCode.INVALID_RECORD_COUNT,
        EvaluationResultValidationCode.INVALID_REASON_SUMMARY,
        EvaluationResultValidationCode.UNCERTAINTY_FIELDS_MISMATCH,
        EvaluationResultValidationCode.INVALID_PROVENANCE_REF,
        EvaluationResultValidationCode.INVALID_PROVENANCE_REF,
        EvaluationResultValidationCode.INVALID_RESULT_CREATED_AT,
    )


@pytest.mark.parametrize("timestamp", ["2026-01-01T00:00:00Z", "2026-01-01T00:00:00+05:30", "2026-01-01T00:00:00-04:00"])
def test_timestamp_acceptance(timestamp: str) -> None:
    assert _codes(result_created_at=timestamp) == ()


@pytest.mark.parametrize("timestamp", ["2026-01-01", "2026-01-01T00:00:00", "2026-01-01 00:00:00Z", "", 1])
def test_timestamp_rejection(timestamp: object) -> None:
    expected = (EvaluationResultValidationCode.INVALID_RESULT_CREATED_AT,)
    if not (type(timestamp) is str and timestamp.strip()):
        expected = (EvaluationResultValidationCode.BLANK_REQUIRED_TEXT,) + expected
    assert _codes(result_created_at=timestamp) == expected


def test_counts_reasons_uncertainty_and_provenance() -> None:
    assert _codes(eligible_record_count=True) == (EvaluationResultValidationCode.INVALID_RECORD_COUNT,)
    assert _codes(total_considered_record_count=3) == (EvaluationResultValidationCode.SAMPLE_ACCOUNTING_MISMATCH,)
    assert _codes(excluded_record_count=1, total_considered_record_count=3) == (EvaluationResultValidationCode.MISSING_REQUIRED_REASON,)
    assert _codes(support_status=EvaluationResultSupportStatus.BLOCKED) == (EvaluationResultValidationCode.MISSING_REQUIRED_REASON,)
    assert _codes(exclusion_block_reason_summary=("same", "same")) == (EvaluationResultValidationCode.INVALID_REASON_SUMMARY,)
    assert _codes(uncertainty_method_id="bootstrap") == (EvaluationResultValidationCode.UNCERTAINTY_FIELDS_MISMATCH,)
    assert _codes(provenance=()) == (EvaluationResultValidationCode.EMPTY_PROVENANCE,)
    assert _codes(provenance=("", "ok", 1)) == (
        EvaluationResultValidationCode.INVALID_PROVENANCE_REF,
        EvaluationResultValidationCode.INVALID_PROVENANCE_REF,
    )


def test_compatibility_and_payload_boundaries() -> None:
    assert _codes(artifact_id=ScoringArtifact.LOG_SCORE) == ()
    assert _codes(artifact_id=ScoringArtifact.PIT_HISTOGRAM) == (
        EvaluationResultValidationCode.RESULT_KIND_ARTIFACT_MISMATCH,
        EvaluationResultValidationCode.REPRESENTATION_MISMATCH,
    )
    assert _codes(method_role=EvaluationResultMethodRole.PAIRED_COMPARISON) == (EvaluationResultValidationCode.METHOD_ROLE_MISMATCH,)
    assert _codes(result_payload=object()) == (EvaluationResultValidationCode.INVALID_PAYLOAD_TYPE,)
    assert _codes(result_payload=ScalarScoreResultPayload(float("nan"), "lower_is_better", "artifact_specific_domain_validated")) == (EvaluationResultValidationCode.INVALID_SCALAR_SCORE_PAYLOAD,)


def test_every_payload_kind_has_a_valid_boundary() -> None:
    cases = (
        (EvaluationResultKind.CALIBRATION_BIN_RESULT, ScoringArtifact.RELIABILITY_DIAGRAM, ScoringPredictionRepresentation.BINARY_OUTCOME_PROBABILITY, CalibrationBinResultPayload("bin", 0, "policy", 2, 0.2, 0.5, "predeclared_order_required")),
        (EvaluationResultKind.DECOMPOSITION_RESULT, ScoringArtifact.BRIER_DECOMPOSITION, ScoringPredictionRepresentation.BINARY_OUTCOME_PROBABILITY, DecompositionResultPayload("policy", 0.1, 0.2, 0.3, "reliability_resolution_uncertainty_required")),
        (EvaluationResultKind.DISTRIBUTION_DIAGNOSTIC_RESULT, ScoringArtifact.PIT_HISTOGRAM, ScoringPredictionRepresentation.FULL_PREDICTIVE_DISTRIBUTION, DistributionDiagnosticResultPayload("policy", ("a", "b"), (1, 1), "predeclared_order_required")),
        (EvaluationResultKind.ENSEMBLE_DIAGNOSTIC_RESULT, ScoringArtifact.RANK_HISTOGRAM, ScoringPredictionRepresentation.FINITE_COMPARABLE_ENSEMBLE, EnsembleDiagnosticResultPayload("policy", ("a", "b"), (1, 1), "finite_comparable_ensemble_required", "predeclared_order_required")),
        (EvaluationResultKind.PAIRED_COMPARISON_RESULT, ScoringArtifact.BRIER_SCORE, ScoringPredictionRepresentation.BINARY_OUTCOME_PROBABILITY, PairedComparisonResultPayload("candidate", "baseline", BaselineType.CLIMATOLOGY, "candidate_minus_baseline_lower_is_better", -0.1, "exact_common_test_record_set_required")),
    )
    for kind, artifact, representation, payload in cases:
        role = EvaluationResultMethodRole.PAIRED_COMPARISON if kind is EvaluationResultKind.PAIRED_COMPARISON_RESULT else EvaluationResultMethodRole.CANDIDATE
        assert _codes(result_kind=kind, artifact_id=artifact, prediction_representation=representation, method_role=role, result_payload=payload) == ()


def test_pair_and_supersession_identity_codes() -> None:
    payload = PairedComparisonResultPayload("same", "same", "climatology", "candidate_minus_baseline_lower_is_better", 0.0, "exact_common_test_record_set_required")  # type: ignore[arg-type]
    assert _codes(result_kind=EvaluationResultKind.PAIRED_COMPARISON_RESULT, method_role=EvaluationResultMethodRole.PAIRED_COMPARISON, result_payload=payload) == (
        EvaluationResultValidationCode.PAIR_BASELINE_NOT_APPROVED,
        EvaluationResultValidationCode.PAIR_RESULT_IDENTITY_COLLISION,
    )
    assert _codes(supersedes_result_id_when_applicable="result-1") == (EvaluationResultValidationCode.SELF_SUPERSESSION,)


# The following oracles are intentionally literal: none is assembled from the
# production declarations whose spelling and order it freezes.
EXPECTED_API = (
    "EvaluationResultKind", "EvaluationResultSupportStatus", "EvaluationResultMethodRole",
    "EvaluationResultValidationSeverity", "EvaluationResultValidationCode",
    "ScalarScoreResultPayload", "CalibrationBinResultPayload", "DecompositionResultPayload",
    "DistributionDiagnosticResultPayload", "EnsembleDiagnosticResultPayload",
    "PairedComparisonResultPayload", "EvaluationResultRecord",
    "EvaluationResultValidationResult", "evaluation_result_record_from_mapping",
    "validate_evaluation_result_record",
)
EXPECTED_ENUMS = {
    "EvaluationResultKind": (
        ("SCALAR_SCORE_RESULT", "scalar_score_result"),
        ("CALIBRATION_BIN_RESULT", "calibration_bin_result"),
        ("DECOMPOSITION_RESULT", "decomposition_result"),
        ("DISTRIBUTION_DIAGNOSTIC_RESULT", "distribution_diagnostic_result"),
        ("ENSEMBLE_DIAGNOSTIC_RESULT", "ensemble_diagnostic_result"),
        ("PAIRED_COMPARISON_RESULT", "paired_comparison_result"),
    ),
    "EvaluationResultSupportStatus": (("SUPPORTED", "supported"), ("INSUFFICIENT", "insufficient"), ("BLOCKED", "blocked"), ("UNAVAILABLE", "unavailable")),
    "EvaluationResultMethodRole": (("CANDIDATE", "candidate"), ("CLIMATOLOGY_BASELINE", "climatology_baseline"), ("PERSISTENCE_BASELINE", "persistence_baseline"), ("PAIRED_COMPARISON", "paired_comparison")),
    "EvaluationResultValidationSeverity": (("PASSED", "passed"), ("BLOCKED", "blocked")),
    "EvaluationResultValidationCode": (
        ("MISSING_REQUIRED_FIELD", "missing_required_field"), ("UNEXPECTED_FIELD", "unexpected_field"),
        ("BLANK_REQUIRED_TEXT", "blank_required_text"), ("INVALID_RESULT_KIND", "invalid_result_kind"),
        ("INVALID_ARTIFACT", "invalid_artifact"), ("INVALID_METHOD_ROLE", "invalid_method_role"),
        ("INVALID_PREDICTION_REPRESENTATION", "invalid_prediction_representation"),
        ("INVALID_SUPPORT_STATUS", "invalid_support_status"), ("INVALID_FIXED_POSTURE", "invalid_fixed_posture"),
        ("INVALID_RECORD_COUNT", "invalid_record_count"), ("SAMPLE_ACCOUNTING_MISMATCH", "sample_accounting_mismatch"),
        ("INVALID_REASON_SUMMARY", "invalid_reason_summary"), ("MISSING_REQUIRED_REASON", "missing_required_reason"),
        ("UNCERTAINTY_FIELDS_MISMATCH", "uncertainty_fields_mismatch"), ("EMPTY_PROVENANCE", "empty_provenance"),
        ("INVALID_PROVENANCE_REF", "invalid_provenance_ref"), ("INVALID_RESULT_CREATED_AT", "invalid_result_created_at"),
        ("RESULT_KIND_ARTIFACT_MISMATCH", "result_kind_artifact_mismatch"), ("REPRESENTATION_MISMATCH", "representation_mismatch"),
        ("METHOD_ROLE_MISMATCH", "method_role_mismatch"), ("INVALID_PAYLOAD_TYPE", "invalid_payload_type"),
        ("INVALID_SCALAR_SCORE_PAYLOAD", "invalid_scalar_score_payload"),
        ("INVALID_CALIBRATION_BIN_PAYLOAD", "invalid_calibration_bin_payload"),
        ("INVALID_DECOMPOSITION_PAYLOAD", "invalid_decomposition_payload"),
        ("INVALID_DISTRIBUTION_DIAGNOSTIC_PAYLOAD", "invalid_distribution_diagnostic_payload"),
        ("INVALID_ENSEMBLE_DIAGNOSTIC_PAYLOAD", "invalid_ensemble_diagnostic_payload"),
        ("INVALID_PAIRED_COMPARISON_PAYLOAD", "invalid_paired_comparison_payload"),
        ("PAIR_BASELINE_NOT_APPROVED", "pair_baseline_not_approved"),
        ("PAIR_RESULT_IDENTITY_COLLISION", "pair_result_identity_collision"), ("SELF_SUPERSESSION", "self_supersession"),
    ),
}
EXPECTED_FIELDS = {
    "ScalarScoreResultPayload": (("result_value", float), ("score_direction", str), ("result_domain_posture", str)),
    "CalibrationBinResultPayload": (("bin_id", str), ("bin_index", int), ("bin_boundary_policy_id", str), ("sample_count", int), ("mean_predicted_probability", float), ("observed_outcome_frequency", float), ("ordered_bin_posture", str)),
    "DecompositionResultPayload": (("decomposition_policy_id", str), ("reliability_value", float), ("resolution_value", float), ("uncertainty_value", float), ("component_posture", str)),
    "DistributionDiagnosticResultPayload": (("pit_treatment_policy_id", str), ("ordered_bin_ids", tuple[str, ...]), ("ordered_bin_counts", tuple[int, ...]), ("ordered_content_posture", str)),
    "EnsembleDiagnosticResultPayload": (("tie_treatment_policy_id", str), ("ordered_rank_ids", tuple[str, ...]), ("ordered_rank_counts", tuple[int, ...]), ("ensemble_comparability_posture", str), ("ordered_content_posture", str)),
    "PairedComparisonResultPayload": (("candidate_result_id", str), ("baseline_result_id", str), ("baseline_type", BaselineType), ("comparison_direction", str), ("paired_comparison_value", float), ("paired_scope_posture", str)),
    "EvaluationResultRecord": (
        ("evaluation_result_id", str), ("result_kind", EvaluationResultKind), ("artifact_id", ScoringArtifact),
        ("artifact_version", str), ("evaluation_definition_id", str), ("evaluation_definition_version", str),
        ("evaluation_run_id", str), ("method_role", EvaluationResultMethodRole), ("method_id", str),
        ("method_version", str), ("prediction_representation", ScoringPredictionRepresentation), ("target_posture", str),
        ("split_id", str), ("split_version", str), ("fold_id", str), ("cutoff_identity", str),
        ("paired_test_record_set_id", str), ("eligibility_policy_id", str), ("aggregation_rule_id", str),
        ("weighting_rule_id", str), ("stratum_id", str), ("eligible_record_count", int),
        ("excluded_record_count", int), ("blocked_record_count", int), ("total_considered_record_count", int),
        ("exclusion_block_reason_summary", tuple[str, ...]), ("uncertainty_method_id", str | None),
        ("uncertainty_level_id", str | None), ("support_status", EvaluationResultSupportStatus),
        ("result_payload", ScalarScoreResultPayload | CalibrationBinResultPayload | DecompositionResultPayload | DistributionDiagnosticResultPayload | EnsembleDiagnosticResultPayload | PairedComparisonResultPayload),
        ("provenance", tuple[str, ...]), ("result_created_at", str), ("supersedes_result_id_when_applicable", str | None),
    ),
    "EvaluationResultValidationResult": (("severity", EvaluationResultValidationSeverity), ("passed", bool), ("codes", tuple[EvaluationResultValidationCode, ...])),
}
EXPECTED_REQUIRED_KEYS = (
    "evaluation_result_id", "result_kind", "artifact_id", "artifact_version", "evaluation_definition_id",
    "evaluation_definition_version", "evaluation_run_id", "method_role", "method_id", "method_version",
    "prediction_representation", "target_posture", "split_id", "split_version", "fold_id", "cutoff_identity",
    "paired_test_record_set_id", "eligibility_policy_id", "aggregation_rule_id", "weighting_rule_id", "stratum_id",
    "eligible_record_count", "excluded_record_count", "blocked_record_count", "total_considered_record_count",
    "exclusion_block_reason_summary", "uncertainty_method_id", "uncertainty_level_id", "support_status",
    "result_payload", "provenance", "result_created_at",
)
EXPECTED_REQUIRED_TEXT = (
    "evaluation_result_id", "artifact_version", "evaluation_definition_id", "evaluation_definition_version",
    "evaluation_run_id", "method_id", "method_version", "target_posture", "split_id", "split_version", "fold_id",
    "cutoff_identity", "paired_test_record_set_id", "eligibility_policy_id", "aggregation_rule_id",
    "weighting_rule_id", "stratum_id", "result_created_at",
)
EXPECTED_GROUPS = (
    "missing keys", "unexpected exact-string keys", "unexpected non-string keys", "required and nullable text",
    "result kind", "artifact", "method role", "prediction representation", "support status", "fixed posture",
    "counts", "sample-accounting identity", "reason-summary structure", "required-reason consistency",
    "uncertainty pairing", "provenance", "result-created timestamp", "result-kind/artifact compatibility",
    "representation compatibility", "method-role compatibility", "payload type", "payload content",
    "paired baseline", "paired identity collision", "self-supersession",
)


def test_complete_independent_structural_oracles() -> None:
    tree = ast.parse(SOURCE)
    imports = tuple(
        (node.module, tuple(alias.name for alias in node.names)) if isinstance(node, ast.ImportFrom)
        else (None, tuple(alias.name for alias in node.names))
        for node in tree.body if isinstance(node, (ast.Import, ast.ImportFrom))
    )
    assert imports == (
        ("__future__", ("annotations",)), ("collections.abc", ("Mapping",)),
        ("dataclasses", ("dataclass",)), ("datetime", ("datetime",)), ("enum", ("StrEnum",)),
        (None, ("math",)), (None, ("re",)), ("meg.weather.stage3.baseline_contracts", ("BaselineType",)),
        ("meg.weather.stage3.scoring_and_diagnostics", ("ScoringArtifact", "ScoringPredictionRepresentation")),
    )
    assert module.__all__ == EXPECTED_API
    assert tuple(node.name for node in tree.body if isinstance(node, (ast.ClassDef, ast.FunctionDef)) and not node.name.startswith("_")) == EXPECTED_API
    for name, expected in EXPECTED_ENUMS.items():
        assert tuple((item.name, item.value) for item in getattr(module, name)) == expected
    for name, expected in EXPECTED_FIELDS.items():
        cls = getattr(module, name)
        hints = typing.get_type_hints(cls)
        assert is_dataclass(cls)
        assert cls.__dataclass_params__.frozen is True
        assert tuple((field.name, hints[field.name]) for field in fields(cls)) == expected
        defaults = tuple(field.default for field in fields(cls))
        if name == "EvaluationResultRecord":
            assert defaults == (MISSING,) * 32 + (None,)
        elif name == "EvaluationResultValidationResult":
            assert defaults == (MISSING, MISSING, ())
        else:
            assert defaults == (MISSING,) * len(expected)
    mapping_hints = typing.get_type_hints(evaluation_result_record_from_mapping)
    validation_hints = typing.get_type_hints(validate_evaluation_result_record)
    assert inspect.signature(evaluation_result_record_from_mapping).parameters["mapping"].annotation == "object"
    assert mapping_hints == {"mapping": object, "return": tuple[EvaluationResultRecord | None, EvaluationResultValidationResult]}
    assert inspect.signature(validate_evaluation_result_record).parameters["record"].annotation == "EvaluationResultRecord"
    assert validation_hints == {"record": EvaluationResultRecord, "return": EvaluationResultValidationResult}
    assert module._REQUIRED_MAPPING_KEYS == EXPECTED_REQUIRED_KEYS
    assert module._OPTIONAL_MAPPING_KEYS == ("supersedes_result_id_when_applicable",)
    assert module._REQUIRED_TEXT_FIELDS == EXPECTED_REQUIRED_TEXT
    assert module._NULLABLE_TEXT_FIELDS == ("uncertainty_method_id", "uncertainty_level_id", "supersedes_result_id_when_applicable")
    assert module._COUNT_FIELDS == ("eligible_record_count", "excluded_record_count", "blocked_record_count", "total_considered_record_count")
    assert module._VALIDATION_GROUPS == EXPECTED_GROUPS
    assert module._RESULT_KIND_ARTIFACT_PAYLOAD_MATRIX == {
        EvaluationResultKind.SCALAR_SCORE_RESULT: ((ScoringArtifact.BRIER_SCORE, ScoringArtifact.LOG_SCORE, ScoringArtifact.CRPS, ScoringArtifact.THRESHOLD_WEIGHTED_CRPS), ScalarScoreResultPayload),
        EvaluationResultKind.CALIBRATION_BIN_RESULT: ((ScoringArtifact.RELIABILITY_DIAGRAM,), CalibrationBinResultPayload),
        EvaluationResultKind.DECOMPOSITION_RESULT: ((ScoringArtifact.BRIER_DECOMPOSITION,), DecompositionResultPayload),
        EvaluationResultKind.DISTRIBUTION_DIAGNOSTIC_RESULT: ((ScoringArtifact.PIT_HISTOGRAM,), DistributionDiagnosticResultPayload),
        EvaluationResultKind.ENSEMBLE_DIAGNOSTIC_RESULT: ((ScoringArtifact.RANK_HISTOGRAM,), EnsembleDiagnosticResultPayload),
        EvaluationResultKind.PAIRED_COMPARISON_RESULT: ((ScoringArtifact.BRIER_SCORE, ScoringArtifact.LOG_SCORE, ScoringArtifact.CRPS, ScoringArtifact.THRESHOLD_WEIGHTED_CRPS), PairedComparisonResultPayload),
    }
    assert module._REPRESENTATION_MATRIX == {
        ScoringArtifact.BRIER_SCORE: ScoringPredictionRepresentation.BINARY_OUTCOME_PROBABILITY,
        ScoringArtifact.LOG_SCORE: ScoringPredictionRepresentation.BINARY_OUTCOME_PROBABILITY,
        ScoringArtifact.RELIABILITY_DIAGRAM: ScoringPredictionRepresentation.BINARY_OUTCOME_PROBABILITY,
        ScoringArtifact.BRIER_DECOMPOSITION: ScoringPredictionRepresentation.BINARY_OUTCOME_PROBABILITY,
        ScoringArtifact.CRPS: ScoringPredictionRepresentation.FULL_PREDICTIVE_DISTRIBUTION,
        ScoringArtifact.PIT_HISTOGRAM: ScoringPredictionRepresentation.FULL_PREDICTIVE_DISTRIBUTION,
        ScoringArtifact.RANK_HISTOGRAM: ScoringPredictionRepresentation.FINITE_COMPARABLE_ENSEMBLE,
        ScoringArtifact.THRESHOLD_WEIGHTED_CRPS: ScoringPredictionRepresentation.FULL_PREDICTIVE_DISTRIBUTION,
    }
    ordinary = (EvaluationResultMethodRole.CANDIDATE, EvaluationResultMethodRole.CLIMATOLOGY_BASELINE, EvaluationResultMethodRole.PERSISTENCE_BASELINE)
    assert module._METHOD_ROLE_MATRIX == {
        EvaluationResultKind.SCALAR_SCORE_RESULT: ordinary,
        EvaluationResultKind.CALIBRATION_BIN_RESULT: ordinary,
        EvaluationResultKind.DECOMPOSITION_RESULT: ordinary,
        EvaluationResultKind.DISTRIBUTION_DIAGNOSTIC_RESULT: ordinary,
        EvaluationResultKind.ENSEMBLE_DIAGNOSTIC_RESULT: ordinary,
        EvaluationResultKind.PAIRED_COMPARISON_RESULT: (EvaluationResultMethodRole.PAIRED_COMPARISON,),
    }


class ItemsMapping(Mapping):
    def __init__(self, supplied: object) -> None:
        self.supplied = supplied

    def __getitem__(self, key: object) -> object:
        raise KeyError(key)

    def __iter__(self):
        return iter(())

    def __len__(self) -> int:
        return 0

    def items(self):
        if isinstance(self.supplied, BaseException):
            raise self.supplied
        return self.supplied


class BrokenIterator:
    def __iter__(self):
        return self

    def __next__(self):
        raise RuntimeError("iteration")


class BadHash:
    def __hash__(self) -> int:
        raise RuntimeError("hash")


class LaterBadHash:
    def __init__(self) -> None:
        self.calls = 0

    def __hash__(self) -> int:
        self.calls += 1
        if self.calls > 2:
            raise RuntimeError("later hash")
        return 7


ROOT_FAILURES = (
    None, 4, object(), ItemsMapping(RuntimeError("items")), ItemsMapping(BrokenIterator()),
    ItemsMapping([("only",)]), ItemsMapping([("one", 2, 3)]), ItemsMapping(3),
    ItemsMapping([BadHash()]), ItemsMapping([(BadHash(), "value")]),
    ItemsMapping([(LaterBadHash(), "value")]),
    ItemsMapping([("x", 1), ("x", 2)]),
    ItemsMapping([(TextSubclass("x"), 1), (TextSubclass("x"), 2)]),
    ItemsMapping([(7, 1), (7, 2)]),
)


@pytest.mark.parametrize("root", ROOT_FAILURES)
def test_complete_mapping_root_failure_matrix(root: object) -> None:
    record, result = evaluation_result_record_from_mapping(root)
    assert record is None
    assert result == EvaluationResultValidationResult(
        EvaluationResultValidationSeverity.BLOCKED,
        False,
        (C.MISSING_REQUIRED_FIELD,) * 32,
    )


@pytest.mark.parametrize("failure", [KeyboardInterrupt(), SystemExit()])
def test_mapping_root_baseexceptions_propagate(failure: BaseException) -> None:
    with pytest.raises(type(failure)):
        evaluation_result_record_from_mapping(ItemsMapping(failure))


@pytest.mark.parametrize("missing", EXPECTED_REQUIRED_KEYS)
def test_each_required_mapping_key_is_required(missing: str) -> None:
    values = _values()
    del values[missing]
    record, result = evaluation_result_record_from_mapping(values)
    assert record is None
    assert result.codes == (C.MISSING_REQUIRED_FIELD,)


def test_shape_order_and_semantic_aggregation() -> None:
    values = _values(result_kind="invalid", artifact_version="")
    del values["evaluation_result_id"]
    values["z-extra"] = 1
    values["a-extra"] = 2
    values[7] = 3
    values[TextSubclass("evaluation_result_id")] = "shadow"
    record, result = evaluation_result_record_from_mapping(values)
    assert record is None
    assert result.codes == (
        C.MISSING_REQUIRED_FIELD,
        C.UNEXPECTED_FIELD, C.UNEXPECTED_FIELD,
        C.UNEXPECTED_FIELD, C.UNEXPECTED_FIELD,
        C.BLANK_REQUIRED_TEXT,
        C.INVALID_RESULT_KIND,
    )


ENUM_CASES = (
    ("result_kind", EvaluationResultKind, EvaluationResultKind.SCALAR_SCORE_RESULT, "scalar_score_result", C.INVALID_RESULT_KIND),
    ("artifact_id", ScoringArtifact, ScoringArtifact.BRIER_SCORE, "brier_score", C.INVALID_ARTIFACT),
    ("method_role", EvaluationResultMethodRole, EvaluationResultMethodRole.CANDIDATE, "candidate", C.INVALID_METHOD_ROLE),
    ("prediction_representation", ScoringPredictionRepresentation, ScoringPredictionRepresentation.BINARY_OUTCOME_PROBABILITY, "binary_outcome_probability", C.INVALID_PREDICTION_REPRESENTATION),
    ("support_status", EvaluationResultSupportStatus, EvaluationResultSupportStatus.SUPPORTED, "supported", C.INVALID_SUPPORT_STATUS),
)


@pytest.mark.parametrize("field,enum_type,member,text,invalid_code", ENUM_CASES)
def test_mapping_enum_adaptation_boundaries(field: str, enum_type: type, member: object, text: str, invalid_code: C) -> None:
    for accepted in (member, text):
        record, result = evaluation_result_record_from_mapping(_values(**{field: accepted}))
        assert result.codes == ()
        assert record is not None and type(getattr(record, field)) is enum_type
    for rejected in ("invalid", TextSubclass(text), UnrelatedEnum.VALUE, object()):
        record, result = evaluation_result_record_from_mapping(_values(**{field: rejected}))
        assert record is None
        assert result.codes[0] is invalid_code


@pytest.mark.parametrize("field,enum_type,member,text,invalid_code", ENUM_CASES)
def test_direct_validation_never_adapts_enum_strings(field: str, enum_type: type, member: object, text: str, invalid_code: C) -> None:
    record = EvaluationResultRecord(**_values(**{field: text}))
    assert validate_evaluation_result_record(record).codes[0] is invalid_code
    assert getattr(record, field) == text and type(getattr(record, field)) is str


@pytest.mark.parametrize("field", EXPECTED_REQUIRED_TEXT)
@pytest.mark.parametrize("bad", ["", "  ", 7, None, TextSubclass("valid")])
def test_every_required_text_field_rejects_non_exact_nonblank_text(field: str, bad: object) -> None:
    codes = _codes(**{field: bad})
    expected = [C.BLANK_REQUIRED_TEXT]
    if field == "target_posture":
        expected.append(C.INVALID_FIXED_POSTURE)
    if field == "result_created_at":
        expected.append(C.INVALID_RESULT_CREATED_AT)
    assert codes == tuple(expected)


@pytest.mark.parametrize("field", ["uncertainty_method_id", "uncertainty_level_id", "supersedes_result_id_when_applicable"])
def test_every_nullable_text_field_matrix(field: str) -> None:
    assert _codes(**{field: None}) == ()
    if field.startswith("uncertainty"):
        other = "uncertainty_level_id" if field == "uncertainty_method_id" else "uncertainty_method_id"
        assert _codes(**{field: "valid", other: "valid"}) == ()
    else:
        assert _codes(**{field: "valid"}) == ()
    for bad in ("", 4, TextSubclass("valid")):
        assert _codes(**{field: bad}) == (C.BLANK_REQUIRED_TEXT,)


@pytest.mark.parametrize("value", ["2026-01-01T00:00:00Z", "2026-01-01T00:00:00+05:30", "2026-01-01T00:00:00-04:00"])
def test_timestamp_valid_forms_are_preserved(value: str) -> None:
    record, result = evaluation_result_record_from_mapping(_values(result_created_at=value))
    assert result.codes == ()
    assert record is not None and record.result_created_at == value


@pytest.mark.parametrize("value", ["2026-01-01T00:00:00+5:30", "2026-01-01T00:00:00", "2026-01-01 00:00:00Z", "2026-01-01t00:00:00Z", "2026-02-30T00:00:00Z", "2026-01-01T25:00:00Z"])
def test_timestamp_invalid_nonblank_forms(value: str) -> None:
    assert _codes(result_created_at=value) == (C.INVALID_RESULT_CREATED_AT,)


def test_missing_timestamp_has_only_missing_code() -> None:
    values = _values()
    del values["result_created_at"]
    assert evaluation_result_record_from_mapping(values)[1].codes == (C.MISSING_REQUIRED_FIELD,)


@pytest.mark.parametrize("field", ["eligible_record_count", "excluded_record_count", "blocked_record_count", "total_considered_record_count"])
@pytest.mark.parametrize("bad", [-1, True, IntSubclass(1), 1.0, "1", object()])
def test_every_count_field_exact_type_matrix(field: str, bad: object) -> None:
    assert _codes(**{field: bad}) == (C.INVALID_RECORD_COUNT,)


def test_count_order_and_accounting_prerequisites() -> None:
    assert _codes(eligible_record_count=0, excluded_record_count=0, blocked_record_count=0, total_considered_record_count=0) == ()
    assert _codes(total_considered_record_count=3) == (C.SAMPLE_ACCOUNTING_MISMATCH,)
    assert _codes(eligible_record_count=-1, excluded_record_count=-1, total_considered_record_count=99) == (C.INVALID_RECORD_COUNT, C.INVALID_RECORD_COUNT)


@pytest.mark.parametrize("bad", [("x", "x"), ("",), (7,), (TextSubclass("x"),), TupleSubclass(("x",)), ["x"], "x", object()])
def test_direct_reason_summary_rejects_every_structural_defect(bad: object) -> None:
    assert _codes(exclusion_block_reason_summary=bad) == (C.INVALID_REASON_SUMMARY,)


def test_mapping_reason_list_adaptation_and_input_preservation() -> None:
    reasons = ["second", "first"]
    source = _values(exclusion_block_reason_summary=reasons)
    record, result = evaluation_result_record_from_mapping(source)
    assert result.codes == () and record is not None
    assert record.exclusion_block_reason_summary == ("second", "first")
    assert reasons == ["second", "first"] and source["exclusion_block_reason_summary"] is reasons


@pytest.mark.parametrize("changes", [
    {"excluded_record_count": 1, "total_considered_record_count": 3},
    {"blocked_record_count": 1, "total_considered_record_count": 3},
    {"support_status": EvaluationResultSupportStatus.INSUFFICIENT},
    {"support_status": EvaluationResultSupportStatus.BLOCKED},
    {"support_status": EvaluationResultSupportStatus.UNAVAILABLE},
])
def test_every_required_reason_trigger(changes: dict[str, object]) -> None:
    assert _codes(**changes) == (C.MISSING_REQUIRED_REASON,)


@pytest.mark.parametrize("changes,expected", [
    ({"exclusion_block_reason_summary": [], "excluded_record_count": 1, "total_considered_record_count": 3}, (C.INVALID_REASON_SUMMARY,)),
    ({"excluded_record_count": -1, "support_status": EvaluationResultSupportStatus.BLOCKED}, (C.INVALID_RECORD_COUNT,)),
    ({"blocked_record_count": -1, "support_status": EvaluationResultSupportStatus.BLOCKED}, (C.INVALID_RECORD_COUNT,)),
    ({"support_status": "bad"}, (C.INVALID_SUPPORT_STATUS,)),
])
def test_required_reason_dependency_suppression(changes: dict[str, object], expected: tuple[C, ...]) -> None:
    assert _codes(**changes) == expected


def test_reason_missing_mapping_prerequisite_suppression() -> None:
    for missing in ("excluded_record_count", "blocked_record_count", "support_status", "exclusion_block_reason_summary"):
        values = _values(support_status=EvaluationResultSupportStatus.BLOCKED)
        del values[missing]
        assert evaluation_result_record_from_mapping(values)[1].codes == (C.MISSING_REQUIRED_FIELD,)


@pytest.mark.parametrize("method,level,expected", [
    (None, None, ()), ("m", "l", ()), ("m", None, (C.UNCERTAINTY_FIELDS_MISMATCH,)),
    (None, "l", (C.UNCERTAINTY_FIELDS_MISMATCH,)), ("", None, (C.BLANK_REQUIRED_TEXT,)),
    (None, "", (C.BLANK_REQUIRED_TEXT,)), (3, None, (C.BLANK_REQUIRED_TEXT,)),
    (None, 3, (C.BLANK_REQUIRED_TEXT,)), (TextSubclass("m"), None, (C.BLANK_REQUIRED_TEXT,)),
])
def test_complete_uncertainty_matrix(method: object, level: object, expected: tuple[C, ...]) -> None:
    assert _codes(uncertainty_method_id=method, uncertainty_level_id=level) == expected


def test_missing_uncertainty_mapping_keys_only_emit_missing() -> None:
    for missing in ("uncertainty_method_id", "uncertainty_level_id"):
        values = _values()
        del values[missing]
        assert evaluation_result_record_from_mapping(values)[1].codes == (C.MISSING_REQUIRED_FIELD,)


@pytest.mark.parametrize("bad,expected", [
    ([], (C.INVALID_PROVENANCE_REF,)), (TupleSubclass(("x",)), (C.INVALID_PROVENANCE_REF,)),
    ("x", (C.INVALID_PROVENANCE_REF,)), ((), (C.EMPTY_PROVENANCE,)), (("",), (C.INVALID_PROVENANCE_REF,)),
    ((7,), (C.INVALID_PROVENANCE_REF,)), ((TextSubclass("x"),), (C.INVALID_PROVENANCE_REF,)),
    (("", 7, TextSubclass("x")), (C.INVALID_PROVENANCE_REF, C.INVALID_PROVENANCE_REF, C.INVALID_PROVENANCE_REF)),
])
def test_direct_provenance_matrix(bad: object, expected: tuple[C, ...]) -> None:
    assert _codes(provenance=bad) == expected


def test_mapping_provenance_adaptation_duplicates_order_and_preservation() -> None:
    refs = ["z", "a", "z"]
    source = _values(provenance=refs)
    first = evaluation_result_record_from_mapping(source)
    second = evaluation_result_record_from_mapping(source)
    assert first == second
    assert first[1].codes == () and first[0] is not None
    assert first[0].provenance == ("z", "a", "z")
    assert refs == ["z", "a", "z"] and source["provenance"] is refs


KIND_ARTIFACTS = {
    EvaluationResultKind.SCALAR_SCORE_RESULT: (ScoringArtifact.BRIER_SCORE, ScoringArtifact.LOG_SCORE, ScoringArtifact.CRPS, ScoringArtifact.THRESHOLD_WEIGHTED_CRPS),
    EvaluationResultKind.CALIBRATION_BIN_RESULT: (ScoringArtifact.RELIABILITY_DIAGRAM,),
    EvaluationResultKind.DECOMPOSITION_RESULT: (ScoringArtifact.BRIER_DECOMPOSITION,),
    EvaluationResultKind.DISTRIBUTION_DIAGNOSTIC_RESULT: (ScoringArtifact.PIT_HISTOGRAM,),
    EvaluationResultKind.ENSEMBLE_DIAGNOSTIC_RESULT: (ScoringArtifact.RANK_HISTOGRAM,),
    EvaluationResultKind.PAIRED_COMPARISON_RESULT: (ScoringArtifact.BRIER_SCORE, ScoringArtifact.LOG_SCORE, ScoringArtifact.CRPS, ScoringArtifact.THRESHOLD_WEIGHTED_CRPS),
}
REPRESENTATIONS = {
    ScoringArtifact.BRIER_SCORE: ScoringPredictionRepresentation.BINARY_OUTCOME_PROBABILITY,
    ScoringArtifact.LOG_SCORE: ScoringPredictionRepresentation.BINARY_OUTCOME_PROBABILITY,
    ScoringArtifact.RELIABILITY_DIAGRAM: ScoringPredictionRepresentation.BINARY_OUTCOME_PROBABILITY,
    ScoringArtifact.BRIER_DECOMPOSITION: ScoringPredictionRepresentation.BINARY_OUTCOME_PROBABILITY,
    ScoringArtifact.CRPS: ScoringPredictionRepresentation.FULL_PREDICTIVE_DISTRIBUTION,
    ScoringArtifact.PIT_HISTOGRAM: ScoringPredictionRepresentation.FULL_PREDICTIVE_DISTRIBUTION,
    ScoringArtifact.RANK_HISTOGRAM: ScoringPredictionRepresentation.FINITE_COMPARABLE_ENSEMBLE,
    ScoringArtifact.THRESHOLD_WEIGHTED_CRPS: ScoringPredictionRepresentation.FULL_PREDICTIVE_DISTRIBUTION,
}


@pytest.mark.parametrize("kind", tuple(EvaluationResultKind))
@pytest.mark.parametrize("artifact", tuple(ScoringArtifact))
def test_complete_kind_artifact_matrix(kind: EvaluationResultKind, artifact: ScoringArtifact) -> None:
    payload = _payload()
    role = EvaluationResultMethodRole.PAIRED_COMPARISON if kind is EvaluationResultKind.PAIRED_COMPARISON_RESULT else EvaluationResultMethodRole.CANDIDATE
    codes = _codes(result_kind=kind, artifact_id=artifact, prediction_representation=REPRESENTATIONS[artifact], method_role=role, result_payload=payload)
    expected = [] if artifact in KIND_ARTIFACTS[kind] else [C.RESULT_KIND_ARTIFACT_MISMATCH]
    if kind is not EvaluationResultKind.SCALAR_SCORE_RESULT:
        expected.append(C.INVALID_PAYLOAD_TYPE)
    assert codes == tuple(expected)


@pytest.mark.parametrize("artifact", tuple(ScoringArtifact))
@pytest.mark.parametrize("representation", tuple(ScoringPredictionRepresentation))
def test_complete_artifact_representation_matrix(artifact: ScoringArtifact, representation: ScoringPredictionRepresentation) -> None:
    codes = _codes(artifact_id=artifact, prediction_representation=representation)
    expected = []
    if artifact not in KIND_ARTIFACTS[EvaluationResultKind.SCALAR_SCORE_RESULT]:
        expected.append(C.RESULT_KIND_ARTIFACT_MISMATCH)
    if representation is not REPRESENTATIONS[artifact]:
        expected.append(C.REPRESENTATION_MISMATCH)
    assert codes == tuple(expected)


@pytest.mark.parametrize("kind", tuple(EvaluationResultKind))
@pytest.mark.parametrize("role", tuple(EvaluationResultMethodRole))
def test_complete_kind_method_role_matrix(kind: EvaluationResultKind, role: EvaluationResultMethodRole) -> None:
    expected_role = role is EvaluationResultMethodRole.PAIRED_COMPARISON
    paired_kind = kind is EvaluationResultKind.PAIRED_COMPARISON_RESULT
    values = _valid_for_kind(kind, _payloads()[kind])
    values["method_role"] = role
    codes = _codes(**values)
    expected = [] if expected_role == paired_kind else [C.METHOD_ROLE_MISMATCH]
    assert codes == tuple(expected)


def test_invalid_compatibility_prerequisites_suppress_dependent_codes() -> None:
    assert _codes(result_kind="bad") == (C.INVALID_RESULT_KIND,)
    assert _codes(artifact_id="bad") == (C.INVALID_ARTIFACT,)
    assert _codes(prediction_representation="bad") == (C.INVALID_PREDICTION_REPRESENTATION,)
    assert _codes(method_role="bad") == (C.INVALID_METHOD_ROLE,)


def _payloads() -> dict[EvaluationResultKind, object]:
    return {
        EvaluationResultKind.SCALAR_SCORE_RESULT: _payload(),
        EvaluationResultKind.CALIBRATION_BIN_RESULT: CalibrationBinResultPayload("bin", 0, "policy", 2, 0.2, 0.5, "predeclared_order_required"),
        EvaluationResultKind.DECOMPOSITION_RESULT: DecompositionResultPayload("policy", 0.1, 0.2, 0.3, "reliability_resolution_uncertainty_required"),
        EvaluationResultKind.DISTRIBUTION_DIAGNOSTIC_RESULT: DistributionDiagnosticResultPayload("policy", ("a", "b"), (1, 1), "predeclared_order_required"),
        EvaluationResultKind.ENSEMBLE_DIAGNOSTIC_RESULT: EnsembleDiagnosticResultPayload("policy", ("a", "b"), (1, 1), "finite_comparable_ensemble_required", "predeclared_order_required"),
        EvaluationResultKind.PAIRED_COMPARISON_RESULT: PairedComparisonResultPayload("candidate", "baseline", BaselineType.CLIMATOLOGY, "candidate_minus_baseline_lower_is_better", 0.0, "exact_common_test_record_set_required"),
    }


def _valid_for_kind(kind: EvaluationResultKind, payload: object) -> dict[str, object]:
    artifact = KIND_ARTIFACTS[kind][0]
    return {
        "result_kind": kind, "artifact_id": artifact, "prediction_representation": REPRESENTATIONS[artifact],
        "method_role": EvaluationResultMethodRole.PAIRED_COMPARISON if kind is EvaluationResultKind.PAIRED_COMPARISON_RESULT else EvaluationResultMethodRole.CANDIDATE,
        "result_payload": payload,
    }


@pytest.mark.parametrize("kind", tuple(EvaluationResultKind))
def test_complete_wrong_payload_type_matrix(kind: EvaluationResultKind) -> None:
    payloads = _payloads()
    assert _codes(**_valid_for_kind(kind, payloads[kind])) == ()
    for other_kind, payload in payloads.items():
        if other_kind is not kind:
            assert _codes(**_valid_for_kind(kind, payload)) == (C.INVALID_PAYLOAD_TYPE,)
    expected_class = type(payloads[kind])
    subclass = type("PayloadSubclass", (expected_class,), {})
    inherited = subclass(*[getattr(payloads[kind], field.name) for field in fields(expected_class)])
    for wrong in (inherited, object(), {"nested": "mapping"}):
        assert _codes(**_valid_for_kind(kind, wrong)) == (C.INVALID_PAYLOAD_TYPE,)


@pytest.mark.parametrize("value", [1, True, IntSubclass(1), float("nan"), float("inf"), float("-inf")])
def test_scalar_requires_exact_finite_float(value: object) -> None:
    assert _codes(result_payload=ScalarScoreResultPayload(value, "lower_is_better", "artifact_specific_domain_validated")) == (C.INVALID_SCALAR_SCORE_PAYLOAD,)  # type: ignore[arg-type]


@pytest.mark.parametrize("field,value", [("score_direction", "wrong"), ("score_direction", TextSubclass("lower_is_better")), ("result_domain_posture", "wrong"), ("result_domain_posture", TextSubclass("artifact_specific_domain_validated"))])
def test_scalar_fixed_postures(field: str, value: object) -> None:
    assert _codes(result_payload=replace(_payload(), **{field: value})) == (C.INVALID_SCALAR_SCORE_PAYLOAD,)


@pytest.mark.parametrize("artifact,valid_values,invalid", [
    (ScoringArtifact.BRIER_SCORE, (0.0, 1.0), -0.01),
    (ScoringArtifact.LOG_SCORE, (0.0, 1.0), -0.01),
    (ScoringArtifact.CRPS, (0.0, 1.0), -0.01),
    (ScoringArtifact.THRESHOLD_WEIGHTED_CRPS, (0.0, 1.0), -0.01),
])
def test_scalar_artifact_numeric_domains(artifact: ScoringArtifact, valid_values: tuple[float, ...], invalid: float) -> None:
    for value in valid_values:
        assert _codes(artifact_id=artifact, prediction_representation=REPRESENTATIONS[artifact], result_payload=replace(_payload(), result_value=value)) == ()
    assert _codes(artifact_id=artifact, prediction_representation=REPRESENTATIONS[artifact], result_payload=replace(_payload(), result_value=invalid)) == (C.INVALID_SCALAR_SCORE_PAYLOAD,)


@pytest.mark.parametrize("field,bad", [
    ("bin_id", ""), ("bin_id", TextSubclass("bin")), ("bin_index", -1), ("bin_index", True),
    ("bin_boundary_policy_id", ""), ("sample_count", -1), ("sample_count", 2.0),
    ("mean_predicted_probability", 0), ("mean_predicted_probability", -0.1), ("mean_predicted_probability", 1.1),
    ("observed_outcome_frequency", float("nan")), ("observed_outcome_frequency", -0.1), ("observed_outcome_frequency", 1.1),
    ("ordered_bin_posture", "wrong"),
])
def test_every_calibration_field_defect(field: str, bad: object) -> None:
    payload = replace(_payloads()[EvaluationResultKind.CALIBRATION_BIN_RESULT], **{field: bad})
    assert _codes(**_valid_for_kind(EvaluationResultKind.CALIBRATION_BIN_RESULT, payload)) == (C.INVALID_CALIBRATION_BIN_PAYLOAD,)


def test_calibration_eligible_dependency() -> None:
    payload = replace(_payloads()[EvaluationResultKind.CALIBRATION_BIN_RESULT], sample_count=99)
    assert _codes(**_valid_for_kind(EvaluationResultKind.CALIBRATION_BIN_RESULT, payload)) == (C.INVALID_CALIBRATION_BIN_PAYLOAD,)
    assert _codes(eligible_record_count=-1, **_valid_for_kind(EvaluationResultKind.CALIBRATION_BIN_RESULT, payload)) == (C.INVALID_RECORD_COUNT,)


@pytest.mark.parametrize("field,bad", [
    ("decomposition_policy_id", ""), ("decomposition_policy_id", TextSubclass("policy")),
    ("reliability_value", 0), ("reliability_value", -0.1), ("reliability_value", float("nan")),
    ("resolution_value", 0), ("resolution_value", -0.1), ("resolution_value", float("inf")),
    ("uncertainty_value", 0), ("uncertainty_value", -0.1), ("uncertainty_value", float("-inf")),
    ("component_posture", "wrong"),
])
def test_every_decomposition_field_defect(field: str, bad: object) -> None:
    payload = replace(_payloads()[EvaluationResultKind.DECOMPOSITION_RESULT], **{field: bad})
    assert _codes(**_valid_for_kind(EvaluationResultKind.DECOMPOSITION_RESULT, payload)) == (C.INVALID_DECOMPOSITION_PAYLOAD,)


@pytest.mark.parametrize("field,bad", [
    ("pit_treatment_policy_id", ""), ("ordered_bin_ids", []), ("ordered_bin_ids", ()),
    ("ordered_bin_ids", ("a",)), ("ordered_bin_ids", ("a", "a")), ("ordered_bin_ids", ("a", "")),
    ("ordered_bin_ids", ("a", TextSubclass("b"))), ("ordered_bin_counts", []),
    ("ordered_bin_counts", ()), ("ordered_bin_counts", (1,)), ("ordered_bin_counts", (1, True)),
    ("ordered_bin_counts", (1, -1)), ("ordered_content_posture", "wrong"),
])
def test_every_distribution_field_defect(field: str, bad: object) -> None:
    payload = replace(_payloads()[EvaluationResultKind.DISTRIBUTION_DIAGNOSTIC_RESULT], **{field: bad})
    assert _codes(**_valid_for_kind(EvaluationResultKind.DISTRIBUTION_DIAGNOSTIC_RESULT, payload)) == (C.INVALID_DISTRIBUTION_DIAGNOSTIC_PAYLOAD,)


def test_distribution_sum_dependency() -> None:
    payload = replace(_payloads()[EvaluationResultKind.DISTRIBUTION_DIAGNOSTIC_RESULT], ordered_bin_counts=(4, 5))
    assert _codes(**_valid_for_kind(EvaluationResultKind.DISTRIBUTION_DIAGNOSTIC_RESULT, payload)) == (C.INVALID_DISTRIBUTION_DIAGNOSTIC_PAYLOAD,)
    assert _codes(eligible_record_count=-1, **_valid_for_kind(EvaluationResultKind.DISTRIBUTION_DIAGNOSTIC_RESULT, payload)) == (C.INVALID_RECORD_COUNT,)


@pytest.mark.parametrize("field,bad", [
    ("tie_treatment_policy_id", ""), ("ordered_rank_ids", []), ("ordered_rank_ids", ()),
    ("ordered_rank_ids", ("a",)), ("ordered_rank_ids", ("a", "a")), ("ordered_rank_ids", ("a", "")),
    ("ordered_rank_counts", []), ("ordered_rank_counts", ()), ("ordered_rank_counts", (1,)),
    ("ordered_rank_counts", (1, True)), ("ordered_rank_counts", (1, -1)),
    ("ensemble_comparability_posture", "wrong"), ("ordered_content_posture", "wrong"),
])
def test_every_ensemble_field_defect(field: str, bad: object) -> None:
    payload = replace(_payloads()[EvaluationResultKind.ENSEMBLE_DIAGNOSTIC_RESULT], **{field: bad})
    assert _codes(**_valid_for_kind(EvaluationResultKind.ENSEMBLE_DIAGNOSTIC_RESULT, payload)) == (C.INVALID_ENSEMBLE_DIAGNOSTIC_PAYLOAD,)


def test_ensemble_sum_dependency() -> None:
    payload = replace(_payloads()[EvaluationResultKind.ENSEMBLE_DIAGNOSTIC_RESULT], ordered_rank_counts=(4, 5))
    assert _codes(**_valid_for_kind(EvaluationResultKind.ENSEMBLE_DIAGNOSTIC_RESULT, payload)) == (C.INVALID_ENSEMBLE_DIAGNOSTIC_PAYLOAD,)
    assert _codes(eligible_record_count=-1, **_valid_for_kind(EvaluationResultKind.ENSEMBLE_DIAGNOSTIC_RESULT, payload)) == (C.INVALID_RECORD_COUNT,)


@pytest.mark.parametrize("field,bad", [
    ("candidate_result_id", ""), ("candidate_result_id", 7), ("candidate_result_id", TextSubclass("candidate")),
    ("baseline_result_id", ""), ("baseline_result_id", 7), ("baseline_result_id", TextSubclass("baseline")),
    ("paired_comparison_value", 0), ("paired_comparison_value", float("nan")),
    ("paired_comparison_value", float("inf")), ("comparison_direction", "wrong"),
    ("paired_scope_posture", "wrong"),
])
def test_every_paired_generic_field_defect(field: str, bad: object) -> None:
    payload = replace(_payloads()[EvaluationResultKind.PAIRED_COMPARISON_RESULT], **{field: bad})
    assert _codes(**_valid_for_kind(EvaluationResultKind.PAIRED_COMPARISON_RESULT, payload)) == (C.INVALID_PAIRED_COMPARISON_PAYLOAD,)


@pytest.mark.parametrize("baseline", ["climatology", TextSubclass("climatology"), UnrelatedEnum.VALUE, object(), None])
def test_each_unapproved_paired_baseline_has_no_generic_double_classification(baseline: object) -> None:
    payload = replace(_payloads()[EvaluationResultKind.PAIRED_COMPARISON_RESULT], baseline_type=baseline)
    assert _codes(**_valid_for_kind(EvaluationResultKind.PAIRED_COMPARISON_RESULT, payload)) == (C.PAIR_BASELINE_NOT_APPROVED,)


def test_paired_independent_codes_and_collision_prerequisites() -> None:
    base = _payloads()[EvaluationResultKind.PAIRED_COMPARISON_RESULT]
    for baseline in (BaselineType.CLIMATOLOGY, BaselineType.PERSISTENCE):
        assert _codes(**_valid_for_kind(EvaluationResultKind.PAIRED_COMPARISON_RESULT, replace(base, baseline_type=baseline))) == ()
    collision = replace(base, candidate_result_id="same", baseline_result_id="same")
    assert _codes(**_valid_for_kind(EvaluationResultKind.PAIRED_COMPARISON_RESULT, collision)) == (C.PAIR_RESULT_IDENTITY_COLLISION,)
    all_three = replace(collision, baseline_type="bad", comparison_direction="bad")
    assert _codes(**_valid_for_kind(EvaluationResultKind.PAIRED_COMPARISON_RESULT, all_three)) == (
        C.INVALID_PAIRED_COMPARISON_PAYLOAD, C.PAIR_BASELINE_NOT_APPROVED, C.PAIR_RESULT_IDENTITY_COLLISION,
    )
    malformed_equal = replace(base, candidate_result_id=TextSubclass("same"), baseline_result_id=TextSubclass("same"))
    assert _codes(**_valid_for_kind(EvaluationResultKind.PAIRED_COMPARISON_RESULT, malformed_equal)) == (C.INVALID_PAIRED_COMPARISON_PAYLOAD,)


@pytest.mark.parametrize("value,expected", [
    (None, ()), ("other", ()), ("result-1", (C.SELF_SUPERSESSION,)),
    ("", (C.BLANK_REQUIRED_TEXT,)), (7, (C.BLANK_REQUIRED_TEXT,)),
    (TextSubclass("result-1"), (C.BLANK_REQUIRED_TEXT,)),
])
def test_complete_supersession_matrix(value: object, expected: tuple[C, ...]) -> None:
    assert _codes(supersedes_result_id_when_applicable=value) == expected


def test_absent_optional_mapping_key_is_valid() -> None:
    values = _values()
    del values["supersedes_result_id_when_applicable"]
    record, result = evaluation_result_record_from_mapping(values)
    assert result.codes == () and record is not None
    assert record.supersedes_result_id_when_applicable is None


def test_result_invariants_immutability_and_repetition() -> None:
    passed = EvaluationResultValidationResult(EvaluationResultValidationSeverity.BLOCKED, False, [])  # type: ignore[arg-type]
    blocked = EvaluationResultValidationResult(EvaluationResultValidationSeverity.PASSED, True, [C.INVALID_RECORD_COUNT, C.INVALID_RECORD_COUNT])  # type: ignore[arg-type]
    assert (passed.severity, passed.passed, passed.codes) == (EvaluationResultValidationSeverity.PASSED, True, ())
    assert (blocked.severity, blocked.passed, blocked.codes) == (EvaluationResultValidationSeverity.BLOCKED, False, (C.INVALID_RECORD_COUNT, C.INVALID_RECORD_COUNT))
    with pytest.raises(FrozenInstanceError):
        blocked.passed = True  # type: ignore[misc]


def test_complete_cross_group_order_and_no_partial_record() -> None:
    values = _values(
        evaluation_result_id=" ", result_kind="bad", artifact_id="bad", method_role="bad",
        prediction_representation="bad", support_status="bad", target_posture=" ",
        eligible_record_count=-1, excluded_record_count=-1, blocked_record_count=-1,
        total_considered_record_count=-1, exclusion_block_reason_summary=("",),
        uncertainty_method_id="method", uncertainty_level_id=None, provenance=("", 1),
        result_created_at=" ", result_payload=object(), supersedes_result_id_when_applicable=" ",
    )
    del values["artifact_version"]
    values["z-extra"] = 1
    values[4] = 2
    record, result = evaluation_result_record_from_mapping(values)
    assert record is None
    assert result.codes == (
        C.MISSING_REQUIRED_FIELD, C.UNEXPECTED_FIELD, C.UNEXPECTED_FIELD,
        C.BLANK_REQUIRED_TEXT, C.BLANK_REQUIRED_TEXT, C.BLANK_REQUIRED_TEXT, C.BLANK_REQUIRED_TEXT,
        C.INVALID_RESULT_KIND, C.INVALID_ARTIFACT, C.INVALID_METHOD_ROLE,
        C.INVALID_PREDICTION_REPRESENTATION, C.INVALID_SUPPORT_STATUS, C.INVALID_FIXED_POSTURE,
        C.INVALID_RECORD_COUNT, C.INVALID_RECORD_COUNT, C.INVALID_RECORD_COUNT, C.INVALID_RECORD_COUNT,
        C.INVALID_REASON_SUMMARY, C.UNCERTAINTY_FIELDS_MISMATCH,
        C.INVALID_PROVENANCE_REF, C.INVALID_PROVENANCE_REF, C.INVALID_RESULT_CREATED_AT,
    )


def test_payload_type_and_supersession_order() -> None:
    assert _codes(result_payload=object(), supersedes_result_id_when_applicable="result-1") == (
        C.INVALID_PAYLOAD_TYPE, C.SELF_SUPERSESSION,
    )


def test_production_ast_purity_and_exact_payload_type_acceptance() -> None:
    tree = ast.parse(SOURCE)
    forbidden_import_roots = {"os", "sys", "pathlib", "socket", "subprocess", "sqlite3", "duckdb", "requests", "urllib", "json", "pickle"}
    forbidden_calls = {"open", "input", "connect", "system", "popen", "run", "getenv", "time", "now", "utcnow", "dump", "dumps", "load", "loads"}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            assert all(alias.name.split(".")[0] not in forbidden_import_roots for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            assert node.module.split(".")[0] not in forbidden_import_roots
        elif isinstance(node, ast.Call):
            name = node.func.id if isinstance(node.func, ast.Name) else node.func.attr if isinstance(node.func, ast.Attribute) else ""
            assert name not in forbidden_calls
    assert "isinstance(payload" not in SOURCE
    for forbidden in ("paper_trade", "place_order", "backtest", "serialize(", "persist(", "orchestrator", "autonomy"):
        assert forbidden not in SOURCE.lower()


def test_all_dataclass_instances_and_caller_objects_remain_frozen_or_unchanged() -> None:
    payloads = tuple(_payloads().values())
    for payload in payloads:
        with pytest.raises(FrozenInstanceError):
            setattr(payload, fields(payload)[0].name, None)
    record = EvaluationResultRecord(**_values())
    before = (record, payloads)
    assert validate_evaluation_result_record(record) == validate_evaluation_result_record(record)
    assert (record, payloads) == before
