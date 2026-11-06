# MCP Deep Practice Lab

A self-contained learning workspace for understanding Model Context Protocol through lessons, demos, exercises, reference solutions, and tests.

**Status:** foundational teaching materials for lessons 00–08 are present. Later HTTP, security, deployment, extension, and capstone phases are planned.

## Start here

The actual workspace is [mcp_deep_practice](mcp_deep_practice). Run its commands from that directory.

```bash
git clone https://github.com/Nitsh-kumar/MCP_2_interview-guide.git
cd MCP_2_interview-guide/mcp_deep_practice
uv sync --locked
uv run python scripts/doctor.py
uv run python scripts/run_lesson.py 00
```

Python 3.12+ is declared. Read [pyproject.toml](mcp_deep_practice/pyproject.toml) and the lockfile for the repository's dependency baseline. Package availability and SDK/protocol claims still need authoritative compatibility verification.

## Lesson map

| Lessons | Topic |
| --- | --- |
| 00–02 | Protocol foundations, JSON-RPC, and MCP architecture |
| 03 | Python SDK examples |
| 04–06 | Tools, resources, and prompts |
| 07–08 | Content/schema handling and stdio transport |

Each lesson includes explanatory material, a demo, intentional learner scaffolding, reference solutions, and exercise tests. TODOs in learner exercises are part of the curriculum.

## Verification

From `mcp_deep_practice/`:

```bash
uv run pytest tests/phase0 -v
uv run pytest tests/phase1 -v
```

These check the implemented foundation/curriculum/reference material. Exercise-local tests can fail until the learner implements the exercise.

The existing `verify_all.py` defaults to foundation checks. Its `--phase all` currently covers foundation/fundamentals, not the future roadmap; missing phase paths can return success without running tests. Do not interpret that output as verification of the whole advertised curriculum.

## Design choices

Deterministic fake-model infrastructure lets learners inspect protocol behavior without paying for model calls. Separate reference solutions preserve the exercise experience. The lab is a teaching environment, not a production MCP deployment.

## Further reading

- [Workspace guide](mcp_deep_practice/README.md)
- [Learning map](mcp_deep_practice/docs/learning_map.md)
- [Version matrix](mcp_deep_practice/docs/version_matrix.md)
- [Security notes](mcp_deep_practice/docs/security_model.md)

The SDK/version matrix has inconsistencies with some example imports. Resolve those before using the notes as authoritative interview guidance.

See [project status](docs/PROJECT_STATUS.md).

## Validation

This documentation was checked against repository files on 13 October 2026. Notebooks, application runs, refreshes, and test suites were not executed during this documentation pass. Saved outputs are historical evidence, not a fresh run.
