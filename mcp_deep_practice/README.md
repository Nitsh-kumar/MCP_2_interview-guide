# MCP Deep Practice Lab

> **Protocol target:** `2026-07-28`
> **SDK baseline:** `mcp==2.0.0` / `mcp-types==2.0.0`
> **Python:** `3.12+`
> **Phase:** Foundation (Phase 0)

---

## Purpose

This is a **learning repository**, not application source code.

After completing this curriculum you will be able to:

- Explain MCP without framework abstractions
- Reason about raw protocol messages
- Build MCP servers and clients from first principles
- Understand MCP Python SDK v2
- Distinguish modern MCP `2026-07-28` from legacy MCP
- Design tools, resources, and prompts correctly
- Build local (stdio) and remote (Streamable HTTP) servers
- Debug protocol problems
- Implement authorization safely
- Reason about MCP security threats
- Handle failures, retries, cancellation, concurrency, and idempotency
- Deploy and horizontally scale remote MCP servers
- Integrate MCP with agent frameworks
- Understand MCP Apps and the Tasks extension
- Migrate v1 MCP implementations to v2
- Evaluate whether MCP is appropriate for a use case
- Design production-grade enterprise MCP architectures

**This is not a collection of finished examples. It is a structured learning environment.**

---

## Critical Warnings

> **Do not skip the foundational lessons.** Lessons are deliberately progressive.
> Framework magic is the enemy of understanding. Resist the urge to jump to agent integration.

The following statements are **challenged and critiqued throughout this curriculum**:

| Simplification | Where it breaks down |
|---|---|
| "MCP is just USB-C for AI" | Lesson 00 |
| "MCP is just tool calling" | Lessons 00–04 |
| "MCP makes tools secure automatically" | Lesson 15 |
| "MCP replaces REST" | Lesson 00 |
| "Retries are always safe" | Lesson 17 |
| "Stateless MCP means no application state" | Lesson 10 |
| "MCP requires Claude" | Lesson 02 |

---

## Learning Progression

Every concept follows five stages:

```
Stage A — Observe   : Run a minimal working example
Stage B — Explain   : Answer protocol-level questions
Stage C — Modify    : Change an existing implementation
Stage D — Debug     : Diagnose an intentionally broken example
Stage E — Build     : Implement from requirements + tests only
```

Target mastery levels for core topics: **L5 — Design**

```
L1 Recognize  →  L2 Explain  →  L3 Implement  →  L4 Debug  →  L5 Design
```

---

## Quick Start

```bash
# Verify environment
uv run python scripts/doctor.py

# Navigate a lesson
uv run python scripts/run_lesson.py 00

# Run all phase-0 verification tests
uv run pytest tests/phase0 -v

# Run full test suite
uv run python scripts/verify_all.py
```

---

## Curriculum Map

See [`docs/learning_map.md`](docs/learning_map.md) for the full checklist.

| Phase | Lessons | Topic |
|---|---|---|
| 0 | — | Foundation & environment |
| 1 | 00–08 | MCP Fundamentals |
| 2 | 09–13 | Modern MCP 2026-07-28 |
| 3 | 14–20 | Production engineering |
| 4 | 21–23 | Extensions |
| 5 | 24–25 | Integration & migration |
| 6 | C01–C30, D01–D15 | Challenges |
| 7 | CAP01–CAP03 | Capstones |

---

## Environment Requirements

| Tool | Required | Notes |
|---|---|---|
| Python 3.12+ | **Yes** | 3.13 also accepted |
| uv | **Yes** | Package manager |
| Node.js / npx | **Yes** | MCP Inspector CLI |
| Docker | No | Optional deployment labs |
| PostgreSQL | No | Optional advanced labs |
| Paid LLM API key | **Never** | All exercises use deterministic fakes |

---

## Isolation

This directory is **fully self-contained**. It has its own:

- `pyproject.toml` and `uv.lock`
- `.venv/`
- `.env.example`

It does **not** modify any parent repository's dependencies, lock files, environment variables, or source code.

---

## Documentation

| File | Purpose |
|---|---|
| [`docs/learning_map.md`](docs/learning_map.md) | Lesson checklist and mastery tracker |
| [`docs/version_matrix.md`](docs/version_matrix.md) | Evidence-based SDK feature support |
| [`docs/legacy_vs_modern.md`](docs/legacy_vs_modern.md) | Side-by-side protocol comparison |
| [`docs/protocol_cheatsheet.md`](docs/protocol_cheatsheet.md) | Quick-reference wire format |
| [`docs/terminology.md`](docs/terminology.md) | Authoritative glossary |
| [`docs/security_model.md`](docs/security_model.md) | Threat model and security controls |
| [`docs/production_checklist.md`](docs/production_checklist.md) | Pre-production validation checklist |
| [`docs/references.md`](docs/references.md) | Authoritative, supplementary, and legacy sources |
