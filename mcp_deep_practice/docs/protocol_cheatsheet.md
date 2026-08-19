# MCP Protocol Quick-Reference Cheatsheet

> Protocol target: `2026-07-28` | SDK: `mcp==2.0.0`

---

## JSON-RPC 2.0 Message Types

### Request (expects a response)
```json
{
  "jsonrpc": "2.0",
  "id": "req-001",
  "method": "tools/call",
  "params": { ... }
}
```
- `id` must be string or integer (never null for requests).
- `params` is optional but almost always present in MCP.

### Response (success)
```json
{
  "jsonrpc": "2.0",
  "id": "req-001",
  "result": { ... }
}
```

### Response (error)
```json
{
  "jsonrpc": "2.0",
  "id": "req-001",
  "error": {
    "code": -32602,
    "message": "Invalid params",
    "data": { "field": "ticket_id", "reason": "required" }
  }
}
```

### Notification (no response expected)
```json
{
  "jsonrpc": "2.0",
  "method": "notifications/toolsListChanged",
  "params": {}
}
```
- No `id` field.
- Server or client can send notifications.

---

## Standard JSON-RPC Error Codes

| Code | Name | Meaning |
|---|---|---|
| -32700 | Parse Error | JSON syntax invalid |
| -32600 | Invalid Request | JSON-RPC structure invalid |
| -32601 | Method Not Found | Method does not exist |
| -32602 | Invalid Params | Parameter types/values wrong |
| -32603 | Internal Error | Server-side unhandled error |
| -32000 to -32099 | Implementation-defined | MCP-specific errors |

---

## Core MCP Methods (2026-07-28)

### Discovery
```
server/discover          → capabilities + full catalog (MODERN)
```

### Tools
```
tools/list               → [ToolInfo, ...]
tools/call               → CallToolResult | CreateTaskResult
```

### Resources
```
resources/list           → [ResourceInfo, ...]
resources/read           → ResourceContent
```

### Prompts
```
prompts/list             → [PromptInfo, ...]
prompts/get              → PromptMessages
```

### Subscriptions (MODERN)
```
subscriptions/listen     → long-lived POST stream of notifications
```

### Tasks Extension (MODERN — SDK NOT_IMPLEMENTED)
```
tasks/get                → TaskStatus + result (if complete)
tasks/update             → server→client progress update
tasks/cancel             → request task cancellation
```
> Task CREATION is server-directed. A `tools/call` response may return
> `CreateTaskResult` with `resultType: "task"` instead of a direct result.

---

## Modern HTTP Request Headers

| Header | Direction | Purpose |
|---|---|---|
| `MCP-Protocol-Version` | Client → Server | Declare protocol version (must match `_meta`) |
| `Mcp-Method` | Client → Server | JSON-RPC method name (gateway routing) |
| `Mcp-Name` | Client → Server | Tool/resource/prompt name (gateway routing) |
| `Content-Type: application/json` | Client → Server | Standard JSON body |
| `Accept: text/event-stream` | Client → Server | Streaming response requested |

---

## Request `_meta` Block (MODERN)

The `_meta` field in request `params` carries protocol metadata in modern requests:

```json
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
```

> ⚠️ `_meta.io.modelcontextprotocol/protocolVersion` and the HTTP header
> `MCP-Protocol-Version` MUST agree. Mismatch → HTTP 400 (`HeaderMismatch`).

---

## Transport Comparison

| Aspect | stdio | Streamable HTTP |
|---|---|---|
| Use case | Local, same-machine | Remote, multi-tenant, scalable |
| Request framing | Newline-delimited JSON | HTTP POST body |
| Streaming | Not applicable | SSE response body |
| Diagnostics | stderr only | Application logs + OTel |
| stdout pollution | Corrupts protocol stream | Not applicable |
| Load balancing | N/A | Works natively (stateless) |

---

## State: Protocol vs Application

```
PROTOCOL STATE (none in modern MCP 2026-07-28)
  No Mcp-Session-Id
  No persistent session
  Each request self-contained

APPLICATION STATE (your responsibility)
  cart_id, user_id, tenant_id, task_id, idempotency_key
  These travel as explicit tool arguments or auth token claims
  The application stores them; the protocol does not
```

---

## Common Python SDK v2 Patterns

```python
from mcp.server import MCPServer
from mcp import Client, ClientSession

# Server
server = MCPServer("my-server")

@server.tool()
async def get_ticket(ticket_id: str) -> dict:
    ...

# Client — high-level (preferred in v2)
async with Client(server) as client:
    tools = await client.list_tools()
    result = await client.call_tool("get_ticket", {"ticket_id": "TKT-42"})

# Client — low-level escape hatch
async with Client(server) as client:
    session: ClientSession = client.session
    # Direct protocol method access
```

---

## Key Design Rules

1. **Narrow tools** — one action per tool, explicit parameters.
2. **Resource for read, tool for action** — don't embed computation in resources.
3. **Idempotency keys** — write tools that may be retried must be idempotent.
4. **Notifications are hints** — always revalidate state after reconnect.
5. **stderr for diagnostics** — never write to stdout in stdio servers.
6. **Application state ≠ protocol state** — pass state explicitly as arguments.
7. **Header ↔ body agreement** — `MCP-Protocol-Version` header must match `_meta`.
8. **Feature detection** — always use `server/discover` before assuming capabilities.
