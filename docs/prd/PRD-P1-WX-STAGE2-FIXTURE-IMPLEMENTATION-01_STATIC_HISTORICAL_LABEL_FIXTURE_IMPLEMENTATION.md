# PRD-P1-WX-STAGE2-FIXTURE-IMPLEMENTATION-01 Static Historical-Label Fixture Implementation

Canonical ID: PRD-P1-WX-STAGE2-FIXTURE-IMPLEMENTATION-01

## 1. Status and scope

This is static fixture implementation only for the Weather Bot Stage 2 historical-label skeleton. The implementation creates three tiny JSON fixture files, one fixture README, this implementation PRD, and static tests. It creates no real historical-label data and no generated data.

## 2. Strategic framing

The standalone Weather Bot PRD frames weather markets as venue-defined settlement objects rather than generic weather forecasts. This fixture implementation preserves that framing by testing supplied source-resolution, point-in-time provenance, label-usability, and canonical identifier metadata without creating any data collection process.

## 3. Stage ladder position

This ticket follows the Stage 2 skeleton, skeleton validation refinements, skeleton closeout, static fixture approval request, static fixture planning, and static fixture implementation approval request. It remains before any data loading, provider integration, scoring, replay, runtime, production, or execution stage.

## 4. Human approval basis

The human operator separately approved static fixture implementation only. That approval is limited to the allowlisted static files and does not approve ingestion, provider/API connectors, external API calls, forecast pulls, scoring/backtesting/runtime/trading/order placement/autonomy, production behavior, or live data processes.

## 5. Static fixture implementation boundary

The implementation boundary is limited to static, synthetic, hand-authored examples and static validation tests. The fixture files are not scraped, not fetched, not generated from external data, and not presented as real historical labels.

No runtime fixture loader, source connector, service client, credential path, configuration loader, forecast pull, probability evaluator, replay harness, operational observer, trade path, or production behavior is created.

## 6. Fixture directory allowlist

The only fixture directory approved by this implementation is:

`tests/fixtures/weather/stage2_historical_labels/`

No other fixture, data, generated, notebook, archive, research-output, SQL, migration, script, workflow, dependency, or secret path is approved.

## 7. Fixture inventory

Exactly three JSON fixtures are implemented:

- `tests/fixtures/weather/stage2_historical_labels/synthetic_valid_source_backed_confirmed.json`
- `tests/fixtures/weather/stage2_historical_labels/synthetic_blocked_missing_provenance.json`
- `tests/fixtures/weather/stage2_historical_labels/synthetic_unclear_requires_adjudication.json`

The valid fixture is expected to pass Stage 2 supplied-metadata validation. The missing-provenance fixture is expected to be blocked. The unclear/adjudication fixture is expected to be blocked, not passed.

## 8. Fixture schema/data-shape implemented

Each fixture includes these top-level keys:

- `fixture_id`
- `fixture_kind`
- `synthetic_or_real`
- `canonical_event_summary`
- `venue_rule_summary`
- `condition_id`
- `token_id`
- `outcome`
- `source_resolution`
- `point_in_time_provenance`
- `label_usability`
- `expected_validation_posture`
- `reviewer_notes`
- `provenance_notes`
- `no_lookahead_notes`
- `non_approval_notes`

The nested `source_resolution`, `point_in_time_provenance`, and `label_usability` objects use the field names and closed values expected by the Stage 2 skeleton mapping builder and validator.

## 9. Synthetic-only posture

All implemented fixtures use `synthetic_or_real: synthetic`. They use synthetic placeholder `condition_id` and `token_id` values and do not represent real venues, real resolver records, real historical labels, provider records, or live market data.

## 10. Provenance and no-lookahead notes

Each fixture includes nonempty `provenance_notes` and `no_lookahead_notes`. These notes are reviewer-readable safeguards that explain the supplied static metadata posture and prohibit using later observations to repair or infer label status.

## 11. Reviewer/adjudication notes

Each fixture includes nonempty `reviewer_notes`, and each nested metadata object includes a reviewer note where relevant. The unclear fixture documents why adjudication is required before any label could be treated as usable.

## 12. Relationship to Stage 2 skeleton validation

The fixtures are compatible with `meg/weather/stage2/historical_label.py` by adapting only the skeleton-relevant fields into the existing mapping builder. Fixture-only notes remain static documentation and are not production inputs.

The valid fixture supplies `source_resolved`, `available_as_of`, `source_backed`, `confirmed`, `usable_after_stage_2_approval`, a nonblank venue rule summary, and a nonblank resolver source identity. The blocked fixtures deliberately supply missing, conflicting, unavailable, ambiguous, unknown, unclear, or adjudication-required metadata so the skeleton fails closed.

## 13. Static validation tests

The static test file `tests/core/test_prd_p1_wx_stage2_fixture_implementation_01.py` verifies the implementation PRD, fixture directory, README, exact fixture inventory, JSON parseability, required top-level keys, synthetic-only posture, unique fixture IDs, synthetic canonical identifier prefixes, absence of legacy identifier fields, absence of provider/API URLs, nonempty reviewer/provenance/no-lookahead/non-approval notes, and expected Stage 2 validation posture.

The tests read only allowlisted static fixture files with Python standard-library file and JSON helpers. They do not create runtime loading APIs or production fixture loaders.

## 14. Explicit non-approval boundaries

This fixture implementation does not create or approve:

- real historical-label data
- generated data
- ingestion
- provider/API connectors
- external API calls
- credentials/secrets/config loading
- forecast pulls
- scoring/backtesting/runtime/trading/order placement/autonomy
- production behavior

Fixture implementation does not imply ingestion readiness, scoring readiness, runtime readiness, production readiness, or trading readiness.

## 15. What remains unbuilt

Historical-label ingestion remains unbuilt. Provider/source integration remains unbuilt. Forecast retrieval remains unbuilt. Scoring and replay remain unbuilt. Runtime observation remains unbuilt. Trading, execution, order placement, position sizing, and autonomy remain unbuilt. Production behavior remains unbuilt.

## 16. Future gates

Future ingestion/loading requires separate explicit approval. Future scoring/backtesting requires separate explicit approval. Future runtime/trading requires separate explicit approval. Any move from synthetic static examples to real source-backed historical labels requires a separate approval gate and review of provenance, source identity, no-lookahead controls, and safety boundaries.

## 17. Acceptance criteria

- The canonical ID `PRD-P1-WX-STAGE2-FIXTURE-IMPLEMENTATION-01` appears in this PRD.
- The fixture directory exists at the allowlisted path only.
- The README exists and documents purpose, allowlist, fixture inventory, synthetic-only posture, no-lookahead rules, provenance/reviewer notes, static-test-only use, and non-approval boundaries.
- Exactly three allowlisted JSON fixture files exist.
- All fixture files are static, synthetic, hand-authored examples.
- No real historical-label data is created.
- No generated data is created.
- The valid fixture passes Stage 2 supplied-metadata validation.
- The blocked and unclear/adjudication fixtures do not pass Stage 2 supplied-metadata validation.
- Static tests prove fixture shape and non-runtime/non-ingestion posture.
- No production source modules, workflows, scripts, SQL, migrations, dependencies, secrets, or generated outputs are modified.
