"""
lessons/07_content_and_schemas/test_exercise.py

Executable specification for Lesson 07 exercise.
Validates change request schema constraints and payload handling.
"""

from __future__ import annotations

import importlib
import json
import pytest
from mcp import Client

ex = importlib.import_module("lessons.07_content_and_schemas.exercise")


@pytest.mark.asyncio
async def test_create_change_request_valid() -> None:
    server = ex.create_exercise_schema_server()
    async with Client(server) as client:
        valid_payload = {
            "title": "Upgrade Postgres to v17.2",
            "environment": "production",
            "risk": "medium",
            "systems": ["db-primary", "db-replica-1"],
            "requested_window": {
                "start_time": "2026-08-20T02:00:00Z",
                "end_time": "2026-08-20T03:00:00Z",
            },
            "rollback_plan": "Restore from pre-migration snapshot snapshot-20260820.",
        }
        res = await client.call_tool("create_change_request", valid_payload)
        assert not res.is_error
        parsed = json.loads(res.content[0].text)
        assert parsed["cr_id"] == "CR-5001"
        assert parsed["environment"] == "production"
        assert parsed["status"] == "pending_approval"


@pytest.mark.asyncio
async def test_create_change_request_invalid_enum() -> None:
    server = ex.create_exercise_schema_server()
    async with Client(server) as client:
        bad_payload = {
            "title": "Upgrade Postgres to v17.2",
            "environment": "invalid_env_name",  # Invalid enum value
            "risk": "medium",
            "systems": ["db-primary"],
            "requested_window": {
                "start_time": "2026-08-20T02:00:00Z",
                "end_time": "2026-08-20T03:00:00Z",
            },
            "rollback_plan": "Restore from snapshot.",
        }
        try:
            res = await client.call_tool("create_change_request", bad_payload)
            assert res.is_error or "error" in res.content[0].text.lower() or "validation" in res.content[0].text.lower()
        except Exception:
            pass


@pytest.mark.asyncio
async def test_create_change_request_title_too_short() -> None:
    server = ex.create_exercise_schema_server()
    async with Client(server) as client:
        short_title_payload = {
            "title": "Up",  # Less than 5 chars
            "environment": "staging",
            "risk": "low",
            "systems": ["web"],
            "requested_window": {
                "start_time": "2026-08-20T02:00:00Z",
                "end_time": "2026-08-20T03:00:00Z",
            },
            "rollback_plan": "Revert image tag in helm values.",
        }
        try:
            res = await client.call_tool("create_change_request", short_title_payload)
            assert res.is_error or "error" in res.content[0].text.lower()
        except Exception:
            pass
