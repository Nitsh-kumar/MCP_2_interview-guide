"""
lessons/01_json_rpc/test_exercise.py

Executable specification for Lesson 01 exercise.
Validates JSON-RPC 2.0 message parsing and educational dispatcher behavior.
"""

from __future__ import annotations

import importlib
import pytest

ex = importlib.import_module("lessons.01_json_rpc.exercise")


# ─── 1. Validation Tests ──────────────────────────────────────────────────────


def test_validate_valid_request() -> None:
    valid_req = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {"name": "test"},
    }
    assert ex.validate_jsonrpc_message(valid_req) == []


def test_validate_valid_notification() -> None:
    valid_notif = {
        "jsonrpc": "2.0",
        "method": "notifications/toolsListChanged",
    }
    assert ex.validate_jsonrpc_message(valid_notif) == []


def test_validate_valid_response() -> None:
    valid_resp = {
        "jsonrpc": "2.0",
        "id": 42,
        "result": {"status": "ok"},
    }
    assert ex.validate_jsonrpc_message(valid_resp) == []


def test_validate_missing_jsonrpc_version() -> None:
    bad_req = {"id": 1, "method": "tools/call"}
    errors = ex.validate_jsonrpc_message(bad_req)
    assert len(errors) > 0


def test_validate_wrong_jsonrpc_version() -> None:
    bad_req = {"jsonrpc": "1.0", "id": 1, "method": "tools/call"}
    errors = ex.validate_jsonrpc_message(bad_req)
    assert any("2.0" in e for e in errors)


def test_validate_response_with_both_result_and_error() -> None:
    bad_resp = {
        "jsonrpc": "2.0",
        "id": 1,
        "result": {"status": "ok"},
        "error": {"code": -32600, "message": "Failed"},
    }
    errors = ex.validate_jsonrpc_message(bad_resp)
    assert len(errors) > 0


def test_validate_response_missing_id() -> None:
    bad_resp = {
        "jsonrpc": "2.0",
        "result": {"status": "ok"},
    }
    errors = ex.validate_jsonrpc_message(bad_resp)
    assert any("id" in e.lower() for e in errors)


# ─── 2. Dispatcher Tests ──────────────────────────────────────────────────────


def test_dispatcher_successful_method_call() -> None:
    dispatcher = ex.EducationalJsonRpcDispatcher()
    dispatcher.register_method("add", lambda a, b: a + b)

    msg = {
        "jsonrpc": "2.0",
        "id": 100,
        "method": "add",
        "params": {"a": 10, "b": 25},
    }
    resp = dispatcher.dispatch(msg)
    assert resp is not None
    assert resp["jsonrpc"] == "2.0"
    assert resp["id"] == 100
    assert resp["result"] == 35
    assert "error" not in resp


def test_dispatcher_method_not_found() -> None:
    dispatcher = ex.EducationalJsonRpcDispatcher()

    msg = {
        "jsonrpc": "2.0",
        "id": 101,
        "method": "non_existent_method",
        "params": {},
    }
    resp = dispatcher.dispatch(msg)
    assert resp is not None
    assert resp["id"] == 101
    assert "error" in resp
    assert resp["error"]["code"] == ex.METHOD_NOT_FOUND


def test_dispatcher_invalid_params() -> None:
    dispatcher = ex.EducationalJsonRpcDispatcher()
    dispatcher.register_method("greet", lambda name: f"Hello, {name}")

    msg = {
        "jsonrpc": "2.0",
        "id": 102,
        "method": "greet",
        "params": {"wrong_arg": "Alice"},
    }
    resp = dispatcher.dispatch(msg)
    assert resp is not None
    assert resp["id"] == 102
    assert "error" in resp
    assert resp["error"]["code"] == ex.INVALID_PARAMS


def test_dispatcher_notification_returns_none() -> None:
    dispatcher = ex.EducationalJsonRpcDispatcher()
    called = []
    dispatcher.register_method("log_event", lambda event: called.append(event))

    msg = {
        "jsonrpc": "2.0",
        "method": "log_event",
        "params": {"event": "user_logged_in"},
    }
    resp = dispatcher.dispatch(msg)
    assert resp is None
    assert called == ["user_logged_in"]
