# Conceptual & Interview Questions: Resources

### Q1 [Factual]: What is the fundamental difference between an MCP Tool and an MCP Resource?
**Answer Rubric:**
- **Resource**: Passive, read-only data entity identified by a URI (e.g. `docs://readme`, `db://schema`). Has MIME type and is safe to cache or pre-fetch.
- **Tool**: Executable action with typed input arguments that can compute results, query dynamic state, or perform side effects on external systems.

---

### Q2 [Reasoning]: Why shouldn't static documentation (like coding standards) be exposed as a `get_coding_standards` Tool?
**Answer Rubric:**
- Exposing static documents as tools consumes tool selection budget in the prompt, increases the risk of LLM hallucinations, and requires an extra model inference turn to invoke.
- As a Resource, the Host can directly attach the documentation into context or let the user reference it with `@docs://standards` without requiring model tool-calling.

---

### Q3 [Architecture]: What is an RFC 6570 URI Template in MCP?
**Answer Rubric:**
- A URI pattern containing parameterized placeholders (e.g. `orders://{order_id}/items`).
- Advertised via `resources/templates/list` so clients know how to construct valid resource URIs dynamically.

---

### Q4 [Debugging]: A client requests a resource URI that does not exist. How should the server respond?
**Answer Rubric:**
- Return a clear error message in the `contents` or raise an MCP resource-not-found error according to SDK conventions, without crashing the server process.

---

### Q5 [Reasoning]: Can reading an MCP resource mutate data in a database?
**Answer Rubric:**
- **No.** The MCP specification mandates that resource reading MUST be idempotent and side-effect free. Any capability that mutates state must be exposed as a Tool.
