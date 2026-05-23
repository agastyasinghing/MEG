from __future__ import annotations

import argparse
import json
from pathlib import Path

import duckdb


def load_sql_file(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def get_expected_bronze_views() -> list[str]:
    return [
        "bronze_kalshi_markets",
        "bronze_kalshi_trades",
        "bronze_poly_markets",
        "bronze_poly_clob_trades",
        "bronze_poly_blocks",
        "bronze_poly_legacy_fpmm_trades",
        "bronze_poly_fpmm_collateral_lookup",
    ]


def get_expected_silver_views() -> list[str]:
    return [
        "silver_kalshi_events",
        "silver_kalshi_markets",
        "silver_kalshi_outcomes",
        "silver_kalshi_market_snapshots",
        "silver_kalshi_fills",
        "silver_kalshi_results",
        "silver_poly_markets",
        "silver_poly_outcomes",
        "silver_poly_clob_tokens",
        "silver_poly_clob_fills",
        "silver_poly_blocks",
        "silver_poly_legacy_fpmm_fills",
        "silver_poly_collateral_assets",
    ]


def create_synthetic_source_relations(con: duckdb.DuckDBPyConnection) -> None:
    con.execute("CREATE TABLE source_kalshi_markets AS SELECT 'KX1' ticker_ref, 'EV1' event_ticker_ref, 'src-kx1' source_market_ref, 'YES' outcome, 'snap1' snapshot_ref, 'res1' result_ref")
    con.execute("CREATE TABLE source_kalshi_trades AS SELECT 'tx-k1' transaction_ref, 'KX1' ticker_ref, 'trade-k1' trade_ref")
    con.execute("CREATE TABLE source_poly_markets AS SELECT 'COND1' condition_ref, 'TOK1' token_ref, 'src-p1' source_market_ref, 'YES' outcome")
    con.execute("CREATE TABLE source_poly_clob_trades AS SELECT 'tx-p1' transaction_ref, 'COND1' condition_ref, 'BLK1' block_ref")
    con.execute("CREATE TABLE source_poly_blocks AS SELECT 'BLK1' block_ref")
    con.execute("CREATE TABLE source_poly_legacy_fpmm_trades AS SELECT 'FPMM1' fpmm_ref, 'USDC' collateral_asset_ref")
    con.execute("CREATE TABLE source_poly_fpmm_collateral_lookup AS SELECT 'USDC' collateral_asset_ref")


def apply_view_sql(con: duckdb.DuckDBPyConnection, bronze_sql: str, silver_sql: str) -> None:
    con.execute(bronze_sql)
    con.execute(silver_sql)


def list_duckdb_views(con: duckdb.DuckDBPyConnection) -> list[str]:
    rows = con.execute("SELECT view_name FROM duckdb_views() WHERE schema_name = 'main' ORDER BY view_name").fetchall()
    return [row[0] for row in rows]


def run_in_memory_view_smoke() -> dict[str, object]:
    repo_root = Path(__file__).resolve().parents[2]
    bronze_sql = load_sql_file(repo_root / "sql/prd_0b/bronze_views.sql")
    silver_sql = load_sql_file(repo_root / "sql/prd_0b/silver_views.sql")

    con = duckdb.connect(database=":memory:")
    create_synthetic_source_relations(con)
    apply_view_sql(con, bronze_sql, silver_sql)

    views = set(list_duckdb_views(con))
    expected_bronze = get_expected_bronze_views()
    expected_silver = get_expected_silver_views()

    row_count_checks = {
        view_name: con.execute(f"SELECT COUNT(*) FROM {view_name}").fetchone()[0]
        for view_name in expected_bronze
    }
    missing_bronze = [name for name in expected_bronze if name not in views]
    missing_silver = [name for name in expected_silver if name not in views]
    ok = not missing_bronze and not missing_silver and all(count >= 1 for count in row_count_checks.values())
    return {
        "ok": ok,
        "status": "ok" if ok else "failed",
        "bronze_view_count": len(expected_bronze),
        "silver_view_count": len(expected_silver),
        "missing_bronze_views": missing_bronze,
        "missing_silver_views": missing_silver,
        "row_count_checks": row_count_checks,
        "warnings": [],
        "wrote_outputs": False,
        "created_duckdb_file": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    run_parser = subparsers.add_parser("run")
    run_parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()

    if args.command == "run":
        summary = run_in_memory_view_smoke()
        if args.as_json:
            print(json.dumps(summary, sort_keys=True))
        else:
            print(summary)
        return 0 if bool(summary["ok"]) else 1
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
