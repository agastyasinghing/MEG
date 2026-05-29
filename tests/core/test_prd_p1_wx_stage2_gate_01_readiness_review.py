from pathlib import Path
import re


PRD_PATH = Path("docs/prd/PRD-P1-WX-STAGE2-GATE-01_STAGE_2_READINESS_IMPLEMENTATION_GATE_REVIEW.md")
CANONICAL_ID = "PRD-P1-WX-STAGE2-GATE-01"
SOURCE_DOC_PATHS = {
    "standalone Weather Bot PRD": Path("docs/prd/PRD-P1-WX-STANDALONE_WEATHER_BOT_PRD.md"),
    "Stage 1 closeout": Path(
        "docs/prd/PRD-P1-WX-STAGE1-CLOSEOUT-01_STAGE_1_CLOSURE_GATES_AND_STAGE_2_READINESS_REVIEW.md"
    ),
    "Stage2-01": Path("docs/prd/PRD-P1-WX-STAGE2-01_SOURCE_COMPATIBLE_HISTORICAL_LABEL_DESIGN.md"),
    "Stage2-02": Path("docs/prd/PRD-P1-WX-STAGE2-02_POINT_IN_TIME_PROVENANCE_EXAMPLE_DESIGN.md"),
    "Stage2-03": Path("docs/prd/PRD-P1-WX-STAGE2-03_SOURCE_RESOLUTION_AUDIT_CHECKLIST_DESIGN.md"),
    "Stage2-04": Path("docs/prd/PRD-P1-WX-STAGE2-04_LABEL_USABILITY_BLOCKING_MATRIX_DESIGN.md"),
}
MACHINE_HEADING = "## Machine-checkable Stage 2 gate review assignments"

ALLOWED = {
    "gate review stage": {"stage_2_readiness_implementation_gate_review"},
    "stage 2 artifact status": {"present", "missing", "incomplete", "blocked"},
    "readiness gate status": {"passed", "caution", "failed", "not_applicable"},
    "implementation gate decision": {
        "do_not_start_implementation",
        "ready_for_separate_approval_request",
        "needs_schema_refinement",
        "blocked_pending_fix",
        "unclear",
    },
    "approval boundary status": {
        "unapproved",
        "separate_approval_required",
        "explicitly_out_of_scope",
        "blocked",
    },
    "next-ticket recommendation": {
        "stage_2_schema_refinement",
        "stage_2_explicit_implementation_approval_request",
        "targeted_fix",
        "hold",
    },
    "language/tooling posture": {
        "markdown_python_static_only",
        "implementation_language_deferred",
        "blocked_until_profiled_hot_path",
    },
    "evidence status": {
        "source_backed",
        "reviewer_inferred",
        "missing",
        "conflicting",
        "not_applicable",
    },
    "label confidence": {"confirmed", "unclear", "unknown"},
}

EXPECTED_ASSIGNMENT_LINES = [
    "- gate review stage: stage_2_readiness_implementation_gate_review",
    "- stage 2 artifact status: present",
    "- stage 2 artifact status: missing",
    "- stage 2 artifact status: incomplete",
    "- stage 2 artifact status: blocked",
    "- readiness gate status: passed",
    "- readiness gate status: caution",
    "- readiness gate status: failed",
    "- readiness gate status: not_applicable",
    "- implementation gate decision: do_not_start_implementation",
    "- implementation gate decision: ready_for_separate_approval_request",
    "- implementation gate decision: needs_schema_refinement",
    "- implementation gate decision: blocked_pending_fix",
    "- implementation gate decision: unclear",
    "- approval boundary status: unapproved",
    "- approval boundary status: separate_approval_required",
    "- approval boundary status: explicitly_out_of_scope",
    "- approval boundary status: blocked",
    "- next-ticket recommendation: stage_2_schema_refinement",
    "- next-ticket recommendation: stage_2_explicit_implementation_approval_request",
    "- next-ticket recommendation: targeted_fix",
    "- next-ticket recommendation: hold",
    "- language/tooling posture: markdown_python_static_only",
    "- language/tooling posture: implementation_language_deferred",
    "- language/tooling posture: blocked_until_profiled_hot_path",
    "- evidence status: source_backed",
    "- evidence status: reviewer_inferred",
    "- evidence status: missing",
    "- evidence status: conflicting",
    "- evidence status: not_applicable",
    "- label confidence: confirmed",
    "- label confidence: unclear",
    "- label confidence: unknown",
]

REQUIRED_TERMS = [
    "prd-p1-wx-stage2-gate-01",
    "standalone meg weather bot prd",
    "prd-p1-wx-stage1-closeout-01",
    "prd-p1-wx-stage2-01",
    "prd-p1-wx-stage2-02",
    "prd-p1-wx-stage2-03",
    "prd-p1-wx-stage2-04",
    "stage 2 readiness / implementation-gate review",
    "stage 2 artifact inventory",
    "stage 2 readiness gates",
    "implementation-gate decision rules",
    "gate review matrix",
    "approval boundary statement",
    "relationship to future implementation planning",
    "relationship to stage 3 scoring",
    "language/tooling posture",
    "machine-checkable stage 2 gate review assignments",
    "non-approval boundaries",
]

NON_APPROVAL_TERMS = [
    "provider integration",
    "connectors",
    "external api calls",
    "provider credentials",
    "config loading",
    "secret reading",
    "data ingestion",
    "historical labels",
    "historical label implementation",
    "json/yaml/csv/parquet fixtures",
    "forecast pulls",
    "model scoring",
    "probability scoring",
    "backtesting",
    "paper simulation",
    "runtime observation",
    "trading",
    "order placement",
    "autonomy",
    "c++/rust runtime components",
]

FORBIDDEN_APPROVAL_PHRASES = [
    "implementation is approved",
    "historical label implementation is approved",
    "data ingestion is approved",
    "provider integration is approved",
    "connectors are approved",
    "connector implementation is approved",
    "external api calls are approved",
    "provider credentials are approved",
    "config loading is approved",
    "secret reading is approved",
    "forecast pulls are approved",
    "model scoring is approved",
    "probability scoring is approved",
    "scoring is approved",
    "backtesting is approved",
    "paper simulation is approved",
    "runtime observation is approved",
    "trading is approved",
    "order placement is approved",
    "autonomy is approved",
    "c++ runtime components are approved",
    "rust runtime components are approved",
]

FORBIDDEN_EXAMPLES = [
    "passed/caution",
    "present/incomplete",
    "do_not_start_implementation/ready_for_separate_approval_request",
    "stage_2_schema_refinement/stage_2_explicit_implementation_approval_request",
    "source_backed/reviewer_inferred",
    "confirmed/unclear",
    "unapproved/separate_approval_required",
    "partial",
    "mixed",
    "likely_confirmed",
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
    "ready_for_runtime",
    "ready_for_trading",
    "implementation_ready",
    "ingestion_ready",
    "scoring_ready",
    "simulation_ready",
    "runtime_ready",
    "trading_ready",
    "approved_for_implementation",
]

ASSIGNMENT_PATTERN = re.compile(
    r"^\s*-\s*(gate review stage|stage 2 artifact status|readiness gate status|"
    r"implementation gate decision|approval boundary status|next-ticket recommendation|"
    r"language/tooling posture|evidence status|label confidence):\s*([a-z0-9_/-]+)\s*$",
    flags=re.MULTILINE,
)


def _text() -> str:
    assert PRD_PATH.exists(), f"Missing PRD document: {PRD_PATH}"
    return PRD_PATH.read_text(encoding="utf-8")


def _machine_section(text: str) -> str:
    pattern = re.compile(rf"^{re.escape(MACHINE_HEADING)}\s*$", flags=re.MULTILINE)
    match = pattern.search(text)
    assert match, f"Missing exact machine-checkable section heading: {MACHINE_HEADING}"
    after_heading = text[match.end() :]
    next_heading = re.search(r"^##\s+", after_heading, flags=re.MULTILINE)
    return after_heading[: next_heading.start()] if next_heading else after_heading


def test_stage2_gate_prd_exists_and_references_required_sources() -> None:
    text = _text()
    lower = text.lower()

    assert CANONICAL_ID in text
    missing = [term for term in REQUIRED_TERMS if term not in lower]
    assert not missing, f"Missing required terms: {missing}"

    missing_source_docs = [name for name, path in SOURCE_DOC_PATHS.items() if not path.exists()]
    assert not missing_source_docs, f"Missing source-of-truth docs: {missing_source_docs}"

    missing_source_filenames = [
        path.name for path in SOURCE_DOC_PATHS.values() if path.name.lower() not in lower
    ]
    assert not missing_source_filenames, f"Missing exact source document filenames: {missing_source_filenames}"


def test_non_approval_boundaries_and_forbidden_approval_phrases() -> None:
    lower = _text().lower()

    missing = [term for term in NON_APPROVAL_TERMS if term not in lower]
    assert not missing, f"Missing non-approval boundary terms: {missing}"

    bad = [phrase for phrase in FORBIDDEN_APPROVAL_PHRASES if phrase in lower]
    assert not bad, f"Forbidden approval language found: {bad}"


def test_forbidden_examples_are_documented_but_not_globally_rejected() -> None:
    lower = _text().lower()

    missing = [example for example in FORBIDDEN_EXAMPLES if example not in lower]
    assert not missing, f"Forbidden examples section missing examples: {missing}"


def test_machine_checkable_assignments_are_section_scoped_and_allowed() -> None:
    section = _machine_section(_text())
    assert "## Approval boundary statement" not in section
    assert "approval boundary statement" not in section.lower()
    parsed: dict[str, list[str]] = {field: [] for field in ALLOWED}

    for match in ASSIGNMENT_PATTERN.finditer(section):
        field = match.group(1)
        value = match.group(2)
        parsed[field].append(value)

    missing_fields = [field for field, values in parsed.items() if not values]
    assert not missing_fields, f"No machine-checkable assignments found for: {missing_fields}"

    for expected_line in EXPECTED_ASSIGNMENT_LINES:
        assert expected_line in section

    for field, values in parsed.items():
        bad = sorted({value for value in values if value not in ALLOWED[field]})
        assert not bad, f"Invalid parsed values for {field}: {bad}"

        missing_values = sorted(ALLOWED[field] - set(values))
        assert not missing_values, f"Machine-checkable assignments missing {field} values: {missing_values}"

    actual_assignment_count = len(ASSIGNMENT_PATTERN.findall(section))
    assert actual_assignment_count == len(EXPECTED_ASSIGNMENT_LINES)
