"""Static checks for the Weather Bot Stage 2 fixture-only source/provider approval change."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DOCS = [
    ROOT / "docs/meta/domain_packets/WEATHER_BOT_PACKET.md",
    ROOT / "docs/meta/MEG_ACTIVE_STATE.md",
    ROOT / "docs/meta/MEG_CHAT_HANDOFF.md",
    ROOT / "docs/meta/MEG_NEXT_CHAT_BOOTSTRAP_PROMPT.md",
]


def _texts() -> list[str]:
    return [path.read_text(encoding="utf-8") for path in DOCS]


def test_fixture_only_source_provider_runtime_approval_change_recorded() -> None:
    required_phrases = [
        "Weather Bot Stage 2 Fixture-Only Source/Provider Runtime Approval Change",
        "source_provider_runtime_decision: approve_fixture_only_source_provider_runtime",
        "source_provider_runtime_decision: hold_source_provider_runtime_track",
        "approval is limited to fixture-only/local-static/caller-supplied source-provider runtime planning and implementation in a future PR",
        "This PR does not implement fixture-only runtime.",
        "live source/provider runtime remains not approved",
        "Live providers remain not approved.",
        "Live source fetching remains not approved.",
        "Provider clients/API calls/scraping/forecast pulls/downloads/SDK usage/credentials/config loading/live ingestion remain not approved.",
        "Paper trading remains not approved.",
        "Trading/execution remains not approved.",
        "Persistence/export writing remain not approved by this decision.",
        "Queue/service/scheduler/broker behavior remains not approved by this decision.",
        "Owner-decision capture/operator decision execution remain not approved by this decision.",
        "Production readiness is not achieved.",
        "fixture-only runtime implementation must preserve fail-closed behavior",
        "fixture-only runtime implementation must preserve no-lookahead constraints",
        "fixture-only runtime implementation must not route on market\\_id",
        "condition_id",
        "token_id",
        "outcome",
        "token_outcome_pair remains derived only.",
        "fixture-only runtime implementation must not bypass operator review",
        "WEATHER-BOT-STAGE2-FIXTURE-ONLY-SOURCE-PROVIDER-RUNTIME-SCAFFOLD-01",
    ]

    for text in _texts():
        for phrase in required_phrases:
            assert phrase in text


def test_fixture_only_approval_change_preserves_safety_boundaries() -> None:
    forbidden_claims = [
        "live source fetching is approved",
        "live providers are approved",
        "paper trading is approved",
        "trading/execution is approved",
        "persistence/export writing is implemented",
        "production readiness is achieved",
    ]

    combined_text = "\n\n".join(_texts())
    for phrase in forbidden_claims:
        assert phrase not in combined_text
