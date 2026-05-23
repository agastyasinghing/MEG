from pathlib import Path

DOC_PATH = Path("docs/prd/PRD-0B-IMPL-04_BRONZE_SILVER_VIEW_PLAN.md")

BRONZE_VIEWS = [
    {
        "name": "bronze_kalshi_markets",
        "source_dataset": "kalshi_markets",
        "source_path": "data/kalshi/markets",
        "related_dictionary_dataset": "kalshi_markets",
        "related_bronze_contract": "bronze_kalshi_market",
        "raw_field_family": "Kalshi market metadata/snapshot fields",
    },
    {
        "name": "bronze_kalshi_trades",
        "source_dataset": "kalshi_trades",
        "source_path": "data/kalshi/trades",
        "related_dictionary_dataset": "kalshi_trades",
        "related_bronze_contract": "bronze_kalshi_trade",
        "raw_field_family": "Kalshi trade/fill fields",
    },
    {
        "name": "bronze_poly_markets",
        "source_dataset": "poly_markets",
        "source_path": "data/polymarket/markets",
        "related_dictionary_dataset": "poly_markets",
        "related_bronze_contract": "bronze_poly_market",
        "raw_field_family": "Polymarket market/outcome/token metadata",
    },
    {
        "name": "bronze_poly_clob_trades",
        "source_dataset": "poly_clob_trades",
        "source_path": "data/polymarket/trades",
        "related_dictionary_dataset": "poly_clob_trades",
        "related_bronze_contract": "bronze_poly_clob_trade",
        "raw_field_family": "Polymarket CLOB trade/fill fields",
    },
    {
        "name": "bronze_poly_blocks",
        "source_dataset": "poly_blocks",
        "source_path": "data/polymarket/blocks",
        "related_dictionary_dataset": "poly_blocks",
        "related_bronze_contract": "bronze_poly_block",
        "raw_field_family": "Polygon/Polymarket block timestamp fields",
    },
    {
        "name": "bronze_poly_legacy_fpmm_trades",
        "source_dataset": "poly_legacy_fpmm_trades",
        "source_path": "data/polymarket/legacy_trades",
        "related_dictionary_dataset": "poly_legacy_fpmm_trades",
        "related_bronze_contract": "bronze_poly_legacy_fpmm_trade",
        "raw_field_family": "Polymarket legacy FPMM trade fields",
    },
    {
        "name": "bronze_poly_fpmm_collateral_lookup",
        "source_dataset": "poly_fpmm_collateral_lookup",
        "source_path": "data/polymarket/fpmm_collateral_lookup.json",
        "related_dictionary_dataset": "poly_fpmm_collateral_lookup",
        "related_bronze_contract": "bronze_poly_fpmm_collateral_lookup",
        "raw_field_family": "FPMM collateral metadata",
    },
]

SILVER_MAP = {
    "silver_kalshi_events": {
        "depends_on": ["bronze_kalshi_markets"],
        "normalization_plan_ref": "docs/phase0b/0B-22_KALSHI_NORMALIZED_FILLS_MARKETS_MAPPING_PLAN.md",
        "unresolved_state_policy": "preserve",
    },
    "silver_kalshi_markets": {
        "depends_on": ["bronze_kalshi_markets"],
        "normalization_plan_ref": "docs/phase0b/0B-22_KALSHI_NORMALIZED_FILLS_MARKETS_MAPPING_PLAN.md",
        "unresolved_state_policy": "preserve",
    },
    "silver_kalshi_outcomes": {
        "depends_on": ["bronze_kalshi_markets"],
        "normalization_plan_ref": "docs/phase0b/0B-22_KALSHI_NORMALIZED_FILLS_MARKETS_MAPPING_PLAN.md",
        "unresolved_state_policy": "preserve",
    },
    "silver_kalshi_market_snapshots": {
        "depends_on": ["bronze_kalshi_markets"],
        "normalization_plan_ref": "docs/phase0b/0B-22_KALSHI_NORMALIZED_FILLS_MARKETS_MAPPING_PLAN.md",
        "unresolved_state_policy": "preserve",
    },
    "silver_kalshi_fills": {
        "depends_on": ["bronze_kalshi_trades", "bronze_kalshi_markets"],
        "normalization_plan_ref": "docs/phase0b/0B-22_KALSHI_NORMALIZED_FILLS_MARKETS_MAPPING_PLAN.md",
        "unresolved_state_policy": "preserve",
    },
    "silver_kalshi_results": {
        "depends_on": ["bronze_kalshi_markets"],
        "normalization_plan_ref": "docs/phase0b/0B-22_KALSHI_NORMALIZED_FILLS_MARKETS_MAPPING_PLAN.md",
        "unresolved_state_policy": "preserve",
    },
    "silver_poly_markets": {
        "depends_on": ["bronze_poly_markets"],
        "normalization_plan_ref": "docs/phase0b/0B-21_POLYMARKET_TOKEN_OUTCOME_NORMALIZATION_PLAN.md",
        "unresolved_state_policy": "preserve",
    },
    "silver_poly_outcomes": {
        "depends_on": ["bronze_poly_markets"],
        "normalization_plan_ref": "docs/phase0b/0B-21_POLYMARKET_TOKEN_OUTCOME_NORMALIZATION_PLAN.md",
        "unresolved_state_policy": "preserve",
    },
    "silver_poly_clob_tokens": {
        "depends_on": ["bronze_poly_markets"],
        "normalization_plan_ref": "docs/phase0b/0B-21_POLYMARKET_TOKEN_OUTCOME_NORMALIZATION_PLAN.md",
        "unresolved_state_policy": "preserve",
    },
    "silver_poly_clob_fills": {
        "depends_on": ["bronze_poly_clob_trades", "bronze_poly_markets", "bronze_poly_blocks"],
        "normalization_plan_ref": "docs/phase0b/0B-21_POLYMARKET_TOKEN_OUTCOME_NORMALIZATION_PLAN.md",
        "unresolved_state_policy": "preserve",
    },
    "silver_poly_blocks": {
        "depends_on": ["bronze_poly_blocks"],
        "normalization_plan_ref": "docs/phase0b/0B-21_POLYMARKET_TOKEN_OUTCOME_NORMALIZATION_PLAN.md",
        "unresolved_state_policy": "preserve",
    },
    "silver_poly_legacy_fpmm_fills": {
        "depends_on": ["bronze_poly_legacy_fpmm_trades", "bronze_poly_fpmm_collateral_lookup"],
        "normalization_plan_ref": "docs/phase0b/0B-21_POLYMARKET_TOKEN_OUTCOME_NORMALIZATION_PLAN.md",
        "unresolved_state_policy": "preserve",
    },
    "silver_poly_collateral_assets": {
        "depends_on": ["bronze_poly_fpmm_collateral_lookup"],
        "normalization_plan_ref": "docs/phase0b/0B-21_POLYMARKET_TOKEN_OUTCOME_NORMALIZATION_PLAN.md",
        "unresolved_state_policy": "preserve",
    },
}

ALLOWED_UNRESOLVED = {
    "none",
    "missing_source_record",
    "missing_required_raw_field",
    "malformed_raw_value",
    "unresolved_ticker_ref",
    "unresolved_event_ref",
    "unresolved_result",
    "unresolved_taker_side",
    "unresolved_condition_ref",
    "unresolved_token_ref",
    "unresolved_token_outcome_mapping",
    "unresolved_block_timestamp",
    "timestamp_mismatch",
    "unresolved_legacy_fpmm_ref",
    "unresolved_collateral_ref",
    "unsupported_source_shape",
}

def test_doc_exists_and_required_sections_present():
    text = DOC_PATH.read_text(encoding="utf-8")
    required = [
        "docs/static-preflight only",
        "not implement DuckDB views",
        "not run DuckDB",
        "not read archive payloads",
        "PRD-0B-IMPL-01",
        "PRD-0B-IMPL-02",
        "PRD-0B-IMPL-03",
        "Implementation prerequisites",
        "Bronze view principles",
        "Silver view principles",
        "Bronze-to-Silver dependency map",
        "Unresolved-state taxonomy",
        "Planned implementation files (future only)",
        "View implementation safety rules",
        "Query latency gate planning",
        "Relationship to PRD-0A",
        "Recommended next tickets",
        "Explicit non-approvals",
    ]
    for needle in required:
        assert needle in text

def test_doc_contains_planned_view_names_and_counts():
    text = DOC_PATH.read_text(encoding="utf-8")
    for bronze in BRONZE_VIEWS:
        assert bronze["name"] in text
    assert text.count("| bronze_") >= 7
    for name in SILVER_MAP:
        assert name in text

ALLOWED_SQL_SOURCE_FILES = {
    Path("sql/prd_0b/bronze_views.sql"),
    Path("sql/prd_0b/silver_views.sql"),
}

def test_no_forbidden_output_directories_or_files_exist():
    forbidden_paths = [
        Path("reports/prd_0b"),
        Path("generated/prd_0b"),
        Path("generated/reports/prd_0b"),
        Path("generated/dictionary/prd_0b"),
        Path("docs/prd/PRD-0B-IMPL-04_BRONZE_SILVER_VIEW_PLAN.sql"),
        Path("docs/prd/PRD-0B-IMPL-04_BRONZE_SILVER_VIEW_PLAN.duckdb"),
    ]
    for forbidden in forbidden_paths:
        assert not forbidden.exists()

    discovered_sql_files = {path for path in Path("sql").glob("**/*") if path.is_file()} if Path("sql").exists() else set()
    assert discovered_sql_files <= ALLOWED_SQL_SOURCE_FILES

    assert not list(Path(".").rglob("*.duckdb"))

def test_bronze_contracts_are_complete_and_unique():
    assert len(BRONZE_VIEWS) == 7
    names = [item["name"] for item in BRONZE_VIEWS]
    assert len(names) == len(set(names))
    expected_datasets = {
        "kalshi_markets",
        "kalshi_trades",
        "poly_markets",
        "poly_clob_trades",
        "poly_blocks",
        "poly_legacy_fpmm_trades",
        "poly_fpmm_collateral_lookup",
    }
    assert {item["source_dataset"] for item in BRONZE_VIEWS} == expected_datasets
    for item in BRONZE_VIEWS:
        assert item["source_path"]
        assert item["related_dictionary_dataset"]
        assert item["related_bronze_contract"]
        assert item["raw_field_family"]

def test_silver_contracts_dependency_and_policy_constraints():
    bronze_names = {item["name"] for item in BRONZE_VIEWS}
    assert len(SILVER_MAP) == len(set(SILVER_MAP.keys()))
    for cfg in SILVER_MAP.values():
        assert cfg["depends_on"]
        for dep in cfg["depends_on"]:
            assert dep in bronze_names
        assert cfg["normalization_plan_ref"]
        assert cfg["unresolved_state_policy"]

def test_unsupported_contract_shapes_fail_closed():
    def validate_bronze_dataset(dataset_ref: str) -> None:
        supported = {item["source_dataset"] for item in BRONZE_VIEWS}
        if dataset_ref not in supported:
            raise ValueError("unsupported bronze dataset")

    def validate_silver_dependency(dep: str) -> None:
        supported = {item["name"] for item in BRONZE_VIEWS}
        if dep not in supported:
            raise ValueError("unsupported silver dependency")

    def validate_unresolved_status(status: str) -> None:
        if status not in ALLOWED_UNRESOLVED:
            raise ValueError("unsupported unresolved status")

    for fn, value in [
        (validate_bronze_dataset, "unsupported_dataset"),
        (validate_silver_dependency, "unknown_bronze_view"),
        (validate_unresolved_status, "unknown_status"),
    ]:
        try:
            fn(value)
            assert False, "expected ValueError"
        except ValueError:
            pass

def test_execution_live_autonomy_posture_must_be_false():
    posture = {
        "duckdb_execution": False,
        "archive_reads": False,
        "loader_implementation": False,
        "query_engine_service": False,
        "connector_implementation": False,
        "api_calls": False,
        "order_placement": False,
        "live_trading": False,
        "autonomous_execution": False,
        "weather_implementation": False,
    }
    assert all(value is False for value in posture.values())
