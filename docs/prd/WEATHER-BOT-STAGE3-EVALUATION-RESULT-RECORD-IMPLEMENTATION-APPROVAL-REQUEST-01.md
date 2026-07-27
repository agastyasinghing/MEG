# WEATHER-BOT-STAGE3-EVALUATION-RESULT-RECORD-IMPLEMENTATION-APPROVAL-REQUEST-01

Canonical ID: WEATHER-BOT-STAGE3-EVALUATION-RESULT-RECORD-IMPLEMENTATION-APPROVAL-REQUEST-01

## Status and decision boundary

This is a deterministic docs/static-test-only approval request. Current status: `request_prepared_implementation_not_approved`. Decision options, in order:

1. `approve_later_evaluation_result_record_implementation_ticket`
2. `request_approval_request_revision`
3. `hold`
4. `block`

Only a separate human approval may authorize `WEATHER-BOT-STAGE3-EVALUATION-RESULT-RECORD-IMPLEMENTATION-01`. This request does not approve or implement it.

## Predecessor and base

Externally verified repository facts, locally confirmed without a preview merge SHA: `ACTUAL_PR_374_MERGE_SHA = 96935708eea4b197283a5a399c8ef57e63b6e795` and `BASE_SHA = 96935708eea4b197283a5a399c8ef57e63b6e795`. PR #374 approved head `e1bbd931813dc79d0254592a51584653bddb5dab` is an ancestor of that actual merge commit. Remote fetch was unavailable in the sandbox.

## Authority and requested future slice

The merged evaluation-result-record planning contract remains authoritative, reconciled with the merged binary-probability record, strict OOS split, baseline contracts, scoring-and-diagnostics modules, and focused tests. Do not invent numeric tolerances, sample minimums, confidence levels, bin counts, resampling lengths, weighting constants, economic thresholds, or claim rules.

A later separately approved slice may create exactly:

1. `meg/weather/stage3/evaluation_result_record.py`
2. `tests/core/test_weather_bot_stage3_evaluation_result_record.py`

No existing file may be modified. The slice is limited to immutable caller-supplied records and payloads, mapping adaptation, and pure fail-closed validation. It must not calculate a score, diagnostic, paired comparison, uncertainty interval, support status, result, or claim.

## Exact public API

Freeze exactly 15 public symbols in source order:

1. `EvaluationResultKind`
2. `EvaluationResultSupportStatus`
3. `EvaluationResultMethodRole`
4. `EvaluationResultValidationSeverity`
5. `EvaluationResultValidationCode`
6. `ScalarScoreResultPayload`
7. `CalibrationBinResultPayload`
8. `DecompositionResultPayload`
9. `DistributionDiagnosticResultPayload`
10. `EnsembleDiagnosticResultPayload`
11. `PairedComparisonResultPayload`
12. `EvaluationResultRecord`
13. `EvaluationResultValidationResult`
14. `evaluation_result_record_from_mapping`
15. `validate_evaluation_result_record`

The future module may import `BaselineType`, `ScoringArtifact`, and `ScoringPredictionRepresentation`, but must not re-export them. No collection validator is approved.

## Exact enums

Every enum uses `StrEnum`.

| Enum | Member | Value |
| --- | --- | --- |
| EvaluationResultKind | SCALAR_SCORE_RESULT | `scalar_score_result` |
| EvaluationResultKind | CALIBRATION_BIN_RESULT | `calibration_bin_result` |
| EvaluationResultKind | DECOMPOSITION_RESULT | `decomposition_result` |
| EvaluationResultKind | DISTRIBUTION_DIAGNOSTIC_RESULT | `distribution_diagnostic_result` |
| EvaluationResultKind | ENSEMBLE_DIAGNOSTIC_RESULT | `ensemble_diagnostic_result` |
| EvaluationResultKind | PAIRED_COMPARISON_RESULT | `paired_comparison_result` |
| EvaluationResultSupportStatus | SUPPORTED | `supported` |
| EvaluationResultSupportStatus | INSUFFICIENT | `insufficient` |
| EvaluationResultSupportStatus | BLOCKED | `blocked` |
| EvaluationResultSupportStatus | UNAVAILABLE | `unavailable` |
| EvaluationResultMethodRole | CANDIDATE | `candidate` |
| EvaluationResultMethodRole | CLIMATOLOGY_BASELINE | `climatology_baseline` |
| EvaluationResultMethodRole | PERSISTENCE_BASELINE | `persistence_baseline` |
| EvaluationResultMethodRole | PAIRED_COMPARISON | `paired_comparison` |
| EvaluationResultValidationSeverity | PASSED | `passed` |
| EvaluationResultValidationSeverity | BLOCKED | `blocked` |

## Immutable payloads

Each payload uses `@dataclass(frozen=True)`, performs no validation or normalization in `__post_init__`, and has exact fields in order:

- `ScalarScoreResultPayload`: `result_value: float`; `score_direction: str`; `result_domain_posture: str`. Fixed: `score_direction = lower_is_better`; `result_domain_posture = artifact_specific_domain_validated`.
- `CalibrationBinResultPayload`: `bin_id: str`; `bin_index: int`; `bin_boundary_policy_id: str`; `sample_count: int`; `mean_predicted_probability: float`; `observed_outcome_frequency: float`; `ordered_bin_posture: str`. Fixed: `ordered_bin_posture = predeclared_order_required`.
- `DecompositionResultPayload`: `decomposition_policy_id: str`; `reliability_value: float`; `resolution_value: float`; `uncertainty_value: float`; `component_posture: str`. Fixed: `component_posture = reliability_resolution_uncertainty_required`.
- `DistributionDiagnosticResultPayload`: `pit_treatment_policy_id: str`; `ordered_bin_ids: tuple[str, ...]`; `ordered_bin_counts: tuple[int, ...]`; `ordered_content_posture: str`. Fixed: `ordered_content_posture = predeclared_order_required`.
- `EnsembleDiagnosticResultPayload`: `tie_treatment_policy_id: str`; `ordered_rank_ids: tuple[str, ...]`; `ordered_rank_counts: tuple[int, ...]`; `ensemble_comparability_posture: str`; `ordered_content_posture: str`. Fixed: `ensemble_comparability_posture = finite_comparable_ensemble_required`; `ordered_content_posture = predeclared_order_required`.
- `PairedComparisonResultPayload`: `candidate_result_id: str`; `baseline_result_id: str`; `baseline_type: BaselineType`; `comparison_direction: str`; `paired_comparison_value: float`; `paired_scope_posture: str`. Fixed: `comparison_direction = candidate_minus_baseline_lower_is_better`; `paired_scope_posture = exact_common_test_record_set_required`.

## Evaluation result record

Freeze `@dataclass(frozen=True) EvaluationResultRecord` with exact ordered fields:

1. `evaluation_result_id: str`
2. `result_kind: EvaluationResultKind`
3. `artifact_id: ScoringArtifact`
4. `artifact_version: str`
5. `evaluation_definition_id: str`
6. `evaluation_definition_version: str`
7. `evaluation_run_id: str`
8. `method_role: EvaluationResultMethodRole`
9. `method_id: str`
10. `method_version: str`
11. `prediction_representation: ScoringPredictionRepresentation`
12. `target_posture: str`
13. `split_id: str`
14. `split_version: str`
15. `fold_id: str`
16. `cutoff_identity: str`
17. `paired_test_record_set_id: str`
18. `eligibility_policy_id: str`
19. `aggregation_rule_id: str`
20. `weighting_rule_id: str`
21. `stratum_id: str`
22. `eligible_record_count: int`
23. `excluded_record_count: int`
24. `blocked_record_count: int`
25. `total_considered_record_count: int`
26. `exclusion_block_reason_summary: tuple[str, ...]`
27. `uncertainty_method_id: str | None`
28. `uncertainty_level_id: str | None`
29. `support_status: EvaluationResultSupportStatus`
30. `result_payload: ScalarScoreResultPayload | CalibrationBinResultPayload | DecompositionResultPayload | DistributionDiagnosticResultPayload | EnsembleDiagnosticResultPayload | PairedComparisonResultPayload`
31. `provenance: tuple[str, ...]`
32. `result_created_at: str`
33. `supersedes_result_id_when_applicable: str | None = None`

No value may be generated and no validation occurs in `EvaluationResultRecord.__post_init__`.

## Validation result and signatures

Freeze `@dataclass(frozen=True) EvaluationResultValidationResult` fields:

1. `severity: EvaluationResultValidationSeverity`
2. `passed: bool`
3. `codes: tuple[EvaluationResultValidationCode, ...] = ()`

Empty codes force `PASSED` and `passed is True`; nonempty codes force `BLOCKED` and `passed is False`.

```python
def evaluation_result_record_from_mapping(
    mapping: object,
) -> tuple[
    EvaluationResultRecord | None,
    EvaluationResultValidationResult,
]:
```

```python
def validate_evaluation_result_record(
    record: EvaluationResultRecord,
) -> EvaluationResultValidationResult:
```

The adapter is public source position 14 and direct validator position 15.

## Mapping keys, shape, and adaptation

Required keys 1 through 32, in order:

1. `evaluation_result_id`
2. `result_kind`
3. `artifact_id`
4. `artifact_version`
5. `evaluation_definition_id`
6. `evaluation_definition_version`
7. `evaluation_run_id`
8. `method_role`
9. `method_id`
10. `method_version`
11. `prediction_representation`
12. `target_posture`
13. `split_id`
14. `split_version`
15. `fold_id`
16. `cutoff_identity`
17. `paired_test_record_set_id`
18. `eligibility_policy_id`
19. `aggregation_rule_id`
20. `weighting_rule_id`
21. `stratum_id`
22. `eligible_record_count`
23. `excluded_record_count`
24. `blocked_record_count`
25. `total_considered_record_count`
26. `exclusion_block_reason_summary`
27. `uncertainty_method_id`
28. `uncertainty_level_id`
29. `support_status`
30. `result_payload`
31. `provenance`
32. `result_created_at`

Only `supersedes_result_id_when_applicable` is optional. Nullable uncertainty keys remain required even when `None`. Readable mappings recognize keys only when `type(key) is str`. Shape order is: missing required keys in field order; unexpected exact built-in string keys in lexical order; all remaining keys in original Mapping iteration order. A string-subclass key cannot satisfy a required key and is unexpected. Shape failures do not return early.

Enum fields `result_kind`, `artifact_id`, `method_role`, `prediction_representation`, and `support_status` accept only the exact enum member or an exact built-in string matching a value. Reject string subclasses, unrelated enums, invalid strings, and other values. Only actual lists for `exclusion_block_reason_summary` and `provenance` may adapt to tuples. A payload must already be one exact approved payload dataclass; never adapt a nested mapping. Direct validation performs no enum or list adaptation.

A non-Mapping root or ordinary exception during root snapshot or materialization returns no record and a blocked result with exactly 32 ordered `MISSING_REQUIRED_FIELD` codes. Catch `Exception`, never `BaseException`. Never construct or return a partial record.

## Text, timestamp, posture, and supersession

Required exact built-in nonblank text validation order: `evaluation_result_id`, `artifact_version`, `evaluation_definition_id`, `evaluation_definition_version`, `evaluation_run_id`, `method_id`, `method_version`, `target_posture`, `split_id`, `split_version`, `fold_id`, `cutoff_identity`, `paired_test_record_set_id`, `eligibility_policy_id`, `aggregation_rule_id`, `weighting_rule_id`, `stratum_id`, `result_created_at`.

Nullable text order: `uncertainty_method_id`, `uncertainty_level_id`, `supersedes_result_id_when_applicable`. A valid non-null value requires `type(value) is str` and nonempty `value.strip()`. Never strip or rewrite values. Payload text and tuple entries are validated only in their payload group.

`result_created_at` requires an exact built-in RFC3339/ISO-8601 string with explicit UTC offset. Reject malformed, naive, non-string, and string-subclass values; do not compare with the clock, generate, or rewrite it.

Require exactly `target_posture = venue_defined_settlement_outcome`. Blank, non-string, or same-valued string subclasses may receive both `BLANK_REQUIRED_TEXT` and `INVALID_FIXED_POSTURE`.

Append `SELF_SUPERSESSION` exactly once only when both `evaluation_result_id` and `supersedes_result_id_when_applicable` are valid exact built-in nonblank strings and equal. Never generate or rewrite identities.

## Counts, reasons, uncertainty, and provenance

`eligible_record_count`, `excluded_record_count`, `blocked_record_count`, and `total_considered_record_count` require exact built-in integers >= 0. Reject bool, subclasses, floats, strings, and negatives; emit one `INVALID_RECORD_COUNT` per invalid field in field order. Only if all are valid require `total_considered_record_count == eligible_record_count + excluded_record_count + blocked_record_count`; otherwise suppress `SAMPLE_ACCOUNTING_MISMATCH`.

Mapping accepts an actual tuple or list reason summary; direct validation requires an actual tuple. Every entry is an exact built-in nonblank string, caller order is preserved, duplicates are rejected, and any container, entry, or duplicate defect emits exactly one `INVALID_REASON_SUMMARY`. A nonempty valid summary is required when excluded or blocked count is positive or support is `INSUFFICIENT`, `BLOCKED`, or `UNAVAILABLE`; with valid prerequisites and empty summary append `MISSING_REQUIRED_REASON`. Never infer reasons.

Uncertainty method and level must both be `None` or both valid exact built-in nonblank strings. Exactly one valid field being `None` appends `UNCERTAINTY_FIELDS_MISMATCH`; suppress it when either non-null value is text-invalid. Never select or interpret uncertainty.

Mapping accepts actual tuple/list provenance; direct validation requires actual tuple. Wrong container gives one `INVALID_PROVENANCE_REF`; empty accepted container gives one `EMPTY_PROVENANCE`; each malformed entry gives one `INVALID_PROVENANCE_REF` in caller order. Valid duplicates/order are preserved. Empty and malformed-entry codes are mutually exclusive. Never generate, resolve, look up, sort, or deduplicate references.

## Compatibility matrices

| Result kind | Approved artifacts | Exact payload |
| --- | --- | --- |
| scalar_score_result | brier_score, log_score, crps, threshold_weighted_crps | ScalarScoreResultPayload |
| calibration_bin_result | reliability_diagram | CalibrationBinResultPayload |
| decomposition_result | brier_decomposition | DecompositionResultPayload |
| distribution_diagnostic_result | pit_histogram | DistributionDiagnosticResultPayload |
| ensemble_diagnostic_result | rank_histogram | EnsembleDiagnosticResultPayload |
| paired_comparison_result | brier_score, log_score, crps, threshold_weighted_crps | PairedComparisonResultPayload |

Mismatch emits `RESULT_KIND_ARTIFACT_MISMATCH` and/or `INVALID_PAYLOAD_TYPE` as applicable.

Representation matrix: Brier, log, reliability, and decomposition require `binary_outcome_probability`; CRPS, PIT, and threshold-weighted CRPS require `full_predictive_distribution`; rank histogram requires `finite_comparable_ensemble`. Evaluate only when artifact and representation are valid.

Method-role matrix: `paired_comparison_result` requires `paired_comparison`; every other valid kind forbids it and permits only `candidate`, `climatology_baseline`, or `persistence_baseline`. Evaluate only when kind and role are valid.

## Payload validation

All payloads remain frozen and unchanged. Count-like fields require exact built-in nonnegative `int`; numeric results require exact built-in finite `float`. Reject bool, subclasses, integers where float is required, NaN, and infinities.

- Scalar: exact fixed postures; Brier in `[0.0, 1.0]`; log, CRPS, and threshold-weighted CRPS >= `0.0`; any failure gives one `INVALID_SCALAR_SCORE_PAYLOAD`.
- Calibration: exact nonblank bin/policy identities; nonnegative bin index/sample count; sample count equals eligible count; probabilities/frequencies in `[0.0, 1.0]`; exact posture; any failure gives one `INVALID_CALIBRATION_BIN_PAYLOAD`.
- Decomposition: exact nonblank policy identity; finite nonnegative reliability, resolution, uncertainty; exact posture; any failure gives one `INVALID_DECOMPOSITION_PAYLOAD`.
- Distribution: exact nonblank PIT policy; exact nonempty equal-length tuples; unique nonblank exact-string bin IDs; nonnegative exact-int counts summing to eligible count; exact posture; any failure gives one `INVALID_DISTRIBUTION_DIAGNOSTIC_PAYLOAD`.
- Ensemble: exact nonblank tie policy; exact nonempty equal-length tuples; unique nonblank exact-string rank IDs; nonnegative exact-int counts summing to eligible count; exact comparability/order postures; any failure gives one `INVALID_ENSEMBLE_DIAGNOSTIC_PAYLOAD`.
- Paired comparison: exact nonblank distinct candidate/baseline IDs; exact `BaselineType.CLIMATOLOGY` or `BaselineType.PERSISTENCE`; exact direction/scope postures; exact finite float value. Unapproved baseline gives `PAIR_BASELINE_NOT_APPROVED`; equal IDs give `PAIR_RESULT_IDENTITY_COLLISION`; other failures give `INVALID_PAIRED_COMPARISON_PAYLOAD`. Never calculate or recompute comparison.

## Validation codes

Freeze this ordered `StrEnum` with matching snake-case values:

1. `MISSING_REQUIRED_FIELD = "missing_required_field"`
2. `UNEXPECTED_FIELD = "unexpected_field"`
3. `BLANK_REQUIRED_TEXT = "blank_required_text"`
4. `INVALID_RESULT_KIND = "invalid_result_kind"`
5. `INVALID_ARTIFACT = "invalid_artifact"`
6. `INVALID_METHOD_ROLE = "invalid_method_role"`
7. `INVALID_PREDICTION_REPRESENTATION = "invalid_prediction_representation"`
8. `INVALID_SUPPORT_STATUS = "invalid_support_status"`
9. `INVALID_FIXED_POSTURE = "invalid_fixed_posture"`
10. `INVALID_RECORD_COUNT = "invalid_record_count"`
11. `SAMPLE_ACCOUNTING_MISMATCH = "sample_accounting_mismatch"`
12. `INVALID_REASON_SUMMARY = "invalid_reason_summary"`
13. `MISSING_REQUIRED_REASON = "missing_required_reason"`
14. `UNCERTAINTY_FIELDS_MISMATCH = "uncertainty_fields_mismatch"`
15. `EMPTY_PROVENANCE = "empty_provenance"`
16. `INVALID_PROVENANCE_REF = "invalid_provenance_ref"`
17. `INVALID_RESULT_CREATED_AT = "invalid_result_created_at"`
18. `RESULT_KIND_ARTIFACT_MISMATCH = "result_kind_artifact_mismatch"`
19. `REPRESENTATION_MISMATCH = "representation_mismatch"`
20. `METHOD_ROLE_MISMATCH = "method_role_mismatch"`
21. `INVALID_PAYLOAD_TYPE = "invalid_payload_type"`
22. `INVALID_SCALAR_SCORE_PAYLOAD = "invalid_scalar_score_payload"`
23. `INVALID_CALIBRATION_BIN_PAYLOAD = "invalid_calibration_bin_payload"`
24. `INVALID_DECOMPOSITION_PAYLOAD = "invalid_decomposition_payload"`
25. `INVALID_DISTRIBUTION_DIAGNOSTIC_PAYLOAD = "invalid_distribution_diagnostic_payload"`
26. `INVALID_ENSEMBLE_DIAGNOSTIC_PAYLOAD = "invalid_ensemble_diagnostic_payload"`
27. `INVALID_PAIRED_COMPARISON_PAYLOAD = "invalid_paired_comparison_payload"`
28. `PAIR_BASELINE_NOT_APPROVED = "pair_baseline_not_approved"`
29. `PAIR_RESULT_IDENTITY_COLLISION = "pair_result_identity_collision"`
30. `SELF_SUPERSESSION = "self_supersession"`

No other or dynamically generated validation code is approved.

## Validation order

For readable mappings exact groups are: (1) missing keys; (2) unexpected exact-string keys; (3) unexpected non-string keys; (4) required and nullable text; (5) result kind; (6) artifact; (7) method role; (8) prediction representation; (9) support status; (10) fixed posture; (11) counts; (12) sample-accounting identity; (13) reason-summary structure; (14) required-reason consistency; (15) uncertainty pairing; (16) provenance; (17) result-created timestamp; (18) result-kind/artifact compatibility; (19) representation compatibility; (20) method-role compatibility; (21) payload type; (22) payload content; (23) paired baseline; (24) paired identity collision; (25) self-supersession.

Aggregate every diagnosable present-value failure. Suppress only checks whose prerequisites are missing or unusable. Preserve repeated occurrences; never finally sort or deduplicate.

## Safety, dependencies, and non-goals

Standard library only for static testing. No dependency, workflow, configuration, environment, credential, schema, migration, fixture, data, service, network, subprocess, database, DuckDB, Parquet, persistence, Phase 0A rail, or either Phase 0A job changes are approved. Phase 0B and DuckDB remain unaffected. Canonical routing remains exactly `condition_id`, `token_id`, and `outcome`; `market_id` remains non-routing and `token_outcome_pair` remains derived only.

Explicitly denied: score calculation; diagnostic calculation; comparison calculation; uncertainty calculation; support-status selection; probability generation; label joining; split or baseline execution; evaluation execution; claim creation or evaluation; evidence-gate evaluation; data or corpus creation; source fetching; persistence; serialization; database tables or migrations; reports or exports; backtesting or simulation; market-price comparison execution; paper trading; trading; order placement; runtime orchestration; autonomy; production behavior.

## Machine assignments

ticket_id: `WEATHER-BOT-STAGE3-EVALUATION-RESULT-RECORD-IMPLEMENTATION-APPROVAL-REQUEST-01`
canonical_id: `WEATHER-BOT-STAGE3-EVALUATION-RESULT-RECORD-IMPLEMENTATION-APPROVAL-REQUEST-01`
actual_pr_374_merge_sha: `96935708eea4b197283a5a399c8ef57e63b6e795`
base_sha: `96935708eea4b197283a5a399c8ef57e63b6e795`
current_status: `request_prepared_implementation_not_approved`
future_ticket: `WEATHER-BOT-STAGE3-EVALUATION-RESULT-RECORD-IMPLEMENTATION-01`
future_file_count: `2`
public_symbol_count: `15`
payload_count: `6`
record_field_count: `33`
required_mapping_key_count: `32`
optional_mapping_key_count: `1`
validation_code_count: `30`
validation_group_count: `25`
decision_options: `approve_later_evaluation_result_record_implementation_ticket`, `request_approval_request_revision`, `hold`, `block`

## Acceptance criteria

Acceptance freezes the exact title/ID, predecessor, future files, API, enums, payload/record/result fields, signatures, keys, adaptation, text/timestamp/posture/count/reason/uncertainty/provenance rules, compatibility matrices, payload validation, codes/order, decisions/status, machine assignments, safety and non-goals. It remains approval-request-only and requires its deterministic independent-literal static test and direct per-path canonical allowlist registration.
