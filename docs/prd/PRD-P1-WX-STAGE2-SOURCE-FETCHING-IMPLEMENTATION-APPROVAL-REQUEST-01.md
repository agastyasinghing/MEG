# PRD-P1-WX-STAGE2-SOURCE-FETCHING-IMPLEMENTATION-APPROVAL-REQUEST-01 — Source-Fetching Implementation Approval Request

Canonical ID: PRD-P1-WX-STAGE2-SOURCE-FETCHING-IMPLEMENTATION-APPROVAL-REQUEST-01

## Status and scope

This is a source-fetching implementation approval request only. It is docs/static-test-only. It starts from the post-PR #253 narrow implementation-planning closeout state and treats PR #253 / `PRD-P1-WX-STAGE2-SOURCE-FETCHING-NARROW-IMPLEMENTATION-PLANNING-CLOSEOUT-01` as the latest completed narrow implementation-planning closeout predecessor.

This artifact is not an approval decision. This artifact does not approve implementation by itself. This artifact does not implement source fetching. Source-fetching implementation is not approved by this artifact. Provider connector implementation is not approved by this artifact. Actual implementation requires a later separate explicit owner approval decision artifact.

## Relationship to narrow implementation-planning closeout

PR #253 is the latest completed narrow implementation-planning closeout predecessor. PR #253 created and merged `PRD-P1-WX-STAGE2-SOURCE-FETCHING-NARROW-IMPLEMENTATION-PLANNING-CLOSEOUT-01`, which closed the narrow implementation-planning layer at the docs/static-test-only planning level only and defaulted to `hold_checkpoint`.

Relationship IDs: `PRD-P1-WX-STAGE2-SOURCE-FETCHING-IMPLEMENTATION-APPROVAL-REQUEST-01`, `PRD-P1-WX-STAGE2-SOURCE-FETCHING-NARROW-IMPLEMENTATION-PLANNING-CLOSEOUT-01`, `PRD-P1-WX-STAGE2-SOURCE-FETCHING-NARROW-IMPLEMENTATION-PLANNING-01`, `PRD-P1-WX-STAGE2-SOURCE-FETCHING-NARROW-PLANNING-REQUEST-01`, `PRD-P1-WX-STAGE2-SOURCE-FETCHING-APPROVAL-REQUEST-OWNER-DISPOSITION-01`, `PRD-P1-WX-STAGE2-SOURCE-FETCHING-APPROVAL-REQUEST-OWNER-DISPOSITION-PLANNING-01`, `PRD-P1-WX-STAGE2-SOURCE-FETCHING-APPROVAL-REQUEST-META-REFRESH-01`, `PRD-P1-WX-STAGE2-SOURCE-FETCHING-APPROVAL-REQUEST-HOLD-CHECKPOINT-01`, `PRD-P1-WX-STAGE2-SOURCE-FETCHING-APPROVAL-REQUEST-DRAFT-CLOSEOUT-01`, `PRD-P1-WX-STAGE2-SOURCE-FETCHING-APPROVAL-REQUEST-DRAFT-01`, `PRD-P1-WX-STAGE2-SOURCE-FETCHING-APPROVAL-REQUEST-DRAFT-PLANNING-01`, `PRD-P1-WX-STAGE2-SOURCE-FETCHING-APPROVAL-REQUEST-CLOSEOUT-01`, `PRD-P1-WX-STAGE2-SOURCE-FETCHING-APPROVAL-REQUEST-PLANNING-01`, `PRD-P1-WX-STAGE2-PROVIDER-SOURCE-COMPATIBILITY-CLOSEOUT-01`, `PRD-P1-WX-STAGE2-PROVIDER-SOURCE-COMPATIBILITY-PLANNING-01`, `PRD-P1-WX-STAGE2-WEATHER-BOT-RETURN-TO-PLANNING-01`, `MEG-ARCH-ALIGN-08`, `PRD-P1-WX-STANDALONE_WEATHER_BOT_PRD`.

## Relationship to narrow implementation planning

`PRD-P1-WX-STAGE2-SOURCE-FETCHING-NARROW-IMPLEMENTATION-PLANNING-01` planned a narrow seam for possible later source-fetching implementation consideration. This request asks only that a later owner approval decision consider that narrow planning scope; it does not convert the planning artifact into approval.

## Relationship to narrow planning request

`PRD-P1-WX-STAGE2-SOURCE-FETCHING-NARROW-PLANNING-REQUEST-01` requested narrow implementation planning only. This artifact follows the completed planning and closeout sequence by opening an approval-request path, not an implementation path.

## Relationship to owner disposition

`PRD-P1-WX-STAGE2-SOURCE-FETCHING-APPROVAL-REQUEST-OWNER-DISPOSITION-01` and `PRD-P1-WX-STAGE2-SOURCE-FETCHING-APPROVAL-REQUEST-OWNER-DISPOSITION-PLANNING-01` preserved planning-only continuation. The owner has now explicitly requested to continue the gated path rather than remain at hold, but this document records only an approval request, not an approval decision.

## Relationship to hold checkpoint

`PRD-P1-WX-STAGE2-SOURCE-FETCHING-APPROVAL-REQUEST-HOLD-CHECKPOINT-01` remains the prior hold checkpoint reference. PR #253 defaulted to `hold_checkpoint`, but the owner has explicitly requested to continue the gated path rather than remain at hold. This artifact therefore opens the `implementation_approval_request_only_after_explicit_owner_approval` path while preserving all non-approval boundaries until a later approval decision exists.

## Relationship to Weather Bot PRD and architecture alignment

This request remains aligned with `PRD-P1-WX-STAGE2-WEATHER-BOT-RETURN-TO-PLANNING-01`, `MEG-ARCH-ALIGN-08`, and `PRD-P1-WX-STANDALONE_WEATHER_BOT_PRD`. Weather Bot models the market settlement rule, not generic weather.

## Approval-request objective

The objective is to request consideration of a narrow source-fetching implementation scope based on the prior planning artifact. This is request-only posture and does not approve source-fetching implementation, provider connector implementation, forecast pulls, API calls, scraping, file downloads, provider SDK usage, credentials/secrets/config loading, generated data, fixture changes, scoring, backtesting, runtime behavior, trading, autonomy, or production behavior. Scoring/backtesting/runtime/trading/autonomy/production behavior is not approved by this artifact.

## Owner continuation signal

The owner continuation signal is `owner_requested_continue_beyond_hold`. This signal permits this docs/static-test-only approval-request artifact to be created after PR #253, but it is not itself implementation approval.

## Requested approval path

This artifact opens the `implementation_approval_request_only_after_explicit_owner_approval` path. The requested next decision track is `source_fetching_implementation_approval_decision`.

## Requested narrow implementation scope

A later owner approval decision may consider only these possible implementation-scope areas:

- `source_identity_recording`
- `retrieval_context_recording`
- `provider_source_family_recording`
- `manual_review_gate`
- `no_lookahead_metadata_gate`
- `fail_closed_validation_gate`
- `static_audit_surface`

Live provider/source fetching is not approved by this request.

## Scope still not approved by this request

Explicitly excluded from this request:

- `source_fetching_implementation_approved`
- `provider_connector_implementation_approved`
- `forecast_pull_execution_approved`
- `api_call_execution_approved`
- `scraping_execution_approved`
- `file_download_execution_approved`
- `provider_sdk_execution_approved`
- `credentials_config_loading_approved`
- `generated_data_creation_approved`
- `fixture_data_modification_approved`
- `scoring_implementation_approved`
- `backtesting_implementation_approved`
- `runtime_behavior_approved`
- `trading_behavior_approved`
- `autonomy_behavior_approved`
- `production_behavior_approved`

These are excluded approval labels, not granted approvals.

## Required later owner approval decision

Implementation requires a later separate explicit owner approval decision artifact. Until that later decision exists, implementation remains not approved by this request.

## Proposed implementation boundaries for later approval

Any later approval decision should remain narrow to metadata and validation boundaries only: source identity recording, retrieval context recording, provider/source family recording, manual review gating, no-lookahead metadata gating, fail-closed validation gating, and static audit surface. This request does not approve execution, live provider usage, real ingestion implementation, provider/source connector implementation, paper simulation, or runtime observation.

## Source identity and provenance requirements

A later approved implementation would need source identity and provenance metadata before source use. This request preserves `source_identity_recording` only as a proposed narrow consideration and does not approve source fetching implementation.

## Retrieval context requirements

A later approved implementation would need access date, retrieval timestamp, retrieval context, source availability timing, and market resolution timing relationship metadata. This request preserves `retrieval_context_recording` only as a proposed narrow consideration and does not approve forecast pulls, API calls, scraping, file downloads, or provider SDK usage.

## No-lookahead requirements

A later approved implementation would need `no_lookahead_metadata_gate` behavior that fails closed against future-information leakage, post-resolution evidence for pre-resolution labels, unavailable-at-decision-time source use, and settlement leakage. This request does not create generated labels or generated data.

## Provider/source family requirements

Closed-set source-family values to preserve:

- `forecast_provider_family`
- `historical_observation_provider_family`
- `official_resolution_source_family`
- `market_metadata_source_family`
- `manual_human_review_source_family`
- `unsupported_source_family`
- `unknown_source_family`

Provider/source families remain labels for review. Provider connector implementation is not approved by this artifact.

## Fetch-boundary requirements

Closed-set retrieval-mode values to preserve:

- `manual_descriptor_only`
- `static_fixture_reference_only`
- `later_source_fetching_request`
- `later_provider_connector_request`
- `prohibited_until_explicit_approval`
- `unknown_requires_review`

Closed-set access-method values to preserve:

- `manual_review`
- `static_reference`
- `api_call`
- `scraping`
- `file_download`
- `provider_sdk`
- `unknown_requires_review`

API calls are not approved by this artifact. Scraping is not approved by this artifact. File downloads are not approved by this artifact. Provider SDK usage is not approved by this artifact. Forecast pulls are not approved by this artifact.

## Credential/config requirements

Closed-set credential/config values to preserve:

- `none_required`
- `credentials_required_later`
- `config_required_later`
- `secrets_required_later`
- `unknown_requires_review`

Credentials/secrets/config loading is not approved by this artifact.

## Generated-data and fixture requirements

Closed-set generated-data/fixture values to preserve:

- `no_generated_data`
- `no_fixture_change`
- `generated_data_requires_later_approval`
- `fixture_change_requires_later_approval`
- `unknown_requires_review`

Generated data is not approved or created by this artifact. Fixture changes are not approved or modified by this artifact.

## Static validation requirements

Static validation must remain stdlib-only and docs/static-test-only for this ticket. Tests must parse machine-checkable assignment values only from the dedicated machine-checkable section and must reject values outside the allowed set.

## Fail-closed requirements

The later approval decision, if any, should preserve `fail_closed_validation_gate` posture. Unknown source family, unknown retrieval mode, unknown access method, unknown credential/config posture, and unknown generated-data/fixture posture must require review rather than silent use.

## Approval posture

This artifact is an approval request only. This artifact is not an approval decision. Implementation is not approved by this request. Source-fetching implementation is not approved. Provider connector implementation is not approved.

## Request-only posture

This artifact opens the implementation approval-request path after the owner continuation signal. It does not approve implementation by itself and does not implement source fetching.

## Canonical identifier posture

The canonical identifier contract is preserved: `condition_id`, `token_id`, and `outcome`. No routing on `market_id` is introduced or approved.

## Provider/source compatibility posture

The provider/source compatibility posture remains request-only. Provider connectors are not approved. Source fetching implementation is not approved. Forecast pulls are not approved. API calls are not approved. Scraping is not approved.

## Offline-ingestion boundary posture

Offline-ingestion boundaries remain intact. This artifact does not approve real ingestion implementation, live provider usage, runtime observation, generated data, fixture data, or paper simulation.

## Test-scope posture

The test scope is limited to a new static PRD test under `tests/core`. It must not import production Weather Bot modules and must not modify fixtures, generated data, runtime code, schemas, migrations, workflows, dependencies, or config loading.

## Risk and failure-mode posture

Primary risks are accidental conversion of request language into approval language, accidental live-provider scope creep, accidental credential/config scope creep, and accidental future-information leakage. This artifact mitigates those risks by keeping request-only posture, explicit exclusions, closed-set values, parser-scoped assignments, canonical identifier preservation, and later-owner-approval requirements.

## Explicit non-approval boundaries

This approval-request artifact explicitly does not implement, approve, create, recommend, or modify:

- provider connectors
- source fetching implementation
- forecast pulls
- API calls
- scraping
- file downloads
- provider SDK usage
- credentials/secrets/config loading
- scoring
- backtesting
- runtime behavior
- execution
- trading
- order placement
- autonomy
- production behavior
- generated data
- fixture data
- workflows
- dependencies
- DB migrations
- schema changes
- source-code migrations
- compatibility shims
- provider/source connector implementation
- real ingestion implementation
- live provider usage
- paper simulation
- runtime observation

Explicit non-approved behavior values preserved:

- `provider_connector`
- `source_fetching`
- `forecast_pull`
- `api_call`
- `scraping`
- `credentials_secrets_config`
- `scoring_backtesting`
- `runtime_behavior`
- `trading_autonomy`
- `production_behavior`
- `generated_data`
- `fixture_change`
- `workflow_change`
- `dependency_change`
- `database_migration`
- `schema_change`
- `source_code_migration`
- `compatibility_shim`

## Blocked implementation work

Blocked implementation work includes provider connectors, source-fetching implementation, forecast pulls, API calls, scraping, file downloads, provider SDK usage, credentials/secrets/config loading, generated data creation, fixture data modification, scoring implementation, backtesting implementation, runtime behavior, trading behavior, autonomy behavior, production behavior, workflow changes, dependency changes, database migrations, schema changes, source-code migrations, and compatibility shims.

## Recommended next ticket

Recommended next track: `source_fetching_implementation_approval_decision`. Conditional next tracks are `hold_checkpoint_if_approval_denied`, `implementation_planning_revision_if_scope_too_broad`, and `narrow_source_fetching_implementation_plan_if_owner_approves`.

## Machine-checkable source-fetching implementation approval-request assignments

- weather bot planning stage: source_fetching_implementation_approval_request
- implementation approval request status: docs_static_test_only
- implementation approval request status: request_only
- implementation approval request status: post_pr_253_closeout
- current state posture: post_closeout_hold_checkpoint
- current state posture: implementation_not_approved
- owner continuation posture: owner_requested_continue_beyond_hold
- approval request posture: approval_request_only
- approval request posture: approval_decision_not_recorded
- approval request posture: implementation_not_approved_by_request
- approval request posture: later_owner_approval_decision_required
- requested approval path: implementation_approval_request_only_after_explicit_owner_approval
- requested narrow implementation scope: source_identity_recording
- requested narrow implementation scope: retrieval_context_recording
- requested narrow implementation scope: provider_source_family_recording
- requested narrow implementation scope: manual_review_gate
- requested narrow implementation scope: no_lookahead_metadata_gate
- requested narrow implementation scope: fail_closed_validation_gate
- requested narrow implementation scope: static_audit_surface
- excluded approval: source_fetching_implementation_approved
- excluded approval: provider_connector_implementation_approved
- excluded approval: forecast_pull_execution_approved
- excluded approval: api_call_execution_approved
- excluded approval: scraping_execution_approved
- excluded approval: file_download_execution_approved
- excluded approval: provider_sdk_execution_approved
- excluded approval: credentials_config_loading_approved
- excluded approval: generated_data_creation_approved
- excluded approval: fixture_data_modification_approved
- excluded approval: scoring_implementation_approved
- excluded approval: backtesting_implementation_approved
- excluded approval: runtime_behavior_approved
- excluded approval: trading_behavior_approved
- excluded approval: autonomy_behavior_approved
- excluded approval: production_behavior_approved
- provider source posture: provider_connectors_not_approved
- provider source posture: source_fetching_implementation_not_approved
- provider source posture: forecast_pulls_not_approved
- provider source posture: api_calls_not_approved
- provider source posture: scraping_not_approved
- provider source posture: provider_source_approval_request_only
- requested source family: unknown_source_family
- requested retrieval mode: prohibited_until_explicit_approval
- requested source access method: manual_review
- credential config posture: unknown_requires_review
- generated data fixture posture: no_generated_data
- generated data fixture posture: no_fixture_change
- implementation posture: request_only
- implementation posture: docs_static_test_only
- implementation posture: no_provider_connector
- implementation posture: no_source_fetching_implementation
- implementation posture: no_forecast_pull
- implementation posture: no_api_call
- implementation posture: no_scraping
- implementation posture: no_file_download
- implementation posture: no_provider_sdk
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
- recommended next track: source_fetching_implementation_approval_decision
- conditional next track: hold_checkpoint_if_approval_denied
- conditional next track: implementation_planning_revision_if_scope_too_broad
- conditional next track: narrow_source_fetching_implementation_plan_if_owner_approves
- evidence status: request_only
- label confidence: confirmed

## Acceptance criteria

- The approval-request PRD exists and carries `PRD-P1-WX-STAGE2-SOURCE-FETCHING-IMPLEMENTATION-APPROVAL-REQUEST-01`.
- The artifact is docs/static-test-only.
- It starts from post-PR #253 closeout state.
- It records owner continuation beyond hold.
- It is an approval request only, not an approval decision.
- It does not implement source fetching.
- It does not approve source-fetching implementation.
- It does not approve provider connector implementation.
- It does not approve forecast pulls, API calls, scraping, file downloads, provider SDK usage, credentials/config loading, generated data, fixture changes, scoring, backtesting, runtime, trading, autonomy, or production behavior.
- It states implementation requires later separate explicit owner approval decision.
- It preserves canonical identifier posture for `condition_id`, `token_id`, and `outcome`, and no routing on `market_id` is introduced or approved.
- It preserves all closed-set and non-approved behavior values.
- It recommends `source_fetching_implementation_approval_decision` as the next track.
