"""
lessons/00_protocol_foundations/test_exercise.py

Executable specification for Lesson 00 exercise.
Validates the learner's scenario architectural analysis.
"""

from __future__ import annotations

import importlib
import pytest

ex = importlib.import_module("lessons.00_protocol_foundations.exercise")


def test_evaluate_scenario_1_non_ai_microservice() -> None:
    eval1 = ex.evaluate_scenario(1)
    assert isinstance(eval1, ex.ScenarioEvaluation)
    assert eval1.scenario_id == 1
    assert eval1.selected_strategy in (ex.ArchitectureStrategy.REST, ex.ArchitectureStrategy.DIRECT_TOOL)
    assert len(eval1.justification) > 20
    assert len(eval1.primary_benefit) > 10


def test_evaluate_scenario_2_ide_tooling() -> None:
    eval2 = ex.evaluate_scenario(2)
    assert isinstance(eval2, ex.ScenarioEvaluation)
    assert eval2.scenario_id == 2
    assert eval2.selected_strategy == ex.ArchitectureStrategy.MCP
    assert len(eval2.justification) > 20


def test_evaluate_scenario_3_multi_saas() -> None:
    eval3 = ex.evaluate_scenario(3)
    assert isinstance(eval3, ex.ScenarioEvaluation)
    assert eval3.scenario_id == 3
    assert eval3.selected_strategy in (ex.ArchitectureStrategy.MCP, ex.ArchitectureStrategy.COMBINATION)
    assert len(eval3.justification) > 20


def test_evaluate_scenario_4_web_app_crud() -> None:
    eval4 = ex.evaluate_scenario(4)
    assert isinstance(eval4, ex.ScenarioEvaluation)
    assert eval4.scenario_id == 4
    assert eval4.selected_strategy == ex.ArchitectureStrategy.REST
    assert len(eval4.justification) > 20


def test_evaluate_scenario_5_shared_tool_catalog() -> None:
    eval5 = ex.evaluate_scenario(5)
    assert isinstance(eval5, ex.ScenarioEvaluation)
    assert eval5.scenario_id == 5
    assert eval5.selected_strategy == ex.ArchitectureStrategy.MCP
    assert len(eval5.justification) > 20


def test_evaluate_scenario_6_agent_negotiation() -> None:
    eval6 = ex.evaluate_scenario(6)
    assert isinstance(eval6, ex.ScenarioEvaluation)
    assert eval6.scenario_id == 6
    assert eval6.selected_strategy == ex.ArchitectureStrategy.A2A
    assert len(eval6.justification) > 20


def test_evaluate_all_scenarios_completeness() -> None:
    all_evals = ex.evaluate_all_scenarios()
    assert len(all_evals) == 6
    for item in all_evals:
        assert isinstance(item.selected_strategy, ex.ArchitectureStrategy)
        assert len(item.justification.strip()) > 15
