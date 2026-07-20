# WEATHER-BOT-STAGE3-STRICT-OOS-SPLIT-IMPLEMENTATION-APPROVAL-REQUEST-01

Canonical ID: WEATHER-BOT-STAGE3-STRICT-OOS-SPLIT-IMPLEMENTATION-APPROVAL-REQUEST-01

## Status and request scope
This artifact is documentation/static-test-only. It asks a human whether a later implementation ticket may create a narrow immutable, caller-supplied strict-OOS split-assignment boundary. It does not approve implementation; it does not execute splits; it does not create split files; it does not partition datasets; it does not approve scoring; a separate human decision is required.

## Actual PR #368 merge predecessor
Immediate predecessor: PR #368 actual merge commit `1676199c89f2d5d472ea14c66ae841c1878c6018`. The implementation head commit `a5d28d50e82c7d0b101036c89d7f61c6fec564af` is recorded as an ancestor of this actual merge commit. This request uses the actual merge commit, not a preview merge SHA.

## Controlling strict-OOS planning contract
Controlling strict-OOS planning contract: `docs/prd/WEATHER-BOT-STAGE3-STRICT-OOS-SPLIT-CONTRACT-PLANNING-01.md`. Implemented upstream immutable probability-record boundary: `meg/weather/stage3/binary_probability_record.py`. PR #360 planning contract is requirements only, not implementation approval.

## Requested future implementation slice identity
Future implementation ticket identity: narrow immutable, caller-supplied strict-OOS split-assignment boundary only. No split generator, fold builder, dataset partitioner, scorer, serializer, repository, service, or execution function is requested.

## Exact future changed-file matrix
| Future file | Action | Boundary |
| --- | --- | --- |
| `meg/weather/stage3/strict_oos_split.py` | create | define only the strict-OOS split assignment dataclasses, closed enums, mapping adapter, and validators |
| `tests/core/test_weather_bot_stage3_strict_oos_split.py` | create | static/unit tests for that narrow boundary only |
Later ticket must not modify `meg/weather/stage3/__init__.py`, `meg/weather/stage3/binary_probability_record.py`, Stage 2 files, existing tests, allowlists, fixtures, datasets, dependencies, workflows, schemas, migrations, reports, or exports.

## Exact future public-symbol matrix
| Order | Public symbol |
| --- | --- |
| 1 | `SplitRole` |
| 2 | `SplitApplicabilityMode` |
| 3 | `SplitAssignmentStatus` |
| 4 | `OverlapControlPosture` |
| 5 | `SplitValidationSeverity` |
| 6 | `SplitValidationCode` |
| 7 | `StrictOOSSplitAssignment` |
| 8 | `StrictOOSSplitValidationResult` |
| 9 | `strict_oos_split_assignment_from_mapping` |
| 10 | `validate_strict_oos_split_assignment` |
| 11 | `validate_strict_oos_split_assignments` |

## Exact future enum matrices
### SplitRole
| Member | Value |
| --- | --- |
| `TRAIN` | `train` |
| `CALIBRATION` | `calibration` |
| `TEST` | `test` |
### SplitApplicabilityMode
| Member | Value |
| --- | --- |
| `PRIMARY_TEMPORAL` | `primary_temporal` |
| `LEAVE_STATION_OUT` | `leave_station_out` |
| `LEAVE_YEAR_OUT` | `leave_year_out` |
| `FAMILY_STRATIFIED` | `family_stratified` |
| `SEASON_OR_REGIME_STRATIFIED` | `season_or_regime_stratified` |
### SplitAssignmentStatus
| Member | Value |
| --- | --- |
| `ASSIGNED` | `assigned` |
| `BLOCKED` | `blocked` |
### OverlapControlPosture
| Member | Value |
| --- | --- |
| `NOT_REQUIRED` | `not_required` |
| `SATISFIED` | `satisfied` |
| `UNSATISFIED` | `unsatisfied` |
### SplitValidationSeverity
| Member | Value |
| --- | --- |
| `PASSED` | `passed` |
| `BLOCKED` | `blocked` |

## Exact future record-field matrix
Request one frozen dataclass: `StrictOOSSplitAssignment`.
| Order | Field | Type |
| --- | --- | --- |
| 1 | `split_assignment_id` | `str` |
| 2 | `split_id` | `str` |
| 3 | `split_version` | `str` |
| 4 | `fold_id` | `str` |
| 5 | `fold_index` | `int` |
| 6 | `prediction_record_id` | `str` |
| 7 | `condition_id` | `str` |
| 8 | `token_id` | `str` |
| 9 | `outcome` | `str` |
| 10 | `settlement_rule_id` | `str` |
| 11 | `settlement_rule_version` | `str` |
| 12 | `split_role` | `SplitRole` |
| 13 | `applicability_modes` | `tuple[SplitApplicabilityMode, ...]` |
| 14 | `assignment_status` | `SplitAssignmentStatus` |
| 15 | `fold_cutoff` | `str` |
| 16 | `prediction_as_of` | `str` |
| 17 | `input_publication_available_at` | `str` |
| 18 | `target_start_at` | `str` |
| 19 | `target_end_at` | `str` |
| 20 | `label_available_at` | `str | None` |
| 21 | `leakage_group_id` | `str` |
| 22 | `overlap_control_posture` | `OverlapControlPosture` |
| 23 | `primary_split_posture` | `str` |
| 24 | `tuning_posture` | `str` |
| 25 | `calibration_posture` | `str` |
| 26 | `baseline_parity_posture` | `str` |
| 27 | `exclusion_reason` | `str | None` |
| 28 | `provenance_refs` | `tuple[str, ...]` |
| 29 | `created_at` | `str` |
| 30 | `supersedes_split_assignment_id` | `str | None = None` |
No identity, timestamp, fold, probability record, cutoff, role, leakage group, provenance, or version may be generated.

## Exact fixed-posture matrix
| Field | Exact value |
| --- | --- |
| `primary_split_posture` | `rolling_origin_or_walk_forward_required` |
| `tuning_posture` | `train_or_calibration_only` |
| `calibration_posture` | `separate_when_required` |
| `baseline_parity_posture` | `same_folds_and_eligibility_required` |
No alternate, hybrid, custom, or dynamically generated posture is requested.

## Exact mapping-input matrix
Future signature: `strict_oos_split_assignment_from_mapping(mapping: object) -> tuple[StrictOOSSplitAssignment | None, StrictOOSSplitValidationResult]`. Mapping adaptation may accept exact enum members, exact enum value strings, exact built-in `int` for `fold_index` with bool rejected, tuple or list for `applicability_modes`, tuple or list for `provenance_refs`, and timezone-aware ISO timestamp strings. It must inspect the complete key set, aggregate all diagnosable failures in deterministic order, reject every unexpected key, supply no required-field default, construct no partial record, return `(None, blocked_result)` for invalid input, and construct a record only after all mapping checks pass.

## Exact single-record validation matrix
Future signature: `validate_strict_oos_split_assignment(record: StrictOOSSplitAssignment) -> StrictOOSSplitValidationResult`. The direct validator must perform no mapping adaptation. General requirements: exact nonblank strings, nonnegative exact int fold index with bool rejected, nonempty tuple applicability modes with `PRIMARY_TEMPORAL` first and no duplicate, exact fixed postures, timezone-aware parseable timestamps, input available no later than prediction, prediction no later than fold cutoff, ordered target window, nonempty provenance tuple of nonblank strings, and no self-supersession. Assigned records require no exclusion reason and no unsatisfied overlap control. Train/calibration require target end and label available by cutoff. Test requires target start strictly after cutoff and any label strictly later than cutoff. Blocked records require nonblank exclusion reason, remain syntactically valid and auditable, are excluded from collection role/leakage calculations, and do not approve pooling, reassignment, or boundary changes.

## Exact collection-validation matrix
Future signature: `validate_strict_oos_split_assignments(assignments: tuple[StrictOOSSplitAssignment, ...]) -> StrictOOSSplitValidationResult`. It must require an actual tuple, reject empty tuple, validate every record, preserve deterministic duplicate code occurrences, require one split identity and version, require unique assignment ids, reject duplicate `(fold_id, prediction_record_id)`, reject same assigned test prediction record in more than one fold, require each fold_id to map to one fold_index and one fold_cutoff, require later fold indices to have strictly later cutoffs, reject assigned leakage group appearing in multiple roles within a fold, ignore blocked records for role-conflict and duplicate-test calculations, generate no folds, modify no assignment, and return no partitioned dataset. Do not request shuffled-random splitting. Do not request numeric fold widths, gap durations, embargo durations, sample minimums, or sufficiency thresholds.

## Exact validation-code matrix
Define closed enum `SplitValidationCode` in this exact order:
1. `MISSING_REQUIRED_FIELD = "missing_required_field"`
2. `UNEXPECTED_FIELD = "unexpected_field"`
3. `BLANK_REQUIRED_TEXT = "blank_required_text"`
4. `INVALID_SPLIT_ROLE = "invalid_split_role"`
5. `INVALID_APPLICABILITY_MODES = "invalid_applicability_modes"`
6. `INVALID_ASSIGNMENT_STATUS = "invalid_assignment_status"`
7. `INVALID_OVERLAP_CONTROL_POSTURE = "invalid_overlap_control_posture"`
8. `INVALID_INTEGER_FIELD = "invalid_integer_field"`
9. `INVALID_FIXED_POSTURE = "invalid_fixed_posture"`
10. `INVALID_TIMESTAMP = "invalid_timestamp"`
11. `INPUT_AVAILABLE_AFTER_PREDICTION = "input_available_after_prediction"`
12. `PREDICTION_AFTER_FOLD_CUTOFF = "prediction_after_fold_cutoff"`
13. `INVALID_TARGET_WINDOW = "invalid_target_window"`
14. `TRAIN_OR_CALIBRATION_AFTER_CUTOFF = "train_or_calibration_after_cutoff"`
15. `TRAIN_OR_CALIBRATION_LABEL_UNAVAILABLE_BY_CUTOFF = "train_or_calibration_label_unavailable_by_cutoff"`
16. `TEST_NOT_STRICTLY_AFTER_CUTOFF = "test_not_strictly_after_cutoff"`
17. `TEST_LABEL_AVAILABLE_BY_CUTOFF = "test_label_available_by_cutoff"`
18. `ASSIGNED_WITH_EXCLUSION_REASON = "assigned_with_exclusion_reason"`
19. `BLOCKED_WITHOUT_EXCLUSION_REASON = "blocked_without_exclusion_reason"`
20. `UNSATISFIED_OVERLAP_CONTROL_ASSIGNED = "unsatisfied_overlap_control_assigned"`
21. `EMPTY_PROVENANCE_REFS = "empty_provenance_refs"`
22. `INVALID_PROVENANCE_REF = "invalid_provenance_ref"`
23. `SELF_SUPERSESSION = "self_supersession"`
24. `INVALID_ASSIGNMENT_COLLECTION_TYPE = "invalid_assignment_collection_type"`
25. `EMPTY_ASSIGNMENT_COLLECTION = "empty_assignment_collection"`
26. `DUPLICATE_ASSIGNMENT_ID = "duplicate_assignment_id"`
27. `DUPLICATE_FOLD_RECORD_ASSIGNMENT = "duplicate_fold_record_assignment"`
28. `DUPLICATE_TEST_RECORD = "duplicate_test_record"`
29. `INCONSISTENT_SPLIT_ID = "inconsistent_split_id"`
30. `INCONSISTENT_SPLIT_VERSION = "inconsistent_split_version"`
31. `INCONSISTENT_FOLD_DEFINITION = "inconsistent_fold_definition"`
32. `NON_MONOTONIC_FOLD_CUTOFF = "non_monotonic_fold_cutoff"`
33. `LEAKAGE_GROUP_ROLE_CONFLICT = "leakage_group_role_conflict"`
No custom validation codes.

## Exact validation-order contract
Validation ordering is exactly: mapping-shape codes; single-record field/type/enum codes; fixed-posture codes; timestamp and temporal codes; assignment-status consistency codes; provenance and supersession codes; collection-shape codes; collection identity and duplicate codes; fold-definition and monotonicity codes; leakage-group role-conflict codes. Repeated codes must remain repeated. No set, sorting, or deduplication may replace ordered results.

## Exact future test matrix
Future tests must cover exact public API; exact enum names, values, and order; exact record/result fields, types, order, defaults, and frozen posture; exact function signatures; mapping-shape aggregation; every required text field; enum adaptation and rejection; exact `fold_index`; timestamp parsing; no-lookahead; fold cutoff eligibility; target-window ordering; train/calibration label isolation; strict test-after-cutoff; test-label no-lookahead; applicability ordering and uniqueness; fixed postures; assignment/exclusion consistency; overlap consistency; provenance; supersession; deterministic repeated-code ordering; collection type and emptiness; split/version consistency; duplicate assignment, fold-record, and test-record detection; fold-definition consistency; monotonically advancing cutoffs; within-fold leakage-group role isolation; blocked-record exclusion; canonical routing; no non-routing market key; no `token_outcome_pair`; and no I/O, providers, services, persistence, split generation, scoring, backtesting, simulation, or trading.

## Dependency and import boundary
The later implementation must remain standard-library-only unless a separate approval changes that boundary. No I/O, providers, services, persistence, schemas, migrations, workflows, dependency changes, dynamic imports, database access, subprocess, network access, shell execution, or Git execution are approved.

## Canonical routing boundary
Canonical routing remains exactly `condition_id`, `token_id`, and `outcome`. `market_id` remains non-routing only and must not become a routing key. `token_outcome_pair` must not be added as a public input or route.

## Temporal and no-lookahead boundary
Strict temporal posture requires timezone-aware timestamps, input availability no later than prediction, prediction no later than fold cutoff, train/calibration labels available by cutoff, and test targets strictly after cutoff without labels available by cutoff. This request does not approve implementation and does not execute splits.

## Leakage-group and fold boundary
Leakage group and fold identifiers must be caller-supplied, immutable, and auditable. The future validator may reject conflicts but must not generate folds, choose cutoffs, partition datasets, or alter assignments.

## Assignment and exclusion semantics
Assigned records are eligible only when exclusion reason is absent and overlap control is not unsatisfied. Blocked records require an exclusion reason and remain auditable but are ignored for collection leakage role conflict and duplicate-test calculations.

## Baseline parity boundary
Baseline parity posture must equal `same_folds_and_eligibility_required`. This preserves later baseline comparability requirements without approving baseline calculation, scoring, diagnostics, claims, or evidence-gate evaluation.

## Explicit future implementation non-goals
The future requested implementation must not:
- generate fold assignments;
- choose cutoffs;
- calculate gaps or embargoes;
- invent sample thresholds;
- load probability records from files;
- fetch data;
- expand the corpus;
- inspect settlement outcomes during split design;
- train models;
- calculate features;
- calculate baselines;
- score predictions;
- calculate diagnostics;
- join labels;
- create evaluation results or claims;
- evaluate an evidence gate;
- persist assignments;
- serialize files;
- create database objects;
- create reports or exports;
- schedule work;
- run background tasks;
- simulate;
- paper trade;
- trade;
- place orders;
- add runtime orchestration;
- grant autonomy;

## Approval decision options
Exact options:
- `approve_later_strict_oos_split_assignment_implementation_ticket`
- `request_approval_request_revision`
- `hold`
- `block`

## Current request status
`request_prepared_implementation_not_approved`

## Human decision and separate-approval boundary
A separate human decision is required before any implementation ticket may proceed. This document does not approve implementation, does not execute splits, does not create split files, does not partition datasets, and does not approve scoring.

## Fail-closed requirements
Invalid mapping input, invalid records, invalid collections, ambiguous values, unexpected keys, missing required fields, non-aware timestamps, temporal leakage risk, duplicate identity, fold inconsistency, and leakage-group role conflict must fail closed with ordered codes.

## Explicit non-approvals
This request does not approve implementation. It does not execute splits. It does not create split files. It does not partition datasets. It does not approve scoring. It does not approve I/O, providers, services, persistence, split generation, backtesting, simulation, paper trading, trading, order placement, runtime orchestration, production behavior, or autonomy. A separate human decision is required.

## Machine-checkable assignments
```yaml
ticket: WEATHER-BOT-STAGE3-STRICT-OOS-SPLIT-IMPLEMENTATION-APPROVAL-REQUEST-01
actual_pr_368_merge_sha: 1676199c89f2d5d472ea14c66ae841c1878c6018
request_status: request_prepared_implementation_not_approved
implementation_approved: false
executes_splits: false
creates_split_files: false
partitions_datasets: false
approves_scoring: false
separate_human_decision_required: true
future_files_exact:
  - meg/weather/stage3/strict_oos_split.py
  - tests/core/test_weather_bot_stage3_strict_oos_split.py
```

## Acceptance criteria
Acceptance requires exactly this document, its deterministic static test, and the canonical allowlist update; no `meg/` changes; actual PR #368 merge SHA recorded; future implementation limited to exactly two new files; exact eleven-symbol API, enums, fields, validation codes, and decision options frozen; explicit non-approval posture preserved; mandatory tests passing; and PR opened but not merged.
