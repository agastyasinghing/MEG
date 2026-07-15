"""Static tests for Weather Bot Stage 3 evidence-gate decision-record contract planning."""
from __future__ import annotations

import ast
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DOC_PATH = REPO_ROOT / "docs/prd/WEATHER-BOT-STAGE3-EVIDENCE-GATE-DECISION-RECORD-CONTRACT-PLANNING-01.md"
ALLOWLIST_PATH = REPO_ROOT / "tests/core/canonical_id_allowlist.py"
TITLE = "WEATHER-BOT-STAGE3-EVIDENCE-GATE-DECISION-RECORD-CONTRACT-PLANNING-01"
CANONICAL_ID = TITLE
ACTUAL_PR_364_MERGE_SHA = "cd3d2c5eff10e9a86b8548b3b49912962a52c3c6"
PREVIEW_MERGE_SHA = "d81c597bdf93bc7ade4efbaa1110c9e65f51cb61"
HEADINGS = ["Status and scope", "Immediate predecessor and merge verification", "Contract purpose and decision boundary", "Controlling Stage 3 evidence-gate definition", "Upstream claim-record dependencies", "Exact evidence-gate component matrix", "Exact component-outcome matrix", "Exact evidence-gate disposition matrix", "Common decision-record requirements", "Gate-rule predeclaration requirements", "Required claim-set completeness", "Cross-baseline predictive-skill component requirements", "Representation-appropriate calibration component requirements", "Threshold-weighted and stratum component requirements", "Selection scope and no-lookahead integrity requirements", "Cross-component consistency requirements", "Multiple-testing and selection-control inheritance", "Decision-disposition precedence and reason requirements", "Evidence insufficiency blockage and unavailable handling", "Scope identity and result-chain traceability", "Identity provenance and immutability", "Implementation-approval separation and interpretation boundaries", "Fail-closed requirements", "Explicit non-approvals", "Canonical routing posture", "Recommended next ticket", "Machine-checkable assignments", "Acceptance criteria"]
EXPECTED_COMPONENT_MATRIX = [['Gate component', 'Required immutable inputs', 'Applicability rule', 'Satisfied posture', 'Fail-closed boundary'], ['---', '---', '---', '---', '---'], ['cross_baseline_predictive_skill', 'one complete candidate_predictive_skill_across_required_baselines claim with its linked immutable result records', 'required for every overall Stage 3 gate decision', 'the predeclared gate rule accepts the complete supported cross-baseline predictive-skill claim', 'block when either required baseline, linked result set, pairing scope, or claim provenance is incomplete or incompatible'], ['representation_appropriate_calibration', 'exactly one predeclared binary_calibration_behavior, distributional_calibration_behavior, or ensemble_calibration_behavior claim selected by prediction representation', 'required according to the candidate representation fixed before test-result inspection', 'the predeclared gate rule accepts the complete supported representation-compatible calibration claim', 'block when representation, diagnostic policy, linked result set, scope, or claim provenance is incompatible'], ['threshold_weighted_skill_when_applicable', 'the complete predeclared threshold_weighted_distribution_skill claim set', 'required only when the gate rule declared threshold-focused evaluation applicable before test-result inspection', 'the applicable threshold-focused claims satisfy the predeclared gate rule, or the component is explicitly component_not_applicable', 'block when applicability is selected post hoc or required threshold-focused claims are missing, incomplete, or incompatible'], ['stratum_specific_skill_when_applicable', 'the complete ordered predeclared stratum_specific_predictive_skill claim set', 'required only for strata declared applicable and supportable before test-result inspection', 'every required stratum claim satisfies the predeclared gate rule, or the component is explicitly component_not_applicable', 'block when strata are selected, removed, pooled, or substituted after claim inspection'], ['selection_scope_and_no_lookahead_integrity', 'all required claim records plus their linked immutable result, split, probability, baseline, and provenance identities', 'required for every overall Stage 3 gate decision', 'claim selection, multiplicity, scope, point-in-time, and no-lookahead requirements are complete and compatible', 'block for leakage, final-archive substitution, hidden omission, post-hoc selection, scope substitution, or provenance failure'], ['overall_stage3_evidence_gate', 'the complete ordered set of all required applicable component outcomes', 'required for every Stage 3 evidence-gate decision record', 'the exact predeclared overall gate rule produces one allowed Stage 3 gate disposition', 'block when any required component identity, outcome, rule, reason, or provenance field is missing or incompatible']]
EXPECTED_OUTCOME_MATRIX = [['Component outcome', 'Required meaning', 'Overall-gate posture'], ['---', '---', '---'], ['component_satisfied', 'every required input for the component is supported, complete, compatible, and satisfies the predeclared component rule', 'eligible for overall rule evaluation'], ['component_not_satisfied', 'every required input is supported, complete, and compatible, but the predeclared component rule is not satisfied', 'prevents stage3_gate_passed unless the predeclared overall rule explicitly and validly does not require satisfaction of that component'], ['component_insufficient', 'no blocking or unavailable condition applies, but a required claim or component-level support rule is insufficient', 'produces stage3_gate_insufficient'], ['component_blocked', 'a contract, leakage, scope, selection, accounting, immutability, or provenance requirement failed', 'produces stage3_gate_blocked'], ['component_unavailable', 'no blocking condition applies, but a required permitted claim record does not exist or is unavailable', 'produces stage3_gate_unavailable'], ['component_not_applicable', 'the gate rule declared this conditional component inapplicable before test-result inspection', 'excluded from satisfaction evaluation but preserved in the record']]
EXPECTED_GATE_MATRIX = [['Gate disposition', 'Required meaning', 'Subsequent-action posture'], ['---', '---', '---'], ['stage3_gate_passed', 'every required applicable component is complete and the predeclared overall gate rule is satisfied', 'eligible only for a later separate implementation-readiness review or explicit approval request'], ['stage3_gate_not_passed', 'every required applicable component is complete and evaluable but the predeclared overall gate rule is not satisfied', 'no implementation-readiness handoff is supported by this decision'], ['stage3_gate_insufficient', 'no blocked or unavailable condition applies, but one or more required components are insufficient', 'gate passage and implementation-readiness handoff are blocked'], ['stage3_gate_blocked', 'a required component is blocked or a gate contract, leakage, scope, selection, accounting, immutability, or provenance requirement failed', 'the decision is invalid for implementation-readiness use'], ['stage3_gate_unavailable', 'no blocked condition applies, but one or more required permitted component inputs are unavailable', 'no substitution, inference, backfill, gate passage, or implementation-readiness use is allowed']]
EXPECTED_COMMON_FIELDS = ['evidence_gate_decision_id', 'evidence_gate_id', 'evidence_gate_version', 'gate_rule_id', 'gate_rule_version', 'gate_disposition', 'gate_disposition_reason', 'target_posture', 'candidate_method_id', 'candidate_method_version', 'prediction_representation', 'required_evaluation_claim_ids', 'observed_evaluation_claim_ids', 'missing_evaluation_claim_ids', 'required_claim_classes', 'observed_claim_classes', 'applicable_gate_components', 'component_outcomes', 'split_id', 'split_version', 'fold_scope', 'cutoff_scope', 'paired_test_record_set_id', 'aggregation_rule_ids', 'weighting_rule_ids', 'stratum_scope', 'uncertainty_policy_ids', 'sample_support_rule_ids', 'selection_control_policy_ids', 'multiple_comparison_policy_ids', 'no_lookahead_review_posture', 'result_chain_traceability_posture', 'subsequent_approval_request_eligibility_posture', 'provenance', 'decision_created_at', 'supersedes_decision_id_when_applicable']
EXPECTED_PRECEDENCE = ['stage3_gate_blocked', 'stage3_gate_unavailable', 'stage3_gate_insufficient', 'evaluate the complete predeclared rule as stage3_gate_passed or stage3_gate_not_passed']
EXPECTED_CLOSED_SETS = {'weather bot planning stage': ['weather_bot_stage3_evidence_gate_decision_record_contract_planning'], 'immediate predecessor pr': ['pr_364'], 'ticket lifecycle status': ['docs_static_test_only', 'contract_planning_only'], 'decision record contract status': ['requirements_defined', 'decision_records_not_created', 'gate_decision_not_made'], 'scoring target posture': ['venue_defined_settlement_outcome'], 'gate component': ['cross_baseline_predictive_skill', 'representation_appropriate_calibration', 'threshold_weighted_skill_when_applicable', 'stratum_specific_skill_when_applicable', 'selection_scope_and_no_lookahead_integrity', 'overall_stage3_evidence_gate'], 'component outcome': ['component_satisfied', 'component_not_satisfied', 'component_insufficient', 'component_blocked', 'component_unavailable', 'component_not_applicable'], 'gate disposition': ['stage3_gate_passed', 'stage3_gate_not_passed', 'stage3_gate_insufficient', 'stage3_gate_blocked', 'stage3_gate_unavailable'], 'disposition precedence': ['blocked_then_unavailable_then_insufficient_then_rule_evaluation'], 'claim dependency posture': ['immutable_evaluation_claim_records_required'], 'claim completeness posture': ['exact_ordered_required_claim_set_required'], 'result traceability posture': ['immutable_result_chain_traceability_required'], 'component applicability posture': ['predeclared_before_claim_inspection'], 'gate rule posture': ['predeclared_versioned_exact_scope_required'], 'selection control posture': ['inherited_predeclared_selection_controls_required'], 'multiple comparison posture': ['inherited_predeclared_policy_required_when_applicable'], 'no lookahead posture': ['point_in_time_and_publication_availability_required'], 'market price posture': ['not_approved_as_baseline_or_truth'], 'implementation approval posture': ['gate_passage_does_not_approve_implementation'], 'subsequent review posture': ['separate_implementation_readiness_review_required'], 'gate decision posture': ['not_approved'], 'persistence posture': ['not_approved'], 'report export posture': ['not_approved'], 'canonical routing field': ['condition_id', 'token_id', 'outcome'], 'non routing field': ['market_id'], 'derived identifier field': ['token_outcome_pair'], 'next ticket recommendation': ['stage3_retrospective_scoring_implementation_readiness_review'], 'evidence status': ['evidence_gate_decision_record_contract_planning_recorded'], 'label confidence': ['confirmed']}
EXPECTED_ASSIGNMENTS = [
    'weather bot planning stage: weather_bot_stage3_evidence_gate_decision_record_contract_planning',
    'immediate predecessor pr: pr_364',
    'ticket lifecycle status: docs_static_test_only',
    'ticket lifecycle status: contract_planning_only',
    'decision record contract status: requirements_defined',
    'decision record contract status: decision_records_not_created',
    'decision record contract status: gate_decision_not_made',
    'scoring target posture: venue_defined_settlement_outcome',
    'gate component: cross_baseline_predictive_skill',
    'gate component: representation_appropriate_calibration',
    'gate component: threshold_weighted_skill_when_applicable',
    'gate component: stratum_specific_skill_when_applicable',
    'gate component: selection_scope_and_no_lookahead_integrity',
    'gate component: overall_stage3_evidence_gate',
    'component outcome: component_satisfied',
    'component outcome: component_not_satisfied',
    'component outcome: component_insufficient',
    'component outcome: component_blocked',
    'component outcome: component_unavailable',
    'component outcome: component_not_applicable',
    'gate disposition: stage3_gate_passed',
    'gate disposition: stage3_gate_not_passed',
    'gate disposition: stage3_gate_insufficient',
    'gate disposition: stage3_gate_blocked',
    'gate disposition: stage3_gate_unavailable',
    'disposition precedence: blocked_then_unavailable_then_insufficient_then_rule_evaluation',
    'claim dependency posture: immutable_evaluation_claim_records_required',
    'claim completeness posture: exact_ordered_required_claim_set_required',
    'result traceability posture: immutable_result_chain_traceability_required',
    'component applicability posture: predeclared_before_claim_inspection',
    'gate rule posture: predeclared_versioned_exact_scope_required',
    'selection control posture: inherited_predeclared_selection_controls_required',
    'multiple comparison posture: inherited_predeclared_policy_required_when_applicable',
    'no lookahead posture: point_in_time_and_publication_availability_required',
    'market price posture: not_approved_as_baseline_or_truth',
    'implementation approval posture: gate_passage_does_not_approve_implementation',
    'subsequent review posture: separate_implementation_readiness_review_required',
    'gate decision posture: not_approved',
    'persistence posture: not_approved',
    'report export posture: not_approved',
    'canonical routing field: condition_id',
    'canonical routing field: token_id',
    'canonical routing field: outcome',
    'non routing field: market_id',
    'derived identifier field: token_outcome_pair',
    'next ticket recommendation: stage3_retrospective_scoring_implementation_readiness_review',
    'evidence status: evidence_gate_decision_record_contract_planning_recorded',
    'label confidence: confirmed',
]
EXPECTED_IMPL = "An evidence-gate decision record is not implementation approval; stage3_gate_passed means only that the complete predeclared Stage 3 evidence-gate rule was satisfied for the exact recorded candidate and scope; stage3_gate_passed may support only a later separate implementation-readiness review or explicit approval request; stage3_gate_not_passed does not permanently reject future refinement; stage3_gate_insufficient, stage3_gate_blocked, and stage3_gate_unavailable do not permit implementation-readiness handoff; no gate disposition approves scoring execution, evaluation execution, persistence, reporting, simulation, runtime behavior, autonomy, production behavior, paper trading, trading, or order placement."
EXPECTED_NON_APPROVALS = "This ticket does not approve or create result calculation; evaluation execution; claim evaluation; claim records; evidence-gate evaluation; evidence-gate decision records; evidence-gate passage; implementation-readiness findings; implementation approval; probability generation; split execution; baseline execution; model training or calibration; data acquisition; corpus creation or expansion; source fetching; provider connectors; runtime schemas; dataclasses; serialization; persistence; database tables; migrations; reports; exports; diagrams; backtesting; simulation; market-price comparison execution; economic-edge findings; executability findings; paper trading; trading; order placement; autonomy; runtime behavior; or production behavior."
EXPECTED_ROUTING = """Canonical routing fields remain exactly:\n\n- condition_id\n- token_id\n- outcome\n\nmarket_id is non-routing only.\n\ntoken_outcome_pair is derived only."""
EXPECTED_NEXT = """WEATHER-BOT-STAGE3-RETROSPECTIVE-SCORING-IMPLEMENTATION-READINESS-REVIEW-01\n\nIt must remain docs/static-test-only/readiness-review-only and must not implement scoring, execute evaluation, create evidence, make a gate decision, approve implementation, persist records, create reports, or add runtime behavior. It may only determine whether the completed Stage 3 contract-planning foundation is coherent enough to support a later separate explicit implementation-approval request."""
EXPECTED_REJECTION = "Missing, duplicate, hybrid, reordered, extra, or custom fields and values are rejected."
NUMERIC_TOKEN_PATTERN = re.compile(r"(?<![A-Za-z0-9_])(?:\d+(?:\.\d+)?|\.\d+)(?:e[+-]?\d+)?%?(?![A-Za-z0-9_])", re.IGNORECASE)
NEW_ALLOWLIST_PATHS = (DOC_PATH.relative_to(REPO_ROOT).as_posix(), "tests/core/test_weather_bot_stage3_evidence_gate_decision_record_contract_planning_01.py")
FORBIDDEN_TERMS = ["@dataclass", "BaseModel", "CREATE TABLE", "ALTER TABLE", "json_schema", "gate engine is approved", "decision implementation is approved", "runtime schema is approved", "persist_decision", "write_report", "simulate_market", "production behavior is approved"]

def _read_doc(text: str | None = None) -> str:
    return DOC_PATH.read_text(encoding="utf-8") if text is None else text

def _replace_once(text: str, old: str, new: str) -> str:
    assert text.count(old) == 1
    return text.replace(old, new, 1)

def _replace_first(text: str, old: str, new: str) -> str:
    assert old in text
    return text.replace(old, new, 1)

def _swap_adjacent_blocks(text: str, first: str, second: str) -> str:
    block = first + "\n" + second
    assert block in text
    return text.replace(block, second + "\n" + first, 1)

def _validate_exact_header(doc: str) -> None:
    lines = doc.splitlines()
    assert lines[0] == f"# {TITLE}"
    assert lines[1] == ""
    assert lines[2] == f"Canonical ID: {CANONICAL_ID}"
    assert doc.count(f"Canonical ID: {CANONICAL_ID}") == 1
    assert len([line for line in lines if line.startswith("Canonical ID:")]) == 1

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
    result: dict[str, list[str]] = {}
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
    flattened = []
    for field, values in closed.items():
        for value in values:
            flattened.append(f"{field}: {value}")
    return flattened

def _market_id_line_count(path: Path) -> int:
    legacy_identifier = "market" + "_id"
    return sum(1 for line in path.read_text(encoding="utf-8").splitlines() if legacy_identifier in line)

def _allowlist() -> dict[str, int]:
    tree = ast.parse(ALLOWLIST_PATH.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) and node.target.id == "ALLOWED_MARKET_ID_OCCURRENCE_LINES":
            value = node.value.args[0] if isinstance(node.value, ast.Call) else node.value
            return ast.literal_eval(value)
    raise AssertionError("allowlist assignment missing")

def _without_ordered_list_numbers(section: str) -> str:
    lines = []
    for line in section.splitlines():
        lines.append(re.sub(r"^\d+\. ", "", line))
    return "\n".join(lines)

def _validate(text: str | None = None) -> None:
    doc = _read_doc(text)
    _validate_exact_header(doc)
    sections = _sections(doc)
    assert _parse_table(sections["Exact evidence-gate component matrix"]) == EXPECTED_COMPONENT_MATRIX
    assert _parse_table(sections["Exact component-outcome matrix"]) == EXPECTED_OUTCOME_MATRIX
    assert _parse_table(sections["Exact evidence-gate disposition matrix"]) == EXPECTED_GATE_MATRIX
    common_block = sections["Common decision-record requirements"].split("Include exactly this ordered semantic-field list:\n\n", 1)[1]
    assert _parse_bullets(common_block) == EXPECTED_COMMON_FIELDS
    precedence_block = sections["Decision-disposition precedence and reason requirements"].split("Require exactly this order:\n\n", 1)[1]
    assert _parse_numbered(precedence_block) == EXPECTED_PRECEDENCE
    closed_sets = _parse_closed_sets(sections["Machine-checkable assignments"])
    assignments = _parse_actual(sections["Machine-checkable assignments"])
    assert closed_sets == EXPECTED_CLOSED_SETS
    assert assignments == EXPECTED_ASSIGNMENTS
    assert _flatten(EXPECTED_CLOSED_SETS) == _flatten(closed_sets) == EXPECTED_ASSIGNMENTS == assignments
    assert doc.count(EXPECTED_REJECTION) == 1
    assert sections["Implementation-approval separation and interpretation boundaries"] == EXPECTED_IMPL
    assert sections["Explicit non-approvals"] == EXPECTED_NON_APPROVALS
    assert sections["Canonical routing posture"] == EXPECTED_ROUTING
    assert sections["Recommended next ticket"] == EXPECTED_NEXT
    predecessor = sections["Immediate predecessor and merge verification"]
    assert "Immediate predecessor: pr_364." in predecessor
    assert f"Verified actual PR #364 merge commit: {ACTUAL_PR_364_MERGE_SHA}." in predecessor
    assert PREVIEW_MERGE_SHA in predecessor
    assert ACTUAL_PR_364_MERGE_SHA != PREVIEW_MERGE_SHA
    for name in ["Multiple-testing and selection-control inheritance", "Decision-disposition precedence and reason requirements"]:
        scanned = _without_ordered_list_numbers(sections[name])
        assert not NUMERIC_TOKEN_PATTERN.search(scanned)
    for term in FORBIDDEN_TERMS:
        assert term not in doc

def test_contract_document_static_requirements() -> None:
    _validate()

def test_allowlist_counts_match_direct_observed_lines() -> None:
    allowlist = _allowlist()
    for rel_path in NEW_ALLOWLIST_PATHS:
        assert rel_path in allowlist
        assert allowlist[rel_path] == _market_id_line_count(REPO_ROOT / rel_path)

def _expect_rejected(mutated: str) -> None:
    assert mutated != _read_doc()
    try:
        _validate(mutated)
    except AssertionError:
        return
    raise AssertionError("mutated document was accepted")

def test_in_memory_mutations_are_rejected() -> None:
    doc = _read_doc()
    mutations = [
        _replace_once(doc, f"Canonical ID: {CANONICAL_ID}", f"Canonical ID: {CANONICAL_ID}-X"),
        _replace_once(doc, f"Canonical ID: {CANONICAL_ID}", f"Canonical ID: {CANONICAL_ID}\nCanonical ID: {CANONICAL_ID}"),
        _replace_once(doc, "## Status and scope", "## TEMP").replace("## Immediate predecessor and merge verification", "## Status and scope", 1).replace("## TEMP", "## Immediate predecessor and merge verification", 1),
        _replace_first(doc, "required for every overall Stage 3 gate decision", "optional for every overall Stage 3 gate decision"),
        _replace_once(doc, "| overall_stage3_evidence_gate |", "| cross_baseline_predictive_skill |"),
        _replace_first(doc, "cross_baseline_predictive_skill", "unknown_component"),
        _replace_once(doc, "eligible for overall rule evaluation", "eligible for waived rule evaluation"),
        _replace_first(doc, "component_unavailable", "component_unknown"),
        _swap_adjacent_blocks(
            doc,
            "| stage3_gate_passed | every required applicable component is complete and the predeclared overall gate rule is satisfied | eligible only for a later separate implementation-readiness review or explicit approval request |",
            "| stage3_gate_not_passed | every required applicable component is complete and evaluable but the predeclared overall gate rule is not satisfied | no implementation-readiness handoff is supported by this decision |",
        ),
        _replace_once(
            doc,
            "| stage3_gate_unavailable | no blocked condition applies, but one or more required permitted component inputs are unavailable | no substitution, inference, backfill, gate passage, or implementation-readiness use is allowed |",
            "| stage3_gate_unknown | no blocked condition applies, but one or more required permitted component inputs are unavailable | no substitution, inference, backfill, gate passage, or implementation-readiness use is allowed |",
        ),
        _replace_once(doc, "- evidence_gate_decision_id\n- evidence_gate_id", "- evidence_gate_id\n- evidence_gate_decision_id"),
        _replace_once(doc, "1. stage3_gate_blocked\n2. stage3_gate_unavailable", "1. stage3_gate_unavailable\n2. stage3_gate_blocked"),
        _swap_adjacent_blocks(
            doc,
            "- weather bot planning stage:\n  - weather_bot_stage3_evidence_gate_decision_record_contract_planning",
            "- immediate predecessor pr:\n  - pr_364",
        ),
        _replace_once(doc, "- label confidence: confirmed", "- label confidence: confirmed\n- label confidence: confirmed"),
        _replace_once(doc, "- label confidence: confirmed", "- label confidence confirmed"),
        _replace_first(doc, "- required_evaluation_claim_ids", "- removed_required_evaluation_claim_ids"),
        _replace_once(doc, "numeric alpha", "90% confidence or numeric alpha"),
        _replace_first(doc, "tolerance", "1e-6 tolerance"),
        _replace_once(doc, "bin count", "12 bins"),
        _replace_once(doc, "is not implementation approval", "is implementation approval"),
        _replace_once(doc, "does not approve or create result calculation", "does approve and create result calculation"),
        _replace_once(doc, "- outcome\n\nmarket_id is non-routing", "- outcome\n- market_id\n\nmarket_id is non-routing"),
        _replace_once(doc, "WEATHER-BOT-STAGE3-RETROSPECTIVE-SCORING-IMPLEMENTATION-READINESS-REVIEW-01", "WEATHER-BOT-STAGE3-SCORING-IMPLEMENTATION-01"),
        _replace_once(doc, EXPECTED_REJECTION, "Missing fields are accepted."),
        _replace_once(doc, EXPECTED_REJECTION, ""),
    ]
    for mutated in mutations:
        _expect_rejected(mutated)
