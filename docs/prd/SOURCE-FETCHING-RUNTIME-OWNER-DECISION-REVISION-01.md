# SOURCE-FETCHING-RUNTIME-OWNER-DECISION-REVISION-01 — Source Fetching Runtime Owner Decision Revision

Canonical ID: SOURCE-FETCHING-RUNTIME-OWNER-DECISION-REVISION-01

## Status and scope

This is docs/static-test-only/owner-decision-revision-only. This ticket does not modify `meg/`. This ticket does not modify meta/handoff files, including `docs/meta/MEG_ACTIVE_STATE.md`, `docs/meta/MEG_CHAT_HANDOFF.md`, and `docs/meta/domain_packets/WEATHER_BOT_PACKET.md`. This ticket records a narrow owner-decision revision only; it is not source-fetching implementation, not source-fetching implementation planning, not a provider connector, not a provider client, and not live provider/source fetching.

## Relationship to Weather Bot Phase 0A meta-refresh self-review

This ticket records an owner-decision revision after `WEATHER-BOT-PHASE0A-META-REFRESH-SELF-REVIEW-01`. The immediate predecessor artifacts are `docs/prd/WEATHER-BOT-PHASE0A-META-REFRESH-SELF-REVIEW-01.md` and `tests/core/test_weather_bot_phase0a_meta_refresh_self_review_01.py`. Weather Bot models the market settlement rule, not generic weather.

## Owner-decision revision objective

The objective is to explicitly revise the source-fetching runtime track posture from held/closed only far enough to allow a future docs/static-test-only implementation-plan ticket. This revision does not perform implementation and does not grant implementation approval.

## Previous owner decision

The previous owner decision was `hold_source_fetching_runtime_track`. Before this revision, Weather Bot Phase 0A remained held and closed for source-fetching runtime work, the source-fetching runtime track was closed/held, source fetching remained not implemented, implementation approval remained not granted, and Stage 2 runtime metadata scaffolds remained supplied-metadata-only and fail-closed.

## Revised owner decision

Revised owner decision: approve_narrow_source_fetching_runtime_implementation_plan

This revised owner decision only unlocks a future docs/static-test-only implementation-plan ticket. It does not implement source fetching. It does not approve source-fetching implementation. It does not approve provider connectors, provider clients, live provider/source fetching, forecast pulls, API calls, scraping, file downloads, provider SDK usage, credentials/config loading, generated data, fixture changes, scoring, backtesting, trading, order placement, autonomy, production, reports, persistence, or export.

## Revision rationale

The revision rationale is limited to:

- `weather_bot_phase0a_meta_refresh_self_review_complete`
- `source_fetching_track_previously_closed_held`
- `owner_explicitly_revises_decision`
- `implementation_plan_needed_before_any_runtime_work`
- `narrow_planning_only_unlock_selected`
- `source_fetching_implementation_still_blocked`
- `provider_execution_still_blocked`
- `trading_autonomy_production_still_blocked`

## Scope unlocked by this revision

Only the following planning-only scope is unlocked by this revision:

- `source_fetching_runtime_implementation_plan_ticket`
- `docs_static_test_only_implementation_planning`
- `provider_source_boundary_planning`
- `credential_config_boundary_planning`
- `generated_data_fixture_boundary_planning`
- `scoring_backtesting_boundary_planning`
- `audit_output_boundary_planning`
- `acceptance_criteria_planning`

## Scope still blocked by this revision

The following scope remains blocked by this revision:

- `source_fetching_implementation`
- `provider_connector_implementation`
- `provider_client_creation`
- `live_provider_source_fetching`
- `forecast_pull_execution`
- `api_call_execution`
- `scraping_execution`
- `file_download_execution`
- `provider_sdk_execution`
- `credentials_config_loading`
- `generated_data_creation`
- `fixture_data_modification`
- `scoring_implementation`
- `backtesting_implementation`
- `runtime_trading_behavior`
- `order_placement`
- `autonomy_behavior`
- `production_behavior`
- `audit_report_generation`
- `audit_output_persistence`
- `external_export_behavior`

## Non-approval boundary

This owner-decision revision is not implementation approval. Silence, continuation, lack of objection, and non-interference are not approval. The next ticket must still be a docs/static-test-only implementation plan, not implementation.

## Source fetching implementation boundary

Source fetching remains not implemented. Implementation remains not performed. Source-fetching implementation remains not approved. This revision does not create source-fetching modules and does not perform source-fetching runtime work.

## Provider/source execution boundary

Provider connectors remain not created and not approved. Provider clients remain not created. Live provider/source fetching remains not executed and not approved. Forecast pulls, API calls, scraping, file downloads, and provider SDK usage remain not approved and not performed.

## Credential/config boundary

Credentials/config loading remains not approved. This ticket does not modify `.env`, secrets, credentials, config, or config-loading behavior.

## Generated-data and fixture boundary

Generated data and fixtures remain not approved. This ticket does not create generated data and does not modify `tests/fixtures/`.

## Scoring/backtesting boundary

Scoring/backtesting remains not approved. This ticket does not add scoring logic, backtesting logic, labels, generated datasets, calibration, or evaluation behavior.

## Trading/autonomy/production boundary

Runtime trading/order placement/autonomy/production remains not approved. This ticket does not add runtime trading behavior, order placement, autonomous execution, production execution, scheduling, queues, jobs, or other production behavior.

## Audit report and export boundary

Report writing, audit output persistence, and external export remain not approved. This ticket does not create audit reports, persisted audit output, export files, external export behavior, generated audit output, or file-writing behavior.

## Canonical identifier posture

The canonical identifier contract remains preserved:

- `condition_id`
- `token_id`
- `outcome`

No routing on `market_id` is introduced or approved.

## Stage 2 runtime metadata posture

Stage 2 runtime metadata scaffolds remain supplied-metadata-only and fail-closed. The landed Stage 2 runtime metadata artifact paths remain:

- `meg/weather/stage2/source_identity_runtime.py`
- `meg/weather/stage2/retrieval_context_runtime.py`
- `meg/weather/stage2/provider_source_family_runtime.py`
- `meg/weather/stage2/manual_review_gate_runtime.py`
- `meg/weather/stage2/no_lookahead_metadata_runtime.py`
- `meg/weather/stage2/fail_closed_validation_runtime.py`
- `meg/weather/stage2/static_audit_surface_runtime.py`

## Recommended next ticket

Recommended next ticket: `source_fetching_runtime_owner_decision_revision_self_review`.

This next ticket should be the secondary self-review prompt/pass for this owner-decision revision PR. It must be docs/static-test-only self-review and not implementation. It must not implement source fetching.

## Machine-checkable source-fetching runtime owner-decision revision assignments

- weather bot planning stage: source_fetching_runtime_owner_decision_revision
- owner decision revision status: docs_static_test_only
- owner decision revision status: owner_decision_revision_only
- owner decision revision status: post_weather_bot_phase0a_meta_refresh_self_review
- previous owner decision: hold_source_fetching_runtime_track
- revised owner decision: approve_narrow_source_fetching_runtime_implementation_plan
- revision rationale: weather_bot_phase0a_meta_refresh_self_review_complete
- revision rationale: source_fetching_track_previously_closed_held
- revision rationale: owner_explicitly_revises_decision
- revision rationale: implementation_plan_needed_before_any_runtime_work
- revision rationale: narrow_planning_only_unlock_selected
- revision rationale: source_fetching_implementation_still_blocked
- revision rationale: provider_execution_still_blocked
- revision rationale: trading_autonomy_production_still_blocked
- unlocked scope: source_fetching_runtime_implementation_plan_ticket
- unlocked scope: docs_static_test_only_implementation_planning
- unlocked scope: provider_source_boundary_planning
- unlocked scope: credential_config_boundary_planning
- unlocked scope: generated_data_fixture_boundary_planning
- unlocked scope: scoring_backtesting_boundary_planning
- unlocked scope: audit_output_boundary_planning
- unlocked scope: acceptance_criteria_planning
- blocked scope: source_fetching_implementation
- blocked scope: provider_connector_implementation
- blocked scope: provider_client_creation
- blocked scope: live_provider_source_fetching
- blocked scope: forecast_pull_execution
- blocked scope: api_call_execution
- blocked scope: scraping_execution
- blocked scope: file_download_execution
- blocked scope: provider_sdk_execution
- blocked scope: credentials_config_loading
- blocked scope: generated_data_creation
- blocked scope: fixture_data_modification
- blocked scope: scoring_implementation
- blocked scope: backtesting_implementation
- blocked scope: runtime_trading_behavior
- blocked scope: order_placement
- blocked scope: autonomy_behavior
- blocked scope: production_behavior
- blocked scope: audit_report_generation
- blocked scope: audit_output_persistence
- blocked scope: external_export_behavior
- stage2 runtime metadata artifact: source_identity_runtime_py
- stage2 runtime metadata artifact: retrieval_context_runtime_py
- stage2 runtime metadata artifact: provider_source_family_runtime_py
- stage2 runtime metadata artifact: manual_review_gate_runtime_py
- stage2 runtime metadata artifact: no_lookahead_metadata_runtime_py
- stage2 runtime metadata artifact: fail_closed_validation_runtime_py
- stage2 runtime metadata artifact: static_audit_surface_runtime_py
- implementation posture: docs_static_test_only
- implementation posture: owner_decision_revision_only
- implementation posture: no_runtime_code_change
- implementation posture: no_source_fetching
- implementation posture: no_source_fetching_implementation
- implementation posture: no_provider_connector
- implementation posture: no_provider_client
- implementation posture: no_live_provider_fetching
- implementation posture: no_credential_config_loading
- implementation posture: no_generated_data
- implementation posture: no_fixture_change
- implementation posture: no_scoring_backtesting
- implementation posture: no_trading_autonomy_production
- implementation posture: no_report_writing
- implementation posture: no_external_export
- implementation posture: no_persistence
- recommended next track: source_fetching_runtime_owner_decision_revision_self_review
- conditional next track: source_fetching_runtime_owner_decision_revision_if_scope_too_broad
- evidence status: owner_decision_revision_recorded
- label confidence: confirmed

## Acceptance criteria

- The document exists with the required title and canonical ID.
- The document records the previous owner decision as `hold_source_fetching_runtime_track`.
- The document records the revised owner decision exactly as `approve_narrow_source_fetching_runtime_implementation_plan`.
- The revision only unlocks a future docs/static-test-only implementation-plan ticket.
- Source-fetching implementation, provider connectors, provider clients, live provider/source fetching, forecast pulls, API calls, scraping, file downloads, provider SDK usage, credentials/config loading, generated data, fixture changes, scoring, backtesting, trading, order placement, autonomy, production, reports, persistence, and export remain blocked.
- The Stage 2 runtime metadata posture remains supplied-metadata-only and fail-closed.
- The canonical identifier contract remains `condition_id`, `token_id`, and `outcome`; no legacy-market routing is introduced or approved.
- Static tests validate this docs/static-test-only owner-decision revision posture.
