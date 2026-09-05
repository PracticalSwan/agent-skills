#!/usr/bin/env python3
"""Skill Risk Check: deterministic pre-install checks for agent artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable


VERSION = "0.1.5"
SCHEMA_VERSION = "1.0"
EXIT_PASS = 0
EXIT_FINDINGS = 1
EXIT_ERROR = 2
SEVERITY_RANK = {"low": 1, "medium": 2, "high": 3, "critical": 4}
DEFAULT_EXCLUDED_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".venv",
    "venv",
    "node_modules",
    "dist",
    "build",
    "__pycache__",
}
LOCAL_RULES = Path(__file__).resolve().parents[1] / "rules" / "default-rules.json"
INSTALLED_RULES = Path(sys.prefix) / "share" / "agent-skillguard" / "rules" / "default-rules.json"
DEFAULT_RULES = LOCAL_RULES if LOCAL_RULES.is_file() else INSTALLED_RULES
SUPPORTED_EXTENSIONS = {
    ".md", ".txt", ".json", ".toml", ".yml", ".yaml", ".py", ".js", ".ts",
    ".jsx", ".tsx", ".sh", ".bash", ".zsh", ".ps1", ".bat", ".cmd",
}
SECRET_PATTERNS = (
    re.compile(r"\bsk-[A-Za-z0-9_-]{8,}"),
    re.compile(r"\bghp_[A-Za-z0-9]{8,}"),
    re.compile(r"\bgithub_pat_[A-Za-z0-9_]{8,}"),
    re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{8,}"),
    re.compile(r"(?i)\bBearer\s+[A-Za-z0-9._~+/=-]{8,}"),
)


class SkillGuardError(ValueError):
    """A user-actionable scan configuration or input error."""


@dataclass(frozen=True)
class Rule:
    id: str
    version: str
    title: str
    description: str
    severity: str
    uncertainty: str
    pattern: str
    extensions: tuple[str, ...]
    remediation: str


@dataclass(frozen=True)
class Finding:
    rule_id: str
    rule_version: str
    title: str
    severity: str
    uncertainty: str
    path: str
    line: int
    column: int
    evidence: str
    message: str
    remediation: str
    fingerprint: str
    suppressed: bool
    suppression_reason: str | None


def _strict_object(value: Any, required: set[str], allowed: set[str], label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise SkillGuardError(f"{label} must be a JSON object")
    unknown = set(value) - allowed
    missing = required - set(value)
    if unknown:
        raise SkillGuardError(f"{label} has unknown fields: {', '.join(sorted(unknown))}")
    if missing:
        raise SkillGuardError(f"{label} is missing fields: {', '.join(sorted(missing))}")
    return value


def load_rules(path: Path) -> list[Rule]:
    """Load and strictly validate a JSON rule pack."""

    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise SkillGuardError(f"cannot load rule pack {path}: {exc}") from exc
    payload = _strict_object(payload, {"schema_version", "rules"}, {"schema_version", "rules"}, "rule pack")
    if payload["schema_version"] != SCHEMA_VERSION or not isinstance(payload["rules"], list):
        raise SkillGuardError("rule pack must use schema_version 1.0 and contain a rules array")
    required = {"id", "version", "title", "description", "severity", "uncertainty", "pattern", "extensions", "remediation"}
    rules: list[Rule] = []
    seen: set[str] = set()
    for index, raw in enumerate(payload["rules"]):
        item = _strict_object(raw, required, required, f"rule[{index}]")
        if not re.fullmatch(r"[A-Z][A-Z0-9_-]{2,31}", str(item["id"])):
            raise SkillGuardError(f"rule[{index}] has invalid id")
        if item["id"] in seen:
            raise SkillGuardError(f"duplicate rule id: {item['id']}")
        if item["severity"] not in SEVERITY_RANK or item["uncertainty"] not in {"low", "medium", "high"}:
            raise SkillGuardError(f"rule {item['id']} has invalid severity or uncertainty")
        if not isinstance(item["extensions"], list) or not item["extensions"]:
            raise SkillGuardError(f"rule {item['id']} must declare extensions")
        try:
            re.compile(str(item["pattern"]), re.IGNORECASE)
        except re.error as exc:
            raise SkillGuardError(f"rule {item['id']} has invalid regex: {exc}") from exc
        seen.add(str(item["id"]))
        rules.append(Rule(**{**item, "extensions": tuple(item["extensions"])}))
    return sorted(rules, key=lambda rule: rule.id)


def load_suppressions(path: Path | None) -> dict[str, dict[str, str]]:
    """Load exact finding suppressions; wildcard suppressions are intentionally unsupported."""

    if path is None or not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise SkillGuardError(f"cannot load suppressions {path}: {exc}") from exc
    payload = _strict_object(
        payload,
        {"schema_version", "suppressions"},
        {"schema_version", "suppressions"},
        "suppression file",
    )
    if payload["schema_version"] != SCHEMA_VERSION or not isinstance(payload["suppressions"], list):
        raise SkillGuardError("suppression file must use schema_version 1.0 and contain a suppressions array")
    output: dict[str, dict[str, str]] = {}
    fields = {"fingerprint", "rule_id", "rule_version", "reason"}
    for index, raw in enumerate(payload["suppressions"]):
        item = _strict_object(raw, fields, fields, f"suppression[{index}]")
        if not re.fullmatch(r"[a-f0-9]{64}", str(item["fingerprint"])):
            raise SkillGuardError(f"suppression[{index}] fingerprint must be lowercase SHA-256")
        if not all(isinstance(item[key], str) and item[key].strip() for key in fields):
            raise SkillGuardError(f"suppression[{index}] values must be non-empty strings")
        output[item["fingerprint"]] = item
    return output


def redact_evidence(value: str) -> str:
    """Redact common credential shapes and keep one bounded evidence line."""

    cleaned = "".join(character if character.isprintable() else " " for character in value).strip()
    for pattern in SECRET_PATTERNS:
        cleaned = pattern.sub("[REDACTED]", cleaned)
    return cleaned[:240] + ("…" if len(cleaned) > 240 else "")


def finding_fingerprint(rule: Rule, relative_path: str, evidence: str) -> str:
    """Bind one finding to its rule version, portable path, and normalized evidence."""

    normalized = " ".join(evidence.split()).casefold()
    material = "\0".join((rule.id, rule.version, relative_path.replace("\\", "/"), normalized))
    return hashlib.sha256(material.encode("utf-8")).hexdigest()


def iter_scan_files(root: Path, *, max_files: int, max_bytes: int) -> Iterable[tuple[Path, str, int]]:
    """Yield eligible files in portable deterministic order without following symlinks."""

    if not root.exists():
        raise SkillGuardError(f"scan target does not exist: {root}")
    if root.is_symlink():
        raise SkillGuardError("scan root must not be a symbolic link")
    candidates = [root] if root.is_file() else sorted(root.rglob("*"), key=lambda item: item.as_posix().casefold())
    yielded = 0
    for path in candidates:
        try:
            relative = path.relative_to(root).as_posix() if root.is_dir() else path.name
        except ValueError:
            continue
        parts = Path(relative).parts
        if path.is_symlink() or any(part in DEFAULT_EXCLUDED_DIRS for part in parts):
            continue
        if not path.is_file() or path.suffix.casefold() not in SUPPORTED_EXTENSIONS:
            continue
        try:
            size = path.stat().st_size
        except OSError as exc:
            raise SkillGuardError(f"cannot stat {relative}: {exc}") from exc
        if size > max_bytes:
            raise SkillGuardError(f"eligible file exceeds --max-bytes limit ({max_bytes}): {relative}")
        yielded += 1
        if yielded > max_files:
            raise SkillGuardError(f"scan exceeds --max-files limit ({max_files})")
        yield path, relative.replace("\\", "/"), size


def _line_location(text: str, offset: int) -> tuple[int, int, str]:
    line_number = text.count("\n", 0, offset) + 1
    start = text.rfind("\n", 0, offset) + 1
    end = text.find("\n", offset)
    if end == -1:
        end = len(text)
    return line_number, offset - start + 1, text[start:end]


def scan_path(
    root: Path,
    *,
    rules_path: Path = DEFAULT_RULES,
    suppressions_path: Path | None = None,
    min_severity: str = "low",
    max_files: int = 5000,
    max_bytes: int = 1_000_000,
) -> dict[str, Any]:
    """Scan one path and return a deterministic, portable report."""

    root = root.expanduser()
    if root.is_symlink():
        raise SkillGuardError("scan root must not be a symbolic link")
    root = root.resolve()
    rules = load_rules(rules_path)
    suppressions = load_suppressions(suppressions_path)
    if min_severity not in SEVERITY_RANK:
        raise SkillGuardError(f"unknown minimum severity: {min_severity}")
    findings: list[Finding] = []
    file_hashes: list[tuple[str, str]] = []
    bytes_scanned = 0
    files_scanned = 0
    for path, relative, size in iter_scan_files(root, max_files=max_files, max_bytes=max_bytes):
        try:
            raw = path.read_bytes()
        except OSError as exc:
            raise SkillGuardError(f"cannot read eligible file {relative}: {exc}") from exc
        if len(raw) > max_bytes:
            raise SkillGuardError(f"eligible file changed beyond --max-bytes limit ({max_bytes}): {relative}")
        if b"\x00" in raw[:4096]:
            raise SkillGuardError(f"eligible file contains binary NUL bytes and was not scanned: {relative}")
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise SkillGuardError(f"eligible file is not valid UTF-8 and was not scanned: {relative}: {exc}") from exc
        files_scanned += 1
        bytes_scanned += len(raw)
        file_hashes.append((relative, hashlib.sha256(raw).hexdigest()))
        suffix = path.suffix.casefold()
        for rule in rules:
            if suffix not in {extension.casefold() for extension in rule.extensions}:
                continue
            if SEVERITY_RANK[rule.severity] < SEVERITY_RANK[min_severity]:
                continue
            expression = re.compile(rule.pattern, re.IGNORECASE)
            for match in expression.finditer(text):
                line, column, evidence_line = _line_location(text, match.start())
                if rule.id == "SG004":
                    prefix = evidence_line[: max(0, column - 1)]
                    if re.search(r"(?:never|do not|don't|must not|shall not)\s*$", prefix[-32:], re.IGNORECASE):
                        continue
                evidence = redact_evidence(evidence_line)
                fingerprint = finding_fingerprint(rule, relative, evidence_line)
                suppression = suppressions.get(fingerprint)
                suppressed = bool(
                    suppression
                    and suppression["rule_id"] == rule.id
                    and suppression["rule_version"] == rule.version
                )
                findings.append(
                    Finding(
                        rule_id=rule.id,
                        rule_version=rule.version,
                        title=rule.title,
                        severity=rule.severity,
                        uncertainty=rule.uncertainty,
                        path=relative,
                        line=line,
                        column=column,
                        evidence=evidence,
                        message=rule.description,
                        remediation=rule.remediation,
                        fingerprint=fingerprint,
                        suppressed=suppressed,
                        suppression_reason=suppression["reason"] if suppressed and suppression else None,
                    )
                )
    findings.sort(key=lambda item: (item.path.casefold(), item.line, item.column, item.rule_id))
    active = [item for item in findings if not item.suppressed]
    severity_counts = {severity: sum(1 for item in active if item.severity == severity) for severity in SEVERITY_RANK}
    scan_material = json.dumps(file_hashes, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return {
        "schema_version": SCHEMA_VERSION,
        "tool": {"name": "agent-skillguard", "version": VERSION},
        "claim_boundary": "Potential policy violations only; this report does not establish that an artifact is safe or malicious.",
        "scan": {
            "root": ".",
            "files_scanned": files_scanned,
            "bytes_scanned": bytes_scanned,
            "scan_digest_sha256": hashlib.sha256(scan_material).hexdigest(),
            "rule_pack": rules_path.name,
            "rule_count": len(rules),
            "minimum_severity": min_severity,
            "symlinks_followed": False,
        },
        "summary": {
            "active_findings": len(active),
            "suppressed_findings": len(findings) - len(active),
            "by_severity": severity_counts,
            "result": "review_required" if active else "no_actionable_findings",
        },
        "findings": [asdict(item) for item in findings],
    }


def render_markdown(report: dict[str, Any]) -> str:
    """Render a concise human-review surface."""

    summary = report["summary"]
    lines = [
        "# Skill Risk Check report",
        "",
        f"> {report['claim_boundary']}",
        "",
        f"- Result: `{summary['result']}`",
        f"- Active findings: `{summary['active_findings']}`",
        f"- Suppressed findings: `{summary['suppressed_findings']}`",
        f"- Files scanned: `{report['scan']['files_scanned']}`",
        f"- Scan digest: `{report['scan']['scan_digest_sha256']}`",
        "",
    ]
    for finding in report["findings"]:
        state = "suppressed" if finding["suppressed"] else "active"
        lines.extend(
            [
                f"## {finding['rule_id']} — {finding['title']}",
                "",
                f"- State: `{state}`",
                f"- Severity: `{finding['severity']}`",
                f"- Uncertainty: `{finding['uncertainty']}`",
                f"- Location: `{finding['path']}:{finding['line']}:{finding['column']}`",
                f"- Fingerprint: `{finding['fingerprint']}`",
                f"- Evidence: `{finding['evidence'].replace('`', chr(39))}`",
                f"- Remediation: {finding['remediation']}",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def render_sarif(report: dict[str, Any], rules: list[Rule]) -> dict[str, Any]:
    """Render SARIF 2.1.0 for active findings."""

    level_map = {"critical": "error", "high": "error", "medium": "warning", "low": "note"}
    results = []
    for finding in report["findings"]:
        if finding["suppressed"]:
            continue
        results.append(
            {
                "ruleId": finding["rule_id"],
                "level": level_map[finding["severity"]],
                "message": {"text": finding["message"]},
                "locations": [
                    {
                        "physicalLocation": {
                            "artifactLocation": {"uri": finding["path"]},
                            "region": {"startLine": finding["line"], "startColumn": finding["column"]},
                        }
                    }
                ],
                "partialFingerprints": {"skillguardFingerprint/v1": finding["fingerprint"]},
                "properties": {
                    "severity": finding["severity"],
                    "uncertainty": finding["uncertainty"],
                    "evidence": finding["evidence"],
                    "remediation": finding["remediation"],
                    "claimBoundary": report["claim_boundary"],
                },
            }
        )
    descriptors = [
        {
            "id": rule.id,
            "name": rule.title,
            "shortDescription": {"text": rule.description},
            "help": {"text": rule.remediation},
            "properties": {"version": rule.version, "severity": rule.severity, "uncertainty": rule.uncertainty},
        }
        for rule in rules
    ]
    return {
        "$schema": "https://json.schemastore.org/sarif-2.1.0.json",
        "version": "2.1.0",
        "runs": [
            {
                "tool": {"driver": {"name": "Skill Risk Check", "version": VERSION, "rules": descriptors}},
                "results": results,
                "properties": {"scanDigestSha256": report["scan"]["scan_digest_sha256"]},
            }
        ],
    }


def write_new(path: Path, content: str) -> None:
    """Create a new output without following or overwriting a final-component symlink."""

    if path.exists() or path.is_symlink():
        raise SkillGuardError(f"refusing to overwrite existing output: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as handle:
        handle.write(content)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", action="version", version=f"agent-skillguard {VERSION}")
    subparsers = parser.add_subparsers(dest="command", required=True)
    scan = subparsers.add_parser("scan", help="Scan a skill or plugin directory without executing it.")
    scan.add_argument("path", type=Path)
    scan.add_argument("--rules", type=Path, default=DEFAULT_RULES)
    scan.add_argument("--suppressions", type=Path)
    scan.add_argument("--format", choices=("json", "markdown", "sarif"), default="json")
    scan.add_argument("--output", type=Path)
    scan.add_argument("--fail-on", choices=tuple(SEVERITY_RANK), default="low")
    scan.add_argument("--max-files", type=int, default=5000)
    scan.add_argument("--max-bytes", type=int, default=1_000_000)
    explain = subparsers.add_parser("explain", help="Explain one built-in rule.")
    explain.add_argument("rule_id")
    init = subparsers.add_parser("init-suppressions", help="Create an empty reviewed-suppression file.")
    init.add_argument("--output", type=Path, default=Path(".skillguard-ignore.json"))
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the CLI with the documented 0/1/2 exit-code contract."""

    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "init-suppressions":
            write_new(args.output, json.dumps({"schema_version": SCHEMA_VERSION, "suppressions": []}, indent=2) + "\n")
            print(args.output.as_posix())
            return EXIT_PASS
        rules = load_rules(DEFAULT_RULES)
        if args.command == "explain":
            rule = next((item for item in rules if item.id == args.rule_id), None)
            if rule is None:
                raise SkillGuardError(f"unknown rule id: {args.rule_id}")
            print(json.dumps(asdict(rule), indent=2))
            return EXIT_PASS
        report = scan_path(
            args.path,
            rules_path=args.rules,
            suppressions_path=args.suppressions,
            min_severity=args.fail_on,
            max_files=args.max_files,
            max_bytes=args.max_bytes,
        )
        if args.format == "markdown":
            rendered = render_markdown(report)
        elif args.format == "sarif":
            rendered = json.dumps(render_sarif(report, load_rules(args.rules)), indent=2) + "\n"
        else:
            rendered = json.dumps(report, indent=2) + "\n"
        if args.output:
            write_new(args.output, rendered)
        else:
            print(rendered, end="")
        return EXIT_FINDINGS if report["summary"]["active_findings"] else EXIT_PASS
    except (SkillGuardError, OSError) as exc:
        print(f"skillguard: {exc}", file=sys.stderr)
        return EXIT_ERROR


if __name__ == "__main__":
    raise SystemExit(main())
