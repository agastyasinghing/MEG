# MEG Chat Handoff

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
