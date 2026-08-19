# Conceptual & Interview Questions: JSON-RPC 2.0

### Q1 [Factual]: What is the exact difference between a JSON-RPC Request and a Notification?
**Answer Rubric:**
- A **Request** contains an `"id"` member (string or integer) and requires the receiver to reply with a Response object bearing the exact same `"id"`.
- A **Notification** MUST NOT contain an `"id"` member. The receiver processes the notification asynchronously and MUST NOT return any response.

---

### Q2 [Factual]: What are the 5 standard JSON-RPC 2.0 reserved error codes?
**Answer Rubric:**
- `-32700`: Parse error (invalid JSON)
- `-32600`: Invalid Request (JSON sent is not a valid Request object)
- `-32601`: Method not found
- `-32602`: Invalid params (invalid method arguments)
- `-32603`: Internal error

---

### Q3 [Reasoning]: In an MCP server, why does a tool failure (e.g. file not found) return a JSON-RPC Success with `isError: true` rather than a `-32603` JSON-RPC Protocol Error?
**Answer Rubric:**
- A JSON-RPC protocol error (`-32603`) signifies that the RPC layer itself failed (e.g., unhandled server exception, transport crash).
- A tool execution failure (e.g., file not found, permission denied) is a legitimate domain result. Returning it as a successful RPC response containing `isError: true` allows the MCP Client/Host to feed the error message back to the LLM so the model can reason about the failure, adjust its parameters, and retry.

---

### Q4 [Debugging]: A client sends `{"jsonrpc": "2.0", "id": null, "method": "ping"}`. Is this a Notification or a Request, and what should the server do?
**Answer Rubric:**
- It is a **Request** because the `"id"` field is present (even though its value is `null`).
- While the JSON-RPC 2.0 spec discourages `null` IDs, if a server can parse the request, it should return a response with `"id": null`.

---

### Q5 [Architecture]: Why did MCP choose JSON-RPC 2.0 instead of inventing a custom binary or REST-based messaging format?
**Answer Rubric:**
- **Simplicity and ubiquity**: JSON is supported natively in every programming language without compilation steps.
- **Bi-directional symmetry**: JSON-RPC works identically over stdio (pipes), WebSockets, and HTTP/SSE.
- **Prior art**: Proven at scale by the Language Server Protocol (LSP) for developer tooling.
