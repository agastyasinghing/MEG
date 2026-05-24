# PRD-P1-WX-02: Weather Data Provider Research and Connector Approval Gate

## 1. Status and scope
- Status: Phase 1 weather provider research ticket.
- Scope: provider research and connector approval gate planning only.
- This document does **not** approve connector implementation.
- This document does **not** approve live external API calls, credentials, runtime execution, forecast pulls, forecast modeling, probability modeling, trading, order placement, or autonomy.
- This document prepares decision criteria for a later connector approval ticket.

## 2. Strategic framing
PRD-P1-WX-02 follows **PRD-P1-WX-01** and continues the weather bot as MEG’s canonical event graph proving ground.

Provider selection is evaluated against this chain:
- real-world weather event
- → canonical weather event identity
- → venue-specific market mapping
- → resolution-rule compatibility
- → resolution-risk classification
- → human-review output
- → later connector approval decision

Why this matters: a generic “best weather API” comparison is insufficient for prediction-market resolution, where source authority, station semantics, time-window definitions, and revision behavior can dominate correctness risk.

## 3. Source and citation standard
- All provider-specific claims must be backed by source notes.
- Preferred sources:
  - official provider docs
  - official provider API docs
  - official provider pricing pages
  - official government/weather-source docs
  - official resolution-source docs
- Each provider claim must include:
  - source URL or source name
  - access date
  - claim confidence status: **confirmed**, **unclear**, or **unknown**
- Uncited claims about pricing, rate limits, historical availability, station granularity, forecast horizon coverage, terms of use, and official-source alignment are not acceptable.
- If sources are ambiguous, claims must be marked **unclear** or **unknown**.

## 4. Provider evaluation dimensions
Provider evaluation for MEG weather markets should include:
- resolution-rule compatibility
- data source transparency
- official-source alignment
- station/observation granularity
- historical data availability
- forecast horizon coverage
- timestamp and timezone semantics
- unit support and unit conversion risk
- location query semantics
- precipitation/snowfall/wind/temperature support
- storm/hurricane/extreme weather support
- API documentation quality
- pricing and free-tier constraints
- rate limits
- latency/update cadence
- data retention and auditability
- terms-of-use concerns
- reliability/failure modes
- suitability for human-review explanations

## 5. Provider candidate matrix

| Provider | Likely data strengths | Likely market-resolution strengths | Likely weaknesses | Transparency posture | Historical support posture | Forecast support posture | Cost/rate-limit posture | Terms-of-use posture | Connector readiness status | Candidate decision | Access date | Confidence |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| NOAA / NWS (`api.weather.gov`) | Official U.S. government weather endpoints, public documentation | Strong for markets resolved against NWS/NOAA source authority | Some endpoint changes/deprecations and product-specific boundaries may require tight rule mapping | Confirmed public standards docs; official authority | Observation/forecast products documented; full historical depth for all market needs not fully unified in one endpoint (**unclear**) | Forecast products present | Public API; pricing not presented as commercial tiers (**confirmed** for public API posture) | Government service terms/policies need explicit connector legal review | Research-ready, not connector-approved | Candidate for source-dependent U.S. markets | 2026-05-24 | confirmed/unclear mix |
| Open-Meteo | Forecast + historical weather + historical forecast APIs documented | Strong for comparative model-based workflows and transparent model references | Direct official-station authority for market resolution may be indirect depending on market rules | Model/source references documented | Historical Weather + Historical Forecast documented | Forecast API coverage documented | Public pricing page with free/commercial tiers and key-based customer endpoint | Commercial terms require later legal review | Research-ready, not connector-approved | Candidate for model-centric and non-authority-dependent markets | 2026-05-24 | confirmed |
| Visual Crossing | Single endpoint framing for historical/current/forecast; broad variable coverage | Useful for operational simplicity and multi-horizon pulls | Resolution-source authority alignment may be unclear for strict official-source markets | Source blending described; exact source-of-record governance per market may be unclear | Historical support advertised | Forecast support advertised | Pricing pages available, plan details present | Terms and redistribution constraints need legal review | Research-ready, not connector-approved | Hold for further resolution-source review | 2026-05-24 | confirmed/unclear mix |
| Tomorrow.io | Platform/API docs with forecast + historical timeline guidance | Structured timeline access may help explicit windowed market checks | Historical depth differs by plan and may require premium/archive request | Public docs exist; proprietary blends may need more explicit source mapping | Historical tiers documented (including archive by request) | Forecast ranges depend on plan tier | Pricing posture primarily plan/sales mediated | Terms/licensing review required | Research-ready, not connector-approved | Candidate pending commercial + source-alignment review | 2026-05-24 | confirmed/unclear mix |
| Meteomatics | Broad global model + observation integration; historical/current/forecast documented | Rich parameter/time/location query power may help edge-case markets | Cost/rate specifics mostly sales-led; source-of-record traceability per field may need deeper verification | Documentation and source categories described | Historical coverage advertised (including long horizon claims) | Forecast and extended products documented | Pricing mainly contact-sales | Contract/legal review required | Research-ready, not connector-approved | Hold for further cost/traceability review | 2026-05-24 | confirmed/unclear mix |
| OpenWeather | Mature API ecosystem with forecast/current/historical product families | Widely used; may support broad market families | Resolution authority compatibility for official-source markets requires explicit mapping; some capabilities plan-tiered | Public documentation exists | Historical products exist but plan/path specifics must be documented per endpoint | Forecast support documented | Pricing/tiering published; endpoint limits are plan-specific | Terms/licensing review required | Research-ready, not connector-approved | Candidate for non-authority-dependent markets, pending rule fit | 2026-05-24 | confirmed/unclear mix |
| WeatherAPI.com | Clear docs and pricing table with explicit historical/forecast horizon differences by plan | Useful for explicit plan-gated horizon planning in market definitions | Commercial plan constraints can create hidden resolution risk if not pinned | Documentation and pricing publicly explicit | Historical range clearly tiered in pricing table | Forecast range clearly tiered in pricing table | Transparent plan matrix shown publicly | Terms/licensing review required | Research-ready, not connector-approved | Candidate for scoped markets where plan constraints are acceptable | 2026-05-24 | confirmed |
| Meteostat | Station-oriented historical endpoints with explicit update-delay caveats | Strong for station-based historical analyses and auditability narratives | API access path and latency caveats may limit near-real-time needs | Docs explicitly describe station endpoints and delays | Historical hourly station data documented | Forecast posture not a primary documented strength in reviewed sources (**unclear**) | Rate/plan posture tied to provider channel; full terms need follow-up | Terms/use via delivery channel requires review | Research-ready, not connector-approved | Candidate for historical/station validation layer | 2026-05-24 | confirmed/unclear mix |
| Weatherbit | Broad weather coverage with historical/forecast endpoints and pricing matrix | Good variable breadth including precip/snow/wind fields | Free/commercial boundaries and historical quotas can affect resolution workflows | Source blend disclosures present in docs | Historical endpoints and horizons documented | Forecast products documented | Pricing and request quotas published | Terms/licensing review required | Research-ready, not connector-approved | Candidate pending quota/rate fit analysis | 2026-05-24 | confirmed |
| AccuWeather | Enterprise-grade API docs and pricing entry points available | Potentially strong for reliability/coverage in commercial settings | Publicly detailed rate/pricing/source traceability may require sales/enterprise docs | Public developer docs available | Historical availability specifics in public docs are limited (**unclear**) | Forecast products documented | Pricing page exists; detailed commercial terms often sales-mediated | Contract/legal review required | Research-ready, not connector-approved | Hold for further public-detail sufficiency review | 2026-05-24 | confirmed/unclear mix |

## 6. Resolution-rule compatibility analysis
Key compatibility observations (provider-specific claims source-backed or marked unclear/unknown):
- **Official station compatibility**: NWS/NOAA official endpoints are high-value when markets explicitly resolve to NWS/NOAA publications (**confirmed**). For blended commercial providers, official-source traceability can be **unclear** without field-level provenance mapping.
- **City vs station ambiguity**: providers with explicit station IDs (for example Meteostat/Weatherbit station-oriented docs) are easier to map to station-resolved markets (**confirmed**), while city-level abstractions can introduce ambiguity (**confirmed general risk; provider-specific severity often unclear**).
- **NWS/NOAA alignment**: for U.S. source-dependent markets, explicit NWS/NOAA source-aligned paths should be preferred (**confirmed strategic requirement**).
- **Historical observations vs forecasts**: several providers separate historical observations, historical forecasts, and forecast products (Open-Meteo, Tomorrow.io, Weatherbit) (**confirmed**); market resolution must specify which class is authoritative.
- **Daily high/low definitions**: aggregation-window and timezone definitions differ by provider docs and query semantics (**confirmed general risk; per-provider defaults often unclear unless endpoint-specific docs are pinned**).
- **Precipitation/snowfall accumulation windows**: accumulation interval conventions can differ; connector approval should require explicit window and unit mapping test vectors (**confirmed as required gate practice**).
- **Wind gust vs sustained wind**: variable naming may differ across APIs and markets; compatibility must be validated per market family (**confirmed general risk**).
- **Storm/hurricane markets**: source authority may need official agency references (e.g., NHC/NWS) depending on market rules; commercial blended feeds may be insufficient without authority mapping (**confirmed strategic caution**).
- **Timezone and observation window mismatch**: all providers require explicit timezone-window normalization to avoid day-boundary errors (**confirmed risk**).
- **Delayed reporting and revision risk**: Meteostat explicitly documents that some hourly data may arrive later; similar revision risks should be assumed and tested elsewhere unless docs state otherwise (**confirmed for Meteostat; unclear for others without explicit revision notes**).

## 7. Provider-to-market-family fit
- **Temperature threshold markets**: prioritize station traceability, daily max/min definition clarity, timezone semantics.
- **Precipitation threshold markets**: prioritize accumulation-window definition, unit semantics, and source authority.
- **Snowfall markets**: prioritize snowfall variable definition (depth/estimate), station coverage, and revision handling.
- **Wind markets**: prioritize gust vs sustained field clarity and timestamp granularity.
- **Storm/hurricane markets**: prioritize official-source alignment and named-event authority.
- **Extreme weather markets**: prioritize authoritative source citation and edge-case revision handling.
- **Daily city/location binary markets**: prioritize location geocoding semantics and station-vs-city disambiguation.
- **Monthly/seasonal aggregate markets**: prioritize historical consistency, revision policy, and aggregation reproducibility.
- **Source-dependent resolution markets**: prioritize source-of-record compatibility above generic forecast quality.

Provider family fit guidance (high-level):
- NOAA/NWS is a primary fit when resolution language references U.S. official sources (**confirmed**).
- Meteostat can be a strong auxiliary for station-centric historical validation (**confirmed**).
- Open-Meteo, WeatherAPI.com, Weatherbit, Tomorrow.io, Visual Crossing, OpenWeather, Meteomatics, and AccuWeather remain conditional on explicit resolution-source and terms compatibility checks (**confirmed/unclear mix**).

## 8. Connector approval gate
Before any connector implementation ticket is approved, all must be satisfied:
1. Explicit user approval for connector implementation.
2. Approved provider shortlist.
3. Source-backed provider evaluation (with URLs/source names, access date, confidence tags).
4. Approved credential/secrets handling plan.
5. Approved fail-closed config behavior (handoff: **PRD-P1-WX-03**).
6. Approved no-network-test strategy.
7. Approved synthetic fixtures.
8. Approved observability/status contract (handoff: **PRD-P1-WX-04**).
9. Documented provider terms-of-use review.
10. Documented resolution-source compatibility for targeted market families.
11. Documented human-review output integration.
12. Explicit non-approval of trading, order placement, and autonomy.

## 9. Recommended provider path (research guidance only)
This section is **research guidance only** and is not implementation approval.

- **Primary candidate for later connector-approval review**: NOAA/NWS for U.S. source-dependent resolution markets, due to official-source alignment.
- **Secondary candidate set**: Open-Meteo and WeatherAPI.com for transparent documentation and explicit historical/forecast framing, subject to rule-specific compatibility checks.
- **Defer/hold for further research**: AccuWeather, Meteomatics, Visual Crossing, Tomorrow.io, OpenWeather, Weatherbit, Meteostat (where terms, source-of-record mapping, or public rate/plan detail remains insufficient for immediate connector approval).
- **Unknowns requiring further review**: provider-specific legal redistribution terms, revision policies, and per-field source provenance maps for each targeted market family.

## 10. Explicit non-goals and non-approvals
PRD-P1-WX-02 does **not** approve:
- connector implementation
- external API calls
- provider credentials
- secrets/config loading
- forecast pulls
- forecast modeling
- probability modeling
- runtime scheduling
- production monitoring
- trading strategy
- order placement
- position sizing
- autonomy
- live market execution
- final standalone Weather Bot PRD synthesis

## 11. Later-ticket handoff
- Config/secrets fail-closed contract is handed off to **PRD-P1-WX-03**.
- Result/status/observability summary contract is handed off to **PRD-P1-WX-04**.
- Deep weather provider/resolution research pack is handed off to later weather research docs.
- Full standalone Weather Bot PRD is handed off to later **Opus** synthesis.
- Connector implementation is handed off to a future ticket only after explicit approval.

## 12. Source notes / research notes

| Provider/authority | Source URL or source name | Source type | Access date | Claims supported | Confidence |
|---|---|---|---|---|---|
| NOAA/NWS | https://www.weather.gov/documentation/services-web-api and https://api.weather.gov/ | official government docs/API | 2026-05-24 | Official API existence, standards posture | confirmed |
| NOAA/NWS (change notices) | https://www.weather.gov/media/notification/pdf_2025/scn25-44_API_latest_changesmay22_2025.pdf and related API notices | official government notice | 2026-05-24 | API change/maintenance posture | confirmed |
| Open-Meteo | https://open-meteo.com/en/docs and https://open-meteo.com/en/pricing | official docs/pricing | 2026-05-24 | Forecast/historical APIs, pricing/commercial endpoint posture | confirmed |
| Visual Crossing | https://www.visualcrossing.com/resources/documentation/weather-api/timeline-weather-api/ and https://www.visualcrossing.com/weather-data-editions/ | official API docs/pricing | 2026-05-24 | Timeline API scope, pricing page availability | confirmed |
| Tomorrow.io | https://www.tomorrow.io/weather-api and https://support.tomorrow.io/hc/en-us/articles/5188370662932-Weather-Timeline-Historical-and-Forecast-Coverage and https://support.tomorrow.io/hc/en-us/articles/23554984091156-How-Does-Pricing-Work-at-Tomorrow-io | official docs/support/pricing overview | 2026-05-24 | Plan-dependent forecast/historical ranges, pricing posture | confirmed/unclear mix |
| Meteomatics | https://www.meteomatics.com/en/api/getting-started/ and https://www.meteomatics.com/en/weather-api/ and https://www.meteomatics.com/en/pricing | official API/docs/pricing | 2026-05-24 | API capabilities, auth posture, pricing via sales contact | confirmed |
| OpenWeather | https://openweathermap.org/api and https://openweathermap.org/price | official API docs/pricing | 2026-05-24 | API product families and pricing posture | confirmed/unclear mix |
| WeatherAPI.com | https://www.weatherapi.com/docs and https://www.weatherapi.com/pricing.aspx | official API docs/pricing | 2026-05-24 | Documented endpoint families, explicit pricing/horizon tiers | confirmed |
| Meteostat | https://dev.meteostat.net/api/stations/hourly | official developer docs | 2026-05-24 | Station-hourly endpoint, delayed update caveat | confirmed |
| Weatherbit | https://www.weatherbit.io/api and https://www.weatherbit.io/pricing and https://www.weatherbit.io/api/historical-weather-daily | official API docs/pricing | 2026-05-24 | Historical/forecast capabilities, pricing/quota posture | confirmed |
| AccuWeather | https://developer.accuweather.com/documentation/overview and https://developer.accuweather.com/pricing | official developer docs/pricing | 2026-05-24 | API and pricing entry points; limited public detail on some enterprise terms | confirmed/unclear mix |

## 13. Acceptance criteria checklist
- [x] Canonical ID `PRD-P1-WX-02` is present exactly.
- [x] Provider research is documented.
- [x] Source notes are included.
- [x] Provider claims include source URLs/source names, access dates, and confidence statuses.
- [x] Resolution-rule compatibility is explicitly analyzed.
- [x] Provider-to-market-family fit is covered.
- [x] Connector approval gate is defined.
- [x] Non-goals and non-approvals are explicit.
- [x] Later-ticket handoff is clear.
- [x] No connector/runtime/API/trading/order/autonomy behavior is introduced.
