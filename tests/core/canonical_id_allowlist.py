"""Static allowlist for legacy ``market_id`` references.

Ticket 0A-01C intentionally does not migrate runtime behavior. This allowlist
freezes the known legacy footprint so new ``market_id`` usage cannot land
silently in Phase 0A shared-rail work. Future migration tickets should shrink
these counts as they replace legacy routing with ``condition_id``, ``token_id``,
and ``outcome``.
"""
from __future__ import annotations

# Files that implement the static/Redis contract tests are excluded by the test
# harness; all remaining legacy occurrences must be listed here explicitly.
# Counts are line counts containing the literal substring ``market_id``.
ALLOWED_MARKET_ID_OCCURRENCE_LINES: dict[str, int] = {
    # Agent instructions and frozen/historical planning docs.
    "AGENTS.md": 1,
    "CHANGELOG.md": 7,
    "MEG_MASTER_PRD.md": 4,
    "MEG_MASTER_PRD_v4.1_patched.md": 4,
    "MEG_PRD_v3_final.md": 21,
    "STATUS.md": 1,
    "TODOS.md": 5,
    "docs/DATA_MODEL.md": 6,
    "docs/PHASE_0A_SHARED_RAIL.md": 7,
    "docs/phase0a/0A-01_CANONICAL_ID_INVENTORY.md": 59,
    # Phase 0B historical-lake doc: legacy identifier noted for compatibility mapping only.
    "docs/phase0b/0B-01_DUCKDB_HISTORICAL_LAKE_PLAN.md": 1,
    # Known legacy runtime modules inventoried in Ticket 0A-01A.
    "meg/agent_core/crowding_detector.py": 2,
    "meg/agent_core/decision_agent.py": 11,
    "meg/agent_core/position_manager.py": 17,
    "meg/agent_core/risk_controller.py": 4,
    "meg/agent_core/saturation_monitor.py": 3,
    "meg/agent_core/signal_aggregator.py": 1,
    "meg/agent_core/trap_detector.py": 11,
    "meg/core/events.py": 36,
    "meg/core/logger.py": 2,
    "meg/dashboard/api/main.py": 19,
    "meg/dashboard/ui/src/App.jsx": 25,
    "meg/data_layer/clob_client.py": 23,
    "meg/data_layer/polygon_feed.py": 11,
    "meg/data_layer/wallet_registry.py": 7,
    "meg/db/migrations/versions/42acac652ac5_initial_schema_six_tables.py": 7,
    "meg/db/migrations/versions/c8f2e4b1a9d3_add_wallet_market_trade_index.py": 3,
    "meg/db/models.py": 10,
    "meg/execution/entry_filter.py": 7,
    "meg/execution/order_router.py": 3,
    "meg/execution/slippage_guard.py": 11,
    "meg/pre_filter/arbitrage_exclusion.py": 8,
    "meg/pre_filter/intent_classifier.py": 7,
    "meg/pre_filter/market_quality.py": 24,
    "meg/pre_filter/pipeline.py": 10,
    "meg/signal_engine/composite_scorer.py": 2,
    "meg/signal_engine/consensus_filter.py": 3,
    "meg/signal_engine/contrarian_detector.py": 3,
    "meg/signal_engine/ladder_detector.py": 2,
    "meg/telegram/bot.py": 5,
    # Legacy tests and fixtures that still exercise the pre-migration contract.
    "tests/agent_core/conftest.py": 12,
    "tests/agent_core/test_decision_agent.py": 8,
    "tests/agent_core/test_position_manager.py": 13,
    "tests/agent_core/test_risk_controller.py": 1,
    "tests/agent_core/test_trap_detector.py": 27,
    "tests/core/test_canonical_id_contract.py": 19,
    "tests/dashboard/test_api.py": 9,
    "tests/data_layer/test_clob_client.py": 20,
    "tests/data_layer/test_polygon_feed.py": 6,
    "tests/data_layer/test_wallet_registry.py": 4,
    "tests/db/test_models.py": 7,
    "tests/execution/conftest.py": 8,
    "tests/execution/test_order_router.py": 3,
    "tests/pre_filter/conftest.py": 12,
    "tests/pre_filter/test_arbitrage_exclusion.py": 16,
    "tests/pre_filter/test_intent_classifier.py": 20,
    "tests/pre_filter/test_market_quality.py": 20,
    "tests/pre_filter/test_pipeline.py": 1,
    "tests/signal_engine/conftest.py": 4,
    "tests/signal_engine/test_consensus_filter.py": 2,
    "tests/signal_engine/test_contrarian_detector.py": 14,
    "tests/signal_engine/test_ladder_detector.py": 12,
    "tests/signal_engine/test_signal_decay.py": 1,
    "tests/telegram/conftest.py": 2,
    "tests/telegram/test_bot.py": 2,
}
