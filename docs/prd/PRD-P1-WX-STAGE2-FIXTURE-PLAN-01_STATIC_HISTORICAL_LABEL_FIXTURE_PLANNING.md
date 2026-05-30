# PRD-P1-WX-STAGE2-FIXTURE-PLAN-01 Static Historical-Label Fixture Planning

Canonical ID: PRD-P1-WX-STAGE2-FIXTURE-PLAN-01

## 1. Status and scope

This is static historical-label fixture planning only for the Stage 2 weather historical-label skeleton. Fixture implementation is not approved. Fixture files are not created. Historical-label data is not created. JSON/YAML/CSV/Parquet fixtures are not created. Generated data is not created.

This document creates no ingestion, no provider/API connectors, no external API calls, no credentials/secrets/config loading, and no forecast pulls. Scoring/backtesting/runtime/trading/order placement/autonomy remain unapproved. Future fixture implementation requires separate explicit human approval.

## 2. Strategic framing

The standalone MEG Weather Bot PRD (`PRD-P1-WX-STANDALONE_WEATHER_BOT_PRD.md`) frames weather markets as venue-defined settlement objects, not generic weather forecasts. This fixture-planning document keeps that framing: any later static fixture would exist to test source-resolution, point-in-time provenance, label usability, and canonical identifier handling before any broader data, scoring, or runtime stage is considered.

The immediate predecessor approval request is `PRD-P1-WX-STAGE2-FIXTURE-APPROVAL-01`, which authorized planning only. This document also follows the Stage 2 closeout checkpoint, `PRD-P1-WX-STAGE2-SKELETON-CLOSEOUT-01`, and remains aligned with the Stage 2 skeleton subphase sequence: `PRD-P1-WX-STAGE2-SKELETON-01`, `PRD-P1-WX-STAGE2-SKELETON-02`, and `PRD-P1-WX-STAGE2-SKELETON-03`.

## 3. Stage ladder position

This ticket sits after the supplied-metadata-only skeleton and after the static fixture/data approval request. It does not move MEG into fixture implementation, historical-label loading, provider integration, scoring, replay, runtime observation, or trading. Fixture planning does not imply ingestion readiness, scoring readiness, runtime readiness, production readiness, or trading readiness.

## 4. Planning authorization boundary

The authorization boundary is narrow: plan what a later static historical-label fixture set would need to prove, how it would be reviewed, and how static validation would guard it. The approval does not permit creating fixture data, creating files in fixture/data directories, adding generated content, implementing ingestion, connecting to providers, loading configuration, or evaluating probabilities.

## 5. Static fixture planning goal

The goal is to define a future fixture contract in prose so a later ticket can request implementation safely. That future contract should be capable of exercising the Stage 2 skeleton's supplied metadata path, canonical identifiers, provenance posture, no-lookahead requirements, and review/adjudication notes without relying on external systems or runtime behavior.

## 6. Fixture purpose and non-purpose

Future static fixtures, if separately approved later, would be intended to document representative historical-label metadata shapes and expected validation posture. They would not prove market edge, source integration, data availability, forecast quality, execution safety, operational readiness, or production suitability.

Non-purpose boundaries are explicit: no historical-label data is created here, no fixture files are created here, no JSON/YAML/CSV/Parquet fixtures are created here, no generated data is created here, and no implementation behavior is authorized here.

## 7. Fixture schema/data-shape planning

A later fixture shape may describe fields in static files only after separate approval. Planning concepts include:

- `fixture_id`: a stable static identifier for the future fixture row or object.
- `fixture_kind`: a closed planning value describing whether the fixture is synthetic, real with required source backing, reviewer-focused, a trap case, blocked, or unclear.
- `synthetic_or_real`: a clear declaration that avoids mixing fabricated examples with source-backed historical cases.
- `canonical_event_summary`: reviewer-readable summary of the venue-defined weather event.
- `venue_rule_summary`: supplied text describing the relevant settlement rule.
- `condition_id` placeholder policy: future fixtures must preserve the canonical identifier contract and avoid routing on any legacy market identifier.
- `token_id` placeholder policy: future fixtures must identify the outcome token placeholder or source-backed token reference according to the fixture type.
- `outcome` placeholder policy: future fixtures must provide the outcome text expected by the Stage 2 skeleton.
- `source_resolution` metadata shape (source_resolution metadata shape): future static metadata describing resolver source identity, status, and evidence status.
- `point_in_time_provenance` metadata shape (point_in_time_provenance metadata shape): future static metadata describing what was available by the relevant decision time.
- `label_usability` metadata shape (label_usability metadata shape): future static metadata describing whether the label is usable, blocked, or unclear for the intended static test.
- `expected_validation_posture`: the planned pass, caution, or block posture expected from the skeleton validation path.
- `reviewer_notes`, `provenance_notes`, and `no_lookahead_notes`: human-readable notes explaining why the future fixture exists and what it must not imply.

These are planning concepts only. They are not fixture records, not examples, and not generated data.

## 8. Synthetic-versus-real fixture distinction

Synthetic examples are acceptable only when the future test needs a shaped metadata object with no claim about a real-world event. A synthetic example must be labeled as synthetic and must not imply source availability, provider integration, or historical truth.

Real examples would require source-backed provenance before real use. A real example must identify how the venue rule, resolver source, settlement window, source availability time, and final label were reviewed. Real examples must not be introduced by inference alone.

## 9. Provenance requirements planning

Future fixtures should carry provenance notes that distinguish source-backed evidence from reviewer inference, missing evidence, conflicts, or non-applicable evidence. For real examples, provenance must be source-backed before real use. For synthetic examples, provenance can be not applicable, but that posture must be explicit.

The provenance plan must avoid implying provider/API integration. Static notes can describe the evidence expected from a reviewer or source packet, but they must not create connectors, external calls, forecast pulls, or configuration loading.

## 10. No-lookahead requirements planning

No-lookahead constraints matter because a label fixture can accidentally encode information that would not have been available at the intended point in time. Future fixtures should separate venue rule information, source-resolution evidence, point-in-time availability, final settlement information, and reviewer adjudication notes.

A future real fixture must document the as-of posture used for review. A synthetic fixture must state that it is not evidence of any actual point-in-time data availability.

## 11. Review/adjudication requirements planning

Future fixture implementation should require human review before any fixture is treated as usable. Review/adjudication notes should identify whether the expected label posture is confirmed, unclear, or unknown; whether source evidence is missing or conflicting; and whether the fixture should be blocked from use.

Reviewer notes must remain documentation for static validation. They must not become permission to ingest, score, simulate, run, trade, place orders, or act without operator approval.

## 12. Future file allowlist planning

If fixture implementation is approved later, that ticket should name every allowed file path before work begins. A future allowlist should distinguish the fixture document, any static test file, and any fixture data file path. This planning ticket does not add or authorize any fixture data path.

The future allowlist should also state forbidden paths, including ingestion, connectors, runtime, trading, execution, infrastructure, workflows, scripts, SQL, migrations, data lakes, generated outputs, secrets, and dependency manifests unless explicitly authorized by that later ticket.

## 13. Static validation requirements planning

A future static validation test should verify that the approved fixture files exist only in the approved paths, use closed values only where closed values are required, preserve the canonical `condition_id`, `token_id`, and `outcome` contract, identify synthetic versus real posture, include provenance and no-lookahead notes, and avoid provider/API, scoring, runtime, and trading claims.

Static validation should parse machine-readable assignments from bounded sections rather than scanning prose for ordinary words. Static validation should not treat forbidden examples in documentation as actual values.

## 14. Relationship to Stage 2 skeleton validation

The Stage 2 skeleton accepts supplied metadata and validates closed metadata postures. Future fixtures should exercise that supplied-metadata-only path without modifying `meg/weather/stage2/historical_label.py` and without changing the existing skeleton tests unless a later ticket explicitly approves a static-test convention update.

The future fixture plan must remain compatible with `PRD-P1-WX-STAGE2-SKELETON-01`, `PRD-P1-WX-STAGE2-SKELETON-02`, and `PRD-P1-WX-STAGE2-SKELETON-03` by preserving fail-closed behavior and static metadata review boundaries.

## 15. Explicit non-approval boundaries

This planning document does not approve historical-label data, fixtures or generated data, ingestion, provider integration, connectors, external API calls, credentials/secrets/config loading, forecast pulls, model scoring, probability scoring, backtesting, paper simulation, runtime observation, trading/order/autonomy behavior, production behavior, or C++/Rust runtime components.

Fixture implementation is not approved. Future fixture implementation requires separate explicit human approval.

## 16. Closed Stage 2 fixture-planning vocabulary

Closed assignment categories for this planning document are fixture planning stage, planning status, fixture kind, fixture planning scope, fixture implementation boundary, fixture data posture, non-approval category, evidence status, and label confidence. Actual closed values are assigned only in the machine-checkable section below.

## 17. Forbidden Stage 2 fixture-planning values

The following examples are forbidden as actual machine-checkable values for this document. They are documented here so the static test can confirm they are not parsed as actual assignments:

- planning_only/fixture_implementation_not_started
- not_implemented/separate_approval_required
- synthetic_example/real_example_requires_source_backing
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
- approved_for_fixtures
- approved_for_ingestion
- approved_for_runtime
- approved_for_scoring
- approved_for_trading
- trade_ready
- auto_execute
- autonomous
- live
- production

## Machine-checkable Stage 2 fixture-planning assignments

- fixture planning stage: stage_2_static_historical_label_fixture_planning
- planning status: planning_only
- planning status: fixture_implementation_not_started
- planning status: human_approval_limited_to_planning
- planning status: blocked_pending_fix
- planning status: unclear
- fixture kind: synthetic_example
- fixture kind: real_example_requires_source_backing
- fixture kind: reviewer_edge_case
- fixture kind: trap_case
- fixture kind: blocked_case
- fixture kind: unclear_case
- fixture planning scope: fixture_schema_shape_planning
- fixture planning scope: synthetic_real_distinction_planning
- fixture planning scope: provenance_requirement_planning
- fixture planning scope: no_lookahead_requirement_planning
- fixture planning scope: review_adjudication_planning
- fixture planning scope: static_validation_planning
- fixture planning scope: file_allowlist_planning
- fixture planning scope: no_ingestion_no_runtime_no_scoring
- fixture implementation boundary: not_implemented
- fixture implementation boundary: separate_approval_required
- fixture implementation boundary: explicitly_out_of_scope
- fixture implementation boundary: blocked
- fixture data posture: no_fixture_data_created
- fixture data posture: no_generated_data_created
- fixture data posture: planning_only
- fixture data posture: provenance_required_before_real_use
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
- evidence status: missing
- evidence status: conflicting
- evidence status: not_applicable
- label confidence: confirmed
- label confidence: unclear
- label confidence: unknown

## 19. Fixture planning matrix

| Planning area | Future expectation | Boundary |
| --- | --- | --- |
| Schema/data shape | Define static metadata fields and expected validation posture. | Planning only; no fixture records. |
| Synthetic examples | Use only for shaped validation cases with no real-world claim. | Must not imply source-backed evidence. |
| Real examples | Require source-backed provenance and review before use. | Must not be created by this ticket. |
| Provenance | Separate source-backed, reviewer-inferred, missing, conflicting, and non-applicable posture. | Must not imply provider integration. |
| No-lookahead | Identify what would have been knowable at the relevant point in time. | Must not encode future information as earlier evidence. |
| Review/adjudication | Require human reviewer notes before use. | Must not approve runtime or action. |
| File allowlist | Name allowed future paths before implementation. | No fixture path is approved here. |
| Static validation | Parse bounded assignment sections and closed values. | Must not parse forbidden examples as assignments. |

## 20. If approved later, fixture implementation boundaries

If approved later, fixture implementation should remain static, minimal, and file-allowlisted. It should create only the files named by that later approval, include no generated data unless separately approved, avoid provider/API integration, avoid scoring or replay claims, and preserve the canonical identifier contract.

That future approval should state whether synthetic examples, real source-backed examples, reviewer edge cases, trap cases, blocked cases, or unclear cases are allowed.

## 21. Relationship to future ingestion

Future ingestion is not created and is not approved. Static fixture planning is not ingestion readiness and must not be described as ready for ingestion. A later ingestion ticket would need separate authorization, source contracts, failure-mode handling, and review gates.

## 22. Relationship to future scoring/backtesting

Future scoring and backtesting are not created and are not approved. Fixture planning is not scoring readiness and is not backtest readiness. Future fixtures, if approved, should test metadata and validation posture, not model quality, probability quality, performance, or replay outcomes.

## 23. Relationship to future runtime/trading

Future runtime observation, trading, order placement, position sizing, and autonomy are not created and are not approved. Fixture planning is not runtime readiness, production readiness, or trading readiness. Nothing here changes MEG's operator-approval requirement.

## 24. Later-ticket handoff

A later ticket may request approval to implement static fixture files only if it repeats the non-approval boundaries, names an explicit file allowlist, avoids external calls, preserves `condition_id`, `token_id`, and `outcome`, and defines static validation before data is added.

The recommended next ticket, if the user wants to proceed, is a static fixture implementation approval request only. It should not implement fixtures, ingestion, scoring, backtesting, runtime, or trading.

## 25. Acceptance criteria

- The document includes canonical ID `PRD-P1-WX-STAGE2-FIXTURE-PLAN-01`.
- The document states that this is static historical-label fixture planning only.
- Fixture implementation is not approved.
- Fixture files are not created.
- Historical-label data is not created.
- JSON/YAML/CSV/Parquet fixtures are not created.
- Generated data is not created.
- Ingestion is not created.
- Provider/API connectors are not created.
- External API calls are not created.
- Credentials/secrets/config loading is not created.
- Forecast pulls are not created.
- Scoring/backtesting/runtime/trading/order placement/autonomy remain unapproved.
- Future fixture implementation requires separate explicit human approval.
- Fixture planning does not imply ingestion readiness, scoring readiness, runtime readiness, production readiness, or trading readiness.
- The machine-checkable section includes every allowed closed-set value and only allowed assignment values.
