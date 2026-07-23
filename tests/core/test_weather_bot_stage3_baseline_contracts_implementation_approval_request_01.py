"""Static tests for Weather Bot Stage 3 baseline contracts implementation approval request."""
from __future__ import annotations

import ast
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DOC_PATH = REPO_ROOT / "docs/prd/WEATHER-BOT-STAGE3-BASELINE-CONTRACTS-IMPLEMENTATION-APPROVAL-REQUEST-01.md"
ALLOWLIST_PATH = REPO_ROOT / "tests/core/canonical_id_allowlist.py"
SELF_PATH = Path(__file__).resolve()
CANONICAL_ID = "WEATHER-BOT-STAGE3-BASELINE-CONTRACTS-IMPLEMENTATION-APPROVAL-REQUEST-01"
ACTUAL_PR_370_MERGE_SHA = "c07cef21809e80be7cc8d0bfd81d1d97e809b3bf"
BASE_SHA = "c07cef21809e80be7cc8d0bfd81d1d97e809b3bf"
EXPECTED_DOC = '# WEATHER-BOT-STAGE3-BASELINE-CONTRACTS-IMPLEMENTATION-APPROVAL-REQUEST-01\n\nCanonical ID: WEATHER-BOT-STAGE3-BASELINE-CONTRACTS-IMPLEMENTATION-APPROVAL-REQUEST-01\n\n## Status and scope\n\nThis approval request is docs/static-test-only and approval-request-only for `WEATHER-BOT-STAGE3-BASELINE-CONTRACTS-IMPLEMENTATION-APPROVAL-REQUEST-01`. Current request status is exactly `request_prepared_implementation_not_approved`.\n\nIt does not implement baseline contracts, calculate climatology, calculate persistence, generate probabilities, create probability records, score records, persist data, add runtime behavior, approve trading, or approve autonomy.\n\n## Immediate predecessor and merge verification\n\nPR #370 is recorded as merged by actual merge commit `ACTUAL_PR_370_MERGE_SHA = c07cef21809e80be7cc8d0bfd81d1d97e809b3bf`. The recorded implementation head `27d09b3691cc1f243a2eeb197811c7e72af09b01` is an ancestor of that actual merge commit, and that actual merge commit is the recorded base for this branch.\n\n`BASE_SHA = c07cef21809e80be7cc8d0bfd81d1d97e809b3bf`.\n\nThe preview merge SHA for PR #370 is not used.\n\n## Approval-request purpose and decision boundary\n\nThis document asks humans whether a later implementation ticket may create the baseline-contracts module and its focused test. It is not that implementation ticket and does not approve implementation by itself.\n\nA later implementation may proceed only after a separate human approval and a separate PR for `WEATHER-BOT-STAGE3-BASELINE-CONTRACTS-IMPLEMENTATION-01`.\n\n## Planning-contract basis\n\nThe authoritative basis is `docs/prd/WEATHER-BOT-STAGE3-BASELINE-CONTRACTS-PLANNING-01.md`, reconciled with the Stage 3 probability-record contract, strict OOS split contract, strict OOS implementation approval request, `meg/weather/stage3/binary_probability_record.py`, `meg/weather/stage3/strict_oos_split.py`, and their focused tests.\n\nThe baseline planning contract remains authoritative. This request invents no numeric history window, smoothing constant, sample minimum, sufficiency threshold, fallback hierarchy value, persisted quantity, conversion formula, fold count, cutoff duration, or metric threshold.\n\n## Requested implementation slice identity\n\nRequested later slice: immutable caller-supplied baseline definitions and pure fail-closed validation only.\n\nThe slice may validate definitions but must not calculate climatology, calculate persistence, inspect historical data, select conditioning dimensions, select smoothing, select a history window, select a fallback, select a persisted quantity, select a conversion rule, generate a probability, create a probability record, execute a split, score a record, join labels, create diagnostics, create claims, persist anything, generate reports, or add runtime behavior.\n\n## Exact future changed-file matrix\n\nA separately approved later implementation ticket may create exactly these two files:\n\n1. `meg/weather/stage3/baseline_contracts.py`\n2. `tests/core/test_weather_bot_stage3_baseline_contracts.py`\n\nNo existing file may be modified by that later implementation ticket.\n\n## Exact future public-symbol matrix\n\nFreeze exactly eight public symbols, in this order:\n\n1. `BaselineType`\n2. `BaselineDefinitionStatus`\n3. `BaselineValidationSeverity`\n4. `BaselineValidationCode`\n5. `BaselineContractDefinition`\n6. `BaselineContractValidationResult`\n7. `baseline_contract_definition_from_mapping`\n8. `validate_baseline_contract_definition`\n\nNo collection validator is approved. No additional public class or function is approved.\n\n## Exact enum matrix\n\nUse `StrEnum`.\n\nBaselineType:\n1. `CLIMATOLOGY = "climatology"`\n2. `PERSISTENCE = "persistence"`\n\nBaselineDefinitionStatus:\n1. `ACTIVE = "active"`\n2. `BLOCKED = "blocked"`\n\nBaselineValidationSeverity:\n1. `PASSED = "passed"`\n2. `BLOCKED = "blocked"`\n\n## Exact future definition-field matrix\n\nDefine later only if separately approved: `@dataclass(frozen=True)` `BaselineContractDefinition` with exact fields, types, order, and default posture:\n\n1. `baseline_definition_id: str`\n2. `baseline_type: BaselineType`\n3. `definition_status: BaselineDefinitionStatus`\n4. `baseline_version: str`\n5. `method_id: str`\n6. `method_version: str`\n7. `split_id: str`\n8. `split_version: str`\n9. `fold_id: str`\n10. `fold_index: int`\n11. `fold_cutoff: str`\n12. `prediction_as_of: str`\n13. `input_publication_available_at: str`\n14. `definition_declared_at: str`\n15. `condition_id: str`\n16. `token_id: str`\n17. `outcome: str`\n18. `settlement_rule_id: str`\n19. `settlement_rule_version: str`\n20. `source_compatibility_posture: str`\n21. `station_compatibility_posture: str`\n22. `threshold: str`\n23. `unit: str`\n24. `comparator: str`\n25. `measurement_window: str`\n26. `archive_finality_layer: str`\n27. `scoring_target_posture: str`\n28. `baseline_input_posture: str`\n29. `conditioning_dimensions: tuple[str, ...]`\n30. `smoothing_definition_id: str | None`\n31. `history_window_definition_id: str | None`\n32. `hierarchy_definition_id: str | None`\n33. `fallback_definition_id: str | None`\n34. `persisted_quantity_id: str | None`\n35. `conversion_rule_id: str | None`\n36. `split_parity_posture: str`\n37. `paired_comparison_posture: str`\n38. `availability_posture: str`\n39. `fallback_posture: str`\n40. `tuning_posture: str`\n41. `output_contract_posture: str`\n42. `market_price_posture: str`\n43. `baseline_execution_posture: str`\n44. `scoring_execution_posture: str`\n45. `storage_persistence_posture: str`\n46. `availability_evidence_refs: tuple[str, ...]`\n47. `provenance_refs: tuple[str, ...]`\n48. `exclusion_reason: str | None`\n49. `supersedes_baseline_definition_id: str | None = None`\n\nNo field value may be generated. No validation may occur in `__post_init__`. No mutable field or custom mutator is approved.\n\n## Exact validation-result matrix\n\nDefine later only if separately approved: `@dataclass(frozen=True)` `BaselineContractValidationResult` with exact fields:\n\n1. `severity: BaselineValidationSeverity`\n2. `passed: bool`\n3. `codes: tuple[BaselineValidationCode, ...] = ()`\n\nPassed invariant: severity is `PASSED`, passed is `True`, and codes is empty. Blocked invariant: severity is `BLOCKED`, passed is `False`, and codes is nonempty. The result may not contain a generated repair, baseline value, probability, record, score, diagnostic, claim, approval status, readiness status, or free-form message.\n\n## Exact mapping-input matrix\n\nFuture mapping signature:\n\n```python\ndef baseline_contract_definition_from_mapping(\n    mapping: object,\n) -> tuple[\n    BaselineContractDefinition | None,\n    BaselineContractValidationResult,\n]:\n```\n\nAccept only `isinstance(mapping, collections.abc.Mapping)`. A non-Mapping root or ordinary exception while snapshotting or reading the Mapping returns no definition, a blocked result, and exactly 48 repeated `MISSING_REQUIRED_FIELD` codes. Do not catch `BaseException`.\n\nFor a readable Mapping, code ordering begins with absent required keys in required-key order, unexpected exact built-in string keys in lexical order, remaining non-exact-string keys in original Mapping iteration order, then all present-value codes in direct-validation order. Aggregate every diagnosable present-value failure, skip only checks whose required inputs are absent or unusable, and never construct or return a partial definition.\n\n## Exact required and optional key matrix\n\nThe first 48 definition fields are required mapping keys. The only optional mapping key is `supersedes_baseline_definition_id`.\n\nRequired nullable mapping keys that must be explicitly present even when `None`: `smoothing_definition_id`, `history_window_definition_id`, `hierarchy_definition_id`, `fallback_definition_id`, `persisted_quantity_id`, `conversion_rule_id`, and `exclusion_reason`.\n\nAbsence is distinct from explicit `None`. No required field receives a default. A string-subclass key does not satisfy an exact required key and is also unexpected.\n\n## Exact fixed-posture matrix\n\nEach field must be an exact built-in string equal to its exact value:\n\n- `scoring_target_posture = "venue_defined_settlement_outcome"`\n- `split_parity_posture = "same_folds_cutoffs_eligibility_and_test_records_required"`\n- `paired_comparison_posture = "common_test_record_set_required"`\n- `availability_posture = "point_in_time_required"`\n- `fallback_posture = "predeclared_compatible_or_fail_closed"`\n- `tuning_posture = "train_or_calibration_only"`\n- `output_contract_posture = "probability_record_contract_required"`\n- `market_price_posture = "not_approved_as_baseline"`\n- `baseline_execution_posture = "not_approved"`\n- `scoring_execution_posture = "not_approved"`\n- `storage_persistence_posture = "not_approved"`\n\nAppend one `INVALID_FIXED_POSTURE` per invalid field in that order. A blank, non-string, or string-subclass fixed posture may receive both its text code and fixed-posture code.\n\n## Exact timestamp and no-lookahead matrix\n\nTimestamp parse order: `fold_cutoff`, `prediction_as_of`, `input_publication_available_at`, `definition_declared_at`.\n\nA valid timestamp requires an exact built-in nonblank string, `datetime.fromisoformat` success, non-`None` `tzinfo`, and non-`None` `utcoffset()`. Do not normalize stored strings and do not access current time.\n\nComparison codes, when prerequisites are valid, occur in this order: `INPUT_AVAILABLE_AFTER_PREDICTION`, `PREDICTION_AFTER_FOLD_CUTOFF`, `DEFINITION_DECLARED_AFTER_PREDICTION`. Equality passes.\n\n## Exact climatology matrix\n\nWhen `baseline_type is CLIMATOLOGY`, `baseline_input_posture` must equal `train_only_as_of_history`; `history_window_definition_id` must be an exact nonblank string; `conditioning_dimensions` may be empty or nonempty but must satisfy its exact tuple contract; `smoothing_definition_id`, `hierarchy_definition_id`, and `fallback_definition_id` may be `None` or exact nonblank strings; `persisted_quantity_id` and `conversion_rule_id` must be `None`.\n\nCode order: `CLIMATOLOGY_INVALID_INPUT_POSTURE`, `CLIMATOLOGY_MISSING_HISTORY_WINDOW`, `CLIMATOLOGY_PERSISTENCE_FIELDS_PRESENT`.\n\nA missing compatible fallback is not repaired here. `None` means future execution must fail closed if compatible conditioned history is unavailable. No numeric history window, smoothing value, hierarchy, fallback, or sample threshold is created.\n\n## Exact persistence matrix\n\nWhen `baseline_type is PERSISTENCE`, `baseline_input_posture` must equal `latest_legitimately_available_compatible_prior_state`; `conditioning_dimensions` must be empty; `smoothing_definition_id`, `history_window_definition_id`, `hierarchy_definition_id`, and `fallback_definition_id` must be `None`; `persisted_quantity_id` and `conversion_rule_id` must be exact nonblank strings.\n\nCode order: `PERSISTENCE_INVALID_INPUT_POSTURE`, `PERSISTENCE_CONDITIONING_FIELDS_PRESENT`, `PERSISTENCE_MISSING_QUANTITY`, `PERSISTENCE_MISSING_CONVERSION_RULE`.\n\nNo persisted quantity or conversion rule is selected, inferred, executed, or evaluated.\n\n## Exact definition-status matrix\n\nFor `ACTIVE`, `exclusion_reason` must be `None`; otherwise append `ACTIVE_WITH_EXCLUSION_REASON`.\n\nFor `BLOCKED`, an explicitly present exclusion reason must be an exact nonblank string; otherwise append `BLOCKED_WITHOUT_EXCLUSION_REASON`. For mapping input, do not append a dependent status code when the required exclusion key is absent; the missing-field code is sufficient.\n\nAppend `SELF_SUPERSESSION` exactly once only when both definition identifiers are exact nonblank strings and `supersedes_baseline_definition_id == baseline_definition_id`. No predecessor identity is generated.\n\n## Exact validation-code matrix\n\nExact members, values, and order:\n\n1. `MISSING_REQUIRED_FIELD = "missing_required_field"`\n2. `UNEXPECTED_FIELD = "unexpected_field"`\n3. `BLANK_REQUIRED_TEXT = "blank_required_text"`\n4. `INVALID_BASELINE_TYPE = "invalid_baseline_type"`\n5. `INVALID_DEFINITION_STATUS = "invalid_definition_status"`\n6. `INVALID_INTEGER_FIELD = "invalid_integer_field"`\n7. `INVALID_FIXED_POSTURE = "invalid_fixed_posture"`\n8. `INVALID_TIMESTAMP = "invalid_timestamp"`\n9. `INPUT_AVAILABLE_AFTER_PREDICTION = "input_available_after_prediction"`\n10. `PREDICTION_AFTER_FOLD_CUTOFF = "prediction_after_fold_cutoff"`\n11. `DEFINITION_DECLARED_AFTER_PREDICTION = "definition_declared_after_prediction"`\n12. `INVALID_CONDITIONING_DIMENSIONS = "invalid_conditioning_dimensions"`\n13. `EMPTY_AVAILABILITY_EVIDENCE_REFS = "empty_availability_evidence_refs"`\n14. `INVALID_AVAILABILITY_EVIDENCE_REF = "invalid_availability_evidence_ref"`\n15. `EMPTY_PROVENANCE_REFS = "empty_provenance_refs"`\n16. `INVALID_PROVENANCE_REF = "invalid_provenance_ref"`\n17. `CLIMATOLOGY_INVALID_INPUT_POSTURE = "climatology_invalid_input_posture"`\n18. `CLIMATOLOGY_MISSING_HISTORY_WINDOW = "climatology_missing_history_window"`\n19. `CLIMATOLOGY_PERSISTENCE_FIELDS_PRESENT = "climatology_persistence_fields_present"`\n20. `PERSISTENCE_INVALID_INPUT_POSTURE = "persistence_invalid_input_posture"`\n21. `PERSISTENCE_CONDITIONING_FIELDS_PRESENT = "persistence_conditioning_fields_present"`\n22. `PERSISTENCE_MISSING_QUANTITY = "persistence_missing_quantity"`\n23. `PERSISTENCE_MISSING_CONVERSION_RULE = "persistence_missing_conversion_rule"`\n24. `ACTIVE_WITH_EXCLUSION_REASON = "active_with_exclusion_reason"`\n25. `BLOCKED_WITHOUT_EXCLUSION_REASON = "blocked_without_exclusion_reason"`\n26. `SELF_SUPERSESSION = "self_supersession"`\n\nNo custom or dynamically generated validation code is permitted.\n\n## Exact validation-order contract\n\nFuture direct signature:\n\n```python\ndef validate_baseline_contract_definition(\n    definition: BaselineContractDefinition,\n) -> BaselineContractValidationResult:\n```\n\nExact code order: required and supplied-nullable `BLANK_REQUIRED_TEXT`; `INVALID_BASELINE_TYPE`; `INVALID_DEFINITION_STATUS`; `INVALID_INTEGER_FIELD`; fixed-posture codes; timestamp codes; temporal comparison codes; `INVALID_CONDITIONING_DIMENSIONS`; availability-evidence codes; provenance codes; climatology or persistence codes; definition-status consistency codes; `SELF_SUPERSESSION`.\n\nRepeated codes remain repeated. No final sorting, filtering, insertion, removal, set conversion, or deduplication is permitted.\n\n## Exact future test matrix\n\nRequire independent exact expectations for public surface order, all enum matrices, all 26 validation codes, all 49 definition fields, all three result fields, both public signatures, private key/text/timestamp/fixed-posture tuples, non-Mapping and hostile-Mapping roots, every missing key, unexpected-key ordering, string-subclass keys, text fields, enum adaptation and direct rejection, fold-index defects, fixed posture defects, timestamp defects and prerequisite suppression, temporal boundaries, conditioning, evidence, provenance, climatology rules, persistence rules, status consistency, supersession, combined mapping code order, no partial definition, frozen inputs and outputs, deterministic repeated calls, canonical routing, and absence of baseline calculation, probability creation, scoring, I/O, persistence, reports, runtime behavior, simulation, or trading.\n\nUse complete tuple equality. Do not use membership-only, sets, or sorted-result substitutions.\n\n## Dependency and import boundary\n\nThe later implementation may use only Python standard-library imports needed for pure contract validation, such as `collections.abc.Mapping`, `dataclasses.dataclass`, `datetime.datetime`, and `enum.StrEnum`.\n\nIt must not add dependencies, workflows, configuration, schemas, migrations, fixtures, datasets, generated files, services, providers, network access, database access, dynamic imports, or package initialization changes.\n\n## Canonical routing and target boundary\n\nCanonical routing remains exactly:\n\n- `condition_id`\n- `token_id`\n- `outcome`\n\nThe non-routing `market_id` identifier remains non-routing. The derived token/outcome identifier remains derived only. Neither is a public input field of the future production module.\n\n## Point-in-time, split-parity, and paired-comparison boundary\n\nThe future definition must preserve point-in-time availability, fold cutoff, prediction as-of, declaration time, availability evidence, strict OOS split identity, fold identity, split parity, and paired-comparison posture.\n\nBaseline definitions must remain aligned to the same folds, cutoffs, eligibility, and test records as the candidate path and must fail closed when compatible information is unavailable.\n\n## Explicit future implementation non-goals\n\nThis approval request explicitly denies approval for: baseline calculation; climatology estimation; persistence calculation; history lookup; persisted-state lookup; conditioning selection; smoothing selection; history-window selection; fallback selection; hierarchy selection; quantity selection; conversion-rule selection; probability generation; probability-record creation; split generation or execution; dataset construction; label joining; scoring; calibration; diagnostics; claims; evidence-gate evaluation; persistence; schemas; migrations; reports; exports; services; providers; scheduling; background work; simulation; paper trading; trading; order placement; production runtime behavior; autonomy.\n\n## Approval decision options\n\nExact decision options:\n\n1. `approve_later_baseline_contracts_implementation_ticket`\n2. `request_approval_request_revision`\n3. `hold`\n4. `block`\n\n## Current request status\n\n`request_prepared_implementation_not_approved`\n\n## Human decision and separate-approval boundary\n\nOnly a human may choose an approval decision option. This document does not approve `WEATHER-BOT-STAGE3-BASELINE-CONTRACTS-IMPLEMENTATION-01`.\n\nThe only approved next ticket after separate human approval is `WEATHER-BOT-STAGE3-BASELINE-CONTRACTS-IMPLEMENTATION-01`.\n\n## Machine-checkable assignments\n\nticket_id: `WEATHER-BOT-STAGE3-BASELINE-CONTRACTS-IMPLEMENTATION-APPROVAL-REQUEST-01`\ncanonical_id: `WEATHER-BOT-STAGE3-BASELINE-CONTRACTS-IMPLEMENTATION-APPROVAL-REQUEST-01`\nactual_pr_370_merge_sha: `c07cef21809e80be7cc8d0bfd81d1d97e809b3bf`\nbase_sha: `c07cef21809e80be7cc8d0bfd81d1d97e809b3bf`\ncurrent_request_status: `request_prepared_implementation_not_approved`\nfuture_ticket: `WEATHER-BOT-STAGE3-BASELINE-CONTRACTS-IMPLEMENTATION-01`\nfuture_file_scope: `meg/weather/stage3/baseline_contracts.py`, `tests/core/test_weather_bot_stage3_baseline_contracts.py`\npublic_symbols: `BaselineType, BaselineDefinitionStatus, BaselineValidationSeverity, BaselineValidationCode, BaselineContractDefinition, BaselineContractValidationResult, baseline_contract_definition_from_mapping, validate_baseline_contract_definition`\ndefinition_field_count: `49`\nrequired_mapping_key_count: `48`\noptional_mapping_key_count: `1`\nvalidation_code_count: `26`\ndecision_options: `approve_later_baseline_contracts_implementation_ticket`, `request_approval_request_revision`, `hold`, `block`\n\n## Acceptance criteria\n\nAcceptance requires exactly this approval-request document, its standard-library-only static test, and the canonical ID allowlist update. The approval request must remain approval-request-only, preserve exact future two-file implementation scope, preserve the eight-symbol public API, preserve the 49-field immutable definition, preserve the 26-code validation boundary, preserve climatology/persistence separation, preserve point-in-time and split-parity posture, and preserve explicit non-approvals.\n'
EXPECTED_HEADINGS = [
    "Status and scope",
    "Immediate predecessor and merge verification",
    "Approval-request purpose and decision boundary",
    "Planning-contract basis",
    "Requested implementation slice identity",
    "Exact future changed-file matrix",
    "Exact future public-symbol matrix",
    "Exact enum matrix",
    "Exact future definition-field matrix",
    "Exact validation-result matrix",
    "Exact mapping-input matrix",
    "Exact required and optional key matrix",
    "Exact fixed-posture matrix",
    "Exact timestamp and no-lookahead matrix",
    "Exact climatology matrix",
    "Exact persistence matrix",
    "Exact definition-status matrix",
    "Exact validation-code matrix",
    "Exact validation-order contract",
    "Exact future test matrix",
    "Dependency and import boundary",
    "Canonical routing and target boundary",
    "Point-in-time, split-parity, and paired-comparison boundary",
    "Explicit future implementation non-goals",
    "Approval decision options",
    "Current request status",
    "Human decision and separate-approval boundary",
    "Machine-checkable assignments",
    "Acceptance criteria",
]
EXPECTED_FUTURE_FILES = ["meg/weather/stage3/baseline_contracts.py", "tests/core/test_weather_bot_stage3_baseline_contracts.py"]
EXPECTED_PUBLIC_SYMBOLS = ["BaselineType", "BaselineDefinitionStatus", "BaselineValidationSeverity", "BaselineValidationCode", "BaselineContractDefinition", "BaselineContractValidationResult", "baseline_contract_definition_from_mapping", "validate_baseline_contract_definition"]
EXPECTED_CODES = ["MISSING_REQUIRED_FIELD", "UNEXPECTED_FIELD", "BLANK_REQUIRED_TEXT", "INVALID_BASELINE_TYPE", "INVALID_DEFINITION_STATUS", "INVALID_INTEGER_FIELD", "INVALID_FIXED_POSTURE", "INVALID_TIMESTAMP", "INPUT_AVAILABLE_AFTER_PREDICTION", "PREDICTION_AFTER_FOLD_CUTOFF", "DEFINITION_DECLARED_AFTER_PREDICTION", "INVALID_CONDITIONING_DIMENSIONS", "EMPTY_AVAILABILITY_EVIDENCE_REFS", "INVALID_AVAILABILITY_EVIDENCE_REF", "EMPTY_PROVENANCE_REFS", "INVALID_PROVENANCE_REF", "CLIMATOLOGY_INVALID_INPUT_POSTURE", "CLIMATOLOGY_MISSING_HISTORY_WINDOW", "CLIMATOLOGY_PERSISTENCE_FIELDS_PRESENT", "PERSISTENCE_INVALID_INPUT_POSTURE", "PERSISTENCE_CONDITIONING_FIELDS_PRESENT", "PERSISTENCE_MISSING_QUANTITY", "PERSISTENCE_MISSING_CONVERSION_RULE", "ACTIVE_WITH_EXCLUSION_REASON", "BLOCKED_WITHOUT_EXCLUSION_REASON", "SELF_SUPERSESSION"]
EXPECTED_DECISIONS = ["approve_later_baseline_contracts_implementation_ticket", "request_approval_request_revision", "hold", "block"]
NEW_ALLOWLIST_PATHS = {
    "docs/prd/WEATHER-BOT-STAGE3-BASELINE-CONTRACTS-IMPLEMENTATION-APPROVAL-REQUEST-01.md": None,
    "tests/core/test_weather_bot_stage3_baseline_contracts_implementation_approval_request_01.py": None,
}


def _read_doc() -> str:
    return DOC_PATH.read_text(encoding="utf-8")


def _section(text: str, heading: str) -> str:
    match = re.search(rf"^## {re.escape(heading)}\n(?P<body>.*?)(?=^## |\Z)", text, re.M | re.S)
    assert match, heading
    return match.group("body")


def _validate_complete(text: str) -> None:
    assert text == EXPECTED_DOC
    assert text.startswith(f"# {CANONICAL_ID}\n\nCanonical ID: {CANONICAL_ID}\n")
    assert ACTUAL_PR_370_MERGE_SHA in text
    assert BASE_SHA in text
    assert [line[3:] for line in text.splitlines() if line.startswith("## ")] == EXPECTED_HEADINGS


def _validate_files(text: str) -> None:
    body = _section(text, "Exact future changed-file matrix")
    assert [re.search(r"`([^`]+)`", line).group(1) for line in body.splitlines() if re.match(r"\d+\. `", line)] == EXPECTED_FUTURE_FILES


def _validate_symbols(text: str) -> None:
    body = _section(text, "Exact future public-symbol matrix")
    assert [re.search(r"`([^`]+)`", line).group(1) for line in body.splitlines() if re.match(r"\d+\. `", line)] == EXPECTED_PUBLIC_SYMBOLS


def _validate_codes(text: str) -> None:
    body = _section(text, "Exact validation-code matrix")
    assert [re.search(r"`([A-Z0-9_]+) =", line).group(1) for line in body.splitlines() if re.match(r"\d+\. `", line)] == EXPECTED_CODES


def _validate_decisions(text: str) -> None:
    body = _section(text, "Approval decision options")
    assert [re.search(r"`([^`]+)`", line).group(1) for line in body.splitlines() if re.match(r"\d+\. `", line)] == EXPECTED_DECISIONS


def _validate_matrices(text: str) -> None:
    for value in EXPECTED_FUTURE_FILES + EXPECTED_PUBLIC_SYMBOLS + EXPECTED_CODES + EXPECTED_DECISIONS:
        assert value in text
    assert "definition_field_count: `49`" in text
    assert "required_mapping_key_count: `48`" in text
    assert "optional_mapping_key_count: `1`" in text
    assert "validation_code_count: `26`" in text
    assert "request_prepared_implementation_not_approved" in text
    assert "baseline_definition_id: str" in text
    assert "supersedes_baseline_definition_id: str | None = None" in text


def test_complete_document_literal_and_structural_oracles() -> None:
    text = _read_doc()
    _validate_complete(text)
    _validate_symbols(text)
    _validate_codes(text)
    _validate_decisions(text)
    _validate_matrices(text)


def test_every_section_insertion_deletion_and_replacement_mutation_rejected() -> None:
    text = _read_doc()
    for heading in EXPECTED_HEADINGS:
        inserted = text.replace(f"## {heading}\n", f"## {heading}\ninserted mutation\n", 1)
        deleted = re.sub(rf"^## {re.escape(heading)}\n.*?(?=^## |\Z)", "", text, count=1, flags=re.M | re.S)
        replaced = re.sub(rf"^## {re.escape(heading)}\n.*?(?=^## |\Z)", f"## {heading}\n\nreplacement mutation\n\n", text, count=1, flags=re.M | re.S)
        for mutated in (inserted, deleted, replaced):
            try:
                _validate_complete(mutated)
            except AssertionError:
                pass
            else:
                raise AssertionError(heading)


def test_structural_mutations_are_rejected_by_dedicated_section_and_complete_validation() -> None:
    mutations = [
        ("Exact future public-symbol matrix", "BaselineType", "BaselineTypeChanged", _validate_symbols),
        ("Exact validation-code matrix", "`MISSING_REQUIRED_FIELD = \"missing_required_field\"`", "`MISSING_FIELD = \"missing_required_field\"`", _validate_codes),
        ("Approval decision options", "`hold`", "`defer`", _validate_decisions),
        ("Machine-checkable assignments", "definition_field_count: `49`", "definition_field_count: `48`", _validate_matrices),
        ("Exact future changed-file matrix", "meg/weather/stage3/baseline_contracts.py", "meg/weather/stage3/other.py", _validate_files),
    ]
    text = _read_doc()
    for _heading, old, new, validator in mutations:
        mutated = text.replace(old, new, 1)
        for check in (validator, _validate_complete):
            try:
                check(mutated)
            except AssertionError:
                pass
            else:
                raise AssertionError(old)


def test_static_test_oracles_are_literal_and_no_forbidden_runtime_behavior() -> None:
    source = SELF_PATH.read_text(encoding="utf-8")
    tree = ast.parse(source)
    forbidden_calls = ('open', 'exec', 'eval', 'compile', '__import__')
    forbidden_import_roots = ('os', 'subprocess', 'socket', 'sqlite3', 'duckdb', 'requests', 'urllib', 'importlib')
    assignments = ('EXPECTED_DOC', 'EXPECTED_HEADINGS', 'EXPECTED_FUTURE_FILES', 'EXPECTED_PUBLIC_SYMBOLS', 'EXPECTED_CODES', 'EXPECTED_DECISIONS', 'NEW_ALLOWLIST_PATHS')
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            names = [alias.name.split(".")[0] for alias in getattr(node, "names", [])]
            if isinstance(node, ast.ImportFrom) and node.module:
                names.append(node.module.split(".")[0])
            assert not (set(names) & set(forbidden_import_roots))
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            assert node.func.id not in forbidden_calls
        if isinstance(node, ast.Assign):
            targets = [target.id for target in node.targets if isinstance(target, ast.Name)]
            for target in targets:
                if target in assignments:
                    assert isinstance(node.value, (ast.Constant, ast.List, ast.Set, ast.Dict))
                    for child in ast.walk(node.value):
                        assert not isinstance(child, (ast.BinOp, ast.JoinedStr, ast.Call, ast.Name))


def test_allowlist_contains_new_paths_once_with_observed_counts() -> None:
    allowlist_source = ALLOWLIST_PATH.read_text(encoding="utf-8")
    tree = ast.parse(allowlist_source)
    observed = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Dict):
            for key, value in zip(node.keys, node.values):
                if isinstance(key, ast.Constant) and isinstance(key.value, str) and key.value in NEW_ALLOWLIST_PATHS:
                    assert isinstance(value, ast.Constant) and isinstance(value.value, int)
                    observed[key.value] = observed.get(key.value, []) + [value.value]
    assert set(observed) == set(NEW_ALLOWLIST_PATHS)
    for rel_path, values in observed.items():
        assert len(values) == 1
        actual = sum(1 for line in (REPO_ROOT / rel_path).read_text(encoding="utf-8").splitlines() if "market_id" in line)
        assert values[0] == actual
