# AI-Driven DevOps Assignments 4.2–4.5

This repository brings together four complete Python projects for the AI-Driven
DevOps assignments. Each project is also maintained in its own GitHub
repository; this repository provides one place to browse the full submission
and its reports.

## Projects

| Assignment | Project | Description | Standalone repository |
|---|---|---|---|
| 4.2 | [Smart Build-Cache Invalidation](smart-build-cache-invalidation/) | Dependency-aware, content-hash build cache with automatic invalidation. | [smart-build-cache-invalidation](https://github.com/mananyamallikarjun16/smart-build-cache-invalidation) |
| 4.3 | [Dynamic Test-Subset Routing](dynamic-test-subset-routing/) | Maps changed files to affected tests, with a safe full-suite fallback. | [dynamic-test-subset-routing](https://github.com/mananyamallikarjun16/dynamic-test-subset-routing) |
| 4.4 | [LLM Build/Error-Log Summarization](llm-build-error-log-summarization/) | Extracts build errors and creates Markdown summaries, with an offline fallback. | [llm-build-error-log-summarization](https://github.com/mananyamallikarjun16/llm-build-error-log-summarization) |
| 4.5 | [Build-Failure Prediction](build-failure-prediction/) | Trains and evaluates a model that estimates build-failure risk. | [build-failure-prediction](https://github.com/mananyamallikarjun16/build-failure-prediction) |

## Run a project locally

From the project directory, create and activate a virtual environment, install
dependencies, and run tests:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pytest -v
```

Each project README provides its demo command, sample input details, and
project-specific setup instructions.

## Continuous integration

The root [GitHub Actions workflow](.github/workflows/ci.yml) runs a separate
Python 3.12 test and demo job for each project on pushes and pull requests.
Each project also retains its own CI workflow in its standalone repository.

## Reports and submission

- Detailed reports: [reports/](reports/)
- Four individual project archives and one combined archive: ZIP files in the
  repository root
- Submission instructions, screenshot checklist, and Classroom steps:
  [SUBMISSION_GUIDE.md](SUBMISSION_GUIDE.md)

The PDFs include screenshot placeholders. Replace them with genuine screenshots
of local execution and GitHub Actions before submitting.
