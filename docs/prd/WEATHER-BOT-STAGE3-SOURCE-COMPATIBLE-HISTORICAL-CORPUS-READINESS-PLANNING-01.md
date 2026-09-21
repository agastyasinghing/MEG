# WEATHER-BOT-STAGE3-SOURCE-COMPATIBLE-HISTORICAL-CORPUS-READINESS-PLANNING-01

## Status and scope

Status: planning contract complete; current corpus readiness is not established.

This docs/static-test-only ticket defines only (1) per-record usability, (2) corpus-level coverage, and (3) sample-sufficiency assessment. It does not perform (4) data acquisition or creation or (5) Stage 3 scoring execution. The conceptual unit is a source-compatible historical market/evaluation example tied to the venue-defined settlement outcome. This is a readiness plan, not a production schema, dataset, or execution approval.

The target is source-compatible venue settlement truth, not generic weather truth. An observation cannot become a usable label merely because it is meteorologically plausible or authoritative in isolation; it must match the historical contract's controlling resolver, source chain, rule version, measurement semantics, and finality treatment.

## Immediate predecessor and merge verification

The required predecessor is PR #384 at actual merge commit `b374dbc1c726abf6d3e167ce215229ac47fbf98c`. An implementation checkout must establish that this commit is `HEAD` or an ancestor of `HEAD`; no `origin/main` or local `main` branch is required.

## Current five-example corpus baseline

The repository baseline is exactly five Stage 2 static JSON fixtures under `tests/fixtures/weather/`: three synthetic historical-label examples and two real source-backed examples. The real pair contains one pass candidate and one blocked conflict candidate. These examples support static validation and reviewer inspection; they are not a historical evaluation corpus, do not establish coverage, and are not sufficient for meaningful strict-OOS retrospective scoring.

Current corpus: `five_static_stage2_examples_only`. Current sample sufficiency: `not_established`.

## Per-record usability requirements

A future example is usable only when supplied evidence establishes every applicable requirement below without hindsight repair. These are conceptual review requirements, not fields for a production schema.

| Requirement | Required evidence or decision |
|---|---|
| canonical route | Exactly `condition_id`, `token_id`, and `outcome` identify the routed venue outcome. |
| historical identity and rules | Historical market/contract identity and the venue rule snapshot effective for settlement are preserved. |
| market family | The venue-defined weather market family is identified. |
| resolver/source | Resolver identity and the exact source chain used by the venue are identified. |
| observation authority | Station, observation point, or classification authority is identified when applicable. |
| measurement semantics | Measurement window and, when applicable, threshold, comparator, unit, rounding, and trace semantics are explicit. |
| resolution label | The historical resolution label is source-compatible with the venue-defined settlement outcome. |
| observation timing | Source publication/availability and observation availability timestamps are evidenced. |
| input timing | Forecast/input publication and availability timestamps are evidenced when applicable. |
| archive layer | First-posted, preliminary, revised, final, or other applicable archive/revision/finality layer is identified. |
| point-in-time provenance | The exact evidence available at each evaluation cutoff is auditable. |
| selection provenance | Station/source selection and any fallback are explained and fixed from venue rules rather than hindsight. |
| traps and adjudication | Applicable trap category, conflict, review, and adjudication status and evidence are preserved. |
| disposition | Exactly one of `usable`, `blocked`, or `excluded` is assigned with a reason. |

`usable` means all applicable source-compatibility, semantic, provenance, timing, and adjudication requirements are evidenced for the intended analysis. `blocked` means potentially remediable required evidence or adjudication is missing. `excluded` means the example is incompatible with the declared evaluation population or cannot be made evidentially safe. Neither blocked nor excluded examples may enter scoring as usable examples.

## Corpus-readiness dimensions

| Dimension | Readiness evidence required |
|---|---|
| source/resolver compatibility | Counts and exceptions demonstrate exact venue resolver/source alignment. |
| point-in-time provenance coverage | Complete versus incomplete as-of evidence is counted and incomplete records are blocked. |
| publication-time availability coverage | Observation and applicable forecast/input publication and availability clocks support replay. |
| revision/finality coverage | First-posted, preliminary, revised, and final layers are identified and not silently mixed. |
| market-family coverage | Supported and sparse families are visible without pooling incompatible settlement semantics. |
| station/source coverage | Counts and gaps by station, observation point, authority, and source are visible. |
| temporal/year coverage | Date spans, years, seasons, gaps, and regime limitations are reported. |
| threshold/comparator coverage | Counts by threshold, distance/bucket, comparator, unit, rounding, and trace treatment are visible. |
| forecast-horizon coverage where applicable | Counts and gaps by decision-time horizon/product are reported. |
| trap-category coverage | Counts and adjudication outcomes by controlling trap category are reported. |
| blocked/excluded-example accounting | Every non-usable example and reason remains visible in denominators and audit totals. |
| strict temporal OOS feasibility | Chronological cutoffs and non-overlapping leakage groups yield supportable train/calibration/test roles. |
| leave-station-out feasibility where applicable | Held-out stations have usable support and no station leakage. |
| leave-year-out feasibility where applicable | Held-out years have usable support and no future-year leakage. |
| climatology baseline feasibility | Only history available before each cutoff supports the declared family/station/season strata. |
| persistence baseline feasibility | The predeclared persisted quantity and conversion rule have a compatible prior state legitimately available before `prediction_as_of` and the applicable cutoff. |
| calibration/threshold-bucket feasibility | Reproducible buckets retain visible support without unsafe pooling. |
| sample-size and uncertainty reporting | Every aggregate and diagnostic exposes usable sample support, exclusions, sparsity, and uncertainty. |

## Point-in-time and no-lookahead requirements

Every evaluation input, resolution artifact, archive layer, and rule snapshot must carry evidence of when it was published and when it became available to the evaluation process. Nominal model initialization, observation time, or final archive date is not a substitute for availability time. Later revisions may be retained as labeled layers but must not be substituted into an earlier as-of view. Venue rule changes, station/source selection, fallback choices, and adjudication cannot be reconstructed with future knowledge.

If publication or availability ordering cannot be established, the record fails closed as blocked or excluded. Split construction must use event and availability cutoffs, preserve leakage groups, and prevent the label, future observations, future revisions, later forecasts, or held-out-period statistics from influencing predictions or baselines.

## Coverage and stratification plan

A future readiness review must publish counts by every relevant cross-section of family, resolver/source, station or authority, year/time period, forecast horizon, threshold/comparator bucket, archive/finality layer, and trap category. It must show usable, blocked, and excluded counts; provenance-complete and incomplete counts; temporal spans and gaps; and whether cross-strata combinations are supported or sparse.

Strata may be combined only when their resolver, venue rules, measurement semantics, availability clocks, and evaluation interpretation are demonstrably compatible. The review must identify unsupported strata rather than conceal them in an aggregate. Coverage is a property of the declared evaluation claims, not merely a total row count.

## Sample-sufficiency assessment method

There is no universal numeric minimum sample count in this contract. A future review must demonstrate sufficiency from observable corpus diagnostics: counts by relevant family/source/station/year/horizon/threshold stratum; usable versus blocked/excluded counts; provenance-complete versus incomplete counts; temporal coverage; split/fold feasibility; baseline-history availability; sparse-stratum identification; and uncertainty/sample-support visibility.

The assessment must connect each intended metric, diagnostic, split, baseline, and claim to its actual eligible support. It must report attrition before and after compatibility/provenance/trap review, fold-level support, missingness, concentration, and uncertainty limitations. A readiness finding fails closed when strict-OOS evaluation, required baselines, or required diagnostics cannot be supported without collapsing incompatible strata, leaking future information, or using insufficiently evidenced records.

No universal numeric minimum is selected here. Before test outcomes are inspected, future evaluation work must select and freeze its evaluation-specific sample-support/sufficiency policy; any thresholds or decision rules required for the relevant metric, diagnostic, split, baseline, claim, fold, role, and stratum; sparse-bucket handling; pooling rules; uncertainty method; and uncertainty interval level. Those choices may not be changed after seeing test outcomes. Corpus-readiness diagnostics alone do not authorize a post-hoc declaration that observed sample counts are "good enough." Sparse or insufficient strata remain blocked or insufficient rather than being silently pooled. This ticket selects no numeric threshold, confidence or interval level, bin count, bootstrap design, resampling block length, weighting constant, or other numeric minimum.

The five current examples do not establish sample sufficiency.

## Strict-OOS feasibility requirements

Before scoring, the proposed evaluation population must permit reproducible chronological or rolling-origin assignments whose training evidence and derived statistics were available before each evaluation cutoff. The readiness review must demonstrate usable support in each required fold, no overlap or leakage across linked markets/evaluation examples, and viable leave-station-out and leave-year-out analyses where applicable. Unsupported split types must be declared infeasible, not weakened or backfilled with future information.

No split is assigned or executed by this ticket.

## Baseline-feasibility requirements

Climatology feasibility requires adequate prior, source-compatible history for the declared family/station/season or other predeclared stratum at every cutoff. Persistence feasibility must support the already-predeclared persisted quantity identity, conversion-rule identity, compatible prior state, and point-in-time availability before `prediction_as_of` and the applicable cutoff. A previous observation existing somewhere in history is not enough: it must be compatible with that predeclared persistence quantity and conversion rule and legitimately available at prediction time. This plan does not define either policy. The future review must count baseline-eligible examples by fold and stratum, document cold starts and missing histories, and prevent held-out data from contributing to baseline construction. If either required baseline cannot be generated fairly, Stage 3 readiness fails closed.

No baseline value is generated or executed by this ticket.

## Blocked and excluded data accounting

All discovered candidate examples must remain reconcilable as usable, blocked, or excluded. The review must report counts and reason codes for missing provenance, unavailable timestamps, source mismatch, rule ambiguity, station ambiguity, semantic mismatch, finality ambiguity, unresolved traps, adjudication need, duplicate/leakage-group conflict, and out-of-population exclusion. It must preserve original totals, transitions after review, reviewer/adjudication evidence, and avoid silently dropping failures. Blocked and excluded examples cannot inflate usable sample support.

## Acquisition and corpus-build boundary

A later, separately approved corpus-construction/acquisition effort might need venue market and rule history; official resolver/archive observations; station metadata; distinct first-posted, preliminary, revised, and final archive layers; historical forecast/model products when required; publication and availability metadata; and reviewer/adjudication evidence.

Before any such information can enter Stage 3 evidence, its venue/source compatibility, applicable rule version, observation or forecast identity, archive/finality layer, publication and availability time, access provenance, selection provenance, and adjudication trail must be point-in-time auditable. Merely finding a final value or a modern archive page is insufficient.

This planning ticket does not fetch, create, download, scrape, acquire, generate, or expand data. It grants no authority for live provider connectors, network calls, scraping, API clients, credentials, downloads, source fetching, or dataset generation. Corpus building requires a separate explicit approval boundary.

## Explicit current readiness finding

Per-record readiness: the plan is defined, but the five existing examples are not reclassified or promoted by this ticket. Coverage readiness: `not_established`. Strict-OOS feasibility: `not_demonstrated`. Sample sufficiency: `not_established`. Earliest remaining blocker: an approved, separately bounded corpus-construction/acquisition request followed by an evidence-backed corpus-readiness review; acquisition itself is not approved here.

Therefore meaningful Stage 3 strict-OOS retrospective scoring is `not_ready` and must not begin from the current five-example baseline.

## Stage 3 execution separation

This plan establishes review criteria only. It does not generate probabilities, train or calibrate models, assign or execute splits, build or execute baselines, calculate scores or diagnostics, run an evaluation, create results or claims, or execute/pass an evidence gate. Even a future corpus-readiness finding would be an input to a separate Stage 3 execution approval decision, not execution authority.

## Stage 4 separation

Stage 4 trap-filtered paper simulation remains separate and unapproved. Corpus readiness or later Stage 3 evidence cannot authorize paper simulation, runtime observation, trading, order placement, production runtime, or autonomy.

## Canonical routing posture

Canonical routing remains exactly `condition_id`, `token_id`, and `outcome`. The legacy `market_id` identifier remains non-routing only. `token_outcome_pair` remains derived only. Historical market identity and venue metadata may support audit and grouping but cannot replace the canonical route.

## Explicit non-approvals

This ticket does not approve or implement corpus construction or expansion, external acquisition, source fetching, provider/API connectors, scraping/downloads, credentials, probability generation, model training/calibration, split execution, baseline execution, score/diagnostic computation, evaluation execution, result generation, claim generation, evidence-gate execution/passage, persistence, reports/exports, paper simulation, runtime observation, trading, order placement, production runtime, or autonomy.

## Recommended next ticket

The exactly one recommended successor is `WEATHER-BOT-STAGE3-HISTORICAL-CORPUS-CONSTRUCTION-AND-ACQUISITION-APPROVAL-REQUEST-01`. It must decide a narrow corpus construction/acquisition boundary before any data is fetched, acquired, created, downloaded, scraped, generated, or expanded; it must not itself assume approval or skip directly to Stage 3 scoring.

## Machine-checkable assignments

```text
ticket_id: WEATHER-BOT-STAGE3-SOURCE-COMPATIBLE-HISTORICAL-CORPUS-READINESS-PLANNING-01
immediate_predecessor_pr: pr_384
actual_merge_sha: b374dbc1c726abf6d3e167ce215229ac47fbf98c
artifact_scope: docs_static_test_only
conceptual_unit: source_compatible_historical_market_evaluation_example_tied_to_venue_defined_settlement_outcome
current_corpus: five_static_stage2_examples_only
synthetic_fixture_count: 3
real_source_backed_fixture_count: 2
per_record_contract: defined_planning_only
coverage_readiness: not_established
strict_oos_feasibility: not_demonstrated
sample_sufficiency: not_established
stage3_scoring_readiness: not_ready
acquisition_authority: not_approved
stage3_execution_authority: not_approved
stage4_posture: separate_and_unapproved
canonical_routing_field: condition_id
canonical_routing_field: token_id
canonical_routing_field: outcome
non_routing_field: market_id
derived_identifier_field: token_outcome_pair
recommended_next_ticket: WEATHER-BOT-STAGE3-HISTORICAL-CORPUS-CONSTRUCTION-AND-ACQUISITION-APPROVAL-REQUEST-01
```

## Acceptance criteria

- The predecessor is frozen as PR #384 and actual merge SHA `b374dbc1c726abf6d3e167ce215229ac47fbf98c`.
- The current baseline is exactly five static examples: three synthetic and two real source-backed, and sample sufficiency remains not established.
- Per-record usability is distinct from corpus coverage and sample sufficiency; acquisition and Stage 3 execution remain separate.
- Every required per-record category and all 18 corpus-readiness dimensions are specified without creating a production schema.
- Point-in-time availability, no-lookahead, strict-OOS, baseline feasibility, stratification, and blocked/excluded accounting fail closed.
- No universal numeric sample minimum is invented; sufficiency depends on observable support and uncertainty diagnostics.
- Canonical routing and all explicit non-approvals remain intact.
- Exactly one successor preserves the separate corpus construction/acquisition approval boundary.
