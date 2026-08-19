# MCP Deep Practice — Terminology Glossary

> Authoritative definitions for terms used throughout this curriculum.
> Protocol target: `2026-07-28` | SDK: `mcp==2.0.0`
> Last verified: 2026-08-19

---

## MCP Architecture Components

**Host**
The application running the agent loop. Responsible for connecting to one or more MCP servers, routing tool calls through the model, and presenting results to the user. Examples: Claude Desktop, VS Code Copilot, a custom Python agent. The host owns the human interface and the agent lifecycle.

**Client**
An MCP client connection managed by the host. Each server gets its own client connection. In Python SDK v2, the high-level `Client` class manages the connection lifecycle; `client.session` provides access to the underlying `ClientSession` for low-level operations.

**ClientSession**
The low-level SDK object representing a single MCP protocol session. In SDK v2, this is the escape hatch for direct protocol access: manual request/response control, MRTR state management, transport-level testing. Available via `client.session`. NOT obsolete or removed.

**Server**
An MCP server exposes tools, resources, and/or prompts to clients. In Python SDK v2, implemented using `MCPServer`. A server does not directly interact with the model — it responds to client requests.

**MCPServer**
The Python SDK v2 server class. (The SDK v1 class was named `FastMCP`; it was renamed to `MCPServer` in SDK v2. Unrelated to the third-party `fastmcp` package.)

**Model**
A language model (LLM). The model decides which tools to call based on the user's request and the available tool catalog. The model does NOT directly open network connections to MCP servers — it requests tool calls through the host/client infrastructure.

**External System**
The actual business system a tool interacts with: a database, an API, a filesystem. The MCP server acts as an adapter between the protocol and the external system.

**Transport**
The communication mechanism between client and server. MCP 2026-07-28 defines two core transports: `stdio` (local, subprocess-based) and `Streamable HTTP` (remote, POST-based).

---

## Protocol Concepts

**JSON-RPC 2.0**
The underlying message format for MCP. Every MCP operation is a JSON-RPC request, response, or notification. Understanding JSON-RPC is prerequisite to understanding MCP.

**Request**
A JSON-RPC message with an `id`, `method`, and optional `params`. Expects a corresponding response.

**Response**
A JSON-RPC message containing a `result` (success) or `error` (failure), matching an outstanding request by `id`.

**Notification**
A JSON-RPC message with a `method` but no `id`. No response is expected. Used for events like tool catalog changes.

**Method**
The operation name in a JSON-RPC request, e.g. `tools/call`, `resources/read`, `server/discover`.

**Stateless Request (MODERN MCP)**
A self-contained request carrying all necessary protocol metadata in its `_meta` block and HTTP headers. No prior handshake required. Any server replica can handle it.

**`_meta` block**
A reserved field in JSON-RPC `params` carrying protocol-level metadata: `io.modelcontextprotocol/protocolVersion`, `io.modelcontextprotocol/clientInfo`, `io.modelcontextprotocol/clientCapabilities`.

**MCP-Protocol-Version header**
HTTP header declaring the protocol version of a request. Must match the version in `_meta`. Mismatch → HTTP 400.

**Mcp-Method header**
HTTP header carrying the JSON-RPC method name. Enables gateways to route and authorize requests without parsing the JSON body.

**Mcp-Name header**
HTTP header carrying the tool/resource/prompt name. Enables fine-grained gateway authorization rules.

---

## Tools, Resources, Prompts

**Tool**
An executable operation with defined input/output schemas. May have side effects. The primary way servers expose capabilities to LLMs. Think: function call.

**Resource**
A readable data item identified by a URI. No side effects. Analogous to a GET request. The server makes data available; the client or model decides what to read.

**Prompt**
A reusable template for constructing LLM messages, parameterized by arguments. Separate from ordinary LLM prompts — these are server-defined building blocks.

**Tool Schema**
A JSON Schema describing the tool's input parameters. Determines how the LLM structures its tool arguments. Schema quality directly affects LLM reliability.

**Resource URI**
A string identifier for a resource, e.g. `tickets://TKT-42`. URIs can be static or templated (`tickets://{ticket_id}`).

**Resource Template**
A URI pattern with named parameters, allowing a single resource handler to serve a family of resources.

---

## Modern MCP (2026-07-28) Specific

**server/discover**
A single stateless JSON-RPC method that returns the server's full capability set, tool catalog, resource catalog, and prompt catalog in one response. Replaces the legacy multi-step initialize + list sequence.

**CreateTaskResult**
The response type returned by a `tools/call` operation when the work is long-running and will be completed asynchronously. Fields: `resultType: "task"`, `taskId`, `status`, `ttlMs`, `pollIntervalMs`. Task creation is server-directed.

**MRTR (Multi Round-Trip Request)**
A protocol mechanism allowing a server to request additional user input mid-operation using `input_required`. The client pauses, collects the input, and resumes the original operation by including `inputResponses` and `request_state`.

**input_required**
The response type indicating the server needs more information from the user before continuing. Contains the question and schema for the expected input.

**request_state**
An opaque token representing the suspended server-side state for an MRTR operation. The client must include this when resuming.

**subscriptions/listen**
A long-lived POST-response stream (SSE body) over Streamable HTTP. The client receives invalidation notifications for resources, tool catalogs, etc. Notifications are hints — clients must revalidate state by re-reading resources. NOT a durable ordered event log.

**Stateless Protocol vs Stateless Application**
MCP 2026-07-28 has no protocol-level session. The application may still have state — but that state is managed via explicit application tokens (e.g., `cart_id`, `task_id`) passed as tool arguments, not via transport session affinity.

---

## Security Terms

**Confused Deputy**
An attack where a legitimate server is tricked into using its elevated permissions to perform an action on behalf of an attacker. Relevant to MCP when a server has broad permissions and accepts untrusted input.

**Prompt Injection**
An attack where malicious content in tool output or resource content causes an LLM to execute unintended actions. Particularly dangerous because tool results flow directly into the model's context.

**Tool Poisoning**
An attack where a malicious MCP server provides tool descriptions that manipulate model behavior in ways invisible to the user.

**SSRF (Server-Side Request Forgery)**
An attack where a tool is manipulated into making HTTP requests to unintended internal or external hosts.

**Token Passthrough**
An anti-pattern where an MCP server forwards an authorization token it received to another downstream service, bypassing proper scope validation at the server boundary.

---

## Reliability Terms

**Idempotency**
A property of an operation where executing it multiple times produces the same result as executing it once. Critical for retry safety on write tools.

**Idempotency Key**
A client-supplied unique identifier for an operation. The server deduplicates requests with the same key, preventing double execution on retry.

**Circuit Breaker**
A reliability pattern that stops calling a failing downstream service after a threshold of failures, giving it time to recover.

**Backpressure**
The mechanism by which a slow consumer signals a fast producer to slow down.

**Compensation (Saga Pattern)**
In a distributed saga, when one step fails, compensation means running a counter-operation to undo the effect of a previously successful step. This is NOT the same as a database rollback — the original step's side effects already occurred.

---

## SDK Terms

**FastMCP (SDK v1 class)**
The server class in MCP Python SDK v1. Renamed to `MCPServer` in SDK v2. Not to be confused with the separate third-party `fastmcp` package.

**httpx2**
The HTTP client library used by the official MCP Python SDK v2. Replaced `httpx`/`httpx-sse` from SDK v1. Use `import httpx2` for all SDK-adjacent HTTP code.

**`client.session`**
A property of the SDK v2 `Client` object that exposes the underlying `ClientSession` for low-level protocol access.
