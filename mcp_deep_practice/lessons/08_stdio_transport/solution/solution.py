"""
lessons/08_stdio_transport/solution/solution.py

Reference Solution for Lesson 08: stdio Line Parser and Safe Stdio Server.
"""

from __future__ import annotations

import json
import logging
import sys
from typing import Any
from mcp.server import MCPServer


def parse_stdio_line(raw_line: str) -> tuple[dict[str, Any] | None, str | None]:
    """Parse a single newline-delimited line from an stdio stream."""
    clean = raw_line.strip()
    if not clean:
        return None, "Empty line"

    try:
        data = json.loads(clean)
        if not isinstance(data, dict):
            return None, f"Expected JSON object, got {type(data).__name__}"
        return data, None
    except json.JSONDecodeError as e:
        return None, f"stdout corruption detected: {e}"


def create_exercise_stdio_server(log_capture_stream: Any = None) -> MCPServer:
    """Create an MCPServer configured for safe stdio transport."""
    dest = log_capture_stream or sys.stderr
    server = MCPServer("exercise-stdio-server")

    @server.tool()
    def format_json(raw_text: str, indent: int = 2) -> str:
        """Format raw JSON text cleanly with indentation."""
        dest.write(f"Formatting JSON payload (indent={indent})\n")
        try:
            parsed = json.loads(raw_text)
            return json.dumps(parsed, indent=indent)
        except Exception as e:
            return f"Error: Invalid JSON ({e})"

    return server
