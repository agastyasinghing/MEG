# Weather Bot Context Packet

## Purpose

Provide compact Weather Bot context for fresh chats, ticket generation, and PR review without granting new implementation authority.

## Source-of-truth hierarchy

1. `AGENTS.md`
2. `docs/meta/MEG_ACTIVE_STATE.md`
3. Weather Bot PRDs, especially `docs/prd/PRD-P1-WX-STANDALONE_WEATHER_BOT_PRD.md`
4. Stage 2 skeleton, fixture, loading/validation, ingestion-boundary-planning, static-ingestion-boundary-skeleton, and real-ingestion-boundary-planning PRDs
5. `docs/meta/MEG_TICKET_STYLE_GUIDE.md` and `docs/meta/MEG_PR_REVIEW_CHECKLIST.md`

## Current phase/status

- Stage 2 skeleton v1 complete.
- Static fixture planning completed by PR #194.
- Stage 2 synthetic static fixture implementation v1 is complete and closed out by PR #198 / PRD-P1-WX-STAGE2-FIXTURE-IMPLEMENTATION-CLOSEOUT-01.
- Stage 2 real source-backed fixture implementation v1 is complete and closed out by PR #204 / PRD-P1-WX-STAGE2-REAL-FIXTURE-IMPLEMENTATION-CLOSEOUT-01.
- Stage 2 historical-label loading/validation planning v1 is complete and closed out by PR #208 / PRD-P1-WX-STAGE2-HISTORICAL-LABEL-LOADING-PLAN-CLOSEOUT-01.
- Stage 2 static historical-label loading/validation implementation v1 is complete and closed out by PR #212 / PRD-P1-WX-STAGE2-HISTORICAL-LABEL-LOADING-IMPLEMENTATION-CLOSEOUT-01.
- Stage 2 ingestion boundary planning v1 is complete and closed out by PR #217 / PRD-P1-WX-STAGE2-INGESTION-PLAN-CLOSEOUT-01.
- Stage 2 static ingestion boundary skeleton v1 is complete and closed out by PR #221 / PRD-P1-WX-STAGE2-INGESTION-IMPLEMENTATION-CLOSEOUT-01.
- Real ingestion boundary planning v1 is complete and closed out by PR #225 / PRD-P1-WX-STAGE2-REAL-INGESTION-PLAN-CLOSEOUT-01.
- PRD-P1-WX-STAGE2-REAL-INGESTION-PLAN-01 is planning-only.
- `meg/weather/stage2/ingestion_boundary.py` exists as static validation only.
- The static ingestion boundary skeleton validates caller-supplied already-human-reviewed descriptor mappings only.
- The static ingestion boundary skeleton is not real ingestion.
- The static ingestion boundary skeleton is not provider/source integration.
- The static ingestion boundary skeleton is not source fetching.
- The static ingestion boundary skeleton is not external API calls.
- The static ingestion boundary skeleton is not scoring/backtesting/runtime/trading.
- The ingestion plan is planning vocabulary only.
- The real ingestion boundary planning is planning-only.
- The real ingestion boundary planning closeout does not approve real ingestion implementation.
- The real ingestion boundary planning closeout does not approve provider/source integration.
- The real ingestion boundary planning closeout does not approve source fetching.
- The real ingestion boundary planning closeout does not approve external API calls.
- The real ingestion boundary planning closeout does not approve credentials/secrets/config loading.
- The real ingestion boundary planning closeout does not approve forecast pulls.
- The real ingestion boundary planning closeout does not approve scoring/backtesting/runtime/trading/order placement/autonomy.
- The ingestion plan is not ingestion implementation.
- The ingestion plan is not provider/source integration.
- The ingestion plan is not source fetching.
- The ingestion plan is not external API calls.
- The ingestion plan is not scoring/backtesting/runtime/trading.
- The static loader exists at `meg/weather/stage2/historical_label_loader.py`.
- The loader is static validation only.
- The loader is not ingestion, provider/source integration, scoring, backtesting, runtime observation, trading, or production behavior.
- No real ingestion, provider/source integration, source fetching, external API calls, scoring, backtesting, runtime, trading, order placement, autonomy, or production behavior is approved.
- No real ingestion implementation, provider/source integration, source fetching, external API calls, scoring, backtesting, runtime, trading, order placement, autonomy, or production behavior is approved.
- No ingestion implementation, provider/source integration, source fetching, external API calls, scoring, backtesting, runtime, trading, order placement, autonomy, or production behavior is approved.
- The synthetic fixture set is exactly three hand-authored JSON fixtures under `tests/fixtures/weather/stage2_historical_labels/`.
- The real source-backed fixture set is exactly two hand-authored source-backed JSON fixtures under `tests/fixtures/weather/stage2_real_source_backed_labels/`.
- The real fixture cap of at most 3 was preserved.
- The third real fixture was intentionally not fabricated.
- Old real-fixture planning/approval tests are successor-aware after PR #203.
- The next default posture is hold/checkpoint.
- If the user explicitly chooses to continue, the next work must be a separate approval/request/planning gate or targeted refinement if a concrete real ingestion planning gap exists, not direct real ingestion/connectors/source fetching/scoring/runtime/trading.

## Recent completed artifacts

- PR #191 covered targeted Stage 2 skeleton mapping-builder validation gaps.
- PR #192 closed out/checkpointed the Stage 2 skeleton and listed future gates without approval.
- PR #193 created the static fixture/data approval-request posture that allowed fixture planning to be requested after human approval.
- PR #194 completed static historical-label fixture planning.
- PR #198 / PRD-P1-WX-STAGE2-FIXTURE-IMPLEMENTATION-CLOSEOUT-01 closed out static fixture implementation v1.
- PR #203 made old real-fixture planning/approval tests successor-aware.
- PR #204 / PRD-P1-WX-STAGE2-REAL-FIXTURE-IMPLEMENTATION-CLOSEOUT-01 closed out real source-backed fixture implementation v1.
- PR #208 / PRD-P1-WX-STAGE2-HISTORICAL-LABEL-LOADING-PLAN-CLOSEOUT-01 closed out historical-label loading/validation planning v1 without creating a loader, modifying fixture files, or creating historical-label data/generated data.
- PR #212 / PRD-P1-WX-STAGE2-HISTORICAL-LABEL-LOADING-IMPLEMENTATION-CLOSEOUT-01 closed out static historical-label loading/validation implementation v1; the loader module exists, all three synthetic and both real source-backed fixtures load through the static loader, fixture README/JSON files were not modified, and no historical-label data/generated data was created.
- PR #217 / PRD-P1-WX-STAGE2-INGESTION-PLAN-CLOSEOUT-01 closed out ingestion boundary planning v1; the planning-only vocabulary and boundaries were captured without creating or approving ingestion implementation, provider/source integration, source fetching, external API calls, scoring, backtesting, runtime, trading, fixture changes, historical-label data, or generated data.
- PR #221 / PRD-P1-WX-STAGE2-INGESTION-IMPLEMENTATION-CLOSEOUT-01 closed out static ingestion boundary skeleton v1; `meg/weather/stage2/ingestion_boundary.py` exists as static validation only for caller-supplied already-human-reviewed descriptor mappings, not real ingestion, provider/source integration, source fetching, external API calls, scoring/backtesting/runtime/trading, fixture changes, historical-label data, or generated data.
- PR #225 / PRD-P1-WX-STAGE2-REAL-INGESTION-PLAN-CLOSEOUT-01 closed out real ingestion boundary planning v1; PRD-P1-WX-STAGE2-REAL-INGESTION-PLAN-01 remains planning-only and recorded planning-only source-intake vocabulary and handoff rules without approving real ingestion implementation, provider/source integration, source fetching, external API calls, credentials/secrets/config loading, forecast pulls, scoring/backtesting/runtime/trading/order placement/autonomy, or production behavior.

## Current approved gate

- Stage 2 skeleton v1 is complete.
- Static fixture planning is complete.
- Stage 2 synthetic static fixture implementation v1 is complete and closed out.
- Exactly three synthetic, hand-authored JSON fixtures are the complete synthetic fixture set for the closed-out synthetic subphase.
- Stage 2 real source-backed fixture implementation v1 is complete and closed out.
- Exactly two real source-backed fixture JSON files exist as hand-authored, source-backed JSON fixtures and are the complete real fixture set for the closed-out real subphase.
- The real fixture cap of at most 3 was preserved, and the third real fixture was intentionally not fabricated.
- Stage 2 historical-label loading/validation planning v1 is complete and closed out.
- Stage 2 static historical-label loading/validation implementation v1 is complete and closed out.
- Stage 2 ingestion boundary planning v1 is complete and closed out.
- Stage 2 static ingestion boundary skeleton v1 is complete and closed out.
- Real ingestion boundary planning v1 is complete and closed out.
- PRD-P1-WX-STAGE2-REAL-INGESTION-PLAN-01 is planning-only.
- `meg/weather/stage2/ingestion_boundary.py` exists as static validation only.
- The static ingestion boundary skeleton validates caller-supplied already-human-reviewed descriptor mappings only.
- The static ingestion boundary skeleton is not real ingestion.
- The static ingestion boundary skeleton is not provider/source integration.
- The static ingestion boundary skeleton is not source fetching.
- The static ingestion boundary skeleton is not external API calls.
- The static ingestion boundary skeleton is not scoring/backtesting/runtime/trading.
- The ingestion plan is planning vocabulary only.
- The real ingestion boundary planning is planning-only.
- The real ingestion boundary planning closeout does not approve real ingestion implementation.
- The real ingestion boundary planning closeout does not approve provider/source integration.
- The real ingestion boundary planning closeout does not approve source fetching.
- The real ingestion boundary planning closeout does not approve external API calls.
- The real ingestion boundary planning closeout does not approve credentials/secrets/config loading.
- The real ingestion boundary planning closeout does not approve forecast pulls.
- The real ingestion boundary planning closeout does not approve scoring/backtesting/runtime/trading/order placement/autonomy.
- The ingestion plan is not ingestion implementation.
- The ingestion plan is not provider/source integration.
- The ingestion plan is not source fetching.
- The ingestion plan is not external API calls.
- The ingestion plan is not scoring/backtesting/runtime/trading.
- The static loader exists at `meg/weather/stage2/historical_label_loader.py`.
- The static loader is static validation only.
- Completion of these fixture, loading/validation, static loader, ingestion boundary planning, and static ingestion boundary skeleton subphases does not authorize real ingestion, ingestion implementation, provider/source integration, source fetching, external API calls, scoring, backtesting, runtime observation, trading, order placement, autonomy, production behavior, or later Weather Bot gates.

## Next possible gate

- The next default Weather Bot posture is hold/checkpoint unless a concrete real ingestion planning gap is found or the user explicitly chooses a later approval/request/planning gate.
- If the user explicitly chooses to continue, the next work must be a separate approval/request/planning gate or targeted refinement if a concrete real ingestion planning gap exists, not direct real ingestion/connectors/source fetching/scoring/runtime/trading.
- Continued work must not proceed directly to ingestion implementation, connectors, provider/source integration, source fetching, scoring, backtesting, runtime observation, trading, order placement, autonomy, or production behavior.
- Do not present real ingestion implementation, provider/source connectors, source fetching, scoring, backtesting, runtime, trading, order placement, autonomy, or production behavior as approved or next by default because real ingestion boundary planning v1 is complete and closed out.

## Explicitly not approved

- Loader expansion is not approved.
- Real historical-label data expansion is not approved.
- Generated data is not approved.
- Ingestion implementation is not approved.
- Ingestion is not approved.
- Provider/source integration and provider/API connectors are not approved.
- Provider/source connector implementation is not approved.
- Source fetching is not approved.
- External API calls are not approved.
- Credentials/secrets/config loading is not approved.
- Forecast pulls are not approved.
- Scraping/polling/streaming is not approved.
- Scheduling/queues/jobs is not approved.
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
- Stage 2 static historical-label loading/validation implementation v1 is complete and closed out.
- Stage 2 ingestion boundary planning v1 is complete and closed out.
- Stage 2 static ingestion boundary skeleton v1 is complete and closed out.
- Real ingestion boundary planning v1 is complete and closed out.
- PRD-P1-WX-STAGE2-REAL-INGESTION-PLAN-01 is planning-only.
- `meg/weather/stage2/ingestion_boundary.py` exists as static validation only.
- The static ingestion boundary skeleton validates caller-supplied already-human-reviewed descriptor mappings only.
- The static ingestion boundary skeleton is not real ingestion, provider/source integration, source fetching, external API calls, scoring/backtesting/runtime/trading, order placement, autonomy, or production behavior.
- The ingestion plan is planning vocabulary only.
- The real ingestion boundary planning is planning-only.
- The real ingestion boundary planning closeout does not approve real ingestion implementation.
- The real ingestion boundary planning closeout does not approve provider/source integration.
- The real ingestion boundary planning closeout does not approve source fetching.
- The real ingestion boundary planning closeout does not approve external API calls.
- The real ingestion boundary planning closeout does not approve credentials/secrets/config loading.
- The real ingestion boundary planning closeout does not approve forecast pulls.
- The real ingestion boundary planning closeout does not approve scoring/backtesting/runtime/trading/order placement/autonomy.
- The ingestion plan is not ingestion implementation.
- The ingestion plan is not provider/source integration.
- The ingestion plan is not source fetching.
- The ingestion plan is not external API calls.
- The ingestion plan is not scoring/backtesting/runtime/trading.
- The static loader exists at `meg/weather/stage2/historical_label_loader.py`.
- The loader is static validation only and is not ingestion, provider/source integration, scoring, backtesting, runtime observation, trading, or production behavior.
- No real ingestion, provider/source integration, source fetching, external API calls, scoring, backtesting, runtime, trading, order placement, autonomy, or production behavior is approved by the fixture, loading/validation, static loader, ingestion boundary planning, or static ingestion boundary skeleton closeouts.
- No ingestion implementation, provider/source integration, source fetching, external API calls, scoring, backtesting, runtime, trading, order placement, autonomy, or production behavior is approved by the fixture, loading/validation, static loader, ingestion boundary planning, or static ingestion boundary skeleton closeouts.
- Hold/checkpoint is the recommended posture unless a concrete real ingestion planning gap is found or the user explicitly chooses a later approval/request/planning gate. If the user explicitly chooses to continue, the next work must be a separate approval/request/planning gate or targeted refinement if a concrete real ingestion planning gap exists, not direct real ingestion/connectors/source fetching/scoring/runtime/trading.

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
- Treat any continued work after fixture, historical-label loading/validation planning, static loader implementation, ingestion boundary planning closeout, static ingestion boundary skeleton closeout, and real ingestion boundary planning closeout as a separately approved later gate, not as ingestion/scoring/runtime/trading authority.

## Weather Bot PR review additions

- Confirm no Weather Bot runtime/source behavior changed in docs/static-test tickets.
- Confirm no loader expansion, real historical-label data expansion, generated data, ingestion implementation, connectors, source fetching, external API calls, scoring/backtesting, runtime observation, trading, order placement, autonomy, or production behavior was added.
- Confirm closed-set/static-test parsing is section-scoped.

## Relationship to future phases

- Targeted loader-validation refinement: only if a concrete gap is found and scoped as a separate gate.
- Loader expansion: not approved unless separately requested/planned/approved.
- Ingestion implementation: not approved by Stage 2 skeleton, fixture planning, fixture implementation, fixture closeout, historical-label loading/validation planning closeout, static loader implementation closeout, ingestion boundary planning closeout, static ingestion boundary skeleton closeout, or real ingestion boundary planning closeout.
- Ingestion: not approved by Stage 2 skeleton, fixture planning, fixture implementation, fixture closeout, historical-label loading/validation planning closeout, static loader implementation closeout, ingestion boundary planning closeout, static ingestion boundary skeleton closeout, or real ingestion boundary planning closeout.
- Provider/source integration: not approved.
- Scoring/backtesting: not approved.
- Paper simulation: not approved.
- Runtime observation: not approved.
- Trading/order/autonomy: not approved.
