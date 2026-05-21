from __future__ import annotations

import importlib
import json
import subprocess
import sys
from pathlib import Path

import pytest

from scripts.phase1.fixture_derivation_safety_shell import (
    APPLEDOUBLE_PREFIX,
    DEFAULT_TINY_ROW_LIMIT,
    MAX_TINY_ROW_LIMIT,
    MIN_TINY_ROW_LIMIT,
    evaluate_fixture_derivation_gate,
    validate_fixture_output_path,
    validate_no_forbidden_runtime_options,
    validate_relative_source_path,
    validate_row_limit,
)


REPO_ROOT = Path(__file__).resolve().parents[2]


def test_module_import_has_no_side_effects() -> None:
    module = importlib.import_module("scripts.phase1.fixture_derivation_safety_shell")
    assert module.APPLEDOUBLE_PREFIX == APPLEDOUBLE_PREFIX


def test_valid_source_relative_paths_pass() -> None:
    paths = [
        "data/kalshi/markets/markets_0_10000.parquet",
        "data/kalshi/trades/trades_0_10000.parquet",
        "data/polymarket/blocks/blocks_10000000_10100000.parquet",
        "data/polymarket/markets/markets_0_10000.parquet",
        "data/polymarket/trades/trades_0_10000.parquet",
        "data/polymarket/legacy_trades/trades_0_10000.parquet",
        "data/polymarket/fpmm_collateral_lookup.json",
    ]
    for path in paths:
        assert validate_relative_source_path(path).allowed


@pytest.mark.parametrize("path", ["/abs/file.parquet", "../data/kalshi/markets/x.parquet", "data/kalshi/markets/._x.parquet", "data/kalshi/markets/data.tar.zst", "data/kalshi/markets/file.duckdb", "data/kalshi/markets/file.db", "data/kalshi/markets/file.sqlite", "data/kalshi/markets/generated_report.json", "tmp/random.parquet"])
def test_invalid_source_paths_rejected(path: str) -> None:
    assert not validate_relative_source_path(path).allowed


def test_valid_output_path_passes() -> None:
    assert validate_fixture_output_path("fixtures/phase1/kalshi_markets_tiny.json").allowed


@pytest.mark.parametrize("path", ["data/phase1/out.json", "/abs/out.json", "fixtures/phase1/../out.json", "fixtures/phase1/out.csv", "fixtures/phase1/out.duckdb", "fixtures/phase1/generated_report.json", "fixtures/phase1/._out.json"])
def test_invalid_output_paths_rejected(path: str) -> None:
    assert not validate_fixture_output_path(path).allowed


def test_row_limits() -> None:
    assert validate_row_limit(MIN_TINY_ROW_LIMIT).allowed
    assert validate_row_limit(MAX_TINY_ROW_LIMIT).allowed
    assert not validate_row_limit(0).allowed
    assert not validate_row_limit(-1).allowed
    assert not validate_row_limit(MAX_TINY_ROW_LIMIT + 1).allowed
    assert not validate_row_limit("5").allowed  # type: ignore[arg-type]


def test_forbidden_runtime_options_rejected_one_by_one() -> None:
    keys = [
        "network_access",
        "api_calls",
        "use_secrets",
        "load_env_credentials",
        "import_trading_connector",
        "import_exchange_connector",
        "order_routing",
        "order_placement",
        "live_trading",
        "autonomous_execution",
        "create_duckdb",
        "generate_report",
        "write_fixtures",
        "archive_import",
        "loader_execution",
    ]
    for key in keys:
        assert not validate_no_forbidden_runtime_options({key: True}).allowed


def _safe_config() -> dict[str, object]:
    return {
        "phase1_01_merged": True,
        "phase0b_26_merged": True,
        "fixture_derivation_approved": False,
        "fixture_commit_approved": False,
        "script_mode": "safety_check_only",
        "source_manifest_ref": "local_poly_kalshi_historical_archive_placeholder",
        "source_relative_path": "data/kalshi/markets/markets_0_10000.parquet",
        "output_relative_path": "fixtures/phase1/kalshi_markets_tiny.json",
        "row_limit": DEFAULT_TINY_ROW_LIMIT,
        "runtime_options": {},
    }


def test_safe_safety_check_config_allowed() -> None:
    decision = evaluate_fixture_derivation_gate(_safe_config())
    assert decision.allowed
    assert any("planning only" in warning for warning in decision.warnings)


def test_derivation_approval_true_rejected() -> None:
    cfg = _safe_config()
    cfg["fixture_derivation_approved"] = True
    assert not evaluate_fixture_derivation_gate(cfg).allowed


def test_commit_approval_true_rejected() -> None:
    cfg = _safe_config()
    cfg["fixture_commit_approved"] = True
    assert not evaluate_fixture_derivation_gate(cfg).allowed


def test_runtime_fixture_writing_rejected() -> None:
    cfg = _safe_config()
    cfg["runtime_options"] = {"write_fixtures": True}
    assert not evaluate_fixture_derivation_gate(cfg).allowed


def test_cli_check_prints_json_and_creates_no_files(tmp_path: Path) -> None:
    cmd = [
        sys.executable,
        "-m",
        "scripts.phase1.fixture_derivation_safety_shell",
        "check",
        "--source-relative-path",
        "data/kalshi/markets/markets_0_10000.parquet",
        "--output-relative-path",
        "fixtures/phase1/example.json",
        "--row-limit",
        "3",
        "--source-manifest-ref",
        "local_poly_kalshi_historical_archive_placeholder",
        "--script-mode",
        "safety_check_only",
    ]
    before = {p.relative_to(tmp_path) for p in tmp_path.rglob("*")}
    result = subprocess.run(cmd, cwd=REPO_ROOT, check=False, capture_output=True, text=True)
    after = {p.relative_to(tmp_path) for p in tmp_path.rglob("*")}

    assert result.returncode == 0
    parsed = json.loads(result.stdout)
    assert parsed["allowed"] is True
    assert before == after


def test_cli_invalid_config_exits_nonzero() -> None:
    cmd = [
        sys.executable,
        "-m",
        "scripts.phase1.fixture_derivation_safety_shell",
        "check",
        "--source-relative-path",
        "data/kalshi/markets/markets_0_10000.parquet",
        "--output-relative-path",
        "fixtures/phase1/example.csv",
        "--row-limit",
        "6",
        "--source-manifest-ref",
        "x",
        "--script-mode",
        "safety_check_only",
    ]
    result = subprocess.run(cmd, cwd=REPO_ROOT, check=False, capture_output=True, text=True)
    assert result.returncode != 0


def test_no_production_runtime_modules_imported() -> None:
    text = Path("scripts/phase1/fixture_derivation_safety_shell.py").read_text(encoding="utf-8")
    disallowed_import_hints = ["import meg", "from meg", "import pandas", "from pandas", "import pyarrow", "from pyarrow", "import requests", "from requests", "import httpx", "from httpx", "import web3", "from web3", "import duckdb", "from duckdb"]
    for hint in disallowed_import_hints:
        assert hint not in text


def test_doc_alignment_phase1_and_phase0b_23() -> None:
    phase101 = Path("docs/phase1/1-01_PHASE1_KICKOFF_FIXTURE_GENERATION_GATE.md").read_text(encoding="utf-8").lower()
    p023 = Path("docs/phase0b/0B-23_TINY_FIXTURE_DERIVATION_SCRIPT_PLAN.md").read_text(encoding="utf-8").lower()

    assert "fixture derivation approval" in phase101
    assert "fixture commit approval" in phase101
    assert "does **not** implement scripts" in phase101
    assert "refuse to run unless explicit approval" in p023
    assert "never call apis" in p023
    assert "never access network" in p023
    assert "never use secrets" in p023
    assert "never use trading connectors" in p023
    assert "does **not** derive fixtures" in p023
    assert "does **not** commit fixture data" in p023
    assert "ignore appledouble files" in p023
