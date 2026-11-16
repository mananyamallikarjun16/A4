from logsummary import analyze_log, render_markdown


def test_extracts_errors_and_identifies_missing_dependency() -> None:
    analysis = analyze_log(
        "Traceback (most recent call last):\n"
        "ModuleNotFoundError: No module named 'requests'\n"
    )
    assert any("ModuleNotFoundError" in line for line in analysis["errors"])
    assert "dependency" in analysis["cause"]


def test_empty_log_has_readable_summary() -> None:
    report = render_markdown(analyze_log("Build completed with warnings only"), "build.log", "offline")
    assert "No explicit error lines detected" in report
    assert "Suggested next steps" in report


def test_unavailable_package_error_has_targeted_suggestion() -> None:
    analysis = analyze_log(
        "ERROR: Could not find a version that satisfies the requirement missing-library==9.9\n"
        "ERROR: No matching distribution found for missing-library==9.9\n"
    )
    assert "package name or pinned version" in analysis["cause"]
