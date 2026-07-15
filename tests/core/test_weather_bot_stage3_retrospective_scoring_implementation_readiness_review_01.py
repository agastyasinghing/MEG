
"""Static tests for Stage 3 retrospective scoring implementation readiness review."""
from __future__ import annotations

import ast
import re
from pathlib import Path

DOC = Path("docs/prd/WEATHER-BOT-STAGE3-RETROSPECTIVE-SCORING-IMPLEMENTATION-READINESS-REVIEW-01.md")
ALLOWLIST = Path("tests/core/canonical_id_allowlist.py")
CANONICAL_ID = "WEATHER-BOT-STAGE3-RETROSPECTIVE-SCORING-IMPLEMENTATION-READINESS-REVIEW-01"
ACTUAL_PR_365_MERGE_SHA = "f67c49bfb697c79c428fbe869af32dd24b12a32f"
PREVIEW_MERGE_SHA = "d2e37990da8b5bf1a982733795d842eb186822f7"
EXPECTED_HEADINGS = [
    "Status and scope",
    "Immediate predecessor and merge verification",
    "Review purpose and readiness boundary",
    "Controlling Stage 3 definition and gate sequence",
    "Reviewed contract-planning artifact inventory",
    "Exact prerequisite artifact matrix",
    "Exact readiness-gate matrix",
    "Exact review-disposition matrix",
    "Contract-chain completeness review",
    "Target routing and settlement-object review",
    "Probability-record contract review",
    "Strict OOS and no-lookahead contract review",
    "Baseline contract review",
    "Scoring and diagnostic contract review",
    "Result claim and decision-record chain review",
    "Static-test and oracle-quality review",
    "Data corpus and evidence-sufficiency boundary",
    "Implementation-scope decomposition requirements",
    "Readiness decision rules and precedence",
    "Current readiness determination",
    "Implementation-approval separation and interpretation boundaries",
    "Explicit non-approvals",
    "Canonical routing posture",
    "Recommended next ticket",
    "Machine-checkable assignments",
    "Acceptance criteria",
]
EXPECTED_PREREQUISITE_MATRIX = [
    ["Artifact role", "Canonical artifact", "Required contribution", "Current review finding", "Blocking condition"],
    ["---", "---", "---", "---", "---"],
    ["stage3_requirements", "WEATHER-BOT-STAGE3-RETROSPECTIVE-PROBABILITY-SCORING-REQUIREMENTS-PLANNING-01", "controls the venue-defined target, strict OOS scoring objective, evidence categories, and non-approval boundary", "present_and_coherent", "block when missing, superseded, or contradictory"],
    ["probability_record_contract", "WEATHER-BOT-STAGE3-PROBABILITY-RECORD-CONTRACT-PLANNING-01", "defines immutable probability-record semantics and point-in-time identity requirements", "present_and_coherent", "block when record identity, target, representation, or provenance requirements are incomplete"],
    ["strict_oos_split_contract", "WEATHER-BOT-STAGE3-STRICT-OOS-SPLIT-CONTRACT-PLANNING-01", "defines strict OOS split, cutoff, no-lookahead, and replay boundaries", "present_and_coherent", "block when future-information or split-scope protections are incomplete"],
    ["baseline_contracts", "WEATHER-BOT-STAGE3-BASELINE-CONTRACTS-PLANNING-01", "defines climatology and persistence baseline semantics and pairing requirements", "present_and_coherent", "block when either required baseline or paired-scope rule is missing"],
    ["scoring_and_diagnostics_contract", "WEATHER-BOT-STAGE3-SCORING-AND-DIAGNOSTICS-CONTRACT-PLANNING-01", "defines representation-appropriate scores, diagnostics, stratification, and uncertainty requirements", "present_and_coherent", "block when applicability, direction, aggregation, or diagnostic boundaries are incomplete"],
    ["evaluation_result_record_contract", "WEATHER-BOT-STAGE3-EVALUATION-RESULT-RECORD-CONTRACT-PLANNING-01", "defines immutable result-record semantics, support status, accounting, and provenance", "present_and_coherent", "block when result identity, support status, accounting, or immutability is incomplete"],
    ["evaluation_claim_contract", "WEATHER-BOT-STAGE3-EVALUATION-CLAIM-CONTRACT-PLANNING-01", "defines predeclared claim classes, dispositions, selection control, and interpretation boundaries", "present_and_coherent", "block when claim completeness, multiplicity, or interpretation separation is incomplete"],
    ["evidence_gate_decision_record_contract", "WEATHER-BOT-STAGE3-EVIDENCE-GATE-DECISION-RECORD-CONTRACT-PLANNING-01", "defines immutable future evidence-gate decision-record semantics and implementation-approval separation", "present_and_coherent", "block when gate components, dispositions, traceability, or approval separation is incomplete"],
]
EXPECTED_READINESS_GATE_MATRIX = [
    ["Readiness gate", "Required finding", "Current status", "Consequence if not passed"],
    ["---", "---", "---", "---"],
    ["predecessor_and_scope_integrity", "PR #365 is the verified immediate predecessor and the review changes only the authorized documentation and static-test paths", "passed", "block the review until lineage and scope are corrected"],
    ["complete_contract_chain", "every required Stage 3 planning artifact is present, ordered, internally coherent, and unsuperseded", "passed", "block or require targeted refinement according to defect severity"],
    ["target_and_routing_preserved", "the venue-defined settlement target and canonical routing fields remain unchanged across the chain", "passed", "block because the reviewed system target would be ambiguous or incorrect"],
    ["strict_oos_and_no_lookahead_defined", "split, cutoff, as-of, publication-time, revision, finality, and future-information boundaries are explicit", "passed", "block because retrospective scoring could leak unavailable information"],
    ["baseline_and_comparator_contracts_defined", "climatology and persistence are both defined with exact paired-scope requirements", "passed", "block because predictive-skill comparison would be incomplete"],
    ["scoring_and_diagnostic_applicability_defined", "scores and diagnostics are representation-compatible, versioned, scoped, and interpretation-limited", "passed", "require refinement or block when applicability cannot be determined safely"],
    ["immutable_result_claim_decision_chain_defined", "result, claim, and future decision records preserve exact identities, provenance, support states, dispositions, and supersession", "passed", "block because auditability and fail-closed interpretation would be incomplete"],
    ["static_test_oracle_integrity", "critical document structure and safety boundaries are enforced by independent literal oracles and direct mutations", "passed", "require targeted refinement before any approval request"],
    ["data_and_evidence_boundary_explicit", "contract readiness is separated from corpus sufficiency, result generation, claim support, and evidence-gate passage", "passed", "block because planning readiness could be misrepresented as evidence"],
    ["separate_approval_request_eligibility", "the complete planning foundation is coherent enough only to request later explicit approval for one narrow implementation slice", "passed", "do not recommend an implementation-approval request"],
]
EXPECTED_REVIEW_DISPOSITION_MATRIX = [
    ["Review disposition", "Required meaning", "Allowed next action"],
    ["---", "---", "---"],
    ["ready_for_separate_implementation_approval_request", "every required readiness gate passed and no missing, conflicting, superseded, or weakly enforced contract boundary remains", "recommend one later separate explicit implementation-approval request; implementation remains unapproved"],
    ["needs_targeted_contract_refinement", "the foundation is broadly coherent but one or more narrow document or static-test defects must be corrected", "recommend one targeted refinement ticket and do not request implementation approval yet"],
    ["blocked_pending_foundation_fix", "a required artifact, target boundary, OOS protection, baseline, record chain, safety boundary, or provenance requirement is missing or contradictory", "stop and repair the foundation before any approval request"],
    ["hold", "the repository state is unavailable or insufficient to determine a safe readiness disposition", "make no implementation or approval-request recommendation"],
]
EXPECTED_PRECEDENCE = [
    "blocked_pending_foundation_fix",
    "hold",
    "needs_targeted_contract_refinement",
    "ready_for_separate_implementation_approval_request",
]
EXPECTED_CLOSED_SETS = {
    "weather bot planning stage": ["weather_bot_stage3_retrospective_scoring_implementation_readiness_review"],
    "immediate predecessor pr": ["pr_365"],
    "ticket lifecycle status": ["docs_static_test_only", "readiness_review_only"],
    "review target": ["stage3_contract_planning_foundation"],
    "artifact review finding": ["present_and_coherent", "missing", "conflicting", "insufficient", "not_applicable"],
    "readiness gate status": ["passed", "caution", "failed", "unavailable", "not_applicable"],
    "review disposition": ["ready_for_separate_implementation_approval_request", "needs_targeted_contract_refinement", "blocked_pending_foundation_fix", "hold"],
    "current review disposition": ["ready_for_separate_implementation_approval_request"],
    "scoring target posture": ["venue_defined_settlement_outcome"],
    "evidence gate posture": ["not_evaluated"],
    "evidence sufficiency posture": ["not_established_by_contract_readiness"],
    "data corpus posture": ["not_established_as_sample_sufficient"],
    "implementation approval posture": ["not_approved"],
    "probability generation posture": ["not_approved"],
    "scoring execution posture": ["not_approved"],
    "evaluation execution posture": ["not_approved"],
    "persistence posture": ["not_approved"],
    "report export posture": ["not_approved"],
    "canonical routing field": ["condition_id", "token_id", "outcome"],
    "non routing field": ["market_id"],
    "derived identifier field": ["token_outcome_pair"],
    "next ticket recommendation": ["stage3_retrospective_scoring_implementation_approval_request"],
    "evidence status": ["stage3_implementation_readiness_review_recorded"],
    "label confidence": ["confirmed"],
}
EXPECTED_ASSIGNMENTS = [
    "weather bot planning stage: weather_bot_stage3_retrospective_scoring_implementation_readiness_review",
    "immediate predecessor pr: pr_365",
    "ticket lifecycle status: docs_static_test_only",
    "ticket lifecycle status: readiness_review_only",
    "review target: stage3_contract_planning_foundation",
    "artifact review finding: present_and_coherent",
    "artifact review finding: missing",
    "artifact review finding: conflicting",
    "artifact review finding: insufficient",
    "artifact review finding: not_applicable",
    "readiness gate status: passed",
    "readiness gate status: caution",
    "readiness gate status: failed",
    "readiness gate status: unavailable",
    "readiness gate status: not_applicable",
    "review disposition: ready_for_separate_implementation_approval_request",
    "review disposition: needs_targeted_contract_refinement",
    "review disposition: blocked_pending_foundation_fix",
    "review disposition: hold",
    "current review disposition: ready_for_separate_implementation_approval_request",
    "scoring target posture: venue_defined_settlement_outcome",
    "evidence gate posture: not_evaluated",
    "evidence sufficiency posture: not_established_by_contract_readiness",
    "data corpus posture: not_established_as_sample_sufficient",
    "implementation approval posture: not_approved",
    "probability generation posture: not_approved",
    "scoring execution posture: not_approved",
    "evaluation execution posture: not_approved",
    "persistence posture: not_approved",
    "report export posture: not_approved",
    "canonical routing field: condition_id",
    "canonical routing field: token_id",
    "canonical routing field: outcome",
    "non routing field: market_id",
    "derived identifier field: token_outcome_pair",
    "next ticket recommendation: stage3_retrospective_scoring_implementation_approval_request",
    "evidence status: stage3_implementation_readiness_review_recorded",
    "label confidence: confirmed",
]
EXPECTED_PREDECESSOR_SECTION = """PR #365 is merged and is the verified immediate predecessor for this readiness-review scope.

ACTUAL_PR_365_MERGE_SHA: f67c49bfb697c79c428fbe869af32dd24b12a32f

The actual PR #365 merge commit is f67c49bfb697c79c428fbe869af32dd24b12a32f and is reachable from current main for this repository state.

The formerly open PR preview merge SHA d2e37990da8b5bf1a982733795d842eb186822f7 is not used as the actual merge commit.

No newer controlling Weather Bot artifact supersedes PR #365 for this readiness-review scope.

Immediate predecessor: pr_365."""
EXPECTED_CURRENT_READINESS_SECTION = """Review disposition: ready_for_separate_implementation_approval_request.

The Stage 3 retrospective-scoring contract-planning foundation is present and coherent enough to support a later separate explicit implementation-approval request for a narrowly bounded implementation slice. This documentation-layer readiness finding does not establish sample sufficiency, execute scoring, create evidence, make or pass an evidence-gate decision, approve implementation, or authorize persistence, reporting, simulation, runtime behavior, autonomy, production behavior, paper trading, trading, or order placement."""
EXPECTED_IMPLEMENTATION_APPROVAL_SECTION = """This readiness review is not implementation approval; ready_for_separate_implementation_approval_request means only that the reviewed planning contracts are coherent enough to ask for a later explicit approval; no implementation work may begin from this review alone; a later approval request must define one narrow implementation slice, exact files, tests, non-goals, rollback boundaries, and prohibited behaviors; the Stage 3 evidence gate remains unevaluated; no readiness disposition approves probability generation, scoring execution, evaluation execution, persistence, reporting, simulation, runtime behavior, autonomy, production behavior, paper trading, trading, or order placement."""
EXPECTED_NON_APPROVALS_SECTION = """This ticket does not approve or create probability generation; scoring execution; diagnostic execution; split execution; baseline execution; evaluation execution; result records; claim evaluation; claim records; evidence-gate evaluation; evidence-gate decision records; evidence-gate passage; implementation code; runtime schemas; dataclasses; serialization; persistence; database tables; migrations; reports; exports; data acquisition; corpus creation or expansion; source fetching; provider connectors; model training or calibration; backtesting; simulation; market-price comparison execution; economic-edge findings; executability findings; paper trading; trading; order placement; autonomy; runtime behavior; or production behavior."""
EXPECTED_ROUTING_SECTION = """Canonical routing fields remain exactly:

- condition_id
- token_id
- outcome

market_id is non-routing only.

token_outcome_pair is derived only."""
EXPECTED_NEXT_TICKET_SECTION = """WEATHER-BOT-STAGE3-RETROSPECTIVE-SCORING-IMPLEMENTATION-APPROVAL-REQUEST-01

It must remain docs/static-test-only/approval-request-only. It may request approval for one narrowly bounded retrospective-scoring implementation slice, but it must not itself implement code, execute scoring, create evidence, make a gate decision, persist records, create reports, or add runtime behavior."""
CRITICAL_SECTIONS = {
    "Immediate predecessor and merge verification": EXPECTED_PREDECESSOR_SECTION,
    "Current readiness determination": EXPECTED_CURRENT_READINESS_SECTION,
    "Implementation-approval separation and interpretation boundaries": EXPECTED_IMPLEMENTATION_APPROVAL_SECTION,
    "Explicit non-approvals": EXPECTED_NON_APPROVALS_SECTION,
    "Canonical routing posture": EXPECTED_ROUTING_SECTION,
    "Recommended next ticket": EXPECTED_NEXT_TICKET_SECTION,
}
REJECTION_SENTENCE = "Missing, duplicate, hybrid, reordered, extra, or custom fields and values are rejected."
NUMERIC_TOKEN_RE = re.compile(r"(?<![A-Za-z0-9_])(?:\d+\.\d+|\d+\.|\.\d+|\d+)(?:[eE][+-]?\d+)?%?(?![A-Za-z0-9_])")
NUMERIC_SCAN_SECTIONS = [
    "Data corpus and evidence-sufficiency boundary",
    "Implementation-scope decomposition requirements",
    "Readiness decision rules and precedence",
]
ALLOWED_NUMBERED_PREFIX_RE = re.compile(r"^[1-4]\. ")


def _read() -> str:
    return DOC.read_text()


def _sections(text: str) -> dict[str, str]:
    lines = text.splitlines()
    headings = [line[3:] for line in lines if line.startswith("## ")]
    assert headings == EXPECTED_HEADINGS
    assert len(headings) == len(set(headings))
    assert not [line for line in lines if line.startswith("## ") and line[3:] not in EXPECTED_HEADINGS]
    parts: dict[str, list[str]] = {}
    current = None
    for line in lines:
        if line.startswith("## "):
            current = line[3:]
            parts[current] = []
        elif current is not None:
            parts[current].append(line)
    result = {k: "\n".join(v).strip() for k, v in parts.items()}
    assert all(result[h].strip() for h in EXPECTED_HEADINGS)
    return result


def _table(section: str) -> list[list[str]]:
    rows = []
    for line in section.splitlines():
        if line.startswith("|"):
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            rows.append(cells)
    return rows


def _closed_sets(section: str) -> dict[str, list[str]]:
    assert section.startswith("Closed sets:\n")
    assert "\n\nActual assignments:\n" in section
    closed_text, actual_text = section.split("\n\nActual assignments:\n", 1)
    parsed: dict[str, list[str]] = {}
    current = None
    for line in closed_text.splitlines()[1:]:
        if line.startswith("- ") and line.endswith(":"):
            current = line[2:-1]
            assert current not in parsed
            parsed[current] = []
        elif line.startswith("  - ") and current:
            value = line[4:]
            assert value not in parsed[current]
            parsed[current].append(value)
        else:
            raise AssertionError(f"malformed closed-set line: {line}")
    assert list(parsed) == list(EXPECTED_CLOSED_SETS)
    assert parsed == EXPECTED_CLOSED_SETS
    assert "\n\n" in actual_text
    assignments_text, rejection = actual_text.rsplit("\n\n", 1)
    assert rejection == REJECTION_SENTENCE
    assignments = []
    for line in assignments_text.splitlines():
        assert line.startswith("- ") and ": " in line
        assignments.append(line[2:])
    assert len(assignments) == len(set(assignments))
    assert assignments == EXPECTED_ASSIGNMENTS
    flattened = []
    for field, values in EXPECTED_CLOSED_SETS.items():
        for value in values:
            flattened.append(f"{field}: {value}")
    assert flattened == EXPECTED_ASSIGNMENTS == assignments
    return parsed


def _validate(text: str) -> None:
    lines = text.splitlines()
    assert lines[0] == CANONICAL_ID
    assert lines[1] == ""
    assert lines[2] == f"Canonical ID: {CANONICAL_ID}"
    assert text.count(f"Canonical ID: {CANONICAL_ID}") == 1
    assert text.count(CANONICAL_ID) >= 2
    sections = _sections(text)
    for name, expected in CRITICAL_SECTIONS.items():
        assert sections[name] == expected
    assert sections["Immediate predecessor and merge verification"].count(f"ACTUAL_PR_365_MERGE_SHA: {ACTUAL_PR_365_MERGE_SHA}") == 1
    assert sections["Immediate predecessor and merge verification"].count(f"The actual PR #365 merge commit is {ACTUAL_PR_365_MERGE_SHA} and is reachable from current main for this repository state.") == 1
    assert sections["Immediate predecessor and merge verification"].count(f"The formerly open PR preview merge SHA {PREVIEW_MERGE_SHA} is not used as the actual merge commit.") == 1
    assert f"ACTUAL_PR_365_MERGE_SHA: {PREVIEW_MERGE_SHA}" not in sections["Immediate predecessor and merge verification"]
    assert _table(sections["Exact prerequisite artifact matrix"]) == EXPECTED_PREREQUISITE_MATRIX
    assert _table(sections["Exact readiness-gate matrix"]) == EXPECTED_READINESS_GATE_MATRIX
    assert _table(sections["Exact review-disposition matrix"]) == EXPECTED_REVIEW_DISPOSITION_MATRIX
    precedence = [line.split(". ", 1)[1] for line in sections["Readiness decision rules and precedence"].splitlines() if re.match(r"^[1-4]\. ", line)]
    assert precedence == EXPECTED_PRECEDENCE
    _closed_sets(sections["Machine-checkable assignments"])
    assert text.count(REJECTION_SENTENCE) == 1
    for section_name in NUMERIC_SCAN_SECTIONS:
        for line in sections[section_name].splitlines():
            if ALLOWED_NUMBERED_PREFIX_RE.match(line):
                line = line[3:]
            line = line.replace("Stage 3", "Stage three")
            assert not NUMERIC_TOKEN_RE.search(line), (section_name, line)
    forbidden_positive_runtime = [
        "This ticket approves",
        "implementation is approved",
        "runtime behavior is approved",
        "persistence is approved",
        "reports are approved",
        "simulation is approved",
        "production behavior is approved",
    ]
    for term in forbidden_positive_runtime:
        assert term not in text


def _replace_in_section(text: str, section_name: str, anchor: str, replacement: str) -> str:
    sections = _sections(text)
    body = sections[section_name]
    assert body.count(anchor) == 1
    new_body = body.replace(anchor, replacement, 1)
    assert new_body != body
    start = text.index(f"## {section_name}\n\n") + len(f"## {section_name}\n\n")
    following = [h for h in EXPECTED_HEADINGS[EXPECTED_HEADINGS.index(section_name) + 1:]]
    end = min([text.index(f"\n\n## {h}\n", start) for h in following] or [len(text)])
    mutated = text[:start] + new_body + text[end:]
    assert mutated != text
    return mutated


def _replace_section_body(text: str, section_name: str, old_body: str, new_body: str) -> str:
    assert old_body != new_body
    start = text.index(f"## {section_name}\n\n") + len(f"## {section_name}\n\n")
    following = [h for h in EXPECTED_HEADINGS[EXPECTED_HEADINGS.index(section_name) + 1:]]
    end = min([text.index(f"\n\n## {h}\n", start) for h in following] or [len(text)])
    assert text[start:end].strip() == old_body
    mutated = text[:start] + new_body + text[end:]
    assert mutated != text
    assert _sections(mutated)[section_name] == new_body.strip()
    return mutated


def _duplicate_exact_table_row_in_section(text: str, section_name: str, row: str) -> str:
    section = _sections(text)[section_name]
    assert section.count(row) == 1
    base_rows = _table(section)
    parsed_row = [cell.strip() for cell in row.strip().strip("|").split("|")]
    assert base_rows.count(parsed_row) == 1
    mutated = _replace_in_section(text, section_name, row, f"{row}\n{row}")
    mutated_section = _sections(mutated)[section_name]
    mutated_rows = _table(mutated_section)
    assert mutated_section.count(row) == 2
    assert mutated_rows.count(parsed_row) == 2
    assert len(mutated_rows) == len(base_rows) + 1
    assert all(cell_a == cell_b for cell_a, cell_b in zip(parsed_row, parsed_row))
    return mutated


def _swap_adjacent_exact_table_rows_in_section(
    text: str, section_name: str, first_row: str, second_row: str
) -> str:
    section = _sections(text)[section_name]
    assert section.count(first_row) == 1
    assert section.count(second_row) == 1
    base_rows = _table(section)
    first_cells = [cell.strip() for cell in first_row.strip().strip("|").split("|")]
    second_cells = [cell.strip() for cell in second_row.strip().strip("|").split("|")]
    first_index = base_rows.index(first_cells)
    assert base_rows[first_index + 1] == second_cells
    mutated = _replace_in_section(text, section_name, f"{first_row}\n{second_row}", f"{second_row}\n{first_row}")
    mutated_rows = _table(_sections(mutated)[section_name])
    assert len(mutated_rows) == len(base_rows)
    assert sorted(mutated_rows) == sorted(base_rows)
    assert mutated_rows[first_index] == second_cells
    assert mutated_rows[first_index + 1] == first_cells
    return mutated


def _remove_exact_table_row_from_section(text: str, section_name: str, row: str) -> str:
    section = _sections(text)[section_name]
    assert section.count(f"{row}\n") == 1
    base_rows = _table(section)
    parsed_row = [cell.strip() for cell in row.strip().strip("|").split("|")]
    assert base_rows.count(parsed_row) == 1
    mutated = _replace_in_section(text, section_name, f"{row}\n", "")
    mutated_rows = _table(_sections(mutated)[section_name])
    assert parsed_row not in mutated_rows
    assert len(mutated_rows) == len(base_rows) - 1
    assert [row_ for row_ in base_rows if row_ != parsed_row] == mutated_rows
    return mutated


def _swap_exact_closed_set_blocks(text: str, first_block: str, second_block: str) -> str:
    section_name = "Machine-checkable assignments"
    section = _sections(text)[section_name]
    closed_text, actual_text = section.split("\n\nActual assignments:\n", 1)
    assert closed_text.count(first_block) == 1
    assert closed_text.count(second_block) == 1
    assert closed_text.index(first_block) < closed_text.index(second_block)
    new_closed_text = closed_text.replace(first_block, "__FIRST_BLOCK__", 1)
    new_closed_text = new_closed_text.replace(second_block, first_block, 1)
    new_closed_text = new_closed_text.replace("__FIRST_BLOCK__", second_block, 1)
    assert new_closed_text.index(second_block) < new_closed_text.index(first_block)
    assert sorted(new_closed_text.splitlines()) == sorted(closed_text.splitlines())
    new_section = f"{new_closed_text}\n\nActual assignments:\n{actual_text}"
    mutated = _replace_section_body(text, section_name, section, new_section)
    assert _sections(mutated)[section_name].split("\n\nActual assignments:\n", 1)[1] == actual_text
    return mutated


def _assert_rejected(mutated: str) -> None:
    try:
        _validate(mutated)
    except AssertionError:
        return
    raise AssertionError("mutation unexpectedly passed")


def _assert_critical_unchanged_except(base: str, mutated: str, changed: str | None = None) -> None:
    base_sections = _sections(base)
    mutated_sections = _sections(mutated)
    for name in CRITICAL_SECTIONS:
        if name != changed:
            assert mutated_sections[name] == base_sections[name]


def test_document_contract() -> None:
    _validate(_read())


def test_allowlist_counts_are_direct() -> None:
    tree = ast.parse(ALLOWLIST.read_text())
    assigned = None
    for node in ast.walk(tree):
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            for target in targets:
                if isinstance(target, ast.Name) and target.id == "ALLOWED_MARKET_ID_OCCURRENCE_LINES":
                    assigned = node.value
    assert isinstance(assigned, ast.Call)
    mapping = ast.literal_eval(assigned.args[0])
    paths = [
        "docs/prd/WEATHER-BOT-STAGE3-RETROSPECTIVE-SCORING-IMPLEMENTATION-READINESS-REVIEW-01.md",
        "tests/core/test_weather_bot_stage3_retrospective_scoring_implementation_readiness_review_01.py",
    ]
    for path in paths:
        assert mapping[path] == sum(1 for line in Path(path).read_text().splitlines() if "market_id" in line)


def test_oracles_are_literal_ast() -> None:
    tree = ast.parse(Path(__file__).read_text())
    names = {
        "EXPECTED_ASSIGNMENTS",
        "EXPECTED_PREREQUISITE_MATRIX",
        "EXPECTED_READINESS_GATE_MATRIX",
        "EXPECTED_REVIEW_DISPOSITION_MATRIX",
        "EXPECTED_CLOSED_SETS",
        "EXPECTED_PREDECESSOR_SECTION",
        "EXPECTED_CURRENT_READINESS_SECTION",
        "EXPECTED_IMPLEMENTATION_APPROVAL_SECTION",
        "EXPECTED_NON_APPROVALS_SECTION",
        "EXPECTED_ROUTING_SECTION",
        "EXPECTED_NEXT_TICKET_SECTION",
    }
    bad = (ast.ListComp, ast.DictComp, ast.SetComp, ast.GeneratorExp, ast.Call, ast.Name)
    found = set()
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id in names:
                    found.add(target.id)
                    assert not any(isinstance(child, bad) for child in ast.walk(node.value)), target.id
                    if target.id == "EXPECTED_ASSIGNMENTS":
                        assert isinstance(node.value, ast.List)
                        assert all(isinstance(elt, ast.Constant) and isinstance(elt.value, str) for elt in node.value.elts)
                    if target.id.startswith("EXPECTED_") and target.id.endswith("MATRIX"):
                        assert isinstance(node.value, ast.List)
                        assert all(isinstance(row, ast.List) for row in node.value.elts)
                    if target.id == "EXPECTED_CLOSED_SETS":
                        assert isinstance(node.value, ast.Dict)
                    if target.id.endswith("SECTION"):
                        assert isinstance(node.value, ast.Constant) and isinstance(node.value.value, str)
    assert found == names


def test_numeric_regex_examples() -> None:
    for token in ["90%", "1e-6", "12", ".5", "0.25"]:
        assert NUMERIC_TOKEN_RE.search(token)


def test_required_direct_mutations_are_rejected() -> None:
    base = _read()
    canonical_declaration = f"Canonical ID: {CANONICAL_ID}"
    assert base.splitlines()[0] == CANONICAL_ID
    assert base.count(canonical_declaration) == 1
    canonical_suffix_mutation = base.replace(canonical_declaration, f"{canonical_declaration}-X", 1)
    assert canonical_suffix_mutation.splitlines()[0] == CANONICAL_ID
    assert f"{canonical_declaration}-X" in canonical_suffix_mutation
    assert canonical_suffix_mutation != base
    _assert_rejected(canonical_suffix_mutation)

    prerequisite_row = (
        "| strict_oos_split_contract | "
        "WEATHER-BOT-STAGE3-STRICT-OOS-SPLIT-CONTRACT-PLANNING-01 | "
        "defines strict OOS split, cutoff, no-lookahead, and replay boundaries | "
        "present_and_coherent | "
        "block when future-information or split-scope protections are incomplete |"
    )
    duplicate_prerequisite = _duplicate_exact_table_row_in_section(
        base, "Exact prerequisite artifact matrix", prerequisite_row
    )
    _assert_critical_unchanged_except(base, duplicate_prerequisite, None)
    _assert_rejected(duplicate_prerequisite)

    readiness_row = (
        "| strict_oos_and_no_lookahead_defined | "
        "split, cutoff, as-of, publication-time, revision, finality, and future-information boundaries are explicit | "
        "passed | "
        "block because retrospective scoring could leak unavailable information |"
    )
    duplicate_readiness = _duplicate_exact_table_row_in_section(
        base, "Exact readiness-gate matrix", readiness_row
    )
    readiness_rows = _table(_sections(duplicate_readiness)["Exact readiness-gate matrix"])
    assert readiness_rows.count([cell.strip() for cell in readiness_row.strip().strip("|").split("|")]) == 2
    _assert_critical_unchanged_except(base, duplicate_readiness, None)
    _assert_rejected(duplicate_readiness)

    first_disposition_row = (
        "| ready_for_separate_implementation_approval_request | "
        "every required readiness gate passed and no missing, conflicting, superseded, or weakly enforced contract boundary remains | "
        "recommend one later separate explicit implementation-approval request; implementation remains unapproved |"
    )
    second_disposition_row = (
        "| needs_targeted_contract_refinement | "
        "the foundation is broadly coherent but one or more narrow document or static-test defects must be corrected | "
        "recommend one targeted refinement ticket and do not request implementation approval yet |"
    )
    swapped_dispositions = _swap_adjacent_exact_table_rows_in_section(
        base, "Exact review-disposition matrix", first_disposition_row, second_disposition_row
    )
    _assert_critical_unchanged_except(base, swapped_dispositions, None)
    _assert_rejected(swapped_dispositions)

    first_closed_set_block = (
        "- weather bot planning stage:\n"
        "  - weather_bot_stage3_retrospective_scoring_implementation_readiness_review"
    )
    second_closed_set_block = "- immediate predecessor pr:\n  - pr_365"
    swapped_closed_sets = _swap_exact_closed_set_blocks(
        base, first_closed_set_block, second_closed_set_block
    )
    swapped_closed_section = _sections(swapped_closed_sets)["Machine-checkable assignments"]
    swapped_closed_text, swapped_actual_text = swapped_closed_section.split("\n\nActual assignments:\n", 1)
    base_closed_text, base_actual_text = _sections(base)["Machine-checkable assignments"].split(
        "\n\nActual assignments:\n", 1
    )
    assert swapped_closed_text.index(second_closed_set_block) < swapped_closed_text.index(first_closed_set_block)
    assert sorted(swapped_closed_text.splitlines()) == sorted(base_closed_text.splitlines())
    assert swapped_actual_text == base_actual_text
    _assert_critical_unchanged_except(base, swapped_closed_sets, None)
    _assert_rejected(swapped_closed_sets)

    removed_prerequisite = _remove_exact_table_row_from_section(
        base, "Exact prerequisite artifact matrix", prerequisite_row
    )
    _assert_critical_unchanged_except(base, removed_prerequisite, None)
    _assert_rejected(removed_prerequisite)

    readiness_status_mutation = _replace_in_section(
        base,
        "Exact readiness-gate matrix",
        readiness_row,
        readiness_row.replace(" | passed | ", " | mystery_status | "),
    )
    base_status_cells = [cell.strip() for cell in readiness_row.strip().strip("|").split("|")]
    mutated_status_row = readiness_row.replace(" | passed | ", " | mystery_status | ")
    mutated_status_cells = [cell.strip() for cell in mutated_status_row.strip().strip("|").split("|")]
    assert len(mutated_status_cells) == 4
    assert base_status_cells[:2] == mutated_status_cells[:2]
    assert base_status_cells[2] == "passed"
    assert mutated_status_cells[2] == "mystery_status"
    assert base_status_cells[3] == mutated_status_cells[3]
    assert _sections(readiness_status_mutation)["Machine-checkable assignments"] == _sections(base)[
        "Machine-checkable assignments"
    ]
    _assert_critical_unchanged_except(base, readiness_status_mutation, None)
    _assert_rejected(readiness_status_mutation)


def test_mutations_are_rejected() -> None:
    base = _read()
    mutations = []
    mutations.append(base.replace(CANONICAL_ID, CANONICAL_ID + "-X", 1))
    mutations.append(base.replace("## Status and scope", f"Canonical ID: {CANONICAL_ID}\n\n## Status and scope", 1))
    mutations.append(base.replace("## Status and scope", "## TEMP", 1).replace("## Immediate predecessor and merge verification", "## Status and scope", 1).replace("## TEMP", "## Immediate predecessor and merge verification", 1))
    mutations.append(_replace_in_section(base, "Exact prerequisite artifact matrix", "| stage3_requirements | WEATHER-BOT-STAGE3-RETROSPECTIVE-PROBABILITY-SCORING-REQUIREMENTS-PLANNING-01 | controls the venue-defined target, strict OOS scoring objective, evidence categories, and non-approval boundary | present_and_coherent |", "| stage3_requirements | WEATHER-BOT-STAGE3-RETROSPECTIVE-PROBABILITY-SCORING-REQUIREMENTS-PLANNING-01 | controls the venue-defined target, strict OOS scoring objective, evidence categories, and non-approval boundary | missing |"))
    mutations.append(_replace_in_section(base, "Exact prerequisite artifact matrix", "| evidence_gate_decision_record_contract", "| stage3_requirements"))
    mutations.append(_replace_in_section(base, "Exact prerequisite artifact matrix", "stage3_requirements", "unknown_artifact_role"))
    mutations.append(_replace_in_section(base, "Exact readiness-gate matrix", "| predecessor_and_scope_integrity | PR #365 is the verified immediate predecessor and the review changes only the authorized documentation and static-test paths | passed |", "| predecessor_and_scope_integrity | PR #365 is the verified immediate predecessor and the review changes only the authorized documentation and static-test paths | failed |"))
    mutations.append(_replace_in_section(base, "Exact readiness-gate matrix", "| separate_approval_request_eligibility", "| predecessor_and_scope_integrity"))
    mutations.append(_replace_in_section(base, "Machine-checkable assignments", "- readiness gate status:\n  - passed\n  - caution", "- readiness gate status:\n  - mystery\n  - caution"))
    mutations.append(_replace_in_section(base, "Exact review-disposition matrix", "| ready_for_separate_implementation_approval_request", "| hold"))
    mutations.append(_replace_in_section(base, "Exact review-disposition matrix", "| ready_for_separate_implementation_approval_request |", "| conditional_ready |"))
    mutations.append(_replace_in_section(base, "Readiness decision rules and precedence", "1. blocked_pending_foundation_fix", "1. ready_for_separate_implementation_approval_request"))
    mutations.append(_replace_in_section(base, "Machine-checkable assignments", "Closed sets:\n- weather bot planning stage:", "Closed sets:\n- label confidence:"))
    mutations.append(_replace_in_section(base, "Machine-checkable assignments", "- label confidence:\n  - confirmed", "- label confidence:\n  - confirmed\n  - confirmed"))
    mutations.append(_replace_in_section(base, "Machine-checkable assignments", "- label confidence: confirmed", "- evidence status: stage3_implementation_readiness_review_recorded"))
    mutations.append(_replace_in_section(base, "Machine-checkable assignments", "- label confidence: confirmed", "- label confidence confirmed"))
    mutations.append(_replace_in_section(base, "Exact prerequisite artifact matrix", "| baseline_contracts", "| baseline_contracts_removed"))
    mutations.append(_replace_in_section(base, "Data corpus and evidence-sufficiency boundary", "sample sufficiency.", "sample sufficiency at 90% confidence."))
    mutations.append(_replace_in_section(base, "Implementation-scope decomposition requirements", "successor dependency.", "successor dependency with 1e-6 tolerance."))
    mutations.append(_replace_in_section(base, "Data corpus and evidence-sufficiency boundary", "Stage 3 evidence.", "Stage 3 evidence across 12 bins."))
    mutations.append(_replace_in_section(base, "Immediate predecessor and merge verification", f"ACTUAL_PR_365_MERGE_SHA: {ACTUAL_PR_365_MERGE_SHA}", f"ACTUAL_PR_365_MERGE_SHA: {PREVIEW_MERGE_SHA}"))
    mutations.append(_replace_in_section(base, "Immediate predecessor and merge verification", "Immediate predecessor: pr_365.", f"ACTUAL_PR_365_MERGE_SHA: {PREVIEW_MERGE_SHA}\n\nImmediate predecessor: pr_365."))
    mutations.append(_replace_in_section(base, "Immediate predecessor and merge verification", "Immediate predecessor: pr_365.", f"The actual PR #365 merge commit is {ACTUAL_PR_365_MERGE_SHA} and is reachable from current main for this repository state.\n\nImmediate predecessor: pr_365."))
    mutations.append(_replace_in_section(base, "Immediate predecessor and merge verification", "is not used as the actual merge commit", "is used as the actual merge commit"))
    mutations.append(_replace_in_section(base, "Current readiness determination", "does not establish sample sufficiency", "does establish sample sufficiency"))
    mutations.append(_replace_in_section(base, "Implementation-approval separation and interpretation boundaries", "is not implementation approval", "is implementation approval"))
    mutations.append(_replace_in_section(base, "Explicit non-approvals", "does not approve or create", "does approve and create"))
    mutations.append(_replace_in_section(base, "Canonical routing posture", "- outcome", "- outcome\n- market_id"))
    mutations.append(_replace_in_section(base, "Recommended next ticket", "WEATHER-BOT-STAGE3-RETROSPECTIVE-SCORING-IMPLEMENTATION-APPROVAL-REQUEST-01", "WEATHER-BOT-STAGE4-PAPER-SIMULATION-REQUEST-01"))
    mutations.append(_replace_in_section(base, "Machine-checkable assignments", REJECTION_SENTENCE, "Custom values are accepted."))
    mutations.append(_replace_in_section(base, "Machine-checkable assignments", REJECTION_SENTENCE, ""))
    for mutated in mutations:
        _assert_rejected(mutated)


def test_critical_mutations_preserve_unrelated_critical_sections() -> None:
    base = _read()
    cases = [
        ("Immediate predecessor and merge verification", "Immediate predecessor: pr_365.", "Immediate predecessor: pr_999."),
        ("Current readiness determination", "ready_for_separate_implementation_approval_request", "blocked_pending_foundation_fix"),
        ("Implementation-approval separation and interpretation boundaries", "no implementation work may begin", "implementation work may begin"),
        ("Explicit non-approvals", "does not approve", "does approve"),
        ("Canonical routing posture", "- outcome", "- outcome\n- market_id"),
        ("Recommended next ticket", "APPROVAL-REQUEST-01", "IMPLEMENTATION-01"),
    ]
    for section, anchor, replacement in cases:
        mutated = _replace_in_section(base, section, anchor, replacement)
        _assert_critical_unchanged_except(base, mutated, section)
        _assert_rejected(mutated)
