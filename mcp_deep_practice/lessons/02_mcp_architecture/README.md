# Lesson Metadata

- Protocol revision: 2026-07-28
- SDK baseline: mcp==2.0.0
- Feature status: FOUNDATION
- SDK support: NOT_APPLICABLE
- Verified against: mcp==2.0.0, mcp-types==2.0.0
- Last verified: 2026-08-19

---

# Lesson 02: MCP Architecture & Trust Boundaries

## 1. Learning Objectives

By the end of this lesson, you will be able to:
1. Diagram and trace the end-to-end message flow: User $\rightarrow$ Host $\rightarrow$ Model $\rightarrow$ MCP Client $\rightarrow$ MCP Server $\rightarrow$ External System.
2. Clearly distinguish between the **Model boundary**, **Protocol boundary**, and **Trust boundary**.
3. Understand why the LLM does NOT directly open network connections or execute MCP socket calls.
4. Compare the 3 primary architectural deployment topologies:
   - Local Subprocess (stdio)
   - Remote Service (Streamable HTTP)
   - Multi-Server Host Aggregation
5. Identify where credentials, session state, tool discovery, and failure isolation reside in multi-server architectures.

---

## 2. The Three Layers in MCP Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│ LAYER 3: Application Orchestration                                      │
│ Host Agent Loop, UI, Approval Modals, Context Assembly, Secrets Store   │
├─────────────────────────────────────────────────────────────────────────┤
│ LAYER 2: SDK Client / Server Abstraction                                │
│ Transport Adapters, Session Management, Capability Negotiation          │
├─────────────────────────────────────────────────────────────────────────┤
│ LAYER 1: Transport & Wire Framing                                       │
│ Stdio OS Pipes / Streamable HTTP SSE connections                        │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Lesson Progression

- **Stage A (Observe)**: Run `uv run python lessons/02_mcp_architecture/demo.py` to trace end-to-end message lifecycles across local, remote, and multi-server topologies.
- **Stage B (Explain)**: Read `concepts.md` with detailed Mermaid architecture diagrams.
- **Stage C (Modify)**: In `exercise.py`, analyze incomplete architecture specifications and map trust boundaries.
- **Stage D (Debug)**: Diagnose failure propagation when one server fails in a multi-server setup.
- **Stage E (Build / Challenge)**: Complete `challenge.md` to design an enterprise IDE multi-server topology.

---

## 4. Verification

Run the lesson tests:
```bash
uv run pytest lessons/02_mcp_architecture/test_exercise.py -v
```
