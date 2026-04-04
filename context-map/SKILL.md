---
name: context-map
description: Scope the real change surface before editing. Use when planning a feature, bugfix, refactor, or review and you need a concrete map of likely touch points, dependencies, tests, and nearby risks.
---
# Context Map

Build a task-focused map of the codebase before changing files.

## When to Use

- A request spans more than one file and the impact is not obvious yet.
- You need to identify the minimum safe edit set before implementation.
- You are debugging a bug or regression and need to trace nearby code paths.
- You want a review-quality summary of likely code, test, config, and documentation touch points.

## Core Workflow

1. Restate the change in one sentence.
2. Search for obvious entry points by feature name, route, symbol, command, or error text.
3. Expand outward into direct dependencies, tests, docs, config, schemas, and scripts.
4. Separate likely edit targets from read-only reference patterns.
5. Call out risk multipliers such as public APIs, migrations, auth, secrets, environment variables, or generated artifacts.
6. Produce a compact context map before implementation.

## Search Order

### 1. Primary Targets

Look for the files most likely to hold the requested behavior:

- route handlers, commands, services, jobs, or pages
- components, helpers, validators, and serializers
- feature-specific configs, manifests, templates, and generated sources

### 2. Direct Dependencies

Trace the files that import, export, call, or configure the primary targets:

- imports and exports
- DI registration and factory wiring
- schema or model definitions
- build or deployment hooks

### 3. Verification Surface

Find the evidence paths that should move with the change:

- unit, integration, E2E, and snapshot tests
- fixtures, golden files, and sample payloads
- README, usage docs, changelogs, and migration notes

### 4. Reference Patterns

Find nearby examples that show the house style for the same kind of work:

- similar endpoints or handlers
- related UI components
- existing test patterns
- prior migrations or config changes

## Output Format

Use this structure unless the user asked for a different format:

```markdown
## Context Map

### Likely Edit Targets
| File | Why it matters | Expected change |
|------|----------------|-----------------|
| path/to/file | Main entry point | Update logic |

### Nearby Dependencies
| File | Relationship |
|------|--------------|
| path/to/file | Imported by the main target |

### Verification Files
| File | Coverage |
|------|----------|
| path/to/test | Existing tests for the feature |

### Reference Patterns
| File | Pattern to reuse |
|------|------------------|
| path/to/example | Similar implementation shape |

### Risks
- Public API or contract may change
- Config, env vars, or generated files may need updates
- Docs or changelog may need to move with the code
```

## Heuristics

- Prefer the smallest edit set that can fully implement the task.
- Include tests and docs whenever the behavior or setup might move.
- Treat migrations, auth, secrets, caching, build scripts, and generated artifacts as high-risk neighbors.
- If multiple subsystems are involved, split the map by subsystem instead of producing one giant table.
- Revise the map after discovery if the real scope is materially different from the initial request.

## Scripts And References

- [Context Map Template](./references/context-map-template.md)
- [Context Map Builder](./scripts/build-context-map.py)

## Cross-Client Portability

This skill is written to stay usable across GitHub Copilot, Claude Code, Codex, and Gemini CLI.

- GitHub Copilot: keep the folder in a Copilot-visible skill or plugin path, or wrap the workflow as project instructions if the host does not support portable skill folders directly.
- Claude Code: keep the folder in a local skills directory or a compatible plugin or marketplace source.
- Codex: install or sync the folder into `$CODEX_HOME/skills/<skill-name>` and restart Codex after major changes.
- Gemini CLI: this repository generates a project command named `/skills:context-map` from this skill. Rebuild commands with `python scripts/export-gemini-skill.py context-map` and then run `/commands reload` inside Gemini CLI.

## MCP Availability And Fallback

No dedicated MCP server is required for the normal workflow in this skill.

- If the current host lacks symbolic code-navigation tools, use `rg`, targeted file reads, and dependency scans from the bundled helper script.
- Treat the generated Markdown map and a quick manual sanity check as the fallback evidence path before implementation begins.

## Related Skills

| Skill | Relationship |
|-------|--------------|
| [writing-plans](../writing-plans/SKILL.md) | Turn the mapped edit surface into an execution plan |
| [systematic-debugging](../systematic-debugging/SKILL.md) | Use after the map when isolating regressions or unknown root causes |
| [verification-before-completion](../verification-before-completion/SKILL.md) | Revisit the mapped verification surface before closing the task |
