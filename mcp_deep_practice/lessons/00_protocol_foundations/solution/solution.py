"""
lessons/00_protocol_foundations/solution/solution.py

Reference Solution for Lesson 00: Architecture Strategy Evaluation.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


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


SCENARIOS = {
    1: {
        "title": "Internal microservice with single backend consumer",
        "strategy": ArchitectureStrategy.REST,
        "justification": (
            "Service-to-service communication between deterministic backend systems "
            "requires maximum throughput and minimal serialization overhead. No AI "
            "reasoning or dynamic tool discovery is involved."
        ),
        "primary_benefit": "Low latency, high throughput, standard gRPC/HTTP tooling.",
        "potential_risk_or_overhead": "Using MCP would add useless protocol negotiation and semantic translation layers.",
    },
    2: {
        "title": "IDE wanting interchangeable code analysis tools",
        "strategy": ArchitectureStrategy.MCP,
        "justification": (
            "An IDE host hosting an AI assistant needs to discover and invoke heterogeneous "
            "local tools (linters, AST analyzers, debuggers) using a standard capability "
            "protocol over stdio without vendor lock-in."
        ),
        "primary_benefit": "Universal plug-and-play tool discovery across arbitrary developer environments.",
        "potential_risk_or_overhead": "Process management overhead and ensuring secure tool execution permissions.",
    },
    3: {
        "title": "AI Agent needing access to 10 distinct enterprise SaaS systems",
        "strategy": ArchitectureStrategy.COMBINATION,
        "justification": (
            "The AI agent host connects via MCP to specialized MCP servers, each of which "
            "translates standard MCP tool invocations into underlying REST API calls with "
            "proper SaaS authentication and rate limiting."
        ),
        "primary_benefit": "Decouples the agent reasoning loop from 10 proprietary REST SDKs.",
        "potential_risk_or_overhead": "Managing authentication tokens and schema evolution across multiple SaaS bridges.",
    },
    4: {
        "title": "Single-page React web application calling backend CRUD API",
        "strategy": ArchitectureStrategy.REST,
        "justification": (
            "Traditional web UI components bound to standard database entities operate "
            "most efficiently with REST/GraphQL endpoints with browser caching and cookies."
        ),
        "primary_benefit": "Predictable caching, standard HTTP status codes, browser security model.",
        "potential_risk_or_overhead": "MCP offers no advantages here and complicates frontend networking.",
    },
    5: {
        "title": "Multiple AI hosts sharing a single enterprise tool catalog",
        "strategy": ArchitectureStrategy.MCP,
        "justification": (
            "Solves the N x M integration problem: Claude Desktop, Cursor, and custom "
            "LangGraph agents can all connect to the same centralized MCP servers for SQL "
            "and AWS controls."
        ),
        "primary_benefit": "Write-once tool catalog reusable across all current and future AI client hosts.",
        "potential_risk_or_overhead": "Centralized governance and permission control across diverse hosts.",
    },
    6: {
        "title": "Two autonomous agent swarms coordinating multi-step negotiations",
        "strategy": ArchitectureStrategy.A2A,
        "justification": (
            "Two peer agents engaging in multi-round strategic negotiations require an "
            "Agent-to-Agent protocol supporting stateful dialogue, shared goal arbitration, "
            "and intent exchange. MCP is a client-server capability protocol, not an agent dialogue protocol."
        ),
        "primary_benefit": "Supports bidirectional peer negotiation, shared memory, and goal arbitration.",
        "potential_risk_or_overhead": "Higher complexity in consensus, timeout handling, and deadlock prevention.",
    },
}


def evaluate_scenario(scenario_id: int) -> ScenarioEvaluation:
    if scenario_id not in SCENARIOS:
        raise ValueError(f"Unknown scenario_id: {scenario_id}")

    data = SCENARIOS[scenario_id]
    return ScenarioEvaluation(
        scenario_id=scenario_id,
        title=data["title"],
        selected_strategy=data["strategy"],
        justification=data["justification"],
        primary_benefit=data["primary_benefit"],
        potential_risk_or_overhead=data["potential_risk_or_overhead"],
    )


def evaluate_all_scenarios() -> list[ScenarioEvaluation]:
    return [evaluate_scenario(sid) for sid in sorted(SCENARIOS.keys())]
