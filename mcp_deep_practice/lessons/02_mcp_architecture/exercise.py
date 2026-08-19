"""
lessons/02_mcp_architecture/exercise.py

Exercise: Architectural Boundary Tracer & Component Ownership.

Your task:
  1. Map components in a multi-server MCP architecture to their proper boundaries:
     - Model Boundary (what the LLM sees / decides)
     - Protocol Boundary (JSON-RPC 2.0 messages)
     - Trust Boundary (authorization, permission prompts)
     - Credential Ownership (who stores secrets)
  2. Implement `trace_message_lifecycle` to trace and validate the sequence of steps
     involved in an MCP tool invocation.
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
    """
    Analyze where credentials should reside for a given server type.

    TODO: Complete the credential ownership mapping for:
      - 'local_stdio_sqlite': local SQLite server
      - 'remote_github_http': remote GitHub server
      - 'enterprise_aws_gateway': corporate AWS IAM server
    """
    # TODO: Implement credential ownership mappings
    if server_type == "local_stdio_sqlite":
        return {
            "credential_holder": ComponentType.MCP_SERVER,
            "secret_type": "file_path_permissions",
            "transmission_over_wire": False,
        }
    elif server_type == "remote_github_http":
        # TODO: Complete mapping for remote_github_http
        raise NotImplementedError("TODO: Implement mapping for remote_github_http")
    elif server_type == "enterprise_aws_gateway":
        # TODO: Complete mapping for enterprise_aws_gateway
        raise NotImplementedError("TODO: Implement mapping for enterprise_aws_gateway")

    raise ValueError(f"Unknown server_type: {server_type}")


def trace_tool_call_lifecycle(user_query: str) -> list[ArchitectureTraceStep]:
    """
    Build the exact sequential trace of an MCP tool invocation.

    TODO: Complete the trace steps (steps 1 through 7):
      Step 1: HOST -> MODEL (Prompt + tool definitions)
      Step 2: MODEL -> HOST (Tool call decision with arguments)
      Step 3: HOST -> MCP_CLIENT (Initiate tool execution)
      Step 4: MCP_CLIENT -> MCP_SERVER (tools/call JSON-RPC message)
      Step 5: MCP_SERVER -> EXTERNAL_SYSTEM (execute query / API)
      Step 6: EXTERNAL_SYSTEM -> MCP_SERVER (return raw data)
      Step 7: MCP_SERVER -> MCP_CLIENT (CallToolResult JSON-RPC)
    """
    steps: list[ArchitectureTraceStep] = []

    # TODO: Fill in all 7 steps with accurate sender, receiver, boundary, and secret info.
    steps.append(
        ArchitectureTraceStep(
            step_number=1,
            sender=ComponentType.HOST,
            receiver=ComponentType.MODEL,
            action="Send prompt and tool definitions to LLM",
            boundary_crossed=BoundaryType.MODEL_BOUNDARY,
            carries_secret=False,
        )
    )

    # TODO: Complete steps 2-7
    raise NotImplementedError("TODO: Implement all 7 lifecycle steps")
