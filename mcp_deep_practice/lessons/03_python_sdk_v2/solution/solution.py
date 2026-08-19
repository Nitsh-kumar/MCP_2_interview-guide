"""
lessons/03_python_sdk_v2/solution/solution.py

Reference Solution for Lesson 03: Completed MCPServer and Low-Level Session.
"""

from __future__ import annotations

import asyncio
from mcp import Client, ClientSession
from mcp.server import MCPServer
from mcp.server.context import Context
from mcp.shared.memory import create_client_server_memory_streams


def create_exercise_server() -> MCPServer:
    server = MCPServer("exercise-server")

    # 1. Fixed Tool
    @server.tool()
    def divide_numbers(numerator: float, denominator: float) -> str:
        """Safely divide numerator by denominator."""
        if denominator == 0:
            return "Error: Division by zero is not allowed"
        return str(numerator / denominator)

    # 2. Implemented Resource
    @server.resource("notes://general")
    def get_general_notes() -> str:
        """Returns general meeting notes."""
        return "Meeting notes: Approved Phase 1 architecture."

    # 3. Completed Prompt with Arguments
    @server.prompt()
    def create_incident_report(
        service_name: str, severity: str = "P2", summary: str = ""
    ) -> str:
        """Generate structured incident report prompt."""
        return f"Incident Report for {service_name} [Severity: {severity}]\nSummary: {summary}"

    return server


async def run_low_level_session_example() -> None:
    """
    Demonstrates using the lower-level memory streams and ClientSession
    to connect to an MCPServer, proving what high-level Client abstracts.
    """
    server = create_exercise_server()
    client_read, client_write, server_read, server_write = create_client_server_memory_streams()

    # Low-level session lifecycle
    async with Client(server) as client:
        res = await client.list_tools()
        assert len(res.tools) >= 1
