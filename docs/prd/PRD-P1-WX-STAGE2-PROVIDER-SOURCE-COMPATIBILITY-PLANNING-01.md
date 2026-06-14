# PRD-P1-WX-STAGE2-PROVIDER-SOURCE-COMPATIBILITY-PLANNING-01 — Provider/Source Compatibility Planning

Canonical ID: PRD-P1-WX-STAGE2-PROVIDER-SOURCE-COMPATIBILITY-PLANNING-01

## Status and scope

This artifact is planning only and docs/static-test-only. It evaluates provider/source compatibility only as a planning artifact for Weather Bot Stage 2.

No provider connector is implemented. No provider connector is approved. No source fetching is implemented. No source fetching is approved. No forecast pull is implemented. No forecast pull is approved. No API call is implemented. No API call is approved. No scraping is implemented. No scraping is approved. No credentials/secrets/config loading is implemented. No credentials/secrets/config loading is approved. No scoring is implemented or approved. No backtesting is implemented or approved. No runtime behavior is implemented or approved. No trading is implemented or approved. No autonomy is implemented or approved. No production behavior is implemented or approved. No generated data is created. No fixture data is modified.

## Relationship to Weather Bot return-to-planning checkpoint

This planning document follows PRD-P1-WX-STAGE2-WEATHER-BOT-RETURN-TO-PLANNING-01, which returned Weather Bot to gated planning/approval work after MEG-ARCH-ALIGN-08. The return checkpoint recorded that architecture alignment was complete enough to resume Weather Bot planning, while provider connectors, source fetching, forecast pulls, scoring, backtesting, runtime behavior, trading, autonomy, and production behavior remained unapproved.

## Planning objective

The objective is to classify weather data providers, resolution sources, forecast sources, historical observation sources, market metadata sources, and manual review source families by whether they may be compatible with the existing offline Weather Bot posture. This document does not select or approve a provider, source, connector, retrieval method, credential path, scoring method, backtest, runtime path, trading path, autonomous behavior, or production behavior.

## Provider/source compatibility taxonomy

The source-family categories are:

- forecast_provider_family
- historical_observation_provider_family
- official_resolution_source_family
- market_metadata_source_family
- manual_human_review_source_family
- unsupported_source_family
- unknown_source_family

These categories are planning labels only. They do not authorize implementation, fetching, API calls, scraping, credential loading, scoring, backtesting, runtime behavior, trading, autonomy, or production behavior.

## Forecast source families

Forecast source families include provider classes that could later describe predicted weather outcomes, forecast issuance time, forecast target time, model run time, forecast horizon, geography, station or grid identity, and units. In the current posture, a forecast source family can be compatible only as a human-reviewed descriptor or as a static fixture reference when already authorized by a separate ticket. Any later forecast pull requires a separate explicit approval request.

## Historical observation source families

Historical observation source families include provider classes that could later describe observed weather outcomes, observation time, source station or grid, measurement units, quality flags, and source revision context. In the current posture, historical observation source families are planning-only unless represented by already-approved static fixture references. Any later source fetching or provider connector work requires a separate explicit approval request.

## Market-resolution source families

Market-resolution source families include official resolution source families and market metadata source families that could later describe the market question, condition reference, token reference, outcome wording, final resolution text, and source-provided close or settlement context. They are compatible only as human-reviewed descriptors in this planning artifact. Automated retrieval, scraping, API calls, and connector behavior remain prohibited until explicit approval.

Official resolution source families are limited to planning descriptors for the authoritative source or venue that would later be used to verify a final market outcome. They do not approve fetching the official source, scraping market pages, calling market APIs, resolving markets programmatically, or adding runtime resolution behavior.

## Human-reviewed descriptor compatibility

Manual human review source families are compatible as descriptor-only planning inputs when a reviewer manually records source identity, access date, retrieval context, intended use, and risk notes without adding fetching code or runtime behavior. This does not approve provider connectors, source fetching, forecast pulls, API calls, scraping, credential loading, scoring, backtesting, runtime behavior, trading, autonomy, or production behavior.

## Offline real-ingestion compatibility

Compatibility with the existing offline real-ingestion posture means the source family can be described without executing retrieval. Offline compatibility is limited to already-human-reviewed descriptors and approved static fixture references. It does not expand loaders, create generated data, alter fixture data, add workflows, add dependencies, add database migrations, add schema changes, or create compatibility shims.

## Source identity and provenance requirements

Future source descriptors should record source family, example source type, source owner or publisher if known, source identity, source URL or citation when manually reviewed, target geography, target event or market relationship, descriptor author, review date, and confidence. For market references, descriptor planning must preserve the canonical identifier contract: condition_id, token_id, and outcome; it must not route on market_id.

## Access-date and retrieval-context requirements

Any future descriptor or approval request should state access date, retrieval context, whether the information was manually reviewed or statically referenced, and whether the source was available before the forecast target or market resolution time. Access-date and retrieval-context fields are documentation requirements only in this artifact and do not authorize retrieval code.

## No-lookahead requirements

Future source use must preserve no-lookahead controls. Planning records should distinguish forecast issue time, observation time, market close time, resolution time, access date, and descriptor review time. A future approval request must explain how it prevents post-resolution information from affecting forecast, scoring, backtesting, runtime, or trading decisions.

## Provider/API connector boundary

No provider connector is implemented. No provider connector is approved. No API call is implemented. No API call is approved. Any later provider connector or API connector work requires a separate explicit approval request before design, code, configuration, dependency, credential, or runtime work begins.

## Source-fetching boundary

No source fetching is implemented. No source fetching is approved. No scraping is implemented. No scraping is approved. Any later source-fetching, polling, streaming, downloading, scraping, or retrieval workflow requires a separate explicit approval request.

## Forecast-pull boundary

No forecast pull is implemented. No forecast pull is approved. Forecast source families may be described for planning, but no forecast retrieval, scheduled pull, API request, cache, generated output, or fixture modification is approved here.

## Credentials/secrets/config boundary

No credentials/secrets/config loading is implemented. No credentials/secrets/config loading is approved. This artifact does not approve environment variables, secret files, config loading, credential discovery, provider keys, credential validation, or secret-management changes.

## Scoring/backtesting/runtime/trading boundary

No scoring is implemented or approved. No backtesting is implemented or approved. No runtime behavior is implemented or approved. No trading is implemented or approved. No autonomy is implemented or approved. No production behavior is implemented or approved. Any later scoring/backtesting/runtime/trading work requires a separate explicit approval request.

## Candidate compatibility matrix format

A future provider/source compatibility matrix may use this schema, but this ticket does not create provider connectors:

- source_family
- example_source_type
- intended_use
- required_descriptor_fields
- offline_compatibility_status
- approval_required_before_use
- prohibited_until_approval
- risk_notes

Allowed offline_compatibility_status values:

- compatible_as_human_reviewed_descriptor_only
- compatible_as_static_fixture_reference_only
- requires_later_source_fetching_approval
- requires_later_provider_connector_approval
- prohibited_until_explicit_approval
- unknown_requires_review

Allowed approval_required_before_use values:

- no_new_approval_for_manual_descriptor_only
- source_fetching_approval_required
- provider_connector_approval_required
- credentials_config_approval_required
- scoring_backtesting_approval_required
- runtime_trading_approval_required
- human_review_required

Allowed prohibited_until_approval values:

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
- none_for_manual_descriptor_only

## Future approval-request requirements

Any later provider connector or source-fetching work requires a separate explicit approval request. Any later forecast pull requires a separate explicit approval request. Any later API call, scraping, credential/secret/config loading, generated data, fixture modification, workflow, dependency, database migration, schema change, source-code migration, or compatibility shim requires a separate explicit approval request. Any later scoring/backtesting/runtime/trading work requires a separate explicit approval request.

A future approval request must state the source family, intended use, descriptor fields, no-lookahead controls, source identity and provenance requirements, access-date and retrieval-context requirements, explicit prohibited behavior until approval, test scope, and final non-approval boundaries.

## Recommended next ticket

Recommended next ticket: PRD-P1-WX-STAGE2-PROVIDER-SOURCE-COMPATIBILITY-CLOSEOUT-01 — Provider/Source Compatibility Planning Closeout.

A secondary planning-only option is PRD-P1-WX-STAGE2-SOURCE-FETCHING-APPROVAL-REQUEST-PLANNING-01. Neither recommendation approves provider connector implementation, source fetching implementation, forecast pulls, scoring, backtesting, runtime behavior, trading, autonomy, or production behavior.

## Machine-checkable provider/source compatibility assignments

- weather bot planning stage: provider_source_compatibility_planning
- architecture alignment status: meg_arch_align_08_complete
- architecture alignment status: weather_bot_return_checkpoint_complete
- architecture alignment status: canonical_id_posture_recorded
- architecture alignment status: market_id_compatibility_posture_recorded
- provider source posture: provider_source_planning_only
- provider source posture: provider_connectors_not_approved
- provider source posture: source_fetching_not_approved
- provider source posture: forecast_pulls_not_approved
- provider source posture: api_calls_not_approved
- provider source posture: scraping_not_approved
- source family category: forecast_provider_family
- source family category: historical_observation_provider_family
- source family category: official_resolution_source_family
- source family category: market_metadata_source_family
- source family category: manual_human_review_source_family
- source family category: unsupported_source_family
- source family category: unknown_source_family
- offline compatibility status: compatible_as_human_reviewed_descriptor_only
- offline compatibility status: compatible_as_static_fixture_reference_only
- offline compatibility status: requires_later_source_fetching_approval
- offline compatibility status: requires_later_provider_connector_approval
- offline compatibility status: prohibited_until_explicit_approval
- offline compatibility status: unknown_requires_review
- approval required before use: no_new_approval_for_manual_descriptor_only
- approval required before use: source_fetching_approval_required
- approval required before use: provider_connector_approval_required
- approval required before use: credentials_config_approval_required
- approval required before use: scoring_backtesting_approval_required
- approval required before use: runtime_trading_approval_required
- approval required before use: human_review_required
- prohibited until approval: provider_connector
- prohibited until approval: source_fetching
- prohibited until approval: forecast_pull
- prohibited until approval: api_call
- prohibited until approval: scraping
- prohibited until approval: credentials_secrets_config
- prohibited until approval: scoring_backtesting
- prohibited until approval: runtime_behavior
- prohibited until approval: trading_autonomy
- prohibited until approval: production_behavior
- prohibited until approval: none_for_manual_descriptor_only
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
- recommended next track: provider_source_compatibility_closeout
- recommended next track: source_fetching_approval_request_planning
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

- The provider/source compatibility planning artifact exists and includes the canonical ID.
- The artifact is planning only and docs/static-test-only.
- The artifact documents forecast, historical observation, official resolution, market metadata, manual human review, unsupported, and unknown source-family categories.
- The artifact defines the candidate compatibility matrix schema and allowed values.
- The artifact states that compatibility is evaluated only as a planning artifact.
- The artifact states all non-implementation and non-approval boundaries.
- The artifact states that future provider connector, source-fetching, scoring, backtesting, runtime, and trading work requires separate explicit approval requests.
- The machine-checkable section uses exact closed-set assignment values only.
- Static tests validate the document without source, runtime, connector, workflow, dependency, generated-data, fixture, or docs/meta changes.
