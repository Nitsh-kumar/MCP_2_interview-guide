"""
lessons/07_content_and_schemas/exercise.py

Exercise: Designing a Misuse-Resistant Change Request Schema.

Your task:
  Implement a strongly-constrained `create_change_request` tool on `create_exercise_schema_server()`
  using Pydantic models with the following exact constraints:
    - title: str, min_length=5, max_length=100
    - environment: Enum ("development", "staging", "production")
    - risk: Enum ("low", "medium", "high", "critical")
    - systems: list[str], min_items=1, max_items=10
    - requested_window: MaintenanceWindow (with start_time: str, end_time: str)
    - rollback_plan: str, min_length=10
"""

from __future__ import annotations

import json
from enum import Enum
from typing import Any
from pydantic import BaseModel, Field
from mcp.server import MCPServer


class EnvironmentEnum(str, Enum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


class RiskLevelEnum(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class MaintenanceWindow(BaseModel):
    start_time: str = Field(description="ISO-8601 UTC start time")
    end_time: str = Field(description="ISO-8601 UTC end time")


def create_exercise_schema_server() -> MCPServer:
    server = MCPServer("exercise-change-mgmt")

    # ─── TODO: Implement create_change_request tool with Pydantic types ───────
    # Arguments:
    #   - title: str (Field min_length=5, max_length=100)
    #   - environment: EnvironmentEnum
    #   - risk: RiskLevelEnum
    #   - systems: list[str] (Field min_length=1, max_length=10)
    #   - requested_window: MaintenanceWindow
    #   - rollback_plan: str (Field min_length=10)
    #
    # Return format:
    #   json.dumps({
    #       "cr_id": "CR-5001",
    #       "title": title,
    #       "environment": environment.value,
    #       "risk": risk.value,
    #       "systems": systems,
    #       "window": {"start": requested_window.start_time, "end": requested_window.end_time},
    #       "rollback_plan": rollback_plan,
    #       "status": "pending_approval"
    #   })
    #
    # Uncomment and implement below:
    # @server.tool()
    # def create_change_request(...) -> str:
    #     ...

    return server
