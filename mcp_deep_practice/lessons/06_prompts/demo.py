#!/usr/bin/env python
"""
lessons/06_prompts/demo.py

Demonstration: MCP Prompts as Protocol-Level Workflow Primitives.

Demonstrates:
  1. Registering parameterized Prompts on an MCPServer
  2. Discovering Prompts via client.list_prompts()
  3. Retrieving rendered Prompt messages via client.get_prompt()
  4. Feeding rendered Prompt messages into a host conversation context
"""

from __future__ import annotations

import asyncio
from mcp import Client
from mcp.server import MCPServer


# ─── Build Prompts MCP Server ────────────────────────────────────────────────


def create_prompts_server() -> MCPServer:
    server = MCPServer("workflow-prompts")

    @server.prompt()
    def review_code(code: str, language: str = "python", focus: str = "security") -> str:
        """
        Structured code review template with focus areas.

        Args:
            code: The source code snippet to review.
            language: Programming language (default: python).
            focus: Review focus (e.g., 'security', 'performance', 'readability').
        """
        return (
            f"You are a Principal Software Engineer specializing in {language} development.\n"
            f"Please conduct a thorough code review focusing primarily on: {focus.upper()}.\n\n"
            f"Source code to analyze:\n"
            f"```{language}\n"
            f"{code}\n"
            f"```\n\n"
            f"Provide actionable feedback with line-by-line rationale."
        )

    @server.prompt()
    def summarize_incident(service: str, severity: str = "P1", timeline: str = "") -> str:
        """
        Incident postmortem summary generator template.
        """
        return (
            f"# INCIDENT SUMMARY: {service} [{severity}]\n\n"
            f"Timeline of events:\n{timeline}\n\n"
            f"Please summarize:\n"
            f"1. Root cause\n"
            f"2. Customer impact\n"
            f"3. Remediation actions"
        )

    return server


# ─── Demonstration ────────────────────────────────────────────────────────────


async def main() -> None:
    print("=" * 64)
    print("  Lesson 06 Demo: MCP Prompts & Workflow Templates")
    print("=" * 64)

    server = create_prompts_server()

    async with Client(server) as client:
        # 1. Discover available prompts
        prompts_res = await client.list_prompts()
        print(f"\n[Prompts] Discovered {len(prompts_res.prompts)} prompt template(s):")
        for p in prompts_res.prompts:
            print(f"  - Name: {p.name}")
            print(f"    Description: {p.description}")
            if p.arguments:
                arg_names = [f"{a.name}{' (required)' if a.required else ' (optional)'}" for a in p.arguments]
                print(f"    Arguments: {', '.join(arg_names)}")

        # 2. Retrieve 'review_code' prompt
        sample_code = "def authenticate(user, password):\n    return user.password == password"
        print(f"\n[Get Prompt] Fetching 'review_code' (focus='security')...")
        review_prompt_res = await client.get_prompt(
            "review_code",
            {"code": sample_code, "language": "python", "focus": "security"},
        )

        message = review_prompt_res.messages[0]
        print(f"\n[Rendered Prompt Message] Role: {message.role}")
        print(f"Content:\n{message.content.text}")

        # 3. Retrieve 'summarize_incident' prompt
        print(f"\n[Get Prompt] Fetching 'summarize_incident'...")
        incident_prompt_res = await client.get_prompt(
            "summarize_incident",
            {
                "service": "PaymentGateway",
                "severity": "P0",
                "timeline": "14:00 Outage detected -> 14:15 Failover triggered -> 14:30 Resolved",
            },
        )
        print(f"Content:\n{incident_prompt_res.messages[0].content.text}")

    print("\n" + "=" * 64)
    print("  Prompt workflow demonstration completed.")
    print("=" * 64)


if __name__ == "__main__":
    asyncio.run(main())
