# Concepts: Content Blocks & Robust JSON Schemas

## 1. Why Tool Schemas Are a Security & Reliability Surface

When an LLM decides to call a tool, its decision is guided entirely by the JSON Schema advertised by the tool.

```
Vague Schema (Dangerous):
  {"properties": {"query": {"type": "string"}, "options": {"type": "object"}}}
  -> LLM hallucinates non-existent options like {"force": true, "bypass_auth": true}

Constrained Schema (Robust):
  {"properties": {"environment": {"enum": ["dev", "staging", "production"]}}}
  -> LLM is strictly constrained to valid, known operational values.
```

---

## 2. Pydantic v2 to JSON Schema Translation

The official Python SDK (`mcp==2.0.0`) utilizes Pydantic v2 to generate JSON Schemas from Python type annotations.

### Essential Constraints:
- **Enums / Literals**: `Literal["development", "staging", "production"]` translates to JSON Schema `{"enum": ["development", "staging", "production"]}`.
- **String Bounds**: `Field(min_length=5, max_length=100)` prevents empty strings and token-flooding attacks.
- **Array Bounds**: `Field(min_length=1, max_length=10)` guarantees non-empty lists and prevents denial-of-service.
- **Descriptions**: `Field(description="...")` gives the LLM semantic guidance on parameter purpose.
- **Nested Models**: Pydantic `BaseModel` classes generate clean `$defs` nested schemas.

---

## 3. Verified MCP Content Block Types

In SDK v2, `CallToolResult.content` is a list of content blocks:

1. **`TextContent`**:
   ```python
   TextContent(type="text", text="JSON or markdown formatted output")
   ```
2. **`ImageContent`**:
   ```python
   ImageContent(type="image", data="base64_encoded_data", mimeType="image/png")
   ```
3. **`EmbeddedResource`**:
   ```python
   EmbeddedResource(type="resource", resource=TextResourceContents(uri="...", text="..."))
   ```

---

## 4. Schema Evolution Best Practices

1. **Never Remove or Rename Required Fields**: Treat MCP schemas as public API contracts.
2. **Add Optional Fields with Defaults**: When evolving schemas, introduce new parameters as optional with safe default values.
3. **Keep Descriptions Precise**: Explicitly describe accepted formats (e.g., ISO-8601 timestamps `YYYY-MM-DDTHH:MM:SSZ`).
