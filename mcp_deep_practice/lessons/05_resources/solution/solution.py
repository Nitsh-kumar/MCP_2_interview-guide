"""
lessons/05_resources/solution/solution.py

Reference Solution for Lesson 05: Resource Templates and Capability Classifier.
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

    @server.resource("docs://guidelines")
    def get_guidelines() -> str:
        """Company coding guidelines."""
        return "1. All code must have type annotations.\n2. No naked exceptions."

    @server.resource("config://services/{service_name}")
    def get_service_config(service_name: str) -> str:
        """Retrieve JSON configuration for a specific backend service."""
        if service_name not in CONFIG_STORE:
            return f"Error: Service '{service_name}' not found."
        return json.dumps(CONFIG_STORE[service_name])

    @server.resource("metrics://system/{metric_name}")
    def get_system_metric(metric_name: str) -> str:
        """Retrieve live numeric telemetry reading by metric name."""
        if metric_name not in METRICS_STORE:
            return f"Error: Metric '{metric_name}' not found."
        return str(METRICS_STORE[metric_name])

    return server


CLASSIFICATIONS = {
    "latest_invoice_pdf": "RESOURCE",
    "search_invoices": "TOOL",
    "retrieve_invoice_by_uri": "RESOURCE",
    "company_coding_guidelines": "RESOURCE",
    "database_schema": "RESOURCE",
    "run_database_migration": "TOOL",
    "project_readme": "RESOURCE",
    "customer_profile": "RESOURCE",
    "generate_incident_summary": "PROMPT",
    "current_system_time": "TOOL",
    "execute_sql_query": "TOOL",
    "template_for_pr_review": "PROMPT",
    "live_sensor_telemetry": "RESOURCE",
    "restart_service": "TOOL",
}


def classify_capability(scenario_key: str) -> str:
    if scenario_key not in CLASSIFICATIONS:
        raise ValueError(f"Unknown scenario_key: {scenario_key}")
    return CLASSIFICATIONS[scenario_key]
