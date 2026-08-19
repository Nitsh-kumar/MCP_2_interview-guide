# Challenge: Decomposing a Monolithic Assistant Workflow

## Objective

Take an oversized, monolithic "do-everything" tool and decompose it into the canonical MCP triad: Resource + Prompt + Tool.

---

## The Monolithic Antipattern

```python
@server.tool()
def generate_and_apply_pull_request(repo: str, branch: str, instructions: str) -> str:
    """Read repo code, design architectural changes, create commits, and push PR."""
    # 1. Fetches code from GitHub
    # 2. Generates LLM prompt internally
    # 3. Invokes another LLM sub-call
    # 4. Writes git commits and pushes branch
    ...
```

---

## Your Decomposition Challenge

1. **Identify the 3 Distinct Responsibilities**:
   - **Resource**: What read-only repository context should be exposed as URI resources (e.g. `repo://{repo_name}/branches/{branch}`)?
   - **Prompt**: What reusable review/generation prompt template should be advertised to the User/Host (e.g. `generate_pr_description`)?
   - **Tool**: What granular write operations should be exposed (e.g. `create_git_commit`, `open_pull_request`)?
2. **Defend the Architectural Split**:
   - How does this split give the human developer control at each milestone?
   - Why does keeping LLM sub-calls out of the MCP server improve observability and predictability?
