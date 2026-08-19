# Challenge: Peeling Back the High-Level `Client` Facade

## Objective

Connect to an `MCPServer` using the low-level `ClientSession` and in-memory streams (`create_client_server_memory_streams`) to understand what the high-level `Client` facade abstracts.

---

## Background

In SDK v1, developers had to manually set up anyio streams, initialize client and server sessions, call `initialize()`, send notifications, and handle cancellation.

In SDK v2 (`mcp==2.0.0`), `Client(server)` handles the in-memory stream lifecycle, protocol version negotiation (`2026-07-28`), and session binding automatically.

---

## The Challenge Task

1. Study how `create_client_server_memory_streams()` creates paired anyio streams.
2. Observe how `ClientSession` wraps `(read_stream, write_stream)`.
3. Explain the responsibilities `Client(server)` takes care of behind the scenes:
   - Establishing memory pipes without network sockets
   - Managing `async with` context entry and graceful stream shutdown
   - Mapping return types to typed result dataclasses (`ListToolsResult`, `CallToolResult`)
   - Managing protocol handshake and capability validation
