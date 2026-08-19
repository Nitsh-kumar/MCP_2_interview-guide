# MCP Deep Practice — Learning Map

> Protocol target: `2026-07-28`
> SDK baseline: `mcp==2.0.0`
> Last updated: 2026-08-19

This is the master checklist. Work through lessons in order.
Tick boxes as you complete each stage.

**Mastery Levels**

| Level | Meaning |
|---|---|
| L1 | Recognize — can identify the concept |
| L2 | Explain — can describe it accurately |
| L3 | Implement — can write working code |
| L4 | Debug — can diagnose failures |
| L5 | Design — can reason about trade-offs and architect solutions |

Target for Lessons 00–03: **L4**.
Target for Lessons 04–08: **L4 / L5**.

---

## Phase 0 — Foundation

- [ ] Environment installed and `doctor.py` reports clean
- [ ] All pinned SDK versions confirmed
- [ ] In-memory MCPServer + Client smoke test passing
- [ ] Documentation reviewed

---

## Phase 1 — MCP Fundamentals (Lessons 00–08)

### Lesson 00 — Protocol Foundations
- [ ] Read concepts (`concepts.md`)
- [ ] Run demo (`demo.py`)
- [ ] Explain mental model (Host, Client, Server, Model, External System)
- [ ] Complete modify exercise (`exercise.py` scenario evaluations)
- [ ] Complete debugging exercise (anti-pattern critique)
- [ ] Build from scratch / design challenge (`challenge.md`)
- [ ] Pass tests (`test_exercise.py`)
- [ ] Answer interview questions (`questions.md`)
- [ ] Target Mastery: **L4**

### Lesson 01 — JSON-RPC 2.0
- [ ] Read concepts (`concepts.md`)
- [ ] Run demo (`demo.py`)
- [ ] Explain message types (Request, Response, Notification, Error codes)
- [ ] Complete modify exercise (`validate_jsonrpc_message`)
- [ ] Complete debugging exercise (identify malformed wire payloads)
- [ ] Build from scratch (`EducationalJsonRpcDispatcher`)
- [ ] Pass tests (`test_exercise.py`)
- [ ] Answer interview questions (`questions.md`)
- [ ] Target Mastery: **L4**

### Lesson 02 — MCP Architecture
- [ ] Read concepts (`concepts.md`)
- [ ] Run demo (`demo.py`)
- [ ] Explain architecture topologies (stdio, HTTP, multi-server aggregation)
- [ ] Complete modify exercise (`analyze_credential_ownership`)
- [ ] Complete debugging exercise (failure isolation and broken servers)
- [ ] Build from scratch (`trace_tool_call_lifecycle`)
- [ ] Pass tests (`test_exercise.py`)
- [ ] Answer interview questions (`questions.md`)
- [ ] Target Mastery: **L4**

### Lesson 03 — Python SDK v2
- [ ] Read concepts (`concepts.md`)
- [ ] Run demo (`demo.py`)
- [ ] Explain SDK v2 primitives (`MCPServer`, `Client`, `ClientSession`, `Context`)
- [ ] Complete modify exercise (fix broken tool, implement resource, complete prompt)
- [ ] Complete debugging exercise (type mismatches on `list_tools().tools`)
- [ ] Build from scratch (`challenge.md` low-level memory streams)
- [ ] Pass tests (`test_exercise.py`)
- [ ] Answer interview questions (`questions.md`)
- [ ] Target Mastery: **L4**

### Lesson 04 — Tools
- [ ] Read concepts (`concepts.md`)
- [ ] Run demo (`demo.py`)
- [ ] Explain tool design (granularity, discoverability, idempotency, side effects)
- [ ] Complete modify exercise (`assign_ticket` tool implementation)
- [ ] Complete debugging exercise (`classify_tool_safety`)
- [ ] Build from scratch (`challenge.md` god-tool decomposition)
- [ ] Pass tests (`test_exercise.py`)
- [ ] Answer interview questions (`questions.md`)
- [ ] Target Mastery: **L4 / L5**

### Lesson 05 — Resources
- [ ] Read concepts (`concepts.md`)
- [ ] Run demo (`demo.py`)
- [ ] Explain resources vs tools vs prompts (URI templates, MIME types, static vs dynamic)
- [ ] Complete modify exercise (implement config and metric resource templates)
- [ ] Complete debugging exercise (handle unknown URIs and missing data)
- [ ] Build from scratch (`classify_capability` for 14 scenarios)
- [ ] Pass tests (`test_exercise.py`)
- [ ] Answer interview questions (`questions.md`)
- [ ] Target Mastery: **L4 / L5**

### Lesson 06 — Prompts
- [ ] Read concepts (`concepts.md`)
- [ ] Run demo (`demo.py`)
- [ ] Explain prompts (workflow templates, host-controlled invocation, arguments)
- [ ] Complete modify exercise (`explain_architecture` prompt)
- [ ] Complete debugging exercise (argument validation and prompt message roles)
- [ ] Build from scratch (`decompose_security_workflow`)
- [ ] Pass tests (`test_exercise.py`)
- [ ] Answer interview questions (`questions.md`)
- [ ] Target Mastery: **L4 / L5**

### Lesson 07 — Content & Schemas
- [ ] Read concepts (`concepts.md`)
- [ ] Run demo (`demo.py`)
- [ ] Explain schema contracts (Pydantic v2, JSON Schema, Content blocks, ambiguity resistance)
- [ ] Complete modify exercise (`create_change_request` with nested models and bounds)
- [ ] Complete debugging exercise (failure experiments on enums, bounds, and missing fields)
- [ ] Build from scratch (`challenge.md` cloud cluster provisioning schema)
- [ ] Pass tests (`test_exercise.py`)
- [ ] Answer interview questions (`questions.md`)
- [ ] Target Mastery: **L4 / L5**

### Lesson 08 — stdio Transport
- [ ] Read concepts (`concepts.md`)
- [ ] Run demo (`demo.py`)
- [ ] Explain stdio process mechanics (file descriptors, anonymous pipes, stdout vs stderr)
- [ ] Complete modify exercise (`parse_stdio_line` stream parser)
- [ ] Complete debugging exercise (diagnose and eliminate stdout pollution)
- [ ] Build from scratch (`create_exercise_stdio_server` with stderr logging)
- [ ] Pass tests (`test_exercise.py`)
- [ ] Answer interview questions (`questions.md`)
- [ ] Target Mastery: **L4 / L5**

---

## Phase 2 — Modern MCP 2026-07-28 (Lessons 09–13)
*(To be implemented in Phase 2)*

### Lesson 09 — Streamable HTTP
### Lesson 10 — Stateless MCP ⭐ MODERN MCP
### Lesson 11 — Discovery & Versioning
### Lesson 12 — Multi Round-Trip Requests (MRTR)
### Lesson 13 — Subscriptions & Notifications
