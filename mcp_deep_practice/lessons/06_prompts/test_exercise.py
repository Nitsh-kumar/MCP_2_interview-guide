"""
lessons/06_prompts/test_exercise.py

Executable specification for Lesson 06 exercise.
Validates the learner's prompt server and workflow decomposition.
"""

from __future__ import annotations

import importlib
import pytest
from mcp import Client

ex = importlib.import_module("lessons.06_prompts.exercise")


@pytest.mark.asyncio
async def test_explain_architecture_discovery() -> None:
    server = ex.create_exercise_prompts_server()
    async with Client(server) as client:
        prompts = await client.list_prompts()
        names = [p.name for p in prompts.prompts]
        assert "explain_architecture" in names, f"Expected 'explain_architecture' in prompts. Got: {names}"


@pytest.mark.asyncio
async def test_explain_architecture_execution() -> None:
    server = ex.create_exercise_prompts_server()
    async with Client(server) as client:
        p_res = await client.get_prompt(
            "explain_architecture",
            {"component": "AuthGateway", "detail_level": "detailed", "target_audience": "DevOps"},
        )
        assert len(p_res.messages) > 0
        text = p_res.messages[0].content.text
        assert "AuthGateway" in text
        assert "detailed" in text
        assert "DevOps" in text


def test_decompose_security_workflow() -> None:
    decomp = ex.decompose_security_workflow()
    assert "resource_uri" in decomp
    assert "prompt_name" in decomp
    assert "tool_name" in decomp
    assert "justification" in decomp
    assert len(decomp["justification"]) > 20
    assert "{" in decomp["resource_uri"]  # Must be a URI template pattern
