# MEG-ARCH-ALIGN-06 migration-candidate review artifact

Canonical ID: MEG-ARCH-ALIGN-06

## Status and scope

This is a review artifact only. This is docs/static-test-only. This artifact reviews target-migration candidates from `MEG-ARCH-ALIGN-03` and `MEG-ARCH-ALIGN-05` at the documentation/static-evidence level only.

No runtime refactor is implemented. No database migration is implemented. No source-code migration is implemented. No provider connector is implemented. No source fetching is implemented. No scoring/backtesting is implemented. No runtime behavior is implemented. No execution/trading/autonomy is implemented. No production behavior is implemented. No compatibility shim is implemented. No schema change is implemented.

This artifact does not approve migration work. This artifact does not approve compatibility shims. This artifact does not approve DB/schema changes. This artifact does not approve provider connectors. This artifact does not approve source fetching. This artifact does not approve Weather Bot provider/source/scoring/runtime/trading expansion.

`condition_id`, `token_id`, and `outcome` remain the target shared-rail identifier contract. `market_id` remains legacy/compatibility unless a later explicit boundary approves otherwise. Target-migration candidates require separate human review before implementation. Future implementation/refactor/migration work requires separate explicit approval.

## Relationship to MEG-ARCH-ALIGN-01

`MEG-ARCH-ALIGN-01` established the dual-architecture transition posture: legacy whale-runtime surfaces remain visible while the shared-rail target contract is `condition_id`, `token_id`, and `outcome`. This artifact preserves that posture by reviewing migration-candidate labels only, without approving implementation work or changing runtime behavior.

## Relationship to MEG-ARCH-ALIGN-02

`MEG-ARCH-ALIGN-02` planned the repository-level `market_id` inventory and classification workflow. This artifact consumes that planning lineage only as static documentation context and does not change the inventory method, source modules, runtime modules, database models, migrations, workflows, dependencies, generated data, or fixtures.

## Relationship to MEG-ARCH-ALIGN-03

`MEG-ARCH-ALIGN-03` created the `market_id` inventory artifact and classified the required candidate paths as target-migration candidates using static repository text evidence. This artifact reviews those candidate labels as planning inputs only and does not mark any path as migrated.

## Relationship to MEG-ARCH-ALIGN-04

`MEG-ARCH-ALIGN-04` planned the shared-rail contract review and migration-candidate review sequence. This artifact follows that plan by creating the migration-candidate review artifact, while preserving the requirement that later source-code, database, compatibility-boundary, provider, source-fetching, scoring, runtime, execution, trading, autonomy, and production work need separate explicit approval.

## Relationship to MEG-ARCH-ALIGN-05

`MEG-ARCH-ALIGN-05` created the shared-rail contract review artifact and recommended a later migration-candidate review artifact or compatibility-boundary review artifact. This artifact is the migration-candidate review artifact. It uses the shared-rail contract review rows as static evidence and does not approve compatibility shims, DB/schema changes, runtime refactors, provider connectors, source fetching, scoring/backtesting, execution/trading/autonomy, or production behavior.

## Review method

The review method uses only static repository/documentation evidence from:

- `MEG-ARCH-ALIGN-01`
- `MEG-ARCH-ALIGN-02`
- `MEG-ARCH-ALIGN-03`
- `MEG-ARCH-ALIGN-04`
- `MEG-ARCH-ALIGN-05`
- `tests/core/canonical_id_allowlist.py`
- `docs/architecture/MEG-ARCH-ALIGN-03_MARKET_ID_INVENTORY.md`
- `docs/architecture/MEG-ARCH-ALIGN-05_SHARED_RAIL_CONTRACT_REVIEW.md`

The method does not inspect runtime behavior, call providers, fetch sources, run backtests, query databases, generate data, modify source code, modify runtime code, modify connector code, modify database models, modify migrations, modify workflows, or modify fixtures.

Rows below are review labels only. They are not migration status, shim status, DB/schema status, runtime status, provider status, source-fetching status, scoring/backtesting status, execution/trading/autonomy status, or production status.

## Migration-candidate review table

| path | current_category | proposed_review_category | current_identifier_usage | target_identifier_contract | likely_surface_type | risk_level | recommended_review_action | reviewer_notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `meg/core/events.py` | target_migration_candidate | confirm_target_migration_candidate | Legacy/compatibility `market_id` footprint appears in event-contract evidence from MEG-ARCH-ALIGN-03 and shared-rail evidence from MEG-ARCH-ALIGN-05. | `condition_id`, `token_id`, and `outcome` | event_contract | high | request_human_review | Event contracts are shared-rail surfaces; review label only, with later human review required before any implementation. |
| `meg/core/logger.py` | target_migration_candidate | confirm_target_migration_candidate | Legacy/compatibility `market_id` footprint appears near operational logging/journaling evidence. | `condition_id`, `token_id`, and `outcome` | journal_contract | medium | request_human_review | Logging/journaling adjacency needs a later explicit boundary before any source-code work. |
| `meg/dashboard/api/main.py` | target_migration_candidate | confirm_target_migration_candidate | Legacy/compatibility `market_id` footprint appears in dashboard API evidence. | `condition_id`, `token_id`, and `outcome` | dashboard_api | high | request_human_review | API-facing identifier changes require separate human review and explicit implementation approval. |
| `meg/dashboard/ui/src/App.jsx` | target_migration_candidate | confirm_target_migration_candidate | Legacy/compatibility `market_id` footprint appears in dashboard UI evidence. | `condition_id`, `token_id`, and `outcome` | dashboard_api | medium | request_human_review | UI display/control posture is reviewed only as a planning input; no UI behavior changes are approved. |
| `meg/data_layer/clob_client.py` | target_migration_candidate | confirm_target_migration_candidate | Legacy/compatibility `market_id` footprint appears in data-layer/CLOB evidence. | `condition_id`, `token_id`, and `outcome` | data_layer | high | request_human_review | Data-layer adjacency can touch provider boundaries; provider connectors and source fetching remain unapproved. |
| `meg/data_layer/polygon_feed.py` | target_migration_candidate | confirm_target_migration_candidate | Legacy/compatibility `market_id` footprint appears in feed/data-layer evidence. | `condition_id`, `token_id`, and `outcome` | data_layer | high | request_human_review | Feed/data-layer review is static only; no source fetching or provider work is approved. |
| `meg/data_layer/wallet_registry.py` | target_migration_candidate | confirm_target_migration_candidate | Legacy/compatibility `market_id` footprint appears in wallet registry evidence. | `condition_id`, `token_id`, and `outcome` | data_layer | medium | request_human_review | Registry migration pressure is a planning label only and needs separate implementation approval. |
| `meg/db/models.py` | target_migration_candidate | requires_more_review | Legacy/compatibility `market_id` footprint appears in database model evidence. | `condition_id`, `token_id`, and `outcome` | database_persistence | blocker | request_human_review | Persistence/model surface is blocker-level because DB/schema work requires separate human review and approval. |
| `meg/db/migrations/versions/42acac652ac5_initial_schema_six_tables.py` | target_migration_candidate | reclassify_as_compatibility_boundary | Legacy/compatibility `market_id` footprint appears in historical migration evidence. | `condition_id`, `token_id`, and `outcome` for future shared-rail boundaries | database_persistence | high | request_human_review | Historical migration files should not be rewritten by this artifact; any DB/schema path needs separate human review. |
| `meg/db/migrations/versions/c8f2e4b1a9d3_add_wallet_market_trade_index.py` | target_migration_candidate | reclassify_as_compatibility_boundary | Legacy/compatibility `market_id` footprint appears in historical index migration evidence. | `condition_id`, `token_id`, and `outcome` for future shared-rail boundaries | database_persistence | high | request_human_review | Historical index posture is compatibility evidence only; DB migration approval is not granted here. |
| `meg/execution/entry_filter.py` | target_migration_candidate | requires_more_review | Legacy/compatibility `market_id` footprint appears in execution-adjacent filter evidence. | `condition_id`, `token_id`, and `outcome` | execution_intent | high | request_human_review | Execution-adjacent surface must remain human-review-required; no execution behavior is approved. |
| `meg/execution/order_router.py` | target_migration_candidate | requires_more_review | Legacy/compatibility `market_id` footprint appears in order-routing evidence. | `condition_id`, `token_id`, and `outcome` | execution_intent | blocker | request_human_review | Order-routing adjacency is safety-critical and requires explicit human approval before any later work. |
| `meg/execution/slippage_guard.py` | target_migration_candidate | requires_more_review | Legacy/compatibility `market_id` footprint appears in execution guard evidence. | `condition_id`, `token_id`, and `outcome` | execution_intent | high | request_human_review | Guard logic is execution-adjacent; review label only and not an implementation decision. |
| `meg/agent_core/risk_controller.py` | target_migration_candidate | requires_more_review | Legacy/compatibility `market_id` footprint appears in risk-controller evidence. | `condition_id`, `token_id`, and `outcome` | risk_gate | high | request_human_review | Risk-gate adjacency requires conservative human review; no risk behavior changes are approved. |
| `meg/telegram/bot.py` | target_migration_candidate | confirm_target_migration_candidate | Legacy/compatibility `market_id` footprint appears in Telegram operator-approval evidence. | `condition_id`, `token_id`, and `outcome` | approval_gate | high | request_human_review | Operator approval remains mandatory; no execution/trading/autonomy authority is introduced. |

## Summary by likely surface type

- `event_contract`: `meg/core/events.py` remains a high-risk shared-rail planning input because event contracts are likely to propagate identifiers.
- `journal_contract`: `meg/core/logger.py` remains a medium-risk planning input because logs/journals may preserve legacy identifiers while later boundaries are defined.
- `dashboard_api`: `meg/dashboard/api/main.py` and `meg/dashboard/ui/src/App.jsx` remain planning inputs for API/UI review, not behavior changes.
- `data_layer`: `meg/data_layer/clob_client.py`, `meg/data_layer/polygon_feed.py`, and `meg/data_layer/wallet_registry.py` remain planning inputs; provider connectors and source fetching remain unapproved.
- `database_persistence`: `meg/db/models.py` and historical migration files require separate human review before DB/schema planning or implementation.
- `execution_intent`: `meg/execution/entry_filter.py`, `meg/execution/order_router.py`, and `meg/execution/slippage_guard.py` require human review because they are execution/order/trading-adjacent.
- `risk_gate`: `meg/agent_core/risk_controller.py` requires human review because risk gates are safety-sensitive.
- `approval_gate`: `meg/telegram/bot.py` requires human review while preserving operator approval as mandatory.

## High-risk candidates

High-risk and blocker candidates identified from static evidence are:

- `meg/core/events.py`
- `meg/dashboard/api/main.py`
- `meg/data_layer/clob_client.py`
- `meg/data_layer/polygon_feed.py`
- `meg/db/models.py`
- `meg/db/migrations/versions/42acac652ac5_initial_schema_six_tables.py`
- `meg/db/migrations/versions/c8f2e4b1a9d3_add_wallet_market_trade_index.py`
- `meg/execution/entry_filter.py`
- `meg/execution/order_router.py`
- `meg/execution/slippage_guard.py`
- `meg/agent_core/risk_controller.py`
- `meg/telegram/bot.py`

These are planning labels only. This section does not approve migration work, DB/schema changes, runtime refactors, compatibility shims, provider connectors, source fetching, scoring/backtesting, execution/trading/autonomy, or production behavior.

## Human-review-required candidates

Human review is required before any later implementation/refactor/migration work for every row in the table. Execution/order/risk/trading-adjacent surfaces are especially constrained:

- `meg/execution/entry_filter.py`
- `meg/execution/order_router.py`
- `meg/execution/slippage_guard.py`
- `meg/agent_core/risk_controller.py`
- `meg/telegram/bot.py`

The human-review requirement is a safety boundary, not implementation permission.

## Explicit non-implementation boundaries

This artifact is review artifact only and docs/static-test-only. It creates no runtime refactor, no database migration, no source-code migration, no provider connector, no source fetching, no scoring/backtesting, no runtime behavior, no execution/trading/autonomy, no production behavior, no compatibility shim, and no schema change.

This artifact does not approve migration work, compatibility shims, DB/schema changes, provider connectors, source fetching, Weather Bot provider/source/scoring/runtime/trading expansion, runtime refactors, source-code migrations, database migrations, execution, trading, autonomy, production behavior, generated data, fixture changes, workflows, or dependencies.

## Recommended next actions

- Treat this table as a migration-candidate review artifact and planning input only.
- Preserve `condition_id`, `token_id`, and `outcome` as the target shared-rail identifier contract.
- Preserve `market_id` as legacy/compatibility unless a later explicit boundary approves otherwise.
- Require separate human review before any target-migration candidate proceeds to implementation planning.
- If this artifact is clean, a next docs/static-test-only ticket may create a compatibility-boundary review artifact.
- Do not use this artifact to approve runtime refactors, DB migrations, provider connectors, source fetching, scoring/backtesting, runtime behavior, execution, trading, autonomy, production behavior, compatibility shims, schema changes, generated data, fixture changes, workflows, or dependencies.

## Machine-checkable migration-candidate review artifact assignments

- architecture alignment stage: migration_candidate_review_artifact
- review artifact status: review_artifact_created
- review artifact status: migration_candidate_table_created
- review artifact status: migration_not_approved
- review artifact status: compatibility_shim_not_approved
- review artifact status: later_implementation_ticket_required
- review coverage status: target_migration_candidates_reviewed_as_planning_inputs
- review coverage status: high_risk_candidates_identified
- review coverage status: human_review_required_candidates_identified
- review coverage status: unknowns_explicitly_marked
- canonical id posture: condition_id_token_id_outcome_target_contract
- canonical id posture: canonical_ids_required_at_true_shared_rail_boundaries
- canonical id posture: canonical_id_enforcement_not_complete
- market id posture: legacy_compatibility_identifier
- market id posture: allowed_only_at_approved_compatibility_boundaries
- market id posture: not_target_shared_rail_identifier
- market id posture: migration_requires_later_approval
- proposed review category: confirm_target_migration_candidate
- proposed review category: reclassify_as_legacy_runtime
- proposed review category: reclassify_as_compatibility_boundary
- proposed review category: reclassify_as_test_harness_guard
- proposed review category: reclassify_as_frozen_doc
- proposed review category: requires_more_review
- likely surface type: event_contract
- likely surface type: journal_contract
- likely surface type: approval_gate
- likely surface type: risk_gate
- likely surface type: execution_intent
- likely surface type: dashboard_api
- likely surface type: data_layer
- likely surface type: database_persistence
- likely surface type: runtime_internal
- likely surface type: documentation
- likely surface type: test_harness
- likely surface type: unknown
- recommended review action: plan_source_code_migration
- recommended review action: plan_database_migration
- recommended review action: plan_compatibility_shim
- recommended review action: keep_as_legacy_runtime
- recommended review action: keep_as_test_guard
- recommended review action: leave_frozen_doc
- recommended review action: request_human_review
- risk level: low
- risk level: medium
- risk level: high
- risk level: blocker
- risk level: unknown
- implementation posture: review_artifact_only
- implementation posture: no_runtime_refactor
- implementation posture: no_database_migration
- implementation posture: no_source_code_migration
- implementation posture: no_source_fetching
- implementation posture: no_provider_connector
- implementation posture: no_scoring_backtesting
- implementation posture: no_execution_trading
- implementation posture: no_production_behavior
- implementation posture: no_compatibility_shim
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

- The artifact exists at `docs/architecture/MEG-ARCH-ALIGN-06_MIGRATION_CANDIDATE_REVIEW.md`.
- The canonical ID `MEG-ARCH-ALIGN-06` appears.
- Required relationship sections for `MEG-ARCH-ALIGN-01` through `MEG-ARCH-ALIGN-05` appear.
- The review artifact / docs-static-only scope is explicit.
- The migration-candidate review table exists with exact required columns and required path rows.
- Table values use closed-set values only.
- High-risk and human-review-required candidates are explicitly identified.
- Weather Bot remains in hold/checkpoint posture: provider connectors, source fetching, scoring, runtime, and trading expansion are not approved.
- The machine-checkable assignment section exists and uses exact closed-set values only.
- Static tests validate this artifact without source-code, runtime, database, provider, source-fetching, scoring/backtesting, execution/trading/autonomy, production, workflow, dependency, generated-data, fixture, or docs/meta changes.
