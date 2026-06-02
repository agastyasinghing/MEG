# PRD-P1-WX-STAGE2-REAL-FIXTURE-APPROVAL-01 — Real Source-Backed Fixture Approval Request

Canonical ID: PRD-P1-WX-STAGE2-REAL-FIXTURE-APPROVAL-01

## Status and scope

This is a real source-backed fixture approval request only. It asks whether a later, separately approved ticket may plan real source-backed Stage 2 historical-label fixtures for Weather Bot.

This document does not approve real source-backed fixture planning. Real source-backed fixture planning is not approved by this document. Real source-backed fixture implementation is not approved. Real source-backed fixture files are not created. Real historical-label data is not created. Generated data is not created. Existing synthetic fixture files are not modified.

The controlling source for the Weather Bot stage ladder remains the standalone MEG Weather Bot PRD (`PRD-P1-WX-STANDALONE_WEATHER_BOT_PRD.md`). This request also references `docs/meta/MEG_ACTIVE_STATE.md`, `docs/meta/domain_packets/WEATHER_BOT_PACKET.md`, `PRD-P1-WX-STAGE2-FIXTURE-IMPLEMENTATION-01`, and `PRD-P1-WX-STAGE2-FIXTURE-IMPLEMENTATION-CLOSEOUT-01`.

## Strategic framing

The standalone MEG Weather Bot PRD frames Weather Bot work as staged evidence-gated work around venue-defined weather settlement objects. This request preserves that posture by asking only whether humans want a future planning ticket for real source-backed fixtures after the static synthetic fixture closeout.

The request does not imply ingestion readiness, scoring readiness, runtime readiness, production readiness, or trading readiness. It does not approve provider access, external data collection, or any production behavior.

## Stage ladder position

This approval request follows the completed Stage 2 skeleton and static synthetic fixture sequence:

- `PRD-P1-WX-STAGE2-SKELETON-CLOSEOUT-01` closed the Stage 2 skeleton checkpoint.
- `PRD-P1-WX-STAGE2-FIXTURE-APPROVAL-01` requested approval for static fixture/data planning.
- `PRD-P1-WX-STAGE2-FIXTURE-PLAN-01` planned static historical-label fixtures.
- `PRD-P1-WX-STAGE2-FIXTURE-IMPLEMENTATION-APPROVAL-01` requested approval for static fixture implementation.
- `PRD-P1-WX-STAGE2-FIXTURE-IMPLEMENTATION-01` implemented static synthetic fixtures.
- `PRD-P1-WX-STAGE2-FIXTURE-IMPLEMENTATION-CLOSEOUT-01` closed out the static fixture implementation checkpoint.
- `MEG_ACTIVE_STATE` records hold/checkpoint as the default posture unless a concrete gap is found or the user explicitly chooses a later gate.

The user has chosen to proceed to a later gate request. This document is that request and remains narrower than planning.

## Real source-backed fixture approval-request boundary

The boundary is approval-request only. The request may ask whether a future ticket can plan real source-backed fixture eligibility and controls, but it may not define final real fixture examples, create fixture files, collect data, or make source calls.

Real source-backed fixture planning is not approved by this document. A later real source-backed fixture planning ticket requires separate explicit human approval. A later real source-backed fixture implementation ticket requires separate explicit approval after planning.

## Dependency on static fixture closeout

This request depends on `PRD-P1-WX-STAGE2-FIXTURE-IMPLEMENTATION-CLOSEOUT-01` and the closed static synthetic fixture posture from `PRD-P1-WX-STAGE2-FIXTURE-IMPLEMENTATION-01`. The dependency is sequencing-only: static fixture closeout makes it reasonable to ask whether humans want a future real-fixture planning gate, but it does not approve real data or implementation.

Existing synthetic fixture files are not modified by this request. The static synthetic fixture set remains the only implemented fixture set at this gate.

## Why real source-backed fixture planning may be useful later

Real source-backed fixture planning may be useful later because source-backed examples could test whether Stage 2 historical-label validation handles real settlement evidence, provenance notes, no-lookahead controls, and reviewer adjudication requirements. Any such benefit is hypothetical until a separate planning ticket is explicitly approved.

Any later real source-backed fixture must be source-backed, reviewable, and no-lookahead safe before it can be considered for real use. This request does not make any fixture real-fixture ready.

## Requested future planning scope

This approval request asks whether a later planning ticket may define:

- real source-backed fixture eligibility;
- source/provenance requirements;
- source URL, source-name, and access-date requirements;
- resolver source identity requirements;
- venue rule compatibility requirements;
- point-in-time availability requirements;
- no-lookahead controls;
- reviewer/adjudication workflow;
- allowed real-fixture count cap;
- allowed fixture directory planning;
- static validation requirements; and
- non-approval boundaries.

This request asks for future real source-backed fixture planning only. It does not ask for permission to create real fixture files now, fetch or scrape data, call providers, pull forecasts, ingest live or historical data, score probabilities, run simulation, run runtime observation, trade, place orders, or act without operator approval.

## Explicitly excluded scope

The following remain excluded and unapproved:

- real source-backed fixture implementation;
- real source-backed fixture files;
- real historical-label data;
- generated data;
- modification of existing synthetic fixture files;
- ingestion;
- provider/API connectors;
- external API calls;
- credentials/secrets/config loading;
- forecast pulls;
- model scoring or probability scoring;
- scoring/backtesting/runtime/trading/order placement/autonomy;
- runtime observation;
- production behavior; and
- C++/Rust runtime components.

## Human approval checklist

Human reviewers should answer only the future planning question:

- Should a later ticket be allowed to plan real source-backed Stage 2 historical-label fixtures?
- Is the request still limited to planning controls, eligibility, provenance, no-lookahead requirements, adjudication, caps, directories, and static validation?
- Is implementation still deferred until a separate explicit approval after planning?
- Are ingestion, connectors, external API calls, credentials/secrets/config loading, forecast pulls, scoring, runtime, trading, order placement, and autonomy still out of scope?

## Approval decision options

The decision options are:

1. Approve opening a later real source-backed fixture planning ticket only.
2. Hold/checkpoint and do not open a later real source-backed fixture planning ticket.
3. Request edits to this approval-request document before deciding.

No option in this document approves real source-backed fixture implementation, real fixture files, historical-label data, ingestion, scoring, runtime, or trading.

## Real source-backed fixture planning risks

Future real source-backed fixture planning could introduce risk if it blurs planning with data creation, treats source availability as settlement truth without review, weakens point-in-time controls, or implies downstream readiness. The planning ticket, if approved separately, must preserve closed-set vocabulary, static validation, and strict non-approval boundaries.

## Source/provenance requirements for any later planning

Any later planning ticket must define source/provenance requirements before real fixture implementation can be considered. Planning should require source identity, source URL or stable source locator, source name, access date, venue rule reference, resolver source identity, and reviewer-visible provenance notes.

The later planning ticket must not fetch or scrape data. It must define requirements only.

## No-lookahead requirements for any later planning

Any later planning ticket must define no-lookahead requirements before real fixture implementation can be considered. Planning should require point-in-time availability evidence, decision-time availability notes, explicit exclusion of final-archive leakage, and reviewable checks that labels are not inferred from information unavailable at the relevant time.

## Reviewer/adjudication requirements for any later planning

Any later planning ticket must define reviewer/adjudication requirements before real fixture implementation can be considered. Planning should describe reviewer roles, required review notes, blocked and unclear states, conflicting-source handling, and a human adjudication workflow for labels that cannot be confirmed safely.

## Relationship to historical-label loading

Historical-label loading remains separate and unapproved. This request does not add loaders, file readers for new fixture data, production source modules, generated assets, or any mechanism that would load real historical-label data.

## Relationship to ingestion

Ingestion is not created. Provider/API connectors are not created. External API calls are not created. Credentials/secrets/config loading is not created. Forecast pulls are not created. A future planning ticket may define non-approval boundaries around ingestion, but it may not implement ingestion.

## Relationship to scoring/backtesting

Scoring/backtesting remains unapproved. This request does not approve model scoring, probability scoring, backtesting, paper simulation, calibration, edge language, or any performance claim.

## Relationship to runtime/trading

Runtime/trading remains unapproved. This request does not approve runtime observation, production behavior, trading, order placement, position sizing, or autonomy. All execution-related behavior remains outside this gate.

## Explicit non-approval boundaries

This request does not approve:

- real source-backed fixture planning;
- real source-backed fixture implementation;
- real fixture files;
- real historical-label data;
- generated data;
- ingestion;
- provider/API connectors;
- external API calls;
- credentials/secrets/config loading;
- forecast pulls;
- scoring/backtesting/runtime/trading/order placement/autonomy;
- production behavior; or
- C++/Rust runtime components.

A later real source-backed fixture planning ticket requires separate explicit human approval. A later real source-backed fixture implementation ticket requires separate explicit approval after planning.

## Closed Stage 2 real-fixture approval-request vocabulary

Actual machine-checkable assignments for this approval request must use only the closed values listed in the machine-checkable section. These closed sets cover the real fixture approval stage, request status, requested future scope, approval boundary status, future ticket permission, fixture data posture, non-approval category, evidence status, and label confidence.

## Forbidden Stage 2 real-fixture approval-request values

The following are forbidden examples for actual machine-checkable assignments and are documented so reviewers can distinguish forbidden examples from valid section-scoped values:

- request_prepared/planning_not_approved
- planning_not_approved/implementation_not_approved
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
- fixtures_ready
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

## Machine-checkable Stage 2 real-fixture approval-request assignments

- real fixture approval stage: stage_2_real_source_backed_fixture_approval_request
- request status: request_prepared
- request status: planning_not_approved
- request status: implementation_not_approved
- request status: human_review_required
- request status: blocked_pending_fix
- request status: unclear
- requested future scope: real_fixture_planning_only
- requested future scope: source_provenance_requirement_planning
- requested future scope: no_lookahead_requirement_planning
- requested future scope: reviewer_adjudication_planning
- requested future scope: venue_rule_compatibility_planning
- requested future scope: static_validation_planning
- requested future scope: fixture_count_cap_planning
- requested future scope: no_ingestion_no_runtime_no_scoring
- approval boundary status: not_approved
- approval boundary status: separate_human_approval_required
- approval boundary status: explicitly_out_of_scope
- approval boundary status: blocked
- future ticket permission: may_request_real_fixture_planning_ticket
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

If human approval is not granted, the recommended next posture is hold/checkpoint. If human approval is granted separately by the user, the recommended next ticket is real source-backed fixture planning only.

The later planning ticket, if approved, must not recommend real fixture implementation, ingestion, scoring, backtesting, runtime, or trading as the next default step. Implementation would require separate explicit approval after planning.

## Acceptance criteria

- The approval-request PRD exists with canonical ID `PRD-P1-WX-STAGE2-REAL-FIXTURE-APPROVAL-01`.
- The standalone MEG Weather Bot PRD, `MEG_ACTIVE_STATE`, `WEATHER_BOT_PACKET`, `PRD-P1-WX-STAGE2-FIXTURE-IMPLEMENTATION-01`, and `PRD-P1-WX-STAGE2-FIXTURE-IMPLEMENTATION-CLOSEOUT-01` are referenced.
- The document clearly states that this is a real source-backed fixture approval request only.
- Real source-backed fixture planning is not approved by this document.
- Real source-backed fixture implementation is not approved.
- Real source-backed fixture files are not created.
- Real historical-label data is not created.
- Generated data is not created.
- Existing synthetic fixture files are not modified.
- Ingestion is not created.
- Provider/API connectors are not created.
- External API calls are not created.
- Credentials/secrets/config loading is not created.
- Forecast pulls are not created.
- Scoring/backtesting/runtime/trading/order placement/autonomy remain unapproved.
- A later real source-backed fixture planning ticket requires separate explicit human approval.
- A later real source-backed fixture implementation ticket requires separate explicit approval after planning.
- Any later real source-backed fixture must be source-backed, reviewable, and no-lookahead safe.
- Historical-label loading remains separate and unapproved.
- Machine-checkable assignments use only the closed values in this document and include every allowed value.
