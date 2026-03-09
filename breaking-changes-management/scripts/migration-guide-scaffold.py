#!/usr/bin/env python3
"""Generate a migration guide skeleton for breaking changes."""

from __future__ import annotations

import argparse
from pathlib import Path


def build_markdown(version: str, title: str, changes: list[str]) -> str:
    bullets = "\n".join(f"- {item}" for item in changes) if changes else "- Describe the breaking change"
    return f"""# {title}

## Summary

- Target version: `{version}`
- Audience: Consumers upgrading from the previous major or minor release

## Breaking Changes

{bullets}

## Before

```text
Document the previous API, configuration, or workflow here.
```

## After

```text
Document the replacement API, configuration, or workflow here.
```

## Upgrade Steps

1. Update dependencies or package versions.
2. Replace removed or renamed APIs.
3. Update configuration keys, environment variables, and scripts.
4. Run tests and smoke checks.

## Validation

- List commands or checks the upgrader should run.

## Rollback Notes

- Describe how to revert if the migration fails.
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", required=True, help="Target release version, for example 3.0.0")
    parser.add_argument("--title", default="Migration Guide", help="Document title")
    parser.add_argument(
        "--change",
        action="append",
        default=[],
        help="Breaking change summary. Repeat for multiple items.",
    )
    parser.add_argument("-o", "--output", type=Path, help="Write output to a file instead of stdout")
    args = parser.parse_args()

    markdown = build_markdown(args.version, args.title, args.change)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(markdown, encoding="utf-8")
        print(f"Wrote {args.output}")
    else:
        print(markdown)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
