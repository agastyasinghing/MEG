# WX-RESEARCH-01: Weather Market Mechanics + Resolution Source Taxonomy

## Executive summary and scope

**Executive summary**

- Weather is a strong canonical event-graph proving ground because weather contracts often expose the core normalization fields directly in their rules: variable, threshold, comparator, time window, location or station, source agency, and settlement timing. That is unusually favorable for canonical mapping compared with many political or social-event markets. citeturn31view0turn31view2turn31view4turn31view10turn31view13
- The cleanest early candidates for Weather Bot planning are station-anchored temperature threshold markets, station-anchored precipitation threshold markets, monthly station precipitation or snowfall markets with explicit source pages, and simple hurricane-designation markets tied to National Hurricane Center or NOAA status determinations. These families have the narrowest ontology and the best audit trail in the reviewed materials. citeturn31view0turn31view2turn31view10turn12search3turn26view1
- The riskiest families are city-level wording that does not anchor to a station, creator-resolved community markets, markets using third-party weather pages rather than primary agencies, catastrophe/fatality markets that depend on damage or casualty tallies, and climate/anomaly markets that use adjusted or derived products instead of raw official observations. citeturn16view0turn16view1turn16view3turn25view1turn25view6
- The most important resolution-source issue is that “official weather data” is not one thing. NWS Daily Climate Reports, NOWData, NCEI CDO, NCEI GHCN-Daily, ISD/LCD products, NHC advisories, NHC best track, Storm Events Database, and airport-station METAR observations each have different production logic, revision patterns, and legal/audit status. citeturn25view0turn25view2turn25view7turn25view8turn26view1turn25view6
- A major trap is preliminary-versus-final mismatch. NWS climate products are preliminary before NCEI quality control, NOWData explicitly warns that finalized “official” data comes from NCEI or Regional Climate Centers, and Climate at a Glance warns that current figures can be preliminary and may differ from official observations. Yet several venue contracts intentionally freeze on the first qualifying report or the value shown at expiration time. citeturn30view4turn25view0turn25view1turn31view3turn31view11
- Another major trap is city-versus-station mismatch. Airport and surface-observation guidance makes clear that weather-station observations are not citywide averages, that different elements may be sensed at different points of an airport complex, and that “station location” can vary by observed element within roughly two miles. citeturn31view21turn31view22
- Venue wording creates non-equivalent markets even when headlines look similar. “Seattle precipitation in January” can mean a Polymarket monthly city-area figure from an NWS monthly summary, a Kalshi monthly total determined from the first complete daily climate report for an exchange-designated station, or a ForecastEx day-specific Weather Underground station summary. Those are related events, not exact equivalents. citeturn12search0turn31view2turn31view14
- ForecastEx provides the clearest published example of fallback logic in the reviewed sample: some daily temperature contracts resolve from NWS climate reports, but can delay settlement and then fall back to the greater of an intraday report maximum or the highest METAR observation if no final version appears by a stated time. That is a different risk profile from “single source, single report” markets. citeturn31view13turn11view0turn11view1
- WX-RESEARCH-03 should go deepest on source mismatch, trace and missing-data rules, station discontinuity, time-window normalization, fallback-source chains, discretionary resolver intervention, and catastrophe-adjacent classification drift. Those are the most repeated traps in the source sample. citeturn31view3turn31view11turn16view0turn16view1turn25view6turn26view1
- WX-RESEARCH-04 should focus on publication latency, revision probability, threshold sensitivity, trace-amount semantics, station-specific versus city-level variance, and the probability consequences of advisory-time versus best-track-time definitions for storm markets. citeturn25view0turn25view1turn26view1turn26view2turn29view3

**Research scope and non-approvals**

This packet is **research only**. It does **not** approve connector implementation, external API use, runtime behavior, forecast pulls, trading behavior, order placement, autonomy, or provider selection for implementation. The scope and guardrails follow the uploaded research brief. fileciteturn0file0

The evidence base below is strongest for: Kalshi contract specifications and help content, ForecastEx contract terms and rulebook language, official Polymarket market pages surfaced through search, official Manifold platform documentation plus representative public market pages, and official NOAA/NWS/NCEI/NHC plus selected Environment and Climate Change Canada and Met Office documentation. Where current public documentation was thinner, this report says so explicitly rather than inferring undocumented mechanics. citeturn1search0turn0search15turn10view3turn12search0turn16view0turn25view0turn29view0turn29view4

## Weather market family taxonomy

The suitability labels below are **MEG planning inferences**, not venue labels. They reflect how safely a market family can be normalized into a canonical real-world weather event using the reviewed evidence. citeturn31view0turn31view2turn31view10turn16view0turn25view0

| Market family | Typical market wording | Underlying real-world event | Canonical fields required | Common resolution source types | Likely resolution timing | Common ambiguity points | MEG modeling difficulty | Early suitability |
|---|---|---|---|---|---|---|---|---|
| Temperature threshold markets | “Will the daily high in [region] exceed [##]°F on [date]?”; “Will the highest/lowest/average temperature in [region] [exceed/be below] [##] F on [date]?” citeturn31view13turn31view15 | A specific station’s daily max/min/avg temperature over a stated observation day | variable kind, station, date, timezone/LST, threshold, comparator, unit, source product, revision rule | NWS Daily Climate Report; Weather Underground daily history; airport station page; METAR fallback in some contracts citeturn31view0turn31view13turn31view15 | Same day + next-morning report, or once first subsequent observation appears; sometimes delayed to a stated time if revision/fallback rules trigger citeturn31view1turn10view2turn31view13 | City vs station naming, local standard time, intraday vs final daily value, fallback-source logic | low to moderate | early_candidate |
| Precipitation threshold markets | “Will the total precipitation in [region] exceed [##] on [date]?”; “Will it rain in LA by next Friday?” citeturn31view14turn12search6 | Daily or multi-day precipitation at a designated station or city climate product | station/location, date window, precipitation metric, threshold/comparator, trace handling, source product | Weather Underground station summary; NWS Daily Climate Report; NWS monthly summary; NCEI archives as fallback in some monthly snow products citeturn31view14turn12search6turn31view11 | After complete daily summary or qualifying report appears citeturn10view1turn12search6 | “Rain” meaning trace vs measurable, day boundary, city climate page versus airport station, continuous updates versus first complete report | moderate | early_candidate |
| Snowfall markets | “Will it snow in Phoenix…?”; “Will [location] have at least [count] inches of new snowfall in [month] [year]?” citeturn31view7turn31view10 | New snowfall amount at a designated station/location over a day, month, or season | snowfall type, location/station, date or seasonal period, trace rule, missing-data rule, unit precision | NWS Daily Climate Reports; NWS NOWData; NCEI CDO fallback in some Kalshi rules; Environment Canada official records in community examples citeturn31view6turn31view10turn31view11turn16view2 | Same-day or monthly/seasonal close depending on product; often next morning or up to a week after month-end for monthly totals citeturn31view7turn31view12 | Trace treatment, manual versus automated snow capability, station discontinuity, season boundary, “new snow” versus snow depth | moderate | early_candidate |
| Wind markets | Kalshi publicly lists wind as a weather category, but this pass did not safely retrieve a detailed current public wind contract text comparable to the temperature/rain/snow files. Exact representative wording therefore remains unclear. citeturn1search0turn24view3 | Wind gust or sustained wind at a station over a stated period | gust vs sustained, averaging interval, station, time window, unit, source product | LCD/ISD station observations; ASOS/AWOS observations; possibly NWS climate products if contract cites them citeturn30view3turn25view8turn25view3 | Often daily or intraday, depending on source | Gust vs sustained, 1-minute vs 2-minute conventions, airport siting, exact product not confirmed in current venue sample | high | later_candidate |
| Storm and hurricane markets | “Will a hurricane form by May 31?”; “Will a hurricane make landfall in the US before October?” citeturn12search3turn16view4 | Storm designation, intensity classification, landfall, or other tropical-cyclone status event | basin, named system or any system, status threshold, temporal cutoff, advisory/best-track source, geography | NHC named-storm lists, storm-specific records, advisories, best track/Tropical Cyclone Reports depending on contract wording citeturn12search3turn26view1turn26view2 | Can resolve immediately on advisory classification, or only after post-storm products if contract says so | Advisory-time versus best-track-time, basin boundaries, landfall definition, UTC versus local time | moderate | early_candidate |
| Extreme weather markets | Severe thunderstorm, hail, tornado, destructive wind, blizzard, flash-flood, or other agency-classified event questions | Agency-classified occurrence or threshold event | event class, official criteria, time window, geography granularity, source authority | NWS/SPC definitions, local warnings, Storm Events Database, agency advisories | Often same-day for warning/advisory markets; months later if Storm Events Database is used | Warning versus observed event, official criteria thresholds, later database revisions, report-source verification | high | later_candidate |
| Daily city or location binary markets | “Will it rain in [city] tomorrow?”; “Highest temperature in [city] on [date]?” citeturn12search5turn15search4 | A daily yes/no or bracketed condition attached to a named place | city label, exact station or “city area” mapping, time zone, threshold/bracket, source page | NWS city-area climate products, airport station pages, creator-selected sources | Same day or next-day | City name masking station identity, unofficial “forecast” versus observation, vague city boundaries | moderate to high | early_candidate only when station/source is explicit |
| Weekly, monthly, and seasonal aggregate markets | “Precipitation in Seattle in January?”; “Will [location] have at least [count] inches in [month/year]?”; “Will it snow in Vancouver during winter season?” citeturn12search0turn31view10turn16view2 | Aggregated totals or averages across a month, week, season, or winter period | aggregation method, complete-period requirement, location/station, source product, missing-day rule, trace rule | NWS monthly summary, first complete daily climate report, NOWData monthly sum, Climate at a Glance, official national archives, Environment Canada official records citeturn31view2turn31view10turn12search0turn29view0 | End-of-period plus publication lag | “First complete report” versus later final archive, climatological-day conventions, missing-data handling, season boundary | moderate | early_candidate when station/product is explicit |
| Source-dependent resolution markets | Markets that name a specific resolver source page, fallback chain, or creator judgment rule | Same physical event, but resolution depends on named documentation source | exact source URL/product, fallback hierarchy, freeze time, source authority, venue override power | Venue-named source, third-party provider, fallback METAR, moderation/review process | Depends entirely on source release and venue rules | Same event can resolve differently across venues because the source chain differs | high | avoid_for_now unless source chain is explicit and primary |
| Catastrophe or disaster-adjacent weather markets | “Hurricane [name] causes 40+ fatalities?”; landfall plus casualties/damage questions citeturn15search17turn25view6 | Impact metrics caused by weather, often outside pure meteorology | impact metric, attribution, authoritative casualty/damage source, cut-off date, revision rule | Storm Events Database, official impact reports, media or encyclopedia pages in community markets | Often delayed; sometimes open-ended | Attribution to weather event, post-event revisions, source quality, legal/insurance interpretation | very high | avoid_for_now |
| Climate and anomaly markets | “Will average temperature in the contiguous U.S. for [month] be above [x]?” citeturn31view4 | Regional or national aggregate anomaly/average from a climate-monitoring product | region/unit, monthly period, adjusted versus raw data, release schedule, source product | NCEI Climate at a Glance, NCEI climate monitoring releases, national summary datasets citeturn31view4turn25view1 | Monthly or longer, tied to publication schedule | Adjusted versus official station observations, preliminary revisions, region-level not station-level semantics | high | later_candidate |

**Practical MEG takeaway**

For the first Weather Bot proving-ground pass, the cleanest families are those where a venue gives MEG a single named station, one variable, one threshold, one observation window, and one authoritative product. Once a market drifts into “city area,” “forecast,” “community judgment,” “fatalities,” or adjusted climate products, equivalence and resolver risk rise sharply. citeturn31view0turn31view2turn31view10turn16view0turn25view1

## Weather market mechanics and resolution source taxonomy

**How weather markets work mechanically**

Most reviewed weather markets are still mechanically simple on payout: they are binary or bracketed threshold contracts that pay based on whether an expiration value is above, below, exactly equal to, at least equal to, or within a range around a weather measurement. Kalshi’s temperature, rainfall, and snowfall contracts spell out threshold and comparator logic directly, and ForecastEx contract terms do the same for daily temperature and precipitation contracts. citeturn31view1turn31view2turn31view3turn31view6turn31view13turn31view14

What makes them hard is not payout logic but **measurement semantics**. The same headline can hide different real-world observation models:

- A contract can reference a **station** even when the headline says a **city**.
- A contract can use a **daily report published the next morning**, not live intraday values.
- A contract can freeze on the **first complete report**, not the later corrected archive.
- A contract can use a **third-party display page** rather than a government primary source.
- A contract can allow venue review, fallback sources, or source replacement if the original source becomes unreliable or unavailable. citeturn31view0turn31view3turn31view11turn31view13turn11view0turn11view1

The city-versus-station distinction is especially important. Official observing guidance says the “station location” can vary by element, that airport observations may place temperature, dew point, and wind near the runway complex, and that multiple locations may exist within about two miles of the station. ASOS documentation likewise notes that many sensors are near the primary runway touchdown zone and that some parameters are intentionally measured where they matter operationally, not where a city resident would think “the city center” is. Weather markets that headline a metro name while resolving against an airport station are therefore inherently **station-event** markets, not generic city-weather markets. citeturn31view21turn31view22

Daily-versus-aggregate mechanics also differ materially. Kalshi’s monthly rainfall contract resolves from the **first daily climate report that contains every calendar day of the month**, counts trace precipitation as 0.00 for threshold purposes, may count a day marked missing as 0.00, and ignores later revised reports once the first complete report exists. By contrast, Kalshi’s monthly NOWData snowfall contract uses the monthly total displayed by NOWData, treats daily snowfall trace as 0.0 inches, applies one-decimal precision, and contains explicit fallback language to NCEI CDO or a CLI report if the month’s data are unavailable. These are not the same aggregation mechanics even though both are “monthly accumulation” contracts. citeturn31view3turn31view10turn31view11turn31view12

Venue rules also create non-equivalence through time handling. ForecastEx temperature and precipitation contracts close at 11:59 PM local time on the listed date, but resolve when the named source or daily summary is published; daily temperature terms can delay settlement if the next-morning climate report is inconsistent with an intraday value, then fall back to a highest METAR observation if no final version appears by a stated time. Kalshi daily temperature contracts instead anchor expiration value to the underlying as documented by the source agency at expiration time, with explicit expiration date and time in the contract specifications. Polymarket market pages frequently hard-code a market-specific source page and boundary rule, such as “higher bracket” if a value lands exactly on a boundary. citeturn31view1turn10view1turn31view13turn12search1

**Resolution disputes, reviews, and cancellation or invalidation risk**

The reviewed venues differ sharply in how much discretion they reserve after listing. Kalshi’s market rules page says every market includes an official rules section and notes that market resolution can be delayed, specific dates can be changed, or markets can be canceled or voided if necessary. Individual Kalshi contract files also reserve a market outcome review process and, in some contracts, the ability to designate a new source agency or underlying if reliability or transparency is materially affected. ForecastEx Rule 413 permits source-agency replacement and contract-spec modification where source reliability or transparency is materially affected, and Rule 415 gives the Event Review Committee full discretion once formal review is initiated. Manifold goes much further toward platform and creator discretion: creators resolve markets, moderators may overturn resolutions, markets can resolve partial, and the platform reserves the right to resolve, re-resolve, cancel, or void markets for ambiguous criteria or other reasons. citeturn0search15turn31view5turn31view8turn11view0turn11view1turn16view0turn16view1

**Resolution source taxonomy**

| Source type | What it means | Examples | Reliability and auditability | Delay and revision risk | Suitability for prediction-market resolution | Provider compatibility implications |
|---|---|---|---|---|---|---|
| Official government source | A government agency’s own officially published product or archive | NWS Daily Climate Report; NCEI CDO; NHC advisories and Tropical Cyclone Reports citeturn31view0turn25view2turn26view0turn26view1 | Strongest audit trail and institutional provenance | Can still be preliminary at first release; product-specific publication delays matter citeturn30view4turn25view0 | Best default when named explicitly | MEG must preserve exact product identity, not just “NOAA” |
| Official meteorological agency | National or regional weather office outside the venue itself | Environment and Climate Change Canada historical climate data; Met Office station data citeturn29view0turn29view4 | Usually strong, but product purpose varies | QC cycles and disclaimers can differ by country and product | Good when the contract cites the agency and product precisely | Provider compatibility must be country- and product-specific |
| Official station observation | A direct station measurement or official daily summary for one station | NWS CLI/LCD, ASOS/AWOS station observations, official climate records | Strong for narrow physical metrics | Site relocation, augmentation, and station discontinuity can affect comparability citeturn25view3turn25view4turn31view22 | Best for daily station markets | MEG must store station ID, not just station name |
| Airport or station observation | Airport-linked surface observation, often through aviation systems or station history pages | METAR, ASOS, airport climate pages, Ben Gurion or SFO station pages in venue markets citeturn31view13turn12search5turn12search9 | Highly auditable for the station itself | Can differ from nearby city conditions; element-specific siting matters | Good for station-event markets, risky for “city” interpretation | Provider layer must map city headline to station identity explicitly |
| Climate data archive | Post-processed archive of daily/monthly station data | NCEI CDO, GHCN-Daily, ISD/Global Hourly, LCD certification products citeturn25view2turn25view7turn25view8turn25view9 | High auditability; often certifiable | Archive timing may lag operational products; some products aggregate/transform source records | Strong for verification and post-hoc QA; not always identical to venue’s operative source | “Official archive” is not always resolution-compatible with a venue’s first-report rule |
| Storm center or advisory source | Specialized agency products for storms and hazards | NHC Public Advisory, NHC named-storm records, NHC best track, WPC transfer products citeturn26view0turn26view1turn26view2 | Strong for storm-status questions | Advisory-time and best-track assessments can differ; responsibility can transfer between agencies | Best for hurricane/tropical-cyclone designation markets | MEG must encode whether the contract keys off advisory status or post-analysis |
| Venue-selected resolver | The venue itself chooses or modifies the governing source | Kalshi source-agency replacement language; ForecastEx Rule 413 source modification citeturn31view5turn31view16 | Depends on transparency of substitute source | Elevated because source regime can change midstream | Acceptable only with explicit source-change governance and human review | Provider compatibility must detect and flag mid-market source mutation |
| Third-party weather provider | Commercial or non-government weather site used directly for resolution | Weather Underground in ForecastEx temperature and precipitation contracts; Wunderground in some Polymarket temperature markets citeturn31view14turn31view15turn12search9 | Auditability depends on how the page is populated and retained | Display-layer changes, page relocation, and undocumented transformations are material risks | Usable only when venue explicitly names the exact page/product | MEG should treat these as distinct resolver types, not substitutes for NOAA/NWS |
| Aggregated or derived source | Product built by averaging, adjusting, or summarizing multiple observations | Climate at a Glance; monthly climate summaries; national averages/anomalies citeturn25view1turn31view4 | Good for macro products, weaker for raw-event identity | Recent values can be preliminary; adjusted data may differ from station observations | Appropriate for anomaly markets, poor substitute for station-event markets | Provider compatibility must capture whether values are adjusted/derived |
| Unclear or discretionary source | Source not fixed to one authoritative product, or judgment is left to creator/moderator | Manifold creator judgment, custom weather station, platform discretion, forecast-page references citeturn16view0turn16view1turn16view3turn15search7 | Weakest auditability | Highest delay and dispute risk | Poor choice for early automation planning | Should trigger hard human review or exclusion |

**Bottom line for source compatibility**

MEG should not ask “Do we have weather data?” It should ask “Do we have **the same product semantics** the venue will use at resolution time?” In weather markets, product identity is part of event identity. citeturn25view0turn25view1turn31view3turn31view11turn31view13

## Canonical event identity implications and resolution-risk taxonomy

**Canonical event identity fields MEG should represent**

MEG should represent at least the following fields before any implementation planning:

- **domain**: weather, tropical cyclone, severe weather, climate aggregate.
- **market family**: temperature threshold, daily precipitation, monthly snowfall, hurricane designation, and so on.
- **location label**: the venue-facing human label.
- **geographic precision**: city area, airport station, weather station, forecast office area, state, CONUS, basin.
- **station or observation point**: station name and stable identifier where available. NCEI HOMR and Environment Canada climate IDs show why this is essential. citeturn25view4turn29view3
- **date or time window**: single day, rolling multi-day, month, winter season, by a stated cutoff.
- **timezone convention**: local time, local standard time, UTC, explicit exchange timezone, or advisory issuance timezone. LCD documentation and NHC product descriptions show that this cannot be inferred safely. citeturn30view2turn31view25
- **weather variable**: max temperature, rainfall, new snowfall, storm designation, landfall, hail size, maximum sustained wind, gust, anomaly, and so on.
- **threshold** and **comparator**: above, below, at least, exactly, between, bracketed.
- **unit**: °F, °C, inches, mph, knots, categorical storm class.
- **aggregation method**: highest hourly observation, daily summary value, monthly total, sum of daily values, adjusted national average, best-track assessment.
- **resolution source**: the exact named product or page.
- **resolution authority**: source agency, venue review committee, creator/moderator.
- **source reference or URL**: human-review link to the proof page or contract rule.
- **venue wording**: full venue-specific market language, because equivalence often breaks here.
- **ambiguity flags**: city/station mismatch, source mismatch, trace rule, missing-data rule, fallback-source rule.
- **resolution-risk flags**: discretionary review allowed, preliminary-data reliance, station discontinuity, advisory-versus-final mismatch, catastrophe attribution, and so on.
- **human-readable summary**: a concise canonical sentence describing the real-world event. citeturn31view0turn31view2turn31view10turn31view13turn16view0

**When markets are equivalent and when they are not**

- **Exact equivalents** are markets that point to the same variable, same station or geographic object, same time window, same unit, same threshold/comparator, and same resolution source/product. Example: two contracts that both resolve from the same NWS Daily Climate Report maximum temperature row for the same station and date. citeturn31view0turn31view13
- **Near-equivalents** share the same real-world phenomenon and threshold but differ in source timing or fallback details. Example: a daily high contract resolved from an NWS climate report versus a contract resolved from a Weather Underground daily summary for the same station/date. citeturn31view13turn31view15
- **Related but non-equivalent** markets talk about the same city or weather headline but use different stations, different products, or different aggregation rules. Example: Polymarket “Seattle precipitation in January?” versus Kalshi RAINM monthly station precipitation. citeturn12search0turn31view2turn31view3
- **Conflicting or incompatible** markets rely on fundamentally different ontologies. Example: a market resolved from adjusted Climate at a Glance values versus a market resolved from raw official station observations; or a creator-judged rain market versus an official station-observation market. citeturn25view1turn16view0turn16view3

**Resolution-risk taxonomy draft**

| Risk | Definition | Example | Why it matters | Market families affected | Human-review note |
|---|---|---|---|---|---|
| Source mismatch risk | Different products describe the same phenomenon differently | NOWData versus final NCEI official data | NOWData explicitly says finalized official data comes from NCEI/RCC; venues may nevertheless freeze on NOWData or first reports citeturn25view0turn31view11 | snow, monthly totals, climate products | Confirm exact operative source and freeze rule |
| Station or location ambiguity | Headline place-name does not uniquely identify a station | “Seattle” or “Phoenix” without station ID | Airport and surface-observation docs show observations are station-based and element-specific; place names alone are insufficient citeturn31view21turn31view22turn25view4 | temp, precip, snow, wind | Require station ID or approved station mapping |
| City versus station mismatch | “City weather” resolves from airport or office station | Los Angeles Downtown CLI or SFO airport history page | A city headline can hide a very specific observing point citeturn12search6turn12search9turn31view22 | daily city binaries, temperature, precipitation | Rewrite canonical summary as station-event |
| Timezone or window mismatch | Observation day boundary differs across products | Local standard time in LCD; UTC in NHC advisories; climatological day in Canada | Time definitions are product-specific and can change outcomes on boundary cases citeturn30view2turn31view25turn29view3 | all families | Store explicit timezone and day-boundary semantics |
| Threshold or comparator ambiguity | “Above,” “at least,” “between,” or bracket resolution differs | Kalshi “between” lower-inclusive/upper-exclusive for rainfall versus NOWDATASNOW inclusive both ends | Comparator semantics alter outcomes at the boundary citeturn31view2turn31view11 | all threshold markets | Normalize comparator explicitly, never infer |
| Unit conversion risk | Market wording and source product use different units or precision | Celsius in Tel Aviv example; Fahrenheit in many U.S. markets; one-decimal snow rounding | Unit and precision changes can flip exact-threshold outcomes citeturn12search5turn31view11turn30view2 | temp, snow, wind | Preserve source-native unit and rounding rule |
| Accumulation-period ambiguity | What counts toward a total is unclear | Daily precipitation on a calendar date versus monthly total from first complete report | Aggregation can depend on report production logic, not intuitive calendar arithmetic citeturn31view3turn29view3 | precip, snow, monthly/seasonal aggregates | Record aggregation algorithm, not just period label |
| Delayed reporting or revision risk | Source values can change after first publication | NWS data preliminary before NCEI QC; Storm Events Database arrives 75–90 days later | Venue rules may intentionally ignore later corrections, creating divergence from final archives citeturn30view4turn25view6turn25view1 | climate, severe weather, monthly aggregates | Flag “preliminary source frozen at resolution” |
| Venue wording ambiguity | Market headline omits critical mechanics buried in rules | “Will it rain…” with creator-selected interpretation or vague city-area scope | Resolution may depend on hidden thresholds or custom definitions citeturn16view0turn15search4turn15search7 | community markets, city binaries | Require full rules text for mapping |
| Discretionary resolver risk | Venue or creator can override or reinterpret | ForecastEx Event Review; Manifold creator/moderator resolution | Human discretion introduces non-data risk into settlement citeturn11view1turn16view0turn16view1 | source-dependent and community markets | Escalate to human review or exclude |
| Cancellation or invalidation risk | Market may be canceled, voided, or accelerated | Kalshi market cancellation/voiding language; ForecastEx accelerated settlement | Event outcome may never be resolved purely by source value citeturn0search15turn31view16 | all families | Track venue contingency clauses separately |
| Extreme-event classification risk | Event depends on agency category assignment, not raw sensor value | Hurricane versus tropical storm; severe thunderstorm criteria | Agency classifications are formal and sometimes post-analyzed differently from raw data citeturn26view1turn27search1turn27search4 | hurricanes, severe weather | Store classification authority and version |
| Aggregate-period ambiguity | Week/month/season definitions vary by source | Vancouver winter Oct–Apr; NWS month-end first-complete report; Canadian climatological day | The “period” is part of the source definition, not just the calendar label citeturn16view2turn31view3turn29view3 | seasonal and monthly markets | Make period boundary explicit in canonical object |

## Venue and source examples with future research methods

**Venue and source examples**

| Venue or source | Market wording or representative wording | Resolution source | Canonical event interpretation | Ambiguity or trap notes | Confidence status |
|---|---|---|---|---|---|
| Kalshi | CHIHIGH: maximum temperature recorded for the specified date in the NWS Daily Climate Report for Chicago Midway; payout when expiration value is strictly greater than the degree threshold citeturn31view0turn31view1 | NWS Daily Climate Report | Station-specific daily maximum temperature at Chicago Midway, not generic “Chicago weather” | Preliminary report language and fixed expiration-time snapshot create revision risk | confirmed |
| Kalshi | RAINM: total monthly precipitation in inches for a specified NWS weather station/city during a month, using the first Daily Climate Report containing all calendar days; trace and some missing rules are explicit citeturn31view2turn31view3 | NWS Daily Climate Report / NOAA | Station-specific monthly precipitation total with first-complete-report semantics | Missing-day treatment and first-report freeze make archive substitutions unsafe | confirmed |
| Kalshi | AVGTEMP: average temperature in the contiguous United States for a month according to NCEI citeturn31view4turn31view5 | NCEI climate monitoring product | National monthly aggregate climate metric | Aggregate/adjusted product, not a station observation; source replacement clause exists | confirmed |
| Kalshi | SNOWS / SNOWAZ / SNOWOVERTIME / NOWDATASNOW variants use NWS daily reports or NOWData monthly snowfall, with explicit trace, rounding, missing-data, and station-discontinuity rules in some files citeturn31view6turn31view7turn31view9turn31view10turn31view11turn31view12 | NWS Daily Climate Report or NWS NOWData, sometimes NCEI CDO fallback | Station-specific new-snow or snowfall-total event over day/month/season | Snow semantics depend heavily on manual observation capability, trace rules, and fallback hierarchy | confirmed |
| ForecastEx | DH terms: “Will the daily high in [region] exceed [##]°F on [date]?” with NWS climatological report and METAR fallback if no final report appears by 10 AM CT citeturn31view13 | NWS climatological report, with METAR fallback | Station-specific daily high temperature event with explicit fallback chain | Fallback chain means same event can differ from pure NWS-report contracts | confirmed |
| ForecastEx | PR terms: daily precipitation accumulation for a designated airport weather observation station, resolved from Weather Underground “History” summary table only citeturn31view14 | Weather Underground daily summary | Station-specific daily precipitation event | Third-party page dependency and display-layer specificity | confirmed |
| ForecastEx | U terms: highest, lowest, or average temperature in region on date, from Weather Underground daily summary table only citeturn31view15 | Weather Underground daily summary | Station-specific daily max/min/avg temperature event | Final daily value only; no other tables or graphs may be used | confirmed |
| ForecastEx | Rulebook: source agency can be replaced if reliability/transparency is affected; Event Review Committee has full discretion once review is initiated citeturn31view16turn31view17 | Venue-selected governance process | Market resolution depends on both source data and venue review powers | Important non-data settlement risk | confirmed |
| Polymarket | “Precipitation in Seattle in January?” with NOAA monthly summarized data for “Seattle City Area,” using venue-stated precision and bracket rules citeturn12search0turn12search1 | NOAA/NWS city-area climate page | Monthly city-area precipitation bracket market | Not necessarily identical to a single-station monthly total market | confirmed |
| Polymarket | “Will a hurricane form by May 31?” resolves to Yes if NOAA designates any Atlantic storm a hurricane within stated dates citeturn12search3 | NOAA/NHC storm lists and individual storm data | Basin-wide storm-designation event | Advisory designation and exact time basis need careful normalization | confirmed |
| Polymarket | “Highest temperature in Tel Aviv on March 25?” uses NOAA figure for Ben Gurion International Airport; “Will it rain in LA by next Friday?” uses a Daily Climate Report figure; some temperature markets cite Wunderground airport history pages citeturn12search5turn12search6turn12search9 | NOAA/NWS or Wunderground, market-specific | Daily station-event market despite city headline | Same venue can mix source types across weather markets | confirmed |
| Manifold | Platform FAQ: creators resolve markets; creators may use judgment; moderators may overturn resolutions; N/A cancels a market citeturn16view0 | Creator plus moderator/platform | Resolver-dependent market family | High discretionary risk by design | confirmed |
| Manifold | Terms: platform reserves right to resolve, re-resolve, cancel, or void any market at its sole discretion for ambiguous criteria and other reasons citeturn16view1 | Platform discretion | Platform-governed outcome regime | Strong reason to exclude from early automated equivalence mapping | confirmed |
| Manifold | “Will it snow in Vancouver?” resolves Yes if measurable snow accumulation at Vancouver International Airport (YVR) during winter season, verified via official Environment Canada records citeturn16view2 | Environment Canada official records at YVR | Seasonal station-specific snow-occurrence event | Good example of a clean non-U.S. station market | confirmed |
| Manifold | “Will it rain in Ripton Vermont on August 5th 2023?” says the creator will use a personal weather station and be physically present citeturn16view3 | Creator’s own weather station / personal observation | Custom, creator-defined event | Unsafe for canonical automation | confirmed |
| Manifold | “Will a hurricane make landfall in the US before October?” says usual rules apply: hurricane strength at time of landfall, NHC advisory, UTC time citeturn16view4 | NHC advisory | Tropical-cyclone classification and landfall-time event | Cleaner than casualty markets, but still requires exact NHC landfall semantics | confirmed |

**Future research methods and reading lists**

**Market wording analysis**

What it is for: parsing venue text into a canonical event object without losing hidden mechanics.  
How MEG might use it later: a contract-ingestion stage that separates headline wording from operative rule text.  
Limits and risks: many platforms hide critical mechanics in rules, comments, or examples, not in the headline. citeturn31view0turn31view2turn31view13turn16view0

Future researcher reading list:
- Kalshi market rules help center page.
- Kalshi CHIHIGH, RAINM, NOWDATASNOW contract files.
- ForecastEx DH / PR / U terms and conditions.
- Polymarket weather market pages with explicit source paragraphs.
- Search term: `site:prediction-market-venue weather market "resolution source"`.

**Resolution-source taxonomy construction**

What it is for: separating “same event” from “same resolver.”  
How MEG might use it later: source compatibility checks and risk scoring.  
Limits and risks: agency family names are insufficient; the exact product matters. citeturn25view0turn25view1turn25view2turn26view1

Future researcher reading list:
- NOAA NOWData FAQ.
- NCEI Climate Data Online and certification pages.
- NHC Public Advisory format and glossary.
- NCEI GHCN-Daily and ISD product pages.
- Search term: `official weather data preliminary final certification`.

**Station and location matching**

What it is for: mapping a venue’s place label to the actual observation point.  
How MEG might use it later: strict station identity resolution and successor-station handling.  
Limits and risks: city names, airport names, office areas, and successor stations diverge. citeturn25view4turn31view21turn31view22turn31view11turn29view3

Future researcher reading list:
- NCEI HOMR.
- NCEI ASOS/AWOS product page.
- WSOH surface observing handbook page on station location.
- Environment Canada climate glossary.
- Search term: `station history successor station climatological data`.

**Time-window normalization**

What it is for: turning a venue’s “today,” “by Friday,” or monthly period into a stable observation window.  
How MEG might use it later: explicit window objects in the canonical event graph.  
Limits and risks: UTC, local time, local standard time, climatological day, and publication day are all live risks. citeturn30view2turn31view25turn29view3turn31view3

Future researcher reading list:
- LCD dataset documentation.
- NHC text product descriptions.
- Environment Canada climatological day glossary entry.
- NWS climate products page and relevant office documentation.
- Search term: `climatological day local standard time daily climate report`.

**Threshold and comparator normalization**

What it is for: preserving exact mathematical meaning at boundaries.  
How MEG might use it later: comparator normalization and safe equivalence matching.  
Limits and risks: “between” semantics vary, exact-equality precision varies, and trace values can be treated as 0.0 or above 0.0 depending on venue. citeturn31view2turn31view6turn31view11

Future researcher reading list:
- Kalshi RAINM contract.
- Kalshi SNOWS and NOWDATASNOW contracts.
- Polymarket Seattle precipitation bracket wording.
- Search term: `prediction market exactly at least between trace amount weather`.

**Aggregation-period interpretation**

What it is for: representing sums, averages, and season totals correctly.  
How MEG might use it later: aggregate-event identity templates.  
Limits and risks: some venues use monthly totals from a report, others sum daily rows, and some products are already adjusted aggregates. citeturn31view3turn31view10turn25view1

Future researcher reading list:
- Kalshi RAINM and NOWDATASNOW contracts.
- NCEI Climate at a Glance documentation page.
- Met Office historic station data notes on provisional and final status.
- Search term: `monthly precipitation total first complete report climate summary`.

**Venue-market equivalence mapping**

What it is for: deciding whether two listed markets are the same event, a near substitute, or incompatible.  
How MEG might use it later: venue-specific market mapping and cross-venue trap detection.  
Limits and risks: identical headlines can hide different sources, stations, or fallback rules. citeturn12search0turn31view2turn31view13turn16view0

Future researcher reading list:
- Polymarket monthly Seattle precipitation page.
- ForecastEx weather contract term sheets.
- Kalshi weather contract specifications.
- Manifold FAQ and terms.
- Search term: `market equivalence source chain prediction contract`.

**Resolution-risk scoring**

What it is for: a reviewable risk label before any downstream provider or bot decision.  
How MEG might use it later: fail-closed human-review gating and PRD requirements.  
Limits and risks: some risks are data risks, others are governance risks, and they should not be merged blindly. citeturn11view1turn16view1turn25view6turn25view0

Future researcher reading list:
- ForecastEx Rule 413–415.
- Manifold terms and FAQ.
- Storm Events Database FAQ.
- NOWData FAQ.
- Search term: `weather contract dispute resolution preliminary data review committee`.

## Implications, open questions, source notes, and final handoff

**Implications for WX-RESEARCH-02**

Provider and source compatibility research should investigate:

- Whether a candidate provider reproduces the **exact venue-cited product semantics**, not just “the same variable.”  
- Whether the provider can preserve **station identity**, **timezone/day-boundary semantics**, **trace handling**, **missing-data handling**, and **fallback-source chains**.  
- Which products are **preliminary**, which are **final**, which are **adjusted/derived**, and whether that is acceptable for a given venue family.  
- Whether non-U.S. official sources expose similarly stable identifiers and archival guarantees.  
- Whether human review needs direct access to the exact source page the venue cites, instead of a normalized API abstraction. citeturn25view0turn25view2turn25view4turn25view7turn25view8turn29view0

**Implications for WX-RESEARCH-03**

Trap categories that should be studied next:

- first-report versus final-report divergence;
- station aliasing and successor-station discontinuity;
- city headline versus airport station reality;
- local time, local standard time, UTC, and climatological-day drift;
- trace-versus-zero semantics;
- missing-day treatment;
- fallback-source and source-replacement chains;
- advisory-time versus best-track-time storm definitions;
- creator/moderator/platform discretion;
- catastrophe-attribution drift from meteorology into impacts. citeturn31view3turn31view11turn31view13turn16view0turn16view1turn26view1turn29view3

**Implications for WX-RESEARCH-04**

Probability and uncertainty questions implied by market mechanics:

- How often do preliminary and final values differ enough to change threshold outcomes?
- How much edge-case probability sits at boundaries because of trace amounts, one-decimal rounding, or exact-equality rules?
- How much forecast uncertainty comes from **station microclimate variance** rather than regional weather uncertainty?
- For hurricane markets, how often do advisory-time status and post-storm best track differ around a cutoff time?
- How much uncertainty is created by publication latency itself, especially when markets can resolve early or delay settlement?
- For monthly and seasonal aggregates, how sensitive are outcomes to one missing day, station discontinuity, or a successor-station handoff? citeturn25view0turn31view11turn26view1turn26view2turn31view13

**Open questions and unknowns**

- Whether currently public detailed wind-contract specifications on major regulated venues are as accessible and explicit as the sampled temperature/rain/snow files in this pass: **unclear**. citeturn1search0turn24view3
- Whether Polymarket publishes a venue-wide weather-specific policy page beyond market-level source paragraphs that materially changes market-resolution behavior: **unclear**. citeturn12search0turn12search3turn12search5
- Whether other active public prediction venues now offer weather contracts with official documentation comparable to Kalshi and ForecastEx: **unknown**.
- Whether some “city area” climate pages used by venues are formally thread-linked to station-successor logic in a way MEG can machine-represent without office-specific exceptions: **unclear**. citeturn31view20turn25view4
- Whether non-U.S. official sources outside the sampled Environment Canada and Met Office materials expose enough uniform metadata for cross-country canonicalization in an early phase: **unclear**. citeturn29view0turn29view3turn29view4
- Whether Storm Events Database should ever be treated as an early-resolution source rather than a late historical verification source, given its delay and external-source caveats: **confirmed** as a risk, but its suitability for any specific venue family remains **unclear**. citeturn25view6

**Source notes**

| Source name | URL | Source type | Access date | Claims supported | Confidence status |
|---|---|---|---|---|---|
| Kalshi Weather Markets help page | `https://help.kalshi.com/trading/markets/kalshi-weather-markets` | official venue rules/help | 2026-05-25 | Weather families listed publicly by Kalshi, including temperatures, snow, wind, rain, hurricanes, and climate-related questions | confirmed |
| Kalshi Market Rules help page | `https://help.kalshi.com/markets/market-rules/market-rules-overview` | official venue rules/help | 2026-05-25 | Every market includes rules; market resolution may be delayed; dates may change; markets may be canceled or voided if necessary | confirmed |
| Kalshi CHIHIGH contract terms | `https://www.cftc.gov/sites/default/files/filings/ptc/21/08/ptc081821kexdcm009.pdf` | official venue contract terms | 2026-05-25 | Daily maximum temperature mechanics, NWS Daily Climate Report source, payout criterion, expiration timing, contingency review | confirmed |
| Kalshi RAINM contract terms | `https://www.cftc.gov/sites/default/files/filings/orgrules/26/02/rules02042638732.pdf` | official venue contract terms | 2026-05-25 | Monthly precipitation mechanics, first-complete-report rule, trace and missing-day treatment, comparator semantics | confirmed |
| Kalshi AVGTEMP contract terms | `https://www.cftc.gov/sites/default/files/filings/ptc/22/11/ptc111822kexdcm001.pdf` | official venue contract terms | 2026-05-25 | Monthly U.S. average temperature mechanics using NCEI, aggregate-climate market example, source-replacement contingency | confirmed |
| Kalshi SNOWS contract terms | `https://www.cftc.gov/sites/default/files/filings/ptc/24/12/ptc12182411788.pdf` | official venue contract terms | 2026-05-25 | Daily snowfall contract mechanics and trace-above-zero rule | confirmed |
| Kalshi SNOWAZ contract terms | `https://www.cftc.gov/sites/default/files/filings/ptc/24/12/ptc12042410321.pdf` | official venue contract terms | 2026-05-25 | Phoenix snowfall contract mechanics, daily climate report source, early expiration possibility, contingency review | confirmed |
| Kalshi SNOWOVERTIME contract terms | `https://www.cftc.gov/sites/default/files/filings/ptc/25/07/ptc07022525257.pdf` | official venue contract terms | 2026-05-25 | Area-based snowfall over configurable time periods, primary official station logic, comparator semantics | confirmed |
| Kalshi NOWDATASNOW contract terms | `https://www.cftc.gov/sites/default/files/filings/ptc/25/12/ptc12012533839.pdf` | official venue contract terms | 2026-05-25 | NOWData monthly snowfall mechanics, trace handling, missing-data rule, NCEI/CLI fallback, station discontinuity | confirmed |
| ForecastEx DH Contract Terms and Conditions | `https://data.forecastex.com/regulatory/DHTermsandConditions.pdf` | official venue contract terms | 2026-05-25 | NWS-based daily high contract, report timing, fallback to highest METAR, local-time trading close | confirmed |
| ForecastEx PR Contract Terms and Conditions | `https://data.forecastex.com/regulatory/PRTermsandConditions.pdf` | official venue contract terms | 2026-05-25 | Weather Underground precipitation resolution mechanics and source exclusivity | confirmed |
| ForecastEx U Contract Terms and Conditions | `https://data.forecastex.com/regulatory/UTermsandConditions.pdf` | official venue contract terms | 2026-05-25 | Weather Underground high/low/average temperature resolution mechanics | confirmed |
| ForecastEx LLC Rulebook | `https://data.forecastex.com/regulatory/ForecastEx_LLC_Rulebook.pdf` | official venue rulebook | 2026-05-25 | Source-agency replacement, accelerated settlement, event review discretion, settlement schedule, coupon rule context | confirmed |
| Polymarket weather market pages | `https://polymarket.com/event/precipitation-in-seattle-in-january` and related indexed pages | official market pages | 2026-05-25 | Monthly precipitation bracket wording, source-page naming, bracket-boundary handling, NOAA source references | confirmed |
| Polymarket hurricane weather market page | `https://polymarket.com/event/will-a-hurricane-form-by-may-31` | official market page | 2026-05-25 | Basin-wide hurricane-designation wording tied to NOAA/NHC storm records | confirmed |
| Polymarket daily weather market pages | `https://polymarket.com/event/highest-temperature-in-tel-aviv-on-march-25-2026`, `https://polymarket.com/event/will-it-rain-in-la-by-next-friday`, `https://polymarket.com/event/highest-temperature-in-san-francisco-on-april-20-2026` | official market pages | 2026-05-25 | Venue mixes official NOAA/NWS and Wunderground station pages across weather markets | confirmed |
| Manifold FAQ | `https://docs.manifold.markets/faq` | official venue documentation | 2026-05-25 | Creator resolution, moderator override, partial and N/A resolution behavior | confirmed |
| Manifold Terms of Service | `https://docs.manifold.markets/terms` | official venue documentation | 2026-05-25 | Platform discretion to resolve, re-resolve, cancel, or void markets | confirmed |
| Manifold Vancouver snow market | `https://manifold.markets/Kam/will-it-snow-in-vancouver` | official public market page | 2026-05-25 | Clean seasonal snow example using official Environment Canada records at YVR | confirmed |
| Manifold private weather station market | `https://manifold.markets/Sailfish/will-it-rain-in-ripton-vermont-on-a` | official public market page | 2026-05-25 | Creator-selected private weather-station resolution example | confirmed |
| Manifold hurricane landfall market | `https://manifold.markets/MachiNi/will-a-hurricane-make-landfall-in-t-chIRgZpOR6` | official public market page | 2026-05-25 | NHC advisory and UTC-based hurricane landfall example | confirmed |
| NWS NOWData FAQ | `https://www.weather.gov/climateservices/nowdatafaq` | government/weather-source doc | 2026-05-25 | NOWData preliminary/final distinctions; NCEI as source of finalized official data | confirmed |
| NWS climate products portal | `https://www.weather.gov/wrh/climate` and office pages such as `https://www.weather.gov/wrh/climate?wfo=sew` | government/weather-source doc | 2026-05-25 | Product families such as Daily Climate Report, Monthly Weather Summary, NOWData availability, preliminary notice | confirmed |
| NWSI 10-1004 Climate Data and Products | `https://www.weather.gov/media/directives/010_pdfs/pd01010004curr.pdf` | government/weather-source doc | 2026-05-25 | Daily CLI / CLM / CF6 / RER product definitions; preliminary status before NCEI QC; ThreadEx mention | confirmed |
| NCEI Climate Data Online | `https://www.ncei.noaa.gov/cdo-web/` | government/weather-source doc | 2026-05-25 | Quality-controlled archive access and certified hard copies for legal use | confirmed |
| NCEI Data Certification | `https://www.ncei.noaa.gov/services/certification` | government/weather-source doc | 2026-05-25 | Which products are certifiable, including LCD, COOP, and GHCN-D | confirmed |
| NCEI ASOS/AWOS product page | `https://www.ncei.noaa.gov/products/land-based-station/automated-surface-weather-observing-systems` | government/weather-source doc | 2026-05-25 | ASOS/AWOS network role, archival context, continual observations | confirmed |
| ASOS User’s Guide | `https://www.weather.gov/media/asos/aum-toc.pdf` | government/weather-source doc | 2026-05-25 | Touchdown-zone and airport siting implications for observations | confirmed |
| Surface Weather Observations Handbook | `https://www.weather.gov/media/surface/WSOH8.pdf` | government/weather-source doc | 2026-05-25 | Element-specific station location and multiple-location concept within about two miles | confirmed |
| LCD Dataset Documentation | `https://www.ncei.noaa.gov/pub/data/cdo/documentation/LCD_documentation.pdf` | government/weather-source technical doc | 2026-05-25 | Local Standard Time conventions, precipitation and wind units, sustained-wind definition, monthly summary structure | confirmed |
| NCEI HOMR | `https://www.ncei.noaa.gov/access/homr/` | government/weather-source doc | 2026-05-25 | Station metadata, identifier history, location and equipment changes | confirmed |
| NCEI GHCN-Daily | `https://www.ncei.noaa.gov/products/land-based-station/global-historical-climatology-network-daily` | government/weather-source doc | 2026-05-25 | Daily climate summaries, integrated sources, quality-assurance reviews | confirmed |
| NCEI ISD / Global Hourly | `https://www.ncei.noaa.gov/products/land-based-station/integrated-surface-database` | government/weather-source doc | 2026-05-25 | Hourly and synoptic station observations, parameter coverage | confirmed |
| NCEI Climate at a Glance | `https://www.ncei.noaa.gov/access/monitoring/climate-at-a-glance/national` | government/weather-source doc | 2026-05-25 | Near-real-time monthly analysis, adjusted observations, preliminary caveat, differences from official observations | confirmed |
| NCEI Storm Events Database and FAQ | `https://www.ncei.noaa.gov/stormevents/` and `https://www.ncei.noaa.gov/stormevents/faq.jsp` | government/weather-source doc | 2026-05-25 | Official Storm Data context, data-source caveats, 75–90 day lag, location precision differences over time | confirmed |
| NHC Public Advisory format | `https://www.nhc.noaa.gov/help/tcp.shtml` | government/weather-source doc | 2026-05-25 | Public advisory structure, warning definitions, issuance content | confirmed |
| NHC Glossary | `https://www.nhc.noaa.gov/aboutgloss.shtml` | government/weather-source doc | 2026-05-25 | Best-track definition, advisory definition, classification semantics | confirmed |
| NHC Text Product Descriptions | `https://www.nhc.noaa.gov/pdf/NHC_Product_Description.pdf` | government/weather-source doc | 2026-05-25 | Advisory issuance intervals, WPC transfer conditions, key-messages uncertainty products | confirmed |
| NWS Severe Thunderstorm Safety / Glossary pages | `https://www.weather.gov/safety/thunderstorm` and NWS glossary entries | government/weather-source doc | 2026-05-25 | Official severe-thunderstorm criteria such as hail size and wind thresholds | confirmed |
| Environment and Climate Change Canada Historical Climate Data | `https://climate.weather.gc.ca/` | official meteorological agency doc | 2026-05-25 | Canadian hourly/daily/monthly official historical climate records and related services | confirmed |
| Environment and Climate Change Canada data-quality and glossary pages | `https://climate.weather.gc.ca/climate_data/data_quality_e.html` and `https://climate.weather.gc.ca/glossary_e.html` | official meteorological agency doc | 2026-05-25 | Climate ID, climatological day, QC caveats, station-operator distinctions | confirmed |
| Met Office historic station data | `https://www.metoffice.gov.uk/research/climate/maps-and-data/historic-station-data` | official meteorological agency doc | 2026-05-25 | UK historic station data use limitations, provisional/final status, monthly variable definitions | confirmed |

**Final handoff summary**

**Key findings**

Weather markets are not hard because weather is fuzzy. They are hard because **resolution semantics are specific**. The canonical event that MEG must model is not merely “rain in Seattle” or “snow in Denver.” It is usually something like: *monthly precipitation total for exchange-designated NWS station X, from the first qualifying daily climate report containing all calendar days of month Y, with trace counted as 0.00 and later revisions ignored.* The sources reviewed make that pattern extremely clear. citeturn31view2turn31view3turn31view10turn31view11

**Most important risks**

The largest risks are source mismatch, city/station ambiguity, time-window mismatch, threshold-boundary semantics, trace and missing-data handling, and any venue rule that reserves discretionary review or source replacement. Those risks are not edge cases; they are core market mechanics. citeturn25view0turn31view22turn31view11turn11view1turn16view1

**Recommended inputs to WX-RESEARCH-03**

Study trap taxonomies around: first report versus final report, exact source identity, fallback chains, station succession, local standard time versus UTC, advisory versus best track, and user-resolved or platform-discretionary weather markets. citeturn31view13turn25view0turn25view4turn26view1turn16view0

**Recommended inputs to WX-RESEARCH-04**

Study uncertainty around: publication timing, revision frequency, threshold sensitivity, station-level variance, trace events around zero, and advisory-time versus post-analysis storm classifications. citeturn25view1turn25view0turn31view11turn26view1turn26view2

**What should not be implemented yet**

Do **not** implement provider choice, connector approval, runtime forecast pulls, autonomous market mapping, trading logic, or any resolution behavior that assumes “NOAA data” is interchangeable across products. Do **not** treat city labels as safe stand-ins for station identity. Do **not** automate community-market resolution or catastrophe-adjacent impact markets in the early Weather Bot phase. fileciteturn0file0