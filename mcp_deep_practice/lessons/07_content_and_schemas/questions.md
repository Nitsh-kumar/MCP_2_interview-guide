# Conceptual & Interview Questions: Content & Schemas

### Q1 [Reasoning]: Why is an unconstrained dictionary parameter (e.g. `options: dict = {}`) considered an anti-pattern in MCP tool design?
**Answer Rubric:**
- An unconstrained `dict` produces an empty schema (`{"type": "object"}`) in JSON Schema.
- The LLM has zero documentation regarding valid key names, expected value types, or allowed configurations. This dramatically increases hallucinations and invalid tool invocations.

---

### Q2 [Factual]: What content block types are officially supported in SDK v2 (`mcp==2.0.0`)?
**Answer Rubric:**
- `TextContent` (plain text, markdown, JSON payloads)
- `ImageContent` (base64-encoded image data with MIME type)
- `EmbeddedResource` (embedded resource contents)

---

### Q3 [Architecture]: How does schema validation happen in the Python SDK?
**Answer Rubric:**
- The SDK uses Pydantic v2 to validate incoming dictionary parameters against the function's type annotations and Pydantic models before the tool function body is executed.
- If validation fails, a descriptive error is returned to the client/LLM without executing the tool body.

---

### Q4 [Debugging]: A tool expects `environment` to be `"staging"`, but the LLM passes `"Staging"`. How can you make the schema resilient to this?
**Answer Rubric:**
- Use Pydantic field validators (`@field_validator`) with `.strip().lower()` or use an Enum that normalizes case during deserialization.

---

### Q5 [Security]: How do string length constraints (`min_length`, `max_length`) protect an MCP server?
**Answer Rubric:**
- Prevent Denial of Service (DoS) and context stuffing attacks where an adversarial prompt injection attempts to pass megabytes of text into a tool argument.
