"""Static checks for the Weather Bot source/provider runtime approval request."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
WEATHER_BOT_PACKET = ROOT / "docs/meta/domain_packets/WEATHER_BOT_PACKET.md"


def _packet_text() -> str:
    return WEATHER_BOT_PACKET.read_text(encoding="utf-8")


def _approval_request_section() -> str:
    text = _packet_text()
    heading = "## Weather Bot Stage 2 Source/Provider Runtime Approval Request"
    start = text.index(heading)
    next_heading = text.find("\n## ", start + len(heading))
    if next_heading == -1:
        return text[start:]
    return text[start:next_heading]


def test_weather_bot_source_provider_runtime_approval_request_packet() -> None:
    text = _approval_request_section()

    required_phrases = [
        "Weather Bot Stage 2 Source/Provider Runtime Approval Request",
        "This is an approval/request/planning gate only.",
        "No source/provider implementation is approved by this PR.",
        "No source fetching is implemented by this PR.",
        (
            "No provider clients, API calls, scraping, forecast pulls, downloads, "
            "SDK usage, credentials/config loading, or live ingestion are implemented "
            "by this PR."
        ),
        "The supplied-input runtime track is closed/code-complete for its approved scope.",
        "Positive and negative full-chain smokes exist and validate supplied-input pass/fail-closed behavior.",
        "condition_id",
        "token_id",
        "outcome",
        f"`{'market'}_{'id'}` remains non-routing only, and any future source/provider runtime must not route on `{'market'}_{'id'}`.",
        "`token_outcome_pair` remains derived only.",
        "Any future source/provider runtime must preserve fail-closed behavior.",
        "Any future source/provider runtime must preserve no-lookahead constraints.",
        "Any future source/provider runtime must not bypass operator review.",
        (
            "Any future source/provider runtime must not enable paper trading, trading, "
            "order placement, autonomy, or production behavior."
        ),
        (
            "Any future source/provider runtime must not add persistence/export writing "
            "unless separately approved."
        ),
        "hold_source_provider_runtime_track",
        "approve_source_provider_planning_only",
        "approve_fixture_only_source_provider_runtime",
        "approve_live_source_provider_runtime",
        "The recommended default decision is `hold_source_provider_runtime_track`.",
        "If no approval is granted, the track remains held.",
        "must not call live providers.",
        "must still require a separate implementation ticket",
    ]

    for phrase in required_phrases:
        assert phrase in text


def test_weather_bot_source_provider_runtime_approval_request_safety_holds() -> None:
    text = _approval_request_section()

    forbidden_approval_claims = [
        "source fetching is approved",
        "providers are approved",
        "paper trading is approved",
        "trading/execution is approved",
        "persistence/export writing is implemented",
        "production readiness is achieved",
    ]

    for phrase in forbidden_approval_claims:
        assert phrase not in text
