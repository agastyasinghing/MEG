"""Static/preflight checks for PRD-0A/0B decision gate document."""

from pathlib import Path

DOC_PATH = Path("docs/prd/PRD-0A-0B_DECISION_GATE.md")
MASTER_PRD_PATH = Path("MEG_MASTER_PRD_v4.1_patched.md")

PHASE_0A_DELIVERABLES = [
    "canonical identifier migration",
    "event schemas + Redis bus contracts",
    "CLOB market-state cache writer",
    "CLOB user-stream service",
    "Telegram proposal queue infrastructure",
    "Postgres journal schema/writers",
    "paper execution simulator",
    "heartbeat emitter",
    "risk envelope skeleton",
]

PHASE_0B_DELIVERABLES = [
    "DuckDB + Parquet + Becker setup",
    "raw partition access / local-only archive read posture",
    "Bronze/Silver normalization views",
    "data dictionary",
    "seven sanity queries",
    "query latency gate",
    "fixture/Bronze foundation from Phase 1R",
]

DECISION_RULES = [
    "If Phase 0A shared rail is unknown/uncertain, do not start weather implementation.",
    "If Phase 0B research lake is planned/static only, start PRD-0B-IMPL-01 before claiming Phase 0B implementation.",
    "If both 0A and 0B are uncertain, start a local-only 0B smoke in parallel with scoped 0A audit prep.",
    "If 0B local smoke requires no runtime rail and no committed data, it may proceed before full 0A completion.",
    "If any work requires runtime proposals, paper execution, Telegram approval, Postgres journal, or risk gates, it must wait for 0A audit/repair.",
    "Do not begin master PRD Phase 1 weather paper engine until 0A/0B readiness is explicitly resolved.",
]


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_decision_gate_doc_exists() -> None:
    assert DOC_PATH.exists()


def test_doc_contains_required_posture_and_outcome() -> None:
    text = _read(DOC_PATH)
    checks = [
        "docs/static-preflight only",
        "Phase 1R-07 corrected naming drift",
        "PRD Phase 0A readiness check",
        "PRD Phase 0B readiness check",
        "Allowed confidence vocabulary",
        "Allowed status vocabulary",
        "Start **PRD-0B-IMPL-01**",
        "start **PRD-0A-AUDIT-01**",
        "Do not start weather paper engine yet.",
        "Language/tooling note",
        "Explicit non-approvals",
    ]
    for item in checks:
        assert item in text


def test_doc_lists_all_phase_0a_and_0b_deliverables_and_rules() -> None:
    text = _read(DOC_PATH)
    for deliverable in PHASE_0A_DELIVERABLES + PHASE_0B_DELIVERABLES:
        assert deliverable in text
    for rule in DECISION_RULES:
        assert rule in text


def test_master_prd_contains_phase_references() -> None:
    text = _read(MASTER_PRD_PATH)
    assert "Phase 0A" in text and "Shared rail" in text
    assert "Phase 0B" in text and "Research lake" in text
    assert "Phase 1" in text and "weather paper engine" in text
