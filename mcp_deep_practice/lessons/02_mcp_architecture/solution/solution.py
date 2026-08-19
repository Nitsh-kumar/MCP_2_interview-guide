"""
lessons/02_mcp_architecture/solution/solution.py

Reference Solution for Lesson 02: Architecture Boundary Tracer.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any


class ComponentType(str, Enum):
    HOST = "HOST"
    MODEL = "MODEL"
    MCP_CLIENT = "MCP_CLIENT"
    MCP_SERVER = "MCP_SERVER"
    EXTERNAL_SYSTEM = "EXTERNAL_SYSTEM"


class BoundaryType(str, Enum):
    MODEL_BOUNDARY = "MODEL_BOUNDARY"
    PROTOCOL_BOUNDARY = "PROTOCOL_BOUNDARY"
    TRUST_BOUNDARY = "TRUST_BOUNDARY"
    TRANSPORT_BOUNDARY = "TRANSPORT_BOUNDARY"


@dataclass
class ArchitectureTraceStep:
    step_number: int
    sender: ComponentType
    receiver: ComponentType
    action: str
    boundary_crossed: BoundaryType
    carries_secret: bool


def analyze_credential_ownership(server_type: str) -> dict[str, Any]:
    if server_type == "local_stdio_sqlite":
        return {
            "credential_holder": ComponentType.MCP_SERVER,
            "secret_type": "file_path_permissions",
            "transmission_over_wire": False,
        }
    elif server_type == "remote_github_http":
        return {
            "credential_holder": ComponentType.HOST,
            "secret_type": "oauth_bearer_token",
            "transmission_over_wire": True,
        }
    elif server_type == "enterprise_aws_gateway":
        return {
            "credential_holder": ComponentType.MCP_SERVER,
            "secret_type": "iam_instance_profile",
            "transmission_over_wire": False,
        }
    raise ValueError(f"Unknown server_type: {server_type}")


def trace_tool_call_lifecycle(user_query: str) -> list[ArchitectureTraceStep]:
    return [
        ArchitectureTraceStep(
            step_number=1,
            sender=ComponentType.HOST,
            receiver=ComponentType.MODEL,
            action="Send prompt and tool definitions to LLM",
            boundary_crossed=BoundaryType.MODEL_BOUNDARY,
            carries_secret=False,
        ),
        ArchitectureTraceStep(
            step_number=2,
            sender=ComponentType.MODEL,
            receiver=ComponentType.HOST,
            action="Return tool call decision (name + args)",
            boundary_crossed=BoundaryType.MODEL_BOUNDARY,
            carries_secret=False,
        ),
        ArchitectureTraceStep(
            step_number=3,
            sender=ComponentType.HOST,
            receiver=ComponentType.MCP_CLIENT,
            action="Forward tool invocation to embedded MCP Client",
            boundary_crossed=BoundaryType.TRUST_BOUNDARY,
            carries_secret=False,
        ),
        ArchitectureTraceStep(
            step_number=4,
            sender=ComponentType.MCP_CLIENT,
            receiver=ComponentType.MCP_SERVER,
            action="Send tools/call JSON-RPC message over transport",
            boundary_crossed=BoundaryType.PROTOCOL_BOUNDARY,
            carries_secret=False,
        ),
        ArchitectureTraceStep(
            step_number=5,
            sender=ComponentType.MCP_SERVER,
            receiver=ComponentType.EXTERNAL_SYSTEM,
            action="Execute query or operation against external system",
            boundary_crossed=BoundaryType.TRANSPORT_BOUNDARY,
            carries_secret=True,
        ),
        ArchitectureTraceStep(
            step_number=6,
            sender=ComponentType.EXTERNAL_SYSTEM,
            receiver=ComponentType.MCP_SERVER,
            action="Return raw query/API result",
            boundary_crossed=BoundaryType.TRANSPORT_BOUNDARY,
            carries_secret=False,
        ),
        ArchitectureTraceStep(
            step_number=7,
            sender=ComponentType.MCP_SERVER,
            receiver=ComponentType.MCP_CLIENT,
            action="Return CallToolResult JSON-RPC response",
            boundary_crossed=BoundaryType.PROTOCOL_BOUNDARY,
            carries_secret=False,
        ),
    ]
