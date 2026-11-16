"""Create reproducible ZIP archives for the four assignment projects."""

from __future__ import annotations

from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parent
PROJECTS = [
    "smart-build-cache-invalidation",
    "dynamic-test-subset-routing",
    "llm-build-error-log-summarization",
    "build-failure-prediction",
]
EXCLUDED_DIRS = {".git", ".pytest_cache", "__pycache__", ".venv", ".cache", "output"}


def add_project(archive: ZipFile, folder_name: str) -> None:
    project = ROOT / folder_name
    for path in sorted(project.rglob("*")):
        relative = path.relative_to(project)
        if any(part in EXCLUDED_DIRS for part in relative.parts):
            continue
        if path.is_file() and path.suffix not in {".pyc", ".pyo"}:
            archive.write(path, (Path(folder_name) / relative).as_posix())


def main() -> None:
    for name in PROJECTS:
        target = ROOT / f"{name}.zip"
        with ZipFile(target, "w", ZIP_DEFLATED) as archive:
            add_project(archive, name)
        print(f"Created {target.name} ({target.stat().st_size:,} bytes)")

    combined = ROOT / "all-four-assignments.zip"
    with ZipFile(combined, "w", ZIP_DEFLATED) as archive:
        for name in PROJECTS:
            add_project(archive, name)
    print(f"Created {combined.name} ({combined.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
