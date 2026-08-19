# Conceptual & Interview Questions: Prompts

### Q1 [Factual]: Who initiates an MCP Prompt call vs an MCP Tool call?
**Answer Rubric:**
- **MCP Prompt**: Initiated by the **User or Host Application** (e.g. user selects a slash command `/review_code` in the UI).
- **MCP Tool**: Initiated autonomously by the **Model (LLM)** during an agent reasoning loop when it decides it needs external data or actions.

---

### Q2 [Reasoning]: Why is an MCP Prompt returned as a list of `PromptMessage` objects rather than raw unstructured text?
**Answer Rubric:**
- Structuring as `PromptMessage(role, content)` allows the server to specify conversational roles (e.g. `user`, `assistant`) and multi-turn few-shot examples or system-level instructions that the Host can inject directly into the LLM conversation history.

---

### Q3 [Architecture]: How does the Resource + Prompt + Tool separation prevent accidental runaway agent loops?
**Answer Rubric:**
- If an MCP tool attempts to do everything (read data, formulate prompt, execute writes), the Host loses visibility and cannot insert human approval checkpoints.
- By separating into Resource (passive read), Prompt (user-triggered guide), and Tool (action), the user reviews the prompt output before authorizing the tool execution.

---

### Q4 [Debugging]: A client calls `await client.get_prompt("summarize", {})` and receives a validation error. What went wrong?
**Answer Rubric:**
- The prompt has required arguments (e.g. `topic: str` without a default value) that were omitted in the arguments dictionary.

---

### Q5 [Factual]: How does the Python SDK generate the schema for `@server.prompt()` arguments?
**Answer Rubric:**
- The SDK inspects the Python function's parameter names, type annotations, and default values to construct `PromptArgument` objects advertised via `prompts/list`.
