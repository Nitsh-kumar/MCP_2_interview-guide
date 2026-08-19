# Concepts: Python SDK v2 (`MCPServer` & `Client`)

## 1. The Modern SDK v2 Architecture (`mcp==2.0.0`)

In SDK v2, the primary server abstraction is `MCPServer`, and the primary client abstraction is `Client`.

```python
# Modern SDK v2 Imports (Verified Baseline)
from mcp import Client, ClientSession
from mcp.server import MCPServer
from mcp.server.context import Context
```

### Core Abstractions:
1. **`MCPServer`**: High-level server instance supporting decorator-based registration of tools, resources, and prompts. Handles JSON-RPC dispatch, schema generation, and routing.
2. **`Client`**: High-level asynchronous client facade. Can connect directly to an `MCPServer` instance in memory (`Client(server)`) or over stdio/HTTP transports.
3. **`ClientSession`**: Low-level session engine accessible via `client.session`. Handles raw protocol message exchange.
4. **`Context`**: Request context injected into tools when needed (accessed via `from mcp.server.context import Context`).

---

## 2. Decorators & Capability Registration

### Tools: `@server.tool()`
Tools represent callable actions that can produce side effects or return dynamic computations:

```python
server = MCPServer("dev-tools")

@server.tool()
def calculate_area(length: float, width: float) -> float:
    """Calculate the area of a rectangle."""
    return length * width
```

### Resources: `@server.resource("uri://...")`
Resources represent read-only context data or documentation:

```python
@server.resource("docs://architecture")
def get_architecture_doc() -> str:
    """Returns static architecture guide."""
    return "# System Architecture\n..."
```

### Prompts: `@server.prompt()`
Prompts represent reusable conversational workflows and templates:

```python
@server.prompt()
def code_review(code: str, language: str = "python") -> str:
    """Template for performing a structured code review."""
    return f"Please review this {language} code for security and performance:\n```\n{code}\n```"
```

---

## 3. High-Level In-Memory Client Usage

Connecting to a server in memory requires zero subprocess or socket configuration:

```python
async with Client(server) as client:
    # 1. Verify modern protocol version
    assert client.protocol_version == "2026-07-28"

    # 2. Access low-level session
    assert isinstance(client.session, ClientSession)

    # 3. List tools (returns ListToolsResult)
    tools_result = await client.list_tools()
    for tool in tools_result.tools:
        print(tool.name, tool.description)

    # 4. Call tool (returns CallToolResult)
    call_result = await client.call_tool("calculate_area", {"length": 5.0, "width": 4.0})
    for content_block in call_result.content:
        print(content_block.text)
```

---

## 4. Crucial Return Types & Structure

| Method | Return Object | Contents Accessor |
|---|---|---|
| `await client.list_tools()` | `ListToolsResult` | `result.tools` (list of `Tool`) |
| `await client.call_tool(name, args)` | `CallToolResult` | `result.content` (list of `TextContent`) |
| `await client.list_resources()` | `ListResourcesResult` | `result.resources` (list of `Resource`) |
| `await client.read_resource(uri)` | `ReadResourceResult` | `result.contents` (list of `TextResourceContents`) |
| `await client.list_prompts()` | `ListPromptsResult` | `result.prompts` (list of `Prompt`) |
| `await client.get_prompt(name, args)` | `GetPromptResult` | `result.messages` (list of `PromptMessage`) |

> [!WARNING]
> Do NOT iterate directly over `await client.list_tools()`. You must access `.tools`.
