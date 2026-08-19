# Conceptual & Interview Questions: Python SDK v2

### Q1 [Factual]: What happened to `FastMCP` in SDK v2 (`mcp==2.0.0`)?
**Answer Rubric:**
- `FastMCP` was the legacy server class in SDK v1.
- In SDK v2, the primary server class is `MCPServer` (imported from `mcp.server import MCPServer`).

---

### Q2 [Factual]: How do you access the list of tools from `await client.list_tools()`?
**Answer Rubric:**
- `await client.list_tools()` returns a `ListToolsResult` object.
- The actual list of `Tool` objects is accessed via the `.tools` attribute (e.g. `result.tools`).

---

### Q3 [Reasoning]: What is the difference between `Client` and `ClientSession` in SDK v2?
**Answer Rubric:**
- `Client` is the high-level asynchronous facade that manages transport connections, context lifecycles, and high-level helper methods.
- `ClientSession` is the lower-level protocol session engine (accessible via `client.session`) managing message IDs, pending requests, and stream framing.

---

### Q4 [Debugging]: A developer wrote `tools = await client.list_tools(); for t in tools: print(t)`. Why does this raise a TypeError?
**Answer Rubric:**
- `ListToolsResult` is a dataclass/Pydantic model, not a list. It is not directly iterable.
- The code must be `for t in tools.tools: print(t)`.

---

### Q5 [Architecture]: Where should `Context` be imported from in SDK v2?
**Answer Rubric:**
- `from mcp.server.context import Context`
- (Legacy v1 tutorials often used `mcp.server.fastmcp.Context`, which fails in v2).
