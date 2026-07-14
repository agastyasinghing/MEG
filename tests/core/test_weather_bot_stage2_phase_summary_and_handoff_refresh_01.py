from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CANONICAL_ID = "WEATHER-BOT-STAGE2-PHASE-SUMMARY-AND-HANDOFF-REFRESH-01"
DOC = ROOT / "docs/prd/WEATHER-BOT-STAGE2-PHASE-SUMMARY-AND-HANDOFF-REFRESH-01.md"
HANDOFFS = {
    "docs/meta/MEG_ACTIVE_STATE.md": "meg_active_state_md",
    "docs/meta/MEG_CHAT_HANDOFF.md": "meg_chat_handoff_md",
    "docs/meta/MEG_NEXT_CHAT_BOOTSTRAP_PROMPT.md": "meg_next_chat_bootstrap_prompt_md",
    "docs/meta/domain_packets/WEATHER_BOT_PACKET.md": "weather_bot_packet_md",
}
SECTIONS = [
    "Status and scope",
    "Immediate predecessor and merge verification",
    "Stage 2 approved-scope completion summary",
    "Completed fixture-only runtime-chain summary",
    "Positive full-chain validation summary",
    "Negative fail-closed validation summary",
    "Current canonical routing posture",
    "Current no-lookahead and fail-closed posture",
    "Current live-provider and source-fetching boundary",
    "Current Stage 3 boundary",
    "Current later-stage boundary",
    "Current persistence, service, and workflow boundary",
    "Repo-native handoff documents refreshed",
    "Fresh-chat bootstrap posture",
    "Controlling-state precedence",
    "New-chat instructions",
    "Recommended next action",
    "Machine-checkable Weather Bot Stage 2 phase-summary and handoff-refresh assignments",
    "Acceptance criteria",
]
EXPECTED_ASSIGNMENTS = {
    "weather bot planning stage": {"weather_bot_stage2_phase_summary_and_handoff_refresh"},
    "immediate predecessor pr": {"pr_355"},
    "handoff lifecycle status": {"docs_static_test_only", "meta_handoff_refresh_only", "final_repo_ticket_before_new_chat"},
    "stage2 approved scope status": {"fixture_only_source_provider_runtime_chain_complete", "eighteen_runtime_objects_landed", "positive_full_chain_validation_complete", "expected_fail_closed_negative_validation_complete", "closeout_readiness_complete"},
    "canonical routing field": {"condition_id", "token_id", "outcome"},
    "non routing field": {"market_id"},
    "derived identifier field": {"token_outcome_pair"},
    "live runtime posture": {"live_provider_runtime_not_approved", "live_source_fetching_not_approved"},
    "stage3 posture": {"stage3_not_approved", "scoring_not_approved", "evaluation_execution_not_approved"},
    "later stage posture": {"paper_simulation_not_approved", "runtime_observation_not_approved", "trading_execution_not_approved"},
    "persistence posture": {"no_persistence", "no_export_writing"},
    "service posture": {"no_real_queue_service", "no_scheduler", "no_broker"},
    "workflow posture": {"no_owner_decision_capture", "no_operator_decision_execution", "no_durable_completion_side_effect"},
    "refreshed handoff file": set(HANDOFFS.values()),
    "controlling precedence": {"post_pr_355_stage2_handoff_controls"},
    "new chat posture": {"ready_for_new_chat", "no_ticket_until_user_request", "stage3_planning_readiness_only_after_user_direction"},
    "recommended next action": {"start_new_chat_from_refreshed_bootstrap"},
    "evidence status": {"stage2_handoff_refresh_recorded"},
    "label confidence": {"confirmed"},
}


def _read(path: Path = DOC) -> str:
    return path.read_text(encoding="utf-8")


def _section(text: str, name: str) -> str:
    marker = f"## {name}\n"
    assert marker in text
    return text.split(marker, 1)[1].split("\n## ", 1)[0].strip()


def _assignments(text: str) -> dict[str, set[str]]:
    section = _section(text, "Machine-checkable Weather Bot Stage 2 phase-summary and handoff-refresh assignments")
    assert section.startswith("```assignments")
    assert section.endswith("```")
    parsed: dict[str, set[str]] = {}
    for line in section.splitlines()[1:-1]:
        key, value = line.split(": ", 1)
        parsed.setdefault(key, set()).add(value)
    return parsed


def _newest_section(path: str) -> str:
    text = _read(ROOT / path)
    first = text.split("\n## ", 2)[1]
    return "## " + first


def test_document_exists_title_id_sections_and_predecessor() -> None:
    assert DOC.exists()
    text = _read()
    assert text.startswith(f"# {CANONICAL_ID}\n")
    assert f"Canonical ID: {CANONICAL_ID}" in text
    for section in SECTIONS:
        assert _section(text, section)
    predecessor = _section(text, "Immediate predecessor and merge verification")
    assert "Immediate predecessor: PR #355" in predecessor
    assert "9f8d5bb Merge pull request #355" in predecessor
    assert "not PR #355's preview merge SHA" in predecessor


def test_handoff_files_refreshed_with_controlling_post_pr_355_sections() -> None:
    doc_text = _read()
    refreshed = _section(doc_text, "Repo-native handoff documents refreshed")
    for path in HANDOFFS:
        assert path in refreshed
        section = _newest_section(path)
        lower = section.lower()
        assert "post-pr #355" in lower
        assert "controlling" in lower
        assert "controls over stale" in lower or "controls over" in lower
        assert "stage 2" in lower


def test_stage2_completion_and_runtime_chain_count() -> None:
    text = _read()
    summary = _section(text, "Stage 2 approved-scope completion summary")
    chain = _section(text, "Completed fixture-only runtime-chain summary")
    assert "approved fixture-only/local-static/caller-supplied" in summary
    assert "PRs #337 through #354" in summary
    assert "PR #355 closed" in summary
    assert "live-provider Stage 2 is not complete" in summary
    assert "All 18 fixture-only runtime-chain objects landed" in chain
    assert chain.count("bridge") >= 17
    assert "caller-supplied and in-memory" in chain


def test_positive_and_negative_smoke_semantics() -> None:
    positive = _section(_read(), "Positive full-chain validation summary")
    assert "fully valid supplied chain" in positive
    assert "metadata validation only" in positive
    assert "no smoke is executed or generated" in positive
    assert "runtime_gate_ready" in positive
    negative = _section(_read(), "Negative fail-closed validation summary")
    assert "Expected fail-closed representation" in negative
    assert "positive bridge must pass" in negative
    assert "supplied negative-smoke record must pass" in negative
    assert "intentionally failing nested integration smoke is not directly required to pass" in negative
    assert "validates as `PASSED`" in negative
    assert "runtime_gate_blocked" in negative
    assert "No progression, execution, delivery, generation, smoke execution, or failure injection" in negative
    assert "nested integration smoke must pass" not in negative.lower()


def test_boundaries_canonical_routing_and_no_owner_decision_capture_lane() -> None:
    text = _read()
    canonical = _section(text, "Current canonical routing posture")
    for field in ("condition_id", "token_id", "outcome"):
        assert f"`{field}`" in canonical
    assert "`market_id` is non-routing only" in canonical
    assert "`token_outcome_pair` is derived only" in canonical
    assert "no timestamp parsing or comparison" in canonical.lower()
    assert "Stage 3 remains not approved" in _section(text, "Current Stage 3 boundary")
    assert "Live providers" in _section(text, "Current live-provider and source-fetching boundary")
    assert "remain not approved" in _section(text, "Current later-stage boundary")
    workflow = _section(text, "Current persistence, service, and workflow boundary")
    assert "owner-decision capture" in workflow
    assert "No owner-decision capture lane is introduced" in workflow


def test_bootstrap_blocks_automatic_tickets_and_stage3_implementation() -> None:
    bootstrap = _read(ROOT / "docs/meta/MEG_NEXT_CHAT_BOOTSTRAP_PROMPT.md")
    newest = _newest_section("docs/meta/MEG_NEXT_CHAT_BOOTSTRAP_PROMPT.md")
    assert "Do not create a repository ticket until the user explicitly asks" in bootstrap
    assert "begin with Stage 3 planning/readiness analysis rather than implementation" in bootstrap
    assert "live-provider/source-fetching runtime and Stage 3 remain unapproved" in bootstrap
    assert "avoid market_id routing" in bootstrap
    assert "Preserve token_outcome_pair as derived only" in bootstrap
    assert "Avoid owner-decision capture" in bootstrap
    assert "initial-scaffold" in newest or "stale" in newest


def test_newest_sections_supersede_stale_initial_scaffold_recommendations() -> None:
    for path in HANDOFFS:
        newest = _newest_section(path).lower()
        assert "fixture-only-source-provider-runtime-scaffold-01" not in newest
        assert "another runtime bridge" not in newest or "not another runtime bridge" in newest
        assert "no later stage begins automatically" in newest or "stage 3" in newest


def test_assignment_parser_is_section_scoped_and_closed() -> None:
    text = _read() + "\nweather bot planning stage: outside_value\n"
    assignments = _assignments(text)
    assert assignments == EXPECTED_ASSIGNMENTS
    assert "outside_value" not in assignments.get("weather bot planning stage", set())
