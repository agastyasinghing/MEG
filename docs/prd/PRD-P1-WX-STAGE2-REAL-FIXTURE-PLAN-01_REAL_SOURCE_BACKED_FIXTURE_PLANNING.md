# PRD-P1-WX-STAGE2-REAL-FIXTURE-PLAN-01 — Real Source-Backed Fixture Planning

Canonical ID: PRD-P1-WX-STAGE2-REAL-FIXTURE-PLAN-01

## Status and scope

This is real source-backed fixture planning only. Real source-backed fixture implementation is not approved.

This planning document creates requirements for a possible later Stage 2 Weather Bot real source-backed historical-label fixture implementation ticket. Real source-backed fixture files are not created by this ticket. Real historical-label data is not created. Generated data is not created. Existing synthetic fixture files are not modified.

This document references the standalone MEG Weather Bot PRD (`PRD-P1-WX-STANDALONE_WEATHER_BOT_PRD.md`), `MEG_ACTIVE_STATE`, `WEATHER_BOT_PACKET`, `PRD-P1-WX-STAGE2-REAL-FIXTURE-APPROVAL-01`, `PRD-P1-WX-STAGE2-FIXTURE-IMPLEMENTATION-CLOSEOUT-01`, and `PRD-P1-WX-STAGE2-FIXTURE-IMPLEMENTATION-01` as controlling context.

## Strategic framing

The strategic objective is to define reviewable requirements before any future real source-backed fixture work can be considered. This document does not collect data, does not define real examples, and does not convert a source into a label.

Any future real source-backed fixture must be source-backed, reviewable, and no-lookahead safe before it can be considered for implementation under a separate explicit approval path.

## Stage ladder position

This ticket follows the completed Stage 2 skeleton closeout, the static synthetic fixture implementation, the static fixture implementation closeout/checkpoint, the active-state update after fixture closeout, and the real source-backed fixture approval request. It remains between approval-request posture and possible later implementation approval; it is not implementation.

The Stage 2 ladder position is planning-only documentation plus static validation. It does not imply ingestion readiness, scoring readiness, runtime readiness, production readiness, or trading readiness.

## Human approval basis

The human approval basis is limited to creating a planning PRD and static validation for future real source-backed fixture requirements. Human approval for this ticket does not approve real source-backed fixture implementation, real fixture files, historical-label data, ingestion, provider/API connectors, external API calls, forecast pulls, scoring, backtesting, runtime, trading, order placement, autonomy, or production behavior.

A later real source-backed fixture implementation approval request requires separate explicit human approval. A later real source-backed fixture implementation ticket requires separate explicit approval after approval request.

## Real source-backed fixture planning boundary

This boundary permits planning future eligibility, provenance, source identity, source URL or stable source locator, access date, venue rule reference, resolver source identity, point-in-time availability notes, no-lookahead notes, reviewer/adjudication notes, conflicting-source notes, expected validation posture, and non-approval notes.

This boundary does not permit creating candidates, examples, source-backed labels, fixture directories, fixture files, ingestion behavior, provider/API connectors, external API calls, credentials/secrets/config loading, forecast pulls, scoring, backtesting, paper simulation, runtime observation, trading, order placement, position sizing, autonomy, or production behavior.

## Dependency on synthetic fixture closeout

This plan depends on `PRD-P1-WX-STAGE2-FIXTURE-IMPLEMENTATION-CLOSEOUT-01` and its closed-out synthetic fixture posture. The existing synthetic fixture set remains exactly the closed-out synthetic set from `PRD-P1-WX-STAGE2-FIXTURE-IMPLEMENTATION-01` and its closeout; existing synthetic fixture files are not modified.

Real source-backed planning must not reinterpret synthetic fixtures as real data and must not use the synthetic fixture closeout as evidence that real source-backed fixtures are implemented.

## Real source-backed fixture purpose and non-purpose

The purpose is to specify planning requirements for future real source-backed Stage 2 Weather Bot historical-label fixture candidates, without creating any actual candidates.

The non-purpose is equally important: this ticket is not a data ticket, not an implementation ticket, not a loader ticket, not a connector ticket, not a provider-integration ticket, not a scoring ticket, not a runtime ticket, and not a trading ticket.

## Eligibility requirements

A future real source-backed fixture candidate would need to satisfy all planning-only eligibility rules before implementation is considered:

- The candidate must be small and reviewable.
- The candidate must map to Stage 2 skeleton metadata expectations.
- The candidate must have source/provenance notes before implementation is considered.
- The candidate must not require live provider/API access.
- The candidate must not imply ingestion/loading behavior.
- The candidate must not imply scoring/backtesting/runtime/trading readiness.
- The candidate must be rejected or blocked if provenance, no-lookahead, or venue-rule compatibility is unclear.

## Source/provenance requirements

A future candidate would need explicit source/provenance requirements before implementation can be considered. Required planning fields include source identity, source name, source URL or stable source locator, access date, venue rule reference, resolver source identity, point-in-time availability notes, no-lookahead notes, reviewer/adjudication notes, conflicting-source notes if applicable, expected validation posture, and non-approval notes.

Provenance must be reviewer-visible. A candidate whose source identity, source name, locator, access date, resolver source identity, or venue rule reference cannot be reviewed must be blocked.

## Source URL/source-name/access-date requirements

Each future candidate would need a source name, source URL or stable source locator, and access date. The access date must record when a human reviewer inspected the source or stable locator for planning or implementation review.

The source URL or stable locator must be durable enough for review. If a source cannot provide stable review evidence without live provider/API access, the candidate must remain blocked.

## Resolver source identity requirements

Each future candidate would need a resolver source identity that identifies the venue-recognized resolution source or adjudication source. The resolver source identity must be separate from analyst inference and must be reviewable against venue rules. These resolver source identity requirements are blocking prerequisites for any later implementation approval path.

If the resolver source identity is unclear, missing, or inconsistent with the venue rule reference, the candidate must be blocked or marked unclear in any later approval path.

## Venue-rule compatibility requirements

Each future candidate would need a venue rule reference and explicit venue-rule compatibility notes. The candidate must show that the planned label semantics match the venue's resolution rule, including thresholds, geography, time windows, measurement source, and edge-case handling.

A candidate must be rejected or blocked if venue-rule compatibility is unclear, if the source does not map to the venue rule, or if reviewer notes cannot explain the compatibility posture.

## Point-in-time availability requirements

Each future candidate would need point-in-time availability notes showing when the relevant source information was available and whether it was available before the label decision boundary. These notes must distinguish decision-time availability from later archival visibility.

A candidate must be blocked if point-in-time availability cannot be documented without relying on later-only information.

## No-lookahead requirements

Each future candidate would need no-lookahead notes. The notes must explain why the planned label does not use information unavailable at the relevant decision or resolution time.

No-lookahead controls must explicitly exclude final-archive leakage, hindsight-only synthesis, and labels inferred from later summaries unless the venue rule and resolver source support that use. A candidate must be blocked if no-lookahead safety is unclear.

## Reviewer/adjudication requirements

Each future candidate would need reviewer/adjudication notes. The notes must identify what a reviewer checked, what source evidence was used, what remains unclear, and whether adjudication is needed.

Reviewer posture must support blocking unclear labels. Reviewer inference cannot replace source-backed evidence unless the later approved workflow explicitly permits an adjudication note and labels the evidence posture accordingly.

## Conflicting-source handling

Each future candidate would need conflicting-source notes if applicable. The notes must identify the conflicting sources, explain which source is resolver-recognized under venue rules, and preserve uncertainty when conflict cannot be resolved.

A candidate must be blocked if conflicting-source handling cannot identify the resolver source identity or cannot explain why one source controls under venue rules.

## Fixture count cap planning

The planning cap for any later first real-fixture implementation ticket is at most 3 real source-backed fixture candidates. Any larger fixture set requires a separate expansion approval request.

The cap is a review-control boundary, not implementation permission. It limits the first later implementation proposal if separately approved.

## Future fixture directory/file allowlist planning

The preferred planned future directory is `tests/fixtures/weather/stage2_real_source_backed_labels/`.

This planned directory is not created by this ticket. The future directory posture is planned only, not created, and separate approval is required before any future directory or file creation.

A later ticket would need a precise directory/file allowlist and must not modify existing synthetic fixture files unless separately approved for a different scope.

## Static validation planning

Static validation planning should enforce the planning-only PRD existence, canonical ID, required cross-references, required non-approval wording, source/provenance requirements, venue-rule compatibility requirements, point-in-time and no-lookahead requirements, reviewer/adjudication requirements, conflicting-source handling, fixture count cap, planned-directory-not-created posture, and closed-set assignments.

Static validation must parse actual machine-checkable values only from the dedicated machine-checkable section and must not parse prose, forbidden-value examples, matrices, or examples as actual assignment values.

## Relationship to existing synthetic fixtures

Existing synthetic fixture files are not modified. The existing synthetic fixtures remain synthetic, hand-authored fixtures for the closed-out static fixture implementation subphase.

This planning document does not convert synthetic fixtures into real fixtures and does not add real source-backed fixture examples.

## Relationship to historical-label loading

Historical-label loading remains separate and unapproved. This planning document does not add loaders, file readers for real historical-label data, production source modules, generated assets, or any mechanism that would load real historical-label data.

## Relationship to ingestion

Ingestion is not created. Provider/API connectors are not created. External API calls are not created. Credentials/secrets/config loading is not created. Forecast pulls are not created.

This document may describe requirements that a future candidate must not require live provider/API access, but it does not implement provider integration.

## Relationship to scoring/backtesting

Scoring/backtesting remains unapproved. This planning document does not approve model scoring, probability scoring, backtesting, paper simulation, calibration, performance evaluation, or any readiness claim.

## Relationship to runtime/trading

Runtime/trading remains unapproved. Scoring/backtesting/runtime/trading/order placement/autonomy remain unapproved. This planning document does not approve runtime observation, trading, order placement, position sizing, autonomy, or production behavior.

## Explicit non-approval boundaries

This planning document does not approve or create:

- real source-backed fixture implementation;
- real source-backed fixture files;
- real historical-label data;
- generated data;
- modifications to existing synthetic fixture files;
- ingestion;
- provider/API connectors;
- external API calls;
- credentials/secrets/config loading;
- forecast pulls;
- model scoring or probability scoring;
- scoring/backtesting/runtime/trading/order placement/autonomy;
- paper simulation;
- runtime observation;
- production behavior; or
- C++/Rust runtime components.

A later real source-backed fixture implementation approval request requires separate explicit human approval. A later real source-backed fixture implementation ticket requires separate explicit approval after approval request.

## Closed Stage 2 real-fixture planning vocabulary

Actual machine-checkable assignments for this planning PRD must use only the closed values listed in the machine-checkable section. These values cover the real fixture planning stage, planning status, fixture candidate kind, source requirement status, fixture planning scope, implementation boundary, fixture data posture, future directory posture, non-approval category, evidence status, and label confidence.

## Forbidden Stage 2 real-fixture planning values

The following are forbidden examples for actual machine-checkable assignments and are documented so reviewers can distinguish forbidden examples from valid section-scoped values:

- planning_only/implementation_not_approved
- source_identity_required/source_name_required
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

These examples may appear in prose as forbidden examples or non-approval language, but they must not be parsed as actual assignments.

## Machine-checkable Stage 2 real-fixture planning assignments

- real fixture planning stage: stage_2_real_source_backed_fixture_planning
- planning status: planning_only
- planning status: implementation_not_approved
- planning status: human_approval_limited_to_planning
- planning status: blocked_pending_fix
- planning status: unclear
- fixture candidate kind: real_source_backed_candidate
- fixture candidate kind: venue_rule_edge_case
- fixture candidate kind: provenance_edge_case
- fixture candidate kind: no_lookahead_edge_case
- fixture candidate kind: conflicting_source_case
- fixture candidate kind: blocked_case
- fixture candidate kind: unclear_case
- source requirement status: source_identity_required
- source requirement status: source_name_required
- source requirement status: source_locator_required
- source requirement status: access_date_required
- source requirement status: venue_rule_reference_required
- source requirement status: resolver_source_identity_required
- source requirement status: point_in_time_availability_required
- source requirement status: reviewer_notes_required
- source requirement status: no_lookahead_notes_required
- fixture planning scope: eligibility_planning
- fixture planning scope: provenance_requirement_planning
- fixture planning scope: venue_rule_compatibility_planning
- fixture planning scope: no_lookahead_requirement_planning
- fixture planning scope: reviewer_adjudication_planning
- fixture planning scope: conflicting_source_handling_planning
- fixture planning scope: fixture_count_cap_planning
- fixture planning scope: directory_allowlist_planning
- fixture planning scope: static_validation_planning
- fixture planning scope: no_ingestion_no_runtime_no_scoring
- implementation boundary: not_implemented
- implementation boundary: separate_approval_required
- implementation boundary: explicitly_out_of_scope
- implementation boundary: blocked
- fixture data posture: no_real_fixture_data_created
- fixture data posture: no_historical_label_data_created
- fixture data posture: no_generated_data_created
- fixture data posture: existing_synthetic_fixtures_unchanged
- fixture data posture: source_backing_required_before_real_use
- fixture data posture: review_required_before_real_use
- fixture data posture: no_lookahead_required_before_real_use
- future directory posture: planned_only
- future directory posture: not_created
- future directory posture: separate_approval_required
- future directory posture: capped_first_real_fixture_set
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

If the planning PRD and static tests are clean, the next permissible Weather Bot step is a real source-backed fixture implementation approval request only, or a hold/checkpoint if the user does not want to proceed.

Do not recommend real fixture implementation, ingestion, scoring, backtesting, runtime, trading, order placement, or autonomy as the next ticket from this planning document.

## Acceptance criteria

- The planning PRD exists and includes canonical ID `PRD-P1-WX-STAGE2-REAL-FIXTURE-PLAN-01`.
- Required repo context references are present, including the standalone MEG Weather Bot PRD, `MEG_ACTIVE_STATE`, `WEATHER_BOT_PACKET`, `PRD-P1-WX-STAGE2-REAL-FIXTURE-APPROVAL-01`, `PRD-P1-WX-STAGE2-FIXTURE-IMPLEMENTATION-CLOSEOUT-01`, and `PRD-P1-WX-STAGE2-FIXTURE-IMPLEMENTATION-01`.
- The document clearly states planning-only scope and all explicit non-approval boundaries.
- The document defines future candidate eligibility, source/provenance, source URL/source-name/access-date, resolver source identity, venue-rule compatibility, point-in-time availability, no-lookahead, reviewer/adjudication, and conflicting-source requirements without creating candidates.
- The document sets the first later implementation-ticket cap at at most 3 real source-backed fixture candidates and requires a separate expansion approval request for larger sets.
- The preferred planned future directory `tests/fixtures/weather/stage2_real_source_backed_labels/` is mentioned and is not created by this ticket.
- Static validation verifies closed-set assignments by parsing only the machine-checkable section.
