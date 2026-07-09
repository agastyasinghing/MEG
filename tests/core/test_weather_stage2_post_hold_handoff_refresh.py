"""Static checks for the Weather Bot Stage 2 post-hold handoff refresh."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
REFRESHED_META_DOCS = [
    ROOT / "docs/meta/MEG_ACTIVE_STATE.md",
    ROOT / "docs/meta/MEG_CHAT_HANDOFF.md",
    ROOT / "docs/meta/MEG_NEXT_CHAT_BOOTSTRAP_PROMPT.md",
]


def _combined_refreshed_meta_docs() -> str:
    return "\n\n".join(path.read_text(encoding="utf-8") for path in REFRESHED_META_DOCS)


def test_weather_stage2_post_hold_handoff_refresh_required_state() -> None:
    text = _combined_refreshed_meta_docs()

    required_phrases = [
        "Weather Bot Stage 2 supplied-input runtime foundation is code-complete for its approved in-memory supplied-input scope.",
        "source_provider_runtime_decision: hold_source_provider_runtime_track",
        "Source/provider runtime remains held.",
        "Source fetching remains not approved.",
        "Provider/source implementation remains not approved.",
        "Fixture-only source/provider runtime remains not approved.",
        "Live source/provider runtime remains not approved.",
        "Paper trading remains not approved.",
        "Trading/execution remains not approved.",
        "Persistence/export writing remain not implemented and not approved.",
        "Queue/service/scheduler/broker behavior remains not implemented and not approved.",
        "Owner-decision capture and operator decision execution remain not implemented and not approved.",
        "Production readiness is not achieved.",
        "condition_id",
        "token_id",
        "outcome",
        "market\\_id remains non-routing only.",
        "token_outcome_pair` remains derived only.",
        "requires a separate explicit approval PR before implementation.",
        "next valid ticket must be an explicit approval-change request, not implementation.",
    ]

    for phrase in required_phrases:
        assert phrase in text


def test_weather_stage2_post_hold_handoff_refresh_safety_holds() -> None:
    text = _combined_refreshed_meta_docs()

    forbidden_approval_claims = [
        "source fetching is approved",
        "providers are approved",
        "fixture-only runtime is approved",
        "live provider runtime is approved",
        "paper trading is approved",
        "trading/execution is approved",
        "persistence/export writing is implemented",
        "production readiness is achieved",
    ]

    for phrase in forbidden_approval_claims:
        assert phrase not in text
