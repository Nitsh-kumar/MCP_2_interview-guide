"""
lessons/06_prompts/solution/solution.py

Reference Solution for Lesson 06: Prompts Server and Workflow Decomposition.
"""

from __future__ import annotations

from mcp.server import MCPServer


def create_exercise_prompts_server() -> MCPServer:
    server = MCPServer("exercise-prompts-service")

    @server.prompt()
    def explain_architecture(
        component: str,
        detail_level: str = "summary",
        target_audience: str = "engineers",
    ) -> str:
        """Generate structured architecture explanation prompt."""
        if detail_level not in {"summary", "detailed"}:
            raise ValueError(f"Invalid detail_level '{detail_level}'. Allowed: 'summary', 'detailed'")
        return (
            f"Explain the architecture of {component} at {detail_level} detail for {target_audience}."
        )

    return server


def decompose_security_workflow() -> dict[str, str]:
    return {
        "resource_uri": "repo://src/{file_path}",
        "prompt_name": "security_audit_instructions",
        "tool_name": "apply_code_patch",
        "justification": (
            "Separating code reading (Resource), audit instructions (Prompt), and "
            "patch application (Tool) allows human inspection of the audit results "
            "and explicit user approval before the write tool is executed."
        ),
    }
