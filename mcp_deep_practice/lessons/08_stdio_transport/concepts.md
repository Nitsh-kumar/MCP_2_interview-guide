# Concepts: `stdio` Transport & Process Mechanics

## 1. Operating System Process Fundamentals

When an AI host (like Claude Desktop or an IDE) connects to a local MCP server over `stdio`, it spawns the server as a **child subprocess** and connects via standard OS anonymous pipes:

```
┌─────────────────────────────────────────────────────────────────────────┐
│ HOST PROCESS (Parent)                                                   │
│                                                                         │
│  [MCP Client]                                                           │
│     │ Writes Request JSON                                               │
│     ▼                                                                   │
│  (Pipe: stdin) ──────────────────────────────────┐                      │
│                                                  ▼                      │
│                                         [stdin (fd 0)]                  │
│                                         ┌────────────────────────────┐  │
│                                         │ SERVER PROCESS (Child)     │  │
│                                         │                            │  │
│                                         │ [MCPServer]                │  │
│                                         └────────────────────────────┘  │
│                                         [stdout (fd 1)] [stderr (fd 2)] │
│                                                │               │        │
│  (Pipe: stdout) ◄──────────────────────────────┘               │        │
│     │ Reads Response JSON                                      │        │
│     ▼                                                          │        │
│  [JSON-RPC Parser]                                             ▼        │
│                                                          (Log Stream)   │
│                                                          IDE Console    │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 2. The Golden Rule of `stdio` Transport

> [!CRITICAL]
> **`stdout` (file descriptor 1) belongs EXCLUSIVELY to the JSON-RPC wire protocol.**
> **All diagnostic logs, progress prints, and debug information MUST go to `stderr` (file descriptor 2).**

### What Happens When You Violate This Rule:
```python
# CATASTROPHIC BUG IN STDIO SERVERS:
print("Initializing database connection...")  # Writes to stdout!
```

1. The server outputs: `Initializing database connection...\n` to `stdout`.
2. The MCP Client reads the line from the pipe and calls `json.loads("Initializing database connection...")`.
3. Python raises `json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)`.
4. The client disconnects or crashes because the framing stream was corrupted!

---

## 3. How to Properly Log in `stdio` MCP Servers

### Approach 1: Configure Python `logging` to stream to `sys.stderr`
```python
import logging
import sys

logging.basicConfig(
    stream=sys.stderr,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("mcp_server")
logger.info("Server started successfully.")  # Safe! Goes to stderr.
```

### Approach 2: Explicit `sys.stderr.write()`
```python
import sys

print("Debug info", file=sys.stderr)  # Safe!
```

---

## 4. Process Lifecycle & Failure Modes

1. **EOF (End of File)**:
   - When the Host terminates or disconnects, it closes the `stdin` pipe.
   - The MCP Server detects EOF on `stdin` and gracefully shuts down.
2. **Child Process Crash**:
   - If the server process crashes, the OS closes `stdout`.
   - The Client catches `EOFError` / broken pipe on `stdout` and reports a clean error to the Host.
3. **Buffer Deadlocks**:
   - If a child writes large unconsumed data to `stderr` while the parent is blocked waiting for `stdout`, a pipe buffer deadlock can occur.
   - Modern MCP clients read `stdout` and `stderr` concurrently using asynchronous tasks (`anyio`).
