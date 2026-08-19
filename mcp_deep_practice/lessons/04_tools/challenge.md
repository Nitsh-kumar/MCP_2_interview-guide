# Challenge: Deconstructing the "God Tool" Anti-Pattern

## Objective

Redesign a dangerous monolithic tool API into a secure, discoverable, and fine-grained MCP tool surface.

---

## The Legacy Monolithic Surface

A legacy service exposes a single endpoint to an LLM:

```python
@server.tool()
def execute_database_operation(action: str, query_or_payload: str) -> str:
    """Execute raw SQL queries or maintenance tasks on the production database."""
    if action == "raw_sql":
        return db.execute_raw(query_or_payload)
    elif action == "truncate_table":
        return db.truncate(query_or_payload)
    elif action == "export_csv":
        return db.export(query_or_payload)
    raise ValueError(f"Unknown action: {action}")
```

---

## The Redesign Task

1. **Decompose into Distinct MCP Tools**:
   - `search_table_records(table_name: str, filters: dict, limit: int = 50)`
   - `get_table_schema(table_name: str)`
   - `request_table_export(table_name: str, format: str)`
2. **Explain Why Truncate Should NOT Be an Automatic Tool**:
   - Explain why destructive operations like `truncate` or `drop` should either not exist in an MCP catalog or require explicit human-in-the-loop approvals.
3. **Draft Strong Pydantic Schemas**:
   - Show how parameterized inputs prevent SQL injection vulnerabilities from prompt-injected LLM outputs.
