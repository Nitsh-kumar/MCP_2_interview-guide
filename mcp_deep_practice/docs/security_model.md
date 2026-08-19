# MCP Security Model

> Protocol target: `2026-07-28` | SDK: `mcp==2.0.0`
> This document is the foundation for Lesson 15 (MCP Security).
> All examples are sandboxed. No real credentials, systems, or destructive exploits.

---

## Core Principle: MCP Does Not Automatically Secure Tools

> ⚠️ "MCP makes tools secure automatically" is FALSE.
>
> MCP is a communication protocol. It defines HOW tools are called, NOT whether those calls are safe.
> Security is the responsibility of the server implementation.

---

## Threat Taxonomy

### Tier 1 — LLM-Layer Attacks (novel to AI systems)

| Threat | Description | MCP-Specific Risk |
|---|---|---|
| **Prompt Injection** | Malicious content in tool output manipulates model behavior | Tool results flow directly into model context |
| **Tool Poisoning** | Malicious tool descriptions bias model decisions | Tool descriptions are trusted by the model |
| **Malicious Resource Content** | Resource content contains attacker-controlled instructions | Resource content rendered in model context |
| **Indirect Prompt Injection** | Attacker plants instructions in data the tool retrieves | Email reader, document processor, web fetch |

### Tier 2 — Authorization & Access Control Failures

| Threat | Description |
|---|---|
| **Over-broad permissions** | Tool granted rights far exceeding its legitimate scope |
| **Confused deputy** | Server manipulated into using its elevated credentials on behalf of attacker |
| **Token passthrough** | Server forwards received tokens to downstream services without scope validation |
| **Missing scope enforcement** | Server validates token presence but not token scopes/audience |
| **Audience mismatch** | Token intended for service A accepted by service B |
| **Cross-server trust escalation** | Tool on server A passes data to server B with different trust level |

### Tier 3 — Input Validation Failures

| Threat | Description |
|---|---|
| **Command injection** | Tool passes LLM-supplied string to shell without sanitization |
| **Path traversal** | Tool accesses files outside intended root via `../../` sequences |
| **Filesystem escape** | Symlink traversal bypasses path restriction |
| **SSRF** | Tool fetches URLs supplied by LLM, reaching internal services |
| **SQL injection** | Tool constructs queries from LLM-supplied strings |
| **Schema bypass** | Actual validation weaker than declared schema |

### Tier 4 — Infrastructure & Supply Chain

| Threat | Description |
|---|---|
| **Untrusted MCP server** | Server installed from untrusted source, exploiting model trust |
| **Supply chain compromise** | Malicious package masquerading as MCP tool |
| **Credential leakage** | Tool logs or returns secrets in response |
| **Unsafe write operations** | Tool modifies production data without confirmation |
| **Audit gap** | No record of what tools were called with what arguments |

---

## Security Controls by Layer

### Tool Design Controls

```
✓ Narrow, single-purpose tools (not do_everything)
✓ Explicit schema validation for all inputs
✓ Allowlist values for enumerable parameters
✓ Human confirmation required for destructive operations (MRTR)
✓ Idempotency keys for write operations
✓ Separation of read and write tools
✓ Tool descriptions that accurately reflect side effects
```

### Input Sanitization Controls

```
✓ Never pass LLM-supplied strings directly to shell commands
✓ Path canonicalization and root confinement for filesystem tools
✓ URL allowlisting for fetch tools
✓ Parameterized queries only for database tools
✓ Output encoding before returning content to model
```

### Authorization Controls

```
✓ Bearer token validation on every request
✓ Audience claim validation (expected audience must match)
✓ Issuer claim validation (expected issuer must match)
✓ Scope validation per operation (read vs write vs admin)
✓ Tenant isolation (no cross-tenant data access)
✓ Rate limiting per authenticated identity
```

### Operational Controls

```
✓ Structured audit log: who called what tool with what args and what result
✓ Secrets never appear in tool responses or logs
✓ No unrestricted shell access from any tool
✓ Filesystem operations confined to an explicit sandbox root
✓ All external API calls authenticated with principle of least privilege
```

---

## Design Rules for Safe MCP Tools

### Rule 1: Every input is adversarial
Assume the LLM has been manipulated. Validate all inputs as if they came from an attacker.

### Rule 2: Side effects must be explicit
If a tool modifies state, its name and description must say so clearly. Use MRTR confirmation for destructive operations.

### Rule 3: Scope is not a UI concept
Just because an operation appears safe in the UI doesn't mean an attacker can't invoke it directly through the MCP protocol.

### Rule 4: Tool output re-enters the model
Malicious content in a tool's response becomes part of the model's prompt. Sanitize or scope what you return.

### Rule 5: Least privilege at every boundary
The MCP server should have only the permissions needed for its tools — not all permissions held by the running process.

### Rule 6: Audit everything
Log every tool call: caller identity, tool name, arguments (sanitized), result status, duration. This is not optional.

---

## What MCP Authorization Is (and Is Not)

**IS:**
- OAuth 2.1 Bearer tokens validated by the MCP server (Resource Server role)
- JWT claims (audience, issuer, scope, subject) checked per request
- Role-based access control implemented in tool handlers

**IS NOT:**
- Automatic — you must implement validation
- Provided by the protocol — the protocol only defines transport headers
- A substitute for input validation — auth + injection are separate layers

---

## Threat Model Template (used in Capstone 03)

```
Asset:           What are we protecting?
Threat:          What could go wrong?
Attacker:        Who is the adversary and what can they control?
Attack vector:   How does the attack reach the vulnerable component?
Impact:          What is the worst-case outcome?
Likelihood:      How realistic is this attack?
Control:         What prevents or detects this attack?
Residual risk:   What risk remains after controls?
```

---

## Testing Security Properties

Security tests must prove mitigation, not just absence of obvious errors:

```python
# Test structure for every security control
def test_path_traversal_rejected():
    """
    Proves that the tool rejects paths outside the sandbox root.
    The test must actually attempt the traversal and verify rejection.
    """
    with pytest.raises(PermissionError):
        sandboxed_read_file("../../etc/passwd")

def test_token_audience_enforced():
    """
    Proves that a token with wrong audience is rejected.
    """
    token = make_token(audience="wrong-service")
    response = call_tool_with_token("get_ticket", token)
    assert response.error.code == UNAUTHORIZED
```

Never test security by checking that the happy path works. Test that attacks fail.
