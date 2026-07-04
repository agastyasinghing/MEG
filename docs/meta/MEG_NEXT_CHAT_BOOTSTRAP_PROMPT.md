# MEG Next Chat Bootstrap Prompt

## Post-PR #301 Weather Bot Phase 0A bootstrap instruction

- This is MEG Weather Bot Phase 0A post-PR #301.
- Read `AGENTS.md`, `docs/meta/MEG_ACTIVE_STATE.md`, `docs/meta/MEG_CHAT_HANDOFF.md`, `docs/meta/MEG_TICKET_STYLE_GUIDE.md`, and `docs/meta/domain_packets/WEATHER_BOT_PACKET.md`.
- Treat post-PR #301 docs as controlling over older post-PR #247/#280 text.
- Do not approve source fetching, provider connectors, runtime validation, scoring, backtesting, paper trading, trading, autonomy, production, persistence, reports, or export.
- Do not treat PR #283 as predecessor unless explicitly merged. PR #283 remains excluded unless explicitly merged.
- Do not create tickets until the user asks.
- Weather Bot models the market settlement rule, not generic weather; source-fetching runtime work remains held/closed; Stage 2 metadata remains supplied-metadata-only and fail-closed; canonical routing fields remain exactly `condition_id`, `token_id`, and `outcome`; the legacy market identifier remains non-routing only.

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
