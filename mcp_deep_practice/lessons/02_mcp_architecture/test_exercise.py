"""
lessons/02_mcp_architecture/test_exercise.py

Executable specification for Lesson 02 exercise.
Validates architectural boundary analysis and tool call tracing.
"""

from __future__ import annotations

import importlib
import pytest

ex = importlib.import_module("lessons.02_mcp_architecture.exercise")


def test_credential_ownership_local_sqlite() -> None:
    res = ex.analyze_credential_ownership("local_stdio_sqlite")
    assert res["credential_holder"] == ex.ComponentType.MCP_SERVER
    assert res["transmission_over_wire"] is False


def test_credential_ownership_remote_github() -> None:
    res = ex.analyze_credential_ownership("remote_github_http")
    assert res["credential_holder"] in (ex.ComponentType.HOST, ex.ComponentType.MCP_CLIENT)
    assert res["transmission_over_wire"] is True


def test_credential_ownership_aws_gateway() -> None:
    res = ex.analyze_credential_ownership("enterprise_aws_gateway")
    assert res["credential_holder"] == ex.ComponentType.MCP_SERVER
    assert res["transmission_over_wire"] is False


def test_trace_tool_call_lifecycle_completeness() -> None:
    steps = ex.trace_tool_call_lifecycle("Find PRs assigned to Alice")
    assert len(steps) == 7

    # Validate step order
    for idx, step in enumerate(steps, start=1):
        assert step.step_number == idx
        assert isinstance(step.sender, ex.ComponentType)
        assert isinstance(step.receiver, ex.ComponentType)
        assert isinstance(step.boundary_crossed, ex.BoundaryType)

    # Step 1: HOST -> MODEL
    assert steps[0].sender == ex.ComponentType.HOST
    assert steps[0].receiver == ex.ComponentType.MODEL

    # Step 4: MCP_CLIENT -> MCP_SERVER
    assert steps[3].sender == ex.ComponentType.MCP_CLIENT
    assert steps[3].receiver == ex.ComponentType.MCP_SERVER
    assert steps[3].boundary_crossed == ex.BoundaryType.PROTOCOL_BOUNDARY

    # Step 7: MCP_SERVER -> MCP_CLIENT
    assert steps[6].sender == ex.ComponentType.MCP_SERVER
    assert steps[6].receiver == ex.ComponentType.MCP_CLIENT
    assert steps[6].boundary_crossed == ex.BoundaryType.PROTOCOL_BOUNDARY
