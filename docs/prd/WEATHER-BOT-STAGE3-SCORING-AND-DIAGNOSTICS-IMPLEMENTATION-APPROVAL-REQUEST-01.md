# WEATHER-BOT-STAGE3-SCORING-AND-DIAGNOSTICS-IMPLEMENTATION-APPROVAL-REQUEST-01

Canonical ID: WEATHER-BOT-STAGE3-SCORING-AND-DIAGNOSTICS-IMPLEMENTATION-APPROVAL-REQUEST-01

## Status

This is a docs/static-test-only, approval-request-only artifact. Its current status is `request_prepared_implementation_not_approved`; it neither grants approval nor implements scoring or diagnostics.

## Predecessor

PR #372 is merged as `ACTUAL_PR_372_MERGE_SHA = be07b2b48b5243d7f4f69c61a9999a78983772de`. Approved head `38888b42ddfc580d1fb348f69503ec63bf0c0ff0` is its ancestor, and the merge is the branch base: `BASE_SHA = be07b2b48b5243d7f4f69c61a9999a78983772de`. No preview merge SHA is used.

## Decision boundary

This request asks humans whether the later ticket may be approved. Only a separate human decision can authorize `WEATHER-BOT-STAGE3-SCORING-AND-DIAGNOSTICS-IMPLEMENTATION-01`.

## Planning basis

The authoritative basis is `docs/prd/WEATHER-BOT-STAGE3-SCORING-AND-DIAGNOSTICS-CONTRACT-PLANNING-01.md`, reconciled with the merged evaluation-result and baseline approval contracts, `binary_probability_record.py`, `strict_oos_split.py`, `baseline_contracts.py`, and focused tests. The planning contract remains authoritative. No clipping constant, tolerance, bin count, sample minimum, confidence or interval level, tie constant, bootstrap design, resampling length, weighting or aggregation value, threshold-weight function, or evidence threshold is selected.

## Requested slice

The later slice is limited to immutable caller-supplied scoring/diagnostic definitions and pure fail-closed validation. It must not calculate any score or diagnostic, select or interpret a policy, or generate any value. There is no validation in `__post_init__`.

## Future files

A separately approved implementation may create exactly:

1. `meg/weather/stage3/scoring_and_diagnostics.py`
2. `tests/core/test_weather_bot_stage3_scoring_and_diagnostics.py`

No existing file may be modified.

## Public API

Freeze exactly nine public symbols, in order:

1. `ScoringArtifact`
2. `ScoringPredictionRepresentation`
3. `ScoringDefinitionStatus`
4. `ScoringValidationSeverity`
5. `ScoringValidationCode`
6. `ScoringDiagnosticDefinition`
7. `ScoringDiagnosticValidationResult`
8. `scoring_diagnostic_definition_from_mapping`
9. `validate_scoring_diagnostic_definition`

`BaselineType` may be imported but must not be re-exported. No collection validator is approved.

## Enums

Use `StrEnum` and freeze these matrices:

| Enum | Member | Value |
| --- | --- | --- |
| ScoringArtifact | BRIER_SCORE | `brier_score` |
| ScoringArtifact | LOG_SCORE | `log_score` |
| ScoringArtifact | RELIABILITY_DIAGRAM | `reliability_diagram` |
| ScoringArtifact | BRIER_DECOMPOSITION | `brier_decomposition` |
| ScoringArtifact | CRPS | `crps` |
| ScoringArtifact | PIT_HISTOGRAM | `pit_histogram` |
| ScoringArtifact | RANK_HISTOGRAM | `rank_histogram` |
| ScoringArtifact | THRESHOLD_WEIGHTED_CRPS | `threshold_weighted_crps` |
| ScoringPredictionRepresentation | BINARY_OUTCOME_PROBABILITY | `binary_outcome_probability` |
| ScoringPredictionRepresentation | FULL_PREDICTIVE_DISTRIBUTION | `full_predictive_distribution` |
| ScoringPredictionRepresentation | FINITE_COMPARABLE_ENSEMBLE | `finite_comparable_ensemble` |
| ScoringDefinitionStatus | ACTIVE | `active` |
| ScoringDefinitionStatus | BLOCKED | `blocked` |
| ScoringValidationSeverity | PASSED | `passed` |
| ScoringValidationSeverity | BLOCKED | `blocked` |

## Definition fields

Freeze `@dataclass(frozen=True)` `ScoringDiagnosticDefinition` with exact ordered fields:

1. `scoring_definition_id: str`
2. `scoring_artifact: ScoringArtifact`
3. `definition_status: ScoringDefinitionStatus`
4. `definition_version: str`
5. `method_id: str`
6. `method_version: str`
7. `prediction_representation: ScoringPredictionRepresentation`
8. `aggregation_rule_id: str`
9. `weighting_rule_id: str`
10. `sample_support_policy_id: str`
11. `uncertainty_method_id: str`
12. `uncertainty_level_id: str`
13. `supported_stratification_axes: tuple[str, ...]`
14. `required_baseline_types: tuple[BaselineType, ...]`
15. `probability_boundary_policy_id: str | None`
16. `binning_policy_id: str | None`
17. `decomposition_policy_id: str | None`
18. `pit_treatment_policy_id: str | None`
19. `tie_treatment_policy_id: str | None`
20. `threshold_weight_policy_id: str | None`
21. `claim_justification_id: str | None`
22. `scoring_target_posture: str`
23. `proper_score_direction_posture: str`
24. `paired_comparison_posture: str`
25. `applicability_posture: str`
26. `availability_posture: str`
27. `predeclaration_posture: str`
28. `tuning_posture: str`
29. `sparse_bucket_posture: str`
30. `interpretation_posture: str`
31. `market_price_posture: str`
32. `scoring_execution_posture: str`
33. `diagnostic_execution_posture: str`
34. `storage_persistence_posture: str`
35. `provenance_refs: tuple[str, ...]`
36. `exclusion_reason: str | None`
37. `supersedes_scoring_definition_id: str | None = None`

No value may be generated and no validation occurs in `__post_init__`.

## Result fields

Freeze `@dataclass(frozen=True)` `ScoringDiagnosticValidationResult`:

1. `severity: ScoringValidationSeverity`
2. `passed: bool`
3. `codes: tuple[ScoringValidationCode, ...] = ()`

Passed means `PASSED`, true, and empty codes; blocked means `BLOCKED`, false, and nonempty codes.

## Mapping input

Future exact signature:

```python
def scoring_diagnostic_definition_from_mapping(
    mapping: object,
) -> tuple[
    ScoringDiagnosticDefinition | None,
    ScoringDiagnosticValidationResult,
]:
```

The function occupies public source position eight, before the direct validator. It accepts only a `Mapping`. Non-Mapping roots and every ordinary exception during `items()` access, iteration, malformed or non-iterable item handling, item unpacking, key hashing, value snapshotting, or materialization return no definition and a blocked result containing exactly 36 ordered `MISSING_REQUIRED_FIELD` codes. Do not catch `BaseException`.

Mapping enum fields `scoring_artifact`, `prediction_representation`, and `definition_status` accept only an exact enum member or an exact built-in string equal to a member value. Accepted strings adapt to exact members. String subclasses, unrelated enums, enum subclasses, invalid strings, and all other values are rejected. Direct validation accepts exact enum members only.

Mapping tuple fields accept containers only as specified by their dedicated sections. Shape errors never cause an early return: aggregate every diagnosable present-value failure, suppress only dependent checks with missing or unusable prerequisites, and never construct or return a partial definition.

## Keys

Exact required mapping keys, in order:

1. `scoring_definition_id`
2. `scoring_artifact`
3. `definition_status`
4. `definition_version`
5. `method_id`
6. `method_version`
7. `prediction_representation`
8. `aggregation_rule_id`
9. `weighting_rule_id`
10. `sample_support_policy_id`
11. `uncertainty_method_id`
12. `uncertainty_level_id`
13. `supported_stratification_axes`
14. `required_baseline_types`
15. `probability_boundary_policy_id`
16. `binning_policy_id`
17. `decomposition_policy_id`
18. `pit_treatment_policy_id`
19. `tie_treatment_policy_id`
20. `threshold_weight_policy_id`
21. `claim_justification_id`
22. `scoring_target_posture`
23. `proper_score_direction_posture`
24. `paired_comparison_posture`
25. `applicability_posture`
26. `availability_posture`
27. `predeclaration_posture`
28. `tuning_posture`
29. `sparse_bucket_posture`
30. `interpretation_posture`
31. `market_price_posture`
32. `scoring_execution_posture`
33. `diagnostic_execution_posture`
34. `storage_persistence_posture`
35. `provenance_refs`
36. `exclusion_reason`

The only optional key is:

1. `supersedes_scoring_definition_id`

Fields 1 through 36 are required, and all seven policy IDs and `exclusion_reason` remain required even when their value is `None`; absence differs from explicit `None`.

Readable mappings recognize required and optional keys only when `type(key) is str`. A string-subclass key does not satisfy an exact required key and is also unexpected. Exact shape order is: missing required keys in the 36-key order; unexpected exact built-in string keys in lexical order; then every remaining non-exact-string key in original Mapping iteration order. Shape errors do not cause an early return. Aggregate every diagnosable present-value failure and construct no partial definition.

## Text fields

Required exact built-in nonblank string fields, in exact validation order:

1. `scoring_definition_id`
2. `definition_version`
3. `method_id`
4. `method_version`
5. `aggregation_rule_id`
6. `weighting_rule_id`
7. `sample_support_policy_id`
8. `uncertainty_method_id`
9. `uncertainty_level_id`
10. `scoring_target_posture`
11. `proper_score_direction_posture`
12. `paired_comparison_posture`
13. `applicability_posture`
14. `availability_posture`
15. `predeclaration_posture`
16. `tuning_posture`
17. `sparse_bucket_posture`
18. `interpretation_posture`
19. `market_price_posture`
20. `scoring_execution_posture`
21. `diagnostic_execution_posture`
22. `storage_persistence_posture`

A valid value requires `type(value) is str` and `value.strip()` to be nonempty. Do not strip, normalize, rewrite, or generate stored values. Each invalid present field appends one `BLANK_REQUIRED_TEXT` in the listed order.

Nullable text fields, in exact validation order after all required-text codes:

1. `probability_boundary_policy_id`
2. `binning_policy_id`
3. `decomposition_policy_id`
4. `pit_treatment_policy_id`
5. `tie_treatment_policy_id`
6. `threshold_weight_policy_id`
7. `claim_justification_id`
8. `exclusion_reason`
9. `supersedes_scoring_definition_id`

Generic nullable-text validation permits `None`. Every present non-`None` value must be an exact built-in nonblank string; each invalid non-`None` value appends one `BLANK_REQUIRED_TEXT`. `provenance_refs` entries are excluded from the generic text matrix and are validated only in the provenance group.

## Fixed postures

| Field | Exact value |
| --- | --- |
| scoring_target_posture | `venue_defined_settlement_outcome` |
| paired_comparison_posture | `same_split_fold_cutoff_eligible_records_labels_metric_aggregation_weighting_and_stratum_required` |
| applicability_posture | `representation_gated` |
| availability_posture | `point_in_time_required` |
| predeclaration_posture | `before_test_inspection_required` |
| tuning_posture | `train_or_calibration_only` |
| sparse_bucket_posture | `blocked_or_insufficient_not_silently_pooled` |
| interpretation_posture | `no_economic_edge_or_executability_inference` |
| market_price_posture | `not_approved_as_baseline_or_truth` |
| scoring_execution_posture | `not_approved` |
| diagnostic_execution_posture | `not_approved` |
| storage_persistence_posture | `not_approved` |

Each fixed posture requires `type(value) is str` and exact equality with its frozen value. A blank, non-string, or same-valued string-subclass posture receives its earlier `BLANK_REQUIRED_TEXT` and also `INVALID_FIXED_POSTURE`. Preserve fixed-posture field order.

## Representation matrix

| Artifact | Representation | Direction |
| --- | --- | --- |
| brier_score | binary_outcome_probability | lower_is_better |
| log_score | binary_outcome_probability | lower_is_better |
| reliability_diagram | binary_outcome_probability | diagnostic_only_not_scalar_ranking |
| brier_decomposition | binary_outcome_probability | diagnostic_only_not_scalar_ranking |
| crps | full_predictive_distribution | lower_is_better |
| pit_histogram | full_predictive_distribution | diagnostic_only_not_scalar_ranking |
| rank_histogram | finite_comparable_ensemble | diagnostic_only_not_scalar_ranking |
| threshold_weighted_crps | full_predictive_distribution | lower_is_better |

No representation is inferred or repaired. Representation mismatch is evaluated only when both scoring artifact and prediction representation are valid. Direction mismatch is evaluated only when scoring artifact is valid and `proper_score_direction_posture` is an exact built-in nonblank string. Missing or invalid prerequisites suppress the dependent mismatch code while generic text and enum codes remain. Otherwise mismatch emits `REPRESENTATION_MISMATCH` or `DIRECTION_MISMATCH` and fails closed.

## Artifact-policy matrix

| Artifact | Required non-null policies | All other policy fields |
| --- | --- | --- |
| brier_score | none | `None` |
| log_score | probability_boundary_policy_id | `None` |
| reliability_diagram | binning_policy_id | `None` |
| brier_decomposition | decomposition_policy_id | `None` |
| crps | none | `None` |
| pit_histogram | pit_treatment_policy_id | `None` |
| rank_histogram | tie_treatment_policy_id | `None` |
| threshold_weighted_crps | threshold_weight_policy_id, claim_justification_id | `None` |

Missing required policies emit their artifact-specific code. Any inapplicable supplied policy emits `INAPPLICABLE_POLICY_FIELDS_PRESENT` exactly once. No policy is selected, interpreted, or executed.All seven policy keys remain required even when `None`. For a required policy: an absent key produces only `MISSING_REQUIRED_FIELD`; present `None` produces its artifact-specific missing-policy code; and present blank, non-string, or string-subclass values produce the earlier `BLANK_REQUIRED_TEXT` followed by the missing-policy code.

For policies inapplicable to a valid artifact, every field must be `None`; any one or more present non-`None` values append exactly one `INAPPLICABLE_POLICY_FIELDS_PRESENT`, retaining any earlier text code. Artifact-policy checks run only for a valid artifact. Artifact-specific codes retain validation-code order. No policy value, formula, threshold, clipping rule, bin count, tie constant, or numeric method is invented.

## Stratification

Allowed axes are exactly `market_family`, `threshold_distance`, `forecast_horizon`, `station_source_compatibility`, `trap_category`, `season_or_regime_when_supported`, and `archive_layer`.

Mapping input accepts only an actual tuple or list and adapts a valid list to a tuple. Direct validation requires an actual tuple. Every entry must be an exact built-in nonblank string and an approved axis. Preserve caller order; reject duplicates. Any container, entry, unsupported-axis, or duplication defect appends exactly one `INVALID_STRATIFICATION_AXES`. Do not sort, normalize, infer, generate, or deduplicate. An empty tuple is valid.

## Baseline comparison

Mapping input accepts only an actual tuple or list. Each element may be an exact `BaselineType` member or an exact built-in string matching that member. After adaptation the value must equal exactly:

```python
(
    BaselineType.CLIMATOLOGY,
    BaselineType.PERSISTENCE,
)
```

Direct validation requires that exact tuple of exact enum members. Reordered, missing, duplicate, additional, string-subclass, unrelated-enum, invalid-string, or invalid-container values append exactly one `INVALID_REQUIRED_BASELINE_TYPES`. Neither baseline substitutes for the other. Market price is not a baseline.

## Provenance

Mapping input accepts only an actual tuple or list and adapts a valid list to a tuple. Direct validation requires an actual tuple. A wrong container appends exactly one `INVALID_PROVENANCE_REF` and prevents entry iteration. An empty accepted container appends exactly one `EMPTY_PROVENANCE_REFS`. Each non-exact-string or blank entry appends one `INVALID_PROVENANCE_REF` in caller order. Empty and invalid-entry codes are mutually exclusive.

Valid duplicates and caller order are preserved. Malformed entries do not receive `BLANK_REQUIRED_TEXT`. No reference is generated, resolved, sorted, deduplicated, looked up, or dereferenced.

## Status and supersession

Status checks run only when `definition_status` is valid. For active definitions, explicit `None` exclusion passes; any explicit non-`None` value appends `ACTIVE_WITH_EXCLUSION_REASON`, retaining an earlier text code when invalid. For blocked definitions, an exact built-in nonblank string passes; explicit `None`, blank, non-string, or string-subclass values append `BLOCKED_WITHOUT_EXCLUSION_REASON`, retaining an earlier text code for invalid non-`None` values. In either status, a missing mapping exclusion key produces only `MISSING_REQUIRED_FIELD`.

Append `SELF_SUPERSESSION` exactly once only when both identities are valid exact built-in nonblank strings and equal. No identity is generated or rewritten.

## Validation codes

Freeze this ordered `StrEnum` with snake-case values:

1. `MISSING_REQUIRED_FIELD = "missing_required_field"`
2. `UNEXPECTED_FIELD = "unexpected_field"`
3. `BLANK_REQUIRED_TEXT = "blank_required_text"`
4. `INVALID_SCORING_ARTIFACT = "invalid_scoring_artifact"`
5. `INVALID_PREDICTION_REPRESENTATION = "invalid_prediction_representation"`
6. `INVALID_DEFINITION_STATUS = "invalid_definition_status"`
7. `INVALID_FIXED_POSTURE = "invalid_fixed_posture"`
8. `INVALID_STRATIFICATION_AXES = "invalid_stratification_axes"`
9. `INVALID_REQUIRED_BASELINE_TYPES = "invalid_required_baseline_types"`
10. `EMPTY_PROVENANCE_REFS = "empty_provenance_refs"`
11. `INVALID_PROVENANCE_REF = "invalid_provenance_ref"`
12. `REPRESENTATION_MISMATCH = "representation_mismatch"`
13. `DIRECTION_MISMATCH = "direction_mismatch"`
14. `LOG_SCORE_MISSING_BOUNDARY_POLICY = "log_score_missing_boundary_policy"`
15. `RELIABILITY_MISSING_BINNING_POLICY = "reliability_missing_binning_policy"`
16. `BRIER_DECOMPOSITION_MISSING_POLICY = "brier_decomposition_missing_policy"`
17. `PIT_MISSING_TREATMENT_POLICY = "pit_missing_treatment_policy"`
18. `RANK_MISSING_TIE_POLICY = "rank_missing_tie_policy"`
19. `THRESHOLD_WEIGHTED_CRPS_MISSING_WEIGHT_POLICY = "threshold_weighted_crps_missing_weight_policy"`
20. `THRESHOLD_WEIGHTED_CRPS_MISSING_CLAIM_JUSTIFICATION = "threshold_weighted_crps_missing_claim_justification"`
21. `INAPPLICABLE_POLICY_FIELDS_PRESENT = "inapplicable_policy_fields_present"`
22. `ACTIVE_WITH_EXCLUSION_REASON = "active_with_exclusion_reason"`
23. `BLOCKED_WITHOUT_EXCLUSION_REASON = "blocked_without_exclusion_reason"`
24. `SELF_SUPERSESSION = "self_supersession"`

No other or dynamically generated code is permitted.

## Validation order

Future exact signature:

```python
def validate_scoring_diagnostic_definition(
    definition: ScoringDiagnosticDefinition,
) -> ScoringDiagnosticValidationResult:
```

The function occupies public source position nine. Readable mappings emit in exact groups: (1) missing keys; (2) unexpected exact-string keys; (3) unexpected non-string keys; (4) required and supplied-nullable text; (5) artifact; (6) representation; (7) status; (8) fixed postures; (9) stratification axes; (10) required baseline types; (11) provenance; (12) representation mismatch; (13) direction mismatch; (14) artifact-specific policy codes; (15) status consistency; (16) self-supersession. Aggregate every diagnosable present-value failure, suppress only checks with absent or unusable prerequisites, preserve repetitions, and never finally sort or deduplicate.

## Future tests

The later focused test must independently freeze all public symbols, enum values, dataclass fields, signatures, required keys, text rules, matrices, codes, ordering, mapping snapshot failures, direct/mapping distinctions, mutation cases for every artifact and boundary, frozen results, determinism, and absence of calculation or I/O. Complete tuple equality is required for combined failures.

## Dependencies

Only standard-library pure-validation dependencies and the merged `BaselineType` import are permitted. No dependency, workflow, configuration, schema, migration, fixture, data, service, network, subprocess, environment, dynamic execution, database, or persistence change is approved.

## Canonical routing

Canonical routing remains exactly `condition_id`, `token_id`, and `outcome`. `market_id` remains non-routing only and the token/outcome pair remains derived only. Neither is added to this definition.

## Non-goals

Explicitly denied: score calculation; diagnostic calculation; probability generation; label joining; split execution; baseline execution; evaluation-result creation; claim creation or evaluation; evidence-gate evaluation; data or corpus creation; dataset creation; source fetching; persistence; reporting; simulation; market comparison execution; paper trading; trading; order placement; runtime orchestration; autonomy; production behavior.

## Decision options and current status

Exact options, in order:

1. `approve_later_scoring_and_diagnostics_implementation_ticket`
2. `request_approval_request_revision`
3. `hold`
4. `block`

Current status: `request_prepared_implementation_not_approved`.

## Machine assignments

ticket_id: `WEATHER-BOT-STAGE3-SCORING-AND-DIAGNOSTICS-IMPLEMENTATION-APPROVAL-REQUEST-01`
canonical_id: `WEATHER-BOT-STAGE3-SCORING-AND-DIAGNOSTICS-IMPLEMENTATION-APPROVAL-REQUEST-01`
actual_pr_372_merge_sha: `be07b2b48b5243d7f4f69c61a9999a78983772de`
base_sha: `be07b2b48b5243d7f4f69c61a9999a78983772de`
current_request_status: `request_prepared_implementation_not_approved`
future_ticket: `WEATHER-BOT-STAGE3-SCORING-AND-DIAGNOSTICS-IMPLEMENTATION-01`
future_file_count: `2`
public_symbol_count: `9`
definition_field_count: `37`
required_mapping_key_count: `36`
optional_mapping_key_count: `1`
validation_code_count: `24`
decision_options: `approve_later_scoring_and_diagnostics_implementation_ticket`, `request_approval_request_revision`, `hold`, `block`

## Acceptance criteria

Acceptance requires exactly this document, its deterministic standard-library-only static test, and direct per-path canonical allowlist registration. The request must freeze every stated literal and matrix, remain non-implementing and non-approving, and preserve the two-file boundary for a later separately approved ticket.
