"""
shared/fake_llm/__init__.py

Deterministic fake LLM for MCP curriculum testing.

Purpose:
    Replaces a real language model so that ALL core curriculum exercises
    work without any paid API key (OpenAI, Anthropic, Google, Azure, etc.).

Design principles:
    - Fully deterministic given the same inputs.
    - Scriptable: callers supply a list of responses in advance.
    - Inspectable: records all calls made to it.
    - Teaches the boundary between the model and MCP clearly.

The model itself does NOT call MCP servers. The HOST/AGENT calls MCP servers
on the model's behalf, based on the model's tool-call decisions.
This fake LLM emulates that boundary without LLM nondeterminism.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ToolCallDecision:
    """Represents the fake LLM deciding to call a tool."""
    tool_name: str
    arguments: dict[str, Any]
    reasoning: str = ""


@dataclass
class TextDecision:
    """Represents the fake LLM deciding to respond with text."""
    text: str


# The model produces either a tool call or a text response.
ModelDecision = ToolCallDecision | TextDecision


@dataclass
class FakeLLM:
    """
    A fully deterministic fake LLM for curriculum exercises.

    Usage::

        llm = FakeLLM(responses=[
            ToolCallDecision("get_ticket", {"ticket_id": "TKT-42"}),
            TextDecision("Here is the ticket information: ..."),
        ])

        decision = llm.decide(messages, available_tools)
        assert isinstance(decision, ToolCallDecision)
        assert decision.tool_name == "get_ticket"

        # After all scripted responses are consumed, raises StopIteration.
        llm.assert_all_responses_consumed()
    """

    responses: list[ModelDecision] = field(default_factory=list)
    _call_log: list[dict[str, Any]] = field(default_factory=list, init=False)
    _index: int = field(default=0, init=False)

    def decide(
        self,
        messages: list[dict[str, Any]],
        available_tools: list[dict[str, Any]] | None = None,
    ) -> ModelDecision:
        """
        Return the next scripted decision.

        Records the call for later inspection.
        Raises StopIteration if all scripted responses have been consumed.
        """
        if self._index >= len(self.responses):
            raise StopIteration(
                f"FakeLLM has no more scripted responses. "
                f"Consumed {self._index} of {len(self.responses)}."
            )

        decision = self.responses[self._index]
        self._call_log.append({
            "index": self._index,
            "messages": messages,
            "available_tools": available_tools,
            "decision": decision,
        })
        self._index += 1
        return decision

    @property
    def call_count(self) -> int:
        """How many times .decide() has been called."""
        return len(self._call_log)

    @property
    def calls(self) -> list[dict[str, Any]]:
        """Full call log for inspection in tests."""
        return list(self._call_log)

    def assert_all_responses_consumed(self) -> None:
        """
        Assert that every scripted response was used.
        Raises AssertionError if unconsumed responses remain.
        """
        remaining = len(self.responses) - self._index
        if remaining > 0:
            raise AssertionError(
                f"FakeLLM has {remaining} unconsumed scripted responses. "
                f"This usually means the agent loop exited early."
            )

    def reset(self) -> None:
        """Reset state for reuse within the same test session."""
        self._call_log.clear()
        self._index = 0


def make_scripted_agent_loop(
    llm: FakeLLM,
    tool_executor: Any,  # callable(tool_name, arguments) -> Any
    initial_messages: list[dict[str, Any]],
    available_tools: list[dict[str, Any]] | None = None,
    max_iterations: int = 20,
) -> list[dict[str, Any]]:
    """
    A minimal deterministic agent loop for curriculum use.

    This is NOT a production agent. It demonstrates the conceptual boundary
    between model decisions and MCP tool execution.

    The model does NOT call MCP servers directly.
    The agent loop (host) calls MCP servers on behalf of the model.

    Flow:
        1. Model sees messages → decides tool call or text response.
        2. If tool call: agent loop calls MCP server → appends result to messages.
        3. Repeat until model returns TextDecision or max_iterations reached.

    Returns the complete message history.
    """
    messages = list(initial_messages)

    for _ in range(max_iterations):
        decision = llm.decide(messages, available_tools)

        if isinstance(decision, TextDecision):
            messages.append({"role": "assistant", "content": decision.text})
            break

        elif isinstance(decision, ToolCallDecision):
            # Agent loop calls MCP server on model's behalf.
            tool_result = tool_executor(decision.tool_name, decision.arguments)
            messages.append({
                "role": "tool",
                "tool_name": decision.tool_name,
                "content": str(tool_result),
            })

    return messages
