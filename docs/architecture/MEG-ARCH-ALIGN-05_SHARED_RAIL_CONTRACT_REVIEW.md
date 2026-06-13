# MEG-ARCH-ALIGN-05 Shared-Rail Contract Review Artifact

Canonical ID: MEG-ARCH-ALIGN-05

## Status and scope

This is a review artifact only. This is docs/static-test-only. It records a static-evidence shared-rail contract review using prior architecture-alignment artifacts and the canonical-ID static allowlist as inputs.

No runtime refactor is implemented. No database migration is implemented. No source-code migration is implemented. No provider connector is implemented. No source fetching is implemented. No scoring/backtesting is implemented. No runtime behavior is implemented. No execution/trading/autonomy is implemented. No production behavior is implemented. No compatibility shim is implemented. No schema change is implemented.

This artifact does not approve migration work. This artifact does not approve compatibility shims. This artifact does not approve DB/schema changes. This artifact does not approve provider connectors. This artifact does not approve source fetching. This artifact does not approve Weather Bot provider/source/scoring/runtime/trading expansion.

`condition_id`, `token_id`, and `outcome` remain the target shared-rail identifier contract. `market_id` remains legacy/compatibility unless a later explicit boundary approves otherwise.

## Relationship to MEG-ARCH-ALIGN-01

`MEG-ARCH-ALIGN-01` established the dual-architecture transition: legacy whale-runtime surfaces remain present while shared-rail planning moves toward canonical identifiers. This artifact preserves that dual-architecture posture by reviewing shared-rail surfaces only at the documentation/static-evidence level and by refusing to treat review labels as migration approval.

## Relationship to MEG-ARCH-ALIGN-02

`MEG-ARCH-ALIGN-02` planned the repository-level inventory/classification method for the legacy identifier footprint. This artifact consumes that method as review discipline: closed-set labels, source-backed evidence, reviewer-inferred notes when needed, and separate approval requirements before any later implementation.

## Relationship to MEG-ARCH-ALIGN-03

`MEG-ARCH-ALIGN-03` created the static inventory artifact and identified target-migration candidates, compatibility-boundary candidates, frozen docs, and test-harness guards. This artifact reviews those categories as planning inputs only. Target-migration candidates require separate human review before implementation, and compatibility-boundary candidates require separate human review before implementation.

## Relationship to MEG-ARCH-ALIGN-04

`MEG-ARCH-ALIGN-04` planned this shared-rail contract review and defined the closed-set review vocabulary. This artifact creates the actual review table planned there, but it still does not implement a runtime refactor, database migration, source-code migration, compatibility shim, provider connector, source-fetching path, scoring/backtesting path, runtime behavior, execution/trading/autonomy path, production behavior, or schema change.

## Review method

This review uses only static repository/documentation evidence from:

- `MEG-ARCH-ALIGN-01`
- `MEG-ARCH-ALIGN-02`
- `MEG-ARCH-ALIGN-03`
- `MEG-ARCH-ALIGN-04`
- `tests/core/canonical_id_allowlist.py`
- `docs/architecture/MEG-ARCH-ALIGN-03_MARKET_ID_INVENTORY.md`

The review did not inspect runtime behavior, call providers, fetch sources, run backtests, query databases, generate data, or modify source code. Labels in the table are documentation/static-evidence review labels only. Future implementation/refactor/migration work requires separate explicit approval.

## Shared-rail contract review table

| surface_name | owning_path_or_module | current_identifier_contract | target_identifier_contract | boundary_type | migration_pressure | compatibility_pressure | required_later_ticket | reviewer_notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| core event contract | `meg/core/events.py` | legacy/compatibility `market_id` footprint appears in a shared event-contract surface | `condition_id`, `token_id`, and `outcome` | shared_rail_surface | high | migrate_later | shared_rail_contract_implementation_planning | High-priority event-contract surface from the inventory; review label only and not a source-code migration approval. |
| operational logger | `meg/core/logger.py` | legacy/compatibility `market_id` footprint appears near operational logging | `condition_id`, `token_id`, and `outcome` | shared_rail_surface | medium | migrate_later | shared_rail_contract_implementation_planning | Logging/journaling adjacency makes this a shared-rail review surface, but implementation requires a later ticket. |
| dashboard API surface | `meg/dashboard/api/main.py` | legacy/compatibility `market_id` footprint appears in dashboard API surface | `condition_id`, `token_id`, and `outcome` | shared_rail_surface | high | migrate_later | shared_rail_contract_implementation_planning | API-facing identifier posture needs later source-code planning; no API behavior changes are approved here. |
| dashboard UI surface | `meg/dashboard/ui/src/App.jsx` | legacy/compatibility `market_id` footprint appears in dashboard UI display/control surface | `condition_id`, `token_id`, and `outcome` | shared_rail_surface | medium | migrate_later | source_code_migration_planning | UI migration pressure is visible from static inventory only; no UI behavior changes are approved. |
| CLOB client/data layer | `meg/data_layer/clob_client.py` | legacy/compatibility `market_id` footprint appears in data-layer surface | `condition_id`, `token_id`, and `outcome` | shared_rail_surface | high | migrate_later | shared_rail_contract_implementation_planning | Data-layer shared-rail adjacency is high priority; provider connector/source-fetching work remains unapproved. |
| Polygon feed/data layer | `meg/data_layer/polygon_feed.py` | legacy/compatibility `market_id` footprint appears in data-layer feed surface | `condition_id`, `token_id`, and `outcome` | shared_rail_surface | high | migrate_later | shared_rail_contract_implementation_planning | Feed/data-layer identifier contract needs later planning; no source fetching or provider work is approved. |
| wallet registry | `meg/data_layer/wallet_registry.py` | legacy/compatibility `market_id` footprint appears in wallet/data registry surface | `condition_id`, `token_id`, and `outcome` | shared_rail_surface | medium | migrate_later | source_code_migration_planning | Registry use requires separate human review before any source-code migration. |
| database model surface | `meg/db/models.py` | legacy/compatibility `market_id` footprint appears in persistence model surface | `condition_id`, `token_id`, and `outcome` | shared_rail_surface | blocker | keep_temporarily | database_migration_planning | Persistence model surface has blocker-level migration pressure because schema work requires separate DB planning and approval. |
| initial database migration | `meg/db/migrations/versions/42acac652ac5_initial_schema_six_tables.py` | frozen legacy/compatibility `market_id` footprint appears in historical migration | `condition_id`, `token_id`, and `outcome` for future shared-rail boundaries | compatibility_boundary | low | keep_temporarily | database_migration_planning | Historical migration should not be rewritten by this artifact; any DB/schema change requires later approval. |
| wallet market trade index migration | `meg/db/migrations/versions/c8f2e4b1a9d3_add_wallet_market_trade_index.py` | frozen legacy/compatibility `market_id` footprint appears in historical index migration | `condition_id`, `token_id`, and `outcome` for future shared-rail boundaries | compatibility_boundary | low | keep_temporarily | database_migration_planning | Historical migration/index posture is compatibility evidence only; no migration is approved. |
| execution entry filter | `meg/execution/entry_filter.py` | legacy/compatibility `market_id` footprint appears in execution-adjacent filter surface | `condition_id`, `token_id`, and `outcome` | legacy_runtime_surface | high | migrate_later | human_review_required | Execution-adjacent surface needs explicit human review; this artifact does not approve execution behavior. |
| execution order router | `meg/execution/order_router.py` | legacy/compatibility `market_id` footprint appears in execution routing surface | `condition_id`, `token_id`, and `outcome` | legacy_runtime_surface | blocker | keep_temporarily | human_review_required | Order-routing adjacency is safety-critical; no execution/trading/autonomy work is approved here. |
| execution slippage guard | `meg/execution/slippage_guard.py` | legacy/compatibility `market_id` footprint appears in execution guard surface | `condition_id`, `token_id`, and `outcome` | legacy_runtime_surface | high | migrate_later | human_review_required | Guard posture requires later human review and explicit implementation approval. |
| risk controller | `meg/agent_core/risk_controller.py` | legacy/compatibility `market_id` footprint appears in risk-gate surface | `condition_id`, `token_id`, and `outcome` | legacy_runtime_surface | high | migrate_later | human_review_required | Risk-gate adjacency requires conservative later review; no risk behavior changes are approved. |
| Telegram approval surface | `meg/telegram/bot.py` | legacy/compatibility `market_id` footprint appears in operator-approval surface | `condition_id`, `token_id`, and `outcome` | shared_rail_surface | high | migrate_later | shared_rail_contract_implementation_planning | Operator approval remains mandatory; no autonomous execution authority is introduced. |
| architecture alignment inventory artifact | `docs/architecture/MEG-ARCH-ALIGN-03_MARKET_ID_INVENTORY.md` | reviewed legacy/compatibility inventory terms | `condition_id`, `token_id`, and `outcome` as documented target | documentation_surface | none | keep_temporarily | no_ticket_required | Documentation evidence source for this review; not migration work. |
| canonical ID allowlist | `tests/core/canonical_id_allowlist.py` | explicit static legacy/compatibility line-count guard | `condition_id`, `token_id`, and `outcome` as enforced target posture | test_harness_surface | low | shrink_later | documentation_refresh_planning | Test-harness surface guards the legacy footprint and may shrink only after later approved changes. |
| unresolved shared-rail surfaces | inventory paths not reviewed in this table | unknown static identifier posture | `condition_id`, `token_id`, and `outcome` | unknown_surface | unknown | unknown | human_review_required | Placeholder for paths outside the required high-priority rows; no implementation approval is implied. |

## Migration-candidate review summary

The target-migration candidates from `MEG-ARCH-ALIGN-03` are planning inputs only. The highest-pressure candidates are shared-rail-facing event, data-layer, dashboard/API, persistence, risk, execution-adjacent, and Telegram approval surfaces where legacy/compatibility `market_id` appears in static inventory evidence.

This review does not approve migration. It does not approve source-code edits, DB/schema changes, provider connectors, source fetching, scoring/backtesting, runtime behavior, execution/trading/autonomy, production behavior, generated data, fixture changes, workflows, dependencies, or compatibility shims. Each target-migration candidate requires a separate later ticket and separate human review before implementation.

## Compatibility-boundary review summary

The compatibility-boundary candidates from `MEG-ARCH-ALIGN-03` are planning inputs only. Frozen historical docs, architecture-alignment planning docs, the inventory artifact, and historical database migrations may preserve compatibility evidence until later explicit review decides whether a boundary remains, shrinks, or needs a separately approved planning track.

This review does not approve compatibility shims. It also does not approve migration work, DB/schema changes, provider connectors, source fetching, Weather Bot provider/source/scoring/runtime/trading expansion, execution/trading/autonomy, or production behavior. Compatibility-boundary candidates require separate human review before implementation.

## High-priority shared-rail surfaces

High-priority shared-rail surfaces identified by this review are:

- Event contract and operational logging surfaces.
- Data-layer CLOB, Polygon/feed, and wallet-registry surfaces.
- Dashboard API/UI surfaces.
- Persistence model and historical migration adjacency surfaces.
- Risk, execution-adjacent, and Telegram approval surfaces.

These are high priority for later review because they are close to shared rails, operational journaling, persistence, approval gates, risk gates, data intake, or execution-adjacent pathways. This priority label does not approve implementation.

## Documentation and test-harness surfaces

Documentation and test-harness surfaces preserve the static-evidence trail for the dual-architecture transition. The canonical-ID allowlist remains a guardrail for explicit line-count review. Architecture-alignment documents remain planning/review artifacts and should not be treated as source-of-truth permission to migrate runtime code.

## Unknowns requiring review

Unknowns remain for any inventory paths not reviewed in the required surface rows and for any ambiguous ownership boundary where static evidence cannot prove whether a surface is shared rail, legacy runtime, compatibility boundary, documentation, or test harness.

Unknowns must be marked `unknown_surface`, `unknown`, or `human_review_required` rather than converted into implementation approval. Future review may split unknowns into source-code migration planning, database migration planning, compatibility-shim planning, shared-rail contract implementation planning, documentation-refresh planning, or no-ticket-required categories.

## Explicit non-implementation boundaries

- Review artifact only.
- Docs/static-test-only.
- No runtime refactor is implemented.
- No database migration is implemented.
- No source-code migration is implemented.
- No provider connector is implemented.
- No source fetching is implemented.
- No scoring/backtesting is implemented.
- No runtime behavior is implemented.
- No execution/trading/autonomy is implemented.
- No production behavior is implemented.
- No compatibility shim is implemented.
- No schema change is implemented.
- This artifact does not approve migration work.
- This artifact does not approve compatibility shims.
- This artifact does not approve DB/schema changes.
- This artifact does not approve provider connectors.
- This artifact does not approve source fetching.
- This artifact does not approve Weather Bot provider/source/scoring/runtime/trading expansion.
- Future implementation/refactor/migration work requires separate explicit approval.

## Recommended next actions

1. Create a migration-candidate review artifact that remains docs/static-test-only and does not approve implementation.
2. Create a compatibility-boundary review artifact that remains docs/static-test-only and does not approve compatibility shims.
3. Keep Weather Bot at the hold/checkpoint posture after offline ingestion closeout; provider connectors, source fetching, scoring/runtime/trading expansion remain unapproved.
4. Require separate explicit human approval before any runtime refactor, source-code migration, DB/schema change, provider connector, source fetching, scoring/backtesting, execution/trading/autonomy, production behavior, or compatibility shim.

## Machine-checkable shared-rail contract review artifact assignments

- architecture alignment stage: shared_rail_contract_review_artifact
- review artifact status: review_artifact_created
- review artifact status: shared_rail_table_created
- review artifact status: migration_not_approved
- review artifact status: compatibility_shim_not_approved
- review artifact status: later_implementation_ticket_required
- review coverage status: target_migration_candidates_reviewed_as_planning_inputs
- review coverage status: compatibility_boundaries_reviewed_as_planning_inputs
- review coverage status: high_priority_shared_rail_surfaces_identified
- review coverage status: unknowns_explicitly_marked
- canonical id posture: condition_id_token_id_outcome_target_contract
- canonical id posture: canonical_ids_required_at_true_shared_rail_boundaries
- canonical id posture: canonical_id_enforcement_not_complete
- market id posture: legacy_compatibility_identifier
- market id posture: allowed_only_at_approved_compatibility_boundaries
- market id posture: not_target_shared_rail_identifier
- market id posture: migration_requires_later_approval
- boundary type: shared_rail_surface
- boundary type: legacy_runtime_surface
- boundary type: compatibility_boundary
- boundary type: documentation_surface
- boundary type: test_harness_surface
- boundary type: unknown_surface
- migration pressure: none
- migration pressure: low
- migration pressure: medium
- migration pressure: high
- migration pressure: blocker
- migration pressure: unknown
- compatibility pressure: none
- compatibility pressure: keep_temporarily
- compatibility pressure: shrink_later
- compatibility pressure: shim_later
- compatibility pressure: migrate_later
- compatibility pressure: unknown
- required later ticket: no_ticket_required
- required later ticket: source_code_migration_planning
- required later ticket: database_migration_planning
- required later ticket: compatibility_shim_planning
- required later ticket: shared_rail_contract_implementation_planning
- required later ticket: documentation_refresh_planning
- required later ticket: human_review_required
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

- The review artifact exists and includes canonical ID `MEG-ARCH-ALIGN-05`.
- All required sections are present.
- The shared-rail contract review table exists with the required exact columns and required surface rows.
- The target identifier contract remains `condition_id`, `token_id`, and `outcome`.
- `market_id` remains legacy/compatibility unless a later explicit boundary approves otherwise.
- Migration-candidate and compatibility-boundary summaries are planning inputs only.
- Weather Bot remains at the hold/checkpoint posture; provider/source/scoring/runtime/trading expansion is not approved.
- Machine-checkable assignments use only allowed closed-set values.
- Static tests validate the artifact without inspecting runtime behavior or changing source code.
