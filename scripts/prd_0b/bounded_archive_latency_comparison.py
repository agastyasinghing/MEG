from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def _sum_elapsed_ms(results: list[dict[str, Any]], fallback: dict[str, Any]) -> tuple[float | None, float | None, int]:
    elapsed_values: list[float] = []
    for item in results:
        value = item.get("elapsed_ms")
        if isinstance(value, (int, float)):
            elapsed_values.append(float(value))
    if not elapsed_values and isinstance(fallback, dict):
        by_query = fallback.get("elapsed_ms_by_query")
        if isinstance(by_query, dict):
            for value in by_query.values():
                if isinstance(value, (int, float)):
                    elapsed_values.append(float(value))
    if not elapsed_values:
        return None, None, 0
    return round(sum(elapsed_values), 3), round(max(elapsed_values), 3), len(elapsed_values)


def run_bounded_archive_latency_comparison(
    archive_root: Path,
    row_limit: int = 1000,
    family_allowlist: list[str] | None = None,
    include_unresolved_cases: bool = True,
) -> dict[str, object]:
    from scripts.prd_0b.bounded_archive_query_smoke import run_bounded_archive_query_smoke
    from scripts.prd_0b.query_latency_gate import run_latency_gate

    summary: dict[str, Any] = {
        "ok": False,
        "status": "fail_closed",
        "source_posture": "local_bounded_comparison_only",
        "archive_root_status": "invalid",
        "synthetic_status": "not_run",
        "archive_status": "not_run",
        "synthetic_query_count": 0,
        "archive_query_count": 0,
        "synthetic_total_elapsed_ms": None,
        "archive_total_elapsed_ms": None,
        "synthetic_max_elapsed_ms": None,
        "archive_max_elapsed_ms": None,
        "comparison_ratio_archive_to_synthetic": None,
        "comparison_interpretation": "not_run",
        "row_limit": row_limit,
        "checked_families": [],
        "missing_families": [],
        "warnings": [],
        "wrote_outputs": False,
        "created_duckdb_file": False,
        "generated_artifacts": [],
        "production_slo_claim": False,
        "final_trading_readiness_claim": False,
    }

    if archive_root is None:
        summary["status"] = "missing_archive_root"
        summary["warnings"].append("archive_root_is_required")
        return summary

    synthetic_summary = run_latency_gate(include_unresolved_cases=include_unresolved_cases)
    archive_summary = run_bounded_archive_query_smoke(
        archive_root=archive_root,
        row_limit=row_limit,
        family_allowlist=family_allowlist,
        json_mode=True,
    )

    summary["archive_root_status"] = str(archive_summary.get("archive_root_status", "invalid"))
    summary["synthetic_status"] = str(synthetic_summary.get("status", "unknown"))
    summary["archive_status"] = str(archive_summary.get("status", "unknown"))
    summary["checked_families"] = list(archive_summary.get("checked_families", []))
    summary["missing_families"] = list(archive_summary.get("missing_families", []))
    summary["warnings"] = list(synthetic_summary.get("warnings", [])) + list(archive_summary.get("warnings", []))

    syn_results = list(synthetic_summary.get("query_results", []))
    arc_results = list(archive_summary.get("query_results", []))
    syn_total, syn_max, syn_count = _sum_elapsed_ms(syn_results, synthetic_summary)
    arc_total, arc_max, arc_count = _sum_elapsed_ms(arc_results, archive_summary)
    summary["synthetic_total_elapsed_ms"] = syn_total
    summary["archive_total_elapsed_ms"] = arc_total
    summary["synthetic_max_elapsed_ms"] = syn_max
    summary["archive_max_elapsed_ms"] = arc_max
    summary["synthetic_query_count"] = syn_count
    summary["archive_query_count"] = arc_count

    if summary["archive_status"] != "ok":
        summary["status"] = "archive_smoke_not_ok"
        summary["comparison_interpretation"] = "archive_smoke_not_ok"
        return summary
    if summary["synthetic_status"] != "ok":
        summary["status"] = "synthetic_gate_not_ok"
        summary["comparison_interpretation"] = "synthetic_gate_not_ok"
        return summary
    if not syn_total or syn_total <= 0:
        summary["status"] = "insufficient_synthetic_timing"
        summary["comparison_interpretation"] = "insufficient_synthetic_timing"
        return summary
    if arc_total is None:
        summary["status"] = "archive_timing_missing"
        summary["comparison_interpretation"] = "archive_smoke_not_ok"
        return summary

    ratio = round(arc_total / syn_total, 6)
    summary["comparison_ratio_archive_to_synthetic"] = ratio
    summary["ok"] = True
    summary["status"] = "ok"
    if ratio <= 10:
        summary["comparison_interpretation"] = "archive_within_synthetic_smoke_band"
    else:
        summary["comparison_interpretation"] = "archive_slower_than_synthetic_smoke_band"
    return summary


def _format_human_summary(summary: dict[str, object]) -> str:
    return "\n".join(
        [
            f"status: {summary.get('status')}",
            f"ok: {summary.get('ok')}",
            f"source_posture: {summary.get('source_posture')}",
            f"archive_root_status: {summary.get('archive_root_status')}",
            f"synthetic_status: {summary.get('synthetic_status')}",
            f"archive_status: {summary.get('archive_status')}",
            f"comparison_interpretation: {summary.get('comparison_interpretation')}",
            f"comparison_ratio_archive_to_synthetic: {summary.get('comparison_ratio_archive_to_synthetic')}",
        ]
    )


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Bounded archive latency comparison harness")
    sub = parser.add_subparsers(dest="command", required=True)
    run = sub.add_parser("run")
    run.add_argument("--archive-root", required=True)
    run.add_argument("--row-limit", type=int, default=1000)
    run.add_argument("--family", action="append", default=[])
    run.add_argument("--without-unresolved-cases", action="store_true")
    run.add_argument("--json", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    summary = run_bounded_archive_latency_comparison(
        archive_root=Path(args.archive_root),
        row_limit=args.row_limit,
        family_allowlist=args.family or None,
        include_unresolved_cases=not args.without_unresolved_cases,
    )
    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))
    else:
        print(_format_human_summary(summary))
    return 0 if summary.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
