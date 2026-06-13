# MEG-ARCH-ALIGN-01 Architecture Alignment Planning for Canonical Rail vs Legacy Whale Runtime

Canonical ID: `MEG-ARCH-ALIGN-01`

## Status and scope

This document is a planning-only architecture alignment artifact for `MEG-ARCH-ALIGN-01`. It records the boundary between the older whale-reaction runtime and the newer PRD-driven Phase 0A / Weather Bot / canonical-ID architecture before any additional feature expansion.

This planning pass implements no product behavior. No runtime refactor is implemented. No database schema change is implemented. No database migration is implemented. No source-fetching work is implemented. No provider/API connector work is implemented. No scoring or backtesting work is implemented. No execution, trading, order placement, autonomy, live behavior, or production behavior is implemented.

## Why this alignment pass is needed

The repository currently contains two architecture tracks that are valid to keep side-by-side during a staged rebuild, but unsafe to let drift without an explicit contract. The older whale-reaction runtime still uses legacy market identity in several places, while the newer Phase 0A shared rail expects canonical identifiers.

The purpose of this alignment pass is to freeze planning terminology and review questions before implementation tickets are written. Future feature expansion should wait until architecture alignment planning is reviewed, especially when a change might affect identifiers, proposal events, approval gates, journaling, execution, or Weather Bot handoff.

## Current dual-architecture state

MEG is in a dual architecture in transition. The legacy whale runtime remains present, and the Phase 0A canonical rail is also present as the target shared-rail direction.

The older whale reaction bot runtime can be summarized as:

1. Polygon RPC.
2. Pre-filter.
3. Signal engine.
4. Agent core.
5. Telegram approval.
6. Order router.

The newer PRD-driven rail can be summarized as:

1. Canonical identifiers.
2. Strategy-agnostic proposal/event contracts.
3. Explicit approval gates.
4. Paper execution and operational journaling boundaries.
5. No live/autonomous execution authority.
6. Weather and research rails that must stay gated until their source, scoring, runtime, and execution posture is approved separately.

## Legacy whale runtime boundary

The legacy whale runtime still exists and must be treated as a bounded compatibility area, not as the target shared architecture. Its existing use of `market_id` is a legacy/compatibility footprint to inventory and classify, not a pattern to expand.

Until an approved alignment or migration ticket says otherwise, whale-runtime code should not add new shared-rail contracts based on `market_id`. Any later compatibility shim should be narrow, documented, operator-gated where execution is implicated, and reviewed as a bridge toward strategy-agnostic proposal/event contracts rather than a new whale-specific expansion.

## New Phase 0A canonical rail boundary

The Phase 0A canonical rail expects the canonical identifier contract: `condition_id`, `token_id`, and `outcome`. These identifiers are the target contract at true shared-rail boundaries.

A true shared-rail boundary includes cross-strategy proposal events, approval queues, journaling contracts, execution-intent surfaces, risk-gate interfaces, and any interface that multiple strategies or research tracks are expected to share. At those boundaries, `condition_id`, `token_id`, and `outcome` must be preserved as the target contract, while `market_id` remains legacy/compatibility unless explicitly approved for a bounded bridge.

## Weather Bot boundary

Weather Bot remains at a hold/checkpoint posture after Stage 2 offline ingestion closeout. Weather Bot should not be pushed into provider/source/scoring/runtime work until the architecture alignment posture is clear.

Weather Bot provider connectors are not approved. Weather Bot source fetching is not approved. Weather Bot scoring is not approved. Weather Bot runtime behavior is not approved. Weather Bot trading, execution, order placement, autonomy, live behavior, and production behavior are not approved.

Weather Bot planning can continue only as planning/static-test work that preserves the canonical rail boundary and does not imply provider readiness, source readiness, scoring readiness, runtime readiness, execution readiness, trading readiness, or production readiness.

## Canonical identifier contract

The target canonical identifier contract is:

- `condition_id`
- `token_id`
- `outcome`

This contract is the target for Phase 0A shared rail, strategy-agnostic proposal/event design, approval handoff, journaling, and later execution-intent planning. The canonical identifier contract is not yet fully enforced everywhere because the legacy whale runtime remains present; therefore, this document records the desired boundary rather than claiming migration completion.

## `market_id` compatibility window

`market_id` remains a legacy/compatibility identifier unless explicitly approved at a documented compatibility boundary. It is not the target shared-rail identifier.

The compatibility window should be treated as temporary and reviewable. Future work should inventory every current `market_id` usage, classify each usage as legacy runtime, compatibility boundary, or target-migration candidate, and prevent new unreviewed shared-rail reliance on `market_id`.

This document does not remove, migrate, rename, reinterpret, backfill, or normalize existing `market_id` usages. It also does not approve database changes or runtime adapters for `market_id` compatibility.

## Strategy-agnostic proposal/event target

The alignment target is a strategy-agnostic event and proposal contract that can be used by whale, weather, and later strategies without embedding a strategy-specific identifier as the shared rail.

The target proposal/event contract should make canonical identifiers explicit, preserve operator approval requirements, describe source/provenance fields only when separately approved, and avoid approving execution behavior. A future planning ticket should define the exact event/proposal vocabulary before any implementation ticket changes runtime modules.

## Runtime/pubsub/journaling concerns

Runtime, pubsub, and journaling boundaries are high-risk because they can silently become production behavior. This ticket does not implement runtime refactors, Redis/pubsub changes, journal writers, approval queues, background jobs, schedulers, execution paths, order routers, or production behavior.

Future alignment planning should identify which event channels, approval queues, heartbeat messages, risk gates, and journaling records are true shared-rail surfaces. Those surfaces should require `condition_id`, `token_id`, and `outcome` unless a documented compatibility shim is explicitly approved.

## Database and persistence concerns

No database schema change is implemented by this document. No migration is implemented by this document. No persistence model, generated data, fixture data, historical data, journal table, or backfill is created or modified by this document.

Future database and persistence work should be planned separately. That planning should distinguish operational journaling from research storage, identify where canonical identifiers must be required, and define any legacy `market_id` mapping requirements without implementing them in the planning ticket.

## README/onboarding concerns

README and onboarding material should eventually explain that MEG contains a legacy whale runtime and a newer Phase 0A canonical rail during staged rebuild. New contributors should not infer that `market_id` is the target shared-rail identifier simply because legacy modules still exist.

This document does not update README or onboarding files. A later README/onboarding refresh ticket should summarize the architecture boundary, the canonical identifier contract, the compatibility posture for legacy `market_id`, and the Weather Bot hold/checkpoint posture.

## Explicit non-implementation boundaries

This ticket is planning only. It does not implement migrations, refactors, runtime behavior, provider connectors, source fetching, scoring, backtesting, execution, trading, autonomy, production behavior, database schema changes, persistence changes, workflows, dependencies, generated data, fixtures, or source modules.

Specifically:

- No runtime refactor is implemented.
- No database schema change is implemented.
- No database migration is implemented.
- No source-fetching implementation is created.
- No provider/API connector implementation is created.
- No scoring/backtesting implementation is created.
- No execution, trading, order-placement, or autonomy implementation is created.
- No production behavior is created.
- No source modules are modified.
- No runtime modules are modified.
- No execution modules are modified.
- No provider connectors are modified.
- No source-fetching modules are modified.
- No scoring or backtesting modules are modified.
- No database models or migrations are modified.

## Recommended alignment sequence

1. Inventory current `market_id` usage.
2. Classify each usage as legacy runtime, compatibility boundary, or target-migration candidate.
3. Define true shared-rail boundary contracts.
4. Define strategy-agnostic event/proposal contract.
5. Define allowed whale-runtime compatibility shim behavior.
6. Define DB/persistence migration planning requirements without implementing them.
7. Define README/onboarding update requirements.
8. Define later implementation tickets.

## Blocked future work until alignment

Future feature expansion should wait until architecture alignment planning is reviewed. In particular, do not advance provider connectors, source fetching, scoring, backtesting, runtime behavior, execution, trading, autonomy, production behavior, or Weather Bot runtime expansion while the canonical rail versus legacy whale boundary remains unreviewed.

Weather Bot should remain at a hold/checkpoint after offline ingestion closeout until the architecture posture is clear. Whale-runtime expansion should also wait unless it is framed as a reviewed compatibility or alignment step that does not create autonomous execution authority.

## Machine-checkable architecture alignment assignments

- architecture alignment stage: architecture_alignment_planning
- current architecture state: dual_architecture_in_transition
- current architecture state: legacy_whale_runtime_present
- current architecture state: phase0a_canonical_rail_present
- current architecture state: weather_stage2_offline_ingestion_skeleton_closed_out
- canonical id posture: condition_id_token_id_outcome_target_contract
- canonical id posture: canonical_ids_required_at_true_shared_rail_boundaries
- canonical id posture: canonical_id_enforcement_not_complete
- market id posture: legacy_compatibility_identifier
- market id posture: allowed_only_at_approved_compatibility_boundaries
- market id posture: not_target_shared_rail_identifier
- legacy runtime posture: whale_runtime_existing
- legacy runtime posture: whale_runtime_must_not_expand_without_alignment
- legacy runtime posture: whale_runtime_candidate_for_strategy_agnostic_wrapping
- weather bot posture: weather_bot_hold_checkpoint_after_offline_ingestion_closeout
- weather bot posture: weather_bot_provider_connectors_not_approved
- weather bot posture: weather_bot_source_fetching_not_approved
- weather bot posture: weather_bot_scoring_runtime_trading_not_approved
- implementation posture: planning_only
- implementation posture: no_runtime_refactor
- implementation posture: no_database_migration
- implementation posture: no_source_fetching
- implementation posture: no_provider_connector
- implementation posture: no_scoring_backtesting
- implementation posture: no_execution_trading
- implementation posture: no_production_behavior
- later gate posture: architecture_alignment_review
- later gate posture: market_id_inventory_ticket
- later gate posture: shared_rail_contract_planning_ticket
- later gate posture: strategy_agnostic_event_contract_planning_ticket
- later gate posture: readme_onboarding_refresh_ticket
- evidence status: source_backed
- evidence status: reviewer_inferred
- evidence status: missing
- evidence status: conflicting
- evidence status: not_applicable
- label confidence: confirmed
- label confidence: unclear
- label confidence: unknown

## Acceptance criteria

- The planning document exists with canonical ID `MEG-ARCH-ALIGN-01`.
- The document includes every required section for the architecture alignment planning pass.
- The document states that this is planning only.
- The document states that no runtime refactor, database schema change, database migration, source fetching, provider/API connector, scoring/backtesting, execution/trading/autonomy, or production behavior is implemented.
- The document identifies the current dual architecture in transition.
- The document identifies that the legacy whale runtime still exists.
- The document identifies that the Phase 0A canonical rail expects `condition_id`, `token_id`, and `outcome`.
- The document identifies `market_id` as legacy/compatibility unless explicitly approved at a boundary.
- The document states that Weather Bot remains at hold/checkpoint after offline ingestion closeout and that provider connectors, source fetching, scoring, runtime, and trading remain unapproved for Weather Bot.
- The document includes the recommended alignment sequence.
- The machine-checkable assignment section exists, is section-scoped, includes every allowed closed-set value, and uses no unapproved actual assignment values.
- Static tests validate the document without importing non-standard-library dependencies.
