#!/usr/bin/env python
"""
lessons/04_tools/demo.py

Demonstration: Production-Grade MCP Tools with In-Memory Ticket Server.

Implements fine-grained, strongly-typed tools:
  - get_ticket: Read-only, idempotent
  - search_tickets: Read-only query
  - add_comment: Non-idempotent write
  - change_status: Idempotent state transition with domain validation
"""

from __future__ import annotations

import asyncio
import json
from dataclasses import asdict, dataclass, field
from typing import Any
from mcp import Client
from mcp.server import MCPServer


# ─── In-Memory Domain Model ──────────────────────────────────────────────────


@dataclass
class TicketComment:
    author: str
    text: str


@dataclass
class Ticket:
    id: str
    title: str
    description: str
    status: str  # "open", "in_progress", "resolved", "closed"
    assignee: str | None = None
    comments: list[TicketComment] = field(default_factory=list)


class TicketRepository:
    """In-memory ticket store for demonstration."""

    VALID_STATUSES = {"open", "in_progress", "resolved", "closed"}

    def __init__(self) -> None:
        self._tickets: dict[str, Ticket] = {
            "T-101": Ticket(
                id="T-101",
                title="Fix Redis connection timeout",
                description="Worker nodes failing to connect during traffic spikes.",
                status="open",
                assignee="alice@example.com",
            ),
            "T-102": Ticket(
                id="T-102",
                title="Update OAuth scope documentation",
                description="Clarify required scopes for enterprise SSO.",
                status="in_progress",
                assignee="bob@example.com",
            ),
        }

    def get(self, ticket_id: str) -> Ticket | None:
        return self._tickets.get(ticket_id)

    def search(self, query: str = "", status: str = "") -> list[Ticket]:
        results = list(self._tickets.values())
        if query:
            q = query.lower()
            results = [t for t in results if q in t.title.lower() or q in t.description.lower()]
        if status:
            results = [t for t in results if t.status == status]
        return results

    def add_comment(self, ticket_id: str, author: str, text: str) -> Ticket:
        ticket = self._tickets.get(ticket_id)
        if not ticket:
            raise KeyError(f"Ticket '{ticket_id}' not found.")
        if not text.strip():
            raise ValueError("Comment text cannot be empty.")
        ticket.comments.append(TicketComment(author=author, text=text))
        return ticket

    def change_status(self, ticket_id: str, new_status: str) -> Ticket:
        ticket = self._tickets.get(ticket_id)
        if not ticket:
            raise KeyError(f"Ticket '{ticket_id}' not found.")
        if new_status not in self.VALID_STATUSES:
            raise ValueError(f"Invalid status '{new_status}'. Allowed: {', '.join(sorted(self.VALID_STATUSES))}")
        ticket.status = new_status
        return ticket


# ─── Build Ticket MCP Server ─────────────────────────────────────────────────


def create_ticket_server(repo: TicketRepository | None = None) -> MCPServer:
    repository = repo or TicketRepository()
    server = MCPServer("ticket-service")

    @server.tool()
    def get_ticket(ticket_id: str) -> str:
        """Retrieve complete details for a ticket by ID (e.g. 'T-101')."""
        ticket = repository.get(ticket_id)
        if not ticket:
            return f"Error: Ticket '{ticket_id}' not found."
        return json.dumps(asdict(ticket), indent=2)

    @server.tool()
    def search_tickets(query: str = "", status: str = "") -> str:
        """Search tickets by substring query in title/description and/or status filter."""
        results = repository.search(query=query, status=status)
        return json.dumps([asdict(t) for t in results], indent=2)

    @server.tool()
    def add_ticket_comment(ticket_id: str, author: str, text: str) -> str:
        """Add a comment to an existing ticket."""
        try:
            ticket = repository.add_comment(ticket_id, author, text)
            return f"Comment added successfully to {ticket_id}. Total comments: {len(ticket.comments)}"
        except (KeyError, ValueError) as e:
            return f"Error: {e}"

    @server.tool()
    def change_ticket_status(ticket_id: str, new_status: str) -> str:
        """Change ticket status ('open', 'in_progress', 'resolved', 'closed')."""
        try:
            ticket = repository.change_status(ticket_id, new_status)
            return f"Status of {ticket_id} updated to '{ticket.status}'."
        except (KeyError, ValueError) as e:
            return f"Error: {e}"

    return server


# ─── Demonstration ────────────────────────────────────────────────────────────


async def main() -> None:
    print("=" * 64)
    print("  Lesson 04 Demo: Fine-Grained Ticket MCP Tools")
    print("=" * 64)

    server = create_ticket_server()

    async with Client(server) as client:
        # 1. Discover tools
        tools = await client.list_tools()
        print(f"\n[Tools] Discovered {len(tools.tools)} tools:")
        for t in tools.tools:
            print(f"  - {t.name}: {t.description}")

        # 2. Search tickets
        print("\n[Tool Call] search_tickets(query='Redis')...")
        res = await client.call_tool("search_tickets", {"query": "Redis"})
        print(f"  Result:\n{res.content[0].text}")

        # 3. Add comment
        print("\n[Tool Call] add_ticket_comment(ticket_id='T-101', author='carol@example.com', text='Root cause identified')...")
        res2 = await client.call_tool(
            "add_ticket_comment",
            {"ticket_id": "T-101", "author": "carol@example.com", "text": "Root cause identified"},
        )
        print(f"  Result:\n{res2.content[0].text}")

        # 4. Change status
        print("\n[Tool Call] change_ticket_status(ticket_id='T-101', new_status='resolved')...")
        res3 = await client.call_tool(
            "change_ticket_status",
            {"ticket_id": "T-101", "new_status": "resolved"},
        )
        print(f"  Result:\n{res3.content[0].text}")

        # 5. Domain Error handling (invalid status)
        print("\n[Tool Call] change_ticket_status(ticket_id='T-101', new_status='invalid_status')...")
        res4 = await client.call_tool(
            "change_ticket_status",
            {"ticket_id": "T-101", "new_status": "invalid_status"},
        )
        print(f"  Result:\n{res4.content[0].text}")

    print("\n" + "=" * 64)
    print("  Tool execution demonstration completed.")
    print("=" * 64)


if __name__ == "__main__":
    asyncio.run(main())
