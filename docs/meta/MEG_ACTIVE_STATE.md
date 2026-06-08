# MEG Active State

This is the first working-memory file to read after `AGENTS.md`.

## Current active project
- MEG repo-native project operations and Weather Bot gated planning.

## Current active area
- MEG Weather Bot Stage 2 historical-label loading/validation planning closeout track.

## Current active phase
- MEG-OPS-01 established the repo-native orchestration layer for durable project handoff.
- The current active Weather Bot area is the post-historical-label loading/validation planning closeout checkpoint.
- Stage 2 skeleton v1 is complete and closed out.
- Stage 2 synthetic static fixture implementation v1 is complete and closed out.
- Stage 2 real source-backed fixture implementation v1 is complete and closed out.
- Stage 2 historical-label loading/validation planning v1 is complete and closed out.
- PRD-P1-WX-STAGE2-FIXTURE-IMPLEMENTATION-CLOSEOUT-01 closed out the static fixture implementation subphase after PR #198.
- PRD-P1-WX-STAGE2-REAL-FIXTURE-IMPLEMENTATION-CLOSEOUT-01 closed out the real source-backed fixture implementation subphase after PR #204.
- PRD-P1-WX-STAGE2-HISTORICAL-LABEL-LOADING-PLAN-CLOSEOUT-01 closed out the historical-label loading/validation planning subphase after PR #208.
- Exactly three static synthetic fixture JSON files exist under `tests/fixtures/weather/stage2_historical_labels/`.
- Exactly two real source-backed fixture JSON files exist under `tests/fixtures/weather/stage2_real_source_backed_labels/`.
- The fixture count cap of at most 3 real source-backed fixtures was preserved.
- The third real fixture was intentionally not fabricated.
- Old real-fixture planning/approval tests are successor-aware after PR #203.

## Latest merged PR
- PR #208 / PRD-P1-WX-STAGE2-HISTORICAL-LABEL-LOADING-PLAN-CLOSEOUT-01 closed out the historical-label loading/validation planning subphase.

## Latest reviewed PR
- PR #208 / PRD-P1-WX-STAGE2-HISTORICAL-LABEL-LOADING-PLAN-CLOSEOUT-01 is the latest Weather Bot closeout/checkpoint item represented by this active state.
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
- No loader was created.
- No fixture JSON/README files were modified.
- No historical-label data files or generated data were created.
- This closeout does not approve real fixture implementation as a next default gate because real fixture implementation v1 is already complete and closed out.
- This closeout does not approve loader implementation, historical-label loading implementation, ingestion, scoring, backtesting, runtime, trading, order placement, autonomy, production behavior, or any later Weather Bot gate.

## Next possible gate
- Current recommended posture: hold/checkpoint unless a concrete loading-planning gap is found or the user explicitly chooses a later approval/request/planning gate.
- Current next possible Weather Bot action, if the user explicitly chooses to continue, is a separately approved later gate only.
- Examples of separately approved later gates include targeted loading-planning refinement if a concrete gap exists, or a later approval-request/planning gate chosen by the user.
- Do not present loader implementation, historical-label loading implementation, ingestion, scoring, backtesting, runtime, trading, order placement, autonomy, or production behavior as approved or next by default.

## Explicitly not approved
- Loader implementation is not approved.
- Historical-label loading implementation is not approved.
- Real historical-label data expansion is not approved.
- Generated data is not approved.
- Ingestion is not approved.
- Provider/API connectors are not approved.
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
- No loader was created.
- No fixture JSON/README files were modified.
- No historical-label data files or generated data were created.
- Historical-label loading implementation remains unapproved.
- The default Weather Bot posture is hold/checkpoint unless a concrete loading-planning gap is found or the user explicitly chooses a later approval/request/planning gate.
- Loader implementation, historical-label loading implementation, ingestion, provider/source integration, scoring/backtesting, paper simulation, runtime observation, trading, order placement, autonomy, and production behavior remain outside the approved gate.

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
- Any continued Weather Bot work requires either a concrete loading-planning gap or an explicit user choice of a separately approved later approval/request/planning gate.

## Last updated by
- Codex for MEG-OPS-WX-ACTIVE-STATE-03, after PR #208 / PRD-P1-WX-STAGE2-HISTORICAL-LABEL-LOADING-PLAN-CLOSEOUT-01.

## How to use this file
- Read this file immediately after `AGENTS.md` in a fresh chat.
- Future chats should use this file as current working memory after MEG-OPS-01 lands.
- Treat real source-backed fixture implementation v1 as complete/closed out after PR #204.
- Default to hold/checkpoint unless a concrete loading-planning gap is found or the user explicitly chooses a later approval/request/planning gate.
- Do not infer approval for loader implementation, historical-label loading implementation, ingestion, scoring, backtesting, runtime, trading, order placement, autonomy, or production behavior from any completed Stage 2 fixture or planning work.
