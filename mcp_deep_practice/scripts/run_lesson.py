#!/usr/bin/env python
"""
scripts/run_lesson.py

MCP Deep Practice Lab — Lesson Navigator

Usage:
    uv run python scripts/run_lesson.py <lesson_number>

Example:
    uv run python scripts/run_lesson.py 00
    uv run python scripts/run_lesson.py 03
"""

from __future__ import annotations

import pathlib
import sys

# Ensure UTF-8 output encoding on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


LESSON_MAP = {
    "00": ("00_protocol_foundations", "Protocol Foundations", "CORE", "1", "Phase 0 Foundation"),
    "01": ("01_json_rpc", "JSON-RPC 2.0", "CORE", "1", "Lesson 00"),
    "02": ("02_mcp_architecture", "MCP Architecture", "CORE", "1", "Lessons 00-01"),
    "03": ("03_python_sdk_v2", "Python SDK v2", "CORE", "1", "Lessons 00-02"),
    "04": ("04_tools", "Tools", "CORE", "1", "Lesson 03"),
    "05": ("05_resources", "Resources", "CORE", "1", "Lesson 03"),
    "06": ("06_prompts", "Prompts", "CORE", "1", "Lessons 03-05"),
    "07": ("07_content_and_schemas", "Content & Schemas", "CORE", "1", "Lessons 03-04"),
    "08": ("08_stdio_transport", "stdio Transport", "CORE", "1", "Lessons 01-03"),
    "09": ("09_streamable_http", "Streamable HTTP", "CORE", "2", "Phase 1"),
    "10": ("10_stateless_mcp", "Stateless MCP [MODERN]", "CORE", "2", "Lesson 09"),
    "11": ("11_discovery_and_versioning", "Discovery & Versioning", "CORE", "2", "Lessons 09-10"),
    "12": ("12_multi_round_trip", "Multi Round-Trip Requests", "CORE", "2", "Lesson 10"),
    "13": ("13_subscriptions_and_notifications", "Subscriptions & Notifications", "CORE", "2", "Lesson 09"),
    "14": ("14_authorization", "Authorization", "CORE", "3", "Phase 2"),
    "15": ("15_security", "MCP Security", "CORE", "3", "Lesson 14"),
    "16": ("16_multi_server_clients", "Multi-Server Clients", "CORE", "3", "Lessons 02, 16"),
    "17": ("17_reliability", "Reliability Engineering", "CORE", "3", "Phase 2"),
    "18": ("18_testing_and_inspector", "Testing & MCP Inspector", "CORE", "3", "Phase 1-2"),
    "19": ("19_observability", "Observability", "CORE", "3", "Phase 2"),
    "20": ("20_deployment_and_scaling", "Deployment & Scaling", "CORE", "3", "Phase 2"),
    "21": ("21_extensions", "Extensions Framework", "EXTENSION", "4", "Phase 2-3"),
    "22": ("22_mcp_apps", "MCP Apps", "EXTENSION", "4", "Lesson 21"),
    "23": ("23_tasks", "Tasks [SDK NOT_IMPLEMENTED]", "EXTENSION", "4", "Phase 2"),
    "24": ("24_agent_integration", "Agent Integration", "CORE", "5", "Phase 1-3"),
    "25": ("25_v1_to_v2_migration", "v1 to v2 Migration", "CORE", "5", "Phase 1-4"),
}

NO_FRAMEWORK_MAGIC_CHECKLIST = """
+-----------------------------------------------------------------+
|               "No Framework Magic" Inspection                   |
|  Answer these questions before marking this lesson complete:    |
+-----------------------------------------------------------------+
|  1. What JSON-RPC method is sent over the wire?                 |
|  2. What does the request body contain (params, _meta)?         |
|  3. Which HTTP headers exist, if HTTP transport is used?        |
|  4. What does a successful response look like?                  |
|  5. What does an error response look like?                      |
|  6. Which state belongs to the protocol vs. the application?   |
|  7. What happens if the server process crashes midway?          |
|  8. What happens if the request is duplicated (client retry)?  |
|  9. How does this work across two load-balanced replicas?       |
+-----------------------------------------------------------------+
"""

LEARNING_STAGES = """
Learning Progression (Observe -> Explain -> Modify -> Debug -> Build):
  Stage A (Observe):   Run demo.py to see working behavior
  Stage B (Explain):   Read concepts.md and answer questions.md
  Stage C (Modify):    Complete TODOs in exercise.py
  Stage D (Debug):     Fix intentional edge-cases in exercise.py
  Stage E (Build):     Solve challenge.md and pass test_exercise.py
"""


def print_lesson(lesson_id: str) -> None:
    if lesson_id not in LESSON_MAP:
        print(f"Unknown lesson: {lesson_id}")
        print(f"Available: {', '.join(sorted(LESSON_MAP.keys()))}")
        sys.exit(1)

    dir_name, title, status, phase, prereqs = LESSON_MAP[lesson_id]
    lessons_root = pathlib.Path(__file__).parent.parent / "lessons"
    lesson_dir = lessons_root / dir_name

    print()
    print("=" * 68)
    print(f"  Lesson {lesson_id}: {title}")
    print(f"  Phase: {phase}  |  Status: {status}")
    print(f"  Prerequisites: {prereqs}")
    print(f"  Protocol: 2026-07-28  |  SDK: mcp==2.0.0")
    print("=" * 68)

    # Check if lesson is created yet
    if not lesson_dir.exists():
        print()
        print(f"  [*] This lesson has not been created yet.")
        print(f"      It will be built in Phase {phase} of the curriculum.")
        print()
        print(f"  Check docs/learning_map.md for the phase schedule.")
        return

    # List lesson files
    print()
    print("  Lesson Files & Concepts:")
    for f in sorted(lesson_dir.iterdir()):
        size = f.stat().st_size if f.is_file() else 0
        marker = "[DIR] " if f.is_dir() else "[FILE]"
        print(f"    {marker} {f.name:<30} {size:>6} bytes")

    # Read objectives from README if available
    readme = lesson_dir / "README.md"
    if readme.exists():
        content = readme.read_text(encoding="utf-8")
        lines = content.split("\n")
        in_objectives = False
        objectives: list[str] = []
        for line in lines:
            if "learning objective" in line.lower():
                in_objectives = True
                continue
            if in_objectives:
                if line.startswith("#") and not line.startswith("## 1"):
                    break
                if line.strip().startswith(("1.", "2.", "3.", "4.", "5.", "6.", "- ", "* ")):
                    objectives.append(line.strip())
        if objectives:
            print()
            print("  Learning Objectives:")
            for obj in objectives[:8]:
                print(f"    {obj}")

    print()
    print("  Commands & Workflow:")
    print(f"    Demo:        uv run python lessons/{dir_name}/demo.py")
    print(f"    Concepts:    cat lessons/{dir_name}/concepts.md")
    print(f"    Exercise:    edit lessons/{dir_name}/exercise.py")
    print(f"    Test:        uv run pytest lessons/{dir_name}/test_exercise.py -v")
    print(f"    Challenge:   cat lessons/{dir_name}/challenge.md")
    print(f"    Questions:   cat lessons/{dir_name}/questions.md")

    print()
    print("  Completion Criteria:")
    print("    1. demo.py runs and output is fully understood.")
    print("    2. concepts.md read and questions.md answered.")
    print("    3. exercise.py modified and test_exercise.py passes 100%.")
    print("    4. challenge.md designed/implemented.")

    print(LEARNING_STAGES)
    print(NO_FRAMEWORK_MAGIC_CHECKLIST)
    print()


def main() -> None:
    if len(sys.argv) < 2:
        print()
        print("MCP Deep Practice Lab — Lesson Navigator")
        print()
        print("Usage:  uv run python scripts/run_lesson.py <lesson_number>")
        print()
        print("Available lessons:")
        for lid, (_, title, status, phase, prereqs) in sorted(LESSON_MAP.items()):
            print(f"  {lid}  Phase {phase}  [{status:<9}]  {title} (Prereqs: {prereqs})")
        print()
        sys.exit(0)

    lesson_id = sys.argv[1].zfill(2)
    print_lesson(lesson_id)


if __name__ == "__main__":
    main()
