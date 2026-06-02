# PRD-P1-WX-STAGE2-REAL-FIXTURE-IMPLEMENTATION-APPROVAL-01 — Real Source-Backed Fixture Implementation Approval Request

Canonical ID: PRD-P1-WX-STAGE2-REAL-FIXTURE-IMPLEMENTATION-APPROVAL-01

## Status and scope

This is a real source-backed fixture implementation approval request only. Real source-backed fixture implementation is not approved by this document.

This document requests a human decision on whether a later, separately approved ticket may create a tiny Stage 2 Weather Bot real source-backed historical-label fixture set. It creates no fixture files, no real source-backed examples, no historical-label data, no generated data, and no runnable behavior.

Real source-backed fixture files are not created. Real historical-label data is not created. Generated data is not created. Existing synthetic fixture files are not modified. The planned real-fixture directory is not created.

## Strategic framing

The controlling source hierarchy remains `AGENTS.md`, `docs/meta/MEG_ACTIVE_STATE.md`, `docs/meta/domain_packets/WEATHER_BOT_PACKET.md`, the standalone MEG Weather Bot PRD (`docs/prd/PRD-P1-WX-STANDALONE_WEATHER_BOT_PRD.md`), and the Stage 2 fixture-track PRDs.

This request follows `PRD-P1-WX-STAGE2-FIXTURE-IMPLEMENTATION-CLOSEOUT-01`, `PRD-P1-WX-STAGE2-REAL-FIXTURE-APPROVAL-01`, and `PRD-P1-WX-STAGE2-REAL-FIXTURE-PLAN-01`. It does not reopen closed synthetic fixture work and does not claim readiness for later Weather Bot phases.

## Stage ladder position

Stage 2 skeleton work is complete, and the Stage 2 static synthetic fixture implementation has been closed out. This approval request sits after real source-backed fixture planning and before any real source-backed fixture implementation.

This approval request does not imply historical-label loading readiness, ingestion readiness, scoring readiness, runtime readiness, production readiness, or trading readiness. Historical-label loading remains separate and unapproved.

## Real source-backed fixture implementation approval-request boundary

This is an approval-request boundary document. It asks whether a future implementation ticket may be prepared and executed only after separate explicit human approval.

Real source-backed fixture implementation is not approved by this document. A later real source-backed fixture implementation ticket requires separate explicit human approval before creating any real fixture directory, fixture README, fixture JSON file, static validation tied to such files, or other implementation artifact.

## Dependency on real source-backed fixture planning

Any future real source-backed fixture must satisfy `PRD-P1-WX-STAGE2-REAL-FIXTURE-PLAN-01` planning requirements. Any future real source-backed fixture must be source-backed, reviewable, and no-lookahead safe.

The planning PRD remains the controlling prerequisite for source/provenance fields, source identity, source name, source locator, access date, venue rule reference, resolver source identity, point-in-time availability notes, no-lookahead notes, reviewer/adjudication notes, conflicting-source notes when applicable, expected validation posture, and non-approval notes.

## Why real source-backed fixture implementation may be useful later

If separately approved, a tiny real source-backed fixture set may help reviewers evaluate whether the Stage 2 historical-label schema can represent real settlement-source provenance without creating ingestion, runtime, scoring, or trading authority.

The usefulness is limited to static documentation and validation review. It is not evidence that historical-label loading, ingestion, model scoring, runtime observation, execution, autonomy, or production behavior is ready.

## Requested future implementation scope

This approval request may ask permission for a later implementation ticket to create a tiny real source-backed fixture set only if separately approved.

The requested future implementation scope may include only:

- creating the planned directory: `tests/fixtures/weather/stage2_real_source_backed_labels/`;
- creating at most 3 real source-backed fixture JSON files;
- creating a README for the real-fixture directory;
- using only human-selected, source-backed, reviewable fixture candidates;
- requiring source identity;
- requiring source name;
- requiring source URL or stable source locator;
- requiring access date;
- requiring venue rule reference;
- requiring resolver source identity;
- requiring point-in-time availability notes;
- requiring no-lookahead notes;
- requiring reviewer/adjudication notes;
- requiring conflicting-source notes when applicable;
- requiring expected validation posture;
- requiring non-approval notes;
- adding static validation tests only; and
- avoiding any production/runtime loader.

The approval request must not ask for permission to fetch or scrape data, call providers, pull forecasts, ingest live or historical data, score probabilities, run any historical performance evaluation, run paper-only execution rehearsal, run runtime observation, trade, place orders, or act under independent execution authority.

## Explicitly excluded scope

Ingestion is not created. Provider/API connectors are not created. External API calls are not created. Credentials/secrets/config loading is not created. Forecast pulls are not created.

Scoring/backtesting/runtime/trading/order placement/autonomy remain unapproved. Historical-label loading remains separate and unapproved.

This ticket does not add dependencies, workflows, scripts, SQL, migrations, data directories, generated outputs, fixture JSON files, fixture README changes, provider integration, connectors, runtime modules, trading components, production behavior, or C++/Rust runtime components.

## Human approval checklist

Before a later implementation ticket may proceed, the human reviewer must explicitly decide whether to permit a tiny real source-backed fixture implementation ticket. The reviewer must confirm that the later ticket remains limited to static files and tests, preserves the first-set cap, and does not request ingestion, connector, scoring, runtime, trading, order, or autonomy scope.

The reviewer must also confirm that the later ticket will require source identity, source name, source locator, access date, venue rule reference, resolver source identity, point-in-time availability notes, no-lookahead notes, reviewer/adjudication notes, and non-approval notes.

## Approval decision options

The human decision options are:

- do not grant approval and hold at the current checkpoint;
- request corrections to this approval request before deciding; or
- separately approve a later real source-backed fixture implementation ticket, capped at the first tiny set and limited to static files and static validation only.

No option in this document approves ingestion, historical-label loading, scoring, runtime, production behavior, trading, order placement, or autonomy.

## Implementation risk controls

Any later approved implementation must remain static and reviewable. It must use human-selected candidates only, must document provenance, must avoid lookahead leakage, and must keep all non-approval notes explicit.

The later ticket must not add provider/API connectors, external calls, credential/config loading, ingestion, scoring, runtime observation, paper-only execution rehearsal, trading, order placement, autonomy, production behavior, or C++/Rust runtime components.

## Source/provenance prerequisites

Every future real source-backed fixture candidate must include source identity, source name, source URL or stable source locator, access date, venue rule reference, resolver source identity, point-in-time availability notes, reviewer/adjudication notes, and non-approval notes.

The source/provenance record must be reviewable without implying that the source has been integrated into MEG runtime systems.

## No-lookahead prerequisites

Every future candidate must include no-lookahead notes describing why the evidence used for the expected label was available at the relevant decision or settlement-review point.

Any uncertain availability posture must remain blocked or unclear, not promoted to readiness. The fixture must be no-lookahead safe before real use.

## Reviewer/adjudication prerequisites

Every future candidate must include reviewer/adjudication notes. Conflicting-source notes are required when applicable, and unclear or conflicting evidence must not be converted into confirmed labels without documented reviewer reasoning.

Reviewer inference must be explicitly labeled and must not masquerade as direct source support.

## Fixture count cap

The first later real-fixture implementation ticket may include at most 3 real source-backed fixture candidates. Any larger fixture set requires a separate expansion approval request.

The cap preserves the planning posture from `PRD-P1-WX-STAGE2-REAL-FIXTURE-PLAN-01` and prevents a small static review step from becoming broad data collection.

## Future directory/file allowlist

If separately approved later, the future implementation ticket may create only the planned directory `tests/fixtures/weather/stage2_real_source_backed_labels/`, at most 3 fixture JSON files in that directory, a README in that directory, and static validation tests specifically for that static real-fixture set.

The planned future directory is mentioned here but not created by this ticket. The planned real-fixture directory is not created.

## Relationship to historical-label loading

Historical-label loading remains separate and unapproved. This approval request does not approve production/runtime loaders, source-backed loading, fixture loading beyond static validation, or any data pipeline.

A future static fixture implementation, if separately approved, would still not imply historical-label loading readiness.

## Relationship to ingestion

Ingestion is not created. This approval request does not approve ingestion readiness and does not approve live or historical data ingestion.

A future static fixture ticket must avoid ingestion and must not treat fixture files as a path to provider or source ingestion.

## Relationship to scoring/backtesting

Scoring/backtesting remains unapproved. This approval request does not approve model scoring, probability scoring, historical performance evaluation, paper-only execution rehearsal, or any analysis that converts labels into trading decisions.

A future static fixture ticket must not request scoring readiness or runtime use.

## Relationship to runtime/trading

Runtime observation, trading, order placement, and autonomy remain unapproved. This approval request does not approve runtime readiness, production readiness, trading readiness, operator approval flows, position sizing, order placement, or autonomous action.

Any future fixture implementation must remain static and must not be connected to runtime or execution behavior.

## Explicit non-approval boundaries

This approval request does not approve real source-backed fixture implementation. It does not approve real historical-label data, generated data, ingestion, provider integration, connectors, external API calls, credentials/secrets/config loading, forecast pulls, model scoring, probability scoring, backtesting, paper simulation, runtime observation, trading, order placement, autonomy, production behavior, or C++/Rust runtime components.

A later real source-backed fixture implementation ticket requires separate explicit human approval.

## Closed Stage 2 real-fixture implementation approval-request vocabulary

Actual machine-checkable values for this approval request are limited to the closed sets in the machine-checkable section. The static validator must parse only that section.

Allowed value categories are real fixture implementation approval stage, request status, requested future implementation scope, approval boundary status, future ticket permission, fixture data posture, non-approval category, evidence status, and label confidence.

## Forbidden Stage 2 real-fixture implementation approval-request values

Forbidden actual values are documented examples only and must not be parsed as machine-checkable assignments outside the dedicated assignment section:

- request_prepared/implementation_not_approved
- not_approved/separate_human_approval_required
- source_backed/reviewer_inferred
- confirmed/unclear
- partial
- mixed
- likely_confirmed
- maybe
- approved
- configured
- available
- real_fixture_ready
- real_fixtures_ready
- data_ready
- ingestion_ready
- scoring_ready
- runtime_ready
- trading_ready
- production_ready
- provider_ready
- model_ready
- backtest_ready
- ready_for_ingestion
- ready_for_scoring
- ready_for_runtime
- ready_for_trading
- approved_for_real_fixtures
- approved_for_ingestion
- approved_for_runtime
- approved_for_scoring
- approved_for_trading
- trade_ready
- auto_execute
- autonomous
- live
- production

## Machine-checkable Stage 2 real-fixture implementation approval-request assignments

- real fixture implementation approval stage: stage_2_real_source_backed_fixture_implementation_approval_request
- request status: request_prepared
- request status: implementation_not_approved
- request status: human_review_required
- request status: blocked_pending_fix
- request status: unclear
- requested future implementation scope: real_fixture_files_only_if_later_approved
- requested future implementation scope: create_real_fixture_directory_if_later_approved
- requested future implementation scope: at_most_3_real_fixture_candidates
- requested future implementation scope: source_backed_candidates_only
- requested future implementation scope: provenance_notes_required
- requested future implementation scope: access_date_required
- requested future implementation scope: venue_rule_reference_required
- requested future implementation scope: resolver_source_identity_required
- requested future implementation scope: no_lookahead_notes_required
- requested future implementation scope: reviewer_adjudication_notes_required
- requested future implementation scope: static_validation_only
- requested future implementation scope: no_ingestion_no_runtime_no_scoring
- approval boundary status: not_approved
- approval boundary status: separate_human_approval_required
- approval boundary status: explicitly_out_of_scope
- approval boundary status: blocked
- future ticket permission: may_request_real_fixture_implementation_ticket
- future ticket permission: must_not_create_real_fixtures_now
- future ticket permission: must_not_create_ingestion
- future ticket permission: must_not_create_runtime
- future ticket permission: must_not_create_scoring
- future ticket permission: must_not_create_trading
- future ticket permission: blocked_until_human_decision
- fixture data posture: no_real_fixture_data_created
- fixture data posture: no_historical_label_data_created
- fixture data posture: no_generated_data_created
- fixture data posture: existing_synthetic_fixtures_unchanged
- fixture data posture: planned_real_fixture_directory_not_created
- fixture data posture: source_backing_required_before_real_use
- fixture data posture: review_required_before_real_use
- fixture data posture: no_lookahead_required_before_real_use
- non-approval category: real_historical_label_data
- non-approval category: generated_data
- non-approval category: ingestion
- non-approval category: provider_integration
- non-approval category: connectors
- non-approval category: external_api_calls
- non-approval category: credentials_secrets_config
- non-approval category: forecast_pulls
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

## Later-ticket handoff

If human approval is not granted, the recommended next ticket is hold/checkpoint only. If human approval is granted separately by the user, the recommended next ticket is a real source-backed fixture implementation ticket only, capped at at most 3 candidates and limited to static files and static validation.

Do not recommend ingestion, scoring, backtesting, runtime, trading, order placement, or autonomy as the next ticket from this approval request.

## Acceptance criteria

- The approval-request PRD exists and includes canonical ID `PRD-P1-WX-STAGE2-REAL-FIXTURE-IMPLEMENTATION-APPROVAL-01`.
- The document references the standalone MEG Weather Bot PRD, `MEG_ACTIVE_STATE`, `WEATHER_BOT_PACKET`, `PRD-P1-WX-STAGE2-FIXTURE-IMPLEMENTATION-CLOSEOUT-01`, `PRD-P1-WX-STAGE2-REAL-FIXTURE-APPROVAL-01`, and `PRD-P1-WX-STAGE2-REAL-FIXTURE-PLAN-01`.
- The document states approval-request-only scope and states that real source-backed fixture implementation is not approved by this document.
- The document states that no real fixture files, real historical-label data, generated data, modified synthetic fixtures, planned real-fixture directory, ingestion, connectors, external API calls, credential/config loading, forecast pulls, scoring, backtesting, runtime, trading, order placement, or autonomy are created or approved.
- The document preserves the at-most-3 first real-fixture candidate cap and requires separate expansion approval for any larger fixture set.
- The document requires source identity, source name, source locator, access date, venue rule reference, resolver source identity, point-in-time availability notes, no-lookahead notes, reviewer/adjudication notes, and non-approval notes for any future real fixture.
- Static tests parse only the machine-checkable section, enforce closed sets, require every allowed value, document forbidden examples without treating them as assignments, and verify that `tests/fixtures/weather/stage2_real_source_backed_labels/` does not exist.
