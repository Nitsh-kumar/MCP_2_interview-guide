# Challenge: Enterprise Multi-Server Architecture Design

## Objective

Design a production-grade multi-server MCP architecture for an enterprise developer workspace.

---

## The Scenario

You are designing the MCP subsystem for a next-generation AI IDE. The IDE integrates four distinct servers:
1. **Local Filesystem MCP** (stdio child process, restricted to project root)
2. **GitHub Enterprise MCP** (remote Streamable HTTP, OAuth 2.0 PKCE flow)
3. **Internal Documentation MCP** (company intranet wiki, vector search, HTTP + API Key)
4. **Postgres Read-Only MCP** (local Docker container over stdio bridge)

---

## Questions to Answer in Your Architecture Document

1. **Client Ownership & Lifecycle**:
   - Does the IDE spawn one MCP Client or four separate MCP Clients?
   - How does the IDE maintain tool discovery when one server starts up after a 5-second delay?

2. **Credential Management**:
   - Where are the GitHub OAuth token and Wiki API Key stored?
   - Are credentials ever visible in the LLM prompt context?

3. **Tool Namespace Collisions**:
   - If both the Filesystem server and the GitHub server expose a tool named `search_files`, how does the Host resolve this collision before presenting schemas to the LLM?

4. **Failure Domains & Resilience**:
   - If the Internal Documentation MCP server experiences a 504 Gateway Timeout, what happens to the user query?
   - How does the Host prevent one slow server from freezing the entire IDE session?
