# MEG Active State

This is the first working-memory file to read after `AGENTS.md`.

## Current active project
- MEG repo-native project operations and Weather Bot gated planning.

## Current active area
- MEG Weather Bot Stage 2 static historical-label fixture track.

## Current active phase
- MEG-OPS-01 established the repo-native orchestration layer for durable project handoff.
- The current active Weather Bot area remains the Stage 2 static historical-label fixture track.
- Stage 2 skeleton v1 is complete.
- Stage 2 static fixture implementation v1 is complete.
- PRD-P1-WX-STAGE2-FIXTURE-IMPLEMENTATION-CLOSEOUT-01 closed out the static fixture implementation subphase after PR #198.
- Exactly three static synthetic fixture JSON files exist under `tests/fixtures/weather/stage2_historical_labels/`.

## Latest merged PR
- PR #198 / PRD-P1-WX-STAGE2-FIXTURE-IMPLEMENTATION-CLOSEOUT-01 closed out the static fixture implementation subphase.

## Latest reviewed PR
- PR #198 / PRD-P1-WX-STAGE2-FIXTURE-IMPLEMENTATION-CLOSEOUT-01 is the latest Weather Bot closeout/checkpoint item represented by this active state.
- PR #195 / MEG-OPS-01 remains the latest reviewed ops-docs handoff sequence item recorded here.

## Current approved gate
- Stage 2 skeleton v1 is complete.
- Static fixture planning was completed by PR #194.
- Static fixture implementation v1 is complete and closed out by PR #198 / PRD-P1-WX-STAGE2-FIXTURE-IMPLEMENTATION-CLOSEOUT-01.
- The complete fixture set is exactly three static synthetic, hand-authored JSON fixtures under `tests/fixtures/weather/stage2_historical_labels/`.
- This closeout does not approve ingestion, scoring, backtesting, runtime, trading, order placement, autonomy, production behavior, or any later Weather Bot gate.

## Next possible gate
- Current recommended posture: hold/checkpoint unless a concrete fixture validation gap is found or the user explicitly chooses a later approval gate.
- Current next possible Weather Bot action, if the user explicitly chooses to continue, is a separately approved later gate only.
- Examples of separately approved later gates include targeted fixture validation refinement if a concrete gap exists, or a later approval-request/planning gate for real source-backed fixtures or historical-label loading.
- Do not present ingestion, scoring, backtesting, runtime, trading, order placement, autonomy, or production behavior as approved or next by default.

## Explicitly not approved
- Real historical-label data is not approved.
- Generated data is not approved.
- Ingestion is not approved.
- Provider/API connectors are not approved.
- External API calls are not approved.
- Credentials/secrets/config loading is not approved.
- Forecast pulls are not approved.
- Scoring is not approved.
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

## Current Weather Bot status summary
- Stage 2 skeleton v1 is complete.
- Static historical-label fixture planning was completed by PR #194.
- Static fixture implementation v1 is complete and closed out by PR #198 / PRD-P1-WX-STAGE2-FIXTURE-IMPLEMENTATION-CLOSEOUT-01.
- Exactly three static synthetic fixture JSON files exist under `tests/fixtures/weather/stage2_historical_labels/`; they are the complete fixture set for this closed-out subphase.
- The default Weather Bot posture is hold/checkpoint unless a concrete fixture validation gap is found or the user explicitly chooses a later approval gate.
- Ingestion, provider/source integration, scoring/backtesting, paper simulation, runtime observation, trading, order placement, autonomy, and production behavior remain outside the approved gate.

## Current ticket style
- Use the MEG ticket format from `docs/meta/MEG_TICKET_STYLE_GUIDE.md`.
- Every ticket response needs verdict/context, next ticket name, bigger-picture fit, research depth flag, language/tooling suitability check, one copyable Main Codex prompt, and one copyable Self-review prompt.

## Current PR review style
- Use `docs/meta/MEG_PR_REVIEW_CHECKLIST.md`.
- Reviews are advisory only and must end with a final merge/block recommendation plus a recommended next ticket.

## Known blockers
- No active ops blocker is known after MEG-OPS-01.
- No active Weather Bot fixture implementation blocker is known after PR #198 closeout.
- Any continued Weather Bot work requires either a concrete fixture validation gap or an explicit user choice of a separately approved later approval/request/planning gate.

## Last updated by
- Codex for MEG-OPS-WX-ACTIVE-STATE-01, after PR #198 / PRD-P1-WX-STAGE2-FIXTURE-IMPLEMENTATION-CLOSEOUT-01.

## How to use this file
- Read this file immediately after `AGENTS.md` in a fresh chat.
- Future chats should use this file as current working memory after MEG-OPS-01 lands.
- Treat it as current working memory, not as a replacement for controlling PRDs.
- Use it to determine the active phase, approved gate, next possible gate, and forbidden scopes before writing tickets or reviewing PRs.
