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
DEFAULT_DRY_RUN_SCHEMA_VERSION = "phase1_fixture_manifest/v1"
DEFAULT_DRY_RUN_MANIFEST_REF = "phase1_04_tiny_fixture_dry_run_manifest"
DRY_RUN_SCRIPT_VERSION = "phase1-04-dry-run"
DRY_RUN_CHECKSUM_PLACEHOLDER = "not_computed_dry_run"
DRY_RUN_GENERATED_CHECKSUM_PLACEHOLDER = "not_generated_dry_run"
DRY_RUN_DERIVATION_TIMESTAMP_PLACEHOLDER = "not_derived_dry_run"

PLANNED_FIXTURE_FAMILIES: tuple[dict[str, object], ...] = (
    {
        "fixture_family": "kalshi_markets_tiny",
        "platform": "kalshi",
        "source_relative_path": "data/kalshi/markets/markets_0_10000.parquet",
        "output_relative_path": "fixtures/phase1/kalshi_markets_tiny.json",
        "selected_row_count": 3,
        "selected_stable_keys": ["ticker_ref", "event_ticker_ref", "fetched_at"],
        "row_selection_rule": "sort ticker_ref, event_ticker_ref, fetched_at then first_n",
        "normalization_plan_ref": "0B-22",
        "source_record_shape_version": "phase0b-19-v1",
        "unresolved_state_policy": "preserve_as_unresolved",
    },
    {
        "fixture_family": "kalshi_trades_tiny",
        "platform": "kalshi",
        "source_relative_path": "data/kalshi/trades/trades_0_10000.parquet",
        "output_relative_path": "fixtures/phase1/kalshi_trades_tiny.json",
        "selected_row_count": 2,
        "selected_stable_keys": ["trade_ref", "ticker_ref", "created_time"],
        "row_selection_rule": "sort trade_ref, ticker_ref, created_time then first_n",
        "normalization_plan_ref": "0B-22",
        "source_record_shape_version": "phase0b-19-v1",
        "unresolved_state_policy": "preserve_as_unresolved",
    },
    {
        "fixture_family": "poly_markets_tiny",
        "platform": "polymarket",
        "source_relative_path": "data/polymarket/markets/markets_0_10000.parquet",
        "output_relative_path": "fixtures/phase1/poly_markets_tiny.json",
        "selected_row_count": 3,
        "selected_stable_keys": ["condition_id", "source_market_ref", "fetched_at"],
        "row_selection_rule": "sort condition_id, source_market_ref, fetched_at then first_n",
        "normalization_plan_ref": "0B-21",
        "source_record_shape_version": "phase0b-19-v1",
        "unresolved_state_policy": "preserve_as_unresolved",
    },
    {
        "fixture_family": "poly_clob_trades_tiny",
        "platform": "polymarket",
        "source_relative_path": "data/polymarket/trades/trades_0_10000.parquet",
        "output_relative_path": "fixtures/phase1/poly_clob_trades_tiny.json",
        "selected_row_count": 4,
        "selected_stable_keys": ["transaction_hash", "log_index", "order_hash"],
        "row_selection_rule": "sort transaction_hash, log_index, order_hash then first_n",
        "normalization_plan_ref": "0B-21",
        "source_record_shape_version": "phase0b-19-v1",
        "unresolved_state_policy": "preserve_as_unresolved",
    },
    {
        "fixture_family": "poly_blocks_tiny",
        "platform": "polymarket",
        "source_relative_path": "data/polymarket/blocks/blocks_10000000_10100000.parquet",
        "output_relative_path": "fixtures/phase1/poly_blocks_tiny.json",
        "selected_row_count": 5,
        "selected_stable_keys": ["block_number"],
        "row_selection_rule": "sort block_number then first_n",
        "normalization_plan_ref": "0B-21",
        "source_record_shape_version": "phase0b-19-v1",
        "unresolved_state_policy": "preserve_as_unresolved",
    },
    {
        "fixture_family": "poly_legacy_fpmm_trades_tiny",
        "platform": "polymarket",
        "source_relative_path": "data/polymarket/legacy_trades/trades_0_10000.parquet",
        "output_relative_path": "fixtures/phase1/poly_legacy_fpmm_trades_tiny.json",
        "selected_row_count": 3,
        "selected_stable_keys": ["transaction_hash", "log_index", "fpmm_address"],
        "row_selection_rule": "sort transaction_hash, log_index, fpmm_address then first_n",
        "normalization_plan_ref": "0B-21",
        "source_record_shape_version": "phase0b-19-v1",
        "unresolved_state_policy": "preserve_as_unresolved",
    },
    {
        "fixture_family": "poly_fpmm_collateral_lookup_tiny",
        "platform": "polymarket",
        "source_relative_path": "data/polymarket/fpmm_collateral_lookup.json",
        "output_relative_path": "fixtures/phase1/poly_fpmm_collateral_lookup_tiny.json",
        "selected_row_count": 2,
        "selected_stable_keys": ["fpmm_address", "collateral_token_address"],
        "row_selection_rule": "sort fpmm_address, collateral_token_address then first_n",
        "normalization_plan_ref": "0B-21",
        "source_record_shape_version": "phase0b-19-v1",
        "unresolved_state_policy": "preserve_as_unresolved",
    },
)


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
    dry = sub.add_parser("dry-run-manifest", help="Build a dry-run tiny fixture manifest")
    dry.add_argument("--source-manifest-ref", required=True)
    dry.add_argument("--source-repo-ref", required=True)
    dry.add_argument("--source-repo-commit", required=True)
    dry.add_argument("--source-archive-ref", required=True)
    dry.add_argument("--created-by", required=True)
    dry.add_argument("--schema-version", default=DEFAULT_DRY_RUN_SCHEMA_VERSION)
    dry.add_argument("--manifest-ref", default=DEFAULT_DRY_RUN_MANIFEST_REF)
    return parser


def build_default_dry_run_config(
    *,
    source_manifest_ref: str,
    source_repo_ref: str,
    source_repo_commit: str,
    source_archive_ref: str,
    created_by: str,
    schema_version: str = DEFAULT_DRY_RUN_SCHEMA_VERSION,
    manifest_ref: str = DEFAULT_DRY_RUN_MANIFEST_REF,
) -> dict[str, object]:
    return {
        "phase1_01_merged": True,
        "phase0b_26_merged": True,
        "fixture_derivation_approved": False,
        "fixture_commit_approved": False,
        "script_mode": "dry_run_plan_only",
        "source_manifest_ref": source_manifest_ref,
        "source_repo_ref": source_repo_ref,
        "source_repo_commit": source_repo_commit,
        "source_archive_ref": source_archive_ref,
        "created_by": created_by,
        "schema_version": schema_version,
        "manifest_ref": manifest_ref,
    }


def build_dry_run_fixture_manifest(config: dict[str, object]) -> dict[str, object]:
    if not isinstance(config, dict):
        raise ValueError("dry-run config must be a dictionary")
    required = ["source_manifest_ref", "source_repo_ref", "source_repo_commit", "source_archive_ref", "created_by"]
    missing = [k for k in required if not isinstance(config.get(k), str) or not str(config.get(k)).strip()]
    if missing:
        raise ValueError(f"missing required dry-run config fields: {', '.join(missing)}")
    fixture_entries: list[dict[str, object]] = []
    for family in PLANNED_FIXTURE_FAMILIES:
        gate = evaluate_fixture_derivation_gate(
            {
                "phase1_01_merged": config.get("phase1_01_merged"),
                "phase0b_26_merged": config.get("phase0b_26_merged"),
                "fixture_derivation_approved": config.get("fixture_derivation_approved"),
                "fixture_commit_approved": config.get("fixture_commit_approved"),
                "script_mode": config.get("script_mode"),
                "source_manifest_ref": config.get("source_manifest_ref"),
                "source_relative_path": family["source_relative_path"],
                "output_relative_path": family["output_relative_path"],
                "row_limit": family["selected_row_count"],
                "runtime_options": {},
            }
        )
        if not gate.allowed:
            raise ValueError(f"dry-run manifest blocked for {family['fixture_family']}: {'; '.join(gate.reasons)}")
        fixture_entries.append(
            {
                "fixture_ref": f"fixture-{family['fixture_family'].replace('_', '-')}",
                **family,
                "source_file_checksum": DRY_RUN_CHECKSUM_PLACEHOLDER,
                "checksum_algorithm": "sha256",
                "generated_fixture_checksum": DRY_RUN_GENERATED_CHECKSUM_PLACEHOLDER,
                "script_version": DRY_RUN_SCRIPT_VERSION,
                "parser_version": "v0-dry-run",
                "derivation_timestamp": DRY_RUN_DERIVATION_TIMESTAMP_PLACEHOLDER,
                "entry_posture": {
                    "fixture_derivation_approved": False,
                    "fixture_commit_approved": False,
                    "fixture_written": False,
                    "archive_rows_read": False,
                    "source_payload_read": False,
                    "normalization_applied": False,
                    "runtime_loader_used": False,
                },
            }
        )
    return {
        "manifest_ref": config.get("manifest_ref", DEFAULT_DRY_RUN_MANIFEST_REF),
        "schema_version": config.get("schema_version", DEFAULT_DRY_RUN_SCHEMA_VERSION),
        "phase": "phase1-04",
        "manifest_status": "dry_run_manifest",
        "created_by": config["created_by"],
        "created_at": "dry_run_manifest_not_timestamped",
        "source_manifest_ref": config["source_manifest_ref"],
        "source_repo_ref": config["source_repo_ref"],
        "source_repo_commit": config["source_repo_commit"],
        "source_archive_ref": config["source_archive_ref"],
        "fixture_derivation_approval_ref": "dry_run_only",
        "fixture_commit_approval_ref": "dry_run_only",
        "fixture_entries": fixture_entries,
        "global_posture": {
            "research_only": True,
            "local_only": True,
            "network_allowed": False,
            "api_calls_allowed": False,
            "secrets_allowed": False,
            "connector_import_allowed": False,
            "archive_import_allowed": False,
            "fixture_writes_allowed": False,
            "loader_execution_allowed": False,
            "order_routing_allowed": False,
            "live_trading_allowed": False,
            "autonomous_execution_allowed": False,
        },
        "artifact_hygiene": {
            "no_compressed_archives_committed": True,
            "no_extracted_archive_data_committed": True,
            "no_absolute_archive_paths_in_payloads": True,
            "no_duckdb_artifacts": True,
            "no_generated_reports": True,
            "no_external_repo_files": True,
            "no_network_outputs": True,
            "no_secret_material": True,
            "appledouble_files_ignored": True,
        },
        "reviewer_envelope": {
            "human_review_required": True,
            "reviewer_ref": None,
            "reviewed_at": None,
            "review_decision": "pending",
            "review_rationale": "dry-run manifest only; no derivation or commit approval granted",
        },
    }


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.command == "check":
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

    config = build_default_dry_run_config(
        source_manifest_ref=args.source_manifest_ref,
        source_repo_ref=args.source_repo_ref,
        source_repo_commit=args.source_repo_commit,
        source_archive_ref=args.source_archive_ref,
        created_by=args.created_by,
        schema_version=args.schema_version,
        manifest_ref=args.manifest_ref,
    )
    try:
        manifest = build_dry_run_fixture_manifest(config)
    except ValueError as exc:
        print(json.dumps({"manifest_status": "dry_run_blocked", "reasons": [str(exc)]}, sort_keys=True))
        return 1
    print(json.dumps(manifest, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
