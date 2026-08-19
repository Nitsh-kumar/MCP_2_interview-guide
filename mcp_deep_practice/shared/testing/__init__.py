"""
shared/testing/__init__.py

Testing utilities for MCP curriculum exercises.

Provides helpers for:
    - In-memory client+server testing (no subprocess, no network)
    - Async test patterns
    - Common assertion helpers
    - Anti-imaginary-API guards (prevents inventing unsupported SDK calls)

VERIFIED API PATHS (mcp==2.0.0):
    - Client(MCPServer) as context manager — primary in-memory test pattern
    - client.list_tools() returns ListToolsResult with .tools attribute (list of Tool)
    - client.call_tool() returns CallToolResult with .content (list of TextContent, etc.)
    - client.session returns ClientSession instance
    - Protocol version is 2026-07-28
"""

from __future__ import annotations

import pathlib
from typing import Any

from mcp import Client, ClientSession
from mcp.server import MCPServer


def get_client(server: MCPServer, **kwargs: Any) -> Client:
    """
    Create a Client connected to an MCPServer.

    The simplest in-memory test pattern in SDK v2:
        Client(MCPServer) — no subprocess, no network, no streams.

    Use as an async context manager::

        async with get_client(my_server) as client:
            result = await client.list_tools()
    """
    return Client(server, **kwargs)


def assert_tool_names(tools_result: Any, expected: list[str]) -> None:
    """
    Assert that a ListToolsResult contains exactly the expected tool names.

    tools_result is the return value of client.list_tools() — a ListToolsResult
    with a .tools attribute (list of Tool objects with .name).
    """
    actual = sorted(t.name for t in tools_result.tools)
    expected_sorted = sorted(expected)
    assert actual == expected_sorted, (
        f"Tool names mismatch.\nExpected: {expected_sorted}\nActual: {actual}"
    )


def assert_call_tool_text(call_result: Any, expected_text: str) -> None:
    """
    Assert that a CallToolResult contains the expected text.

    call_result is the return value of client.call_tool() — a CallToolResult.
    Content blocks with .text attribute are searched.
    """
    texts = [
        block.text
        for block in call_result.content
        if hasattr(block, "text") and block.text is not None
    ]
    combined = " ".join(texts)
    assert expected_text in combined, (
        f"Expected {expected_text!r} in tool result text.\nGot: {combined!r}"
    )


def assert_call_tool_not_error(call_result: Any) -> None:
    """Assert that a CallToolResult does not represent an error."""
    assert not call_result.is_error, (
        f"Tool call returned an error:\n{call_result.content}"
    )


def assert_no_imaginary_sdk_api(
    source_path: str | pathlib.Path,
    forbidden_names: list[str],
) -> None:
    """
    Assert that a source file does NOT use any forbidden (imaginary) SDK API names.

    Used in Lesson 23 to prevent accidentally inventing Tasks SDK APIs
    that do not exist in mcp==2.0.0.

    Example::

        assert_no_imaginary_sdk_api(
            "lessons/23_tasks/demo.py",
            forbidden_names=["@mcp.task", "client.create_task", "MCPServer(tasks="],
        )
    """
    path = pathlib.Path(source_path)
    if not path.exists():
        return  # File not yet created — no violation

    source = path.read_text(encoding="utf-8")
    violations = [name for name in forbidden_names if name in source]
    assert not violations, (
        f"File {path} uses imaginary SDK APIs not present in mcp==2.0.0:\n"
        + "\n".join(f"  - {v}" for v in violations)
    )
