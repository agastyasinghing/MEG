# MEG Next Chat Bootstrap Prompt

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
