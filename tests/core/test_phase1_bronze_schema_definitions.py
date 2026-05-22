from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
DOC_PATH = REPO_ROOT / "docs/phase1/1-06_BRONZE_SCHEMA_DEFINITIONS.md"

COMMON_FIELDS = {
    "fixture_ref",
    "fixture_family",
    "source_platform",
    "source_manifest_ref",
    "source_repo_ref",
    "source_repo_commit",
    "source_archive_ref",
    "source_relative_path",
    "source_file_checksum",
    "source_record_index",
    "source_record_hash",
    "parser_version",
    "schema_version",
    "ingestion_mode",
    "record_status",
    "unresolved_reasons",
    "created_from_fixture",
    "execution_allowed",
    "live_trading_allowed",
    "autonomous_execution_allowed",
}

INGESTION_MODE_ALLOWLIST = {"tiny_fixture", "dry_run_contract"}
RECORD_STATUS_ALLOWLIST = {
    "raw_preserved",
    "parsed_with_warnings",
    "malformed_preserved",
    "unresolved_preserved",
}
UNRESOLVED_REASON_ALLOWLIST = {
    "none",
    "missing_required_raw_field",
    "malformed_raw_value",
    "missing_source_provenance",
    "unresolved_event_grouping",
    "unresolved_ticker_link",
    "unresolved_token_mapping",
    "unresolved_direction",
    "unresolved_block_timestamp",
    "unresolved_legacy_fpmm_mapping",
    "unresolved_collateral_mapping",
    "unsupported_fixture_family",
    "unsupported_source_shape",
}

SCHEMA_MAPPING = {
    "kalshi_markets_tiny": "bronze_kalshi_market",
    "kalshi_trades_tiny": "bronze_kalshi_trade",
    "poly_markets_tiny": "bronze_poly_market",
    "poly_clob_trades_tiny": "bronze_poly_clob_trade",
    "poly_blocks_tiny": "bronze_poly_block",
    "poly_legacy_fpmm_trades_tiny": "bronze_poly_legacy_fpmm_trade",
    "poly_fpmm_collateral_lookup_tiny": "bronze_poly_fpmm_collateral_lookup",
}

RAW_FIELDS_BY_SCHEMA = {
    "bronze_kalshi_market": {
        "ticker", "event_ticker", "market_type", "title", "yes_sub_title", "no_sub_title", "status",
        "yes_bid", "yes_ask", "no_bid", "no_ask", "last_price", "volume", "volume_24h", "open_interest",
        "result", "created_time", "open_time", "close_time", "fetched_at",
        "price_fields_preserved", "result_preserved", "event_grouping_unresolved",
    },
    "bronze_kalshi_trade": {
        "trade_id", "ticker", "count", "yes_price", "no_price", "taker_side", "created_time", "fetched_at",
        "linked_market_unresolved", "taker_side_preserved", "price_fields_preserved",
    },
    "bronze_poly_market": {
        "source_market_ref", "condition_id", "question", "slug", "outcomes", "outcome_prices", "clob_token_ids",
        "volume", "liquidity", "active", "closed", "end_date", "created_at", "market_maker_address", "fetched_at",
        "outcomes_preserved", "clob_token_ids_preserved", "token_mapping_unresolved",
    },
    "bronze_poly_clob_trade": {
        "block_number", "transaction_hash", "log_index", "order_hash", "maker", "taker", "maker_asset_id",
        "taker_asset_id", "maker_amount", "taker_amount", "fee", "timestamp", "fetched_at", "contract_ref",
        "maker_asset_preserved", "taker_asset_preserved", "token_mapping_unresolved", "direction_unresolved",
    },
    "bronze_poly_block": {"block_number", "timestamp", "block_timestamp_preserved"},
    "bronze_poly_legacy_fpmm_trade": {
        "block_number", "transaction_hash", "log_index", "fpmm_address", "trader", "amount", "fee_amount",
        "outcome_index", "outcome_tokens", "is_buy", "timestamp", "fetched_at",
        "legacy_fpmm_path", "outcome_tokens_preserved", "collateral_mapping_unresolved",
    },
    "bronze_poly_fpmm_collateral_lookup": {
        "fpmm_or_contract_ref", "collateral_token", "collateral_symbol", "collateral_decimals", "collateral_lookup_preserved",
    },
}


def _doc_text() -> str:
    return DOC_PATH.read_text(encoding="utf-8")


def _base_common(fixture_family: str) -> dict[str, object]:
    return {
        "fixture_ref": f"{fixture_family}::sample",
        "fixture_family": fixture_family,
        "source_platform": "kalshi" if fixture_family.startswith("kalshi") else "polymarket",
        "source_manifest_ref": "local_poly_kalshi_historical_archive_placeholder",
        "source_repo_ref": "agastyasinghing/MEG",
        "source_repo_commit": "7574d0d",
        "source_archive_ref": "local_archive_placeholder",
        "source_relative_path": "archives/phase1/sanitized_source.json",
        "source_file_checksum": "sha256:abc123",
        "source_record_index": 0,
        "source_record_hash": "sha256:def456",
        "parser_version": "phase1-06-draft",
        "schema_version": "phase1-06",
        "ingestion_mode": "tiny_fixture",
        "record_status": "raw_preserved",
        "unresolved_reasons": ["none"],
        "created_from_fixture": True,
        "execution_allowed": False,
        "live_trading_allowed": False,
        "autonomous_execution_allowed": False,
    }


def _records() -> dict[str, dict[str, object]]:
    return {
        "bronze_kalshi_market": {
            **_base_common("kalshi_markets_tiny"),
            "ticker": "KX-EXAMPLE-001",
            "event_ticker": "KX-EVT",
            "market_type": "binary",
            "title": "Sample Kalshi market",
            "yes_sub_title": "Yes",
            "no_sub_title": "No",
            "status": "open",
            "yes_bid": 48,
            "yes_ask": 52,
            "no_bid": 47,
            "no_ask": 53,
            "last_price": 50,
            "volume": 1000,
            "volume_24h": 200,
            "open_interest": 800,
            "result": "unresolved",
            "created_time": "2026-05-21T00:00:00Z",
            "open_time": "2026-05-21T00:05:00Z",
            "close_time": "2026-05-21T23:55:00Z",
            "fetched_at": "2026-05-21T12:00:00Z",
            "price_fields_preserved": True,
            "result_preserved": True,
            "event_grouping_unresolved": False,
        },
        "bronze_kalshi_trade": {
            **_base_common("kalshi_trades_tiny"),
            "trade_id": "trade-1",
            "ticker": "KX-EXAMPLE-001",
            "count": 3,
            "yes_price": 51,
            "no_price": 49,
            "taker_side": "yes",
            "created_time": "2026-05-21T00:06:00Z",
            "fetched_at": "2026-05-21T12:00:00Z",
            "linked_market_unresolved": False,
            "taker_side_preserved": True,
            "price_fields_preserved": True,
        },
        "bronze_poly_market": {
            **_base_common("poly_markets_tiny"),
            "source_market_ref": "poly-native-001",
            "condition_id": "0xcondition001",
            "question": "Sample Polymarket question?",
            "slug": "sample-polymarket-question",
            "outcomes": ["Yes", "No"],
            "outcome_prices": [0.52, 0.48],
            "clob_token_ids": ["100", "200"],
            "volume": "5000",
            "liquidity": "2000",
            "active": True,
            "closed": False,
            "end_date": "2026-06-01T00:00:00Z",
            "created_at": "2026-05-20T00:00:00Z",
            "market_maker_address": "0xmarketmaker",
            "fetched_at": "2026-05-21T12:00:00Z",
            "outcomes_preserved": True,
            "clob_token_ids_preserved": True,
            "token_mapping_unresolved": False,
        },
        "bronze_poly_clob_trade": {
            **_base_common("poly_clob_trades_tiny"),
            "block_number": 123,
            "transaction_hash": "0xtxhash",
            "log_index": 1,
            "order_hash": "0xorderhash",
            "maker": "0xmaker",
            "taker": "0xtaker",
            "maker_asset_id": "asset-a",
            "taker_asset_id": "asset-b",
            "maker_amount": "100",
            "taker_amount": "200",
            "fee": "1",
            "timestamp": "2026-05-21T12:01:00Z",
            "fetched_at": "2026-05-21T12:02:00Z",
            "contract_ref": "clob-v2",
            "maker_asset_preserved": True,
            "taker_asset_preserved": True,
            "token_mapping_unresolved": False,
            "direction_unresolved": False,
        },
        "bronze_poly_block": {
            **_base_common("poly_blocks_tiny"),
            "block_number": 123,
            "timestamp": "2026-05-21T12:00:00Z",
            "block_timestamp_preserved": True,
        },
        "bronze_poly_legacy_fpmm_trade": {
            **_base_common("poly_legacy_fpmm_trades_tiny"),
            "block_number": 88,
            "transaction_hash": "0xlegacytx",
            "log_index": 2,
            "fpmm_address": "0xfpmm",
            "trader": "0xtrader",
            "amount": "50",
            "fee_amount": "1",
            "outcome_index": 0,
            "outcome_tokens": "77",
            "is_buy": True,
            "timestamp": "2026-05-21T12:05:00Z",
            "fetched_at": "2026-05-21T12:06:00Z",
            "legacy_fpmm_path": True,
            "outcome_tokens_preserved": True,
            "collateral_mapping_unresolved": False,
        },
        "bronze_poly_fpmm_collateral_lookup": {
            **_base_common("poly_fpmm_collateral_lookup_tiny"),
            "fpmm_or_contract_ref": "0xfpmm",
            "collateral_token": "0xusdc",
            "collateral_symbol": "USDC",
            "collateral_decimals": 6,
            "collateral_lookup_preserved": True,
        },
    }


def _validate(schema_name: str, record: dict[str, object]) -> None:
    missing_common = COMMON_FIELDS - set(record)
    assert not missing_common
    assert record["fixture_family"] in SCHEMA_MAPPING
    assert SCHEMA_MAPPING[record["fixture_family"]] == schema_name
    assert record["ingestion_mode"] in INGESTION_MODE_ALLOWLIST
    assert record["record_status"] in RECORD_STATUS_ALLOWLIST
    assert isinstance(record["unresolved_reasons"], list)
    assert set(record["unresolved_reasons"]).issubset(UNRESOLVED_REASON_ALLOWLIST)
    assert record["execution_allowed"] is False
    assert record["live_trading_allowed"] is False
    assert record["autonomous_execution_allowed"] is False

    source_relative_path = str(record["source_relative_path"])
    assert not source_relative_path.startswith("/")
    assert not source_relative_path.startswith("C:\\")
    assert "archive" in source_relative_path

    missing_raw = RAW_FIELDS_BY_SCHEMA[schema_name] - set(record)
    assert not missing_raw


def test_bronze_schema_doc_exists() -> None:
    assert DOC_PATH.exists()


def test_doc_posture_and_prd_alignment_notes_present() -> None:
    lowered = _doc_text().lower()
    assert "documentation + static/preflight only" in lowered
    assert "does **not** generate, derive, or commit fixtures" in lowered
    assert "does **not** read archive payloads" in lowered
    assert "real phase 1 target is the **weather paper engine**" in lowered


def test_doc_includes_metadata_contracts_mappings_and_taxonomy() -> None:
    text = _doc_text()
    for field in COMMON_FIELDS:
        assert f"`{field}`" in text
    for schema_name in RAW_FIELDS_BY_SCHEMA:
        assert f"`{schema_name}`" in text
    for fixture_family, schema_name in SCHEMA_MAPPING.items():
        assert f"`{fixture_family}` -> `{schema_name}`" in text
    for reason in UNRESOLVED_REASON_ALLOWLIST:
        assert f"`{reason}`" in text
    assert "Bronze does not create `silver_kalshi_markets`" in text
    assert "must remain false" in text


def test_representative_records_pass_validation() -> None:
    for schema_name, record in _records().items():
        _validate(schema_name, record)


def test_missing_common_metadata_field_fails() -> None:
    record = deepcopy(_records()["bronze_kalshi_market"])
    record.pop("schema_version")
    with pytest.raises(AssertionError):
        _validate("bronze_kalshi_market", record)


def test_missing_raw_field_fails() -> None:
    record = deepcopy(_records()["bronze_poly_market"])
    record.pop("condition_id")
    with pytest.raises(AssertionError):
        _validate("bronze_poly_market", record)


def test_unsupported_fixture_family_fails() -> None:
    record = deepcopy(_records()["bronze_poly_block"])
    record["fixture_family"] = "unsupported_family"
    with pytest.raises(AssertionError):
        _validate("bronze_poly_block", record)


def test_unsupported_ingestion_mode_fails() -> None:
    record = deepcopy(_records()["bronze_poly_block"])
    record["ingestion_mode"] = "runtime_import"
    with pytest.raises(AssertionError):
        _validate("bronze_poly_block", record)


def test_unsupported_record_status_fails() -> None:
    record = deepcopy(_records()["bronze_poly_block"])
    record["record_status"] = "ready_for_live"
    with pytest.raises(AssertionError):
        _validate("bronze_poly_block", record)


def test_unsupported_unresolved_reason_fails() -> None:
    record = deepcopy(_records()["bronze_poly_block"])
    record["unresolved_reasons"] = ["unknown_reason"]
    with pytest.raises(AssertionError):
        _validate("bronze_poly_block", record)


def test_execution_flags_true_fails() -> None:
    record = deepcopy(_records()["bronze_poly_block"])
    record["execution_allowed"] = True
    with pytest.raises(AssertionError):
        _validate("bronze_poly_block", record)


def test_absolute_source_relative_path_fails() -> None:
    record = deepcopy(_records()["bronze_poly_block"])
    record["source_relative_path"] = "/tmp/local/archive.json"
    with pytest.raises(AssertionError):
        _validate("bronze_poly_block", record)


def test_fixture_family_maps_to_expected_schema() -> None:
    for fixture_family, schema_name in SCHEMA_MAPPING.items():
        record = next(v for v in _records().values() if v["fixture_family"] == fixture_family)
        _validate(schema_name, record)


def test_no_fixture_output_directory_exists() -> None:
    assert not (REPO_ROOT / "fixtures/phase1").exists()


def test_no_real_fixture_payloads_or_runtime_fixture_reads_required() -> None:
    fixtures_dir = REPO_ROOT / "fixtures/phase1"
    assert not fixtures_dir.exists()

    fixture_payload_candidates = list((REPO_ROOT / "fixtures").glob("phase1/*.json"))
    assert fixture_payload_candidates == []

    archive_payload_candidates = list((REPO_ROOT / "fixtures").glob("phase1/*.parquet"))
    assert archive_payload_candidates == []


def test_bronze_schema_contract_test_is_static_and_pathlib_only() -> None:
    test_source = Path(__file__).read_text(encoding="utf-8")
    lowered = test_source.lower()
    assert "import " + "subprocess" not in lowered
    assert "sub" + "process." not in lowered
    assert "git" + " status" not in lowered
    assert ".r" + "glob(" not in test_source
    assert "read_text" in test_source
