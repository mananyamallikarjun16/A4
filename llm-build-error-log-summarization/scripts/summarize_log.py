"""Summarize a log with the optional API or the offline rule-based analyzer."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from logsummary import analyze_log, render_markdown, summarize_with_llm
import os
import urllib.error


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("log_file", type=Path)
    parser.add_argument("--output", type=Path, default=Path("build-summary.md"))
    parser.add_argument("--llm", action="store_true", help="Try the API when OPENAI_API_KEY is set")
    args = parser.parse_args()

    text = args.log_file.read_text(encoding="utf-8", errors="replace")
    report: str
    mode = "offline"
    api_key = os.environ.get("OPENAI_API_KEY")
    if args.llm and api_key:
        try:
            report = summarize_with_llm(text, api_key, os.environ.get("OPENAI_MODEL", "gpt-4o-mini"))
            mode = "LLM API"
        except (urllib.error.URLError, TimeoutError, ValueError, KeyError) as error:
            print(f"LLM request failed ({error}); using the offline analyzer.", file=sys.stderr)
            report = render_markdown(analyze_log(text), args.log_file.name, mode)
    else:
        if args.llm and not api_key:
            print("OPENAI_API_KEY is not set; using the offline analyzer.", file=sys.stderr)
        report = render_markdown(analyze_log(text), args.log_file.name, mode)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(report.rstrip() + "\n", encoding="utf-8")
    print(f"Summary written to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
