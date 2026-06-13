# MEG-ARCH-ALIGN-04 Shared-Rail Contract Review and market_id Migration Candidate Planning

Canonical ID: MEG-ARCH-ALIGN-04

## Status and scope

This is planning only. This ticket creates a static planning document and companion static test for a later shared-rail contract review. It does not create the actual shared-rail contract review table, does not create the actual migration-candidate review table, and does not approve any implementation.

No runtime refactor is implemented. No database migration is implemented. No source-code migration is implemented. No provider connector is implemented. No source fetching is implemented. No scoring/backtesting is implemented. No runtime behavior is implemented. No execution/trading/autonomy is implemented. No production behavior is implemented.

This ticket does not approve migration work. This ticket does not approve compatibility shims. This ticket does not approve DB/schema changes. This ticket does not approve provider connectors. This ticket does not approve source fetching. This ticket does not approve Weather Bot provider/source/scoring/runtime/trading expansion.

## Relationship to MEG-ARCH-ALIGN-01

`MEG-ARCH-ALIGN-01` established that MEG is in a dual-architecture transition: legacy whale-runtime surfaces still exist while shared-rail planning moves toward canonical identifiers. This planning document preserves that posture by treating the later shared-rail contract review as a review gate, not as permission to migrate runtime or persistence surfaces.

## Relationship to MEG-ARCH-ALIGN-02

`MEG-ARCH-ALIGN-02` planned the repository-level `market_id` inventory/classification method and required closed-set classification discipline before any migration work. This planning document uses that method as the input discipline for a later review: inventory labels are planning inputs, not implementation decisions.

## Relationship to MEG-ARCH-ALIGN-03

`MEG-ARCH-ALIGN-03` created the static `market_id` inventory artifact and identified paths classified as `target_migration_candidate` and `approved_compatibility_boundary` using static text evidence. This planning document reviews those categories only at the planning-method level and defines how a later ticket should examine them before implementation, refactor, migration, provider, source, scoring, runtime, trading, autonomy, or production work.

## Shared-rail contract review objective

A future shared-rail contract review should identify true shared-rail surfaces, document each surface's current identifier contract, and compare it with the target identifier contract. The future review should determine whether each surface is a shared-rail surface, legacy runtime surface, compatibility boundary, documentation surface, test harness surface, or unknown surface.

The future review must be source-backed where possible and must preserve human review for ambiguous labels. It must not infer that a `market_id` occurrence is safe merely because it appears in an existing path; it must inspect surface ownership, runtime adjacency, persistence implications, and approval-gate implications.

## Target-migration candidate review objective

A future migration-candidate review should examine every path classified as `target_migration_candidate` in `MEG-ARCH-ALIGN-03`. For each path, the reviewer should determine whether the path touches events, journaling, approval gates, risk gates, execution intent, dashboard/API surfaces, data-layer surfaces, database/persistence surfaces, runtime internals, documentation, or test harnesses.

The objective is to decide what later planning track is required: source-code migration planning, database migration planning, compatibility shim planning, documentation-refresh planning, shared-rail contract implementation planning, or human review. Target-migration candidates require separate human review before implementation.

## Compatibility-boundary review objective

A future compatibility-boundary review should examine every path classified as `approved_compatibility_boundary` in `MEG-ARCH-ALIGN-03`. The review should decide whether each boundary should remain, shrink later, become a compatibility shim later, become a migration candidate later, or remain unknown until additional review.

Compatibility-boundary candidates require separate human review before implementation. This document does not approve compatibility shims and does not approve movement of any compatibility boundary into source-code, database, provider, source-fetching, scoring, runtime, execution, trading, autonomy, or production work.

## Target canonical identifier contract

`condition_id`, `token_id`, and `outcome` remain the target shared-rail identifier contract. Canonical IDs are required at true shared-rail boundaries, and canonical-ID enforcement is not complete.

A future review should verify whether each candidate surface currently accepts, emits, stores, displays, derives, or routes identifiers using the target contract. Where a surface lacks the target contract, the review should label the gap and recommend a later planning ticket rather than changing code in the review ticket.

## market_id compatibility posture

`market_id` remains legacy/compatibility unless a later explicit boundary approves otherwise. It is not the target shared-rail identifier. It may appear only at approved compatibility boundaries or in frozen/test-harness contexts that have been explicitly reviewed.

A future review should treat `market_id` usage as a compatibility concern and should not approve migration work, compatibility shims, DB/schema changes, or provider/source behavior changes without a separate explicit approval.

## Candidate review method

The future candidate review should start from the `MEG-ARCH-ALIGN-03` `target_migration_candidate` list. For each path, reviewers should:

1. Identify the owning path or module and the likely surface type.
2. Determine whether the path touches events, journaling, approval gates, risk gates, execution intent, dashboard/API surfaces, data-layer surfaces, or database/persistence surfaces.
3. Record current identifier usage without changing source code.
4. Compare current usage against the target `condition_id`, `token_id`, and `outcome` contract.
5. Assign a closed-set proposed review category, risk level, and recommended review action.
6. Decide whether the candidate requires a source-code migration plan, DB migration plan, compatibility shim plan, documentation-only treatment, or human review.
7. Stop before implementation; future implementation/refactor/migration work requires separate explicit approval.

## Compatibility-boundary review method

The future compatibility-boundary review should start from the `MEG-ARCH-ALIGN-03` `approved_compatibility_boundary` list. For each path, reviewers should:

1. Confirm whether the boundary is documentation-only, a test-harness guard, or a live code/runtime-adjacent surface.
2. Determine whether the boundary should remain, shrink later, become a compatibility shim later, become a migration candidate later, or remain unknown.
3. Assign compatibility pressure without changing source code.
4. Assign a required later ticket if the boundary cannot remain as-is.
5. Preserve `market_id` as legacy/compatibility and avoid treating compatibility text as shared-rail target approval.
6. Stop before implementation; compatibility-boundary candidates require separate human review before implementation.

## Future shared-rail contract output format

A later ticket may create an actual shared-rail contract review table. This ticket defines the future table schema but does not create the actual table yet.

Future columns:

- surface_name
- owning_path_or_module
- current_identifier_contract
- target_identifier_contract
- boundary_type
- migration_pressure
- compatibility_pressure
- required_later_ticket
- reviewer_notes

Allowed `boundary_type` values:

- shared_rail_surface
- legacy_runtime_surface
- compatibility_boundary
- documentation_surface
- test_harness_surface
- unknown_surface

Allowed `migration_pressure` values:

- none
- low
- medium
- high
- blocker
- unknown

Allowed `compatibility_pressure` values:

- none
- keep_temporarily
- shrink_later
- shim_later
- migrate_later
- unknown

Allowed `required_later_ticket` values:

- no_ticket_required
- source_code_migration_planning
- database_migration_planning
- compatibility_shim_planning
- shared_rail_contract_implementation_planning
- documentation_refresh_planning
- human_review_required

## Future migration-candidate review output format

A later ticket may create an actual migration-candidate review table. This ticket defines the future table schema but does not create the actual table yet.

Future columns:

- path
- current_category
- proposed_review_category
- current_identifier_usage
- target_identifier_contract
- likely_surface_type
- risk_level
- recommended_review_action
- reviewer_notes

Allowed `proposed_review_category` values:

- confirm_target_migration_candidate
- reclassify_as_legacy_runtime
- reclassify_as_compatibility_boundary
- reclassify_as_test_harness_guard
- reclassify_as_frozen_doc
- requires_more_review

Allowed `likely_surface_type` values:

- event_contract
- journal_contract
- approval_gate
- risk_gate
- execution_intent
- dashboard_api
- data_layer
- database_persistence
- runtime_internal
- documentation
- test_harness
- unknown

Allowed `recommended_review_action` values:

- plan_source_code_migration
- plan_database_migration
- plan_compatibility_shim
- keep_as_legacy_runtime
- keep_as_test_guard
- leave_frozen_doc
- request_human_review

Allowed `risk_level` values:

- low
- medium
- high
- blocker
- unknown

## Explicit non-implementation boundaries

- Planning only.
- No runtime refactor is implemented.
- No database migration is implemented.
- No source-code migration is implemented.
- No provider connector is implemented.
- No source fetching is implemented.
- No scoring/backtesting is implemented.
- No runtime behavior is implemented.
- No execution/trading/autonomy is implemented.
- No production behavior is implemented.
- This ticket does not approve migration work.
- This ticket does not approve compatibility shims.
- This ticket does not approve DB/schema changes.
- This ticket does not approve provider connectors.
- This ticket does not approve source fetching.
- This ticket does not approve Weather Bot provider/source/scoring/runtime/trading expansion.
- Future implementation/refactor/migration work requires separate explicit approval.

## Blocked future work until review

The following future work remains blocked until a separate human-reviewed planning or approval ticket authorizes it:

- Runtime refactors that change identifier routing.
- Database migrations or DB/schema changes.
- Source-code migrations from `market_id` to canonical identifiers.
- Compatibility shim implementation.
- Provider connectors or source-fetching behavior.
- Scoring, backtesting, runtime behavior, execution, trading, autonomy, or production behavior.
- Weather Bot provider/source/scoring/runtime/trading expansion.

## Recommended later ticket sequence

1. `MEG-ARCH-ALIGN-05_SHARED_RAIL_CONTRACT_REVIEW_ARTIFACT`: docs/static-test only; create the actual shared-rail contract review table from the schema above; do not implement runtime, database, provider, source, scoring, execution, trading, autonomy, or production changes.
2. `MEG-ARCH-ALIGN-06_MIGRATION_CANDIDATE_REVIEW_ARTIFACT`: docs/static-test only; create the actual migration-candidate review table from the schema above; do not implement source-code migration or compatibility shims.
3. `MEG-ARCH-ALIGN-07_COMPATIBILITY_BOUNDARY_REVIEW_ARTIFACT`: docs/static-test only; review whether boundaries remain, shrink, become shims later, become migration candidates later, or require human review; do not implement shims.
4. Later approval-request tickets, if needed, should request explicit human approval for narrowly scoped planning. They must not bundle runtime refactor, DB migration, provider connector, source fetching, scoring, backtesting, runtime behavior, trading, autonomy, or production behavior.

## Machine-checkable shared-rail contract review assignments

- architecture alignment stage: shared_rail_contract_review_planning
- review artifact status: planning_created
- review artifact status: no_review_table_created
- review artifact status: later_review_ticket_required
- review artifact status: migration_not_approved
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

- The planning document exists at `docs/prd/MEG-ARCH-ALIGN-04_SHARED_RAIL_CONTRACT_REVIEW_PLANNING.md`.
- The canonical ID `MEG-ARCH-ALIGN-04` appears.
- All required sections appear.
- Relationships to `MEG-ARCH-ALIGN-01`, `MEG-ARCH-ALIGN-02`, and `MEG-ARCH-ALIGN-03` appear.
- Planning-only scope and explicit non-implementation boundaries are stated.
- The target identifier contract remains `condition_id`, `token_id`, and `outcome`.
- `market_id` remains legacy/compatibility unless a later explicit boundary approves otherwise.
- Future shared-rail contract and migration-candidate output formats are defined without creating actual review output tables.
- Every required closed-set value appears in the document and in the machine-checkable section.
- The machine-checkable parser is section-scoped.
- Weather Bot remains at the hold/checkpoint posture for provider/source/scoring/runtime/trading work.
