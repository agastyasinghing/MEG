# WEATHER-BOT-STAGE3-CENTRAL-PARK-MONTHLY-PRECIPITATION-SOURCE-ACCESS-STORAGE-APPROVAL-REQUEST-01

## Status and scope

**Status: BLOCKED; not decision-ready.** This is a source/access/storage approval-request-only docs/static-test artifact. It records current research, an exact proposed storage boundary, and the facts that prevent a coherent source approval. It performs no acquisition and grants no authority. Research depth is **deep current first-party research attempted; core external verification unavailable and failed closed**. Markdown and a stdlib/pytest static oracle are suitable for this contract; production code is not.

## Immediate predecessor and actual merge verification

PR #389's real post-merge commit is `9073a25cbdce9ba7c67508ee234cfa4d969d9edf`, not reviewed head `b0b1f46a2c3080b0b1cbd167571903dc849c82a8`. The local GitHub-created merge object says “Merge pull request #389,” and its parents are `62bbeadbfee3707fac316e9eab7f0ca20d254b48` and the reviewed head. Before work, `HEAD` equaled the merge commit; therefore its lineage contains the reviewed head and no `main` branch was required. Remote GitHub CLI/API/fetch attempts were unavailable in this environment, but the actual checked-out merge object establishes the post-merge SHA without guessing or using a preview SHA.

## Current first-slice state

The target remains exactly Polymarket Central Park NYC calendar-month total-precipitation range contracts whose contemporaneous rules use NOAA's finalized monthly summarized Central Park precipitation figure. The repository has one reviewed Stage 2 page-derived example, not a corpus. It does not independently establish an exact NOAA product, archive equivalence, station ID, historical publication clock, or durable rule history.

## Research method and source-quality standard

On 2026-09-27, research began from the venue evidence, then considered only first-party product, station, access, and terms evidence. The inspected repo sources were the controlling Stage 3 documents, WX research packets, and both real-source-backed fixtures; neither fixture was modified. Attempts to retrieve current GitHub, Polymarket, NWS, and NCEI public material from this execution environment were blocked by its external network/authentication boundary. No URL pattern or older Stage 2 assertion was promoted to a current verified fact.

The first-party references requiring successful human re-review are:

- [Polymarket contract page](https://polymarket.com/event/precipitation-in-nyc-in-may) — contemporaneous rule, brackets, amendments, proposal/dispute/final outcome;
- [Polymarket Gamma API introduction](https://docs.polymarket.com/developers/gamma-markets-api/overview) — only if it documents retrieval of the required historical market/rule fields;
- [NWS New York climate/NOWData entry](https://www.weather.gov/wrh/Climate?wfo=okx) — exact displayed workflow and preliminary/final disclaimer;
- [NCEI Daily Summaries](https://www.ncei.noaa.gov/products/land-based-station/daily-summaries) and [search](https://www.ncei.noaa.gov/access/search/data-search/daily-summaries) — candidate archive documentation, not an approved mapping;
- [NCEI LCD](https://www.ncei.noaa.gov/products/land-based-station/local-climatological-data) — a distinct candidate product, not interchangeable with Daily Summaries;
- [NCEI Access Data Service documentation](https://www.ncei.noaa.gov/support/access-data-service-api-user-documentation) — candidate access documentation only;
- [NOAA information-quality guidance](https://www.noaa.gov/organization/information-technology/policy-oversight/information-quality) and [Department of Commerce data policy](https://www.commerce.gov/data-and-reports) — terms/public-data context requiring product-specific confirmation.

Reading these descriptions or an individual rule page would be planning research. Batch download, enumeration, scraping, credentials, clients, and corpus writes are prohibited.

## Verified venue rule/source

The 2026-06-02 static fixture preserves page-review evidence that the May 2026 market measured total precipitation in inches in Central Park, New York City, from May 1 through May 31 at 11:59 PM ET; used ranges; and named NOAA's finalized monthly summarized Central Park precipitation figure with venue-stated revision handling. That evidence is sufficient to retain the candidate family, but not to claim a currently verified exact NOAA/NWS page, product, endpoint, timezone implementation, trace/missing convention, or archive mapping.

Accordingly, `venue_source_verification_status` is blocked. The venue market/rule evidence, Polymarket resolution evidence, and meteorological settlement source are three separate roles. Exact contemporaneous wording and all comparator endpoints must be preserved verbatim by a later approved evidence process; they are not reconstructed here.

## Venue resolution/finality evidence

The fixture reports page-displayed “Outcome proposed: No,” no dispute, and final outcome No for one token, with review on 2026-06-02. It is a static reviewed example, not a verified durable historical API. The venue-defined rule reportedly freezes once NOAA finalizes the monthly figure and disregards subsequent changes, but current first-party rule text and its exact finalization instruction could not be reverified. Proposal, dispute, venue final resolution, and meteorological finality remain distinct clocks and evidence objects.

## Archive-equivalence analysis

Daily Summaries, LCD, and any NWS climate display are candidates only. No authoritative evidence retrieved in this work proves that one reproduces the venue-controlling value across station identity/history, element, calendar window, ET/local-day semantics, units, trace/missing handling, aggregation, finality, corrections, and the value actually used by the venue. Being NOAA products is insufficient.

Therefore no archive is proposed for approval, observation acquisition remains unresolved, and equivalence fails closed. An intentionally narrower metadata/scaffold request would still falsely imply a usable first slice without the controlling source mapping, so this artifact does not request it.

## Station identity analysis

The only source-visible location supported by the reviewed fixture is “Central Park, New York City” / “Central Park NY.” No current authoritative station metadata was retrieved. No WBAN, GHCN, COOP, LCD, ICAO, or other identifier is frozen. Different official identifiers may describe distinct networks/products and cannot be collapsed. Effective dates, moves, renames, instrumentation, and relation to the venue workflow are unresolved; this ambiguity blocks approval.

## Revision/finality analysis

The required states are source first-posted, preliminary, revised, final, venue proposal, venue final resolution, and venue-defined source-finalization point. A current corrected archive value cannot rewrite settlement if the contemporaneous rule froze an earlier finalized state. Later archive, revision, or finality evidence must never be projected backward into an earlier prediction, fold, label-availability view, or venue-resolution state. No verified archive/version mechanism was established that reconstructs the exact venue-relevant historical state and its availability time. Latest-only archive data would be inadequate; revision/finality reconstruction is blocked.

## Point-in-time and label-availability analysis

The distinct clocks remain `prediction_as_of`, `input_publication_available_at`, `fold_cutoff`, `source_published_at`, `source_available_at`, `label_available_at`, `venue_resolution_proposed_at`, `venue_resolution_final_at`, `archive_revised_at`, `source_final_at`, and `acquired_at`. No timestamp substitutes for another.

Prediction inputs require `input_publication_available_at <= prediction_as_of`. Train/calibration labels require `label_available_at <= fold_cutoff`. Test labels must not be available by `fold_cutoff`; later legitimate test labels may be used afterward only for retrospective scoring. Settlement-label evidence is not required at prediction time. This request performs no split or scoring. Because historical publication/finality reconstructability was not verified, affected candidates remain blocked rather than assigned inferred times.

## Polymarket historical-evidence mechanism

The only supported posture now is `manual_source_review` of the named individual public page. `static_public_reference` is not proposed as sufficient because a mutable current page is not a durable historical version. No verified public file or API mechanism was established for historical wording, amendments, source instruction, `condition_id`/`token_id`/`outcome`, proposals, disputes, final outcomes, and timestamps. Scraping would require separate approval. Missing contemporaneous rule/version evidence makes a candidate unusable and retained as blocked/excluded in the manifest.

## NOAA/NWS/NCEI access-method analysis

No observation method is selected. `offline_public_file_acquisition` and `offline_public_api_acquisition` were considered, but current authoritative documentation and exact product equivalence could not be verified; selecting either would be speculative. Station metadata is limited to `manual_source_review` until an exact first-party product page is verified. Generic NOAA, API, or file permission is not requested.

## Authentication/rate/access posture

For the proposed manual reviews, no credential is proposed and no numeric quota is asserted. For every possible file/API method, authentication, key requirement, quota, user-agent/header requirements, coverage, bulk/API distinction, and reproducible failure behavior remain undocumented by evidence retrieved in this ticket. “Undocumented” is not treated as “unlimited.” Credentials remain unapproved; inability to verify exact access blocks selection.

## Terms/attribution/retention posture

No legal conclusion is made. Product-specific first-party terms covering retention, local storage, redistribution, repository inclusion, attribution, derived normalized records, and evidence receipts were not successfully retrieved. Public-agency origin alone is not a redistribution determination, and Polymarket page availability alone is not archive permission. Raw retention and redistribution therefore remain unapproved. Checksums, locators, access dates, and attribution would be mandatory if later approved; large or source-derived artifacts may never enter Git.

## Proposed exact source-role matrix

| Role | Exact proposed source | Posture |
|---|---|---|
| Venue market/rule | Named individual Polymarket market page, contemporaneous version | manual review only; durable history unresolved |
| Venue resolution | Same contract's proposal/dispute/final-resolution record | manual review only; durable mechanism unresolved |
| Meteorological settlement | Exact NOAA finalized monthly summarized Central Park figure named by the rule | exact product/workflow unresolved; blocked |
| Historical archive | None selected among Daily Summaries/LCD/other official products | equivalence unproven; blocked |
| Station authority | Exact product-specific NCEI/NWS station metadata | identity/effective history unresolved; blocked |
| Availability/revision | Source-native publication/version/finality evidence | reconstructability unresolved; blocked |

## Proposed exact access-method matrix

| Source role | One proposed method |
|---|---|
| Polymarket rule evidence | `manual_source_review` |
| Polymarket resolution evidence | `manual_source_review` |
| NOAA observation bytes | unresolved |
| NOAA station metadata | `manual_source_review` |
| Publication/revision evidence | unresolved |

Only `manual_source_review`, `static_public_reference`, `offline_public_file_acquisition`, `offline_public_api_acquisition`, `source_specific_credentials_required`, `scraping_requires_separate_approval`, and `live_runtime_provider_requires_separate_approval` were considered. No interchangeable fallback method is requested.

## Proposed storage posture

If a later decision follows successful source research, the requested future root would be a separately configured external artifact root, **not** the repository's `data/` tree and not created now. A clean checkout would locate it only through caller-supplied configuration validated by later approved code; no secret-loading change is implied. PostgreSQL remains operational journal only; DuckDB-over-Parquet remains the historical/research plane.

- **RAW:** `weather/stage3/central_park_monthly_precipitation/raw/sha256/<digest>` beneath that root; immutable original bytes and sidecar source metadata when terms permit; no destructive overwrite.
- **NORMALIZED:** versioned Parquet under `.../normalized/schema=<version>/parser=<version>/`; derivable only from identified raw checksums.
- **MANIFEST:** append-only records under `.../manifests/`, covering usable, blocked, and excluded candidates, source/rule/station lineage, reconciliation, versions, and checksums.
- **GOLD:** excluded from this request.

Only docs, schemas, code, and tiny deterministic license-cleared fixtures could later enter Git after separate approval. Raw source bytes, normalized corpus data, manifests containing source content, Parquet, DuckDB, and large artifacts may never enter Git. This posture is proposed only; storage writes remain unapproved.

## Reproducibility/checksum posture

Future raw bytes would use SHA-256 content addresses with byte length, media type, exact locator, source/product/version, retrieval/acquisition time, and response/file metadata. Normalization would record raw checksum, parser and schema versions, deterministic output checksum, and supersession links. Append-only manifests would reconcile every candidate and preserve exclusions. Receipts may identify externally retained artifacts without committing them, but a checksum alone cannot prove rule meaning, availability time, or legal retention.

## Requested future implementation scope

This artifact presents the intended approval question but is not a concrete approvable request yet because the core source mapping is unresolved. It therefore requests no future implementation permission and must not be routed to a decision ticket in its present state. After successful research and an approval-request revision, the maximum bounded scaffold that a later human decision could consider would validate research records, build append-only manifests, normalize caller-supplied bytes, use tiny license-cleared fixtures, and test checksums/reconciliation/no-lookahead. A downloader, connector, or actual acquisition would remain a separate gate.

## Remaining blockers

1. Reverify exact contemporaneous venue rule wording, named NOAA/NWS workflow, brackets, trace/missing/revision/finality semantics, and amendments.
2. Establish effective-dated Central Park station identity in that workflow.
3. Prove one official archive's semantic and historical-state equivalence or narrow the family honestly.
4. Verify durable Polymarket rule and resolution history with timestamps.
5. Verify one exact acquisition mechanism, authentication, rates/headers, coverage, and failure behavior.
6. Verify product-specific retention, attribution, redistribution, and derived-use terms.

These are core blockers, not implementation details.

## Human decision options

The exact available options are:

- `approve_central_park_monthly_precipitation_source_access_storage`
- `request_approval_request_revision`
- `hold`
- `block`

No option is selected. Because this request is not decision-ready, an approver should not select the approval option on this evidence.

## Current approval posture

The posture is request-only with no recorded decision. Source use, acquisition, storage writes, credentials, scraping, and live provider runtime are not approved. Stage 3 scoring is not ready. No prose in this document changes those assignments.

## Explicit non-approvals

This ticket does not approve or implement corpus acquisition, batch fetching, downloaded datasets, HTTP/API clients, scraping, credentials/secrets, provider connectors, live weather runtime, continuous ingestion, schedulers/services/workers, training, probability generation, split or baseline execution, scoring/diagnostics/evaluation, results/claims, evidence-gate passage, Stage 4, paper simulation, trading, order placement, production runtime, or autonomy.

## Canonical routing posture

Canonical routing remains exactly `condition_id`, `token_id`, and `outcome`. The legacy `market_id` is non-routing only. External venue references, slugs, source/station/dataset IDs, and contract references are provenance metadata only. `token_outcome_pair` is derived only.

## Recommended next ticket

None. The specified approval-decision ticket is recommended if and only if the request becomes decision-ready. This artifact is BLOCKED, so the next action is external evidence resolution and approval-request revision, not a decision or implementation ticket.

## Machine-checkable assignments

```text
ticket_id: WEATHER-BOT-STAGE3-CENTRAL-PARK-MONTHLY-PRECIPITATION-SOURCE-ACCESS-STORAGE-APPROVAL-REQUEST-01
immediate_predecessor_pr: pr_389
actual_merge_sha: 9073a25cbdce9ba7c67508ee234cfa4d969d9edf
artifact_scope: docs_static_test_only
request_posture: request_only
approval_decision_posture: approval_decision_not_recorded
selected_first_slice: polymarket_central_park_nyc_calendar_month_total_precipitation_range_contracts_using_noaa_finalized_monthly_summarized_central_park_figure
venue_source_verification_status: blocked_current_first_party_exact_workflow_not_reverified
venue_settlement_source_role: exact_rule_named_noaa_finalized_monthly_summarized_central_park_precipitation_figure
venue_finality_posture: blocked_exact_source_finalization_and_revision_rule_not_reverified
archive_source_role: none_selected_official_candidates_not_proven_equivalent
archive_equivalence_posture: blocked_fail_closed
station_identity_posture: blocked_no_authoritative_product_specific_identifier_frozen
polymarket_rule_evidence_posture: manual_source_review
polymarket_resolution_evidence_posture: manual_source_review
observation_access_method: unresolved
station_metadata_access_method: manual_source_review
publication_availability_posture: blocked_historical_reconstructability_not_verified
revision_finality_posture: blocked_historical_venue_relevant_state_not_verified
authentication_posture: no_credentials_proposed_exact_external_method_requirements_undocumented
terms_storage_posture: blocked_product_specific_retention_redistribution_attribution_not_verified
raw_storage_posture: requested_future_external_artifact_root_immutable_sha256_content_addressed_no_overwrite
normalized_storage_posture: requested_future_external_artifact_root_versioned_parquet_schema_and_parser_versioned
manifest_storage_posture: requested_future_external_artifact_root_append_only_all_dispositions_and_lineage
git_large_data_posture: prohibited
point_in_time_posture: distinct_semantic_clocks_missing_evidence_blocks_no_inference
label_availability_posture: train_calibration_available_by_fold_cutoff_test_unavailable_by_fold_cutoff_later_scoring_only
historical_truth_posture: later_archive_revision_or_finality_evidence_never_projects_backward_or_rewrites_venue_settlement
source_use_authority: not_approved
data_acquisition_authority: not_approved
storage_write_authority: not_approved
credential_use_authority: not_approved
scraping_authority: not_approved
live_provider_runtime_authority: not_approved
stage3_scoring_readiness: not_ready
human_decision_option: approve_central_park_monthly_precipitation_source_access_storage
human_decision_option: request_approval_request_revision
human_decision_option: hold
human_decision_option: block
human_decision_selection: none
canonical_routing_field: condition_id
canonical_routing_field: token_id
canonical_routing_field: outcome
non_routing_legacy_identifier: market_id
derived_identifier: token_outcome_pair
recommended_next_ticket: none_blocked_pending_core_external_evidence
```

## Acceptance criteria

1. The artifact remains BLOCKED unless the venue workflow, station identity, archive equivalence, historical-state capability, access method, and terms are supported by current first-party evidence.
2. Venue, resolution, meteorological settlement, and archive roles remain separate.
3. No acquisition, storage write, connector, credential, or runtime authority is granted.
4. The proposed future storage plane stays external to Git and separate from PostgreSQL operational journaling.
5. Timing preserves prediction, role-specific fold, and later retrospective-scoring boundaries.
6. The four decision options are exact and unselected; no decision successor is recommended while blocked.
