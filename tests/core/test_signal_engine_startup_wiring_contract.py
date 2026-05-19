"""Phase 0A-05F startup wiring contract checks for main integration.

These checks are intentionally static and non-invasive.
"""
from __future__ import annotations

import ast
from pathlib import Path

import pytest


MAIN_PATH = Path(__file__).resolve().parents[2] / "meg" / "main.py"


def _main_ast() -> ast.AST:
    return ast.parse(MAIN_PATH.read_text(encoding="utf-8"))


def test_main_imports_signal_engine_runner() -> None:
    source = MAIN_PATH.read_text(encoding="utf-8")

    assert "from meg.signal_engine import runner as signal_engine_runner" in source


def test_main_wires_signal_engine_runner_task_once() -> None:
    source = MAIN_PATH.read_text(encoding="utf-8")

    assert 'name="signal_engine_runner"' in source
    assert source.count('name="signal_engine_runner"') == 1


def test_existing_main_task_names_are_still_present() -> None:
    source = MAIN_PATH.read_text(encoding="utf-8")

    for task_name in (
        'name="polygon_feed"',
        'name="pre_filter_pipeline"',
        'name="signal_aggregator"',
        'name="position_monitor"',
        'name="telegram_bot"',
    ):
        assert task_name in source
