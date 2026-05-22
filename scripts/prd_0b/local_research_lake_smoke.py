from __future__ import annotations

import argparse
import json
import pathlib
import sys
from dataclasses import asdict, dataclass, field
from typing import Any

EXPECTED_ARCHIVE_FAMILIES = [
    "data/kalshi/markets",
    "data/kalshi/trades",
    "data/polymarket/blocks",
    "data/polymarket/markets",
    "data/polymarket/trades",
    "data/polymarket/legacy_trades",
]
EXPECTED_JSON_FILES = ["data/polymarket/fpmm_collateral_lookup.json"]
APPLEDOUBLE_PREFIX = "._"
FORBIDDEN_OUTPUT_SUFFIXES = {".duckdb", ".db", ".sqlite", ".csv", ".parquet", ".zst", ".tar", ".zip"}
MAX_SAMPLE_FILES_PER_FAMILY = 1
DEFAULT_ROW_LIMIT = 5


@dataclass
class SmokeResult:
    ok: bool
    status: str
    reasons: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    archive_root: str | None = None
    family_results: list[dict[str, object]] = field(default_factory=list)
    duckdb_available: bool = False
    wrote_outputs: bool = False
    created_duckdb_file: bool = False


def validate_archive_root_path(archive_root: str) -> SmokeResult:
    result = SmokeResult(ok=False, status="invalid_archive_root", archive_root=archive_root)
    if not archive_root or not archive_root.strip():
        result.reasons.append("archive_root_empty")
        return result
    if ".." in pathlib.PurePath(archive_root).parts:
        result.reasons.append("archive_root_parent_traversal_rejected")
        return result
    root = pathlib.Path(archive_root)
    if root.suffix.lower() in {".zst", ".tar", ".zip", ".gz", ".tgz"}:
        result.reasons.append("archive_root_looks_compressed")
        return result
    if not root.exists():
        result.reasons.append("archive_root_missing")
        return result
    if not root.is_dir():
        result.reasons.append("archive_root_not_directory")
        return result
    missing = [family for family in EXPECTED_ARCHIVE_FAMILIES if not (root / family).is_dir()]
    if missing:
        result.reasons.append("expected_families_missing")
        result.reasons.extend(f"missing_family:{family}" for family in missing)
        return result
    result.ok = True
    result.status = "archive_root_valid"
    return result


def discover_expected_families(archive_root: str) -> dict[str, object]:
    root = pathlib.Path(archive_root)
    family_results: list[dict[str, object]] = []
    warnings: list[str] = []
    for family in EXPECTED_ARCHIVE_FAMILIES:
        family_path = root / family
        entry: dict[str, object] = {"family": family, "exists": family_path.is_dir(), "status": "present" if family_path.is_dir() else "missing", "parquet_count": 0, "sample_file": None}
        if family_path.is_dir():
            parquet_files = [p for p in family_path.glob("*.parquet") if not p.name.startswith(APPLEDOUBLE_PREFIX)]
            entry["parquet_count"] = len(parquet_files)
            if parquet_files:
                entry["sample_file"] = str(parquet_files[0].relative_to(root))
            appledouble_hits = [p.name for p in family_path.glob(f"{APPLEDOUBLE_PREFIX}*")]
            if appledouble_hits:
                warnings.append(f"appledouble_ignored:{family}:{len(appledouble_hits)}")
        family_results.append(entry)
    json_status = []
    for rel in EXPECTED_JSON_FILES:
        p = root / rel
        json_status.append({"path": rel, "exists": p.is_file()})
    return {"family_results": family_results, "json_files": json_status, "warnings": warnings}


def find_sample_parquet_files(archive_root: str) -> dict[str, str | None]:
    root = pathlib.Path(archive_root)
    out: dict[str, str | None] = {}
    for family in EXPECTED_ARCHIVE_FAMILIES:
        family_path = root / family
        sample = None
        if family_path.is_dir():
            for item in family_path.glob("*.parquet"):
                if item.name.startswith(APPLEDOUBLE_PREFIX):
                    continue
                sample = str(item.relative_to(root))
                break
        out[family] = sample
    return out


def try_import_duckdb() -> tuple[bool, object | None, str | None]:
    try:
        import duckdb  # type: ignore
        return True, duckdb, None
    except Exception as exc:
        return False, None, f"duckdb_unavailable:{exc.__class__.__name__}"


def _duckdb_quote(path: str) -> str:
    return "'" + path.replace("'", "''") + "'"


def run_duckdb_readonly_smoke(archive_root: str, row_limit: int = DEFAULT_ROW_LIMIT) -> dict[str, object]:
    ok, duckdb_mod, err = try_import_duckdb()
    result: dict[str, object] = {"status": "duckdb_unavailable", "duckdb_available": False, "family_query_results": [], "reason": err}
    if not ok or duckdb_mod is None:
        return result
    samples = find_sample_parquet_files(archive_root)
    conn = duckdb_mod.connect(":memory:")
    family_query_results = []
    try:
        for family, sample in samples.items():
            if not sample:
                family_query_results.append({"family": family, "status": "no_sample"})
                continue
            full_path = str((pathlib.Path(archive_root) / sample).resolve())
            qpath = _duckdb_quote(full_path)
            try:
                schema_rows = conn.execute(f"DESCRIBE SELECT * FROM parquet_scan({qpath}) LIMIT 0").fetchall()
                count_rows = conn.execute(f"SELECT COUNT(*) FROM parquet_scan({qpath}) LIMIT {int(row_limit)}").fetchall()
                family_query_results.append({
                    "family": family,
                    "status": "ok",
                    "schema_columns": len(schema_rows),
                    "row_count": int(count_rows[0][0]) if count_rows else 0,
                })
            except Exception as exc:
                family_query_results.append({"family": family, "status": "query_failed", "reason": exc.__class__.__name__})
    finally:
        conn.close()
    return {"status": "duckdb_smoke_complete", "duckdb_available": True, "family_query_results": family_query_results}


def build_smoke_summary(archive_root: str, row_limit: int, require_duckdb: bool = False) -> dict[str, object]:
    validation = validate_archive_root_path(archive_root)
    summary = asdict(validation)
    root_path = pathlib.Path(archive_root)
    can_discover = root_path.exists() and root_path.is_dir()
    if can_discover:
        discovery = discover_expected_families(archive_root)
        summary["family_results"] = discovery["family_results"]
        summary["warnings"].extend(discovery["warnings"])
        summary["json_files"] = discovery["json_files"]
    if not validation.ok:
        return summary
    smoke = run_duckdb_readonly_smoke(archive_root, row_limit=row_limit)
    summary["duckdb_available"] = bool(smoke.get("duckdb_available", False))
    summary["duckdb_smoke"] = smoke
    if not summary["duckdb_available"]:
        summary["status"] = "duckdb_unavailable"
        summary["warnings"].append(str(smoke.get("reason", "duckdb_unavailable")))
        if require_duckdb:
            summary["ok"] = False
            summary["reasons"].append("require_duckdb_but_unavailable")
    else:
        summary["status"] = "ok"
        summary["ok"] = True
    return summary


def _parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="PRD-0B local research lake smoke")
    sub = parser.add_subparsers(dest="command", required=True)
    check = sub.add_parser("check")
    check.add_argument("--archive-root", required=True)
    check.add_argument("--row-limit", type=int, default=DEFAULT_ROW_LIMIT)
    check.add_argument("--json", action="store_true", dest="as_json")
    check.add_argument("--require-duckdb", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv or sys.argv[1:])
    if args.command != "check":
        return 2
    summary = build_smoke_summary(args.archive_root, args.row_limit, require_duckdb=args.require_duckdb)
    if args.as_json:
        print(json.dumps(summary, indent=2, sort_keys=True))
    else:
        print(summary.get("status", "unknown"))
    return 0 if summary.get("ok", False) else 1


if __name__ == "__main__":
    raise SystemExit(main())
