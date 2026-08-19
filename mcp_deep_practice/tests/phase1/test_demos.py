"""
tests/phase1/test_demos.py

Demo Execution Tests for Phase 1 (Lessons 00–08).

Executes every demo.py script directly and asserts clean exit code 0.
"""

from __future__ import annotations

import pathlib
import subprocess
import sys
import pytest

LESSONS_ROOT = pathlib.Path(__file__).parent.parent.parent / "lessons"

DEMOS = [
    "00_protocol_foundations/demo.py",
    "01_json_rpc/demo.py",
    "02_mcp_architecture/demo.py",
    "03_python_sdk_v2/demo.py",
    "04_tools/demo.py",
    "05_resources/demo.py",
    "06_prompts/demo.py",
    "07_content_and_schemas/demo.py",
    "08_stdio_transport/demo.py",
]


@pytest.mark.parametrize("demo_relpath", DEMOS)
def test_demo_executes_cleanly(demo_relpath: str) -> None:
    demo_path = LESSONS_ROOT / demo_relpath
    assert demo_path.exists(), f"Demo file '{demo_path}' does not exist."

    res = subprocess.run(
        [sys.executable, str(demo_path)],
        capture_output=True,
        text=True,
        timeout=15,
    )

    assert res.returncode == 0, (
        f"Demo '{demo_relpath}' failed with exit code {res.returncode}.\n"
        f"STDOUT:\n{res.stdout}\n"
        f"STDERR:\n{res.stderr}"
    )
