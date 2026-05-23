from __future__ import annotations

import argparse
import json
import re
import time
from pathlib import Path

import duckdb


SOURCE_POSTURE = "synthetic_in_memory_only"
_REQUIRED_FIELDS = {
    "name",
    "description",
    "sql",
    "expected_min_rows",
    "budget_ms",
    "source_posture",
}
_WRITE_STATEMENT_PATTERNS = (
    r"\bcreate\s+table\b",
    r"\bcreate\s+view\b",
    r"\bcopy\b",
    r"\binsert\b",
    r"\bupdate\b",
    r"\bdelete\b",
    r"\battach\b",
    r"\bexport\b",
    r"\binstall\b",
    r"\bload\b",
)
_FORBIDDEN_SQL_PATTERNS = (
    r"parquet_scan",
    r"http://",
    r"https://",
    r"\bapi\.",
    r"requests\.",
    r"urllib",
    r"websocket",
    r"\barchive\b",
    r"data/kalshi/",
    r"data/polymarket/",
)


def get_latency_query_specs() -> list[dict[str, object]]:
    return [
        {
            "name": "silver_view_inventory",
            "description": "Count expected synthetic Silver views.",
            "sql": (
                "SELECT COUNT(*) AS row_count FROM duckdb_views() "
                "WHERE schema_name='main' AND view_name LIKE 'silver_%'"
            ),
            "expected_min_rows": 1,
            "budget_ms": 500,
            "source_posture": SOURCE_POSTURE,
        },
        {
            "name": "unresolved_status_counts",
            "description": "Aggregate unresolved status values across synthetic Silver views.",
            "sql": (
                "SELECT unresolved_status, COUNT(*) FROM ("
                "SELECT unresolved_status FROM silver_kalshi_events UNION ALL "
                "SELECT unresolved_status FROM silver_kalshi_markets UNION ALL "
                "SELECT unresolved_status FROM silver_kalshi_outcomes UNION ALL "
                "SELECT unresolved_status FROM silver_kalshi_market_snapshots UNION ALL "
                "SELECT unresolved_status FROM silver_kalshi_fills UNION ALL "
                "SELECT unresolved_status FROM silver_kalshi_results UNION ALL "
                "SELECT unresolved_status FROM silver_poly_markets UNION ALL "
                "SELECT unresolved_status FROM silver_poly_outcomes UNION ALL "
                "SELECT unresolved_status FROM silver_poly_clob_tokens UNION ALL "
                "SELECT unresolved_status FROM silver_poly_clob_fills UNION ALL "
                "SELECT unresolved_status FROM silver_poly_blocks UNION ALL "
                "SELECT unresolved_status FROM silver_poly_legacy_fpmm_fills UNION ALL "
                "SELECT unresolved_status FROM silver_poly_collateral_assets"
                ") u GROUP BY unresolved_status"
            ),
            "expected_min_rows": 1,
            "budget_ms": 500,
            "source_posture": SOURCE_POSTURE,
        },
        {
            "name": "dependency_status_counts",
            "description": "Aggregate dependency status values across synthetic Silver views.",
            "sql": (
                "SELECT dependency_status, COUNT(*) FROM ("
                "SELECT dependency_status FROM silver_kalshi_events UNION ALL "
                "SELECT dependency_status FROM silver_kalshi_markets UNION ALL "
                "SELECT dependency_status FROM silver_kalshi_outcomes UNION ALL "
                "SELECT dependency_status FROM silver_kalshi_market_snapshots UNION ALL "
                "SELECT dependency_status FROM silver_kalshi_fills UNION ALL "
                "SELECT dependency_status FROM silver_kalshi_results UNION ALL "
                "SELECT dependency_status FROM silver_poly_markets UNION ALL "
                "SELECT dependency_status FROM silver_poly_outcomes UNION ALL "
                "SELECT dependency_status FROM silver_poly_clob_tokens UNION ALL "
                "SELECT dependency_status FROM silver_poly_clob_fills UNION ALL "
                "SELECT dependency_status FROM silver_poly_blocks UNION ALL "
                "SELECT dependency_status FROM silver_poly_legacy_fpmm_fills UNION ALL "
                "SELECT dependency_status FROM silver_poly_collateral_assets"
                ") d GROUP BY dependency_status"
            ),
            "expected_min_rows": 1,
            "budget_ms": 500,
            "source_posture": SOURCE_POSTURE,
        },
        {
            "name": "kalshi_fill_dependency_scan",
            "description": "Scan Kalshi synthetic fill dependency statuses.",
            "sql": "SELECT dependency_status, COUNT(*) FROM silver_kalshi_fills GROUP BY dependency_status",
            "expected_min_rows": 1,
            "budget_ms": 250,
            "source_posture": SOURCE_POSTURE,
        },
        {
            "name": "poly_clob_dependency_scan",
            "description": "Scan Polymarket synthetic CLOB fill dependency statuses.",
            "sql": "SELECT dependency_status, COUNT(*) FROM silver_poly_clob_fills GROUP BY dependency_status",
            "expected_min_rows": 1,
            "budget_ms": 250,
            "source_posture": SOURCE_POSTURE,
        },
        {
            "name": "legacy_fpmm_dependency_scan",
            "description": "Scan Polymarket synthetic legacy FPMM dependency statuses.",
            "sql": "SELECT dependency_status, COUNT(*) FROM silver_poly_legacy_fpmm_fills GROUP BY dependency_status",
            "expected_min_rows": 1,
            "budget_ms": 250,
            "source_posture": SOURCE_POSTURE,
        },
        {
            "name": "bronze_row_count_scan",
            "description": "Scan Bronze row counts for synthetic source coverage.",
            "sql": (
                "SELECT view_name, row_count FROM ("
                "SELECT 'bronze_kalshi_markets' AS view_name, COUNT(*) AS row_count FROM bronze_kalshi_markets UNION ALL "
                "SELECT 'bronze_kalshi_trades', COUNT(*) FROM bronze_kalshi_trades UNION ALL "
                "SELECT 'bronze_poly_markets', COUNT(*) FROM bronze_poly_markets UNION ALL "
                "SELECT 'bronze_poly_clob_trades', COUNT(*) FROM bronze_poly_clob_trades UNION ALL "
                "SELECT 'bronze_poly_blocks', COUNT(*) FROM bronze_poly_blocks UNION ALL "
                "SELECT 'bronze_poly_legacy_fpmm_trades', COUNT(*) FROM bronze_poly_legacy_fpmm_trades UNION ALL "
                "SELECT 'bronze_poly_fpmm_collateral_lookup', COUNT(*) FROM bronze_poly_fpmm_collateral_lookup"
                ") b"
            ),
            "expected_min_rows": 1,
            "budget_ms": 500,
            "source_posture": SOURCE_POSTURE,
        },
    ]


def validate_latency_query_specs(specs: list[dict[str, object]]) -> None:
    names: set[str] = set()
    for spec in specs:
        missing = _REQUIRED_FIELDS - set(spec)
        if missing:
            raise ValueError(f"Missing required fields: {sorted(missing)}")

        name = spec["name"]
        if not isinstance(name, str):
            raise ValueError("Query spec name must be a string")
        if name in names:
            raise ValueError(f"Duplicate query name: {name}")
        names.add(name)

        sql = spec["sql"]
        if not isinstance(sql, str):
            raise ValueError(f"SQL must be a string for query: {name}")

        lowered_sql = sql.lower()
        for pattern in _FORBIDDEN_SQL_PATTERNS + _WRITE_STATEMENT_PATTERNS:
            if re.search(pattern, lowered_sql):
                raise ValueError(f"Forbidden SQL pattern for query {name}: {pattern}")

        budget_ms = spec["budget_ms"]
        if not isinstance(budget_ms, (int, float)) or budget_ms <= 0:
            raise ValueError(f"budget_ms must be positive for query: {name}")

        expected_min_rows = spec["expected_min_rows"]
        if not isinstance(expected_min_rows, int) or expected_min_rows < 0:
            raise ValueError(f"expected_min_rows must be a non-negative integer for query: {name}")

        source_posture = spec["source_posture"]
        if source_posture != SOURCE_POSTURE:
            raise ValueError(f"source_posture must be {SOURCE_POSTURE} for query: {name}")


def run_latency_gate(include_unresolved_cases: bool = True) -> dict[str, object]:
    from scripts.prd_0b import run_view_smoke

    repo_root = Path(__file__).resolve().parents[2]
    bronze_sql = run_view_smoke.load_sql_file(repo_root / "sql/prd_0b/bronze_views.sql")
    silver_sql = run_view_smoke.load_sql_file(repo_root / "sql/prd_0b/silver_views.sql")

    specs = get_latency_query_specs()
    validate_latency_query_specs(specs)

    con = duckdb.connect(":memory:")
    run_view_smoke.create_synthetic_source_relations(
        con, include_unresolved_cases=include_unresolved_cases
    )
    run_view_smoke.apply_view_sql(con, bronze_sql, silver_sql)

    query_results: list[dict[str, object]] = []
    for spec in specs:
        start = time.perf_counter()
        rows = con.execute(spec["sql"]).fetchall()
        elapsed_ms = (time.perf_counter() - start) * 1000.0
        row_count = len(rows)
        passed = row_count >= int(spec["expected_min_rows"]) and elapsed_ms <= float(spec["budget_ms"])

        query_results.append(
            {
                "name": spec["name"],
                "status": "pass" if passed else "fail",
                "elapsed_ms": round(elapsed_ms, 3),
                "budget_ms": spec["budget_ms"],
                "row_count": row_count,
                "expected_min_rows": spec["expected_min_rows"],
                "warning": None if passed else "synthetic_budget_or_row_count_check_failed",
            }
        )

    passed_count = sum(1 for result in query_results if result["status"] == "pass")
    failed_count = len(query_results) - passed_count
    max_elapsed_ms = max((float(result["elapsed_ms"]) for result in query_results), default=0.0)
    total_elapsed_ms = sum(float(result["elapsed_ms"]) for result in query_results)
    ok = failed_count == 0

    return {
        "ok": ok,
        "status": "ok" if ok else "failed",
        "query_count": len(query_results),
        "passed_query_count": passed_count,
        "failed_query_count": failed_count,
        "max_elapsed_ms": round(max_elapsed_ms, 3),
        "total_elapsed_ms": round(total_elapsed_ms, 3),
        "budgets_are_synthetic_only": True,
        "source_posture": SOURCE_POSTURE,
        "wrote_outputs": False,
        "created_duckdb_file": False,
        "query_results": query_results,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    run_parser = subparsers.add_parser("run")
    run_parser.add_argument("--json", action="store_true", dest="as_json")
    run_parser.add_argument("--without-unresolved-cases", action="store_true")
    args = parser.parse_args()

    if args.command == "run":
        summary = run_latency_gate(
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
