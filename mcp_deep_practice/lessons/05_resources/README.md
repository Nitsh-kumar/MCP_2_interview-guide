# Lesson Metadata

- Protocol revision: 2026-07-28
- SDK baseline: mcp==2.0.0
- Feature status: CORE
- SDK support: FULL
- Verified against: mcp==2.0.0, mcp-types==2.0.0
- Last verified: 2026-08-19

---

# Lesson 05: Resources & URI Templates

## 1. Learning Objectives

By the end of this lesson, you will be able to:
1. Distinguish between an MCP **Resource** (passive, read-only, URI-addressable context) and an MCP **Tool** (active, side-effect producing, parameter-driven action).
2. Register static resources (`@server.resource("docs://...")`) and dynamic resource templates (`@server.resource("tickets://{id}")`).
3. Set appropriate MIME types (`text/plain`, `application/json`, `text/markdown`, `application/pdf`).
4. Perform resource discovery and reading using `await client.list_resources()`, `await client.list_resource_templates()`, and `await client.read_resource(uri)`.
5. Classify at least 12 real-world capabilities into **Tool**, **Resource**, or **Prompt** with clear architectural defense.
6. Handle resource retrieval failure cases cleanly (unknown URI, malformed URI, missing record).

---

## 2. The Three Layers of MCP Resources

```
┌─────────────────────────────────────────────────────────────────────────┐
│ LAYER 3: Application Data & Filesystem                                  │
│ In-memory dictionaries, documentation files, telemetry buffers          │
├─────────────────────────────────────────────────────────────────────────┤
│ LAYER 2: SDK Resource Router & URI Templates                            │
│ @server.resource("schema://{var}"), URI matching, MIME type headers     │
├─────────────────────────────────────────────────────────────────────────┤
│ LAYER 1: Wire Protocol (JSON-RPC)                                       │
│ resources/list -> resources/read -> ReadResourceResult.contents         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Lesson Progression

- **Stage A (Observe)**: Run `uv run python lessons/05_resources/demo.py` to observe static and dynamic URI template reading.
- **Stage B (Explain)**: Read `concepts.md` and master the "Tool vs. Resource vs. Prompt" decision framework.
- **Stage C (Modify)**: In `exercise.py`, implement dynamic resource templates and classify 12 integration scenarios.
- **Stage D (Debug)**: Handle URI resolution failures and invalid template parameters.
- **Stage E (Build / Challenge)**: In `challenge.md`, refactor a bloated read-only tool surface into clean URI resources.

---

## 4. Verification

Run the lesson tests:
```bash
uv run pytest lessons/05_resources/test_exercise.py -v
```
