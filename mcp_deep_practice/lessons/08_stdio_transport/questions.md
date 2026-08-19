# Conceptual & Interview Questions: `stdio` Transport

### Q1 [Critical / Debugging]: Why does calling `print("Server initialized")` inside an MCP stdio server break the connection with Claude Desktop or Cursor?
**Answer Rubric:**
- In `stdio` transport, `stdout` is the raw byte pipe for JSON-RPC 2.0 protocol frames.
- `print(...)` writes plain text to `stdout`. When the client reads this line and calls `json.loads()`, parsing fails with `JSONDecodeError`, causing the client to crash or drop the session.
- Diagnostic prints must always be sent to `sys.stderr` (e.g. `print(..., file=sys.stderr)` or `logger.info(...)` configured on `sys.stderr`).

---

### Q2 [Factual]: How are messages framed over `stdio` in MCP?
**Answer Rubric:**
- Newline-delimited JSON (ndjson). Each JSON-RPC request or response object is serialized onto a single line terminated by `\n`.

---

### Q3 [Reasoning]: How does a stdio MCP server detect that the host application has closed or crashed?
**Answer Rubric:**
- The operating system closes the `stdin` pipe when the parent process exits.
- The server's `stdin` reader receives an EOF (End of File) / empty read, triggering graceful termination of the event loop.

---

### Q4 [Architecture]: What are the trade-offs between `stdio` transport and `Streamable HTTP` transport?
**Answer Rubric:**
- **`stdio`**:
  - *Pros*: Zero network setup, zero port collisions, automatic OS-managed lifecycle, strict local sandboxing, lowest latency.
  - *Cons*: Single host only, local machine execution only, cannot be scaled horizontally across containers.
- **`Streamable HTTP`**:
  - *Pros*: Multi-tenant, remote cloud hosting, horizontal autoscaling, load-balanced.
  - *Cons*: Requires network security (TLS, OAuth), port management, gateway infrastructure.

---

### Q5 [Debugging]: What happens if a child process writes gigabytes of debug logs to `stderr` and the parent process only reads `stdout`?
**Answer Rubric:**
- The OS pipe buffer for `stderr` fills up (typically 64KB on Linux/Windows). Once full, the child process blocks on write, causing a pipe buffer deadlock where the server hangs indefinitely.
- Robust MCP hosts must read `stdout` and `stderr` asynchronously on separate background tasks.
