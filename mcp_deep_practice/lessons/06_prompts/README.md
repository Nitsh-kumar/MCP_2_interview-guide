# Lesson Metadata

- Protocol revision: 2026-07-28
- SDK baseline: mcp==2.0.0
- Feature status: CORE
- SDK support: FULL
- Verified against: mcp==2.0.0, mcp-types==2.0.0
- Last verified: 2026-08-19

---

# Lesson 06: MCP Prompts & Workflow Templates

## 1. Learning Objectives

By the end of this lesson, you will be able to:
1. Define what an **MCP Prompt** is at the protocol layer and distinguish it from a model's base system prompt or general prompt engineering.
2. Register parameterized prompt templates using `@server.prompt()` with typed arguments and default values.
3. Discover and inspect available prompts using `await client.list_prompts()`.
4. Retrieve rendered prompt message lists using `await client.get_prompt(name, arguments)` returning `GetPromptResult.messages`.
5. Apply the **Resource + Prompt + Tool** triad to decompose bloated monolithic workflows into clean protocol primitives.

---

## 2. The Three Layers of MCP Prompts

```
┌─────────────────────────────────────────────────────────────────────────┐
│ LAYER 3: User Interface & Host Slash Commands                           │
│ User types "/review_code" in UI -> Host requests prompt from server     │
├─────────────────────────────────────────────────────────────────────────┤
│ LAYER 2: Python SDK Template Engine                                     │
│ @server.prompt(), PromptArgument schema generation, PromptMessage list  │
├─────────────────────────────────────────────────────────────────────────┤
│ LAYER 1: Wire Protocol (JSON-RPC)                                       │
│ prompts/list -> prompts/get -> GetPromptResult {messages: [...]}        │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Lesson Progression

- **Stage A (Observe)**: Run `uv run python lessons/06_prompts/demo.py` to observe `review_code` and `summarize_incident` prompt workflows.
- **Stage B (Explain)**: Read `concepts.md` on why Prompts are user/host-driven workflows rather than autonomous LLM actions.
- **Stage C (Modify)**: In `exercise.py`, implement the `explain_architecture` prompt with typed arguments and choices.
- **Stage D (Debug)**: Diagnose prompt argument validation errors and message role structures.
- **Stage E (Build / Challenge)**: In `challenge.md`, decompose a bloated "do-everything" tool into the Resource + Prompt + Tool triad.

---

## 4. Verification

Run the lesson tests:
```bash
uv run pytest lessons/06_prompts/test_exercise.py -v
```
