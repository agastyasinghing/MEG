# Stage 2 Historical-Label Static Fixtures

## Purpose

This directory contains a tiny, static, synthetic, hand-authored fixture set for the Weather Bot Stage 2 historical-label skeleton. The fixtures exist only to exercise supplied-metadata validation expectations in tests.

## Fixture directory allowlist

The only approved directory for this first fixture implementation is:

`tests/fixtures/weather/stage2_historical_labels/`

No fixture files outside this directory are approved by this fixture implementation.

## Fixture files

Exactly three JSON fixture files are in scope:

- `synthetic_valid_source_backed_confirmed.json`
- `synthetic_blocked_missing_provenance.json`
- `synthetic_unclear_requires_adjudication.json`

## Synthetic-only posture

All fixtures in this first implementation are marked `synthetic`. They are not real historical labels, not provider records, not fetched records, and not generated data. They use placeholder canonical identifiers and reviewer-readable notes only.

## No-lookahead rule

Each fixture must include a nonempty `no_lookahead_notes` field explaining that the static example does not rely on later observations to determine the supplied label posture.

## Provenance and reviewer note rule

Each fixture must include nonempty `provenance_notes` and `reviewer_notes` fields. These notes explain why the fixture is usable or blocked for static validation only and must not be treated as source collection or production evidence.

## Static-test-only rule

The fixture files are read only by static tests. This directory does not define a runtime loader, ingestion path, source adapter, service client, configuration path, or production data interface.

## Explicit non-approval boundaries

This fixture implementation does not approve or create:

- no ingestion
- no provider/API connectors
- no external API calls
- no credentials/secrets/config loading
- no forecast pulls
- no scoring/backtesting/runtime/trading/order placement/autonomy
- no production behavior
