from pathlib import Path
import re


PRD_PATH = Path(
    "docs/prd/PRD-P1-WX-STAGE1-CLOSEOUT-01_STAGE_1_CLOSURE_GATES_AND_STAGE_2_READINESS_REVIEW.md"
)
CANONICAL_ID = "PRD-P1-WX-STAGE1-CLOSEOUT-01"
FORBIDDEN_CANONICAL_ID_ALIAS_PATTERNS = [
    r"(?<!PRD-P1-)WX-STAGE1-CLOSEOUT-01",
    r"P1-WX-S1-CLOSEOUT-01",
    r"PRD-WX-STAGE1-CLOSEOUT-01",
    r"PRD-P1-WEATHER-STAGE1-CLOSEOUT-01",
    r"PRD-P1-WX-STAGE-1-CLOSEOUT-01",
]

ALLOWED = {
    "closeout stage": {"stage_1_closeout_review"},
    "stage 1 artifact status": {"present", "missing", "incomplete", "blocked"},
    "closure gate status": {"passed", "caution", "failed", "not_applicable"},
    "coverage decision": {
        "sufficient_for_stage_2_design",
        "needs_stage_1_expansion",
        "blocked_pending_fix",
        "unclear",
    },
    "stage 2 readiness posture": {
        "not_ready",
        "ready_for_design_ticket",
        "blocked",
        "unclear",
    },
    "next-ticket recommendation": {
        "stage_1_expansion",
        "stage_2_historical_label_design",
        "targeted_fix",
        "hold",
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
    "- closeout stage: stage_1_closeout_review",
    "- stage 1 artifact status: present",
    "- stage 1 artifact status: missing",
    "- stage 1 artifact status: incomplete",
    "- stage 1 artifact status: blocked",
    "- closure gate status: passed",
    "- closure gate status: caution",
    "- closure gate status: failed",
    "- closure gate status: not_applicable",
    "- coverage decision: sufficient_for_stage_2_design",
    "- coverage decision: needs_stage_1_expansion",
    "- coverage decision: blocked_pending_fix",
    "- coverage decision: unclear",
    "- stage 2 readiness posture: not_ready",
    "- stage 2 readiness posture: ready_for_design_ticket",
    "- stage 2 readiness posture: blocked",
    "- stage 2 readiness posture: unclear",
    "- next-ticket recommendation: stage_1_expansion",
    "- next-ticket recommendation: stage_2_historical_label_design",
    "- next-ticket recommendation: targeted_fix",
    "- next-ticket recommendation: hold",
    "- evidence status: source_backed",
    "- evidence status: reviewer_inferred",
    "- evidence status: missing",
    "- evidence status: conflicting",
    "- evidence status: not_applicable",
    "- label confidence: confirmed",
    "- label confidence: unclear",
    "- label confidence: unknown",
]

FORBIDDEN_EXAMPLES = [
    "present/incomplete",
    "passed/caution",
    "ready_for_design_ticket/blocked",
    "stage_1_expansion/stage_2_historical_label_design",
    "source_backed/reviewer_inferred",
    "confirmed/unclear",
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
    "ready_for_runtime",
    "ready_for_trading",
    "c++",
    "rust",
    "cpp_runtime",
    "rust_runtime",
    "production_ready",
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
    "provider integration is approved",
    "connectors are approved",
    "connector implementation is approved",
    "external api calls are approved",
    "provider credentials are approved",
    "config loading is approved",
    "secret reading is approved",
    "data ingestion is approved",
    "historical labels are approved",
    "forecast pulls are approved",
    "model scoring is approved",
    "probability scoring is approved",
    "backtesting is approved",
    "paper simulation is approved",
    "runtime observation is approved",
    "trading is approved",
    "order placement is approved",
    "autonomy is approved",
    "c++ runtime components are approved",
    "rust runtime components are approved",
]


def _text() -> str:
    assert PRD_PATH.exists(), f"Missing PRD file: {PRD_PATH}"
    return PRD_PATH.read_text(encoding="utf-8")


def _machine_section(text: str) -> str:
    marker = "## Machine-checkable Stage 1 closeout assignments"
    assert text.count(marker) == 1, "Expected exactly one machine-checkable closeout section"
    start = text.find(marker)
    after_start = text[start + len(marker) :]
    next_heading = re.search(r"^##\s+", after_start, flags=re.MULTILINE)
    return after_start if next_heading is None else after_start[: next_heading.start()]


def test_exact_canonical_id_is_present_without_aliases() -> None:
    text = _text()
    assert CANONICAL_ID in text
    aliases = [
        pattern
        for pattern in FORBIDDEN_CANONICAL_ID_ALIAS_PATTERNS
        if re.search(pattern, text)
    ]
    assert not aliases, f"Forbidden canonical ID aliases found: {aliases}"


def test_closeout_prd_presence_and_core_terms() -> None:
    text = _text().lower()
    required = [
        CANONICAL_ID.lower(),
        "standalone meg weather bot prd",
        "prd-p1-wx-stage1-01",
        "prd-p1-wx-stage1-02",
        "prd-p1-wx-stage1-03",
        "prd-p1-wx-stage1-04",
        "stage 1 closeout/readiness review only",
        "stage 1 artifact inventory",
        "stage 1 closure gates",
        "stage 1 coverage review",
        "stage 2 readiness review",
        "language/tooling posture",
        "advanced math posture",
        "machine-checkable stage 1 closeout assignments",
        "non-approval boundaries",
    ]
    missing = [token for token in required if token not in text]
    assert not missing, f"Missing required terms: {missing}"


def test_stage_ladder_and_non_approval_scope_are_documented() -> None:
    text = _text().lower()
    required = [
        "stage 0",
        "stage 1",
        "stage 2",
        "stage 3",
        "stage 4",
        "stage 5",
        "stage 6",
        "stage 7",
        "source-compatible historical-label design",
        "stage 2 design only",
        "does not approve",
    ]
    missing = [token for token in required if token not in text]
    assert not missing, f"Missing stage ladder or non-approval scope terms: {missing}"


def test_non_approval_boundary_terms_are_present_without_approval_language() -> None:
    text = _text().lower()
    missing = [term for term in NON_APPROVAL_TERMS if term not in text]
    assert not missing, f"Missing non-approval boundary terms: {missing}"

    bad_approvals = [phrase for phrase in FORBIDDEN_APPROVAL_PHRASES if phrase in text]
    assert not bad_approvals, f"Forbidden approval language found: {bad_approvals}"


def test_forbidden_examples_are_documented_but_not_globally_rejected() -> None:
    text = _text().lower()
    missing = [example for example in FORBIDDEN_EXAMPLES if example not in text]
    assert not missing, f"Forbidden examples section missing examples: {missing}"


def test_machine_checkable_section_contains_expected_assignment_lines() -> None:
    section_lines = [
        line.strip()
        for line in _machine_section(_text()).splitlines()
        if line.strip()
    ]
    missing = [line for line in EXPECTED_ASSIGNMENT_LINES if line not in section_lines]
    assert not missing, f"Missing expected assignment lines: {missing}"


def test_machine_checkable_values_are_allowed_and_section_scoped() -> None:
    section = _machine_section(_text())
    for field, allowed_values in ALLOWED.items():
        pattern = rf"^\s*-\s*{re.escape(field)}:\s*([a-z0-9_/-]+)\s*$"
        values = [
            match.group(1).strip()
            for match in re.finditer(pattern, section, flags=re.MULTILINE)
        ]
        assert values, f"No machine-checkable assignments found for {field}"
        bad = sorted({value for value in values if value not in allowed_values})
        assert not bad, f"Invalid parsed values for {field}: {bad}"
        missing_values = sorted(allowed_values - set(values))
        assert not missing_values, f"Missing allowed values for {field}: {missing_values}"


def test_machine_checkable_section_has_no_unrecognized_assignment_fields() -> None:
    section = _machine_section(_text())
    parsed_fields = []
    for match in re.finditer(r"^\s*-\s*([a-z0-9 -]+):\s*([a-z0-9_/-]+)\s*$", section, flags=re.MULTILINE):
        parsed_fields.append(match.group(1).strip())
    unknown = sorted({field for field in parsed_fields if field not in ALLOWED})
    assert not unknown, f"Unknown machine-checkable assignment fields: {unknown}"
