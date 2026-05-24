# MEG Next Chat Bootstrap Prompt

## 1) Bootstrap prompt
You are continuing MEG. Read these repo files first:
- docs/meta/MEG_CURRENT_STATE.md
- docs/meta/MEG_CHAT_HANDOFF.md
- docs/meta/MEG_WORKFLOW_PLAYBOOK.md
- docs/meta/MEG_TICKET_PROMPT_TEMPLATE.md
- docs/meta/MEG_PHASE_HISTORY_SUMMARY.md
- docs/meta/MEG_DUCKDB_RESEARCH_RAIL_EXPLAINER.md
- docs/meta/MEG_STRATEGIC_IDEA_REGISTRY.md
- docs/prd/PRD-P1-WX-KICKOFF_PHASE_1_WEATHER_BOT_TICKET_PLAN.md

Then continue with the next ticket:
- PRD-P1-WX-01 Weather bot requirements and market taxonomy planning

Rules:
- Preserve the existing PR check / next ticket workflow.
- Do not open unnecessary issues.
- Always include main prompt and self-review prompt.
- Always include research depth flag.
- Always include language/tooling suitability check.
- Do not start implementation before planning/approval gates.
- Keep weather execution, connectors/API calls, trading/autonomy unapproved until gates.

## 2) Condensed project state
- Phase 0B local research readiness completed.
- Phase 0A shared rail closure completed.
- Phase 1 unblocked for kickoff/planning only.
- PRD-P1-WX-KICKOFF defines sequence.
- Next ticket is PRD-P1-WX-01.
- Weather runtime implementation not started.
- External weather/API connector behavior not started.
- Production execution not approved.
- Live trading/order placement/autonomy not approved.
- DuckDB is dev/research-only.
- Bounded local research posture is preserved.
- Docs/static tests are preferred for governance tickets.

## 3) First thing to ask user
Should we proceed directly to PRD-P1-WX-01, or first discuss strategic decisions around weather bot scope, canonical event graph pilot, provider research depth, market taxonomy, and idea registry prioritization?
