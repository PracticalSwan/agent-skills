#!/usr/bin/env python3
"""Print common Markdown documentation templates."""

from __future__ import annotations

import argparse

TEMPLATES = {
    "api": """# API Name

## Overview
## Authentication
## Request
## Response
## Errors
## Examples
""",
    "feature": """# Feature Name

## Purpose
## User Flow
## Constraints
## Rollout
## Troubleshooting
""",
    "config": """# Configuration Guide

## Overview
## Required Variables
## Optional Variables
## Example
## Failure Modes
""",
    "migration": """# Migration Guide

## What Changed
## Before
## After
## Upgrade Steps
## Validation
""",
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("kind", choices=sorted(TEMPLATES))
    args = parser.parse_args()
    print(TEMPLATES[args.kind])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
