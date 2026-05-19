# Phase 0B-08 — Research CLI Usage (Fixture Smoke)

## Purpose

This document explains how to run the **Phase 0B fixture research smoke flow locally**.

Scope of this flow:

- local fixture research smoke only,
- not live trading,
- not connected to Redis, Postgres, or execution rails.

## Setup

Install development dependencies:

```bash
python -m pip install -r requirements-dev.txt
```

Verify DuckDB import/version:

```bash
python -c "import duckdb; print(duckdb.__version__)"
```

## Run the Phase 0B fixture report CLI

Default fixture inputs:

```bash
python -m meg.research.duckdb_lake.cli --output /tmp/fixture_lead_lag_report.json
```

Optional forward horizon override:

```bash
python -m meg.research.duckdb_lake.cli \
  --output /tmp/fixture_lead_lag_report.json \
  --horizon-ms 600000
```

Optional explicit fixture/data paths:

```bash
python -m meg.research.duckdb_lake.cli \
  --fills-csv tests/fixtures/phase0b/normalized_fills_sample.csv \
  --snapshots-csv tests/fixtures/phase0b/price_snapshots_sample.csv \
  --output /tmp/fixture_lead_lag_report.json
```

## Run research tests

```bash
python -m pytest -q tests/research/test_duckdb_loader.py
python -m pytest -q tests/research/test_lead_lag_queries.py
python -m pytest -q tests/research/test_fixture_report.py
python -m pytest -q tests/research/test_fixture_report_cli.py
python -m pytest -q tests/core/test_static_canonical_ids.py
```

## Expected output

The CLI writes a JSON report containing:

- `report_name`,
- `generated_from="fixture"`,
- `horizon_ms`,
- `fills_analyzed`,
- `fills_with_future_price`,
- `average_forward_return_bps`,
- `rows`.

## Git/data hygiene

- Do not commit generated reports.
- Do not commit `.duckdb` files.
- Do not commit large data files.
- Use temporary output paths (for example `/tmp/...`) or ignored repository paths such as `data/exports/`.

## CI smoke coverage

The workflow `.github/workflows/phase0b-research-smoke.yml` runs this smoke scope in CI.

It:

- installs `requirements-dev.txt`,
- verifies DuckDB import/version,
- runs the Phase 0B research smoke test set.

## Non-goals

This ticket/flow does not include:

- full ~36 GiB historical import,
- external repository vendoring,
- live strategy/scoring changes,
- execution or approval-model changes.

## Recommended next ticket

Phase 0B-09:

- source manifest / fixture provenance spec, **or**
- first real source manifest for Jon-Becker/local historical archive (docs-only).
