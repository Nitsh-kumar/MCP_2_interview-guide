"""
lessons/05_resources/exercise.py

Exercise: Implementing Resource Templates and Capability Classification.

Your task:
  1. Implement dynamic resource templates on `create_exercise_resource_server()`:
     - "config://services/{service_name}" -> returns JSON config for service
     - "metrics://system/{metric_name}" -> returns current metric reading
  2. Implement `classify_capability(scenario_key: str) -> str` returning:
     "TOOL", "RESOURCE", or "PROMPT" for each of the 14 standard scenarios.
"""

from __future__ import annotations

import json
from typing import Any
from mcp.server import MCPServer


CONFIG_STORE = {
    "auth": {"port": 8080, "db": "auth_db", "log_level": "INFO"},
    "payments": {"port": 8081, "db": "pay_db", "log_level": "DEBUG"},
}

METRICS_STORE = {
    "cpu_usage": 42.5,
    "memory_used_mb": 1024,
    "active_connections": 150,
}


def create_exercise_resource_server() -> MCPServer:
    server = MCPServer("exercise-resource-service")

    # ─── 1. Static Resource ───────────────────────────────────────────────────
    @server.resource("docs://guidelines")
    def get_guidelines() -> str:
        """Company coding guidelines."""
        return "1. All code must have type annotations.\n2. No naked exceptions."

    # ─── 2. TODO: Implement Dynamic Resource Template for Configs ────────────
    # Pattern: "config://services/{service_name}"
    # If service_name in CONFIG_STORE, return json.dumps(CONFIG_STORE[service_name])
    # Else return f"Error: Service '{service_name}' not found."
    #
    # Uncomment and implement:
    # @server.resource("config://services/{service_name}")
    # def get_service_config(service_name: str) -> str:
    #     ...

    # ─── 3. TODO: Implement Dynamic Resource Template for Metrics ────────────
    # Pattern: "metrics://system/{metric_name}"
    # If metric_name in METRICS_STORE, return str(METRICS_STORE[metric_name])
    # Else return f"Error: Metric '{metric_name}' not found."
    #
    # Uncomment and implement:
    # @server.resource("metrics://system/{metric_name}")
    # def get_system_metric(metric_name: str) -> str:
    #     ...

    return server


# ─── 4. Capability Classifier ────────────────────────────────────────────────


def classify_capability(scenario_key: str) -> str:
    """
    Classify each scenario into "TOOL", "RESOURCE", or "PROMPT".

    TODO: Implement classifications for all 14 scenarios.
    """
    # TODO: Complete the mapping for all 14 scenarios
    raise NotImplementedError("TODO: Implement classify_capability")
