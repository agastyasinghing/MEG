from pathlib import Path
import re


PRD_PATH = Path("docs/prd/PRD-P1-WX-STAGE1-03_REVIEWER_CHECKLIST_ADJUDICATION_PROTOCOL.md")

ALLOWED = {
    "adjudication stage": {"stage_1_reviewer_adjudication"},
    "checklist item category": {
        "settlement_rule",
        "resolver_source",
        "station_location",
        "time_window",
        "threshold_unit",
        "measurement_method",
        "revision_finality",
        "classification_authority",
        "source_compatibility",
        "trap_review",
        "false_edge_review",
        "canonical_mapping",
        "evidence_quality",
        "non_approval_boundary",
        "reviewer_note",
        "other_unclear",
    },
    "review decision": {"pass", "caution", "block", "needs_more_evidence", "not_applicable"},
    "adjudication outcome": {"accepted", "revised", "escalated", "blocked", "deferred"},
    "evidence status": {"source_backed", "reviewer_inferred", "missing", "conflicting", "not_applicable"},
    "disagreement status": {
        "no_disagreement",
        "minor_disagreement",
        "material_disagreement",
        "unresolved_disagreement",
    },
    "label confidence": {"confirmed", "unclear", "unknown"},
    "review posture": {"informational", "review_only", "blocked"},
    "reviewer workflow state": {
        "unreviewed",
        "caution_under_review",
        "blocking_under_review",
        "reviewed_pass",
        "reviewed_caution",
        "reviewed_block",
    },
}

EXPECTED_ASSIGNMENT_LINES = [
    "- adjudication stage: stage_1_reviewer_adjudication",
    "- checklist item category: settlement_rule",
    "- checklist item category: resolver_source",
    "- checklist item category: station_location",
    "- checklist item category: time_window",
    "- checklist item category: threshold_unit",
    "- checklist item category: measurement_method",
    "- checklist item category: revision_finality",
    "- checklist item category: classification_authority",
    "- checklist item category: source_compatibility",
    "- checklist item category: trap_review",
    "- checklist item category: false_edge_review",
    "- checklist item category: canonical_mapping",
    "- checklist item category: evidence_quality",
    "- checklist item category: non_approval_boundary",
    "- checklist item category: reviewer_note",
    "- checklist item category: other_unclear",
    "- review decision: pass",
    "- review decision: caution",
    "- review decision: block",
    "- review decision: needs_more_evidence",
    "- review decision: not_applicable",
    "- adjudication outcome: accepted",
    "- adjudication outcome: revised",
    "- adjudication outcome: escalated",
    "- adjudication outcome: blocked",
    "- adjudication outcome: deferred",
    "- evidence status: source_backed",
    "- evidence status: reviewer_inferred",
    "- evidence status: missing",
    "- evidence status: conflicting",
    "- evidence status: not_applicable",
    "- disagreement status: no_disagreement",
    "- disagreement status: minor_disagreement",
    "- disagreement status: material_disagreement",
    "- disagreement status: unresolved_disagreement",
    "- label confidence: confirmed",
    "- label confidence: unclear",
    "- label confidence: unknown",
    "- review posture: informational",
    "- review posture: review_only",
    "- review posture: blocked",
    "- reviewer workflow state: unreviewed",
    "- reviewer workflow state: caution_under_review",
    "- reviewer workflow state: blocking_under_review",
    "- reviewer workflow state: reviewed_pass",
    "- reviewer workflow state: reviewed_caution",
    "- reviewer workflow state: reviewed_block",
]



def _text() -> str:
    assert PRD_PATH.exists(), f"Missing PRD file: {PRD_PATH}"
    return PRD_PATH.read_text(encoding="utf-8")


def _machine_section(text: str) -> str:
    marker = "## Machine-checkable reviewer-adjudication field assignments"
    assert text.count(marker) == 1, "Expected exactly one machine-checkable section heading"
    start = text.find(marker)
    after_start = text[start + len(marker) :]
    next_heading = re.search(r"^##\s+", after_start, flags=re.MULTILINE)
    return after_start if next_heading is None else after_start[: next_heading.start()]


def test_stage1_03_prd_presence_and_core_terms() -> None:
    text = _text().lower()
    required = [
        "prd-p1-wx-stage1-03",
        "standalone meg weather bot prd",
        "prd-p1-wx-stage1-01",
        "prd-p1-wx-stage1-02",
        "stage 1",
        "reviewer checklist/adjudication protocol",
        "source-defined settlement object",
        "reviewer checklist",
        "adjudication workflow",
        "decision rules",
        "disagreement and escalation protocol",
        "static adjudication template",
        "relationship to manual labels and trap labels",
        "machine-checkable reviewer-adjudication field assignments",
        "non-approval boundaries",
        "prd-p1-wx-stage1-04",
    ]
    missing = [token for token in required if token not in text]
    assert not missing, f"Missing required terms: {missing}"


def test_closed_set_values_are_documented() -> None:
    text = _text().lower()
    missing = []
    for field, allowed_values in ALLOWED.items():
        if field not in text:
            missing.append(field)
        missing.extend(sorted(value for value in allowed_values if value not in text))
    assert not missing, f"Missing closed-set field names or values: {missing}"


def test_machine_checkable_section_contains_exact_assignment_lines() -> None:
    section = _machine_section(_text())
    section_lines = [line.strip() for line in section.splitlines() if line.strip()]
    assert section_lines == EXPECTED_ASSIGNMENT_LINES


def test_machine_checkable_assignments_use_only_allowed_values() -> None:
    section = _machine_section(_text()).lower()

    for field, allowed_values in ALLOWED.items():
        pattern = rf"^\s*-\s*{re.escape(field)}:\s*([a-z0-9_/-]+)\s*$"
        values = [m.group(1).strip() for m in re.finditer(pattern, section, flags=re.MULTILINE)]
        assert values, f"No machine-checkable assignments found for {field}"

        bad = sorted({v for v in values if v not in allowed_values})
        assert not bad, f"Invalid parsed values for {field}: {bad}"

        missing = sorted(allowed_values - set(values))
        assert not missing, f"Missing machine-checkable values for {field}: {missing}"


def test_forbidden_examples_do_not_break_section_limited_parser() -> None:
    text = _text().lower()
    section = _machine_section(_text()).lower()
    forbidden_examples = [
        "pass/caution",
        "caution/block",
        "accepted/revised",
        "source_backed/reviewer_inferred",
        "no_disagreement/minor_disagreement",
        "confirmed/unclear",
        "review_only/blocked",
        "partial",
        "mixed",
        "likely",
        "maybe",
        "approved",
        "configured",
        "available",
        "trade_ready",
        "auto_execute",
        "autonomous",
        "live",
        "production",
        "provider_ready",
        "model_ready",
        "backtest_ready",
        "ready_for_ingestion",
        "ready_for_scoring",
    ]
    missing_examples = [example for example in forbidden_examples if example not in text]
    assert not missing_examples, f"Missing forbidden examples: {missing_examples}"

    parsed_values = []
    for field in ALLOWED:
        pattern = rf"^\s*-\s*{re.escape(field)}:\s*([a-z0-9_/-]+)\s*$"
        parsed_values.extend(m.group(1).strip() for m in re.finditer(pattern, section, flags=re.MULTILINE))
    bad = sorted(set(parsed_values) & set(forbidden_examples))
    assert not bad, f"Forbidden examples used as parsed actual values: {bad}"


def test_non_approval_boundary_terms_present() -> None:
    text = _text().lower()
    required_terms = [
        "provider integration",
        "connectors",
        "external api calls",
        "provider credentials",
        "config loading",
        "secret reading",
        "data ingestion",
        "historical labels",
        "seed examples",
        "forecast pulls",
        "model scoring",
        "probability scoring",
        "backtesting",
        "paper simulation",
        "runtime observation",
        "trading",
        "order placement",
        "autonomy",
    ]
    missing = [term for term in required_terms if term not in text]
    assert not missing, f"Missing non-approval boundary terms: {missing}"


def test_non_approval_boundaries_do_not_use_approval_phrasing() -> None:
    text = _text().lower()
    forbidden_approval_phrases = [
        "provider integration is approved",
        "connectors are approved",
        "connector implementation is approved",
        "external api calls are approved",
        "provider credentials are approved",
        "config loading is approved",
        "secret reading is approved",
        "data ingestion is approved",
        "historical labels are approved",
        "seed examples are approved",
        "forecast pulls are approved",
        "model scoring is approved",
        "probability scoring is approved",
        "backtesting is approved",
        "paper simulation is approved",
        "runtime observation is approved",
        "trading is approved",
        "order placement is approved",
        "autonomy is approved",
    ]
    bad = [phrase for phrase in forbidden_approval_phrases if phrase in text]
    assert not bad, f"Forbidden approval language found: {bad}"
