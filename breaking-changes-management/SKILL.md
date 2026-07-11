---
name: breaking-changes-management
version: "1.3"
last_updated: 2026-07-11
tags: [breaking, changes, management, workflow, quality]
description: "Manage breaking API changes, migration guides, deprecation notices, and semver versioning. Use when introducing breaking changes, writing migration paths, updating changelogs, or releasing major versions."
---
# Breaking Changes Management

Use this skill when behavior, interfaces, configuration, or compatibility contracts change in a way that can break consumers.

- Leverage native parallel subagent dispatch and 200k+ context windows where available.


## Activation Conditions

Use symptom -> action triggers: when one matches, apply this skill and verify with the protocol below.

- Releasing a major version
- Renaming or removing public APIs
- Changing request or response shapes
- Replacing config keys, env vars, CLI flags, or file formats
- Writing migration notes, deprecation notices, or upgrade checklists

## Workflow

1. Identify the exact consumer-visible break.
2. State who is affected and from which version.
3. Provide the replacement path or mitigation.
4. Add before/after examples.
5. Update `CHANGELOG.md` and any setup or usage docs that changed.

## Required Outputs

- Changelog entry with a clear `BREAKING` label
- Migration guide with old usage, new usage, and upgrade steps
- Deprecation timeline if removal is delayed
- Validation notes for any examples or scripts that changed

## Anti-Patterns

- Starting work before the plan or gate is clear: Execution drifts when success criteria are implied instead of explicit.
- Treating verification as optional cleanup: The last mile is where regressions and missing updates are usually hiding.
- Mixing planning, implementation, and release work in one jump: You lose the causal chain that explains why a change is safe.

## Verification Protocol

Before claiming "skill applied successfully":

1. Pass/fail: The Breaking Changes Management workflow starts from explicit success criteria, constraints, and stop conditions.
2. Pass/fail: Required evidence is collected before any completion, approval, or readiness claim.
3. Pass/fail: The next action follows the documented gate order without skipping review or verification steps.
4. Pressure-test scenario: Apply the workflow under time pressure with one failing check and one tempting shortcut.
5. Success metric: Zero rationalizations; blocked, failed, or unverified work is reported as such.

## Migration Checklist

- [ ] Old behavior described precisely
- [ ] New behavior described precisely
- [ ] Replacement path documented
- [ ] Upgrade steps ordered and testable
- [ ] Rollback or compatibility notes included
- [ ] README/setup docs updated if user-facing behavior changed

## References & Resources

### Documentation
- [Deprecation Procedures](./references/deprecation.md) - Deprecation wording, timelines, and migration guidance patterns

### Scripts
- [Migration Guide Scaffold](./scripts/migration-guide-scaffold.py) - Generate a migration guide skeleton with version, impact, and step sections

<!-- PORTABILITY:START -->
## Cross-Client Portability

This skill is written to stay usable across GitHub Copilot, Claude Code, Codex, and Gemini CLI.

- GitHub Copilot: keep the folder in a Copilot-visible skill or plugin path, or wrap the workflow as project instructions if the host does not support portable skill folders directly.
- Claude Code: keep the folder in a local skills directory or a compatible plugin or marketplace source.
- Codex: install or sync the folder into `$CODEX_HOME/skills/<skill-name>` and restart Codex after major changes.
- Gemini CLI: this repository generates a project command named `/skills:breaking-changes-management` from this skill. Rebuild commands with `python scripts/export-gemini-skill.py breaking-changes-management` and then run `/commands reload` inside Gemini CLI.

<!-- PORTABILITY:END -->

<!-- MCP:START -->
## MCP Availability And Fallback

Preferred MCP Server: None required

- Fallback prompt: "Use the Breaking Changes Management skill without MCP. Rely on the local `SKILL.md`, bundled references or scripts, and manual verification. Show the exact commands, evidence, and final checks you used before concluding."
- If the current host does not expose a matching server, use the bundled references, scripts, native toolchain, and manual workflow already described in this skill.
- Treat direct local verification, rendered output, logs, tests, or screenshots as the fallback evidence path before completion.

<!-- MCP:END -->

## Related Skills

- [development-workflow](../development-workflow/SKILL.md): Use it when the workflow also needs planning, quality gates, and delivery tracking.
- [code-quality](../code-quality/SKILL.md): Use it when the workflow also needs two-stage review (spec compliance first, then code quality), maintainability, and refactoring guidance.
- [systematic-debugging](../systematic-debugging/SKILL.md): Use it when the workflow also needs root-cause debugging before proposing fixes.
- [test-driven-development](../test-driven-development/SKILL.md): Use it when the workflow also needs test-first implementation and regression safety.
