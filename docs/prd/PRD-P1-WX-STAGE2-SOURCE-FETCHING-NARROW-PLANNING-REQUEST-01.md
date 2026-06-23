# PRD-P1-WX-STAGE2-SOURCE-FETCHING-NARROW-PLANNING-REQUEST-01 — Narrow Source-Fetching Implementation-Planning Request

Canonical ID: PRD-P1-WX-STAGE2-SOURCE-FETCHING-NARROW-PLANNING-REQUEST-01

## Status and scope

This is a narrow source-fetching implementation-planning request only. It is docs/static-test-only and request-only. PR #250 is merged in local history as the latest completed owner-disposition predecessor. This ticket requests a later implementation-planning artifact and does not itself create that implementation-planning artifact. This ticket does not approve source-fetching implementation. This ticket does not approve provider connector implementation. This ticket does not approve forecast pulls. This ticket does not approve API calls. This ticket does not approve scraping. This ticket does not approve credentials/secrets/config loading. This ticket does not approve generated data. This ticket does not approve fixture changes. This ticket does not approve scoring. This ticket does not approve backtesting. This ticket does not approve runtime behavior. This ticket does not approve trading, order placement, autonomy, or production behavior. Actual implementation requires a later separate explicit approval.

## Relationship to owner disposition

PR #250 / PRD-P1-WX-STAGE2-SOURCE-FETCHING-APPROVAL-REQUEST-OWNER-DISPOSITION-01 is the immediate predecessor. The owner disposition selected `approve_narrow_source_fetching_planning_only`, allowing only the current permitted next track `narrow_source_fetching_planning_request`.

## Relationship to owner-disposition planning

PRD-P1-WX-STAGE2-SOURCE-FETCHING-APPROVAL-REQUEST-OWNER-DISPOSITION-PLANNING-01 planned the owner-disposition shape and closed-set options; this request follows the selected disposition without expanding it.

## Relationship to meta refresh

PRD-P1-WX-STAGE2-SOURCE-FETCHING-APPROVAL-REQUEST-META-REFRESH-01 refreshed stale handoff/meta posture; newer merged PRDs and verified PR metadata override stale handoff state.

## Relationship to hold checkpoint

PRD-P1-WX-STAGE2-SOURCE-FETCHING-APPROVAL-REQUEST-HOLD-CHECKPOINT-01 remains the hold checkpoint context. Current state posture is `hold_checkpoint` plus narrow planning request allowed by PR #250 only.

## Relationship to source-fetching approval-request draft

PRD-P1-WX-STAGE2-SOURCE-FETCHING-APPROVAL-REQUEST-DRAFT-01 and PRD-P1-WX-STAGE2-SOURCE-FETCHING-APPROVAL-REQUEST-DRAFT-CLOSEOUT-01 remain draft/closeout context only and do not approve implementation.

## Relationship to source-fetching approval-request planning sequence

This sequence includes PRD-P1-WX-STAGE2-SOURCE-FETCHING-APPROVAL-REQUEST-DRAFT-PLANNING-01, PRD-P1-WX-STAGE2-SOURCE-FETCHING-APPROVAL-REQUEST-CLOSEOUT-01, and PRD-P1-WX-STAGE2-SOURCE-FETCHING-APPROVAL-REQUEST-PLANNING-01. It stays docs/static-test-only.

## Relationship to provider/source compatibility sequence

PRD-P1-WX-STAGE2-PROVIDER-SOURCE-COMPATIBILITY-CLOSEOUT-01 and PRD-P1-WX-STAGE2-PROVIDER-SOURCE-COMPATIBILITY-PLANNING-01 provide compatibility context only; provider connector implementation is not approved.

## Relationship to Weather Bot PRD and architecture alignment

This request remains aligned with PRD-P1-WX-STAGE2-WEATHER-BOT-RETURN-TO-PLANNING-01, MEG-ARCH-ALIGN-08, and PRD-P1-WX-STANDALONE_WEATHER_BOT_PRD. Weather Bot models the market settlement rule, not generic weather.

## Narrow planning-request objective

The objective is to request a later narrow source-fetching implementation-planning artifact and define the exact constraints that later artifact must satisfy while keeping scope narrow, bounded, and non-runtime.

## Current permitted next track

The current permitted next track is `narrow_source_fetching_planning_request`. It is request-only and cannot be treated as implementation authorization.

## Requested later planning artifact

This ticket requests a later narrow source-fetching implementation-planning artifact. This ticket does not itself create that implementation-planning artifact. The later planning artifact must not implement source fetching.

## Proposed narrow planning scope

The later implementation-planning artifact may plan only:

- `source_identity_and_provenance_planning`
- `access_date_and_retrieval_context_planning`
- `no_lookahead_boundary_planning`
- `provider_source_family_selection_planning`
- `fetch_boundary_design_planning`
- `credential_config_boundary_planning`
- `generated_data_fixture_boundary_planning`
- `static_validation_audit_planning`
- `fail_closed_behavior_planning`

## Explicitly excluded scope

The following scope is explicitly excluded:

- `source_fetching_implementation`
- `provider_connector_implementation`
- `forecast_pull_execution`
- `api_call_execution`
- `scraping_execution`
- `credentials_config_loading`
- `generated_data_creation`
- `fixture_data_modification`
- `scoring_implementation`
- `backtesting_implementation`
- `runtime_behavior`
- `trading_behavior`
- `autonomy_behavior`
- `production_behavior`
- `workflow_change`
- `dependency_change`
- `database_migration`
- `schema_change`
- `source_code_migration`
- `compatibility_shim`

## Planning artifact requirements

The later artifact must remain docs/static-test-only, must plan but not implement, must include static validation and audit requirements, and must preserve manual-review-first, fail-closed, no-lookahead, and later-explicit-approval constraints.

## Source identity and provenance planning requirements

Plan manual-review-first source identity and provenance requirements only.

## Access-date and retrieval-context planning requirements

Plan access-date and retrieval-context requirements only.

## No-lookahead planning requirements

Plan no-lookahead requirements that prevent post-settlement or unavailable evidence from informing earlier labels.

## Provider/source family planning requirements

Plan a provider/source family selection framework using preserved closed-set values.

## Fetch-boundary planning requirements

Plan a fetch boundary design proposal only; no forecast pull execution, API call execution, scraping execution, file download, or provider SDK use is approved.

## Credential/config planning requirements

Plan credential/config handling boundaries only; credentials/secrets/config loading is not approved.

## Generated-data and fixture planning requirements

Plan generated-data and fixture prohibitions or later-approval requirements only; generated data creation and fixture data modification are not approved.

## Static validation planning requirements

Plan static validation and audit requirements only, using tests/core style static tests.

## Fail-closed planning requirements

Plan fail-closed implementation constraints only; do not implement fail-closed runtime behavior.

## Approval posture

This is a narrow implementation-planning request only. This ticket does not approve source-fetching implementation. This ticket does not approve provider connector implementation. This ticket does not approve forecast pulls. This ticket does not approve API calls. This ticket does not approve scraping. This ticket does not approve credentials/secrets/config loading. This ticket does not approve generated data. This ticket does not approve fixture changes. This ticket does not approve scoring. This ticket does not approve backtesting. This ticket does not approve runtime behavior. This ticket does not approve trading, order placement, autonomy, or production behavior. Actual implementation requires a later separate explicit approval.

## Planning-only posture

This artifact requests later planning and is not the later implementation-planning artifact. It does not implement, approve, create, recommend, or modify implementation work.

## Canonical identifier posture

The canonical identifier contract is preserved exactly: `condition_id`, `token_id`, and `outcome`. No routing on `market_id` is introduced or approved.

## Provider/source compatibility posture

Closed-set source-family values are preserved: `forecast_provider_family`, `historical_observation_provider_family`, `official_resolution_source_family`, `market_metadata_source_family`, `manual_human_review_source_family`, `unsupported_source_family`, `unknown_source_family`. Retrieval-mode, access-method, credential/config, and generated-data/fixture values are also preserved: `manual_descriptor_only`, `static_fixture_reference_only`, `later_source_fetching_request`, `later_provider_connector_request`, `prohibited_until_explicit_approval`, `unknown_requires_review`, `manual_review`, `static_reference`, `api_call`, `scraping`, `file_download`, `provider_sdk`, `none_required`, `credentials_required_later`, `config_required_later`, `secrets_required_later`, `no_generated_data`, `no_fixture_change`, `generated_data_requires_later_approval`, `fixture_change_requires_later_approval`.

## Offline-ingestion boundary posture

This request does not approve provider/source connector implementation, real ingestion implementation, live provider usage, paper simulation, or runtime observation. Offline/manual descriptor boundaries remain planning-only.

## Test-scope posture

Tests are static tests only under tests/core and do not import production Weather Bot modules. No runtime/source/provider/fixture/generated-data workflow is exercised.

## Risk and failure-mode posture

Risks include accidental scope expansion into connector work, source fetching, API calls, scraping, credential loading, generated data, fixture changes, scoring, backtesting, or runtime behavior; all must fail closed pending later separate explicit approval.

## Explicit non-approval boundaries

This narrow planning-request artifact does not implement, approve, create, recommend, or modify: provider connectors; source fetching implementation; forecast pulls; API calls; scraping; credentials/secrets/config loading; scoring; backtesting; runtime behavior; execution; trading; order placement; autonomy; production behavior; generated data; fixture data; workflows; dependencies; DB migrations; schema changes; source-code migrations; compatibility shims; provider/source connector implementation; real ingestion implementation; live provider usage; paper simulation; runtime observation. Non-approved behavior values preserved: `provider_connector`, `source_fetching`, `forecast_pull`, `api_call`, `scraping`, `credentials_secrets_config`, `scoring_backtesting`, `runtime_behavior`, `trading_autonomy`, `production_behavior`, `generated_data`, `fixture_change`, `workflow_change`, `dependency_change`, `database_migration`, `schema_change`, `source_code_migration`, `compatibility_shim`.

## Blocked implementation work

Blocked work includes all excluded scope values and any actual provider connector, source-fetching implementation, forecast pull, API call, scraping, credential/config loading, scoring, backtesting, runtime, trading, autonomy, production, generated-data, fixture, workflow, dependency, DB migration, schema, source-code migration, or compatibility-shim work.

## Recommended next ticket

Recommended next track: `narrow_source_fetching_implementation_planning`. This is a later docs/static-test-only planning artifact, not implementation.

## Machine-checkable source-fetching narrow planning-request assignments

- weather bot planning stage: source_fetching_narrow_planning_request
- narrow planning request status: docs_static_test_only
- narrow planning request status: request_only
- narrow planning request status: post_pr_250_owner_disposition
- current state posture: hold_checkpoint
- current state posture: narrow_planning_request_allowed
- owner disposition posture: approve_narrow_source_fetching_planning_only
- requested planning scope: source_identity_and_provenance_planning
- requested planning scope: access_date_and_retrieval_context_planning
- requested planning scope: no_lookahead_boundary_planning
- requested planning scope: provider_source_family_selection_planning
- requested planning scope: fetch_boundary_design_planning
- requested planning scope: credential_config_boundary_planning
- requested planning scope: generated_data_fixture_boundary_planning
- requested planning scope: static_validation_audit_planning
- requested planning scope: fail_closed_behavior_planning
- excluded scope: source_fetching_implementation
- excluded scope: provider_connector_implementation
- excluded scope: forecast_pull_execution
- excluded scope: api_call_execution
- excluded scope: scraping_execution
- excluded scope: credentials_config_loading
- excluded scope: generated_data_creation
- excluded scope: fixture_data_modification
- excluded scope: scoring_implementation
- excluded scope: backtesting_implementation
- excluded scope: runtime_behavior
- excluded scope: trading_behavior
- excluded scope: autonomy_behavior
- excluded scope: production_behavior
- excluded scope: workflow_change
- excluded scope: dependency_change
- excluded scope: database_migration
- excluded scope: schema_change
- excluded scope: source_code_migration
- excluded scope: compatibility_shim
- approval request posture: narrow_implementation_planning_request_only
- approval request posture: source_fetching_implementation_not_approved
- approval request posture: provider_connector_implementation_not_approved
- approval request posture: later_explicit_implementation_approval_required
- provider source posture: provider_connectors_not_approved
- provider source posture: source_fetching_implementation_not_approved
- provider source posture: forecast_pulls_not_approved
- provider source posture: api_calls_not_approved
- provider source posture: scraping_not_approved
- provider source posture: provider_source_planning_only
- requested source family: unknown_source_family
- requested retrieval mode: prohibited_until_explicit_approval
- requested source access method: manual_review
- credential config posture: unknown_requires_review
- generated data fixture posture: no_generated_data
- generated data fixture posture: no_fixture_change
- implementation posture: narrow_planning_request_only
- implementation posture: docs_static_test_only
- implementation posture: no_provider_connector
- implementation posture: no_source_fetching_implementation
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
- implementation posture: no_source_code_migration
- implementation posture: no_compatibility_shim
- recommended next track: narrow_source_fetching_implementation_planning
- conditional next track: hold_checkpoint_if_scope_blocker_found
- conditional next track: owner_disposition_revision_if_scope_exceeds_permission
- conditional next track: additional_docs_only_evidence_if_needed
- evidence status: request_only
- label confidence: confirmed

## Acceptance criteria

- The narrow planning-request PRD exists and carries the canonical ID.
- The artifact is docs/static-test-only and post-PR #250 owner-disposition state.
- It recognizes `approve_narrow_source_fetching_planning_only` and requests only a later narrow source-fetching implementation-planning artifact.
- It does not create the implementation-planning artifact and does not approve source-fetching implementation or other excluded behavior.
- It states implementation requires later separate explicit approval and preserves canonical identifiers, closed-set values, and safe next-track posture.
