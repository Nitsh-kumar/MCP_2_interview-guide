"""
lessons/05_resources/test_exercise.py

Executable specification for Lesson 05 exercise.
Validates the learner's resource server templates and capability classifications.
"""

from __future__ import annotations

import importlib
import pytest
from mcp import Client

ex = importlib.import_module("lessons.05_resources.exercise")


@pytest.mark.asyncio
async def test_read_static_guidelines() -> None:
    server = ex.create_exercise_resource_server()
    async with Client(server) as client:
        res = await client.read_resource("docs://guidelines")
        assert len(res.contents) > 0
        assert "type annotations" in res.contents[0].text


@pytest.mark.asyncio
async def test_read_dynamic_config_template_success() -> None:
    server = ex.create_exercise_resource_server()
    async with Client(server) as client:
        res = await client.read_resource("config://services/auth")
        assert len(res.contents) > 0
        text = res.contents[0].text
        assert "auth_db" in text
        assert "8080" in text


@pytest.mark.asyncio
async def test_read_dynamic_config_template_missing() -> None:
    server = ex.create_exercise_resource_server()
    async with Client(server) as client:
        res = await client.read_resource("config://services/unknown_svc")
        assert len(res.contents) > 0
        text = res.contents[0].text
        assert "not found" in text.lower() or "error" in text.lower()


@pytest.mark.asyncio
async def test_read_dynamic_metrics_template() -> None:
    server = ex.create_exercise_resource_server()
    async with Client(server) as client:
        res = await client.read_resource("metrics://system/cpu_usage")
        assert len(res.contents) > 0
        assert "42.5" in res.contents[0].text


def test_classify_capability_all_14() -> None:
    expected = {
        "latest_invoice_pdf": "RESOURCE",
        "search_invoices": "TOOL",
        "retrieve_invoice_by_uri": "RESOURCE",
        "company_coding_guidelines": "RESOURCE",
        "database_schema": "RESOURCE",
        "run_database_migration": "TOOL",
        "project_readme": "RESOURCE",
        "customer_profile": "RESOURCE",
        "generate_incident_summary": "PROMPT",
        "current_system_time": "TOOL",
        "execute_sql_query": "TOOL",
        "template_for_pr_review": "PROMPT",
        "live_sensor_telemetry": "RESOURCE",
        "restart_service": "TOOL",
    }
    for key, expected_type in expected.items():
        actual = ex.classify_capability(key)
        assert actual == expected_type, f"Scenario '{key}' expected {expected_type}, got {actual}"
