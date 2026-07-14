# MEG Active State

## Post-PR #355 Weather Bot Stage 2 final handoff refresh (controlling)

- Newest controlling Weather Bot Stage 2 checkpoint: PR #355 / `WEATHER-BOT-STAGE2-FIXTURE-ONLY-SOURCE-PROVIDER-RUNTIME-CLOSEOUT-READINESS-01`, verified in repository history as merge commit `9f8d5bb`.
- This post-PR #355 Stage 2 handoff controls over stale post-PR #334, Phase 0A, source-fetching-hold, and older Stage 2 sections retained below.
- Stage 2 approved fixture-only/local-static/caller-supplied source/provider runtime scope is code-complete and closed.
- All 18 fixture-only runtime-chain objects landed in PRs #337 through #354.
- Positive full-chain validation and expected-negative fail-closed validation paths landed; positive representation requires `runtime_gate_ready`, while correct expected-failure representation can validate as `PASSED` and retain `runtime_gate_blocked`.
- The intentionally invalid nested integration smoke is not directly required to pass. No smoke is executed or generated, and no failure is injected or generated.
- Live-provider/source-fetching runtime remains unapproved; Stage 3 remains unapproved.
- Weather Bot models market settlement rules, not generic weather. Canonical routing fields remain exactly `condition_id`, `token_id`, and `outcome`; `market_id` remains non-routing only; `token_outcome_pair` remains derived only.
- Persistence/export writing, real queue services, schedulers, brokers, handoff delivery, owner-decision capture, operator-decision execution, durable workflow-completion side effects, paper simulation, runtime observation, trading, execution, autonomy, and production behavior remain unapproved.
- Repository is ready for a fresh chat. The next action is fresh-chat bootstrap, not another runtime bridge, not a standalone self-review ticket, and not automatic Stage 3 work.
- No repository ticket should be created automatically in the new chat; wait for explicit user direction.


## Post-PR #334 Weather Bot Stage 2 post-hold handoff refresh

- Weather Bot Stage 2 supplied-input runtime foundation is code-complete for its approved in-memory supplied-input scope.
- PR #331 created the Weather Bot Stage 2 source/provider runtime approval request.
- PR #332 recorded `source_provider_runtime_decision: hold_source_provider_runtime_track`.
- PR #333 completed the source/provider runtime hold closeout.
- PR #334 completed the Weather Bot Stage 2 post-hold static roadmap.
- Source/provider runtime decision is now `source_provider_runtime_decision: approve_fixture_only_source_provider_runtime`.
- Fixture-only source/provider runtime planning and implementation may proceed only in a separate future implementation PR; live providers/source fetching remain not approved.
- Source fetching remains not approved.
- Provider/source implementation remains not approved.
- Fixture-only source/provider runtime implementation is not implemented by this approval-change PR.
- Live source/provider runtime remains not approved.
- Paper trading remains not approved.
- Trading/execution remains not approved.
- Persistence/export writing remain not implemented and not approved.
- Queue/service/scheduler/broker behavior remains not implemented and not approved.
- Owner-decision capture and operator decision execution remain not implemented and not approved.
- Durable workflow-completion side effects remain not implemented and not approved.
- Production readiness is not achieved.
- Weather Bot models market settlement rules, not generic weather.
- Canonical routing fields remain exactly `condition_id`, `token_id`, and `outcome`.
- market\_id remains non-routing only.
- `token_outcome_pair` remains derived only.
- Any future source/provider, fixture-only, live-provider, persistence, paper-trading, operator-workflow, or production lane requires a separate explicit approval PR before implementation.
- Recommended next action: use the separate fixture-only implementation ticket; do not start live provider runtime.
- Next valid implementation ticket: `WEATHER-BOT-STAGE2-FIXTURE-ONLY-SOURCE-PROVIDER-RUNTIME-SCAFFOLD-01`.

## Weather Bot Stage 2 Fixture-Only Source/Provider Runtime Approval Change

- This is an explicit approval-change record for the Weather Bot Stage 2 source/provider runtime lane.
- Previous recorded decision was: source_provider_runtime_decision: hold_source_provider_runtime_track
- Historical post-hold handoff wording said: Source/provider runtime remains held.
- Historical post-hold handoff wording said: Fixture-only source/provider runtime remains not approved.
- Historical post-hold handoff wording said the next valid ticket must be an explicit approval-change request, not implementation.
- New recorded decision is: source_provider_runtime_decision: approve_fixture_only_source_provider_runtime
- The approval is limited to fixture-only/local-static/caller-supplied source-provider runtime planning and implementation in a future PR.
- This PR does not implement fixture-only runtime.
- This PR does not approve live source/provider runtime; live source/provider runtime remains not approved.
- Live providers remain not approved.
- Live source fetching remains not approved.
- Provider clients/API calls/scraping/forecast pulls/downloads/SDK usage/credentials/config loading/live ingestion remain not approved.
- Provider clients, API calls, scraping, forecast pulls, downloads, SDK usage, credentials/config loading, and live ingestion remain not approved.
- Paper trading remains not approved.
- Trading/execution remains not approved.
- Persistence/export writing remain not approved by this decision.
- Queue/service/scheduler/broker behavior remains not approved by this decision.
- Owner-decision capture/operator decision execution remain not approved by this decision.
- Owner-decision capture and operator decision execution remain not approved by this decision.
- Durable workflow-completion side effects remain not approved by this decision.
- Production readiness is not achieved.
- Any fixture-only runtime implementation must preserve fail-closed behavior.
- Any fixture-only runtime implementation must preserve no-lookahead constraints.
- Any fixture-only runtime implementation must not route on market\_id.
- Any fixture-only runtime implementation must preserve canonical routing fields exactly:
  - condition_id
  - token_id
  - outcome
- token_outcome_pair remains derived only.
- Any fixture-only runtime implementation must not bypass operator review.
- Any fixture-only runtime implementation must not enable paper trading, trading, order placement, autonomy, persistence/export writing, live provider calls, or production behavior.
- Fixture-only implementation may proceed only in a separate implementation PR.
- The next implementation ticket is fixture-only, not live provider runtime.
- The next valid implementation ticket is: WEATHER-BOT-STAGE2-FIXTURE-ONLY-SOURCE-PROVIDER-RUNTIME-SCAFFOLD-01


## Post-PR #308 Weather Bot Phase 0A static planning lane closeout handoff

- Latest Weather Bot static planning closeout: PR #308 / `WEATHER-BOT-PHASE0A-STATIC-PLANNING-LANE-CLOSEOUT-REFRESH-01` merged the static planning lane closeout.
- Predecessor context: PR #307 / `WEATHER-BOT-PHASE0A-NON-OWNER-RUNTIME-GATE-HOLD-REFRESH-PLANNING-01` remains predecessor context; PR #283 remains excluded unless explicitly merged and is not treated as a predecessor.
- Current lane status: Weather Bot Phase 0A static planning lane closed out.
- Weather Bot models the market settlement rule, not generic weather.
- Canonical routing fields remain exactly `condition_id`, `token_id`, and `outcome`; `token_outcome_pair` remains derived only; `market_id` remains non-routing only.
- Runtime approval remains not granted; source-fetching approval remains not granted; provider/source approval remains not granted; paper-trade approval remains not granted; trading/production approval remains not granted.
- Source-fetching runtime track remains closed/held; the already-closed source-fetching runtime track posture remains `hold_source_fetching_runtime_track`; source fetching remains not implemented; provider/source implementation remains not approved.
- No owner-decision capture lane is active; do not reopen owner-decision capture and do not create owner capture as a next track.
- No runtime/source/provider/paper-trade/trading implementation lane is active.
- Runtime implementation, source/provider implementation, evaluation execution, paper trading, trading, autonomy, and production remain blocked and unapproved.
- Runtime settlement-rule interpreter, runtime no-lookahead validation, runtime fail-closed validation, manual-review runtime workflow, operator decision execution, and operator decision persistence remain not implemented.
- Next safe track: `weather_bot_phase0a_meta_state_handoff_revision_if_needed`.
- Conditional revision track if this handoff scope is too broad: `weather_bot_phase0a_meta_handoff_refresh_revision_if_scope_too_broad`.

## Post-PR #301 Weather Bot Phase 0A planning handoff refresh

- Latest merged PR: PR #301.
- This post-PR #301 section is newer and controlling over older post-PR #280 or post-PR #247 sections retained below.
- Current recommended next track: `weather_bot_phase0a_next_chat_bootstrap_or_hold`.
- Next repo-native action after this refresh is either a new chat bootstrap or a later explicitly requested safe planning ticket.
- PR #283 remains excluded unless explicitly merged.
- Weather Bot models the market settlement rule, not generic weather.
- Weather Bot Phase 0A remains held and closed for source-fetching runtime work; source-fetching runtime track remains closed/held; closed owner decision remains `hold_source_fetching_runtime_track`; source fetching remains not implemented; implementation approval remains not granted.
- Stage 2 runtime metadata scaffolds remain supplied-metadata-only and fail-closed.
- Canonical routing fields remain exactly `condition_id`, `token_id`, and `outcome`; `token_outcome_pair` remains a derived relationship; `market_id` remains non-routing only; no routing on `market_id` is introduced or approved.
- Paper-trade readiness and evaluation readiness remain not achieved; operator workflow, supplied market-contract input, settlement-rule interpreter, no-lookahead validation, and fail-closed validation runtime behavior remain not implemented.
- Source fetching, provider connectors, provider clients, live provider/source fetching, forecast pulls, API calls, scraping, file downloads, provider SDK usage, credentials/config loading, generated data, fixtures, schema changes, DB migrations, runtime validation, runtime parser/interpreter, runtime ingestion, scoring, evaluation execution, metric persistence, backtesting, paper trading, order simulation, trading, autonomy, production, reports, persistence, audit output, and exports remain not approved.
- Completed Phase 0A planning artifacts: `WEATHER-BOT-PHASE0A-NON-SOURCE-FETCHING-SCOPE-INVENTORY-01`, `WEATHER-BOT-PHASE0A-MARKET-CONTRACT-STATIC-INVENTORY-01`, `WEATHER-BOT-PHASE0A-CANONICAL-IDENTIFIER-STATIC-AUDIT-01`, `WEATHER-BOT-PHASE0A-NO-LOOKAHEAD-POLICY-DOCUMENTATION-01`, `WEATHER-BOT-PHASE0A-FAIL-CLOSED-ERROR-TAXONOMY-PLANNING-01`, `WEATHER-BOT-PHASE0A-STAGE2-METADATA-CONTRACT-DOCUMENTATION-01`, `WEATHER-BOT-PHASE0A-PAPER-TRADE-READINESS-GAP-INVENTORY-01`, `WEATHER-BOT-PHASE0A-EVALUATION-METRICS-PLANNING-01`, `WEATHER-BOT-PHASE0A-OPERATOR-WORKFLOW-PLANNING-01`, `WEATHER-BOT-PHASE0A-SUPPLIED-MARKET-CONTRACT-INPUT-PLANNING-01`, `WEATHER-BOT-PHASE0A-SETTLEMENT-RULE-INTERPRETER-PLANNING-01`, `WEATHER-BOT-PHASE0A-NO-LOOKAHEAD-VALIDATION-PLANNING-01`, `WEATHER-BOT-PHASE0A-FAIL-CLOSED-VALIDATION-PLANNING-01`.


## Post-PR #280 Weather Bot Phase 0A meta refresh posture

- Latest merged closeout: `WEATHER-BOT-PHASE0A-HOLD-STATE-CLOSEOUT-01`.
- Current posture: `weather_bot_phase0a_held_closed`.
- Source-fetching runtime track: `closed_held`.
- Closed owner decision: `hold_source_fetching_runtime_track`.
- Source fetching: `not_implemented`.
- Implementation approval: `not_granted`.
- Stage 2 runtime metadata: `supplied_metadata_only`.
- Stage 2 validation posture: `fail_closed`.
- Future reopen condition: a later owner-decision revision must explicitly select `approve_narrow_source_fetching_runtime_implementation_plan`; otherwise the track remains held, closed, or routed to revision.
- Weather Bot models the market settlement rule, not generic weather.
- Stage 2 runtime metadata artifacts: `meg/weather/stage2/source_identity_runtime.py`, `meg/weather/stage2/retrieval_context_runtime.py`, `meg/weather/stage2/provider_source_family_runtime.py`, `meg/weather/stage2/manual_review_gate_runtime.py`, `meg/weather/stage2/no_lookahead_metadata_runtime.py`, `meg/weather/stage2/fail_closed_validation_runtime.py`, and `meg/weather/stage2/static_audit_surface_runtime.py`.
- Provider connectors remain not approved; provider clients remain not created; live provider/source fetching, credentials/config loading, generated data, fixture changes, scoring/backtesting, trading/order placement/autonomy/production behavior, report writing, audit output persistence, and external export remain not approved.


## Post-PR #247 Weather Bot source-fetching approval-request hold checkpoint refresh

- Current active Weather Bot Stage 2 state is post-PR #247 hold checkpoint.
- PR #247 is merged in local history and is the latest completed Weather Bot Stage 2 source-fetching approval-request checkpoint.
- Latest canonical checkpoint is `PRD-P1-WX-STAGE2-SOURCE-FETCHING-APPROVAL-REQUEST-HOLD-CHECKPOINT-01`.
- Current safe next state is `hold_checkpoint`.
- Source-fetching approval-request draft sequence is paused by default; the draft artifact, draft closeout, and hold checkpoint exist.
- `source_fetching_not_approved`; no source-fetching approval exists.
- `implementation_not_approved`; no implementation is approved or recommended.
- No provider connector/source fetching/forecast pull/API/scraping/credentials/config/generated-data/fixture/scoring/backtesting/runtime/trading/autonomy/production work is approved.
- Future chats must prefer newer merged PRDs, closeout docs, checkpoint docs, and verified PR metadata over stale handoff state.

This is the first working-memory file to read after `AGENTS.md`.

## Current active project
- MEG repo-native project operations and Weather Bot gated planning.

## Current active area
- MEG Weather Bot Stage 2 source-fetching approval-request post-PR #247 hold checkpoint track.

## Current active phase
- MEG-OPS-01 established the repo-native orchestration layer for durable project handoff.
- The current active Weather Bot area is the source-fetching approval-request post-PR #247 hold checkpoint.
- Stage 2 skeleton v1 is complete and closed out.
- Stage 2 synthetic static fixture implementation v1 is complete and closed out.
- Stage 2 real source-backed fixture implementation v1 is complete and closed out.
- Stage 2 historical-label loading/validation planning v1 is complete and closed out.
- Stage 2 static historical-label loading/validation implementation v1 is complete and closed out.
- Stage 2 ingestion boundary planning v1 is complete and closed out.
- Stage 2 static ingestion boundary skeleton v1 is complete and closed out.
- Stage 2 real ingestion boundary planning v1 is complete and closed out.
- Stage 2 provider/source compatibility planning and closeout are complete.
- Stage 2 source-fetching approval-request planning, closeout, draft planning, draft, draft closeout, and hold checkpoint are complete at the docs/checkpoint layer only.
- The current safe next state is `hold_checkpoint`.
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
- PR #247 / PRD-P1-WX-STAGE2-SOURCE-FETCHING-APPROVAL-REQUEST-HOLD-CHECKPOINT-01 is the latest completed Weather Bot Stage 2 source-fetching approval-request checkpoint represented by this active state.
- PR #225 / PRD-P1-WX-STAGE2-REAL-INGESTION-PLAN-CLOSEOUT-01 remains historical as the real ingestion boundary planning closeout.

## Latest reviewed PR
- PR #247 / PRD-P1-WX-STAGE2-SOURCE-FETCHING-APPROVAL-REQUEST-HOLD-CHECKPOINT-01 is the latest Weather Bot closeout/checkpoint item represented by this active state.
- PR #225 / PRD-P1-WX-STAGE2-REAL-INGESTION-PLAN-CLOSEOUT-01 remains represented as the historical real ingestion boundary planning closeout.
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
- Current recommended posture: `hold_checkpoint` after PR #247.
- Current next possible Weather Bot action, if any, must be explicitly requested docs/static-test-only meta, review, or revision work unless later explicit approval grants a broader scope.
- Examples of conditional later docs-only tracks include human review of the draft if explicitly requested, source-fetching approval-request draft revision if explicitly requested, or a future docs/static-test-only meta refresh if needed.
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
- No active source-fetching approval-request hold-checkpoint blocker is known after PR #247.
- Any continued Weather Bot work defaults to `hold_checkpoint`; broader provider/source implementation work requires later explicit approval.

## Last updated by
- Codex for PRD-P1-WX-STAGE2-SOURCE-FETCHING-APPROVAL-REQUEST-META-REFRESH-01, after PR #247 / PRD-P1-WX-STAGE2-SOURCE-FETCHING-APPROVAL-REQUEST-HOLD-CHECKPOINT-01.

## How to use this file
- Read this file immediately after `AGENTS.md` in a fresh chat.
- Future chats should use this file as current working memory after MEG-OPS-01 lands.
- Treat real source-backed fixture implementation v1 as complete/closed out after PR #204.
- Default to hold/checkpoint unless a concrete real ingestion planning gap is found or the user explicitly chooses a later approval/request/planning gate.
- Do not infer approval for real ingestion, ingestion implementation, provider/source connectors, source fetching, external API calls, scoring, backtesting, runtime, trading, order placement, autonomy, or production behavior from any completed Stage 2 fixture, planning, loader implementation, ingestion planning, static ingestion skeleton, or closeout work.
