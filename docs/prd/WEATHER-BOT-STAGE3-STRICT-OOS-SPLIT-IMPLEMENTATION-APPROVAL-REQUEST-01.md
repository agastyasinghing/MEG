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
Request one frozen dataclass: `@dataclass(frozen=True) class StrictOOSSplitAssignment`.
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

Request one frozen dataclass: `@dataclass(frozen=True) class StrictOOSSplitValidationResult`.
| Order | Field | Type |
| --- | --- | --- |
| 1 | `severity` | `SplitValidationSeverity` |
| 2 | `passed` | `bool` |
| 3 | `codes` | `tuple[SplitValidationCode, ...] = ()` |
Passed result invariants: severity is `PASSED`; passed is `True`; codes is empty.
Blocked result invariants: severity is `BLOCKED`; passed is `False`; codes is nonempty.
The result must contain no record payload, assignments, partitioned output, free-form message, field name, generated repair, score, claim, approval status, readiness status, or evidence-gate result.

## Exact fixed-posture matrix
| Field | Exact value |
| --- | --- |
| `primary_split_posture` | `rolling_origin_or_walk_forward_required` |
| `tuning_posture` | `train_or_calibration_only` |
| `calibration_posture` | `separate_when_required` |
| `baseline_parity_posture` | `same_folds_and_eligibility_required` |
No alternate, hybrid, custom, or dynamically generated posture is requested.

## Exact mapping-input matrix
Future signature: `strict_oos_split_assignment_from_mapping(mapping: object) -> tuple[StrictOOSSplitAssignment | None, StrictOOSSplitValidationResult]`.

Exact ordered required mapping keys:
1. `split_assignment_id`
2. `split_id`
3. `split_version`
4. `fold_id`
5. `fold_index`
6. `prediction_record_id`
7. `condition_id`
8. `token_id`
9. `outcome`
10. `settlement_rule_id`
11. `settlement_rule_version`
12. `split_role`
13. `applicability_modes`
14. `assignment_status`
15. `fold_cutoff`
16. `prediction_as_of`
17. `input_publication_available_at`
18. `target_start_at`
19. `target_end_at`
20. `label_available_at`
21. `leakage_group_id`
22. `overlap_control_posture`
23. `primary_split_posture`
24. `tuning_posture`
25. `calibration_posture`
26. `baseline_parity_posture`
27. `exclusion_reason`
28. `provenance_refs`
29. `created_at`

The only optional mapping key is:
- `supersedes_split_assignment_id`

`label_available_at` is a required key whose value may be `None`. `exclusion_reason` is a required key whose value may be `None`. Absence of either required nullable key produces `MISSING_REQUIRED_FIELD`. Explicit `None` is distinct from absence. No required key receives a default. No unexpected key is discarded. A mapping with shape errors still validates every diagnosable present value. An invalid mapping never returns a partial record. Unexpected-key ordering is exact built-in string keys in lexical order, then non-string keys afterward in original mapping iteration order. Do not sort arbitrary objects by `repr()`.

For `split_role`, `assignment_status`, and `overlap_control_posture`, mapping adaptation accepts only the exact enum member or the exact built-in string equal to an enum value. It rejects string subclasses, unrelated `StrEnum` members, custom enum members, and every other value. For `applicability_modes`, mapping adaptation accepts only an actual tuple or list. Each entry may be an exact `SplitApplicabilityMode` member or an exact built-in string equal to a member value. After adaptation, output is a tuple, the tuple is nonempty, `PRIMARY_TEMPORAL` is exactly first, no mode is duplicated, caller order is preserved, and any container, entry, ordering, emptiness, or duplicate failure produces exactly one `INVALID_APPLICABILITY_MODES`. For `fold_index`, require `type(value) is int`, reject bool and int subclasses, require value greater than or equal to zero, and any failure produces exactly one `INVALID_INTEGER_FIELD`. For `provenance_refs` mapping input, accept only an actual tuple or list, convert an accepted list to a tuple, preserve order and repeated references, make wrong container produce exactly one `INVALID_PROVENANCE_REF`, make empty tuple/list produce exactly one `EMPTY_PROVENANCE_REFS`, and make each blank, string-subclass, or non-string entry produce one `INVALID_PROVENANCE_REF` in entry order.

## Exact single-record validation matrix
Future signature: `validate_strict_oos_split_assignment(record: StrictOOSSplitAssignment) -> StrictOOSSplitValidationResult`. The direct validator performs no mapping adaptation, no tuple/list conversion, and no enum-string adaptation. Require exact enum members, not strings; `type(record.applicability_modes) is tuple`; `type(fold_index) is int`; `type(record.provenance_refs) is tuple`; and exact built-in strings for text and timestamps. Direct applicability modes must be a nonempty tuple, every entry must be an exact `SplitApplicabilityMode` member, enum subclasses, strings, unrelated enums, and all other entries are rejected, `SplitApplicabilityMode.PRIMARY_TEMPORAL` must be exactly first, no entry may occur more than once, caller order is preserved, any container, entry, emptiness, first-position, or duplication failure appends exactly one `INVALID_APPLICABILITY_MODES`, and later applicability checks do not append additional copies for the same record. Invalid `split_role` appends exactly one `INVALID_SPLIT_ROLE`; invalid `assignment_status` appends exactly one `INVALID_ASSIGNMENT_STATUS`; invalid `overlap_control_posture` appends exactly one `INVALID_OVERLAP_CONTROL_POSTURE`; invalid `fold_index` appends exactly one `INVALID_INTEGER_FIELD`; `type(fold_index) is int` and value must be nonnegative; bool and int subclasses are rejected. Mapping adaptation uses the same one-code-per-field behavior after attempted exact enum-value adaptation.

Required nonblank text fields in exact order:
1. `split_assignment_id`
2. `split_id`
3. `split_version`
4. `fold_id`
5. `prediction_record_id`
6. `condition_id`
7. `token_id`
8. `outcome`
9. `settlement_rule_id`
10. `settlement_rule_version`
11. `leakage_group_id`
12. `primary_split_posture`
13. `tuning_posture`
14. `calibration_posture`
15. `baseline_parity_posture`
Each invalid field produces one `BLANK_REQUIRED_TEXT`. If `exclusion_reason` is not `None`, it must be an exact nonblank built-in string. `supersedes_split_assignment_id is None` is accepted. If `supersedes_split_assignment_id` is not `None`, it must already be an exact nonblank built-in string. Each invalid supplied nullable text value produces one `BLANK_REQUIRED_TEXT` after required-text checks. Append `SELF_SUPERSESSION` exactly once when both identifiers are valid exact nonblank strings and `supersedes_split_assignment_id == split_assignment_id`. Do not append `SELF_SUPERSESSION` when either identifier is text-invalid. A distinct valid superseded identifier is accepted. No identifier is generated or rewritten.

Direct provenance requires `type(record.provenance_refs) is tuple`; a non-tuple container appends exactly one `INVALID_PROVENANCE_REF`; a valid tuple container that is empty appends exactly one `EMPTY_PROVENANCE_REFS`; every entry must be an exact built-in nonblank string; each invalid entry appends one `INVALID_PROVENANCE_REF` in tuple order; duplicate valid references are allowed; caller order and duplicate references are preserved; no sorting, deduplication, conversion, normalization, or generated provenance occurs; container failure prevents entry iteration; and emptiness and entry errors are mutually exclusive for one tuple.

Timestamp fields in exact parse order: `fold_cutoff`, `prediction_as_of`, `input_publication_available_at`, `target_start_at`, `target_end_at`, `label_available_at` only when not `None`, and `created_at`. A timestamp is valid only when the value is an exact built-in nonblank string, `datetime.fromisoformat` accepts it, `tzinfo` is not `None`, and `utcoffset()` is not `None`. Do not normalize or rewrite stored timestamp strings. Do not use current time. Produce one `INVALID_TIMESTAMP` for every invalid timestamp in that exact order. Only perform a comparison when all timestamps required by that comparison are valid. General temporal rules apply to assigned and blocked records in this code order: `INPUT_AVAILABLE_AFTER_PREDICTION` for `input_publication_available_at <= prediction_as_of`, `PREDICTION_AFTER_FOLD_CUTOFF` for `prediction_as_of <= fold_cutoff`, and `INVALID_TARGET_WINDOW` for `target_start_at <= target_end_at`.

Role-specific temporal and label rules apply only when `assignment_status is ASSIGNED`. For assigned `TRAIN` or `CALIBRATION`, require `target_end_at <= fold_cutoff`, require `label_available_at` not `None`, require the label timestamp to be valid, and require a valid label timestamp `<= fold_cutoff`; codes occur as `TRAIN_OR_CALIBRATION_AFTER_CUTOFF` then `TRAIN_OR_CALIBRATION_LABEL_UNAVAILABLE_BY_CUTOFF`. For assigned `TEST`, require `target_start_at > fold_cutoff`; `label_available_at` may be `None`; if a valid label timestamp is present, it must be strictly later than `fold_cutoff`; codes occur as `TEST_NOT_STRICTLY_AFTER_CUTOFF` then `TEST_LABEL_AVAILABLE_BY_CUTOFF`. Assignment-status consistency codes occur afterward as `ASSIGNED_WITH_EXCLUSION_REASON`, `BLOCKED_WITHOUT_EXCLUSION_REASON`, and `UNSATISFIED_OVERLAP_CONTROL_ASSIGNED`. Assigned record requires `exclusion_reason is None`; blocked record requires an exact nonblank exclusion reason; assigned record may not use `UNSATISFIED`; blocked record may use `UNSATISFIED`; blocked records skip assigned role-specific temporal and label checks; blocked records still receive general syntax, enum, fixed-posture, timestamp, general temporal, provenance, and supersession validation.

## Exact collection-validation matrix
Future signature: `validate_strict_oos_split_assignments(assignments: tuple[StrictOOSSplitAssignment, ...]) -> StrictOOSSplitValidationResult`. Root behavior: non-tuple root returns only `INVALID_ASSIGNMENT_COLLECTION_TYPE`; empty tuple returns only `EMPTY_ASSIGNMENT_COLLECTION`; a nonempty tuple validates each element in tuple order; an element that is not an actual `StrictOOSSplitAssignment` produces one `INVALID_ASSIGNMENT_COLLECTION_TYPE` in its tuple position and is skipped by later collection comparisons.

For a nonempty tuple, final result order is each element’s complete direct-record validation codes in tuple order, then `DUPLICATE_ASSIGNMENT_ID`, `DUPLICATE_FOLD_RECORD_ASSIGNMENT`, `DUPLICATE_TEST_RECORD`, `INCONSISTENT_SPLIT_ID`, `INCONSISTENT_SPLIT_VERSION`, `INCONSISTENT_FOLD_DEFINITION`, `NON_MONOTONIC_FOLD_CUTOFF`, and `LEAKAGE_GROUP_ROLE_CONFLICT`. Append one `DUPLICATE_ASSIGNMENT_ID` for each later valid record whose nonblank `split_assignment_id` was previously seen, using tuple order. Append one `DUPLICATE_FOLD_RECORD_ASSIGNMENT` for each later valid record whose valid `(fold_id, prediction_record_id)` pair was previously seen, including assigned and blocked records. Append one `DUPLICATE_TEST_RECORD` for each later assigned `TEST` record whose valid `prediction_record_id` previously appeared as an assigned `TEST` record in a different fold, ignoring blocked records. Use the first valid nonblank split identity as the baseline and append one `INCONSISTENT_SPLIT_ID` for each later valid record whose valid split ID differs. Use the first valid nonblank split version as the baseline and append one `INCONSISTENT_SPLIT_VERSION` for each later valid record whose valid split version differs. For valid records, each `fold_id` must map to exactly one `fold_index` and `fold_cutoff`, and each `fold_index` must map to exactly one `fold_id` and `fold_cutoff`; append one `INCONSISTENT_FOLD_DEFINITION` for each later record that conflicts with either previously established mapping. For monotonic fold cutoffs, use the first-seen consistent valid definition for each fold index, order unique definitions by numeric `fold_index`, and append one `NON_MONOTONIC_FOLD_CUTOFF` for each adjacent later index whose valid cutoff is less than or equal to the previous valid cutoff. Do not alter, generate, or infer a cutoff. For leakage-group role conflict, use assigned records only, key by `(fold_id, leakage_group_id)`, record the first valid role, append one `LEAKAGE_GROUP_ROLE_CONFLICT` for each later assigned record with the same key but a different role, and ignore blocked records. Do not generate folds, partitions, replacements, or corrected assignments.

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
Complete direct-record validation order: all `BLANK_REQUIRED_TEXT` occurrences; `INVALID_SPLIT_ROLE`; `INVALID_APPLICABILITY_MODES`; `INVALID_ASSIGNMENT_STATUS`; `INVALID_OVERLAP_CONTROL_POSTURE`; `INVALID_INTEGER_FIELD`; one `INVALID_FIXED_POSTURE` per invalid fixed field in primary split, tuning, calibration, baseline parity order; all `INVALID_TIMESTAMP` occurrences; general temporal codes; assigned role-specific temporal/label codes; assignment-status consistency codes; `EMPTY_PROVENANCE_REFS`; all `INVALID_PROVENANCE_REF` occurrences; `SELF_SUPERSESSION`. Complete mapping result order: accept exactly a `collections.abc.Mapping` root and reject strings, sequences, arbitrary objects, and objects that merely expose a `keys` attribute; if the root is not an accepted mapping object, return `(None, blocked_result)` without throwing a raw exception; append one `MISSING_REQUIRED_FIELD` for every absent required key in `EXPECTED_MAPPING_REQUIRED_KEYS` order; append one `UNEXPECTED_FIELD` for every unexpected key with exact built-in string keys in lexical order and non-string keys afterward in original mapping iteration order; append all diagnosable present-value validation codes using required and nullable text, role, applicability modes, assignment status, overlap posture, integer, fixed postures, timestamps, general temporal checks, assigned role-specific temporal checks, status consistency, provenance, and supersession order; skip only checks whose required input is absent or invalid; preserve every repeated code occurrence; perform no final sorting, filtering, insertion, set conversion, or deduplication; if any code exists, return `(None, blocked_result)`; construct `StrictOOSSplitAssignment` only when the complete code sequence is empty; and a successfully constructed record must satisfy direct validation and return the exact passed result. Collection validation order follows the collection-validation matrix. Repeated codes must remain repeated. No final sorting, set conversion, filtering, insertion, or deduplication is permitted.

## Exact future test matrix
Future tests must cover exact public API; exact enum names, values, and order; exact record/result fields, types, order, defaults, and frozen posture; exact function signatures; mapping-shape aggregation; every required text field; enum adaptation and rejection; exact `fold_index`; timestamp parsing; no-lookahead; fold cutoff eligibility; target-window ordering; train/calibration label isolation; strict test-after-cutoff; test-label no-lookahead; applicability ordering and uniqueness; fixed postures; assignment/exclusion consistency; overlap consistency; provenance; supersession; deterministic repeated-code ordering; collection type and emptiness; split/version consistency; duplicate assignment, fold-record, and test-record detection; fold-definition consistency; monotonically advancing cutoffs; within-fold leakage-group role isolation; blocked-record exclusion; canonical routing; no non-routing market key; no `token_outcome_pair`; and no I/O, providers, services, persistence, split generation, scoring, backtesting, simulation, or trading. Future mapping-order tests must require complete expected tuples for cases combining multiple missing required keys, multiple unexpected built-in string keys, multiple non-string unexpected keys, missing plus unexpected keys, missing plus malformed present text, unexpected plus invalid enums, malformed applicability modes plus invalid integer, timestamp and provenance failures, repeated identical validation codes, and shape and temporal failures together. These tests must require complete tuple equality, including duplicate occurrences and order.

## Dependency and import boundary
The later implementation must remain standard-library-only unless a separate approval changes that boundary. No I/O, providers, services, persistence, schemas, migrations, workflows, dependency changes, dynamic imports, database access, subprocess, network access, shell execution, or Git execution are approved.

## Canonical routing boundary
Canonical routing remains exactly `condition_id`, `token_id`, and `outcome`. `market_id` remains non-routing only and must not become a routing key. `token_outcome_pair` must not be added as a public input or route.

## Temporal and no-lookahead boundary
Strict temporal posture requires timezone-aware timestamps, input availability no later than prediction, prediction no later than fold cutoff, train/calibration labels available by cutoff, and test targets strictly after cutoff without labels available by cutoff. Rolling-origin or walk-forward primacy is preserved; shuffled-random primary splitting is not requested. This request does not approve implementation and does not execute splits.

## Leakage-group and fold boundary
Leakage group and fold identifiers must be caller-supplied, immutable, and auditable. Caller-supplied fold definitions and immutable cutoffs are required. The future validator may reject conflicts but must not generate folds, choose cutoffs, partition datasets, alter assignments, invent fold count, invent fold duration, invent sample minimums, or invent embargo duration.

## Assignment and exclusion semantics
Assigned records are eligible only when exclusion reason is absent and overlap control is not unsatisfied. Blocked records require an exclusion reason and remain syntactically valid and auditable, but are ignored for collection leakage role conflict and duplicate-test calculations. Blocked status does not approve pooling, reassignment, or boundary changes.

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
Invalid mapping input, invalid records, invalid collections, ambiguous values, unexpected keys, missing required fields, non-aware timestamps, temporal leakage risk, duplicate identity, fold inconsistency, and leakage-group role conflict must fail closed with ordered codes. Invalid input must not produce partial records, generated folds, partitioned datasets, replacements, corrected assignments, scores, claims, or approvals.

## Explicit non-approvals
This request does not approve implementation. It does not execute splits. It does not create split files. It does not partition datasets. It does not approve scoring. It does not approve I/O, providers, services, persistence, split generation, backtesting, reporting, simulation, paper trading, trading, order placement, runtime orchestration, production behavior, or autonomy. A separate human decision is required.

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
Acceptance requires exactly this document, its deterministic static test, and the canonical allowlist update; no `meg/` changes; actual PR #368 merge SHA recorded; future implementation limited to exactly two new files; exact eleven-symbol API, assignment and result dataclasses, enums, fields, mapping keys, fixed postures, validation codes, decision options, direct-record ordering, collection occurrence semantics, 29-section literal freeze, mutation coverage, allowlist AST/count validation, source-safety audit, and explicit non-approval posture preserved; mandatory tests passing; and PR updated but not merged.
