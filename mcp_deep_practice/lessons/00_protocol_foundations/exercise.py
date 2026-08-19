"""
lessons/00_protocol_foundations/exercise.py

Exercise: Protocol vs. Alternative Architectures Decision Engine.

Your task is to analyze 6 real-world integration scenarios and determine
the most suitable communication architecture:
  - "MCP" (Model Context Protocol)
  - "REST" (Traditional REST/gRPC API)
  - "A2A" (Agent-to-Agent negotiation protocol)
  - "DIRECT_TOOL" (Hardcoded, vendor-specific function calling)
  - "COMBINATION" (e.g. MCP wrapping REST endpoints)

Complete the TODO sections below by selecting the correct strategy and
providing architectural justifications.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any


class ArchitectureStrategy(str, Enum):
    MCP = "MCP"
    REST = "REST"
    A2A = "A2A"
    DIRECT_TOOL = "DIRECT_TOOL"
    COMBINATION = "COMBINATION"


@dataclass
class ScenarioEvaluation:
    scenario_id: int
    title: str
    selected_strategy: ArchitectureStrategy
    justification: str
    primary_benefit: str
    potential_risk_or_overhead: str


# ─── Scenarios to Evaluate ───────────────────────────────────────────────────

SCENARIOS = {
    1: {
        "title": "Internal microservice with single backend consumer",
        "description": (
            "A PaymentProcessing service in a Kubernetes cluster called only by "
            "the OrderService. High throughput (10,000 req/s), strictly typed, "
            "no AI or LLM components involved."
        ),
    },
    2: {
        "title": "IDE wanting interchangeable code analysis tools",
        "description": (
            "An AI-enabled IDE (like VS Code or Cursor) wants to connect to arbitrary "
            "local static analysis engines (linters, AST parsers, test runners) installed "
            "by the developer without writing proprietary adapters for each one."
        ),
    },
    3: {
        "title": "AI Agent needing access to 10 distinct enterprise SaaS systems",
        "description": (
            "An enterprise customer support AI agent needs to read tickets from Jira, "
            "query CRM records in Salesforce, search Slack channels, and look up "
            "knowledge base articles in Zendesk across multiple developer teams."
        ),
    },
    4: {
        "title": "Single-page React web application calling backend CRUD API",
        "description": (
            "A frontend browser application displaying a user dashboard with standard "
            "pagination, sorting, session authentication, and REST endpoints."
        ),
    },
    5: {
        "title": "Multiple AI hosts sharing a single enterprise tool catalog",
        "description": (
            "An organization has developers using Claude Desktop, Cursor IDE, and an "
            "in-house LangGraph agent. All three need identical access to internal SQL "
            "databases and AWS deployment controls."
        ),
    },
    6: {
        "title": "Two autonomous agent swarms coordinating multi-step negotiations",
        "description": (
            "A SupplyChainBuyerAgent negotiates pricing, delivery dates, and volume "
            "contracts with a SupplierSellerAgent. Both agents have memory, goals, "
            "and multi-round bargaining strategies."
        ),
    },
}


def evaluate_scenario(scenario_id: int) -> ScenarioEvaluation:
    """
    Evaluate the given scenario and return an architectural recommendation.

    TODO: Implement the architectural evaluation for all 6 scenarios.
    Replace the placeholder responses with correct ArchitectureStrategy values
    and meaningful justifications.
    """
    if scenario_id not in SCENARIOS:
        raise ValueError(f"Unknown scenario_id: {scenario_id}")

    title = SCENARIOS[scenario_id]["title"]

    if scenario_id == 1:
        # Scenario 1: Internal microservice with single backend consumer
        # TODO: Choose strategy and explain why MCP is or is not suitable.
        return ScenarioEvaluation(
            scenario_id=1,
            title=title,
            selected_strategy=ArchitectureStrategy.REST,  # or gRPC
            justification="Traditional service-to-service communication requires raw performance, schema stability, and low latency without LLM tool-calling abstraction.",
            primary_benefit="High throughput, low latency, standard gRPC/REST tooling.",
            potential_risk_or_overhead="Adding MCP would introduce unnecessary JSON-RPC parsing overhead and context translation where no LLM is present.",
        )

    elif scenario_id == 2:
        # Scenario 2: IDE wanting interchangeable code analysis tools
        # TODO: Complete evaluation for Scenario 2
        raise NotImplementedError("TODO: Implement evaluation for Scenario 2")

    elif scenario_id == 3:
        # Scenario 3: AI Agent needing access to 10 distinct enterprise SaaS systems
        # TODO: Complete evaluation for Scenario 3
        raise NotImplementedError("TODO: Implement evaluation for Scenario 3")

    elif scenario_id == 4:
        # Scenario 4: Single-page React web application calling backend CRUD API
        # TODO: Complete evaluation for Scenario 4
        raise NotImplementedError("TODO: Implement evaluation for Scenario 4")

    elif scenario_id == 5:
        # Scenario 5: Multiple AI hosts sharing a single enterprise tool catalog
        # TODO: Complete evaluation for Scenario 5
        raise NotImplementedError("TODO: Implement evaluation for Scenario 5")

    elif scenario_id == 6:
        # Scenario 6: Two autonomous agent swarms coordinating negotiations
        # TODO: Complete evaluation for Scenario 6
        raise NotImplementedError("TODO: Implement evaluation for Scenario 6")

    raise NotImplementedError(f"Scenario {scenario_id} not implemented")


def evaluate_all_scenarios() -> list[ScenarioEvaluation]:
    """Evaluate all 6 scenarios."""
    return [evaluate_scenario(sid) for sid in sorted(SCENARIOS.keys())]
