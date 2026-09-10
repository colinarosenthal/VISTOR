"""
VISTOR Test Suite Runner

Discovers and runs every test_*.py module in this folder, each in its own
subprocess so a crash or sys.exit in one module can't abort the rest.
Excludes itself to avoid infinite recursion.

Run from the repo root: python src/tests/test_suite.py
"""

import subprocess
import sys

from pathlib import Path


def main():
    here = Path(__file__).resolve().parent
    this_file = Path(__file__).resolve().name

    modules = sorted(
        p for p in here.glob("test_*.py")
        if p.name != this_file
    )

    failures = []

    for module in modules:
        print(f"\n{'=' * 60}")
        print(f"RUNNING: {module.name}")
        print(f"{'=' * 60}")

        result = subprocess.run([sys.executable, str(module)])

        if result.returncode != 0:
            failures.append(module.name)

    print(f"\n{'=' * 60}")
    print("SUITE SUMMARY")
    print(f"{'=' * 60}")
    print(f"Ran {len(modules)} test modules.")

    if failures:
        print("FAILED:", ", ".join(failures))
        sys.exit(1)

    print("All test modules passed.")


if __name__ == "__main__":
    main()
