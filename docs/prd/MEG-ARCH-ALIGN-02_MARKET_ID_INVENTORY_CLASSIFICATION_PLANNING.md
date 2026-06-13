# MEG-ARCH-ALIGN-02 Legacy market_id Inventory and Classification Planning

Canonical ID: `MEG-ARCH-ALIGN-02`

## Status and scope

This document is a planning-only artifact for `MEG-ARCH-ALIGN-02`. It defines how MEG should later inventory and classify the current `market_id` footprint during the dual-architecture transition.

This ticket creates only an inventory/classification planning artifact. It does not create the actual inventory output unless explicitly approved later in a separate ticket.

This planning pass implements no product behavior. No migration is implemented. No runtime refactor is implemented. No source-code migration is implemented. No database schema change is implemented. No database migration is implemented. No source fetching is implemented. No provider/API connector is implemented. No scoring/backtesting is implemented. No execution/trading/autonomy is implemented. No production behavior is implemented.

## Relationship to MEG-ARCH-ALIGN-01

`MEG-ARCH-ALIGN-01` established that MEG is in a dual-architecture transition. The older whale runtime remains present and still uses `market_id`, while the newer Phase 0A canonical rail targets `condition_id`, `token_id`, and `outcome` at true shared-rail boundaries.

This document follows `MEG-ARCH-ALIGN-01` by narrowing the next planning question: how to inventory the legacy `market_id` footprint and classify it before expanding shared-rail features. It does not supersede `MEG-ARCH-ALIGN-01`; it adds a planning schema for a later inventory artifact.

## Inventory objective

The objective is to prepare a repo-level inventory plan for every current literal `market_id` usage so reviewers can distinguish legacy runtime compatibility from migration candidates without changing runtime code.

Every current `market_id` usage should eventually be classified before shared-rail feature expansion. Until that classification exists, `market_id` remains legacy/compatibility unless explicitly classified and approved otherwise.

The target shared-rail identifier contract remains `condition_id`, `token_id`, and `outcome`. `market_id` is not the target shared-rail identifier.

## Classification categories

Future inventory rows must use only these classification categories:

- `legacy_whale_runtime`
- `approved_compatibility_boundary`
- `target_migration_candidate`
- `frozen_historical_doc`
- `test_harness_guard`
- `unknown_requires_review`

These categories are closed-set labels for planning and review. They do not approve migrations, runtime adapters, schema changes, source fetching, provider connectors, scoring/backtesting, execution, trading, autonomy, or production behavior.

## Legacy whale-runtime usage

`legacy_whale_runtime` is for current whale-runtime files whose existing behavior still depends on `market_id` as part of the older runtime footprint. This category preserves the MEG-ARCH-ALIGN-01 finding that older whale-runtime usage is present and bounded.

A `legacy_whale_runtime` classification is not permission to expand whale-runtime behavior, add new shared-rail contracts based on `market_id`, approve trading, approve autonomous execution, or bypass Telegram/operator approval. It is an inventory label only.

## Compatibility-boundary usage

`approved_compatibility_boundary` is for explicitly documented boundaries where `market_id` may remain visible as a compatibility identifier while canonical shared-rail boundaries move toward `condition_id`, `token_id`, and `outcome`.

A compatibility-boundary classification should be narrow, source-backed, and reviewable. It must not become a general permission to route shared-rail features on `market_id`.

## Target-migration candidates

`target_migration_candidate` is for current `market_id` usage that appears to touch, resemble, or feed a shared-rail boundary that should eventually move toward the canonical `condition_id`, `token_id`, and `outcome` contract.

A target-migration classification only identifies later work. This document does not implement any source-code migration, compatibility shim, database schema change, database migration, runtime refactor, or production behavior.

## Out-of-scope implementation boundaries

This ticket is planning only. It creates a planning document and a static test for that document.

The following remain out of scope:

- no migration is implemented
- no runtime refactor is implemented
- no source-code migration is implemented
- no database schema change is implemented
- no database migration is implemented
- no source fetching is implemented
- no provider/API connector is implemented
- no scoring/backtesting is implemented
- no execution/trading/autonomy is implemented
- no production behavior is implemented
- no generated data is created
- no fixture file is changed
- no workflow or dependency is changed

Weather Bot remains hold/checkpoint for provider/source/scoring/runtime/trading work. Weather Bot provider connectors are not approved. Weather Bot source fetching is not approved. Weather Bot scoring/runtime/trading work is not approved by this ticket.

## Inventory method

The recommended future inventory method is:

1. Use a static text scan for the literal `market_id`.
2. Compare observed files and line counts against `tests/core/canonical_id_allowlist.py`.
3. Classify each file by path and architectural role.
4. Do not change runtime code during inventory.
5. Do not shrink or expand the allowlist without explicit review.
6. Produce a later inventory artifact only in a separate ticket.

The inventory method should use repository text evidence and reviewer notes, not runtime execution, source fetching, provider/API calls, scoring, backtesting, trading, or production workflows.

## Classification method

A reviewer should classify each future inventory row by combining static text evidence, file path, source-of-truth PRD context, and architectural role.

Suggested classification rules:

- Use `legacy_whale_runtime` for existing whale-runtime modules and tests that preserve the old runtime footprint.
- Use `approved_compatibility_boundary` only where a compatibility boundary is explicitly documented and reviewable.
- Use `target_migration_candidate` for shared-rail-facing surfaces that should eventually move toward `condition_id`, `token_id`, and `outcome`.
- Use `frozen_historical_doc` for historical or frozen source-of-truth documents that should not be edited only to remove legacy terms.
- Use `test_harness_guard` for tests or allowlists that intentionally guard the legacy footprint.
- Use `unknown_requires_review` when the path or role is unclear.

## Expected inventory output format

A later ticket may create the actual inventory artifact. This ticket defines only the future table schema and does not create the table yet.

Future inventory rows should use these fields:

- `path`
- `line_count`
- `current_category`
- `proposed_category`
- `rationale`
- `recommended_next_action`
- `risk_level`
- `reviewer_notes`

Allowed values for `current_category` and `proposed_category` are:

- `legacy_whale_runtime`
- `approved_compatibility_boundary`
- `target_migration_candidate`
- `frozen_historical_doc`
- `test_harness_guard`
- `unknown_requires_review`

Allowed values for `recommended_next_action` are:

- `keep_as_legacy_boundary`
- `wrap_with_compatibility_shim_later`
- `migrate_to_canonical_ids_later`
- `leave_frozen_doc`
- `keep_test_guard`
- `needs_human_review`

Allowed values for `risk_level` are:

- `low`
- `medium`
- `high`
- `blocker`
- `unknown`

## Review and approval requirements

The later inventory artifact must be reviewed before it is used to authorize implementation work. Classification labels should be source-backed when possible and explicitly marked as reviewer-inferred, missing, conflicting, or not applicable when evidence is limited.

Any later migration, compatibility shim, source-code edit, database schema change, database migration, provider/API connector, source-fetching path, scoring/backtesting work, execution/trading/autonomy work, or production behavior requires a separate approved ticket.

## Blocked future work until classification

Shared-rail feature expansion that depends on identifier posture is blocked until the current `market_id` footprint is inventoried and classified.

Blocked work includes runtime refactors, source-code migrations, database migrations, provider connectors, source fetching, scoring/backtesting, execution/trading/autonomy, and production behavior. Weather Bot remains hold/checkpoint for provider/source/scoring/runtime/trading work until separate approvals exist.

## Machine-checkable market_id inventory assignments

- architecture alignment stage: market_id_inventory_classification_planning
- inventory status: inventory_not_created
- inventory status: inventory_method_defined
- inventory status: classification_schema_defined
- inventory status: later_inventory_ticket_required
- canonical id posture: condition_id_token_id_outcome_target_contract
- canonical id posture: canonical_ids_required_at_true_shared_rail_boundaries
- canonical id posture: canonical_id_enforcement_not_complete
- market id posture: legacy_compatibility_identifier
- market id posture: allowed_only_at_approved_compatibility_boundaries
- market id posture: not_target_shared_rail_identifier
- market id posture: inventory_required_before_expansion
- classification category: legacy_whale_runtime
- classification category: approved_compatibility_boundary
- classification category: target_migration_candidate
- classification category: frozen_historical_doc
- classification category: test_harness_guard
- classification category: unknown_requires_review
- future inventory field: path
- future inventory field: line_count
- future inventory field: current_category
- future inventory field: proposed_category
- future inventory field: rationale
- future inventory field: recommended_next_action
- future inventory field: risk_level
- future inventory field: reviewer_notes
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
- implementation posture: planning_only
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

- The planning PRD exists at `docs/prd/MEG-ARCH-ALIGN-02_MARKET_ID_INVENTORY_CLASSIFICATION_PLANNING.md`.
- The canonical ID `MEG-ARCH-ALIGN-02` appears.
- All required sections appear.
- The relationship to `MEG-ARCH-ALIGN-01` is explicit.
- Planning-only scope and non-implementation boundaries are explicit.
- The target canonical identifiers `condition_id`, `token_id`, and `outcome` appear.
- `market_id` is described as legacy/compatibility unless explicitly classified.
- All classification categories appear.
- The future inventory output fields and allowed values appear.
- The recommended future inventory method appears.
- Weather Bot hold/checkpoint posture appears.
- The machine-checkable section is section-scoped and uses only allowed closed-set values.
