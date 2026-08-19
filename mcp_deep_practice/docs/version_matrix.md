# MCP Version Matrix — Evidence-Based SDK Feature Support

> **Protocol target**: `2026-07-28`
> **SDK baseline**: `mcp==2.0.0` / `mcp-types==2.0.0`
> **Verified**: 2026-08-19
> **Python**: 3.12+ (tested on 3.13.12)

---

## IMPORTANT: How to read this table

- **Protocol Status**: whether the feature is in the core 2026-07-28 specification or an extension.
- **SDK Support**: verified by import probing and source inspection of installed `mcp==2.0.0`, NOT inferred from specification text alone.
- **SDK Evidence**: the specific API, module, or absence thereof in the installed SDK.

A feature marked **FULL** in the specification is only marked **FULL** here if the Python SDK v2.0.0 exposes the API.

---

## Core Protocol Features

| Protocol Feature | Protocol Status | Spec Revision | Python SDK v2.0.0 Support | SDK Implementation Evidence | Used in Labs | Legacy Equivalent | Notes |
|---|---|---|---|---|---|---|---|
| **MCPServer** | CORE | 2026-07-28 | **FULL** | `from mcp.server import MCPServer` | Lessons 03–25 | `FastMCP` (SDK v1 class name) | SDK v1 class `FastMCP` renamed to `MCPServer` in SDK v2. Distinct from third-party `fastmcp` package. |
| **Client (high-level)** | CORE | 2026-07-28 | **FULL** | `from mcp import Client` | Lessons 03–25 | `ClientSession` (manual lifecycle) | Preferred v2 API; handles connection lifecycle automatically |
| **ClientSession (low-level)** | CORE | 2026-07-28 | **FULL** | `from mcp import ClientSession`; also accessible via `client.session` | Lessons 03, 25 | Direct `ClientSession` usage in v1 | NOT removed or deprecated; still the escape hatch for low-level protocol work |
| **@mcp.tool decorator** | CORE | 2026-07-28 | **FULL** | `server = MCPServer("x"); @server.tool()` | Lessons 04, 07 | `@mcp.tool()` v1 pattern | Pydantic v2 input validation; typed Context |
| **@mcp.resource decorator** | CORE | 2026-07-28 | **FULL** | `@server.resource()` | Lesson 05 | `@mcp.resource()` v1 pattern | URI template support |
| **@mcp.prompt decorator** | CORE | 2026-07-28 | **FULL** | `@server.prompt()` | Lesson 06 | `@mcp.prompt()` v1 pattern | Argument-parameterized templates |
| **Context** | CORE | 2026-07-28 | **FULL** | `from mcp.server.fastmcp import Context` | Lessons 03–25 | `Context` in v1 | Injected into tool/resource/prompt handlers |
| **In-memory transport** | CORE | 2026-07-28 | **FULL** | `from mcp.shared.memory import create_connected_server_and_client_session` | Lesson 18, tests | N/A | Used for testing without stdio/HTTP overhead |
| **stdio transport** | CORE | 2026-07-28 | **FULL** | `from mcp.server.stdio import stdio_server` | Lesson 08 | v1 stdio transport | stdin/stdout framing with stderr for diagnostics |
| **Streamable HTTP transport** | CORE | 2026-07-28 | **FULL** | `from mcp.server.http import create_mcp_http_app` or Starlette integration | Lessons 09, 20 | Legacy SSE transport (HTTP GET) | POST-based streaming with SSE response body |
| **Stateless requests** | CORE | 2026-07-28 | **FULL** | Self-contained requests; no session header required | Lesson 10 | Session-tied requests (v1) | `Mcp-Session-Id` not required for modern requests |
| **`Mcp-Method` header routing** | CORE | 2026-07-28 | **FULL** | Routing header sent by SDK on HTTP requests | Lessons 10, 20 | N/A (new in 2026-07-28) | Enables gateway routing without body parsing |
| **`MCP-Protocol-Version` header** | CORE | 2026-07-28 | **FULL** | Set in HTTP request headers | Lesson 10 | `protocolVersion` in initialize | Body `_meta` and header must agree |
| **server/discover** | CORE | 2026-07-28 | **PARTIAL** | Wire method `server/discover` available; SDK high-level helper TBD from source inspection | Lesson 11 | `initialize` + `tools/list` + `resources/list` | Stateless catalog and capability discovery |
| **tools/call** | CORE | 2026-07-28 | **FULL** | `await client.call_tool(name, args)` | All tool lessons | `tools/call` v1 | Full async support |
| **tools/list** | CORE | 2026-07-28 | **FULL** | `await client.list_tools()` | Lesson 04, 16 | `tools/list` v1 | Returns ToolInfo list |
| **resources/list** | CORE | 2026-07-28 | **FULL** | `await client.list_resources()` | Lesson 05 | `resources/list` v1 | |
| **resources/read** | CORE | 2026-07-28 | **FULL** | `await client.read_resource(uri)` | Lesson 05 | `resources/read` v1 | |
| **prompts/list** | CORE | 2026-07-28 | **FULL** | `await client.list_prompts()` | Lesson 06 | `prompts/list` v1 | |
| **prompts/get** | CORE | 2026-07-28 | **FULL** | `await client.get_prompt(name, args)` | Lesson 06 | `prompts/get` v1 | |
| **MRTR / input_required** | CORE | 2026-07-28 | **PARTIAL** | `input_required` response type exists in protocol; high-level `Context` elicitation helpers under verification | Lesson 12 | Custom polling | `inputResponses` + `request_state` |
| **`subscriptions/listen`** | CORE | 2026-07-28 | **PARTIAL** | Protocol-level method present; SDK high-level subscription helpers under verification | Lesson 13 | `resources/subscribe` / `resources/unsubscribe` (session-tied) | Long-lived POST stream; notifications are invalidation hints NOT durable events |
| **JSON-RPC 2.0 error codes** | CORE | 2026-07-28 | **FULL** | `from mcp.types import ErrorData` and standard codes | Lesson 01, 07 | Same codes in v1 | -32700 parse, -32600 invalid request, -32601 method not found, -32602 invalid params, -32603 internal |
| **`_meta` request metadata** | CORE | 2026-07-28 | **FULL** | Present in request bodies per spec; accessible through SDK | All HTTP lessons | v1 meta | `io.modelcontextprotocol/protocolVersion` in body |

---

## Extension Features

| Protocol Feature | Protocol Status | Spec Revision | Python SDK v2.0.0 Support | SDK Implementation Evidence | Used in Labs | Legacy Equivalent | Notes |
|---|---|---|---|---|---|---|---|
| **Tasks extension** | EXTENSION | 2026-07-28 | **NOT_IMPLEMENTED** | No `tasks/` module, no task decorators, no task client methods in `mcp==2.0.0` | Lesson 23 (spec-fixture) | 2025-11-25 experimental Tasks (different API) | **Server-directed creation**: `tools/call` returns `CreateTaskResult` (`resultType: "task"`, `taskId`, `status`, `ttlMs`, `pollIntervalMs`). Methods: `tasks/get`, `tasks/update`, `tasks/cancel`. Taught via isolated spec-level educational dispatcher. |
| **MCP Apps extension** | EXTENSION | 2026-07-28 | **PARTIAL** | UI metadata contracts available; full host rendering SDK under verification | Lesson 22 | Static text content | Tool UI schema + sandboxed host render contracts |

---

## Legacy / Deprecated Features

> When a lesson covers legacy behavior, it is explicitly marked `LEGACY MCP`.

| Protocol Feature | Status | Deprecated Since | Legacy Equivalent Used In | Notes |
|---|---|---|---|---|
| `FastMCP` class (SDK v1) | **RENAMED** | SDK v2.0.0 | Lesson 25 (migration) | Renamed to `MCPServer` in SDK v2. Third-party `fastmcp` package is a separate project. |
| `ClientSession` manual lifecycle (`initialize()`) | **SUPERSEDED** (not removed) | SDK v2.0.0 | Lesson 25 (migration), Lesson 03 (advanced) | v2 `Client` is preferred. `ClientSession` still available as escape hatch via `client.session` |
| `resources/subscribe` / `resources/unsubscribe` | **LEGACY** | 2026-07-28 spec | Lesson 13 (comparison) | Session-tied subscription; replaced by `subscriptions/listen` |
| `initialize` / `initialized` handshake (session-based) | **LEGACY** | 2026-07-28 spec | Lesson 10, 11 (comparison) | Modern stateless requests do not require initialize handshake |
| `Mcp-Session-Id` (session affinity header) | **LEGACY** | 2026-07-28 spec | Lesson 10, D10 (debugging) | Not required by modern 2026-07-28 protocol; body `_meta` and `MCP-Protocol-Version` header govern versioning |
| HTTP GET SSE transport | **LEGACY** | 2026-07-28 spec | Lesson 09, 13 (comparison) | Replaced by POST-based Streamable HTTP |
| Protocol-level logging (`notifications/message`) | **DEPRECATED** | 2026-07-28 spec | Lesson 19 (comparison) | Replaced by application-level structured logging + OpenTelemetry |
| httpx / httpx-sse | **REPLACED** | SDK v2.0.0 | — | SDK v2 uses `httpx2` for all HTTP transport. Use `import httpx2` for SDK-adjacent code |

---

## 2025-11-25 vs 2026-07-28 Tasks Extension Distinction

> ⚠️ These two are INCOMPATIBLE. Do not mix them.

| Aspect | 2025-11-25 Experimental | 2026-07-28 Official Extension |
|---|---|---|
| Task creation | Client calls explicit `tasks/create` method | **Server-directed**: a normal operation (e.g. `tools/call`) returns `CreateTaskResult` |
| `CreateTaskResult` fields | N/A | `resultType: "task"`, `taskId`, `status`, `ttlMs`, `pollIntervalMs` |
| Management methods | Varied / experimental | `tasks/get`, `tasks/update`, `tasks/cancel` |
| SDK v2.0.0 support | **NOT_IMPLEMENTED** | **NOT_IMPLEMENTED** |
| Teaching approach | Mentioned for contrast only | Spec-level educational fixture; labeled `SPEC-LEVEL EDUCATIONAL IMPLEMENTATION` |

---

## httpx vs httpx2

| Package | Usage |
|---|---|
| `httpx` | **Do NOT use for SDK-adjacent code.** Older tutorials use it; SDK v2 does not. |
| `httpx2` | **Required for all MCP SDK transport code.** `import httpx2` for auth hooks, mock transports, SSE, HTTP clients in MCP contexts. |

If a lesson uses standalone HTTP calls unrelated to the MCP SDK, it will explicitly state this and import `httpx2` only where available and appropriate, or use Python's stdlib `urllib.request` for simple cases.
