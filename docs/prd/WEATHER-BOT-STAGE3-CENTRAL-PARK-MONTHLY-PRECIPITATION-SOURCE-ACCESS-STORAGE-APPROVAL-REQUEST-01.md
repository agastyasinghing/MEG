# WEATHER-BOT-STAGE3-CENTRAL-PARK-MONTHLY-PRECIPITATION-SOURCE-ACCESS-STORAGE-APPROVAL-REQUEST-01

## Status and scope

**Status: BLOCKED; not decision-ready.** This source/access/storage approval-request-only docs/static-test artifact now separates verified current facts, verified archive/station candidates, and genuine blockers. It performs no acquisition and grants no authority. Research depth is **fresh current first-party source review dated 2026-09-28**. Markdown and an independent stdlib/pytest oracle are suitable; production code is not.

## Immediate predecessor and actual merge verification

PR #389's real post-merge commit is `9073a25cbdce9ba7c67508ee234cfa4d969d9edf`, not reviewed head `b0b1f46a2c3080b0b1cbd167571903dc849c82a8`. The local GitHub-created merge object says “Merge pull request #389,” and its parents are `62bbeadbfee3707fac316e9eab7f0ca20d254b48` and the reviewed head. Before work, `HEAD` equaled the merge commit; therefore its lineage contains the reviewed head and no `main` branch was required. Remote GitHub CLI/API/fetch attempts were unavailable in this environment, but the actual checked-out merge object establishes the post-merge SHA without guessing or using a preview SHA.

## Current first-slice state

The slice remains Polymarket Central Park NYC calendar-month total-precipitation range contracts whose contemporaneous rules use the NOAA/NWS New York climate page's monthly summarized Central Park precipitation value. The venue workflow and finalization instruction are now verified current facts. NCEI station and archive facts are verified candidates in their own domain, but their equivalence to the venue workflow and its historical state is not established. The repository's single Stage 2 example is not a corpus.

## Research method and source-quality standard

Research accessed or re-reviewed current first-party materials on 2026-09-28, starting with the venue rule rather than an archive candidate:

- [Polymarket May 2026 NYC precipitation market](https://polymarket.com/event/precipitation-in-nyc-in-may): controlling workflow, precision, finalization, revision, brackets, and displayed resolution evidence.
- [Polymarket Gamma API overview](https://docs.polymarket.com/developers/gamma-markets-api/overview), [markets overview](https://docs.polymarket.com/developers/gamma-markets-api/get-markets), and [market-by-slug reference](https://docs.polymarket.com/api-reference/markets/get-market-by-slug): public market metadata retrieval and lookup behavior.
- [NWS New York climate page](https://www.weather.gov/wrh/climate?wfo=okx) and [NOWData FAQ](https://www.weather.gov/wrh/ClimateFAQ): the venue-named interactive workflow and NWS warning that NOWData can contain preliminary and archived observations while official final records are at NCEI.
- [NCEI station search](https://www.ncei.noaa.gov/access/search/data-search/daily-summaries), [Daily Summaries](https://www.ncei.noaa.gov/products/land-based-station/daily-summaries), [Global Summary of the Month](https://www.ncei.noaa.gov/products/land-based-station/global-summary-of-the-month), and [Local Climatological Data](https://www.ncei.noaa.gov/products/land-based-station/local-climatological-data): authoritative station/product candidates, kept distinct.
- [NCEI Access Data Service documentation](https://www.ncei.noaa.gov/support/access-data-service-api-user-documentation): documented public GET retrieval parameters for dataset, station, and dates.
- [NOAA copyright notice](https://www.noaa.gov/disclaimer) and [NCEI citation guidance](https://www.ncei.noaa.gov/citation): general federal-data reuse and attribution posture, subject to identified third-party/product exceptions.
- [Polymarket Terms of Use](https://polymarket.com/tos): reviewed separately; it does not establish the durable local archival/redistribution permission required here.

No corpus enumeration, source-byte download, credential use, scraping, client construction, or artifact write occurred. Mutable claims carry the research date above; exact page/version evidence must still be preserved by a later approved process.

## Verified venue rule/source

The live Polymarket rule identifies `https://www.weather.gov/wrh/climate?wfo=okx` and directs the user to select **Monthly summarized data**, **Central Park NY**, and **Precipitation**. It resolves the calendar-month range using the precipitation figure displayed by that workflow and specifies use of the source's full displayed precision. This exact NWS/NOAA workflow—not an NCEI dataset—is the venue-defined meteorological settlement source.

The market window is total precipitation in Central Park, New York City, from May 1 through May 31, 2026 at 11:59 PM ET. Exact bracket endpoints belong to each market/token rule artifact. Trace and missing-data behavior are not independently defined by the venue text reviewed, so they must be preserved from the controlling displayed value rather than re-aggregated by assumption.

## Venue resolution/finality evidence

The live rule says settlement waits for the NOAA/NWS monthly summarized figure to be finalized and that revisions after that venue-defined finalization point do not change resolution. That rule establishes venue finality; it does not prove how an archive labels preliminary versus final records.

Market/rule evidence, proposal/dispute/final-resolution evidence, and meteorological finality remain distinct. The resolved page displays proposal/no-dispute/final-outcome evidence for the reviewed token, but current public retrieval is not proof of immutable historical versions or amendment history.

## Archive-equivalence analysis

NCEI Daily Summaries, GSOM, and LCD are official candidate archive products, but none is approved as equivalent to the venue's NWS monthly-summary display. NWS documents that NOWData can include preliminary and archived values and directs users to NCEI for official final records. Processing, quality control, synchronization, and later corrections can therefore make a present NCEI value different from the value displayed when the venue finalized.

Equivalence remains blocked until one exact product is matched across station/effective history, precipitation element, local calendar window and timezone, inches and precision, trace/missing handling, monthly aggregation, venue-relevant final state, revisions, controlling numerical value, and actual availability. “Official NOAA” is not synonymous with “venue-equivalent.” No observation acquisition method is selected.

## Station identity analysis

Current NCEI station metadata verifies the candidate **NY CITY CENTRAL PARK, NY US**, identifier `GHCND:USW00094728`, at approximately `40.77898, -73.96925`, with Daily Summaries/GSOM coverage exposed for that NCEI station family. This is authoritative NCEI candidate identity metadata.

It does not prove that the NWS interactive workflow used exactly that identifier, product, effective station lineage, processing state, or numerical value at venue finalization. Moves, instrumentation/network history, effective-date mapping, and workflow equivalence remain to be reconciled. The identifier is provenance metadata only, never routing.

## May 2026 known-month reconciliation

The bounded reconciliation case is the already-reviewed Polymarket event `precipitation-in-nyc-in-may`, specifically the **less than 2 inches** candidate represented by fixture identifiers `real_fixture_condition_stage2_polymarket_nyc_precip_may_2026_001`, `real_fixture_token_stage2_polymarket_nyc_precip_less_than_2_no_001`, and outcome `No`. These fixture identifiers preserve the canonical relationship for the reviewed example; the slug is provenance only. The window is Central Park, May 1–31, 2026 through 11:59 PM ET, in inches, using the NWS workflow and finalization rule above. The current venue evidence supports proposed `No`, no dispute, and final `No`; it does not supply trustworthy proposal/final timestamps, and the fixture's June 2 review time is not substituted for them.

Adversarial self-review found that the prior draft did not preserve exact first-party NWS product identifiers/locators, full issuance headers, or row-coverage references for the reported `1.77 in` CF6, `3.05 in` completed CF6, and `3.05 in` June 1 CLM observations. Those numbers are therefore retained only as **reported candidate observations requiring reproducible first-party artifact verification**, not verified facts. If an exact in-month CF6 shows incomplete row coverage, `1.77 → 3.05` would be normal accumulation rather than a correction; without that artifact and header, the classification itself remains provisional.

The same review found no exact retained NCEI request/record locator or response evidence supporting the asserted current GSOM `PRCP = 3.05 in`. The NCEI station and GSOM product remain authoritative candidates, but the May value is downgraded to a reported candidate until the exact direct-monthly record, units, status, and retrieval reference are reproducibly cited. No Daily Summaries sum is performed, and LCD remains excluded because semantic applicability was not established.

| Source / product | Role | State / issue evidence | Value | Status | Venue compatibility |
|---|---|---|---:|---|---|
| NWS NOWData monthly summarized display | Venue-defined source | Historical first-availability/display state not preserved | unresolved | Venue waits for finalized display | Controlling workflow; exact historical value state unresolved |
| NWS CF6, in-month candidate | Reported archived NWS evidence | Exact product ID/header/row coverage not retained | reported 1.77 in | Candidate preliminary partial-month state | Not verified; cannot establish revision classification or NOWData identity |
| NWS CF6, completed-month candidate | Reported archived NWS evidence | Exact product ID/header/row coverage not retained | reported 3.05 in | Candidate preliminary complete-month state | Not verified; exact NOWData mapping unproven |
| NWS CLM monthly candidate | Reported archived NWS evidence | Reported 2026-06-01 issue; exact product ID/header/clock not retained | reported 3.05 in | Candidate completed monthly report | Not verified; exact NOWData mapping unproven |
| NCEI GSOM candidate | Reported current archive cross-check | Exact request/record locator and response not retained | reported 3.05 in | Candidate direct monthly PRCP | Not verified; historical state and general equivalence unproven |
| Polymarket reviewed token | Venue result | Proposal/final timestamps not established; reviewed 2026-06-02 | less-than-2: No | Proposed No, no dispute, final No displayed | Outcome consistent with 3.05; not proof of source-state identity |

The strongest supported classification after self-review is **reported numerical alignment, not yet verified numerical agreement**. Exact product/record citations are missing, so even the numerical level is not independently reproducible from this artifact. Semantic compatibility, historical-state compatibility, and general equivalence remain unestablished.

## Historical source-path assessment

- **Option A — NCEI primary:** not selectable. The reported GSOM number lacks a reproducible record citation and would not establish historical NOWData state even if verified.
- **Option B — NWS archived CF6/CLM primary, NCEI cross-check:** plausible but not selectable. Exact NWS product artifacts and issuance headers must first be cited; even then, the CF6/CLM-to-NOWData relationship would remain separate.
- **Option C — additional preserved NOWData/ACIS state required:** unresolved. No historical evidence path is selected for acquisition.

`observation_valid_at` is the measured May interval. A product header's `source_product_issued_at` establishes that that product existed no later than issuance, but it is not automatically NOWData `source_available_at`. Venue finalization and `label_available_at` also remain unknown absent legitimate venue timestamps and the controlling display state. The first unresolved question is more basic: reproduce the reported May values with exact NWS product identifiers/locators and headers and an exact NCEI GSOM record reference. Only after that succeeds does the mapping question arise: whether CF6/CLM states are authoritatively mapped to the venue's NOWData monthly summarized display or a preserved NOWData/ACIS state is required. The next action remains limited to May 2026 and is not corpus acquisition.

## Revision/finality analysis

The required states are source first-posted, preliminary, revised, final, venue proposal, venue final resolution, and venue-defined source-finalization point. A current corrected archive value cannot rewrite settlement if the contemporaneous rule froze an earlier finalized state. Later archive, revision, or finality evidence must never be projected backward into an earlier prediction, fold, label-availability view, or venue-resolution state. No verified archive/version mechanism was established that reconstructs the exact venue-relevant historical state and its availability time. Latest-only archive data would be inadequate; revision/finality reconstruction is blocked.

## Point-in-time and label-availability analysis

The distinct clocks remain `prediction_as_of`, `input_publication_available_at`, `fold_cutoff`, `source_published_at`, `source_available_at`, `label_available_at`, `venue_resolution_proposed_at`, `venue_resolution_final_at`, `archive_revised_at`, `source_final_at`, and `acquired_at`. No timestamp substitutes for another.

Prediction inputs require `input_publication_available_at <= prediction_as_of`. Train/calibration labels require `label_available_at <= fold_cutoff`. Test labels must not be available by `fold_cutoff`; later legitimate test labels may be used afterward only for retrospective scoring. Settlement-label evidence is not required at prediction time. This request performs no split or scoring. Because historical publication/finality reconstructability was not verified, affected candidates remain blocked rather than assigned inferred times.

## Polymarket historical-evidence mechanism

Polymarket documents public Gamma market-data retrieval without authentication, including lookup/filtering by slug and documented market filters such as closed state. The documented response exposes the fields present in the current market/event record, including identifiers and current descriptive/status metadata. The exact future posture for that current metadata is `offline_public_api_acquisition`; individual rule and proposal/dispute/final-resolution adjudication remains `manual_source_review`.

Neither the developer documentation nor a current mutable market record establishes an immutable ledger of every contemporaneous rule version or amendment. Proposal, dispute, and finality fields must be verified for the exact response/page, and durable historical rule/version evidence remains blocked. Public API availability does not authorize scraping or establish archival/redistribution rights.

## NOAA/NWS/NCEI access-method analysis

NCEI documents Access Data Service GET requests parameterized by dataset, station, start date, end date, and output format. The documented service is a public, unauthenticated candidate for bounded offline retrieval; no API key is documented for that service. Daily Summaries, GSOM, and LCD remain separate candidate products, not interchangeable methods or settlement-equivalent sources.

Thus `offline_public_api_acquisition` is a verified technical capability for a later selected NCEI product, but the actual corpus observation method remains unresolved until equivalence selects exactly one product. Station metadata may be preserved by `static_public_reference`. No generic NOAA permission, bulk download, file fallback, client, or runtime provider is requested.

## Authentication/rate/access posture

Polymarket Gamma market-data endpoints are documented as public and do not require authentication for the relevant reads. NCEI Access Data Service documentation likewise does not document a credential/API key for its public GET service. Documented numeric rate limits relevant to this bounded research use were not found; “undocumented” is not “unlimited,” and later work must use bounded requests and preserve failure/response metadata. No credential, special header, scraping, or live-provider authority is implied.

## Terms/attribution/retention posture

No legal conclusion is made. NOAA states that material it produces is generally not copyrighted/public domain unless otherwise noted; NCEI provides citation guidance. This supports a general candidate posture for local retention, derived records, and redistribution of identified NOAA/NCEI-produced data with attribution, while product-level notices, embedded third-party material, and selected-product exceptions still require review.

Polymarket is separate. Its current Terms and developer documentation do not clearly establish the retention, immutable local archival, redistribution, or republication rights needed for copied page/API rule evidence. Polymarket raw archival/redistribution therefore remains blocked. Checksums and locator-only receipts do not cure missing permission. Large artifacts remain prohibited from Git.

## Proposed exact source-role matrix

| Category | Role | Exact source/fact | Posture |
|---|---|---|---|
| VERIFIED | Venue meteorological source | NWS New York climate workflow: Monthly summarized data → Central Park NY → Precipitation | controlling venue source |
| VERIFIED | Venue finality | Full displayed precision; post-finalization revisions do not change resolution | controlling rule behavior |
| VERIFIED | Current venue metadata | Polymarket public page/Gamma current closed-market record | public current retrieval; not version history |
| VERIFIED CANDIDATE | Station authority | NCEI `NY CITY CENTRAL PARK, NY US`, `GHCND:USW00094728`, `40.77898,-73.96925` | authoritative NCEI candidate only |
| VERIFIED CANDIDATE | Archive products | NCEI Daily Summaries, GSOM, and LCD | official products; none selected/equivalent |
| STILL BLOCKED | Historical archive | No exact product proven to reproduce venue-finalized display | fail closed |
| STILL BLOCKED | Historical venue evidence | Contemporaneous rules/amendments and resolution timeline | durable mechanism unresolved |
| STILL BLOCKED | Availability/revision | First-posted/preliminary/final/revised values and actual availability | reconstruction unresolved |

## Proposed exact access-method matrix

| Source role | One exact posture |
|---|---|
| Polymarket individual rule adjudication | `manual_source_review` |
| Polymarket current public market metadata | `offline_public_api_acquisition` |
| Polymarket durable historical rule/version evidence | unresolved |
| NWS venue workflow documentation | `static_public_reference` |
| NCEI candidate station metadata | `static_public_reference` |
| NCEI candidate technical data access | `offline_public_api_acquisition` |
| Actual corpus observation bytes | unresolved pending exact-product equivalence |

The complete allowed vocabulary remains `manual_source_review`, `static_public_reference`, `offline_public_file_acquisition`, `offline_public_api_acquisition`, `source_specific_credentials_required`, `scraping_requires_separate_approval`, and `live_runtime_provider_requires_separate_approval`. Consideration does not grant authority; there is no interchangeable fallback.

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

The known-month experiment resolves the values but not the provenance chain. Remaining blockers are now:

1. **Smallest blocker:** reproducibly cite and verify the exact May 2026 NWS CF6/CLM product artifacts, full issuance headers/row coverage, and exact NCEI GSOM record that support the reported values.
2. Recover legitimate venue finalization/proposal/final timestamps and durable contemporaneous rule/version evidence; the fixture review time is not a substitute.
3. Establish historical NOWData first-availability and NCEI GSOM revision-state evidence; current GSOM proves only a current value.
4. Reconcile effective station history with the NWS workflow's station/product mapping.
5. Determine whether a metadata-receipt-only Polymarket posture—locator, retrieval time, normalized fields, permitted checksum, manual provenance, and canonical identifiers—is sufficient under first-party terms. Until justified, terms remain `blocking_for_required_evidence`.
6. Review the ultimately selected NCEI product's notices/exceptions before any retention or redistribution approval.

Thus the reported `3.05 in` alignment is not yet independently verified numerical agreement, much less general equivalence, and does not select observation acquisition. After item 1, the next question is the NOWData-to-archived-product mapping using only this known case.

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
known_month_reconciliation_case: may_2026_central_park_less_than_2_inches_outcome_no
known_month_venue_value: unresolved_exact_historical_nowdata_display_not_preserved
known_month_nws_partial_cf6_value: reported_1.77_inches_artifact_locator_header_and_row_coverage_unverified
known_month_nws_completed_cf6_value: reported_3.05_inches_artifact_locator_header_and_row_coverage_unverified
known_month_nws_clm_value: reported_3.05_inches_2026_06_01_issue_exact_product_header_unverified
known_month_ncei_gsom_value: reported_3.05_inches_exact_record_locator_and_response_unverified
known_month_polymarket_outcome: less_than_2_inches_no_proposed_no_dispute_final_no_timestamps_unresolved
known_month_value_agreement_posture: reported_numerical_alignment_not_independently_reproducible
nws_historical_evidence_posture: reported_products_require_exact_locator_header_and_row_coverage_verification
ncei_historical_evidence_posture: reported_current_gsom_value_requires_exact_record_verification
venue_archive_mapping_posture: unresolved_values_not_reproducibly_verified_and_exact_workflow_mapping_unproven
historical_availability_evidence_posture: blocked_exact_product_headers_nowdata_first_available_and_venue_finalization_unresolved
venue_source_verification_status: verified_nws_okx_monthly_summarized_data_central_park_ny_precipitation
venue_settlement_source_role: nws_okx_monthly_summarized_data_central_park_ny_precipitation_display
venue_finality_posture: verified_full_displayed_precision_post_finalization_revisions_do_not_change_resolution
archive_source_role: ncei_daily_summaries_gsom_lcd_official_candidates_none_selected
archive_equivalence_posture: blocked_fail_closed
station_identity_posture: authoritative_ncei_station_candidate_ghcnd_usw00094728_verified_venue_equivalence_unresolved
polymarket_rule_evidence_posture: manual_source_review
polymarket_resolution_evidence_posture: manual_source_review
polymarket_current_metadata_access_method: offline_public_api_acquisition
observation_access_method: unresolved
station_metadata_access_method: static_public_reference
publication_availability_posture: blocked_historical_reconstructability_not_verified
revision_finality_posture: blocked_historical_venue_relevant_state_not_verified
authentication_posture: source_specific_public_reads_unauthenticated_numeric_rates_undocumented
polymarket_authentication_posture: public_gamma_market_reads_no_authentication_documented
ncei_authentication_posture: public_access_data_service_get_no_api_key_documented
ncei_candidate_access_method: offline_public_api_acquisition
noaa_ncei_terms_posture: general_noaa_produced_data_public_domain_with_attribution_and_exception_review
polymarket_terms_storage_posture: blocking_for_required_evidence
terms_storage_posture: source_specific_split_noaa_general_open_attribution_verified_polymarket_archival_rights_blocked
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
