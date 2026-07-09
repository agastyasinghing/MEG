"""Static checks for the Weather Bot source/provider runtime hold closeout."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
WEATHER_BOT_PACKET = ROOT / "docs/meta/domain_packets/WEATHER_BOT_PACKET.md"


def _hold_closeout_section() -> str:
    text = WEATHER_BOT_PACKET.read_text(encoding="utf-8")
    heading = "## Weather Bot Stage 2 Source/Provider Runtime Hold Closeout"
    start = text.index(heading)
    next_heading = text.find("\n## ", start + len(heading))
    if next_heading == -1:
        return text[start:]
    return text[start:next_heading]


def test_weather_bot_source_provider_runtime_hold_closeout_packet() -> None:
    text = _hold_closeout_section()

    required_phrases = [
        "Weather Bot Stage 2 Source/Provider Runtime Hold Closeout",
        "This is a hold-closeout record for the source/provider runtime track.",
        "It closes the current source/provider approval-request and approval-decision sequence.",
        "source_provider_runtime_decision: hold_source_provider_runtime_track",
        "source/provider runtime remains held.",
        "Source fetching remains not approved.",
        "Provider/source implementation remains not approved.",
        "Fixture-only source/provider runtime remains not approved.",
        "Live source/provider runtime remains not approved.",
        (
            "Provider clients, API calls, scraping, forecast pulls, downloads, SDK usage, "
            "credentials/config loading, and live ingestion remain not approved."
        ),
        (
            "Planning-only follow-up may occur only as static documentation/planning, "
            "and no runtime behavior may be added."
        ),
        "Paper trading remains not approved.",
        "Trading/execution remains not approved.",
        "Persistence/export writing remain not implemented and not approved by this closeout.",
        "Queue/service/scheduler/broker behavior remains not implemented and not approved by this closeout.",
        (
            "Owner-decision capture and operator decision execution remain not implemented "
            "and not approved by this closeout."
        ),
        "Durable workflow-completion side effects remain not implemented and not approved by this closeout.",
        "Production readiness is not achieved.",
        "condition_id",
        "token_id",
        "outcome",
        "market\\_id remains non-routing only.",
        "`token_outcome_pair` remains derived only.",
        "No-lookahead and fail-closed constraints remain mandatory for any future approval.",
        "Any future move out of hold requires a separate explicit approval PR.",
        "WEATHER-BOT-STAGE2-POST-HOLD-STATIC-ROADMAP-01",
    ]

    for phrase in required_phrases:
        assert phrase in text


def test_weather_bot_source_provider_runtime_hold_closeout_safety_holds() -> None:
    text = _hold_closeout_section()

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
