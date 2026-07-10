# MEG Chat Handoff

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


## Post-PR #308 Weather Bot Phase 0A continuation handoff

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


## Post-PR #247 Weather Bot handoff

- PR #247 merged.
- Current Weather Bot Stage 2 state is source-fetching approval-request hold checkpoint: `hold_checkpoint`.
- Latest canonical checkpoint is `PRD-P1-WX-STAGE2-SOURCE-FETCHING-APPROVAL-REQUEST-HOLD-CHECKPOINT-01`.
- No human review is pending by default for this small gate.
- `implementation_not_approved`; no implementation is approved or recommended.
- `source_fetching_not_approved`; no source-fetching approval exists.
- Next safe work, if any, must be docs/static-test-only and explicit.

## 1) What MEG is
MEG is a prediction market intelligence and research platform. It is moving from local research infrastructure into Phase 1 weather bot planning. It emphasizes contracts, bounded research, human-reviewed outputs, and gated runtime behavior. It is not approved for live trading, production execution, autonomous behavior, or order placement.

## 2) User/project workflow preference
- User often asks: “check PR X and give next ticket.”
- Assistant should fetch PR diff and CI.
- Assistant should judge merge readiness.
- Assistant should **do not open unnecessary issues** and should not open issues unless user reports a blocker or asks.
- If PR is clean, say merge-ready and provide next ticket.
- If user reports blocker, provide targeted fix prompt and self-review prompt.
- Always include main prompt + self-review prompt for tickets.
- Always include research depth flag.
- Always include language/tooling suitability check.
- Always include bigger-picture fit.
- Keep prompts comprehensive and specific.
- Do not rush phase sequencing.

## 3) Current conversation lessons learned
- Avoid opening issues prematurely.
- Git-status or mtime-based changed-file checks in unit tests are brittle and should generally be avoided.
- Explicit safety disclaimers in docs are not forbidden runtime behavior.
- Separate docs/static-test tickets from implementation tickets.
- “Blocked” in an audit can be the correct audit output, not a merge blocker.
- DuckDB is dev/research-only, not production DB.
- Phase 1 weather bot begins with planning/taxonomy, not connectors.

## 4) How to answer future PR checks
- “Reviewed PR #X. Verdict: merge-ready / blocked.”
- Changed files list.
- Key verification summary.
- CI status summary.
- Merge recommendation.
- No unnecessary issues opened.
- Next ticket.

## 5) How to answer future blocker reports
- Validate whether blocker is real or expected audit output.
- If real, provide narrow fix prompt.
- Provide self-review prompt.
- Do not open issue unless requested or required.
- If issue is needed, user approval (or explicit workflow requirement) should exist.

## 6) Tone and style
- Direct, practical, high-context.
- Explain complexity on request.
- Start concise, then provide detailed prompts.
- Do not overclaim.
- Be conservative with readiness language.

## 7) Next chat bootstrap
Use `docs/meta/MEG_NEXT_CHAT_BOOTSTRAP_PROMPT.md`.
