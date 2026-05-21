from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass, field
from pathlib import PurePosixPath
from typing import Any

APPLEDOUBLE_PREFIX = "._"
FORBIDDEN_OUTPUT_SUFFIXES = (
    ".duckdb",
    ".db",
    ".sqlite",
    ".parquet",
    ".csv",
    ".zst",
    ".tar",
    ".zip",
)
ALLOWED_FUTURE_FIXTURE_SUFFIXES = (".json",)
FORBIDDEN_PATH_PARTS = ("data", ".git", "__pycache__")
DEFAULT_TINY_ROW_LIMIT = 5
MIN_TINY_ROW_LIMIT = 1
MAX_TINY_ROW_LIMIT = 5

_ALLOWED_SOURCE_PREFIXES = (
    "data/kalshi/markets/",
    "data/kalshi/trades/",
    "data/polymarket/blocks/",
    "data/polymarket/markets/",
    "data/polymarket/trades/",
    "data/polymarket/legacy_trades/",
)
_ALLOWED_SOURCE_EXACT = {
    "data/polymarket/fpmm_collateral_lookup.json",
}
_ALLOWED_OUTPUT_PREFIX = "fixtures/phase1/"
_FORBIDDEN_REPORT_HINTS = ("report", "reports")

_FORBIDDEN_SOURCE_SUFFIXES = (".duckdb", ".db", ".sqlite", ".zst", ".tar", ".zip")

_FORBIDDEN_RUNTIME_OPTION_KEYS = {
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
}


@dataclass
class SafetyDecision:
    allowed: bool
    reasons: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _combine(*decisions: SafetyDecision) -> SafetyDecision:
    allowed = all(d.allowed for d in decisions)
    reasons: list[str] = []
    warnings: list[str] = []
    for decision in decisions:
        reasons.extend(decision.reasons)
        warnings.extend(decision.warnings)
    return SafetyDecision(allowed=allowed, reasons=reasons, warnings=warnings)


def _path_decision(path_text: str, *, kind: str, check_output_suffixes: bool) -> tuple[PurePosixPath | None, SafetyDecision]:
    reasons: list[str] = []
    if not isinstance(path_text, str) or not path_text.strip():
        return None, SafetyDecision(False, [f"{kind} path must be a non-empty relative string."])

    path = PurePosixPath(path_text)
    if path.is_absolute():
        reasons.append(f"{kind} path must be relative, not absolute.")

    parts = path.parts
    if any(part == ".." for part in parts):
        reasons.append(f"{kind} path must not contain parent traversal.")
    if any(part.startswith(APPLEDOUBLE_PREFIX) for part in parts):
        reasons.append(f"{kind} path must not include AppleDouble components.")

    lowered = path_text.lower()
    if check_output_suffixes and any(lowered.endswith(suffix) for suffix in FORBIDDEN_OUTPUT_SUFFIXES):
        reasons.append(f"{kind} path has a forbidden artifact suffix.")
    if any(hint in lowered for hint in _FORBIDDEN_REPORT_HINTS):
        reasons.append(f"{kind} path appears to target generated reports.")

    if reasons:
        return path, SafetyDecision(False, reasons)
    return path, SafetyDecision(True)


def validate_relative_source_path(source_relative_path: str) -> SafetyDecision:
    path, base = _path_decision(source_relative_path, kind="source", check_output_suffixes=False)
    if path is None or not base.allowed:
        return base

    normalized = path.as_posix()
    lowered = normalized.lower()
    if any(lowered.endswith(suffix) for suffix in _FORBIDDEN_SOURCE_SUFFIXES):
        return SafetyDecision(False, ["Source path has a forbidden artifact suffix."])

    allowed_family = any(normalized.startswith(prefix) for prefix in _ALLOWED_SOURCE_PREFIXES)
    allowed_exact = normalized in _ALLOWED_SOURCE_EXACT
    if not (allowed_family or allowed_exact):
        return SafetyDecision(False, ["Source path must be within approved archive families only."])

    return SafetyDecision(True)


def validate_fixture_output_path(output_relative_path: str) -> SafetyDecision:
    path, base = _path_decision(output_relative_path, kind="output", check_output_suffixes=True)
    if path is None or not base.allowed:
        return base

    normalized = path.as_posix()
    lowered = normalized.lower()
    if any(part in FORBIDDEN_PATH_PARTS for part in path.parts):
        return SafetyDecision(False, ["Output path must avoid forbidden path parts."])
    if not normalized.startswith(_ALLOWED_OUTPUT_PREFIX):
        return SafetyDecision(False, ["Output path must be under fixtures/phase1/."])
    if not any(lowered.endswith(suffix) for suffix in ALLOWED_FUTURE_FIXTURE_SUFFIXES):
        return SafetyDecision(False, ["Output path must use an approved future fixture suffix."])

    return SafetyDecision(True)


def validate_row_limit(row_limit: int) -> SafetyDecision:
    if not isinstance(row_limit, int) or isinstance(row_limit, bool):
        return SafetyDecision(False, ["Row limit must be an integer."])
    if row_limit < MIN_TINY_ROW_LIMIT or row_limit > MAX_TINY_ROW_LIMIT:
        return SafetyDecision(False, [f"Row limit must be between {MIN_TINY_ROW_LIMIT} and {MAX_TINY_ROW_LIMIT}."])
    return SafetyDecision(True)


def validate_no_forbidden_runtime_options(options: dict[str, object]) -> SafetyDecision:
    if not isinstance(options, dict):
        return SafetyDecision(False, ["Runtime options must be a dictionary."])

    reasons: list[str] = []
    for key in sorted(_FORBIDDEN_RUNTIME_OPTION_KEYS):
        if options.get(key):
            reasons.append(f"Forbidden runtime option requested: {key}.")
    return SafetyDecision(allowed=not reasons, reasons=reasons)


def evaluate_fixture_derivation_gate(config: dict[str, object]) -> SafetyDecision:
    if not isinstance(config, dict):
        return SafetyDecision(False, ["Config must be a dictionary."])

    decisions: list[SafetyDecision] = []
    reasons: list[str] = []
    warnings: list[str] = []

    if config.get("phase1_01_merged") is not True:
        reasons.append("phase1_01_merged must be true.")
    if config.get("phase0b_26_merged") is not True:
        reasons.append("phase0b_26_merged must be true.")

    if config.get("fixture_derivation_approved") is not False:
        reasons.append("fixture_derivation_approved must remain false in this ticket.")
    if config.get("fixture_commit_approved") is not False:
        reasons.append("fixture_commit_approved must remain false in this ticket.")

    mode = config.get("script_mode")
    if mode not in {"safety_check_only", "dry_run_plan_only"}:
        reasons.append("script_mode must be safety_check_only or dry_run_plan_only.")

    if not config.get("source_manifest_ref"):
        reasons.append("source_manifest_ref is required.")

    decisions.append(validate_relative_source_path(str(config.get("source_relative_path", ""))))
    decisions.append(validate_fixture_output_path(str(config.get("output_relative_path", ""))))
    decisions.append(validate_row_limit(config.get("row_limit")))
    decisions.append(validate_no_forbidden_runtime_options(config.get("runtime_options", {})))

    if reasons:
        decisions.append(SafetyDecision(False, reasons))

    all_decision = _combine(*decisions)
    if all_decision.allowed:
        warnings.append("Safety checks passed for planning only; fixture derivation and fixture writing remain disallowed in Phase 1-02.")
    return SafetyDecision(all_decision.allowed, all_decision.reasons, all_decision.warnings + warnings)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Phase 1 fixture derivation safety shell")
    sub = parser.add_subparsers(dest="command", required=True)
    check = sub.add_parser("check", help="Run safety-only gate checks")
    check.add_argument("--source-relative-path", required=True)
    check.add_argument("--output-relative-path", required=True)
    check.add_argument("--row-limit", required=True, type=int)
    check.add_argument("--source-manifest-ref", required=True)
    check.add_argument("--script-mode", required=True, choices=["safety_check_only", "dry_run_plan_only"])
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    config: dict[str, object] = {
        "phase1_01_merged": True,
        "phase0b_26_merged": True,
        "fixture_derivation_approved": False,
        "fixture_commit_approved": False,
        "script_mode": args.script_mode,
        "source_manifest_ref": args.source_manifest_ref,
        "source_relative_path": args.source_relative_path,
        "output_relative_path": args.output_relative_path,
        "row_limit": args.row_limit,
        "runtime_options": {},
    }
    decision = evaluate_fixture_derivation_gate(config)
    print(json.dumps(decision.to_dict(), sort_keys=True))
    return 0 if decision.allowed else 1


if __name__ == "__main__":
    raise SystemExit(main())
