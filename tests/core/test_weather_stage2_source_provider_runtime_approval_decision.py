"""Static checks for the Weather Bot source/provider runtime approval decision."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
WEATHER_BOT_PACKET = ROOT / "docs/meta/domain_packets/WEATHER_BOT_PACKET.md"


def _approval_decision_section() -> str:
    text = WEATHER_BOT_PACKET.read_text(encoding="utf-8")
    heading = "## Weather Bot Stage 2 Source/Provider Runtime Approval Decision"
    start = text.index(heading)
    next_heading = text.find("\n## ", start + len(heading))
    if next_heading == -1:
        return text[start:]
    return text[start:next_heading]


def test_weather_bot_source_provider_runtime_approval_decision_packet() -> None:
    text = _approval_decision_section()

    required_phrases = [
        "Weather Bot Stage 2 Source/Provider Runtime Approval Decision",
        "This is a project approval-decision record for the source/provider runtime track only.",
        "It is not owner-decision capture.",
        "It is not operator decision execution.",
        "It is not trading approval.",
        "It is not paper-trading approval.",
        "It is not production approval.",
        "source_provider_runtime_decision: hold_source_provider_runtime_track",
        "source/provider runtime implementation remains held.",
        "Source fetching remains not approved.",
        "Provider/source implementation remains not approved.",
        (
            "Live provider clients, API calls, scraping, forecast pulls, downloads, "
            "SDK usage, credentials/config loading, or live ingestion remain not approved."
        ),
        "Fixture-only source/provider runtime is not approved by this decision.",
        "Live source/provider runtime is not approved by this decision.",
        (
            "Planning-only source/provider follow-up may be allowed only if it remains "
            "static documentation/planning and does not add runtime behavior."
        ),
        "condition_id",
        "token_id",
        "outcome",
        "market\\_id remains non-routing only.",
        "token_outcome_pair remains derived only.",
        "No-lookahead and fail-closed constraints remain mandatory for any future approval.",
        "Any future move out of hold requires a separate explicit approval PR.",
        "WEATHER-BOT-STAGE2-SOURCE-PROVIDER-RUNTIME-HOLD-CLOSEOUT-01",
    ]

    for phrase in required_phrases:
        assert phrase in text


def test_weather_bot_source_provider_runtime_approval_decision_safety_holds() -> None:
    text = _approval_decision_section()

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
