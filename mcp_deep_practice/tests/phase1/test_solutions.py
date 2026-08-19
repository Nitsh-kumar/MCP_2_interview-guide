"""
tests/phase1/test_solutions.py

Curriculum Reference Implementation Tests for Phase 1 (Lessons 00–08).

Proves that all reference solutions in `lessons/*/solution/solution.py`
pass their respective executable specifications.
"""

from __future__ import annotations

import importlib
import io
import json
import pytest
from mcp import Client


# ─── Lesson 00 Solution Tests ────────────────────────────────────────────────


def test_solution_lesson_00_scenarios() -> None:
    sol00 = importlib.import_module("lessons.00_protocol_foundations.solution.solution")

    evals = sol00.evaluate_all_scenarios()
    assert len(evals) == 6
    assert evals[0].selected_strategy == sol00.ArchitectureStrategy.REST
    assert evals[1].selected_strategy == sol00.ArchitectureStrategy.MCP
    assert evals[2].selected_strategy == sol00.ArchitectureStrategy.COMBINATION
    assert evals[3].selected_strategy == sol00.ArchitectureStrategy.REST
    assert evals[4].selected_strategy == sol00.ArchitectureStrategy.MCP
    assert evals[5].selected_strategy == sol00.ArchitectureStrategy.A2A


# ─── Lesson 01 Solution Tests ────────────────────────────────────────────────


def test_solution_lesson_01_jsonrpc() -> None:
    sol01 = importlib.import_module("lessons.01_json_rpc.solution.solution")

    # Validation tests
    valid_req = {"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "test"}}
    assert sol01.validate_jsonrpc_message(valid_req) == []

    bad_req = {"id": 1, "method": "tools/call"}
    assert len(sol01.validate_jsonrpc_message(bad_req)) > 0

    # Dispatcher tests
    dispatcher = sol01.EducationalJsonRpcDispatcher()
    dispatcher.register_method("multiply", lambda a, b: a * b)

    resp = dispatcher.dispatch({"jsonrpc": "2.0", "id": 10, "method": "multiply", "params": {"a": 4, "b": 5}})
    assert resp is not None
    assert resp["result"] == 20

    # Notification
    called = []
    dispatcher.register_method("notify", lambda x: called.append(x))
    notif_resp = dispatcher.dispatch({"jsonrpc": "2.0", "method": "notify", "params": {"x": 42}})
    assert notif_resp is None
    assert called == [42]


# ─── Lesson 02 Solution Tests ────────────────────────────────────────────────


def test_solution_lesson_02_architecture() -> None:
    sol02 = importlib.import_module("lessons.02_mcp_architecture.solution.solution")

    cred_local = sol02.analyze_credential_ownership("local_stdio_sqlite")
    assert cred_local["credential_holder"] == sol02.ComponentType.MCP_SERVER

    steps = sol02.trace_tool_call_lifecycle("Test query")
    assert len(steps) == 7
    assert steps[0].sender == sol02.ComponentType.HOST
    assert steps[3].sender == sol02.ComponentType.MCP_CLIENT
    assert steps[6].sender == sol02.ComponentType.MCP_SERVER


# ─── Lesson 03 Solution Tests ────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_solution_lesson_03_sdk() -> None:
    sol03 = importlib.import_module("lessons.03_python_sdk_v2.solution.solution")

    server = sol03.create_exercise_server()
    async with Client(server) as client:
        # Tool test
        div_res = await client.call_tool("divide_numbers", {"numerator": 10.0, "denominator": 2.0})
        assert not div_res.is_error
        assert "5" in div_res.content[0].text

        zero_res = await client.call_tool("divide_numbers", {"numerator": 10.0, "denominator": 0.0})
        assert "zero" in zero_res.content[0].text.lower() or "error" in zero_res.content[0].text.lower()

        # Resource test
        res_data = await client.read_resource("notes://general")
        assert "Phase 1" in res_data.contents[0].text

        # Prompt test
        p_res = await client.get_prompt("create_incident_report", {"service_name": "API"})
        assert "API" in p_res.messages[0].content.text


# ─── Lesson 04 Solution Tests ────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_solution_lesson_04_tools() -> None:
    sol04 = importlib.import_module("lessons.04_tools.solution.solution")

    repo = sol04.ExerciseTicketRepository()
    server = sol04.create_exercise_ticket_server(repo)

    async with Client(server) as client:
        res = await client.call_tool("assign_ticket", {"ticket_id": "T-201", "assignee": "dev@co.com"})
        assert not res.is_error
        assert "T-201" in res.content[0].text
        assert repo.get("T-201").assignee == "dev@co.com"

    safety = sol04.classify_tool_safety("delete_all_tickets")
    assert safety["requires_approval"] is True


# ─── Lesson 05 Solution Tests ────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_solution_lesson_05_resources() -> None:
    sol05 = importlib.import_module("lessons.05_resources.solution.solution")

    server = sol05.create_exercise_resource_server()
    async with Client(server) as client:
        cfg = await client.read_resource("config://services/auth")
        assert "auth_db" in cfg.contents[0].text

        metric = await client.read_resource("metrics://system/cpu_usage")
        assert "42.5" in metric.contents[0].text

    assert sol05.classify_capability("search_invoices") == "TOOL"
    assert sol05.classify_capability("latest_invoice_pdf") == "RESOURCE"
    assert sol05.classify_capability("generate_incident_summary") == "PROMPT"


# ─── Lesson 06 Solution Tests ────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_solution_lesson_06_prompts() -> None:
    sol06 = importlib.import_module("lessons.06_prompts.solution.solution")

    server = sol06.create_exercise_prompts_server()
    async with Client(server) as client:
        res = await client.get_prompt("explain_architecture", {"component": "Redis"})
        assert "Redis" in res.messages[0].content.text

    decomp = sol06.decompose_security_workflow()
    assert decomp["tool_name"] == "apply_code_patch"


# ─── Lesson 07 Solution Tests ────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_solution_lesson_07_content_and_schemas() -> None:
    sol07 = importlib.import_module("lessons.07_content_and_schemas.solution.solution")

    server = sol07.create_exercise_schema_server()
    async with Client(server) as client:
        payload = {
            "title": "Database Index Optimization",
            "environment": "staging",
            "risk": "low",
            "systems": ["db-main"],
            "requested_window": {"start_time": "2026-08-20T00:00:00Z", "end_time": "2026-08-20T01:00:00Z"},
            "rollback_plan": "Drop newly created index concurrently.",
        }
        res = await client.call_tool("create_change_request", payload)
        assert not res.is_error
        parsed = json.loads(res.content[0].text)
        assert parsed["cr_id"] == "CR-5001"


# ─── Lesson 08 Solution Tests ────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_solution_lesson_08_stdio() -> None:
    sol08 = importlib.import_module("lessons.08_stdio_transport.solution.solution")

    # Line parser test
    parsed, err = sol08.parse_stdio_line('{"jsonrpc": "2.0", "id": 1, "method": "ping"}')
    assert err is None
    assert parsed["method"] == "ping"

    # Server execution test
    log_stream = io.StringIO()
    server = sol08.create_exercise_stdio_server(log_capture_stream=log_stream)

    async with Client(server) as client:
        res = await client.call_tool("format_json", {"raw_text": '{"x": 100}', "indent": 2})
        assert not res.is_error
        assert '"x": 100' in res.content[0].text
        assert "Formatting JSON" in log_stream.getvalue()
