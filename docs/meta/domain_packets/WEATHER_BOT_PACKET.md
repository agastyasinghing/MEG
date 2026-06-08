# Weather Bot Context Packet

## Purpose

Provide compact Weather Bot context for fresh chats, ticket generation, and PR review without granting new implementation authority.

## Source-of-truth hierarchy

1. `AGENTS.md`
2. `docs/meta/MEG_ACTIVE_STATE.md`
3. Weather Bot PRDs, especially `docs/prd/PRD-P1-WX-STANDALONE_WEATHER_BOT_PRD.md`
4. Stage 2 skeleton and fixture PRDs
5. `docs/meta/MEG_TICKET_STYLE_GUIDE.md` and `docs/meta/MEG_PR_REVIEW_CHECKLIST.md`

## Current phase/status

- Stage 2 skeleton v1 complete.
- Static fixture planning completed by PR #194.
- Stage 2 synthetic static fixture implementation v1 is complete and closed out by PR #198 / PRD-P1-WX-STAGE2-FIXTURE-IMPLEMENTATION-CLOSEOUT-01.
- Stage 2 real source-backed fixture implementation v1 is complete and closed out by PR #204 / PRD-P1-WX-STAGE2-REAL-FIXTURE-IMPLEMENTATION-CLOSEOUT-01.
- Stage 2 historical-label loading/validation planning v1 is complete and closed out by PR #208 / PRD-P1-WX-STAGE2-HISTORICAL-LABEL-LOADING-PLAN-CLOSEOUT-01.
- No loader exists.
- No historical-label loading implementation is approved.
- No ingestion/scoring/backtesting/runtime/trading is approved.
- The synthetic fixture set is exactly three hand-authored JSON fixtures under `tests/fixtures/weather/stage2_historical_labels/`.
- The real source-backed fixture set is exactly two hand-authored source-backed JSON fixtures under `tests/fixtures/weather/stage2_real_source_backed_labels/`.
- The real fixture cap of at most 3 was preserved.
- The third real fixture was intentionally not fabricated.
- Old real-fixture planning/approval tests are successor-aware after PR #203.
- The next default posture is hold/checkpoint.

## Recent completed artifacts

- PR #191 covered targeted Stage 2 skeleton mapping-builder validation gaps.
- PR #192 closed out/checkpointed the Stage 2 skeleton and listed future gates without approval.
- PR #193 created the static fixture/data approval-request posture that allowed fixture planning to be requested after human approval.
- PR #194 completed static historical-label fixture planning.
- PR #198 / PRD-P1-WX-STAGE2-FIXTURE-IMPLEMENTATION-CLOSEOUT-01 closed out static fixture implementation v1.
- PR #203 made old real-fixture planning/approval tests successor-aware.
- PR #204 / PRD-P1-WX-STAGE2-REAL-FIXTURE-IMPLEMENTATION-CLOSEOUT-01 closed out real source-backed fixture implementation v1.
- PR #208 / PRD-P1-WX-STAGE2-HISTORICAL-LABEL-LOADING-PLAN-CLOSEOUT-01 closed out historical-label loading/validation planning v1 without creating a loader, modifying fixture files, or creating historical-label data/generated data.

## Current approved gate

- Stage 2 skeleton v1 is complete.
- Static fixture planning is complete.
- Stage 2 synthetic static fixture implementation v1 is complete and closed out.
- Exactly three synthetic, hand-authored JSON fixtures are the complete synthetic fixture set for the closed-out synthetic subphase.
- Stage 2 real source-backed fixture implementation v1 is complete and closed out.
- Exactly two real source-backed fixture JSON files exist as hand-authored, source-backed JSON fixtures and are the complete real fixture set for the closed-out real subphase.
- The real fixture cap of at most 3 was preserved, and the third real fixture was intentionally not fabricated.
- Stage 2 historical-label loading/validation planning v1 is complete and closed out.
- No loader exists.
- Completion of these fixture and planning subphases does not authorize loader implementation, historical-label loading implementation, ingestion, scoring, backtesting, runtime, trading, order placement, autonomy, production behavior, or later Weather Bot gates.

## Next possible gate

- The next default Weather Bot posture is hold/checkpoint unless a concrete loading-planning gap is found or the user explicitly chooses a later approval/request/planning gate.
- If the user explicitly chooses to continue, the next work must be a separate approval/request/planning gate or targeted refinement if a concrete loading-planning gap exists, not direct implementation/ingestion/scoring/runtime/trading.
- Continued work must not proceed directly to loader implementation, historical-label loading implementation, ingestion, scoring, backtesting, runtime, trading, order placement, autonomy, or production behavior.
- Do not present real fixture implementation or historical-label loading implementation as the next default gate because real fixture implementation v1 and historical-label loading/validation planning v1 are complete and closed out.

## Explicitly not approved

- Loader implementation is not approved.
- Historical-label loading implementation is not approved.
- Real historical-label data expansion is not approved.
- Generated data is not approved.
- Ingestion is not approved.
- Provider/source integration and provider/API connectors are not approved.
- External API calls are not approved.
- Credentials/secrets/config loading is not approved.
- Forecast pulls are not approved.
- Scoring is not approved.
- Probability scoring is not approved.
- Backtesting is not approved.
- Paper simulation is not approved.
- Runtime observation is not approved.
- Trading is not approved.
- Order placement is not approved.
- Autonomy is not approved.
- Production behavior is not approved.
- C++/Rust runtime components are not approved.

## Stage 2 skeleton summary

- The Stage 2 skeleton v1 is complete.
- The skeleton accepts supplied metadata and preserves static review boundaries.
- It must remain fail-closed around required metadata and closed-set values.
- Do not modify Weather Bot behavior while handling docs/static-test operations tickets.

## Fixture track summary

- Stage 2 synthetic static fixture implementation v1 is complete and closed out.
- Exactly three synthetic, hand-authored JSON fixtures exist under `tests/fixtures/weather/stage2_historical_labels/`.
- The three synthetic fixtures remain the complete synthetic fixture set for that closed-out subphase.
- Stage 2 real source-backed fixture implementation v1 is complete and closed out.
- Exactly two real source-backed fixture JSON files exist under `tests/fixtures/weather/stage2_real_source_backed_labels/`.
- The two real fixtures remain the complete hand-authored source-backed fixture set for that closed-out subphase.
- The at-most-3 real fixture cap was preserved, and the third real fixture was intentionally not fabricated.
- Old real-fixture planning/approval tests are successor-aware after PR #203.
- Stage 2 historical-label loading/validation planning v1 is complete and closed out.
- No loader exists.
- No historical-label loading implementation, ingestion, scoring, backtesting, runtime, trading, order placement, autonomy, or production behavior is approved by the fixture and planning closeouts.
- Hold/checkpoint is the recommended posture unless a concrete loading-planning gap is found or the user explicitly chooses a later approval/request/planning gate.

## Closed-set/static-test pitfalls

- Define exact allowed values.
- Parse actual values only from bounded machine-checkable sections.
- Reject hybrid/custom values.
- Do not use optional-missing exceptions unless explicitly approved.
- Do not treat forbidden prose examples as actual values.

## Weather Bot ticket conventions

- State current gate and next possible gate.
- Include allowed files and do-not-modify lists.
- Keep docs/static-test tickets separate from implementation tickets.
- Preserve non-approval language for later phases.
- Treat any continued work after fixture and historical-label loading/validation planning closeout as a separately approved later gate, not as direct implementation authority.

## Weather Bot PR review additions

- Confirm no Weather Bot runtime/source behavior changed in docs/static-test tickets.
- Confirm no loader, historical-label loading implementation, real historical-label data expansion, generated data, ingestion, connectors, external API calls, scoring/backtesting, runtime observation, trading, order placement, autonomy, or production behavior was added.
- Confirm closed-set/static-test parsing is section-scoped.

## Relationship to future phases

- Targeted loading-planning refinement: only if a concrete gap is found and scoped as a separate gate.
- Loader implementation: not approved unless separately requested/planned/approved.
- Historical-label loading implementation: not approved unless separately requested/planned/approved.
- Ingestion: not approved by Stage 2 skeleton, fixture planning, fixture implementation, fixture closeout, or historical-label loading/validation planning closeout.
- Provider/source integration: not approved.
- Scoring/backtesting: not approved.
- Paper simulation: not approved.
- Runtime observation: not approved.
- Trading/order/autonomy: not approved.
