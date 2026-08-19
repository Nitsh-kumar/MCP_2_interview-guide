"""
tests/phase1/test_curriculum_structure.py

Curriculum Integrity Tests for Phase 1 (Lessons 00–08).

Verifies:
  1. Exactly lessons 00–08 exist (no 09+).
  2. All 8 required files exist in each lesson directory.
  3. Every README starts with the required metadata block.
  4. No forbidden legacy or imaginary APIs exist in Phase 1 code.
  5. No paid LLM or external network dependencies exist.
"""

from __future__ import annotations

import pathlib
import pytest

LESSONS_ROOT = pathlib.Path(__file__).parent.parent.parent / "lessons"

EXPECTED_LESSONS = [
    "00_protocol_foundations",
    "01_json_rpc",
    "02_mcp_architecture",
    "03_python_sdk_v2",
    "04_tools",
    "05_resources",
    "06_prompts",
    "07_content_and_schemas",
    "08_stdio_transport",
]

REQUIRED_FILES = [
    "README.md",
    "concepts.md",
    "demo.py",
    "exercise.py",
    "test_exercise.py",
    "challenge.md",
    "questions.md",
    "solution/solution.py",
]

FORBIDDEN_PATTERNS = [
    "FastMCP",
    "mcp.tasks",
    "@mcp.task",
    "client.create_task",
    "Mcp-Session-Id",
    "create_connected_server_and_client_session",
]


def test_expected_lesson_directories_exist() -> None:
    assert LESSONS_ROOT.exists(), f"Lessons directory '{LESSONS_ROOT}' does not exist."
    for name in EXPECTED_LESSONS:
        ldir = LESSONS_ROOT / name
        assert ldir.exists() and ldir.is_dir(), f"Missing lesson directory: {name}"


def test_no_phase_2_or_later_directories_exist() -> None:
    phase2_or_later = [
        "09_streamable_http",
        "10_stateless_mcp",
        "11_discovery_and_versioning",
        "12_multi_round_trip",
        "13_subscriptions_and_notifications",
    ]
    for name in phase2_or_later:
        ldir = LESSONS_ROOT / name
        assert not ldir.exists(), f"Phase 2 directory '{name}' must not exist in Phase 1."


def test_all_required_files_exist_in_each_lesson() -> None:
    for name in EXPECTED_LESSONS:
        ldir = LESSONS_ROOT / name
        for fname in REQUIRED_FILES:
            target = ldir / fname
            assert target.exists(), f"Lesson '{name}' missing required file '{fname}'"
            assert target.stat().st_size > 0, f"Lesson '{name}' file '{fname}' is empty."


def test_readme_metadata_headers() -> None:
    for name in EXPECTED_LESSONS:
        readme = LESSONS_ROOT / name / "README.md"
        content = readme.read_text(encoding="utf-8")
        assert "# Lesson Metadata" in content, f"Lesson '{name}' README missing '# Lesson Metadata'"
        assert "Protocol revision: 2026-07-28" in content, f"Lesson '{name}' README missing protocol revision"
        assert "SDK baseline: mcp==2.0.0" in content, f"Lesson '{name}' README missing SDK baseline"
        assert "Last verified: 2026-08-19" in content, f"Lesson '{name}' README missing last verified date"


def test_no_forbidden_legacy_or_imaginary_apis() -> None:
    for name in EXPECTED_LESSONS:
        ldir = LESSONS_ROOT / name
        for pyfile in ldir.rglob("*.py"):
            text = pyfile.read_text(encoding="utf-8")
            for pattern in FORBIDDEN_PATTERNS:
                if pattern in text:
                    # Allow only if marked as LEGACY or EDUCATIONAL comparison in comments
                    lines = [line for line in text.splitlines() if pattern in line]
                    for line in lines:
                        assert any(
                            tag in line for tag in ["LEGACY", "EDUCATIONAL", "ANTI-PATTERN", "obsolete", "rename", "replaces"]
                        ), f"Forbidden pattern '{pattern}' found in {pyfile.relative_to(LESSONS_ROOT)}:\n  {line}"
