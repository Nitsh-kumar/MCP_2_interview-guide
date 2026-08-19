# Conceptual & Interview Questions: MCP Architecture

### Q1 [Factual]: Why is the MCP Client embedded inside the Host rather than running as a standalone daemon?
**Answer Rubric:**
- The Host owns the user interface, agent loop, and LLM orchestration.
- Embedding the MCP Client in the Host allows direct translation between the LLM's tool call decisions and protocol messages, with local enforcement of user approval dialogues and security policies.

---

### Q2 [Reasoning]: If an MCP Server crashes mid-execution, who detects the failure and how is it reported?
**Answer Rubric:**
- The MCP Client detects the broken pipe (stdio) or terminated connection / timeout (HTTP).
- The Client raises an exception or returns a synthetic `CallToolResult(isError=True, content="Server process terminated")` to the Host.
- The Host notifies the LLM or user without crashing the whole application.

---

### Q3 [Architecture]: Where should tool permission checks (e.g., "Allow deleting file X?") be implemented?
**Answer Rubric:**
- In the **Host Application** (Trust Boundary).
- The Host intercepts the tool call before the MCP Client sends the JSON-RPC request over the wire, presenting a UI confirmation prompt to the human user.

---

### Q4 [Reasoning]: How does a multi-server Host handle two servers advertising a tool with the same name?
**Answer Rubric:**
- The Host must namespace the tool names when exposing them to the LLM (e.g., `github__search` vs `jira__search`).
- When the LLM calls `github__search`, the Host strips the prefix and routes the invocation to the GitHub MCP Client.

---

### Q5 [Debugging]: An LLM hallucinates an invalid parameter name for an MCP tool. Which component catches this error?
**Answer Rubric:**
- The **MCP Server** (or client-side Pydantic validator if schema validation is enabled).
- The Server validates the arguments against its registered JSON Schema and returns a `-32602 Invalid params` error or `isError: true` result.
