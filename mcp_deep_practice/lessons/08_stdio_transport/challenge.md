# Challenge: Building a Standalone stdio MCP Developer Utility

## Objective

Build a standalone, executable stdio MCP utility CLI script using `MCPServer` that can be launched as a child process by any MCP host.

---

## Requirements & Constraints

1. **Self-Contained Executable**:
   - The script must be executable with `python script.py`.
   - When run, it must execute `server.run_stdio_async()` (or `server.run(transport="stdio")`).
2. **Strict Protocol Compliance**:
   - `stdout` must NEVER receive unstructured text.
   - All logging must be redirected to `sys.stderr`.
3. **Safe Tools Surface**:
   - Tool 1: `evaluate_regex(pattern: str, text: str)` -> matches/groups extraction.
   - Tool 2: `convert_timestamp(epoch_seconds: float, target_tz: str = "UTC")` -> formatted datetime string.
   - No arbitrary shell command execution!
   - No unrestricted filesystem access!
