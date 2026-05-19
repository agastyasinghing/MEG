from __future__ import annotations

import argparse
from pathlib import Path

from .loader import (
    connect_duckdb,
    create_normalized_fills_table,
    create_price_snapshots_table,
    load_normalized_fills_csv,
    load_price_snapshots_csv,
)
from .reports import build_fixture_lead_lag_report, write_report_json

DEFAULT_FILLS_CSV = Path("tests/fixtures/phase0b/normalized_fills_sample.csv")
DEFAULT_SNAPSHOTS_CSV = Path("tests/fixtures/phase0b/price_snapshots_sample.csv")


def build_fixture_report_cli(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build fixture lead-lag research report JSON.")
    parser.add_argument("--fills-csv", default=str(DEFAULT_FILLS_CSV), help="Path to normalized_fills CSV fixture.")
    parser.add_argument(
        "--snapshots-csv",
        default=str(DEFAULT_SNAPSHOTS_CSV),
        help="Path to price_snapshots CSV fixture.",
    )
    parser.add_argument("--output", required=True, help="Output JSON path.")
    parser.add_argument("--horizon-ms", type=int, default=300000, help="Forward horizon in milliseconds.")
    args = parser.parse_args(argv)

    conn = connect_duckdb()
    try:
        create_normalized_fills_table(conn)
        create_price_snapshots_table(conn)
        load_normalized_fills_csv(conn, args.fills_csv)
        load_price_snapshots_csv(conn, args.snapshots_csv)
        report = build_fixture_lead_lag_report(conn, horizon_ms=args.horizon_ms)
    finally:
        conn.close()

    write_report_json(report, args.output)
    print(f"Fixture lead-lag report written to {args.output}")
    return 0


def main() -> int:
    return build_fixture_report_cli()


if __name__ == "__main__":
    raise SystemExit(main())
