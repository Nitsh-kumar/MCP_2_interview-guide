"""
shared/protocol_capture/__init__.py

Protocol message capture utilities for wire-level inspection.

Purpose:
    MCP uses JSON-RPC 2.0 over various transports.
    Understanding the wire format is essential to understanding MCP.
    These utilities let lessons and tests inspect raw protocol messages
    without hiding everything behind the SDK abstraction.

Design:
    Lesson 01 (JSON-RPC) and Lesson 09 (Streamable HTTP) use these
    utilities to make the protocol visible.

Level of abstraction:
    LEVEL 1 — Raw protocol messages (this module)
    LEVEL 2 — Official MCP SDK
    LEVEL 3 — Agent framework integration

    This module operates at LEVEL 1.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any


@dataclass
class CapturedMessage:
    """A single JSON-RPC protocol message with direction metadata."""
    direction: str  # "client->server" or "server->client"
    raw: dict[str, Any]

    @property
    def is_request(self) -> bool:
        return "id" in self.raw and "method" in self.raw

    @property
    def is_response(self) -> bool:
        return "id" in self.raw and ("result" in self.raw or "error" in self.raw)

    @property
    def is_notification(self) -> bool:
        return "id" not in self.raw and "method" in self.raw

    @property
    def method(self) -> str | None:
        return self.raw.get("method")

    @property
    def id(self) -> Any:
        return self.raw.get("id")

    def pretty(self) -> str:
        return f"[{self.direction}]\n{json.dumps(self.raw, indent=2)}"


@dataclass
class ProtocolCapture:
    """
    Captures a sequence of protocol messages for inspection.

    Used in wire-level lessons to make the protocol visible.
    """
    messages: list[CapturedMessage] = field(default_factory=list)

    def record(self, direction: str, raw: dict[str, Any]) -> None:
        """Record a single protocol message."""
        self.messages.append(CapturedMessage(direction=direction, raw=raw))

    def requests(self) -> list[CapturedMessage]:
        return [m for m in self.messages if m.is_request]

    def responses(self) -> list[CapturedMessage]:
        return [m for m in self.messages if m.is_response]

    def notifications(self) -> list[CapturedMessage]:
        return [m for m in self.messages if m.is_notification]

    def method_calls(self, method: str) -> list[CapturedMessage]:
        return [m for m in self.messages if m.method == method]

    def print_all(self) -> None:
        for msg in self.messages:
            print(msg.pretty())
            print()

    def clear(self) -> None:
        self.messages.clear()


def make_jsonrpc_request(
    method: str,
    params: dict[str, Any] | None = None,
    request_id: str | int = 1,
) -> dict[str, Any]:
    """Build a minimal valid JSON-RPC 2.0 request."""
    msg: dict[str, Any] = {
        "jsonrpc": "2.0",
        "id": request_id,
        "method": method,
    }
    if params is not None:
        msg["params"] = params
    return msg


def make_jsonrpc_notification(
    method: str,
    params: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build a minimal valid JSON-RPC 2.0 notification (no id)."""
    msg: dict[str, Any] = {"jsonrpc": "2.0", "method": method}
    if params is not None:
        msg["params"] = params
    return msg


def make_modern_tools_call(
    tool_name: str,
    arguments: dict[str, Any],
    request_id: str | int = 1,
    protocol_version: str = "2026-07-28",
) -> dict[str, Any]:
    """
    Build a modern MCP 2026-07-28 tools/call request.

    Includes the _meta block with protocol version and client info
    as required by the modern specification.

    The corresponding HTTP request must also include:
        MCP-Protocol-Version: 2026-07-28
        Mcp-Method: tools/call
        Mcp-Name: <tool_name>
    """
    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": arguments,
            "_meta": {
                "io.modelcontextprotocol/protocolVersion": protocol_version,
                "io.modelcontextprotocol/clientInfo": {
                    "name": "mcp-deep-practice-client",
                    "version": "1.0.0",
                },
                "io.modelcontextprotocol/clientCapabilities": {
                    "tools": {},
                },
            },
        },
    }


def validate_jsonrpc_message(msg: dict[str, Any]) -> list[str]:
    """
    Validate a JSON-RPC 2.0 message structure.

    Returns a list of error strings (empty if valid).
    Used in Lesson 01 exercises.
    """
    errors: list[str] = []

    if msg.get("jsonrpc") != "2.0":
        errors.append('Missing or incorrect "jsonrpc": "2.0" field')

    has_id = "id" in msg
    has_method = "method" in msg
    has_result = "result" in msg
    has_error = "error" in msg

    if has_method:
        # Request or notification
        if not isinstance(msg["method"], str):
            errors.append('"method" must be a string')
        if has_id and not isinstance(msg["id"], (str, int)):
            errors.append('"id" must be a string or integer')
    elif has_result or has_error:
        # Response
        if not has_id:
            errors.append('Response must have an "id" field')
        if has_result and has_error:
            errors.append('Response cannot have both "result" and "error"')
        if has_error:
            err = msg["error"]
            if not isinstance(err, dict):
                errors.append('"error" must be an object')
            elif "code" not in err or "message" not in err:
                errors.append('"error" must have "code" and "message"')
    else:
        errors.append('Message must have "method" (request/notification) or "result"/"error" (response)')

    return errors
