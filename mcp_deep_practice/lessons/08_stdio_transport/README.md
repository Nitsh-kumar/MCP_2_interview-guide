# Lesson Metadata

- Protocol revision: 2026-07-28
- SDK baseline: mcp==2.0.0
- Feature status: CORE
- SDK support: FULL
- Verified against: mcp==2.0.0, mcp-types==2.0.0
- Last verified: 2026-08-19

---

# Lesson 08: `stdio` Transport & Process Mechanics

## 1. Learning Objectives

By the end of this lesson, you will be able to:
1. Explain how the `stdio` transport works from operating system process fundamentals: parent/child processes, file descriptors 0 (`stdin`), 1 (`stdout`), and 2 (`stderr`), and anonymous pipes.
2. Master the **Golden Rule of `stdio` Transport**:
   - `stdout` belongs EXCLUSIVELY to newline-delimited JSON-RPC protocol traffic.
   - All logging, debug messages, and diagnostics MUST be routed to `stderr`.
3. Diagnose and fix the classic "stdout pollution" bug caused by stray `print()` calls in MCP servers.
4. Implement a clean stdio MCP server utility and client using the official SDK.
5. Handle process lifecycle events: clean launch, EOF detection, broken pipe errors, and graceful termination.

---

## 2. The Three Layers of stdio Transport

```
┌─────────────────────────────────────────────────────────────────────────┐
│ LAYER 3: Application Tools & Diagnostic Logging                         │
│ Tool implementations, logging.basicConfig(stream=sys.stderr)            │
├─────────────────────────────────────────────────────────────────────────┤
│ LAYER 2: SDK stdio Server & Framing                                     │
│ mcp.server.stdio.stdio_server, newline-delimited JSON-RPC serialization  │
├─────────────────────────────────────────────────────────────────────────┤
│ LAYER 1: OS Process Pipes & File Descriptors                            │
│ Parent stdin/stdout pipes, child fd 0/1/2, OS signal SIGTERM / EOF      │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Lesson Progression

- **Stage A (Observe)**: Run `uv run python lessons/08_stdio_transport/demo.py` to observe process launch, stdio pipe communication, stderr logging, and clean teardown.
- **Stage B (Explain)**: Read `concepts.md` detailing OS process pipe mechanics and stream framing.
- **Stage C (Modify)**: In `exercise.py`, configure logging and diagnostic channels so stdout remains 100% pure protocol traffic.
- **Stage D (Debug)**: Fix an intentionally broken stdio server that corrupts the JSON-RPC wire with stray stdout prints.
- **Stage E (Build / Challenge)**: Complete `challenge.md` to build a standalone developer utility server over stdio.

---

## 4. Verification

Run the lesson tests:
```bash
uv run pytest lessons/08_stdio_transport/test_exercise.py -v
```
