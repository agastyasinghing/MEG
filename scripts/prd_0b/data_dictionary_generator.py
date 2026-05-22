from __future__ import annotations

import argparse
import json
import pathlib
import sys
import datetime
from typing import Any

from scripts.prd_0b.local_research_lake_smoke import (
    find_sample_parquet_files,
    try_import_duckdb,
    validate_archive_root_path,
)

REQUIRED_SPEC_FIELDS = {
    "dataset_ref",
    "source_platform",
    "source_kind",
    "source_relative_path",
    "related_sanity_check_name",
    "related_bronze_schema",
    "related_normalization_plan",
    "expected_columns",
    "primary_reference_fields",
    "temporal_fields",
    "numeric_fields",
    "boolean_fields",
    "json_fields",
    "provenance_fields",
    "unresolved_state_fields",
    "known_raw_field_aliases",
}


def get_dataset_dictionary_specs() -> list[dict[str, object]]:
    return [
        {"dataset_ref": "kalshi_markets", "source_platform": "kalshi", "source_kind": "parquet_family", "source_relative_path": "data/kalshi/markets", "related_sanity_check_name": "kalshi_markets_schema_count_sample", "related_bronze_schema": "bronze_kalshi_market", "related_normalization_plan": "docs/phase0b/0B-22_KALSHI_NORMALIZED_FILLS_MARKETS_MAPPING_PLAN.md", "expected_columns": ["ticker", "event_ticker", "market_type", "title", "yes_sub_title", "no_sub_title", "status", "yes_bid", "yes_ask", "no_bid", "no_ask", "last_price", "volume", "volume_24h", "open_interest", "result", "created_time", "open_time", "close_time", "_fetched_at"], "primary_reference_fields": ["ticker", "event_ticker"], "temporal_fields": ["created_time", "open_time", "close_time", "_fetched_at"], "numeric_fields": ["yes_bid", "yes_ask", "no_bid", "no_ask", "last_price", "volume", "volume_24h", "open_interest"], "boolean_fields": [], "json_fields": [], "provenance_fields": ["_fetched_at"], "unresolved_state_fields": ["result", "status"], "known_raw_field_aliases": []},
        {"dataset_ref": "kalshi_trades", "source_platform": "kalshi", "source_kind": "parquet_family", "source_relative_path": "data/kalshi/trades", "related_sanity_check_name": "kalshi_trades_schema_count_sample", "related_bronze_schema": "bronze_kalshi_trade", "related_normalization_plan": "docs/phase0b/0B-22_KALSHI_NORMALIZED_FILLS_MARKETS_MAPPING_PLAN.md", "expected_columns": ["trade_id", "ticker", "count", "yes_price", "no_price", "taker_side", "created_time", "_fetched_at"], "primary_reference_fields": ["trade_id", "ticker"], "temporal_fields": ["created_time", "_fetched_at"], "numeric_fields": ["count", "yes_price", "no_price"], "boolean_fields": [], "json_fields": [], "provenance_fields": ["_fetched_at"], "unresolved_state_fields": ["taker_side"], "known_raw_field_aliases": []},
        {"dataset_ref": "poly_markets", "source_platform": "polymarket", "source_kind": "parquet_family", "source_relative_path": "data/polymarket/markets", "related_sanity_check_name": "poly_markets_schema_count_sample", "related_bronze_schema": "bronze_poly_market", "related_normalization_plan": "docs/phase0b/0B-21_POLYMARKET_TOKEN_OUTCOME_NORMALIZATION_PLAN.md", "expected_columns": ["id", "condition_id", "question", "slug", "outcomes", "outcome_prices", "clob_token_ids", "volume", "liquidity", "active", "closed", "end_date", "created_at", "market_maker_address", "_fetched_at"], "primary_reference_fields": ["id", "condition_id"], "temporal_fields": ["created_at", "end_date", "_fetched_at"], "numeric_fields": ["volume", "liquidity"], "boolean_fields": ["active", "closed"], "json_fields": ["outcomes", "outcome_prices", "clob_token_ids"], "provenance_fields": ["_fetched_at"], "unresolved_state_fields": ["active", "closed"], "known_raw_field_aliases": [{"source_field": "id", "canonical_hint": "source_market_ref"}]},
        {"dataset_ref": "poly_clob_trades", "source_platform": "polymarket", "source_kind": "parquet_family", "source_relative_path": "data/polymarket/trades", "related_sanity_check_name": "poly_clob_trades_schema_count_sample", "related_bronze_schema": "bronze_poly_clob_trade", "related_normalization_plan": "docs/phase0b/0B-21_POLYMARKET_TOKEN_OUTCOME_NORMALIZATION_PLAN.md", "expected_columns": ["block_number", "transaction_hash", "log_index", "order_hash", "maker", "taker", "maker_asset_id", "taker_asset_id", "maker_amount", "taker_amount", "fee", "timestamp", "_fetched_at", "_contract"], "primary_reference_fields": ["transaction_hash", "log_index", "order_hash"], "temporal_fields": ["timestamp", "_fetched_at"], "numeric_fields": ["block_number", "maker_amount", "taker_amount", "fee"], "boolean_fields": [], "json_fields": [], "provenance_fields": ["_fetched_at", "_contract"], "unresolved_state_fields": [], "known_raw_field_aliases": []},
        {"dataset_ref": "poly_blocks", "source_platform": "polymarket", "source_kind": "parquet_family", "source_relative_path": "data/polymarket/blocks", "related_sanity_check_name": "poly_blocks_schema_count_sample", "related_bronze_schema": "bronze_poly_block", "related_normalization_plan": "docs/phase0b/0B-21_POLYMARKET_TOKEN_OUTCOME_NORMALIZATION_PLAN.md", "expected_columns": ["block_number", "timestamp"], "primary_reference_fields": ["block_number"], "temporal_fields": ["timestamp"], "numeric_fields": ["block_number"], "boolean_fields": [], "json_fields": [], "provenance_fields": [], "unresolved_state_fields": [], "known_raw_field_aliases": []},
        {"dataset_ref": "poly_legacy_fpmm_trades", "source_platform": "polymarket", "source_kind": "parquet_family", "source_relative_path": "data/polymarket/legacy_trades", "related_sanity_check_name": "poly_legacy_fpmm_trades_schema_count_sample", "related_bronze_schema": "bronze_poly_legacy_fpmm_trade", "related_normalization_plan": "docs/phase0b/0B-21_POLYMARKET_TOKEN_OUTCOME_NORMALIZATION_PLAN.md", "expected_columns": ["block_number", "transaction_hash", "log_index", "fpmm_address", "trader", "amount", "fee_amount", "outcome_index", "outcome_tokens", "is_buy", "timestamp", "_fetched_at"], "primary_reference_fields": ["transaction_hash", "log_index"], "temporal_fields": ["timestamp", "_fetched_at"], "numeric_fields": ["block_number", "amount", "fee_amount", "outcome_index", "outcome_tokens"], "boolean_fields": ["is_buy"], "json_fields": [], "provenance_fields": ["_fetched_at"], "unresolved_state_fields": ["outcome_index"], "known_raw_field_aliases": []},
        {"dataset_ref": "poly_fpmm_collateral_lookup", "source_platform": "polymarket", "source_kind": "json_sidecar", "source_relative_path": "data/polymarket/fpmm_collateral_lookup.json", "related_sanity_check_name": "poly_fpmm_collateral_lookup_presence", "related_bronze_schema": "bronze_poly_fpmm_collateral_lookup", "related_normalization_plan": "docs/phase0b/0B-21_POLYMARKET_TOKEN_OUTCOME_NORMALIZATION_PLAN.md", "expected_columns": ["fpmm_or_contract_ref", "collateral_token", "collateral_symbol", "collateral_decimals"], "primary_reference_fields": ["fpmm_or_contract_ref"], "temporal_fields": [], "numeric_fields": ["collateral_decimals"], "boolean_fields": [], "json_fields": [], "provenance_fields": [], "unresolved_state_fields": [], "known_raw_field_aliases": []},
    ]


def validate_dataset_dictionary_specs(specs: list[dict[str, object]]) -> list[str]:
    errors: list[str] = []
    if len(specs) != 7:
        errors.append("dataset_spec_count_not_seven")
    refs = [str(s.get("dataset_ref", "")) for s in specs]
    if len(set(refs)) != len(refs):
        errors.append("dataset_refs_not_unique")
    for spec in specs:
        ref = str(spec.get("dataset_ref", "unknown"))
        for field in REQUIRED_SPEC_FIELDS:
            if field not in spec:
                errors.append(f"missing_required_field:{ref}:{field}")
    return errors


def build_static_column_metadata(dataset_spec: dict[str, object], observed_columns: list[str] | None = None, observed_types: dict[str, str] | None = None) -> list[dict[str, object]]:
    observed_columns = observed_columns or []
    observed_types = observed_types or {}
    out = []
    for col in list(dataset_spec["expected_columns"]):
        is_obs = col in observed_columns
        out.append({"column_name": col, "source_name": col, "logical_role": "contract_field", "raw_type_observed": observed_types.get(col, "not_observed_static_contract" if not is_obs else "observed_via_duckdb_describe"), "normalized_type_target": "string_or_numeric_needs_review", "nullable_status": "unknown_needs_review", "semantic_notes": "planned_from_prd_0b_impl_03", "validation_notes": "expected_column_contract", "pii_or_secret_status": "public_chain_address_or_actor_ref" if any(t in col for t in ["maker", "taker", "trader", "address"]) else "no_private_pii_expected", "used_for_joining": col in set(dataset_spec.get("primary_reference_fields", [])), "used_for_time_filtering": col in set(dataset_spec.get("temporal_fields", [])), "used_for_price_or_size": col in set(dataset_spec.get("numeric_fields", [])), "used_for_resolution_or_result": col in {"result", "outcome_index", "outcome_tokens"}, "used_for_wallet_or_actor": any(t in col for t in ["maker", "taker", "trader", "address"]), "unresolved_handling": "defer_to_review"})
    return out


def extract_duckdb_schema_metadata(archive_root: str, dataset_specs: list[dict[str, object]], require_duckdb: bool = False) -> dict[str, object]:
    ok, duckdb_mod, err = try_import_duckdb()
    if not ok or duckdb_mod is None:
        if require_duckdb:
            raise RuntimeError("require_duckdb_but_unavailable")
        return {"duckdb_available": False, "warnings": [str(err or "duckdb_unavailable")], "observed": {}, "payload_read": False, "duckdb_execution": False}
    samples = find_sample_parquet_files(archive_root)
    observed: dict[str, dict[str, object]] = {}
    conn = duckdb_mod.connect(":memory:")
    try:
        for spec in dataset_specs:
            if spec["source_kind"] != "parquet_family":
                continue
            family = str(spec["source_relative_path"])
            sample = samples.get(family)
            ref = str(spec["dataset_ref"])
            if not sample:
                observed[ref] = {"observed_columns": [], "observed_types": {}, "warnings": ["missing_sample"]}
                continue
            qpath = "'" + str((pathlib.Path(archive_root) / sample).resolve()).replace("'", "''") + "'"
            try:
                rows = conn.execute(f"DESCRIBE SELECT * FROM parquet_scan({qpath})").fetchall()
                observed[ref] = {"observed_columns": [str(r[0]) for r in rows], "observed_types": {str(r[0]): str(r[1]) for r in rows}, "warnings": []}
            except Exception as exc:
                observed[ref] = {"observed_columns": [], "observed_types": {}, "warnings": [f"query_failed:{exc.__class__.__name__}"]}
    finally:
        conn.close()
    return {"duckdb_available": True, "warnings": [], "observed": observed, "payload_read": True, "duckdb_execution": True}


def build_data_dictionary(config: dict[str, object]) -> dict[str, object]:
    specs = get_dataset_dictionary_specs()
    errors = validate_dataset_dictionary_specs(specs)
    if errors:
        raise ValueError(";".join(errors))
    mode = str(config["mode"])
    if mode not in {"static_specs_only", "duckdb_schema_metadata_if_available"}:
        raise ValueError("unsupported_mode")
    output_mode = str(config["output_mode"])
    if output_mode not in {"stdout_only", "tempdir_only_for_tests"}:
        raise ValueError("blocked_output_mode")
    observed_map: dict[str, dict[str, object]] = {}
    warnings: list[str] = []
    payload_read = False
    duck_exec = False
    if mode == "duckdb_schema_metadata_if_available":
        meta = extract_duckdb_schema_metadata(str(config["archive_root"]), specs, require_duckdb=bool(config.get("require_duckdb", False)))
        observed_map = {k: v for k, v in meta["observed"].items()} if "observed" in meta else {}
        warnings.extend(list(meta.get("warnings", [])))
        payload_read = bool(meta.get("payload_read", False))
        duck_exec = bool(meta.get("duckdb_execution", False))
    entries = []
    for spec in specs:
        ref = str(spec["dataset_ref"])
        observed_cols = list(observed_map.get(ref, {}).get("observed_columns", []))
        observed_types = dict(observed_map.get(ref, {}).get("observed_types", {}))
        missing = [c for c in list(spec["expected_columns"]) if c not in observed_cols] if observed_cols else []
        entries.append({**spec, "observed_columns": observed_cols, "missing_columns": missing, "column_metadata": build_static_column_metadata(spec, observed_cols, observed_types), "future_dictionary_status": "generated_from_local_archive" if observed_cols else "planned_only", "generation_notes": ["json_sidecar_static_only"] if spec["source_kind"] == "json_sidecar" else list(observed_map.get(ref, {}).get("warnings", []))})
    now = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    return {"dictionary_ref": "prd_0b_local_data_dictionary", "schema_version": "0.1.0", "phase": "PRD-0B-IMPL-05", "dictionary_status": "generated_pending_review", "created_by": config["created_by"], "created_at": now, "source_manifest_ref": config["source_manifest_ref"], "source_repo_ref": config["source_repo_ref"], "source_repo_commit": config["source_repo_commit"], "source_archive_ref": config["source_archive_ref"], "generation_mode": "local_generated_from_sanity_harness", "dataset_entries": entries, "global_posture": {"research_only": True, "local_only": True, "archive_payload_read_allowed": payload_read, "duckdb_execution_allowed": duck_exec, "generated_output_allowed": True, "committed_data_allowed": False, "fixture_commit_allowed": False, "bronze_silver_view_creation_allowed": False, "loader_execution_allowed": False, "connector_import_allowed": False, "api_calls_allowed": False, "order_routing_allowed": False, "live_trading_allowed": False, "autonomous_execution_allowed": False}, "artifact_hygiene": {"no_row_level_archive_export": True, "no_committed_dictionary_file": True, "no_duckdb_artifacts": True, "no_generated_reports": True, "no_committed_archive_data": True, "no_fixture_outputs": True, "no_external_repo_files": True, "no_secret_material": True, "no_absolute_archive_paths": True}, "reviewer_envelope": {"warnings": warnings}}


def write_dictionary_tempdir_only(dictionary: dict[str, object], output_dir: str) -> pathlib.Path:
    if not output_dir:
        raise ValueError("output_dir_required")
    out = pathlib.Path(output_dir).resolve()
    if not out.exists() or not out.is_dir():
        raise ValueError("output_dir_must_exist_dir")
    cwd = pathlib.Path.cwd().resolve()
    if out == cwd:
        raise ValueError("unsafe_output_dir")
    blocked = {"docs", "data", "fixtures", "reports", "generated", "sql"}
    if any(part in blocked for part in out.parts):
        raise ValueError("unsafe_output_dir")
    if cwd in out.parents and "pytest-" not in str(out):
        raise ValueError("unsafe_output_dir")
    target = out / "prd_0b_data_dictionary.generated.json"
    target.write_text(json.dumps(dictionary, indent=2, sort_keys=True), encoding="utf-8")
    return target


def _parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    gen = sub.add_parser("generate")
    gen.add_argument("--archive-root")
    gen.add_argument("--source-manifest-ref", required=True)
    gen.add_argument("--source-repo-ref", required=True)
    gen.add_argument("--source-repo-commit", required=True)
    gen.add_argument("--source-archive-ref", required=True)
    gen.add_argument("--created-by", required=True)
    gen.add_argument("--mode", required=True, choices=["static_specs_only", "duckdb_schema_metadata_if_available"])
    gen.add_argument("--output-mode", required=True, choices=["stdout_only", "tempdir_only_for_tests"])
    gen.add_argument("--output-dir")
    gen.add_argument("--require-duckdb", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv or sys.argv[1:])
    if args.command != "generate":
        return 2
    if args.mode == "duckdb_schema_metadata_if_available":
        if not args.archive_root:
            print("archive_root_required_for_duckdb_mode", file=sys.stderr)
            return 1
        if not validate_archive_root_path(args.archive_root).ok:
            print("invalid_archive_root", file=sys.stderr)
            return 1
    config = vars(args)
    try:
        dictionary = build_data_dictionary(config)
        if args.output_mode == "stdout_only":
            print(json.dumps(dictionary, indent=2, sort_keys=True))
        else:
            if not args.output_dir:
                print("output_dir_required", file=sys.stderr)
                return 1
            write_dictionary_tempdir_only(dictionary, args.output_dir)
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
