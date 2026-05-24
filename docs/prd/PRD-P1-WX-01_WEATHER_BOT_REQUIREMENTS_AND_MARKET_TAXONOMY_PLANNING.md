# PRD-P1-WX-01: Weather Bot Requirements and Market Taxonomy Planning

## 1. Status and scope
- Status: Phase 1 weather bot planning ticket.
- Scope: requirements + taxonomy planning only.
- This document does **not** approve implementation, connectors, external API calls, runtime execution, trading, order placement, position sizing, or autonomy.
- This document is conceptual planning guidance for future tickets and research docs.

## 2. Strategic framing
PRD-P1-WX-01 explicitly frames the weather bot as **MEG’s first canonical event graph proving ground**, not as a narrow weather API feature.

The target intelligence flow is:
- real-world weather event
- → canonical weather event identity
- → venue-specific market mapping
- → resolution-risk classification
- → human-review output

Non-target flow (explicitly insufficient):
- weather API → forecast → trade

## 3. Roadmap position
This ticket establishes the first taxonomy/requirements foundation in the broader sequence:
- **PRD-P1-WX-01** (this document): requirements/taxonomy foundation.
- **PRD-P1-WX-02**: provider research + connector approval gate (still no connector implementation by default).
- **PRD-P1-WX-03** and **PRD-P1-WX-04**: config/secrets fail-closed and result/status/observability contracts.
- Later deep Weather Bot research document pack: mechanics, provider comparison, resolution-rule compatibility, canonical taxonomy depth, trap taxonomy, uncertainty/distribution concerns, and edge-case examples.
- Later Opus standalone Weather Bot PRD synthesis from approved planning artifacts.

## 4. Canonical weather event identity
Canonical weather event identity is conceptual and not a schema class in this ticket.

Minimum conceptual identity fields:
- domain
- event family
- location
- geographic precision
- date or time window
- timezone
- weather variable
- comparator
- threshold
- unit
- measurement source
- resolution authority
- venue-market references
- ambiguity flags
- resolution-risk flags
- human-readable event summary

Planning expectation:
- A canonical event identity must isolate real-world event meaning from venue wording.
- Identity precision should make mismatches explicit (for example city-wide wording vs station-specific wording).
- Identity is the anchor for later human-review output and no-trade reasoning.

## 5. Weather market taxonomy
The Phase 1 taxonomy should classify at least these families:

1. **Temperature threshold markets**
   - Resolves whether temperature crossed a threshold in a defined place/time window.
   - Key fields: location, geographic precision, weather variable, comparator/threshold, unit, window/timezone, measurement source.
   - Risks: station mismatch, unit confusion, timezone boundary ambiguity.
   - Phase 1 complexity: simple-to-moderate.

2. **Precipitation threshold markets**
   - Resolves whether precipitation amount met/exceeded threshold.
   - Key fields: threshold, unit, location precision, source/authority, window.
   - Risks: measurable-vs-threshold wording drift, source mismatch.
   - Phase 1 complexity: moderate.

3. **Snowfall markets**
   - Resolves snowfall depth/occurrence in defined area/window.
   - Key fields: weather variable subtype, threshold, unit, measurement source, location precision.
   - Risks: mixed precipitation interpretation, station coverage gaps.
   - Phase 1 complexity: moderate.

4. **Wind markets**
   - Resolves wind speed or gust thresholds.
   - Key fields: variable definition (sustained vs gust), threshold/unit, source, window.
   - Risks: variable-definition mismatch across venues.
   - Phase 1 complexity: moderate.

5. **Storm/hurricane markets**
   - Resolves named-event occurrence, landfall/location, category/intensity conditions.
   - Key fields: event family, geography precision, authority, window.
   - Risks: discretionary wording, authority mismatch, timeline ambiguity.
   - Phase 1 complexity: complex.

6. **Extreme weather markets**
   - Resolves occurrence of unusual or severe conditions (e.g., record events).
   - Key fields: comparator/threshold semantics, authority, location scope.
   - Risks: subjective wording and source dependency.
   - Phase 1 complexity: complex.

7. **Daily city/location binary markets**
   - Resolves yes/no daily condition for a place.
   - Key fields: location precision, window/timezone, variable definition.
   - Risks: vague location naming and window boundaries.
   - Phase 1 complexity: simple-to-moderate.

8. **Monthly or seasonal aggregate markets**
   - Resolves aggregate condition over longer interval.
   - Key fields: aggregation window, timezone, authority/source, threshold semantics.
   - Risks: delayed reporting, revisions, aggregation rule ambiguity.
   - Phase 1 complexity: complex.

9. **Source-dependent resolution markets**
   - Resolves based primarily on named source/authority output.
   - Key fields: measurement source, resolution authority, exact wording alignment.
   - Risks: source substitution invalidation and authority conflicts.
   - Phase 1 complexity: complex.

## 6. Venue-market mapping concepts
A single canonical event may map to one or more venue-specific markets with varying equivalence.

Mapping classes:
- exact equivalent markets
- near-equivalent markets
- related but non-equivalent markets

Mismatch and risk lenses:
- conflicting venue wording
- source mismatch
- location mismatch
- threshold mismatch
- window/timezone mismatch
- resolution authority mismatch

Illustrative non-equivalence example family:
- "NYC receives at least 1 inch of rain on May 28"
- "Central Park records at least 1 inch of rain on May 28"
- "LaGuardia records at least 1 inch of rain on May 28"
- "NYC receives measurable rain on May 28"

These are related but should not be auto-collapsed as identical because station, threshold, and wording semantics diverge.

## 7. Resolution-risk categories
PRD-P1-WX-01 defines resolution-risk taxonomy as core intelligence-layer planning:
- clean official-source resolution
- source mismatch risk
- measurement-station ambiguity
- location ambiguity
- timezone/window ambiguity
- threshold/comparator ambiguity
- unit conversion risk
- delayed reporting risk
- venue wording ambiguity
- cancellation/market invalidation risk
- subjective or discretionary resolution risk

Resolution-risk classification should directly feed later human-review outputs and no-trade/caution reasoning.

## 8. Human-review output expectations
Future reviewer-facing output (conceptual only in this ticket) should communicate:
- canonical event summary
- mapped venue markets
- market family
- event identity confidence
- resolution source
- resolution-risk flags
- ambiguity notes
- no-trade or caution reasons
- later provider compatibility notes
- concise reviewer-facing explanation

This ticket does not implement runtime output code or schema classes.

## 9. Explicit non-goals and approval gates
PRD-P1-WX-01 does **not** approve:
- weather API connectors
- connector implementation
- external API calls
- provider selection
- provider credentials
- forecast pulls
- forecast modeling
- probability modeling
- runtime scheduling
- runtime execution
- production monitoring
- trading strategy
- order placement
- position sizing
- autonomy
- live market execution
- final standalone Weather Bot PRD synthesis

Approval posture clarity:
- Weather/API connectors are not approved in PRD-P1-WX-01.
- External API calls are not approved in PRD-P1-WX-01.
- Runtime execution is not approved in PRD-P1-WX-01.
- Forecast pulls and forecast modeling are not approved in PRD-P1-WX-01.
- Trading strategy, order placement, and position sizing are not approved in PRD-P1-WX-01.
- Autonomy and live market execution are not approved in PRD-P1-WX-01.

## 10. Later-ticket handoff
Handoff boundaries are explicit:
- Provider research and connector approval evidence moves to **PRD-P1-WX-02**.
- Config/secrets fail-closed contract moves to **PRD-P1-WX-03**.
- Result/status/observability summary contract moves to **PRD-P1-WX-04**.
- Deep weather research pack moves to later dedicated weather research docs.
- Full standalone Weather Bot PRD moves to later Opus synthesis.

## 11. Acceptance criteria
This planning document is complete only if all are true:
- [x] canonical event graph framing is explicit.
- [x] canonical weather event identity is defined.
- [x] weather market taxonomy is defined.
- [x] venue-market mapping concepts are defined.
- [x] resolution-risk taxonomy is defined.
- [x] human-review expectations are defined.
- [x] non-goals and approval boundaries are explicit.
- [x] later-ticket handoff (WX-02/WX-03/WX-04 + deeper research + Opus synthesis) is explicit.
- [x] no connector/runtime/trading/order-placement/autonomy behavior is introduced.
