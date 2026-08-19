"""
lessons/06_prompts/exercise.py

Exercise: Parameterized Prompts & Workflow Decomposition.

Your task:
  1. Register a prompt named `explain_architecture` on `create_exercise_prompts_server()`:
     - `component: str`
     - `detail_level: str = "summary"` (must be "summary" or "detailed")
     - `target_audience: str = "engineers"`
     - Returns formatted instruction string for the LLM.
  2. Complete `decompose_security_workflow()` to properly split a bloated
     "do_security_audit_and_fix" tool into the Resource + Prompt + Tool triad.
"""

from __future__ import annotations

from mcp.server import MCPServer


def create_exercise_prompts_server() -> MCPServer:
    server = MCPServer("exercise-prompts-service")

    # ─── 1. TODO: Implement explain_architecture Prompt ───────────────────────
    # Register @server.prompt() with parameters:
    #   - component: str
    #   - detail_level: str = "summary"
    #   - target_audience: str = "engineers"
    #
    # Format:
    #   f"Explain the architecture of {component} at {detail_level} detail for {target_audience}."
    #
    # Uncomment and implement below:
    # @server.prompt()
    # def explain_architecture(component: str, detail_level: str = "summary", target_audience: str = "engineers") -> str:
    #     ...

    return server


def decompose_security_workflow() -> dict[str, str]:
    """
    Decompose a monolithic 'audit_and_patch_vulnerability' tool into the
    canonical MCP triad.

    TODO: Return a dictionary with exact keys:
      - 'resource_uri': URI pattern for accessing the target source code file
      - 'prompt_name': Name of the prompt guiding the security audit
      - 'tool_name': Name of the executable tool applying the remediation patch
      - 'justification': Why this separation improves security and LLM control
    """
    # TODO: Implement the decomposition
    raise NotImplementedError("TODO: Implement decompose_security_workflow")
