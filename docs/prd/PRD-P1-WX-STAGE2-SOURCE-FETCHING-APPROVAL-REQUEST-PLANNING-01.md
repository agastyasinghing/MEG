# PRD-P1-WX-STAGE2-SOURCE-FETCHING-APPROVAL-REQUEST-PLANNING-01 — Source-Fetching Approval Request Planning

Canonical ID: PRD-P1-WX-STAGE2-SOURCE-FETCHING-APPROVAL-REQUEST-PLANNING-01

## Status and scope

This is planning only. This is docs/static-test-only. This defines what a future approval request must contain. This is not the approval request itself.

This artifact prepares the structure, evidence expectations, source identity/provenance requirements, access-date/no-lookahead controls, and safety gates for possible later Weather Bot Stage 2 source-fetching work. It does not grant permission to implement, run, fetch, connect, score, backtest, trade, or operate anything.

No provider connector is implemented. No provider connector is approved. No source fetching is implemented. No source fetching is approved. No forecast pull is implemented. No forecast pull is approved. No API call is implemented. No API call is approved. No scraping is implemented. No scraping is approved. No credentials/secrets/config loading is implemented. No credentials/secrets/config loading is approved. No scoring is implemented or approved. No backtesting is implemented or approved. No runtime behavior is implemented or approved. No trading is implemented or approved. No autonomy is implemented or approved. No production behavior is implemented or approved. No generated data is created. No fixture data is modified. No workflow or dependency change is approved. No DB migration or schema change is approved. No source-code migration is implemented or approved. No compatibility shim is implemented or approved.

Any later source-fetching implementation requires a separate explicit approval request. Any later provider connector implementation requires a separate explicit approval request. Any later scoring/backtesting/runtime/trading/autonomy/production work requires a separate explicit approval request.

## Relationship to provider/source compatibility closeout

This planning artifact follows and depends on PRD-P1-WX-STAGE2-PROVIDER-SOURCE-COMPATIBILITY-CLOSEOUT-01 as the provider/source compatibility closeout checkpoint. The closeout posture remains controlling: provider connectors, source fetching, forecast pulls, API calls, scraping, credentials/secrets/config loading, scoring, backtesting, runtime behavior, trading, autonomy, production behavior, generated data, fixture changes, workflows, dependencies, DB migrations, schema changes, source-code migrations, and compatibility shims remain unapproved.

It also references PRD-P1-WX-STAGE2-PROVIDER-SOURCE-COMPATIBILITY-PLANNING-01 for the source-family taxonomy and compatibility boundaries; PRD-P1-WX-STAGE2-WEATHER-BOT-RETURN-TO-PLANNING-01 for the Weather Bot return checkpoint after architecture alignment; and MEG-ARCH-ALIGN-08 for the architecture alignment closeout posture.

## Planning objective

Define the minimum required contents of a future Weather Bot Stage 2 source-fetching approval request before any source-fetching, provider connector, forecast pull, API call, scraping, credential/config loading, scoring, backtesting, runtime, trading, autonomy, production, generated-data, fixture, workflow, dependency, migration, schema, source-code migration, or compatibility-shim work can be considered.

## Future approval-request purpose

A future approval request must allow reviewers to decide whether a proposed source-fetching or provider-connector track is sufficiently described, source-backed, no-lookahead safe, operationally bounded, and testable. The future request must be explicit about what it asks to approve and what remains blocked. This artifact does not submit that future request and does not approve the future request.

## Source-fetching approval-request template

A future source-fetching approval request must include every field below. Empty, unknown, or not-applicable fields must be explicit and reviewed rather than silently omitted.

- requested_source_family: one allowed source-family value.
- requested_source_name: human-readable source name.
- requested_source_owner_or_publisher: accountable source owner, publisher, agency, platform, or reviewer group.
- requested_source_identity: stable identity string sufficient to distinguish the source from similarly named sources.
- requested_source_url_or_citation: URL, document citation, dataset citation, or manual review citation.
- requested_source_access_method: one allowed access-method value.
- requested_retrieval_mode: one allowed retrieval-mode value.
- intended_weather_market_use: intended weather-market planning use and why it is needed.
- intended_forecast_or_resolution_target: forecast horizon, observation window, or resolution target.
- required_descriptor_fields: descriptor fields needed before any later ingestion or validation step.
- required_identifier_contract: must preserve condition_id, token_id, and outcome as the canonical identifier contract and must not introduce alternate routing identifiers.
- access_date_policy: required capture of access date and source publication/effective date.
- retrieval_context_policy: required capture of retrieval context, operator context, and source version context.
- no_lookahead_control_plan: controls proving later use cannot use information unavailable at the asserted decision time.
- provenance_capture_plan: source identity, publisher, citation, access method, retrieval context, and reviewer evidence to capture.
- credential_or_config_requirement: one allowed credential/config requirement value.
- generated_data_or_fixture_plan: one allowed generated-data/fixture-plan value.
- test_scope_plan: proposed static, fixture, integration, connector, or runtime tests, with unapproved categories clearly separated.
- risk_and_failure_mode_summary: known risks, source instability, failure handling, ambiguity, rate-limit/legal/terms concerns, and fail-closed behavior.
- explicit_non_approved_behaviors: exact list of behaviors not approved by the request unless separately and explicitly authorized.

Allowed requested_retrieval_mode values:
- manual_descriptor_only
- static_fixture_reference_only
- later_source_fetching_request
- later_provider_connector_request
- prohibited_until_explicit_approval
- unknown_requires_review

Allowed requested_source_family values:
- forecast_provider_family
- historical_observation_provider_family
- official_resolution_source_family
- market_metadata_source_family
- manual_human_review_source_family
- unsupported_source_family
- unknown_source_family

Allowed requested_source_access_method values:
- manual_review
- static_reference
- api_call
- scraping
- file_download
- provider_sdk
- unknown_requires_review

Allowed credential_or_config_requirement values:
- none_required
- credentials_required_later
- config_required_later
- secrets_required_later
- unknown_requires_review

Allowed generated_data_or_fixture_plan values:
- no_generated_data
- no_fixture_change
- generated_data_requires_later_approval
- fixture_change_requires_later_approval
- unknown_requires_review

## Required source identity fields

A future request must identify source family, source name, owner or publisher, stable source identity, source URL or citation, intended source role, source authority limits, and whether the source is primary, secondary, official, derived, manual-review-only, unsupported, or unknown. Source identity must be sufficient for a reviewer to distinguish similarly named providers, endpoints, publications, files, or manual review artifacts.

## Required provenance fields

A future request must define provenance capture for source owner or publisher, source citation, source version or publication timestamp when available, reviewer/operator identity when manual review is used, descriptor creation path, access method, retrieval mode, retrieval context, source limitations, and any transformation chain proposed for later approval. Provenance must be retained as evidence, not inferred after the fact.

## Required access-date and retrieval-context fields

A future request must require an access date, source publication/effective date when available, retrieval time window, retrieval actor or system, source version marker, query parameters or file identifiers when applicable, timezone assumptions, and any caching or snapshot context. Unknown access-date or retrieval-context values must use unknown_requires_review or a stricter blocked posture in the future request.

## Required no-lookahead controls

A future request must explain how source data, forecast data, observations, official resolutions, market metadata, and manual descriptors are constrained to information available at the asserted decision or labeling time. Required controls include source publication-time evidence, access-date evidence, retrieval-context evidence, separation between forecast and resolution material, reviewer checks for post-event information, and fail-closed handling when timing evidence is missing or conflicting.

## Required provider/source compatibility references

A future request must reference PRD-P1-WX-STAGE2-PROVIDER-SOURCE-COMPATIBILITY-CLOSEOUT-01 and PRD-P1-WX-STAGE2-PROVIDER-SOURCE-COMPATIBILITY-PLANNING-01. It must map the requested source family, access method, retrieval mode, credential/config posture, generated-data/fixture posture, and prohibited behaviors back to those compatibility boundaries before any later approval can be evaluated.

## Required offline-ingestion boundary references

A future request must reference the existing Stage 2 offline ingestion boundary posture: static, human-reviewed descriptors and static fixture references are separate from real source fetching, provider connectors, forecast pulls, API calls, scraping, credentials/secrets/config loading, generated data, fixture changes, workflows, dependencies, DB migrations, schema changes, source-code migrations, compatibility shims, scoring, backtesting, runtime behavior, trading, autonomy, and production behavior. Any transition from offline descriptor planning into actual fetching requires a separate explicit approval request.

## Required risk and failure-mode analysis

A future request must summarize source authority risk, provider instability, endpoint or citation ambiguity, terms/licensing constraints, rate limits, authentication or configuration requirements, stale data, delayed publication, missing timestamps, conflicting source values, no-lookahead failure modes, provenance gaps, reviewer error, fixture contamination risk, generated-data risk, workflow/dependency risk, migration/schema risk, and fail-closed behavior. Risks must not be converted into approval by being listed.

## Required test-scope proposal

A future request must propose test scope by category and approval posture. Static documentation tests may validate templates and closed sets. Any connector, source-fetching, forecast-pull, API-call, scraping, credentials/secrets/config loading, generated-data, fixture-change, workflow, dependency, DB migration, schema-change, source-code migration, compatibility-shim, scoring, backtesting, runtime, trading, autonomy, or production test must be explicitly deferred until a separate approval request grants that scope.

## Explicit non-approval boundaries

The explicit non-approved behaviors list is:

- provider_connector
- source_fetching
- forecast_pull
- api_call
- scraping
- credentials_secrets_config
- scoring_backtesting
- runtime_behavior
- trading_autonomy
- production_behavior
- generated_data
- fixture_change
- workflow_change
- dependency_change
- database_migration
- schema_change

These behaviors are not approved or implemented by this planning artifact.

## Blocked implementation work

Blocked work includes provider connectors, source fetching, forecast pulls, API calls, scraping, credentials/secrets/config loading, scoring, backtesting, runtime behavior, execution, trading, autonomy, production behavior, generated data, fixture changes, workflows, dependencies, DB migrations, schema changes, source-code migrations, compatibility shims, and changes to runtime/source/provider/scoring/database modules. A future approval request may ask to unblock a narrow scope, but that future request must be separate and explicit.

## Recommended next ticket

Recommended next ticket: PRD-P1-WX-STAGE2-SOURCE-FETCHING-APPROVAL-REQUEST-CLOSEOUT-01 or PRD-P1-WX-STAGE2-SOURCE-FETCHING-APPROVAL-REQUEST-DRAFT-PLANNING-01. Neither recommendation approves provider connector implementation, source fetching implementation, forecast pulls, scoring, backtesting, runtime behavior, trading, autonomy, or production behavior.

## Machine-checkable source-fetching approval-request planning assignments

- weather bot planning stage: source_fetching_approval_request_planning
- approval request posture: template_defined
- approval request posture: approval_request_not_submitted
- approval request posture: approval_not_granted
- approval request posture: implementation_not_approved
- approval request posture: later_explicit_approval_required
- provider source posture: provider_connectors_not_approved
- provider source posture: source_fetching_not_approved
- provider source posture: forecast_pulls_not_approved
- provider source posture: api_calls_not_approved
- provider source posture: scraping_not_approved
- provider source posture: provider_source_planning_only
- requested retrieval mode: manual_descriptor_only
- requested retrieval mode: static_fixture_reference_only
- requested retrieval mode: later_source_fetching_request
- requested retrieval mode: later_provider_connector_request
- requested retrieval mode: prohibited_until_explicit_approval
- requested retrieval mode: unknown_requires_review
- requested source family: forecast_provider_family
- requested source family: historical_observation_provider_family
- requested source family: official_resolution_source_family
- requested source family: market_metadata_source_family
- requested source family: manual_human_review_source_family
- requested source family: unsupported_source_family
- requested source family: unknown_source_family
- requested source access method: manual_review
- requested source access method: static_reference
- requested source access method: api_call
- requested source access method: scraping
- requested source access method: file_download
- requested source access method: provider_sdk
- requested source access method: unknown_requires_review
- credential config posture: no_credentials_config_loading
- credential config posture: credentials_required_later
- credential config posture: config_required_later
- credential config posture: secrets_required_later
- credential config posture: credentials_config_approval_required
- credential config posture: unknown_requires_review
- generated data fixture posture: no_generated_data
- generated data fixture posture: no_fixture_change
- generated data fixture posture: generated_data_requires_later_approval
- generated data fixture posture: fixture_change_requires_later_approval
- generated data fixture posture: unknown_requires_review
- implementation posture: planning_only
- implementation posture: docs_static_test_only
- implementation posture: no_provider_connector
- implementation posture: no_source_fetching
- implementation posture: no_forecast_pull
- implementation posture: no_api_call
- implementation posture: no_scraping
- implementation posture: no_credentials_config_loading
- implementation posture: no_scoring_backtesting
- implementation posture: no_runtime_behavior
- implementation posture: no_trading_autonomy
- implementation posture: no_production_behavior
- implementation posture: no_generated_data
- implementation posture: no_fixture_change
- implementation posture: no_workflow_change
- implementation posture: no_dependency_change
- implementation posture: no_database_migration
- implementation posture: no_schema_change
- recommended next track: source_fetching_approval_request_closeout
- recommended next track: source_fetching_approval_request_draft_planning
- recommended next track: forecast_resolution_source_mapping_planning
- recommended next track: scoring_backtesting_approval_request_planning
- recommended next track: stage2_active_state_refresh
- evidence status: source_backed
- evidence status: reviewer_inferred
- evidence status: missing
- evidence status: conflicting
- evidence status: not_applicable
- label confidence: confirmed
- label confidence: unclear
- label confidence: unknown

## Acceptance criteria

- The canonical ID appears in this document.
- All required sections are present.
- The document states planning-only and docs/static-test-only scope.
- The document defines what a future approval request must contain.
- The document states this is not the approval request itself.
- The future approval-request template includes all required fields and closed-set values.
- Required source identity, provenance, access-date, retrieval-context, no-lookahead, provider/source compatibility, offline-ingestion boundary, risk, and test-scope expectations are present.
- The explicit non-approved behaviors list is present.
- The machine-checkable assignments use only exact allowed values.
- The recommended next ticket does not approve implementation.
