# PRD-P1-WX-STAGE2-REAL-INGESTION-PLAN-01 — Real Ingestion Boundary Planning

Canonical ID: PRD-P1-WX-STAGE2-REAL-INGESTION-PLAN-01

## Status and scope

This is real ingestion boundary planning only for the MEG Weather Bot Stage 2 track. Real ingestion implementation is not approved, no ingestion code is created, and no static ingestion boundary skeleton expansion is created or approved.

This planning PRD is governed by the standalone MEG Weather Bot PRD at `docs/prd/PRD-P1-WX-STANDALONE_WEATHER_BOT_PRD.md`, `docs/meta/MEG_ACTIVE_STATE.md` / `MEG_ACTIVE_STATE`, and `docs/meta/domain_packets/WEATHER_BOT_PACKET.md` / `WEATHER_BOT_PACKET`.

## Strategic framing

Weather Bot evidence must remain source-defined, venue-aware, point-in-time, and human-gated before any future real source intake is requested. Current fixture, loading, loader, ingestion planning, static ingestion skeleton, and closeout documents do not imply real ingestion readiness, provider readiness, source readiness, scoring readiness, runtime readiness, production readiness, or trading readiness.

## Stage ladder position

This document follows `PRD-P1-WX-STAGE2-REAL-INGESTION-PLANNING-APPROVAL-01`, `PRD-P1-WX-STAGE2-INGESTION-IMPLEMENTATION-CLOSEOUT-01`, `PRD-P1-WX-STAGE2-INGESTION-IMPLEMENTATION-01`, and `PRD-P1-WX-STAGE2-INGESTION-PLAN-CLOSEOUT-01`. It records planning vocabulary for a possible later approval chain without changing Stage 2 behavior.

## Human approval basis

The current human approval basis permits real ingestion boundary planning only. Future real ingestion implementation requires a later separate approval chain, future provider/API connector implementation requires a later separate approval chain, and future source fetching requires a later separate approval chain.

## Planning-only boundary

This planning document creates no source-fetching path, no provider/API connector implementation, no external API calls, no credentials/secrets/config loading, no forecast pulls, and no scraping, polling, streaming, scheduling, queues, jobs, or background tasks. Scoring/backtesting/runtime/trading/order-placement/autonomy remain unapproved.

The document does not define concrete implementation details: no function signatures, no classes, no modules, no CLI commands, no scripts, no configs, no DB schemas, no APIs, no connector interfaces, no runtime workflows, no job schedules, no queue names, no provider-specific client behavior, and no file formats beyond planning vocabulary.

## Real ingestion boundary vocabulary

Real ingestion boundary vocabulary is the planning-only language used to describe future movement from static evidence artifacts toward source intake. It marks the point where future work would need explicit approval before any source is contacted, retrieved, transformed, cached, or used.

## Source-intake boundary vocabulary

Source-intake boundary vocabulary separates human-reviewed planning statements from any future source intake. The boundary applies before first retrieval, before any access method is selected, and before any source material is treated as usable Weather Bot evidence.

## Provider/source category taxonomy

Provider/source category taxonomy is planning-only. It may label future source categories such as official resolution sources, venue rule sources, weather station sources, market metadata sources, forecast provider sources, exchange market sources, manual research notes, and human-reviewed fixture sources. These labels do not approve provider integration or source use.

## Allowed future source-intake modes

Allowed future source-intake modes are only planning labels. Human-reviewed manual entry and offline static descriptors may be discussed as controlled planning patterns. Future provider connectors, future source fetches, and future manual uploads require later approval before use.

## Prohibited source-intake modes

Prohibited source-intake modes include unauthenticated runtime scrape, private credentials without approval, live market feed without approval, unreviewed bulk dataset, unattributed social post, unverified AI summary, and unknown source. These modes are not acceptable as actual source intake under this planning PRD.

## Pre-fetch human approval gates

A future ticket must obtain human approval before any source is fetched, before any provider access is attempted, before credentials/secrets/config loading is introduced, before any forecast pull is attempted, and before any source material is used outside human-reviewed planning.

## Source identity and provenance requirements

Future source-intake planning must require source identity and source provenance before use. Source identity should identify what the source is in planning terms, and source provenance should identify why the source is relevant to venue-defined Weather Bot evidence. Missing source identity or provenance is fail-closed.

## Access-date and retrieval-context requirements

Future source-intake planning must require access-date and retrieval-context evidence before use. Retrieval context should describe how the source was obtained in human-reviewable terms without defining an implementation method. Missing access-date or retrieval context is fail-closed.

## No-lookahead safeguards

No-lookahead safeguards require future source evidence to distinguish event time, source publication timing, availability timing, and any later revision posture before use. If a source could leak future knowledge into an earlier decision window, the source must be blocked pending human review.

## Static-descriptor-to-real-ingestion separation

Static descriptors are planning artifacts and are not real ingestion artifacts. A static descriptor must not be treated as proof that source fetching is approved or that a provider/source connector implementation is approved.

## Static-loader-to-real-ingestion separation

The existing static loader boundary remains separate from real ingestion. No loader expansion is created or approved, and no fixture JSON files are read by new source/runtime code.

## Static-skeleton-to-real-ingestion separation

The static ingestion skeleton remains a non-source-fetching skeleton. No static ingestion boundary skeleton expansion is created or approved by this planning PRD.

## Fail-closed real-ingestion blocker taxonomy

Future planning must fail closed for missing source identity, missing access-date, missing retrieval context, missing source provenance, missing venue rule, missing resolver source, unsupported source category, unsupported access mode, prohibited access mode, private credentials requirement, source conflict, provider conflict, time-window conflict, fixture/real-ingestion confusion, static-loader/real-ingestion confusion, static-skeleton/real-ingestion confusion, runtime drift, connector drift, scoring drift, trading drift, or other unclear blockers.

## Provider connector handoff rules

Provider connector handoff rules are planning-only. Provider/API connector implementation is not approved, and any future connector planning or implementation must receive separate human approval before work begins.

## Source-fetching handoff rules

Source-fetching handoff rules are planning-only. Source fetching is not approved, external API calls are not approved, and any future source fetching requires a later separate approval chain before work begins.

## Scoring/backtesting handoff rules

Future scoring/backtesting requires separate explicit approval. This PRD does not approve model scoring, probability scoring, backtesting, paper-simulation behavior, or any evaluation workflow.

## Runtime/trading handoff rules

Future runtime/trading requires separate explicit approval. This PRD does not approve runtime observation, trading, order-placement behavior, autonomy, production behavior, or C++/Rust runtime components.

## What this planning document confirms

This planning document confirms a vocabulary-only, docs/static-test-only boundary for later real ingestion discussions. It confirms that no ingestion code is created, no provider/API connector implementation is approved, no source fetching is approved, no external API calls are approved, forecast pulls are not approved, and credentials/secrets/config loading is not approved.

## What remains unbuilt

Real ingestion remains unbuilt. Provider/API connectors remain unbuilt. Source fetching remains unbuilt. External access, credentials/secrets/config loading, forecast pulls, scraping, polling, streaming, scheduling, queues, jobs, background tasks, scoring, backtesting, paper-simulation behavior, runtime observation, trading, order-placement behavior, autonomy, production behavior, and C++/Rust runtime components remain unbuilt.

## Explicit non-approval boundaries

This PRD explicitly does not approve real ingestion implementation, provider integration, connectors, source fetching, external API calls, credentials/secrets/config loading, forecast pulls, scraping/polling/streaming, scheduling/queues/jobs, model scoring, probability scoring, backtesting, paper-simulation behavior, runtime observation, trading/order-placement/autonomy, production behavior, or C++/Rust runtime components.

## Future gates

Future real ingestion implementation requires a later separate approval chain. Future provider/API connector implementation requires a later separate approval chain. Future source fetching requires a later separate approval chain. Future scoring/backtesting requires separate explicit approval. Future runtime/trading requires separate explicit approval.

## Closed real ingestion boundary planning vocabulary

The machine-checkable section below is the only actual assignment source for closed values. Prose may describe planning concepts, but closed-set enforcement must use the dedicated assignment section only.

## Forbidden real ingestion boundary planning values

Forbidden examples that must not be parsed as actual assignments:

- planning_prepared/implementation_not_approved
- preserved/not_approved
- source_backed/reviewer_inferred
- confirmed/unclear
- partial
- mixed
- likely_confirmed
- maybe
- approved
- configured
- available
- real_ingestion_ready
- ingestion_ready
- connector_ready
- provider_ready
- source_ready
- scoring_ready
- runtime_ready
- trading_ready
- production_ready
- model_ready
- backtest_ready
- ready_for_ingestion
- ready_for_connectors
- ready_for_source_fetching
- ready_for_scoring
- ready_for_runtime
- ready_for_trading
- approved_for_real_ingestion
- approved_for_ingestion
- approved_for_connectors
- approved_for_source_fetching
- approved_for_runtime
- approved_for_scoring
- approved_for_trading
- trade_ready
- auto_execute
- autonomous
- live
- production

## Machine-checkable real ingestion boundary planning assignments

- real ingestion planning stage: stage_2_real_ingestion_boundary_planning
- planning status: planning_prepared
- planning status: implementation_not_approved
- planning status: source_fetching_not_approved
- planning status: human_review_required
- planning status: blocked_pending_fix
- planning status: unclear
- planned boundary category: real_ingestion_boundary_vocabulary
- planned boundary category: source_intake_boundary_vocabulary
- planned boundary category: provider_source_category_taxonomy
- planned boundary category: allowed_source_intake_mode
- planned boundary category: prohibited_source_intake_mode
- planned boundary category: pre_fetch_human_approval_gate
- planned boundary category: source_identity_requirement
- planned boundary category: source_provenance_requirement
- planned boundary category: access_date_requirement
- planned boundary category: retrieval_context_requirement
- planned boundary category: no_lookahead_requirement
- planned boundary category: static_descriptor_real_ingestion_separation
- planned boundary category: static_loader_real_ingestion_separation
- planned boundary category: static_skeleton_real_ingestion_separation
- planned boundary category: fail_closed_real_ingestion_blocker_taxonomy
- planned boundary category: provider_connector_handoff
- planned boundary category: source_fetching_handoff
- planned boundary category: scoring_backtesting_handoff
- planned boundary category: runtime_trading_handoff
- provider/source category: official_resolution_source
- provider/source category: venue_rule_source
- provider/source category: weather_station_source
- provider/source category: market_metadata_source
- provider/source category: forecast_provider_source
- provider/source category: exchange_market_source
- provider/source category: manual_research_note
- provider/source category: human_reviewed_fixture_source
- provider/source category: not_applicable
- allowed source-intake mode: human_reviewed_manual_entry
- allowed source-intake mode: offline_static_descriptor
- allowed source-intake mode: future_provider_connector_after_approval
- allowed source-intake mode: future_source_fetch_after_approval
- allowed source-intake mode: future_manual_upload_after_approval
- allowed source-intake mode: not_applicable
- prohibited source-intake mode: unauthenticated_runtime_scrape
- prohibited source-intake mode: private_credentials_without_approval
- prohibited source-intake mode: live_market_feed_without_approval
- prohibited source-intake mode: unreviewed_bulk_dataset
- prohibited source-intake mode: unattributed_social_post
- prohibited source-intake mode: unverified_ai_summary
- prohibited source-intake mode: unknown_source
- prohibited source-intake mode: not_applicable
- planned blocker category: missing_source_identity
- planned blocker category: missing_access_date
- planned blocker category: missing_retrieval_context
- planned blocker category: missing_source_provenance
- planned blocker category: missing_venue_rule
- planned blocker category: missing_resolver_source
- planned blocker category: unsupported_source_category
- planned blocker category: unsupported_access_mode
- planned blocker category: prohibited_access_mode
- planned blocker category: private_credentials_required
- planned blocker category: source_conflict
- planned blocker category: provider_conflict
- planned blocker category: time_window_conflict
- planned blocker category: fixture_real_ingestion_confusion
- planned blocker category: static_loader_real_ingestion_confusion
- planned blocker category: static_skeleton_real_ingestion_confusion
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
- future ticket permission: may_request_real_ingestion_implementation_approval_later
- future ticket permission: may_request_provider_connector_planning_later
- future ticket permission: may_request_source_fetching_planning_later
- future ticket permission: may_request_scoring_backtesting_planning_later
- future ticket permission: may_request_runtime_observation_planning_later
- future ticket permission: must_not_create_real_ingestion_now
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
- data posture: no_static_ingestion_skeleton_expansion_created
- data posture: no_real_ingestion_artifacts_created
- data posture: no_runtime_data_access
- data posture: no_source_fetching
- data posture: planning_only
- non-approval category: real_ingestion_implementation
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

- The planning PRD exists and includes the canonical ID.
- The planning PRD references the standalone MEG Weather Bot PRD, `MEG_ACTIVE_STATE`, `WEATHER_BOT_PACKET`, and the controlling predecessor Stage 2 documents.
- The PRD states real ingestion boundary planning-only scope.
- The PRD states real ingestion implementation is not approved.
- The PRD states no ingestion code is created.
- The PRD states no fixture JSON files are created or modified.
- The PRD states no fixture README files are created or modified.
- The PRD states no fixture JSON/README files are created or modified.
- The PRD states no historical-label data files are created.
- The PRD states no generated data is created.
- Static tests parse actual closed-set values only from the machine-checkable section.

## Later-ticket handoff

The recommended next ticket after clean validation is a real ingestion boundary planning closeout/checkpoint. Do not use this handoff to recommend real ingestion implementation, connectors, source fetching, scoring, backtesting, runtime, or trading.
