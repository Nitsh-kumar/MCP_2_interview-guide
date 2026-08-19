# Production MCP Server Checklist

> Protocol target: `2026-07-28` | SDK: `mcp==2.0.0`
> Use this before deploying any remote MCP server to production.
> For the full implementation guide, see Lesson 20 and Capstone 03.

---

## Protocol Correctness

- [ ] Server responds to `server/discover` correctly
- [ ] All tools have accurate input schemas (not overly broad)
- [ ] Tool names are descriptive and unambiguous
- [ ] Tool descriptions accurately state side effects
- [ ] Resources use meaningful, stable URIs
- [ ] Resource templates correctly parameterized
- [ ] Prompts have documented argument schemas
- [ ] JSON-RPC error codes are appropriate and not leaking internal details
- [ ] `MCP-Protocol-Version` header processed and validated
- [ ] `_meta` block version agrees with HTTP routing header

## Transport Security

- [ ] HTTPS enforced (TLS 1.2+ minimum, TLS 1.3 recommended)
- [ ] Invalid certificates rejected (no skip-verify in production)
- [ ] HTTP headers validated: `Mcp-Method`, `Mcp-Name`, `MCP-Protocol-Version`
- [ ] Maximum request body size enforced
- [ ] Timeouts configured for all operations
- [ ] Connection limits configured

## Authorization

- [ ] Every request requires a valid Bearer token
- [ ] JWT signature verified (asymmetric RS256 recommended)
- [ ] `aud` (audience) claim verified against expected value
- [ ] `iss` (issuer) claim verified against expected value
- [ ] `exp` (expiration) enforced
- [ ] Scope checked per tool (read scope ≠ write scope)
- [ ] Tenant isolation enforced where applicable
- [ ] Admin tools require elevated scope

## Input Validation

- [ ] All tool inputs validated against declared JSON Schema
- [ ] No LLM-supplied strings passed to shell commands
- [ ] Filesystem tools confined to explicit sandbox root
- [ ] URL parameters allowlisted or validated against SSRF
- [ ] Database queries use parameterized statements only
- [ ] Numeric inputs bounds-checked

## Write Tool Safety

- [ ] Destructive tools require explicit MRTR confirmation
- [ ] All write tools support idempotency keys
- [ ] Idempotency deduplication cache configured with TTL
- [ ] Write tools return clear, auditable results
- [ ] Double-execution of write tools produces correct idempotent outcome

## Reliability

- [ ] All external calls have timeouts
- [ ] Retry policy documented and tested
- [ ] Circuit breakers configured for downstream dependencies
- [ ] Graceful shutdown: in-flight requests complete or are cancelled cleanly
- [ ] Health check endpoint responds correctly under load
- [ ] Readiness check blocks traffic until server is ready

## Stateless Scalability

- [ ] No in-process session state that must survive replica restart
- [ ] Application state is stored in external store (cache/DB), not process memory
- [ ] Load-balanced requests land on any replica without error
- [ ] `subscriptions/listen` uses shared notification bus, not per-process state

## Observability

- [ ] Structured logs written to stderr/log aggregator (not stdout for stdio)
- [ ] Every tool call logged: caller, tool name, status, duration
- [ ] Authorization failures logged (without leaking token content)
- [ ] OpenTelemetry traces enabled and exported
- [ ] Tool latency metrics collected
- [ ] Error rate alerting configured
- [ ] Audit log retained per compliance requirements

## Security Operations

- [ ] Secrets injected at runtime (env / secret manager), not in code or images
- [ ] No credentials in logs or tool responses
- [ ] Dependency vulnerability scanning configured
- [ ] Container image uses non-root user
- [ ] Minimal filesystem permissions in container

## Deployment

- [ ] Docker image uses pinned base image digest
- [ ] Container resources (CPU/memory) limited
- [ ] Liveness and readiness probes configured
- [ ] Horizontal pod autoscaling tested
- [ ] Rolling update strategy configured (not recreate)
- [ ] Rollback procedure documented and tested

## Documentation

- [ ] API surface documented (tool names, schemas, behavior, errors)
- [ ] Authorization requirements documented per tool
- [ ] Changelog maintained
- [ ] Threat model reviewed
- [ ] Incident response runbook exists
- [ ] SLA/SLO defined

---

## Pre-Deployment Test Requirements

Run before every production deployment:

```bash
# Full test suite
uv run pytest --tb=short -q

# Doctor check
uv run python scripts/doctor.py

# Verify all phases
uv run python scripts/verify_all.py

# Security-specific tests
uv run pytest tests/ -k "security or auth or injection or traversal" -v

# Load test (optional but recommended)
# locust -f tests/load/locustfile.py --headless -u 50 -r 5 --run-time 60s
```

No deployment proceeds if any security test fails.
