"""
lessons/04_tools/exercise.py

Exercise: Adding Safe Tools and Categorizing Tool Reliability.

Your task:
  1. Implement `assign_ticket(ticket_id: str, assignee: str) -> str` on the ticket server.
     - Validates that ticket exists (otherwise returns clear error message).
     - Validates that assignee is a non-empty string containing "@".
     - Updates the ticket's assignee field.
     - Returns confirmation string: f"Ticket {ticket_id} assigned to {assignee}."
  2. Implement `classify_tool_safety(tool_name: str) -> dict[str, bool]` to classify
     operational properties (is_read_only, is_idempotent, requires_approval).
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
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

    # ─── TODO: Implement assign_ticket tool ──────────────────────────────────
    # @server.tool()
    # def assign_ticket(ticket_id: str, assignee: str) -> str:
    #     """
    #     Assign an existing ticket to an engineer by email.
    #     Validates ticket existence and valid email format.
    #     """
    #     ...

    return server


def classify_tool_safety(tool_name: str) -> dict[str, bool]:
    """
    Classify tool operational properties for retry and approval policies.

    Expected keys in returned dict:
      - 'is_read_only': bool
      - 'is_idempotent': bool
      - 'requires_approval': bool

    TODO: Implement classification for:
      - 'get_ticket'
      - 'search_tickets'
      - 'assign_ticket'
      - 'delete_all_tickets' (high risk)
    """
    # TODO: Implement classification logic
    raise NotImplementedError("TODO: Implement classify_tool_safety")
