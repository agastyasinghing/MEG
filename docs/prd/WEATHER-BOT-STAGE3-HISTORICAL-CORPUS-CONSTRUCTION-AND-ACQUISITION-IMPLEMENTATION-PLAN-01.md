# WEATHER-BOT-STAGE3-HISTORICAL-CORPUS-CONSTRUCTION-AND-ACQUISITION-IMPLEMENTATION-PLAN-01

## Status and scope

**Status:** implementation plan complete; external-source approval and implementation remain blocked. This docs/static-test-only artifact converts the narrow planning path approved by PR #388 into a future contract. It performs no acquisition, API call, scrape, download, corpus creation, dependency installation, or loader implementation.

The plan is deliberately smaller than an eventual weather corpus: prove one source-compatible market family and its audit machinery before expansion. Research depth is **targeted current source/access research attempted, with unavailable external verification failed closed**. Markdown plus an independent Python stdlib/pytest oracle are suitable because this ticket freezes decisions rather than implementing a data plane.

## Immediate predecessor and actual merge verification

PR #388 is represented in the checked-out Git history by merge commit `62bbeadbfee3707fac316e9eab7f0ca20d254b48`, authored by GitHub, whose second parent is the reviewed head `4499fa6941e78752b0b630ad0e769820c52db82a`. `git merge-base --is-ancestor 62bbeadbfee3707fac316e9eab7f0ca20d254b48 HEAD` succeeded before work began. Thus the reviewed head is not misrepresented as the merge commit, and neither `origin/main` nor a local `main` is required.

The real post-merge SHA was obtained from the checked-out GitHub-created merge metadata, not inferred from the reviewed head: the commit object explicitly identifies “Merge pull request #388,” records GitHub as committer, and has both expected parents. It is an ancestor of the checkout. This plan records that exact merge object. The unauthenticated GitHub web/API surface was unavailable for a redundant remote lookup; if a reviewer cannot reconcile the checked-out GitHub merge metadata to PR #388, review must fail closed rather than substitute a preview or guessed SHA.

## Decision authority inherited from #388

PR #388 selected `approve_narrow_historical_corpus_construction_and_acquisition` only for narrow implementation planning. It granted no execution authority and approved no individual access method. This plan may propose researched postures, storage, and future files; it cannot elevate them to source-use or implementation approval.

## Current blocker/state

The repository still contains only five static Stage 2 examples: three synthetic and two real source-backed examples. They are examples, not a corpus; coverage and sample sufficiency are not established, strict OOS feasibility is not demonstrated, and Stage 3 scoring is not ready.

External first-party pages could not be retrieved from the execution environment on 2026-09-25. Consequently the exact NOAA product/locator, historical publication-time reconstruction, Polymarket historical rule retrieval mechanism, and both providers' current terms/redistribution posture are unresolved implementation blockers. The selected slice is a plan target, not permission to move bytes.

## Research findings

Targeted research considered the repository's controlling PRDs/research and inspected all five existing JSON fixtures without modifying them. The precipitation fixture records a Polymarket monthly NYC precipitation rule naming NOAA's finalized monthly summarized Central Park figure. The temperature fixture records mixed Wunderground KLGA, Central Park/LaGuardia, and NWS language and is deliberately blocked.

Current first-party verification was attempted for NCEI Daily Summaries search, Local Climatological Data, Access Data Service documentation, the GHCN-Daily README, NWS climate pages, and Polymarket market API documentation. Network access returned no retrievable source content. No mutable external fact is therefore promoted as verified. Repository evidence supports candidate selection, while the next gate must establish current authoritative source facts.

Planning hypotheses requiring verification are: Central Park's station identity is likely represented by an NCEI identifier; NOAA/NCEI may expose public files and/or an offline API; final archives can differ from first-posted values; and venue pages may not provide durable historical availability timestamps. None is treated as approved fact here.

## Candidate first-slice comparison

| Candidate | Source/rule clarity | Point-in-time and finality | Recurrence / machinery value | Decision |
|---|---|---|---|---|
| Polymarket Central Park monthly precipitation ranges naming NOAA finalized monthly summary | Strongest repo evidence: venue rule, station place, monthly window, units, brackets, revision handling, final venue label | Final layer is described, but exact NOAA product and first-publication clock remain blocked | Recurring monthly family can exercise rule versions, brackets, manifests, revisions, and reconciliation | **Select narrowly, subject to blockers** |
| Polymarket NYC daily high temperature using Wunderground KLGA | Existing fixture demonstrates conflicting station/source semantics | Availability and finalization semantics unresolved | Recurrent, but ambiguity would validate the wrong behavior | Reject for first clean slice; retain as blocked adjudication evidence |
| Severe/tropical or forecast-dependent families | Resolver products and amendments can be complex | Advisory versus best-track/revision clocks add ambiguity | Useful later but not minimal | Defer |

Selection is not based merely on the suggested fixture. The monthly precipitation family has fewer semantic degrees of freedom and needs no historical forecast/model input to construct settlement labels. It can test immutable source evidence, venue rules, station selection, finality, and correction chains without combining unrelated families.

## Selected first acquisition slice

The exact slice is **Polymarket Central Park NYC calendar-month total-precipitation range contracts whose contemporaneous venue rule explicitly names NOAA/NCEI's finalized monthly summarized Central Park precipitation figure**. Include only contracts with recoverable canonical identifiers, versioned rule evidence, an unambiguous calendar-month ET window, inches, explicit range comparator semantics, venue outcome evidence, and an approved exact NOAA/NCEI source mapping.

This is one family, not every NYC precipitation market and not daily temperature. No arbitrary record count is promised. A candidate lacking any required evidence is represented with `blocked` or `excluded` disposition and remains in manifest totals; it is never silently dropped or made usable.

## Source-role matrix

| Role | Candidate and semantic match | Proposed access / credentials / approval | Point-in-time and finality capability | Required provenance and unresolved risk |
|---|---|---|---|---|
| Venue market/rule source | Contemporaneous Polymarket public contract/rules artifact; defines family, brackets, window, source, and label | `manual_source_review` plus `static_public_reference`; no credential proposed; source-specific approval still required | Historical rule version and first availability are not yet verified | locator, contract reference, content checksum/snapshot reference, retrieved/acquired time, rule version, reviewer; durable historical mechanism and terms blocked |
| Settlement/resolver source | Polymarket proposal/dispute/final-resolution evidence for the same contract | `manual_source_review` plus `static_public_reference`; no credential proposed; approval required | Proposal, dispute, and finality clocks must be independently captured; history availability unresolved | resolver identity, proposal/finality times, outcome, evidence locator/checksum, reviewer; historical availability blocked |
| Observation/archive source | Exact NOAA/NCEI monthly summarized Central Park precipitation product named/matched by the rule | `manual_source_review` only now; a later gate may choose exactly one of `offline_public_file_acquisition`, `offline_public_api_acquisition`, or `source_specific_credentials_required`; approval required | Must retain first-posted/preliminary/revised/final layers and actual availability evidence; capability unresolved | agency, dataset/product/version, station identifier, locator, access posture, bytes checksum, valid/publication/availability/revision/finality/acquisition times; exact product blocked |
| Station/observation authority | NOAA/NCEI station metadata for the exact Central Park observing identity and effective dates | `static_public_reference` proposed only after verification; no credential assumed; approval required | Effective-dated station identity/source selection required | station IDs/names, authority, effective interval, metadata locator/version/checksum, selected_at, reviewer; ID and history unresolved |
| Historical forecast/model source | None for label-corpus construction in this first slice | `not_applicable_first_slice`; no access | Forecast clocks nullable only because no forecast is ingested | Any later Stage 3 probability input is a separate approval; never backfill forecasts into this acquisition |
| Publication/availability evidence source | Source-native NOAA/NCEI metadata/headers/catalog plus preserved HTTP/file metadata, exact mechanism unresolved | `manual_source_review` only now; approval required before selecting an acquisition method | A nominal observation or update schedule is insufficient; actual historical availability must be evidenced | publication/availability timestamp, evidence type, locator, capture time/checksum, confidence; reconstructability blocked |
| Revision/finality evidence source | NOAA/NCEI source-native status/revision metadata plus venue rule's finality instruction | `manual_source_review` only now; approval required before selecting an acquisition method | Must distinguish first-posted, preliminary, revised, final, superseded | revision ID/time, finality time/status, predecessor, evidence; exact semantics blocked |
| Reviewer/adjudication evidence | MEG human review record, using preserved source evidence only | `manual_source_review`; no external credential; future implementation approval required | Reviewer time never substitutes for source availability/finality | reviewer identity/ref, reviewed_at, decision, rationale, evidence refs; disagreement blocks usability |

A convenient weather API is not the settlement authority. It cannot substitute for the exact NOAA/NCEI product required by the contemporaneous venue rule.

## Access-method matrix

Only the #387/#388 vocabulary is an allowable external consideration vocabulary:

`manual_source_review`, `static_public_reference`, `offline_public_file_acquisition`, `offline_public_api_acquisition`, `source_specific_credentials_required`, `scraping_requires_separate_approval`, and `live_runtime_provider_requires_separate_approval` are the complete closed set. Listing a posture for consideration does not select or approve it.

| Source | Planned posture | Authority now |
|---|---|---|
| Polymarket rule and resolution evidence | `manual_source_review`; `static_public_reference` | proposed, not approved or executed |
| NOAA/NCEI product/access research | `manual_source_review` | proposed for the later approval gate; no source bytes move |
| NOAA/NCEI observation bytes | no planned method selected; later gate may select exactly one supported consideration posture | blocked |
| NOAA/NCEI station metadata | `static_public_reference` only after exact verification | blocked pending source-specific approval |
| Credentialed source, if verification shows authentication is mandatory | `source_specific_credentials_required` | credential use unapproved |
| Any scraping | `scraping_requires_separate_approval` | not approved |
| Any live provider | `live_runtime_provider_requires_separate_approval` | not approved |

Unknown posture fails closed. The plan makes no API call, file download, or static source capture. No hybrid or custom access posture is created: an unresolved method is **not selected**, rather than encoded as an access-method value.

## Source-specific unresolved blockers

1. Identify and cite the exact venue-defined NOAA/NCEI product, Central Park station identifier(s), element, unit/trace semantics, and effective station history.
2. Verify whether official public files or an offline public API reproduce the finalized monthly summary; select exactly one acquisition mechanism and document authentication/rate constraints.
3. Establish whether first-posted, preliminary, revised, and final values and their historical publication/availability times can be reconstructed. If not, affected as-of uses remain blocked.
4. Verify stable historical Polymarket rule/resolution locators or an approved immutable capture method, including amendments and actual availability times.
5. Review current attribution, license/terms, retention, derived-use, and redistribution constraints for each external source. Unclear terms block acquisition/storage.
6. Obtain source-specific and storage approval; no credential may be introduced by implication.

## Corpus storage/data-plane design

The future corpus uses DuckDB-over-Parquet as the historical research plane; PostgreSQL remains operational journaling and is not used for this corpus. The weather-specific conceptual root is external/local artifact storage, not created here: `data/weather/stage3_historical_corpus/` with `raw/`, `normalized/`, and `manifests/`. DuckDB may query Parquet but no `.duckdb` database is a committed corpus artifact.

Large/raw/normalized source data, manifests containing redistributed source content, Parquet, and DuckDB files stay out of Git and require a separately approved artifact store and retention policy. Only tiny deterministic, license-cleared, synthetic or minimally derived test fixtures may be Git-tracked. Gold/evaluation views are not produced by acquisition implementation and need later approval.

## Raw/normalized/manifest boundaries

**Raw / bronze.** Content-addressed, immutable source artifacts and sidecars. Preserve original bytes where terms allow, source locator/version, request-free acquisition method, SHA-256, byte size/media type, acquisition time, publication/availability evidence, and legal posture. Never overwrite; if raw retention is disallowed, store only an approved evidence/checksum/locator receipt and block claims needing unavailable bytes.

**Normalized / silver.** Versioned Parquet records derived reproducibly from raw evidence. Normalize canonical identifiers, source contract identity, station/source selection, thresholds/comparators/units/windows, clocks, label, archive layer, provenance, disposition, and correction links. A parser version produces a new partition/version; it does not mutate history.

**Manifest / audit.** Append-only JSONL or Parquet manifest records covering every attempted candidate and artifact, including blocked/excluded records. Freeze source locator/version, access posture, SHA-256 where bytes exist, `acquired_at`, source publication/availability clocks, parser/schema versions, row counts, reconciliation status, terms review reference, and supersession links.

**Research / gold.** Later derived evaluation views only. The first acquisition implementation neither creates gold outputs nor scoring/splits/baselines.

## Point-in-time timestamp contract

Every semantic clock has its own nullable UTC-normalized field plus original timestamp/text/timezone and evidence reference:

- `market_event_start_at` / `market_event_end_at` describe the contract window;
- `market_close_at` and `evaluation_cutoff_at` describe venue close and the particular as-of decision cutoff;
- `observation_valid_at` describes what period an observation measures;
- `source_published_at` describes asserted source publication;
- `source_available_at` describes evidenced retrievability;
- `forecast_initialized_at`, `forecast_published_at`, and `forecast_available_at` are not applicable for this first label slice, never silently synthesized;
- `venue_resolution_proposed_at` and `venue_resolution_final_at` describe venue resolution/finality;
- `archive_revised_at` describes a source revision;
- `source_final_at` describes source finality and is distinct from venue finality;
- `acquired_at` describes MEG acquisition only;
- `station_source_selected_at` describes selection/adjudication of authority;
- `reviewed_at` describes reviewer action.

No timestamp substitutes for another. A record is `usable` for an as-of evaluation only if all clocks required for that use have direct evidence and `source_available_at <= evaluation_cutoff_at`; later revisions/finality/labels cannot enter earlier views. Missing or merely inferred required publication/availability evidence yields `blocked_missing_point_in_time_evidence`, not a guessed time.

## Archive/revision/finality contract

`archive_layer` is one of `first_posted`, `preliminary`, `revised`, `final`, or `superseded`. Each distinct acquired representation gets an immutable artifact/version identity, checksum, asserted valid time, evidenced publication/availability time, optional revision/finality time, and `supersedes_record_id` / `corrected_by_record_id` links.

A correction appends raw evidence, manifest event, and normalized version. It never overwrites bytes or rewrites an earlier as-of view. Final is a source-evidenced state, not “latest acquired.” First-posted is permitted only with direct evidence of first availability. Unknown layers are blocked. Venue corrections and NOAA/NCEI revisions are separately represented and linked.

## Corpus record/disposition design

This is a research representation, not a production runtime schema. A future normalized record must support:

- `condition_id`, `token_id`, `outcome`; source market reference/historical contract identity; rule version; market family;
- venue/resolver/source identities; station/observation authority with effective dates and selection provenance;
- threshold lower/upper bounds, comparator, inches, calendar-month/window/timezone, trace/missing semantics, and resolution label;
- every applicable clock above and explicit not-applicable reason for forecast clocks;
- archive/finality layer; artifact, locator, access posture, checksum, schema/parser versions, acquisition batch, and reviewer/adjudication evidence;
- leakage-group identity grouping overlapping contract outcomes/month/source window;
- disposition exactly `usable`, `blocked`, or `excluded`, a reason code/rationale, and correction/supersession linkage.

Manifest reconciliation counts all three dispositions. Blocked/excluded candidates remain auditable and cannot silently disappear from candidate, contract, label, artifact, or row totals.

## Reproducibility/checksum/versioning design

SHA-256 covers exact retained source bytes and deterministic fixtures. Manifest identities bind source locator/version, checksum, byte size, acquisition method/time, source clocks, parser version, schema version, and output partition checksums. Deterministic normalization fixes UTC conversion, units, sorting, null encoding, and serialization settings. Re-running identical inputs/version must reproduce normalized checksums and counts.

Source changes, rule amendments, parser fixes, and adjudications append versions and explicit lineage. They never edit an acquired version in place. A release manifest pins all inputs and code/schema/parser versions; data absent from the release manifest is not corpus evidence.

## First implementation file/scope boundary

After the next approval gate, one small implementation PR may create only a generic offline corpus scaffold for this selected family, with exact proposed boundaries:

- `meg/weather/stage3/corpus/contracts.py` — research record/manifest value validation only;
- `meg/weather/stage3/corpus/manifest.py` — append-only manifest construction and reconciliation;
- `meg/weather/stage3/corpus/normalize_central_park_monthly_precip.py` — caller-supplied raw-byte normalization only;
- `tests/fixtures/weather/stage3_corpus/` — tiny deterministic license-cleared inputs/manifests, no fetched corpus;
- `tests/weather/stage3/corpus/` — contract, checksum, reconciliation, no-lookahead, failure, and deterministic-output tests;
- local external artifact layout `data/weather/stage3_historical_corpus/{raw,normalized,manifests}/` — conceptual/runtime-created only after approval, never populated or committed by this plan.

No connector, HTTP client, API invocation, downloader, scraper, credential loader, scheduler, service, production schema, Gold view, or broad-family abstraction belongs in that PR. Exact filenames remain gated together with source/access/storage approval; this plan creates none of them.

## Validation/reconciliation plan

The future implementation must fail closed on:

1. incomplete source/acquisition manifests or unsupported/unknown source/access posture;
2. missing/mismatched SHA-256 or source bytes where required;
3. source artifact → parsed row → normalized record count mismatch;
4. duplicate artifact, contract-version, canonical route, or record-version identity;
5. anything other than exact canonical routing consistency;
6. impossible timestamp order or publication/availability evidence missing for the intended as-of use;
7. venue rule, resolver, NOAA/NCEI product, station, element, unit, window, or finality incompatibility;
8. absent rule version or station/source-selection provenance;
9. unknown archive/finality layer or broken correction/supersession graph (including cycles);
10. candidate totals not equaling usable + blocked + excluded;
11. no-lookahead, including a source/forecast/label/revision available after cutoff;
12. nondeterministic normalization or output-checksum mismatch.

Tiny fixtures cover first-posted→revised→final lineage, a blocked missing-availability case, an excluded incompatible-source case, duplicate detection, checksum failure, and the existing temperature ambiguity pattern without modifying existing fixtures.

## Security/terms posture

| External source | Public/private / authentication | Attribution and terms | Redistribution/storage posture |
|---|---|---|---|
| Polymarket market/rule/resolution evidence | Public-page candidate; authentication requirement for durable historical access unverified | Current terms, attribution, archive rights, and automated access unverified | Raw redistribution into Git is prohibited by this plan; external retention blocked pending review |
| NOAA/NCEI observation and station evidence | Public-source candidate; exact endpoint/file authentication and limits unverified | Exact product terms, attribution, and downstream-use language must be cited | No raw Git data; artifact-store retention/redistribution blocked pending product-specific review |
| MEG reviewer evidence | Internal, no external authentication | Preserve reviewer/audit policy | Small structured evidence may be retained only in approved artifact/fixture scope |

This is not a legal conclusion. Unclear terms remain a blocker for acquisition, storage, and redistribution. No secret or credential is added or authorized.

## Sample-sufficiency separation

Corpus correctness does not establish Stage 3 support. No universal sample N is selected. Future support thresholds must be predeclared before test inspection; exact primary roles remain `train`, `calibration`, and `test`; test outcomes cannot drive corpus membership; sparse strata cannot be silently pooled. The first implementation proves a reproducible path, not coverage, strict OOS feasibility, scoring readiness, or evidence-gate passage.

## Explicit non-approvals

This plan neither approves nor implements actual acquisition, corpus creation, source fetching, API calls, downloads, scraping, credentials/secrets, live providers, connectors, continuous ingestion, schedulers/workers/services, probabilities, training/calibration, split or baseline execution, scoring/diagnostics/evaluation, results or claims, evidence-gate execution/passage, Stage 4, paper simulation, runtime observation, trading, order placement, production runtime, or autonomy.

`offline_public_file_acquisition` and `offline_public_api_acquisition` are consideration labels only. Scraping requires separate approval; live runtime providers require separate approval. Operator-approved execution constraints remain untouched.

## Stage 3 / Stage 4 separation

This corpus path is prerequisite evidence infrastructure for possible Stage 3 retrospective evaluation only. It performs no Stage 3 scoring and cannot pass the evidence gate. Stage 4 trap-filtered paper simulation remains separate and unapproved; corpus labels, scores, or later claims cannot authorize it.

## Canonical routing posture

Canonical routing remains exactly `condition_id`, `token_id`, and `outcome`. The legacy `market_id` is non-routing only and is not a planned corpus field. External venue metadata uses `source_market_reference` / `historical_contract_identity`, never alternate routing. `token_outcome_pair` is derived only.

## Recommended next ticket

Exactly one successor is recommended: **WEATHER-BOT-STAGE3-CENTRAL-PARK-MONTHLY-PRECIPITATION-SOURCE-ACCESS-STORAGE-APPROVAL-REQUEST-01**.

It is the narrowest gate because it must resolve the exact NOAA/NCEI product/station, point-in-time capability, access mechanism, venue-history mechanism, credentials/rates, terms/attribution/retention, and external artifact-store posture before any acquisition or scaffold implementation. It must request explicit approval or record a hold/block; it must not fetch data or jump to scoring.

## Machine-checkable assignments

```text
ticket_id: WEATHER-BOT-STAGE3-HISTORICAL-CORPUS-CONSTRUCTION-AND-ACQUISITION-IMPLEMENTATION-PLAN-01
immediate_predecessor_pr: pr_388
actual_merge_sha: 62bbeadbfee3707fac316e9eab7f0ca20d254b48
artifact_scope: docs_static_test_only
plan_posture: implementation_contract_only_no_execution
approved_path_source: pr_388_narrow_implementation_planning_only
current_corpus: five_static_stage2_examples_only
corpus_coverage: not_established
sample_sufficiency: not_established
strict_oos_feasibility: not_demonstrated
stage3_scoring_readiness: not_ready
selected_first_slice: polymarket_central_park_nyc_calendar_month_total_precipitation_range_contracts_naming_noaa_ncei_finalized_monthly_summary
venue_source_role: polymarket_contemporaneous_contract_rules_and_resolution_evidence
settlement_source_role: polymarket_resolver_proposal_dispute_and_final_outcome_evidence
archive_source_role: exact_noaa_ncei_monthly_summary_product_and_central_park_station_mapping_unresolved_fail_closed
forecast_source_role: not_applicable_first_slice
polymarket_access_posture: manual_source_review
polymarket_access_posture: static_public_reference
noaa_observation_access_posture: manual_source_review
noaa_station_access_posture: static_public_reference
credential_access_posture: source_specific_credentials_required
scraping_access_posture: scraping_requires_separate_approval
live_provider_access_posture: live_runtime_provider_requires_separate_approval
publication_availability_access_posture: manual_source_review
revision_finality_access_posture: manual_source_review
reviewer_access_posture: manual_source_review
observation_acquisition_method_selection: blocked_pending_source_access_storage_approval
consideration_access_posture: manual_source_review
consideration_access_posture: static_public_reference
consideration_access_posture: offline_public_file_acquisition
consideration_access_posture: offline_public_api_acquisition
consideration_access_posture: source_specific_credentials_required
consideration_access_posture: scraping_requires_separate_approval
consideration_access_posture: live_runtime_provider_requires_separate_approval
raw_storage_posture: immutable_content_addressed_external_artifacts_with_sha256_no_destructive_overwrite
normalized_storage_posture: versioned_parquet_silver_records_for_duckdb_research_queries
manifest_storage_posture: append_only_jsonl_or_parquet_audit_manifest_all_dispositions
research_gold_posture: not_created_without_separate_approval
git_large_data_posture: prohibited_only_tiny_deterministic_license_cleared_fixtures_allowed
correction_posture: append_new_versions_preserve_as_of_views_link_supersession_no_overwrite
point_in_time_missing_evidence_posture: blocked_missing_point_in_time_evidence
record_dispositions: usable_blocked_excluded_all_reconciled
primary_sample_roles: train_calibration_test
acquisition_execution_authority: not_approved
scraping_authority: not_approved
live_provider_runtime_authority: not_approved
canonical_routing_field: condition_id
canonical_routing_field: token_id
canonical_routing_field: outcome
non_routing_legacy_identifier: market_id
derived_identifier: token_outcome_pair
recommended_next_ticket: WEATHER-BOT-STAGE3-CENTRAL-PARK-MONTHLY-PRECIPITATION-SOURCE-ACCESS-STORAGE-APPROVAL-REQUEST-01
```

## Acceptance criteria

1. The selected family, role/access matrix, unresolved blockers, data plane, record/disposition boundary, semantic clocks, revision lineage, and future implementation files are frozen without moving data.
2. Every unknown external fact fails closed; no convenient provider substitutes for venue-defined settlement semantics.
3. Raw evidence is immutable; normalized and manifest versions reconcile; corrections preserve prior as-of views.
4. Future validation covers completeness, checksums, counts, duplicates, routing, clocks, compatibility, rules, station selection, finality, lineage, dispositions, no-lookahead, and unknown access.
5. Sample sufficiency, Stage 3 scoring, Stage 4, runtime, and execution remain separate and unapproved.
6. The independent static oracle freezes headings and the complete ordered machine assignment set, and exactly one successor is named.
