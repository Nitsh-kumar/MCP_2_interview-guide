# Challenge: Anti-Pattern Architecture Design (When NOT to use MCP)

## Objective

Design a complete software architecture for a system where introducing MCP adds **zero or negative architectural value**.

---

## The Scenario

You are the Principal Architect at a high-frequency trading firm or an embedded telemetry system (e.g., automotive braking controller).

### Requirements
1. Describe the system requirements (throughput, latency, participants, determinism).
2. Diagram or describe the communication flow between components.
3. Explicitly explain why wrapping internal tools or data stores in an MCP Server would degrade the system in terms of:
   - Serialization & Framing latency (JSON-RPC overhead vs binary protocols like Protobuf/gRPC)
   - Cognitive overhead (lack of an LLM or reasoning agent in the critical path)
   - Failure modes & Non-deterministic tool selection
   - Security boundaries and blast radius

---

## Evaluation Criteria

Your architectural critique must demonstrate mastery of:
- The distinction between deterministic machine-to-machine protocols and cognitive capability protocols.
- The performance cost of text-based JSON-RPC vs zero-copy binary RPCs.
- Why MCP should only be introduced when an AI model or host application requires dynamic capability discovery and execution.
