# Lesson Metadata

- Protocol revision: 2026-07-28
- SDK baseline: mcp==2.0.0
- Feature status: FOUNDATION
- SDK support: NOT_APPLICABLE
- Verified against: mcp==2.0.0, mcp-types==2.0.0
- Last verified: 2026-08-19

---

# Lesson 00: Protocol Foundations

## 1. Learning Objectives

By the end of this lesson, you will be able to:
1. Define what a protocol is in distributed systems and why Model Context Protocol (MCP) was created.
2. Explain the fundamental roles: Host, Client, Server, Model, and External Systems.
3. Compare MCP with alternatives: REST APIs, OpenAPI specs, direct function calling, provider-native tool schemas, Agent-to-Agent (A2A) protocols, and custom plugin architectures.
4. Critically analyze common industry myths (e.g., "MCP is USB-C for AI", "MCP replaces REST", "MCP servers are autonomous agents").
5. Articulate the three distinct layers of any MCP interaction: Protocol, SDK, and Application.
6. Evaluate real-world integration architectures to determine when MCP adds value versus when it adds unnecessary overhead.

---

## 2. The Three-Layer Mental Model

Every MCP interaction operates across three distinct conceptual layers:

```
┌─────────────────────────────────────────────────────────────────────────┐
│ LAYER 3: Application & Domain Layer                                     │
│ Business logic, database queries, API auth, agent reasoning loops       │
├─────────────────────────────────────────────────────────────────────────┤
│ LAYER 2: SDK Abstraction Layer                                          │
│ Python types (MCPServer, Client, Context), Pydantic schemas, routing     │
├─────────────────────────────────────────────────────────────────────────┤
│ LAYER 1: Protocol & Wire Layer                                          │
│ JSON-RPC 2.0 messages, framing, transport (stdio / Streamable HTTP)     │
└─────────────────────────────────────────────────────────────────────────┘
```

- **Layer 1 (Protocol)**: What actually crosses the transport boundary. Standardized JSON-RPC 2.0 payloads defining `tools/call`, `resources/read`, `prompts/get`, and metadata blocks.
- **Layer 2 (SDK)**: High-level language libraries (`mcp==2.0.0`) translating idiomatic language constructs into Layer 1 wire messages and vice-versa.
- **Layer 3 (Application)**: Your actual business logic, database connectors, or agent workflows that consume tools and resources.

---

## 3. Lesson Progression

- **Stage A (Observe)**: Run `uv run python lessons/00_protocol_foundations/demo.py` to trace host-client-server boundaries without framework magic.
- **Stage B (Explain)**: Read `concepts.md` and answer the conceptual check questions in `questions.md`.
- **Stage C (Modify)**: Open `exercise.py` and implement the scenario classification and trade-off defense system.
- **Stage D (Debug)**: Diagnose architectural anti-patterns where MCP is misapplied.
- **Stage E (Build / Challenge)**: Read `challenge.md` and design an architecture where MCP provides zero or negative value.

---

## 4. Verification

Run the lesson tests:
```bash
uv run pytest lessons/00_protocol_foundations/test_exercise.py -v
```
