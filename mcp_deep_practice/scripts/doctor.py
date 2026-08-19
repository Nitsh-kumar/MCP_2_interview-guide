#!/usr/bin/env python
"""
scripts/doctor.py

MCP Deep Practice Lab — Environment Diagnostics

Usage:
    uv run python scripts/doctor.py

Reports:
    - Python version
    - uv version
    - MCP SDK version vs curriculum baseline
    - Actual installed package versions (via importlib.metadata)
    - SDK API availability check
    - Protocol version verification
    - MCP Inspector availability (npx)
    - Docker availability (OPTIONAL)
    - Environment variable configuration
    - Overall health status

IMPORTANT:
    - Package versions are read via importlib.metadata.version()
    - Secret values are NEVER printed
    - If SDK version differs from baseline (2.0.0), a WARNING is issued
    - Docker is OPTIONAL; core lessons do not require it
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from importlib.metadata import PackageNotFoundError, version as pkg_version


# ─── Constants ────────────────────────────────────────────────────────────────

SDK_BASELINE = "2.0.0"
MCTYPES_BASELINE = "2.0.0"
PROTOCOL_TARGET = "2026-07-28"
PYTHON_MIN = (3, 12)


# ─── Helpers ──────────────────────────────────────────────────────────────────

def ok(msg: str) -> None:
    print(f"  [OK]   {msg}")

def warn(msg: str) -> None:
    print(f"  [WARN] {msg}")

def fail(msg: str) -> None:
    print(f"  [FAIL] {msg}")

def section(title: str) -> None:
    print()
    dashes = "-" * max(1, 60 - len(title))
    print(f"-- {title} {dashes}")


def get_version(pkg: str) -> str | None:
    try:
        return pkg_version(pkg)
    except PackageNotFoundError:
        return None


def run_cmd(cmd: list[str]) -> tuple[int, str]:
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=5
        )
        return result.returncode, (result.stdout + result.stderr).strip()
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return -1, ""


# ─── Checks ───────────────────────────────────────────────────────────────────

def check_python() -> bool:
    version = sys.version_info
    ver_str = f"{version.major}.{version.minor}.{version.micro}"
    if version >= PYTHON_MIN:
        ok(f"Python {ver_str}")
        return True
    else:
        fail(f"Python {ver_str} — requires {PYTHON_MIN[0]}.{PYTHON_MIN[1]}+")
        return False


def check_uv() -> bool:
    rc, out = run_cmd(["uv", "--version"])
    if rc == 0 and out:
        ok(f"uv: {out.strip()}")
        return True
    else:
        fail("uv not found — install from https://docs.astral.sh/uv/")
        return False


def check_sdk_versions() -> bool:
    all_ok = True

    # mcp
    mcp_ver = get_version("mcp")
    if mcp_ver is None:
        fail("mcp is not installed — run: uv sync")
        all_ok = False
    elif mcp_ver == SDK_BASELINE:
        ok(f"mcp=={mcp_ver} (curriculum baseline)")
    else:
        warn(
            f"mcp=={mcp_ver} -- SDK VERSION DIFFERS FROM CURRICULUM BASELINE ({SDK_BASELINE}). "
            f"Version-sensitive lessons (especially Lesson 23 Tasks) may behave differently."
        )

    # mcp-types
    mcp_types_ver = get_version("mcp-types")
    if mcp_types_ver is None:
        fail("mcp-types is not installed -- run: uv sync")
        all_ok = False
    elif mcp_types_ver == MCTYPES_BASELINE:
        ok(f"mcp-types=={mcp_types_ver} (curriculum baseline)")
    else:
        warn(f"mcp-types=={mcp_types_ver} -- differs from baseline ({MCTYPES_BASELINE})")

    # httpx2
    httpx2_ver = get_version("httpx2")
    if httpx2_ver:
        ok(f"httpx2=={httpx2_ver} (SDK v2 HTTP transport dependency)")
    else:
        fail("httpx2 is not installed -- SDK v2 requires httpx2, not httpx")
        all_ok = False

    # Other critical packages
    for pkg in ["pydantic", "starlette", "uvicorn", "pytest", "pytest-asyncio",
                "opentelemetry-api", "pyjwt", "jsonschema", "rich", "typer"]:
        v = get_version(pkg)
        if v:
            ok(f"{pkg}=={v}")
        else:
            warn(f"{pkg} is not installed")

    return all_ok


def check_sdk_imports() -> bool:
    """Verify critical import paths exist in the installed SDK."""
    all_ok = True
    imports_to_check = [
        ("mcp.server", "MCPServer"),
        ("mcp", "Client"),
        ("mcp", "ClientSession"),
        ("mcp.server.context", "Context"),
        ("mcp.server.stdio", "stdio_server"),
        ("mcp.shared.memory", "create_client_server_memory_streams"),
        ("mcp.server.subscriptions", "InMemorySubscriptionBus"),
        ("mcp.server.elicitation", "elicit_with_validation"),
    ]

    for module_path, attr in imports_to_check:
        try:
            mod = __import__(module_path, fromlist=[attr])
            if hasattr(mod, attr):
                ok(f"from {module_path} import {attr}")
            else:
                fail(f"from {module_path} import {attr} — attribute not found")
                all_ok = False
        except ImportError as e:
            fail(f"from {module_path} import {attr} — IMPORT ERROR: {e}")
            all_ok = False

    # Tasks extension: confirm NOT_IMPLEMENTED
    try:
        import mcp.tasks  # type: ignore
        warn(
            "mcp.tasks module EXISTS — Tasks extension may now be implemented. "
            "Update docs/version_matrix.md and Lesson 23."
        )
    except ImportError:
        ok("mcp.tasks: NOT_IMPLEMENTED (expected for mcp==2.0.0)")

    return all_ok


def check_protocol_version() -> bool:
    """Verify the SDK resolves to protocol version 2026-07-28."""
    try:
        import asyncio
        from mcp import Client
        from mcp.server import MCPServer

        server = MCPServer("doctor-probe")

        @server.tool()
        def ping() -> str:
            return "pong"

        async def probe() -> str:
            async with Client(server) as client:
                return client.protocol_version or "unknown"

        pv = asyncio.run(probe())
        if pv == PROTOCOL_TARGET:
            ok(f"Protocol version: {pv} (VERIFIED)")
            return True
        else:
            warn(
                f"Protocol version: {pv} -- expected {PROTOCOL_TARGET}. "
                f"Modern MCP semantics may not apply."
            )
            return False
    except Exception as e:
        fail(f"Protocol version check failed: {e}")
        return False


def check_inspector() -> None:
    """Check MCP Inspector CLI availability."""
    rc, out = run_cmd(["npx", "--version"])
    if rc == 0:
        npx_ver = out.strip().split("\n")[0]
        ok(f"npx {npx_ver} -- MCP Inspector CLI available via: npx @modelcontextprotocol/inspector")
    else:
        warn(
            "npx not found -- MCP Inspector CLI unavailable. "
            "Install Node.js from https://nodejs.org/"
        )

    rc2, out2 = run_cmd(["node", "--version"])
    if rc2 == 0:
        ok(f"Node.js: {out2.strip()}")


def check_docker() -> None:
    """Check Docker availability (OPTIONAL -- not required for core lessons)."""
    rc, out = run_cmd(["docker", "--version"])
    if rc == 0:
        ok(f"Docker: {out.strip()} (optional labs enabled)")
    else:
        warn(
            "Docker not available -- OPTIONAL lab exercises will be skipped. "
            "All core curriculum lessons work without Docker."
        )


def check_environment_config() -> None:
    """Check environment variable configuration (without printing secret values)."""
    env_file = os.path.join(os.path.dirname(__file__), "..", ".env")
    if os.path.exists(env_file):
        ok(".env file found")
    else:
        warn(".env file not found -- copy .env.example to .env for local config")

    # Check for accidental secret exposure
    secret_vars = ["MCP_AUTH_SECRET", "OPENAI_API_KEY", "ANTHROPIC_API_KEY",
                   "DATABASE_URL", "ANTHROPIC_API_KEY"]
    for var in secret_vars:
        val = os.environ.get(var, "")
        if val and var in ["OPENAI_API_KEY", "ANTHROPIC_API_KEY"]:
            warn(
                f"{var} is set -- note that all core curriculum exercises work "
                f"without LLM API keys. This is only needed for optional Lesson 24 adapters."
            )
        # NEVER print the value


# ─── Main ─────────────────────────────────────────────────────────────────────

def main() -> None:
    print()
    print("=" * 64)
    print("  MCP Deep Practice Lab -- Environment Doctor")
    print(f"  Protocol target: {PROTOCOL_TARGET}")
    print(f"  SDK baseline:    mcp=={SDK_BASELINE}")
    print("=" * 64)

    issues: list[str] = []

    section("Python & Package Manager")
    if not check_python():
        issues.append("Python version too old")
    check_uv()

    section("Dependency Versions")
    if not check_sdk_versions():
        issues.append("Missing or mismatched dependencies")

    section("SDK Import Paths")
    if not check_sdk_imports():
        issues.append("SDK import failures detected")

    section("Protocol Version Verification")
    if not check_protocol_version():
        issues.append("Protocol version not 2026-07-28")

    section("MCP Inspector (npx)")
    check_inspector()

    section("Docker (Optional)")
    check_docker()

    section("Environment Configuration")
    check_environment_config()

    # ── Summary ────────────────────────────────────────────────────────────────
    print()
    print("-" * 64)
    if not issues:
        print("  [OK] ALL CHECKS PASSED -- environment is ready for the curriculum")
        print(f"  [OK] Protocol target: {PROTOCOL_TARGET}")
        print(f"  [OK] SDK baseline: mcp=={SDK_BASELINE}")
        print()
        print("  Start here:  uv run python scripts/run_lesson.py 00")
        print("  Run tests:   uv run pytest tests/phase0 -v")
    else:
        print(f"  [WARN] {len(issues)} issue(s) found:")
        for issue in issues:
            print(f"      - {issue}")
        print()
        print("  Resolve the issues above before starting the curriculum.")
        sys.exit(1)
    print()


if __name__ == "__main__":
    main()
