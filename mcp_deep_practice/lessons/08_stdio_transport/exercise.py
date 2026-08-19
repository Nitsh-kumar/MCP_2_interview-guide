"""
lessons/08_stdio_transport/exercise.py

Exercise: Diagnosing stdout Pollution and Implementing Safe stdio Tools.

Your task:
  1. Complete `parse_stdio_line(raw_line: str) -> tuple[dict | None, str | None]`:
     - Parses a single newline-delimited line from an stdio stream.
     - If line is valid JSON-RPC, returns (parsed_dict, None).
     - If line is corrupted by non-JSON stdout prints (e.g. "Server started"), returns (None, error_message).
  2. Implement `create_exercise_stdio_server()` with tools that log exclusively to `sys.stderr`.
"""

from __future__ import annotations

import json
import logging
import sys
from typing import Any
from mcp.server import MCPServer


# ─── Part 1: Stream Framing Parser ───────────────────────────────────────────


def parse_stdio_line(raw_line: str) -> tuple[dict[str, Any] | None, str | None]:
    """
    Parse a single line received over an stdio pipe.

    TODO: Implement parsing logic:
      1. Strip trailing newlines and whitespace.
      2. If line is empty, return (None, "Empty line").
      3. Try json.loads(line):
         - If JSONDecodeError -> return (None, f"stdout corruption detected: {e}")
         - If valid JSON dict -> return (parsed_dict, None)
    """
    # TODO: Implement robust line parsing
    raise NotImplementedError("TODO: Implement parse_stdio_line")


# ─── Part 2: Safe stdio Server Implementation ─────────────────────────────────


def create_exercise_stdio_server(log_capture_stream: Any = None) -> MCPServer:
    """
    Create an MCPServer configured for stdio transport.

    All diagnostic messages MUST be directed to log_capture_stream or sys.stderr,
    NEVER to stdout (sys.stdout).
    """
    dest = log_capture_stream or sys.stderr
    server = MCPServer("exercise-stdio-server")

    # ─── TODO: Implement format_json_tool ─────────────────────────────────────
    # Tool: format_json(raw_text: str, indent: int = 2) -> str
    # Logs "Formatting JSON..." to dest (sys.stderr).
    # If raw_text is valid JSON, returns formatted JSON string.
    # If invalid JSON, returns f"Error: Invalid JSON ({e})".
    #
    # Uncomment and implement below:
    # @server.tool()
    # def format_json(raw_text: str, indent: int = 2) -> str:
    #     ...

    return server
