#!/usr/bin/env python
"""
lessons/08_stdio_transport/demo.py

Demonstration: stdio Transport & Safe Stderr Logging.

Demonstrates:
  1. Setting up an MCPServer for stdio execution
  2. Routing all diagnostics, logs, and trace information strictly to sys.stderr
  3. Using in-memory client connection to verify tool execution without stdout corruption
  4. Simulating how stdout framing works (newline-delimited JSON-RPC messages)
"""

from __future__ import annotations

import asyncio
import io
import json
import logging
import sys
from mcp import Client
from mcp.server import MCPServer


# ─── 1. Configure Logging to sys.stderr ──────────────────────────────────────

# CRITICAL: stdio transport requires that stdout ONLY contain JSON-RPC frames.
# All logging MUST be directed to sys.stderr.
logging.basicConfig(
    stream=sys.stderr,
    level=logging.INFO,
    format="[STDERR LOG] %(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("stdio_server_demo")


# ─── 2. Build stdio-Ready Server ─────────────────────────────────────────────


def create_stdio_demo_server() -> MCPServer:
    server = MCPServer("stdio-system-utils")

    @server.tool()
    def get_system_timestamp() -> str:
        """Return ISO-8601 formatted UTC timestamp."""
        # Safe logging to stderr
        logger.info("Executing tool: get_system_timestamp()")
        import datetime

        return datetime.datetime.now(datetime.timezone.utc).isoformat()

    @server.tool()
    def calculate_checksum(text: str, algorithm: str = "sha256") -> str:
        """Calculate cryptographic hash of text string."""
        logger.info(f"Executing calculate_checksum (algo={algorithm})")
        import hashlib

        if algorithm == "sha256":
            return hashlib.sha256(text.encode("utf-8")).hexdigest()
        elif algorithm == "md5":
            return hashlib.md5(text.encode("utf-8")).hexdigest()
        return f"Error: Unsupported algorithm '{algorithm}'"

    return server


# ─── 3. Wire-Level Framing Simulator ─────────────────────────────────────────


def simulate_stdio_framing() -> None:
    print("\n--- stdio Protocol Framing Simulation ---", file=sys.stderr)

    # 1. Request frame from Client to Server (stdin)
    req_frame = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {"name": "calculate_checksum", "arguments": {"text": "hello"}},
    }
    # In stdio transport, each message is serialized to JSON on a single line terminated by '\n'
    raw_stdin_line = json.dumps(req_frame) + "\n"
    print(f"[stdin line written by Client]: {raw_stdin_line.strip()}", file=sys.stderr)

    # 2. Server decodes stdin line
    received_req = json.loads(raw_stdin_line)
    assert received_req["method"] == "tools/call"

    # 3. Server generates response frame to stdout
    resp_frame = {
        "jsonrpc": "2.0",
        "id": 1,
        "result": {
            "content": [
                {
                    "type": "text",
                    "text": "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824",
                }
            ],
            "isError": False,
        },
    }
    raw_stdout_line = json.dumps(resp_frame) + "\n"
    print(f"[stdout line written by Server]: {raw_stdout_line.strip()}", file=sys.stderr)


# ─── 4. Client Execution ──────────────────────────────────────────────────────


async def main() -> None:
    print("=" * 64, file=sys.stderr)
    print("  Lesson 08 Demo: stdio Transport & Stderr Logging", file=sys.stderr)
    print("=" * 64, file=sys.stderr)

    simulate_stdio_framing()

    server = create_stdio_demo_server()

    # Verify execution via SDK client
    async with Client(server) as client:
        tools = await client.list_tools()
        logger.info(f"Discovered {len(tools.tools)} tools via client session.")

        res = await client.call_tool("calculate_checksum", {"text": "mcp-protocol"})
        logger.info(f"Tool Result: {res.content[0].text}")

    print("\n" + "=" * 64, file=sys.stderr)
    print("  stdio Transport Demo completed successfully.", file=sys.stderr)
    print("=" * 64, file=sys.stderr)


if __name__ == "__main__":
    asyncio.run(main())
