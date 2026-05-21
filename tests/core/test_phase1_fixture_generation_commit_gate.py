from __future__ import annotations

from pathlib import Path

from scripts.phase1 import fixture_derivation_safety_shell as safety_shell
from tests.core import test_phase1_fixture_manifest_provenance_contract as manifest_contract

REPO_ROOT = Path(__file__).resolve().parents[2]
GATE_DOC = REPO_ROOT / "docs/phase1/1-05_TINY_FIXTURE_GENERATION_COMMIT_GATE.md"

REQUIRED_FAMILIES = {
    "kalshi_markets_tiny",
    "kalshi_trades_tiny",
    "poly_markets_tiny",
    "poly_clob_trades_tiny",
    "poly_blocks_tiny",
    "poly_legacy_fpmm_trades_tiny",
    "poly_fpmm_collateral_lookup_tiny",
}

REQUIRED_EVIDENCE_ITEMS = {
    "phase 1-04 dry-run manifest json",
    "source_manifest_ref",
    "source_repo_ref",
    "source_repo_commit",
    "source_archive_ref",
    "approved local archive root",
    "source relative path list",
    "output relative path list",
    "selected stable keys",
    "row-selection rule",
    "selected row/object counts",
    "source file checksums",
    "generated fixture checksums",
    "script version",
    "parser version",
    "derivation timestamp",
    "reviewer reference",
    "no absolute path evidence",
    "no secret/pii evidence",
    "no `.duckdb`/report/archive artifact evidence",
    "ci test command evidence",
}

REQUIRED_BLOCKERS = {
    "phase 1-04 dry-run manifest missing",
    "fewer/more than seven planned families",
    "outside approved source families",
    "outside `fixtures/phase1/`",
    "outside `1..5`",
    "source checksum missing before derivation",
    "generated checksum missing before commit",
    "absolute local archive path",
    "secrets/api keys/private pii",
    "`.duckdb`/report/archive/external repo artifact",
    "appledouble source selected",
    "unresolved license/provenance posture",
    "reviewer approval missing",
    "ci failing",
    "execution/order/live/autonomy posture enabled",
}


def _doc_text() -> str:
    return GATE_DOC.read_text(encoding="utf-8")


def test_gate_doc_exists() -> None:
    assert GATE_DOC.exists()


def test_doc_states_no_generation_or_commit_in_this_ticket() -> None:
    text = _doc_text().lower()
    assert "does **not** generate, derive, or commit fixtures" in text
    assert "documentation + static/preflight test only" in text
    assert "does **not** read archive payloads" in text


def test_doc_separates_three_gate_stages() -> None:
    text = _doc_text()
    assert "A) Dry-run manifest review" in text
    assert "B) Local derivation approval" in text
    assert "C) Fixture commit approval" in text


def test_doc_includes_seven_fixture_families() -> None:
    text = _doc_text()
    for family in REQUIRED_FAMILIES:
        assert family in text


def test_doc_includes_required_evidence_items() -> None:
    lowered = _doc_text().lower()
    for item in REQUIRED_EVIDENCE_ITEMS:
        assert item in lowered


def test_doc_includes_required_blocking_conditions() -> None:
    lowered = _doc_text().lower()
    for blocker in REQUIRED_BLOCKERS:
        assert blocker in lowered


def test_doc_references_phase104_and_related_phase_contracts() -> None:
    lowered = _doc_text().lower()
    assert "phase 1-04 dry-run manifest" in lowered
    assert "phase 1-02 safety shell" in lowered
    assert "phase 1-03 manifest/provenance contract" in lowered


def test_doc_has_no_real_fixture_payload_or_live_derivation_commands() -> None:
    lowered = _doc_text().lower()
    assert '"fixture_family":' not in lowered
    assert '"source_relative_path":' not in lowered
    assert "python scripts/phase1/fixture_derivation_safety_shell.py derive" not in lowered
    assert "--approve-derivation" not in lowered


def test_safety_shell_still_exposes_dry_run_manifest() -> None:
    parser = safety_shell._build_parser()
    choices = parser._subparsers._group_actions[0].choices  # pylint: disable=protected-access
    assert "dry-run-manifest" in choices


def test_phase103_contract_allows_dry_run_manifest_status() -> None:
    assert "dry_run_manifest" in manifest_contract.MANIFEST_STATUS_ALLOWLIST


def test_no_fixture_output_directory_exists() -> None:
    assert not (REPO_ROOT / "fixtures/phase1").exists()


def test_no_artifact_paths_were_added_in_gate_doc() -> None:
    lowered = _doc_text().lower()
    forbidden_snippets = [
        "data.tar.zst",
        ".duckdb",
        "fixtures/phase1/fixture_manifest.json",
        "archive extraction output",
    ]
    assert "does **not** read archive payloads" in lowered
    for snippet in forbidden_snippets:
        if snippet == ".duckdb":
            # .duckdb is allowed only in explicit negative/hygiene statements.
            assert lowered.count(snippet) >= 1
        else:
            assert "commit " + snippet not in lowered
