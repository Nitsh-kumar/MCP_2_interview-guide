"""
lessons/03_python_sdk_v2/exercise.py

Exercise: Completing an MCPServer with Tools, Resources, and Prompts.

Your task:
  1. Fix the broken `divide_numbers` tool (handle division by zero cleanly with error text).
  2. Implement the missing `@server.resource("notes://general")` resource.
  3. Complete the `@server.prompt()` decorator for `create_incident_report` with typed arguments:
     `service_name: str`, `severity: str = "P2"`, `summary: str = ""`.
"""

from __future__ import annotations

from mcp.server import MCPServer
from mcp.server.context import Context


def create_exercise_server() -> MCPServer:
    server = MCPServer("exercise-server")

    # ─── 1. Fix Broken Tool ───────────────────────────────────────────────────
    @server.tool()
    def divide_numbers(numerator: float, denominator: float) -> str:
        """
        Safely divide numerator by denominator.

        TODO: If denominator == 0, return a clear error string instead of
        raising ZeroDivisionError. Otherwise return the division result as a string.
        """
        # TODO: Fix the division logic to handle zero division
        if denominator == 0:
            return "Error: Division by zero is not allowed"
        return str(numerator / denominator)

    # ─── 2. Implement Missing Resource ────────────────────────────────────────
    # TODO: Register a resource at URI "notes://general" that returns
    # "Meeting notes: Approved Phase 1 architecture."
    # Use @server.resource("notes://general")
    #
    # Uncomment and complete below:
    # @server.resource("notes://general")
    # def get_general_notes() -> str:
    #     ...

    # ─── 3. Complete Prompt with Arguments ────────────────────────────────────
    # TODO: Register a prompt named "create_incident_report" with parameters:
    #   - service_name: str
    #   - severity: str (default: "P2")
    #   - summary: str (default: "")
    # Should return:
    #   f"Incident Report for {service_name} [Severity: {severity}]\nSummary: {summary}"
    #
    # Uncomment and complete below:
    # @server.prompt()
    # def create_incident_report(...) -> str:
    #     ...

    return server
