# LLM-Based Build/Error-Log Summarization

Reads a build log, extracts important failure lines, infers likely causes, and
writes a Markdown report. Offline analysis works without credentials. With
`--llm` and `OPENAI_API_KEY`, the project can ask the OpenAI chat-completions API
for an additional natural-language diagnosis; API/network failures are reported
and fall back to the offline analyzer.

## Setup and run

Requires Python 3.10+.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python scripts\summarize_log.py sample\build.log --output summary.md
python scripts\summarize_log.py sample\build.log --llm --output summary.md
python -m pytest -v
```

Set `OPENAI_API_KEY` in your environment to enable the optional API. The
`OPENAI_MODEL` variable can override the default `gpt-4o-mini`. Never commit an
API key. The GitHub workflow deliberately runs offline so it needs no secret,
network service, or paid API usage.

## Important files

- `logsummary/summarizer.py` extracts errors, applies offline root-cause rules,
  formats Markdown, and makes an optional API request using Python's standard
  library.
- `scripts/summarize_log.py` is the command-line entry point.
- `sample/build.log` is a safe example input; `tests/` cover offline analysis.
- `.github/workflows/ci.yml` runs tests and produces a sample summary on Python
  3.12 for every push and pull request.

## CI failure demonstration

The workflow runs pytest, so an intentional bad expectation in a test produces
a red check and a visible traceback under **Actions → Python CI → failed run →
test**. Restore the original expectation in a follow-up commit; a green check
appears once the new workflow run passes. To inspect the summarizer in CI,
expand the `run: python scripts\summarize_log.py...` step and review its output.

## Publish

The public repository is available at
https://github.com/mananyamallikarjun16/llm-build-error-log-summarization. The
remote is configured locally; push the main branch with:

```powershell
git push -u origin main
```
