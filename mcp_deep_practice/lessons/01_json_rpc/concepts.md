# Concepts: JSON-RPC 2.0

## 1. What is JSON-RPC 2.0?

JSON-RPC 2.0 is a stateless, lightweight remote procedure call (RPC) protocol encoded in JSON. It defines how a client invokes a method on a server and how the server returns the result or an error.

MCP adopts JSON-RPC 2.0 as its underlying message framing standard for all transports (both stdio and Streamable HTTP).

---

## 2. The Four Message Types

### 1. Request
A request invokes a method on the receiver and demands a response with a matching `id`.

```json
{
  "jsonrpc": "2.0",
  "id": "req-101",
  "method": "tools/call",
  "params": {
    "name": "calculate_tax",
    "arguments": {"amount": 100.0, "rate": 0.08}
  }
}
```

Rules:
- `jsonrpc` MUST be `"2.0"`.
- `method` MUST be a string.
- `id` MUST be a string, integer, or null (string/integer recommended; null discouraged).
- `params` MAY be an object (by-name) or array (by-position). MCP standardizes on objects.

---

### 2. Success Response
Returned by the receiver when a request succeeds.

```json
{
  "jsonrpc": "2.0",
  "id": "req-101",
  "result": {
    "content": [{"type": "text", "text": "Tax: 8.0"}],
    "isError": false
  }
}
```

Rules:
- `id` MUST match the request's `id`.
- `result` is required on success.
- MUST NOT contain an `error` member.

---

### 3. Error Response
Returned by the receiver when a request fails at the protocol or execution level.

```json
{
  "jsonrpc": "2.0",
  "id": "req-101",
  "error": {
    "code": -32601,
    "message": "Method not found: tools/unknown_tool",
    "data": {"details": "Available methods: tools/call, tools/list"}
  }
}
```

Rules:
- `id` MUST match the request's `id` (or `null` if the request ID could not be parsed).
- `error` MUST be an object with `code` (integer) and `message` (string).
- `data` is optional additional context.
- MUST NOT contain a `result` member.

---

### 4. Notification
A one-way, fire-and-forget message. The receiver MUST NOT reply.

```json
{
  "jsonrpc": "2.0",
  "method": "notifications/toolsListChanged"
}
```

Rules:
- MUST NOT contain an `id` property.
- If an `id` is included (even if `null`), it is considered a Request, not a Notification!

---

## 3. Standard JSON-RPC Error Codes

| Code | Name | Meaning |
|---|---|---|
| `-32700` | Parse error | Invalid JSON was received by the server. |
| `-32600` | Invalid Request | The JSON sent is not a valid Request object. |
| `-32601` | Method not found | The method does not exist / is not available. |
| `-32602` | Invalid params | Invalid method parameter(s). |
| `-32603` | Internal error | Internal JSON-RPC error. |
| `-32000` to `-32099` | Server error | Reserved for implementation-defined server errors. |

---

## 4. MCP Protocol Errors vs. Tool Execution Errors

A critical distinction in MCP:

1. **Protocol-Level Error (JSON-RPC Error)**:
   - Example: Client sends unknown method `system/reboot` -> Server returns `-32601 Method not found`.
   - Example: Client sends invalid JSON -> Server returns `-32700 Parse error`.
2. **Tool-Level Error (Domain Error inside JSON-RPC Success Result)**:
   - Example: Client calls tool `get_file` with path `/nonexistent` -> Server successfully handles `tools/call` and returns a JSON-RPC **result** with `isError: true` and a text error message.
   - Why? Because the LLM needs to *read* the tool failure message in its conversation context and self-correct! A JSON-RPC protocol error would abort the transport stream.
