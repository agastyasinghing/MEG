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


def create_synthetic_source_relations(
    con: duckdb.DuckDBPyConnection,
    include_unresolved_cases: bool = True,
) -> None:
    con.execute(
        "CREATE TABLE source_kalshi_markets AS "
        "SELECT * FROM (VALUES ('KX1','EV1','src-kx1','YES','snap1','res1')) "
        "t(ticker_ref,event_ticker_ref,source_market_ref,outcome,snapshot_ref,result_ref)"
    )
    con.execute(
        "CREATE TABLE source_kalshi_trades AS "
        "SELECT * FROM (VALUES ('tx-k1','KX1','trade-k1')) "
        "t(transaction_ref,ticker_ref,trade_ref)"
    )
    con.execute(
        "CREATE TABLE source_poly_markets AS "
        "SELECT * FROM (VALUES ('COND1','TOK1','src-p1','YES')) "
        "t(condition_ref,token_ref,source_market_ref,outcome)"
    )
    con.execute(
        "CREATE TABLE source_poly_clob_trades AS "
        "SELECT * FROM (VALUES ('tx-p1','COND1','BLK1')) "
        "t(transaction_ref,condition_ref,block_ref)"
    )
    con.execute(
        "CREATE TABLE source_poly_blocks AS "
        "SELECT * FROM (VALUES ('BLK1')) t(block_ref)"
    )
    con.execute(
        "CREATE TABLE source_poly_legacy_fpmm_trades AS "
        "SELECT * FROM (VALUES ('FPMM1','USDC')) t(fpmm_ref,collateral_asset_ref)"
    )
    con.execute(
        "CREATE TABLE source_poly_fpmm_collateral_lookup AS "
        "SELECT * FROM (VALUES ('USDC')) t(collateral_asset_ref)"
    )

    if include_unresolved_cases:
        con.execute(
            "INSERT INTO source_kalshi_trades VALUES "
            "('tx-k-miss-market','KX404','trade-k404'),("
            "'tx-k-null',NULL,NULL)"
        )
        con.execute(
            "INSERT INTO source_poly_clob_trades VALUES "
            "('tx-p-miss-market','COND404','BLK1'),"
            "('tx-p-miss-block','COND1','BLK404'),"
            "(NULL,NULL,NULL)"
        )
        con.execute(
            "INSERT INTO source_poly_legacy_fpmm_trades VALUES "
            "('FPMM404','DAI404'),(NULL,NULL)"
        )


def apply_view_sql(
    con: duckdb.DuckDBPyConnection,
    bronze_sql: str,
    silver_sql: str,
) -> None:
    con.execute(bronze_sql)
    con.execute(silver_sql)


def list_duckdb_views(con: duckdb.DuckDBPyConnection) -> list[str]:
    rows = con.execute(
        "SELECT view_name FROM duckdb_views() "
        "WHERE schema_name='main' ORDER BY view_name"
    ).fetchall()
    return [row[0] for row in rows]


def _collect_status_counts(
    con: duckdb.DuckDBPyConnection,
    column_name: str,
) -> dict[str, int]:
    union_query = " UNION ALL ".join(
        [f"SELECT {column_name} AS status_value FROM {view_name}" for view_name in get_expected_silver_views()]
    )
    rows = con.execute(
        f"SELECT status_value, COUNT(*) FROM ({union_query}) status_rows GROUP BY 1"
    ).fetchall()
    return {row[0]: row[1] for row in rows}


def run_in_memory_view_smoke(include_unresolved_cases: bool = True) -> dict[str, object]:
    repo_root = Path(__file__).resolve().parents[2]
    bronze_sql = load_sql_file(repo_root / "sql/prd_0b/bronze_views.sql")
    silver_sql = load_sql_file(repo_root / "sql/prd_0b/silver_views.sql")

    con = duckdb.connect(":memory:")
    create_synthetic_source_relations(con, include_unresolved_cases=include_unresolved_cases)
    apply_view_sql(con, bronze_sql, silver_sql)

    views = set(list_duckdb_views(con))
    expected_bronze = get_expected_bronze_views()
    expected_silver = get_expected_silver_views()

    row_count_checks = {
        view_name: con.execute(f"SELECT COUNT(*) FROM {view_name}").fetchone()[0]
        for view_name in expected_bronze + expected_silver
    }
    unresolved_status_counts = _collect_status_counts(con, "unresolved_status")
    dependency_status_counts = _collect_status_counts(con, "dependency_status")

    missing_bronze = [name for name in expected_bronze if name not in views]
    missing_silver = [name for name in expected_silver if name not in views]
    ok = (
        not missing_bronze
        and not missing_silver
        and all(count >= 1 for count in row_count_checks.values())
    )

    return {
        "ok": ok,
        "status": "ok" if ok else "failed",
        "bronze_view_count": len(expected_bronze),
        "silver_view_count": len(expected_silver),
        "missing_bronze_views": missing_bronze,
        "missing_silver_views": missing_silver,
        "row_count_checks": row_count_checks,
        "unresolved_status_counts": unresolved_status_counts,
        "dependency_status_counts": dependency_status_counts,
        "warnings": [],
        "wrote_outputs": False,
        "created_duckdb_file": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    run_parser = subparsers.add_parser("run")
    run_parser.add_argument("--json", action="store_true", dest="as_json")
    run_parser.add_argument("--without-unresolved-cases", action="store_true")
    args = parser.parse_args()

    if args.command == "run":
        summary = run_in_memory_view_smoke(
            include_unresolved_cases=not args.without_unresolved_cases
        )
        if args.as_json:
            print(json.dumps(summary, sort_keys=True))
        else:
            print(summary)
        return 0 if bool(summary["ok"]) else 1

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
