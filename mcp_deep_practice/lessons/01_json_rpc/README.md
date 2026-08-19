# Lesson Metadata

- Protocol revision: 2026-07-28
- SDK baseline: mcp==2.0.0
- Feature status: FOUNDATION
- SDK support: NOT_APPLICABLE
- Verified against: mcp==2.0.0, mcp-types==2.0.0
- Last verified: 2026-08-19

---

# Lesson 01: JSON-RPC 2.0 Foundation

## 1. Learning Objectives

By the end of this lesson, you will be able to:
1. Explain the anatomy of JSON-RPC 2.0 messages: Request, Response, Notification, and Error.
2. Differentiate between a Request (requires an `id` and expects a response) and a Notification (fire-and-forget, MUST NOT have an `id`).
3. Construct and parse standard JSON-RPC 2.0 error codes (`-32700`, `-32600`, `-32601`, `-32602`, `-32603`).
4. Validate incoming JSON-RPC payloads strictly against the specification.
5. Build an educational wire dispatcher from scratch without SDK abstractions.
6. Understand how MCP builds its domain semantics (`tools/call`, `resources/read`, etc.) directly on top of JSON-RPC 2.0.

---

## 2. The Three Layers in JSON-RPC

```
┌─────────────────────────────────────────────────────────────────────────┐
│ LAYER 3: Application Domain                                             │
│ Tool implementation: add(a, b) -> a + b                                 │
├─────────────────────────────────────────────────────────────────────────┤
│ LAYER 2: SDK Protocol Binding                                           │
│ MCPServer dispatches method "tools/call" to Python function             │
├─────────────────────────────────────────────────────────────────────────┤
│ LAYER 1: Raw JSON-RPC 2.0 Frame                                         │
│ {"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {...}}   │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Lesson Progression

- **Stage A (Observe)**: Run `uv run python lessons/01_json_rpc/demo.py` to inspect raw JSON-RPC 2.0 requests, responses, notifications, and error frames.
- **Stage B (Explain)**: Read `concepts.md` and review standard JSON-RPC 2.0 error codes and semantics.
- **Stage C (Modify / Validate)**: Complete `validate_jsonrpc_message()` in `exercise.py`.
- **Stage D (Debug)**: Diagnose malformed wire payloads in `exercise.py`.
- **Stage E (Build from Scratch)**: Complete `EducationalJsonRpcDispatcher` in `exercise.py`.

---

## 4. Verification

Run the lesson tests:
```bash
uv run pytest lessons/01_json_rpc/test_exercise.py -v
```
