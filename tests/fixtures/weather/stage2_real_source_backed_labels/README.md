# Stage 2 Real Source-Backed Weather Label Fixtures

## Purpose

This directory contains a tiny capped set of static, hand-authored Stage 2 Weather Bot historical-label fixture candidates backed by public source evidence reviewed on 2026-06-02. The files exist only to exercise the supplied-metadata Stage 2 validation skeleton against real source-backed candidate shapes.

## Directory allowlist

Allowed directory: `tests/fixtures/weather/stage2_real_source_backed_labels/`.

No fixture, generated record, provider output, or data file outside this directory is part of this implementation.

## Fixture count cap

This directory may contain at most three JSON fixture files for this ticket. This implementation created two because two reviewable public source-backed candidates were sufficient for one pass posture and one blocked conflict posture.

## Fixture files created

- `polymarket_nyc_may_2026_precipitation_less_than_2_no.json`
- `polymarket_nyc_may_12_2026_temperature_conflict.json`

## Source-backed posture

Each JSON file must identify the source identity, source name, source locator, access date, venue rule reference, resolver source identity, reviewer notes, provenance notes, no-lookahead notes, conflict notes, expected validation posture, and non-approval notes.

## Source URL/source-name/access-date rule

Every fixture must include a nonempty `source_name`, `source_locator`, and ISO `access_date`. A vague source name without a stable locator and access date is not acceptable for this directory.

## Venue-rule compatibility rule

Every fixture must include a venue rule reference that can be reviewed against the cited public source. Fixture metadata must remain compatible with the existing Stage 2 supplied-metadata skeleton: `source_resolution`, `point_in_time_provenance`, and `label_usability` use the skeleton's existing field names and closed values.

## No-lookahead rule

Every fixture must explain why the cited evidence was available at the relevant settlement-review point. If availability is ambiguous, the fixture must use a blocked or caution posture rather than pass.

## Provenance/reviewer note rule

Every fixture must include nonempty reviewer, provenance, no-lookahead, and non-approval notes so a human reviewer can understand why the candidate is pass, blocked, or caution without adding runtime behavior.

## Static-test-only rule

These files are static test fixtures only. They are not loaded by production code and do not add any runtime fixture loader.

## Explicit non-approval boundaries

This directory does not approve or implement:

- no ingestion
- no provider/API connectors
- no external API calls from runtime code
- no credentials/secrets/config loading
- no forecast pulls
- no scoring/backtesting/runtime/trading/order placement/autonomy
- no production behavior

These fixtures do not approve historical-label loading.
