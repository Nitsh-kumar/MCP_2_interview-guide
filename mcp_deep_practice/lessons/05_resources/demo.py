#!/usr/bin/env python
"""
lessons/05_resources/demo.py

Demonstration: Static Resources and Dynamic Resource Templates.

Demonstrates:
  1. Static Resource registration: "docs://architecture"
  2. Dynamic Resource Template registration: "ticket://{ticket_id}" and "ticket://{ticket_id}/comments"
  3. Client discovery via list_resources() and list_resource_templates()
  4. Reading static and templated resources via read_resource()
"""

from __future__ import annotations

import asyncio
import json
from mcp import Client
from mcp.server import MCPServer


# ─── In-Memory Data Store ────────────────────────────────────────────────────

TICKETS_DB = {
    "101": {
        "id": "101",
        "title": "Migrate auth service to OAuth 2.0 PKCE",
        "status": "in_progress",
        "comments": ["Approved by Security Team", "Initial PR opened"],
    },
    "102": {
        "id": "102",
        "title": "Fix memory leak in websocket gateway",
        "status": "resolved",
        "comments": ["Patched in v2.4.1 release"],
    },
}

STATIC_DOCS = {
    "docs://architecture": "# System Architecture\n\nAll services communicate over mutual TLS and JSON-RPC 2.0."
}


# ─── Build Resource MCP Server ───────────────────────────────────────────────


def create_resource_server() -> MCPServer:
    server = MCPServer("resource-service")

    # 1. Static Resource
    @server.resource("docs://architecture")
    def get_architecture_doc() -> str:
        """Static architecture documentation."""
        return STATIC_DOCS["docs://architecture"]

    # 2. Dynamic Resource Template: Single Ticket
    @server.resource("ticket://{ticket_id}")
    def get_ticket(ticket_id: str) -> str:
        """Retrieve ticket details by ID."""
        if ticket_id not in TICKETS_DB:
            return f"Error: Ticket '{ticket_id}' not found."
        return json.dumps(TICKETS_DB[ticket_id], indent=2)

    # 3. Dynamic Resource Template: Ticket Comments
    @server.resource("ticket://{ticket_id}/comments")
    def get_ticket_comments(ticket_id: str) -> str:
        """Retrieve comments for a specific ticket."""
        if ticket_id not in TICKETS_DB:
            return f"Error: Ticket '{ticket_id}' not found."
        return json.dumps(TICKETS_DB[ticket_id]["comments"], indent=2)

    return server


# ─── Demonstration ────────────────────────────────────────────────────────────


async def main() -> None:
    print("=" * 64)
    print("  Lesson 05 Demo: MCP Resources & URI Templates")
    print("=" * 64)

    server = create_resource_server()

    async with Client(server) as client:
        # 1. Discover Static Resources
        res_list = await client.list_resources()
        print(f"\n[Static Resources] Discovered {len(res_list.resources)} resource(s):")
        for r in res_list.resources:
            print(f"  - URI: {r.uri} | Name: {r.name}")

        # 2. Discover Resource Templates
        tmpl_list = await client.list_resource_templates()
        print(f"\n[Resource Templates] Discovered {len(tmpl_list.resource_templates)} template(s):")
        for tmpl in tmpl_list.resource_templates:
            print(f"  - Pattern: {tmpl.uri_template} | Name: {tmpl.name}")

        # 3. Read Static Resource
        print("\n[Read Resource] Reading 'docs://architecture'...")
        doc_res = await client.read_resource("docs://architecture")
        print(f"  Content:\n{doc_res.contents[0].text}")

        # 4. Read Dynamic Resource via Template
        print("\n[Read Resource] Reading 'ticket://101'...")
        t101_res = await client.read_resource("ticket://101")
        print(f"  Content:\n{t101_res.contents[0].text}")

        # 5. Read Nested Dynamic Resource
        print("\n[Read Resource] Reading 'ticket://101/comments'...")
        comments_res = await client.read_resource("ticket://101/comments")
        print(f"  Content:\n{comments_res.contents[0].text}")

        # 6. Read Non-Existent Resource
        print("\n[Read Resource] Reading 'ticket://999' (non-existent)...")
        err_res = await client.read_resource("ticket://999")
        print(f"  Content:\n{err_res.contents[0].text}")

    print("\n" + "=" * 64)
    print("  Resource demonstration completed.")
    print("=" * 64)


if __name__ == "__main__":
    asyncio.run(main())
