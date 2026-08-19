# Conceptual & Interview Questions: Protocol Foundations

### Q1 [Factual]: What core problem does MCP solve that OpenAPI does not?
**Answer Rubric:**
- OpenAPI defines HTTP API schemas (endpoints, HTTP verbs, path params) for REST services.
- MCP is a state-aware protocol that standardizes how AI hosts dynamically discover, inspect, and invoke capabilities (Tools, Resources, Prompts) across local (stdio) and remote (Streamable HTTP) transports.
- MCP abstracts away provider-specific tool schemas and provides unified resource URIs and prompt templates.

---

### Q2 [Reasoning]: Why is the analogy "MCP is USB-C for AI" potentially dangerous if taken too literally?
**Answer Rubric:**
- USB-C is a physical hardware standard with fixed pinouts and deterministic voltage/packet delivery.
- In MCP:
  1. Context window constraints mean exposing too many tools degrades LLM accuracy.
  2. Tool selection is probabilistic, not deterministic.
  3. Untrusted tool output can cause indirect prompt injection, whereas USB hardware does not parse natural language instructions.

---

### Q3 [Reasoning]: What is the difference between an MCP Client and an MCP Server?
**Answer Rubric:**
- **MCP Client**: Initiates connections, discovers capabilities, formats tool/resource requests from the Host/LLM, and handles responses. Resides in the Host (e.g., Claude Desktop, IDE).
- **MCP Server**: Listens for connections, exposes tool schemas/resource templates/prompts, and executes domain logic against backend services or filesystems upon receiving requests.

---

### Q4 [Architecture]: Why should an LLM never open raw MCP sockets or directly execute OS commands?
**Answer Rubric:**
- Security and isolation: The LLM is a non-deterministic inference engine. Giving it direct socket or execution access creates catastrophic vulnerability to prompt injection.
- Protocol boundary: The Host and MCP Client act as the security boundary, validating schemas, asking for user confirmation when appropriate, and enforcing sandbox boundaries.

---

### Q5 [Debugging / Architecture]: A team proposes converting all internal microservices from gRPC to MCP to make them "AI-ready". How do you evaluate this proposal?
**Answer Rubric:**
- Reject full migration. gRPC is optimized for low-latency, binary-serialized service-to-service communication.
- Instead, adopt a gateway / adapter pattern: keep internal services on gRPC/REST and build focused MCP Servers that expose only the curated subset of capabilities an AI assistant actually needs to call.

---

### Q6 [Factual]: What are the 3 layers of an MCP interaction?
**Answer Rubric:**
- Layer 1: Protocol & Wire Layer (JSON-RPC 2.0 messages, framing, transport).
- Layer 2: SDK Abstraction Layer (Python SDK `mcp==2.0.0`, MCPServer, Client).
- Layer 3: Application Layer (Host agent loop, domain logic, external databases).
