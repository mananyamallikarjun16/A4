# Dynamic Test-Subset Routing

This project maps changed paths to module tests and also selects tests for
downstream dependent modules. Shared configuration changes, unmapped files, and
empty change lists safely fall back to the complete test suite.

## Setup and use

Requires Python 3.10+ and Git.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pytest -v
python scripts\route_tests.py --files src\calculator.py --dry-run
python scripts\route_tests.py --files src\calculator.py
```

For repository changes, run
`python scripts\route_tests.py --base origin/main`. The tool executes
`git diff --name-only`, prints its decision, then runs the selected pytest paths.
Use `--dry-run` to inspect routing without executing the tests.

## Important files

- `routing/router.py` matches glob patterns, computes dependent-module closure,
  and chooses a safe full-suite fallback.
- `test-routing.json` declares source/test mappings, dependencies and shared
  configuration paths.
- `scripts/route_tests.py` obtains changed paths from Git or explicit arguments
  and invokes pytest with the selected paths.
- `tests/` covers sample application behavior, dependency routing, and fallback.
- `.github/workflows/ci.yml` runs all tests and a routing dry run on Python 3.12.

## GitHub Actions and failure demonstration

Every push and pull request runs `python -m pytest -v`; the CI workflow also
prints a dry-run route. To demonstrate a failed red check, temporarily change
the expected output in `tests/test_calculator.py`, commit and push it, then open
**Actions → Python CI → failed run → test** to see the assertion. Revert that
test expectation in a new commit and push; the resulting successful run shows
the green check. Do not leave an intentional failure in the final branch.

## Publish

The public repository is available at
https://github.com/mananyamallikarjun16/dynamic-test-subset-routing. The remote
is configured locally; push the main branch with:

```powershell
git push -u origin main
```
