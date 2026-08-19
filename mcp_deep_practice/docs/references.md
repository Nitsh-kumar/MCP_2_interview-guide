# References — MCP Deep Practice Lab

> Protocol target: `2026-07-28` | SDK: `mcp==2.0.0`
> Last verified: 2026-08-19
>
> Sources are categorized as AUTHORITATIVE, SUPPLEMENTARY, or LEGACY.
> Do not rely on uncategorized blog posts when an AUTHORITATIVE source exists.
> Summaries are original language. Large blocks of external documentation are not reproduced here.

---

## AUTHORITATIVE

These sources are the source of truth for protocol semantics and SDK behavior.

### MCP Specification — 2026-07-28

**URL:** https://modelcontextprotocol.io/specification/2026-07-28
**Description:** The definitive protocol specification. Defines message formats, methods, transports, authorization model, and extensions. Any protocol claim in this curriculum must be traceable to this document.
**Key sections:**
- Core protocol: JSON-RPC, methods, transports
- Authorization: OAuth 2.1 integration, token validation
- Extensions: Tasks, MCP Apps
- Streamable HTTP transport details

### MCP Extension Specifications

**Tasks Extension:** https://modelcontextprotocol.io/specification/2026-07-28/extensions/tasks
**MCP Apps Extension:** https://modelcontextprotocol.io/specification/2026-07-28/extensions/mcp-apps
**Description:** Official extension specifications defining server-directed task creation (`CreateTaskResult`), task management methods (`tasks/get`, `tasks/update`, `tasks/cancel`), and MCP App UI contracts.

### MCP Python SDK v2 — Official Repository

**URL:** https://github.com/modelcontextprotocol/python-sdk
**PyPI:** https://pypi.org/project/mcp/
**Installed version:** `mcp==2.0.0` (pinned baseline for this curriculum)
**Description:** The official Python SDK. Import paths, class names, and API signatures are verified against the installed package.

**Verified import paths (mcp==2.0.0):**
```
from mcp.server import MCPServer
from mcp import Client
from mcp import ClientSession
from mcp.server.context import Context
from mcp.server.stdio import stdio_server
from mcp.shared.memory import create_client_server_memory_streams
from mcp.types import ErrorData, Tool, Resource, Prompt
```

**SDK internal modules of interest:**
```
mcp.server.subscriptions    — subscriptions/listen infrastructure
mcp.server.elicitation      — MRTR elicitation helpers
mcp.server.request_state    — MRTR request state management
mcp.server.auth             — OAuth/Bearer auth integration
mcp.shared.memory           — in-memory test streams
```

### MCP Inspector

**URL:** https://github.com/modelcontextprotocol/inspector
**npm:** @modelcontextprotocol/inspector
**Node.js available:** v25.8.0 / npx 11.17.0 (verified on host)
**Description:** The official MCP testing and debugging tool. Provides CLI, Web UI, and TUI interfaces for inspecting MCP servers interactively. Used in Lesson 18.

**CLI smoke test command:**
```bash
npx @modelcontextprotocol/inspector --help
```

### MCP Python SDK v2 Documentation

**URL:** https://modelcontextprotocol.io/sdk/python
**Description:** Official SDK documentation for Python. Used alongside source inspection to verify API surface. Where documentation and source differ, source takes precedence.

---

## SUPPLEMENTARY

These sources provide useful context, teaching patterns, or supplementary exercises.
They are not authoritative for protocol semantics.

### Microsoft MCP for Beginners

**URL:** https://github.com/microsoft/mcp-for-beginners
**Description:** A beginner-oriented curriculum for MCP. Useful for additional exercises and alternative explanations. NOT used as architectural authority. Where it conflicts with the MCP 2026-07-28 specification, the specification wins.

---

## LEGACY

These sources describe older MCP behavior that is contrasted with modern MCP in the curriculum.
Marked `LEGACY MCP` wherever cited.

### MCP Specification — 2025-11-25

**URL:** https://modelcontextprotocol.io/specification/2025-11-25
**Description:** The previous major specification revision. Key differences from 2026-07-28 include: session-based initialization handshake, `Mcp-Session-Id`, HTTP GET SSE transport, `resources/subscribe`/`resources/unsubscribe`, and experimental Tasks with client-initiated `tasks/create`.

### MCP Specification — 2024-11-05

**URL:** https://modelcontextprotocol.io/specification/2024-11-05
**Description:** The original public specification. Very different architecture — useful only for understanding how MCP evolved.

### MCP Python SDK v1

**Historical package:** `mcp<2.0.0`
**Description:** Used `FastMCP` class (renamed `MCPServer` in v2), `ClientSession` manual lifecycle, `httpx`/`httpx-sse` transport. Relevant to Lesson 25 (v1 to v2 migration).

---

## Documentation Discrepancies Tracked

| Discrepancy | Specification says | SDK v2.0.0 behaves | Resolution |
|---|---|---|---|
| `Context` import path | Not specified | `from mcp.server.context import Context` | Use verified import path |
| In-memory test helper | Not specified | `create_client_server_memory_streams` in `mcp.shared.memory` | Use verified function name |
| Tasks extension | Defines `tasks/get`, `tasks/update`, `tasks/cancel` | No implementation in mcp==2.0.0 | Teach spec-level via educational fixture |
| `server/discover` | Defined in spec | Present as wire method; high-level SDK helper unconfirmed | Teach at wire level |

---

## Lesson-Specific Authoritative References (Phase 1)

### Lesson 00 — Protocol Foundations
- **MCP Architectural Overview:** https://modelcontextprotocol.io/introduction
- **Distributed Systems Protocol Design:** RFC 8259 (The JSON Data Interchange Format)

### Lesson 01 — JSON-RPC 2.0
- **JSON-RPC 2.0 Specification:** https://www.jsonrpc.org/specification (Official Standard)
- **JSON-RPC Error Codes:** Specification Section 5.1 (Standard Error Definitions)

### Lesson 02 — MCP Architecture
- **MCP Architecture & Core Roles:** https://modelcontextprotocol.io/specification/2026-07-28#architecture
- **Transport Topologies:** stdio OS pipe model and Streamable HTTP endpoint structure

### Lesson 03 — Python SDK v2
- **Official Python SDK v2 Repository:** https://github.com/modelcontextprotocol/python-sdk (`mcp==2.0.0`)
- **SDK Class Interfaces:** `MCPServer`, `Client`, `ClientSession`, `Context`

### Lesson 04 — Tools
- **MCP Tools Specification:** https://modelcontextprotocol.io/specification/2026-07-28#tools
- **JSON Schema Validation:** Draft 2020-12 / OpenAPI 3.1 Tool Calling Definitions

### Lesson 05 — Resources
- **MCP Resources Specification:** https://modelcontextprotocol.io/specification/2026-07-28#resources
- **URI Template Standard:** RFC 6570 (URI Template syntax for parameterized resources)

### Lesson 06 — Prompts
- **MCP Prompts Specification:** https://modelcontextprotocol.io/specification/2026-07-28#prompts

### Lesson 07 — Content & Schemas
- **MCP Content Block Types:** `TextContent`, `ImageContent`, `EmbeddedResource`
- **Pydantic v2 Schema Generation:** https://docs.pydantic.dev/latest/concepts/json_schema/

### Lesson 08 — stdio Transport
- **MCP stdio Transport Specification:** https://modelcontextprotocol.io/specification/2026-07-28#transports-stdio
- **OS Stream Mechanics:** POSIX Standard File Descriptors (0=stdin, 1=stdout, 2=stderr)

---

## Access Policy

All authoritative sources are accessed via official URLs.
Verification dates are recorded because MCP is evolving rapidly.
If more than 90 days have passed since the last verification date, re-verify before relying on SDK API claims.
