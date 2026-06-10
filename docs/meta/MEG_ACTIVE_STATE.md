# MEG Active State

This is the first working-memory file to read after `AGENTS.md`.

## Current active project
- MEG repo-native project operations and Weather Bot gated planning.

## Current active area
- MEG Weather Bot Stage 2 post-real-ingestion-boundary-planning closeout checkpoint track.

## Current active phase
- MEG-OPS-01 established the repo-native orchestration layer for durable project handoff.
- The current active Weather Bot area is the post-real-ingestion-boundary-planning closeout checkpoint.
- Stage 2 skeleton v1 is complete and closed out.
- Stage 2 synthetic static fixture implementation v1 is complete and closed out.
- Stage 2 real source-backed fixture implementation v1 is complete and closed out.
- Stage 2 historical-label loading/validation planning v1 is complete and closed out.
- Stage 2 static historical-label loading/validation implementation v1 is complete and closed out.
- Stage 2 ingestion boundary planning v1 is complete and closed out.
- Stage 2 static ingestion boundary skeleton v1 is complete and closed out.
- Stage 2 real ingestion boundary planning v1 is complete and closed out.
- PRD-P1-WX-STAGE2-FIXTURE-IMPLEMENTATION-CLOSEOUT-01 closed out the static fixture implementation subphase after PR #198.
- PRD-P1-WX-STAGE2-REAL-FIXTURE-IMPLEMENTATION-CLOSEOUT-01 closed out the real source-backed fixture implementation subphase after PR #204.
- PRD-P1-WX-STAGE2-HISTORICAL-LABEL-LOADING-PLAN-CLOSEOUT-01 closed out the historical-label loading/validation planning subphase after PR #208.
- PRD-P1-WX-STAGE2-HISTORICAL-LABEL-LOADING-IMPLEMENTATION-CLOSEOUT-01 closed out the static loader/validator implementation subphase after PR #212.
- PRD-P1-WX-STAGE2-INGESTION-PLAN-CLOSEOUT-01 closed out the ingestion boundary planning subphase after PR #217.
- PRD-P1-WX-STAGE2-INGESTION-IMPLEMENTATION-CLOSEOUT-01 closed out the static ingestion boundary skeleton subphase after PR #221.
- PRD-P1-WX-STAGE2-REAL-INGESTION-PLAN-CLOSEOUT-01 closed out the real ingestion boundary planning subphase after PR #225.
- PRD-P1-WX-STAGE2-REAL-INGESTION-PLAN-01 remains a planning-only artifact.
- The ingestion boundary planning artifact defined planning-only vocabulary, allowed/prohibited future source categories, no-lookahead safeguards, fixture/loader separation rules, fail-closed blockers, and later handoff gates.
- The real ingestion boundary planning artifact defined planning-only source-intake vocabulary, provider/source category taxonomy, allowed/prohibited source-intake modes, pre-fetch approval gates, provenance/access-date/retrieval-context requirements, no-lookahead safeguards, separation rules, fail-closed blockers, and handoff gates.
- `meg/weather/stage2/historical_label_loader.py` exists as the narrow static historical-label fixture loader/validator module.
- The loader is limited to explicit static fixture validation.
- The loader reads only caller-supplied paths under the two allowlisted fixture directories.
- The directory loader is non-recursive.
- The loader reuses the existing Stage 2 metadata validator.
- All three synthetic and both real source-backed fixtures load through the static loader.
- Exactly three static synthetic fixture JSON files exist under `tests/fixtures/weather/stage2_historical_labels/`.
- Exactly two real source-backed fixture JSON files exist under `tests/fixtures/weather/stage2_real_source_backed_labels/`.
- The fixture count cap of at most 3 real source-backed fixtures was preserved.
- The third real fixture was intentionally not fabricated.
- Old real-fixture planning/approval tests are successor-aware after PR #203.

## Latest merged PR
- PR #225 / PRD-P1-WX-STAGE2-REAL-INGESTION-PLAN-CLOSEOUT-01 closed out the real ingestion boundary planning subphase.

## Latest reviewed PR
- PR #225 / PRD-P1-WX-STAGE2-REAL-INGESTION-PLAN-CLOSEOUT-01 is the latest Weather Bot closeout/checkpoint item represented by this active state.
- PR #221 / PRD-P1-WX-STAGE2-INGESTION-IMPLEMENTATION-CLOSEOUT-01 remains represented as the static ingestion boundary skeleton closeout.
- PR #217 / PRD-P1-WX-STAGE2-INGESTION-PLAN-CLOSEOUT-01 remains represented as the ingestion boundary planning closeout.
- PR #212 / PRD-P1-WX-STAGE2-HISTORICAL-LABEL-LOADING-IMPLEMENTATION-CLOSEOUT-01 remains represented as the static historical-label loading/validation implementation closeout.
- PR #208 / PRD-P1-WX-STAGE2-HISTORICAL-LABEL-LOADING-PLAN-CLOSEOUT-01 remains represented as the historical-label loading/validation planning closeout.
- PR #203 is represented as the blocker fix that made old real-fixture planning/approval tests successor-aware after approved real-fixture implementation.
- PR #195 / MEG-OPS-01 remains the latest reviewed ops-docs handoff sequence item recorded here.

## Current approved gate
- Stage 2 skeleton v1 is complete and closed out.
- Static fixture planning was completed by PR #194.
- Stage 2 static fixture implementation v1 is complete and closed out by PR #198 / PRD-P1-WX-STAGE2-FIXTURE-IMPLEMENTATION-CLOSEOUT-01.
- The complete synthetic fixture set is exactly three static synthetic, hand-authored JSON fixtures under `tests/fixtures/weather/stage2_historical_labels/`.
- Stage 2 real source-backed fixture implementation v1 is complete and closed out by PR #204 / PRD-P1-WX-STAGE2-REAL-FIXTURE-IMPLEMENTATION-CLOSEOUT-01.
- The complete real source-backed fixture set is exactly two hand-authored source-backed JSON fixtures under `tests/fixtures/weather/stage2_real_source_backed_labels/`.
- The real fixture count cap of at most 3 was preserved, and the third real fixture was intentionally not fabricated.
- Stage 2 historical-label loading/validation planning v1 is complete and closed out by PR #208 / PRD-P1-WX-STAGE2-HISTORICAL-LABEL-LOADING-PLAN-CLOSEOUT-01.
- PRD-P1-WX-STAGE2-HISTORICAL-LABEL-LOADING-PLAN-CLOSEOUT-01 closed out the historical-label loading/validation planning subphase.
- Stage 2 static historical-label loading/validation implementation v1 is complete and closed out by PR #212 / PRD-P1-WX-STAGE2-HISTORICAL-LABEL-LOADING-IMPLEMENTATION-CLOSEOUT-01.
- PRD-P1-WX-STAGE2-HISTORICAL-LABEL-LOADING-IMPLEMENTATION-CLOSEOUT-01 closed out the static loader/validator implementation subphase.
- Stage 2 ingestion boundary planning v1 is complete and closed out by PR #217 / PRD-P1-WX-STAGE2-INGESTION-PLAN-CLOSEOUT-01.
- PRD-P1-WX-STAGE2-INGESTION-PLAN-CLOSEOUT-01 closed out the ingestion boundary planning subphase.
- Stage 2 static ingestion boundary skeleton v1 is complete and closed out by PR #221 / PRD-P1-WX-STAGE2-INGESTION-IMPLEMENTATION-CLOSEOUT-01.
- PRD-P1-WX-STAGE2-INGESTION-IMPLEMENTATION-CLOSEOUT-01 closed out the static ingestion boundary skeleton subphase.
- Stage 2 real ingestion boundary planning v1 is complete and closed out by PR #225 / PRD-P1-WX-STAGE2-REAL-INGESTION-PLAN-CLOSEOUT-01.
- PRD-P1-WX-STAGE2-REAL-INGESTION-PLAN-CLOSEOUT-01 closed out the real ingestion boundary planning subphase after PR #225.
- PRD-P1-WX-STAGE2-REAL-INGESTION-PLAN-01 remains a planning-only artifact.
- The real ingestion boundary planning artifact defined planning-only source-intake vocabulary, provider/source category taxonomy, allowed/prohibited source-intake modes, pre-fetch approval gates, provenance/access-date/retrieval-context requirements, no-lookahead safeguards, separation rules, fail-closed blockers, and handoff gates.
- `meg/weather/stage2/ingestion_boundary.py` exists as a static validator only.
- The static ingestion boundary skeleton validates caller-supplied already-human-reviewed descriptor mappings only.
- It uses closed vocabularies.
- It returns pass, caution, or blocked validation results.
- It is stdlib-only.
- It does not read files, write files, call services, open network connections, load credentials/secrets/config, create schemas, or start jobs.
- The ingestion boundary planning artifact defined planning-only vocabulary, allowed/prohibited future source categories, no-lookahead safeguards, fixture/loader separation rules, fail-closed blockers, and later handoff gates.
- `meg/weather/stage2/historical_label_loader.py` exists.
- The loader is limited to explicit static fixture validation.
- The loader reads only caller-supplied paths under the two allowlisted fixture directories: `tests/fixtures/weather/stage2_historical_labels/` and `tests/fixtures/weather/stage2_real_source_backed_labels/`.
- The directory loader is non-recursive.
- The loader reuses the existing Stage 2 metadata validator.
- All three synthetic and both real source-backed fixtures load through the static loader.
- No fixture README/JSON files were modified.
- No historical-label data files or generated data were created.
- No real ingestion was created or approved.
- No real ingestion implementation was created or approved.
- No ingestion implementation was created or approved.
- No provider/API connectors were created or approved.
- No provider/source connector implementation was created or approved.
- No source fetching was created or approved.
- No external API calls were created or approved.
- No credentials/secrets/config loading was created or approved.
- No forecast pulls were created or approved.
- No scraping/polling/streaming/scheduling/queues/jobs/background tasks were created or approved.
- No scoring/backtesting/runtime/trading/order placement/autonomy was created or approved.
- No loader expansion was created or approved.
- No scoring/backtesting/runtime/trading/order placement/autonomy is approved.
- This closeout does not approve real ingestion, ingestion implementation, provider/source connector implementation, source fetching, external API calls, scoring, backtesting, runtime, trading, order placement, autonomy, production behavior, or any later Weather Bot gate.

## Next possible gate
- Current recommended posture: hold/checkpoint unless a concrete real ingestion planning gap is found or the user explicitly chooses a later approval/request/planning gate.
- Current next possible Weather Bot action, if the user explicitly chooses to continue, is a separately approved later gate only.
- Examples of separately approved later gates include targeted real ingestion planning refinement if a concrete planning gap exists, or a later approval-request/planning gate chosen by the user.
- Do not present ingestion implementation, provider/source connectors, source fetching, scoring, backtesting, runtime, trading, order placement, autonomy, or production behavior as approved or next by default.

## Explicitly not approved
- Loader expansion is not approved.
- Ingestion implementation is not approved.
- Ingestion is not approved.
- Real historical-label data expansion is not approved.
- Generated data is not approved.
- Provider/API connectors are not approved.
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
- Real ingestion implementation is not approved.
- Do not present real ingestion implementation, provider/source connectors, source fetching, scoring, backtesting, runtime, trading, order placement, autonomy, or production behavior as approved or next by default.

## Current controlling docs
- `AGENTS.md`
- `docs/meta/MEG_ACTIVE_STATE.md`
- `docs/meta/MEG_CONTEXT_ROUTER.md`
- `docs/meta/MEG_WORKFLOW_PLAYBOOK.md`
- `docs/meta/MEG_TICKET_STYLE_GUIDE.md`
- `docs/meta/MEG_PR_REVIEW_CHECKLIST.md`
- `docs/meta/MEG_PHASE_LEDGER.md`
- `docs/meta/domain_packets/WEATHER_BOT_PACKET.md`
- `docs/meta/domain_packets/CORE_WORKFLOW_PACKET.md`
- `docs/prd/PRD-P1-WX-STANDALONE_WEATHER_BOT_PRD.md`
- `docs/prd/PRD-P1-WX-STAGE2-SKELETON-CLOSEOUT-01_STAGE_2_SKELETON_CLOSEOUT_CHECKPOINT.md`
- `docs/prd/PRD-P1-WX-STAGE2-FIXTURE-APPROVAL-01_STATIC_FIXTURE_DATA_APPROVAL_REQUEST.md`
- `docs/prd/PRD-P1-WX-STAGE2-FIXTURE-PLAN-01_STATIC_HISTORICAL_LABEL_FIXTURE_PLANNING.md`
- `docs/prd/PRD-P1-WX-STAGE2-FIXTURE-IMPLEMENTATION-01_STATIC_HISTORICAL_LABEL_FIXTURE_IMPLEMENTATION.md`
- `docs/prd/PRD-P1-WX-STAGE2-FIXTURE-IMPLEMENTATION-CLOSEOUT-01_STATIC_FIXTURE_IMPLEMENTATION_CLOSEOUT_CHECKPOINT.md`
- `docs/prd/PRD-P1-WX-STAGE2-REAL-FIXTURE-IMPLEMENTATION-01_REAL_SOURCE_BACKED_FIXTURE_IMPLEMENTATION.md`
- `docs/prd/PRD-P1-WX-STAGE2-REAL-FIXTURE-IMPLEMENTATION-CLOSEOUT-01_REAL_SOURCE_BACKED_FIXTURE_IMPLEMENTATION_CLOSEOUT_CHECKPOINT.md`
- `docs/prd/PRD-P1-WX-STAGE2-HISTORICAL-LABEL-LOADING-APPROVAL-01_HISTORICAL_LABEL_LOADING_VALIDATION_PLANNING_APPROVAL_REQUEST.md`
- `docs/prd/PRD-P1-WX-STAGE2-HISTORICAL-LABEL-LOADING-PLAN-01_STATIC_HISTORICAL_LABEL_LOADING_VALIDATION_PLANNING.md`
- `docs/prd/PRD-P1-WX-STAGE2-HISTORICAL-LABEL-LOADING-PLAN-CLOSEOUT-01_HISTORICAL_LABEL_LOADING_VALIDATION_PLANNING_CLOSEOUT_CHECKPOINT.md`
- `docs/prd/PRD-P1-WX-STAGE2-HISTORICAL-LABEL-LOADING-IMPLEMENTATION-APPROVAL-01_HISTORICAL_LABEL_LOADING_VALIDATION_IMPLEMENTATION_APPROVAL_REQUEST.md`
- `docs/prd/PRD-P1-WX-STAGE2-HISTORICAL-LABEL-LOADING-IMPLEMENTATION-01_STATIC_HISTORICAL_LABEL_LOADING_VALIDATION_IMPLEMENTATION.md`
- `docs/prd/PRD-P1-WX-STAGE2-HISTORICAL-LABEL-LOADING-IMPLEMENTATION-CLOSEOUT-01_STATIC_HISTORICAL_LABEL_LOADING_VALIDATION_IMPLEMENTATION_CLOSEOUT_CHECKPOINT.md`
- `docs/prd/PRD-P1-WX-STAGE2-INGESTION-PLANNING-APPROVAL-01_INGESTION_PLANNING_APPROVAL_REQUEST.md`
- `docs/prd/PRD-P1-WX-STAGE2-INGESTION-PLAN-01_INGESTION_BOUNDARY_PLANNING.md`
- `docs/prd/PRD-P1-WX-STAGE2-INGESTION-PLAN-CLOSEOUT-01_INGESTION_BOUNDARY_PLANNING_CLOSEOUT_CHECKPOINT.md`
- `docs/prd/PRD-P1-WX-STAGE2-INGESTION-IMPLEMENTATION-APPROVAL-01_INGESTION_IMPLEMENTATION_APPROVAL_REQUEST.md`
- `docs/prd/PRD-P1-WX-STAGE2-INGESTION-IMPLEMENTATION-01_STATIC_INGESTION_BOUNDARY_SKELETON.md`
- `docs/prd/PRD-P1-WX-STAGE2-INGESTION-IMPLEMENTATION-CLOSEOUT-01_STATIC_INGESTION_BOUNDARY_SKELETON_CLOSEOUT_CHECKPOINT.md`

## Current Weather Bot status summary
- Stage 2 skeleton v1 is complete and closed out.
- Static historical-label fixture planning was completed by PR #194.
- Stage 2 static fixture implementation v1 is complete and closed out by PR #198 / PRD-P1-WX-STAGE2-FIXTURE-IMPLEMENTATION-CLOSEOUT-01.
- Exactly three static synthetic fixture JSON files exist under `tests/fixtures/weather/stage2_historical_labels/`; they are the complete synthetic fixture set for that closed-out subphase.
- Stage 2 real source-backed fixture implementation v1 is complete and closed out by PR #204 / PRD-P1-WX-STAGE2-REAL-FIXTURE-IMPLEMENTATION-CLOSEOUT-01.
- Exactly two real source-backed fixture JSON files exist under `tests/fixtures/weather/stage2_real_source_backed_labels/`; they are the complete real source-backed fixture set for that closed-out subphase.
- The at-most-3 real fixture cap was preserved, and the third real fixture was intentionally not fabricated.
- Old real-fixture planning/approval tests are successor-aware after PR #203.
- Stage 2 historical-label loading/validation planning v1 is complete and closed out by PR #208 / PRD-P1-WX-STAGE2-HISTORICAL-LABEL-LOADING-PLAN-CLOSEOUT-01.
- PRD-P1-WX-STAGE2-HISTORICAL-LABEL-LOADING-PLAN-CLOSEOUT-01 closed out the historical-label loading/validation planning subphase.
- Stage 2 static historical-label loading/validation implementation v1 is complete and closed out by PR #212 / PRD-P1-WX-STAGE2-HISTORICAL-LABEL-LOADING-IMPLEMENTATION-CLOSEOUT-01.
- PRD-P1-WX-STAGE2-HISTORICAL-LABEL-LOADING-IMPLEMENTATION-CLOSEOUT-01 closed out the static loader/validator implementation subphase.
- Stage 2 ingestion boundary planning v1 is complete and closed out by PR #217 / PRD-P1-WX-STAGE2-INGESTION-PLAN-CLOSEOUT-01.
- PRD-P1-WX-STAGE2-INGESTION-PLAN-CLOSEOUT-01 closed out the ingestion boundary planning subphase.
- Stage 2 static ingestion boundary skeleton v1 is complete and closed out by PR #221 / PRD-P1-WX-STAGE2-INGESTION-IMPLEMENTATION-CLOSEOUT-01.
- PRD-P1-WX-STAGE2-INGESTION-IMPLEMENTATION-CLOSEOUT-01 closed out the static ingestion boundary skeleton subphase.
- Stage 2 real ingestion boundary planning v1 is complete and closed out by PR #225 / PRD-P1-WX-STAGE2-REAL-INGESTION-PLAN-CLOSEOUT-01.
- PRD-P1-WX-STAGE2-REAL-INGESTION-PLAN-CLOSEOUT-01 closed out the real ingestion boundary planning subphase after PR #225.
- PRD-P1-WX-STAGE2-REAL-INGESTION-PLAN-01 remains a planning-only artifact.
- The real ingestion boundary planning artifact defined planning-only source-intake vocabulary, provider/source category taxonomy, allowed/prohibited source-intake modes, pre-fetch approval gates, provenance/access-date/retrieval-context requirements, no-lookahead safeguards, separation rules, fail-closed blockers, and handoff gates.
- The ingestion boundary planning artifact defined planning-only vocabulary, allowed/prohibited future source categories, no-lookahead safeguards, fixture/loader separation rules, fail-closed blockers, and later handoff gates.
- `meg/weather/stage2/ingestion_boundary.py` exists as a static validator only.
- The static ingestion boundary skeleton validates caller-supplied already-human-reviewed descriptor mappings only.
- It uses closed vocabularies.
- It returns pass, caution, or blocked validation results.
- It is stdlib-only.
- It does not read files, write files, call services, open network connections, load credentials/secrets/config, create schemas, or start jobs.
- `meg/weather/stage2/historical_label_loader.py` exists.
- The loader is limited to explicit static fixture validation.
- The loader reads only caller-supplied paths under the two allowlisted fixture directories.
- The directory loader is non-recursive.
- The loader reuses the existing Stage 2 metadata validator.
- All three synthetic and both real source-backed fixtures load through the static loader.
- No fixture JSON/README files were modified.
- No fixture README/JSON files were modified.
- No historical-label data files or generated data were created.
- No ingestion implementation was created or approved.
- No provider/API connectors were created or approved.
- No provider/source connector implementation was created or approved.
- No source fetching was created or approved.
- No external API calls were created or approved.
- No credentials/secrets/config loading was created or approved.
- No forecast pulls were created or approved.
- No scraping/polling/streaming/scheduling/queues/jobs/background tasks were created or approved.
- No scoring/backtesting/runtime/trading/order placement/autonomy was created or approved.
- No loader expansion was created or approved.
- The current recommended posture is hold/checkpoint unless a concrete real ingestion planning gap is found or the user explicitly chooses a later approval/request/planning gate.
- No scoring/backtesting/runtime/trading/order placement/autonomy is approved.
- Ingestion implementation, provider/source connector implementation, source fetching, external API calls, scoring/backtesting, paper simulation, runtime observation, trading, order placement, autonomy, and production behavior remain outside the approved gate.

## Current ticket style
- Use the MEG ticket format from `docs/meta/MEG_TICKET_STYLE_GUIDE.md`.
- Every ticket response needs verdict/context, next ticket name, bigger-picture fit, research depth flag, language/tooling suitability check, one copyable Main Codex prompt, and one copyable Self-review prompt.

## Current PR review style
- Use `docs/meta/MEG_PR_REVIEW_CHECKLIST.md`.
- Reviews are advisory only and must end with a final merge/block recommendation plus a recommended next ticket.

## Known blockers
- No active ops blocker is known after MEG-OPS-01.
- No active Weather Bot fixture implementation blocker is known after PR #204 closeout.
- No active historical-label loading/validation planning blocker is known after PR #208 closeout.
- No active static loader/validator implementation blocker is known after PR #212 closeout.
- No active ingestion boundary planning blocker is known after PR #217 closeout.
- No active static ingestion boundary skeleton blocker is known after PR #221 closeout.
- No active real ingestion boundary planning blocker is known after PR #225 closeout.
- Any continued Weather Bot work requires either a concrete real ingestion planning gap or an explicit user choice of a separately approved later approval/request/planning gate.

## Last updated by
- Codex for MEG-OPS-WX-ACTIVE-STATE-07, after PR #225 / PRD-P1-WX-STAGE2-REAL-INGESTION-PLAN-CLOSEOUT-01.

## How to use this file
- Read this file immediately after `AGENTS.md` in a fresh chat.
- Future chats should use this file as current working memory after MEG-OPS-01 lands.
- Treat real source-backed fixture implementation v1 as complete/closed out after PR #204.
- Default to hold/checkpoint unless a concrete real ingestion planning gap is found or the user explicitly chooses a later approval/request/planning gate.
- Do not infer approval for real ingestion, ingestion implementation, provider/source connectors, source fetching, external API calls, scoring, backtesting, runtime, trading, order placement, autonomy, or production behavior from any completed Stage 2 fixture, planning, loader implementation, ingestion planning, static ingestion skeleton, or closeout work.
