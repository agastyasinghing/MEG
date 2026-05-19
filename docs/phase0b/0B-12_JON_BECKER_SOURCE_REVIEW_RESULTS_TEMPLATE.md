# Phase 0B-12 — Jon-Becker / Local Archive Source Review Results Template

## 1) Purpose

Use this template to record findings **after** source inspection commands are run for:

- `Jon-Becker/prediction-market-analysis`, and/or
- a local Polymarket/Kalshi archive snapshot.

This template is review-documentation only:

- no import authorization by itself,
- no loader expansion by itself,
- no runtime/shared-rail/trading behavior impact.

## 2) Review metadata

| Field | Value to fill |
|---|---|
| `reviewer` | `TODO` |
| `review_date` | `TODO_YYYY-MM-DD` |
| `target_source` | `TODO` |
| `source_id` | `TODO_MATCH_MANIFEST_ID` |
| `local_path_or_url` | `TODO` |
| `git_commit_or_snapshot_id` | `TODO` |
| `review_status` | `TODO` (`draft` / `completed` / `blocked`) |

## 3) Source inventory findings

### 3.1 Inventory summary

| Item | Finding | Evidence (command/path) | Notes |
|---|---|---|---|
| File count | `TODO` | `TODO` | `TODO` |
| Total size | `TODO` | `TODO` | `TODO` |
| Top-level directories | `TODO` | `TODO` | `TODO` |
| Detected file formats | `TODO` | `TODO` | `TODO` |
| Candidate parquet/csv/json/jsonl files | `TODO` | `TODO` | `TODO` |
| Notebooks/scripts | `TODO` | `TODO` | `TODO` |
| README/license files | `TODO` | `TODO` | `TODO` |
| Manifest/provenance files (if present) | `TODO` | `TODO` | `TODO` |

### 3.2 Candidate files list (optional expanded section)

| Path | Format | Size | Candidate use | Include in follow-up? |
|---|---|---:|---|---|
| `TODO` | `TODO` | `TODO` | `TODO` | `TODO` |

## 4) Schema/data findings

| Candidate table/file | Row count estimate | Columns observed | Timestamp fields | `condition_id` / `token_id` / `outcome` availability | Legacy market identifier availability | Wallet fields | Price/size/side fields | Resolution/outcome labels | Notes |
|---|---:|---|---|---|---|---|---|---|---|
| `TODO` | `TODO` | `TODO` | `TODO` | `TODO` | `TODO` | `TODO` | `TODO` | `TODO` | `TODO` |

## 5) License/provenance findings

| Field | Finding | Evidence |
|---|---|---|
| License file path | `TODO` | `TODO` |
| License status | `TODO` (`approved` / `pending_review` / `restricted` / `rejected`) | `TODO` |
| Terms concern | `TODO` | `TODO` |
| Allowed use recommendation | `TODO` (`local inspection only` / `research-only transform` / `internal fixture derivation`) | `TODO` |
| Unresolved questions | `TODO` | `TODO` |
| Import decision | `TODO` (`hold` / `not approved` / `approved for planning only`) | `TODO` |

## 6) Fixture candidate assessment

| Candidate fixture name | Source file/path | Proposed rows | Proposed columns | Purpose | Checksum plan | Regeneration plan | Decision |
|---|---|---:|---|---|---|---|---|
| `TODO` | `TODO` | `TODO` | `TODO` | `TODO` | `TODO` | `TODO` | `TODO` |

## 7) Decision matrix

| Decision item | Status (`yes` / `no` / `blocked`) | Rationale | Follow-up ticket |
|---|---|---|---|
| Local inspection only | `TODO` | `TODO` | `TODO` |
| Safe for source manifest entry | `TODO` | `TODO` | `TODO` |
| Safe for tiny fixture derivation | `TODO` | `TODO` | `TODO` |
| Safe for loader implementation | `TODO` | `TODO` | `TODO` |
| Blocked pending license/provenance review | `TODO` | `TODO` | `TODO` |

## 8) Required evidence checklist

Mark each item only when concrete evidence is recorded in this document.

- [ ] Command outputs recorded.
- [ ] Checksum strategy recorded.
- [ ] Schema fingerprint recorded.
- [ ] Timestamp range recorded.
- [ ] Canonical identifier coverage recorded (`condition_id`, `token_id`, `outcome`).
- [ ] License/provenance reviewed.

## 9) Non-goals

This template does not do any of the following:

- import data,
- commit data files,
- produce or commit DuckDB artifacts,
- vendor external repositories,
- alter runtime/shared-rail/trading behavior.

## 10) Recommended next ticket options

Select one path after completing this review template:

1. **Phase 0B-13:** Fill `docs/phase0b/source_manifest.example.yaml` with reviewed Jon-Becker/local archive metadata.
2. **Phase 0B-13:** Draft tiny source-derived fixture plan if review gates pass.
3. **Phase 0B-13:** Stop/hold if license/provenance remains unclear.
