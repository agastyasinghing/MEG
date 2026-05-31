"""Static checks for MEG-OPS-01 repo-native orchestration docs."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

DOCS = {
    "agents": REPO_ROOT / "AGENTS.md",
    "active": REPO_ROOT / "docs/meta/MEG_ACTIVE_STATE.md",
    "router": REPO_ROOT / "docs/meta/MEG_CONTEXT_ROUTER.md",
    "style": REPO_ROOT / "docs/meta/MEG_TICKET_STYLE_GUIDE.md",
    "review": REPO_ROOT / "docs/meta/MEG_PR_REVIEW_CHECKLIST.md",
    "ledger": REPO_ROOT / "docs/meta/MEG_PHASE_LEDGER.md",
    "bootstrap": REPO_ROOT / "docs/meta/MEG_NEXT_CHAT_BOOTSTRAP_PROMPT.md",
    "agent_workflow": REPO_ROOT / "docs/meta/MEG_AGENT_WORKFLOW.md",
    "weather_packet": REPO_ROOT / "docs/meta/domain_packets/WEATHER_BOT_PACKET.md",
    "core_packet": REPO_ROOT / "docs/meta/domain_packets/CORE_WORKFLOW_PACKET.md",
}

OPS_DOC_KEYS = tuple(DOCS)


def _read(key: str) -> str:
    return DOCS[key].read_text(encoding="utf-8")


def _lower(key: str) -> str:
    return _read(key).lower()


def _assert_contains(text: str, required: list[str]) -> None:
    missing = [item for item in required if item not in text]
    assert not missing, missing


def test_required_ops_docs_exist() -> None:
    for path in DOCS.values():
        assert path.exists(), path


def test_agents_contains_core_operating_rules() -> None:
    text = _lower("agents")
    _assert_contains(
        text,
        [
            "meg is prd-driven",
            "read repo meta docs before generating tickets or reviewing prs",
            "do not open issues unless explicitly asked or approved",
            "do not merge prs",
            "do not approve prs as final authority",
            "do not approve connectors, runtime behavior, trading, order placement, or autonomy",
            "do not change secrets",
            "do not alter source-of-truth prds without explicit approval",
            "preserve closed-set enum/status/value requirements exactly",
            "do not invent hybrid/custom values unless explicitly allowed",
            "use `tests/core` for static prd/meta tests",
            "brief verdict/context",
            "main codex prompt in one copyable code block",
            "self-review prompt in one copyable code block",
            "files changed",
            "scope summary",
            "safety/non-approval summary",
            "test command results",
            "final merge recommendation",
            "recommended next ticket",
        ],
    )


def test_active_state_required_fields_and_post_194_gate() -> None:
    text = _lower("active")
    _assert_contains(
        text,
        [
            "## current active project",
            "## current active area",
            "## current active phase",
            "## latest merged pr",
            "## latest reviewed pr",
            "## current approved gate",
            "## next possible gate",
            "## explicitly not approved",
            "## current controlling docs",
            "## current weather bot status summary",
            "## current ticket style",
            "## current pr review style",
            "## known blockers",
            "## last updated by",
            "## how to use this file",
            "pr #194",
            "next possible gate is static fixture implementation approval request only",
        ],
    )
    for phrase in [
        "fixture implementation is not approved",
        "ingestion is not approved",
        "scoring is not approved",
        "runtime observation is not approved",
        "trading is not approved",
        "order placement is not approved",
        "autonomy is not approved",
    ]:
        assert phrase in text


def test_context_router_routes_are_present() -> None:
    text = _lower("router")
    _assert_contains(
        text,
        [
            "fresh chat bootstrap",
            "generating a weather bot ticket",
            "reviewing a pr",
            "checking current project state",
            "generating a codex prompt",
            "generating a self-review prompt",
            "evaluating closed-set/static-test requirements",
            "discussing weather bot strategy",
            "discussing agentic workflow/orchestration",
            "deciding next ticket after pr merge",
            "handling blocker/fix prompts",
            "required docs",
            "optional docs",
            "expected output",
            "forbidden actions",
        ],
    )


def test_ticket_style_required_response_and_return_formats() -> None:
    text = _lower("style")
    _assert_contains(
        text,
        [
            "required assistant response structure",
            "brief verdict/context",
            "next ticket name",
            "bigger-picture fit",
            "research depth flag",
            "language/tooling suitability check",
            "main codex prompt in one code block",
            "self-review prompt in one code block",
            "required codex return format",
            "files changed",
            "scope summary",
            "safety/non-approval summary",
            "test command results",
            "final merge recommendation",
            "recommended next ticket",
            "closed-set discipline",
            "tests must reject hybrid/custom actual values",
            "no optional-missing exceptions unless explicitly approved",
        ],
    )


def test_pr_review_checklist_core_items() -> None:
    text = _lower("review")
    _assert_contains(
        text,
        [
            "changed-file scope check",
            "allowed-files/do-not-modify check",
            "closed-set completeness check",
            "machine-checkable section scope check",
            "ci/workflow check",
            "ci status",
            "final merge/block recommendation format",
            "recommended next ticket format",
            "special blocker/fix review procedure",
        ],
    )


def test_phase_ledger_references_recent_sequence() -> None:
    text = _read("ledger")
    for item in ["PR #191", "PR #192", "PR #193", "PR #194", "MEG-OPS-01"]:
        assert item in text


def test_bootstrap_tells_new_chat_to_wait_for_user_ticket_request() -> None:
    text = _lower("bootstrap")
    _assert_contains(
        text,
        [
            "do not generate a ticket until the user asks",
            "do not open issues",
            "do not approve runtime, connectors, trading, or autonomy",
            "do not assume implementation approval from planning or approval-request docs",
        ],
    )


def test_agent_workflow_prohibitions() -> None:
    text = _lower("agent_workflow")
    _assert_contains(
        text,
        [
            "no autonomous builder by default",
            "auto-merge",
            "change secrets",
            "approve connectors, runtime, trading, order placement, or autonomy",
            "no full autonomy",
        ],
    )


def test_weather_packet_current_gate() -> None:
    text = _lower("weather_packet")
    _assert_contains(
        text,
        [
            "stage 2 skeleton v1 complete",
            "pr #194",
            "next possible weather bot gate is static fixture implementation approval request only",
            "fixture implementation is not approved",
        ],
    )


def test_core_workflow_packet_roles_and_no_autonomous_merge_deploy() -> None:
    text = _lower("core_packet")
    _assert_contains(
        text,
        [
            "opus/gpt-5.5/codex roles",
            "opus/gpt-5.5",
            "codex",
            "human operator",
            "do not perform an autonomous merge or deploy",
        ],
    )


def test_ops_docs_do_not_contain_positive_approval_drift() -> None:
    bad_fragments = [
        "auto-merge" + " approved",
        "autonomous builder" + " approved",
        "runtime" + " approved",
        "trading" + " approved",
        "order placement" + " approved",
        "connector implementation" + " approved",
        "fixture implementation" + " approved",
        "ingestion" + " approved",
        "scoring" + " approved",
        "backtesting" + " approved",
    ]
    offenders: dict[str, list[str]] = {}
    for key in OPS_DOC_KEYS:
        text = _lower(key)
        hits = [fragment for fragment in bad_fragments if fragment in text]
        if hits:
            offenders[key] = hits
    assert offenders == {}
