#!/usr/bin/env python
"""
lessons/07_content_and_schemas/demo.py

Demonstration: Schema Constraints and Structured Content in MCP.

Compares:
  1. BAD: Unconstrained tool with dynamic dict options (hallucination hazard)
  2. GOOD: Strongly-typed Pydantic model with Enums, Field bounds, and nested objects
"""

from __future__ import annotations

import asyncio
import json
from enum import Enum
from typing import Annotated, Literal
from pydantic import BaseModel, Field
from mcp import Client
from mcp.server import MCPServer


# ─── Domain Models ───────────────────────────────────────────────────────────


class Environment(str, Enum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


class ExecutionWindow(BaseModel):
    start_time: str = Field(description="ISO-8601 start timestamp")
    end_time: str = Field(description="ISO-8601 end timestamp")


# ─── Build Servers ────────────────────────────────────────────────────────────


def create_schema_demo_server() -> MCPServer:
    server = MCPServer("schema-demo")

    # 1. BAD: Unconstrained Tool
    @server.tool()
    def deploy_bad(service: str, options: dict) -> str:
        """Deploy service with unconstrained options dict."""
        return f"Deployed {service} with {options}"

    # 2. GOOD: Strictly Constrained Tool
    @server.tool()
    def deploy_service(
        service_name: Annotated[str, Field(min_length=3, max_length=50, description="Target service")],
        environment: Annotated[Environment, Field(description="Deployment target environment")],
        replica_count: Annotated[int, Field(ge=1, le=20, description="Target pods")] = 2,
        window: Annotated[ExecutionWindow | None, Field(description="Maintenance window")] = None,
    ) -> str:
        """Safely deploy a microservice with strict domain validation."""
        win_str = f" from {window.start_time} to {window.end_time}" if window else " immediately"
        return f"SUCCESS: Scheduled deployment for '{service_name}' in '{environment.value}' with {replica_count} replica(s){win_str}."

    return server


# ─── Demonstration ────────────────────────────────────────────────────────────


async def main() -> None:
    print("=" * 64)
    print("  Lesson 07 Demo: Content Blocks & Robust JSON Schemas")
    print("=" * 64)

    server = create_schema_demo_server()

    async with Client(server) as client:
        # 1. Inspect generated JSON Schemas (using t.input_schema)
        tools_res = await client.list_tools()
        print("\n[Tool Schema Inspection]")
        for t in tools_res.tools:
            print(f"\n--- Tool: {t.name} ---")
            print(json.dumps(t.input_schema, indent=2))

        # 2. Valid invocation of constrained tool
        print("\n[Tool Call] deploy_service with valid parameters...")
        res = await client.call_tool(
            "deploy_service",
            {
                "service_name": "AuthService",
                "environment": "staging",
                "replica_count": 3,
                "window": {
                    "start_time": "2026-08-19T22:00:00Z",
                    "end_time": "2026-08-19T23:00:00Z",
                },
            },
        )
        print(f"  Result:\n  {res.content[0].text}")

        # 3. Invalid enum invocation (e.g. LLM hallucinated 'qa-env')
        print("\n[Tool Call] deploy_service with invalid environment 'qa-env'...")
        try:
            err_res = await client.call_tool(
                "deploy_service",
                {"service_name": "AuthService", "environment": "qa-env"},
            )
            print(f"  Result (isError={err_res.is_error}): {err_res.content[0].text}")
        except Exception as e:
            print(f"  Rejected at validation layer: {e}")

    print("\n" + "=" * 64)
    print("  Schema demonstration completed.")
    print("=" * 64)


if __name__ == "__main__":
    asyncio.run(main())
