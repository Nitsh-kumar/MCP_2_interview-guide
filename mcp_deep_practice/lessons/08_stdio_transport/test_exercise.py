"""
lessons/08_stdio_transport/test_exercise.py

Executable specification for Lesson 08 exercise.
Validates stdio line framing parsing and safe stderr logging.
"""

from __future__ import annotations

import importlib
import io
import pytest
from mcp import Client

ex = importlib.import_module("lessons.08_stdio_transport.exercise")


def test_parse_stdio_line_valid_jsonrpc() -> None:
    valid_line = '{"jsonrpc": "2.0", "id": 1, "method": "ping"}\n'
    data, err = ex.parse_stdio_line(valid_line)
    assert err is None
    assert data is not None
    assert data["method"] == "ping"


def test_parse_stdio_line_corrupted_by_print() -> None:
    corrupted_line = "Server started on port 8000\n"
    data, err = ex.parse_stdio_line(corrupted_line)
    assert data is None
    assert err is not None
    assert "corruption" in err.lower() or "json" in err.lower()


def test_parse_stdio_line_empty() -> None:
    data, err = ex.parse_stdio_line("   \n")
    assert data is None
    assert err is not None


@pytest.mark.asyncio
async def test_format_json_tool_execution() -> None:
    log_capture = io.StringIO()
    server = ex.create_exercise_stdio_server(log_capture_stream=log_capture)

    async with Client(server) as client:
        result = await client.call_tool("format_json", {"raw_text": '{"a": 1, "b": 2}', "indent": 4})
        assert not result.is_error
        text = result.content[0].text
        assert "    " in text
        assert '"a": 1' in text

        logs = log_capture.getvalue()
        assert len(logs) > 0
        assert "Formatting JSON" in logs
