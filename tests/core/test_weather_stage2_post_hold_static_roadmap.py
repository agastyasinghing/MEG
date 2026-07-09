"""Static checks for the Weather Bot Stage 2 post-hold static roadmap."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
WEATHER_BOT_PACKET = ROOT / "docs/meta/domain_packets/WEATHER_BOT_PACKET.md"


def _post_hold_static_roadmap_section() -> str:
    text = WEATHER_BOT_PACKET.read_text(encoding="utf-8")
    heading = "## Weather Bot Stage 2 Post-Hold Static Roadmap"
    start = text.index(heading)
    next_heading = text.find("\n## ", start + len(heading))
    if next_heading == -1:
        return text[start:]
    return text[start:next_heading]


def test_weather_bot_stage2_post_hold_static_roadmap_packet() -> None:
    text = _post_hold_static_roadmap_section()

    required_phrases = [
        "Weather Bot Stage 2 Post-Hold Static Roadmap",
        "This is a static roadmap only.",
        "It does not reopen source/provider runtime implementation.",
        "It does not approve source fetching.",
        "It does not approve provider/source implementation.",
        "It does not approve fixture-only source/provider runtime.",
        "It does not approve live source/provider runtime.",
        "It does not approve paper trading.",
        "It does not approve trading/execution.",
        "It does not approve persistence/export writing.",
        "It does not approve queue/service/scheduler/broker behavior.",
        "It does not approve owner-decision capture or operator decision execution.",
        "It does not approve production behavior.",
        "source_provider_runtime_decision: hold_source_provider_runtime_track",
        "Source/provider runtime remains held until a separate explicit approval PR changes the decision.",
        (
            "The supplied-input runtime track remains the only code-complete approved "
            "runtime foundation for Weather Bot Stage 2."
        ),
        "condition_id",
        "token_id",
        "outcome",
        "market\\_id remains non-routing only.",
        "token_outcome_pair remains derived only.",
        "No-lookahead and fail-closed constraints remain mandatory for any future phase.",
        "source/provider planning-only gate",
        "fixture-only source/provider runtime approval gate",
        "live source/provider runtime approval gate",
        "persistence/export approval gate",
        "operator workflow approval gate",
        "paper-trade/evaluation approval gate",
        "production readiness approval gate",
        "Each future lane requires a separate explicit approval PR before implementation.",
        "WEATHER-BOT-STAGE2-POST-HOLD-HANDOFF-REFRESH-01",
    ]

    for phrase in required_phrases:
        assert phrase in text


def test_weather_bot_stage2_post_hold_static_roadmap_safety_holds() -> None:
    text = _post_hold_static_roadmap_section()

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
