"""
lessons/01_json_rpc/exercise.py

Exercise: JSON-RPC 2.0 Message Validator and Educational Dispatcher.

Your task:
  1. Complete `validate_jsonrpc_message(msg: dict) -> list[str]` to strictly
     validate JSON-RPC 2.0 messages.
  2. Implement `EducationalJsonRpcDispatcher` to dispatch requests and handle notifications.

DISCLAIMER:
  EDUCATIONAL ONLY — NOT AN MCP SERVER IMPLEMENTATION.
  This is a low-level protocol exercise to understand the wire format before
  using the high-level Python SDK in Lesson 03.
"""

from __future__ import annotations

import inspect
from typing import Any, Callable


# ─── Standard JSON-RPC 2.0 Error Codes ────────────────────────────────────────

PARSE_ERROR = -32700
INVALID_REQUEST = -32600
METHOD_NOT_FOUND = -32601
INVALID_PARAMS = -32602
INTERNAL_ERROR = -32603


# ─── Part 1: Message Validator ────────────────────────────────────────────────


def validate_jsonrpc_message(msg: dict[str, Any]) -> list[str]:
    """
    Validate a JSON-RPC 2.0 message according to the official specification.

    Returns a list of human-readable error descriptions. If the list is empty,
    the message is valid.

    Rules to enforce:
      1. Must contain "jsonrpc": "2.0".
      2. If "method" is present:
         - "method" must be a string.
         - If "id" is present, it is a Request (id must be str or int).
         - If "id" is NOT present, it is a Notification.
         - Must not contain "result" or "error".
      3. If "result" or "error" is present:
         - It is a Response.
         - Must have an "id" field (str, int, or None).
         - Cannot have BOTH "result" and "error".
         - Cannot have "method".
         - If "error" is present, it must be a dict with integer "code" and string "message".
      4. If neither "method", "result", nor "error" is present:
         - Invalid message structure.
    """
    errors: list[str] = []

    # TODO: Implement complete JSON-RPC 2.0 validation rules
    if not isinstance(msg, dict):
        return ["Message must be a dictionary"]

    if msg.get("jsonrpc") != "2.0":
        errors.append('Missing or invalid "jsonrpc" version (must be "2.0")')

    has_method = "method" in msg
    has_result = "result" in msg
    has_error = "error" in msg
    has_id = "id" in msg

    # TODO: Complete the validation branches for Requests, Notifications, and Responses
    # Replace the placeholder below with strict validation logic.
    if not (has_method or has_result or has_error):
        errors.append('Message must contain "method" (request/notification) or "result"/"error" (response)')

    return errors


# ─── Part 2: Educational JSON-RPC Dispatcher ──────────────────────────────────


class EducationalJsonRpcDispatcher:
    """
    EDUCATIONAL ONLY — NOT AN MCP SERVER IMPLEMENTATION.

    A minimal JSON-RPC 2.0 dispatcher demonstrating method registration,
    parameter binding, error translation, and notification semantics.
    """

    def __init__(self) -> None:
        self._methods: dict[str, Callable[..., Any]] = {}

    def register_method(self, name: str, handler: Callable[..., Any]) -> None:
        """Register a Python callable under a method name."""
        self._methods[name] = handler

    def dispatch(self, message: dict[str, Any]) -> dict[str, Any] | None:
        """
        Process an incoming JSON-RPC message.

        Returns:
          - A response dictionary for Requests (with matching "id").
          - None for Notifications (no "id" in message).
          - An error response dictionary if validation or execution fails on a Request.
        """
        # Step 1: Validate basic JSON-RPC frame
        validation_errors = validate_jsonrpc_message(message)
        has_id = "id" in message
        req_id = message.get("id") if has_id else None

        if validation_errors:
            if has_id:
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {
                        "code": INVALID_REQUEST,
                        "message": f"Invalid Request: {'; '.join(validation_errors)}",
                    },
                }
            return None

        method_name = message.get("method")
        params = message.get("params", {})

        # TODO: Implement method lookup and execution logic:
        # 1. If method_name not in self._methods:
        #    If request (has_id), return -32601 error. If notification, return None.
        # 2. Call the method with params (handle dict or list params, or TypeError for invalid params -> -32602)
        # 3. If execution raises Exception -> return -32603 (Internal error)
        # 4. If request (has_id), return {"jsonrpc": "2.0", "id": req_id, "result": result}
        # 5. If notification (not has_id), return None

        raise NotImplementedError("TODO: Implement dispatch logic")
