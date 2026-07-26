# WEATHER-BOT-STAGE3-BASELINE-CONTRACTS-IMPLEMENTATION-APPROVAL-REQUEST-01

Canonical ID: WEATHER-BOT-STAGE3-BASELINE-CONTRACTS-IMPLEMENTATION-APPROVAL-REQUEST-01

## Status and scope

This approval request is docs/static-test-only and approval-request-only for `WEATHER-BOT-STAGE3-BASELINE-CONTRACTS-IMPLEMENTATION-APPROVAL-REQUEST-01`. Current request status is exactly `request_prepared_implementation_not_approved`.

It does not implement baseline contracts, calculate climatology, calculate persistence, generate probabilities, create probability records, score records, persist data, add runtime behavior, approve trading, or approve autonomy.

## Immediate predecessor and merge verification

PR #370 is recorded as merged by actual merge commit `ACTUAL_PR_370_MERGE_SHA = c07cef21809e80be7cc8d0bfd81d1d97e809b3bf`. The recorded implementation head `27d09b3691cc1f243a2eeb197811c7e72af09b01` is an ancestor of that actual merge commit, and that actual merge commit is the recorded base for this branch.

`BASE_SHA = c07cef21809e80be7cc8d0bfd81d1d97e809b3bf`.

The preview merge SHA for PR #370 is not used.

## Approval-request purpose and decision boundary

This document asks humans whether a later implementation ticket may create the baseline-contracts module and its focused test. It is not that implementation ticket and does not approve implementation by itself.

A later implementation may proceed only after a separate human approval and a separate PR for `WEATHER-BOT-STAGE3-BASELINE-CONTRACTS-IMPLEMENTATION-01`.

## Planning-contract basis

The authoritative basis is `docs/prd/WEATHER-BOT-STAGE3-BASELINE-CONTRACTS-PLANNING-01.md`, reconciled with the Stage 3 probability-record contract, strict OOS split contract, strict OOS implementation approval request, `meg/weather/stage3/binary_probability_record.py`, `meg/weather/stage3/strict_oos_split.py`, and their focused tests.

The baseline planning contract remains authoritative. This request invents no numeric history window, smoothing constant, sample minimum, sufficiency threshold, fallback hierarchy value, persisted quantity, conversion formula, fold count, cutoff duration, or metric threshold.

## Requested implementation slice identity

Requested later slice: immutable caller-supplied baseline definitions and pure fail-closed validation only.

The slice may validate definitions but must not calculate climatology, calculate persistence, inspect historical data, select conditioning dimensions, select smoothing, select a history window, select a fallback, select a persisted quantity, select a conversion rule, generate a probability, create a probability record, execute a split, score a record, join labels, create diagnostics, create claims, persist anything, generate reports, or add runtime behavior.

## Exact future changed-file matrix

A separately approved later implementation ticket may create exactly these two files:

1. `meg/weather/stage3/baseline_contracts.py`
2. `tests/core/test_weather_bot_stage3_baseline_contracts.py`

No existing file may be modified by that later implementation ticket.

## Exact future public-symbol matrix

Freeze exactly eight public symbols, in this order:

1. `BaselineType`
2. `BaselineDefinitionStatus`
3. `BaselineValidationSeverity`
4. `BaselineValidationCode`
5. `BaselineContractDefinition`
6. `BaselineContractValidationResult`
7. `baseline_contract_definition_from_mapping`
8. `validate_baseline_contract_definition`

No collection validator is approved. No additional public class or function is approved.

## Exact enum matrix

Use `StrEnum`.

BaselineType:
1. `CLIMATOLOGY = "climatology"`
2. `PERSISTENCE = "persistence"`

BaselineDefinitionStatus:
1. `ACTIVE = "active"`
2. `BLOCKED = "blocked"`

BaselineValidationSeverity:
1. `PASSED = "passed"`
2. `BLOCKED = "blocked"`

## Exact future definition-field matrix

Define later only if separately approved: `@dataclass(frozen=True)` `BaselineContractDefinition` with exact fields, types, order, and default posture:

1. `baseline_definition_id: str`
2. `baseline_type: BaselineType`
3. `definition_status: BaselineDefinitionStatus`
4. `baseline_version: str`
5. `method_id: str`
6. `method_version: str`
7. `split_id: str`
8. `split_version: str`
9. `fold_id: str`
10. `fold_index: int`
11. `fold_cutoff: str`
12. `prediction_as_of: str`
13. `input_publication_available_at: str`
14. `definition_declared_at: str`
15. `condition_id: str`
16. `token_id: str`
17. `outcome: str`
18. `settlement_rule_id: str`
19. `settlement_rule_version: str`
20. `source_compatibility_posture: str`
21. `station_compatibility_posture: str`
22. `threshold: str`
23. `unit: str`
24. `comparator: str`
25. `measurement_window: str`
26. `archive_finality_layer: str`
27. `scoring_target_posture: str`
28. `baseline_input_posture: str`
29. `conditioning_dimensions: tuple[str, ...]`
30. `smoothing_definition_id: str | None`
31. `history_window_definition_id: str | None`
32. `hierarchy_definition_id: str | None`
33. `fallback_definition_id: str | None`
34. `persisted_quantity_id: str | None`
35. `conversion_rule_id: str | None`
36. `split_parity_posture: str`
37. `paired_comparison_posture: str`
38. `availability_posture: str`
39. `fallback_posture: str`
40. `tuning_posture: str`
41. `output_contract_posture: str`
42. `market_price_posture: str`
43. `baseline_execution_posture: str`
44. `scoring_execution_posture: str`
45. `storage_persistence_posture: str`
46. `availability_evidence_refs: tuple[str, ...]`
47. `provenance_refs: tuple[str, ...]`
48. `exclusion_reason: str | None`
49. `supersedes_baseline_definition_id: str | None = None`

No field value may be generated. No validation may occur in `__post_init__`. No mutable field or custom mutator is approved.

## Exact validation-result matrix

Define later only if separately approved: `@dataclass(frozen=True)` `BaselineContractValidationResult` with exact fields:

1. `severity: BaselineValidationSeverity`
2. `passed: bool`
3. `codes: tuple[BaselineValidationCode, ...] = ()`

Passed invariant: severity is `PASSED`, passed is `True`, and codes is empty. Blocked invariant: severity is `BLOCKED`, passed is `False`, and codes is nonempty. The result may not contain a generated repair, baseline value, probability, record, score, diagnostic, claim, approval status, readiness status, or free-form message.

## Exact mapping-input matrix

Future mapping signature:

```python
def baseline_contract_definition_from_mapping(
    mapping: object,
) -> tuple[
    BaselineContractDefinition | None,
    BaselineContractValidationResult,
]:
```

Accept only `isinstance(mapping, collections.abc.Mapping)`. For a non-Mapping root, or any ordinary exception during `items()` access, iteration, item unpacking, key recognition, value snapshotting, or mapping materialization, return no definition, a blocked result, and exactly 48 ordered `MISSING_REQUIRED_FIELD` occurrences. Do not catch `BaseException`.

Mapping enum fields accept only the exact enum member or an exact built-in string equal to a member value; accepted strings adapt to exact members. String subclasses, unrelated enums, enum subclasses, and every other object are rejected. Direct validation accepts exact enum members only. A present invalid field appends exactly one corresponding `INVALID_BASELINE_TYPE` or `INVALID_DEFINITION_STATUS`.

`fold_index` requires `type(value) is int` and a value of at least zero. Bool, integer subclasses, and every other object are rejected with exactly one `INVALID_INTEGER_FIELD`; no coercion is permitted.

Mapping `conditioning_dimensions`, `availability_evidence_refs`, and `provenance_refs` accept only an actual tuple or list and convert a list to a tuple. Direct validation requires `type(value) is tuple` and performs no conversion.

For a readable Mapping, exact result order is:

1. missing required keys in required-key order;
2. unexpected exact built-in string keys in lexical order;
3. unexpected non-exact-string keys in original Mapping iteration order;
4. required and supplied-nullable text codes;
5. `INVALID_BASELINE_TYPE`;
6. `INVALID_DEFINITION_STATUS`;
7. `INVALID_INTEGER_FIELD`;
8. fixed-posture codes;
9. timestamp codes;
10. temporal comparison codes;
11. `INVALID_CONDITIONING_DIMENSIONS`;
12. availability-evidence codes;
13. provenance codes;
14. climatology or persistence codes;
15. definition-status consistency codes;
16. `SELF_SUPERSESSION`.

Aggregate every diagnosable present-value failure even when missing or unexpected fields exist. Skip only checks whose prerequisites are absent or unusable. Preserve repeated occurrences. Do not finally sort, filter, insert, remove, convert to a set, or deduplicate codes. Never construct or return a partial definition. Construct the frozen definition only when the complete code sequence is empty, and require it to pass direct validation before return.

## Exact required and optional key matrix

The exact required mapping keys, in order, are:

1. `baseline_definition_id`
2. `baseline_type`
3. `definition_status`
4. `baseline_version`
5. `method_id`
6. `method_version`
7. `split_id`
8. `split_version`
9. `fold_id`
10. `fold_index`
11. `fold_cutoff`
12. `prediction_as_of`
13. `input_publication_available_at`
14. `definition_declared_at`
15. `condition_id`
16. `token_id`
17. `outcome`
18. `settlement_rule_id`
19. `settlement_rule_version`
20. `source_compatibility_posture`
21. `station_compatibility_posture`
22. `threshold`
23. `unit`
24. `comparator`
25. `measurement_window`
26. `archive_finality_layer`
27. `scoring_target_posture`
28. `baseline_input_posture`
29. `conditioning_dimensions`
30. `smoothing_definition_id`
31. `history_window_definition_id`
32. `hierarchy_definition_id`
33. `fallback_definition_id`
34. `persisted_quantity_id`
35. `conversion_rule_id`
36. `split_parity_posture`
37. `paired_comparison_posture`
38. `availability_posture`
39. `fallback_posture`
40. `tuning_posture`
41. `output_contract_posture`
42. `market_price_posture`
43. `baseline_execution_posture`
44. `scoring_execution_posture`
45. `storage_persistence_posture`
46. `availability_evidence_refs`
47. `provenance_refs`
48. `exclusion_reason`

The only optional mapping key is `supersedes_baseline_definition_id`.

Required nullable mapping keys that must be explicitly present even when `None`: `smoothing_definition_id`, `history_window_definition_id`, `hierarchy_definition_id`, `fallback_definition_id`, `persisted_quantity_id`, `conversion_rule_id`, and `exclusion_reason`.

Absence is distinct from explicit `None`. No required field receives a default. A string-subclass key does not satisfy an exact required key and is also unexpected.

Required exact built-in nonblank text fields, in exact validation order, are:

1. `baseline_definition_id`
2. `baseline_version`
3. `method_id`
4. `method_version`
5. `split_id`
6. `split_version`
7. `fold_id`
8. `condition_id`
9. `token_id`
10. `outcome`
11. `settlement_rule_id`
12. `settlement_rule_version`
13. `source_compatibility_posture`
14. `station_compatibility_posture`
15. `threshold`
16. `unit`
17. `comparator`
18. `measurement_window`
19. `archive_finality_layer`
20. `scoring_target_posture`
21. `baseline_input_posture`
22. `split_parity_posture`
23. `paired_comparison_posture`
24. `availability_posture`
25. `fallback_posture`
26. `tuning_posture`
27. `output_contract_posture`
28. `market_price_posture`
29. `baseline_execution_posture`
30. `scoring_execution_posture`
31. `storage_persistence_posture`

A value is valid only when `type(value) is str` and `value.strip()` is nonempty. Each invalid value appends one `BLANK_REQUIRED_TEXT` in this order. Stored values are not stripped or rewritten. Timestamp fields are excluded from this matrix.

Nullable text fields, in exact validation order, are:

1. `smoothing_definition_id`
2. `history_window_definition_id`
3. `hierarchy_definition_id`
4. `fallback_definition_id`
5. `persisted_quantity_id`
6. `conversion_rule_id`
7. `exclusion_reason`
8. `supersedes_baseline_definition_id`

At the generic nullable-text layer, `None` is text-valid. Every supplied non-`None` value must be an exact built-in nonblank string; each invalid supplied value appends one `BLANK_REQUIRED_TEXT` after all required-text checks. Mapping absence remains distinct from explicit `None`.

## Exact fixed-posture matrix

Each field must be an exact built-in string equal to its exact value:

- `scoring_target_posture = "venue_defined_settlement_outcome"`
- `split_parity_posture = "same_folds_cutoffs_eligibility_and_test_records_required"`
- `paired_comparison_posture = "common_test_record_set_required"`
- `availability_posture = "point_in_time_required"`
- `fallback_posture = "predeclared_compatible_or_fail_closed"`
- `tuning_posture = "train_or_calibration_only"`
- `output_contract_posture = "probability_record_contract_required"`
- `market_price_posture = "not_approved_as_baseline"`
- `baseline_execution_posture = "not_approved"`
- `scoring_execution_posture = "not_approved"`
- `storage_persistence_posture = "not_approved"`

Append one `INVALID_FIXED_POSTURE` per invalid field in that order. A blank, non-string, or string-subclass fixed posture may receive both its text code and fixed-posture code.

## Exact timestamp and no-lookahead matrix

Timestamp parse order: `fold_cutoff`, `prediction_as_of`, `input_publication_available_at`, `definition_declared_at`.

A valid timestamp requires an exact built-in nonblank string, `datetime.fromisoformat` success, non-`None` `tzinfo`, and non-`None` `utcoffset()`. Do not normalize stored strings and do not access current time.

Comparison codes, when prerequisites are valid, occur in this order: `INPUT_AVAILABLE_AFTER_PREDICTION`, `PREDICTION_AFTER_FOLD_CUTOFF`, `DEFINITION_DECLARED_AFTER_PREDICTION`. Equality passes.

Conditioning-dimension contract: mapping accepts only an actual tuple or list and converts a list to a tuple; direct input requires `type(conditioning_dimensions) is tuple` without conversion. Each entry must be an exact built-in nonblank string. Caller order is preserved and duplicates are rejected. No sorting, normalization, inference, generation, or deduplication occurs. Any container, entry, or duplication defect appends exactly one `INVALID_CONDITIONING_DIMENSIONS`; container failure prevents entry iteration. An empty valid tuple is allowed for climatology and required for persistence. Persistence's nonempty role check runs only for a generically valid tuple.

Availability-evidence contract: mapping accepts only an actual tuple or list and converts a list to a tuple; direct input requires an actual tuple without conversion. A wrong container appends exactly one `INVALID_AVAILABILITY_EVIDENCE_REF`; an empty accepted container appends exactly one `EMPTY_AVAILABILITY_EVIDENCE_REFS`; each non-exact-string or blank entry appends one `INVALID_AVAILABILITY_EVIDENCE_REF` in caller order. Valid duplicates and caller order are preserved. Container failure prevents entry iteration, and emptiness and entry failures are mutually exclusive. References are not generated, resolved, dereferenced, sorted, or deduplicated.

Provenance contract: mapping accepts only an actual tuple or list and converts a list to a tuple; direct input requires an actual tuple without conversion. A wrong container appends exactly one `INVALID_PROVENANCE_REF`; an empty accepted container appends exactly one `EMPTY_PROVENANCE_REFS`; each invalid entry appends one `INVALID_PROVENANCE_REF` in caller order. Valid duplicates and caller order are preserved. Container failure prevents entry iteration, and emptiness and entry failures are mutually exclusive. References are not normalized, generated, looked up, dereferenced, sorted, or deduplicated.

## Exact climatology matrix

Climatology checks run only when baseline type is valid and is `CLIMATOLOGY`. For explicitly present prerequisites, `baseline_input_posture` must be the exact built-in string `train_only_as_of_history`, otherwise append `CLIMATOLOGY_INVALID_INPUT_POSTURE`. `history_window_definition_id` must be an exact built-in nonblank string; `None`, blank, string subclass, or non-string appends `CLIMATOLOGY_MISSING_HISTORY_WINDOW`, and a non-`None` generic text defect retains its earlier `BLANK_REQUIRED_TEXT`. Valid `conditioning_dimensions` may be empty or nonempty. `smoothing_definition_id`, `hierarchy_definition_id`, and `fallback_definition_id` may be `None` or exact built-in nonblank strings. `persisted_quantity_id` and `conversion_rule_id` must be `None`; when either or both explicitly present values are non-`None`, append exactly one `CLIMATOLOGY_PERSISTENCE_FIELDS_PRESENT`.

Code order: `CLIMATOLOGY_INVALID_INPUT_POSTURE`, `CLIMATOLOGY_MISSING_HISTORY_WINDOW`, `CLIMATOLOGY_PERSISTENCE_FIELDS_PRESENT`.

A missing compatible fallback is not repaired here. `None` means future execution must fail closed if compatible conditioned history is unavailable. No numeric history window, smoothing value, hierarchy, fallback, or sample threshold is created.

For mapping input, a missing required prerequisite receives only its missing-field code and no dependent climatology code.

## Exact persistence matrix

Persistence checks run only when baseline type is valid and is `PERSISTENCE`. For explicitly present prerequisites, `baseline_input_posture` must be the exact built-in string `latest_legitimately_available_compatible_prior_state`, otherwise append `PERSISTENCE_INVALID_INPUT_POSTURE`. A generically valid `conditioning_dimensions` tuple must be empty. `smoothing_definition_id`, `history_window_definition_id`, `hierarchy_definition_id`, and `fallback_definition_id` must all be `None`. If a generically valid conditioning tuple is nonempty or any one or more of those four explicitly present fields is non-`None`, append exactly one `PERSISTENCE_CONDITIONING_FIELDS_PRESENT`.

`persisted_quantity_id` must be an exact built-in nonblank string; `None`, blank, string subclass, or non-string appends `PERSISTENCE_MISSING_QUANTITY`. `conversion_rule_id` has the same posture and appends `PERSISTENCE_MISSING_CONVERSION_RULE`. A text-invalid non-`None` value retains its earlier `BLANK_REQUIRED_TEXT`.

Code order: `PERSISTENCE_INVALID_INPUT_POSTURE`, `PERSISTENCE_CONDITIONING_FIELDS_PRESENT`, `PERSISTENCE_MISSING_QUANTITY`, `PERSISTENCE_MISSING_CONVERSION_RULE`.

No persisted quantity or conversion rule is selected, inferred, executed, or evaluated.

For mapping input, a missing required prerequisite receives only its missing-field code and no dependent persistence code.

## Exact definition-status matrix

Status consistency checks run only when definition status is valid. For `ACTIVE`, explicitly present `exclusion_reason is None` passes; any explicitly present non-`None` value appends `ACTIVE_WITH_EXCLUSION_REASON`. A text-invalid non-`None` value retains its earlier `BLANK_REQUIRED_TEXT`; a missing mapping key receives only `MISSING_REQUIRED_FIELD`.

For `BLOCKED`, an explicitly present exact built-in nonblank string passes. Explicit `None`, blank, string subclass, or non-string appends `BLOCKED_WITHOUT_EXCLUSION_REASON`; invalid non-`None` text retains its earlier `BLANK_REQUIRED_TEXT`; a missing mapping key receives only `MISSING_REQUIRED_FIELD`.

Append `SELF_SUPERSESSION` exactly once only when both identifiers are exact built-in nonblank strings and equal. Do not append it when either is text-invalid. No identity is generated or rewritten.

## Exact validation-code matrix

Exact members, values, and order:

1. `MISSING_REQUIRED_FIELD = "missing_required_field"`
2. `UNEXPECTED_FIELD = "unexpected_field"`
3. `BLANK_REQUIRED_TEXT = "blank_required_text"`
4. `INVALID_BASELINE_TYPE = "invalid_baseline_type"`
5. `INVALID_DEFINITION_STATUS = "invalid_definition_status"`
6. `INVALID_INTEGER_FIELD = "invalid_integer_field"`
7. `INVALID_FIXED_POSTURE = "invalid_fixed_posture"`
8. `INVALID_TIMESTAMP = "invalid_timestamp"`
9. `INPUT_AVAILABLE_AFTER_PREDICTION = "input_available_after_prediction"`
10. `PREDICTION_AFTER_FOLD_CUTOFF = "prediction_after_fold_cutoff"`
11. `DEFINITION_DECLARED_AFTER_PREDICTION = "definition_declared_after_prediction"`
12. `INVALID_CONDITIONING_DIMENSIONS = "invalid_conditioning_dimensions"`
13. `EMPTY_AVAILABILITY_EVIDENCE_REFS = "empty_availability_evidence_refs"`
14. `INVALID_AVAILABILITY_EVIDENCE_REF = "invalid_availability_evidence_ref"`
15. `EMPTY_PROVENANCE_REFS = "empty_provenance_refs"`
16. `INVALID_PROVENANCE_REF = "invalid_provenance_ref"`
17. `CLIMATOLOGY_INVALID_INPUT_POSTURE = "climatology_invalid_input_posture"`
18. `CLIMATOLOGY_MISSING_HISTORY_WINDOW = "climatology_missing_history_window"`
19. `CLIMATOLOGY_PERSISTENCE_FIELDS_PRESENT = "climatology_persistence_fields_present"`
20. `PERSISTENCE_INVALID_INPUT_POSTURE = "persistence_invalid_input_posture"`
21. `PERSISTENCE_CONDITIONING_FIELDS_PRESENT = "persistence_conditioning_fields_present"`
22. `PERSISTENCE_MISSING_QUANTITY = "persistence_missing_quantity"`
23. `PERSISTENCE_MISSING_CONVERSION_RULE = "persistence_missing_conversion_rule"`
24. `ACTIVE_WITH_EXCLUSION_REASON = "active_with_exclusion_reason"`
25. `BLOCKED_WITHOUT_EXCLUSION_REASON = "blocked_without_exclusion_reason"`
26. `SELF_SUPERSESSION = "self_supersession"`

No custom or dynamically generated validation code is permitted.

## Exact validation-order contract

Future direct signature:

```python
def validate_baseline_contract_definition(
    definition: BaselineContractDefinition,
) -> BaselineContractValidationResult:
```

Exact code order: required and supplied-nullable `BLANK_REQUIRED_TEXT`; `INVALID_BASELINE_TYPE`; `INVALID_DEFINITION_STATUS`; `INVALID_INTEGER_FIELD`; fixed-posture codes; timestamp codes; temporal comparison codes; `INVALID_CONDITIONING_DIMENSIONS`; availability-evidence codes; provenance codes; climatology or persistence codes; definition-status consistency codes; `SELF_SUPERSESSION`.

Repeated codes remain repeated. No final sorting, filtering, insertion, removal, set conversion, or deduplication is permitted.

The direct validator assumes an actual `BaselineContractDefinition`. It performs no mapping adaptation, enum-string adaptation, list-to-tuple conversion, text normalization, timestamp normalization, identity generation, evidence generation, provenance generation, or repair.

## Exact future test matrix

Require independent exact expectations for public surface order, all enum matrices, all 26 validation codes, all 49 definition fields, all three result fields, both public signatures, private key/text/timestamp/fixed-posture tuples, non-Mapping and hostile-Mapping roots, every missing key, unexpected-key ordering, string-subclass keys, text fields, enum adaptation and direct rejection, fold-index defects, fixed posture defects, timestamp defects and prerequisite suppression, temporal boundaries, conditioning, evidence, provenance, climatology rules, persistence rules, status consistency, supersession, combined mapping code order, no partial definition, frozen inputs and outputs, deterministic repeated calls, canonical routing, and absence of baseline calculation, probability creation, scoring, I/O, persistence, reports, runtime behavior, simulation, or trading.

Use complete tuple equality. Do not use membership-only, sets, or sorted-result substitutions.

Combined mapping cases must independently assert complete expected tuples for: multiple missing keys; missing plus unexpected keys; missing plus malformed present text; unexpected keys plus invalid enums; invalid integer plus fixed-posture failures; multiple invalid timestamps; temporal plus conditioning failures; evidence plus provenance failures; climatology text and role-specific failures together; persistence conditioning, quantity, and conversion failures together; status plus supersession failures; repeated identical validation codes; and shape plus role-specific failures with dependent-check suppression. Membership-only, count-only, set, or sorted assertions are insufficient.

## Dependency and import boundary

The later implementation may use only Python standard-library imports needed for pure contract validation, such as `collections.abc.Mapping`, `dataclasses.dataclass`, `datetime.datetime`, and `enum.StrEnum`.

It must not add dependencies, workflows, configuration, schemas, migrations, fixtures, datasets, generated files, services, providers, network access, database access, dynamic imports, or package initialization changes.

## Canonical routing and target boundary

Canonical routing remains exactly:

- `condition_id`
- `token_id`
- `outcome`

The non-routing `market_id` identifier remains non-routing. The derived token/outcome identifier remains derived only. Neither is a public input field of the future production module.

## Point-in-time, split-parity, and paired-comparison boundary

The future definition must preserve point-in-time availability, fold cutoff, prediction as-of, declaration time, availability evidence, strict OOS split identity, fold identity, split parity, and paired-comparison posture.

Baseline definitions must remain aligned to the same folds, cutoffs, eligibility, and test records as the candidate path and must fail closed when compatible information is unavailable.

## Explicit future implementation non-goals

This approval request explicitly denies approval for: baseline calculation; climatology estimation; persistence calculation; history lookup; persisted-state lookup; conditioning selection; smoothing selection; history-window selection; fallback selection; hierarchy selection; quantity selection; conversion-rule selection; probability generation; probability-record creation; split generation or execution; dataset construction; label joining; scoring; calibration; diagnostics; claims; evidence-gate evaluation; persistence; schemas; migrations; reports; exports; services; providers; scheduling; background work; simulation; paper trading; trading; order placement; production runtime behavior; autonomy.

## Approval decision options

Exact decision options:

1. `approve_later_baseline_contracts_implementation_ticket`
2. `request_approval_request_revision`
3. `hold`
4. `block`

## Current request status

`request_prepared_implementation_not_approved`

## Human decision and separate-approval boundary

Only a human may choose an approval decision option. This document does not approve `WEATHER-BOT-STAGE3-BASELINE-CONTRACTS-IMPLEMENTATION-01`.

The only approved next ticket after separate human approval is `WEATHER-BOT-STAGE3-BASELINE-CONTRACTS-IMPLEMENTATION-01`.

## Machine-checkable assignments

ticket_id: `WEATHER-BOT-STAGE3-BASELINE-CONTRACTS-IMPLEMENTATION-APPROVAL-REQUEST-01`
canonical_id: `WEATHER-BOT-STAGE3-BASELINE-CONTRACTS-IMPLEMENTATION-APPROVAL-REQUEST-01`
actual_pr_370_merge_sha: `c07cef21809e80be7cc8d0bfd81d1d97e809b3bf`
base_sha: `c07cef21809e80be7cc8d0bfd81d1d97e809b3bf`
current_request_status: `request_prepared_implementation_not_approved`
future_ticket: `WEATHER-BOT-STAGE3-BASELINE-CONTRACTS-IMPLEMENTATION-01`
future_file_scope: `meg/weather/stage3/baseline_contracts.py`, `tests/core/test_weather_bot_stage3_baseline_contracts.py`
public_symbols: `BaselineType, BaselineDefinitionStatus, BaselineValidationSeverity, BaselineValidationCode, BaselineContractDefinition, BaselineContractValidationResult, baseline_contract_definition_from_mapping, validate_baseline_contract_definition`
definition_field_count: `49`
required_mapping_key_count: `48`
optional_mapping_key_count: `1`
validation_code_count: `26`
decision_options: `approve_later_baseline_contracts_implementation_ticket`, `request_approval_request_revision`, `hold`, `block`

## Acceptance criteria

Acceptance requires exactly this approval-request document, its standard-library-only static test, and the canonical ID allowlist update. The approval request must remain approval-request-only, preserve exact future two-file implementation scope, preserve the eight-symbol public API, preserve the 49-field immutable definition, preserve the 26-code validation boundary, preserve climatology/persistence separation, preserve point-in-time and split-parity posture, and preserve explicit non-approvals.
