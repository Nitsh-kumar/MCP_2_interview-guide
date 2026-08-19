# Challenge: Batch Requests & Transport Framing in JSON-RPC 2.0

## Objective

Extend your understanding of the JSON-RPC wire format by analyzing JSON-RPC 2.0 Batch Requests and framing challenges over stdio and HTTP.

---

## The Challenge

1. **Batch Requests**:
   - The JSON-RPC 2.0 specification allows a client to send an Array of Request/Notification objects in a single message payload.
   - Explain how a server must process a batch containing:
     - 2 valid requests
     - 1 notification
     - 1 request for an unknown method
     - 1 malformed request object
   - What does the response array look like? Does it include responses for notifications? What if the batch contains *only* notifications?

2. **Transport Framing**:
   - Over raw TCP or stdio, JSON objects arrive as a continuous byte stream.
   - Explain the two primary methods of framing JSON-RPC messages over a byte stream:
     - Newline-delimited JSON (ndjson / line framing)
     - `Content-Length` headers (LSP-style framing)
   - Why did modern MCP standardize on newline-delimited framing for stdio and HTTP POST/SSE for remote transports?
