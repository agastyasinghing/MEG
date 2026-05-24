from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Any

MAX_ROW_LIMIT = 1000
ENRICHMENT_MODE = "bounded_sample_metadata_only"
APPROVED_SAMPLE_KEYS = {
    "family",
    "source_platform",
    "source_kind",
    "source_relative_path",
    "sample_enrichment_status",
    "sample_source_relative_path",
    "sample_file_kind",
    "sample_row_limit",
    "sample_row_count_observed",
    "sample_column_count_observed",
    "sample_columns_observed",
    "sample_elapsed_ms",
    "sample_warning",
    "sample_generated_from_archive_root",
    "sample_persistent_output_written",
}


def get_sample_enrichment_mode() -> str:
    return ENRICHMENT_MODE


def enrich_data_dictionary_with_samples(
    archive_root: Path,
    row_limit: int = 1000,
    family_allowlist: list[str] | None = None,
) -> dict[str, object]:
    summary: dict[str, Any] = {
        "ok": False,
        "status": "fail_closed",
        "archive_root_status": "invalid",
        "duckdb_status": "not_checked",
        "enrichment_mode": get_sample_enrichment_mode(),
        "family_count": 0,
        "enriched_families": [],
        "skipped_families": [],
        "missing_families": [],
        "representative_files": {},
        "row_limit": row_limit,
        "sample_enrichment_results": [],
        "warnings": [],
        "wrote_outputs": False,
        "created_duckdb_file": False,
        "generated_artifacts": [],
        "committed_fixtures": False,
        "production_readiness_claim": False,
        "final_trading_readiness_claim": False,
    }
    if archive_root is None:
        summary["status"] = "missing_archive_root"
        return summary
    if row_limit <= 0 or row_limit > MAX_ROW_LIMIT:
        summary["status"] = "invalid_row_limit"
        summary["warnings"].append("row_limit_must_be_between_1_and_1000")
        return summary

    root = archive_root.resolve()
    if not root.exists() or not root.is_dir():
        summary["status"] = "invalid_archive_root"
        return summary
    summary["archive_root_status"] = "ok"

    from scripts.prd_0b.bounded_archive_query_smoke import (
        get_approved_archive_family_specs,
        select_representative_files,
    )

    specs = get_approved_archive_family_specs()
    allowed_names = {str(s["name"]) for s in specs}
    if family_allowlist is not None:
        unknown = sorted(name for name in family_allowlist if name not in allowed_names)
        if unknown:
            summary["status"] = "unknown_family_allowlist"
            summary["warnings"].append(f"unknown_family_names:{','.join(unknown)}")
            return summary
        selected_names = set(family_allowlist)
        specs = [s for s in specs if str(s["name"]) in selected_names]
        summary["skipped_families"] = sorted(allowed_names - selected_names)

    if not specs:
        summary["status"] = "empty_active_family_set"
        return summary

    summary["family_count"] = len(specs)
    selected = select_representative_files(root, specs)
    summary["representative_files"] = selected["representative_files"]
    summary["missing_families"] = selected["missing_families"]
    summary["warnings"].extend(selected["warnings"])

    if selected["unsafe_families"]:
        summary["status"] = "unsafe_archive_paths"
        summary["warnings"].append("unsafe_family_paths_detected")
        return summary

    try:
        import duckdb
    except ModuleNotFoundError:
        summary["duckdb_status"] = "missing"
        summary["status"] = "duckdb_missing"
        return summary

    summary["duckdb_status"] = "ok"
    con = duckdb.connect(":memory:")
    try:
        for spec in specs:
            family = str(spec["name"])
            if family not in summary["representative_files"]:
                continue
            rel = str(summary["representative_files"][family])
            sample_path = (root / rel).resolve()
            start = time.perf_counter()
            kind = str(spec["file_kind"])
            if kind == "json":
                row_count = 1 if sample_path.is_file() else 0
                columns = ["json_sidecar_present"] if sample_path.is_file() else []
                status = "pass" if sample_path.is_file() else "fail"
            else:
                cursor = con.execute("SELECT * FROM parquet_scan(?) LIMIT ?", [str(sample_path), row_limit])
                rows = cursor.fetchall()
                row_count = len(rows)
                columns = [str(col[0]) for col in (cursor.description or [])]
                status = "pass"
            elapsed = round((time.perf_counter() - start) * 1000.0, 3)
            result = {
                "family": family,
                "source_platform": str(spec["source_platform"]),
                "source_kind": str(spec["source_kind"]),
                "source_relative_path": rel,
                "sample_enrichment_status": status,
                "sample_source_relative_path": rel,
                "sample_file_kind": kind,
                "sample_row_limit": row_limit,
                "sample_row_count_observed": row_count,
                "sample_column_count_observed": len(columns),
                "sample_columns_observed": columns,
                "sample_elapsed_ms": elapsed,
                "sample_warning": None,
                "sample_generated_from_archive_root": True,
                "sample_persistent_output_written": False,
            }
            summary["sample_enrichment_results"].append(result)
            summary["enriched_families"].append(family)
    finally:
        con.close()

    if any(set(r.keys()) != APPROVED_SAMPLE_KEYS for r in summary["sample_enrichment_results"]):
        summary["status"] = "invalid_sample_metadata_keys"
        return summary
    if summary["missing_families"]:
        summary["status"] = "missing_required_families"
        return summary
    if len(summary["enriched_families"]) != len(specs):
        summary["status"] = "missing_required_families"
        return summary
    if any(r["sample_enrichment_status"] != "pass" for r in summary["sample_enrichment_results"]):
        summary["status"] = "enrichment_failures"
        return summary

    summary["ok"] = True
    summary["status"] = "ok"
    return summary


def _format_human_summary(summary: dict[str, object]) -> str:
    return "\n".join(
        [
            f"status: {summary.get('status')}",
            f"ok: {summary.get('ok')}",
            f"enrichment_mode: {summary.get('enrichment_mode')}",
            f"archive_root_status: {summary.get('archive_root_status')}",
            f"duckdb_status: {summary.get('duckdb_status')}",
            f"enriched_families: {', '.join(summary.get('enriched_families', []))}",
            f"missing_families: {', '.join(summary.get('missing_families', []))}",
            f"warnings: {', '.join(summary.get('warnings', []))}",
        ]
    )


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Bounded archive-backed data dictionary sample enrichment")
    sub = parser.add_subparsers(dest="command", required=True)
    run = sub.add_parser("run")
    run.add_argument("--archive-root", required=True)
    run.add_argument("--row-limit", type=int, default=1000)
    run.add_argument("--family", action="append", default=[])
    run.add_argument("--json", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    families = args.family if args.family else None
    summary = enrich_data_dictionary_with_samples(Path(args.archive_root), row_limit=args.row_limit, family_allowlist=families)
    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))
    else:
        print(_format_human_summary(summary))
    return 0 if bool(summary.get("ok")) else 1


if __name__ == "__main__":
    raise SystemExit(main())
