"""
shared/fixtures/servers.py

Reusable test MCP servers for curriculum exercises.

All servers here are minimal and educational.
None connect to real external systems.
"""

from __future__ import annotations

from mcp.server import MCPServer
from mcp.server.context import Context


def make_calculator_server(name: str = "calculator") -> MCPServer:
    """
    A minimal calculator MCP server for Phase 0 smoke tests.

    Tools:
        add(a, b) -> a + b
        multiply(a, b) -> a * b

    Demonstrates:
        - MCPServer instantiation
        - @server.tool() decorator
        - Typed inputs (Pydantic validation)
        - Deterministic, side-effect-free tools
    """
    server = MCPServer(name)

    @server.tool()
    def add(a: float, b: float) -> float:
        """Add two numbers and return the result."""
        return a + b

    @server.tool()
    def multiply(a: float, b: float) -> float:
        """Multiply two numbers and return the result."""
        return a * b

    return server


def make_echo_server(name: str = "echo") -> MCPServer:
    """
    A minimal echo MCP server.

    Tools:
        echo(message) -> message

    Demonstrates the simplest possible tool for sanity testing.
    """
    server = MCPServer(name)

    @server.tool()
    def echo(message: str) -> str:
        """Return the input message unchanged."""
        return message

    return server


def make_stateful_counter_server(name: str = "counter") -> MCPServer:
    """
    A counter server that stores state in memory.

    ⚠️  EDUCATIONAL: This demonstrates why in-process state breaks
    horizontal scaling. Used as the anti-pattern example in Lesson 10.

    Tools:
        increment() -> new count
        get_count() -> current count
        reset() -> 0

    The count is stored in this process. A second replica would have
    a different count. This is the D12_session_leak_stateless bug scenario.
    """
    server = MCPServer(name)
    _count: list[int] = [0]  # mutable container for closure capture

    @server.tool()
    def increment() -> int:
        """Increment the counter and return the new value."""
        _count[0] += 1
        return _count[0]

    @server.tool()
    def get_count() -> int:
        """Return the current counter value."""
        return _count[0]

    @server.tool()
    def reset() -> int:
        """Reset the counter to zero."""
        _count[0] = 0
        return 0

    return server
