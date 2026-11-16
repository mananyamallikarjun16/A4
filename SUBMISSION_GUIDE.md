# Assignment 4.2–4.5 Submission Guide

## Local deliverables

This workspace contains four independent Git repositories and four PDF reports.
The ZIP files include each project folder separately and all four projects
together. The PDFs contain project-specific steps, code excerpts, test results
recorded from local execution, and clearly labeled screenshot placeholders.

## GitHub repositories

The combined submission repository is
https://github.com/mananyamallikarjun16/A4. Its root GitHub Actions workflow
runs tests and a demo for all four project folders on pushes and pull requests.

These four public repositories have been created in the signed-in GitHub
account:

1. `smart-build-cache-invalidation`
2. `dynamic-test-subset-routing`
3. `llm-build-error-log-summarization`
4. `build-failure-prediction`

Each local project has its `origin` remote configured. Open PowerShell in the
project directory and run:

```powershell
git push -u origin main
```

If Git prompts for authentication, finish the Git Credential Manager browser
sign-in. Do not paste a password or token into source code. Verify the pushed
files on each repository homepage and check **Actions** for the first workflow
run.

## Intentional CI failure exercise

Use a test file in one project and temporarily change an assertion to an
incorrect expected result. Commit and push that change. In GitHub, open
**Actions**, select **Python CI**, open the failed run, select the failed job,
and expand the `python -m pytest -v` step. The red check and traceback show the
test name, expected value, and actual value. Restore the original correct
assertion in a new commit and push it. Wait for the new run and confirm the green
check before submission. Never leave the intentional failure in `main`.

## Genuine screenshots

The PDF screenshot boxes are intentionally blank: this environment did not
capture your VS Code window or your authenticated GitHub account. Capture the
real VS Code project tree, demo output, passing local tests, repository pages,
successful and failed Actions runs, expanded failure log, and final successful
run after you perform those steps. Paste the images into the corresponding PDF
placeholders or submit them separately. Do not label placeholders as screenshots.

## Google Classroom

1. Complete the GitHub pushes and verify each URL and workflow status.
2. Fill in the student/course/date fields on each report.
3. Replace screenshot placeholders with genuine screenshots.
4. Upload the four PDF reports and, if requested, the four individual ZIPs or
   the combined ZIP to the appropriate Google Classroom assignment.
5. Paste the four verified repository URLs into the Classroom submission text.
6. Reopen the submission page to confirm all attachments and links are present,
   then click **Turn in**.
