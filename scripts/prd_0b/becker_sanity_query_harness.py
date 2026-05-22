from __future__ import annotations

import argparse
import json
import pathlib
import sys
from typing import Any

from scripts.prd_0b.local_research_lake_smoke import (
    APPLEDOUBLE_PREFIX,
    EXPECTED_ARCHIVE_FAMILIES,
    EXPECTED_JSON_FILES,
    find_sample_parquet_files,
    try_import_duckdb,
    validate_archive_root_path,
)


def get_sanity_check_specs() -> list[dict[str, object]]:
    return [
        {"check_name": "kalshi_markets_schema_count_sample", "kind": "parquet_schema_count", "family": "data/kalshi/markets", "expected_columns": ["ticker", "event_ticker", "market_type", "title", "yes_sub_title", "no_sub_title", "status", "yes_bid", "yes_ask", "no_bid", "no_ask", "last_price", "volume", "volume_24h", "open_interest", "result", "created_time", "open_time", "close_time", "_fetched_at"]},
        {"check_name": "kalshi_trades_schema_count_sample", "kind": "parquet_schema_count", "family": "data/kalshi/trades", "expected_columns": ["trade_id", "ticker", "count", "yes_price", "no_price", "taker_side", "created_time", "_fetched_at"]},
        {"check_name": "poly_markets_schema_count_sample", "kind": "parquet_schema_count", "family": "data/polymarket/markets", "expected_columns": ["id", "condition_id", "question", "slug", "outcomes", "outcome_prices", "clob_token_ids", "volume", "liquidity", "active", "closed", "end_date", "created_at", "market_maker_address", "_fetched_at"]},
        {"check_name": "poly_clob_trades_schema_count_sample", "kind": "parquet_schema_count", "family": "data/polymarket/trades", "expected_columns": ["block_number", "transaction_hash", "log_index", "order_hash", "maker", "taker", "maker_asset_id", "taker_asset_id", "maker_amount", "taker_amount", "fee", "timestamp", "_fetched_at", "_contract"]},
        {"check_name": "poly_blocks_schema_count_sample", "kind": "parquet_schema_count", "family": "data/polymarket/blocks", "expected_columns": ["block_number", "timestamp"]},
        {"check_name": "poly_legacy_fpmm_trades_schema_count_sample", "kind": "parquet_schema_count", "family": "data/polymarket/legacy_trades", "expected_columns": ["block_number", "transaction_hash", "log_index", "fpmm_address", "trader", "amount", "fee_amount", "outcome_index", "outcome_tokens", "is_buy", "timestamp", "_fetched_at"]},
        {"check_name": "poly_fpmm_collateral_lookup_presence", "kind": "json_sidecar_presence", "path": "data/polymarket/fpmm_collateral_lookup.json", "expected_columns": []},
    ]


def validate_sanity_check_specs() -> list[str]:
    errors: list[str] = []
    specs = get_sanity_check_specs()
    if len(specs) != 7:
        errors.append("sanity_spec_count_not_seven")
    names = [str(spec.get("check_name", "")) for spec in specs]
    if len(set(names)) != len(names):
        errors.append("sanity_spec_names_not_unique")
    for spec in specs:
        name = str(spec.get("check_name", "unknown"))
        kind = spec.get("kind")
        if kind == "parquet_schema_count":
            cols = spec.get("expected_columns")
            if not isinstance(cols, list) or not cols:
                errors.append(f"missing_expected_columns:{name}")
            if not spec.get("family"):
                errors.append(f"missing_family:{name}")
        elif kind == "json_sidecar_presence":
            if not spec.get("path"):
                errors.append(f"missing_path:{name}")
        else:
            errors.append(f"unknown_kind:{name}")
    return errors


def _empty_result(spec: dict[str, object]) -> dict[str, object]:
    return {
        "check_name": spec["check_name"],
        "kind": spec["kind"],
        "status": "skipped",
        "family": spec.get("family"),
        "path": spec.get("path"),
        "sample_file": None,
        "expected_columns": list(spec.get("expected_columns", [])),
        "observed_columns": [],
        "missing_columns": [],
        "row_count_sample": None,
        "reasons": [],
        "warnings": [],
    }


def _duckdb_quote(path: str) -> str:
    return "'" + path.replace("'", "''") + "'"


def run_parquet_schema_count_check(spec: dict[str, object], archive_root: str, duckdb_mod: object | None, row_limit: int = 5) -> dict[str, object]:
    result = _empty_result(spec)
    family = str(spec["family"])
    family_path = pathlib.Path(archive_root) / family
    if not family_path.is_dir():
        result["status"] = "missing_family"
        result["reasons"].append("missing_family")
        return result

    sample_rel = find_sample_parquet_files(archive_root).get(family)
    result["sample_file"] = sample_rel
    if not sample_rel:
        result["status"] = "missing_sample"
        result["reasons"].append("missing_sample")
        return result

    if duckdb_mod is None:
        result["status"] = "duckdb_unavailable"
        result["reasons"].append("duckdb_unavailable")
        return result

    conn = duckdb_mod.connect(":memory:")
    try:
        full_path = str((pathlib.Path(archive_root) / sample_rel).resolve())
        qpath = _duckdb_quote(full_path)
        schema_rows = conn.execute(f"DESCRIBE SELECT * FROM parquet_scan({qpath})").fetchall()
        observed = [str(row[0]) for row in schema_rows]
        result["observed_columns"] = observed
        expected = list(spec.get("expected_columns", []))
        missing = [c for c in expected if c not in observed]
        result["missing_columns"] = missing
        count_rows = conn.execute(f"SELECT COUNT(*) FROM parquet_scan({qpath}) LIMIT {int(row_limit)}").fetchall()
        result["row_count_sample"] = int(count_rows[0][0]) if count_rows else 0
        if missing:
            result["status"] = "missing_expected_columns"
            result["reasons"].append("missing_expected_columns")
        else:
            result["status"] = "passed"
    except Exception as exc:
        result["status"] = "query_failed"
        result["reasons"].append(f"query_failed:{exc.__class__.__name__}")
    finally:
        conn.close()
    return result


def run_json_sidecar_presence_check(spec: dict[str, object], archive_root: str) -> dict[str, object]:
    result = _empty_result(spec)
    sidecar = pathlib.Path(archive_root) / str(spec["path"])
    result["status"] = "sidecar_present" if sidecar.is_file() else "sidecar_missing"
    if result["status"] == "sidecar_missing":
        result["reasons"].append("sidecar_missing")
    return result


def build_harness_summary(archive_root: str, sanity_results: list[dict[str, object]], duckdb_available: bool, require_duckdb: bool = False) -> dict[str, object]:
    reasons: list[str] = []
    warnings: list[str] = []
    statuses = [str(r.get("status", "")) for r in sanity_results]
    sidecar_ok = "sidecar_present" in statuses
    parquet_bad = any(s in {"query_failed", "missing_expected_columns", "missing_family", "missing_sample"} for s in statuses)
    parquet_duckdb_unavailable = any(s == "duckdb_unavailable" for s in statuses)
    ok = False
    status = "failed"
    if require_duckdb and not duckdb_available:
        reasons.append("require_duckdb_but_unavailable")
        status = "duckdb_unavailable"
    elif parquet_bad or not sidecar_ok:
        status = "failed"
    elif parquet_duckdb_unavailable and not require_duckdb:
        ok = True
        status = "ok_without_duckdb"
        warnings.append("duckdb_unavailable")
    else:
        ok = True
        status = "ok"
    return {"ok": ok, "status": status, "archive_root": archive_root, "duckdb_available": duckdb_available, "sanity_check_count": 7, "sanity_results": sanity_results, "reasons": reasons, "warnings": warnings, "wrote_outputs": False, "created_duckdb_file": False}


def run_becker_sanity_harness(archive_root: str, row_limit: int = 5, require_duckdb: bool = False) -> dict[str, object]:
    spec_errors = validate_sanity_check_specs()
    if spec_errors:
        return {
            "ok": False,
            "status": "invalid_sanity_check_specs",
            "archive_root": archive_root,
            "duckdb_available": False,
            "sanity_check_count": len(get_sanity_check_specs()),
            "sanity_results": [],
            "reasons": spec_errors,
            "warnings": [],
            "wrote_outputs": False,
            "created_duckdb_file": False,
        }

    validation = validate_archive_root_path(archive_root)
    if not validation.ok:
        root = pathlib.Path(archive_root)
        missing_results = []
        if root.exists() and root.is_dir():
            for spec in get_sanity_check_specs():
                if spec["kind"] == "parquet_schema_count":
                    missing_results.append(run_parquet_schema_count_check(spec, archive_root, None, row_limit=row_limit))
                else:
                    missing_results.append(run_json_sidecar_presence_check(spec, archive_root))
        return build_harness_summary(archive_root, missing_results, duckdb_available=False, require_duckdb=require_duckdb) | {"ok": False, "status": "invalid_archive_root", "reasons": list(validation.reasons)}

    ok_duckdb, duckdb_mod, _ = try_import_duckdb()
    results: list[dict[str, object]] = []
    for spec in get_sanity_check_specs():
        if spec["kind"] == "parquet_schema_count":
            results.append(run_parquet_schema_count_check(spec, archive_root, duckdb_mod if ok_duckdb else None, row_limit=row_limit))
        else:
            results.append(run_json_sidecar_presence_check(spec, archive_root))
    return build_harness_summary(archive_root, results, duckdb_available=bool(ok_duckdb), require_duckdb=require_duckdb)


def _parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="PRD-0B Becker archive sanity query harness")
    sub = parser.add_subparsers(dest="command", required=True)
    run = sub.add_parser("run")
    run.add_argument("--archive-root", required=True)
    run.add_argument("--row-limit", type=int, default=5)
    run.add_argument("--json", action="store_true", dest="as_json")
    run.add_argument("--require-duckdb", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv or sys.argv[1:])
    if args.command != "run":
        return 2
    summary = run_becker_sanity_harness(args.archive_root, row_limit=args.row_limit, require_duckdb=args.require_duckdb)
    if args.as_json:
        print(json.dumps(summary, indent=2, sort_keys=True))
    else:
        print(f"{summary.get('status')} ok={summary.get('ok')} checks={summary.get('sanity_check_count')}")
    return 0 if summary.get("ok", False) else 1


if __name__ == "__main__":
    raise SystemExit(main())
