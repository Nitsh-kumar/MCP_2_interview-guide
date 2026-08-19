"""
lessons/04_tools/solution/solution.py

Reference Solution for Lesson 04: Ticket Server with assign_ticket & Tool Classification.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from typing import Any
from mcp.server import MCPServer


@dataclass
class Ticket:
    id: str
    title: str
    description: str
    status: str
    assignee: str | None = None


class ExerciseTicketRepository:
    def __init__(self) -> None:
        self._tickets: dict[str, Ticket] = {
            "T-201": Ticket("T-201", "Database backup failure", "Nightly snapshot timed out", "open"),
            "T-202": Ticket("T-202", "CORS policy error on /api/v2", "Frontend blocked by origin policy", "in_progress"),
        }

    def get(self, ticket_id: str) -> Ticket | None:
        return self._tickets.get(ticket_id)

    def assign(self, ticket_id: str, assignee: str) -> Ticket:
        ticket = self._tickets.get(ticket_id)
        if not ticket:
            raise KeyError(f"Ticket '{ticket_id}' not found.")
        if not assignee or "@" not in assignee:
            raise ValueError(f"Invalid assignee email format: '{assignee}'")
        ticket.assignee = assignee
        return ticket


def create_exercise_ticket_server(repo: ExerciseTicketRepository | None = None) -> MCPServer:
    repository = repo or ExerciseTicketRepository()
    server = MCPServer("exercise-ticket-service")

    @server.tool()
    def get_ticket(ticket_id: str) -> str:
        """Retrieve ticket by ID."""
        ticket = repository.get(ticket_id)
        if not ticket:
            return f"Error: Ticket '{ticket_id}' not found."
        return json.dumps(asdict(ticket))

    @server.tool()
    def assign_ticket(ticket_id: str, assignee: str) -> str:
        """Assign an existing ticket to an engineer by email."""
        try:
            repository.assign(ticket_id, assignee)
            return f"Ticket {ticket_id} assigned to {assignee}."
        except (KeyError, ValueError) as e:
            return f"Error: {e}"

    return server


def classify_tool_safety(tool_name: str) -> dict[str, bool]:
    rules = {
        "get_ticket": {
            "is_read_only": True,
            "is_idempotent": True,
            "requires_approval": False,
        },
        "search_tickets": {
            "is_read_only": True,
            "is_idempotent": True,
            "requires_approval": False,
        },
        "assign_ticket": {
            "is_read_only": False,
            "is_idempotent": True,  # Assigning the same engineer repeatedly is idempotent
            "requires_approval": False,
        },
        "delete_all_tickets": {
            "is_read_only": False,
            "is_idempotent": True,
            "requires_approval": True,  # Destructive action
        },
    }
    if tool_name not in rules:
        raise ValueError(f"Unknown tool: {tool_name}")
    return rules[tool_name]
