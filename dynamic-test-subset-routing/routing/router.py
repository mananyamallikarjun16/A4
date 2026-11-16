"""Plan a minimal test selection with a safe full-suite fallback."""

from __future__ import annotations

import fnmatch
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class RoutePlan:
    test_paths: tuple[str, ...]
    modules: tuple[str, ...]
    full_suite: bool
    reason: str


class TestRouter:
    __test__ = False

    def __init__(self, config: dict[str, Any]) -> None:
        self.modules = config.get("modules", {})
        self.all_tests = tuple(config.get("all_tests", ["tests"]))
        self.full_suite_patterns = tuple(config.get("full_suite_patterns", []))

    def plan(self, changed_files: list[str]) -> RoutePlan:
        files = [Path(name).as_posix() for name in changed_files]
        if not files:
            return self._full("No changed files were provided")

        for changed in files:
            if any(fnmatch.fnmatchcase(changed, pattern) for pattern in self.full_suite_patterns):
                return self._full(f"{changed} affects shared configuration")

        matched: set[str] = set()
        unmatched: list[str] = []
        for changed in files:
            file_matches = {
                name
                for name, details in self.modules.items()
                if any(
                    fnmatch.fnmatchcase(changed, pattern)
                    for pattern in details.get("patterns", [])
                )
            }
            if file_matches:
                matched.update(file_matches)
            else:
                unmatched.append(changed)
        if unmatched:
            return self._full(f"Unmapped changed file(s): {', '.join(unmatched)}")

        pending = list(matched)
        while pending:
            name = pending.pop()
            for dependent, details in self.modules.items():
                if name in details.get("depends_on", []) and dependent not in matched:
                    matched.add(dependent)
                    pending.append(dependent)

        tests = sorted(
            {
                test
                for name in matched
                for test in self.modules[name].get("tests", [])
            }
        )
        if not tests:
            return self._full("No tests are mapped to the changed modules")
        return RoutePlan(tuple(tests), tuple(sorted(matched)), False, "Mapped changes and dependents")

    def _full(self, reason: str) -> RoutePlan:
        return RoutePlan(self.all_tests, (), True, reason)
