# Phase 0B-16 — Local 36 GiB Archive Inspection Plan

## 1) Purpose

This ticket defines a **plan-only** procedure for inspecting a local/downloaded ~36 GiB Polymarket/Kalshi archive before any downstream Phase 0B data work.

This plan explicitly allows:

- read-only inventory and metadata inspection,
- schema reconnaissance on a minimal sample basis,
- provenance/license evidence capture for future review.

This plan explicitly does **not** allow:

- import into MEG research loaders,
- loader expansion,
- fixture derivation,
- runtime/trading behavior changes.

Net impact for this ticket is documentation-only with no runtime, execution, Redis, Postgres, or Telegram approval-flow behavior change.

## 2) Preconditions

Before running archive inspection steps in a follow-up ticket, confirm all preconditions:

1. Archive path is outside the MEG repository working tree.
2. Local disk capacity is sufficient for temporary read-only inspection workflows.
3. Archive/source path is recorded in review notes.
4. A corresponding source entry exists in `docs/phase0b/source_manifest.example.yaml`.
5. License/provenance remains pending until verified by concrete evidence.
6. No generated artifacts are staged/committed into this repository.

## 3) Recommended local paths (outside MEG repository)

Use external local paths for review staging and temporary outputs:

- `~/meg_source_review/`
- `~/meg_source_review/prediction-market-analysis/`
- `~/meg_source_review/archive/`
- `/tmp/meg_archive_inspection/`

These paths are intentionally outside `agastyasinghing/MEG` so large data and temporary analysis artifacts cannot be accidentally committed.

## 4) Read-only command plan

Use read-only shell commands to inventory archive structure and size characteristics.

```bash
pwd
du -sh <archive_or_data_dir>
find <archive_or_data_dir> -maxdepth 4 -type f | sort | head -200
find <archive_or_data_dir> -type f | wc -l
find <archive_or_data_dir> -type f \( -name "*.parquet" -o -name "*.csv" -o -name "*.json" -o -name "*.jsonl" -o -name "*.zst" -o -name "*.tar" \)
find <archive_or_data_dir> -type f | awk -F. 'NF>1 {print tolower($NF)}' | sort | uniq -c | sort -nr
```

Checksum guidance (archive files only, when practical):

```bash
sha256sum <archive_file>
# or on systems without sha256sum:
shasum -a 256 <archive_file>
```

Checksum scope rule:

- Do not hash every file in a full ~36 GiB subtree by default.
- Hash only top-level archive bundles or selected files unless an intentional full-hash plan is approved.

## 5) Dataset layout checks

During inspection, verify presence/absence of expected dataset family paths referenced by prior Jon-Becker review context:

- `data/kalshi/markets`
- `data/kalshi/trades`
- `data/polymarket/blocks`
- `data/polymarket/markets`
- `data/polymarket/trades`
- `data/polymarket/fpmm_trades` (or legacy trades variants, if present)

Record exact discovered paths and note any path/version deviations.

## 6) Schema inspection plan (safe, sample-first)

Use DuckDB in ephemeral mode for schema introspection only (no persistent database files).

Example command pattern:

```bash
duckdb -c "DESCRIBE SELECT * FROM parquet_scan('<path>/*.parquet') LIMIT 0;"
```

Rules for safe schema checks:

1. Inspect one file per dataset family first.
2. Use `DESCRIBE ... LIMIT 0` for column discovery without full scans.
3. Run `SELECT COUNT(*)` only on tiny/sample files, or after estimating scan cost.
4. Run timestamp range queries (`MIN`/`MAX`) only when scan size is confirmed safe.
5. Do not create or commit persistent `.duckdb` files.

Optional sample-only query pattern when safe:

```bash
duckdb -c "SELECT MIN(timestamp), MAX(timestamp) FROM parquet_scan('<single_small_file.parquet>');"
```

## 7) Required fields to look for

For each inspected dataset family, capture whether these fields exist (exact or clearly mappable names):

- `condition_id`
- `token_id` or `clob_token_ids` / asset IDs
- `outcome` / `outcomes`
- maker / taker
- wallet/address fields
- timestamp / created_time / block timestamp
- price / yes_price / no_price
- side / taker_side
- size / count / amount fields
- resolution/result fields
- legacy market identifier fields

## 8) Evidence to capture in follow-up results

The follow-up inspection-results ticket should include:

1. Archive path
2. Total size
3. File count
4. Extension summary
5. Top-level tree
6. Dataset family paths found
7. Sample schema outputs
8. Timestamp range (if safely available)
9. Checksum strategy used
10. License/provenance notes
11. Fields observed

## 9) Safety rules

During archive inspection work:

1. Do not commit archive files.
2. Do not commit extracted data.
3. Do not commit `.duckdb` files.
4. Do not commit generated reports.
5. Do not vendor external repositories.
6. Do not run live trading/runtime code.
7. Do not alter Redis/Postgres/runtime rails.
8. Use temporary paths or ignored paths only.

## 10) Decision gates after inspection

After evidence capture, apply these gates:

1. Source manifest update is allowed only if inspection evidence is adequate.
2. Tiny fixture derivation planning is allowed only if license/provenance and schema evidence pass.
3. Loader expansion is allowed only after fixture-derivation planning is complete and approved.
4. If license or provenance remains unclear, stop/hold and do not proceed.

## 11) Non-goals

This ticket does not perform:

- actual archive inspection,
- import,
- loader expansion,
- fixture derivation,
- strategy/scoring changes,
- execution/approval model changes.

## 12) Recommended next ticket

Choose one next step based on local environment readiness:

1. **Phase 0B-17: Manual local archive metadata inspection results**, or
2. **Phase 0B-17: Pause if archive path/storage unavailable**.
