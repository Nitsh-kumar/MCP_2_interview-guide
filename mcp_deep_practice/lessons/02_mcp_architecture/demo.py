#!/usr/bin/env python
"""
lessons/02_mcp_architecture/demo.py

Demonstration: Three Core Architectural Topologies in MCP.

Simulates and compares:
  Topology 1: Local stdio subprocess server (in-process pipe model)
  Topology 2: Remote HTTP server with authentication bearer token
  Topology 3: Multi-server host aggregating tools from multiple servers
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any


# ─── Data Models ─────────────────────────────────────────────────────────────


@dataclass
class ToolDefinition:
    server_name: str
    name: str
    description: str
    schema: dict[str, Any]


# ─── Topology 1: Local Server (stdio model) ──────────────────────────────────


class LocalFilesystemMCPServer:
    """Simulates a local stdio MCP server accessing the local workspace."""

    def __init__(self, workspace_path: str) -> None:
        self.name = "local_fs"
        self.workspace_path = workspace_path
        self._files = {
            "README.md": "# Project Title\nThis is a sample repository.",
            "config.json": '{"environment": "staging", "debug": true}',
        }

    def list_tools(self) -> list[ToolDefinition]:
        return [
            ToolDefinition(
                server_name=self.name,
                name="read_workspace_file",
                description="Read file content from local workspace.",
                schema={"type": "object", "properties": {"filename": {"type": "string"}}},
            )
        ]

    def call_tool(self, name: str, args: dict[str, Any]) -> dict[str, Any]:
        if name == "read_workspace_file":
            fn = args.get("filename", "")
            if fn in self._files:
                return {"content": [{"type": "text", "text": self._files[fn]}], "isError": False}
            return {"content": [{"type": "text", "text": f"File not found: {fn}"}], "isError": True}
        return {"content": [{"type": "text", "text": f"Unknown tool: {name}"}], "isError": True}


# ─── Topology 2: Remote Server (HTTP Model with Bearer Token) ────────────────


class RemoteGitHubMCPServer:
    """Simulates a remote cloud MCP server behind an authenticated HTTP gateway."""

    def __init__(self, expected_token: str) -> None:
        self.name = "remote_github"
        self._token = expected_token
        self._issues = [
            {"id": 101, "title": "Fix login race condition", "state": "open"},
            {"id": 102, "title": "Add OAuth2 refresh endpoint", "state": "closed"},
        ]

    def list_tools(self, auth_header: str) -> list[ToolDefinition]:
        self._verify_auth(auth_header)
        return [
            ToolDefinition(
                server_name=self.name,
                name="list_repo_issues",
                description="List issues from GitHub repository.",
                schema={"type": "object", "properties": {"state": {"type": "string"}}},
            )
        ]

    def call_tool(self, name: str, args: dict[str, Any], auth_header: str) -> dict[str, Any]:
        self._verify_auth(auth_header)
        if name == "list_repo_issues":
            state = args.get("state", "all")
            filtered = [
                i for i in self._issues if state == "all" or i["state"] == state
            ]
            return {"content": [{"type": "text", "text": json.dumps(filtered)}], "isError": False}
        return {"content": [{"type": "text", "text": f"Unknown tool: {name}"}], "isError": True}

    def _verify_auth(self, auth_header: str) -> None:
        if auth_header != f"Bearer {self._token}":
            raise PermissionError("HTTP 401 Unauthorized: Invalid or missing Bearer token.")


# ─── Topology 3: Multi-Server Host Aggregator ────────────────────────────────


class MultiServerMCPHost:
    """
    Host application that connects to multiple MCP servers concurrently,
    aggregates their tool catalogs, routes calls, and isolates failures.
    """

    def __init__(self) -> None:
        self._clients: dict[str, Any] = {}
        self._tool_catalog: dict[str, ToolDefinition] = {}

    def attach_local_server(self, server: LocalFilesystemMCPServer) -> None:
        self._clients[server.name] = ("local", server)
        for tool in server.list_tools():
            self._tool_catalog[tool.name] = tool

    def attach_remote_server(self, server: RemoteGitHubMCPServer, token: str) -> None:
        self._clients[server.name] = ("remote", server, token)
        for tool in server.list_tools(auth_header=f"Bearer {token}"):
            self._tool_catalog[tool.name] = tool

    def get_unified_tools(self) -> list[ToolDefinition]:
        return list(self._tool_catalog.values())

    def execute_tool(self, tool_name: str, args: dict[str, Any]) -> dict[str, Any]:
        if tool_name not in self._tool_catalog:
            return {"content": [{"type": "text", "text": f"Tool '{tool_name}' not found."}], "isError": True}

        tool_meta = self._tool_catalog[tool_name]
        server_info = self._clients[tool_meta.server_name]

        if server_info[0] == "local":
            server: LocalFilesystemMCPServer = server_info[1]
            return server.call_tool(tool_name, args)
        else:
            server: RemoteGitHubMCPServer = server_info[1]
            token: str = server_info[2]
            return server.call_tool(tool_name, args, auth_header=f"Bearer {token}")


# ─── Demonstration ────────────────────────────────────────────────────────────


def main() -> None:
    print("=" * 64)
    print("  Lesson 02 Demo: MCP Architecture Topologies")
    print("=" * 64)

    # 1. Instantiate servers
    local_fs = LocalFilesystemMCPServer(workspace_path="/home/user/project")
    remote_github = RemoteGitHubMCPServer(expected_token="ghp_super_secret_token_123")

    # 2. Host attaches both servers
    host = MultiServerMCPHost()
    host.attach_local_server(local_fs)
    host.attach_remote_server(remote_github, token="ghp_super_secret_token_123")

    # 3. Unified discovery
    unified_tools = host.get_unified_tools()
    print(f"\n[Host Aggregator] Discovered {len(unified_tools)} tools across 2 servers:")
    for t in unified_tools:
        print(f"  - [{t.server_name}] {t.name}: {t.description}")

    # 4. Invoke tool from Local Server
    print("\n[Host] Executing local tool: 'read_workspace_file' (README.md)...")
    res1 = host.execute_tool("read_workspace_file", {"filename": "README.md"})
    print(f"  Result (isError={res1['isError']}):\n  {res1['content'][0]['text']}")

    # 5. Invoke tool from Remote Server
    print("\n[Host] Executing remote tool: 'list_repo_issues' (open issues)...")
    res2 = host.execute_tool("list_repo_issues", {"state": "open"})
    print(f"  Result (isError={res2['isError']}):\n  {res2['content'][0]['text']}")

    # 6. Failure isolation demonstration
    print("\n[Host] Testing authentication failure on remote server...")
    bad_host = MultiServerMCPHost()
    try:
        bad_host.attach_remote_server(remote_github, token="wrong_token")
    except PermissionError as e:
        print(f"  Remote Auth Protection Successful: {e}")

    print("\n" + "=" * 64)
    print("  Key Takeaway:")
    print("    - The Host owns credentials and manages client connections.")
    print("    - Multiple heterogeneous servers (stdio + HTTP) coexist seamlessly.")
    print("=" * 64)


if __name__ == "__main__":
    main()
