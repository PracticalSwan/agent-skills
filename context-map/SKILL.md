---
name: context-map
version: "1.3"
last_updated: 2026-07-11
tags: [context, map, agents, delegation, workflow]
description: "Scope the real change surface before editing. Use when planning a feature, bugfix, refactor, or review and you need a concrete map of likely touch points, dependencies, tests, and nearby risks."
---
# Context Map

Build a task-focused map of the codebase before changing files.

- Leverage native parallel subagent dispatch and 200k+ context windows where available.


## When to Use

Use symptom -> action triggers: when one matches, apply this skill and verify with the protocol below.

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

## Anti-Patterns

- Delegating or evaluating without a scoped success condition: The output becomes hard to review and easy to overbuild.
- Skipping the evidence step: A workflow that cannot be re-checked quickly is not ready for handoff.
- Bundling unrelated subtasks together: It creates noisy prompts, weaker ownership, and avoidable integration risk.

## Verification Protocol

Before claiming "skill applied successfully":

1. Pass/fail: The Context Map workflow names the agent boundary, delegated scope, and expected return artifact.
2. Pass/fail: Context passed to helpers is minimal, task-local, and free of hidden expected answers.
3. Pass/fail: Results are integrated only after evidence, diffs, or citations are checked by the controller.
4. Pressure-test scenario: Run the workflow on two similar tasks that must not share assumptions or leaked context.
5. Success metric: Zero context leakage; every delegated output is independently reviewable.

## Scripts And References

- [Context Map Template](./references/context-map-template.md)
- [Context Map Builder](./scripts/build-context-map.py)

<!-- PORTABILITY:START -->
## Cross-Client Portability

This skill is written to stay usable across GitHub Copilot, Claude Code, Codex, and Gemini CLI.

- GitHub Copilot: keep the folder in a Copilot-visible skill or plugin path, or wrap the workflow as project instructions if the host does not support portable skill folders directly.
- Claude Code: keep the folder in a local skills directory or a compatible plugin or marketplace source.
- Codex: install or sync the folder into `$CODEX_HOME/skills/<skill-name>` and restart Codex after major changes.
- Gemini CLI: this repository generates a project command named `/skills:context-map` from this skill. Rebuild commands with `python scripts/export-gemini-skill.py context-map` and then run `/commands reload` inside Gemini CLI.

<!-- PORTABILITY:END -->

<!-- MCP:START -->
## MCP Availability And Fallback

Preferred MCP Server: None required

- Fallback prompt: "Use the Context Map skill without MCP. Rely on the local `SKILL.md`, bundled references or scripts, and manual verification. Show the exact commands, evidence, and final checks you used before concluding."
- If the current host does not expose a matching server, use the bundled references, scripts, native toolchain, and manual workflow already described in this skill.
- Treat direct local verification, rendered output, logs, tests, or screenshots as the fallback evidence path before completion.

<!-- MCP:END -->

## Related Skills

- [agent-task-mapping](../agent-task-mapping/SKILL.md): Use it when the workflow also needs task-to-agent routing decisions.
- [custom-agent-usage](../custom-agent-usage/SKILL.md): Use it when the workflow also needs loading and invoking custom agent definitions safely.
- [subagent-delegation](../subagent-delegation/SKILL.md): Use it when the workflow also needs safe, scoped delegation to helper agents.
- [subagent-driven-development](../subagent-driven-development/SKILL.md): Use it when the workflow also needs plan-driven implementation with reviewer loops.
