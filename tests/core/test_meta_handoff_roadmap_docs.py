from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs" / "meta"


def _read(p: str) -> str:
    return (DOCS / p).read_text(encoding="utf-8").lower()


def test_all_meta_docs_exist() -> None:
    files = [
        "MEG_CURRENT_STATE.md",
        "MEG_CHAT_HANDOFF.md",
        "MEG_WORKFLOW_PLAYBOOK.md",
        "MEG_TICKET_PROMPT_TEMPLATE.md",
        "MEG_PHASE_HISTORY_SUMMARY.md",
        "MEG_DUCKDB_RESEARCH_RAIL_EXPLAINER.md",
        "MEG_STRATEGIC_IDEA_REGISTRY.md",
        "MEG_NEXT_CHAT_BOOTSTRAP_PROMPT.md",
    ]
    for name in files:
        assert (DOCS / name).exists(), name


def test_required_content_presence() -> None:
    state = _read("MEG_CURRENT_STATE.md")
    assert "prd-p1-wx-01" in state
    assert "no weather bot runtime behavior has been implemented yet" in state

    handoff = _read("MEG_CHAT_HANDOFF.md")
    assert "do not open unnecessary issues" in handoff
    assert "check pr" in handoff

    playbook = _read("MEG_WORKFLOW_PLAYBOOK.md")
    assert "blockers" in playbook and "non-blockers" in playbook
    assert "avoid git status" in playbook
    assert "avoid mtime" in playbook

    template = _read("MEG_TICKET_PROMPT_TEMPLATE.md")
    for phrase in ["main prompt template", "self-review prompt template", "fix prompt template", "pr review response template"]:
        assert phrase in template

    history = _read("MEG_PHASE_HISTORY_SUMMARY.md")
    for phrase in ["phase 0a", "phase 0b", "phase 1 weather bot gating summary"]:
        assert phrase in history

    duck = _read("MEG_DUCKDB_RESEARCH_RAIL_EXPLAINER.md")
    assert "dev/research" in duck and "not the production database" in duck
    assert "what duckdb proved" in duck and "what duckdb did not prove" in duck


def test_strategic_ideas_and_bootstrap_and_safety() -> None:
    ideas = _read("MEG_STRATEGIC_IDEA_REGISTRY.md")
    required = [
        "canonical cross-market event graph",
        "proposal envelope schema",
        "runtime topology documentation",
        "research vs production boundary",
        "golden path tests",
        "reviewer-facing readme section",
        "multi-market vision section",
        "weather canonical event taxonomy",
        "weather resolution rule risk classifier",
        "weather provider compatibility matrix",
        "forecast uncertainty / probability distribution model",
        "weather market trap taxonomy",
        "regime detection",
        "synthetic fair-value engine",
        "simulation and counterfactual backtesting engine",
        "meta-whale / cross-venue identity tracking",
        "hero end-to-end story",
    ]
    for phrase in required:
        assert phrase in ideas

    boot = _read("MEG_NEXT_CHAT_BOOTSTRAP_PROMPT.md")
    for phrase in [
        "docs/meta/meg_current_state.md",
        "docs/meta/meg_chat_handoff.md",
        "docs/meta/meg_workflow_playbook.md",
        "docs/meta/meg_ticket_prompt_template.md",
        "docs/meta/meg_phase_history_summary.md",
        "docs/meta/meg_duckdb_research_rail_explainer.md",
        "docs/meta/meg_strategic_idea_registry.md",
        "prd-p1-wx-01",
    ]:
        assert phrase in boot

    combined = "\n".join(_read(f) for f in [
        "MEG_CURRENT_STATE.md",
        "MEG_CHAT_HANDOFF.md",
        "MEG_WORKFLOW_PLAYBOOK.md",
        "MEG_PHASE_HISTORY_SUMMARY.md",
    ])
    assert "no runtime behavior" in combined
    assert "not approved" in combined
    assert "connector" in combined
    assert "trading" in combined and "autonomy" in combined and "order placement" in combined


def test_no_duckdb_or_generated_output_dirs() -> None:
    assert not any(ROOT.rglob("*.duckdb"))
    banned_dirs = [
        "generated_sql",
        "generated_reports",
        "generated_dictionary",
        "fixture_output",
    ]
    for d in banned_dirs:
        assert not any(p for p in ROOT.rglob(d) if p.is_dir())


def test_no_legacy_identifier_literal_in_new_artifacts() -> None:
    targets = [
        DOCS / "MEG_CURRENT_STATE.md",
        DOCS / "MEG_CHAT_HANDOFF.md",
        DOCS / "MEG_WORKFLOW_PLAYBOOK.md",
        DOCS / "MEG_TICKET_PROMPT_TEMPLATE.md",
        DOCS / "MEG_PHASE_HISTORY_SUMMARY.md",
        DOCS / "MEG_DUCKDB_RESEARCH_RAIL_EXPLAINER.md",
        DOCS / "MEG_STRATEGIC_IDEA_REGISTRY.md",
        DOCS / "MEG_NEXT_CHAT_BOOTSTRAP_PROMPT.md",
        Path(__file__),
    ]
    for t in targets:
        legacy = "market" + "_id"
        assert legacy not in t.read_text(encoding="utf-8")
