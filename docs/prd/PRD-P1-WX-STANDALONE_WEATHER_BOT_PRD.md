# MEG Weather Bot PRD

**Document type:** Standalone Product Requirements Document
**Status:** Frozen research-stage PRD (Stage 0 of WX-RESEARCH-06 evidence ladder)
**Date:** May 26, 2026
**Reconciled against:** PRD-P1-WX-UNBLOCK, PRD-P1-WX-KICKOFF, PRD-P1-WX-01, PRD-P1-WX-02, PRD-P1-WX-03, and PRD-P1-WX-04. This PRD does **not** supersede those planning documents. Where this PRD and a WX planning document discuss the same machine-checkable closed-set vocabulary (readiness state, summary severity, review posture), the WX planning document governs and this PRD has been aligned to it. Where this PRD adds research synthesis (canonical event ontology, trap taxonomy, evidence ladder, alpha-hypothesis framework, false-edge framework, quantitative roadmap) not addressed by a WX planning document, this PRD is the active synthesis until explicitly revised. See the Reconciliation notes appendix for the full list of alignments performed.
**Inherits from:** MEG Master PRD v4.1; WX-RESEARCH-01 through WX-RESEARCH-06; BWX-RESEARCH-05A; BWX-RESEARCH-05Q
**Authoritative successors:** This document is the source of truth for any future Codex implementation/planning ticket, provider-gate decision, validation design, and human-review design that touches Weather Bot. Conflicts between this PRD and a later child document are resolved in favor of this PRD until this PRD is explicitly revised.

---

## Global non-approval banner (read first, applies to every section below)

This PRD is a **research and planning document**. It explicitly does NOT approve any of the following, in any section, under any reading, regardless of phrasing elsewhere in the document:

- connector implementation
- external API calls
- provider credentials
- config loading
- secret reading
- runtime execution
- forecast pulls
- forecast model implementation
- data ingestion
- live provider usage
- production monitoring
- trading strategy
- position sizing
- order placement
- live market execution
- autonomy
- profitability claims
- implementation-adjacent tickets before the relevant stage-gate evidence (as defined in §17) exists

Throughout this PRD, the words "must," "shall," and "is required to" describe **design intent for future, separately approved work**, not authorization to build. The words "candidate," "hypothesis," "research target," and "future design" mark concepts that are explicitly **not approved** for implementation by this document.

Profitability is not claimed. Market prices are not treated as truth. Generic provider data is not treated as resolver truth. Forecast-provider truth is not treated as settlement truth. Source/station/window/threshold/revision/classification uncertainty is not collapsed into ordinary forecast uncertainty. Research hypotheses are not converted into implementation approval. "Alpha hypothesis" is not converted into "trading strategy." Nothing in this PRD implies the system may trade or execute autonomously.

Confidence values used in this document, where labeled, are drawn from a closed set: `confirmed`, `unclear`, `unknown`. Trap severities, where labeled, are drawn from a closed set: `caution`, `blocking`. No hybrid or invented values are used.

---

## 1. Product thesis and MEG fit

**Thesis.** Weather Bot is MEG's first canonical event graph proving ground. Its purpose is not to "forecast weather" but to demonstrate, end to end, that MEG can model a prediction-market settlement object as a **source-defined canonical event**, separate that event from generic real-world weather, separate resolver truth from convenience data, separate forecast uncertainty from resolution uncertainty, and route the result through trap detection, calibration, validation, and human review — without ever conflating any of those layers, and without ever implying autonomous execution.

**Why Weather Bot belongs inside MEG.** The MEG Master PRD v4.1 sequences the system as rail-first, weather-first, MEG-second: a shared Polymarket-style rail proven by a tightly scoped weather strategy before any whale lead-lag thesis is layered on. Weather is selected not because the bot is meant to be a weather product but because weather contracts more often expose, in published rules, the exact normalization fields a canonical event graph needs — variable, threshold, comparator, time window, location or station, source agency, and settlement timing. Where many political, social, or impact markets bury settlement semantics in narrative or moderation discretion, weather markets sometimes name the exact climate product or station they resolve against. That makes weather the cleanest domain in which to *prove the canonical event graph itself*, before the graph is asked to handle harder domains. (WX-RESEARCH-01.)

**Why weather is a good first proving ground — without being a generic weather bot.** The proof is precisely that the bot does *not* treat weather as weather. It treats each weather market as an instance of a generalizable problem: a *venue-defined settlement object* whose probability is conditioned on a specific resolver/source/station/window/threshold/revision/classification rule. The work of Weather Bot is the work of canonicalizing that rule, comparing it against compatible data sources, scoring source compatibility, tagging traps, decomposing uncertainty, generating reviewer-readable intelligence, and refusing to act when any required field is unpinned. Generic "forecast says X, market says Y" reasoning is exactly the failure mode this design rejects.

**Generalization claim (intentionally narrow).** If MEG can canonicalize a station-anchored daily temperature market, distinguish it from a city-area monthly precipitation contract that uses a first-complete-report rule, distinguish either from a tropical-cyclone classification market that resolves on NHC advisory state at issuance time rather than HURDAT2 best-track post-analysis, and refuse to conflate any of those with a convenience-provider archived forecast — then the same canonical pattern is portable, by hypothesis, to other event-graph domains where resolution semantics are also venue-defined: election certification timing, sports-fixture statistical settlement, regulatory-action timestamps, economic-indicator release products, and similar source-specified objects. This portability is asserted as a design hypothesis, not as a validated capability.

**What Weather Bot is NOT, restated for clarity.** It is not a generic weather forecast bot. It is not a simple weather-API wrapper. It is not a live trading bot. It is not a "forecast says X, market says Y" comparator. It is not an implementation-ready connector project. It is not an autonomy or order-placement system. It is a *source-defined event-intelligence system* whose true target variable is the probability that the venue-defined market resolves Yes under its specific resolver/source/station/window/threshold/revision/classification rule.

---

## 2. Problem statement

Weather prediction markets are routinely misread as questions about the weather. They are not. They are questions about whether a specific named source product, evaluated against a specific named station or geography, over a specific named time window, against a specific threshold and comparator, with specific trace and missing-value handling, under a specific revision/finality rule, and under a specific classification or discretionary authority, will report a value that satisfies the contract.

The four research packets WX-RESEARCH-01 through WX-RESEARCH-03 and the deep alpha/quant packets BWX-RESEARCH-05A and BWX-RESEARCH-05Q converge on this point: the same headline can hide different real-world observation models. A contract can reference a *station* when the headline says a *city*. A contract can use a *daily report published the next morning* rather than live intraday values. A contract can *freeze on the first complete report* rather than the corrected archive. A contract can use a *third-party display page* rather than a government primary source. A contract can permit *venue review, fallback sources, or source replacement* if the original source becomes unreliable. (WX-RESEARCH-01, WX-RESEARCH-03.)

Naive weather-API comparisons therefore manufacture false edge. WeatherAPI.com's own pricing FAQ states its "historical weather" is archived forecast data and "not actuals" — direct disqualification for any observed-event resolution use. Meteostat point data interpolate across multiple stations and, in default settings, blend observations with model-derived data. Open-Meteo automatically stitches multiple model runs and selects the highest-resolution model for each point. OpenWeather returns "measured or calculated" values from a proprietary blended model. None of these is intrinsically wrong as a *modeling input*; all of them are intrinsically wrong as *resolution evidence* for a market whose rule names a different operative product. (WX-RESEARCH-02, WX-RESEARCH-03, BWX-RESEARCH-05A.)

The probability estimation problem is therefore not `P(weather variable crosses threshold)`. It is `P(the venue-defined source/station/window/threshold/revision/classification rule resolves Yes)`. Those are different objects. A model perfectly calibrated to the former can be directionally wrong on the latter even when the meteorology is correct, because the resolution semantics are external to the meteorological process. (WX-RESEARCH-04, BWX-RESEARCH-05Q.)

The first job of Weather Bot is therefore to *make this distinction explicit, structurally enforced, and reviewable*. Every downstream capability — calibration, alpha hypothesis evaluation, false-edge detection, validation — must inherit this distinction or it is invalid.

---

## 3. Goals

The Weather Bot PRD defines the following goals. All of them are **research and design goals** for the document and for the future, separately approved work this document is intended to inform. None of them authorizes implementation by itself.

1. **Model weather markets as canonical source-defined events.** Define a canonical weather event schema (§6) that exposes the resolver/source/station/window/threshold/revision/classification fields as first-class objects, not as residual annotations on a generic weather record.

2. **Distinguish resolver truth from convenience data.** Maintain a strict, structurally enforced separation (§§8–10) between official resolver sources, official forecast/observation products, climate archives, forecast/model providers, historical-data providers, convenience APIs, aggregators, and venue-discretionary resolvers. No convenience-provider value may be treated as a settlement-equivalent value.

3. **Identify trap/risk conditions.** Implement, in design, a trap taxonomy (§11) controlled by WX-RESEARCH-03 severity. Trap detection must be capable of producing `caution` and `blocking` outcomes for the families WX-03 names, and `blocking` outcomes must fail closed.

4. **Decompose uncertainty by layer.** Decompose probability into forecast, observation, resolver/source, station/location, time-window, threshold/comparator, rounding/unit, trace/missing, revision/finality, classification authority, market mapping, provider compatibility, and market microstructure components (§§12–13). These layers must remain individually expressible in human-review output and must not be silently collapsed into a single number.

5. **Support human-reviewable intelligence.** Produce structured human-review packets (§24) that explain, for each market, the canonical event interpretation, the active resolver/source mapping, the active trap flags, the active uncertainty components, any active alpha hypothesis, any active false-edge risks, the validation stage achieved, and the no-trade/caution/blocking decision with its reason.

6. **Support staged validation before implementation.** Inherit, in full and without weakening, the WX-RESEARCH-06 seven-stage evidence ladder (§17) as the safety backbone. No implementation-adjacent ticket may be opened until the relevant stage-gate evidence exists.

7. **Create a foundation for later tickets after explicit approval gates.** Define a planning-level roadmap (§§27, 30) whose stages map cleanly to the evidence ladder, so that future tickets can reference an unambiguous gate before they can be drafted.

8. **Generalize beyond weather only after weather is proven.** Keep the canonical event ontology (§6), source/provider architecture (§8), trap taxonomy (§11), uncertainty decomposition (§12), and validation ladder (§17) abstract enough that the same shapes can later host other event-graph domains, but **do not** approve generalization until weather has cleared the evidence ladder.

---

## 4. Non-goals and explicit non-approvals

The following are explicit non-goals and explicit non-approvals of this PRD. Every item on this list is **not approved** by this document. Each item also serves as a fail-closed gate elsewhere in the document.

| Non-goal / non-approval | Notes |
|---|---|
| Connector implementation | No connector code, scaffolding, or integration-test fixture against a live provider is approved. |
| External API calls | No outbound HTTP, gRPC, websocket, or other network call to any weather provider is approved. |
| Provider credentials | No credentials, tokens, API keys, OAuth flows, or service-account material may be obtained, stored, or referenced by Weather Bot under this PRD. |
| Config loading | No runtime config loader, secret reader, or environment-variable consumer is approved for Weather Bot under this PRD. |
| Secret reading | No reading of `.env`, vaults, secret managers, or equivalent is approved for Weather Bot under this PRD. |
| Runtime execution | No production or staging runtime process is approved to execute Weather Bot logic. |
| Forecast pulls | No forecast pull, model-output retrieval, observation pull, or archive pull is approved. |
| Forecast model implementation | No model training, fitting, or scoring run is approved. |
| Data ingestion | No ingestion pipeline — batch, streaming, or hybrid — is approved. |
| Live provider usage | No production use of any provider, paid or free, is approved. |
| Production monitoring | No production observability target is approved for Weather Bot under this PRD. |
| Trading strategy | No trading strategy, signal, or proposal generator is approved. |
| Position sizing | No sizing logic, Kelly logic, or capital-allocation logic is approved for Weather Bot under this PRD. |
| Order placement | No order placement, including paper, canary, or test, is approved for Weather Bot under this PRD. |
| Live market execution | No execution path is approved. |
| Autonomy | No autonomous behavior of any kind is approved. |
| Profitability claims | No claim that Weather Bot is or will be profitable is made or approved. |
| Implementation-adjacent tickets before stage-gate evidence | No ticket may be opened that would touch any of the above before the relevant stage in §17 has been cleared with the required evidence. |

**Interaction with the broader MEG rail.** The MEG Master PRD v4.1 separately specifies an operator-approval-queue architecture, a paper-and-canary execution rail, risk gates, and a heartbeat. Nothing in this Weather Bot PRD overrides those non-approvals or alters their gating. In particular, the MEG-wide rule that no strategy receives autonomous execution authority in any phase covered by the master PRD is reaffirmed here.

---

## 5. Core principle: source-defined market events

The single controlling principle of this PRD, from which every other section is derived, is:

> **Weather Bot must model the market's settlement rule, not the generic weather phenomenon.**

Operationally, this means that the canonical object for Weather Bot is not "Seattle precipitation in January" or "Will it rain in LA tomorrow?" It is the venue-defined settlement rule that resolves a specific market: a specific named source product, evaluated against a specific named station or geography, over a specific named time window, with specific threshold and comparator semantics, in specific units with specific rounding, with specific trace and missing-value treatment, under a specific revision/finality rule, under a specific classification authority where applicable, and subject to any specific venue discretion/fallback/invalidation provisions.

The principle is supported, controlling-fashion, by WX-RESEARCH-01, WX-RESEARCH-03, WX-RESEARCH-04, BWX-RESEARCH-05A, and BWX-RESEARCH-05Q. WX-RESEARCH-01 establishes the ontology: "the canonical event MEG must model is not merely 'rain in Seattle' or 'snow in Denver' — it is usually something like *monthly precipitation total for exchange-designated NWS station X, from the first qualifying daily climate report containing all calendar days of month Y, with trace counted as 0.00 and later revisions ignored.*" WX-RESEARCH-04 promotes that ontology into a probability statement: `P(market Yes) = Σ_r P(r) · P(g_r(Y_r) = Yes | r, forecast)`, where `r` indexes plausible resolution scenarios. BWX-RESEARCH-05Q formalizes the math: the target is `P(R(O(Y)) = Yes | I)`, not `P(Y > τ | I)`.

The fields below are mandatory parts of any "weather market" identity carried by Weather Bot. None of them is optional. None of them is allowed to be silently defaulted. If a field cannot be pinned from the venue's published rule text and the named source's published documentation, the market is **not** representable as a canonical event and **must** be treated as `blocking` until human review resolves the ambiguity.

| Mandatory field | Description |
|---|---|
| Resolver source | The exact source product/page/archive that the venue rule names. Not the agency family alone. |
| Source station | The exact station ID and station record, where station-anchored. |
| Measurement window | The exact start and end timestamps, in the exact timezone or climatological-day convention used by the source. |
| Threshold semantics | The exact threshold value and its source-native units. |
| Comparator semantics | The exact comparator (`≥`, `>`, `≤`, `<`, `=`, bracketed range, etc.). |
| Unit and rounding | The unit the source publishes in, the precision the source publishes at, and the rounding rule the venue applies. |
| Trace and missing-value rule | Whether trace counts as 0, as Yes, or otherwise; whether a missing day counts as 0, missing, or otherwise. |
| Revision / finality behavior | Whether the venue freezes on first-posted, on a named publication, or on a later archive layer; whether later revisions are ignored. |
| Classification authority | For event-classification markets (severe, tropical, etc.), the exact authority and product layer. |
| Venue wording | The full headline plus rules-summary plus contract terms, archived at decision time. |
| Market-specific settlement logic | Any cancellation, invalidation, fallback, source-replacement, or review/discretion clauses that the venue reserves. |

If any of these is unpinned, the market is `blocking` for Weather Bot processing per WX-RESEARCH-03.

---

## 6. Canonical event ontology / event graph model

The Weather Bot canonical event is a structured object intended to be the durable identity of a single venue-defined settlement event. Multiple markets at multiple venues may map to the same canonical event only when every load-bearing field below matches. Same canonical event identity is **identity**, not correlation; near matches must remain explicitly near matches.

### 6.1 Canonical event fields

The fields below derive from WX-RESEARCH-01 and WX-RESEARCH-03 (which collectively name `station_id`, `source_product`, `freeze_rule`, `comparator`, `aggregation_rule`, `trace_rule`, `missing_rule`, `fallback_chain`, `observable_type`, `rounding_rule`, `source_url`, `geographic_precision`, `bracket_rule`, `classification_authority`, `cutoff_time`, `basin`, `source_chain`, `settlement_time`, `time_window_start`, `time_window_end`, `timezone`, `country_source`, `day_definition`, `venue_status_rule`, `review_state`, `archive_layer`, `manual_override_flag`, and `canonical_event_summary` as required mapping fields). Field names below are normative for design discussion; physical schema design is a future ticket.

| Field group | Field | Required | Notes |
|---|---|---|---|
| identity | `canonical_event_id` | yes | Stable hash over the load-bearing identity fields below. Same id ⇒ same event. |
| identity | `domain` | yes | `weather` for this PRD. Reserved as an extensibility hook. |
| identity | `market_family` | yes | One of the families enumerated in §7. |
| identity | `venue_market_reference` | yes | Venue-specific market id, contract id, or stable URL. |
| identity | `raw_market_wording` | yes | Headline plus rules summary plus full contract terms, archived at decision time. |
| identity | `canonical_event_summary` | yes | Human-readable single-sentence summary of the canonical event. |
| location | `event_location_label` | yes | The venue's place label (e.g., "Seattle"). |
| location | `station_id` | conditional | Required if the venue rule names a station or a station-anchored source product. |
| location | `station_source_authority` | conditional | E.g., NCEI HOMR record, FAA station record. |
| location | `geographic_precision` | yes | One of `station`, `airport_complex`, `city_area`, `region`, `state`, `country`, `basin`, `other_specified`, `unspecified`. `unspecified` is `blocking`. |
| resolver | `resolver_source` | yes | The exact named source product. Not just the agency family. |
| resolver | `resolver_source_authority` | yes | E.g., NWS CLI, NWS NOWData, NCEI CDO, NCEI GHCN-Daily, NCEI ISD, NCEI Storm Events, NHC advisory archive, NHC TCR, NHC HURDAT2, SPC outlook, SPC storm reports, Weather Underground station page, third-party display page, venue-discretionary resolver. |
| resolver | `source_url` | yes | Stable source URL or stable archive identifier. |
| resolver | `source_chain` | yes | Ordered fallback chain as published by the venue rule, including any explicit METAR or alternate-product fallbacks. |
| resolver | `archive_layer` | yes | One of `first_posted`, `next_morning_climate_report`, `monthly_summary`, `archive_quality`, `post_analysis_best_track`, `final_official_archive`, `other`, `unclear`. |
| variable | `measurement_variable` | yes | E.g., daily max temperature, daily min temperature, daily mean temperature, hourly temperature, daily total precipitation, monthly total precipitation, new snowfall, snow depth, snow water equivalent, sustained wind, gust, tropical-cyclone classification, etc. Snowfall, snow depth, and SWE are *different* variables. (WX-RESEARCH-03.) |
| variable | `observable_type` | yes | Distinguishes flow versus stock (snowfall versus snow depth), measured versus estimated wind, etc. |
| threshold | `threshold_value` | yes | In source-native units. |
| threshold | `threshold_unit` | yes | The source's native unit, not a converted equivalent. |
| threshold | `comparator` | yes | Exact comparator. |
| threshold | `bracket_rule` | conditional | For bracketed/range markets. |
| threshold | `rounding_rule` | yes | Source-native precision plus the venue's rounding rule. Full source precision governs where stated. |
| time | `time_window_start` | yes | Inclusive lower bound timestamp. |
| time | `time_window_end` | yes | Inclusive/exclusive upper bound, made explicit. |
| time | `timezone` | yes | One of `local_civil`, `local_standard`, `local_climatological_day`, `UTC`, `0601_UTC_climatological_day`, `other`, `unclear`. |
| time | `aggregation_method` | yes | E.g., `daily_max`, `daily_min`, `daily_total`, `monthly_total_first_complete_report`, `monthly_total_archive`, `multi_day_event_total`, etc. |
| handling | `trace_rule` | yes | One of `trace_as_zero`, `trace_as_yes`, `trace_excluded`, `unclear`. |
| handling | `missing_rule` | yes | E.g., `missing_as_zero`, `missing_as_missing`, `missing_blocks_resolution`, `unclear`. |
| revision | `freeze_rule` | yes | E.g., `first_complete_report`, `value_at_expiration_time`, `first_qualifying_observation`, `post_analysis`, `unclear`. |
| revision | `revision_treatment` | yes | E.g., `later_revisions_ignored`, `final_archive_governs`, `unclear`. |
| authority | `classification_authority` | conditional | For event-classification markets: NHC, SPC, NCEI Storm Events, local WFO, venue moderator, etc. |
| authority | `classification_time_layer` | conditional | E.g., `advisory_at_issuance`, `intermediate_advisory`, `best_track_post_analysis`, `tropical_cyclone_report`, `preliminary_severe_report`, `final_storm_data`, `monthly_state_count`. |
| compatibility | `provider_source_compatibility_flags` | yes | Per-provider compatibility judgments (see §8). |
| compatibility | `source_compatibility_status` | yes | One of `compatible`, `partially_compatible`, `incompatible`, `unclear`. |
| traps | `active_trap_flags` | yes | Set of trap codes from §11. |
| traps | `controlling_trap_severity` | yes | The strictest severity across active flags. One of `caution`, `blocking`. |
| uncertainty | `active_uncertainty_components` | yes | Set of uncertainty layers from §§12–13. |
| review | `human_review_state` | yes | One of `unreviewed`, `caution_under_review`, `blocking_under_review`, `reviewed_pass`, `reviewed_caution`, `reviewed_block`. |
| review | `manual_override_flag` | yes | Indicates a human override has been recorded. |
| venue | `venue_status_rule` | yes | Cancellation, invalidation, void, review-committee, and source-replacement clauses. |
| venue | `review_state` | yes | Venue-level outcome-review state, if any. |

The `canonical_event_id` is the stable identity hash. Two markets share `canonical_event_id` only when the entire identity-relevant set of fields matches exactly. Otherwise they are explicitly distinct events, even when they are correlated, even when the headline reads identically, even when the underlying weather is the same.

### 6.2 Equivalence levels between markets

Drawn directly from WX-RESEARCH-01: "Same event versus same resolver" is the central distinction. Markets are grouped into four explicit equivalence classes. Implicit conflation across classes is not allowed.

| Equivalence class | Definition | Allowed treatment |
|---|---|---|
| Exact-equivalent | All load-bearing canonical fields match; same `canonical_event_id`. | May be treated as one market for purposes of canonical-event reasoning. Cross-venue execution is **not** approved by this PRD and remains gated by §17. |
| Near-equivalent | Same variable, station, window, and threshold semantics, but a different resolver source product, archive layer, or freeze rule. | **Distinct events**. May be modeled in parallel for source-disagreement research only; may not be treated as a single edge. |
| Related but non-equivalent | Same broad weather phenomenon (e.g., "rain in Seattle") but materially different station, window, comparator, archive, or authority. | **Distinct events**. Useful as coherence checks (§14) but not as equivalences. |
| Incompatible | Different variable family, different geography, or fundamentally different resolution authority. | **Distinct events**. Not comparable. |

**Correlation is not equivalence.** Two threshold-ladder bucket markets on the same station are correlated, not equivalent. Two airport markets in the same metro area are correlated, not equivalent. CME-style location basis-risk literature explicitly formalizes this for standardized reference indexes; BWX-RESEARCH-05A confirms the structural mechanism for Weather Bot. Cross-market and cross-venue analyses are coherence checks until explicitly normalized — never blanket-arbitrage statements. (WX-RESEARCH-01, BWX-RESEARCH-05A.)

---

## 7. Market family taxonomy

The market families below are drawn from WX-RESEARCH-01 and are reinforced by WX-RESEARCH-03. Suitability labels are MEG planning inferences, not venue labels. They reflect *how safely* a market family can currently be normalized into a canonical event, not whether the family will ever be approved for implementation. Implementation remains separately gated by §17.

The label `early_candidate` means the family is permitted to enter Stage 1 work (static examples and manual labels). The label `later_candidate` means the family is research-eligible but should not be prioritized for Stage 1. The label `avoid_for_now` means the family should be treated as `blocking` until the underlying ambiguity is resolved.

### 7.1 Temperature threshold markets

- **What the market resolves.** A specific station's daily maximum, minimum, or average temperature against a threshold and comparator over a stated observation day.
- **Canonical fields required.** `measurement_variable`, `station_id`, `time_window_start/end`, `timezone`, `threshold_value`, `threshold_unit`, `comparator`, `rounding_rule`, `resolver_source`, `archive_layer`, `freeze_rule`, `revision_treatment`.
- **Likely resolver/source needs.** NWS Daily Climate Report (CLI), Weather Underground daily history with explicit station mapping, airport ASOS/METAR, with venue-specific fallback to METAR for some contracts.
- **Common traps.** City-vs-station mismatch (`blocking`); local-vs-UTC day (`blocking`); intraday-vs-final daily value (`blocking`); fallback-chain semantics (`blocking`); comparator and rounding (`caution`).
- **Uncertainty issues.** Forecast uncertainty interacts with station-mapping uncertainty and rounding uncertainty especially near the threshold.
- **Validation requirements.** Source-compatible CLI/station replay; threshold-bucket calibration near strike; reliability diagrams by station family; horizon stratification.
- **Posture.** `early_candidate` only where station, product, freeze rule, and rounding are all explicitly pinned. Otherwise `avoid_for_now`.

### 7.2 Precipitation threshold markets

- **What the market resolves.** Daily or multi-day precipitation totals at a designated station or city climate product against a threshold and comparator.
- **Canonical fields required.** As above plus `trace_rule` and `aggregation_method`.
- **Likely resolver/source needs.** Weather Underground station summary; NWS Daily Climate Report; NWS monthly summary; NCEI archives in some fallback rules.
- **Common traps.** Trace semantics (`blocking`); "measurable rain" wording (`blocking`); day-boundary mismatch (`blocking`); first-report vs final-archive (`blocking`); gauge-vs-radar provider substitution (`blocking`).
- **Uncertainty issues.** Probability mass near zero is unusually important; small rule differences at zero dominate payout.
- **Validation requirements.** Zero-inflated/hurdle/censored modeling families (research candidate, BWX-05Q); trace-sensitivity ablation; first-report layer reconstruction.
- **Posture.** `early_candidate` when station, product, trace rule, and rounding are pinned. Otherwise `avoid_for_now`.

### 7.3 Snowfall markets

- **What the market resolves.** New snowfall amount at a designated station/location over a day, month, or season.
- **Canonical fields required.** As above plus explicit `observable_type` (snowfall vs snow depth vs snow-water-equivalent) and explicit `fallback_chain` (e.g., NCEI CDO or CLI fallback in some Kalshi NOWData rules; Environment Canada records in community examples).
- **Likely resolver/source needs.** NWS Daily Climate Reports; NWS NOWData; NCEI CDO fallback; Environment Canada official records (international).
- **Common traps.** Snowfall vs snow depth vs SWE (`blocking`); trace handling (`blocking`); manual-vs-automated capability (`blocking` where source product differs); seasonal/monthly boundary (`blocking`); station discontinuity (`blocking`).
- **Uncertainty issues.** NWS snow measurement guidelines prescribe representative siting, multiple measurements in windy areas, and the "highest 24-hour accumulation" logic; siting and exposure matter.
- **Validation requirements.** Source-compatible monthly replay with explicit trace and missing-day policies; comparator-specific calibration; ablation studies on trace and rounding.
- **Posture.** `early_candidate` only when `observable_type`, station, product, trace rule, and `freeze_rule` are pinned. Otherwise `avoid_for_now`.

### 7.4 Wind / gust markets

- **What the market resolves.** Wind gust or sustained wind at a station over a stated period.
- **Canonical fields required.** As above plus `observable_type` (sustained vs gust) and `averaging_interval`.
- **Likely resolver/source needs.** LCD/ISD station observations; ASOS/AWOS; potentially NWS climate products if cited.
- **Common traps.** Sustained vs gust (`blocking`); 1-minute vs 2-minute conventions (`caution`); measured-vs-estimated semantics in Storm Data (`blocking` for severe-occurrence framing).
- **Uncertainty issues.** Upper-tail and measurement-interval sensitivity; station exposure and instrumentation effects.
- **Validation requirements.** Truncated/nonnegative distributional families; NGR/EMOS for wind (BWX-05Q research candidate); tail-aware validation.
- **Posture.** `later_candidate` due to thinner current public contract evidence and higher modeling difficulty (WX-RESEARCH-01).

### 7.5 Storm and hurricane markets

- **What the market resolves.** Tropical-cyclone formation, classification, intensity, landfall, or status events.
- **Canonical fields required.** As above plus `basin`, `classification_authority`, `classification_time_layer`, `cutoff_time`.
- **Likely resolver/source needs.** NHC advisory archive; NHC Tropical Cyclone Reports; HURDAT2 best track; storm-specific NHC records.
- **Common traps.** Advisory-time vs post-analysis status (`blocking`); basin boundaries (`blocking` where ambiguous); landfall definition (`blocking`); UTC vs local time (`blocking`).
- **Uncertainty issues.** Different time-layers of the same storm lifecycle encode different events; "form by date," "reach category," "make landfall" can each resolve differently across advisory and best-track layers.
- **Validation requirements.** Authority-layer audit; classification-layer holdout tests.
- **Posture.** `early_candidate` when `classification_time_layer` is explicit. Otherwise `avoid_for_now`.

### 7.6 Severe / extreme weather markets

- **What the market resolves.** Agency-classified occurrence of tornado, hail, severe wind, flash flood, blizzard, or similar.
- **Canonical fields required.** As above plus `classification_authority`, `classification_time_layer`, `geography`, `verification_state`.
- **Likely resolver/source needs.** SPC outlook/watch products; SPC storm reports (preliminary); NCEI Storm Events Database (post-event official); local WFO storm reports; SPC monthly tornado data (state-count series).
- **Common traps.** Preliminary vs final (`blocking`); split authorities (`blocking`); verification caveats in Storm Data (`caution`); UTC convective day vs market local day (`blocking`).
- **Uncertainty issues.** Storm Events lag is documented at roughly 75–90 days; same-day SPC/WFO reports are explicitly preliminary.
- **Validation requirements.** Preliminary-vs-final label audit; authority-layer comparison; rare-event sample handling.
- **Posture.** `later_candidate`. Occurrence-family settlement authority is explicitly unresolved per WX-RESEARCH-02 open question. `avoid_for_now` for any market without explicit authority-layer wording.

### 7.7 Daily city/location binary markets

- **What the market resolves.** A daily yes/no or bracketed condition attached to a named place.
- **Canonical fields required.** As temperature/precipitation/snow above; the `geographic_precision` field is especially load-bearing here.
- **Likely resolver/source needs.** NWS city-area climate products, airport station pages, or creator-selected sources.
- **Common traps.** City name masking station identity (`blocking`); unofficial forecast vs observation (`blocking`); vague city boundaries (`blocking`).
- **Posture.** `early_candidate` *only* when the station/source mapping is explicit in the venue rule. Without that mapping, `avoid_for_now`.

### 7.8 Weekly / monthly / seasonal aggregate markets

- **What the market resolves.** Aggregated totals or averages across a month, week, season, or winter period.
- **Canonical fields required.** As above plus explicit `aggregation_method`, `freeze_rule` (first-complete-report vs later-final-archive), and `missing_rule`.
- **Likely resolver/source needs.** NWS monthly summary; first complete daily climate report; NOWData monthly sum; Climate at a Glance; official national archives; Environment Canada records.
- **Common traps.** "First complete report" vs later final archive (`blocking`); climatological-day vs civil-day (`blocking`); season-boundary definitions (`blocking`); missing-day handling (`blocking`).
- **Posture.** `early_candidate` when `aggregation_method`, `freeze_rule`, station/product, trace rule, and missing rule are all pinned. Otherwise `avoid_for_now`.

### 7.9 Source-dependent resolution markets

- **What the market resolves.** The same physical event, but resolution depends on a named documentation source, fallback chain, or creator-judgment rule.
- **Common traps.** Same event can resolve differently across venues because the source chain differs; mid-market source mutation (`blocking`); venue-discretion clauses (`blocking`).
- **Posture.** `avoid_for_now` unless the source chain is explicit and primary.

### 7.10 Catastrophe / disaster-adjacent weather markets

- **What the market resolves.** Impact metrics caused by weather, often outside pure meteorology (fatalities, damage, attribution).
- **Common traps.** Attribution to a weather event (`blocking`); post-event revisions (`blocking`); source-quality variance (`blocking`); legal/insurance interpretation drift (`blocking`).
- **Posture.** `avoid_for_now`.

### 7.11 Climate / anomaly markets

- **What the market resolves.** Regional or national aggregate anomaly/average from a climate-monitoring product.
- **Common traps.** Adjusted vs raw station observations (`blocking`); preliminary revisions (`blocking`); region-level vs station-level semantics (`blocking`).
- **Posture.** `later_candidate` only; not `early_candidate`.

---

## 8. Source / provider architecture and compatibility rules

The most important structural rule in this PRD is the **separation of provider classes**. WX-RESEARCH-02 establishes that "official weather data" is not one thing, and that NWS API, NCEI ISD, NCEI GHCN-Daily, NCEI Climate at a Glance, NHC advisory archives, NHC TCRs, HURDAT2, SPC outlooks/watches/reports, and provider archives like Meteomatics, Meteostat, Open-Meteo, Visual Crossing, WeatherAPI.com, OpenWeather, Weatherbit, and Tomorrow.io each have different production logic, revision patterns, and source-compatibility implications. WX-RESEARCH-03 reinforces that the same agency name can map to multiple products with materially different settlement semantics.

Weather Bot must therefore treat the following classes as **structurally distinct**. Treating any class as a substitute for another is a `blocking` source mismatch.

### 8.1 Provider/source classes

| Class | Definition | Examples | MEG default role |
|---|---|---|---|
| Official resolver source | The exact product/page/archive the venue rule names as the operative resolver. | NWS CLI for a venue that cites NWS CLI; Weather Underground daily station history for a venue that cites that page; NHC advisory archive for an advisory-time market; HURDAT2 for a post-analysis market. | Sole settlement-evidence source for the canonical event. Cannot be substituted. |
| Official government weather source | An official government meteorological product not necessarily named by the venue. | NWS API forecasts/alerts/observations; NCEI ISD; NCEI GHCN-Daily; NCEI Climate at a Glance; SPC products; ECCC historical climate data; Met Office historic station data. | Strong candidate for non-resolver roles such as historical reference, station-observation evidence, and provider-comparison anchoring, **only** if the named venue resolver is something else. |
| Official station observation | A direct station measurement or official daily summary for one station. | ASOS/AWOS observations; NWS LCD; NCEI Local Climatological Data; official station climate records. | Important for station-identity reasoning. Storage of station IDs, not station names, is required. (WX-01.) |
| Climate data archive | Post-processed archive of daily/monthly station data. | NCEI CDO; GHCN-Daily; ISD; LCD certification products. | Strong for post-hoc verification and validation labels, **not** automatically the venue's operative source. |
| Forecast / model provider | A provider of forecast model output, possibly grid- or ensemble-based. | GFS / GEFS; ECMWF HRES / ENS; HRRR; LAMP; NDFD; Open-Meteo forecast API; Meteomatics model-source paths. | Permitted as a **modeling input** in research only; never settlement evidence. |
| Historical-data provider | A provider whose primary product is a historical archive, sometimes blended. | Meteostat; Visual Crossing; Weatherbit historical; Open-Meteo historical-forecast/archive. | Permitted as a **research input** with hard constraints to station/observation-only modes (BWX-05A). Never settlement evidence. |
| Convenience API | A general-purpose weather API with proprietary blending and limited source transparency. | WeatherAPI.com; OpenWeather One Call; some Visual Crossing modes. | `reject_for_now` for the resolution-authority layer. WeatherAPI.com's own docs say historical = archived forecast, not actuals (WX-RESEARCH-02). |
| Aggregator / interpolated source | A point/grid product that blends multiple stations, models, and radar at the query point. | Meteostat point data in default settings; OpenWeather coordinate retrieval; Open-Meteo grid-cell point. | `blocking` substitution for any station-anchored market. Permitted only in research roles where the blend is explicit and constrained. |
| Storm/advisory source | Specialized agency products for storms and hazards. | NHC Public Advisory; NHC TCR; HURDAT2; WPC products; SPC outlooks/watches. | Required for storm/severe-classification markets; layer (advisory vs best-track vs final-archive) must be explicit. |
| Venue-selected discretionary resolver | A market where the venue chooses, modifies, or replaces the source agency mid-market. | Kalshi's source-agency replacement language; ForecastEx Rule 413 source modification; Manifold creator/moderator discretion. | `blocking` until §11 trap is resolved by human review. |

### 8.2 Provider compatibility rules

The compatibility rules below are normative for design discussion. They derive from WX-RESEARCH-02 and WX-RESEARCH-03 and from BWX-RESEARCH-05A's false-edge taxonomy. None of them authorizes connector implementation.

1. **Resolver-first.** The official resolver source named in the venue rule is the only acceptable settlement-evidence source. No other class may substitute for it.

2. **Class transparency.** Every input value carried by Weather Bot must be tagged with its source class. Untagged inputs are `blocking`.

3. **Station-identity preservation.** When a market is station-anchored, the station ID (not the station name, not the city) is the identity. Station succession, instrumentation changes, and element-specific siting differences (per WMO siting classification and NCEI HOMR records) must be preserved.

4. **No silent blending.** Provider point products that interpolate from multiple stations, fill gaps with model output, or apply altitude/elevation correction must be tagged as such. Default settings on Meteostat, Open-Meteo, OpenWeather, and Visual Crossing already blend; the blend must be explicit, never inferred from "consensus."

5. **No archived-forecast-as-history.** Any "historical" product that is in fact an archived forecast (WeatherAPI.com is the explicit example) is `blocking` as settlement evidence.

6. **Layer-explicit advisory products.** NHC products at the advisory, intermediate-advisory, TCR, and HURDAT2 layers are different events; SPC preliminary reports and NCEI Storm Events are different events. The layer must be explicit; layer drift is `blocking`.

7. **Timezone/day-convention explicit.** Provider-day, source-day, climatological-day, and UTC-day conventions must be explicit per field. Climatological-day variants (e.g., ECCC's 0601–0600 UTC for many sites) must not be flattened to civil midnight.

8. **No connector approval implied.** Listing a provider in the candidate matrix below is **not** a connector approval. Per WX-RESEARCH-02, "provider usefulness does not imply connector approval."

### 8.3 Candidate matrix (planning, non-binding, non-approval)

This matrix is drawn directly from WX-RESEARCH-02's candidate analyses. The "recommendation" column is the WX-02 recommendation. No provider here is approved for implementation, even those labeled `candidate`.

| Provider/source | Class | Recommendation (per WX-02) | Confidence | Notes |
|---|---|---|---|---|
| NOAA NWS API | official government | candidate | confirmed | Live forecasts, alerts, observations; `/points` returns observation stations; rate-limit posture is "generous but undisclosed." |
| NOAA NCEI ISD Global Hourly | official archive | candidate | confirmed | Hourly station archive at >35,000 stations; typically 24-hour delay; authentic-copy semantics. |
| NHC advisory archive / TCRs / HURDAT2 | storm/advisory | candidate | confirmed | Best fit for tropical-cyclone identity. Layer must be explicit. |
| SPC outlook/watch/report products | storm/advisory | candidate (forecast/watch family) | unclear | Occurrence-family final archive is unresolved. |
| Meteomatics | private multi-source | candidate (secondary) | confirmed | Explicit source identifiers (`mix-obs`, `mm-mos`); station-observation mode documented. Commercial terms opaque. |
| Meteostat | aggregator (constrained) | candidate (secondary) | confirmed | Default point data is blended with model output; must be constrained to observation-only modes. |
| Open-Meteo | forecast/model + aggregator | candidate (forecast comparison only) | confirmed | Strong source transparency for forecast comparison; not an official observed-event archive. |
| Visual Crossing | aggregator | defer | confirmed | Vendor-managed "best available" selector; multi-station blending. |
| Weatherbit | aggregator | defer | confirmed | Discloses source families; historical revision-version concept; not a final authority. |
| Tomorrow.io | aggregator | defer | unclear | Public methodology not sufficiently captured. |
| OpenWeather | convenience API | reject_for_now | confirmed | Proprietary blended model; "measured or calculated" semantics. |
| WeatherAPI.com | convenience API | reject_for_now | confirmed | Own FAQ states historical product is archived forecast data, not actuals. |

---

## 9. Official resolver strategy

The resolver strategy is the operational implementation of §5's core principle and §8's compatibility rules. It governs how, for every canonical event, Weather Bot identifies and locks the resolver source before any modeling or comparison occurs.

### 9.1 Resolver-first market interpretation

For every market entering Weather Bot, the canonical event interpretation **must** start from the venue's published resolver text, not from any provider's available data. The venue rule defines the resolver; the resolver defines the canonical event; the canonical event constrains which providers (if any) are even eligible to contribute analysis inputs.

If the venue rule does not pin a resolver to a product-level identity (not just an agency family), `resolver_source = "unclear"` and the market is `blocking` per WX-RESEARCH-03's "Unspecified official source" trap.

### 9.2 Official-source alignment

The resolver source must be matched against an official-source registry to confirm:

- the source exists and is presently maintained;
- the source's documented publication cadence is consistent with the venue's `freeze_rule`;
- the source's documented revision behavior is consistent with the venue's `revision_treatment`;
- the source's documented unit and precision are consistent with the venue's `threshold_unit` and `rounding_rule`.

Mismatch on any of these is `blocking`.

### 9.3 Station / source mapping

For station-anchored markets, the station identity must be mapped to a stable station record (e.g., NCEI HOMR identifier, FAA observing-station record). Station name alone is insufficient; "same name nearby" stations and station-history reconciliation issues are documented (WX-RESEARCH-03).

Station-element siting differences (per FAA surface observing guidance and WMO siting classification) must be preserved: temperature, dew point, and wind may be measured at different points within an airport complex. Element-specific station-location handling is required.

### 9.4 Point-in-time source provenance

Every resolver-source datum the system reasons about, in any future stage, must carry:

- the source identifier;
- the publication timestamp (not the model-cycle init time);
- the archive layer (`first_posted`, `archive_quality`, etc.);
- the revision version, where the source exposes one (e.g., Weatherbit revision IDs, NCEI Storm Events versions);
- the retrieval timestamp;
- the as-of decision timestamp the system was reasoning at.

These fields are required even at Stage 0 (documentation). Decision-time replay (§19) requires them. Their absence is `blocking`.

### 9.5 Archive / finality handling

The system must explicitly distinguish, for each market:

- the `first_posted` value, where applicable;
- the `archive_quality` / final-archive value, where applicable;
- the `post_analysis` / TCR / HURDAT2 value, where applicable.

These are *different events* if the venue rule freezes on one and ignores the others. Using the final archive in place of a first-posted-governed market is a `blocking` revision/finality leak.

GHCN-Daily, for example, explicitly instructs users to confirm whether a real-time source has been replaced by an archive-quality source (typically 45–60 days after month-end). Weather Bot must preserve this distinction structurally, not opportunistically.

### 9.6 Revision handling

When a venue freezes on first-posted but the source later revises, Weather Bot must continue to reason on the first-posted value for that market. When a venue freezes on the final archive, Weather Bot must reason on the final-archive value and explicitly hold a `pending_finalization` state until the archive layer becomes available.

NOWData is explicitly preliminary and unofficial for final records; final records live at NCEI. Confusing NOWData with final certified data is `blocking`.

### 9.7 Storm / severe-weather authority handling

For tropical-cyclone markets:

- the controlling layer must be explicit (advisory, intermediate advisory, TCR, HURDAT2, or special advisory);
- advisory-time decisions must use the advisory archive timestamped at issuance;
- post-analysis decisions must use HURDAT2/TCR products as published;
- mixing the two is `blocking`.

For severe-occurrence markets:

- the controlling authority must be explicit (SPC storm reports, NCEI Storm Events / Storm Data, SPC monthly state counts, or local WFO);
- preliminary same-day SPC/WFO reports must not be treated as final;
- Storm Events lag (~75–90 days) must be respected;
- SPC's daily storm summaries are organized 1200–1159 UTC and must not be conflated with local civil days.

Authority drift is `blocking`.

### 9.8 Source URL / reference requirements

Each resolver must carry a stable, archivable URL or archive identifier. URL drift, page deletion, or stable-identifier rotation must be detectable. If the resolver source no longer exists or no longer publishes the named product, the market enters `blocking` until human review resolves.

### 9.9 Unsupported / unclear source treatment

If `resolver_source = "unclear"`, `resolver_source_authority = "unclear"`, `archive_layer = "unclear"`, or any combination, the market is `blocking`. Inferring the resolver from context, similar markets, or "what NOAA usually means" is not permitted.

---

## 10. Provider / convenience-source risk model

This section names the structural risks that convenience and aggregator providers introduce when used outside their proper role. It is not a list of provider failings; it is a list of *uses* that are unsafe regardless of provider quality.

### 10.1 Hidden station selection

Many providers select stations automatically. Meteostat point queries interpolate across nearby stations and may fill gaps with model data. Visual Crossing can use up to three stations and can mix `obs`, `remote`, `fcst`, `histfcst`, `stats`, `comb` source types. Hidden station selection is a `blocking` source mismatch for any station-anchored market because the provider's selection is not the venue's selection.

### 10.2 Gridded / interpolated data

Open-Meteo's grid-cell selection can choose cells some kilometres from the requested coordinate, with elevation-aware logic. NWS gridpoint data are 2.5 km grid forecasts; they are not station observations. A gridded value substituted for a station value is `blocking`.

### 10.3 Model-derived estimates

Provider responses can include "measured or calculated" data without distinguishing them at the field level (OpenWeather One Call is explicit about this). A modeled value substituted for an observed value is `blocking` for settlement evidence.

### 10.4 Incomplete historical availability

Provider historical archives may not cover the dates a venue resolves on. Coverage gaps are `blocking` for settlement evidence and `caution` for research labels.

### 10.5 Forecast / observation mismatch

WeatherAPI.com's "historical weather" is archived forecast data, not actuals. Any treatment of such data as observation is `blocking`. Open-Meteo's historical product can be reanalysis-based, which is also `blocking` for observed-event settlement.

### 10.6 Source opacity

If a provider does not disclose, for a given field, which source produced the value, the value cannot serve as settlement evidence. Opacity is `blocking`.

### 10.7 Timestamp ambiguity

Provider timestamps may refer to local clock time, local standard time, UTC, or a model valid-time. Ambiguous timestamps are `blocking`.

### 10.8 Rate-limit / terms / auditability issues

NWS API rate limits are described as "generous" but undisclosed; WeatherAPI quotas reset monthly and stop service when exceeded. Rate-limit and terms posture is `caution`-level for research auditability; it becomes load-bearing only at the connector-approval gate, which is not approved here.

### 10.9 Commercial-use ambiguity

Some provider terms restrict commercial or redistribution use. Until terms are reviewed at the connector-approval gate, commercial-use posture is `unclear` and `blocking` for any non-research use.

### 10.10 Provider outage / failure modes

Live provider availability is irrelevant under this PRD because no live provider use is approved. Future stages that depend on a provider must independently model outage as a `blocking` failure mode with fail-closed behavior.

### 10.11 The governing rule

**Provider usefulness does not imply connector approval.** This sentence, from WX-RESEARCH-02, is the controlling rule. A provider may be excellent for forecast comparison, excellent for historical labels, excellent for source-disagreement research — and *still* be unfit as settlement evidence and *still* be unapproved for connector implementation.

---

## 11. Trap taxonomy and fail-closed rules

**Controlling source:** WX-RESEARCH-03 controls trap severity throughout this PRD. Where any other section appears to soften a trap, WX-RESEARCH-03's stricter reading governs. Severity is drawn from the closed set `{caution, blocking}`. `Blocking` traps fail closed (§26): no automated action, no implementation-adjacent ticket, no proposal, no proxy. `Caution` traps must produce a structured human-review note and may not be silently suppressed.

The trap families below derive directly from WX-RESEARCH-03's tables. Examples and sources have been preserved to keep nuance and audit trail.

### 11.1 Market wording traps

| Trap | Description | Example | Severity | Fail-closed treatment |
|---|---|---|---|---|
| Vague city/location wording | A city headline is not a measurable object; the real object is a station, grid cell, or office product. | "Will it rain in LA tomorrow?" | blocking | `geographic_precision = city_area` or `unspecified` without station mapping → block. |
| "Measurable rain" vs threshold precipitation | "Measurable" can mean archive trace, ≥0.01 in some U.S. contexts, or venue-specific non-zero logic. | "Will there be measurable rain?" | blocking | Require explicit `trace_rule`; otherwise block. |
| "At least" vs "more than" | Boundary semantics differ exactly at threshold and are common silent-mismatch sources. | "At least 1.0 in" vs "more than 1.0 in" | caution | Extract `comparator` explicitly; do not infer. |
| "On [date]" without day definition | Calendar day, climatological day, UTC day, and exchange-local day can each produce different values. | "On May 31" | blocking | Require explicit `timezone` and `day_definition`; otherwise block. |
| "Records" vs "receives" | "Records" implies a station measurement; "receives" can read as a city-level statement. | "City receives rain" | blocking | Require explicit `observable_type` and `station_binding`. (Confidence: unclear — partly an inference.) |
| "Official source" unspecified | Official agency families expose multiple products. | "Official NOAA/NWS data" | blocking | Require product-level pinning. |
| Hidden station assumptions | A venue can bury the operative station in rules while the headline names only the city. | "Seattle precipitation in January?" | blocking | Require `station_id` or explicit venue-to-station mapping. |
| Event cancellation/invalidation wording | Some markets embed voiding/cancellation/accelerated-settlement clauses. | "Market may be voided if source unavailable" | blocking | Record `venue_status_rule`; block until reviewed. |
| Venue-specific resolution discretion | Moderator/review-committee discretion may override plain-source reading. | "Event Review Committee determination" | blocking | Record `manual_override_flag`; block. |

### 11.2 Resolution-source traps

| Trap | Description | Severity | Fail-closed treatment |
|---|---|---|---|
| Unspecified official source | "Official source" is not self-executing. | blocking | Require product-level pinning. |
| Official source mismatch | Different official products disagree because they answer different questions. | blocking | Require named-product alignment. |
| Source changed after market creation | Venue substitution or source-agency replacement can alter event identity after listing. | blocking | Require detection of mid-market source mutation; block on detection. |
| Station replaced or unavailable | Archive crosswalks (e.g., GHCNd ASOS/WBAN crosswalks) do not equal venue intent. | blocking | Require station-history match with venue's intended station. |
| City weather vs station weather | "City area" products and station products are related but not identical. | blocking | Require explicit `geographic_precision`. |
| Airport vs downtown station | Airport observations are station-specific, not citywide. | blocking | Preserve `station_id`. |
| Government archive revisions | Real-time feeds can be replaced by archive-quality sources (e.g., GHCNd ~45–60 days post-month-end). | blocking | Require archive-layer pinning. |
| Delayed final reports | Final publication can trail by days or months (Storm Events ~75–90 days). | blocking | Require `archive_layer` and `pending_finalization` handling. |
| Tropical advisory vs final report mismatch | NHC advisory archive, TCR, and HURDAT2 encode different time-layers. | blocking | Require `classification_time_layer`. |
| Severe-weather verification | Preliminary reports are operationally useful but not final; even Storm Data carries verification caveats. | blocking | Require `verification_state`. |
| Preliminary vs final archive | NOWData / Climate at a Glance can be preliminary; archives later differ. | blocking | Require `archive_layer = first_posted` or `final_archive` explicit. |
| First-report freeze vs later revision | Operational/early-posted pages differ from later archive records. | blocking | Require `freeze_rule` explicit. |
| Venue fallback chain or source replacement | Venues may fall back to METAR, replace a source agency, or invoke discretion. | blocking | Store full ordered `source_chain`; block if not parseable. |
| International archive mismatch | Country-specific products, station IDs, and day boundaries differ. | blocking | Require country-specific official product and station IDs. |

### 11.3 Provider / source-compatibility traps

| Trap | Description | Severity |
|---|---|---|
| Provider gridded/downscaled vs station resolver | Open-Meteo grid cells may be kilometres from the requested coordinate. | blocking |
| Provider station selection hidden or blended | Meteostat point joins multiple stations; Visual Crossing mixes obs/remote/fcst/stats/comb. | blocking |
| Provider historical data are not actual observations | WeatherAPI.com states its history = archived forecast, not actuals. | blocking |
| Provider observation not the venue's official product | OpenWeather "measured or calculated" data are not a cited NWS/NCEI/NHC product. | blocking |
| Provider horizon / product family insufficient | NWS alerts archive only past 7 days; final archive is at NCEI. | caution |
| Provider historical data delayed/revised vs venue resolution | NWS API upstream MADIS observations can be delayed by QC ~20 minutes. | caution |
| Provider daily aggregation differs from venue source | GHCNd notes Global Summary of the Day can differ from local-midnight summaries, especially for precipitation. | blocking |
| Provider units/conversions differ from resolution product | Native units differ across Open-Meteo, WeatherAPI, OpenWeather, ECCC, NWS. | caution |
| Terms/quotas/product structure reduce auditability | Rate-limit and quota differences affect audit reproducibility. | caution |

### 11.4 Location / station traps

| Trap | Severity |
|---|---|
| City centroid vs official station | blocking |
| Airport station vs urban station | blocking |
| Multiple stations in one metro area | blocking |
| Station relocation or instrumentation/site change | blocking |
| Elevation differences | caution |
| Coastal vs inland microclimates | caution (unclear in current public sample) |
| Mountain / snow measurement ambiguity | blocking |
| International station naming or ID mismatch | blocking |

### 11.5 Time-window traps

| Trap | Severity |
|---|---|
| Local date vs UTC date | blocking |
| Observation-day definition | blocking |
| Daily highs/lows are period-specific | caution |
| Precipitation accumulation windows | blocking |
| Multi-day storms crossing market boundaries | caution (unclear) |
| Monthly / seasonal aggregation windows | blocking |
| Daylight saving time | caution |
| Reporting lag | caution |

### 11.6 Threshold / unit / comparator traps

| Trap | Severity |
|---|---|
| `≥` vs `>` | caution |
| "Over" vs "at least" | caution |
| Inches vs millimeters | caution |
| Fahrenheit vs Celsius | caution |
| Rounding rules | caution |
| Trace precipitation | blocking |
| Snow depth vs snowfall | blocking |
| Sustained wind vs gust | blocking |
| Central pressure vs hurricane category | caution |
| Official category timing | blocking |

### 11.7 Data revision / finality traps

| Trap | Severity |
|---|---|
| Provisional vs final observations | blocking |
| Delayed quality control | caution |
| Corrected/reprocessed archive content | caution |
| Final storm reports lag | blocking |
| Archived climate-data source replacement | blocking |
| Venue resolves before official archive finalization | blocking |

### 11.8 Venue discretion / authority / classification traps

| Trap | Severity |
|---|---|
| Venue-selected discretionary resolver | blocking |
| Outcome-review committee discretion | blocking |
| Mid-market source mutation | blocking |
| Classification authority drift | blocking |
| Advisory-time vs post-analysis layer drift | blocking |

### 11.9 Cancellation / invalidation traps

| Trap | Severity |
|---|---|
| Cancellation / void clauses | blocking |
| Accelerated settlement clauses | blocking |
| Source-unavailability fallback | blocking |

### 11.10 Provider/source mismatch traps (already covered §11.3)

### 11.11 False-equivalence traps

| Trap | Severity |
|---|---|
| Same headline ≠ same event across venues | blocking |
| Same broad weather phenomenon ≠ same canonical event | blocking |
| Correlation ≠ equivalence (ladders, neighboring airports) | caution |
| Cross-venue same wording ≠ same resolver chain | blocking |

### 11.12 Fail-closed rule

For any market entering Weather Bot, the controlling trap severity is computed as the maximum severity across active flags. If any `blocking` trap is active, the market is `blocking` and no further automated reasoning may produce a settlement-equivalent inference for that market. Human review is the only path forward; human review may downgrade the controlling severity to `caution` only with documented rationale recorded against the market's `human_review_state` (§6.1) as `reviewed_caution`, never silently. `Caution` traps must produce reviewer notes but do not by themselves block. The `human_review_state` closed set (`unreviewed`, `caution_under_review`, `blocking_under_review`, `reviewed_pass`, `reviewed_caution`, `reviewed_block`) is the only allowed mechanism for recording reviewer adjudication outcomes; hybrid or invented downgrade values are forbidden.

---

## 12. Probability and uncertainty architecture

**Controlling source:** WX-RESEARCH-04 controls probability framing throughout this PRD. WX-RESEARCH-04 establishes that, for Weather Bot, "P(market Yes) is not merely P(weather variable crosses threshold), but P(the venue-defined source/station/window/threshold/revision/classification rule resolves Yes)." That is the only probability semantics permitted in Weather Bot intelligence outputs.

### 12.1 The operational framing

Formally, Weather Bot's target is:

`P(market Yes) = Σ_r P(r) · P(g_r(Y_r) = Yes | r, forecast)`

where `r` indexes plausible resolution scenarios (source product, station mapping, day boundary, comparator interpretation, trace treatment, revision state, classification authority). When the venue rule pins `r`, the sum collapses to a single conditional term. When it does not, the ambiguity is *not* silently selected away; the canonical event is either `blocking` per §11 or the ambiguity is exposed as a mixture in the reviewer-readable output.

The mathematical restatement from BWX-RESEARCH-05Q is: the target is `P(R(O(Y)) = Yes | I)`, where `Y` is the latent weather quantity, `O` is the observation/resolution process (provider choice, station placement, sampling, missing rules, revisions), and `R` is the market rule map (threshold, comparator, time window, trace, venue discretion). It is **not** `P(Y > τ | I)`.

### 12.2 Why point forecasts are insufficient

WX-RESEARCH-04 lists four reasons:

1. Threshold markets require the probability mass around a boundary, not just a mean or median.
2. The market target can differ from the forecast target because of station-vs-city, observation-vs-archive, advisory-vs-best-track, or preliminary-vs-final semantics.
3. Errors grow with forecast horizon; raw ensembles are not automatically calibrated.
4. Near-threshold markets can be dominated by non-meteorological uncertainty modes even when the physical forecast is sharp.

None of these is fixed by "better point forecasts."

### 12.3 Threshold probability modeling

Threshold probability must be reasoned in five layers (per WX-RESEARCH-04):

1. Specify the exact event as `comparator + threshold + units`.
2. Choose or fit a predictive distribution for the weather quantity (research only, no implementation approved).
3. Map the latent variable into the observation/archive process actually used by the resolver.
4. Apply the resolution policy for trace, missing, and revised values.
5. Only then compare to market-implied probability.

For continuous predictive `F`, the clean object is `P(X ≥ t) = 1 - F(t⁻)` or `P(X > t) = 1 - F(t)`. In practice, weather markets resolve on a measured and rounded value `Y`, not latent `X`. A model that estimates `P(X > t)` while the market resolves on `Y ≥ t` after rounding can be directionally wrong even when the meteorology is correct.

### 12.4 Distributional and ensemble forecasts

Per BWX-RESEARCH-05Q's mathematical taxonomy, distributional forecasts (predictive densities, quantile regression, distributional regression, GAMLSS, EMOS/NGR, BMA, censored/mixture precipitation models) are **research candidates** at later stages. None is approved for implementation by this PRD. Raw ensemble output is typically biased and under-dispersive; post-processing is not optional once an ensemble stage is reached.

### 12.5 Uncertainty components — the structural decomposition

Weather Bot must carry these uncertainty components as **distinct first-class objects**, not as a single blended residual. Only the first is purely meteorological. (WX-RESEARCH-04, WX-RESEARCH-03, BWX-RESEARCH-05Q.)

| Component | Definition |
|---|---|
| Forecast uncertainty | Uncertainty in the future atmospheric state or future verified value conditional on the chosen target. |
| Observation uncertainty | Noise/measurement uncertainty in the observing system used as truth. |
| Resolver / source uncertainty | Which source product, archive layer, or feed is effectively operative. |
| Station / location uncertainty | Which station, grid cell, or observation point really maps to the market wording. |
| Time-window uncertainty | Start/end times, timezone, climatological day, aggregation interval. |
| Threshold / comparator uncertainty | Comparator, units, rounding, bracket rules. |
| Trace / missing-value uncertainty | How trace precipitation or missing observations convert into market logic. |
| Revision / finality uncertainty | Whether preliminary values can change; which freeze rule governs. |
| Classification authority uncertainty | Which authority defines the event class and at what stage. |
| Market-mapping uncertainty | Whether the market wording maps to the intended resolver object. |
| Provider compatibility uncertainty | Whether forecast/observation inputs are compatible with the stated resolver source. |
| Market microstructure uncertainty | Spread, depth, fees, stale quote risk, adverse selection. (Tradable families only; not approved for trading.) |
| Model uncertainty | Uncertainty over which postprocessor or forecast source is structurally best. |

### 12.6 Calibration

WX-RESEARCH-04 requires that any future probability layer be **calibration-first**. Reliability diagrams, calibration curves, PIT or rank histograms (for ensembles or full distributions), Brier-score decomposition (reliability, resolution, uncertainty), and threshold-bucket reliability checks are all named as required. Proper scoring rules — Brier, log score, CRPS — are the primary skill measures. ROC/AUC measures discrimination, not calibration, and is at best secondary. Threshold-weighted scoring (twCRPS) is appropriate near strikes but carries body-tail tradeoffs that must be tracked.

### 12.7 Source uncertainty as a first-class object

Source uncertainty is *not* a residual of forecast uncertainty. It has its own scenarios (`r` above), its own mixture weights `P(r)`, and its own audit trail. Per BWX-RESEARCH-05Q: "A perfectly calibrated forecast for the wrong provider is still wrong for payout." Source-uncertainty modeling is a `defer` or `advanced_candidate` research direction (BWX-05Q "source uncertainty adjustment" row), not an early-implementation target.

---

## 13. Forecast uncertainty versus market-resolution uncertainty

The following components are **distinct** and must not be silently collapsed. This list is the explicit anti-flattening rule for Weather Bot.

| Component | Distinct from |
|---|---|
| Forecast uncertainty | All other components below. |
| Observation uncertainty | Forecast uncertainty. |
| Resolver / source uncertainty | Forecast uncertainty. Source choice can change the answer at fixed weather. |
| Station / location uncertainty | Forecast uncertainty. Nearby stations can differ at exactly the threshold. |
| Time-window uncertainty | Forecast uncertainty. Climatological-day vs civil-day can flip outcomes. |
| Threshold / comparator uncertainty | Forecast uncertainty. `≥` vs `>` at the boundary flips outcomes. |
| Rounding / unit uncertainty | Forecast uncertainty. Source-native precision can govern. |
| Trace / missing-value uncertainty | Forecast uncertainty. Trace handling can flip rain/no-rain markets. |
| Revision / finality uncertainty | Forecast uncertainty. First-posted vs final-archive layers can disagree. |
| Classification-authority uncertainty | Forecast uncertainty. Advisory vs best-track encodes different events. |
| Market-mapping uncertainty | Forecast uncertainty. The headline may not mean what the rule does. |
| Provider-compatibility uncertainty | Forecast uncertainty. Provider value need not be settlement-equivalent. |
| Market microstructure uncertainty | All meteorological components. Edge can vanish to spreads and fees. |

**The anti-flattening rule:** Weather Bot's human-review output and any internal scoring layer must keep these components separable. A single "confidence" number that mixes them is **not** acceptable. If a downstream layer needs a scalar, it must be accompanied by the decomposition.

---

## 14. Alpha hypothesis framework (from WX-RESEARCH-05A)

**Controlling source:** BWX-RESEARCH-05A controls alpha hypotheses and false-edge categories throughout this PRD. The framework below is preserved as **research hypotheses only**. Nothing in this section approves implementation, model training, runtime use, trading strategy, position sizing, or order placement. Each hypothesis is a research target with its own validation requirements; until BWX-RESEARCH-05A's `keep-alive` evidence (as defined in WX-RESEARCH-06 §17) is in hand, an alpha hypothesis is exactly that — a hypothesis.

The confidence column refers only to whether the *mechanism or risk* is directly source-backed. It does **not** mean profitability is proven. A hypothesis can be `confirmed` as a mechanism and still remain entirely unproven as an executable edge.

### 14.1 Source, station, and timing hypotheses

| Hypothesis | Why it might exist | Required validation | Primary false-edge risks | Human-review treatment | Confidence | Non-approval reminder |
|---|---|---|---|---|---|---|
| Resolution-source mismatch alpha | Market may price the broad weather story while the contract resolves on a narrower object (specific climate report, station, full source precision, freeze-time snapshot). | Relabel historical markets against the exact source chain and compare against generic-provider interpretations. | City-vs-station, third-party "actuals," preliminary-vs-final, post-expiration QC, trace/missing rules. | Surface as source-risk note; explain non-equivalence; never present as approved trade. | unclear | Not approved for trading or model implementation. |
| Station/location precision alpha | Local gradients matter more than city-level weather when settlement is station-specific. | Station-pair and city-vs-station replay; microclimate buckets (coast/inland, elevation, lake-effect regime). | City label masking airport station; model grid vs station; poor gauge siting; runway-complex exposure. | Note station-level evidence; document siting exposure; abstain on ambiguous mapping. | confirmed | Not approved for trading. |
| Forecast update timing alpha | Model/forecast products update on known clocks (GFS/GEFS 00/06/12/18 UTC; ECMWF main 00/12 UTC + supplementary 06/18; HRRR hourly with radar assimilation; LAMP hourly; NDFD twice per hour around :25/:55). | Event-time study around official product release clocks using publish time, not init time, with no-lookahead controls. | Watching the wrong model family; using init time instead of public availability; market closes before info is tradable. | Surface as timing context; never present as approved trade. | unclear | Not approved. |
| Observation release lag alpha | Some settlement-relevant observations arrive after the event has effectively happened (CLI examples post early morning; NOWData preliminary; ISD typically 24-hour delay; GHCN-Daily reconstructs weekly). | Product-level release calendars; intraday price response; final-vs-first-dissemination replay. | Confusing real-time observations with settlement product; first report vs final archive; local-office variance. | Surface as availability-window note; mark stage. | unclear | Not approved. |
| Nowcasting alpha | Short-horizon (0–6 hr) information can improve event probability once storms or local precipitation regimes are observable; WoFS assimilates radar/satellite every 5–15 minutes. | Near-close signal-vs-price tests with executable spread/depth filters and clock-synchronized data feeds. | Using nowcast products that are not settlement-equivalent; market already closed; low liquidity near close; last-minute spread blowouts. | Surface near-close information context; never present as approved trade. | confirmed | Not approved. |
| Radar / satellite signal alpha | Radar, GOES, lightning, and surface data can materially improve short-term convective assessment. | Compare radar-only, radar+satellite, and settlement-equivalent station outcomes over near-close windows. | Radar-estimated precipitation vs gauge/official settlement; cell motion extrapolation without growth/decay; source latency. | Surface as signal-vs-resolver disagreement note. | confirmed | Not approved. |
| Observation-source disagreement alpha | 1-minute ASOS-style data can improve awareness even when settlement is hourly METAR or CLI; NOAA explicitly distinguishes minute-level data from METAR observations. | Compare predictive value of sub-hourly observations while enforcing settlement-source separation. | Treating 1-minute ASOS as already the settlement observation; AWOS vs ASOS differences. | Surface as source-disagreement note. | confirmed | Not approved. |

### 14.2 Uncertainty, threshold, and belief-formation hypotheses

| Hypothesis | Why it might exist | Required validation | Primary false-edge risks | Confidence | Non-approval reminder |
|---|---|---|---|---|---|
| Ensemble dispersion alpha | Calibrated spread carries information; raw ensemble output is typically biased/under-dispersive. | Build calibrated source-compatible threshold probabilities; test whether prices reflect distributional widening/narrowing. | Treating raw spread as calibrated probability; source mismatch between model grid and station settlement. | confirmed | Not approved. |
| Threshold proximity alpha | Near a strike, small differences in source precision, trace, and freeze rules cause large payout jumps. | Bucket historical markets by distance-to-threshold under the actual resolution source and compare calibration. | Rounding from media pages; unit conversions; hidden fallback; wrong day window. | confirmed | Not approved. |
| Tails / extreme-event alpha | Tail events can be misread; weighted verification and rare-event methods treat tails differently. | Rare-event label audit; weighted-score calibration; authority-layer comparison for preliminary vs final. | Sparse samples; authority drift; preliminary vs final reports; event-identity drift. | unclear | Not approved. |
| Seasonality / climatology mispricing alpha | Climatology is a strong baseline; markets may underweight seasonal base rates when headlines dominate. | Compare source-compatible climatological base rates against market priors by season and horizon. | Using climatology for the wrong station/source/window; ignoring regime changes. | unclear | Not approved. |
| Human salience / narrative mispricing alpha | Behavioral mispricing is plausible when traders overweight vivid headlines or recent streaks; favorite-longshot bias documented in prediction-market literature. | Weather-specific bias decomposition controlling for source updates, thresholds, liquidity. | Confusing favorite-longshot bias with true source mismatch. | unclear | Not approved. |
| Venue wording ambiguity alpha | Venue text may contain exploitable nuance the crowd misreads. Treated as a human-review filter, not a trade signal. | Rules parser + reviewer notes comparing headline, strike card, full rule text. | Overreading ambiguous text; fallback discretion; silent source substitution. | confirmed | Not approved. |
| Cancellation / invalidation awareness alpha | Event conclusion, determination, payout, and invalidation are not the same clock. | Resolution-state machine for close/determine/settle/void/source-failure contingencies. | Assuming "weather already happened" means contract is locked; ignoring fallback. | confirmed | Not approved. |
| Cross-source disagreement alpha | When official observations, interpolated point products, and reanalyses disagree, the disagreement itself can signal edge or danger. | Source disagreement dashboards that label disagreement type before any probability comparison. | Mistaking non-equivalent products for "consensus"; hidden interpolation; archived-forecast-as-history. | confirmed | Not approved. |

### 14.3 Microstructure and network hypotheses

| Hypothesis | Why it might exist | Required validation | Primary false-edge risks | Confidence | Non-approval reminder |
|---|---|---|---|---|---|
| Stale market price alpha | Prices may lag fresh source updates, especially in thin books. | Event studies on price response to NDFD/LAMP/HRRR/CLI/NHC/severe updates. | Apparent mispricing vanishes once spread/depth is counted; market closed before update is tradable. | unclear | Not approved. |
| Liquidity / spread-aware alpha | Execution matters as much as signal. Spread, depth, fees, fill probability, adverse selection. | Convert model advantage into executable edge net of spread, fees, fill probability, adverse selection. | "Edge" exists only at midpoint; taker execution destroys it; depth disappears when info arrives. | confirmed | Not approved. |
| Correlated market structure alpha | Related contracts can become incoherent; threshold ladders, range buckets, storm-state graphs. | Coherence tests for monotonic ladders, exhaustive partitions, event-graph consistency after source normalization. | Correlation ≠ equivalence; nested thresholds can resolve off different sources or different times. | unclear | Not approved. |
| Cross-venue disagreement alpha | Same broad event may trade at different prices across venues, but only meaningful after rule/source/timing normalization. | Contract-equivalence audit before any price comparison, then net-of-fee disparity study. | Topic similarity ≠ contract identity; different sources, close times, invalidation rules. | unclear | Not approved. |

### 14.4 Governing rules for alpha hypotheses

- Every alpha hypothesis must carry an explicit source-compatibility statement, an explicit timing layer, an explicit station/window/threshold mapping, an explicit active-false-edge list, an explicit validation state, an explicit confidence value (`confirmed`/`unclear`/`unknown`), and a clear `no-trade` / `caution` / `blocking` note when appropriate.
- Every alpha note must explicitly state whether the underlying signal is coming from an official settlement-adjacent source, a non-equivalent convenience source, or a purely methodological analogy.
- *Alpha hypothesis ≠ trading strategy.* No hypothesis in §14 is a trading strategy. Conversion of any hypothesis into trading logic is explicitly not approved by this PRD.

---

## 15. False-edge detection framework

False-edge detection is the **first useful capability** of Weather Bot. Before any edge claim, before any probability comparison, the false-edge filter runs. The false-edge categories below derive from BWX-RESEARCH-05A's table and from WX-RESEARCH-03's trap families. Severity is drawn from `{caution, blocking}`.

### 15.1 False-edge categories

| Category | Why it creates false edge | Treatment | Confidence |
|---|---|---|---|
| Provider source mismatch | Third-party products may be interpolated, model-based, or forecast-archive rather than the resolution source. | blocking | confirmed |
| Station mismatch | City headline can conceal an airport or climate station with materially different conditions. | blocking | confirmed |
| Gridded vs station mismatch | A forecast grid point or reanalysis cell is not the same object as a station observation. | blocking | confirmed |
| Local time vs UTC mismatch | Daily pages and event logs may use UTC windows. SPC daily storm summaries run 1200–1159 UTC. | blocking | confirmed |
| Threshold rounding mismatch | Source-agency full precision can govern even when public pages or media round. | blocking | confirmed |
| Precipitation accumulation mismatch | Gauge totals, radar-estimated totals, and summary products differ; missing-day or sum rules apply. | blocking | confirmed |
| Snow depth vs snowfall mismatch | New snowfall, snow depth, and SWE are different observables. | blocking | confirmed |
| Forecast target vs market resolution mismatch | A forecast may target the atmospheric variable while the market resolves on a venue-defined product. | blocking | confirmed |
| Stale provider data | Provider data may arrive with daily offsets or backfills, or may be forecast-archive rather than actuals. | blocking | confirmed |
| Stale market data | Apparent edge at midpoint can vanish because the displayed book is old. | caution | confirmed |
| Wide spreads / illiquidity | Wide spreads and thin depth can overwhelm any informational gap. | caution | confirmed |
| Fees and slippage overwhelming edge | Immediate matching incurs fees; quick orders can sweep multiple price levels. | blocking | confirmed |
| Final resolution source unavailable | If the controlling source is delayed/unavailable/ambiguous, fallback or discretion may dominate. | blocking | confirmed |
| Discretionary market wording | Headline may imply one event while the rule text defines another; venue discretion remains. | blocking | confirmed |

### 15.2 Treatment definitions

| Treatment | Definition |
|---|---|
| `caution` | Produce a structured human-review note. Do not suppress; do not auto-act. The market may continue to be reasoned about, but every downstream output must carry the caution. |
| `blocking` | Fail closed. No automated reasoning may produce a settlement-equivalent inference, and no implementation-adjacent ticket may proceed for this market. The market is reviewable only by humans; humans may downgrade only with documented rationale. |

### 15.3 Validation requirements before any false-edge filter is implementation-adjacent

Per WX-RESEARCH-06 §17, false-edge filter behavior must be validated as part of Stage 1 (static examples / manual labels) and Stage 2 (source-compatible labels with point-in-time provenance). Specifically:

- false-negative rate on `blocking` traps must be measurable and bounded (any unbounded false-negative rate is an automatic block);
- false-positive rate on `caution` warnings must be bounded enough that reviewers receive incremental value, not noise;
- inter-rater agreement on adjudicated examples must reach Cohen's-kappa-style thresholds (WX-RESEARCH-06).

Until these gates are cleared, the false-edge filter is research-only; it produces reviewer-readable notes only, never automated action.

---

## 16. Advanced quantitative roadmap (from WX-RESEARCH-05Q)

**Controlling source:** BWX-RESEARCH-05Q controls the quantitative-methods taxonomy and staged suitability throughout this PRD. The roadmap below preserves the staged maturity assignments from BWX-RESEARCH-05Q. **No method named here is approved for implementation by this PRD.** Each method is named as a future design candidate at a specific stage of the WX-RESEARCH-06 evidence ladder, with required validation before implementation could even be proposed.

### 16.1 Staged quant roadmap

| Stage | Maturity goal | Methods in scope | What is explicitly NOT approved |
|---|---|---|---|
| Stage 0 | Research-only discipline. | Target audits; source schema; validation design; literature mapping. | Any implementation, connectors, live pulls, execution. |
| Stage 1 | Baseline climatology and persistence. | Base rates; persistence; simple threshold climatology; no-trade rules for ambiguous markets. | Live trading or alpha claims. |
| Stage 2 | Calibrated simple threshold models. | Binary GLMs (logistic/probit); basic recalibration maps (isotonic, Platt, beta); family-wise reliability analysis. | Autonomy or connector/runtime approval. |
| Stage 3 | Ensemble and postprocessing layer. | EMOS/NGR/MOS; BMA; analog ensembles; quantile/distributional regression for selected families. | Full automation or complex market-timing logic. |
| Stage 4 | Source-aware uncertainty decomposition. | Hierarchical source/station models; revision-aware labels; geostatistical local correction (GMA, kriging, GAMs/GAMLSS); adaptive weighting with strong safeguards. | Broad multivariate/tail stack without validated labels. |
| Stage 5 | Advanced spatial-temporal, dependence, tail, market-aware. | Copulas / ensemble copula coupling; spatial-temporal latent models; EVT/POT for rare families; microstructure-aware filters; sequential timing research (state-space, Kalman, particle); HMM/regime-switching; conformal wrappers as abstention layers only. | Execution approval; autonomous order logic; profitability claims. |

### 16.2 Method-by-method preservation of BWX-05Q suitability labels

| Method family | Purpose | Possible future use | Data requirements | Limitations | Suitability per BWX-05Q | Validation needed before implementation |
|---|---|---|---|---|---|---|
| Calibrated probabilistic forecasting (general principle) | Optimize sharpness subject to calibration. | Overarching design principle for any future probability layer. | Source-aligned truths and forecast features. | If target label is wrong, calibrated forecast is calibrated to wrong event. | baseline_candidate (foundational) | Reliability, sharpness, resolution, conditional calibration by family. |
| GLMs for threshold events (logistic, probit, conditional exceedance) | Directly estimate `P(event exceeds threshold)`. | Baseline for binary threshold markets. | Historical forecasts; exact threshold labels; covariates. | Sensitive to misspecified link, unmodeled nonlinearity, label leakage. | baseline_candidate | Brier/log loss, reliability by threshold family, comparator-specific relabeling. |
| EMOS / NGR / MOS | Parametric postprocessing linking distribution parameters to ensemble statistics. | Convert raw ensembles into calibrated predictive distributions. | Archived ensemble forecasts; reforecasts/hindcasts; verifying observations. | Splits ignoring model-upgrade eras flatter results; local sample size limiting. | baseline_candidate (once source-aligned archive exists) | CRPS, log score, Brier by lead/station/season/model-epoch; recalibration drift. |
| Bayesian Model Averaging (BMA) | Mixture over members or systems with weights from past performance. | Multimodel calibrated threshold probabilities. | Ensemble-member forecasts; verifying observations. | Weights unstable across regimes; exchangeability/missing-member issues. | advanced_candidate (Stage 3–4) | OOS log score, CRPS; weight stability; leave-season-out CV. |
| Forecast combination / stacking | Combine predictive distributions/quantiles from several calibrated systems. | Regime-dependent best-of selection. | Multiple calibrated streams with common history. | Naïve pooling does not preserve calibration; weights can chase noise. | advanced_candidate (Stage 3–4) | Nested CV; rolling-origin weights; post-combination recalibration. |
| Bayesian updating over forecast cycles | Sequential update of predictive distribution as new model runs arrive. | Run-to-run probability revision. | Successive cycles; recent observations; run history. | If revisions driven by target mismatch, updating accelerates to the wrong answer. | advanced_candidate (Stage 3–4) | Prequential scoring; revision-consistency diagnostics. |
| Bayesian hierarchical models | Partial pooling across stations/seasons/lead times/source strata. | Sparse-family modeling with local heterogeneity. | Rich archive with station metadata. | Can hide misspecification behind regularization; posterior certainty can mislead. | advanced_candidate (Stage 4–5) | Posterior predictive checks; leave-station-out and leave-year-out CV; prior sensitivity. |
| Quantile regression | Conditional quantiles instead of mean. | Near-threshold risk; asymmetric loss. | Predictor set, source-aligned observations; enough tail data. | Quantile crossing; tail extrapolation. | baseline_candidate (linear/constrained); forests later | Coverage diagnostics; CRPS/twCRPS; tail-bin reliability. |
| Distributional regression | Full conditional distribution by linking parameters to covariates. | Predictive density for non-Gaussian variables. | Rich covariates; sample size. | Easier to overfit; parametric family choice matters. | advanced_candidate (Stage 3–4) | PIT, CRPS, log score, tail-weighted scores. |
| GAMs / GAMLSS | Smooth nonlinear effects on location/scale/shape. | Seasonality, elevation, persistence covariates. | Long station histories; smooth-term-friendly covariates. | Specification difficulty with many interactions. | advanced_candidate (Stage 3–4) | Penalty tuning; blocked CV by season/station; PIT/tail checks. |
| Zero-inflated / hurdle / censored / mixture precipitation models | Point mass at zero + positive amount distribution. | Rain/no-rain and rain-amount markets. | Exact precipitation labels with trace coding. | Provider-specific trace conventions must be encoded. | baseline_candidate (precip families) | Occurrence calibration; positive-tail CRPS; trace sensitivity. |
| Calibration maps (isotonic / Platt / beta) | Monotone or parametric remapping of probabilities. | Post-hoc recalibration. | Independent calibration set. | Easy to contaminate via overlap. | baseline_candidate | Reliability, calibration-in-the-large, drift, separate splits. |
| Proper scoring rules and weighted scores (Brier, log, CRPS, twCRPS) | Honest probabilistic-forecast evaluation. | Validation backbone. | Forecast probabilities/distributions + verified outcomes. | Wrong score choice creates fake superiority. | baseline_candidate (immediate and mandatory) | Brier, log, CRPS/twCRPS, PIT/rank, reliability, sharpness, subgroups. |
| EVT / GEV / POT | Tail models for rare high-threshold events. | Rare-event family probability. | Long homogeneous series; many exceedances. | Nonstationarity; threshold selection; sparsity. Earliest research stage is Stage 5 in §16.1; treated as `defer` for any earlier-stage use. | advanced_candidate | Threshold-stability plots; tail-weighted scores; return-level validation; decade-block CV. |
| State-space models | Latent forecast bias or weather state evolves over time. | Forecast-error tracking. | Sequential forecast/observation histories. | Misapplied when process is regime-switching. | advanced_candidate (Stage 4) | One-step-ahead diagnostics; filtered-residual whiteness. |
| Kalman filters | Linear-Gaussian state-space special case. | Short-horizon bias correction. | Frequent updates. | Linear-Gaussian assumption misses jumps and tails. | advanced_candidate (later short-range) | Update-cycle backtests; lead-hour stratification. |
| Particle filters | Nonlinear assimilation. | Future, deferred. | Heavy. | High burden, easy to misuse. | defer | Not approved as primary engine. |
| Conformal prediction | Coverage-calibrated intervals / regions. | Possible abstention wrapper only; not a settlement-probability layer. | Clean calibration segment; stable nonconformity. | Coverage ≠ calibrated market probability. | defer | Empirical coverage; interval width; nonstationarity tests. |
| HMM / regime-switching | Regime-aware state shifts. | Seasonal/large-scale families. | Long time series with transitions. | Regimes not always stable or interpretable. | defer | OOS score; regime stability. |
| Geostatistical model averaging / kriging / GP | Local postprocessing; spatial coherence. | Translate grid forecasts to point-like targets. | Multi-station network. | Skill collapses under station holdout; representativeness mismatch. | advanced_candidate (Stage 4) | CRPS; spatial consistency; holdout by station. |
| Copulas / ensemble copula coupling | Dependence reconstruction after marginal calibration. | Multi-threshold or compound markets. | Multivariate matched histories. | Dependence unstable OOS. | advanced_candidate (Stage 5) | Multivariate scores; dependence calibration. |
| Analog forecasting | Case-based empirical probabilities. | Site-specific or gridpoint probabilities. | Large archives. | Similarity metric design; archive size. | baseline_candidate (where archives exist) | Brier, CRPS, analog stability. |
| Online learning / adaptive weighting | Adaptive combinations. | Multi-provider probability layer. | Time-ordered streams. | Weight updates can leak future information. | advanced_candidate | Rolling proper scores; purged-replay regret. |
| Information half-life / signal decay | Whether a signal remains actionable after publication. | Timing analysis. | Timestamps for source release and quotes. | Treating stale data as fresh. | research_candidate | Event-time decay curves; net EV by lag bucket. |
| Optimal stopping / sequential decision | Whether timing helps in principle. | Future, deferred. | Quote history, signal updates, close rules. | Hindsight re-optimization easy. | defer | Net EV by predeclared rule. |
| Market-aware probability adjustment | Market state influencing forecast-to-decision translation. | Future research. | Quotes, spreads, depth, source probabilities. | Feedback leakage from post-close prices; carries elevated reviewer caution because market-state feedback can amplify miscalibration if mishandled. | advanced_candidate | Net proper scores vs model-only and market-only baselines. |
| Source uncertainty adjustment | Explicit scenario or latent-state treatment of source/venue semantics. | Central MEG differentiator if pursued later; would be a bespoke research layer rather than an off-the-shelf method. | Resolution-rule archive; venue history; source-labeled outcomes. | Off-the-shelf literature thin. | defer | Separate semantic calibration; not just meteorological calibration. |

### 16.3 Variable-family suitability (per BWX-05Q)

Variable family matters as much as method. Temperature, precipitation, wind, snow, tropical, severe, and aggregates have different distribution families, zero structure, tail structure, and source sensitivity. Validation must be family-stratified. (BWX-RESEARCH-05Q.)

| Variable family | Candidate distribution families (research only) | Source-compatibility concerns |
|---|---|---|
| Temperature | Gaussian/NGR/EMOS; heteroscedastic normal; quantile regression; local BMA/GMA. | Airport-vs-city; time-of-observation. |
| Precipitation occurrence/amount | Zero-inflated/hurdle; gamma mixtures; left-censored GEV; censored shifted gamma; BMA-precip. | Trace, measurable threshold, accumulation window, source revisions. |
| Snowfall | Mixture; zero-inflated/censored; quantile/distributional; tail-aware. | Snowfall vs snow depth vs SWE; siting; phase change. |
| Wind/gust | Truncated/nonnegative; NGR/EMOS-wind; BMA; EVT (advanced); vector postprocessing for direction. | Station exposure; instrumentation; airport siting. |
| Hurricane / storm | Track/intensity ensembles; regime-dependent; copulas; EVT. | City/region wording vs storm-object definition. |
| Extreme-event families | EVT; GEV; POT; threshold-weighted scoring; tail-dependence. | Nonstationarity; revisions can flatter tails. |
| Monthly / seasonal aggregates | Bias-corrected combined distributions; Bayesian combinations; spatial-temporal. | Aggregation can mask daily station mismatches; window boundaries. |

### 16.4 The non-approval restated

No method named in §16 is approved for implementation. Method choice is **gated by §17**. A research candidate at a stage is research-eligible *at that stage*, never sooner.

---

## 17. Validation / evidence ladder (from WX-RESEARCH-06)

**This section is the safety backbone of the PRD.** Every implementation-adjacent ticket, every connector approval, every runtime decision, every model implementation, and every trading-adjacent step is gated by this ladder. No section elsewhere in this PRD overrides §17. Where any section appears to soften §17, §17 governs.

The ladder is drawn verbatim, in structure, from WX-RESEARCH-06. The seven stages are exact. No additional stages are introduced. No stage is renamed.

### 17.1 The seven stages

| Stage | Required evidence | Allowed conclusion | Allowed artifacts | What remains prohibited |
|---|---|---|---|---|
| **Stage 0** | Documentation and source-backed research only. | No implementation claims. Discussion of design and definitions only. | This PRD; research packets; canonical-event schema discussion; provider taxonomy discussion; trap taxonomy discussion; uncertainty decomposition discussion; method-family discussion. | Everything else, including all of §4. |
| **Stage 1** | Static examples and manual labels across families. | Can evaluate mapping logic and trap definitions only. | A manually-reviewed canonical-event-mapping gold set; trap-labeled example markets; family-stratified examples; inter-rater agreement evidence. | Any provider call; any connector code; any model run; any backtest claim. |
| **Stage 2** | Source-compatible historical labels with point-in-time provenance. | Can test label construction and compatibility, not edge. | Resolver-accurate historical labels; archive-layer-explicit labels; first-posted vs final-archive snapshots where applicable; station-ID-locked station records; publication-time-stamped advisory/observation/forecast records. | Edge claims; calibration claims on labels; live use. |
| **Stage 3** | Retrospective probability scoring on strict OOS splits. | Can discuss calibration and ranking quality. | Brier, log, CRPS, twCRPS as appropriate; reliability diagrams; PIT/rank histograms; threshold-bucket calibration; comparison vs climatology and persistence baselines; rolling-origin / walk-forward splits; leave-station-out and leave-year-out CV where applicable. | Trading claims; executable-cost claims; runtime behavior. |
| **Stage 4** | Trap-filtered paper simulation with executable quotes, fees, spreads, depth assumptions. | Can discuss net-of-cost paper evidence; still no implementation approval. | Paper-simulation records using best bid/ask, quote age, depth, fees, maker/taker semantics, partial-fill assumptions; net-EV, fill rate, spread paid, fee burden; ablations vs midpoint, vs no-fee, vs stale-quote, vs taker-only. | Live execution; live ingestion; live monitoring; autonomy. |
| **Stage 5** | Human-reviewed dry run with reviewer packets and override logs. | Can assess operational intelligibility. | Reviewer packets per §24; override logs with reason capture; inter-rater agreement (Cohen's-kappa-style); reviewer drift audits. | Live execution; live ingestion; autonomy. |
| **Stage 6** | Runtime observation only under separate approval. | Observe behavior without execution. **Not approved by this PRD.** | (None under this PRD.) | Execution; trading; order placement. |
| **Stage 7** | Any execution/trading after separate explicit approval. | **Outside the scope of this PRD.** | (None under this PRD.) | Everything not in the separately approved scope. |

### 17.2 Gate-passage rules

- Each stage requires the evidence specified above to **exist and be reviewable**. Existence is not sufficient; a human reviewer must have confirmed each artifact at the gate.
- Each stage requires that the **previous stage's** evidence remain intact and unrevoked. Regression in an earlier stage automatically de-stages the bot.
- Each stage gate is a *hard gate*. No conditional bypass, no "fast track," no "the spec is mostly there." A gate is cleared or it is not.
- The PRD-level posture for §17 is: **the current packet posture is Stage 0**. This PRD is itself a Stage 0 artifact. Nothing in this PRD authorizes Stage 1.

### 17.3 Mandatory backbone statement

> **No implementation-adjacent ticket may be opened until the relevant stage-gate evidence exists.**

This sentence is the operational backbone of the PRD. It is reproduced in every implementation-roadmap section (§§27, 30) and in every fail-closed rule (§26). It is not subject to delegation, exception, or interpretation.

---

## 18. Data requirements and archive requirements

The data requirements below are **planning requirements** for the work that would have to be done to clear Stages 1–4 of §17. None of them is an authorization to acquire, ingest, or store data. None of them is an approval to call a provider. They define what would need to exist before implementation-adjacent work is permitted to begin.

### 18.1 Required future data categories

| Data category | Why needed | Likely sources | Availability challenges | Leakage risk | Confidence |
|---|---|---|---|---|---|
| Venue market metadata | Without contract semantics, no valid label task exists. | Venue rule pages, rules summaries, timeline/payout, rulebook, market outcomes. | Historical contract-term snapshots may be incomplete; outcome review can alter normal paths. | Hindsight mapping; missing fallbacks/discretion. | confirmed |
| Raw market wording | Headline plus rules summary plus full contract terms archived at decision time. | Venue contract files. | As above. | As above. | confirmed |
| Market rules / resolution text | Operative settlement logic. | Venue contracts; rulebooks. | As above. | As above. | confirmed |
| Market price history | Time-ordered trade and quote history. | Venue last-trade and quote feeds. | Historical depth may be incomplete. | Midpoint fantasy; cost omission. | confirmed |
| Executable quote / order-book snapshots (if Stage 4+ later approved) | Cost-aware paper-simulation realism. | Venue order book; quick/limit-order docs; fee schedule; full quote history if available. | Historical depth/quote data often incomplete; fill probabilities venue-specific. | Midpoint leakage; adverse-selection blindness. | confirmed |
| Official resolver source records | Source-compatible labels for stages 2+. | NWS CLI/CF6/NOWData; NCEI CDO/GHCN-Daily/Storm Events; NHC advisory archive; HURDAT2; SPC/NCEI severe archives. | First-posted snapshots not always preserved; some archives are explicitly post-analyzed or delayed. | Final-archive leakage; revision leakage. | confirmed |
| Station metadata | Station-identity correctness. | ASOS/AWOS docs; GSH/1-minute ASOS; NCEI Station Histories; HOMR; FAA observing guidance. | Element locations differ; historical moves matter. | Station mismatch; representativeness mismatch. | confirmed |
| Historical observations | Validation labels and source-comparison anchors. | NCEI archives; agency products. | Delays; revisions; reprocessing. | Revision leakage. | confirmed |
| Forecast data available at decision time | Decision-time replay; forecast-run leakage prevention. | NCEI GFS/GEFS archives; HRRR; LAMP; NDFD; ECMWF Open Data / MARS / archive docs. | Exact publish timestamps harder than cycle timestamps; archive access varies by service. | Forecast-run leakage; hindsight provider choice. | confirmed |
| Model-run publication timestamps | Distinguish init time from public availability time. | Provider/agency publication logs. | Often only cycle time is canonical; publish time may need derivation. | Timing leakage. | unclear |
| Advisory products | Storm/severe market authority layers. | NHC advisory archive and product descriptions; NCEI Storm Events / Storm Data; SPC where relevant. | Preliminary vs official disagreement; multi-month archive lag. | Advisory-vs-post-analysis leakage; authority mismatch. | confirmed |
| Provider / source metadata | Source-class tagging; auditability. | Provider docs; agency docs. | Variable transparency across providers. | Untagged inputs. | confirmed |
| Archive revision / finality records | Distinguish first-posted from final. | Source-side version history (e.g., Weatherbit revision IDs; Storm Events versions; GHCNd reprocessing). | Variable across products. | Revision leakage. | confirmed |
| Human labels | Manual canonical-mapping gold set; trap labels. | Internal review. | Production volume; reviewer time. | Reviewer drift. | confirmed |
| Trap labels | Stage 1 validation. | Internal review. | As above. | As above. | confirmed |
| Validation splits | Rolling-origin / walk-forward / leave-station-out / leave-year-out. | Internal design. | Sample sufficiency for rare families. | Split leakage. | confirmed |
| Paper simulation records | Stage 4 evidence. | Internal records. | Quote/depth history quality. | Midpoint leakage; partial-fill misassumption. | confirmed |

### 18.2 The point-in-time provenance requirement

Every datum used at any future stage of Weather Bot must carry the provenance fields named in §9.4: source identifier, publication timestamp, archive layer, revision version (where exposed), retrieval timestamp, and as-of decision timestamp. Provenance is *not* a logging nicety. It is the precondition for §§19–21.

---

## 19. Point-in-time replay requirements

Decision-time replay is the single most important defense against forecast-run leakage and final-archive leakage. Any future stage 2+ work must satisfy the rules below; rules are derived from WX-RESEARCH-06 and BWX-RESEARCH-05A.

### 19.1 As-of joins

- Every join between a market record and a source/forecast record must be performed as-of a documented decision timestamp.
- The decision timestamp is the timestamp at which a hypothetical human reviewer could have acted, given the data available to them at that moment.
- Future-stamped data may not participate in the join.

### 19.2 Decision-time snapshots

- Source records used in replay must be the snapshot **as it appeared at the decision timestamp**.
- For sources that revise, the first-posted snapshot must be retrievable separately from later archive-quality snapshots.

### 19.3 Source availability at decision time

- A source value may be used at decision time only if its publication time is on or before the decision timestamp.
- Where publication time is unknown (only cycle time is canonical), the value's `availability_status` is `unclear`; using it as available is a `blocking` leakage.

### 19.4 Model run publication time

- Model runs (GFS, GEFS, ECMWF, HRRR, LAMP, NDFD, others) are timestamped by **publication time**, not by initialization time.
- Initialization time may be metadata; it may not serve as decision-time availability.

### 19.5 No future forecast updates

- Forecast cycles later than the decision timestamp may not contribute features to the replay.
- Forecast updates that arrived after market close may not be used as decision inputs.

### 19.6 No final archive leakage

- Final archives may not be used as decision-time observations for markets that resolved on preliminary or first-posted data.
- Storm Events Database values (lag ~75–90 days) must not appear in decision-time replay for markets that resolved earlier.
- HURDAT2 / TCR post-analysis values may not appear for advisory-time markets.

### 19.7 Market close / resolution timing

- Market close, market determination, market settlement, and outcome-review windows are separately timestamped.
- A trade is feasible only before close; a feature is decision-time-available only before the decision timestamp; a label is observable only after the venue-defined resolution time and only at the venue-defined `archive_layer`.

### 19.8 Station / source selection timing

- Station selection cannot use information that arrived after the listing.
- Provider selection cannot be hindsight-driven by outcome.
- Source-product selection cannot be hindsight-driven by what later best matched the realized outcome.

### 19.9 Provider availability timing

- Provider availability (presence, rate-limit headroom, terms in force) at the decision timestamp must be modeled, where any future stage proposes using provider data.

### 19.10 Human review timestamping

- Reviewer notes, override decisions, and reviewer adjudication must themselves be timestamped, so that human-review evidence cannot be retro-fitted to outcomes.

---

## 20. No-lookahead and no-final-archive-leakage rules

The no-lookahead rules below are mandatory for every future stage of Weather Bot that uses historical evidence. Each rule is enforceable; any violation is a `blocking` validation failure per §17.

| Rule | Statement |
|---|---|
| No final observations before they were available | An observation value may not participate in a replay as available at time `t` unless its publication time ≤ `t`. |
| No revised archive values treated as real-time truth | An archive-quality value may not stand in for a first-posted value at a market that resolves on first-posted. |
| No hindsight station/source choice | The station, the source product, the archive layer, and the provider must be fixed prior to outcome inspection. |
| No future market prices | Market prices later than the decision timestamp may not contribute features at that timestamp. |
| No post-resolution labels before resolution time | Labels become observable only at and after the venue-defined resolution time, at the venue-defined `archive_layer`. |
| No future forecast cycles | Forecast runs published after the decision timestamp may not contribute features at that timestamp. |
| No tuned thresholds using test data | Threshold-bucket boundaries, calibration maps, and hyperparameters may not be tuned on the test split. |
| No provider selected after seeing outcomes | The candidate provider set, the constraints applied, and the source-class tags must be fixed prior to outcome inspection. |

WX-RESEARCH-06 lists these as "Weather Bot–specific temporal and semantic leaks." They are not generic ML hygiene. They are the specific mechanisms by which false edge is manufactured in weather-market work.

---

## 21. Forecast-run publication-time rules

These rules are an explicit subset of §§19–20, broken out because forecast-run timing is the single most frequent leak mode named in BWX-RESEARCH-05A.

| Rule | Statement |
|---|---|
| Forecast runs are timestamped by publication / availability time | Init/cycle time is metadata; publication time is the decision-relevant timestamp. |
| Model cycles are handled as-of | At any decision timestamp `t`, only runs with publication time ≤ `t` are available. |
| Advisories are handled by release time | NHC advisory archives, intermediate advisories, special advisories: release time governs. |
| Observation updates are handled by availability time | Station observations, METAR, climate-report posting times: availability governs. |
| Archive revisions are separately tracked | Real-time feeds and archive-quality replacements (GHCNd ~45–60 days post-month-end; Storm Events ~75–90 days) are distinct timestamps. |
| Any later implementation must prove data was available at the claimed decision time | This is the load-bearing audit requirement for any Stage 3+ replay; absence of proof is `blocking`. |

Provider-side and agency-side publication clocks are documented in BWX-RESEARCH-05A's timing table (GFS/GEFS at 00/06/12/18 UTC; ECMWF main at 00/12 UTC with 06/18 supplementary; HRRR hourly with 15-minute radar assimilation; LAMP hourly with some 15-minute guidance; NDFD twice per hour at ~:25/:55; ASOS continuous with hourly METAR and SPECI special observations; NEXRAD per volume scan; NHC full advisories every 6 hours, intermediates every 3 hours when watches/warnings exist, special advisories anytime; HURDAT2 post-season). These are *cadence* anchors; **publication-time** values must be ascertained per record.

---

## 22. Threshold-bucket calibration requirements

Threshold-bucket calibration is a Stage 3 requirement (§17). It addresses the fact that weather markets are most fragile precisely at the threshold. Reliability and proper-score performance averaged across the entire distribution can hide calibration failure exactly where calibration matters most.

### 22.1 Calibration dimensions

Future stage-3 work must compute calibration along the following axes simultaneously, not only globally:

| Axis | Why |
|---|---|
| By market family | Temperature, precip, snow, wind, tropical, severe, aggregates have different distribution families and source sensitivities. |
| By threshold distance | Near-strike vs interior-of-distribution buckets behave very differently. |
| By calibration near cutoffs | Reliability bins around the strike must be reproducible and accompanied by sample-size histograms. |
| By forecast horizon | Calibration tends to worsen with lead time. |
| By station / source compatibility | Source-compatibility status is a calibration covariate. |
| By trap category | Markets with active `caution` traps may calibrate differently than `pass` markets. |
| By season / regime | Where supported by sample size; seasonal/subseasonal anomaly definitions must be consistent (WX-RESEARCH-04). |
| By archive layer | First-posted-resolved markets must be calibrated against first-posted labels, not final archives. |

### 22.2 Scoring rules and diagnostics

| Score / diagnostic | Use |
|---|---|
| Brier score | Headline for yes/no threshold markets; stratify by family and threshold, not just global average. |
| Brier decomposition (reliability, resolution, uncertainty) | Distinguish overconfidence from low discrimination. |
| Log score | Supplemental to Brier; harsh under overconfident misses. |
| CRPS | Default for continuous predictive distributions. |
| Threshold-weighted CRPS (twCRPS) | Mandatory for rare-event families and near-strike windows; track body-tail tradeoff. |
| Reliability diagrams | Mandatory for binary markets; reproducible bins; sample histograms; interval estimates. |
| PIT / rank histograms | Full-distribution or ensemble products before threshold extraction. |
| Sharpness | Track jointly with calibration, never alone. |
| ROC / AUC | Discrimination only; not a calibration measure. |
| Calibration-in-the-large | Sanity check; pair with reliability and subgroup tests. |
| Market-specific scoring | Score against the exact settled market event, not just the meteorological variable. (Confidence: unclear; future MEG construct.) |
| Resolution-risk-adjusted scoring | Future internal score combining forecast quality with penalties for unresolved semantic or source risk. (Confidence: unclear; future MEG construct.) |

### 22.3 Rare-event handling

Tail events are small-sample problems by construction. EVT-heavy or threshold-weighted training carries body-tail tradeoffs that must be tracked, not optimized over silently. Stage 5 in §16 is the earliest research stage at which EVT pipelines become candidates; Stage 3 calibration work must respect the limitation rather than disguise it.

### 22.4 Mandatory threshold-bucket evidence before any "edge" language

WX-RESEARCH-06 is explicit: no "edge" language is permitted in Weather Bot intelligence outputs until threshold-bucket calibration has been demonstrated on strict OOS splits. This is a Stage 3 hard gate.

---

## 23. Market microstructure and executable-cost simulation requirements

This section is a future Stage 4 requirement (§17). It defines what would have to be true for any "edge" claim to survive being haircut by realistic execution costs. It does not approve trading.

### 23.1 Required simulation components

| Component | Why |
|---|---|
| Bid / ask spread | Edge at midpoint is not edge at executable price. |
| Liquidity / depth | Quick orders can execute across multiple price levels; depth disappears on information shocks. |
| Fees | Trading fees on immediate matches; maker rebates where they exist; venue-specific fee categories. |
| Slippage | Sweep through depth; partial-fill behavior. |
| Stale prices | The displayed book may be older than the latest source publication. |
| Time to resolution | Capital locked up until determination/settlement; opportunity cost. |
| Quote availability | Periods of no quotes are not periods of zero spread. |
| Partial fill assumptions | Limit orders may partially execute; quick orders may sweep. |
| Market close timing | Close vs determination vs settlement are distinct clocks. |
| Adverse selection | Informed counterparties widen spreads when information arrives. |
| Crowding | Other participants reacting to the same source updates. |
| Maker / taker asymmetry | Recent Kalshi research finds maker-side trades outperform taker-side on average. |

### 23.2 Required reporting fields per simulated trade

WX-RESEARCH-06 requires that, at minimum, a research simulation report: best bid / ask used; quote age; assumed fill rule; fee rule; spread paid; depth consumed; whether the order was maker-like or taker-like.

### 23.3 Required ablations

| Ablation | Test |
|---|---|
| Midpoint vs executable | Edge that exists at midpoint but not at bid/ask → `false_edge`. |
| With and without fees | Edge that vanishes after fees → `false_edge`. |
| Stale quotes vs fresh quotes | Edge that requires guaranteed fill at stale quotes → `false_edge`. |
| Maker-only vs taker-only | Edge that requires guaranteed maker fills → `caution`. |
| Depth-respecting vs unlimited depth | Edge that requires non-existent depth → `false_edge`. |
| Partial-fill aware | Edge that assumes full fills → `caution`. |

### 23.4 The non-trading reminder

§23 defines what *would* be required for any future edge claim to be meaningful. It does **not** authorize trading, paper or live; it does **not** authorize order placement; it does **not** authorize any execution path. Stage 4 evidence is paper-simulation evidence reviewed by humans, not trades.

---

## 24. Human-review workflow

Human review is a first-class capability of Weather Bot, not a UX afterthought. WX-RESEARCH-06 makes the case directly: "venue discretion, resolver fallback, and language ambiguity cannot always be resolved statistically." The human reviewer is therefore the only correct authority for `blocking` adjudication, override decisions, and ambiguity resolution. The MEG Master PRD v4.1 also requires operator approval through Telegram for any strategy execution, but that pathway is **separately gated** and not approved here; the §24 reviewer is a Stage 1–5 research and intelligence reviewer, not an execution operator.

### 24.1 Future human-review packet contents

Each future packet (Stage 1+) per market must contain at minimum the following fields. Field names below are normative for design discussion.

| Field | Description |
|---|---|
| `canonical_event_summary` | Single-sentence summary of the canonical event. |
| `venue_market_wording` | Headline + rules summary + full contract terms archived at decision time. |
| `resolver_source` / `resolver_source_authority` / `source_url` / `archive_layer` / `freeze_rule` / `revision_treatment` | Per §§6, 9. |
| `station_id` / `station_source_authority` / `geographic_precision` | Per §§6, 9. |
| `measurement_window` (`time_window_start`, `time_window_end`, `timezone`, `aggregation_method`) | Per §6. |
| `threshold_value`, `threshold_unit`, `comparator`, `rounding_rule`, `trace_rule`, `missing_rule` | Per §6. |
| `classification_authority`, `classification_time_layer` | Per §6 (storm/severe only). |
| `provider_source_compatibility_flags` | Per §8. Includes per-provider class tags and any forbidden substitutions. |
| `active_trap_flags` and `controlling_trap_severity` | Per §11. |
| `active_uncertainty_components` | Per §§12–13. |
| `alpha_hypothesis_if_any` | From §14, with explicit non-approval reminder, source-compatibility statement, timing layer, station/window/threshold mapping, false-edge list, validation state, confidence value, and `no-trade` / `caution` / `blocking` note. |
| `false_edge_risks_active` | Per §15, with severity and reason. |
| `validation_stage` | The §17 stage that this market's evidence has reached. |
| `status_readiness` | Per §25 (one of the readiness states). |
| `no_trade_caution_blocking_explanation` | A reviewer-readable rationale for any caution or blocking decision. |
| `unresolved_questions` | Any field flagged `unclear` or `unknown`. |
| `non_approval_boundaries` | A restatement, per market, of the §4 non-approvals that apply. |

### 24.2 Reviewer adjudication

- Reviewers may downgrade a `blocking` trap only with documented rationale. Silent downgrades are forbidden.
- Reviewers may upgrade a `caution` trap to `blocking` at their discretion.
- Reviewer decisions must be timestamped, logged, and auditable (§19.10).
- Inter-rater agreement must be measurable via a Cohen's-kappa-style statistic (WX-RESEARCH-06). Low agreement on `blocking` / `caution` / `pass` decisions is itself a `blocking` Stage 5 evidence failure.

### 24.3 Override logs

- Every override must record the reviewer, the timestamp, the trap/field overridden, the rationale, the alternative state recorded, and the evidence cited.
- Override prevalence is itself a metric; drift in override patterns is `caution`.

### 24.4 Non-execution scope

§24's reviewer is a research and intelligence reviewer at Stages 1–5. The §24 reviewer does not place orders, does not approve execution, does not approve runtime ingestion, and does not bypass §17. Execution authority is separate and not approved by this PRD.

---

## 25. Observability / status / result summary requirements

**Controlling source:** PRD-P1-WX-04 (the result/status/observability summary contract) controls the closed-set vocabulary used in this section for readiness state, summary severity, and review posture, and PRD-P1-WX-03 controls the closed-set vocabulary for config/secrets readiness. Where the WX-03 / WX-04 closed sets and this PRD diverge, WX-03 / WX-04 govern and this section has been aligned accordingly. WX-RESEARCH-03 continues to control trap severity (`{caution, blocking}`) and WX-RESEARCH-06 continues to control the human-review and safety constraints layered on top of the WX-04 summary contract.

### 25.1 Safe non-secret summaries

Every status/result/observability output of Weather Bot at any future stage must:

- contain no secrets, no credentials, no raw tokens;
- contain no provider API responses verbatim (where any future stage uses them);
- contain no implication of execution;
- contain no implication of forecast pull unless that is explicitly approved in a later stage;
- contain no trading, order, or autonomy implication.

### 25.2 Readiness states (closed set, aligned with PRD-P1-WX-03 §4 and PRD-P1-WX-04 §5)

The only machine-checkable readiness-state values used in Weather Bot status/result/observability summaries are those defined by PRD-P1-WX-03 §4 and PRD-P1-WX-04 §5. Hybrid, custom, or slash-based actual values are forbidden. Nuance belongs in prose notes, not custom field values.

| State | Meaning (per WX-03 / WX-04) |
|---|---|
| `missing` | Required config, status, or summary input is absent. |
| `disabled` | The relevant weather/provider/connector path is intentionally disabled. |
| `unapproved` | Provider, connector, runtime, environment, forecast, or actionability approval has not been granted. |
| `invalid` | Status/summary inputs are present but malformed, inconsistent, unsafe, stale, or fail validation. |
| `ready` | The specific summary/input condition is present, valid, explicitly approved for the scope of this PRD's planning posture, and still subject to later connector/runtime/trading gates per §17. |

`ready` does **not** approve connector implementation, runtime execution, external API calls, forecast pulls, trading, order placement, or autonomy. Reading `ready` as authorization is prohibited.

Concepts that the PRD synthesis prior to reconciliation expressed through readiness values (research-only posture, awaiting-review posture, reviewer-cleared-caution, reviewer-affirmed-block, awaiting archive finalization) are not eliminated; they are simply expressed through other PRD fields rather than through the readiness-state value:

- **Per-market reviewer-workflow state** lives in §6.1's `human_review_state` closed set: `unreviewed`, `caution_under_review`, `blocking_under_review`, `reviewed_pass`, `reviewed_caution`, `reviewed_block`.
- **Per-market evidence stage** lives in §17's seven-stage ladder; a reviewer packet records the stage explicitly via the `validation_stage` field in §24.1.
- **Awaiting archive finalization** is expressed by `archive_layer = "unclear"` or by the venue-defined `revision_treatment` field per §6.1 and §9.6, accompanied by a reviewer note. It is not a top-level readiness-state value.

Forbidden as actual readiness-state values, per WX-03 §5 and WX-04 §6 and reinforced here: `not_ready`, `research_only`, `ready_for_review`, `reviewed_caution` (as a *readiness-state* value — it remains valid as a `human_review_state` value per §6.1), `reviewed_block` (same caveat), `pending_finalization` (as a *readiness-state* value), `partial`, `mixed`, `ready_with_warnings`, `maybe_ready`, `approved`, `configured`, `available`, `unknown`, `warning`, `error`, `critical`, `success`, `ok`, `actionable`, `trade_ready`, `auto_execute`, `autonomous`, `live`.

### 25.3 Summary severity (closed set, aligned with PRD-P1-WX-04 §5)

| Severity | Meaning (per WX-04) |
|---|---|
| `info` | Safe informational summary with no blocker; background or contextual statement. |
| `caution` | Reviewer-visible caveat or risk note that does not imply execution approval; corresponds to active `caution` per §§11, 15. |
| `blocked` | Must prevent provider/runtime/forecast/action behavior; corresponds to active `blocking` per §§11, 15. |

`info` does not approve connector implementation, runtime execution, external API calls, forecast pulls, trading, order placement, or autonomy. Forbidden as actual summary-severity values, per WX-04 §6: `warning`, `error`, `critical`, `success`, `ok`, `ready_with_warnings`, `info/caution`, `caution/blocked`, and any other hybrid or invented value.

### 25.4 Review posture (closed set, aligned with PRD-P1-WX-04 §5)

| Posture | Meaning (per WX-04) |
|---|---|
| `informational` | Non-actionable context only. The summary is provided for reviewer understanding and does not imply execution authority. |
| `review_only` | Human-reviewable summary that does **not** approve execution; reviewer must inspect before any downstream consumer treats the summary as actionable. |
| `blocked` | Summary indicates the system must not proceed. Downstream consumers must treat the underlying path as fail-closed. |

`informational` and `review_only` do not approve connector implementation, runtime execution, external API calls, forecast pulls, trading, order placement, or autonomy. Forbidden as actual review-posture values: `no_review_needed`, `human_review_pending`, `human_review_complete`, `human_override`, `partial`, `mixed`, `approved`, `configured`, `available`, `actionable`, `trade_ready`, `auto_execute`, `autonomous`, `live`, and any other hybrid or invented value.

Per-market reviewer-workflow detail (who reviewed, whether review is pending, whether an override has been recorded) is **not** expressed in the WX-04 review-posture field. Reviewer-workflow detail lives in §6.1's `human_review_state` field, in `manual_override_flag`, and in the override-log records described in §24.3.

### 25.5 Style requirements

- Summaries are concise, factual, and source-tagged.
- Summaries never imply approval the bot does not have.
- Summaries never present probabilities as truth.
- Summaries never present market prices as truth.
- Summaries explicitly state the §17 stage of the underlying evidence.

### 25.6 Hard observability prohibitions

- No telemetry channel may export secrets or credentials.
- No logging may emit raw provider API responses (where any future stage uses them).
- No status board may imply trading or execution.
- No external pageable channel may exist for Weather Bot under this PRD; alerting design is gated by Stage 6 of §17, which is not approved here.

---

## 26. Risk gates and fail-closed behavior

Risk gates below are the operational expression of §11 (trap severity), §15 (false-edge), §17 (evidence ladder), §25 (observability), and §4 (non-approvals). Every gate fails closed.

### 26.1 Fail-closed gates

| Gate | Trigger | Closed behavior |
|---|---|---|
| Missing config / source / provider information | Any required field is absent or `unclear`. | Block. No automated reasoning, no implementation-adjacent ticket. |
| Disabled provider path | A provider has not cleared its source-compatibility review. | Block any analysis that would have used the provider as settlement-equivalent. |
| Unapproved connector / runtime / forecast path | A path required for the analysis is not approved by §17. | Block. |
| Invalid / malformed config | Schema mismatch, missing required field, malformed token (where any future stage involves config). | Block. |
| Unclear resolver source | `resolver_source = "unclear"` or `archive_layer = "unclear"`. | Block. |
| Source mismatch | Provider class does not match the venue's resolver class. | Block. |
| Trap severity blocking | Any active `blocking` trap. | Block. |
| Missing point-in-time provenance | Provenance fields absent or untrustworthy. | Block. |
| Insufficient validation stage | Implementation-adjacent ticket attempted before §17 stage clearance. | Block ticket creation. |
| Microstructure cost uncertainty | Stage 4 paper-simulation evidence absent or unreviewed. | Block edge claims. |
| Human-review override requirement | A `blocking` trap is being downgraded. | Block until reviewer rationale is recorded. |

### 26.2 The fail-closed default

If none of §26.1's gates can be evaluated, the system fails closed. "We don't know" is identical to "we are blocking."

### 26.3 Re-opening a gate

A gate may be re-opened only when the precondition that caused it to close has been corrected and the correction has been reviewed. Re-opening is recorded with the same audit fidelity as override (§24.3).

---

## 27. Implementation roadmap by phase (planning level only)

This roadmap is **planning-level only**. No phase below is approved for implementation. Phases A–E are research/design work consistent with Stage 0–3 of §17. Phases F–G map to Stage 4–5. Phases H–I are explicitly gated by §17 Stages 6–7 and are **not** approved by this PRD.

| Phase | Goal | Maps to §17 stage | Allowed work | Explicitly not approved |
|---|---|---|---|---|
| **A. PRD approval and research freeze** | This PRD is reviewed, approved, and frozen as the source of truth for downstream tickets. Research packets are frozen at their current versions. | Stage 0 | PRD review; freeze of WX-01..06, BWX-05A, BWX-05Q. | Any §4 activity. |
| **B. Static examples / manual labels** | Build a manually reviewed canonical-event-mapping gold set across the family taxonomy in §7. Build trap-labeled example markets per §11. | Stage 1 | Reviewer adjudication; family-stratified examples; inter-rater pilot; gold-set design notes. | Any provider call; any connector code; any model run. |
| **C. Historical label design** | Design (not run) source-compatible historical labeling protocols for the early-candidate families in §7. Specify how first-posted, archive-quality, and post-analysis layers will be distinguished. | Stage 2 (design only) | Label-protocol design; archive-layer schema; station-binding registry design. | Live provider calls; ingestion. |
| **D. Validation dataset design** | Design (not build) the validation splits: rolling-origin, walk-forward, leave-station-out, leave-year-out, family-stratified. | Stage 2 (design only) | Split-design documentation; sample-sufficiency analysis on paper. | Building datasets through live calls. |
| **E. Probability scoring research** | Design (not run) the probability-scoring methodology: Brier, log, CRPS, twCRPS, reliability diagrams, PIT/rank histograms, threshold-bucket calibration. Identify baseline candidates (climatology, persistence) and stage-2 candidates (logistic/probit, isotonic/Platt calibration) per §16. | Stage 3 (design only) | Method documentation; literature mapping; reading lists. | Model runs; backtests. |
| **F. Paper simulation design** | Design (not run) the executable-cost paper simulation per §23, including quote/depth/fee/maker-taker handling. | Stage 4 (design only) | Simulation-design documentation; reporting-field design. | Live execution; paper trades; canary runs. |
| **G. Human-reviewed dry-run design** | Design (not run) the reviewer packets per §24, the override log structure, and the inter-rater protocol. | Stage 5 (design only) | Reviewer-packet schema; override-log schema; Cohen's-kappa protocol design. | Live observation; live ingestion. |
| **H. Runtime observation proposal** | **Not approved by this PRD.** A separate approval is required. | Stage 6 (gated) | (None under this PRD.) | Everything not in the separately approved proposal scope. |
| **I. Execution / trading proposal** | **Not approved by this PRD.** A separate explicit approval is required. | Stage 7 (gated) | (None under this PRD.) | Everything not in the separately approved scope. |

**No jumps.** Codex tickets, design tickets, or any planning artifacts that propose jumping past a phase are not allowed. The roadmap is strictly sequential through Phase G; Phases H and I are out of scope.

---

## 28. Testing strategy

The testing categories below are **planning** for future test design. None of them is approved to run against live providers, live ingestion, or live execution. They are the test categories the system would have to satisfy at each §17 stage.

| Category | Purpose | Stage |
|---|---|---|
| Static doc/spec tests | Verify that canonical-event schema, trap taxonomy, uncertainty decomposition, and provider classification are internally consistent and stable across review cycles. | Stage 0–1 |
| Canonical event mapping tests | Verify, on the gold set, that mapping logic produces correct `canonical_event_id` values and correctly populates load-bearing fields. Critical-field accuracy, ambiguity recall, and exact-match accuracy are required metrics. | Stage 1 |
| Source compatibility tests | Verify that the provider/source classification (§8) produces correct compatibility judgments on labeled examples. False-positive and false-negative rates required. | Stage 1–2 |
| Trap taxonomy tests | Verify trap precision and recall on labeled examples. False-negative rate on `blocking` traps is the controlling metric. | Stage 1 |
| Closed-set validation tests | Verify that severity, readiness, posture, severity, confidence values only ever take values from the closed sets defined in this PRD. Hybrid/invented values must fail. | Stage 0 onward |
| Point-in-time replay tests | Verify that historical replay enforces §19's rules: as-of joins, decision-time snapshots, source availability at decision time, model run publication time, no future forecast updates, no final archive leakage. | Stage 2–3 |
| No-lookahead tests | Verify §20's rules: no final observations before they were available, no revised archive as real-time truth, no hindsight station/source/provider choice, no tuned thresholds on test data. | Stage 2–3 |
| Provider/source fixture tests (if later approved) | If a future stage approves provider use, fixture tests verify that connector code (also future, not approved here) correctly tags source class, archive layer, publication time, station identity. | Stage 6+ (gated) |
| Probability calibration tests | Brier, log, CRPS, twCRPS, reliability diagrams, PIT/rank histograms, threshold-bucket reliability — all stratified per §22. | Stage 3 |
| Paper simulation tests | Verify §23's required ablations; verify executable-cost behavior at quote-age boundaries, fee boundaries, depth boundaries, maker/taker assignment. | Stage 4 |
| Human-review packet tests | Verify §24's reviewer-packet schema is complete and well-typed; verify override-log schema integrity; verify Cohen's-kappa pipeline. | Stage 5 |
| Safety / non-approval tests | Verify that no test, fixture, or pipeline introduces `live`, `production`, `trading`, `execution`, or `autonomy` codepaths absent the appropriate §17 approval. | All stages |

---

## 29. Open blockers and unresolved research questions

| Question / blocker | Source / research basis | Why it matters | Current confidence | Recommended next research / planning action | Blocks implementation-adjacent work? |
|---|---|---|---|---|---|
| Exact NOAA/NCEI daily archive and local-day convention for U.S. daily precipitation/snowfall markets when venue rules are silent | WX-RESEARCH-02 open question | Drives `archive_layer` and `day_definition` defaults; absence creates `blocking` traps. | unclear | Per-family product/freeze-rule audit before Stage 2. | yes |
| Final authority for severe-weather occurrence markets (SPC reports vs Storm Data/Storm Events vs WFO vs venue text) | WX-RESEARCH-02 open question | Determines whether severe-occurrence markets can be brought above `avoid_for_now`. | unclear | Authority-layer audit; venue-text census. | yes |
| Canonical location policy for "city" markets (named airport, station set, geofence, or official gridpoint) | WX-RESEARCH-02 open question | Drives `geographic_precision` and station mapping. | unclear | Policy decision before Stage 2. | yes |
| Whether Meteostat can be used safely in any resolution-sensitive flow without forcing station/observation-only mode | WX-RESEARCH-02 open question | Source-class tagging implications. | unclear | Constrained-mode audit before any provider use is proposed. | yes |
| Whether Meteomatics commercial terms / redistribution rights / audit constraints are acceptable for a future connector | WX-RESEARCH-02 open question | Stage 6+ connector gating. | unknown | Terms review at connector-approval gate, which is not approved here. | yes |
| Whether Open-Meteo commercial terms, SLA, and long-term commitments suffice for a future production connector | WX-RESEARCH-02 open question | Stage 6+ connector gating. | unknown | Terms review at connector-approval gate. | yes |
| Whether Weatherbit should remain `defer` once deeper aggregation semantics and revision behavior are audited | WX-RESEARCH-02 open question | Source-class refinement. | unclear | Deeper docs audit; defer decision. | yes |
| Whether AccuWeather can be scored in a later pass | WX-RESEARCH-02 open question | Shortlist completeness. | unknown | Future research pass once public docs improve. | not on its own |
| International (non-U.S.) national meteorological agency role analogues to NOAA/NWS/NCEI | WX-RESEARCH-02 open question | International markets require country-specific official product. | unknown | Per-country audit; ECCC + Met Office partly mapped. | yes (for non-U.S. markets) |
| Historical access to first-posted snapshots for every resolver layer (not only final archives) | WX-RESEARCH-06 open question | Some alpha hypotheses cannot be validated safely without this layer. | unclear | Archive-availability audit per family. | yes |
| Full historical order-book depth and quote-age data, not just last-trade / midpoint | WX-RESEARCH-06 open question | Cost-aware simulation (§23) fails without it. | unclear | Venue-side data audit. | yes (for Stage 4) |
| Historical publication timestamps for all candidate forecast providers/products, beyond nominal run cycles | WX-RESEARCH-06 open question | Timing alpha is unsafe without availability clocks. | unclear | Provider-side metadata audit. | yes |
| Lossless machine-readable archival of venue contract terms and amendments across time | WX-RESEARCH-06 open question | Mapping validation depends on historical rule snapshots. | unclear | Internal archival design. | yes |
| Sufficient strictly source-compatible samples after trap filtering for rare severe/tropical families | WX-RESEARCH-06 open question | Rare-event families may need to remain `defer` for sample-size reasons until ample evidence is built. | unclear | Sample-sufficiency study at Stage 2. | yes (for rare families) |
| Whether conformal and other distribution-free methods maintain useful coverage when labels are source-defined and nonstationary | WX-RESEARCH-06 open question | Whether they progress beyond `defer`. | unclear | Long-run research; not near-term. | not on its own |
| Whether cross-venue disagreement contains real information after rule/source/fallback normalization | WX-RESEARCH-06 open question | Cross-venue research direction. | unknown | Out-of-scope until contract-equivalence audit lands. | not on its own |
| Whether EVT-based methods survive honest out-of-era validation once provider revisions and station changes are fully tracked | BWX-RESEARCH-05Q open question | EVT-based research at Stage 5. | unclear | Long-run research. | not on its own |
| Whether market-aware probability adjustment produces calibrated improvement after market frictions and source risk | BWX-RESEARCH-05Q open question | Stage 5 research candidate. | unclear | Long-run research. | not on its own |
| Whether microstructure models create meaningful stand-alone signal beyond no-trade filtering | BWX-RESEARCH-05Q open question | Microstructure roadmap. | unknown | Long-run research. | not on its own |
| Whether revision/finality effects are large enough to justify a dedicated label-state model | BWX-RESEARCH-05Q open question | Stage 4 research candidate. | unclear | Per-family sensitivity study. | not on its own |
| Whether online weighting outperforms static combinations in sparse, nonstationary weather-market histories without destroying calibration | BWX-RESEARCH-05Q open question | Stage 3–4 research candidate. | unclear | Long-run research. | not on its own |
| Whether optimal-stopping / timing systems retain durable value after spreads, fees, and stale-quote risk | BWX-RESEARCH-05Q open question | Stage 5+ research candidate. | unknown | Long-run research. | not on its own |
| Whether tropical / severe occurrence markets can be brought above `avoid_for_now` without explicit authority-layer wording | This PRD synthesis | Family suitability gating. | unclear | Per-market venue-text census. | yes (for those families) |

---

## 30. Future ticket roadmap after PRD approval

The tickets below are **planning recommendations** for future Codex / human-authored implementation-planning tickets. **No ticket below is approved by this PRD.** Each ticket is gated by the §17 stage in its row. Tickets that target Stage 6 or Stage 7 work are explicitly **not approved** and are listed only to make the gating sequence visible.

| Future ticket | Purpose | Gated by | Approval status |
|---|---|---|---|
| PRD review / approval ticket | Review this PRD; freeze research packets at versions cited; approve Stage 0 status. | §17 Stage 0 | Not approved by this PRD. |
| Static example / manual label ticket | Build the canonical-event-mapping gold set and trap-labeled examples per §§6, 11. | §17 Stage 1 | Not approved by this PRD. |
| Canonical event schema planning ticket | Specify the schema for `canonical_event_id` and all load-bearing fields per §6. | §17 Stage 1 | Not approved by this PRD. |
| Source-compatible historical label planning ticket | Specify how first-posted, archive-quality, and post-analysis labels will be constructed per §§9, 18. | §17 Stage 2 | Not approved by this PRD. |
| Point-in-time archive design ticket | Specify the archive design that satisfies §§19–21 without live calls. | §17 Stage 2 | Not approved by this PRD. |
| Trap taxonomy static fixture planning ticket | Specify the test fixtures and trap-labeling protocols that satisfy §11 and §28. | §17 Stage 1 | Not approved by this PRD. |
| Probability scoring research-to-design ticket | Specify the scoring methodology per §22 and the method candidates per §16. | §17 Stage 3 (design) | Not approved by this PRD. |
| Paper simulation design ticket | Specify the executable-cost paper simulation per §23. | §17 Stage 4 (design) | Not approved by this PRD. |
| Human-review packet design ticket | Specify reviewer packets, override logs, Cohen's-kappa protocol per §24. | §17 Stage 5 (design) | Not approved by this PRD. |
| Provider connector planning ticket | (Only after Stages 1–5 of §17 are cleared and after a separate connector-approval gate is reached.) | §17 Stage 6 / connector approval | **Not approved by this PRD.** |
| Runtime observation planning ticket | (Only after a separate Stage 6 approval.) | §17 Stage 6 | **Not approved by this PRD.** |
| Execution / trading ticket | Never permitted without separate explicit approval. | §17 Stage 7 | **Not approved by this PRD.** |

---

## 31. Glossary / canonical terms

The glossary below is the canonical vocabulary of this PRD. Where a term is used elsewhere in the PRD it must mean exactly what is written here. None of these definitions approves implementation; they govern how the concepts are referred to in later planning, review, and (only after the §17 ladder is cleared) implementation-planning tickets.

| Term | Canonical definition (this PRD) |
|---|---|
| **Canonical weather event** | A normalized, source-defined event identity for a weather market, expressed by the full §6 field set (variable, location, station/source, window, threshold, comparator, unit, aggregation, revision rule, classification authority, resolver source, etc.). The canonical event is **not** the underlying physical weather; it is the venue-defined settlement object as represented in the event graph. |
| **Venue-defined settlement object** | The exact rule-defined object that determines whether a venue resolves a market `Yes` or `No`. It is composed of `resolver_source`, `station_or_source`, `measurement_window`, `threshold`, `comparator`, `unit`, `aggregation_method`, `revision_or_finality_rule`, `classification_authority`, and the venue's wording. Sections §§5–6 and §11 are bound to this concept. |
| **Resolver source** | The specific authority and product the venue cites (explicitly or implicitly) for settling the market — for example, an NWS/NCEI archive product, an ASOS station record, an SPC product, an NHC/HURDAT2 product, or a venue-discretionary determination. Per §9, the resolver source is the first-class object; provider data is **not** automatically resolver data. |
| **Official source** | A government / authoritative meteorological source whose product is, or could plausibly be, the resolver source: NOAA / NWS / NCEI / SPC / NHC and equivalent national-meteorological-agency products (e.g., ECCC, Met Office) where applicable. "Official" describes the **publisher class**; whether a given official product is the resolver for a given market is determined by the venue's wording, not by the provider's reputation. |
| **Convenience provider** | A non-resolver data source (commercial or otherwise) that may be useful for context, near-real-time observation snapshots, ensemble availability, or model output, but whose output **is not settlement truth**. Per §10, convenience-provider usefulness does not imply connector approval and does not promote the provider into a resolver role. |
| **Station / source compatibility** | The property that a candidate data product (a station record, a gridded product, a model output, an aggregator estimate, a forecast) refers to the **same** physical and rule-defined object the venue's resolver uses. Per §§8–9, station/source compatibility is a binary precondition for any historical label, probability estimate, or review packet to be treated as source-aligned; the absence of compatibility is itself a `blocking` trap (§11). |
| **Event graph** | The structured representation, per §6, that links canonical weather events to venue markets, resolver products, stations/sources, provider compatibility statuses, trap labels, uncertainty components, and validation stage. The event graph is the data structure the rest of the PRD reasons over. |
| **Market family** | A grouping of markets that share canonical-field structure and trap profile — e.g., temperature threshold, daily precipitation threshold, snowfall depth, wind / gust threshold, daily-city binary, weekly/monthly/seasonal aggregate, source-dependent, severe/extreme, tropical/hurricane, catastrophe-adjacent, and climate/anomaly families (§7). Family membership controls which §17 stage and which §11 traps apply by default. |
| **Trap** | A structural condition (per §11 and WX-RESEARCH-03) that would cause a naive mapping or model to misread the venue-defined settlement object. Traps carry a severity from the closed set `{caution, blocking}`. A `blocking` trap fails closed in any future review or readiness check. |
| **False edge** | An apparent probabilistic disagreement between a model/provider view and the market price that does **not** survive source-compatibility, trap, microstructure, and validation tests (§§11, 15, 23). False edges include source mismatches, station mismatches, gridded-vs-station mismatches, timezone errors, threshold/rounding mismatches, snowfall-vs-snow-depth confusion, stale data, illiquidity-driven mids, transaction-cost overhang, and venue-discretion exposure. |
| **Source mismatch** | A specific class of false edge / trap (§§11.3, 15) in which the data used to form a probability or label is not the venue's resolver source. Source mismatch includes wrong-station, wrong-product (e.g., gridded reanalysis instead of station archive), wrong-revision-state (e.g., post-revision archive used as first-posted), and wrong-authority (e.g., model report used where an official classification is required). |
| **Point-in-time provenance** | A property of a record asserting **exactly** which version of a source product, at which publication / availability timestamp, was used to construct it (§§18–19). Records without point-in-time provenance cannot be used in any honest label, probability score, paper simulation, or review packet, and are `blocking` under §11.7 and §17. |
| **No-lookahead leakage** | The principle (§20) that no record, label, feature, threshold, or model decision may rely on information that was not actually available at the relevant decision time — including future forecast cycles, future market prices, post-resolution labels before resolution, post-hoc station/source choices, revised archive values used as real-time truth, and any threshold or hyperparameter tuned on data the model would not have had. |
| **Forecast-run publication time** | The timestamp at which a specific forecast product / model cycle / advisory / observation update was actually made available to consumers (§21). All staged validation must treat data **as of** publication time, not nominal run time, and must separately track later archive revisions. |
| **Final archive leakage** | A particular no-lookahead violation (§§20–21) in which a final, post-revision archive value (e.g., a settled NCEI daily summary, a post-event Storm Data record, a finalized HURDAT2 best-track) is used to label or score a decision made before that value became available. Final archive leakage is `blocking`. |
| **Threshold bucket** | A discretized calibration partition (§22) over which Brier / log-loss / CRPS / reliability statistics are reported separately — for example, by market family, by distance to threshold, by forecast horizon, by source-compatibility band, by trap category, and (where supported) by season / regime. Threshold-bucket calibration is the unit of evidence for §17 Stage 3 reliability claims. |
| **Human-review packet** | The structured artifact (§24) presented to a reviewer at §17 Stage 5 (and earlier, in shadow form) containing the canonical event, venue wording, resolver/source/station/window interpretation, provider-compatibility status, trap flags, uncertainty decomposition, alpha hypothesis (if any), false-edge risks, validation stage, readiness state, blocked/caution rationale, unresolved questions, and explicit non-approval boundaries. |
| **Fail-closed** | The default behavior (§26) in which missing, ambiguous, or unverifiable information produces a non-actionable readiness state (per the §25.2 closed set, e.g., `missing`, `unapproved`, or `invalid`, with summary severity `blocked` and review posture `blocked`) rather than a permissive one. Fail-closed applies to config/secrets readiness, trap severity, source compatibility, provenance, and microstructure cost uncertainty. |
| **Runtime observation** | The hypothetical future posture (§17 Stage 6) in which the system passively records its own readiness, status, and (where authorized) source-availability signals against live timestamps — **without** trading, order placement, position sizing, or execution. Runtime observation is **not approved** by this PRD. |
| **Paper simulation** | The §17 Stage 4 posture in which trap-filtered, source-compatible historical samples are replayed under a fully specified microstructure cost model (§23) with executable quotes, fees, spreads, depth, and slippage assumptions — **without** any live execution. Paper simulation is `not approved` as an implementation step by this PRD; only its **design** is in scope after Stages 1–3 are cleared. |
| **Execution approval** | A separate, explicit, future approval (§17 Stage 7) — outside the scope of this PRD — that would be required to permit any form of live order placement, trading, or autonomous market action. Execution approval is **never** implied by passage of earlier stages. |

---

## 32. Appendices

The appendices below are condensed reference views over the PRD body. They are **not** authoritative — the body sections (§§1–31) control. The appendices exist to make the §17 evidence ladder, §11 trap taxonomy, §6 event graph, and §29 open-question register easier to navigate in later planning tickets. **No appendix below approves implementation.**

### Appendix A — Market family table (condensed from §7)

| Family | Resolves on | Typical resolver class | Dominant traps | Posture |
|---|---|---|---|---|
| Temperature threshold | Daily/period extreme vs threshold at a named station/source | NWS/NCEI station archive (ASOS-class) | Local-day, station selection, revision | early_candidate |
| Daily precipitation threshold | Calendar-day precipitation total at a named station vs threshold | NWS/NCEI daily archive | Local-day window, trace handling, station/grid mismatch | early_candidate |
| Snowfall (vs snow-depth) | New snowfall over a window at a named station | NWS/NCEI snowfall product | Snowfall-vs-depth confusion, observer cadence, revision | later_candidate |
| Wind / gust threshold | Peak gust / sustained wind at a named station | NWS/NCEI station archive | Sustained-vs-gust, averaging interval, station exposure | later_candidate |
| Storm / hurricane (tropical) | Named storm formation, landfall, intensity, basin presence | NHC advisories / HURDAT2 best-track | Advisory-vs-best-track, definition timing, basin boundaries, revision | later_candidate (often `avoid_for_now` until authority layer is explicit) |
| Severe / extreme (tornado, hail, severe wind) | Occurrence/classification of a severe event in a region | SPC products / Storm Data | Authority layer (LSR vs Storm Data), classification, geography | avoid_for_now until authority is explicit |
| Daily city / location binary | Yes/No condition on a named city/location for a calendar day | Station-class product implied by venue | "City" = which station / gridpoint? local-day boundary | early_candidate where station is named, else later_candidate |
| Weekly / monthly / seasonal aggregate | Aggregate over an extended window | Archive product (NCEI monthly summary, etc.) | Aggregation rule, missing-day handling, revision/finality | later_candidate |
| Source-dependent | Venue explicitly names a non-government index, provider, or proprietary number | Whatever the venue cites | Source availability, redistribution, revision | later_candidate where the named source is auditable; `avoid_for_now` otherwise |
| Catastrophe / disaster-adjacent | Resolution depends on insurance/catastrophe-industry classification | Industry index/authority | Industry-classification timing, revision, scope | avoid_for_now |
| Climate / anomaly | Resolution depends on anomaly/percentile/climate-index product | NCEI/CPC/equivalent climate product | Period of record, anomaly base, revision | later_candidate |

### Appendix B — Trap taxonomy table (condensed from §11; severities from WX-RESEARCH-03 are controlling)

| Trap family | Example | Severity (closed set) | Default treatment |
|---|---|---|---|
| Market wording | Ambiguous threshold/comparator/aggregation language | caution or blocking | caution if explicit and reviewer-confirmable; blocking otherwise |
| Resolution-source | No clear resolver / discretionary venue determination | blocking | blocking |
| Provider / source compatibility | Provider product is not source-compatible with the resolver | blocking | blocking |
| Station / location | Wrong station, wrong gridpoint, "city" with no named station | blocking | blocking until station/source mapping is explicit |
| Time-window / timezone | Local-day vs UTC, end-of-day boundary, overlap with revision | caution or blocking | blocking when local-day boundary is unresolved |
| Threshold / unit / comparator | Unit mismatch, rounding ambiguity, strict-vs-inclusive comparator | caution or blocking | blocking when comparator or unit is ambiguous |
| Measurement method | Sustained-vs-gust, snowfall-vs-snow-depth, trace handling | caution or blocking | blocking on snowfall-vs-snow-depth confusion; caution elsewhere if reviewer-confirmable |
| Data revision / finality | First-posted vs revised vs final archive used incorrectly | blocking | blocking |
| Venue discretion | Venue reserves right to make non-deterministic determinations | blocking | blocking |
| Classification authority | Severe-event / tropical-event authority is unclear | blocking | blocking |
| Cancellation / invalidation | Conditions under which the market is voided | caution | caution; surfaced in review packet |
| False-equivalence | Two markets look identical but settle on different sources | blocking | blocking |

### Appendix C — Source / provider type table (condensed from §§8, 10)

| Class | Examples (illustrative, not connector approval) | Resolver role? | Convenience role? | Connector approval implied? |
|---|---|---|---|---|
| Official resolver / government archive | NOAA / NWS / NCEI products; SPC; NHC / HURDAT2; ECCC; Met Office | Yes, where venue cites them | Yes, with caveats | **No** |
| Official station observation | ASOS / AWOS station records via NWS / NCEI | Yes, where venue cites the station | Yes | **No** |
| Climate archive | NCEI climate / anomaly products; CPC products | Yes, where venue cites them | Yes | **No** |
| Forecast / model provider | GFS, GEFS, ECMWF, HRRR, LAMP, NDFD (publication-time governed) | No (forecasts do not resolve) | Yes, with timing controls | **No** |
| Historical-data provider | Meteostat, Meteomatics (historical layers), Open-Meteo (archive layers) | Only where independently verifiable as the venue's archive | Yes, with caveats | **No** |
| Convenience / aggregator API | Visual Crossing, Weatherbit, Tomorrow.io, OpenWeather, WeatherAPI.com | Generally no | Sometimes, with strong caveats | **No** |
| Gridded / interpolated product | Reanalysis grids, interpolated estimates | Generally no | Context only | **No** |
| Venue-selected discretionary resolver | Whatever a venue names per market | Yes, per venue | n/a | **No** |

### Appendix D — Uncertainty decomposition table (condensed from §§12–13)

| Uncertainty component | What it captures | Cannot be collapsed into "forecast uncertainty" because |
|---|---|---|
| Forecast uncertainty | Predictive uncertainty over the physical variable | Baseline |
| Observation uncertainty | Sensor / instrument noise at the station/source | Independent of forecast skill |
| Resolver / source uncertainty | Which authority/product actually settles the market | Structural, not stochastic |
| Station / location uncertainty | Whether the chosen station/source matches the venue's resolver | Source-compatibility issue |
| Time-window uncertainty | Local-day vs UTC, window boundary handling | Definitional |
| Threshold / comparator uncertainty | Strict vs inclusive, rounding, units | Rule semantics |
| Rounding / unit uncertainty | How the venue rounds and to which precision | Rule semantics |
| Revision / finality uncertainty | First-posted vs revised vs final | Label-state, not predictive |
| Classification authority uncertainty | Which authority's classification counts | Structural |
| Market mapping uncertainty | Whether the canonical event correctly represents the market | Modeler-side risk |
| Provider compatibility uncertainty | Whether available providers match the resolver | Source-class issue |
| Market microstructure uncertainty | Spreads, depth, fees, slippage, stale quotes | Cost / executability, not physics |
| Model uncertainty | Disagreement among modeling choices and ensembles | Methodological |

### Appendix E — Alpha hypothesis table (condensed from §14; all entries are research hypotheses only)

| Hypothesis cluster | Sub-hypotheses | Validation requirement (§17 stage) | Approval status |
|---|---|---|---|
| Source / station / timing | Resolution-source mismatch; station/location precision; forecast-update timing; observation-release lag; nowcasting; radar/satellite signal | Stage 2–3 (label + scoring), then Stage 4 (cost-aware) | Research hypothesis only; not approved |
| Uncertainty / threshold / belief | Ensemble dispersion; threshold proximity; tails / extreme-event; seasonality / climatology mispricing | Stage 3 (scoring), then Stage 4 (cost-aware) | Research hypothesis only; not approved |
| Microstructure / network | Stale market price; liquidity / spread-aware; correlated market structure; cross-source disagreement; cross-venue disagreement (if supported) | Stage 4 (cost-aware) at minimum; Stage 5 review for any actionable form | Research hypothesis only; not approved |

### Appendix F — Quant method roadmap table (condensed from §16; suitability per BWX-RESEARCH-05Q is controlling)

| Method family | Earliest stage where research is justified | Approved here? |
|---|---|---|
| Baseline climatology / persistence | Stage 1–2 | Research only; not approved |
| Simple calibrated threshold models | Stage 2–3 | Research only; not approved |
| Ensemble / post-processing methods | Stage 3 | Research only; not approved |
| Bayesian and hierarchical methods | Stage 3–4 | Research only; not approved |
| Quantile / distributional regression | Stage 3–4 | Research only; not approved |
| Spatial-temporal methods | Stage 4 | Research only; not approved |
| EVT / tail methods | Stage 4–5 | Research only; not approved |
| Precipitation mixture models | Stage 3–4 | Research only; not approved |
| Calibration / scoring methods | Stage 3 (transverse) | Research only; not approved |
| Market-aware probabilistic filters | Stage 4–5 | Research only; not approved |
| Conformal / distribution-free | Defer until coverage under source-defined labels is studied | Research only; not approved |

### Appendix G — Validation evidence ladder table (condensed from §17; this is the safety backbone)

| Stage | Posture | What is allowed | What remains prohibited | Required artifacts to advance |
|---|---|---|---|---|
| 0 | Documentation / research only | This PRD; cited research packets | All implementation; all live calls | PRD approval |
| 1 | Static examples / manual labels | Canonical-event gold sets; trap-labeled fixtures | Any live data | Reviewer-signed gold set; trap fixtures |
| 2 | Source-compatible historical labels | First-posted / archive-quality labels with point-in-time provenance | Live calls; tuned thresholds on test data | Labeled dataset with provenance; strict OOS splits defined |
| 3 | Retrospective probability scoring | Probability scoring on strict OOS splits with Brier / log / CRPS / reliability by §22 buckets | Cost-aware simulation; any live execution | Calibration report passing pre-edge gate |
| 4 | Trap-filtered paper simulation | Cost-aware simulation per §23 with executable quotes, fees, spreads, depth | Live execution; runtime observation | Cost-aware simulation report with required ablations |
| 5 | Human-reviewed dry run | Reviewer packets per §24 with adjudication, override logs, Cohen's-kappa protocol | Live execution; runtime observation | Reviewer-signed dry-run report |
| 6 | Runtime observation only under separate approval | (Hypothetical) passive timestamping of readiness/status | **Trading; order placement; sizing; execution** | **Separate approval — not granted by this PRD** |
| 7 | Execution / trading only after separate explicit approval | (Hypothetical) live execution under explicit authorization | n/a | **Separate explicit approval — not granted by this PRD** |

### Appendix H — Future reading / research map (where attached materials support pointers)

| Topic | Attached source(s) | Use |
|---|---|---|
| Event / source ontology | WX-RESEARCH-01 | Controlling for §§5–7 |
| Provider / source compatibility | WX-RESEARCH-02 | Controlling for §§8–10, Appendix C |
| Trap taxonomy and severities | WX-RESEARCH-03 | Controlling for §11, Appendix B |
| Probability framing | WX-RESEARCH-04 | Controlling for §§12–13, §25, Appendix D |
| Alpha hypotheses and false edges | BWX-RESEARCH-05A | Controlling for §§14–15, Appendix E |
| Quantitative method suitability | BWX-RESEARCH-05Q | Controlling for §16, Appendix F |
| Backtesting / validation | WX-RESEARCH-06 | Controlling for §§17–23, §28, Appendix G |
| MEG fit and phase posture | MEG master PRD (v4.1, patched) | Controlling for §§1–4, §27 |

Topics not covered by attached materials are marked `unknown` in §29 and elsewhere, and are recommended future research questions, not gaps in this PRD's scope.

### Appendix I — Open-question register (cross-reference to §29)

| Register class | Sources of entries | Where the entries live |
|---|---|---|
| Resolver-product / archive-layer ambiguities | WX-RESEARCH-02 open questions | §29 rows 1–4, 7–9 |
| Connector-terms / commercial / SLA ambiguities | WX-RESEARCH-02 open questions | §29 rows 5–6, 8 |
| Archive / order-book / publication-timestamp availability | WX-RESEARCH-06 open questions | §29 rows 10–13 |
| Rare-family sample-sufficiency | WX-RESEARCH-06 open questions | §29 row 14 |
| Method-suitability questions | BWX-RESEARCH-05Q open questions | §29 rows 15–22 |
| Family-suitability gating | This PRD synthesis | §29 row 23 |

The register is a planning surface, not an approval surface. Each row is gated by a §17 stage or by a separate connector-approval gate per §§8, 10, and 27; none of those gates is granted by this PRD.

---

### Appendix J — Reconciliation notes (PRD draft → reconciled PRD against PRD-P1-WX-KICKOFF and PRD-P1-WX-01 through PRD-P1-WX-04)

This appendix records every change made when reconciling the originally drafted MEG Weather Bot PRD against PRD-P1-WX-KICKOFF, PRD-P1-WX-01, PRD-P1-WX-02, PRD-P1-WX-03, and PRD-P1-WX-04. The reconciliation pass was targeted and narrow: it preserved this PRD's core structure and research synthesis from WX-RESEARCH-01 through WX-RESEARCH-06 and BWX-RESEARCH-05A/05Q, and changed only what was needed to align machine-checkable closed-set vocabularies, eliminate hybrid/custom field values, and reframe a supersession claim that the reconciliation did not support.

The non-approval posture is unchanged. No connector implementation, no external API calls, no config loading, no secret reading, no runtime execution, no forecast pulls, no data ingestion, no trading, no order placement, no autonomy, and no profitability claim is approved by this document. WX-RESEARCH-06's seven-stage evidence ladder (§17) remains the safety backbone of the PRD; no section weakens it; the PRD remains a Stage 0 artifact.

#### J.1 What was changed

| # | Location | Change | Why |
|---|---|---|---|
| 1 | Document header (`Supersedes:` line) | Replaced the `Supersedes:` line with a `Reconciled against:` line listing PRD-P1-WX-UNBLOCK, PRD-P1-WX-KICKOFF, and PRD-P1-WX-01 through PRD-P1-WX-04. The new line explicitly states this PRD does **not** supersede the WX planning documents and that WX-03 / WX-04 govern on shared closed-set vocabularies. | The original supersession claim was inverted by the reconciliation: this PRD aligned **to** the WX closed sets, not the other way around. Per the reconciliation directive, the `Supersedes` line was not retained because reconciliation did not confirm a supersession relationship. |
| 2 | §11.12 Fail-closed rule | Replaced the machine-checkable downgrade value `caution_pass` with `reviewed_caution`, drawn from the existing §6.1 `human_review_state` closed set (`unreviewed`, `caution_under_review`, `blocking_under_review`, `reviewed_pass`, `reviewed_caution`, `reviewed_block`). Added an explicit sentence that the `human_review_state` closed set is the only allowed mechanism for recording reviewer adjudication outcomes. | `caution_pass` was an invented value used in a machine-checkable position. The PRD already declares the `human_review_state` closed set in §6.1 and `reviewed_caution` is the correctly scoped value for the concept. |
| 3 | §16.2 EVT / GEV / POT row | Replaced the compound suitability value `advanced_candidate (Stage 5); defer for early use` with the single value `advanced_candidate`, and moved the "Stage 5; defer for early use" qualifier into the Limitations column. | Compound suitability values are hybrid machine-checkable values. The cleanest fix preserves the staged-eligibility nuance in prose without using a compound token. |
| 4 | §16.2 Conformal prediction row | Replaced `defer (abstention only)` with `defer`. Moved the "abstention only" scope into the Possible future use column. | Same as #3. |
| 5 | §16.2 Market-aware probability adjustment row | Replaced `advanced_candidate (caution)` with `advanced_candidate`. Moved the elevated-caution language into the Limitations column. | This was the specific hybrid pattern called out in the reconciliation directive. The caution is preserved in prose, not in the closed-set value. |
| 6 | §16.2 Source uncertainty adjustment row | Replaced `defer (bespoke research layer)` with `defer`. Moved the "bespoke research layer" qualifier into the Possible future use column. | Same as #3. |
| 7 | §25 (Observability / status / result summary requirements) intro | Updated the controlling-source paragraph to state that PRD-P1-WX-04 controls the closed-set vocabulary used in this section (because WX-04 is in fact available in the workspace, contrary to the original draft's footnote), and that PRD-P1-WX-03 controls config/secrets readiness. WX-RESEARCH-03 continues to control trap severity and WX-RESEARCH-06 continues to control human-review/safety constraints. | The original draft assumed WX-04's exact wording was not available and used principles-derived values. With WX-04 available, alignment is required. |
| 8 | §25.2 Readiness states | Replaced the previous closed set `{not_ready, research_only, ready_for_review, reviewed_caution, reviewed_block, pending_finalization}` with the WX-03 §4 / WX-04 §5 closed set `{missing, disabled, unapproved, invalid, ready}`. Added explicit pointers showing where the original semantic concepts now live: per-market reviewer-workflow state in §6.1 `human_review_state`; per-market evidence stage in §17's stage tag (and §24.1's `validation_stage` field); awaiting-archive-finalization in `archive_layer` / `revision_treatment` (per §6.1, §9.6). Reproduced the WX-03 / WX-04 forbidden-values list. | This was the central closed-set conflict between the PRD draft and the WX-03 / WX-04 contract. WX-03 / WX-04 govern. The PRD's richer semantic concepts are preserved by being moved to PRD-defined fields where they were already represented, rather than being eliminated. |
| 9 | §25.3 Summary severity | Kept the existing closed set `{info, caution, blocked}` (which already matched WX-04 §5) but rewrote the meaning column in WX-04's language and added an explicit forbidden-values list. | Cosmetic alignment; no semantic change. |
| 10 | §25.4 Review posture | Replaced the previous closed set `{no_review_needed, human_review_pending, human_review_complete, human_override}` with the WX-04 §5 closed set `{informational, review_only, blocked}`. Added an explicit pointer that per-market reviewer-workflow detail is **not** carried in the WX-04 review-posture field; it lives in `human_review_state`, `manual_override_flag`, and override-log records (§24.3). | This was the second central closed-set conflict between the PRD draft and the WX-04 contract. WX-04 governs. As with #8, the original concepts are preserved by being moved to fields where they were already represented. |
| 11 | §29 row 14 (rare-family sample sufficiency) | Replaced the invented value `later_validation` in the prose with `defer` only, preserving the same intent (the family may remain `defer` until sample-size evidence accumulates). | `later_validation` is not declared as a closed-set value in this PRD or in any of the WX planning documents. `defer` is consistent with §16's BWX-05Q-derived maturity vocabulary. |
| 12 | §31 Glossary, `Fail-closed` row | Replaced the example readiness-state value `not_ready` with the §25.2-aligned examples `missing`, `unapproved`, or `invalid`, accompanied by summary severity `blocked` and review posture `blocked`. | After #8, `not_ready` is forbidden as a readiness-state value. The example now uses values that are allowed. |

#### J.2 What was not changed

| Element | Why it was preserved |
|---|---|
| Core structure of the PRD (§§1–32) and all section numbering | The reconciliation directive required preservation of the PRD's core structure and research synthesis. |
| WX-RESEARCH-06's seven-stage evidence ladder in §17 | Explicitly identified as the safety backbone of the PRD; reconciliation must not weaken it. |
| All canonical-event field definitions in §6.1 and their inline closed sets (`geographic_precision`, `archive_layer`, `trace_rule`, `timezone`, `freeze_rule`, `human_review_state`, `source_compatibility_status`) | These are PRD-internal closed sets that do not conflict with WX-03 / WX-04 and are load-bearing for the rest of the PRD. |
| Confidence-value closed set `{confirmed, unclear, unknown}` (line 39 and throughout) | Explicitly declared by the PRD as a PRD-level closed set; no WX document overrides it. `unknown` is forbidden specifically as a *readiness-state* value (§25.2) but remains valid as a *confidence* value. |
| Trap-severity closed set `{caution, blocking}` (line 39 and throughout) | Explicitly declared by the PRD as a PRD-level closed set; reinforced by WX-RESEARCH-03. |
| Family-suitability labels in §7 (`early_candidate`, `later_candidate`, `avoid_for_now`) | PRD-defined and used consistently as a closed set; no WX document defines an alternative. |
| All §16.2 single-token maturity labels (`baseline_candidate`, `advanced_candidate`, `defer`, `research_candidate`) | Preserved from BWX-RESEARCH-05Q. Only the hybrid parenthetical annotations were removed (see #3–#6 above). |
| §8.3 provider/source candidate matrix (drawn from WX-RESEARCH-02) | The matrix is consistent with WX-RESEARCH-02. No closed-set conflict with WX-03 / WX-04. |
| §17.2 PRD-level Stage 0 posture and the §17.3 mandatory backbone statement | Required by the reconciliation directive and by the WX-RESEARCH-06 evidence ladder. |
| §4 non-goal / non-approval list and the §1–§32 global non-approval banner | Required by the reconciliation directive and consistent with WX-KICKOFF §§4, 11; WX-01 §9; WX-02 (planning posture); WX-03 §13; WX-04 §13. |
| Field-level use of `pending_finalization` in §9.6 and §11.2 (as a state of `archive_layer`, not a top-level readiness-state value) | Per the §25.2 rewrite, this is a per-field intermediate marker and is not equivalent to a top-level readiness-state value. WX-03 / WX-04 do not regulate field-level markers of this kind. |

#### J.3 Cross-document alignment summary

| Closed-set vocabulary | Controlling document | Allowed values | Where used in this PRD |
|---|---|---|---|
| Trap severity | WX-RESEARCH-03; PRD §11 reaffirms | `caution`, `blocking` | §§11, 15, 24, 26; throughout |
| Confidence | This PRD (§ global banner) | `confirmed`, `unclear`, `unknown` | §§8.3, 14, 15, 16, 18, 22, 29; throughout |
| Family suitability | This PRD (§7) | `early_candidate`, `later_candidate`, `avoid_for_now` | §7, Appendix A |
| Method maturity (research-only) | BWX-RESEARCH-05Q; PRD §16 preserves | `baseline_candidate`, `advanced_candidate`, `defer`, `research_candidate` | §16.2, §29 |
| Config/secrets readiness state | PRD-P1-WX-03 §4 | `missing`, `disabled`, `unapproved`, `invalid`, `ready` | §25.2 (status/result summary); §26 risk gates discuss in prose |
| Summary/status readiness state | PRD-P1-WX-04 §5 | `missing`, `disabled`, `unapproved`, `invalid`, `ready` | §25.2 |
| Summary severity | PRD-P1-WX-04 §5 | `info`, `caution`, `blocked` | §25.3 |
| Review posture | PRD-P1-WX-04 §5 | `informational`, `review_only`, `blocked` | §25.4 |
| Reviewer workflow state (per-market) | This PRD §6.1 | `unreviewed`, `caution_under_review`, `blocking_under_review`, `reviewed_pass`, `reviewed_caution`, `reviewed_block` | §§6.1, 11.12, 24, 25.2, 25.4 |
| Equivalence class (between markets) | This PRD §6.2 | `Exact-equivalent`, `Near-equivalent`, `Related but non-equivalent`, `Incompatible` | §6.2 |

#### J.4 Reconciliation posture restated

This PRD remains a Stage 0 artifact under §17 and a planning artifact under PRD-P1-WX-KICKOFF §10–§11. Nothing in this reconciliation pass approves anything that the PRD draft did not approve, and the reconciliation has not lifted any of the WX-KICKOFF, WX-01, WX-02, WX-03, or WX-04 non-approvals. The reconciliation is descriptive of how this PRD's closed-set vocabulary is now aligned with the WX planning contracts; it does not move any approval gate.

---

**End of MEG Weather Bot PRD.**

**Frozen at §17 Stage 0 — documentation and source-backed research only. No implementation is approved by this document. No connector, no live call, no forecast pull, no runtime, no order placement, no trading, and no autonomy is approved by this document. All advances beyond Stage 0 require the artifacts and gates specified in §17, and Stages 6–7 require separate explicit approvals that are not granted here.**
