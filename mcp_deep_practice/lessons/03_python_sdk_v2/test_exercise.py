"""
lessons/03_python_sdk_v2/test_exercise.py

Executable specification for Lesson 03 exercise.
Validates the learner's completed MCPServer tools, resources, and prompts.
"""

from __future__ import annotations

import importlib
import pytest
from mcp import Client

ex = importlib.import_module("lessons.03_python_sdk_v2.exercise")


@pytest.mark.asyncio
async def test_server_instantiation() -> None:
    server = ex.create_exercise_server()
    assert server is not None
    assert server.name == "exercise-server"


@pytest.mark.asyncio
async def test_tool_divide_numbers_valid() -> None:
    server = ex.create_exercise_server()
    async with Client(server) as client:
        result = await client.call_tool("divide_numbers", {"numerator": 20.0, "denominator": 4.0})
        assert not result.is_error
        texts = [b.text for b in result.content if hasattr(b, "text")]
        assert any("5" in t for t in texts)


@pytest.mark.asyncio
async def test_tool_divide_numbers_zero() -> None:
    server = ex.create_exercise_server()
    async with Client(server) as client:
        result = await client.call_tool("divide_numbers", {"numerator": 10.0, "denominator": 0.0})
        texts = [b.text for b in result.content if hasattr(b, "text")]
        assert any("zero" in t.lower() or "error" in t.lower() for t in texts)


@pytest.mark.asyncio
async def test_resource_notes_general() -> None:
    server = ex.create_exercise_server()
    async with Client(server) as client:
        res = await client.list_resources()
        uris = [r.uri for r in res.resources]
        assert "notes://general" in uris, f"Expected 'notes://general' in resources. Found: {uris}"

        read_res = await client.read_resource("notes://general")
        assert len(read_res.contents) > 0
        assert "Phase 1" in read_res.contents[0].text


@pytest.mark.asyncio
async def test_prompt_incident_report() -> None:
    server = ex.create_exercise_server()
    async with Client(server) as client:
        prompts = await client.list_prompts()
        prompt_names = [p.name for p in prompts.prompts]
        assert "create_incident_report" in prompt_names, f"Expected 'create_incident_report' in prompts. Found: {prompt_names}"

        p_res = await client.get_prompt(
            "create_incident_report",
            {"service_name": "AuthService", "severity": "P1", "summary": "DB Connection Pool Exhausted"},
        )
        assert len(p_res.messages) > 0
        text = p_res.messages[0].content.text
        assert "AuthService" in text
        assert "P1" in text
        assert "Exhausted" in text
