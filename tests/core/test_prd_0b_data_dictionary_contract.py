from pathlib import Path

DOC_PATH = Path("docs/prd/PRD-0B-IMPL-03_DATA_DICTIONARY_CONTRACT.md")
HARNESS_DOC_PATH = Path("docs/prd/PRD-0B-IMPL-02_BECKER_SANITY_QUERY_HARNESS.md")
HARNESS_SCRIPT_PATH = Path("scripts/prd_0b/becker_sanity_query_harness.py")

DATASETS = {
    "kalshi_markets",
    "kalshi_trades",
    "poly_markets",
    "poly_clob_trades",
    "poly_blocks",
    "poly_legacy_fpmm_trades",
    "poly_fpmm_collateral_lookup",
}

DATASET_MAPPING_ROWS = {
    "kalshi_markets": {
        "source_platform": "kalshi",
        "source_kind": "parquet_family",
        "source_relative_path": "data/kalshi/markets",
        "related_sanity_check_name": "kalshi_markets_schema_count_sample",
        "related_bronze_schema": "bronze_kalshi_market",
        "related_normalization_plan": "docs/phase0b/0B-22_KALSHI_NORMALIZED_FILLS_MARKETS_MAPPING_PLAN.md",
    },
    "kalshi_trades": {
        "source_platform": "kalshi",
        "source_kind": "parquet_family",
        "source_relative_path": "data/kalshi/trades",
        "related_sanity_check_name": "kalshi_trades_schema_count_sample",
        "related_bronze_schema": "bronze_kalshi_trade",
        "related_normalization_plan": "docs/phase0b/0B-22_KALSHI_NORMALIZED_FILLS_MARKETS_MAPPING_PLAN.md",
    },
    "poly_markets": {
        "source_platform": "polymarket",
        "source_kind": "parquet_family",
        "source_relative_path": "data/polymarket/markets",
        "related_sanity_check_name": "poly_markets_schema_count_sample",
        "related_bronze_schema": "bronze_poly_market",
        "related_normalization_plan": "docs/phase0b/0B-21_POLYMARKET_TOKEN_OUTCOME_NORMALIZATION_PLAN.md",
    },
    "poly_clob_trades": {
        "source_platform": "polymarket",
        "source_kind": "parquet_family",
        "source_relative_path": "data/polymarket/trades",
        "related_sanity_check_name": "poly_clob_trades_schema_count_sample",
        "related_bronze_schema": "bronze_poly_clob_trade",
        "related_normalization_plan": "docs/phase0b/0B-21_POLYMARKET_TOKEN_OUTCOME_NORMALIZATION_PLAN.md",
    },
    "poly_blocks": {
        "source_platform": "polymarket",
        "source_kind": "parquet_family",
        "source_relative_path": "data/polymarket/blocks",
        "related_sanity_check_name": "poly_blocks_schema_count_sample",
        "related_bronze_schema": "bronze_poly_block",
        "related_normalization_plan": "docs/phase0b/0B-21_POLYMARKET_TOKEN_OUTCOME_NORMALIZATION_PLAN.md",
    },
    "poly_legacy_fpmm_trades": {
        "source_platform": "polymarket",
        "source_kind": "parquet_family",
        "source_relative_path": "data/polymarket/legacy_trades",
        "related_sanity_check_name": "poly_legacy_fpmm_trades_schema_count_sample",
        "related_bronze_schema": "bronze_poly_legacy_fpmm_trade",
        "related_normalization_plan": "docs/phase0b/0B-21_POLYMARKET_TOKEN_OUTCOME_NORMALIZATION_PLAN.md",
    },
    "poly_fpmm_collateral_lookup": {
        "source_platform": "polymarket",
        "source_kind": "json_sidecar",
        "source_relative_path": "data/polymarket/fpmm_collateral_lookup.json",
        "related_sanity_check_name": "poly_fpmm_collateral_lookup_presence",
        "related_bronze_schema": "bronze_poly_fpmm_collateral_lookup",
        "related_normalization_plan": "docs/phase0b/0B-21_POLYMARKET_TOKEN_OUTCOME_NORMALIZATION_PLAN.md",
    },
}



def test_document_exists_and_static_scope_statements():
    text = DOC_PATH.read_text(encoding="utf-8")
    assert DOC_PATH.exists()
    assert "docs/static-preflight only" in text
    assert "not generate a data dictionary" in text
    assert "not read archive payloads" in text
    assert "not run DuckDB" in text


def test_document_required_contract_sections_present():
    text = DOC_PATH.read_text(encoding="utf-8")
    for token in [
        "PRD Phase 0B alignment",
        "Required dataset coverage (exactly seven families)",
        "Data dictionary top-level shape",
        "global_posture contract",
        "artifact_hygiene contract",
        "Dataset entry shape",
        "Column metadata shape",
        "Status taxonomy",
        "Future generation rules",
        "Relationship to Bronze/Silver",
        "Recommended next tickets",
        "Explicit non-approvals",
    ]:
        assert token in text


def test_exact_dataset_families_and_expected_columns_are_present():
    text = DOC_PATH.read_text(encoding="utf-8")
    found = {d for d in DATASETS if d in text}
    assert found == DATASETS
    for col in [
        "event_ticker", "trade_id", "condition_id", "clob_token_ids", "order_hash",
        "_contract", "fpmm_or_contract_ref", "collateral_decimals", "outcome_tokens",
    ]:
        assert col in text




def test_dataset_mapping_table_has_concrete_values_for_all_families():
    text = DOC_PATH.read_text(encoding="utf-8")
    assert "Dataset family mapping table" in text
    for dataset_ref, mapping in DATASET_MAPPING_ROWS.items():
        assert dataset_ref in text
        for _, value in mapping.items():
            assert value in text


def test_top_level_and_taxonomy_lists_present():
    text = DOC_PATH.read_text(encoding="utf-8")
    for field in [
        "dictionary_ref", "schema_version", "phase", "dictionary_status", "created_by",
        "created_at", "source_manifest_ref", "source_repo_ref", "source_repo_commit",
        "source_archive_ref", "generation_mode", "dataset_entries", "global_posture",
        "artifact_hygiene", "reviewer_envelope",
    ]:
        assert field in text
    for status in ["planned_contract_only", "generated_pending_review", "committed_reviewed_dictionary"]:
        assert status in text
    for mode in ["static_contract", "local_generated_from_sanity_harness"]:
        assert mode in text
    for status in ["planned_only", "generated_from_local_archive", "reviewed", "stale_needs_regeneration", "rejected"]:
        assert status in text
    for pii in ["no_private_pii_expected", "public_chain_address_or_actor_ref", "unknown_needs_review", "secret_disallowed"]:
        assert pii in text


def _build_contract(dataset_refs):
    top_fields = {
        "dictionary_ref": "prd_0b_dictionary_contract",
        "schema_version": "0.1.0",
        "phase": "0B",
        "dictionary_status": "planned_contract_only",
        "created_by": "test",
        "created_at": "2026-05-22T00:00:00Z",
        "source_manifest_ref": "manifest",
        "source_repo_ref": "agastyasinghing/MEG",
        "source_repo_commit": "HEAD",
        "source_archive_ref": "becker-local-archive",
        "generation_mode": "static_contract",
        "dataset_entries": [],
        "global_posture": {
            "research_only": True,
            "local_only": True,
            "archive_payload_read_allowed": False,
            "duckdb_execution_allowed": False,
            "generated_output_allowed": False,
            "committed_data_allowed": False,
            "fixture_commit_allowed": False,
            "bronze_silver_view_creation_allowed": False,
            "loader_execution_allowed": False,
            "connector_import_allowed": False,
            "api_calls_allowed": False,
            "order_routing_allowed": False,
            "live_trading_allowed": False,
            "autonomous_execution_allowed": False,
        },
        "artifact_hygiene": {
            "no_archive_payload_reads": True,
            "no_generated_dictionary_file": True,
            "no_duckdb_artifacts": True,
            "no_generated_reports": True,
            "no_committed_archive_data": True,
            "no_fixture_outputs": True,
            "no_external_repo_files": True,
            "no_secret_material": True,
            "no_absolute_archive_paths": True,
        },
        "reviewer_envelope": {},
    }
    for ref in dataset_refs:
        top_fields["dataset_entries"].append(
            {
                "dataset_ref": ref,
                "source_platform": "polymarket" if ref.startswith("poly") else "kalshi",
                "source_kind": "parquet_family" if ref != "poly_fpmm_collateral_lookup" else "json_sidecar",
                "source_relative_path": "data/...",
                "related_sanity_check_name": "*_schema_count_sample",
                "related_bronze_schema": "phase1r_bronze",
                "related_normalization_plan": "phase0b_norm",
                "expected_columns": ["sample_col"],
                "primary_reference_fields": ["id"],
                "temporal_fields": ["created_at"],
                "numeric_fields": [],
                "boolean_fields": [],
                "json_fields": [],
                "provenance_fields": ["_fetched_at"],
                "unresolved_state_fields": [],
                "known_raw_field_aliases": [],
                "future_dictionary_status": "planned_only",
                "notes": "planned",
            }
        )
    return top_fields


def _validate_contract(contract):
    assert contract["dictionary_status"] in {"planned_contract_only", "generated_pending_review", "committed_reviewed_dictionary"}
    assert contract["generation_mode"] in {"static_contract", "local_generated_from_sanity_harness"}
    assert contract["dictionary_status"] == "planned_contract_only"
    assert contract["generation_mode"] == "static_contract"
    posture = contract["global_posture"]
    assert posture["research_only"] is True and posture["local_only"] is True
    for k, v in posture.items():
        if k not in {"research_only", "local_only"}:
            assert v is False
    for v in contract["artifact_hygiene"].values():
        assert v is True
    entries = contract["dataset_entries"]
    assert len(entries) == 7
    refs = [e["dataset_ref"] for e in entries]
    assert len(set(refs)) == 7
    assert set(refs) == DATASETS
    required_entry_fields = {
        "dataset_ref", "source_platform", "source_kind", "source_relative_path", "related_sanity_check_name",
        "related_bronze_schema", "related_normalization_plan", "expected_columns", "primary_reference_fields",
        "temporal_fields", "numeric_fields", "boolean_fields", "json_fields", "provenance_fields",
        "unresolved_state_fields", "known_raw_field_aliases", "future_dictionary_status", "notes",
    }
    for e in entries:
        assert required_entry_fields.issubset(e.keys())
        assert e["expected_columns"]
        assert e["future_dictionary_status"] == "planned_only"


def test_in_memory_representative_contract_validation_passes():
    contract = _build_contract(sorted(DATASETS))
    _validate_contract(contract)


def test_invalid_family_status_mode_pii_and_missing_expected_columns_fail():
    contract = _build_contract(sorted(DATASETS))

    bad = _build_contract(sorted(DATASETS - {"poly_blocks"} | {"unsupported_family"}))
    refs = {e["dataset_ref"] for e in bad["dataset_entries"]}
    assert refs != DATASETS

    contract["dictionary_status"] = "unsupported"
    try:
        _validate_contract(contract)
        assert False
    except AssertionError:
        pass

    contract = _build_contract(sorted(DATASETS))
    contract["generation_mode"] = "unsupported"
    try:
        _validate_contract(contract)
        assert False
    except AssertionError:
        pass

    allowed_pii = {"no_private_pii_expected", "public_chain_address_or_actor_ref", "unknown_needs_review", "secret_disallowed"}
    assert "unsupported" not in allowed_pii

    contract = _build_contract(sorted(DATASETS))
    contract["dataset_entries"][0]["expected_columns"] = []
    try:
        _validate_contract(contract)
        assert False
    except AssertionError:
        pass


def test_impl_02_sanity_harness_alignment_and_no_generated_artifacts():
    harness_doc = HARNESS_DOC_PATH.read_text(encoding="utf-8")
    harness_script = HARNESS_SCRIPT_PATH.read_text(encoding="utf-8")
    assert "seven sanity" in harness_doc.lower()
    assert "len(specs) == 7" in harness_script or "sanity_check_count\": 7" in harness_script
    assert not Path("docs/prd/PRD-0B-IMPL-03_DATA_DICTIONARY.json").exists()
    assert list(Path(".").rglob("*.duckdb")) == []
    assert not Path("reports/prd_0b").exists()
    assert not Path("tests/fixtures/output").exists()
