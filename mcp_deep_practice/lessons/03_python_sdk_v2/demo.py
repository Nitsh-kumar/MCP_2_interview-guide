#!/usr/bin/env python
"""
lessons/03_python_sdk_v2/demo.py

Demonstration: Official Python SDK v2 (MCPServer + Client in memory).

Proves:
  1. MCPServer instantiation with 1 tool, 1 resource, 1 prompt
  2. Client(server) in-memory connection
  3. Protocol version resolves to 2026-07-28
  4. client.session is a ClientSession instance
  5. Tools discovery (result.tools) and invocation (result.content)
  6. Resource discovery (result.resources) and reading (result.contents)
  7. Prompt discovery (result.prompts) and retrieval (result.messages)
"""

from __future__ import annotations

import asyncio
from mcp import Client, ClientSession
from mcp.server import MCPServer
from mcp.server.context import Context


# ─── 1. Build Minimal MCPServer ──────────────────────────────────────────────


def build_demo_server() -> MCPServer:
    server = MCPServer("demo-server")

    # 1. Register a tool
    @server.tool()
    def multiply_numbers(a: float, b: float) -> float:
        """Multiply two numbers and return the result."""
        return a * b

    # 2. Register a resource
    @server.resource("system://info")
    def get_system_info() -> str:
        """Return system status information."""
        return "System status: ALL SERVICES OPERATIONAL"

    # 3. Register a prompt
    @server.prompt()
    def summarize_text(topic: str, length: str = "short") -> str:
        """Generate a prompt asking for a summary of a topic."""
        return f"Please provide a {length} summary of the topic: {topic}."

    return server


# ─── 2. Client Connection and Protocol Probes ────────────────────────────────


async def run_demo() -> None:
    print("=" * 64)
    print("  Lesson 03 Demo: Python SDK v2 (MCPServer & Client)")
    print("=" * 64)

    server = build_demo_server()
    assert server.name == "demo-server"
    print(f"\n[Server] Created MCPServer '{server.name}'")

    async with Client(server) as client:
        # 1. Verify Protocol Version
        print(f"\n[Protocol] Negotiated version: {client.protocol_version}")
        assert client.protocol_version == "2026-07-28", f"Expected 2026-07-28, got {client.protocol_version}"

        # 2. Verify Session type
        assert isinstance(client.session, ClientSession), "client.session must be ClientSession"
        print("[Session] client.session is verified as ClientSession instance.")

        # 3. Tool Discovery & Execution
        tools_result = await client.list_tools()
        print(f"\n[Tools] Discovered {len(tools_result.tools)} tool(s):")
        for t in tools_result.tools:
            print(f"  - {t.name}: {t.description}")
        assert any(t.name == "multiply_numbers" for t in tools_result.tools)

        call_result = await client.call_tool("multiply_numbers", {"a": 6.0, "b": 7.0})
        assert not call_result.is_error
        result_text = call_result.content[0].text if hasattr(call_result.content[0], "text") else str(call_result.content[0])
        print(f"[Tool Call] multiply_numbers(6, 7) -> {result_text}")
        assert "42" in result_text

        # 4. Resource Discovery & Reading
        resources_result = await client.list_resources()
        print(f"\n[Resources] Discovered {len(resources_result.resources)} resource(s):")
        for r in resources_result.resources:
            print(f"  - {r.uri}: {r.name}")

        read_result = await client.read_resource("system://info")
        print(f"[Resource Read] 'system://info' -> {read_result.contents[0].text}")
        assert "OPERATIONAL" in read_result.contents[0].text

        # 5. Prompt Discovery & Retrieval
        prompts_result = await client.list_prompts()
        print(f"\n[Prompts] Discovered {len(prompts_result.prompts)} prompt(s):")
        for p in prompts_result.prompts:
            print(f"  - {p.name}: {p.description}")

        get_prompt_result = await client.get_prompt("summarize_text", {"topic": "Quantum Computing", "length": "concise"})
        print(f"[Prompt Get] 'summarize_text' -> {get_prompt_result.messages[0].content.text}")
        assert "Quantum Computing" in get_prompt_result.messages[0].content.text

    print("\n" + "=" * 64)
    print("  All SDK v2 assertions passed successfully!")
    print("=" * 64)


if __name__ == "__main__":
    asyncio.run(run_demo())
