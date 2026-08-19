"""
tests/phase1/test_exercise_templates.py

Learner Exercise Template Incompleteness Tests for Phase 1.

Verifies that `exercise.py` in each lesson contains TODO markers and
is not prematurely solved, guaranteeing that the learner has to implement
the solutions.
"""

from __future__ import annotations

import pathlib
import pytest

LESSONS_ROOT = pathlib.Path(__file__).parent.parent.parent / "lessons"

LESSON_EXERCISES = [
    "00_protocol_foundations/exercise.py",
    "01_json_rpc/exercise.py",
    "02_mcp_architecture/exercise.py",
    "03_python_sdk_v2/exercise.py",
    "04_tools/exercise.py",
    "05_resources/exercise.py",
    "06_prompts/exercise.py",
    "07_content_and_schemas/exercise.py",
    "08_stdio_transport/exercise.py",
]


@pytest.mark.parametrize("exercise_relpath", LESSON_EXERCISES)
def test_exercise_contains_todos(exercise_relpath: str) -> None:
    ex_path = LESSONS_ROOT / exercise_relpath
    assert ex_path.exists(), f"Exercise '{ex_path}' does not exist."

    content = ex_path.read_text(encoding="utf-8")
    assert "TODO" in content, f"Exercise '{exercise_relpath}' must contain 'TODO' markers for the learner."
    assert (
        "raise NotImplementedError" in content or "..." in content or "# @" in content
    ), f"Exercise '{exercise_relpath}' must have scaffolded/unimplemented sections."
