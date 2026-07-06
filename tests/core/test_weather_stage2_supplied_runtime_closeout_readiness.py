"""Static checks for Weather Bot supplied runtime closeout/readiness inventory."""

from pathlib import Path


DOMAIN_PACKET = Path("docs/meta/domain_packets/WEATHER_BOT_PACKET.md")


def _packet_text() -> str:
    return DOMAIN_PACKET.read_text(encoding="utf-8")


def test_weather_stage2_supplied_runtime_closeout_readiness_inventory() -> None:
    text = _packet_text()

    assert "Weather Bot Stage 2 Runtime Foundation — Supplied Input Track" in text
    assert "full-chain integration smoke" in text
    assert "full-chain negative smoke" in text

    for field in ("condition_id", "token_id", "outcome"):
        assert field in text

    assert "Source fetching remains held/not approved" in text
    assert "Provider/source implementation remains held/not approved" in text
    assert "Paper trading remains not approved" in text
    assert "Trading/execution remains not approved" in text
    assert "Persistence and export writing are not implemented in this track" in text
    assert "Queue/service/scheduler/broker behavior is not implemented in this track" in text
    assert (
        "Owner-decision capture and operator decision execution are not implemented in this track"
        in text
    )
    assert "The next phase is an approval/request/planning gate, not implementation" in text
    assert "WEATHER-BOT-STAGE2-SOURCE-PROVIDER-RUNTIME-APPROVAL-REQUEST-01" in text
