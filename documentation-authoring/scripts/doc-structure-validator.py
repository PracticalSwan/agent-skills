#!/usr/bin/env python3
"""
Markdown Document Structure & Quality Validator

Validates a markdown document for common quality issues:
- Heading hierarchy (no skipped levels)
- Empty sections
- Internal link targets
- Word count per section
- TODO/TBD/FIXME markers
- Code blocks missing language tags
- Images missing alt text

Usage:
    python doc-structure-validator.py <path-to-markdown-file>
    python doc-structure-validator.py <path-to-markdown-file> --json
    python doc-structure-validator.py <directory> --recursive

Stdlib only — no third-party dependencies.
"""

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


@dataclass
class Issue:
    line: int
    severity: str  # "error", "warning", "info"
    category: str
    message: str


@dataclass
class SectionInfo:
    heading: str
    level: int
    line: int
    word_count: int


@dataclass
class ValidationReport:
    file_path: str
    total_words: int = 0
    total_headings: int = 0
    total_code_blocks: int = 0
    total_images: int = 0
    total_links: int = 0
    sections: list = field(default_factory=list)
    issues: list = field(default_factory=list)

    @property
    def error_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == "error")

    @property
    def warning_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == "warning")

    @property
    def info_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == "info")


MARKER_PATTERN = re.compile(r"\b(TODO|TBD|FIXME|HACK|XXX)\b", re.IGNORECASE)
HEADING_PATTERN = re.compile(r"^(#{1,6})\s+(.+)$")
IMAGE_PATTERN = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
LINK_PATTERN = re.compile(r"(?<!!)\[([^\]]+)\]\(([^)]+)\)")
ANCHOR_PATTERN = re.compile(r"<a\s+(?:name|id)\s*=\s*[\"']([^\"']+)[\"']", re.IGNORECASE)


def slugify_heading(text: str) -> str:
    """Convert heading text to a GitHub-style anchor slug."""
    text = text.strip().lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s]+", "-", text)
    return text


def count_words(text: str) -> int:
    """Count words in a string, excluding code blocks and markdown syntax."""
    cleaned = re.sub(r"`[^`]+`", "", text)
    cleaned = re.sub(r"[#*_\[\]()>|]", " ", cleaned)
    return len(cleaned.split())


def parse_document(lines: list[str]) -> tuple[list, list, list, list, list]:
    """Parse markdown lines into headings, code blocks, images, links, and content sections."""
    headings = []
    code_blocks = []
    images = []
    links = []
    in_code_block = False
    code_block_start = -1
    code_block_lang = None

    for i, line in enumerate(lines, 1):
        stripped = line.strip()

        if stripped.startswith("```"):
            if not in_code_block:
                in_code_block = True
                code_block_start = i
                lang = stripped[3:].strip().split()[0] if len(stripped) > 3 else ""
                code_block_lang = lang
            else:
                in_code_block = False
                code_blocks.append({
                    "start": code_block_start,
                    "end": i,
                    "lang": code_block_lang,
                })
                code_block_lang = None
            continue

        if in_code_block:
            continue

        heading_match = HEADING_PATTERN.match(stripped)
        if heading_match:
            level = len(heading_match.group(1))
            text = heading_match.group(2).strip()
            headings.append({"level": level, "text": text, "line": i})

        for img_match in IMAGE_PATTERN.finditer(line):
            images.append({
                "alt": img_match.group(1),
                "src": img_match.group(2),
                "line": i,
            })

        for link_match in LINK_PATTERN.finditer(line):
            links.append({
                "text": link_match.group(1),
                "href": link_match.group(2),
                "line": i,
            })

    if in_code_block:
        code_blocks.append({
            "start": code_block_start,
            "end": len(lines),
            "lang": code_block_lang,
            "unclosed": True,
        })

    return headings, code_blocks, images, links


def validate_heading_hierarchy(headings: list, issues: list[Issue]) -> None:
    """Check that heading levels don't skip (e.g., H2 -> H4)."""
    if not headings:
        issues.append(Issue(
            line=1, severity="warning", category="structure",
            message="Document has no headings.",
        ))
        return

    prev_level = 0
    for h in headings:
        level = h["level"]
        if prev_level > 0 and level > prev_level + 1:
            issues.append(Issue(
                line=h["line"], severity="error", category="heading-hierarchy",
                message=f"Heading level skipped: H{prev_level} -> H{level} "
                        f"('{h['text']}'). Expected H{prev_level + 1} or lower.",
            ))
        prev_level = level


def validate_empty_sections(
    headings: list, lines: list[str], issues: list[Issue]
) -> list[SectionInfo]:
    """Check for sections with no content between headings."""
    sections = []
    total_lines = len(lines)

    for idx, h in enumerate(headings):
        start_line = h["line"]
        end_line = headings[idx + 1]["line"] - 1 if idx + 1 < len(headings) else total_lines

        content_lines = []
        in_code = False
        for li in range(start_line, end_line):
            raw = lines[li].strip() if li < total_lines else ""
            if raw.startswith("```"):
                in_code = not in_code
                continue
            if not in_code and raw and not HEADING_PATTERN.match(raw):
                content_lines.append(raw)

        word_count = sum(count_words(cl) for cl in content_lines)
        sections.append(SectionInfo(
            heading=h["text"], level=h["level"],
            line=h["line"], word_count=word_count,
        ))

        if word_count == 0:
            issues.append(Issue(
                line=h["line"], severity="warning", category="empty-section",
                message=f"Section '{h['text']}' appears to have no content.",
            ))

    return sections


def validate_internal_links(
    headings: list, links: list, lines: list[str], issues: list[Issue]
) -> None:
    """Validate that internal anchor links (#...) point to existing headings."""
    heading_slugs = set()
    for h in headings:
        heading_slugs.add(slugify_heading(h["text"]))

    for anchor in ANCHOR_PATTERN.finditer("\n".join(lines)):
        heading_slugs.add(anchor.group(1).lower())

    for link in links:
        href = link["href"]
        if href.startswith("#"):
            target = href[1:].lower()
            if target not in heading_slugs:
                issues.append(Issue(
                    line=link["line"], severity="error", category="broken-link",
                    message=f"Internal link '#{target}' does not match any heading or anchor.",
                ))


def validate_code_blocks(code_blocks: list, issues: list[Issue]) -> None:
    """Check that code blocks have language tags and are properly closed."""
    for cb in code_blocks:
        if cb.get("unclosed"):
            issues.append(Issue(
                line=cb["start"], severity="error", category="code-block",
                message="Unclosed code block (missing closing ```).",
            ))
        elif not cb["lang"]:
            issues.append(Issue(
                line=cb["start"], severity="warning", category="code-block",
                message="Code block missing language tag (e.g., ```python).",
            ))


def validate_images(images: list, issues: list[Issue]) -> None:
    """Check that images have alt text."""
    for img in images:
        if not img["alt"].strip():
            issues.append(Issue(
                line=img["line"], severity="warning", category="accessibility",
                message=f"Image missing alt text: {img['src']}",
            ))


def validate_markers(lines: list[str], issues: list[Issue]) -> None:
    """Find TODO/TBD/FIXME/HACK/XXX markers."""
    in_code = False
    for i, line in enumerate(lines, 1):
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        for match in MARKER_PATTERN.finditer(line):
            issues.append(Issue(
                line=i, severity="info", category="marker",
                message=f"Found '{match.group()}' marker: {line.strip()[:80]}",
            ))


def validate_document(file_path: str) -> ValidationReport:
    """Run all validations on a markdown file and return a report."""
    report = ValidationReport(file_path=file_path)

    path = Path(file_path)
    if not path.exists():
        report.issues.append(Issue(
            line=0, severity="error", category="file",
            message=f"File not found: {file_path}",
        ))
        return report

    try:
        content = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        content = path.read_text(encoding="latin-1")

    lines = content.split("\n")
    headings, code_blocks, images, links = parse_document(lines)

    report.total_headings = len(headings)
    report.total_code_blocks = len(code_blocks)
    report.total_images = len(images)
    report.total_links = len(links)

    in_code = False
    word_lines = []
    for line in lines:
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        if not in_code:
            word_lines.append(line)
    report.total_words = count_words(" ".join(word_lines))

    validate_heading_hierarchy(headings, report.issues)
    report.sections = validate_empty_sections(headings, lines, report.issues)
    validate_internal_links(headings, links, lines, report.issues)
    validate_code_blocks(code_blocks, report.issues)
    validate_images(images, report.issues)
    validate_markers(lines, report.issues)

    return report


def format_report_text(report: ValidationReport) -> str:
    """Format a validation report as human-readable text."""
    out = []
    out.append(f"\n{'='*60}")
    out.append(f"  Document Quality Report")
    out.append(f"  {report.file_path}")
    out.append(f"{'='*60}\n")

    out.append(f"  Words: {report.total_words}  |  Headings: {report.total_headings}  "
               f"|  Code blocks: {report.total_code_blocks}")
    out.append(f"  Images: {report.total_images}  |  Links: {report.total_links}")
    out.append(f"  Issues: {report.error_count} errors, {report.warning_count} warnings, "
               f"{report.info_count} info\n")

    if report.sections:
        out.append("  Sections:")
        out.append(f"  {'Ln':<5} {'Lvl':<4} {'Words':<7} {'Heading'}")
        out.append(f"  {'---':<5} {'---':<4} {'-----':<7} {'-------'}")
        for s in report.sections:
            indent = "  " * (s.level - 1)
            out.append(f"  {s.line:<5} H{s.level:<3} {s.word_count:<7} {indent}{s.heading}")
        out.append("")

    if report.issues:
        out.append("  Issues:")
        severity_order = {"error": 0, "warning": 1, "info": 2}
        sorted_issues = sorted(report.issues, key=lambda i: (severity_order.get(i.severity, 3), i.line))
        for issue in sorted_issues:
            icon = {"error": "[ERR]", "warning": "[WRN]", "info": "[INF]"}.get(issue.severity, "[???]")
            out.append(f"  {icon} Line {issue.line}: [{issue.category}] {issue.message}")
        out.append("")
    else:
        out.append("  No issues found. Document looks good!\n")

    score = max(0, 100 - (report.error_count * 10) - (report.warning_count * 3) - report.info_count)
    out.append(f"  Quality Score: {score}/100")
    out.append(f"{'='*60}\n")
    return "\n".join(out)


def format_report_json(report: ValidationReport) -> str:
    """Format a validation report as JSON."""
    data = {
        "file": report.file_path,
        "stats": {
            "words": report.total_words,
            "headings": report.total_headings,
            "code_blocks": report.total_code_blocks,
            "images": report.total_images,
            "links": report.total_links,
        },
        "sections": [
            {"heading": s.heading, "level": s.level, "line": s.line, "words": s.word_count}
            for s in report.sections
        ],
        "issues": [
            {"line": i.line, "severity": i.severity, "category": i.category, "message": i.message}
            for i in report.issues
        ],
        "summary": {
            "errors": report.error_count,
            "warnings": report.warning_count,
            "info": report.info_count,
            "score": max(0, 100 - (report.error_count * 10) - (report.warning_count * 3) - report.info_count),
        },
    }
    return json.dumps(data, indent=2)


def find_markdown_files(directory: str) -> list[str]:
    """Recursively find all .md files in a directory."""
    md_files = []
    for root, _dirs, files in os.walk(directory):
        for f in files:
            if f.lower().endswith(".md"):
                md_files.append(os.path.join(root, f))
    return sorted(md_files)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate markdown document structure and quality.",
    )
    parser.add_argument("path", help="Path to a markdown file or directory.")
    parser.add_argument("--json", action="store_true", help="Output report as JSON.")
    parser.add_argument("--recursive", "-r", action="store_true",
                        help="Recursively validate all .md files in a directory.")
    parser.add_argument("--fail-on-warnings", action="store_true",
                        help="Exit with non-zero status if warnings exist.")
    args = parser.parse_args()

    target = Path(args.path)

    if target.is_dir():
        if not args.recursive:
            print(f"Error: '{args.path}' is a directory. Use --recursive to validate all .md files.",
                  file=sys.stderr)
            sys.exit(1)
        files = find_markdown_files(str(target))
        if not files:
            print(f"No .md files found in '{args.path}'.", file=sys.stderr)
            sys.exit(1)
    elif target.is_file():
        files = [str(target)]
    else:
        print(f"Error: '{args.path}' not found.", file=sys.stderr)
        sys.exit(1)

    total_errors = 0
    total_warnings = 0
    reports = []

    for file_path in files:
        report = validate_document(file_path)
        reports.append(report)
        total_errors += report.error_count
        total_warnings += report.warning_count

    if args.json:
        if len(reports) == 1:
            print(format_report_json(reports[0]))
        else:
            combined = [json.loads(format_report_json(r)) for r in reports]
            print(json.dumps(combined, indent=2))
    else:
        for report in reports:
            print(format_report_text(report))

        if len(reports) > 1:
            print(f"  Validated {len(reports)} files: "
                  f"{total_errors} total errors, {total_warnings} total warnings.\n")

    if total_errors > 0:
        sys.exit(1)
    if args.fail_on_warnings and total_warnings > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
