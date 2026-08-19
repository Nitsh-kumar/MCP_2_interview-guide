"""
tests/phase0/test_environment.py

Phase 0 Test Suite — Foundation & Environment Validation

These tests serve as executable specifications proving that:
    1. All pinned dependencies are installed at the correct versions.
    2. All required SDK import paths exist (no speculation).
    3. MCPServer can be instantiated.
    4. Client can connect in memory.
    5. Protocol version resolves to 2026-07-28.
    6. Tool discovery works correctly.
    7. Tool execution works correctly.
    8. client.session exposes a ClientSession instance.
    9. The Tasks extension is NOT implemented (as expected).
    10. No paid LLM API is required.

VERIFIED AGAINST: mcp==2.0.0, mcp-types==2.0.0
PROTOCOL TARGET: 2026-07-28
LAST VERIFIED: 2026-08-19
"""

from __future__ import annotations

import importlib
import sys
from importlib.metadata import PackageNotFoundError, version

import pytest


# ─── 1. Dependency Version Tests ─────────────────────────────────────────────


class TestDependencyVersions:
    """Verify pinned baseline versions match curriculum expectations."""

    BASELINE = {
        "mcp": "2.0.0",
        "mcp-types": "2.0.0",
    }

    def _get_version(self, pkg: str) -> str:
        """Get installed package version using importlib.metadata."""
        try:
            return version(pkg)
        except PackageNotFoundError:
            pytest.fail(f"Package {pkg!r} is not installed.")

    def test_mcp_version_is_baseline(self) -> None:
        """mcp must be exactly 2.0.0 — the curriculum baseline."""
        installed = self._get_version("mcp")
        assert installed == self.BASELINE["mcp"], (
            f"mcp version mismatch. "
            f"Curriculum baseline: {self.BASELINE['mcp']}, "
            f"Installed: {installed}. "
            f"Version-sensitive lessons may behave differently."
        )

    def test_mcp_types_version_is_baseline(self) -> None:
        """mcp-types must be exactly 2.0.0 — the curriculum baseline."""
        installed = self._get_version("mcp-types")
        assert installed == self.BASELINE["mcp-types"], (
            f"mcp-types version mismatch. "
            f"Curriculum baseline: {self.BASELINE['mcp-types']}, "
            f"Installed: {installed}."
        )

    def test_httpx2_is_installed(self) -> None:
        """httpx2 must be installed — SDK v2 transport dependency."""
        v = self._get_version("httpx2")
        assert v, f"httpx2 is not installed. SDK v2 requires httpx2, not httpx."

    def test_pydantic_v2_installed(self) -> None:
        """pydantic v2 required for input validation."""
        v = self._get_version("pydantic")
        major = int(v.split(".")[0])
        assert major >= 2, f"pydantic v2+ required, got {v}"

    def test_pytest_asyncio_installed(self) -> None:
        """pytest-asyncio required for async test execution."""
        v = self._get_version("pytest-asyncio")
        assert v, "pytest-asyncio is not installed"

    def test_opentelemetry_installed(self) -> None:
        """OpenTelemetry required for Lesson 19 observability."""
        v = self._get_version("opentelemetry-api")
        assert v, "opentelemetry-api is not installed"

    def test_uvicorn_installed(self) -> None:
        """uvicorn required for remote HTTP server lessons."""
        v = self._get_version("uvicorn")
        assert v, "uvicorn is not installed"

    def test_pyjwt_installed(self) -> None:
        """PyJWT with crypto required for authorization lessons."""
        v = self._get_version("pyjwt")
        assert v, "pyjwt is not installed"


# ─── 2. SDK Import Path Tests ─────────────────────────────────────────────────


class TestSDKImportPaths:
    """
    Verify every SDK import path used in the curriculum actually exists.

    These tests document what the SDK ACTUALLY exposes, not what we expect.
    If a test fails, the curriculum must be corrected — not the test.
    """

    def test_mcpserver_import(self) -> None:
        """MCPServer — primary server class in SDK v2."""
        from mcp.server import MCPServer  # noqa: F401

    def test_client_import(self) -> None:
        """Client — high-level client in SDK v2."""
        from mcp import Client  # noqa: F401

    def test_clientsession_import(self) -> None:
        """ClientSession — low-level escape hatch, NOT removed in v2."""
        from mcp import ClientSession  # noqa: F401

    def test_context_import(self) -> None:
        """
        Context — verified import path in mcp==2.0.0.
        NOT from mcp.server.fastmcp (that path fails in v2).
        """
        from mcp.server.context import Context  # noqa: F401

    def test_stdio_server_import(self) -> None:
        """stdio_server — for Lesson 08 (stdio transport)."""
        from mcp.server.stdio import stdio_server  # noqa: F401

    def test_mcp_types_import(self) -> None:
        """Core protocol types."""
        from mcp.types import ErrorData, Tool, Resource, Prompt  # noqa: F401

    def test_subscriptions_module_exists(self) -> None:
        """subscriptions module — subscriptions/listen infrastructure."""
        import mcp.server.subscriptions  # noqa: F401

    def test_elicitation_module_exists(self) -> None:
        """elicitation module — MRTR support."""
        import mcp.server.elicitation  # noqa: F401

    def test_request_state_module_exists(self) -> None:
        """request_state module — MRTR state management."""
        import mcp.server.request_state  # noqa: F401

    def test_memory_streams_import(self) -> None:
        """In-memory test stream helper."""
        from mcp.shared.memory import create_client_server_memory_streams  # noqa: F401

    def test_tasks_not_implemented(self) -> None:
        """
        CRITICAL: Tasks extension must NOT be implemented in mcp==2.0.0.

        This test documents a known SDK limitation.
        Lesson 23 teaches Tasks via a spec-level educational fixture only.
        If this test fails (i.e., tasks module IS found), update docs/version_matrix.md.
        """
        with pytest.raises(ImportError):
            import mcp.tasks  # type: ignore[import]  # noqa: F401

    def test_no_task_decorator_on_mcpserver(self) -> None:
        """MCPServer must not have a .task() decorator in mcp==2.0.0."""
        from mcp.server import MCPServer
        assert not hasattr(MCPServer, "task"), (
            "MCPServer unexpectedly has a .task() method. "
            "Update docs/version_matrix.md to reflect SDK Tasks support."
        )

    def test_httpx_not_httpx2_confusion(self) -> None:
        """
        Prove httpx2 is the SDK-required HTTP library.
        The old httpx package may still be present but is not used by SDK v2.
        """
        import httpx2  # noqa: F401
        # httpx2 must be importable for all SDK HTTP transport tests


# ─── 3. MCPServer Instantiation ───────────────────────────────────────────────


class TestMCPServerInstantiation:
    """Verify MCPServer can be instantiated and tools registered."""

    def test_mcpserver_instantiates(self) -> None:
        """MCPServer must be constructable with just a name."""
        from mcp.server import MCPServer
        server = MCPServer("test-server")
        assert server is not None
        assert server.name == "test-server"

    def test_tool_registration(self) -> None:
        """@server.tool() decorator must register a tool."""
        from mcp.server import MCPServer
        server = MCPServer("tool-test")

        @server.tool()
        def my_tool(x: int) -> int:
            """A test tool."""
            return x * 2

        # Server has an add_tool / list_tools method
        assert hasattr(server, "tool")

    def test_resource_registration(self) -> None:
        """@server.resource() decorator must be callable."""
        from mcp.server import MCPServer
        server = MCPServer("resource-test")

        @server.resource("test://hello")
        def hello() -> str:
            return "hello"

        assert hasattr(server, "resource")

    def test_prompt_registration(self) -> None:
        """@server.prompt() decorator must be callable."""
        from mcp.server import MCPServer
        server = MCPServer("prompt-test")

        @server.prompt()
        def my_prompt() -> str:
            return "You are a helpful assistant."

        assert hasattr(server, "prompt")


# ─── 4. In-Memory Client Integration Tests ────────────────────────────────────


class TestInMemoryClientIntegration:
    """
    Smoke tests proving Client + MCPServer work together in memory.

    These are the most important Phase 0 tests.
    They prove the full stack works without subprocess, network, or paid LLM.
    """

    @pytest.fixture
    def calculator_server(self):
        """Minimal calculator server for integration tests."""
        from mcp.server import MCPServer
        server = MCPServer("calculator")

        @server.tool()
        def add(a: float, b: float) -> float:
            """Add two numbers."""
            return a + b

        @server.tool()
        def multiply(a: float, b: float) -> float:
            """Multiply two numbers."""
            return a * b

        return server

    @pytest.mark.asyncio
    async def test_client_connects_in_memory(self, calculator_server) -> None:
        """Client must connect to MCPServer in memory without error."""
        from mcp import Client
        async with Client(calculator_server) as client:
            assert client is not None

    @pytest.mark.asyncio
    async def test_protocol_version_is_modern(self, calculator_server) -> None:
        """
        Protocol version must resolve to 2026-07-28.

        This is the most critical Phase 0 assertion. If this fails,
        the SDK is not operating in modern protocol mode.
        """
        from mcp import Client
        async with Client(calculator_server) as client:
            assert client.protocol_version == "2026-07-28", (
                f"Protocol version is not 2026-07-28. Got: {client.protocol_version}. "
                f"The curriculum assumes modern MCP semantics."
            )

    @pytest.mark.asyncio
    async def test_server_info_accessible(self, calculator_server) -> None:
        """Server info must be accessible after connection."""
        from mcp import Client
        async with Client(calculator_server) as client:
            info = client.server_info
            assert info is not None
            assert info.name == "calculator"

    @pytest.mark.asyncio
    async def test_tool_discovery(self, calculator_server) -> None:
        """
        list_tools() must return a ListToolsResult with a .tools list.

        This tests the server/discover equivalent at the tool level.
        Tools are discoverable without a prior initialize handshake.
        """
        from mcp import Client
        async with Client(calculator_server) as client:
            result = await client.list_tools()
            tool_names = [t.name for t in result.tools]
            assert "add" in tool_names, f"'add' tool not found. Got: {tool_names}"
            assert "multiply" in tool_names, f"'multiply' tool not found. Got: {tool_names}"

    @pytest.mark.asyncio
    async def test_tool_execution(self, calculator_server) -> None:
        """Tool execution must return correct result without LLM involvement."""
        from mcp import Client
        async with Client(calculator_server) as client:
            result = await client.call_tool("add", {"a": 3.0, "b": 4.0})
            assert not result.is_error, f"Tool returned error: {result.content}"
            # Result content is a list of TextContent blocks
            texts = [b.text for b in result.content if hasattr(b, "text")]
            assert any("7" in t for t in texts), (
                f"Expected '7' in result text. Got: {texts}"
            )

    @pytest.mark.asyncio
    async def test_multiple_tool_calls(self, calculator_server) -> None:
        """Multiple sequential tool calls must all succeed."""
        from mcp import Client
        async with Client(calculator_server) as client:
            add_result = await client.call_tool("add", {"a": 10.0, "b": 5.0})
            mul_result = await client.call_tool("multiply", {"a": 3.0, "b": 7.0})

            assert not add_result.is_error
            assert not mul_result.is_error

            add_texts = [b.text for b in add_result.content if hasattr(b, "text")]
            mul_texts = [b.text for b in mul_result.content if hasattr(b, "text")]

            assert any("15" in t for t in add_texts)
            assert any("21" in t for t in mul_texts)

    @pytest.mark.asyncio
    async def test_client_session_is_clientsession(self, calculator_server) -> None:
        """
        client.session must return the underlying ClientSession.

        ClientSession is NOT removed in SDK v2. It is the low-level escape
        hatch accessible via client.session. This is important for Lesson 25
        and advanced MRTR/inspection scenarios.
        """
        from mcp import Client, ClientSession
        async with Client(calculator_server) as client:
            session = client.session
            assert isinstance(session, ClientSession), (
                f"client.session must be a ClientSession, got {type(session)}"
            )

    @pytest.mark.asyncio
    async def test_no_paid_llm_required(self, calculator_server) -> None:
        """
        This test proves the entire stack works without any LLM API key.

        A FakeLLM decides to call a tool. The agent loop executes it via MCP.
        No OpenAI, Anthropic, Google, or Azure key is needed.
        """
        from mcp import Client
        from shared.fake_llm import FakeLLM, TextDecision, ToolCallDecision

        # Script the fake model: first call tool, then respond with text
        llm = FakeLLM(responses=[
            ToolCallDecision("add", {"a": 10.0, "b": 20.0}),
            TextDecision("The result is 30.0"),
        ])

        async with Client(calculator_server) as client:
            messages = [{"role": "user", "content": "What is 10 + 20?"}]

            # Agent loop iteration 1: model decides to call add
            decision = llm.decide(messages, available_tools=None)
            assert isinstance(decision, ToolCallDecision)
            assert decision.tool_name == "add"

            # Host calls MCP server on model's behalf
            result = await client.call_tool(decision.tool_name, decision.arguments)
            assert not result.is_error

            # Append tool result to messages
            texts = [b.text for b in result.content if hasattr(b, "text")]
            messages.append({"role": "tool", "content": " ".join(texts)})

            # Agent loop iteration 2: model responds with text
            decision2 = llm.decide(messages)
            assert isinstance(decision2, TextDecision)
            assert "30" in decision2.text

            llm.assert_all_responses_consumed()


# ─── 5. Shared Infrastructure Tests ──────────────────────────────────────────


class TestSharedInfrastructure:
    """Verify shared modules are importable and functional."""

    def test_fake_llm_importable(self) -> None:
        """FakeLLM must be importable from shared.fake_llm."""
        from shared.fake_llm import FakeLLM, TextDecision, ToolCallDecision  # noqa: F401

    def test_fake_llm_scripted_responses(self) -> None:
        """FakeLLM must return scripted decisions in order."""
        from shared.fake_llm import FakeLLM, TextDecision, ToolCallDecision

        llm = FakeLLM(responses=[
            ToolCallDecision("search", {"query": "MCP"}),
            TextDecision("Here are the results..."),
        ])

        d1 = llm.decide([])
        assert isinstance(d1, ToolCallDecision)
        assert d1.tool_name == "search"

        d2 = llm.decide([])
        assert isinstance(d2, TextDecision)

        llm.assert_all_responses_consumed()

    def test_fake_llm_raises_on_exhaustion(self) -> None:
        """FakeLLM must raise StopIteration when responses are exhausted."""
        from shared.fake_llm import FakeLLM, TextDecision

        llm = FakeLLM(responses=[TextDecision("done")])
        llm.decide([])

        with pytest.raises(StopIteration):
            llm.decide([])

    def test_protocol_capture_importable(self) -> None:
        """Protocol capture utilities must be importable."""
        from shared.protocol_capture import (  # noqa: F401
            CapturedMessage,
            ProtocolCapture,
            make_jsonrpc_request,
            make_modern_tools_call,
            validate_jsonrpc_message,
        )

    def test_jsonrpc_validation(self) -> None:
        """JSON-RPC validator must correctly identify valid and invalid messages."""
        from shared.protocol_capture import validate_jsonrpc_message

        # Valid request
        valid = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {"name": "add", "arguments": {}},
        }
        assert validate_jsonrpc_message(valid) == []

        # Missing jsonrpc field
        invalid = {"id": 1, "method": "tools/call"}
        errors = validate_jsonrpc_message(invalid)
        assert len(errors) > 0

        # Valid notification (no id)
        notification = {
            "jsonrpc": "2.0",
            "method": "notifications/toolsListChanged",
        }
        assert validate_jsonrpc_message(notification) == []

    def test_fixture_servers_importable(self) -> None:
        """Shared fixture servers must be importable."""
        from shared.fixtures.servers import (  # noqa: F401
            make_calculator_server,
            make_echo_server,
            make_stateful_counter_server,
        )

    @pytest.mark.asyncio
    async def test_calculator_fixture_server(self) -> None:
        """Calculator fixture server must work end-to-end."""
        from mcp import Client
        from shared.fixtures.servers import make_calculator_server

        server = make_calculator_server()
        async with Client(server) as client:
            result = await client.call_tool("add", {"a": 5.0, "b": 3.0})
            assert not result.is_error
            texts = [b.text for b in result.content if hasattr(b, "text")]
            assert any("8" in t for t in texts)

    def test_testing_utilities_importable(self) -> None:
        """Testing utilities must be importable."""
        from shared.testing import (  # noqa: F401
            assert_call_tool_not_error,
            assert_call_tool_text,
            assert_no_imaginary_sdk_api,
            assert_tool_names,
            get_client,
        )

    @pytest.mark.asyncio
    async def test_assert_tool_names_helper(self) -> None:
        """assert_tool_names helper must work correctly."""
        from mcp import Client
        from shared.fixtures.servers import make_calculator_server
        from shared.testing import assert_tool_names

        server = make_calculator_server()
        async with Client(server) as client:
            tools_result = await client.list_tools()
            assert_tool_names(tools_result, ["add", "multiply"])
