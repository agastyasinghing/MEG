from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from scripts.phase1.fixture_derivation_safety_shell import (
    build_default_dry_run_config,
    build_dry_run_fixture_manifest,
    validate_fixture_output_path,
    validate_relative_source_path,
)

REPO_ROOT = Path(__file__).resolve().parents[2]


def _config() -> dict[str, object]:
    return build_default_dry_run_config(
        source_manifest_ref="local_poly_kalshi_historical_archive_placeholder",
        source_repo_ref="agastyasinghing/MEG",
        source_repo_commit="97c15e9",
        source_archive_ref="local_archive_ref",
        created_by="phase1-04-test",
    )


def test_dry_run_manifest_shape_and_families() -> None:
    manifest = build_dry_run_fixture_manifest(_config())
    assert manifest["manifest_status"] == "dry_run_manifest"
    assert manifest["phase"] == "phase1-04"
    required = {
        "manifest_ref", "schema_version", "phase", "manifest_status", "created_by", "created_at",
        "source_manifest_ref", "source_repo_ref", "source_repo_commit", "source_archive_ref",
        "fixture_derivation_approval_ref", "fixture_commit_approval_ref", "fixture_entries",
        "global_posture", "artifact_hygiene", "reviewer_envelope",
    }
    assert required.issubset(manifest.keys())

    entries = manifest["fixture_entries"]
    families = [entry["fixture_family"] for entry in entries]
    assert families == [
        "kalshi_markets_tiny",
        "kalshi_trades_tiny",
        "poly_markets_tiny",
        "poly_clob_trades_tiny",
        "poly_blocks_tiny",
        "poly_legacy_fpmm_trades_tiny",
        "poly_fpmm_collateral_lookup_tiny",
    ]
    for entry in entries:
        assert validate_relative_source_path(entry["source_relative_path"]).allowed
        assert validate_fixture_output_path(entry["output_relative_path"]).allowed
        assert 1 <= entry["selected_row_count"] <= 5
        assert entry["source_file_checksum"] == "not_computed_dry_run"
        assert entry["generated_fixture_checksum"] == "not_generated_dry_run"
        assert entry["derivation_timestamp"] == "not_derived_dry_run"
        assert entry["entry_posture"] == {
            "fixture_derivation_approved": False,
            "fixture_commit_approved": False,
            "fixture_written": False,
            "archive_rows_read": False,
            "source_payload_read": False,
            "normalization_applied": False,
            "runtime_loader_used": False,
        }


def test_posture_hygiene_and_reviewer_pending() -> None:
    manifest = build_dry_run_fixture_manifest(_config())
    assert manifest["global_posture"] == {
        "research_only": True,
        "local_only": True,
        "network_allowed": False,
        "api_calls_allowed": False,
        "secrets_allowed": False,
        "connector_import_allowed": False,
        "archive_import_allowed": False,
        "fixture_writes_allowed": False,
        "loader_execution_allowed": False,
        "order_routing_allowed": False,
        "live_trading_allowed": False,
        "autonomous_execution_allowed": False,
    }
    assert all(manifest["artifact_hygiene"].values())
    reviewer = manifest["reviewer_envelope"]
    assert reviewer["human_review_required"] is True
    assert reviewer["reviewer_ref"] is None
    assert reviewer["reviewed_at"] is None
    assert reviewer["review_decision"] == "pending"


def test_unsafe_config_fails_closed() -> None:
    cfg = _config()
    cfg["fixture_derivation_approved"] = True
    with pytest.raises(ValueError):
        build_dry_run_fixture_manifest(cfg)


def test_missing_source_manifest_ref_fails_closed() -> None:
    cfg = _config()
    cfg["source_manifest_ref"] = ""
    with pytest.raises(ValueError):
        build_dry_run_fixture_manifest(cfg)


def test_commit_approval_true_fails_closed() -> None:
    cfg = _config()
    cfg["fixture_commit_approved"] = True
    with pytest.raises(ValueError):
        build_dry_run_fixture_manifest(cfg)


def test_cli_dry_run_manifest_prints_json_no_outputs(tmp_path: Path) -> None:
    cmd = [
        sys.executable,
        "-m",
        "scripts.phase1.fixture_derivation_safety_shell",
        "dry-run-manifest",
        "--source-manifest-ref", "local_poly_kalshi_historical_archive_placeholder",
        "--source-repo-ref", "agastyasinghing/MEG",
        "--source-repo-commit", "97c15e9",
        "--source-archive-ref", "local_archive_ref",
        "--created-by", "cli-test",
    ]
    before = {p.relative_to(tmp_path) for p in tmp_path.rglob("*")}
    result = subprocess.run(cmd, cwd=REPO_ROOT, check=False, capture_output=True, text=True)
    after = {p.relative_to(tmp_path) for p in tmp_path.rglob("*")}
    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["manifest_status"] == "dry_run_manifest"
    assert before == after
    assert not (REPO_ROOT / "fixtures/phase1").exists()


def test_cli_missing_required_args_exits_nonzero() -> None:
    cmd = [sys.executable, "-m", "scripts.phase1.fixture_derivation_safety_shell", "dry-run-manifest", "--source-manifest-ref", "x"]
    result = subprocess.run(cmd, cwd=REPO_ROOT, check=False, capture_output=True, text=True)
    assert result.returncode != 0


def test_existing_check_command_still_works() -> None:
    cmd = [
        sys.executable,
        "-m",
        "scripts.phase1.fixture_derivation_safety_shell",
        "check",
        "--source-relative-path", "data/kalshi/markets/markets_0_10000.parquet",
        "--output-relative-path", "fixtures/phase1/example.json",
        "--row-limit", "3",
        "--source-manifest-ref", "local_poly_kalshi_historical_archive_placeholder",
        "--script-mode", "safety_check_only",
    ]
    result = subprocess.run(cmd, cwd=REPO_ROOT, check=False, capture_output=True, text=True)
    assert result.returncode == 0


def test_no_production_runtime_imports_and_doc_alignment() -> None:
    shell_text = Path("scripts/phase1/fixture_derivation_safety_shell.py").read_text(encoding="utf-8").lower()
    phase101 = Path("docs/phase1/1-01_PHASE1_KICKOFF_FIXTURE_GENERATION_GATE.md").read_text(encoding="utf-8").lower()
    p023 = Path("docs/phase0b/0B-23_TINY_FIXTURE_DERIVATION_SCRIPT_PLAN.md").read_text(encoding="utf-8").lower()
    contract = Path("tests/core/test_phase1_fixture_manifest_provenance_contract.py").read_text(encoding="utf-8").lower()
    assert "dry-run-manifest" in shell_text
    assert "fixture derivation and fixture writing remain disallowed" in shell_text
    assert "dry_run_manifest" in contract
    assert "fixture derivation approval" in phase101 and "fixture commit approval" in phase101
    assert "provenance" in phase101 and "checksum" in phase101
    assert "manifest" in p023 and "provenance" in p023
    disallowed = ["import pandas", "import pyarrow", "import duckdb", "import requests", "from meg", "import meg"]
    for hint in disallowed:
        assert hint not in shell_text
