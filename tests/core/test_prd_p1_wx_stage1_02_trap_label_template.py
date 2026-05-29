from pathlib import Path
import re


PRD_PATH = Path("docs/prd/PRD-P1-WX-STAGE1-02_STATIC_TRAP_LABEL_FIXTURE_TEMPLATE.md")

ALLOWED = {
    "trap label stage": {"stage_1_static_trap_label"},
    "trap source": {
        "market_wording",
        "resolution_source",
        "provider_source",
        "location_station",
        "time_window",
        "threshold_unit",
        "measurement_method",
        "data_revision",
        "venue_discretion",
        "external_event_classification",
        "market_microstructure",
        "validation_provenance",
        "other_unclear",
    },
    "trap severity": {"caution", "blocking"},
    "trap action": {
        "reviewer_note",
        "caution_flag",
        "block_mapping",
        "block_actionability",
        "needs_adjudication",
    },
    "false-edge risk": {
        "none_identified",
        "possible_false_edge",
        "likely_false_edge",
        "blocking_false_edge",
        "unclear",
    },
    "canonical mapping impact": {
        "no_material_impact",
        "mapping_unclear",
        "near_equivalence_only",
        "non_equivalent",
        "mapping_blocked",
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


def _text() -> str:
    assert PRD_PATH.exists(), f"Missing PRD file: {PRD_PATH}"
    return PRD_PATH.read_text(encoding="utf-8")


def _machine_section(text: str) -> str:
    marker = "## Machine-checkable trap-label field assignments"
    assert text.count(marker) == 1, "Expected exactly one machine-checkable section heading"
    start = text.find(marker)
    next_heading = text.find("\n## ", start + len(marker))
    return text[start:] if next_heading == -1 else text[start:next_heading]


def test_stage1_02_prd_presence_and_core_terms() -> None:
    text = _text().lower()
    required = [
        "prd-p1-wx-stage1-02",
        "standalone meg weather bot prd",
        "prd-p1-wx-stage1-01",
        "stage 1",
        "source-defined settlement object",
        "static trap-label fixture/template",
        "trap-label reviewer checklist",
        "trap-label to manual-label relationship",
        "machine-checkable trap-label field assignments",
        "false-edge risk",
        "canonical mapping impact",
        "non-approval boundaries",
        "prd-p1-wx-stage1-03",
        "prd-p1-wx-stage1-04",
    ]
    missing = [token for token in required if token not in text]
    assert not missing, f"Missing required terms: {missing}"


def test_machine_checkable_assignments_use_only_allowed_values() -> None:
    section = _machine_section(_text()).lower()

    for field, allowed_values in ALLOWED.items():
        pattern = rf"^- {re.escape(field)}:\s*([a-z0-9_/-]+)\s*$"
        values = [m.group(1).strip() for m in re.finditer(pattern, section, flags=re.MULTILINE)]
        assert values, f"No machine-checkable assignments found for {field}"

        bad = sorted({v for v in values if v not in allowed_values})
        assert not bad, f"Invalid parsed values for {field}: {bad}"

        missing = sorted(allowed_values - set(values))
        assert not missing, f"Missing machine-checkable values for {field}: {missing}"


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
