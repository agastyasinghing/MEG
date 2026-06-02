# MEG Next Chat Bootstrap Prompt

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
Treat Weather Bot fixture implementation v1 as complete/closed out after PR #198, with hold/checkpoint as the default posture unless a concrete fixture validation gap is found or the user explicitly chooses a later approval gate.
Do not merge PRs or approve PRs as final authority.
```

## Legacy bootstrap compatibility references

Older meta-handoff tests and historical chats may also reference these documents. Read them when reconciling older Phase 1 planning context, but defer to `docs/meta/MEG_ACTIVE_STATE.md` for current post-PR #198 fixture-closeout posture:

- docs/meta/meg_current_state.md
- docs/meta/meg_chat_handoff.md
- docs/meta/meg_workflow_playbook.md
- docs/meta/meg_ticket_prompt_template.md
- docs/meta/meg_phase_history_summary.md
- docs/meta/meg_duckdb_research_rail_explainer.md
- docs/meta/meg_strategic_idea_registry.md
- prd-p1-wx-01
