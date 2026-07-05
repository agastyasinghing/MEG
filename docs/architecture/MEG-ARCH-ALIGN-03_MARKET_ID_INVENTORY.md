# MEG-ARCH-ALIGN-03 market_id Inventory and Classification Artifact

Canonical ID: MEG-ARCH-ALIGN-03

## Status and scope

This is an inventory/classification artifact only. This is not a migration. No runtime refactor is implemented. No source-code migration is implemented. No database schema change is implemented. No database migration is implemented. No source fetching is implemented. No provider/API connector is implemented. No scoring/backtesting is implemented. No execution/trading/autonomy is implemented. No production behavior is implemented.

`condition_id`, `token_id`, and `outcome` remain the target shared-rail identifier contract. `market_id` remains legacy/compatibility unless explicitly classified. This inventory does not approve later implementation work. Future migration/refactor/compatibility-shim work requires separate explicit approval. Weather Bot remains hold/checkpoint for provider/source/scoring/runtime/trading work.

## Relationship to MEG-ARCH-ALIGN-01

`MEG-ARCH-ALIGN-01` established the architecture-alignment planning posture: MEG is in a dual-architecture transition, the older whale-runtime footprint remains visible, and the shared-rail target contract is `condition_id`, `token_id`, and `outcome`. This artifact follows that posture by classifying literal `market_id` usage without changing runtime behavior.

## Relationship to MEG-ARCH-ALIGN-02

`MEG-ARCH-ALIGN-02` planned this repository-level inventory and defined the closed classification categories, recommended next actions, risk levels, and machine-checkable assignment vocabulary. This artifact creates the actual static inventory described by `MEG-ARCH-ALIGN-02`; it does not perform any of the future migration, refactor, compatibility-shim, provider, source, scoring, execution, trading, autonomy, or production work that would require separate approval.

## Inventory method

The inventory uses static repository text evidence only. The source footprint is the current `tests/core/canonical_id_allowlist.py` mapping of paths to line counts containing the literal `market_id`. Each row below preserves the allowlist path and count, then assigns a closed-set current and proposed category based on path role, allowlist comments, and architecture-alignment context. The method does not fetch sources, call providers, generate data, change fixtures, or inspect runtime behavior.

## Classification categories

Allowed `current_category` and `proposed_category` values are exactly:

- legacy_whale_runtime
- approved_compatibility_boundary
- target_migration_candidate
- frozen_historical_doc
- test_harness_guard
- unknown_requires_review

Allowed `recommended_next_action` values are exactly:

- keep_as_legacy_boundary
- wrap_with_compatibility_shim_later
- migrate_to_canonical_ids_later
- leave_frozen_doc
- keep_test_guard
- needs_human_review

Allowed `risk_level` values are exactly:

- low
- medium
- high
- blocker
- unknown

## Inventory table

| path | line_count | current_category | proposed_category | rationale | recommended_next_action | risk_level | reviewer_notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| AGENTS.md | 1 | approved_compatibility_boundary | approved_compatibility_boundary | Active instruction/planning guard documents the legacy compatibility posture without migration claims. | keep_as_legacy_boundary | low | Static text evidence only; no migration status is claimed. |
| CHANGELOG.md | 7 | frozen_historical_doc | frozen_historical_doc | Historical or frozen documentation records legacy wording and should not be rewritten by this inventory. | leave_frozen_doc | low | Static text evidence only; no migration status is claimed. |
| MEG_MASTER_PRD.md | 4 | frozen_historical_doc | frozen_historical_doc | Historical or frozen documentation records legacy wording and should not be rewritten by this inventory. | leave_frozen_doc | low | Static text evidence only; no migration status is claimed. |
| MEG_MASTER_PRD_v4.1_patched.md | 4 | frozen_historical_doc | frozen_historical_doc | Historical or frozen documentation records legacy wording and should not be rewritten by this inventory. | leave_frozen_doc | low | Static text evidence only; no migration status is claimed. |
| MEG_PRD_v3_final.md | 21 | frozen_historical_doc | frozen_historical_doc | Historical or frozen documentation records legacy wording and should not be rewritten by this inventory. | leave_frozen_doc | low | Static text evidence only; no migration status is claimed. |
| STATUS.md | 1 | frozen_historical_doc | frozen_historical_doc | Historical or frozen documentation records legacy wording and should not be rewritten by this inventory. | leave_frozen_doc | low | Static text evidence only; no migration status is claimed. |
| TODOS.md | 5 | frozen_historical_doc | frozen_historical_doc | Historical or frozen documentation records legacy wording and should not be rewritten by this inventory. | leave_frozen_doc | low | Static text evidence only; no migration status is claimed. |
| docs/DATA_MODEL.md | 6 | frozen_historical_doc | frozen_historical_doc | Historical or frozen documentation records legacy wording and should not be rewritten by this inventory. | leave_frozen_doc | low | Static text evidence only; no migration status is claimed. |
| docs/PHASE_0A_SHARED_RAIL.md | 7 | frozen_historical_doc | frozen_historical_doc | Historical or frozen documentation records legacy wording and should not be rewritten by this inventory. | leave_frozen_doc | low | Static text evidence only; no migration status is claimed. |
| docs/phase0a/0A-01_CANONICAL_ID_INVENTORY.md | 59 | frozen_historical_doc | frozen_historical_doc | Historical or frozen documentation records legacy wording and should not be rewritten by this inventory. | leave_frozen_doc | low | Static text evidence only; no migration status is claimed. |
| docs/phase0b/0B-01_DUCKDB_HISTORICAL_LAKE_PLAN.md | 1 | frozen_historical_doc | frozen_historical_doc | Historical or frozen documentation records legacy wording and should not be rewritten by this inventory. | leave_frozen_doc | low | Static text evidence only; no migration status is claimed. |
| docs/prd/MEG-ARCH-ALIGN-01_ARCHITECTURE_ALIGNMENT_PLANNING.md | 13 | approved_compatibility_boundary | approved_compatibility_boundary | Active instruction/planning guard documents the legacy compatibility posture without migration claims. | keep_as_legacy_boundary | low | Static text evidence only; no migration status is claimed. |
| tests/core/test_meg_arch_align_01.py | 4 | test_harness_guard | test_harness_guard | Static guard test for architecture alignment closed-set and identifier posture. | keep_test_guard | low | Static text evidence only; no migration status is claimed. |
| docs/prd/MEG-ARCH-ALIGN-02_MARKET_ID_INVENTORY_CLASSIFICATION_PLANNING.md | 17 | approved_compatibility_boundary | approved_compatibility_boundary | Active instruction/planning guard documents the legacy compatibility posture without migration claims. | keep_as_legacy_boundary | low | Static text evidence only; no migration status is claimed. |
| tests/core/test_meg_arch_align_02.py | 13 | test_harness_guard | test_harness_guard | Static guard test for architecture alignment closed-set and identifier posture. | keep_test_guard | low | Static text evidence only; no migration status is claimed. |
| docs/architecture/MEG-ARCH-ALIGN-03_MARKET_ID_INVENTORY.md | 11 | approved_compatibility_boundary | approved_compatibility_boundary | Active instruction/planning guard documents the legacy compatibility posture without migration claims. | keep_as_legacy_boundary | low | Static text evidence only; no migration status is claimed. |
| tests/core/test_meg_arch_align_03.py | 8 | test_harness_guard | test_harness_guard | Static guard test for architecture alignment closed-set and identifier posture. | keep_test_guard | low | Static text evidence only; no migration status is claimed. |
| docs/prd/PRD-P1-WX-STAGE2-SKELETON-03_TARGETED_MAPPING_BUILDER_VALIDATION_COVERAGE.md | 1 | frozen_historical_doc | frozen_historical_doc | Historical or frozen documentation records legacy wording and should not be rewritten by this inventory. | leave_frozen_doc | low | Static text evidence only; no migration status is claimed. |
| docs/prd/PRD-P1-WX-STAGE2-FIXTURE-IMPLEMENTATION-CLOSEOUT-01_STATIC_FIXTURE_IMPLEMENTATION_CLOSEOUT_CHECKPOINT.md | 2 | frozen_historical_doc | frozen_historical_doc | Historical or frozen documentation records legacy wording and should not be rewritten by this inventory. | leave_frozen_doc | low | Static text evidence only; no migration status is claimed. |
| tests/core/test_prd_p1_wx_stage2_real_fixture_implementation_01.py | 1 | test_harness_guard | test_harness_guard | Static guard test for architecture alignment closed-set and identifier posture. | keep_test_guard | low | Static text evidence only; no migration status is claimed. |
| docs/prd/PRD-P1-WX-STAGE2-REAL-FIXTURE-IMPLEMENTATION-CLOSEOUT-01_REAL_SOURCE_BACKED_FIXTURE_IMPLEMENTATION_CLOSEOUT_CHECKPOINT.md | 2 | frozen_historical_doc | frozen_historical_doc | Historical or frozen documentation records legacy wording and should not be rewritten by this inventory. | leave_frozen_doc | low | Static text evidence only; no migration status is claimed. |
| meg/agent_core/crowding_detector.py | 2 | legacy_whale_runtime | legacy_whale_runtime | Path is part of the existing whale-runtime or its legacy tests and remains pre-migration footprint. | wrap_with_compatibility_shim_later | medium | Static text evidence only; no migration status is claimed. |
| meg/agent_core/decision_agent.py | 11 | legacy_whale_runtime | legacy_whale_runtime | Path is part of the existing whale-runtime or its legacy tests and remains pre-migration footprint. | wrap_with_compatibility_shim_later | medium | Static text evidence only; no migration status is claimed. |
| meg/agent_core/position_manager.py | 17 | legacy_whale_runtime | legacy_whale_runtime | Path is part of the existing whale-runtime or its legacy tests and remains pre-migration footprint. | wrap_with_compatibility_shim_later | medium | Static text evidence only; no migration status is claimed. |
| meg/agent_core/risk_controller.py | 4 | target_migration_candidate | target_migration_candidate | Path appears to touch shared-rail, event, journal, execution, risk, data, dashboard, or Telegram surfaces that need later canonical-ID review. | migrate_to_canonical_ids_later | high | Static text evidence only; no migration status is claimed. |
| meg/agent_core/saturation_monitor.py | 3 | legacy_whale_runtime | legacy_whale_runtime | Path is part of the existing whale-runtime or its legacy tests and remains pre-migration footprint. | wrap_with_compatibility_shim_later | medium | Static text evidence only; no migration status is claimed. |
| meg/agent_core/signal_aggregator.py | 1 | legacy_whale_runtime | legacy_whale_runtime | Path is part of the existing whale-runtime or its legacy tests and remains pre-migration footprint. | wrap_with_compatibility_shim_later | medium | Static text evidence only; no migration status is claimed. |
| meg/agent_core/trap_detector.py | 11 | legacy_whale_runtime | legacy_whale_runtime | Path is part of the existing whale-runtime or its legacy tests and remains pre-migration footprint. | wrap_with_compatibility_shim_later | medium | Static text evidence only; no migration status is claimed. |
| meg/core/events.py | 36 | target_migration_candidate | target_migration_candidate | Path appears to touch shared-rail, event, journal, execution, risk, data, dashboard, or Telegram surfaces that need later canonical-ID review. | migrate_to_canonical_ids_later | high | Static text evidence only; no migration status is claimed. |
| meg/core/logger.py | 2 | target_migration_candidate | target_migration_candidate | Path appears to touch shared-rail, event, journal, execution, risk, data, dashboard, or Telegram surfaces that need later canonical-ID review. | migrate_to_canonical_ids_later | high | Static text evidence only; no migration status is claimed. |
| meg/dashboard/api/main.py | 19 | target_migration_candidate | target_migration_candidate | Path appears to touch shared-rail, event, journal, execution, risk, data, dashboard, or Telegram surfaces that need later canonical-ID review. | migrate_to_canonical_ids_later | high | Static text evidence only; no migration status is claimed. |
| meg/dashboard/ui/src/App.jsx | 25 | target_migration_candidate | target_migration_candidate | Path appears to touch shared-rail, event, journal, execution, risk, data, dashboard, or Telegram surfaces that need later canonical-ID review. | migrate_to_canonical_ids_later | high | Static text evidence only; no migration status is claimed. |
| meg/data_layer/clob_client.py | 23 | target_migration_candidate | target_migration_candidate | Path appears to touch shared-rail, event, journal, execution, risk, data, dashboard, or Telegram surfaces that need later canonical-ID review. | migrate_to_canonical_ids_later | high | Static text evidence only; no migration status is claimed. |
| meg/data_layer/polygon_feed.py | 11 | target_migration_candidate | target_migration_candidate | Path appears to touch shared-rail, event, journal, execution, risk, data, dashboard, or Telegram surfaces that need later canonical-ID review. | migrate_to_canonical_ids_later | high | Static text evidence only; no migration status is claimed. |
| meg/data_layer/wallet_registry.py | 7 | target_migration_candidate | target_migration_candidate | Path appears to touch shared-rail, event, journal, execution, risk, data, dashboard, or Telegram surfaces that need later canonical-ID review. | migrate_to_canonical_ids_later | high | Static text evidence only; no migration status is claimed. |
| meg/db/migrations/versions/42acac652ac5_initial_schema_six_tables.py | 7 | target_migration_candidate | target_migration_candidate | Path appears to touch shared-rail, event, journal, execution, risk, data, dashboard, or Telegram surfaces that need later canonical-ID review. | migrate_to_canonical_ids_later | high | Static text evidence only; no migration status is claimed. |
| meg/db/migrations/versions/c8f2e4b1a9d3_add_wallet_market_trade_index.py | 3 | target_migration_candidate | target_migration_candidate | Path appears to touch shared-rail, event, journal, execution, risk, data, dashboard, or Telegram surfaces that need later canonical-ID review. | migrate_to_canonical_ids_later | high | Static text evidence only; no migration status is claimed. |
| meg/db/models.py | 10 | target_migration_candidate | target_migration_candidate | Path appears to touch shared-rail, event, journal, execution, risk, data, dashboard, or Telegram surfaces that need later canonical-ID review. | migrate_to_canonical_ids_later | high | Static text evidence only; no migration status is claimed. |
| meg/execution/entry_filter.py | 7 | target_migration_candidate | target_migration_candidate | Path appears to touch shared-rail, event, journal, execution, risk, data, dashboard, or Telegram surfaces that need later canonical-ID review. | migrate_to_canonical_ids_later | high | Static text evidence only; no migration status is claimed. |
| meg/execution/order_router.py | 3 | target_migration_candidate | target_migration_candidate | Path appears to touch shared-rail, event, journal, execution, risk, data, dashboard, or Telegram surfaces that need later canonical-ID review. | migrate_to_canonical_ids_later | high | Static text evidence only; no migration status is claimed. |
| meg/execution/slippage_guard.py | 11 | target_migration_candidate | target_migration_candidate | Path appears to touch shared-rail, event, journal, execution, risk, data, dashboard, or Telegram surfaces that need later canonical-ID review. | migrate_to_canonical_ids_later | high | Static text evidence only; no migration status is claimed. |
| meg/pre_filter/arbitrage_exclusion.py | 8 | legacy_whale_runtime | legacy_whale_runtime | Path is part of the existing whale-runtime or its legacy tests and remains pre-migration footprint. | wrap_with_compatibility_shim_later | medium | Static text evidence only; no migration status is claimed. |
| meg/pre_filter/intent_classifier.py | 7 | legacy_whale_runtime | legacy_whale_runtime | Path is part of the existing whale-runtime or its legacy tests and remains pre-migration footprint. | wrap_with_compatibility_shim_later | medium | Static text evidence only; no migration status is claimed. |
| meg/pre_filter/market_quality.py | 24 | legacy_whale_runtime | legacy_whale_runtime | Path is part of the existing whale-runtime or its legacy tests and remains pre-migration footprint. | wrap_with_compatibility_shim_later | medium | Static text evidence only; no migration status is claimed. |
| meg/pre_filter/pipeline.py | 10 | legacy_whale_runtime | legacy_whale_runtime | Path is part of the existing whale-runtime or its legacy tests and remains pre-migration footprint. | wrap_with_compatibility_shim_later | medium | Static text evidence only; no migration status is claimed. |
| meg/signal_engine/composite_scorer.py | 2 | legacy_whale_runtime | legacy_whale_runtime | Path is part of the existing whale-runtime or its legacy tests and remains pre-migration footprint. | wrap_with_compatibility_shim_later | medium | Static text evidence only; no migration status is claimed. |
| meg/signal_engine/consensus_filter.py | 3 | legacy_whale_runtime | legacy_whale_runtime | Path is part of the existing whale-runtime or its legacy tests and remains pre-migration footprint. | wrap_with_compatibility_shim_later | medium | Static text evidence only; no migration status is claimed. |
| meg/signal_engine/contrarian_detector.py | 3 | legacy_whale_runtime | legacy_whale_runtime | Path is part of the existing whale-runtime or its legacy tests and remains pre-migration footprint. | wrap_with_compatibility_shim_later | medium | Static text evidence only; no migration status is claimed. |
| meg/signal_engine/ladder_detector.py | 2 | legacy_whale_runtime | legacy_whale_runtime | Path is part of the existing whale-runtime or its legacy tests and remains pre-migration footprint. | wrap_with_compatibility_shim_later | medium | Static text evidence only; no migration status is claimed. |
| meg/telegram/bot.py | 5 | target_migration_candidate | target_migration_candidate | Path appears to touch shared-rail, event, journal, execution, risk, data, dashboard, or Telegram surfaces that need later canonical-ID review. | migrate_to_canonical_ids_later | high | Static text evidence only; no migration status is claimed. |
| tests/agent_core/conftest.py | 12 | legacy_whale_runtime | legacy_whale_runtime | Path is part of the existing whale-runtime or its legacy tests and remains pre-migration footprint. | wrap_with_compatibility_shim_later | medium | Static text evidence only; no migration status is claimed. |
| tests/agent_core/test_decision_agent.py | 8 | legacy_whale_runtime | legacy_whale_runtime | Path is part of the existing whale-runtime or its legacy tests and remains pre-migration footprint. | wrap_with_compatibility_shim_later | medium | Static text evidence only; no migration status is claimed. |
| tests/agent_core/test_position_manager.py | 13 | legacy_whale_runtime | legacy_whale_runtime | Path is part of the existing whale-runtime or its legacy tests and remains pre-migration footprint. | wrap_with_compatibility_shim_later | medium | Static text evidence only; no migration status is claimed. |
| tests/agent_core/test_risk_controller.py | 1 | target_migration_candidate | target_migration_candidate | Path appears to touch shared-rail, event, journal, execution, risk, data, dashboard, or Telegram surfaces that need later canonical-ID review. | migrate_to_canonical_ids_later | high | Static text evidence only; no migration status is claimed. |
| tests/agent_core/test_trap_detector.py | 27 | legacy_whale_runtime | legacy_whale_runtime | Path is part of the existing whale-runtime or its legacy tests and remains pre-migration footprint. | wrap_with_compatibility_shim_later | medium | Static text evidence only; no migration status is claimed. |
| tests/core/test_canonical_id_contract.py | 19 | target_migration_candidate | target_migration_candidate | Path appears to touch shared-rail, event, journal, execution, risk, data, dashboard, or Telegram surfaces that need later canonical-ID review. | migrate_to_canonical_ids_later | high | Static text evidence only; no migration status is claimed. |
| docs/meta/MEG_CHAT_HANDOFF.md | 2 | approved_compatibility_boundary | approved_compatibility_boundary | Weather Bot handoff documents the non-routing market identifier boundary. | keep_as_legacy_boundary | low | Static text evidence only; no migration status is claimed. |
| docs/meta/MEG_NEXT_CHAT_BOOTSTRAP_PROMPT.md | 3 | approved_compatibility_boundary | approved_compatibility_boundary | Weather Bot bootstrap documents the non-routing market identifier boundary. | keep_as_legacy_boundary | low | Static text evidence only; no migration status is claimed. |
| tests/dashboard/test_api.py | 9 | target_migration_candidate | target_migration_candidate | Path appears to touch shared-rail, event, journal, execution, risk, data, dashboard, or Telegram surfaces that need later canonical-ID review. | migrate_to_canonical_ids_later | high | Static text evidence only; no migration status is claimed. |
| tests/data_layer/test_clob_client.py | 20 | target_migration_candidate | target_migration_candidate | Path appears to touch shared-rail, event, journal, execution, risk, data, dashboard, or Telegram surfaces that need later canonical-ID review. | migrate_to_canonical_ids_later | high | Static text evidence only; no migration status is claimed. |
| tests/data_layer/test_polygon_feed.py | 6 | target_migration_candidate | target_migration_candidate | Path appears to touch shared-rail, event, journal, execution, risk, data, dashboard, or Telegram surfaces that need later canonical-ID review. | migrate_to_canonical_ids_later | high | Static text evidence only; no migration status is claimed. |
| tests/data_layer/test_wallet_registry.py | 4 | target_migration_candidate | target_migration_candidate | Path appears to touch shared-rail, event, journal, execution, risk, data, dashboard, or Telegram surfaces that need later canonical-ID review. | migrate_to_canonical_ids_later | high | Static text evidence only; no migration status is claimed. |
| tests/db/test_models.py | 7 | target_migration_candidate | target_migration_candidate | Path appears to touch shared-rail, event, journal, execution, risk, data, dashboard, or Telegram surfaces that need later canonical-ID review. | migrate_to_canonical_ids_later | high | Static text evidence only; no migration status is claimed. |
| tests/execution/conftest.py | 8 | target_migration_candidate | target_migration_candidate | Path appears to touch shared-rail, event, journal, execution, risk, data, dashboard, or Telegram surfaces that need later canonical-ID review. | migrate_to_canonical_ids_later | high | Static text evidence only; no migration status is claimed. |
| tests/execution/test_order_router.py | 3 | target_migration_candidate | target_migration_candidate | Path appears to touch shared-rail, event, journal, execution, risk, data, dashboard, or Telegram surfaces that need later canonical-ID review. | migrate_to_canonical_ids_later | high | Static text evidence only; no migration status is claimed. |
| tests/pre_filter/conftest.py | 12 | legacy_whale_runtime | legacy_whale_runtime | Path is part of the existing whale-runtime or its legacy tests and remains pre-migration footprint. | wrap_with_compatibility_shim_later | medium | Static text evidence only; no migration status is claimed. |
| tests/pre_filter/test_arbitrage_exclusion.py | 16 | legacy_whale_runtime | legacy_whale_runtime | Path is part of the existing whale-runtime or its legacy tests and remains pre-migration footprint. | wrap_with_compatibility_shim_later | medium | Static text evidence only; no migration status is claimed. |
| tests/pre_filter/test_intent_classifier.py | 20 | legacy_whale_runtime | legacy_whale_runtime | Path is part of the existing whale-runtime or its legacy tests and remains pre-migration footprint. | wrap_with_compatibility_shim_later | medium | Static text evidence only; no migration status is claimed. |
| tests/pre_filter/test_market_quality.py | 20 | legacy_whale_runtime | legacy_whale_runtime | Path is part of the existing whale-runtime or its legacy tests and remains pre-migration footprint. | wrap_with_compatibility_shim_later | medium | Static text evidence only; no migration status is claimed. |
| tests/pre_filter/test_pipeline.py | 1 | legacy_whale_runtime | legacy_whale_runtime | Path is part of the existing whale-runtime or its legacy tests and remains pre-migration footprint. | wrap_with_compatibility_shim_later | medium | Static text evidence only; no migration status is claimed. |
| tests/signal_engine/conftest.py | 4 | legacy_whale_runtime | legacy_whale_runtime | Path is part of the existing whale-runtime or its legacy tests and remains pre-migration footprint. | wrap_with_compatibility_shim_later | medium | Static text evidence only; no migration status is claimed. |
| tests/signal_engine/test_consensus_filter.py | 2 | legacy_whale_runtime | legacy_whale_runtime | Path is part of the existing whale-runtime or its legacy tests and remains pre-migration footprint. | wrap_with_compatibility_shim_later | medium | Static text evidence only; no migration status is claimed. |
| tests/signal_engine/test_contrarian_detector.py | 14 | legacy_whale_runtime | legacy_whale_runtime | Path is part of the existing whale-runtime or its legacy tests and remains pre-migration footprint. | wrap_with_compatibility_shim_later | medium | Static text evidence only; no migration status is claimed. |
| tests/signal_engine/test_ladder_detector.py | 12 | legacy_whale_runtime | legacy_whale_runtime | Path is part of the existing whale-runtime or its legacy tests and remains pre-migration footprint. | wrap_with_compatibility_shim_later | medium | Static text evidence only; no migration status is claimed. |
| tests/signal_engine/test_signal_decay.py | 1 | legacy_whale_runtime | legacy_whale_runtime | Path is part of the existing whale-runtime or its legacy tests and remains pre-migration footprint. | wrap_with_compatibility_shim_later | medium | Static text evidence only; no migration status is claimed. |
| tests/telegram/conftest.py | 2 | target_migration_candidate | target_migration_candidate | Path appears to touch shared-rail, event, journal, execution, risk, data, dashboard, or Telegram surfaces that need later canonical-ID review. | migrate_to_canonical_ids_later | high | Static text evidence only; no migration status is claimed. |
| tests/telegram/test_bot.py | 2 | target_migration_candidate | target_migration_candidate | Path appears to touch shared-rail, event, journal, execution, risk, data, dashboard, or Telegram surfaces that need later canonical-ID review. | migrate_to_canonical_ids_later | high | Static text evidence only; no migration status is claimed. |

## Summary by category

- legacy_whale_runtime: 28 paths
- approved_compatibility_boundary: 4 paths
- target_migration_candidate: 26 paths
- frozen_historical_doc: 13 paths
- test_harness_guard: 4 paths
- unknown_requires_review: 0 paths

## High-risk target-migration candidates

The following paths are high-risk target-migration candidates because they appear to touch proposal/event/journal/execution/risk/shared-rail-adjacent surfaces. They are candidates only; this artifact does not claim they have been fixed or migrated.

- `meg/agent_core/risk_controller.py` (4 lines): Path appears to touch shared-rail, event, journal, execution, risk, data, dashboard, or Telegram surfaces that need later canonical-ID review.
- `meg/core/events.py` (36 lines): Path appears to touch shared-rail, event, journal, execution, risk, data, dashboard, or Telegram surfaces that need later canonical-ID review.
- `meg/core/logger.py` (2 lines): Path appears to touch shared-rail, event, journal, execution, risk, data, dashboard, or Telegram surfaces that need later canonical-ID review.
- `meg/dashboard/api/main.py` (19 lines): Path appears to touch shared-rail, event, journal, execution, risk, data, dashboard, or Telegram surfaces that need later canonical-ID review.
- `meg/dashboard/ui/src/App.jsx` (25 lines): Path appears to touch shared-rail, event, journal, execution, risk, data, dashboard, or Telegram surfaces that need later canonical-ID review.
- `meg/data_layer/clob_client.py` (23 lines): Path appears to touch shared-rail, event, journal, execution, risk, data, dashboard, or Telegram surfaces that need later canonical-ID review.
- `meg/data_layer/polygon_feed.py` (11 lines): Path appears to touch shared-rail, event, journal, execution, risk, data, dashboard, or Telegram surfaces that need later canonical-ID review.
- `meg/data_layer/wallet_registry.py` (7 lines): Path appears to touch shared-rail, event, journal, execution, risk, data, dashboard, or Telegram surfaces that need later canonical-ID review.
- `meg/db/migrations/versions/42acac652ac5_initial_schema_six_tables.py` (7 lines): Path appears to touch shared-rail, event, journal, execution, risk, data, dashboard, or Telegram surfaces that need later canonical-ID review.
- `meg/db/migrations/versions/c8f2e4b1a9d3_add_wallet_market_trade_index.py` (3 lines): Path appears to touch shared-rail, event, journal, execution, risk, data, dashboard, or Telegram surfaces that need later canonical-ID review.
- `meg/db/models.py` (10 lines): Path appears to touch shared-rail, event, journal, execution, risk, data, dashboard, or Telegram surfaces that need later canonical-ID review.
- `meg/execution/entry_filter.py` (7 lines): Path appears to touch shared-rail, event, journal, execution, risk, data, dashboard, or Telegram surfaces that need later canonical-ID review.
- `meg/execution/order_router.py` (3 lines): Path appears to touch shared-rail, event, journal, execution, risk, data, dashboard, or Telegram surfaces that need later canonical-ID review.
- `meg/execution/slippage_guard.py` (11 lines): Path appears to touch shared-rail, event, journal, execution, risk, data, dashboard, or Telegram surfaces that need later canonical-ID review.
- `meg/telegram/bot.py` (5 lines): Path appears to touch shared-rail, event, journal, execution, risk, data, dashboard, or Telegram surfaces that need later canonical-ID review.
- `tests/agent_core/test_risk_controller.py` (1 lines): Path appears to touch shared-rail, event, journal, execution, risk, data, dashboard, or Telegram surfaces that need later canonical-ID review.
- `tests/core/test_canonical_id_contract.py` (19 lines): Path appears to touch shared-rail, event, journal, execution, risk, data, dashboard, or Telegram surfaces that need later canonical-ID review.
- `tests/dashboard/test_api.py` (9 lines): Path appears to touch shared-rail, event, journal, execution, risk, data, dashboard, or Telegram surfaces that need later canonical-ID review.
- `tests/data_layer/test_clob_client.py` (20 lines): Path appears to touch shared-rail, event, journal, execution, risk, data, dashboard, or Telegram surfaces that need later canonical-ID review.
- `tests/data_layer/test_polygon_feed.py` (6 lines): Path appears to touch shared-rail, event, journal, execution, risk, data, dashboard, or Telegram surfaces that need later canonical-ID review.
- `tests/data_layer/test_wallet_registry.py` (4 lines): Path appears to touch shared-rail, event, journal, execution, risk, data, dashboard, or Telegram surfaces that need later canonical-ID review.
- `tests/db/test_models.py` (7 lines): Path appears to touch shared-rail, event, journal, execution, risk, data, dashboard, or Telegram surfaces that need later canonical-ID review.
- `tests/execution/conftest.py` (8 lines): Path appears to touch shared-rail, event, journal, execution, risk, data, dashboard, or Telegram surfaces that need later canonical-ID review.
- `tests/execution/test_order_router.py` (3 lines): Path appears to touch shared-rail, event, journal, execution, risk, data, dashboard, or Telegram surfaces that need later canonical-ID review.
- `tests/telegram/conftest.py` (2 lines): Path appears to touch shared-rail, event, journal, execution, risk, data, dashboard, or Telegram surfaces that need later canonical-ID review.
- `tests/telegram/test_bot.py` (2 lines): Path appears to touch shared-rail, event, journal, execution, risk, data, dashboard, or Telegram surfaces that need later canonical-ID review.

## Compatibility-boundary candidates

These paths are currently classified as approved compatibility boundaries because they document or guard the legacy compatibility posture rather than route runtime behavior.

- `AGENTS.md`: keep_as_legacy_boundary
- `docs/prd/MEG-ARCH-ALIGN-01_ARCHITECTURE_ALIGNMENT_PLANNING.md`: keep_as_legacy_boundary
- `docs/prd/MEG-ARCH-ALIGN-02_MARKET_ID_INVENTORY_CLASSIFICATION_PLANNING.md`: keep_as_legacy_boundary
- `docs/architecture/MEG-ARCH-ALIGN-03_MARKET_ID_INVENTORY.md`: keep_as_legacy_boundary

## Frozen historical docs and test-harness guards

Frozen historical docs remain unchanged, and test-harness guards continue to enforce the static footprint. They are not migration work.

- `CHANGELOG.md`: frozen_historical_doc
- `MEG_MASTER_PRD.md`: frozen_historical_doc
- `MEG_MASTER_PRD_v4.1_patched.md`: frozen_historical_doc
- `MEG_PRD_v3_final.md`: frozen_historical_doc
- `STATUS.md`: frozen_historical_doc
- `TODOS.md`: frozen_historical_doc
- `docs/DATA_MODEL.md`: frozen_historical_doc
- `docs/PHASE_0A_SHARED_RAIL.md`: frozen_historical_doc
- `docs/phase0a/0A-01_CANONICAL_ID_INVENTORY.md`: frozen_historical_doc
- `docs/phase0b/0B-01_DUCKDB_HISTORICAL_LAKE_PLAN.md`: frozen_historical_doc
- `tests/core/test_meg_arch_align_01.py`: test_harness_guard
- `tests/core/test_meg_arch_align_02.py`: test_harness_guard
- `tests/core/test_meg_arch_align_03.py`: test_harness_guard
- `docs/prd/PRD-P1-WX-STAGE2-SKELETON-03_TARGETED_MAPPING_BUILDER_VALIDATION_COVERAGE.md`: frozen_historical_doc
- `docs/prd/PRD-P1-WX-STAGE2-FIXTURE-IMPLEMENTATION-CLOSEOUT-01_STATIC_FIXTURE_IMPLEMENTATION_CLOSEOUT_CHECKPOINT.md`: frozen_historical_doc
- `tests/core/test_prd_p1_wx_stage2_real_fixture_implementation_01.py`: test_harness_guard
- `docs/prd/PRD-P1-WX-STAGE2-REAL-FIXTURE-IMPLEMENTATION-CLOSEOUT-01_REAL_SOURCE_BACKED_FIXTURE_IMPLEMENTATION_CLOSEOUT_CHECKPOINT.md`: frozen_historical_doc

## Unknowns requiring review

- No unknown paths are currently assigned from the allowlist.

## Explicit non-implementation boundaries

- Inventory/classification only.
- Not a migration.
- No runtime refactor is implemented.
- No source-code migration is implemented.
- No database schema change is implemented.
- No database migration is implemented.
- No source fetching is implemented.
- No provider/API connector is implemented.
- No scoring/backtesting is implemented.
- No execution/trading/autonomy is implemented.
- No production behavior is implemented.
- No Weather Bot provider/source/scoring/runtime/trading work is approved.
- No later migration/refactor/compatibility-shim work is approved by this artifact.

## Recommended next actions

1. Keep this artifact as the static classification baseline for current literal `market_id` usage.
2. Review high-risk target-migration candidates in a separate planning or approval-request ticket before any code changes.
3. Preserve compatibility-boundary and frozen historical doc classifications unless a later approved ticket explicitly changes the source-of-truth posture.
4. Keep test-harness guards in place so new `market_id` usage cannot land silently.
5. Keep Weather Bot at hold/checkpoint for provider/source/scoring/runtime/trading work until separate explicit approvals exist.

## Machine-checkable market_id inventory assignments

- architecture alignment stage: market_id_inventory_artifact
- inventory artifact status: inventory_created
- inventory artifact status: line_counts_match_allowlist
- inventory artifact status: classifications_assigned
- inventory artifact status: human_review_required_before_migration
- inventory coverage status: all_allowlist_paths_included
- inventory coverage status: no_unlisted_market_id_paths_allowed
- inventory coverage status: unknowns_explicitly_marked
- canonical id posture: condition_id_token_id_outcome_target_contract
- canonical id posture: canonical_ids_required_at_true_shared_rail_boundaries
- canonical id posture: canonical_id_enforcement_not_complete
- market id posture: legacy_compatibility_identifier
- market id posture: allowed_only_at_approved_compatibility_boundaries
- market id posture: not_target_shared_rail_identifier
- market id posture: migration_requires_later_approval
- classification category: legacy_whale_runtime
- classification category: approved_compatibility_boundary
- classification category: target_migration_candidate
- classification category: frozen_historical_doc
- classification category: test_harness_guard
- classification category: unknown_requires_review
- recommended next action: keep_as_legacy_boundary
- recommended next action: wrap_with_compatibility_shim_later
- recommended next action: migrate_to_canonical_ids_later
- recommended next action: leave_frozen_doc
- recommended next action: keep_test_guard
- recommended next action: needs_human_review
- risk level: low
- risk level: medium
- risk level: high
- risk level: blocker
- risk level: unknown
- implementation posture: inventory_only
- implementation posture: no_runtime_refactor
- implementation posture: no_database_migration
- implementation posture: no_source_code_migration
- implementation posture: no_source_fetching
- implementation posture: no_provider_connector
- implementation posture: no_scoring_backtesting
- implementation posture: no_execution_trading
- implementation posture: no_production_behavior
- weather bot posture: weather_bot_hold_checkpoint_after_offline_ingestion_closeout
- weather bot posture: weather_bot_provider_connectors_not_approved
- weather bot posture: weather_bot_source_fetching_not_approved
- weather bot posture: weather_bot_scoring_runtime_trading_not_approved
- evidence status: source_backed
- evidence status: reviewer_inferred
- evidence status: missing
- evidence status: conflicting
- evidence status: not_applicable
- label confidence: confirmed
- label confidence: unclear
- label confidence: unknown

## Acceptance criteria

- The artifact exists at `docs/architecture/MEG-ARCH-ALIGN-03_MARKET_ID_INVENTORY.md`.
- The canonical ID `MEG-ARCH-ALIGN-03` appears.
- Every allowlist path with literal `market_id` line-count entries appears in the inventory table.
- Every inventory `line_count` matches `tests/core/canonical_id_allowlist.py`.
- Every category, recommended next action, and risk level uses the closed values listed above.
- The machine-checkable assignment section is section-scoped and contains only approved closed-set values.
- The document states that `condition_id`, `token_id`, and `outcome` remain the target shared-rail identifier contract.
- The document states that `market_id` remains legacy/compatibility unless explicitly classified.
- The document states the non-implementation boundaries and Weather Bot hold/checkpoint posture.
