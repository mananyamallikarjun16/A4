"""Generate four student-friendly PDF reports from the checked-out project files."""

from __future__ import annotations

import json
import os
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parent
REPORTS = ROOT / "reports"
PROJECTS = [
    {
        "folder": "smart-build-cache-invalidation",
        "assignment": "Assignment 4.2",
        "title": "Smart Build-Cache Invalidation",
        "intro": (
            "Repeated builds waste time when their inputs have not changed. This project "
            "uses SHA-256 content fingerprints to decide whether a prior result can be "
            "reused. Inputs and declared module dependencies are tracked together, so "
            "changing a dependency causes an automatic cache miss."
        ),
        "objectives": [
            "Track build inputs and module-to-file dependencies.",
            "Hash file names and file contents to detect real changes.",
            "Distinguish cache hits from misses and rebuild after invalidation.",
            "Verify behavior with pytest and a Python 3.12 GitHub Actions workflow.",
        ],
        "tools": "Python, pathlib, hashlib, JSON, pytest, Git, and GitHub Actions.",
        "install": [
            "Create and activate a Python virtual environment.",
            "Install the project's requirements with `python -m pip install -r requirements.txt`.",
            "Run `python scripts/demo.py` twice to observe MISS followed by HIT.",
            "Edit sample/message.txt and run the demo again to see invalidation.",
            "Run `python -m pytest -v` to execute automated tests.",
        ],
        "dataset": "No training dataset is needed. The sample/message.txt file is a tracked source input used to demonstrate content-based invalidation.",
        "github": "The CI workflow runs tests for pushes and pull requests with Python 3.12. A deliberate failing assertion produces a red check and an expanded pytest traceback. Restoring the correct assertion and pushing again produces a green check.",
        "problems": "A timestamp-only cache can reuse stale outputs when a file is changed and its timestamp is preserved. Hashing file contents avoids this weakness. A missing declared input is reported explicitly rather than treated as a valid empty input.",
        "outcomes": "The student learns dependency tracking, deterministic content fingerprints, cache hit/miss behavior, atomic cache writes, unit testing, and CI feedback.",
        "repo": "smart-build-cache-invalidation",
        "screenshot_captions": [
            "VS Code Explorer showing the project folders and files.",
            "First demo execution showing the cache MISS and generated value.",
            "Second demo execution showing the cache HIT.",
            "Pytest output from a successful local run.",
            "GitHub repository homepage after publishing.",
            "GitHub Actions successful green run.",
            "GitHub Actions failed red run after a temporary test change.",
            "Expanded failed Actions log showing the exact assertion.",
            "Final successful green run after the fix.",
        ],
    },
    {
        "folder": "dynamic-test-subset-routing",
        "assignment": "Assignment 4.3",
        "title": "Dynamic Test-Subset Routing",
        "intro": (
            "Large test suites take longer when every test runs for every change. "
            "This project maps changed paths to affected modules and their dependent "
            "modules, then runs the mapped tests. If the change cannot be safely mapped, "
            "it selects the full suite."
        ),
        "objectives": [
            "Detect changed files from an explicit list or a Git diff.",
            "Map path patterns to modules and relevant test files.",
            "Follow module dependencies to include downstream tests.",
            "Use the full suite for empty, unmapped, or shared-configuration changes.",
            "Test routing and run CI on Python 3.12.",
        ],
        "tools": "Python, Git, JSON, fnmatch, subprocess, pytest, and GitHub Actions.",
        "install": [
            "Create and activate a virtual environment and install requirements.txt.",
            "Run `python -m pytest -v` for the project's own tests.",
            "Preview a route with `python scripts/route_tests.py --files src/calculator.py --dry-run`.",
            "Run the selected tests by omitting `--dry-run`.",
            "For a branch comparison, use `python scripts/route_tests.py --base origin/main`.",
        ],
        "dataset": "No separate dataset is needed. test-routing.json is the routing configuration: source patterns, tests, module dependencies, and paths that force a full-suite run.",
        "github": "The workflow runs the complete test suite for every push and pull request, then runs a routing dry run. The full CI suite is retained as a safety net while the router is demonstrated locally.",
        "problems": "Incorrectly selecting no tests can hide a regression. The router therefore falls back to all tests for an empty change list, unmapped path, shared configuration change, or module with no configured tests.",
        "outcomes": "The student learns Git change detection, path-based routing, dependency graph traversal, safe fallback design, test automation, and CI workflows.",
        "repo": "dynamic-test-subset-routing",
        "screenshot_captions": [
            "VS Code Explorer showing src, routing, scripts, and tests.",
            "Routing dry-run output for a calculator source change.",
            "Selected pytest cases passing.",
            "GitHub repository homepage after publishing.",
            "GitHub Actions successful green run.",
            "GitHub Actions failed red run after a temporary test change.",
            "Expanded failed Actions log showing the exact test error.",
            "Final successful green run after the fix.",
        ],
    },
    {
        "folder": "llm-build-error-log-summarization",
        "assignment": "Assignment 4.4",
        "title": "LLM-Based Build/Error-Log Summarization",
        "intro": (
            "Build logs can be long and difficult to diagnose. This project extracts "
            "important error lines, infers likely causes using offline rules, and writes "
            "a readable Markdown report. If explicitly enabled and an API key is "
            "available, an OpenAI-compatible chat-completions request can add an LLM "
            "summary; API failures are reported before the offline fallback is used."
        ),
        "objectives": [
            "Read build/error logs and identify error and failure messages.",
            "Infer likely root causes and suggest practical fixes.",
            "Create a readable Markdown report.",
            "Offer optional API assistance without requiring a secret for offline use or CI.",
            "Test and run the workflow on Python 3.12.",
        ],
        "tools": "Python, regular expressions, urllib, JSON, Markdown, pytest, and GitHub Actions.",
        "install": [
            "Create and activate a virtual environment and install requirements.txt.",
            "Run `python scripts/summarize_log.py sample/build.log --output summary.md`.",
            "Read summary.md to review extracted errors, cause, and next steps.",
            "Run `python -m pytest -v`.",
            "Optionally set OPENAI_API_KEY and use --llm; never commit the key.",
        ],
        "dataset": "sample/build.log contains a short example dependency-resolution failure. It is an input example, not a model-training dataset.",
        "github": "CI uses the deterministic offline analyzer, avoiding secrets and paid services. It runs pytest and generates a sample summary on pushes and pull requests.",
        "problems": "LLM services may be unavailable, costly, or require credentials. Offline analysis is the default and always available. When an explicitly requested API call fails, the CLI prints the failure reason and then uses the offline analyzer. Log text is treated as untrusted input in the LLM prompt.",
        "outcomes": "The student learns log parsing, rule-based diagnosis, optional language-model integration, credential hygiene, graceful fallback, and Markdown reporting.",
        "repo": "llm-build-error-log-summarization",
        "screenshot_captions": [
            "VS Code Explorer showing the log summarizer project.",
            "CLI output showing the generated Markdown report.",
            "Markdown report opened with errors, cause, and suggested fixes.",
            "Successful pytest output.",
            "GitHub repository homepage after publishing.",
            "GitHub Actions successful green run.",
            "GitHub Actions failed red run after a temporary test change.",
            "Expanded failed Actions log showing the exact traceback.",
            "Final successful green run after the fix.",
        ],
    },
    {
        "folder": "build-failure-prediction",
        "assignment": "Assignment 4.5",
        "title": "Build-Failure Prediction",
        "intro": (
            "Historical CI data can help estimate the risk of a future failure. "
            "This project validates a CSV, preprocesses numeric and categorical "
            "features, trains a logistic-regression classifier, evaluates it, and "
            "reports a failure probability with a Low, Medium, or High label."
        ),
        "objectives": [
            "Load and validate historical build records.",
            "Scale numeric data and encode categorical branch data.",
            "Train a scikit-learn model and evaluate accuracy and ROC AUC.",
            "Predict probability and map it to an explicit risk category.",
            "Run tests and a sample prediction in Python 3.12 CI.",
        ],
        "tools": "Python, pandas, scikit-learn, joblib, pytest, Git, and GitHub Actions.",
        "install": [
            "Create and activate a virtual environment and install requirements.txt.",
            "Run `python -m pytest -v`.",
            "Run `python scripts/predict_build.py data/historical_builds.csv`.",
            "Use `--json` for machine-readable evaluation and prediction output.",
        ],
        "dataset": "data/historical_builds.csv contains synthetic illustrative records with changed-file count, number of tests, average duration, flaky-test count, recent failure rate, dependency-change flag, branch, and the binary failed target. It is deliberately small for a student demonstration and must not be presented as production evidence.",
        "github": "CI installs the ML dependencies on Python 3.12, executes pytest, and trains/evaluates the sample model. The pipeline requires no external service or secret.",
        "problems": "A small synthetic dataset can make evaluation results unstable and unrealistic. This sample's held-out split has only 10 rows and produced 1.00 accuracy and 1.00 ROC AUC in the local run; those scores reflect the deliberately separable sample and are not evidence of production performance. Production use requires representative, time-ordered records, leakage checks, calibration, and evaluation appropriate for class imbalance. The risk cutoffs are configurable policy choices, not universal safety thresholds.",
        "outcomes": "The student learns dataset validation, preprocessing pipelines, classification, held-out evaluation, probability interpretation, risk labeling, and reproducible CI.",
        "repo": "build-failure-prediction",
        "screenshot_captions": [
            "VS Code Explorer showing the model, dataset, scripts, and tests.",
            "Training/evaluation and sample prediction output.",
            "Successful pytest output.",
            "GitHub repository homepage after publishing.",
            "GitHub Actions successful green run.",
            "GitHub Actions failed red run after a temporary test change.",
            "Expanded failed Actions log showing the exact traceback.",
            "Final successful green run after the fix.",
        ],
    },
]


def build_styles():
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name="CoverTitle", parent=styles["Title"], fontName="Helvetica-Bold",
        fontSize=26, leading=32, textColor=colors.HexColor("#14365D"),
        alignment=TA_CENTER, spaceAfter=16,
    ))
    styles.add(ParagraphStyle(
        name="CoverSub", parent=styles["Normal"], fontSize=14, leading=20,
        textColor=colors.HexColor("#277DA1"), alignment=TA_CENTER,
    ))
    styles.add(ParagraphStyle(
        name="Section", parent=styles["Heading2"], fontName="Helvetica-Bold",
        fontSize=15, leading=19, textColor=colors.HexColor("#14365D"),
        spaceBefore=12, spaceAfter=8, keepWithNext=True,
    ))
    styles.add(ParagraphStyle(
        name="BodyCustom", parent=styles["BodyText"], fontSize=9.4,
        leading=14, spaceAfter=7,
    ))
    styles.add(ParagraphStyle(
        name="SmallCustom", parent=styles["BodyText"], fontSize=8,
        leading=11, spaceAfter=4,
    ))
    styles.add(ParagraphStyle(
        name="CodeCustom", fontName="Courier", fontSize=6.2,
        leading=7.6, leftIndent=5, rightIndent=5, backColor=colors.HexColor("#F2F5F8"),
        borderColor=colors.HexColor("#D4DEE8"), borderWidth=0.4,
        borderPadding=5, spaceAfter=8,
    ))
    return styles


def on_page(canvas, document):
    canvas.saveState()
    if document.page > 1:
        canvas.setStrokeColor(colors.HexColor("#D5DFE8"))
        canvas.line(18 * mm, 15 * mm, 192 * mm, 15 * mm)
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(colors.HexColor("#526579"))
        canvas.drawString(18 * mm, 10 * mm, "AI-Driven DevOps Assignment Report")
        canvas.drawRightString(192 * mm, 10 * mm, f"Page {document.page}")
    canvas.restoreState()


def project_tree(project: Path) -> str:
    rows = []
    for path in sorted(project.rglob("*")):
        if any(part in {".git", "__pycache__", ".pytest_cache", ".venv"} for part in path.parts):
            continue
        if path.is_file():
            rows.append(path.relative_to(project).as_posix())
    return "\n".join(rows)


def add_bullets(story, items, styles):
    for item in items:
        story.append(Paragraph(f"&bull; {escape(item)}", styles["BodyCustom"]))


def add_screenshots(story, captions, styles):
    story.append(Paragraph("Screenshot checklist and placeholders", styles["Section"]))
    story.append(Paragraph(
        "The boxes below are placeholders, not captured screenshots. Replace each "
        "box with a genuine image from your own VS Code run, GitHub repository, or "
        "GitHub Actions history after completing the account-dependent steps.",
        styles["BodyCustom"],
    ))
    for index, caption in enumerate(captions, 1):
        cell = Paragraph(
            f"<b>Screenshot {index}.</b> {escape(caption)}<br/><br/>"
            "<font color='#687A8A'>Insert genuine screenshot here.</font>",
            styles["SmallCustom"],
        )
        table = Table([[cell]], colWidths=[170 * mm], rowHeights=[23 * mm])
        table.setStyle(TableStyle([
            ("BOX", (0, 0), (-1, -1), 0.8, colors.HexColor("#92A9BD")),
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F7FAFC")),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ]))
        story.append(table)
        story.append(Spacer(1, 4 * mm))


def explain_file(repo, relative):
    explanations = {
        "smart-build-cache-invalidation": {
            "smartcache/cache.py": "Core cache implementation: hashes every declared input and dependency, validates JSON entries, rebuilds on fingerprint changes, and writes replacement entries atomically.",
            "smartcache/__init__.py": "Exports the public BuildCache and CacheResult types.",
            "scripts/demo.py": "Runnable example that uses a sample dependency and prints MISS/HIT, the output, and its fingerprint.",
            "tests/test_cache.py": "Checks first-build and repeated-hit behavior, dependency invalidation, and a clear error for a missing input.",
        },
        "dynamic-test-subset-routing": {
            "routing/router.py": "Matches changed paths to modules, follows dependent-module edges, and safely selects the complete test suite for uncertain changes.",
            "routing/__init__.py": "Exports the route plan and router for library use.",
            "scripts/route_tests.py": "Reads explicit paths or Git diffs (committed, staged/unstaged, and untracked changes), prints the plan, and optionally runs pytest.",
            "src/calculator.py": "Example source module with addition and mean functions.",
            "src/report.py": "Example downstream module that calls the calculator's mean function.",
            "tests/test_calculator.py": "Tests calculator behavior, including the empty-input error.",
            "tests/test_report.py": "Checks that the report uses the calculator result.",
            "tests/test_router.py": "Checks dependency expansion and the full-suite fallback for unmapped files.",
        },
        "llm-build-error-log-summarization": {
            "logsummary/summarizer.py": "Extracts log errors, applies offline root-cause rules, formats Markdown, and sends an optional API request using the standard library.",
            "logsummary/__init__.py": "Exports the analysis, Markdown rendering, and LLM request functions.",
            "scripts/summarize_log.py": "Reads the CLI input, optionally requests an LLM summary, reports API failures, and writes the Markdown output.",
            "tests/test_summarizer.py": "Checks missing-module extraction, likely-cause detection, and readable output for logs without explicit errors.",
        },
        "build-failure-prediction": {
            "buildpredict/model.py": "Validates the CSV, builds preprocessing and logistic-regression steps, evaluates a held-out split, predicts probabilities, labels risk, and supports model persistence.",
            "buildpredict/__init__.py": "Marks the model implementation as an importable package.",
            "scripts/predict_build.py": "Loads sample history, trains and evaluates the model, then prints a future-build risk prediction.",
            "tests/test_model.py": "Checks sample-model training, metric ranges, unknown branch handling, risk labels, and missing-column validation.",
        },
    }
    return explanations.get(repo, {}).get(relative, "Supporting project code used by the demo and automated test suite.")


def make_report(project_info, validation):
    folder = ROOT / project_info["folder"]
    output = REPORTS / f"{project_info['assignment'].lower().replace(' ', '-')}-{project_info['repo']}.pdf"
    styles = build_styles()
    story = [
        Spacer(1, 34 * mm),
        Paragraph(escape(project_info["assignment"]), styles["CoverSub"]),
        Spacer(1, 8 * mm),
        Paragraph(escape(project_info["title"]), styles["CoverTitle"]),
        Spacer(1, 8 * mm),
        Paragraph("AI-Driven DevOps | B.Tech Computer Science and Engineering", styles["CoverSub"]),
        Spacer(1, 34 * mm),
        Paragraph("<b>Student:</b> __________________________________________", styles["BodyCustom"]),
        Paragraph("<b>Course / section:</b> ____________________________________", styles["BodyCustom"]),
        Paragraph("<b>Submission date:</b> ____________________________________", styles["BodyCustom"]),
        Spacer(1, 28 * mm),
        Paragraph("Implementation report and reproducibility guide", styles["CoverSub"]),
        PageBreak(),
    ]

    sections = [
        ("1. Introduction", project_info["intro"]),
        ("2. Aim and objectives", None),
        ("3. Software and hardware requirements", None),
        ("4. Tools and technologies", project_info["tools"]),
        ("5. Project folder structure", None),
        ("6. Implementation steps", None),
        ("7. Important code files", None),
        ("8. Dataset / sample input", project_info["dataset"]),
        ("9. Installation and execution", None),
        ("10. Testing procedure and actual result", None),
        ("11. GitHub repository setup", None),
        ("12. GitHub Actions configuration", project_info["github"]),
        ("13. Intentional failure and recovery exercise", None),
        ("14. Problems encountered and solutions", project_info["problems"]),
        ("15. Learning outcomes", project_info["outcomes"]),
        ("16. Screenshot checklist", None),
        ("17. Conclusion", project_info["intro"] + " The code, tests, example inputs, and CI workflow are included in the companion project folder."),
    ]
    for title, body in sections:
        story.append(Paragraph(escape(title), styles["Section"]))
        if body:
            story.append(Paragraph(escape(body), styles["BodyCustom"]))
        elif title == "2. Aim and objectives":
            add_bullets(story, project_info["objectives"], styles)
        elif title == "3. Software and hardware requirements":
            story.append(Paragraph(
                "Software: Python 3.12 for CI (Python 3.10+ for local examples), "
                "pip, Git, a code editor such as VS Code, and internet access only "
                "for package installation and GitHub publishing. Hardware: a modern "
                "computer with about 2 GB free disk space and 4 GB RAM is sufficient "
                "for these small projects; no GPU is required.",
                styles["BodyCustom"],
            ))
        elif title == "5. Project folder structure":
            story.append(Preformatted(project_tree(folder), styles["CodeCustom"], maxLineLength=90))
        elif title == "6. Implementation steps":
            add_bullets(story, [
                "Create the project package, sample input, CLI/demo, focused tests, and CI workflow.",
                "Declare runtime/test dependencies in requirements.txt and ignore local caches or generated artifacts.",
                "Run the sample command and tests locally, then review the exact output.",
                "Create a GitHub repository, push the main branch, and inspect its first Actions run.",
                "Capture genuine screenshots only after the corresponding local or GitHub action has actually occurred.",
            ], styles)
        elif title == "7. Important code files":
            py_files = sorted(folder.rglob("*.py"))
            for path in py_files:
                relative = path.relative_to(folder).as_posix()
                story.append(Paragraph(f"<b>{escape(relative)}</b>", styles["SmallCustom"]))
                story.append(Paragraph(escape(explain_file(project_info["repo"], relative)), styles["BodyCustom"]))
                content = path.read_text(encoding="utf-8")
                story.append(Preformatted(content, styles["CodeCustom"], maxLineLength=96))
            extras = [
                folder / ".github" / "workflows" / "ci.yml",
                folder / "requirements.txt",
                *sorted(folder.glob("*.json")),
            ]
            for extra in extras:
                if not extra.is_file():
                    continue
                story.append(Paragraph(f"<b>{escape(extra.relative_to(folder).as_posix())}</b>", styles["SmallCustom"]))
                story.append(Preformatted(extra.read_text(encoding="utf-8"), styles["CodeCustom"], maxLineLength=96))
        elif title == "9. Installation and execution":
            add_bullets(story, project_info["install"], styles)
            story.append(Paragraph(
                "For Windows PowerShell, activate a virtual environment with "
                "<font name='Courier'>.\\.venv\\Scripts\\Activate.ps1</font>. "
                "Use the slash-separated command spelling in the report or the "
                "platform-appropriate path spelling shown in the project README.",
                styles["BodyCustom"],
            ))
        elif title == "10. Testing procedure and actual result":
            result = validation.get(project_info["repo"], {})
            if result.get("status") == "passed":
                text = (
                    f"Validated in this workspace with Python {escape(result.get('python', ''))}: "
                    f"{escape(str(result.get('passed', 0)))} test(s) passed and "
                    f"{escape(str(result.get('failed', 0)))} failed. "
                    f"Command: {escape(result.get('command', 'python -m pytest -v'))}."
                )
            else:
                text = "No successful execution result was recorded when this report was generated. Run the tests and regenerate the report before submission."
            story.append(Paragraph(escape(text), styles["BodyCustom"]))
            story.append(Paragraph(
                "The local interpreter version can differ from the Python 3.12 version "
                "used by GitHub Actions. A local pass does not claim that a remote "
                "workflow passed; verify the Actions run after publishing.",
                styles["BodyCustom"],
            ))
        elif title == "11. GitHub repository setup":
            story.append(Paragraph(
                f"The public repository <b>{escape(project_info['repo'])}</b> has been created "
                "in the signed-in GitHub account. The local project is committed on main, "
                "with its Git remote configured. Push with "
                "<font name='Courier'>git push -u origin main</font>. "
                f"Repository URL: https://github.com/mananyamallikarjun16/{escape(project_info['repo'])}.",
                styles["BodyCustom"],
            ))
        elif title == "13. Intentional failure and recovery exercise":
            add_bullets(story, [
                "Temporarily change a test assertion to an incorrect expected value.",
                "Commit and push the change. Open GitHub Actions and select the newest failed workflow run.",
                "Open the failing job and expand the pytest step; capture the test name and assertion traceback.",
                "Restore the correct expectation in a new commit and push it.",
                "Wait for the new run to complete, then capture the green check and final successful job.",
                "Do not leave the intentionally failing test in the submitted main branch.",
            ], styles)
        elif title == "16. Screenshot checklist":
            add_screenshots(story, project_info["screenshot_captions"], styles)

    story.append(Paragraph("Complete code and configuration excerpts", styles["Section"]))
    story.append(Paragraph(
        "The preceding code-file section reproduces each Python source and test file "
        "from the project as generated. The project directory remains the authoritative "
        "copy; the report should be regenerated if the code changes.",
        styles["BodyCustom"],
    ))
    REPORTS.mkdir(parents=True, exist_ok=True)
    document = SimpleDocTemplate(
        str(output), pagesize=A4, rightMargin=20 * mm, leftMargin=20 * mm,
        topMargin=18 * mm, bottomMargin=20 * mm, title=project_info["title"],
        author="B.Tech CSE - AI-Driven DevOps",
    )
    document.build(story, onFirstPage=on_page, onLaterPages=on_page)
    return output


def main():
    validation_file = ROOT / "validation-results.json"
    validation = json.loads(validation_file.read_text(encoding="utf-8")) if validation_file.exists() else {}
    for project_info in PROJECTS:
        output = make_report(project_info, validation)
        print(f"Created {output}")


if __name__ == "__main__":
    main()
