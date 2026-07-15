"""Static tests for Weather Bot Stage 3 evaluation claim contract planning."""
from __future__ import annotations

import ast
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DOC_PATH = REPO_ROOT / "docs/prd/WEATHER-BOT-STAGE3-EVALUATION-CLAIM-CONTRACT-PLANNING-01.md"
ALLOWLIST_PATH = REPO_ROOT / "tests/core/canonical_id_allowlist.py"
TITLE = "WEATHER-BOT-STAGE3-EVALUATION-CLAIM-CONTRACT-PLANNING-01"
CANONICAL_ID = TITLE
MERGE_COMMIT = "ba641e2b73cc5108b5506861e1924260d4516e1f"
PREVIEW_MERGE_SHA = "e7f7f68f824e419989d7b2a1780b87ac4113c805"
SUCCESSOR = "WEATHER-BOT-STAGE3-EVIDENCE-GATE-DECISION-RECORD-CONTRACT-PLANNING-01"
HEADINGS = ["Status and scope", "Immediate predecessor and merge verification", "Contract purpose and claim boundary", "Upstream result-record dependencies", "Exact evaluation claim-class matrix", "Exact claim-disposition matrix", "Common claim-record requirements", "Claim-rule predeclaration requirements", "Candidate-versus-climatology claim requirements", "Candidate-versus-persistence claim requirements", "Cross-baseline predictive-skill claim requirements", "Binary calibration claim requirements", "Distribution and ensemble diagnostic claim requirements", "Threshold-weighted and stratified claim requirements", "Multiple-testing and selection-control requirements", "Scope identity and result-set completeness", "Claim-disposition precedence and reason requirements", "Identity provenance and immutability", "Evidence-gate separation and interpretation boundaries", "Fail-closed requirements", "Explicit non-approvals", "Canonical routing posture", "Recommended next ticket", "Machine-checkable assignments", "Acceptance criteria"]
EXPECTED_CLAIM_CLASS_MATRIX = [['Claim class', 'Required immutable result records', 'Required scope or comparator', 'Allowed future conclusion', 'Forbidden inference'], ['---', '---', '---', '---', '---'], ['candidate_vs_climatology_predictive_skill', 'one or more predeclared paired_comparison_result records under applicable proper scores', 'candidate versus climatology under one exact paired scope', 'whether the predeclared candidate-versus-climatology claim rule is satisfied for the exact metrics and scope', 'overall superiority, calibration, economic edge, executability, implementation approval, or trading approval'], ['candidate_vs_persistence_predictive_skill', 'one or more predeclared paired_comparison_result records under applicable proper scores', 'candidate versus persistence under one exact paired scope', 'whether the predeclared candidate-versus-persistence claim rule is satisfied for the exact metrics and scope', 'overall superiority, calibration, economic edge, executability, implementation approval, or trading approval'], ['candidate_predictive_skill_across_required_baselines', 'the complete predeclared paired_comparison_result set against both climatology and persistence', 'identical candidate definition with both required baselines and compatible exact scopes', 'whether the predeclared cross-baseline predictive-skill rule is satisfied', 'universal superiority, robustness outside the declared scope, economic edge, executability, implementation approval, or trading approval'], ['binary_calibration_behavior', 'calibration_bin_result plus every compatible scalar_score_result or decomposition_result required by the predeclared claim rule', 'one compatible binary representation, split scope, aggregation, weighting, and stratum', 'whether the predeclared binary-calibration claim rule is satisfied for the exact scope', 'predictive-skill superiority, economic edge, executability, implementation approval, or trading approval'], ['distributional_calibration_behavior', 'distribution_diagnostic_result plus every compatible scalar_score_result required by the predeclared claim rule', 'one compatible full-distribution representation and exact scope', 'whether the predeclared distributional-calibration claim rule is satisfied', 'scalar-ranking superiority, economic edge, executability, implementation approval, or trading approval'], ['ensemble_calibration_behavior', 'ensemble_diagnostic_result and every supporting result required by the predeclared claim rule', 'one compatible finite-ensemble representation, tie treatment, and exact scope', 'whether the predeclared ensemble-calibration claim rule is satisfied', 'scalar-ranking superiority, economic edge, executability, implementation approval, or trading approval'], ['threshold_weighted_distribution_skill', 'paired_comparison_result under threshold_weighted_crps with its declared threshold-weight policy', 'one justified threshold-focused scope and approved climatology or persistence comparator', 'whether the predeclared threshold-weighted skill rule is satisfied for the exact threshold-focused scope', 'general predictive superiority, economic edge, executability, implementation approval, or trading approval'], ['stratum_specific_predictive_skill', 'the complete predeclared paired_comparison_result set for one exact supported stratum', 'one declared stratum and approved climatology or persistence comparator', 'whether the predeclared stratum-specific skill rule is satisfied', 'generalization beyond the stratum, post-hoc subgroup discovery, economic edge, executability, implementation approval, or trading approval']]
EXPECTED_DISPOSITION_MATRIX = [['Claim disposition', 'Required meaning', 'Evidence-gate posture'], ['---', '---', '---'], ['claim_supported', 'every required result is supported, the exact result set is complete, and the predeclared claim rule is satisfied', 'eligible only for a later evidence-gate decision; no gate passage is approved here'], ['claim_not_supported', 'every required result is supported and complete but the predeclared claim rule is not satisfied', 'evidence-gate support from this claim is absent'], ['claim_insufficient', 'no blocking or unavailable condition applies, but one or more required results or the claim-level support rule is insufficient', 'evidence-gate use is blocked'], ['claim_blocked', 'a required result is blocked or a contract, leakage, scope, selection, accounting, immutability, or provenance requirement failed', 'claim is invalid for evidence-gate use'], ['claim_unavailable', 'no blocking condition applies, but one or more required permitted result records do not exist or are unavailable', 'no substitution, inference, backfill, or evidence-gate use is allowed']]
EXPECTED_COMMON_FIELDS = ['evaluation_claim_id', 'claim_class', 'claim_rule_id', 'claim_rule_version', 'claim_disposition', 'claim_disposition_reason', 'target_posture', 'candidate_method_id', 'candidate_method_version', 'baseline_type_when_applicable', 'baseline_method_id_when_applicable', 'baseline_method_version_when_applicable', 'prediction_representation', 'metric_or_diagnostic_ids', 'metric_or_diagnostic_versions', 'required_evaluation_result_ids', 'observed_evaluation_result_ids', 'missing_evaluation_result_ids', 'split_id', 'split_version', 'fold_scope', 'cutoff_scope', 'paired_test_record_set_id', 'aggregation_rule_id', 'weighting_rule_id', 'stratum_id_when_applicable', 'uncertainty_policy_id', 'sample_support_rule_id', 'selection_control_policy_id', 'multiple_comparison_policy_id_when_applicable', 'evidence_gate_eligibility_posture', 'provenance', 'claim_created_at', 'supersedes_claim_id_when_applicable']
EXPECTED_PRECEDENCE = ['claim_blocked', 'claim_unavailable', 'claim_insufficient', 'evaluate the predeclared rule as claim_supported or claim_not_supported']
EXPECTED_CLOSED_SETS = {'weather bot planning stage': ['weather_bot_stage3_evaluation_claim_contract_planning'], 'immediate predecessor pr': ['pr_363'], 'ticket lifecycle status': ['docs_static_test_only', 'contract_planning_only'], 'claim contract status': ['requirements_defined', 'claim_records_not_created', 'claim_decisions_not_created'], 'scoring target posture': ['venue_defined_settlement_outcome'], 'claim class': ['candidate_vs_climatology_predictive_skill', 'candidate_vs_persistence_predictive_skill', 'candidate_predictive_skill_across_required_baselines', 'binary_calibration_behavior', 'distributional_calibration_behavior', 'ensemble_calibration_behavior', 'threshold_weighted_distribution_skill', 'stratum_specific_predictive_skill'], 'claim disposition': ['claim_supported', 'claim_not_supported', 'claim_insufficient', 'claim_blocked', 'claim_unavailable'], 'disposition precedence': ['blocked_then_unavailable_then_insufficient_then_rule_evaluation'], 'result dependency posture': ['immutable_evaluation_result_records_required'], 'claim rule posture': ['predeclared_versioned_exact_scope_required'], 'result completeness posture': ['exact_required_result_list_required'], 'selection control posture': ['no_post_hoc_metric_stratum_comparator_or_rule_selection'], 'multiple comparison posture': ['predeclared_policy_required_when_applicable'], 'baseline-specific posture': ['climatology_and_persistence_claims_remain_distinct'], 'cross-baseline posture': ['both_climatology_and_persistence_required'], 'market price posture': ['not_approved_as_baseline_or_truth'], 'evidence gate posture': ['claim_disposition_does_not_pass_evidence_gate'], 'immutability posture': ['superseding_claim_version_required'], 'claim evaluation posture': ['not_approved'], 'persistence posture': ['not_approved'], 'report export posture': ['not_approved'], 'canonical routing field': ['condition_id', 'token_id', 'outcome'], 'non routing field': ['market_id'], 'derived identifier field': ['token_outcome_pair'], 'next ticket recommendation': ['stage3_evidence_gate_decision_record_contract_planning'], 'evidence status': ['evaluation_claim_contract_planning_recorded'], 'label confidence': ['confirmed']}
EXPECTED_ASSIGNMENTS = [f"{field}: {value}" for field, values in EXPECTED_CLOSED_SETS.items() for value in values]
EXPECTED_EVIDENCE_GATE = "A claim record is not an evidence-gate decision; claim_supported does not mean the Stage 3 evidence gate passed; claim_not_supported does not by itself reject implementation permanently; calibration, predictive skill, economic edge, executability, implementation approval, and trading approval remain separate claim or decision classes; no claim record approves runtime implementation, persistence, reports, autonomy, production behavior, paper trading, trading, or order placement; only a later separately contracted evidence-gate decision may consume immutable claim records."
EXPECTED_NON_APPROVALS = "This ticket does not approve or create result calculation; evaluation execution; claim evaluation; claim records; claim approval; evidence-gate decisions; evidence-gate passage; implementation approval; probability generation; split execution; baseline execution; model training or calibration; data acquisition; source fetching; provider connectors; runtime schemas; dataclasses; serialization; persistence; database tables; migrations; reports; exports; diagrams; backtesting; simulation; market-price comparison execution; economic-edge findings; executability findings; paper trading; trading; order placement; autonomy; runtime behavior; or production behavior."
EXPECTED_REJECTION_SENTENCE = "Missing, duplicate, hybrid, reordered, extra, or custom fields and values are rejected."
NUMERIC_TOKEN_PATTERN = re.compile(r"(?<![A-Za-z0-9_])(?:\d+(?:\.\d+)?|\.\d+)(?:e[+-]?\d+)?%?(?![A-Za-z0-9_])", re.IGNORECASE)
NEW_ALLOWLIST_PATHS = {"docs/prd/WEATHER-BOT-STAGE3-EVALUATION-CLAIM-CONTRACT-PLANNING-01.md", "tests/core/test_weather_bot_stage3_evaluation_claim_contract_planning_01.py"}
FORBIDDEN_TERMS = ["@dataclass", "BaseModel", "CREATE TABLE", "ALTER TABLE", "json_schema", "claim engine is approved", "runtime schema is approved", "persist_claim", "write_report", "production behavior is approved"]

def _read_doc(text: str | None = None) -> str:
    return DOC_PATH.read_text(encoding="utf-8") if text is None else text

def _replace_once(text: str, old: str, new: str) -> str:
    assert text.count(old) == 1
    return text.replace(old, new, 1)

def _swap_adjacent_sections(text: str, first: str, second: str) -> str:
    first_marker = f"## {first}\n"
    second_marker = f"## {second}\n"
    first_start = text.index(first_marker)
    second_start = text.index(second_marker, first_start)
    third_match = re.search(r"^## .+$", text[second_start + len(second_marker):], re.MULTILINE)
    second_end = second_start + len(second_marker) + third_match.start() if third_match else len(text)
    return text[:first_start] + text[second_start:second_end] + text[first_start:second_start] + text[second_end:]

def _swap_table_rows(text: str, first_row: str, second_row: str) -> str:
    block = f"{first_row}\n{second_row}"
    assert block in text
    return text.replace(block, f"{second_row}\n{first_row}", 1)

def _sections(text: str) -> dict[str, str]:
    matches = list(re.finditer(r"^## (.+)$", text, re.MULTILINE))
    names = [m.group(1) for m in matches]
    assert names == HEADINGS
    assert len(names) == len(set(names)) == len(HEADINGS)
    out = {}
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        body = text[match.end():end].strip()
        assert body
        out[match.group(1)] = body
    return out

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
    assert len(output) == len(set(output))
    return output

def _parse_numbered(block: str) -> list[str]:
    output = []
    for line in block.splitlines():
        match = re.match(r"^(\d+)\. (.+)$", line)
        if match:
            assert int(match.group(1)) == len(output) + 1
            output.append(match.group(2))
        elif output and line.strip():
            break
    assert len(output) == len(set(output))
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

def _market_id_line_count(path: Path) -> int:
    return sum(1 for line in path.read_text(encoding="utf-8").splitlines() if "market_id" in line)

def _allowlist() -> dict[str, int]:
    tree = ast.parse(ALLOWLIST_PATH.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) and node.target.id == "ALLOWED_MARKET_ID_OCCURRENCE_LINES":
            value = node.value.args[0] if isinstance(node.value, ast.Call) else node.value
            return ast.literal_eval(value)
    raise AssertionError("allowlist assignment missing")

def _validate(text: str | None = None) -> None:
    doc = _read_doc(text)
    assert doc.startswith(f"# {TITLE}\n\nCanonical ID: {CANONICAL_ID}")
    sections = _sections(doc)
    assert _parse_table(sections["Exact evaluation claim-class matrix"]) == EXPECTED_CLAIM_CLASS_MATRIX
    assert _parse_table(sections["Exact claim-disposition matrix"]) == EXPECTED_DISPOSITION_MATRIX
    assert "No custom, hybrid, pending, partial, or additional claim disposition is allowed." in sections["Exact claim-disposition matrix"]
    common_block = sections["Common claim-record requirements"].split("Include exactly this ordered semantic-field list:\n\n", 1)[1]
    assert _parse_bullets(common_block) == EXPECTED_COMMON_FIELDS
    precedence_block = sections["Claim-disposition precedence and reason requirements"].split("Require exactly this precedence order:\n\n", 1)[1]
    assert _parse_numbered(precedence_block) == EXPECTED_PRECEDENCE
    assert sections["Evidence-gate separation and interpretation boundaries"] == EXPECTED_EVIDENCE_GATE
    assert sections["Explicit non-approvals"] == EXPECTED_NON_APPROVALS
    closed = _parse_closed_sets(sections["Machine-checkable assignments"])
    assert list(closed) == list(EXPECTED_CLOSED_SETS)
    assert closed == EXPECTED_CLOSED_SETS
    actual = _parse_actual(sections["Machine-checkable assignments"])
    assert actual == EXPECTED_ASSIGNMENTS
    assert actual == [f"{field}: {value}" for field, values in closed.items() for value in values]
    assert sections["Machine-checkable assignments"].count(EXPECTED_REJECTION_SENTENCE) == 1
    assert "Immediate predecessor: pr_363." in sections["Immediate predecessor and merge verification"]
    assert f"ACTUAL_PR_363_MERGE_SHA: {MERGE_COMMIT}" in sections["Immediate predecessor and merge verification"]
    assert PREVIEW_MERGE_SHA in sections["Immediate predecessor and merge verification"]
    assert f"ACTUAL_PR_363_MERGE_SHA: {PREVIEW_MERGE_SHA}" not in sections["Immediate predecessor and merge verification"]
    assert SUCCESSOR in sections["Recommended next ticket"]
    assert "- condition_id\n- token_id\n- outcome" in sections["Canonical routing posture"]
    assert "market_id is non-routing only." in sections["Canonical routing posture"]
    assert "token_outcome_pair is derived only." in sections["Canonical routing posture"]
    policy = sections["Multiple-testing and selection-control requirements"]
    precedence_policy = "\n".join(
        line for line in sections["Claim-disposition precedence and reason requirements"].splitlines()
        if not re.match(r"^\d+\. ", line)
    )
    assert not NUMERIC_TOKEN_PATTERN.search(policy)
    assert not NUMERIC_TOKEN_PATTERN.search(precedence_policy)
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
    class_row_1 = "| candidate_vs_climatology_predictive_skill | one or more predeclared paired_comparison_result records under applicable proper scores | candidate versus climatology under one exact paired scope | whether the predeclared candidate-versus-climatology claim rule is satisfied for the exact metrics and scope | overall superiority, calibration, economic edge, executability, implementation approval, or trading approval |"
    class_row_2 = "| candidate_vs_persistence_predictive_skill | one or more predeclared paired_comparison_result records under applicable proper scores | candidate versus persistence under one exact paired scope | whether the predeclared candidate-versus-persistence claim rule is satisfied for the exact metrics and scope | overall superiority, calibration, economic edge, executability, implementation approval, or trading approval |"
    disposition_row_1 = "| claim_supported | every required result is supported, the exact result set is complete, and the predeclared claim rule is satisfied | eligible only for a later evidence-gate decision; no gate passage is approved here |"
    disposition_row_2 = "| claim_not_supported | every required result is supported and complete but the predeclared claim rule is not satisfied | evidence-gate support from this claim is absent |"
    mutations = [
        _swap_adjacent_sections(base, "Status and scope", "Immediate predecessor and merge verification"),
        _replace_once(base, class_row_1, class_row_1.replace("overall superiority, calibration", "overall superiority, changed calibration")),
        _replace_once(base, class_row_2, class_row_1),
        _replace_once(base, class_row_1, class_row_1.replace("candidate_vs_climatology_predictive_skill", "unknown_claim_class")),
        _swap_table_rows(base, disposition_row_1, disposition_row_2),
        _replace_once(base, disposition_row_1, disposition_row_1.replace("claim_supported", "unknown_claim_disposition", 1)),
        _replace_once(base, "- evaluation_claim_id\n- claim_class", "- claim_class\n- evaluation_claim_id"),
        _replace_once(base, "1. claim_blocked\n2. claim_unavailable", "1. claim_unavailable\n2. claim_blocked"),
        _replace_once(base, "- weather bot planning stage:\n", "- label confidence:\n"),
        _replace_once(base, "- label confidence: confirmed", "- label confidence: confirmed\n- label confidence: confirmed"),
        _replace_once(base, "- label confidence: confirmed", "- label confidence confirmed"),
        _replace_once(base, "required_evaluation_result_ids\n- observed_evaluation_result_ids", "observed_evaluation_result_ids"),
        _replace_once(base, "confidence level", "90% confidence"),
        _replace_once(base, "tolerance", "1e-6 tolerance"),
        _replace_once(base, "bin count", "12 bins"),
        _replace_once(base, "claim_supported does not mean", "claim_supported means"),
        _replace_once(base, "does not approve or create", "does approve and create"),
        _replace_once(base, EXPECTED_REJECTION_SENTENCE, "Missing values are rejected."),
        _replace_once(base, EXPECTED_REJECTION_SENTENCE, ""),
    ]
    for mutated in mutations:
        assert mutated != base
        try:
            _validate(mutated)
        except AssertionError:
            continue
        raise AssertionError("mutation was not rejected")
