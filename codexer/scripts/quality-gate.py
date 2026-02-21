"""
Python Quality Gate Script

Runs static quality checks on a Python file or directory using only
the standard library (ast module). Checks:
  1. Type hints presence on function parameters and return types
  2. Docstring coverage on modules, classes, and functions
  3. Import organization (stdlib / third-party / local grouping)
  4. Function length (< 50 lines)
  5. PEP 8 naming conventions

Usage:
  python quality-gate.py <path>          # file or directory
  python quality-gate.py src/            # scan all .py files recursively
  python quality-gate.py my_module.py    # single file
"""

import ast
import sys
import os
import keyword
import re
from pathlib import Path
from dataclasses import dataclass, field

STDLIB_TOP_LEVEL = {
    "abc", "aifc", "argparse", "array", "ast", "asynchat", "asyncio",
    "asyncore", "atexit", "audioop", "base64", "bdb", "binascii",
    "binhex", "bisect", "builtins", "bz2", "calendar", "cgi", "cgitb",
    "chunk", "cmath", "cmd", "code", "codecs", "codeop", "collections",
    "colorsys", "compileall", "concurrent", "configparser", "contextlib",
    "contextvars", "copy", "copyreg", "cProfile", "crypt", "csv",
    "ctypes", "curses", "dataclasses", "datetime", "dbm", "decimal",
    "difflib", "dis", "distutils", "doctest", "email", "encodings",
    "enum", "errno", "faulthandler", "fcntl", "filecmp", "fileinput",
    "fnmatch", "formatter", "fractions", "ftplib", "functools", "gc",
    "getopt", "getpass", "gettext", "glob", "grp", "gzip", "hashlib",
    "heapq", "hmac", "html", "http", "idlelib", "imaplib", "imghdr",
    "imp", "importlib", "inspect", "io", "ipaddress", "itertools",
    "json", "keyword", "lib2to3", "linecache", "locale", "logging",
    "lzma", "mailbox", "mailcap", "marshal", "math", "mimetypes",
    "mmap", "modulefinder", "multiprocessing", "netrc", "nis", "nntplib",
    "numbers", "operator", "optparse", "os", "ossaudiodev", "parser",
    "pathlib", "pdb", "pickle", "pickletools", "pipes", "pkgutil",
    "platform", "plistlib", "poplib", "posix", "posixpath", "pprint",
    "profile", "pstats", "pty", "pwd", "py_compile", "pyclbr",
    "pydoc", "queue", "quopri", "random", "re", "readline", "reprlib",
    "resource", "rlcompleter", "runpy", "sched", "secrets", "select",
    "selectors", "shelve", "shlex", "shutil", "signal", "site",
    "smtpd", "smtplib", "sndhdr", "socket", "socketserver", "spwd",
    "sqlite3", "sre_compile", "sre_constants", "sre_parse", "ssl",
    "stat", "statistics", "string", "stringprep", "struct", "subprocess",
    "sunau", "symtable", "sys", "sysconfig", "syslog", "tabnanny",
    "tarfile", "telnetlib", "tempfile", "termios", "test", "textwrap",
    "threading", "time", "timeit", "tkinter", "token", "tokenize",
    "tomllib", "trace", "traceback", "tracemalloc", "tty", "turtle",
    "turtledemo", "types", "typing", "unicodedata", "unittest", "urllib",
    "uu", "uuid", "venv", "warnings", "wave", "weakref", "webbrowser",
    "winreg", "winsound", "wsgiref", "xdrlib", "xml", "xmlrpc",
    "zipapp", "zipfile", "zipimport", "zlib", "_thread",
}

MAX_FUNCTION_LINES = 50


@dataclass
class Issue:
    file: str
    line: int
    category: str
    message: str
    severity: str = "warning"


@dataclass
class Report:
    issues: list[Issue] = field(default_factory=list)
    files_checked: int = 0
    functions_checked: int = 0
    classes_checked: int = 0

    @property
    def passed(self) -> bool:
        return not any(i.severity == "error" for i in self.issues)

    def add(self, file: str, line: int, category: str, message: str,
            severity: str = "warning"):
        self.issues.append(Issue(file, line, category, message, severity))


def check_type_hints(tree: ast.Module, filepath: str, report: Report):
    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        if node.name.startswith("_") and node.name != "__init__":
            continue

        report.functions_checked += 1

        for arg in node.args.args:
            if arg.arg == "self" or arg.arg == "cls":
                continue
            if arg.annotation is None:
                report.add(
                    filepath, node.lineno, "type-hints",
                    f"Parameter '{arg.arg}' in '{node.name}' missing type hint",
                    "error",
                )

        if node.name != "__init__" and node.returns is None:
            report.add(
                filepath, node.lineno, "type-hints",
                f"Function '{node.name}' missing return type annotation",
                "error",
            )


def check_docstrings(tree: ast.Module, filepath: str, report: Report):
    if not ast.get_docstring(tree):
        report.add(filepath, 1, "docstrings", "Module missing docstring")

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            report.classes_checked += 1
            if not ast.get_docstring(node):
                report.add(
                    filepath, node.lineno, "docstrings",
                    f"Class '{node.name}' missing docstring",
                )

        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.name.startswith("_") and node.name != "__init__":
                continue
            if not ast.get_docstring(node):
                report.add(
                    filepath, node.lineno, "docstrings",
                    f"Function '{node.name}' missing docstring",
                )


def check_import_organization(tree: ast.Module, filepath: str,
                              report: Report):
    imports: list[tuple[int, str, str]] = []

    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                top = alias.name.split(".")[0]
                group = "stdlib" if top in STDLIB_TOP_LEVEL else "third-party"
                imports.append((node.lineno, group, alias.name))
        elif isinstance(node, ast.ImportFrom):
            if node.module is None:
                continue
            top = node.module.split(".")[0]
            if node.level > 0:
                group = "local"
            elif top in STDLIB_TOP_LEVEL:
                group = "stdlib"
            else:
                group = "third-party"
            imports.append((node.lineno, group, node.module))

    if not imports:
        return

    group_order = {"stdlib": 0, "third-party": 1, "local": 2}
    prev_group_rank = -1
    saw_blank_between = True

    for i, (lineno, group, name) in enumerate(imports):
        rank = group_order[group]
        if rank < prev_group_rank:
            report.add(
                filepath, lineno, "imports",
                f"Import '{name}' ({group}) appears after a later group; "
                "expected order: stdlib → third-party → local",
            )
        prev_group_rank = rank


def check_function_length(tree: ast.Module, filepath: str, report: Report):
    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue

        end_lineno = getattr(node, "end_lineno", None)
        if end_lineno is None:
            continue

        length = end_lineno - node.lineno + 1
        if length > MAX_FUNCTION_LINES:
            report.add(
                filepath, node.lineno, "function-length",
                f"Function '{node.name}' is {length} lines "
                f"(max {MAX_FUNCTION_LINES})",
                "error",
            )


SNAKE_CASE = re.compile(r"^_{0,2}[a-z][a-z0-9_]*_{0,2}$")
UPPER_SNAKE = re.compile(r"^[A-Z][A-Z0-9_]*$")
PASCAL_CASE = re.compile(r"^_?[A-Z][a-zA-Z0-9]*$")


def check_naming(tree: ast.Module, filepath: str, report: Report):
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            if not PASCAL_CASE.match(node.name):
                report.add(
                    filepath, node.lineno, "naming",
                    f"Class '{node.name}' should use PascalCase",
                )

        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if not SNAKE_CASE.match(node.name):
                report.add(
                    filepath, node.lineno, "naming",
                    f"Function '{node.name}' should use snake_case",
                )

        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if not isinstance(target, ast.Name):
                    continue
                name = target.id
                if keyword.iskeyword(name):
                    continue
                # Module-level ALL_CAPS constants are acceptable
                if UPPER_SNAKE.match(name):
                    continue
                if not SNAKE_CASE.match(name):
                    report.add(
                        filepath, getattr(node, "lineno", 0), "naming",
                        f"Variable '{name}' should use snake_case",
                    )


def analyze_file(filepath: str, report: Report):
    try:
        source = Path(filepath).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        report.add(filepath, 0, "parse", f"Cannot read file: {exc}", "error")
        return

    try:
        tree = ast.parse(source, filename=filepath)
    except SyntaxError as exc:
        report.add(
            filepath, exc.lineno or 0, "parse",
            f"Syntax error: {exc.msg}", "error",
        )
        return

    report.files_checked += 1
    check_type_hints(tree, filepath, report)
    check_docstrings(tree, filepath, report)
    check_import_organization(tree, filepath, report)
    check_function_length(tree, filepath, report)
    check_naming(tree, filepath, report)


def collect_python_files(path: str) -> list[str]:
    target = Path(path)
    if target.is_file() and target.suffix == ".py":
        return [str(target)]
    if target.is_dir():
        return sorted(str(p) for p in target.rglob("*.py"))
    return []


def format_report(report: Report) -> str:
    lines: list[str] = []
    lines.append("=" * 60)
    lines.append("  PYTHON QUALITY GATE REPORT")
    lines.append("=" * 60)
    lines.append(
        f"Files: {report.files_checked}  |  "
        f"Functions: {report.functions_checked}  |  "
        f"Classes: {report.classes_checked}"
    )
    lines.append("-" * 60)

    if not report.issues:
        lines.append("ALL CHECKS PASSED")
        lines.append("=" * 60)
        return "\n".join(lines)

    by_category: dict[str, list[Issue]] = {}
    for issue in report.issues:
        by_category.setdefault(issue.category, []).append(issue)

    errors = sum(1 for i in report.issues if i.severity == "error")
    warnings = sum(1 for i in report.issues if i.severity == "warning")

    for category, issues in sorted(by_category.items()):
        lines.append(f"\n[{category.upper()}]")
        for issue in issues:
            marker = "ERROR" if issue.severity == "error" else "WARN "
            lines.append(f"  {marker}  {issue.file}:{issue.line}")
            lines.append(f"         {issue.message}")

    lines.append("\n" + "-" * 60)
    lines.append(f"Total: {errors} error(s), {warnings} warning(s)")
    status = "FAILED" if not report.passed else "PASSED (with warnings)"
    lines.append(f"Status: {status}")
    lines.append("=" * 60)
    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("Usage: python quality-gate.py <file_or_directory>")
        sys.exit(2)

    target = sys.argv[1]
    files = collect_python_files(target)

    if not files:
        print(f"No Python files found at: {target}")
        sys.exit(2)

    report = Report()
    for f in files:
        analyze_file(f, report)

    print(format_report(report))
    sys.exit(0 if report.passed else 1)


if __name__ == "__main__":
    main()
