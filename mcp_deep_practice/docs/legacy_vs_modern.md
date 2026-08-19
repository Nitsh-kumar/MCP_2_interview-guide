# Legacy vs Modern MCP — Side-by-Side Protocol Comparison

> LEGACY MCP refers to patterns from MCP specification revisions before 2026-07-28 (e.g., 2025-11-25, 2024-11-05).
> MODERN MCP refers exclusively to the 2026-07-28 specification.
>
> These labels appear throughout the curriculum wherever a distinction matters.
> Never mix them silently.

---

## 1. Session Lifecycle & Initialization

### LEGACY MCP — Session-Based Initialization

Before a client could call any method, it had to complete a mandatory handshake.

**Step 1 — Client sends `initialize`:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "protocolVersion": "2025-11-25",
    "capabilities": { "tools": {} },
    "clientInfo": { "name": "my-client", "version": "1.0.0" }
  }
}
```

**Step 2 — Server responds:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "protocolVersion": "2025-11-25",
    "capabilities": { "tools": { "listChanged": true } },
    "serverInfo": { "name": "my-server", "version": "1.0.0" }
  }
}
```

**Step 3 — Client sends `notifications/initialized`:**
```json
{
  "jsonrpc": "2.0",
  "method": "notifications/initialized"
}
```

Only after this three-step handshake could the client issue real requests.

**Problems for horizontal scaling:**
- Server had to maintain session state between the handshake and subsequent requests.
- A second replica had no knowledge of the handshake that happened on replica one.
- Sticky sessions or shared session stores were required.

---

### MODERN MCP — Stateless Self-Contained Requests

Under MCP 2026-07-28, a modern `tools/call` request is self-contained:

```json
{
  "jsonrpc": "2.0",
  "id": "req-001",
  "method": "tools/call",
  "params": {
    "name": "get_ticket",
    "arguments": { "ticket_id": "TKT-42" },
    "_meta": {
      "io.modelcontextprotocol/protocolVersion": "2026-07-28",
      "io.modelcontextprotocol/clientInfo": {
        "name": "my-client",
        "version": "2.0.0"
      },
      "io.modelcontextprotocol/clientCapabilities": {
        "tools": {}
      }
    }
  }
}
```

**With HTTP routing headers:**
```
POST /mcp HTTP/1.1
Content-Type: application/json
MCP-Protocol-Version: 2026-07-28
Mcp-Method: tools/call
Mcp-Name: get_ticket
```

**Key properties:**
- No prior handshake required.
- Any load-balanced replica can serve the request.
- Protocol version is declared both in the HTTP header AND in `_meta`.
- Header and body must agree — mismatch causes HTTP 400 (see D10_protocol_header_mismatch).
- `Mcp-Session-Id` is NOT present for normal modern requests.

---

## 2. Mcp-Session-Id

### LEGACY MCP — Session ID for Affinity

Older Streamable HTTP transport included a session ID header to route subsequent requests to the same server instance:

```
Mcp-Session-Id: sess_abc123
```

This created implicit statefulness at the transport layer, requiring sticky load balancers or distributed session stores.

### MODERN MCP — No Protocol-Level Session

MCP 2026-07-28 does **not** use `Mcp-Session-Id` for modern stateless request routing.

**Application-layer state is managed explicitly by the application**, not by the protocol transport.

Example: a shopping cart server does NOT track session:
```json
{
  "method": "tools/call",
  "params": {
    "name": "add_to_cart",
    "arguments": {
      "cart_id": "cart_tok_9f8e2a",
      "item_id": "PROD-007",
      "quantity": 1
    }
  }
}
```

The `cart_id` is an explicit application token, not a protocol session. Any replica can serve this request.

---

## 3. Server Discovery

### LEGACY MCP — Discovery via Initialization

Under the old pattern, the client learned about server capabilities through the `initialize` handshake response. Discovering available tools required a subsequent `tools/list` call after initialization.

```
initialize → [capabilities]
tools/list → [tool catalog]
resources/list → [resource catalog]
prompts/list → [prompt catalog]
```

Four sequential round-trips before any real work could begin.

### MODERN MCP — server/discover

```json
{
  "jsonrpc": "2.0",
  "id": "disc-001",
  "method": "server/discover",
  "params": {}
}
```

Response:
```json
{
  "jsonrpc": "2.0",
  "id": "disc-001",
  "result": {
    "protocolVersion": "2026-07-28",
    "capabilities": { "tools": {}, "resources": {}, "prompts": {} },
    "tools": [ { "name": "get_ticket", "description": "...", "inputSchema": {} } ],
    "resources": [],
    "prompts": []
  }
}
```

A single stateless call returns everything. No prior handshake needed.

---

## 4. Subscriptions

### LEGACY MCP — Session-Tied Resource Subscriptions

```json
{ "method": "resources/subscribe", "params": { "uri": "tickets://TKT-42" } }
```

Subscription was bound to the current session. If the session died, the subscription was lost. Unsubscribe:

```json
{ "method": "resources/unsubscribe", "params": { "uri": "tickets://TKT-42" } }
```

HTTP GET SSE was used as a standalone notification channel in some implementations.

### MODERN MCP — subscriptions/listen

```json
{
  "jsonrpc": "2.0",
  "id": "sub-001",
  "method": "subscriptions/listen",
  "params": {
    "topics": ["resource:tickets://TKT-42", "catalog:tools"]
  }
}
```

- A **long-lived POST-response stream** (SSE body on Streamable HTTP transport).
- Decoupled from any session state.
- Notifications are **invalidation hints**, NOT a durable ordered event log.
- If the connection drops, the client must reconnect AND **revalidate state** (re-read the resource) — it cannot assume missed notifications will be replayed.

> ⚠️ WebSockets are NOT the standard transport for `subscriptions/listen` in 2026-07-28. This is a POST-based SSE stream. WebSocket transport, if discussed, is a custom non-core extension.

---

## 5. Transport

### LEGACY MCP — HTTP GET SSE

```
GET /sse HTTP/1.1
Accept: text/event-stream
```

Server kept a persistent GET connection open and pushed events to the client. Inherently unidirectional. Client had to use a separate POST endpoint for requests.

### MODERN MCP — Streamable HTTP (POST)

```
POST /mcp HTTP/1.1
Content-Type: application/json
MCP-Protocol-Version: 2026-07-28
```

A single POST endpoint handles all requests. The response may be:
- A direct JSON response (for simple tool calls)
- An SSE stream body (for streaming responses or `subscriptions/listen`)

This is simpler to proxy, load-balance, and reason about.

---

## 6. Tasks Extension

### 2025-11-25 Experimental Tasks (LEGACY)

Some 2025-era MCP implementations included an experimental `tasks/create` client-initiated method. **This API does not exist in the 2026-07-28 official Tasks extension.**

### 2026-07-28 Official Tasks Extension (MODERN)

Task creation is **server-directed**, not client-initiated.

A normal operation such as `tools/call` returns a `CreateTaskResult` when the operation is long-running:

```json
{
  "jsonrpc": "2.0",
  "id": "req-001",
  "result": {
    "resultType": "task",
    "taskId": "task_abc123",
    "status": "running",
    "ttlMs": 300000,
    "pollIntervalMs": 2000
  }
}
```

The client then manages the task using:
- `tasks/get` — poll current status and result
- `tasks/update` — send progress or partial results (server → client)
- `tasks/cancel` — request cancellation

There is **no `tasks/create` method** in the 2026-07-28 specification.

**Python SDK v2.0.0 does not implement the Tasks extension.**
Lesson 23 teaches this via a spec-level educational fixture only.

---

## 7. Protocol-Level Logging

### LEGACY MCP — notifications/message

Older MCP used a protocol-level logging mechanism: `notifications/message` to send diagnostic log entries through the MCP protocol itself.

### MODERN MCP — Application-Level Observability

MCP 2026-07-28 deprecates protocol-level logging in favor of:
- **Structured application logging to stderr** (for stdio transport diagnostics)
- **OpenTelemetry** for distributed tracing, metrics, and structured logs

See Lesson 19 for the full observability curriculum.

---

## 8. SDK Class Names

### LEGACY MCP — FastMCP (SDK v1)

```python
from mcp import FastMCP

mcp = FastMCP("my-server")

@mcp.tool()
def my_tool(): ...
```

### MODERN MCP — MCPServer (SDK v2)

```python
from mcp.server import MCPServer

server = MCPServer("my-server")

@server.tool()
def my_tool(): ...
```

The `FastMCP` class in the official `modelcontextprotocol/python-sdk` was **renamed** to `MCPServer` in SDK v2. It was not deprecated in the sense of being removed — the functionality is equivalent.

> ⚠️ The **third-party `fastmcp` package** (a separate project not from Anthropic/MCP team) is a different library entirely. All curriculum lessons target the official `mcp` package from PyPI (`modelcontextprotocol/python-sdk`).
