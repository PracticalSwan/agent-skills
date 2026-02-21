"""
Code Review Checklist — Static Analysis for JavaScript/TypeScript

Performs basic static analysis on a JS/TS file and generates a review report.
Uses only Python standard library (regex-based, since ast cannot parse JS).

Checks:
  - Functions over 50 lines
  - Files over 300 lines
  - TODO / FIXME counts
  - console.log statements left in code
  - Deeply nested code (>3 levels of braces)
  - Magic numbers (numeric literals outside common patterns)
  - Long lines (>120 characters)
  - Empty catch blocks

Usage:
  python review-checklist.py <file_path> [--json]
"""

import re
import sys
import json
from pathlib import Path
from dataclasses import dataclass, field, asdict


@dataclass
class Issue:
    rule: str
    severity: str
    line: int
    message: str


@dataclass
class ReviewReport:
    file: str
    total_lines: int
    issues: list[Issue] = field(default_factory=list)

    @property
    def summary(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for issue in self.issues:
            counts[issue.rule] = counts.get(issue.rule, 0) + 1
        return counts


FUNCTION_PATTERN = re.compile(
    r"(?:^|\s)"
    r"(?:export\s+)?(?:default\s+)?(?:async\s+)?"
    r"(?:function\s+(\w+)|"                # function declaration
    r"(?:const|let|var)\s+(\w+)\s*=\s*"    # arrow / function expression
    r"(?:async\s+)?(?:function|\([^)]*\)\s*=>|\w+\s*=>))"
    r"|(\w+)\s*\([^)]*\)\s*\{",           # method shorthand
    re.MULTILINE,
)

CONSOLE_LOG_PATTERN = re.compile(r"\bconsole\.(log|debug|info|warn|error|trace)\s*\(")
TODO_PATTERN = re.compile(r"\b(TODO|FIXME|HACK|XXX)\b", re.IGNORECASE)
MAGIC_NUMBER_PATTERN = re.compile(
    r"(?<![.\w])"          # not preceded by dot or word char
    r"-?(?:[2-9]\d{1,}|"  # numbers >= 20
    r"\d+\.\d+)"          # or any decimal
    r"(?![.\w])"           # not followed by dot or word char
)
EMPTY_CATCH_PATTERN = re.compile(r"catch\s*\([^)]*\)\s*\{\s*\}")
SAFE_NUMBER_CONTEXTS = re.compile(
    r"(?:port|timeout|delay|width|height|size|length|index|count|max|min|limit"
    r"|version|STATUS|CODE|padding|margin|offset|duration)\s*[:=]\s*$",
    re.IGNORECASE,
)


def find_function_spans(lines: list[str]) -> list[tuple[str, int, int]]:
    """Find function start/end lines by tracking brace depth."""
    functions: list[tuple[str, int, int]] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        match = FUNCTION_PATTERN.search(line)
        if match:
            name = match.group(1) or match.group(2) or match.group(3) or "<anonymous>"
            if "{" in line:
                start = i
                depth = 0
                for j in range(i, len(lines)):
                    for ch in lines[j]:
                        if ch == "{":
                            depth += 1
                        elif ch == "}":
                            depth -= 1
                    if depth <= 0 and j > i:
                        functions.append((name, start + 1, j + 1))
                        break
        i += 1
    return functions


def strip_comments_and_strings(line: str) -> str:
    """Remove string literals and single-line comments for analysis."""
    result = re.sub(r'(["\'])(?:(?!\1|\\).|\\.)*\1', '""', line)
    result = re.sub(r"`(?:[^`\\]|\\.)*`", '""', result)
    result = re.sub(r"//.*$", "", result)
    return result


def check_file(filepath: str) -> ReviewReport:
    path = Path(filepath)
    if not path.exists():
        print(f"Error: File not found: {filepath}", file=sys.stderr)
        sys.exit(1)

    content = path.read_text(encoding="utf-8", errors="replace")
    lines = content.splitlines()
    report = ReviewReport(file=str(path), total_lines=len(lines))

    if len(lines) > 300:
        report.issues.append(Issue(
            rule="file-length",
            severity="warning",
            line=1,
            message=f"File has {len(lines)} lines (threshold: 300)",
        ))

    functions = find_function_spans(lines)
    for name, start, end in functions:
        length = end - start + 1
        if length > 50:
            report.issues.append(Issue(
                rule="long-function",
                severity="warning",
                line=start,
                message=f"Function '{name}' is {length} lines (threshold: 50)",
            ))

    in_block_comment = False
    for i, raw_line in enumerate(lines, 1):
        stripped = strip_comments_and_strings(raw_line)

        if "/*" in raw_line and "*/" not in raw_line:
            in_block_comment = True
            continue
        if in_block_comment:
            if "*/" in raw_line:
                in_block_comment = False
            continue

        todo_matches = TODO_PATTERN.findall(raw_line)
        for tag in todo_matches:
            report.issues.append(Issue(
                rule="todo-fixme",
                severity="info",
                line=i,
                message=f"Found {tag.upper()} comment",
            ))

        if CONSOLE_LOG_PATTERN.search(stripped):
            report.issues.append(Issue(
                rule="console-log",
                severity="warning",
                line=i,
                message="console.log/debug/warn/error left in code",
            ))

        brace_depth = 0
        max_depth = 0
        for ch in stripped:
            if ch == "{":
                brace_depth += 1
                max_depth = max(max_depth, brace_depth)
            elif ch == "}":
                brace_depth -= 1
        if max_depth > 3:
            report.issues.append(Issue(
                rule="deep-nesting",
                severity="warning",
                line=i,
                message=f"Line has {max_depth} levels of nesting (threshold: 3)",
            ))

        for match in MAGIC_NUMBER_PATTERN.finditer(stripped):
            prefix = stripped[:match.start()]
            if SAFE_NUMBER_CONTEXTS.search(prefix):
                continue
            if re.search(r"(?:import|require|from)\s", raw_line):
                continue
            report.issues.append(Issue(
                rule="magic-number",
                severity="info",
                line=i,
                message=f"Magic number: {match.group()}",
            ))

        if len(raw_line) > 120:
            report.issues.append(Issue(
                rule="long-line",
                severity="info",
                line=i,
                message=f"Line is {len(raw_line)} characters (threshold: 120)",
            ))

    for match in EMPTY_CATCH_PATTERN.finditer(content):
        line_num = content[:match.start()].count("\n") + 1
        report.issues.append(Issue(
            rule="empty-catch",
            severity="warning",
            line=line_num,
            message="Empty catch block — errors are silently swallowed",
        ))

    report.issues.sort(key=lambda issue: issue.line)
    return report


SEVERITY_COLORS = {"warning": "\033[33m", "info": "\033[36m", "error": "\033[31m"}
RESET = "\033[0m"


def print_report(report: ReviewReport) -> None:
    print(f"\n{'=' * 60}")
    print(f"  Code Review Report: {report.file}")
    print(f"  Total lines: {report.total_lines}")
    print(f"{'=' * 60}\n")

    if not report.issues:
        print("  ✓ No issues found. Code looks clean!\n")
        return

    summary = report.summary
    print(f"  Found {len(report.issues)} issue(s) across {len(summary)} rule(s):\n")

    for rule, count in sorted(summary.items()):
        print(f"    {rule}: {count}")
    print()

    for issue in report.issues:
        color = SEVERITY_COLORS.get(issue.severity, "")
        print(f"  {color}[{issue.severity.upper():>7}]{RESET} "
              f"L{issue.line:<4} {issue.rule}: {issue.message}")

    print(f"\n{'=' * 60}\n")


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python review-checklist.py <file_path> [--json]", file=sys.stderr)
        sys.exit(1)

    filepath = sys.argv[1]
    output_json = "--json" in sys.argv

    report = check_file(filepath)

    if output_json:
        data = asdict(report)
        data["summary"] = report.summary
        print(json.dumps(data, indent=2))
    else:
        print_report(report)

    warning_count = sum(1 for i in report.issues if i.severity == "warning")
    sys.exit(1 if warning_count > 0 else 0)


if __name__ == "__main__":
    main()
