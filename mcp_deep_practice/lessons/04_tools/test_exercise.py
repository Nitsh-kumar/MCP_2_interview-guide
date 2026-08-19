"""
lessons/04_tools/test_exercise.py

Executable specification for Lesson 04 exercise.
Validates the learner's assign_ticket tool and tool safety classifier.
"""

from __future__ import annotations

import importlib
import pytest
from mcp import Client

ex = importlib.import_module("lessons.04_tools.exercise")


@pytest.mark.asyncio
async def test_assign_ticket_success() -> None:
    repo = ex.ExerciseTicketRepository()
    server = ex.create_exercise_ticket_server(repo)

    async with Client(server) as client:
        result = await client.call_tool(
            "assign_ticket",
            {"ticket_id": "T-201", "assignee": "engineer@example.com"},
        )
        assert not result.is_error
        text = result.content[0].text
        assert "T-201" in text
        assert "engineer@example.com" in text

        # Verify repo state updated
        ticket = repo.get("T-201")
        assert ticket is not None
        assert ticket.assignee == "engineer@example.com"


@pytest.mark.asyncio
async def test_assign_ticket_invalid_email() -> None:
    server = ex.create_exercise_ticket_server()

    async with Client(server) as client:
        result = await client.call_tool(
            "assign_ticket",
            {"ticket_id": "T-201", "assignee": "not-an-email"},
        )
        text = result.content[0].text
        assert "error" in text.lower() or "invalid" in text.lower()


@pytest.mark.asyncio
async def test_assign_ticket_nonexistent_ticket() -> None:
    server = ex.create_exercise_ticket_server()

    async with Client(server) as client:
        result = await client.call_tool(
            "assign_ticket",
            {"ticket_id": "T-999", "assignee": "eng@example.com"},
        )
        text = result.content[0].text
        assert "not found" in text.lower() or "error" in text.lower()


def test_classify_tool_safety_read_tools() -> None:
    get_t = ex.classify_tool_safety("get_ticket")
    assert get_t["is_read_only"] is True
    assert get_t["is_idempotent"] is True
    assert get_t["requires_approval"] is False


def test_classify_tool_safety_destructive() -> None:
    del_t = ex.classify_tool_safety("delete_all_tickets")
    assert del_t["is_read_only"] is False
    assert del_t["requires_approval"] is True
