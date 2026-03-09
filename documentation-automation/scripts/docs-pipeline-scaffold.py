#!/usr/bin/env python3
"""Print starter documentation automation commands for common stacks."""

from __future__ import annotations

import argparse
import json


def node_config() -> dict[str, str]:
    return {
        "docs:lint": "markdownlint '**/*.md'",
        "docs:links": "lychee --no-progress .",
        "docs:spell": "cspell .",
        "docs:validate": "npm run docs:lint && npm run docs:links && npm run docs:spell",
    }


def python_config() -> dict[str, str]:
    return {
        "docs:lint": "markdownlint '**/*.md'",
        "docs:links": "python scripts/doc-link-check.py .",
        "docs:spell": "cspell .",
        "docs:validate": "python -m subprocess_placeholder",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stack", choices=("node", "python"), default="node")
    args = parser.parse_args()

    scripts = node_config() if args.stack == "node" else python_config()
    print(json.dumps({"scripts": scripts}, indent=2))
    print()
    print("CI checklist:")
    print("- Install doc tooling dependencies")
    print("- Run the same docs:validate command used locally")
    print("- Upload any generated doc artifacts only after validation passes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
