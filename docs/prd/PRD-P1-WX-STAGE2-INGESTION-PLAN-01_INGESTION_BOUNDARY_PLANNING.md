# PRD-P1-WX-STAGE2-INGESTION-PLAN-01 — Weather Bot Ingestion Boundary Planning

Canonical ID: PRD-P1-WX-STAGE2-INGESTION-PLAN-01

## Status and scope

This is ingestion boundary planning only. It is a docs/static-test planning artifact for Weather Bot Stage 2 and does not create, approve, or imply any ingestion implementation.

This planning document is aligned with `AGENTS.md`, `docs/meta/MEG_ACTIVE_STATE.md`, `docs/meta/domain_packets/WEATHER_BOT_PACKET.md`, and the standalone MEG Weather Bot PRD at `docs/prd/PRD-P1-WX-STANDALONE_WEATHER_BOT_PRD.md`.

## Strategic framing

Weather Bot Stage 2 has completed skeleton, fixture, real source-backed fixture, historical-label loading/validation planning, and static loader/validator closeout work. This document records the boundary vocabulary that would be needed before any later ingestion work can even be requested.

The strategic purpose is to prevent fixture, loader, and planning artifacts from being mistaken for source intake, provider readiness, scoring readiness, runtime readiness, production readiness, or trading readiness.

## Stage ladder position

This planning step follows these prior Stage 2 checkpoints:

- `PRD-P1-WX-STAGE2-SKELETON-CLOSEOUT-01`
- `PRD-P1-WX-STAGE2-FIXTURE-IMPLEMENTATION-CLOSEOUT-01`
- `PRD-P1-WX-STAGE2-REAL-FIXTURE-IMPLEMENTATION-CLOSEOUT-01`
- `PRD-P1-WX-STAGE2-HISTORICAL-LABEL-LOADING-PLAN-CLOSEOUT-01`
- `PRD-P1-WX-STAGE2-HISTORICAL-LABEL-LOADING-IMPLEMENTATION-01`
- `PRD-P1-WX-STAGE2-HISTORICAL-LABEL-LOADING-IMPLEMENTATION-CLOSEOUT-01`
- `PRD-P1-WX-STAGE2-INGESTION-PLANNING-APPROVAL-01`

The stage ladder remains gated. The current fixture, loading, loader, and ingestion-planning documents do not imply ingestion readiness, provider readiness, scoring readiness, runtime readiness, production readiness, or trading readiness.

## Human approval context

`PRD-P1-WX-STAGE2-INGESTION-PLANNING-APPROVAL-01` requested human approval for future ingestion boundary planning only. The current human choice permits this planning step and nothing beyond it.

Future ingestion implementation requires a later separate approval chain. Future provider/API connector implementation requires a later separate approval chain. Future provider/source connector implementation requires a later separate approval chain. Future source fetching requires a later separate approval chain. Future scoring/backtesting requires separate explicit approval. Future runtime/trading requires separate explicit approval.

## Planning-only boundary

This ticket may define vocabulary, source-category boundaries, provenance requirements, no-lookahead requirements, fixture/loader separation rules, fail-closed blocker categories, and handoff gates.

It must not define concrete implementation details: no function signatures, no classes, no modules, no CLI commands, no scripts, no configs, no DB schemas, no APIs, no connector interfaces, no runtime workflows, no job schedules, no queue names, and no provider-specific client behavior.

## Ingestion boundary vocabulary

The planning vocabulary separates these concepts:

- `ingestion_boundary_vocabulary`: terms used to describe possible later intake boundaries.
- `source_category_boundary`: closed source-category labels for future planning review.
- `source_identity_requirement`: required identity facts that must exist before later intake can be requested.
- `source_provenance_requirement`: required evidence trail facts that must exist before later intake can be requested.
- `access_date_requirement`: requirement that future source review record when the source was accessed.
- `no_lookahead_requirement`: requirement that later labels and evidence not use unavailable future information.
- `fixture_ingestion_separation`: fixtures remain static validation artifacts, not intake artifacts.
- `loader_ingestion_separation`: the static loader remains validation-only, not intake behavior.
- `fail_closed_blocker_taxonomy`: blockers that stop later handoff when evidence is missing or ambiguous.
- `provider_connector_handoff`: later planning gate for provider/source connector questions.
- `scoring_backtesting_handoff`: later planning gate for scoring/backtesting questions.
- `runtime_trading_handoff`: later planning gate for runtime/trading questions.

## Allowed future source categories for planning

Allowed future source categories for planning vocabulary are:

- `human_reviewed_fixture_source`: a human-reviewed source used to explain static fixture evidence.
- `official_resolution_source`: a source that records final settlement or resolution facts.
- `venue_rule_source`: a source that records venue-defined rule language and settlement criteria.
- `weather_station_source`: a source that records station observations or station metadata.
- `market_metadata_source`: a source that records market-level metadata relevant to source interpretation.
- `manual_research_note`: a human-authored note that summarizes source review while preserving source identity and access context.
- `not_applicable`: a closed-set placeholder when no allowed future source category applies to a row.

These are planning labels only and do not approve source fetching or provider/API connector implementation.

## Prohibited source categories

Prohibited source categories are:

- `unattributed_social_post`
- `unverified_ai_summary`
- `live_market_feed`
- `broker_execution_feed`
- `private_credentials_source`
- `runtime_scrape`
- `unreviewed_bulk_dataset`
- `unknown_source`
- `not_applicable`

These labels identify categories that must fail closed or remain out of scope in any later planning discussion unless a later human-approved document changes the boundary.

## Source identity and provenance requirements

Before any later ingestion can exist, source identity planning must require the source owner or publisher, source title or stable description, source category, relevant venue or station context, and a human-reviewable reason the source is relevant.

Before any later ingestion can exist, source provenance planning must require access date, retrieval context, evidence status, label confidence, known conflict notes, and a record of whether the source is direct, reviewer-inferred, missing, conflicting, or not applicable.

This document does not define source file formats beyond planning vocabulary.

## No-lookahead safeguards

No-lookahead planning requires that future evidence be evaluated according to what would have been available at the relevant decision or label time. Any later source review must identify access date, retrieval context, publication or resolution posture when relevant, and conflicts between source timing and label timing.

A later ticket must fail closed on time-window conflict when evidence depends on information unavailable at the relevant planned label boundary.

## Fixture-to-ingestion separation rules

Static fixtures remain static validation artifacts. No fixture JSON files are read by new source/runtime code. No fixture JSON files are created or modified. No fixture README files are created or modified.

Fixtures may document evidence examples, but they do not become ingestion artifacts, source-fetching artifacts, generated data, runtime data access, production behavior, or trading support.

## Static-loader-to-ingestion separation rules

The static historical-label loader remains a narrow validation artifact. No loader expansion is created or approved. The loader is not a provider connector, not source fetching, not external API calls, not credentials/secrets/config loading, not forecast pulls, not runtime observation, and not production behavior.

This document does not modify `meg/weather/stage2/historical_label_loader.py` or `meg/weather/stage2/historical_label.py`.

## Fail-closed ingestion blocker taxonomy

Later planning must fail closed on these blocker categories:

- `missing_source_identity`
- `missing_access_date`
- `missing_venue_rule`
- `missing_resolver_source`
- `unsupported_source_category`
- `unknown_source_category`
- `source_conflict`
- `time_window_conflict`
- `fixture_ingestion_confusion`
- `loader_ingestion_confusion`
- `runtime_drift`
- `connector_drift`
- `scoring_drift`
- `trading_drift`
- `other_unclear`

A fail-closed blocker means the later work must stop until a human-reviewed ticket resolves the ambiguity.

## Provider/source connector handoff rules

Provider/API connector implementation is not approved. Provider/source connector planning may only be requested later if this boundary plan is closed out and a separate approval chain asks whether connector planning is appropriate.

Future provider/API connector implementation requires a later separate approval chain. Future provider/source connector implementation requires a later separate approval chain. Future source fetching requires a later separate approval chain.

## Scoring/backtesting handoff rules

Scoring/probability scoring is not approved. Backtesting/paper simulation is not approved. Future scoring/backtesting requires separate explicit approval and must not be inferred from fixture, loading, loader, or ingestion-planning artifacts.

Any later scoring/backtesting planning must preserve no-lookahead safeguards and fail closed on evidence or timing drift.

## Runtime/trading handoff rules

Runtime observation is not approved. Trading, order placement, position sizing, and autonomy are not approved. Production behavior is not approved. C++/Rust runtime components are not approved.

Future runtime/trading requires separate explicit approval and must not be inferred from Weather Bot Stage 2 planning, fixture, loading, or loader artifacts.

## What this planning document confirms

This document confirms a planning-only vocabulary and boundary posture for Weather Bot Stage 2 ingestion discussions. It confirms separation between static fixtures, the static loader, and any possible later ingestion artifacts.

It also confirms that no historical-label data files are created and no generated data is created by this planning step.

## What remains unbuilt

Ingestion implementation is not approved and remains unbuilt. Provider/API connector implementation is not approved and remains unbuilt. Source fetching is not approved and remains unbuilt. External API calls are not approved and remain unbuilt. Credentials/secrets/config loading is not approved and remains unbuilt. Forecast pulls are not approved and remain unbuilt.

Scraping, polling, streaming, scheduling, queues, jobs, and background tasks are not approved and remain unbuilt. The phrase scraping, polling, streaming, scheduling, queues, jobs, and background tasks are not approved is a non-approval boundary, not implementation permission. Scoring/probability scoring is not approved and remains unbuilt. Backtesting/paper simulation is not approved and remains unbuilt. Runtime observation is not approved and remains unbuilt. Trading, order placement, position sizing, and autonomy are not approved and remain unbuilt. Production behavior is not approved and remains unbuilt. C++/Rust runtime components are not approved and remain unbuilt.

## Explicit non-approval boundaries

The following categories are explicitly not approved by this document:

- `ingestion_implementation`
- `provider_integration`
- `connectors`
- `source_fetching`
- `external_api_calls`
- `credentials_secrets_config`
- `forecast_pulls`
- `scraping_polling_streaming`
- `scheduling_queues_jobs`
- `model_scoring`
- `probability_scoring`
- `backtesting`
- `paper_simulation`
- `runtime_observation`
- `trading_order_autonomy`
- `production_behavior`
- `cplusplus_rust_runtime`
- `other_unclear`

These non-approval boundaries are intended to prevent approval drift.

## Future gates

Future tickets may only request human decisions within these boundaries:

- `may_request_ingestion_implementation_approval_later`
- `may_request_provider_connector_planning_later`
- `may_request_scoring_backtesting_planning_later`
- `may_request_runtime_observation_planning_later`
- `blocked_until_human_decision`

Future tickets must also preserve these prohibitions until separately approved:

- `must_not_create_ingestion_now`
- `must_not_create_connectors`
- `must_not_create_source_fetching`
- `must_not_create_external_api_calls`
- `must_not_create_runtime`
- `must_not_create_scoring`
- `must_not_create_trading`

## Closed ingestion boundary planning vocabulary

Closed value families for this planning document are ingestion planning stage, planning status, planned ingestion boundary category, allowed future source category, prohibited source category, planned blocker category, boundary status, future ticket permission, data posture, non-approval category, evidence status, and label confidence.

Actual machine-checkable assignments must use only the exact values listed in the machine-checkable section.

## Forbidden ingestion boundary planning values

Forbidden examples are documented here so future reviewers do not treat them as actual assignment values:

- `planning_prepared/implementation_not_approved`
- `preserved/not_approved`
- `source_backed/reviewer_inferred`
- `confirmed/unclear`
- `partial`
- `mixed`
- `likely_confirmed`
- `maybe`
- `approved`
- `configured`
- `available`
- `ingestion_ready`
- `connector_ready`
- `provider_ready`
- `source_ready`
- `scoring_ready`
- `runtime_ready`
- `trading_ready`
- `production_ready`
- `model_ready`
- `backtest_ready`
- `ready_for_ingestion`
- `ready_for_connectors`
- `ready_for_source_fetching`
- `ready_for_scoring`
- `ready_for_runtime`
- `ready_for_trading`
- `approved_for_ingestion`
- `approved_for_connectors`
- `approved_for_source_fetching`
- `approved_for_runtime`
- `approved_for_scoring`
- `approved_for_trading`
- `trade_ready`
- `auto_execute`
- `autonomous`
- `live`
- `production`

These examples are forbidden as actual machine-checkable values, but normal prose may still state non-approval boundaries.

## Machine-checkable ingestion boundary planning assignments

- ingestion planning stage: stage_2_ingestion_boundary_planning
- planning status: planning_prepared
- planning status: implementation_not_approved
- planning status: source_fetching_not_approved
- planning status: human_review_required
- planning status: blocked_pending_fix
- planning status: unclear
- planned ingestion boundary category: ingestion_boundary_vocabulary
- planned ingestion boundary category: source_category_boundary
- planned ingestion boundary category: source_identity_requirement
- planned ingestion boundary category: source_provenance_requirement
- planned ingestion boundary category: access_date_requirement
- planned ingestion boundary category: no_lookahead_requirement
- planned ingestion boundary category: fixture_ingestion_separation
- planned ingestion boundary category: loader_ingestion_separation
- planned ingestion boundary category: fail_closed_blocker_taxonomy
- planned ingestion boundary category: provider_connector_handoff
- planned ingestion boundary category: scoring_backtesting_handoff
- planned ingestion boundary category: runtime_trading_handoff
- allowed future source category: human_reviewed_fixture_source
- allowed future source category: official_resolution_source
- allowed future source category: venue_rule_source
- allowed future source category: weather_station_source
- allowed future source category: market_metadata_source
- allowed future source category: manual_research_note
- allowed future source category: not_applicable
- prohibited source category: unattributed_social_post
- prohibited source category: unverified_ai_summary
- prohibited source category: live_market_feed
- prohibited source category: broker_execution_feed
- prohibited source category: private_credentials_source
- prohibited source category: runtime_scrape
- prohibited source category: unreviewed_bulk_dataset
- prohibited source category: unknown_source
- prohibited source category: not_applicable
- planned blocker category: missing_source_identity
- planned blocker category: missing_access_date
- planned blocker category: missing_venue_rule
- planned blocker category: missing_resolver_source
- planned blocker category: unsupported_source_category
- planned blocker category: unknown_source_category
- planned blocker category: source_conflict
- planned blocker category: time_window_conflict
- planned blocker category: fixture_ingestion_confusion
- planned blocker category: loader_ingestion_confusion
- planned blocker category: runtime_drift
- planned blocker category: connector_drift
- planned blocker category: scoring_drift
- planned blocker category: trading_drift
- planned blocker category: other_unclear
- boundary status: preserved
- boundary status: not_approved
- boundary status: explicitly_out_of_scope
- boundary status: separate_human_approval_required
- boundary status: blocked
- boundary status: unclear
- future ticket permission: may_request_ingestion_implementation_approval_later
- future ticket permission: may_request_provider_connector_planning_later
- future ticket permission: may_request_scoring_backtesting_planning_later
- future ticket permission: may_request_runtime_observation_planning_later
- future ticket permission: must_not_create_ingestion_now
- future ticket permission: must_not_create_connectors
- future ticket permission: must_not_create_source_fetching
- future ticket permission: must_not_create_external_api_calls
- future ticket permission: must_not_create_runtime
- future ticket permission: must_not_create_scoring
- future ticket permission: must_not_create_trading
- future ticket permission: blocked_until_human_decision
- data posture: no_fixture_files_created
- data posture: no_fixture_files_modified
- data posture: no_historical_label_data_created
- data posture: no_generated_data_created
- data posture: no_loader_expansion_created
- data posture: no_ingestion_artifacts_created
- data posture: no_runtime_data_access
- data posture: no_source_fetching
- data posture: planning_only
- non-approval category: ingestion_implementation
- non-approval category: provider_integration
- non-approval category: connectors
- non-approval category: source_fetching
- non-approval category: external_api_calls
- non-approval category: credentials_secrets_config
- non-approval category: forecast_pulls
- non-approval category: scraping_polling_streaming
- non-approval category: scheduling_queues_jobs
- non-approval category: model_scoring
- non-approval category: probability_scoring
- non-approval category: backtesting
- non-approval category: paper_simulation
- non-approval category: runtime_observation
- non-approval category: trading_order_autonomy
- non-approval category: production_behavior
- non-approval category: cplusplus_rust_runtime
- non-approval category: other_unclear
- evidence status: source_backed
- evidence status: reviewer_inferred
- evidence status: missing
- evidence status: conflicting
- evidence status: not_applicable
- label confidence: confirmed
- label confidence: unclear
- label confidence: unknown

## Acceptance criteria

- The planning document exists with canonical ID `PRD-P1-WX-STAGE2-INGESTION-PLAN-01`.
- The document references `MEG_ACTIVE_STATE`, `WEATHER_BOT_PACKET`, and the standalone MEG Weather Bot PRD.
- The document references the ingestion planning approval request, loader implementation documents, fixture closeouts, and Stage 2 skeleton closeout.
- The document states ingestion boundary planning-only scope.
- The document states ingestion implementation is not approved.
- The document states provider/API connector implementation is not approved.
- The document states source fetching is not approved.
- The document states external API calls are not approved.
- The document states credentials/secrets/config loading is not approved.
- The document states forecast pulls are not approved.
- The document states scoring/backtesting/runtime/trading/order placement/autonomy remain unapproved.
- The document states no loader expansion is created or approved.
- The document states no fixture JSON/README files are created or modified.
- The document states no historical-label data/generated data is created.
- The document includes allowed source categories, prohibited source categories, and fail-closed blocker categories.
- The machine-checkable section includes every allowed closed-set value and no unsupported assignment values.

## Later-ticket handoff

If this planning document is accepted, the recommended next ticket is an ingestion boundary planning closeout/checkpoint or active-state update after ingestion boundary planning closeout.

Do not recommend ingestion implementation, connectors, scoring, backtesting, runtime, or trading as the immediate next ticket.
