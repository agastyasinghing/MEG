# Phase 0B-13 — Jon-Becker / Local Archive Review Record (Pending Placeholder)

## 1) Purpose

This document records manual source review findings for `Jon-Becker/prediction-market-analysis` and status for the local Polymarket/Kalshi archive candidate source.

- Completed partial review for repository snapshot findings.
- Local archive remains pending/unavailable in this ticket.
- No import authorization.
- No loader expansion.
- No runtime/shared-rail/trading impact.

## 2) Review metadata

| Field | Value |
|---|---|
| `reviewer` | `operator local read-only inspection` |
| `review_date` | `2026-05-19` |
| `target_source` | `Jon-Becker/prediction-market-analysis and local Polymarket/Kalshi archive placeholder` |
| `source_id_references` | `jon_becker_prediction_market_analysis_snapshot`; `local_poly_kalshi_historical_archive_placeholder` |
| `local_path_or_url` | `https://github.com/Jon-Becker/prediction-market-analysis.git` |
| `git_commit_or_snapshot_id` | `f3ab641264d9acbedb72b5db9040bc9d078d5ff0` |
| `review_status` | `completed_partial` |

## 3) Source inventory findings

### 3.1 Inventory summary

| Item | Finding | Evidence (command/path) | Notes |
|---|---|---|---|
| File count | `110` | `operator local read-only inspection notes` | `shallow clone inspection` |
| Total size | `2.0M` | `operator local read-only inspection notes` | `repository clone size only` |
| Top-level directories | `docs/`; `scripts/`; `src/`; `tests/` | `operator local read-only inspection notes` | `aligned with discovered important files` |
| Detected file formats | `md`, `py`, `toml`, `sh`, `mk`, repo text/code assets | `docs/ANALYSIS.md`; `docs/SCHEMAS.md`; repo file inventory notes | `documented at repository level only` |
| Candidate parquet/csv/json/jsonl files | `none committed in shallow clone` | `operator shallow inspection notes` | `no committed dataset payload files identified` |
| Notebooks/scripts | `scripts/download.sh` | `operator local read-only inspection notes` | `script present; no data import performed` |
| README/license files | `README.md`; `LICENSE`; `Makefile`; `pyproject.toml` | `operator local read-only inspection notes` | `core repo metadata/build files present` |
| Manifest/provenance files (if present) | `not confirmed in this ticket` | `inspection scope notes` | `dataset/archive provenance remains pending` |

### 3.2 Candidate files list

| Path | Format | Size | Candidate use | Include in follow-up? |
|---|---|---:|---|---|
| `docs/ANALYSIS.md` | `markdown` | `not recorded` | `analysis approach and query-method evidence` | `yes` |
| `docs/SCHEMAS.md` | `markdown` | `not recorded` | `schema/canonical identifier evidence for planning` | `yes` |
| `scripts/download.sh` | `shell` | `not recorded` | `future provenance review context only` | `yes, review-only` |
| `src/indexers/kalshi/*` | `python` | `not recorded` | `kalshi ingestion/indexing reference only` | `yes, planning` |
| `src/indexers/polymarket/*` | `python` | `not recorded` | `polymarket ingestion/indexing reference only` | `yes, planning` |
| `src/analysis/kalshi/*` | `python` | `not recorded` | `kalshi analysis reference only` | `yes, planning` |
| `src/analysis/polymarket/*` | `python` | `not recorded` | `polymarket analysis reference only` | `yes, planning` |
| `tests/*` | `python` | `not recorded` | `reference for methodology only` | `yes, planning` |

## 4) Schema/data findings

| Candidate table/file | Row count estimate | Columns observed | Timestamp fields | `condition_id` / `token_id` / `outcome` availability | Legacy market identifier availability | Wallet fields | Price/size/side fields | Resolution/outcome labels | Notes |
|---|---:|---|---|---|---|---|---|---|---|
| `docs/SCHEMAS.md` (Polymarket market schema) | `not recorded` | `condition_id`, `outcomes`, `outcome_prices` | `not recorded in this row` | `partial: condition_id documented; token_id/outcome not explicitly confirmed in this source row` | `not required for canonical path; legacy market identifier may exist in broader ecosystem but not relied upon` | `not recorded` | `outcome_prices` observed | `outcomes` observed | `documented schema evidence only; no dataset import or sampling` |
| `docs/SCHEMAS.md` (Polymarket trade schema + block mapping) | `not recorded` | `maker`, `taker`, `maker_asset_id`, `taker_asset_id`, `maker_amount`, `taker_amount` | `block mapping includes timestamp` | `not explicitly confirmed` | `not explicitly confirmed` | `maker`, `taker` | `maker_amount`, `taker_amount` | `not recorded` | `schema evidence supports trade-level planning only` |
| `docs/SCHEMAS.md` (Kalshi schema signals) | `not recorded` | `yes_price`, `no_price`, `taker_side`, `result` | `not recorded` | `not explicitly confirmed` | `not explicitly confirmed` | `not recorded` | `yes_price`, `no_price`, `taker_side` | `result` | `schema evidence from documentation only` |
| `docs/ANALYSIS.md` and `src/analysis/*` | `not recorded` | `DuckDB query usage over Parquet files` | `timestamp usage implied by analysis and block mapping notes` | `not directly enumerated in this evidence row` | `not directly enumerated` | `not recorded` | `maker/taker and calibration/win-rate analysis reported` | `comparison analysis reported` | `analysis methodology evidence only; no data extraction approved` |

## 5) License/provenance findings

| Field | Finding | Evidence |
|---|---|---|
| License file path | `LICENSE` | `operator local read-only inspection notes` |
| License status | `repo_code_license_reviewed_acceptable / dataset_terms_pending_review` | `operator manual license review statement` |
| Terms concern | `dataset/archive terms and provenance not yet verified against actual downloaded data/checksum/source chain` | `ticket context and operator notes` |
| Allowed use recommendation | `research planning and local inspection only` | `review decision for this ticket` |
| Unresolved questions | `actual downloaded dataset provenance, checksums, timestamp ranges, and archive terms remain unverified` | `inspection scope limits` |
| Import decision | `approved for source-manifest planning only; hold on import` | `review decision` |

## 6) Fixture candidate assessment

No fixture derivation is approved yet.

| Candidate fixture name | Source file/path | Proposed rows | Proposed columns | Purpose | Checksum plan | Regeneration plan | Decision |
|---|---|---:|---|---|---|---|---|
| `phase0b_polymarket_schema_stub_candidate` | `docs/SCHEMAS.md` (documentation-only signal) | `0 (not derived)` | `N/A` | `future planning placeholder only` | `pending until actual data selected` | `pending until provenance review` | `pending_no_approval` |
| `phase0b_kalshi_schema_stub_candidate` | `docs/SCHEMAS.md` (documentation-only signal) | `0 (not derived)` | `N/A` | `future planning placeholder only` | `pending until actual data selected` | `pending until provenance review` | `pending_no_approval` |

## 7) Decision matrix

| Decision item | Status (`yes` / `no` / `blocked`) | Rationale | Follow-up ticket |
|---|---|---|---|
| Local inspection only | `yes` | `Review was executed as operator local read-only inspection.` | `Phase 0B-15` |
| Safe for source manifest entry | `yes / planning-only` | `Repository snapshot evidence is sufficient for source-manifest planning metadata, not import approval.` | `Phase 0B-15` |
| Safe for tiny fixture derivation | `no / pending` | `Fixture derivation requires actual data/checksum/provenance review not completed here.` | `Phase 0B-15` |
| Safe for loader implementation | `no` | `Loader remains blocked until provenance/terms and concrete dataset verification are complete.` | `Phase 0B-15` |
| Blocked pending dataset provenance review | `yes` | `Local 36 GiB archive and dataset provenance/checksums were not inspected in this ticket.` | `Phase 0B-15` |

## 8) Required evidence checklist

- [x] Command outputs recorded.
- [ ] Checksum strategy recorded.
- [x] Schema fingerprint recorded.
- [ ] Timestamp range recorded.
- [x] Canonical identifier coverage recorded (`condition_id`, `token_id`, `outcome`) where backed by documented schema evidence.
- [x] License/provenance reviewed.

## 9) Non-goals

- no import,
- no data commit,
- no DuckDB artifact,
- no external repo vendoring,
- no runtime/trading change.

## 10) Recommended next ticket

- **Phase 0B-15: Inspect the local ~36 GiB archive with read-only provenance/checksum capture and complete pending dataset terms review** before any fixture derivation or loader implementation approval.
