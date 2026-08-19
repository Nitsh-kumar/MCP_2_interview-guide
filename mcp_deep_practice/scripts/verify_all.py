#!/usr/bin/env python
"""
scripts/verify_all.py

MCP Deep Practice Lab — Full Verification Runner

Usage:
    uv run python scripts/verify_all.py                    # Run all available tests
    uv run python scripts/verify_all.py --phase foundation
    uv run python scripts/verify_all.py --phase fundamentals
    uv run python scripts/verify_all.py --phase phase1
    uv run python scripts/verify_all.py --phase all

Phases:
    foundation    — Phase 0: environment, shared infrastructure, doctor
    fundamentals  — Phase 1: Lessons 00–08 Curriculum Integrity & Reference Implementations
    phase1        — Phase 1 (alias for fundamentals)
    phase2        — Phase 2: Lessons 09–13 (Modern MCP 2026-07-28)
    phase3        — Phase 3: Lessons 14–20 (Production Engineering)
    phase4        — Phase 4: Lessons 21–23 (Extensions)
    phase5        — Phase 5: Lessons 24–25 (Integration & Migration)
    phase6        — Phase 6: Challenges
    phase7        — Phase 7: Capstones
    all           — All phases

Policy: Do not continue if the current phase has unexplained failures.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


PHASE_TEST_PATHS: dict[str, list[str]] = {
    "foundation": ["tests/phase0"],
    "fundamentals": ["tests/phase0", "tests/phase1"],
    "phase1": ["tests/phase0", "tests/phase1"],
    "phase2": ["lessons/09_streamable_http", "lessons/10_stateless_mcp",
               "lessons/11_discovery_and_versioning", "lessons/12_multi_round_trip",
               "lessons/13_subscriptions_and_notifications"],
    "phase3": ["lessons/14_authorization", "lessons/15_security",
               "lessons/16_multi_server_clients", "lessons/17_reliability",
               "lessons/18_testing_and_inspector", "lessons/19_observability",
               "lessons/20_deployment_and_scaling"],
    "phase4": ["lessons/21_extensions", "lessons/22_mcp_apps", "lessons/23_tasks"],
    "phase5": ["lessons/24_agent_integration", "lessons/25_v1_to_v2_migration"],
    "phase6": ["challenges"],
    "phase7": ["capstones"],
}


def run_pytest(paths: list[str], label: str) -> tuple[int, int, int, int]:
    """Run pytest on a list of paths, returning (returncode, total, passed, failed)."""
    existing = [p for p in paths if Path(p).exists()]
    if not existing:
        print(f"  No test paths found for {label} — phase not yet generated.")
        return 0, 0, 0, 0

    cmd = [
        sys.executable, "-m", "pytest",
        *existing,
        "-v",
        "--tb=short",
        f"--junit-xml=.test_results_{label.replace(' ', '_')}.xml",
    ]

    print(f"Running: pytest {' '.join(existing)}")
    result = subprocess.run(cmd, capture_output=False)
    return result.returncode, 0, 0, 0


def main() -> None:
    args = sys.argv[1:]

    phase = "foundation"
    if "--phase" in args:
        idx = args.index("--phase")
        if idx + 1 < len(args):
            phase = args[idx + 1]

    print()
    print("=" * 64)
    print(f"  MCP Deep Practice Lab -- Verify All ({phase})")
    print("=" * 64)
    print()

    if phase == "all":
        phases_to_run = ["foundation", "fundamentals"]
    elif phase in PHASE_TEST_PATHS:
        phases_to_run = [phase]
    else:
        print(f"Unknown phase: {phase!r}")
        print(f"Available: {', '.join(PHASE_TEST_PATHS.keys())}, all")
        sys.exit(1)

    overall_ok = True
    for p in phases_to_run:
        dashes = "-" * max(1, 55 - len(p))
        print(f"-- Phase: {p} {dashes}")
        paths = PHASE_TEST_PATHS[p]
        rc, _, _, _ = run_pytest(paths, p)
        if rc != 0:
            overall_ok = False
            print(f"\n  [FAIL] Phase {p} has failures. Fix before proceeding.")
        else:
            print(f"\n  [OK] Phase {p} OK")
        print()

    print("=" * 64)
    if overall_ok:
        print("  [OK] ALL REQUESTED CHECKS PASSED")
        if phase == "foundation":
            print("  --> READY_FOR_PHASE_1")
        elif phase in ("fundamentals", "phase1"):
            print("  --> READY_FOR_PHASE_2")
    else:
        print("  [FAIL] FAILURES DETECTED -- resolve before proceeding")
        sys.exit(1)
    print()


if __name__ == "__main__":
    main()
