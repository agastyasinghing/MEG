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

`scoring_diagnostic_definition_from_mapping` accepts a `Mapping`. Non-Mapping roots or ordinary snapshot exceptions return no definition and a blocked result with exactly 36 ordered `MISSING_REQUIRED_FIELD` codes. Do not catch `BaseException`. Enum strings adapt only from exact built-in strings. Tuple fields accept an actual tuple or list; lists adapt to tuples. Direct validation accepts actual tuples and exact enum members only. No partial definition is returned.

## Keys

Fields 1 through 36 are required keys in definition-field order. Only `supersedes_scoring_definition_id` is optional. The seven policy IDs and `exclusion_reason` are nullable but required and must be explicitly present; absence differs from `None`. Unexpected exact-string keys precede unexpected non-string keys as specified by validation order.

## Text fields

All textual identities, versions, rules, policies when supplied, postures, provenance entries, exclusion reason when required, and supersession identity when supplied require exact built-in nonblank strings. Values are neither stripped nor generated. Invalid required or supplied-nullable text emits `BLANK_REQUIRED_TEXT` in field order.

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

Mismatch emits `REPRESENTATION_MISMATCH` or `DIRECTION_MISMATCH` and fails closed.

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

Missing required policies emit their artifact-specific code. Any inapplicable supplied policy emits `INAPPLICABLE_POLICY_FIELDS_PRESENT` exactly once. No policy is selected, interpreted, or executed.

## Stratification

Allowed axes are exactly `market_family`, `threshold_distance`, `forecast_horizon`, `station_source_compatibility`, `trap_category`, `season_or_regime_when_supported`, and `archive_layer`. Caller order is preserved. Empty is permitted. Duplicates or invalid entries emit `INVALID_STRATIFICATION_AXES` exactly once.

## Baseline comparison

`required_baseline_types` must be exactly `(BaselineType.CLIMATOLOGY, BaselineType.PERSISTENCE)`. Mapping may adapt those exact strings; direct validation requires that exact enum tuple. Neither baseline substitutes for the other; defects emit `INVALID_REQUIRED_BASELINE_TYPES` once.

## Provenance

`provenance_refs` is an actual tuple for direct validation, nonempty, and contains exact built-in nonblank strings. Empty emits `EMPTY_PROVENANCE_REFS`; each invalid occurrence emits `INVALID_PROVENANCE_REF`, preserving repetitions.

## Status and supersession

Active requires `exclusion_reason is None`; otherwise emit `ACTIVE_WITH_EXCLUSION_REASON`. Blocked requires an explicitly present exact built-in nonblank exclusion reason; otherwise emit `BLOCKED_WITHOUT_EXCLUSION_REASON`, except a missing mapping key produces only its missing-field code. Emit `SELF_SUPERSESSION` only when both valid exact string identities are equal.

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

Readable mappings emit in exact groups: (1) missing keys; (2) unexpected exact-string keys; (3) unexpected non-string keys; (4) required and supplied-nullable text; (5) artifact; (6) representation; (7) status; (8) fixed postures; (9) stratification axes; (10) required baseline types; (11) provenance; (12) representation mismatch; (13) direction mismatch; (14) artifact-specific policy codes; (15) status consistency; (16) self-supersession. Aggregate every diagnosable present-value failure, suppress only checks with absent or unusable prerequisites, preserve repetitions, and never finally sort or deduplicate.

## Future tests

The later focused test must independently freeze all public symbols, enum values, dataclass fields, signatures, required keys, text rules, matrices, codes, ordering, mapping snapshot failures, direct/mapping distinctions, mutation cases for every artifact and boundary, frozen results, determinism, and absence of calculation or I/O. Complete tuple equality is required for combined failures.

## Dependencies

Only standard-library pure-validation dependencies and the merged `BaselineType` import are permitted. No dependency, workflow, configuration, schema, migration, fixture, data, service, network, subprocess, environment, dynamic execution, database, or persistence change is approved.

## Canonical routing

Canonical routing remains exactly `condition_id`, `token_id`, and `outcome`. `market_id` remains non-routing only and the token/outcome pair remains derived only. Neither is added to this definition.

## Non-goals

Explicitly denied: score calculation; diagnostic calculation; probability generation; label joining; split execution; baseline execution; evaluation-result creation; claim creation or evaluation; evidence-gate evaluation; data or corpus creation; source fetching; persistence; reporting; simulation; market comparison execution; trading; runtime orchestration; autonomy.

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
