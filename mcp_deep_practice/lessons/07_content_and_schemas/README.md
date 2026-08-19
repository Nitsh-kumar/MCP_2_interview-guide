# Lesson Metadata

- Protocol revision: 2026-07-28
- SDK baseline: mcp==2.0.0
- Feature status: CORE
- SDK support: FULL
- Verified against: mcp==2.0.0, mcp-types==2.0.0
- Last verified: 2026-08-19

---

# Lesson 07: Content Blocks & Robust JSON Schemas

## 1. Learning Objectives

By the end of this lesson, you will be able to:
1. Define the contract between Python type annotations, Pydantic models, JSON Schema, and MCP content blocks.
2. Contrast vague, unconstrained schemas (e.g. `query: str, options: dict`) with tightly constrained, misuse-resistant domain schemas.
3. Apply schema constraints: required vs. optional fields, string length bounds (`min_length`, `max_length`), enum choices, array length bounds (`min_items`, `max_items`), and nested models.
4. Construct verified MCP content blocks (`TextContent`, `ImageContent`) supported in `mcp==2.0.0`.
5. Design schemas specifically to minimize LLM hallucinations, parameter guessing, and unintended execution paths.

---

## 2. The Three Layers of MCP Schemas & Content

```
┌─────────────────────────────────────────────────────────────────────────┐
│ LAYER 3: Domain Validation & Pydantic Constraints                       │
│ Pydantic BaseModel with Field(min_length=5, pattern="^ISO...$")         │
├─────────────────────────────────────────────────────────────────────────┤
│ LAYER 2: Python SDK Type Marshaling                                     │
│ Type hints -> JSON Schema inputSchema, TextContent block packaging      │
├─────────────────────────────────────────────────────────────────────────┤
│ LAYER 1: Wire JSON-RPC Payload                                          │
│ inputSchema: {"type": "object", "properties": {...}, "required": [...]} │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Lesson Progression

- **Stage A (Observe)**: Run `uv run python lessons/07_content_and_schemas/demo.py` to compare an unconstrained vs. a strongly-typed tool schema.
- **Stage B (Explain)**: Read `concepts.md` on misuse-resistant schema engineering.
- **Stage C (Modify)**: In `exercise.py`, implement the constrained `create_change_request` tool using Pydantic models.
- **Stage D (Debug)**: Test failure cases: unknown enums, missing nested fields, and length boundary violations.
- **Stage E (Build / Challenge)**: Complete `challenge.md` to design an ambiguity-resistant schema for cloud deployments.

---

## 4. Verification

Run the lesson tests:
```bash
uv run pytest lessons/07_content_and_schemas/test_exercise.py -v
```
