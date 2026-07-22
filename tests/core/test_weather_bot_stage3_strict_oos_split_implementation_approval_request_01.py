"""Static, deterministic approval-request contract; no production imports."""
import ast
import re
from pathlib import Path

DOC = Path("docs/prd/WEATHER-BOT-STAGE3-STRICT-OOS-SPLIT-IMPLEMENTATION-APPROVAL-REQUEST-01.md")
ALLOWLIST = Path("tests/core/canonical_id_allowlist.py")
CANONICAL_ID = 'WEATHER-BOT-STAGE3-STRICT-OOS-SPLIT-IMPLEMENTATION-APPROVAL-REQUEST-01'
ACTUAL_PR_368_MERGE_SHA = '1676199c89f2d5d472ea14c66ae841c1878c6018'
EXPECTED_HEADINGS = ['Status and request scope', 'Actual PR #368 merge predecessor', 'Controlling strict-OOS planning contract', 'Requested future implementation slice identity', 'Exact future changed-file matrix', 'Exact future public-symbol matrix', 'Exact future enum matrices', 'Exact future record-field matrix', 'Exact fixed-posture matrix', 'Exact mapping-input matrix', 'Exact single-record validation matrix', 'Exact collection-validation matrix', 'Exact validation-code matrix', 'Exact validation-order contract', 'Exact future test matrix', 'Dependency and import boundary', 'Canonical routing boundary', 'Temporal and no-lookahead boundary', 'Leakage-group and fold boundary', 'Assignment and exclusion semantics', 'Baseline parity boundary', 'Explicit future implementation non-goals', 'Approval decision options', 'Current request status', 'Human decision and separate-approval boundary', 'Fail-closed requirements', 'Explicit non-approvals', 'Machine-checkable assignments', 'Acceptance criteria']
EXPECTED_SECTION_BODIES = {'Status and request scope': 'This artifact is documentation/static-test-only. It asks a human whether a later implementation ticket may create a narrow immutable, caller-supplied strict-OOS split-assignment boundary. It does not approve implementation; it does not execute splits; it does not create split files; it does not partition datasets; it does not approve scoring; a separate human decision is required.', 'Actual PR #368 merge predecessor': 'Immediate predecessor: PR #368 actual merge commit `1676199c89f2d5d472ea14c66ae841c1878c6018`. The implementation head commit `a5d28d50e82c7d0b101036c89d7f61c6fec564af` is recorded as an ancestor of this actual merge commit. This request uses the actual merge commit, not a preview merge SHA.', 'Controlling strict-OOS planning contract': 'Controlling strict-OOS planning contract: `docs/prd/WEATHER-BOT-STAGE3-STRICT-OOS-SPLIT-CONTRACT-PLANNING-01.md`. Implemented upstream immutable probability-record boundary: `meg/weather/stage3/binary_probability_record.py`. PR #360 planning contract is requirements only, not implementation approval.', 'Requested future implementation slice identity': 'Future implementation ticket identity: narrow immutable, caller-supplied strict-OOS split-assignment boundary only. No split generator, fold builder, dataset partitioner, scorer, serializer, repository, service, or execution function is requested.', 'Exact future changed-file matrix': '| Future file | Action | Boundary |\n| --- | --- | --- |\n| `meg/weather/stage3/strict_oos_split.py` | create | define only the strict-OOS split assignment dataclasses, closed enums, mapping adapter, and validators |\n| `tests/core/test_weather_bot_stage3_strict_oos_split.py` | create | static/unit tests for that narrow boundary only |\nLater ticket must not modify `meg/weather/stage3/__init__.py`, `meg/weather/stage3/binary_probability_record.py`, Stage 2 files, existing tests, allowlists, fixtures, datasets, dependencies, workflows, schemas, migrations, reports, or exports.', 'Exact future public-symbol matrix': '| Order | Public symbol |\n| --- | --- |\n| 1 | `SplitRole` |\n| 2 | `SplitApplicabilityMode` |\n| 3 | `SplitAssignmentStatus` |\n| 4 | `OverlapControlPosture` |\n| 5 | `SplitValidationSeverity` |\n| 6 | `SplitValidationCode` |\n| 7 | `StrictOOSSplitAssignment` |\n| 8 | `StrictOOSSplitValidationResult` |\n| 9 | `strict_oos_split_assignment_from_mapping` |\n| 10 | `validate_strict_oos_split_assignment` |\n| 11 | `validate_strict_oos_split_assignments` |', 'Exact future enum matrices': '### SplitRole\n| Member | Value |\n| --- | --- |\n| `TRAIN` | `train` |\n| `CALIBRATION` | `calibration` |\n| `TEST` | `test` |\n### SplitApplicabilityMode\n| Member | Value |\n| --- | --- |\n| `PRIMARY_TEMPORAL` | `primary_temporal` |\n| `LEAVE_STATION_OUT` | `leave_station_out` |\n| `LEAVE_YEAR_OUT` | `leave_year_out` |\n| `FAMILY_STRATIFIED` | `family_stratified` |\n| `SEASON_OR_REGIME_STRATIFIED` | `season_or_regime_stratified` |\n### SplitAssignmentStatus\n| Member | Value |\n| --- | --- |\n| `ASSIGNED` | `assigned` |\n| `BLOCKED` | `blocked` |\n### OverlapControlPosture\n| Member | Value |\n| --- | --- |\n| `NOT_REQUIRED` | `not_required` |\n| `SATISFIED` | `satisfied` |\n| `UNSATISFIED` | `unsatisfied` |\n### SplitValidationSeverity\n| Member | Value |\n| --- | --- |\n| `PASSED` | `passed` |\n| `BLOCKED` | `blocked` |', 'Exact future record-field matrix': 'Request one frozen dataclass: `@dataclass(frozen=True) class StrictOOSSplitAssignment`.\n| Order | Field | Type |\n| --- | --- | --- |\n| 1 | `split_assignment_id` | `str` |\n| 2 | `split_id` | `str` |\n| 3 | `split_version` | `str` |\n| 4 | `fold_id` | `str` |\n| 5 | `fold_index` | `int` |\n| 6 | `prediction_record_id` | `str` |\n| 7 | `condition_id` | `str` |\n| 8 | `token_id` | `str` |\n| 9 | `outcome` | `str` |\n| 10 | `settlement_rule_id` | `str` |\n| 11 | `settlement_rule_version` | `str` |\n| 12 | `split_role` | `SplitRole` |\n| 13 | `applicability_modes` | `tuple[SplitApplicabilityMode, ...]` |\n| 14 | `assignment_status` | `SplitAssignmentStatus` |\n| 15 | `fold_cutoff` | `str` |\n| 16 | `prediction_as_of` | `str` |\n| 17 | `input_publication_available_at` | `str` |\n| 18 | `target_start_at` | `str` |\n| 19 | `target_end_at` | `str` |\n| 20 | `label_available_at` | `str | None` |\n| 21 | `leakage_group_id` | `str` |\n| 22 | `overlap_control_posture` | `OverlapControlPosture` |\n| 23 | `primary_split_posture` | `str` |\n| 24 | `tuning_posture` | `str` |\n| 25 | `calibration_posture` | `str` |\n| 26 | `baseline_parity_posture` | `str` |\n| 27 | `exclusion_reason` | `str | None` |\n| 28 | `provenance_refs` | `tuple[str, ...]` |\n| 29 | `created_at` | `str` |\n| 30 | `supersedes_split_assignment_id` | `str | None = None` |\nNo identity, timestamp, fold, probability record, cutoff, role, leakage group, provenance, or version may be generated.\n\nRequest one frozen dataclass: `@dataclass(frozen=True) class StrictOOSSplitValidationResult`.\n| Order | Field | Type |\n| --- | --- | --- |\n| 1 | `severity` | `SplitValidationSeverity` |\n| 2 | `passed` | `bool` |\n| 3 | `codes` | `tuple[SplitValidationCode, ...] = ()` |\nPassed result invariants: severity is `PASSED`; passed is `True`; codes is empty.\nBlocked result invariants: severity is `BLOCKED`; passed is `False`; codes is nonempty.\nThe result must contain no record payload, assignments, partitioned output, free-form message, field name, generated repair, score, claim, approval status, readiness status, or evidence-gate result.', 'Exact fixed-posture matrix': '| Field | Exact value |\n| --- | --- |\n| `primary_split_posture` | `rolling_origin_or_walk_forward_required` |\n| `tuning_posture` | `train_or_calibration_only` |\n| `calibration_posture` | `separate_when_required` |\n| `baseline_parity_posture` | `same_folds_and_eligibility_required` |\nNo alternate, hybrid, custom, or dynamically generated posture is requested.', 'Exact mapping-input matrix': 'Future signature: `strict_oos_split_assignment_from_mapping(mapping: object) -> tuple[StrictOOSSplitAssignment | None, StrictOOSSplitValidationResult]`.\n\nExact ordered required mapping keys:\n1. `split_assignment_id`\n2. `split_id`\n3. `split_version`\n4. `fold_id`\n5. `fold_index`\n6. `prediction_record_id`\n7. `condition_id`\n8. `token_id`\n9. `outcome`\n10. `settlement_rule_id`\n11. `settlement_rule_version`\n12. `split_role`\n13. `applicability_modes`\n14. `assignment_status`\n15. `fold_cutoff`\n16. `prediction_as_of`\n17. `input_publication_available_at`\n18. `target_start_at`\n19. `target_end_at`\n20. `label_available_at`\n21. `leakage_group_id`\n22. `overlap_control_posture`\n23. `primary_split_posture`\n24. `tuning_posture`\n25. `calibration_posture`\n26. `baseline_parity_posture`\n27. `exclusion_reason`\n28. `provenance_refs`\n29. `created_at`\n\nThe only optional mapping key is:\n- `supersedes_split_assignment_id`\n\n`label_available_at` is a required key whose value may be `None`. `exclusion_reason` is a required key whose value may be `None`. Absence of either required nullable key produces `MISSING_REQUIRED_FIELD`. Explicit `None` is distinct from absence. No required key receives a default. No unexpected key is discarded. A mapping with shape errors still validates every diagnosable present value. An invalid mapping never returns a partial record. Unexpected-key ordering is exact built-in string keys in lexical order, then non-string keys afterward in original mapping iteration order. Do not sort arbitrary objects by `repr()`.\n\nFor `split_role`, `assignment_status`, and `overlap_control_posture`, mapping adaptation accepts only the exact enum member or the exact built-in string equal to an enum value. It rejects string subclasses, unrelated `StrEnum` members, custom enum members, and every other value. For `applicability_modes`, mapping adaptation accepts only an actual tuple or list. Each entry may be an exact `SplitApplicabilityMode` member or an exact built-in string equal to a member value. After adaptation, output is a tuple, the tuple is nonempty, `PRIMARY_TEMPORAL` is exactly first, no mode is duplicated, caller order is preserved, and any container, entry, ordering, emptiness, or duplicate failure produces exactly one `INVALID_APPLICABILITY_MODES`. For `fold_index`, require `type(value) is int`, reject bool and int subclasses, require value greater than or equal to zero, and any failure produces exactly one `INVALID_INTEGER_FIELD`. For `provenance_refs` mapping input, accept only an actual tuple or list, convert an accepted list to a tuple, preserve order and repeated references, make wrong container produce exactly one `INVALID_PROVENANCE_REF`, make empty tuple/list produce exactly one `EMPTY_PROVENANCE_REFS`, and make each blank, string-subclass, or non-string entry produce one `INVALID_PROVENANCE_REF` in entry order.', 'Exact single-record validation matrix': 'Future signature: `validate_strict_oos_split_assignment(record: StrictOOSSplitAssignment) -> StrictOOSSplitValidationResult`. The direct validator performs no mapping adaptation. Require exact enum members, not strings; an actual tuple of exact applicability enum members; `type(fold_index) is int`; an actual tuple for provenance; and exact built-in strings for text and timestamps.\n\nRequired nonblank text fields in exact order:\n1. `split_assignment_id`\n2. `split_id`\n3. `split_version`\n4. `fold_id`\n5. `prediction_record_id`\n6. `condition_id`\n7. `token_id`\n8. `outcome`\n9. `settlement_rule_id`\n10. `settlement_rule_version`\n11. `leakage_group_id`\n12. `primary_split_posture`\n13. `tuning_posture`\n14. `calibration_posture`\n15. `baseline_parity_posture`\nEach invalid field produces one `BLANK_REQUIRED_TEXT`. If `exclusion_reason` is not `None`, it must be an exact nonblank built-in string. If `supersedes_split_assignment_id` is not `None`, it must be an exact nonblank built-in string. Each invalid supplied nullable text value produces one `BLANK_REQUIRED_TEXT` after required-text checks.\n\nTimestamp fields in exact parse order: `fold_cutoff`, `prediction_as_of`, `input_publication_available_at`, `target_start_at`, `target_end_at`, `label_available_at` only when not `None`, and `created_at`. A timestamp is valid only when the value is an exact built-in nonblank string, `datetime.fromisoformat` accepts it, `tzinfo` is not `None`, and `utcoffset()` is not `None`. Do not normalize or rewrite stored timestamp strings. Do not use current time. Produce one `INVALID_TIMESTAMP` for every invalid timestamp in that exact order. Only perform a comparison when all timestamps required by that comparison are valid. General temporal rules apply to assigned and blocked records in this code order: `INPUT_AVAILABLE_AFTER_PREDICTION` for `input_publication_available_at <= prediction_as_of`, `PREDICTION_AFTER_FOLD_CUTOFF` for `prediction_as_of <= fold_cutoff`, and `INVALID_TARGET_WINDOW` for `target_start_at <= target_end_at`.\n\nRole-specific temporal and label rules apply only when `assignment_status is ASSIGNED`. For assigned `TRAIN` or `CALIBRATION`, require `target_end_at <= fold_cutoff`, require `label_available_at` not `None`, require the label timestamp to be valid, and require a valid label timestamp `<= fold_cutoff`; codes occur as `TRAIN_OR_CALIBRATION_AFTER_CUTOFF` then `TRAIN_OR_CALIBRATION_LABEL_UNAVAILABLE_BY_CUTOFF`. For assigned `TEST`, require `target_start_at > fold_cutoff`; `label_available_at` may be `None`; if a valid label timestamp is present, it must be strictly later than `fold_cutoff`; codes occur as `TEST_NOT_STRICTLY_AFTER_CUTOFF` then `TEST_LABEL_AVAILABLE_BY_CUTOFF`. Assignment-status consistency codes occur afterward as `ASSIGNED_WITH_EXCLUSION_REASON`, `BLOCKED_WITHOUT_EXCLUSION_REASON`, and `UNSATISFIED_OVERLAP_CONTROL_ASSIGNED`. Assigned record requires `exclusion_reason is None`; blocked record requires an exact nonblank exclusion reason; assigned record may not use `UNSATISFIED`; blocked record may use `UNSATISFIED`; blocked records skip assigned role-specific temporal and label checks; blocked records still receive general syntax, enum, fixed-posture, timestamp, general temporal, provenance, and supersession validation.', 'Exact collection-validation matrix': 'Future signature: `validate_strict_oos_split_assignments(assignments: tuple[StrictOOSSplitAssignment, ...]) -> StrictOOSSplitValidationResult`. Root behavior: non-tuple root returns only `INVALID_ASSIGNMENT_COLLECTION_TYPE`; empty tuple returns only `EMPTY_ASSIGNMENT_COLLECTION`; a nonempty tuple validates each element in tuple order; an element that is not an actual `StrictOOSSplitAssignment` produces one `INVALID_ASSIGNMENT_COLLECTION_TYPE` in its tuple position and is skipped by later collection comparisons.\n\nFor a nonempty tuple, final result order is each element’s complete direct-record validation codes in tuple order, then `DUPLICATE_ASSIGNMENT_ID`, `DUPLICATE_FOLD_RECORD_ASSIGNMENT`, `DUPLICATE_TEST_RECORD`, `INCONSISTENT_SPLIT_ID`, `INCONSISTENT_SPLIT_VERSION`, `INCONSISTENT_FOLD_DEFINITION`, `NON_MONOTONIC_FOLD_CUTOFF`, and `LEAKAGE_GROUP_ROLE_CONFLICT`. Append one `DUPLICATE_ASSIGNMENT_ID` for each later valid record whose nonblank `split_assignment_id` was previously seen, using tuple order. Append one `DUPLICATE_FOLD_RECORD_ASSIGNMENT` for each later valid record whose valid `(fold_id, prediction_record_id)` pair was previously seen, including assigned and blocked records. Append one `DUPLICATE_TEST_RECORD` for each later assigned `TEST` record whose valid `prediction_record_id` previously appeared as an assigned `TEST` record in a different fold, ignoring blocked records. Use the first valid nonblank split identity as the baseline and append one `INCONSISTENT_SPLIT_ID` for each later valid record whose valid split ID differs. Use the first valid nonblank split version as the baseline and append one `INCONSISTENT_SPLIT_VERSION` for each later valid record whose valid split version differs. For valid records, each `fold_id` must map to exactly one `fold_index` and `fold_cutoff`, and each `fold_index` must map to exactly one `fold_id` and `fold_cutoff`; append one `INCONSISTENT_FOLD_DEFINITION` for each later record that conflicts with either previously established mapping. For monotonic fold cutoffs, use the first-seen consistent valid definition for each fold index, order unique definitions by numeric `fold_index`, and append one `NON_MONOTONIC_FOLD_CUTOFF` for each adjacent later index whose valid cutoff is less than or equal to the previous valid cutoff. Do not alter, generate, or infer a cutoff. For leakage-group role conflict, use assigned records only, key by `(fold_id, leakage_group_id)`, record the first valid role, append one `LEAKAGE_GROUP_ROLE_CONFLICT` for each later assigned record with the same key but a different role, and ignore blocked records. Do not generate folds, partitions, replacements, or corrected assignments.', 'Exact validation-code matrix': 'Define closed enum `SplitValidationCode` in this exact order:\n1. `MISSING_REQUIRED_FIELD = "missing_required_field"`\n2. `UNEXPECTED_FIELD = "unexpected_field"`\n3. `BLANK_REQUIRED_TEXT = "blank_required_text"`\n4. `INVALID_SPLIT_ROLE = "invalid_split_role"`\n5. `INVALID_APPLICABILITY_MODES = "invalid_applicability_modes"`\n6. `INVALID_ASSIGNMENT_STATUS = "invalid_assignment_status"`\n7. `INVALID_OVERLAP_CONTROL_POSTURE = "invalid_overlap_control_posture"`\n8. `INVALID_INTEGER_FIELD = "invalid_integer_field"`\n9. `INVALID_FIXED_POSTURE = "invalid_fixed_posture"`\n10. `INVALID_TIMESTAMP = "invalid_timestamp"`\n11. `INPUT_AVAILABLE_AFTER_PREDICTION = "input_available_after_prediction"`\n12. `PREDICTION_AFTER_FOLD_CUTOFF = "prediction_after_fold_cutoff"`\n13. `INVALID_TARGET_WINDOW = "invalid_target_window"`\n14. `TRAIN_OR_CALIBRATION_AFTER_CUTOFF = "train_or_calibration_after_cutoff"`\n15. `TRAIN_OR_CALIBRATION_LABEL_UNAVAILABLE_BY_CUTOFF = "train_or_calibration_label_unavailable_by_cutoff"`\n16. `TEST_NOT_STRICTLY_AFTER_CUTOFF = "test_not_strictly_after_cutoff"`\n17. `TEST_LABEL_AVAILABLE_BY_CUTOFF = "test_label_available_by_cutoff"`\n18. `ASSIGNED_WITH_EXCLUSION_REASON = "assigned_with_exclusion_reason"`\n19. `BLOCKED_WITHOUT_EXCLUSION_REASON = "blocked_without_exclusion_reason"`\n20. `UNSATISFIED_OVERLAP_CONTROL_ASSIGNED = "unsatisfied_overlap_control_assigned"`\n21. `EMPTY_PROVENANCE_REFS = "empty_provenance_refs"`\n22. `INVALID_PROVENANCE_REF = "invalid_provenance_ref"`\n23. `SELF_SUPERSESSION = "self_supersession"`\n24. `INVALID_ASSIGNMENT_COLLECTION_TYPE = "invalid_assignment_collection_type"`\n25. `EMPTY_ASSIGNMENT_COLLECTION = "empty_assignment_collection"`\n26. `DUPLICATE_ASSIGNMENT_ID = "duplicate_assignment_id"`\n27. `DUPLICATE_FOLD_RECORD_ASSIGNMENT = "duplicate_fold_record_assignment"`\n28. `DUPLICATE_TEST_RECORD = "duplicate_test_record"`\n29. `INCONSISTENT_SPLIT_ID = "inconsistent_split_id"`\n30. `INCONSISTENT_SPLIT_VERSION = "inconsistent_split_version"`\n31. `INCONSISTENT_FOLD_DEFINITION = "inconsistent_fold_definition"`\n32. `NON_MONOTONIC_FOLD_CUTOFF = "non_monotonic_fold_cutoff"`\n33. `LEAKAGE_GROUP_ROLE_CONFLICT = "leakage_group_role_conflict"`\nNo custom validation codes.', 'Exact validation-order contract': 'Complete direct-record validation order: all `BLANK_REQUIRED_TEXT` occurrences; `INVALID_SPLIT_ROLE`; `INVALID_APPLICABILITY_MODES`; `INVALID_ASSIGNMENT_STATUS`; `INVALID_OVERLAP_CONTROL_POSTURE`; `INVALID_INTEGER_FIELD`; one `INVALID_FIXED_POSTURE` per invalid fixed field in primary split, tuning, calibration, baseline parity order; all `INVALID_TIMESTAMP` occurrences; general temporal codes; assigned role-specific temporal/label codes; assignment-status consistency codes; `EMPTY_PROVENANCE_REFS`; all `INVALID_PROVENANCE_REF` occurrences; `SELF_SUPERSESSION`. Collection validation order follows the collection-validation matrix. Repeated codes must remain repeated. No final sorting, set conversion, filtering, insertion, or deduplication is permitted.', 'Exact future test matrix': 'Future tests must cover exact public API; exact enum names, values, and order; exact record/result fields, types, order, defaults, and frozen posture; exact function signatures; mapping-shape aggregation; every required text field; enum adaptation and rejection; exact `fold_index`; timestamp parsing; no-lookahead; fold cutoff eligibility; target-window ordering; train/calibration label isolation; strict test-after-cutoff; test-label no-lookahead; applicability ordering and uniqueness; fixed postures; assignment/exclusion consistency; overlap consistency; provenance; supersession; deterministic repeated-code ordering; collection type and emptiness; split/version consistency; duplicate assignment, fold-record, and test-record detection; fold-definition consistency; monotonically advancing cutoffs; within-fold leakage-group role isolation; blocked-record exclusion; canonical routing; no non-routing market key; no `token_outcome_pair`; and no I/O, providers, services, persistence, split generation, scoring, backtesting, simulation, or trading.', 'Dependency and import boundary': 'The later implementation must remain standard-library-only unless a separate approval changes that boundary. No I/O, providers, services, persistence, schemas, migrations, workflows, dependency changes, dynamic imports, database access, subprocess, network access, shell execution, or Git execution are approved.', 'Canonical routing boundary': 'Canonical routing remains exactly `condition_id`, `token_id`, and `outcome`. `market_id` remains non-routing only and must not become a routing key. `token_outcome_pair` must not be added as a public input or route.', 'Temporal and no-lookahead boundary': 'Strict temporal posture requires timezone-aware timestamps, input availability no later than prediction, prediction no later than fold cutoff, train/calibration labels available by cutoff, and test targets strictly after cutoff without labels available by cutoff. Rolling-origin or walk-forward primacy is preserved; shuffled-random primary splitting is not requested. This request does not approve implementation and does not execute splits.', 'Leakage-group and fold boundary': 'Leakage group and fold identifiers must be caller-supplied, immutable, and auditable. Caller-supplied fold definitions and immutable cutoffs are required. The future validator may reject conflicts but must not generate folds, choose cutoffs, partition datasets, alter assignments, invent fold count, invent fold duration, invent sample minimums, or invent embargo duration.', 'Assignment and exclusion semantics': 'Assigned records are eligible only when exclusion reason is absent and overlap control is not unsatisfied. Blocked records require an exclusion reason and remain syntactically valid and auditable, but are ignored for collection leakage role conflict and duplicate-test calculations. Blocked status does not approve pooling, reassignment, or boundary changes.', 'Baseline parity boundary': 'Baseline parity posture must equal `same_folds_and_eligibility_required`. This preserves later baseline comparability requirements without approving baseline calculation, scoring, diagnostics, claims, or evidence-gate evaluation.', 'Explicit future implementation non-goals': 'The future requested implementation must not:\n- generate fold assignments;\n- choose cutoffs;\n- calculate gaps or embargoes;\n- invent sample thresholds;\n- load probability records from files;\n- fetch data;\n- expand the corpus;\n- inspect settlement outcomes during split design;\n- train models;\n- calculate features;\n- calculate baselines;\n- score predictions;\n- calculate diagnostics;\n- join labels;\n- create evaluation results or claims;\n- evaluate an evidence gate;\n- persist assignments;\n- serialize files;\n- create database objects;\n- create reports or exports;\n- schedule work;\n- run background tasks;\n- simulate;\n- paper trade;\n- trade;\n- place orders;\n- add runtime orchestration;\n- grant autonomy;', 'Approval decision options': 'Exact options:\n- `approve_later_strict_oos_split_assignment_implementation_ticket`\n- `request_approval_request_revision`\n- `hold`\n- `block`', 'Current request status': '`request_prepared_implementation_not_approved`', 'Human decision and separate-approval boundary': 'A separate human decision is required before any implementation ticket may proceed. This document does not approve implementation, does not execute splits, does not create split files, does not partition datasets, and does not approve scoring.', 'Fail-closed requirements': 'Invalid mapping input, invalid records, invalid collections, ambiguous values, unexpected keys, missing required fields, non-aware timestamps, temporal leakage risk, duplicate identity, fold inconsistency, and leakage-group role conflict must fail closed with ordered codes. Invalid input must not produce partial records, generated folds, partitioned datasets, replacements, corrected assignments, scores, claims, or approvals.', 'Explicit non-approvals': 'This request does not approve implementation. It does not execute splits. It does not create split files. It does not partition datasets. It does not approve scoring. It does not approve I/O, providers, services, persistence, split generation, backtesting, reporting, simulation, paper trading, trading, order placement, runtime orchestration, production behavior, or autonomy. A separate human decision is required.', 'Machine-checkable assignments': '```yaml\nticket: WEATHER-BOT-STAGE3-STRICT-OOS-SPLIT-IMPLEMENTATION-APPROVAL-REQUEST-01\nactual_pr_368_merge_sha: 1676199c89f2d5d472ea14c66ae841c1878c6018\nrequest_status: request_prepared_implementation_not_approved\nimplementation_approved: false\nexecutes_splits: false\ncreates_split_files: false\npartitions_datasets: false\napproves_scoring: false\nseparate_human_decision_required: true\nfuture_files_exact:\n  - meg/weather/stage3/strict_oos_split.py\n  - tests/core/test_weather_bot_stage3_strict_oos_split.py\n```', 'Acceptance criteria': 'Acceptance requires exactly this document, its deterministic static test, and the canonical allowlist update; no `meg/` changes; actual PR #368 merge SHA recorded; future implementation limited to exactly two new files; exact eleven-symbol API, assignment and result dataclasses, enums, fields, mapping keys, fixed postures, validation codes, decision options, direct-record ordering, collection occurrence semantics, 29-section literal freeze, mutation coverage, allowlist AST/count validation, source-safety audit, and explicit non-approval posture preserved; mandatory tests passing; and PR updated but not merged.'}
EXPECTED_FUTURE_CHANGED_FILE_TABLE = [['Future file', 'Action', 'Boundary'], ['---', '---', '---'], ['meg/weather/stage3/strict_oos_split.py', 'create', 'define only the strict-OOS split assignment dataclasses, closed enums, mapping adapter, and validators'], ['tests/core/test_weather_bot_stage3_strict_oos_split.py', 'create', 'static/unit tests for that narrow boundary only']]
EXPECTED_PUBLIC_SYMBOL_TABLE = [['Order', 'Public symbol'], ['---', '---'], ['1', 'SplitRole'], ['2', 'SplitApplicabilityMode'], ['3', 'SplitAssignmentStatus'], ['4', 'OverlapControlPosture'], ['5', 'SplitValidationSeverity'], ['6', 'SplitValidationCode'], ['7', 'StrictOOSSplitAssignment'], ['8', 'StrictOOSSplitValidationResult'], ['9', 'strict_oos_split_assignment_from_mapping'], ['10', 'validate_strict_oos_split_assignment'], ['11', 'validate_strict_oos_split_assignments']]
EXPECTED_ENUMS = {'SplitRole': [('TRAIN', 'train'), ('CALIBRATION', 'calibration'), ('TEST', 'test')], 'SplitApplicabilityMode': [('PRIMARY_TEMPORAL', 'primary_temporal'), ('LEAVE_STATION_OUT', 'leave_station_out'), ('LEAVE_YEAR_OUT', 'leave_year_out'), ('FAMILY_STRATIFIED', 'family_stratified'), ('SEASON_OR_REGIME_STRATIFIED', 'season_or_regime_stratified')], 'SplitAssignmentStatus': [('ASSIGNED', 'assigned'), ('BLOCKED', 'blocked')], 'OverlapControlPosture': [('NOT_REQUIRED', 'not_required'), ('SATISFIED', 'satisfied'), ('UNSATISFIED', 'unsatisfied')], 'SplitValidationSeverity': [('PASSED', 'passed'), ('BLOCKED', 'blocked')]}
EXPECTED_RECORD_FIELDS = [('split_assignment_id', 'str'), ('split_id', 'str'), ('split_version', 'str'), ('fold_id', 'str'), ('fold_index', 'int'), ('prediction_record_id', 'str'), ('condition_id', 'str'), ('token_id', 'str'), ('outcome', 'str'), ('settlement_rule_id', 'str'), ('settlement_rule_version', 'str'), ('split_role', 'SplitRole'), ('applicability_modes', 'tuple[SplitApplicabilityMode, ...]'), ('assignment_status', 'SplitAssignmentStatus'), ('fold_cutoff', 'str'), ('prediction_as_of', 'str'), ('input_publication_available_at', 'str'), ('target_start_at', 'str'), ('target_end_at', 'str'), ('label_available_at', 'str | None'), ('leakage_group_id', 'str'), ('overlap_control_posture', 'OverlapControlPosture'), ('primary_split_posture', 'str'), ('tuning_posture', 'str'), ('calibration_posture', 'str'), ('baseline_parity_posture', 'str'), ('exclusion_reason', 'str | None'), ('provenance_refs', 'tuple[str, ...]'), ('created_at', 'str'), ('supersedes_split_assignment_id', 'str | None = None')]
EXPECTED_RESULT_FIELDS = [('severity', 'SplitValidationSeverity'), ('passed', 'bool'), ('codes', 'tuple[SplitValidationCode, ...] = ()')]
EXPECTED_MAPPING_REQUIRED_KEYS = ['split_assignment_id', 'split_id', 'split_version', 'fold_id', 'fold_index', 'prediction_record_id', 'condition_id', 'token_id', 'outcome', 'settlement_rule_id', 'settlement_rule_version', 'split_role', 'applicability_modes', 'assignment_status', 'fold_cutoff', 'prediction_as_of', 'input_publication_available_at', 'target_start_at', 'target_end_at', 'label_available_at', 'leakage_group_id', 'overlap_control_posture', 'primary_split_posture', 'tuning_posture', 'calibration_posture', 'baseline_parity_posture', 'exclusion_reason', 'provenance_refs', 'created_at']
EXPECTED_MAPPING_OPTIONAL_KEYS = ['supersedes_split_assignment_id']
EXPECTED_FIXED_POSTURES = [('primary_split_posture', 'rolling_origin_or_walk_forward_required'), ('tuning_posture', 'train_or_calibration_only'), ('calibration_posture', 'separate_when_required'), ('baseline_parity_posture', 'same_folds_and_eligibility_required')]
EXPECTED_VALIDATION_CODES = ['MISSING_REQUIRED_FIELD = "missing_required_field"', 'UNEXPECTED_FIELD = "unexpected_field"', 'BLANK_REQUIRED_TEXT = "blank_required_text"', 'INVALID_SPLIT_ROLE = "invalid_split_role"', 'INVALID_APPLICABILITY_MODES = "invalid_applicability_modes"', 'INVALID_ASSIGNMENT_STATUS = "invalid_assignment_status"', 'INVALID_OVERLAP_CONTROL_POSTURE = "invalid_overlap_control_posture"', 'INVALID_INTEGER_FIELD = "invalid_integer_field"', 'INVALID_FIXED_POSTURE = "invalid_fixed_posture"', 'INVALID_TIMESTAMP = "invalid_timestamp"', 'INPUT_AVAILABLE_AFTER_PREDICTION = "input_available_after_prediction"', 'PREDICTION_AFTER_FOLD_CUTOFF = "prediction_after_fold_cutoff"', 'INVALID_TARGET_WINDOW = "invalid_target_window"', 'TRAIN_OR_CALIBRATION_AFTER_CUTOFF = "train_or_calibration_after_cutoff"', 'TRAIN_OR_CALIBRATION_LABEL_UNAVAILABLE_BY_CUTOFF = "train_or_calibration_label_unavailable_by_cutoff"', 'TEST_NOT_STRICTLY_AFTER_CUTOFF = "test_not_strictly_after_cutoff"', 'TEST_LABEL_AVAILABLE_BY_CUTOFF = "test_label_available_by_cutoff"', 'ASSIGNED_WITH_EXCLUSION_REASON = "assigned_with_exclusion_reason"', 'BLOCKED_WITHOUT_EXCLUSION_REASON = "blocked_without_exclusion_reason"', 'UNSATISFIED_OVERLAP_CONTROL_ASSIGNED = "unsatisfied_overlap_control_assigned"', 'EMPTY_PROVENANCE_REFS = "empty_provenance_refs"', 'INVALID_PROVENANCE_REF = "invalid_provenance_ref"', 'SELF_SUPERSESSION = "self_supersession"', 'INVALID_ASSIGNMENT_COLLECTION_TYPE = "invalid_assignment_collection_type"', 'EMPTY_ASSIGNMENT_COLLECTION = "empty_assignment_collection"', 'DUPLICATE_ASSIGNMENT_ID = "duplicate_assignment_id"', 'DUPLICATE_FOLD_RECORD_ASSIGNMENT = "duplicate_fold_record_assignment"', 'DUPLICATE_TEST_RECORD = "duplicate_test_record"', 'INCONSISTENT_SPLIT_ID = "inconsistent_split_id"', 'INCONSISTENT_SPLIT_VERSION = "inconsistent_split_version"', 'INCONSISTENT_FOLD_DEFINITION = "inconsistent_fold_definition"', 'NON_MONOTONIC_FOLD_CUTOFF = "non_monotonic_fold_cutoff"', 'LEAKAGE_GROUP_ROLE_CONFLICT = "leakage_group_role_conflict"']
EXPECTED_DECISION_OPTIONS = ['approve_later_strict_oos_split_assignment_implementation_ticket', 'request_approval_request_revision', 'hold', 'block']
EXPECTED_MACHINE_ASSIGNMENTS = {'ticket': 'WEATHER-BOT-STAGE3-STRICT-OOS-SPLIT-IMPLEMENTATION-APPROVAL-REQUEST-01', 'actual_pr_368_merge_sha': '1676199c89f2d5d472ea14c66ae841c1878c6018', 'request_status': 'request_prepared_implementation_not_approved', 'implementation_approved': 'false', 'executes_splits': 'false', 'creates_split_files': 'false', 'partitions_datasets': 'false', 'approves_scoring': 'false', 'separate_human_decision_required': 'true'}
EXPECTED_MACHINE_FUTURE_FILES = ['meg/weather/stage3/strict_oos_split.py', 'tests/core/test_weather_bot_stage3_strict_oos_split.py']
EXPECTED_HEADING_CATEGORIES = {'exact_structured_table': ['Exact future changed-file matrix', 'Exact future public-symbol matrix', 'Exact future enum matrices', 'Exact future record-field matrix', 'Exact fixed-posture matrix', 'Exact mapping-input matrix', 'Exact single-record validation matrix', 'Exact collection-validation matrix', 'Exact validation-code matrix', 'Approval decision options'], 'exact_machine_block': ['Machine-checkable assignments'], 'exact_prose_body': ['Status and request scope', 'Actual PR #368 merge predecessor', 'Controlling strict-OOS planning contract', 'Requested future implementation slice identity', 'Exact validation-order contract', 'Exact future test matrix', 'Dependency and import boundary', 'Canonical routing boundary', 'Temporal and no-lookahead boundary', 'Leakage-group and fold boundary', 'Assignment and exclusion semantics', 'Baseline parity boundary', 'Explicit future implementation non-goals', 'Current request status', 'Human decision and separate-approval boundary', 'Fail-closed requirements', 'Explicit non-approvals', 'Acceptance criteria']}
EXPECTED_ALLOWLIST_PATHS = ['docs/prd/WEATHER-BOT-STAGE3-STRICT-OOS-SPLIT-IMPLEMENTATION-APPROVAL-REQUEST-01.md', 'tests/core/test_weather_bot_stage3_strict_oos_split_implementation_approval_request_01.py']

REQUIRED_ORACLE_NAMES = [
    "CANONICAL_ID", "ACTUAL_PR_368_MERGE_SHA", "EXPECTED_HEADINGS", "EXPECTED_SECTION_BODIES",
    "EXPECTED_FUTURE_CHANGED_FILE_TABLE", "EXPECTED_PUBLIC_SYMBOL_TABLE", "EXPECTED_ENUMS",
    "EXPECTED_RECORD_FIELDS", "EXPECTED_RESULT_FIELDS", "EXPECTED_MAPPING_REQUIRED_KEYS",
    "EXPECTED_MAPPING_OPTIONAL_KEYS", "EXPECTED_FIXED_POSTURES", "EXPECTED_VALIDATION_CODES",
    "EXPECTED_DECISION_OPTIONS", "EXPECTED_MACHINE_ASSIGNMENTS", "EXPECTED_MACHINE_FUTURE_FILES",
    "EXPECTED_HEADING_CATEGORIES", "EXPECTED_ALLOWLIST_PATHS",
]

def _read(path):
    return path.read_text()

def _headings(text):
    return re.findall(r"^## (.+)$", text, re.MULTILINE)

def _sections(text):
    matches = list(re.finditer(r"^## (.+)$", text, re.MULTILINE))
    result = {}
    for index, match in enumerate(matches):
        start = match.end() + 1
        end = matches[index + 1].start() - 1 if index + 1 < len(matches) else len(text)
        result[match.group(1)] = text[start:end].rstrip("\n")
    return result

def _table_rows(section):
    rows = []
    for line in section.splitlines():
        if line.startswith("|"):
            rows.append([cell.strip().strip("`") for cell in line.strip().strip("|").split("|")])
    return rows

def _record_result_rows(section, marker):
    after = section.split(marker, 1)[1]
    rows = []
    for line in after.splitlines():
        match = re.match(r"^\| (\d+) \| `([^`]+)` \| `([^`]+)` \|$", line)
        if match:
            rows.append((match.group(2), match.group(3)))
    return rows

def _numbered(section):
    rows = []
    for line in section.splitlines():
        match = re.match(r"^(\d+)\. `(.+)`$", line)
        if match:
            rows.append((match.group(1), match.group(2)))
    return rows

def _bullets(section):
    rows = []
    for line in section.splitlines():
        match = re.match(r"^- `(.+)`$", line)
        if match:
            rows.append(match.group(1))
    return rows

def _machine(section):
    values = {}
    files = []
    in_block = False
    for line in section.splitlines():
        if line == "```yaml":
            in_block = True
            continue
        if line == "```":
            in_block = False
            continue
        if not in_block:
            continue
        if line.startswith("  - "):
            files.append(line[4:])
        elif ": " in line:
            key, value = line.split(": ", 1)
            values[key] = value
    return values, files

def validate_header(text):
    lines = text.splitlines()
    assert lines[0] == "# " + CANONICAL_ID
    assert lines[2] == "Canonical ID: " + CANONICAL_ID
    assert _headings(text) == EXPECTED_HEADINGS

def validate_exact_section_bodies(sections):
    assert list(sections.keys()) == EXPECTED_HEADINGS
    assert sections == EXPECTED_SECTION_BODIES

def validate_future_changed_file_table(sections):
    assert _table_rows(sections["Exact future changed-file matrix"]) == EXPECTED_FUTURE_CHANGED_FILE_TABLE

def validate_public_symbol_table(sections):
    assert _table_rows(sections["Exact future public-symbol matrix"]) == EXPECTED_PUBLIC_SYMBOL_TABLE

def validate_enum_section(sections):
    section = sections["Exact future enum matrices"]
    names = re.findall(r"^### (.+)$", section, re.MULTILINE)
    assert names == list(EXPECTED_ENUMS.keys())
    for name, expected in EXPECTED_ENUMS.items():
        match = re.search(r"^### " + re.escape(name) + r"\n(.+?)(?=^### |\Z)", section, re.MULTILINE | re.DOTALL)
        assert match is not None
        rows = _table_rows(match.group(1))
        assert rows == [["Member", "Value"], ["---", "---"]] + [[member, value] for member, value in expected]

def validate_record_result_section(sections):
    section = sections["Exact future record-field matrix"]
    assert "`@dataclass(frozen=True) class StrictOOSSplitAssignment`" in section
    assert "`@dataclass(frozen=True) class StrictOOSSplitValidationResult`" in section
    record_part = section.split("Request one frozen dataclass: `@dataclass(frozen=True) class StrictOOSSplitValidationResult`.", 1)[0]
    record_rows = []
    for line in record_part.splitlines():
        match = re.match(r"^\| (\d+) \| `([^`]+)` \| `([^`]+)` \|$", line)
        if match:
            assert int(match.group(1)) == len(record_rows) + 1
            record_rows.append((match.group(2), match.group(3)))
    assert record_rows == EXPECTED_RECORD_FIELDS
    result_rows = _record_result_rows(section, "Request one frozen dataclass: `@dataclass(frozen=True) class StrictOOSSplitValidationResult`.")
    assert result_rows == EXPECTED_RESULT_FIELDS
    assert "Passed result invariants: severity is `PASSED`; passed is `True`; codes is empty." in section
    assert "Blocked result invariants: severity is `BLOCKED`; passed is `False`; codes is nonempty." in section

def validate_mapping_section(sections):
    section = sections["Exact mapping-input matrix"]
    numbered = _numbered(section)
    assert numbered == [(str(index), key) for index, key in enumerate(EXPECTED_MAPPING_REQUIRED_KEYS, 1)]
    assert _bullets(section) == EXPECTED_MAPPING_OPTIONAL_KEYS
    for phrase in ["label_available_at` is a required key whose value may be `None`", "exclusion_reason` is a required key whose value may be `None`", "Explicit `None` is distinct from absence", "Do not sort arbitrary objects by `repr()`", "string subclasses", "type(value) is int", "EMPTY_PROVENANCE_REFS"]:
        assert phrase in section

def validate_fixed_postures(sections):
    rows = _table_rows(sections["Exact fixed-posture matrix"])
    assert rows == [["Field", "Exact value"], ["---", "---"]] + [[field, value] for field, value in EXPECTED_FIXED_POSTURES]

def validate_validation_codes(sections):
    numbered = _numbered(sections["Exact validation-code matrix"])
    assert numbered == [(str(index), code) for index, code in enumerate(EXPECTED_VALIDATION_CODES, 1)]

def validate_decisions(sections):
    assert _bullets(sections["Approval decision options"]) == EXPECTED_DECISION_OPTIONS

def validate_machine(sections):
    values, files = _machine(sections["Machine-checkable assignments"])
    assert values == EXPECTED_MACHINE_ASSIGNMENTS
    assert files == EXPECTED_MACHINE_FUTURE_FILES

def validate_heading_categories():
    validators = {
        "exact_structured_table": [validate_future_changed_file_table, validate_public_symbol_table, validate_enum_section, validate_record_result_section, validate_mapping_section, validate_fixed_postures, validate_validation_codes, validate_decisions],
        "exact_machine_block": [validate_machine],
        "exact_prose_body": [validate_exact_section_bodies],
    }
    assigned = []
    for category, headings in EXPECTED_HEADING_CATEGORIES.items():
        assert category in validators
        assert headings
        assigned.extend(headings)
    ordered = []
    for heading in EXPECTED_HEADINGS:
        assert heading in assigned
        ordered.append(heading)
    assert ordered == EXPECTED_HEADINGS
    assert len(assigned) == len(set(assigned))

def validate_allowlist():
    source = _read(ALLOWLIST)
    tree = ast.parse(source)
    registry_hits = 0
    mapping_hits = 0
    counts = {}
    for node in ast.walk(tree):
        value_node = None
        target_names = []
        if isinstance(node, ast.Assign):
            target_names = [target.id for target in node.targets if isinstance(target, ast.Name)]
            value_node = node.value
        if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            target_names = [node.target.id]
            value_node = node.value
        if value_node is None:
            continue
        if "_ARCH_ALIGN_03_DOWNSTREAM_ARTIFACTS" in target_names:
            for element in value_node.elts:
                if isinstance(element, ast.Constant) and element.value in EXPECTED_ALLOWLIST_PATHS:
                    registry_hits += 1
        if "ALLOWED_MARKET_ID_OCCURRENCE_LINES" in target_names:
            call = value_node
            assert isinstance(call, ast.Call)
            mapping = call.args[0]
            assert isinstance(mapping, ast.Dict)
            for key, value in zip(mapping.keys, mapping.values):
                if isinstance(key, ast.Constant) and key.value in EXPECTED_ALLOWLIST_PATHS:
                    mapping_hits += 1
                    assert isinstance(value, ast.Constant)
                    assert isinstance(value.value, int)
                    counts[key.value] = value.value
    assert registry_hits == 2
    assert mapping_hits == 2
    for path in EXPECTED_ALLOWLIST_PATHS:
        observed = 0
        for line in Path(path).read_text().splitlines():
            if "market_id" in line:
                observed += 1
        assert counts[path] == observed

def validate_complete(text):
    validate_header(text)
    sections = _sections(text)
    validate_exact_section_bodies(sections)
    validate_future_changed_file_table(sections)
    validate_public_symbol_table(sections)
    validate_enum_section(sections)
    validate_record_result_section(sections)
    validate_mapping_section(sections)
    validate_fixed_postures(sections)
    validate_validation_codes(sections)
    validate_decisions(sections)
    validate_machine(sections)
    validate_heading_categories()

def test_document_contract():
    validate_complete(_read(DOC))

def test_allowlist_registration_and_counts():
    validate_allowlist()

def test_oracles_are_literal_and_complete():
    source = _read(Path(__file__))
    tree = ast.parse(source)
    required = list(REQUIRED_ORACLE_NAMES)
    seen = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id in required:
                    seen[target.id] = seen.get(target.id, 0) + 1
                    assert isinstance(node.value, (ast.Constant, ast.List, ast.Tuple, ast.Dict))
                    for child in ast.walk(node.value):
                        assert not isinstance(child, (ast.Set, ast.Name, ast.Attribute, ast.Subscript, ast.Call, ast.BinOp, ast.JoinedStr, ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp, ast.Starred))
        if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) and node.target.id in required:
            seen[node.target.id] = seen.get(node.target.id, 0) + 1
            assert isinstance(node.value, (ast.Constant, ast.List, ast.Tuple, ast.Dict))
    assert seen == {name: 1 for name in required}
    assert len(EXPECTED_SECTION_BODIES) == 29
    assert list(EXPECTED_SECTION_BODIES.keys()) == EXPECTED_HEADINGS

def _replace_section(text, heading, new_body):
    sections = _sections(text)
    sections[heading] = new_body
    lines = ["# " + CANONICAL_ID, "", "Canonical ID: " + CANONICAL_ID, ""]
    for item in EXPECTED_HEADINGS:
        lines.extend(["## " + item, sections[item], ""])
    return "\n".join(lines).rstrip() + "\n"

def _assert_rejected(mutated, intended_validator):
    sections = _sections(mutated)
    try:
        intended_validator(sections)
    except AssertionError:
        pass
    else:
        raise AssertionError("intended validator accepted mutation")
    try:
        validate_complete(mutated)
    except AssertionError:
        pass
    else:
        raise AssertionError("complete validator accepted mutation")

def _substitute(text, old, new):
    index = text.find(old)
    assert index >= 0
    return text[:index] + new + text[index + len(old):]

def test_every_section_body_mutations_are_rejected():
    text = _read(DOC)
    validators = {
        "Exact future changed-file matrix": validate_future_changed_file_table,
        "Exact future public-symbol matrix": validate_public_symbol_table,
        "Exact future enum matrices": validate_enum_section,
        "Exact future record-field matrix": validate_record_result_section,
        "Exact fixed-posture matrix": validate_fixed_postures,
        "Exact mapping-input matrix": validate_mapping_section,
        "Exact validation-code matrix": validate_validation_codes,
        "Approval decision options": validate_decisions,
        "Machine-checkable assignments": validate_machine,
    }
    for heading in EXPECTED_HEADINGS:
        body = EXPECTED_SECTION_BODIES[heading]
        validator = validate_exact_section_bodies
        mutations = [body + "\nAdditional forbidden sentence.", body.rsplit("\n", 1)[0] if "\n" in body else "", _substitute(body, body[0], "Z")]
        for mutated_body in mutations:
            mutated = _replace_section(text, heading, mutated_body)
            changed = []
            mutated_sections = _sections(mutated)
            for candidate in EXPECTED_HEADINGS:
                if mutated_sections[candidate] != EXPECTED_SECTION_BODIES[candidate]:
                    changed.append(candidate)
            assert changed == [heading]
            _assert_rejected(mutated, validator)

def test_structural_mutations_are_rejected():
    text = _read(DOC)
    cases = [
        ("Actual PR #368 merge predecessor", validate_exact_section_bodies, ACTUAL_PR_368_MERGE_SHA, "0000000000000000000000000000000000000000"),
        ("Exact future changed-file matrix", validate_future_changed_file_table, "| `tests/core/test_weather_bot_stage3_strict_oos_split.py` | create | static/unit tests for that narrow boundary only |", "| `tests/core/test_weather_bot_stage3_strict_oos_split.py` | create | static/unit tests for that narrow boundary only |\n| `extra.py` | create | forbidden |"),
        ("Exact future changed-file matrix", validate_future_changed_file_table, "| `meg/weather/stage3/strict_oos_split.py` | create |", "| `meg/weather/stage3/strict_oos_split.py` | modify |"),
        ("Exact future changed-file matrix", validate_future_changed_file_table, "define only the strict-OOS split assignment dataclasses", "define too much"),
        ("Exact future public-symbol matrix", validate_public_symbol_table, "| 11 | `validate_strict_oos_split_assignments` |", "| 11 | `validate_strict_oos_split_assignments` |\n| 12 | `generate_strict_oos_splits` |"),
        ("Exact future public-symbol matrix", validate_public_symbol_table, "| 1 | `SplitRole` |", "| 99 | `SplitRole` |"),
        ("Exact future enum matrices", validate_enum_section, "### SplitValidationSeverity", "### ExtraEnum\n| Member | Value |\n| --- | --- |\n| `X` | `x` |\n### SplitValidationSeverity"),
        ("Exact future enum matrices", validate_enum_section, "| `TRAIN` | `train` |", "| `TRAIN` | `training` |"),
        ("Exact future record-field matrix", validate_record_result_section, "| 3 | `codes` | `tuple[SplitValidationCode, ...] = ()` |", "| 3 | `codes` | `tuple[SplitValidationCode, ...] = ()` |\n| 4 | `message` | `str` |"),
        ("Exact future record-field matrix", validate_record_result_section, "| 1 | `severity` | `SplitValidationSeverity` |\n| 2 | `passed` | `bool` |", "| 1 | `passed` | `bool` |\n| 2 | `severity` | `SplitValidationSeverity` |"),
        ("Exact mapping-input matrix", validate_mapping_section, "1. `split_assignment_id`\n", ""),
        ("Exact mapping-input matrix", validate_mapping_section, "`label_available_at` is a required key", "`label_available_at` is an optional key"),
        ("Exact mapping-input matrix", validate_mapping_section, "- `supersedes_split_assignment_id`", "- `supersedes_split_assignment_id`\n- `extra_optional`"),
        ("Exact fixed-posture matrix", validate_fixed_postures, "rolling_origin_or_walk_forward_required", "rolling_origin_optional"),
        ("Exact validation-code matrix", validate_validation_codes, "1. `MISSING_REQUIRED_FIELD", "1. `UNEXPECTED_FIELD"),
        ("Exact validation-code matrix", validate_validation_codes, "33. `LEAKAGE_GROUP_ROLE_CONFLICT", "99. `LEAKAGE_GROUP_ROLE_CONFLICT"),
        ("Exact validation-code matrix", validate_validation_codes, "No custom validation codes.", "34. `CUSTOM = \"custom\"`\nNo custom validation codes."),
        ("Approval decision options", validate_decisions, "- `block`", "- `block`\n- `approve_now`"),
        ("Current request status", validate_exact_section_bodies, "request_prepared_implementation_not_approved", "approved"),
        ("Machine-checkable assignments", validate_machine, "future_files_exact:", "extra_key: forbidden\nfuture_files_exact:"),
        ("Machine-checkable assignments", validate_machine, "implementation_approved: false", "implementation_approved: true"),
        ("Status and request scope", validate_exact_section_bodies, "It does not approve implementation;", "It does not approve implementation; This also approves implementation;"),
        ("Status and request scope", validate_exact_section_bodies, "it does not execute splits;", "it does not execute splits; This also executes splits;"),
    ]
    for heading, validator, old, new in cases:
        body = EXPECTED_SECTION_BODIES[heading]
        assert old in body
        mutated = _replace_section(text, heading, _substitute(body, old, new))
        _assert_rejected(mutated, validator)
    lines = text.splitlines()
    insert = lines[:5] + ["## Extra heading", "No."] + lines[5:]
    try:
        validate_complete("\n".join(insert) + "\n")
    except AssertionError:
        pass
    else:
        raise AssertionError("heading insertion accepted")
    deleted = _substitute(text, "## Acceptance criteria\n" + EXPECTED_SECTION_BODIES["Acceptance criteria"] + "\n", "")
    try:
        validate_complete(deleted)
    except AssertionError:
        pass
    else:
        raise AssertionError("heading deletion accepted")
    reordered = _substitute(text, "## Status and request scope", "## Actual PR #368 merge predecessor")
    try:
        validate_complete(reordered)
    except AssertionError:
        pass
    else:
        raise AssertionError("heading reorder accepted")

def test_static_source_safety():
    source = _read(Path(__file__))
    tree = ast.parse(source)
    imports = []
    blocked_names = ["eval", "exec", "open", "getenv", "__import__"]
    blocked_attrs = ["write_text", "write_bytes", "touch", "unlink", "rename"]
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name.split(".")[0])
        if isinstance(node, ast.ImportFrom):
            imports.append((node.module or "").split(".")[0])
        if isinstance(node, ast.Name):
            assert node.id not in blocked_names
        if isinstance(node, ast.Attribute):
            assert node.attr not in blocked_attrs
    assert imports == ["ast", "re", "pathlib"]
