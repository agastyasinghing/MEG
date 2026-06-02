# PRD-P1-WX-STAGE2-REAL-FIXTURE-IMPLEMENTATION-01 — Real Source-Backed Fixture Implementation

Canonical ID: PRD-P1-WX-STAGE2-REAL-FIXTURE-IMPLEMENTATION-01

## 1. Status and scope

Status: implemented as a narrow static fixture ticket.

Scope is real source-backed fixture implementation only. This ticket created two static JSON fixture candidates, a README, this implementation PRD, and a standard-library static validation test. At most 3 real source-backed fixture JSON files were allowed, at most 3 real source-backed fixture JSON files were created, and no generated data was created.

## 2. Strategic framing

Stage 2 needs reviewable examples that prove the supplied-metadata validation skeleton can represent real venue/source evidence without creating ingestion, connectors, live calls, or production behavior. The fixtures are deliberately tiny so source review remains practical.

## 3. Stage ladder position

This ticket follows the Stage 2 skeleton closeout, synthetic fixture implementation, synthetic fixture closeout, active-state checkpoint, real fixture approval request, real fixture planning, and real fixture implementation approval request. It remains inside the static historical-label fixture track only.

## 4. Human approval basis

The user separately approved real source-backed fixture implementation only. That approval does not approve ingestion, provider/API connectors, external API calls from runtime code, forecast pulls, scoring/backtesting/runtime/trading/order placement/autonomy, historical-label loading, or production behavior.

## 5. Real source-backed fixture implementation boundary

Implemented boundary:

- Static Markdown documentation.
- Static JSON fixture candidates under the allowlisted fixture directory.
- Static validation tests under `tests/core`.
- No production source changes.
- No runtime loader.
- No generated data.

## 6. Source-backed research basis

Targeted source review used public pages available on 2026-06-02:

- Polymarket NYC May 2026 precipitation market page: `https://polymarket.com/event/precipitation-in-nyc-in-may`.
- Polymarket NYC May 12, 2026 temperature market page: `https://polymarket.com/event/highest-temperature-in-nyc-on-may-12-2026?marketSlug=highest-temperature-in-nyc-on-may-12-2026-64-65f&outcomeIndex=1`.
- Polymarket US Weather FAQ: `https://docs.polymarket.us/faqs/weather-faqs`.
- Kalshi HIGH contract terms as a venue-rule comparator for NWS Daily Climate Report usage: `https://kalshi-public-docs.s3.amazonaws.com/contract_terms/HIGH.pdf`.

The implementation did not fetch or scrape data with code. The static source notes were hand-authored from browser-reviewed public evidence.

## 7. Fixture directory allowlist

Fixture directory: `tests/fixtures/weather/stage2_real_source_backed_labels/`.

No files outside this directory are fixture outputs for this ticket.

## 8. Fixture inventory

| fixture file path | source identity | source name | source locator | access date | venue rule reference | resolver source identity | expected validation posture | reviewer note summary | no-lookahead summary | confidence/status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `tests/fixtures/weather/stage2_real_source_backed_labels/polymarket_nyc_may_2026_precipitation_less_than_2_no.json` | polymarket_nyc_may_2026_precipitation_market_page | Polymarket NYC May 2026 precipitation market page | `https://polymarket.com/event/precipitation-in-nyc-in-may` | 2026-06-02 | Polymarket page Rules and Market Context sections naming NOAA monthly summarized Central Park NY precipitation as source | Polymarket resolver 0x69c47De9D... displayed on the venue page | pass | Venue page displayed rule source, resolver identity, no-dispute state, and final No outcome for the selected less-than-2-inch candidate token | Reviewed after the May 2026 measurement window and page final label display, so this is settlement-review evidence | confirmed |
| `tests/fixtures/weather/stage2_real_source_backed_labels/polymarket_nyc_may_12_2026_temperature_conflict.json` | polymarket_nyc_may_12_2026_temperature_market_page | Polymarket NYC May 12, 2026 temperature market page | `https://polymarket.com/event/highest-temperature-in-nyc-on-may-12-2026?marketSlug=highest-temperature-in-nyc-on-may-12-2026-64-65f&outcomeIndex=1` | 2026-06-02 | Polymarket page Rules section naming LaGuardia Airport Station and Wunderground KLGA daily history | Polymarket resolver 0x69c47De9D... displayed on the venue page | blocked | Venue page has reviewable evidence but mixed station/source summary language requires adjudication | Reviewed after the event; because source identity is ambiguous, the fixture remains blocked rather than pass | unclear |

Only two fixture files were created because these two public examples safely cover one pass posture and one blocked conflict posture. A third fixture was not added because the ticket forbids fabricating variety merely to fill the cap.

## 9. Fixture schema/data-shape implemented

Each fixture includes:

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
- `source_identity`
- `source_name`
- `source_locator`
- `access_date`
- `venue_rule_reference`
- `resolver_source_identity`
- `reviewer_notes`
- `provenance_notes`
- `no_lookahead_notes`
- `conflicting_source_notes`
- `non_approval_notes`

The nested `source_resolution`, `point_in_time_provenance`, and `label_usability` mappings use the existing Stage 2 skeleton field names and closed values.

## 10. Source/provenance summary

The precipitation fixture is source-backed by the public venue page's displayed rule, resolver, no-dispute state, and final No outcome for the selected token. The temperature conflict fixture is source-backed as an edge case by the public venue page's rule/source text and mixed summary language.

## 11. Access-date summary

All fixture source notes use access date `2026-06-02`, the date of targeted source review.

## 12. Venue-rule compatibility summary

The fixtures retain the venue's named source-rule text in `venue_rule_summary` and `venue_rule_reference`. The precipitation candidate uses the venue page's NOAA monthly summarized Central Park NY rule. The temperature conflict candidate uses the venue page's LaGuardia/Wunderground rule while marking mixed source wording as blocked.

## 13. Point-in-time/no-lookahead summary

The pass fixture is reviewed after the May 2026 measurement window and after the venue page displayed final label evidence. The blocked fixture is reviewed after the May 12, 2026 event but remains blocked because the source identity is ambiguous. Neither fixture claims pre-event availability or uses later evidence to make a trading decision.

## 14. Reviewer/adjudication summary

Reviewer notes are fixture-local and advisory. The precipitation candidate needs no adjudication for static skeleton validation. The temperature candidate requires adjudication before any real label could be treated as confirmed.

## 15. Relationship to Stage 2 skeleton validation

The fixtures are adapted into `historical_label_metadata_from_mapping` and checked with `validate_historical_label_metadata`. The pass fixture supplies `source_resolved`, `source_backed`, `available_as_of`, `usable_after_stage_2_approval`, and `confirmed`. The blocked fixture supplies conflict and adjudication values so the skeleton fails closed.

## 16. Static validation tests

`tests/core/test_prd_p1_wx_stage2_real_fixture_implementation_01.py` validates PRD existence, README existence, fixture count, required keys, closed values, identifier prefixes, source evidence fields, ISO access dates, expected posture alignment with the skeleton validator, PRD confidence/status closed values, source-placeholder rejection, secret-token rejection, and allowlisted file-change boundaries.

## 17. Explicit non-approval boundaries

This implementation does not create or approve:

- generated data
- ingestion
- provider/API connectors
- external API calls from runtime code
- credentials/secrets/config loading
- forecast pulls
- scoring/backtesting/runtime/trading/order placement/autonomy
- production behavior
- historical-label loading readiness
- ingestion readiness
- scoring readiness
- runtime readiness
- production readiness
- trading readiness

For avoidance of doubt: no generated data was created; no ingestion was created; no provider/API connectors were created; no external API calls from runtime code were created; no credentials/secrets/config loading was created; no forecast pulls were created; and no scoring/backtesting/runtime/trading/order placement/autonomy were created. Fixture implementation does not imply historical-label loading readiness, ingestion readiness, scoring readiness, runtime readiness, production readiness, or trading readiness.

## 18. What remains unbuilt

Historical-label loading remains unbuilt. Ingestion remains unbuilt. Provider/API connectors remain unbuilt. Forecast pulls remain unbuilt. Scoring/backtesting remains unbuilt. Runtime observation remains unbuilt. Trading, order placement, and autonomy remain unbuilt.

## 19. Future gates

future historical-label loading requires separate explicit approval. future ingestion requires separate explicit approval. future scoring/backtesting requires separate explicit approval. future runtime/trading requires separate explicit approval.

## 20. Acceptance criteria

- Implementation PRD exists and contains the canonical ID.
- README exists under the real source-backed fixture directory.
- Fixture directory contains between 1 and 3 JSON files.
- Every fixture is static, hand-authored, and source-backed.
- Every fixture has required source, provenance, no-lookahead, reviewer, conflict, expected posture, and non-approval notes.
- Fixture JSON files are compatible with the existing Stage 2 skeleton mapping builder and validator.
- No production source modules are modified.
- No generated data is created.
- No ingestion, provider/API connectors, external runtime calls, credential loading, forecast pulls, scoring/backtesting/runtime/trading/order placement/autonomy, or production behavior is created.

## 21. Later-ticket handoff

Recommended next ticket is a real source-backed fixture implementation closeout/checkpoint, or targeted validation/source-evidence refinement only if a concrete source-evidence gap is found. Do not proceed to ingestion, scoring/backtesting, runtime, or trading without separate explicit approval.
