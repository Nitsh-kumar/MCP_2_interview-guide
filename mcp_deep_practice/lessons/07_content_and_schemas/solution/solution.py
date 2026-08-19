"""
lessons/07_content_and_schemas/solution/solution.py

Reference Solution for Lesson 07: Change Request Server with Pydantic Validation.
"""

from __future__ import annotations

import json
from enum import Enum
from typing import Annotated
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

    @server.tool()
    def create_change_request(
        title: Annotated[str, Field(min_length=5, max_length=100, description="Change request title")],
        environment: Annotated[EnvironmentEnum, Field(description="Target environment")],
        risk: Annotated[RiskLevelEnum, Field(description="Risk assessment")],
        systems: Annotated[list[str], Field(min_length=1, max_length=10, description="Affected systems")],
        requested_window: Annotated[MaintenanceWindow, Field(description="Requested maintenance execution window")],
        rollback_plan: Annotated[str, Field(min_length=10, description="Detailed rollback plan")],
    ) -> str:
        """Create a production change request with strict validation constraints."""
        data = {
            "cr_id": "CR-5001",
            "title": title,
            "environment": environment.value,
            "risk": risk.value,
            "systems": systems,
            "window": {
                "start": requested_window.start_time,
                "end": requested_window.end_time,
            },
            "rollback_plan": rollback_plan,
            "status": "pending_approval",
        }
        return json.dumps(data, indent=2)

    return server
