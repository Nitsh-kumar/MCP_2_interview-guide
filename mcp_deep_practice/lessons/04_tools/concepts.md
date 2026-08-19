# Concepts: Tools & Capability Engineering

## 1. Anatomy of an MCP Tool

In the Model Context Protocol, a **Tool** is a callable capability advertised by the server.

Every tool has:
1. **`name`**: Unique identifier (e.g. `get_ticket`, `create_pull_request`).
2. **`description`**: Human/LLM-readable explanation of when and how to use the tool.
3. **`inputSchema`**: JSON Schema describing argument types, required fields, constraints, and descriptions.
4. **Execution Handler**: A function that accepts arguments conforming to `inputSchema` and returns a `CallToolResult` containing content blocks (typically `TextContent`).

---

## 2. The Monolithic Tool Anti-Pattern vs. Fine-Grained Design

### The Anti-Pattern: "God Tools"
```python
# DANGEROUS / ANTI-PATTERN
@server.tool()
def execute(action: str, payload: dict) -> dict:
    """Execute any action in the system."""
    ...
```

Why this fails catastrophically in production:
1. **Schema Opacity**: The `inputSchema` only says `payload: object`. The LLM has no schema documentation for what fields `payload` needs for action `"close_ticket"` vs `"create_invoice"`.
2. **Authorization Impasse**: The Host cannot enforce least-privilege security. It cannot permit `read` operations while blocking `delete` operations because both pass through `execute()`.
3. **Audit Blindness**: Logs only record `execute()`, obscuring what the agent actually attempted.
4. **High Hallucination Rate**: LLMs perform drastically worse when guessing dynamic dictionary structures compared to validated, typed parameters.

---

### The Best Practice: Fine-Grained, Purpose-Built Tools
```python
# RECOMMENDED / ROBUST
@server.tool()
def get_ticket(ticket_id: str) -> dict:
    """Fetch complete ticket details by ID."""
    ...

@server.tool()
def change_ticket_status(ticket_id: str, new_status: str) -> dict:
    """Transition ticket status (e.g., 'in_progress', 'resolved')."""
    ...
```

Benefits:
- Clear, distinct descriptions and self-documenting JSON Schemas.
- Independent permission policies (Host can prompt for approval on `change_ticket_status` while auto-approving `get_ticket`).
- Safe retry policies (Idempotent read tools can be safely retried automatically on network drops).

---

## 3. Reliability & Safety Taxonomy for Tools

| Category | Definition | Retry Policy | Approval Policy | Example |
|---|---|---|---|---|
| **Read-Only / Pure** | No side effects on external state. | Safe to retry infinitely. | Auto-approved. | `get_ticket`, `search_logs` |
| **Idempotent Write** | Produces side effects, but executing multiple times has the same outcome. | Safe to retry if timeout occurs. | Prompt or rule-based. | `set_user_status(active=False)`, `upload_file(path, content)` |
| **Non-Idempotent Write** | Executing twice creates duplicate records or double charges. | **NEVER** auto-retry blindly. | Mandatory confirmation. | `charge_credit_card(amount)`, `post_slack_message()` |
| **Destructive** | Irreversible data loss or infrastructure teardown. | Manual intervention only. | Multi-factor confirmation. | `drop_database()`, `delete_repo()` |

---

## 4. Proper Error Reporting in Tools

When a tool fails due to business validation (e.g. invalid ticket ID):
- Return a structured result with `is_error=True` or an explanatory string.
- Do **NOT** raise an unhandled exception that crashes the server transport.
- Make the error message actionable so the LLM can self-correct (e.g. `"Error: ticket_id 'T-999' not found. Available IDs: T-101, T-102"`).
