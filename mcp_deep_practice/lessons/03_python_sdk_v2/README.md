# Lesson Metadata

- Protocol revision: 2026-07-28
- SDK baseline: mcp==2.0.0
- Feature status: CORE
- SDK support: FULL
- Verified against: mcp==2.0.0, mcp-types==2.0.0
- Last verified: 2026-08-19

---

# Lesson 03: Python SDK v2 (`MCPServer` & `Client`)

## 1. Learning Objectives

By the end of this lesson, you will be able to:
1. Construct and configure an `MCPServer` instance using the modern SDK v2 baseline (`mcp==2.0.0`).
2. Register the three core capability primitives using decorators:
   - `@server.tool()` for callable actions
   - `@server.resource("uri://...")` for read-only context data
   - `@server.prompt()` for reusable prompt templates
3. Connect an in-memory `Client(server)` and verify protocol version `2026-07-28`.
4. Inspect the relationship between the high-level `Client` facade and the underlying `ClientSession`.
5. Access results correctly using official SDK types (`ListToolsResult.tools`, `CallToolResult.content`, `ReadResourceResult.contents`, `GetPromptResult.messages`).

---

## 2. The Three Layers in SDK v2

```
┌─────────────────────────────────────────────────────────────────────────┐
│ LAYER 3: Python Functions & Business Logic                              │
│ def add(a: int, b: int) -> int: return a + b                            │
├─────────────────────────────────────────────────────────────────────────┤
│ LAYER 2: SDK v2 High-Level Facade (MCPServer & Client)                  │
│ @server.tool(), Client(server), Pydantic type inference, Context        │
├─────────────────────────────────────────────────────────────────────────┤
│ LAYER 1: Low-Level Session & In-Memory Streams                          │
│ ClientSession, create_client_server_memory_streams, JSON-RPC messages   │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Lesson Progression

- **Stage A (Observe)**: Run `uv run python lessons/03_python_sdk_v2/demo.py` to observe an end-to-end `MCPServer` with tools, resources, and prompts connected via `Client(server)`.
- **Stage B (Explain)**: Read `concepts.md` comparing SDK v1 vs SDK v2 architectures.
- **Stage C (Modify)**: In `exercise.py`, fix the broken tool, implement the missing resource, and complete the prompt arguments.
- **Stage D (Debug)**: Diagnose return-type unpack mismatches (e.g. iterating over `result` instead of `result.tools`).
- **Stage E (Build / Challenge)**: Reimplement client connection using low-level `ClientSession` and in-memory streams in `challenge.md`.

---

## 4. Verification

Run the lesson tests:
```bash
uv run pytest lessons/03_python_sdk_v2/test_exercise.py -v
```
