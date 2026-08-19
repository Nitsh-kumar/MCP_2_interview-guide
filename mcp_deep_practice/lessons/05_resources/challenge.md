# Challenge: Refactoring Read Tools to URI Resources

## Objective

Refactor a poorly designed server that abuses MCP tools for passive data reading into clean, standard MCP Resources with URI schemes.

---

## The Flawed Legacy Tool Surface

```python
# CODE SMELL: Exposing read-only file/config lookups as active tools
@server.tool()
def get_readme_file() -> str:
    return open("README.md").read()

@server.tool()
def get_config_value(section: str, key: str) -> str:
    return config_parser.get(section, key)

@server.tool()
def get_user_profile(user_id: str) -> str:
    return json.dumps(user_db.get(user_id))
```

---

## The Refactoring Plan

1. **Design URI Schemes**:
   - `file:///workspace/README.md` (MIME: `text/markdown`)
   - `config://app/{section}/{key}` (MIME: `text/plain` or `application/json`)
   - `users://profiles/{user_id}` (MIME: `application/json`)
2. **Implement as `@server.resource()`**:
   - Convert static reads to fixed URI resources.
   - Convert parameterized reads to URI templates.
3. **Explain the Advantages**:
   - Why do Resources avoid bloating the LLM's active tool schema selection?
   - How can Hosts automatically pre-fetch or subscribe to resources for context injection without model tool-calling turns?
