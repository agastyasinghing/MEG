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

Accept only `isinstance(mapping, collections.abc.Mapping)`. A non-Mapping root or ordinary exception while snapshotting or reading the Mapping returns no definition, a blocked result, and exactly 48 repeated `MISSING_REQUIRED_FIELD` codes. Do not catch `BaseException`.

For a readable Mapping, code ordering begins with absent required keys in required-key order, unexpected exact built-in string keys in lexical order, remaining non-exact-string keys in original Mapping iteration order, then all present-value codes in direct-validation order. Aggregate every diagnosable present-value failure, skip only checks whose required inputs are absent or unusable, and never construct or return a partial definition.

## Exact required and optional key matrix

The first 48 definition fields are required mapping keys. The only optional mapping key is `supersedes_baseline_definition_id`.

Required nullable mapping keys that must be explicitly present even when `None`: `smoothing_definition_id`, `history_window_definition_id`, `hierarchy_definition_id`, `fallback_definition_id`, `persisted_quantity_id`, `conversion_rule_id`, and `exclusion_reason`.

Absence is distinct from explicit `None`. No required field receives a default. A string-subclass key does not satisfy an exact required key and is also unexpected.

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

## Exact climatology matrix

When `baseline_type is CLIMATOLOGY`, `baseline_input_posture` must equal `train_only_as_of_history`; `history_window_definition_id` must be an exact nonblank string; `conditioning_dimensions` may be empty or nonempty but must satisfy its exact tuple contract; `smoothing_definition_id`, `hierarchy_definition_id`, and `fallback_definition_id` may be `None` or exact nonblank strings; `persisted_quantity_id` and `conversion_rule_id` must be `None`.

Code order: `CLIMATOLOGY_INVALID_INPUT_POSTURE`, `CLIMATOLOGY_MISSING_HISTORY_WINDOW`, `CLIMATOLOGY_PERSISTENCE_FIELDS_PRESENT`.

A missing compatible fallback is not repaired here. `None` means future execution must fail closed if compatible conditioned history is unavailable. No numeric history window, smoothing value, hierarchy, fallback, or sample threshold is created.

## Exact persistence matrix

When `baseline_type is PERSISTENCE`, `baseline_input_posture` must equal `latest_legitimately_available_compatible_prior_state`; `conditioning_dimensions` must be empty; `smoothing_definition_id`, `history_window_definition_id`, `hierarchy_definition_id`, and `fallback_definition_id` must be `None`; `persisted_quantity_id` and `conversion_rule_id` must be exact nonblank strings.

Code order: `PERSISTENCE_INVALID_INPUT_POSTURE`, `PERSISTENCE_CONDITIONING_FIELDS_PRESENT`, `PERSISTENCE_MISSING_QUANTITY`, `PERSISTENCE_MISSING_CONVERSION_RULE`.

No persisted quantity or conversion rule is selected, inferred, executed, or evaluated.

## Exact definition-status matrix

For `ACTIVE`, `exclusion_reason` must be `None`; otherwise append `ACTIVE_WITH_EXCLUSION_REASON`.

For `BLOCKED`, an explicitly present exclusion reason must be an exact nonblank string; otherwise append `BLOCKED_WITHOUT_EXCLUSION_REASON`. For mapping input, do not append a dependent status code when the required exclusion key is absent; the missing-field code is sufficient.

Append `SELF_SUPERSESSION` exactly once only when both definition identifiers are exact nonblank strings and `supersedes_baseline_definition_id == baseline_definition_id`. No predecessor identity is generated.

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

## Exact future test matrix

Require independent exact expectations for public surface order, all enum matrices, all 26 validation codes, all 49 definition fields, all three result fields, both public signatures, private key/text/timestamp/fixed-posture tuples, non-Mapping and hostile-Mapping roots, every missing key, unexpected-key ordering, string-subclass keys, text fields, enum adaptation and direct rejection, fold-index defects, fixed posture defects, timestamp defects and prerequisite suppression, temporal boundaries, conditioning, evidence, provenance, climatology rules, persistence rules, status consistency, supersession, combined mapping code order, no partial definition, frozen inputs and outputs, deterministic repeated calls, canonical routing, and absence of baseline calculation, probability creation, scoring, I/O, persistence, reports, runtime behavior, simulation, or trading.

Use complete tuple equality. Do not use membership-only, sets, or sorted-result substitutions.

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
