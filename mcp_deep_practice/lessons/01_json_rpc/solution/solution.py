"""
lessons/01_json_rpc/solution/solution.py

Reference Solution for Lesson 01: JSON-RPC 2.0 Message Validator & Dispatcher.
"""

from __future__ import annotations

import inspect
from typing import Any, Callable


PARSE_ERROR = -32700
INVALID_REQUEST = -32600
METHOD_NOT_FOUND = -32601
INVALID_PARAMS = -32602
INTERNAL_ERROR = -32603


def validate_jsonrpc_message(msg: dict[str, Any]) -> list[str]:
    """Validate a JSON-RPC 2.0 message according to spec."""
    errors: list[str] = []

    if not isinstance(msg, dict):
        return ["Message must be a dictionary"]

    if msg.get("jsonrpc") != "2.0":
        errors.append('Missing or invalid "jsonrpc" version (must be "2.0")')

    has_method = "method" in msg
    has_result = "result" in msg
    has_error = "error" in msg
    has_id = "id" in msg

    if has_method:
        if not isinstance(msg["method"], str):
            errors.append('"method" must be a string')
        if has_result or has_error:
            errors.append('Request/Notification cannot have "result" or "error"')
        if has_id:
            # Request
            if msg["id"] is not None and not isinstance(msg["id"], (str, int)):
                errors.append('"id" must be a string, integer, or null')
        if "params" in msg and not isinstance(msg["params"], (dict, list)):
            errors.append('"params" must be an object or array')

    elif has_result or has_error:
        # Response
        if not has_id:
            errors.append('Response must have an "id" field')
        elif msg["id"] is not None and not isinstance(msg["id"], (str, int)):
            errors.append('Response "id" must be a string, integer, or null')

        if has_result and has_error:
            errors.append('Response cannot have both "result" and "error"')

        if has_error:
            err = msg["error"]
            if not isinstance(err, dict):
                errors.append('"error" must be an object')
            else:
                if "code" not in err or not isinstance(err["code"], int):
                    errors.append('"error" must have an integer "code"')
                if "message" not in err or not isinstance(err["message"], str):
                    errors.append('"error" must have a string "message"')
    else:
        errors.append('Message must contain "method" (request/notification) or "result"/"error" (response)')

    return errors


class EducationalJsonRpcDispatcher:
    """
    EDUCATIONAL ONLY — NOT AN MCP SERVER IMPLEMENTATION.
    """

    def __init__(self) -> None:
        self._methods: dict[str, Callable[..., Any]] = {}

    def register_method(self, name: str, handler: Callable[..., Any]) -> None:
        self._methods[name] = handler

    def dispatch(self, message: dict[str, Any]) -> dict[str, Any] | None:
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

        method_name = message["method"]
        params = message.get("params", {})

        if method_name not in self._methods:
            if has_id:
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {
                        "code": METHOD_NOT_FOUND,
                        "message": f"Method not found: {method_name}",
                    },
                }
            return None

        handler = self._methods[method_name]

        try:
            if isinstance(params, dict):
                result = handler(**params)
            elif isinstance(params, list):
                result = handler(*params)
            else:
                result = handler()
        except TypeError as e:
            if has_id:
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {
                        "code": INVALID_PARAMS,
                        "message": f"Invalid params for method '{method_name}': {e}",
                    },
                }
            return None
        except Exception as e:
            if has_id:
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {
                        "code": INTERNAL_ERROR,
                        "message": f"Internal error during execution: {e}",
                    },
                }
            return None

        if has_id:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": result,
            }
        return None
