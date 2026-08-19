#!/usr/bin/env python
"""
lessons/00_protocol_foundations/demo.py

Demonstration: Mental Model and Architectural Boundaries of MCP.

This script demonstrates the interaction boundaries between:
  1. Host Application (orchestrates user session and agent loop)
  2. Model (LLM cognitive reasoning engine)
  3. MCP Client (protocol translation boundary)
  4. MCP Server (capability provider boundary)
  5. External System (underlying data/service)

Notice: No heavy decorators or framework magic. This demonstrates the pure
architectural responsibilities.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any


# ─── 1. External System ───────────────────────────────────────────────────────


class ExternalWeatherDatabase:
    """Simulates a live third-party database or API."""

    _DATA = {
        "San Francisco": {"temp_c": 16.5, "condition": "Foggy", "humidity": 82},
        "Tokyo": {"temp_c": 24.0, "condition": "Clear", "humidity": 55},
        "London": {"temp_c": 14.0, "condition": "Rainy", "humidity": 90},
    }

    def fetch_weather(self, city: str) -> dict[str, Any]:
        if city not in self._DATA:
            raise KeyError(f"City '{city}' not found in weather records.")
        return self._DATA[city]


# ─── 2. MCP Server (Capability Provider) ──────────────────────────────────────


class MinimalMCPServer:
    """
    Exposes capabilities (Tools, Resources) to any standard MCP Client.

    Boundary Role: Translates standard protocol requests (JSON-RPC) into
    operations against external systems and returns structured results.
    """

    def __init__(self, external_db: ExternalWeatherDatabase) -> None:
        self._db = external_db

    def get_tool_definitions(self) -> list[dict[str, Any]]:
        """Advertise available tools in standard MCP schema format."""
        return [
            {
                "name": "get_current_weather",
                "description": "Retrieve real-time weather information for a given city.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "city": {
                            "type": "string",
                            "description": "The target city name (e.g. 'Tokyo').",
                        }
                    },
                    "required": ["city"],
                },
            }
        ]

    def handle_protocol_call(self, tool_name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute a tool call received over the protocol."""
        if tool_name == "get_current_weather":
            city = arguments.get("city", "")
            try:
                data = self._db.fetch_weather(city)
                return {
                    "content": [{"type": "text", "text": json.dumps(data)}],
                    "isError": False,
                }
            except KeyError as e:
                return {
                    "content": [{"type": "text", "text": f"Error: {e}"}],
                    "isError": True,
                }
        return {
            "content": [{"type": "text", "text": f"Unknown tool: {tool_name}"}],
            "isError": True,
        }


# ─── 3. MCP Client (Protocol Consumer) ────────────────────────────────────────


class MinimalMCPClient:
    """
    Resides inside the Host. Manages the connection to the Server and
    translates between the Host's internal representation and wire protocol.
    """

    def __init__(self, server: MinimalMCPServer) -> None:
        self._server = server

    def discover_tools(self) -> list[dict[str, Any]]:
        return self._server.get_tool_definitions()

    def execute_tool(self, name: str, args: dict[str, Any]) -> dict[str, Any]:
        # In a real system, this sends JSON-RPC 2.0 over stdio or Streamable HTTP.
        return self._server.handle_protocol_call(name, args)


# ─── 4. Model (LLM Simulator) ─────────────────────────────────────────────────


class SimulatedModel:
    """
    The LLM reasoning engine.

    Notice: The model has NO network access and NO direct reference to the MCP Server.
    It receives tool definitions as text/JSON schemas and outputs structured intent.
    """

    def generate_plan(self, prompt: str, tool_schemas: list[dict[str, Any]]) -> dict[str, Any]:
        # Simulated reasoning: if prompt asks for weather in Tokyo, produce tool call intent
        if "weather" in prompt.lower() and "tokyo" in prompt.lower():
            return {
                "type": "tool_call",
                "tool_name": "get_current_weather",
                "arguments": {"city": "Tokyo"},
            }
        return {
            "type": "text_response",
            "text": "I can answer general questions or check weather via tools.",
        }

    def generate_final_response(self, user_prompt: str, tool_result: dict[str, Any]) -> str:
        return f"Based on live data: The weather in Tokyo is {tool_result['content'][0]['text']}."


# ─── 5. Host Application (Orchestrator) ────────────────────────────────────────


def run_host_orchestration() -> None:
    print("=" * 64)
    print("  Lesson 00 Demo: Host -> Client -> Server Architectural Boundaries")
    print("=" * 64)

    # 1. Initialize external resources and MCP server
    db = ExternalWeatherDatabase()
    server = MinimalMCPServer(external_db=db)

    # 2. Host embeds an MCP Client and connects to the server
    client = MinimalMCPClient(server=server)
    model = SimulatedModel()

    # 3. Step 1: Tool Discovery
    available_tools = client.discover_tools()
    print(f"\n[Host] Discovered {len(available_tools)} tool(s) from MCP Server:")
    for t in available_tools:
        print(f"  - {t['name']}: {t['description']}")

    # 4. Step 2: User Prompt & Model Decision
    user_query = "What is the weather like in Tokyo right now?"
    print(f"\n[User Query] '{user_query}'")
    print("[Host] Formatting prompt and schemas for Model...")

    decision = model.generate_plan(user_query, available_tools)
    print(f"[Model Decision] Intent = {decision['type']}, Tool = {decision.get('tool_name')}")

    # 5. Step 3: MCP Client Execution
    if decision["type"] == "tool_call":
        print(f"[MCP Client] Dispatching '{decision['tool_name']}' with args: {decision['arguments']}")
        result = client.execute_tool(decision["tool_name"], decision["arguments"])
        print(f"[MCP Server Result] isError={result['isError']}, Content={result['content']}")

        # 6. Step 4: Host synthesizes final answer with Model
        final_answer = model.generate_final_response(user_query, result)
        print(f"\n[Host Final Output to User]\n  {final_answer}")

    print("\n" + "=" * 64)
    print("  Summary of Boundaries:")
    print("    - Model never touched external DB.")
    print("    - Server knew nothing about the User prompt.")
    print("    - Client bridged standard protocol schemas to host execution.")
    print("=" * 64)


if __name__ == "__main__":
    run_host_orchestration()
