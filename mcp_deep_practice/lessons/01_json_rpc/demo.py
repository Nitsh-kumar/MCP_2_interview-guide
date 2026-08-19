#!/usr/bin/env python
"""
lessons/01_json_rpc/demo.py

Demonstration: Raw JSON-RPC 2.0 Message Structure and Wire Inspection.

Shows the exact byte/JSON frames that cross the wire during:
  1. Standard Request
  2. Success Response
  3. Notification (no id, no response expected)
  4. Protocol Error Response (method not found / invalid params)
  5. Distinction between Protocol Error vs. Tool Application Error
"""

from __future__ import annotations

import json


def print_frame(title: str, payload: dict) -> None:
    print(f"\n--- {title} ---")
    print(json.dumps(payload, indent=2))


def main() -> None:
    print("=" * 64)
    print("  Lesson 01 Demo: Raw JSON-RPC 2.0 Protocol Frames")
    print("=" * 64)

    # 1. Valid Request (Client -> Server)
    valid_request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": "calculate_hash",
            "arguments": {"input": "hello world", "algorithm": "sha256"},
        },
    }
    print_frame("1. Valid Tool Call Request (Client -> Server)", valid_request)

    # 2. Valid Success Response (Server -> Client)
    success_response = {
        "jsonrpc": "2.0",
        "id": 1,
        "result": {
            "content": [
                {
                    "type": "text",
                    "text": "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9",
                }
            ],
            "isError": False,
        },
    }
    print_frame("2. Success Response (Server -> Client)", success_response)

    # 3. Valid Notification (Client -> Server or Server -> Client)
    notification = {
        "jsonrpc": "2.0",
        "method": "notifications/toolsListChanged",
    }
    print_frame("3. Notification (Fire-and-Forget, NO 'id')", notification)

    # 4. Protocol Error: Method Not Found (-32601)
    protocol_error_response = {
        "jsonrpc": "2.0",
        "id": 2,
        "error": {
            "code": -32601,
            "message": "Method not found: admin/destroy_everything",
            "data": {"supported_namespaces": ["tools", "resources", "prompts", "ping"]},
        },
    }
    print_frame("4. Protocol Error Response (Method Not Found)", protocol_error_response)

    # 5. Application/Tool Error (JSON-RPC Success Frame with Tool isError=True)
    tool_error_response = {
        "jsonrpc": "2.0",
        "id": 3,
        "result": {
            "content": [
                {
                    "type": "text",
                    "text": "FileNotFoundError: File '/secret/data.csv' does not exist.",
                }
            ],
            "isError": True,
        },
    }
    print_frame("5. Tool Domain Error (JSON-RPC success, isError=True for LLM)", tool_error_response)

    print("\n" + "=" * 64)
    print("  Key Takeaway:")
    print("    - Protocol errors (e.g. -32601) mean the transport/RPC contract failed.")
    print("    - Tool domain errors return a JSON-RPC 'result' with isError=True so the")
    print("      host/LLM can read the failure message and self-correct.")
    print("=" * 64)


if __name__ == "__main__":
    main()
