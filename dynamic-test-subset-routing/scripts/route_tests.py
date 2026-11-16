"""Detect changed files, print the route, and optionally run selected tests."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from routing import TestRouter


def changed_files(base: str) -> list[str]:
    paths: set[str] = set()
    commands = [
        ["git", "diff", "--name-only", f"{base}...HEAD"],
        ["git", "diff", "--name-only", "HEAD"],
        ["git", "ls-files", "--others", "--exclude-standard"],
    ]
    for command in commands:
        result = subprocess.run(
            command,
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        paths.update(line for line in result.stdout.splitlines() if line.strip())
    return sorted(paths)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", help="Base branch or commit for git diff")
    parser.add_argument("--files", nargs="*", help="Explicit changed paths")
    parser.add_argument("--dry-run", action="store_true", help="Print selection without running pytest")
    args = parser.parse_args()

    try:
        files = args.files if args.files is not None else changed_files(args.base or "HEAD~1")
    except (subprocess.CalledProcessError, FileNotFoundError) as error:
        print(f"Could not determine changed files ({error}); running the full suite.", file=sys.stderr)
        files = []
    with (ROOT / "test-routing.json").open(encoding="utf-8") as config_file:
        plan = TestRouter(json.load(config_file)).plan(files)

    print(f"Changed files: {', '.join(files) if files else '(none)'}")
    print(f"Route: {'full suite' if plan.full_suite else ', '.join(plan.modules)}")
    print(f"Reason: {plan.reason}")
    print(f"Tests: {' '.join(plan.test_paths)}")
    if args.dry_run:
        return 0
    result = subprocess.run([sys.executable, "-m", "pytest", "-v", *plan.test_paths], cwd=ROOT)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
