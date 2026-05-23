from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Any


MAX_ROW_LIMIT = 1000


def get_approved_archive_family_specs() -> list[dict[str, object]]:
    return [
        {"name": "kalshi_markets", "source_platform": "kalshi", "source_kind": "markets", "relative_path": "kalshi/markets", "file_kind": "parquet", "required": True},
        {"name": "kalshi_trades", "source_platform": "kalshi", "source_kind": "trades", "relative_path": "kalshi/trades", "file_kind": "parquet", "required": True},
        {"name": "poly_markets", "source_platform": "polymarket", "source_kind": "markets", "relative_path": "polymarket/markets", "file_kind": "parquet", "required": True},
        {"name": "poly_clob_trades", "source_platform": "polymarket", "source_kind": "trades", "relative_path": "polymarket/trades", "file_kind": "parquet", "required": True},
        {"name": "poly_blocks", "source_platform": "polymarket", "source_kind": "blocks", "relative_path": "polymarket/blocks", "file_kind": "parquet", "required": True},
        {"name": "poly_legacy_fpmm_trades", "source_platform": "polymarket", "source_kind": "legacy_trades", "relative_path": "polymarket/legacy_trades", "file_kind": "parquet", "required": True},
        {"name": "poly_fpmm_collateral_lookup", "source_platform": "polymarket", "source_kind": "fpmm_collateral_lookup", "relative_path": "polymarket/fpmm_collateral_lookup.json", "file_kind": "json", "required": True},
    ]


def _is_within_root(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def select_representative_files(archive_root: Path, family_specs: list[dict[str, object]]) -> dict[str, object]:
    selected: dict[str, str] = {}
    missing: list[str] = []
    warnings: list[str] = []
    unsafe: list[str] = []
    root = archive_root.resolve()
    for spec in family_specs:
        name = str(spec["name"])
        rel = Path(str(spec["relative_path"]))
        kind = str(spec["file_kind"])
        target = (root / rel).resolve()
        if not _is_within_root(target, root):
            unsafe.append(name)
            continue
        if kind == "json":
            if target.is_file():
                selected[name] = str(target.relative_to(root).as_posix())
            else:
                missing.append(name)
            continue
        if not target.exists() or not target.is_dir():
            missing.append(name)
            continue
        candidates = sorted(
            p for p in target.iterdir() if p.is_file() and p.suffix.lower() == ".parquet" and not p.name.startswith("._")
        )
        if not candidates:
            missing.append(name)
            continue
        chosen = candidates[0].resolve()
        if not _is_within_root(chosen, root):
            unsafe.append(name)
            continue
        selected[name] = str(chosen.relative_to(root).as_posix())
        if len(candidates) > 1:
            warnings.append(f"multiple_files_found_for_{name}_using_first_sorted")
    return {"representative_files": selected, "missing_families": missing, "warnings": warnings, "unsafe_families": unsafe}


def run_bounded_archive_query_smoke(
    archive_root: Path,
    row_limit: int = 1000,
    family_allowlist: list[str] | None = None,
    json_mode: bool = True,
) -> dict[str, object]:
    del json_mode
    summary: dict[str, Any] = {
        "ok": False,
        "status": "fail_closed",
        "archive_root_status": "invalid",
        "duckdb_status": "not_checked",
        "family_count": 0,
        "checked_families": [],
        "skipped_families": [],
        "missing_families": [],
        "representative_files": {},
        "row_limit": row_limit,
        "query_results": [],
        "elapsed_ms_by_query": {},
        "warnings": [],
        "wrote_outputs": False,
        "created_duckdb_file": False,
        "generated_artifacts": [],
    }
    if row_limit <= 0 or row_limit > MAX_ROW_LIMIT:
        summary["status"] = "invalid_row_limit"
        summary["warnings"].append("row_limit_must_be_between_1_and_1000")
        return summary
    if archive_root is None:
        summary["status"] = "missing_archive_root"
        return summary
    root = archive_root.resolve()
    if not root.exists() or not root.is_dir():
        summary["status"] = "invalid_archive_root"
        return summary
    summary["archive_root_status"] = "ok"

    specs = get_approved_archive_family_specs()
    allowed_names = {str(s["name"]) for s in specs}
    if family_allowlist is not None:
        unknown = [name for name in family_allowlist if name not in allowed_names]
        if unknown:
            summary["status"] = "unknown_family_allowlist"
            summary["warnings"].append(f"unknown_family_names:{','.join(sorted(unknown))}")
            return summary
        selected_names = set(family_allowlist)
        specs = [s for s in specs if str(s["name"]) in selected_names]
        summary["skipped_families"] = sorted(allowed_names - selected_names)

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
            name = str(spec["name"])
            if name not in summary["representative_files"]:
                continue
            rel = str(summary["representative_files"][name])
            path = (root / rel).resolve()
            file_kind = str(spec["file_kind"])
            start = time.perf_counter()
            if file_kind == "json":
                result = {
                    "family": name,
                    "source_platform": spec["source_platform"],
                    "source_kind": spec["source_kind"],
                    "source_relative_path": rel,
                    "file_kind": file_kind,
                    "status": "pass" if path.is_file() else "fail",
                    "row_count_observed": None,
                    "column_count_observed": None,
                    "elapsed_ms": round((time.perf_counter() - start) * 1000.0, 3),
                    "warning": None,
                }
            else:
                rows = con.execute("SELECT * FROM parquet_scan(?) LIMIT ?", [str(path), row_limit]).fetchall()
                elapsed = round((time.perf_counter() - start) * 1000.0, 3)
                col_count = len(rows[0]) if rows else 0
                result = {
                    "family": name,
                    "source_platform": spec["source_platform"],
                    "source_kind": spec["source_kind"],
                    "source_relative_path": rel,
                    "file_kind": file_kind,
                    "status": "pass",
                    "row_count_observed": len(rows),
                    "column_count_observed": col_count,
                    "elapsed_ms": elapsed,
                    "warning": None,
                }
            summary["query_results"].append(result)
            summary["checked_families"].append(name)
            summary["elapsed_ms_by_query"][name] = result["elapsed_ms"]
    finally:
        con.close()

    missing_required = bool(summary["missing_families"])
    any_failed = any(r["status"] != "pass" for r in summary["query_results"])
    if not summary["checked_families"]:
        summary["status"] = "no_families_checked"
    elif missing_required:
        summary["status"] = "missing_required_families"
    elif any_failed:
        summary["status"] = "query_failures"
    else:
        summary["ok"] = True
        summary["status"] = "ok"
    return summary


def _format_human_summary(summary: dict[str, object]) -> str:
    lines = [
        f"status: {summary.get('status')}",
        f"ok: {summary.get('ok')}",
        f"archive_root_status: {summary.get('archive_root_status')}",
        f"duckdb_status: {summary.get('duckdb_status')}",
        f"family_count: {summary.get('family_count')}",
        f"checked_families: {', '.join(summary.get('checked_families', []))}",
        f"missing_families: {', '.join(summary.get('missing_families', []))}",
        f"warnings: {', '.join(summary.get('warnings', []))}",
    ]
    return "\n".join(lines)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Bounded archive query smoke harness")
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
    summary = run_bounded_archive_query_smoke(
        Path(args.archive_root),
        row_limit=args.row_limit,
        family_allowlist=families,
        json_mode=args.json,
    )
    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))
    else:
        print(_format_human_summary(summary))
    return 0 if bool(summary.get("ok")) else 1


if __name__ == "__main__":
    raise SystemExit(main())
