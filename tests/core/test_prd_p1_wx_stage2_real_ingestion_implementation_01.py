"""Static checks for the offline real-ingestion implementation skeleton PRD."""
from __future__ import annotations

import ast
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PRD_REL = "docs/prd/PRD-P1-WX-STAGE2-REAL-INGESTION-IMPLEMENTATION-01_OFFLINE_REAL_INGESTION_IMPLEMENTATION_SKELETON.md"
MODULE_REL = "meg/weather/stage2/real_ingestion.py"
UNIT_TEST_REL = "tests/unit/weather/stage2/test_real_ingestion.py"
THIS_TEST_REL = "tests/core/test_prd_p1_wx_stage2_real_ingestion_implementation_01.py"
CANONICAL_ID = "PRD-P1-WX-STAGE2-REAL-INGESTION-IMPLEMENTATION-01"


def _read(rel_path: str) -> str:
    return (REPO_ROOT / rel_path).read_text(encoding="utf-8")


def test_prd_exists_and_contains_canonical_id() -> None:
    path = REPO_ROOT / PRD_REL
    assert path.is_file()
    text = _read(PRD_REL)
    assert CANONICAL_ID in text


def test_prd_references_approval_plan_and_closeout_prds() -> None:
    text = _read(PRD_REL)
    for required in (
        "PRD-P1-WX-STAGE2-REAL-INGESTION-PLANNING-APPROVAL-01",
        "PRD-P1-WX-STAGE2-REAL-INGESTION-PLAN-01",
        "PRD-P1-WX-STAGE2-REAL-INGESTION-PLAN-CLOSEOUT-01",
        "PRD-P1-WX-STAGE2-REAL-INGESTION-IMPLEMENTATION-APPROVAL-01",
        "PRD-P1-WX-STAGE2-INGESTION-IMPLEMENTATION-CLOSEOUT-01",
    ):
        assert required in text


def test_prd_states_offline_implementation_only_boundary() -> None:
    text = _read(PRD_REL)
    for required in (
        "offline implementation skeleton only",
        "caller-supplied source descriptor validation only",
        "already-reviewed source descriptor values only",
        "does not create production ingestion behavior",
    ):
        assert required in text


def test_prd_states_non_approval_boundaries() -> None:
    text = _read(PRD_REL)
    required_phrases = (
        "no provider/API connectors are implemented",
        "no source fetching is implemented",
        "no external API calls are implemented",
        "no secrets/config loading is implemented",
        "no forecast pulls are implemented",
        "no scraping/polling/streaming/scheduling/jobs are implemented",
        "no scoring/back-testing/runtime/trading/order-placement/autonomy is implemented",
        "Future provider connector implementation requires later approval",
        "Future source fetching requires later approval",
        "Future scoring/back-testing/runtime/trading requires later approval",
    )
    for phrase in required_phrases:
        assert phrase in text


def test_no_positive_approval_drift_appears() -> None:
    text = _read(PRD_REL).lower()
    forbidden_positive_phrases = (
        "approved for real ingestion",
        "approved for provider",
        "approved for source fetching",
        "approved for scoring",
        "approved for runtime",
        "approved for trading",
        "ready for production",
        "production ready",
    )
    offenders = [phrase for phrase in forbidden_positive_phrases if phrase in text]
    assert offenders == []


def test_no_forbidden_implementation_tokens_in_source_or_docs() -> None:
    forbidden = (
        "requests" + ".",
        "httpx" + ".",
        "aio" + "http",
        "urllib" + ".request",
        "os" + ".environ",
        "load" + "_dot" + "env",
        "dot" + "env",
        "api" + "_key",
        "secret" + "_key",
        "weather" + "_api" + "_key",
        "read" + "_csv",
        "to" + "_csv",
        "json" + ".load",
        "duck" + "db",
        "pan" + "das",
        "pol" + "ars",
        "sql" + "alchemy",
        "fast" + "api",
        "fla" + "sk",
    )
    scanned = {
        PRD_REL: _read(PRD_REL),
        MODULE_REL: _read(MODULE_REL),
    }
    offenders = {
        rel_path: [token for token in forbidden if token.lower() in text.lower()]
        for rel_path, text in scanned.items()
    }
    assert offenders == {PRD_REL: [], MODULE_REL: []}


def test_unit_and_static_tests_keep_forbidden_literals_constructed_only() -> None:
    for rel_path in (UNIT_TEST_REL, THIS_TEST_REL):
        tree = ast.parse(_read(rel_path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                lowered = node.value.lower()
                assert ("requests" + ".") not in lowered
                assert ("httpx" + ".") not in lowered
                assert ("urllib" + ".request") not in lowered
                assert ("json" + ".load") not in lowered
                assert ("api" + "_key") not in lowered
                assert ("secret" + "_key") not in lowered
