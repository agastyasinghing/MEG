"""Static tests for Weather Bot Stage 3 evaluation result record contract planning."""
from __future__ import annotations

import ast
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DOC_PATH = REPO_ROOT / "docs/prd/WEATHER-BOT-STAGE3-EVALUATION-RESULT-RECORD-CONTRACT-PLANNING-01.md"
ALLOWLIST_PATH = REPO_ROOT / "tests/core/canonical_id_allowlist.py"
TEST_PATH = Path(__file__).resolve()
TITLE = 'WEATHER-BOT-STAGE3-EVALUATION-RESULT-RECORD-CONTRACT-PLANNING-01'
CANONICAL_ID = TITLE
MERGE_COMMIT = "1073494197c5c2e527ee1e8c5b2b66a2dfbb96e6"
PREVIEW_MERGE_SHA = "d33a247d730b3358be92d2fc0e983a34aabecc3b"
SUCCESSOR = "WEATHER-BOT-STAGE3-EVALUATION-CLAIM-CONTRACT-PLANNING-01"
HEADINGS = ['Status and scope', 'Immediate predecessor and merge verification', 'Contract purpose and result boundary', 'Upstream contract dependencies', 'Exact evaluation result-kind matrix', 'Exact result-support status matrix', 'Common result-record requirements', 'Scalar score result requirements', 'Calibration and decomposition result requirements', 'Distribution and ensemble diagnostic result requirements', 'Paired comparison result requirements', 'Scope identity and sample accounting', 'Uncertainty and support-status requirements', 'Exclusion block and missingness requirements', 'Identity provenance and immutability', 'Claim separation and interpretation boundaries', 'Fail-closed requirements', 'Explicit non-approvals', 'Canonical routing posture', 'Recommended next ticket', 'Machine-checkable assignments', 'Acceptance criteria']
EXPECTED_RESULT_KIND_MATRIX = [['Result kind', 'Applies to', 'Required result content', 'Required linkage', 'Fail-closed boundary'], ['---', '---', '---', '---', '---'], ['scalar_score_result', 'brier_score, log_score, crps, threshold_weighted_crps', 'one metric identity and version, one result value, direction, sample accounting, and uncertainty or support posture as applicable', 'method role and version, representation, split, fold, cutoff, paired test-record set, aggregation, weighting, and stratum', 'block when applicability, result domain, linkage, provenance, or sample accounting is invalid'], ['calibration_bin_result', 'reliability_diagram', 'ordered predeclared bin identity, boundary policy, sample count, mean predicted probability, observed outcome frequency, and uncertainty or support status', 'reliability definition and version, method identity, split scope, paired test-record set, aggregation, weighting, and stratum', 'block when bin policy, ordering, compatible support, or required linkage is absent'], ['decomposition_result', 'brier_decomposition', 'declared decomposition method and component values for reliability, resolution, and uncertainty with sample accounting', 'decomposition definition and version, method identity, binary representation, split scope, paired test-record set, aggregation, weighting, and stratum', 'block when the decomposition method, representation, support, or linkage is incompatible'], ['distribution_diagnostic_result', 'pit_histogram', 'declared PIT treatment, ordered bin definitions and counts, sample accounting, and uncertainty or support status', 'PIT definition and version, full-distribution representation, method identity, split scope, paired test-record set, aggregation, weighting, and stratum', 'block when PIT treatment, representation, ordered content, support, or linkage is incompatible'], ['ensemble_diagnostic_result', 'rank_histogram', 'declared tie treatment, ordered ranks or bins and counts, ensemble comparability, sample accounting, and uncertainty or support status', 'rank-histogram definition and version, ensemble representation, method identity, split scope, paired test-record set, aggregation, weighting, and stratum', 'block when members, tie treatment, ordered content, support, or linkage are incompatible'], ['paired_comparison_result', 'candidate versus climatology or persistence under one applicable proper score', 'candidate result identity, baseline result identity, comparison direction, paired comparison payload, and shared sample accounting', 'the same metric and version, representation, split, fold, cutoff, paired test-record set, aggregation, weighting, and stratum', 'block when the scope is not exactly paired or the baseline and scoring contracts are not satisfied']]
EXPECTED_SUPPORT_STATUS_MATRIX = [['Support status', 'Required meaning', 'Claim posture'], ['---', '---', '---'], ['supported', 'the result satisfies its upstream contracts and its predeclared sample-support rule', 'eligible only for later claim review; no claim is approved here'], ['insufficient', 'the result is otherwise contract-compatible but does not satisfy its predeclared sample-support rule', 'claim use is blocked'], ['blocked', 'a contract, compatibility, leakage, pairing, accounting, immutability, or provenance requirement failed', 'result is invalid for claims'], ['unavailable', 'a required permitted input or result artifact does not exist', 'no substitution, backfill, inference, or claim is allowed']]
EXPECTED_COMMON_FIELDS = ['evaluation_result_id', 'result_kind', 'artifact_id', 'artifact_version', 'evaluation_definition_id', 'evaluation_definition_version', 'evaluation_run_id', 'method_role', 'method_id', 'method_version', 'prediction_representation', 'target_posture', 'split_id', 'split_version', 'fold_id', 'cutoff_identity', 'paired_test_record_set_id', 'eligibility_policy_id', 'aggregation_rule_id', 'weighting_rule_id', 'stratum_id', 'eligible_record_count', 'excluded_record_count', 'blocked_record_count', 'total_considered_record_count', 'exclusion_block_reason_summary', 'uncertainty_method_id', 'uncertainty_level_id', 'support_status', 'result_payload', 'provenance', 'result_created_at', 'supersedes_result_id_when_applicable']
EXPECTED_CLOSED_SETS = {'weather bot planning stage': ['weather_bot_stage3_evaluation_result_record_contract_planning'], 'immediate predecessor pr': ['pr_362'], 'ticket lifecycle status': ['docs_static_test_only', 'contract_planning_only'], 'result record contract status': ['requirements_defined', 'runtime_schema_not_created', 'result_values_not_created'], 'scoring target posture': ['venue_defined_settlement_outcome'], 'result kind': ['scalar_score_result', 'calibration_bin_result', 'decomposition_result', 'distribution_diagnostic_result', 'ensemble_diagnostic_result', 'paired_comparison_result'], 'result support status': ['supported', 'insufficient', 'blocked', 'unavailable'], 'scope identity posture': ['exact_single_scope_required'], 'sample accounting posture': ['eligible_excluded_blocked_total_identity_required'], 'terminal category posture': ['mutually_exclusive_required'], 'exclusion block posture': ['explicit_reason_required'], 'uncertainty posture': ['predeclared_method_level_and_support_rule_required'], 'paired comparison posture': ['exact_common_test_record_set_required'], 'baseline comparison posture': ['climatology_or_persistence_only'], 'market price posture': ['not_approved_as_baseline_or_truth'], 'immutability posture': ['superseding_result_version_required'], 'claim posture': ['result_records_do_not_approve_claims'], 'result calculation posture': ['not_approved'], 'persistence posture': ['not_approved'], 'report export posture': ['not_approved'], 'canonical routing field': ['condition_id', 'token_id', 'outcome'], 'non routing field': ['market_id'], 'derived identifier field': ['token_outcome_pair'], 'next ticket recommendation': ['stage3_evaluation_claim_contract_planning'], 'evidence status': ['evaluation_result_record_contract_planning_recorded'], 'label confidence': ['confirmed']}
EXPECTED_ASSIGNMENTS = ['weather bot planning stage: weather_bot_stage3_evaluation_result_record_contract_planning', 'immediate predecessor pr: pr_362', 'ticket lifecycle status: docs_static_test_only', 'ticket lifecycle status: contract_planning_only', 'result record contract status: requirements_defined', 'result record contract status: runtime_schema_not_created', 'result record contract status: result_values_not_created', 'scoring target posture: venue_defined_settlement_outcome', 'result kind: scalar_score_result', 'result kind: calibration_bin_result', 'result kind: decomposition_result', 'result kind: distribution_diagnostic_result', 'result kind: ensemble_diagnostic_result', 'result kind: paired_comparison_result', 'result support status: supported', 'result support status: insufficient', 'result support status: blocked', 'result support status: unavailable', 'scope identity posture: exact_single_scope_required', 'sample accounting posture: eligible_excluded_blocked_total_identity_required', 'terminal category posture: mutually_exclusive_required', 'exclusion block posture: explicit_reason_required', 'uncertainty posture: predeclared_method_level_and_support_rule_required', 'paired comparison posture: exact_common_test_record_set_required', 'baseline comparison posture: climatology_or_persistence_only', 'market price posture: not_approved_as_baseline_or_truth', 'immutability posture: superseding_result_version_required', 'claim posture: result_records_do_not_approve_claims', 'result calculation posture: not_approved', 'persistence posture: not_approved', 'report export posture: not_approved', 'canonical routing field: condition_id', 'canonical routing field: token_id', 'canonical routing field: outcome', 'non routing field: market_id', 'derived identifier field: token_outcome_pair', 'next ticket recommendation: stage3_evaluation_claim_contract_planning', 'evidence status: evaluation_result_record_contract_planning_recorded', 'label confidence: confirmed']
NEW_ALLOWLIST_PATHS = {
    "docs/prd/WEATHER-BOT-STAGE3-EVALUATION-RESULT-RECORD-CONTRACT-PLANNING-01.md",
    "tests/core/test_weather_bot_stage3_evaluation_result_record_contract_planning_01.py",
}
FORBIDDEN_TERMS = ["@dataclass", "BaseModel", "CREATE TABLE", "ALTER TABLE", "json_schema", "persist_result", "calculate_score", "execute_evaluation", "write_report", "export_results", "production behavior is approved"]

def _read_doc(text: str | None = None) -> str:
    return DOC_PATH.read_text(encoding="utf-8") if text is None else text

def _sections(text: str) -> dict[str, str]:
    matches = list(re.finditer(r"^## (.+)$", text, re.MULTILINE))
    names = [m.group(1) for m in matches]
    assert names == HEADINGS
    assert len(names) == len(set(names))
    sections = {}
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        body = text[match.end():end].strip()
        assert body
        sections[match.group(1)] = body
    return sections

def _parse_table(section: str) -> list[list[str]]:
    rows = []
    for line in section.splitlines():
        if line.startswith("|"):
            rows.append([cell.strip() for cell in line.strip().strip("|").split("|")])
        elif rows and line.strip():
            break
    assert rows
    assert all(len(row) == len(rows[0]) for row in rows)
    return rows

def _parse_bullets(block: str) -> list[str]:
    output = []
    for line in block.splitlines():
        if line.startswith("- "):
            output.append(line[2:])
        elif output and line.strip():
            break
    return output

def _parse_closed_sets(section: str) -> dict[str, list[str]]:
    text = section.split("Declared closed sets:\n\n", 1)[1].split("\nActual assignments:", 1)[0]
    result = {}
    current = None
    for line in text.splitlines():
        if not line:
            continue
        if line.startswith("- ") and line.endswith(":"):
            current = line[2:-1]
            assert current not in result
            result[current] = []
        elif line.startswith("  - ") and current:
            value = line[4:]
            assert value not in result[current]
            result[current].append(value)
        else:
            raise AssertionError(f"malformed closed-set line: {line!r}")
    return result

def _parse_actual(section: str) -> list[str]:
    text = section.split("Actual assignments:\n\n", 1)[1].split("\n\nMissing, duplicate", 1)[0]
    assignments = []
    for line in text.splitlines():
        if not line:
            continue
        if not line.startswith("- ") or ": " not in line[2:]:
            raise AssertionError(f"malformed assignment line: {line!r}")
        assignments.append(line[2:])
    assert len(assignments) == len(set(assignments))
    return assignments

def _flatten(closed: dict[str, list[str]]) -> list[str]:
    return [f"{field}: {value}" for field, values in closed.items() for value in values]

def _market_id_line_count(path: Path) -> int:
    return sum(1 for line in path.read_text(encoding="utf-8").splitlines() if "market_id" in line)

def _allowlist() -> dict[str, int]:
    tree = ast.parse(ALLOWLIST_PATH.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.AnnAssign):
            if isinstance(node.target, ast.Name) and node.target.id == "ALLOWED_MARKET_ID_OCCURRENCE_LINES":
                value = node.value
                if isinstance(value, ast.Call):
                    value = value.args[0]
                return ast.literal_eval(value)
    raise AssertionError("allowlist assignment missing")

def _validate(text: str | None = None) -> None:
    doc = _read_doc(text)
    assert doc.startswith(f"# {TITLE}\n\nCanonical ID: {CANONICAL_ID}")
    sections = _sections(doc)
    assert _parse_table(sections["Exact evaluation result-kind matrix"]) == EXPECTED_RESULT_KIND_MATRIX
    assert _parse_table(sections["Exact result-support status matrix"]) == EXPECTED_SUPPORT_STATUS_MATRIX
    assert "No custom, hybrid, or additional support status is allowed." in sections["Exact result-support status matrix"]
    assert _parse_bullets(sections["Common result-record requirements"].split("Include exactly this ordered semantic-field list:\n\n", 1)[1]) == EXPECTED_COMMON_FIELDS
    closed = _parse_closed_sets(sections["Machine-checkable assignments"])
    assert list(closed) == list(EXPECTED_CLOSED_SETS)
    assert closed == EXPECTED_CLOSED_SETS
    assignments = _parse_actual(sections["Machine-checkable assignments"])
    assert assignments == EXPECTED_ASSIGNMENTS == _flatten(closed)
    assert "total_considered_record_count =\neligible_record_count + excluded_record_count + blocked_record_count" in sections["Scope identity and sample accounting"]
    assert "Immediate predecessor: pr_362." in sections["Immediate predecessor and merge verification"]
    assert f"ACTUAL_PR_362_MERGE_SHA: {MERGE_COMMIT}" in sections["Immediate predecessor and merge verification"]
    assert PREVIEW_MERGE_SHA in sections["Immediate predecessor and merge verification"]
    assert SUCCESSOR in sections["Recommended next ticket"]
    assert "- condition_id\n- token_id\n- outcome" in sections["Canonical routing posture"]
    assert "market_id is non-routing only." in sections["Canonical routing posture"]
    assert "token_outcome_pair is derived only." in sections["Canonical routing posture"]
    scoped = "\n".join(sections[name] for name in ["Scope identity and sample accounting", "Uncertainty and support-status requirements"])
    assert not re.search(r"\b(?:95%|0\.95|10|100|minimum of)\b", scoped)
    assert not any(term in doc for term in FORBIDDEN_TERMS)

def test_document_contract_is_exact() -> None:
    _validate()

def test_allowlist_counts_match_direct_observation_for_new_files() -> None:
    allowlist = _allowlist()
    assert set(allowlist) >= NEW_ALLOWLIST_PATHS
    for rel_path in NEW_ALLOWLIST_PATHS:
        assert allowlist[rel_path] == _market_id_line_count(REPO_ROOT / rel_path)

def test_parser_mutations_are_rejected() -> None:
    base = _read_doc()
    mutations = [
        base.replace("## Status and scope\n", "## Immediate predecessor and merge verification\n", 1),
        base.replace("one metric identity and version", "one changed identity and version", 1),
        base.replace("| paired_comparison_result |", "| scalar_score_result |", 1),
        base.replace("- evaluation_result_id\n- result_kind", "- result_kind\n- evaluation_result_id", 1),
        base.replace("- weather bot planning stage:\n", "- label confidence:\n", 1),
        base.replace("- label confidence: confirmed", "- label confidence: confirmed\n- label confidence: confirmed", 1),
        base.replace("- label confidence: confirmed", "- label confidence confirmed", 1),
        base.replace("| unavailable | a required permitted input", "| pending | a required permitted input", 1),
    ]
    for mutated in mutations:
        try:
            _validate(mutated)
        except AssertionError:
            continue
        raise AssertionError("mutation was not rejected")
