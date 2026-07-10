# MEG Next Chat Bootstrap Prompt

## Post-PR #334 Weather Bot Stage 2 bootstrap instruction

- Weather Bot Stage 2 supplied-input runtime foundation is code-complete for its approved in-memory supplied-input scope.
- PR #331 created the source/provider runtime approval request; PR #332 recorded `source_provider_runtime_decision: hold_source_provider_runtime_track`; PR #333 completed the source/provider runtime hold closeout; PR #334 completed the post-hold static roadmap.
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

```text
You are helping with the MEG repository in Weather Bot Stage 2 after WEATHER-BOT-STAGE2-FIXTURE-ONLY-SOURCE-PROVIDER-RUNTIME-APPROVAL-CHANGE-01. The supplied-input runtime foundation is code-complete only for its approved in-memory supplied-input scope. The previous recorded source/provider runtime decision was source_provider_runtime_decision: hold_source_provider_runtime_track. The current recorded source/provider runtime decision is source_provider_runtime_decision: approve_fixture_only_source_provider_runtime. Fixture-only/local-static/caller-supplied source-provider runtime planning and implementation may proceed only in a separate future implementation PR. This approval-change PR does not implement fixture-only runtime and does not approve live source/provider runtime. Live providers, live source fetching, provider clients, API calls, scraping, forecast pulls, downloads, SDK usage, credentials/config loading, live ingestion, paper trading, trading/execution, persistence/export writing, queue/service/scheduler/broker behavior, owner-decision capture, operator decision execution, durable workflow-completion side effects, and production behavior remain not approved. Production readiness is not achieved. Canonical routing fields remain exactly condition_id, token_id, and outcome; market\_id remains non-routing only; token_outcome_pair remains derived only. The next implementation ticket is fixture-only, not live provider runtime: WEATHER-BOT-STAGE2-FIXTURE-ONLY-SOURCE-PROVIDER-RUNTIME-SCAFFOLD-01.
```

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


## Post-PR #308 Weather Bot Phase 0A bootstrap instruction

- PR #308 merged `WEATHER-BOT-PHASE0A-STATIC-PLANNING-LANE-CLOSEOUT-REFRESH-01`; Weather Bot Phase 0A static planning lane closed out.
- PR #307 remains predecessor context; PR #283 remains excluded unless explicitly merged and is not a predecessor.
- Runtime/source/provider/paper-trade/trading remain unapproved: runtime approval remains not granted; source-fetching approval remains not granted; provider/source approval remains not granted; paper-trade approval remains not granted; trading/production approval remains not granted.
- Canonical routing fields remain exactly `condition_id`, `token_id`, and `outcome`; `market_id` remains non-routing only; `token_outcome_pair` remains derived only.
- Source-fetching runtime track remains closed/held with `hold_source_fetching_runtime_track`; source fetching remains not implemented; provider/source implementation remains not approved.
- No owner-decision capture lane is active; do not reopen owner-decision capture.
- No runtime/source/provider/paper-trade/trading implementation lane is active; continue only with meta/handoff maintenance or narrow revision unless explicitly instructed otherwise.
- Next safe track: `weather_bot_phase0a_meta_state_handoff_revision_if_needed`.
- Conditional revision track if this handoff scope is too broad: `weather_bot_phase0a_meta_handoff_refresh_revision_if_scope_too_broad`.

```text
You are helping with the MEG repository in Weather Bot Phase 0A post-PR #308. PR #308 merged WEATHER-BOT-PHASE0A-STATIC-PLANNING-LANE-CLOSEOUT-REFRESH-01, and the Weather Bot Phase 0A static planning lane is closed out. PR #307 remains predecessor context. Do not treat PR #283 as predecessor unless explicitly merged. Runtime/source/provider/paper-trade/trading remain unapproved. Canonical routing fields remain exactly condition_id, token_id, and outcome; `market_id` remains non-routing only; token_outcome_pair remains derived only. Source-fetching runtime track remains closed/held with hold_source_fetching_runtime_track. No owner-decision capture lane is active. Continue only with meta/handoff maintenance or narrow revision unless explicitly instructed otherwise.
```

## Post-PR #301 Weather Bot Phase 0A bootstrap instruction

- This is MEG Weather Bot Phase 0A post-PR #301.
- Read `AGENTS.md`, `docs/meta/MEG_ACTIVE_STATE.md`, `docs/meta/MEG_CHAT_HANDOFF.md`, `docs/meta/MEG_TICKET_STYLE_GUIDE.md`, and `docs/meta/domain_packets/WEATHER_BOT_PACKET.md`.
- Treat post-PR #301 docs as controlling over older post-PR #247/#280 text.
- Do not approve source fetching, provider connectors, runtime validation, scoring, backtesting, paper trading, trading, autonomy, production, persistence, reports, or export.
- Do not treat PR #283 as predecessor unless explicitly merged. PR #283 remains excluded unless explicitly merged.
- Do not create tickets until the user asks.
- Weather Bot models the market settlement rule, not generic weather; source-fetching runtime work remains held/closed; Stage 2 metadata remains supplied-metadata-only and fail-closed; canonical routing fields remain exactly `condition_id`, `token_id`, and `outcome`; `market_id` remains non-routing only.

```text
You are helping with the MEG repository in Weather Bot Phase 0A post-PR #301.

First read:
- AGENTS.md
- docs/meta/MEG_ACTIVE_STATE.md
- docs/meta/MEG_CHAT_HANDOFF.md
- docs/meta/MEG_TICKET_STYLE_GUIDE.md
- docs/meta/domain_packets/WEATHER_BOT_PACKET.md

Treat post-PR #301 docs as controlling over older post-PR #247/#280 text. Do not approve source fetching, provider connectors, runtime validation, scoring, backtesting, paper trading, trading, autonomy, production, persistence, reports, or export. Do not treat PR #283 as predecessor unless explicitly merged. PR #283 remains excluded unless explicitly merged. Do not create tickets until the user asks.
```


## Post-PR #247 Weather Bot bootstrap instruction

- Read the latest Weather Bot hold checkpoint: `PRD-P1-WX-STAGE2-SOURCE-FETCHING-APPROVAL-REQUEST-HOLD-CHECKPOINT-01`.
- Treat stale handoff/meta state as subordinate to newer merged PRDs, closeout docs, checkpoint docs, and verified PR metadata; prefer newer merged PRDs/checkpoints/verified PR metadata over stale handoff state.
- Default to `hold_checkpoint` after PR #247 unless the user explicitly asks for a safe docs/static-test-only meta, review, or revision ticket.
- Do not generate provider/source implementation tickets without later explicit approval.
- Do not proceed into provider connectors, source fetching, forecast pulls, API calls, scraping, credentials/config loading, generated data, fixtures, scoring, backtesting, runtime behavior, trading, autonomy, or production behavior without later explicit approval.

Copy this prompt into a fresh chat when restarting MEG work.

```text
You are helping with the MEG repository.

First read these repo-native operating-memory docs before producing tickets or reviews:
- AGENTS.md
- docs/meta/MEG_ACTIVE_STATE.md
- docs/meta/MEG_CONTEXT_ROUTER.md
- docs/meta/MEG_WORKFLOW_PLAYBOOK.md
- docs/meta/MEG_TICKET_STYLE_GUIDE.md
- docs/meta/MEG_PR_REVIEW_CHECKLIST.md
- docs/meta/domain_packets/WEATHER_BOT_PACKET.md when Weather Bot is active

Then summarize:
1. current project state
2. current active phase
3. latest merged/reviewed PR
4. current approved gate
5. next possible gate
6. explicitly forbidden scopes
7. source-of-truth docs
8. MEG ticket formatting rules

Do not generate a ticket until the user asks.
Do not open issues.
Do not approve runtime, connectors, trading, or autonomy.
Do not assume later-gate approval from planning, approval-request, implementation, or closeout docs.
Treat Weather Bot synthetic fixture implementation v1 as complete/closed out after PR #198 and real source-backed fixture implementation v1 as complete/closed out after PR #204, with hold/checkpoint as the default posture unless a concrete source-evidence/validation gap is found or the user explicitly chooses a later approval/request/planning gate.
Do not merge PRs or approve PRs as final authority.
```

## Legacy bootstrap compatibility references

Older meta-handoff tests and historical chats may also reference these documents. Read them when reconciling older Phase 1 planning context, but defer to `docs/meta/MEG_ACTIVE_STATE.md` for current post-PR #204 real-fixture-closeout posture:

- docs/meta/meg_current_state.md
- docs/meta/meg_chat_handoff.md
- docs/meta/meg_workflow_playbook.md
- docs/meta/meg_ticket_prompt_template.md
- docs/meta/meg_phase_history_summary.md
- docs/meta/meg_duckdb_research_rail_explainer.md
- docs/meta/meg_strategic_idea_registry.md
- prd-p1-wx-01
