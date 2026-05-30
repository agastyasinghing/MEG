# PRD-P1-WX-STAGE2-FIXTURE-APPROVAL-01 — Static Fixture/Data Approval Request

Canonical ID: `PRD-P1-WX-STAGE2-FIXTURE-APPROVAL-01`

## 1. Status and scope

This is a static fixture/data approval request only for the Weather Bot Stage 2 historical-label skeleton. Static fixtures are not approved by this document. Fixture/data planning has not started. Fixture/data implementation has not started.

This document asks whether a later, separately approved static fixture/data planning ticket may be created. It does not create historical-label data, JSON/YAML/CSV/Parquet fixtures, generated data, ingestion, provider/API connectors, external API calls, credentials/secrets/config loading, forecast pulls, scoring, backtesting, runtime observation, trading, order placement, or autonomy.

## 2. Strategic framing

The controlling source for Weather Bot staging remains the standalone MEG Weather Bot PRD (`PRD-P1-WX-STANDALONE_WEATHER_BOT_PRD.md`). The Weather Bot program models venue-defined weather settlement objects rather than generic weather data access or independent execution behavior.

This approval request is intentionally narrow. It preserves the Stage 2 skeleton posture while asking whether humans want a future planning-only step for static historical-label examples.

## 3. Stage ladder position

This request follows the completed Stage 2 skeleton sequence:

- `PRD-P1-WX-STAGE2-SKELETON-01`: narrow supplied-metadata-only skeleton implementation.
- `PRD-P1-WX-STAGE2-SKELETON-02`: validation coverage refinement.
- `PRD-P1-WX-STAGE2-SKELETON-03`: targeted mapping-builder validation coverage.
- `PRD-P1-WX-STAGE2-SKELETON-CLOSEOUT-01`: Stage 2 skeleton closeout/checkpoint.

The closeout recommends holding unless the user explicitly chooses a next gate. The user has selected only this static fixture/data approval-request gate.

## 4. Fixture/data approval-request boundary

This document is not a fixture plan and is not a fixture implementation. It asks only whether a later static fixture/data planning ticket may be prepared under separate human approval.

The boundary is:

- historical-label data is not created;
- JSON/YAML/CSV/Parquet fixtures are not created;
- generated data is not created;
- ingestion is not created;
- provider/API connectors are not created;
- external API calls are not created;
- credentials/secrets/config loading is not created;
- forecast pulls are not created;
- scoring/backtesting/runtime/trading/order placement/autonomy remain unapproved.

## 5. Why static fixtures may be useful next

Static fixtures may eventually help reviewers inspect shape, provenance, no-lookahead constraints, and human adjudication expectations for historical labels before any broader data work is considered.

That possible value does not approve fixture creation here. It only motivates asking whether a future planning ticket should define safe fixture boundaries.

## 6. Requested future scope

This approval request may ask permission for a later planning ticket to define:

- static fixture purpose and boundaries;
- static fixture schema/data shape;
- synthetic-versus-real fixture distinction;
- fixture provenance requirements;
- no-lookahead requirements;
- fixture review/adjudication requirements;
- fixture file allowlist planning;
- static validation requirements;
- fixture non-approval boundaries.

A later static fixture/data planning ticket requires separate human approval.

## 7. Explicitly excluded scope

This approval request does not ask permission to ingest live or historical data, call providers, pull forecasts, score probabilities, backtest, run runtime observation, trade, place orders, or act autonomously.

It also does not approve fixture implementation, data creation, generated examples, new dependencies, C++/Rust components, production behavior, scripts, workflows, SQL, migrations, notebooks, secrets, or configuration loading.

## 8. Dependency on Stage 2 skeleton closeout

This request depends on `PRD-P1-WX-STAGE2-SKELETON-CLOSEOUT-01`, which documented the Stage 2 skeleton checkpoint and the hold posture before any next gate.

The dependency is procedural only: the closeout identifies possible future gates, while this document requests human review for one planning-only gate.

## 9. Human approval checklist

Before any later planning ticket exists, a human reviewer should confirm:

- this document is a static fixture/data approval request only;
- static fixtures are not approved by this document;
- fixture/data planning has not started;
- fixture/data implementation has not started;
- future static fixture/data planning requires separate human approval;
- future fixture implementation requires separate explicit approval after planning;
- all runtime, scoring, ingestion, provider, and trading boundaries remain closed.

## 10. Approval decision options

A human reviewer may choose one of these outcomes for future work:

1. Hold: do not create a later fixture/data planning ticket.
2. Approve only a later static fixture/data planning ticket.
3. Request clarification before any later ticket.

None of these options approves fixture/data implementation in this document.

## 11. Closed Stage 2 fixture approval-request vocabulary

The machine-checkable assignments below must use only the closed values listed here.

fixture approval stage:
- stage_2_static_fixture_data_approval_request

request status:
- request_prepared
- fixtures_not_approved
- human_review_required
- blocked_pending_fix
- unclear

requested future scope:
- static_fixture_planning_only
- fixture_schema_planning
- fixture_provenance_planning
- fixture_review_adjudication_planning
- fixture_static_validation_planning
- no_ingestion_no_runtime_no_scoring

approval boundary status:
- not_approved
- separate_human_approval_required
- explicitly_out_of_scope
- blocked

future ticket permission:
- may_request_fixture_planning_ticket
- must_not_create_fixtures_now
- must_not_create_ingestion
- must_not_create_runtime
- must_not_create_scoring
- must_not_create_trading
- blocked_until_human_decision

fixture data posture:
- no_fixture_data_created
- planning_only
- synthetic_or_real_distinction_required
- provenance_required_before_use
- review_required_before_use

non-approval category:
- historical_label_data
- fixtures_or_generated_data
- ingestion
- provider_integration
- connectors
- external_api_calls
- credentials_secrets_config
- forecast_pulls
- model_scoring
- probability_scoring
- backtesting
- paper_simulation
- runtime_observation
- trading_order_autonomy
- production_behavior
- cplusplus_rust_runtime
- other_unclear

evidence status:
- source_backed
- reviewer_inferred
- missing
- conflicting
- not_applicable

label confidence:
- confirmed
- unclear
- unknown

## 12. Forbidden Stage 2 fixture approval-request values

The following are forbidden examples for actual machine-checkable assignments. They are documented here as examples only and must not be parsed as actual assignments:

- request_prepared/fixtures_not_approved
- not_approved/separate_human_approval_required
- static_fixture_planning_only/fixture_schema_planning
- source_backed/reviewer_inferred
- confirmed/unclear
- partial
- mixed
- likely_confirmed
- maybe
- approved
- configured
- available
- fixture_ready
- fixtures_ready
- data_ready
- trade_ready
- auto_execute
- autonomous
- live
- production
- provider_ready
- model_ready
- backtest_ready
- ready_for_ingestion
- ready_for_scoring
- ready_for_runtime
- ready_for_trading
- implementation_ready
- ingestion_ready
- scoring_ready
- simulation_ready
- runtime_ready
- trading_ready
- approved_for_fixtures
- approved_for_ingestion
- approved_for_runtime
- approved_for_scoring
- approved_for_trading

## Machine-checkable Stage 2 fixture approval-request assignments

- fixture approval stage: stage_2_static_fixture_data_approval_request
- request status: request_prepared
- request status: fixtures_not_approved
- request status: human_review_required
- requested future scope: static_fixture_planning_only
- requested future scope: fixture_schema_planning
- requested future scope: fixture_provenance_planning
- requested future scope: fixture_review_adjudication_planning
- requested future scope: fixture_static_validation_planning
- requested future scope: no_ingestion_no_runtime_no_scoring
- approval boundary status: not_approved
- approval boundary status: separate_human_approval_required
- approval boundary status: explicitly_out_of_scope
- future ticket permission: may_request_fixture_planning_ticket
- future ticket permission: must_not_create_fixtures_now
- future ticket permission: must_not_create_ingestion
- future ticket permission: must_not_create_runtime
- future ticket permission: must_not_create_scoring
- future ticket permission: must_not_create_trading
- future ticket permission: blocked_until_human_decision
- fixture data posture: no_fixture_data_created
- fixture data posture: planning_only
- fixture data posture: synthetic_or_real_distinction_required
- fixture data posture: provenance_required_before_use
- fixture data posture: review_required_before_use
- non-approval category: historical_label_data
- non-approval category: fixtures_or_generated_data
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
- evidence status: not_applicable
- label confidence: confirmed
- label confidence: unclear

## 14. Fixture approval-request matrix

| Review item | Current posture | Boundary |
| --- | --- | --- |
| Static fixture/data request | Prepared for human review | Does not approve fixtures |
| Static fixture planning | Not started | Requires later separate approval |
| Static fixture implementation | Not started | Requires separate explicit approval after planning |
| Historical-label examples | Not created | Remain outside this ticket |
| Future gates | Listed for decision support | No gate is approved here |

## 15. If approved later, next-ticket boundaries

If a human separately approves a later planning ticket, that ticket should remain static and planning-only. It may define fixture purpose, schema/data shape, provenance, no-lookahead requirements, review/adjudication expectations, file allowlist planning, static validation, and non-approval boundaries.

The later planning ticket must not create fixtures or data, and must not add ingestion, provider calls, scoring, runtime behavior, trading, or autonomy.

## 16. Explicit non-approval boundaries

Static fixtures are not approved by this document. Fixture/data planning has not started. Fixture/data implementation has not started. Historical-label data is not created. JSON/YAML/CSV/Parquet fixtures are not created. Generated data is not created.

Ingestion is not created. Provider/API connectors are not created. External API calls are not created. Credentials/secrets/config loading is not created. Forecast pulls are not created. Scoring/backtesting/runtime/trading/order placement/autonomy remain unapproved.

## 17. Relationship to future ingestion

Future ingestion remains outside this approval request. A fixture/data planning ticket, if separately approved, must keep ingestion explicitly out of scope and must not imply readiness for ingestion.

## 18. Relationship to future scoring/backtesting

Future scoring and backtesting remain outside this approval request. A fixture/data planning ticket, if separately approved, must not evaluate probabilities, model behavior, historical performance, or simulation outcomes.

## 19. Relationship to future runtime/trading

Future runtime observation, trading, order placement, position sizing, and autonomy remain outside this approval request. A fixture/data planning ticket, if separately approved, must not create runtime behavior or execution authority.

## 20. Later-ticket handoff

If human approval is not granted, the recommended next state is hold.

If human approval is granted separately by the user, the recommended next ticket is static historical-label fixture planning only. A later fixture implementation ticket requires separate explicit approval after planning.

## 21. Acceptance criteria

- The canonical ID `PRD-P1-WX-STAGE2-FIXTURE-APPROVAL-01` appears in this document.
- The standalone MEG Weather Bot PRD is referenced.
- `PRD-P1-WX-STAGE2-SKELETON-CLOSEOUT-01` is referenced.
- `PRD-P1-WX-STAGE2-SKELETON-01`, `PRD-P1-WX-STAGE2-SKELETON-02`, and `PRD-P1-WX-STAGE2-SKELETON-03` are referenced.
- This is a static fixture/data approval request only.
- Static fixtures are not approved by this document.
- Fixture/data planning has not started.
- Fixture/data implementation has not started.
- No historical-label data, fixtures, generated data, ingestion, connectors, external API calls, scoring, backtesting, runtime behavior, trading, order placement, or autonomy are created or approved.
- Future static fixture/data planning requires separate human approval.
- Future fixture implementation requires separate explicit approval after planning.
