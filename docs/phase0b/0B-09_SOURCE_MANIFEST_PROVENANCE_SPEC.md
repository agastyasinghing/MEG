# Phase 0B-09 — Source Manifest and Fixture Provenance Spec

## 1) Purpose

This ticket defines the documentation standard for **source provenance before import** in Phase 0B.

This spec establishes:

- how future historical sources must be recorded before any loader ticket starts,
- how fixture artifacts must record lineage back to an approved source record,
- and how provenance review remains isolated from runtime/shared-rail execution behavior.

This is a **research-lake governance spec**, not a runtime spec:

- it applies to DuckDB/Parquet historical research ingestion planning,
- it does not alter Redis channels, Postgres operational journaling contracts, or Telegram approval flow,
- and it does not introduce strategy logic or live/paper execution changes.

## 2) Manifest record schema (required for each candidate source)

Every candidate historical source must have a manifest record with the following fields before import design work proceeds.

| Field | Required | Description |
|---|---:|---|
| `source_id` | yes | Stable internal identifier for the source record (for example `poly_trades_archive_v1`). |
| `source_name` | yes | Human-readable source name. |
| `source_type` | yes | Source class (repo snapshot, local archive, API export, capture stream, curated labels, reference metadata). |
| `origin_url_or_path` | yes | Canonical origin reference (URL, git reference, or local path). |
| `acquisition_method` | yes | How bytes/records were obtained (manual download, scripted export, filesystem handoff, API capture). |
| `acquired_at` | yes | UTC timestamp when the source snapshot was acquired. |
| `snapshot_date_range` | yes | Time interval represented by the source records (start/end UTC). |
| `expected_format` | yes | Declared container/encoding (parquet, csv, jsonl, ndjson, mixed bundle, repo files). |
| `expected_size_bytes` | yes | Estimated byte size for planning and guardrails. |
| `checksum_strategy` | yes | Hashing plan (for example whole-file SHA256, partition-level checksum, manifest hash set). |
| `license_or_terms_status` | yes | Review status for license/terms (approved, pending review, restricted, rejected). |
| `allowed_use` | yes | Explicit allowed use in MEG context (local inspection only, research-only transform, internal fixture derivation). |
| `refresh_policy` | yes | Whether source is one-off snapshot or periodic refresh, including cadence/owner. |
| `owner_reviewer` | yes | Accountable owner/reviewer pair for provenance and terms signoff. |
| `import_priority` | yes | Planned order of import evaluation (P0/P1/P2 or numeric rank). |
| `notes` | no | Freeform caveats, quality concerns, mapping assumptions, and blockers. |

### Manifest status rule

A source is not eligible for loader ticketing unless:

1. all required fields are present,
2. checksum strategy is defined,
3. license/terms status is explicitly reviewed,
4. and allowed use is compatible with intended Phase 0B research scope.

## 3) Fixture provenance schema (required for each committed fixture)

Every fixture committed for Phase 0B research tests/CLI must include a provenance record with the fields below.

| Field | Required | Description |
|---|---:|---|
| `fixture_id` | yes | Stable fixture identifier. |
| `fixture_path` | yes | Repository path for fixture artifact. |
| `derived_from_source_id` | yes | Reference to manifest `source_id` used to derive the fixture. |
| `rows` | yes | Expected row count. |
| `columns` | yes | Expected ordered column list (or equivalent schema signature reference). |
| `checksum` | yes | Fixture checksum used for deterministic validation. |
| `purpose` | yes | Why this fixture exists (loader smoke, lead-lag query smoke, report CLI smoke, schema regression guard). |
| `expected_test_modules` | yes | Test modules/commands expected to consume this fixture. |
| `regeneration_instructions` | yes | Deterministic steps to regenerate fixture from approved source subset. |

### Fixture provenance rule

No new fixture should be added unless it can be traced to a reviewed source manifest record via `derived_from_source_id`.

## 4) Source categories covered by this spec

This manifest/provenance policy must cover the following candidate source families:

1. `Jon-Becker/prediction-market-analysis` source materials.
2. Local ~36 GiB Polymarket/Kalshi historical archive (if available in local environment).
3. Polymarket market metadata sources.
4. Polymarket trade/fill history sources.
5. Kalshi market/time-series sources.
6. CLOB/order-book snapshot sources.
7. Wallet-level trade activity datasets.
8. Manual wallet label sources.
9. External outcome/resolution metadata sources.

## 5) License and data-safety rules

The following controls are mandatory for Phase 0B source intake:

1. **No vendored external repositories without explicit review.**
2. **No committing large datasets** to the MEG repository.
3. **No committing `.duckdb` files** or derived local database artifacts.
4. **No coupling to Redis, Postgres, or runtime execution rails** from this research manifest process.
5. **Unknown-license or unresolved-terms data cannot move beyond local inspection** and cannot be used for import tickets.
6. **Source rights and provenance must be documented before loader implementation tickets** are opened.

## 6) Suggested manifest location (future implementation, not this ticket)

This ticket is spec-only. Suggested future artifact locations:

- `docs/phase0b/source_manifest.example.yaml` (example contract file), and/or
- `data/manifest/` for local operational manifests in later tickets.

For this ticket:

- do not add manifest data files,
- do not add source snapshots,
- and do not add generated outputs.

## 7) Validation checklist before any import

Before a source proceeds to import implementation, run and record:

1. checksum verification,
2. row-count estimate/reconciliation,
3. schema fingerprint capture,
4. timestamp range validation,
5. duplicate key scan,
6. canonical identifier coverage check (`condition_id`, `token_id`, `outcome`),
7. source/license review completion.

## 8) Non-goals

This ticket does not include:

1. real source import,
2. DuckDB loader expansion,
3. ingestion of the ~36 GiB archive,
4. external repository vendoring,
5. runtime/shared-rail/trading behavior changes,
6. execution approval-model changes.

## 9) Recommended next ticket

Recommended follow-up:

- **Phase 0B-10: Source manifest example YAML**

Alternative if review-first sequencing is preferred:

- **Phase 0B-10: Jon-Becker/local archive source review checklist**
