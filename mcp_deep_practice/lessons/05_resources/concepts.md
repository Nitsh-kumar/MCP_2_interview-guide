# Concepts: Resources & URI Templates

## 1. What is an MCP Resource?

In the Model Context Protocol, a **Resource** represents passive, read-only data that can be attached as context to a conversation or read by an AI host.

Key Characteristics of Resources:
- **Addressable by URI**: Every resource has a unique URI (e.g. `docs://architecture`, `postgres://tables/users`, `file:///workspace/README.md`).
- **Read-Only / Side-Effect Free**: Reading a resource MUST NOT alter external state or trigger write actions.
- **MIME-Typed**: Every resource specifies its content type (e.g. `text/plain`, `application/json`, `text/markdown`).
- **Discovery**: Clients discover resources via `resources/list` (for fixed URIs) and `resources/templates/list` (for parameterized URI patterns).

---

## 2. Static Resources vs. Dynamic Resource Templates

### Static Resource (Fixed URI)
Fixed context files that always exist at a known URI:
```python
@server.resource("docs://architecture")
def get_architecture() -> str:
    """Static architecture documentation."""
    return "# System Architecture Guide\n..."
```

### Dynamic Resource Template (RFC 6570 URI Pattern)
Parameterized templates for reading individual entities by ID or path:
```python
@server.resource("tickets://{ticket_id}")
def get_ticket_resource(ticket_id: str) -> str:
    """Read ticket details as a resource by URI."""
    ticket = db.find(ticket_id)
    return json.dumps(ticket)
```

---

## 3. Decision Framework: Tool vs. Resource vs. Prompt

When designing an MCP server, use this decision tree:

```
Is it an instruction template for the LLM?
 ├─ YES ──> MCP PROMPT (e.g. "review_code", "summarize_incident")
 └─ NO
     │
     Is it a passive read with a predictable, direct URI?
      ├─ YES ──> MCP RESOURCE (e.g. "file://...", "docs://...", "config://...")
      └─ NO
          │
          Does it require active computation, parameter searching, or cause side effects?
           └─ YES ──> MCP TOOL (e.g. "search_tickets", "send_email", "calculate_tax")
```

---

## 4. Analysis of 14 Real-World Capabilities

| Scenario | Classification | Architectural Justification |
|---|---|---|
| 1. Latest invoice PDF | **Resource** | A document with a known URI (`invoices://latest.pdf`) and standard MIME type (`application/pdf`). |
| 2. Search invoices | **Tool** | Search requires query parameters, sorting, pagination, and multi-field filters. |
| 3. Retrieve invoice by known URI | **Resource** | Direct lookup by known URI (`invoices://{invoice_id}`). |
| 4. Company coding guidelines | **Resource** | Static reference documentation (`docs://standards/coding-style.md`). |
| 5. Database schema | **Resource** | Static/cached structural metadata describing tables (`postgres://schema/public`). |
| 6. Run database migration | **Tool** | Destructive write action that modifies database state. |
| 7. Project README | **Resource** | Static repository file (`file:///workspace/README.md`). |
| 8. Customer profile | **Resource** | Direct entity lookup by customer ID (`crm://customers/{customer_id}`). |
| 9. Generate incident summary | **Prompt** | Templated instruction guide directing the LLM how to format an incident postmortem. |
| 10. Current system time | **Tool** (or Resource) | Dynamic computation evaluated at invocation time. |
| 11. Execute SQL query | **Tool** | Active parameterized computation against a database engine. |
| 12. Template for PR review | **Prompt** | Conversational workflow template (`review_pull_request`). |
| 13. Live sensor telemetry | **Resource** | Read-only state snapshot (`telemetry://sensors/{sensor_id}`). |
| 14. Restart service | **Tool** | Active write action with operational side effects. |
