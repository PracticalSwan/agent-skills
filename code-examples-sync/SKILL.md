---
name: code-examples-sync
version: "2.0"
last_updated: 2026-07-29
tags: [code, examples, sync, workflow, quality]
description: "Synchronize and verify code examples in documentation. Use when function signatures change, API interfaces update, imports shift, or documentation snippets become outdated and need correction."
---
# Code Example Synchronization

Use this skill when docs contain code snippets that are likely to drift from the real implementation.

- Leverage native parallel subagent dispatch and 200k+ context windows where available.


## Activation Conditions

Use symptom -> action triggers: when one matches, apply this skill and verify with the protocol below.

- Function signatures changed
- Imports or package names changed
- Request or response contracts changed
- Framework guidance or recommended patterns changed
- A doc snippet compiles conceptually but no longer matches the codebase

## Workflow

1. Find the canonical implementation first.
2. Update every affected snippet in docs, examples, and READMEs.
3. Verify syntax, imports, and expected outputs.
4. Note any intentional divergence, such as simplified tutorial snippets.

## Anti-Patterns

- Starting work before the plan or gate is clear: Execution drifts when success criteria are implied instead of explicit.
- Treating verification as optional cleanup: The last mile is where regressions and missing updates are usually hiding.
- Mixing planning, implementation, and release work in one jump: You lose the causal chain that explains why a change is safe.

## Verification Protocol

Before claiming "skill applied successfully":

1. Pass/fail: The Code Examples Sync workflow starts from explicit success criteria, constraints, and stop conditions.
2. Pass/fail: Required evidence is collected before any completion, approval, or readiness claim.
3. Pass/fail: The next action follows the documented gate order without skipping review or verification steps.
4. Pressure-test scenario: Apply the workflow under time pressure with one failing check and one tempting shortcut.
5. Success metric: Zero rationalizations; blocked, failed, or unverified work is reported as such.

## Quality Checklist

- [ ] Snippet matches current API shape
- [ ] Imports and package names are current
- [ ] Async, error handling, and setup steps still make sense
- [ ] Output examples match current behavior
- [ ] Duplicate snippets across docs were updated together

## References & Resources

### Documentation
- [Code Example Verification](./references/verification.md) - Checks for examples, imports, outputs, and compatibility

### Scripts
- [Example Sync Check](./scripts/example-sync-check.py) - Audit Markdown files for untyped fences, placeholder text, and obviously stale examples

<!-- MCP:START -->

<!-- PORTABILITY:START -->
## Cross-Client Portability

This skill is written to stay usable across GitHub Copilot, Claude Code, and Codex.

- GitHub Copilot: keep the folder in a Copilot-visible skill path or wrap the
  workflow in project instructions when folder discovery is unavailable.
- Claude Code: keep the folder in a local skills directory or a compatible plugin source.
- Codex: install or sync the folder into
  `$CODEX_HOME/skills/code-examples-sync` and restart Codex after major changes.

<!-- PORTABILITY:END -->

## MCP Availability And Fallback

Preferred MCP Server: None required

- Fallback prompt: "Use the Code Example Synchronization skill without MCP. Rely on the local `SKILL.md`, bundled references or scripts, and manual verification. Show the exact commands, evidence, and final checks you used before concluding."
- If the current host does not expose a matching server, use the bundled references, scripts, native toolchain, and manual workflow already described in this skill.
- Treat direct local verification, rendered output, logs, tests, or screenshots as the fallback evidence path before completion.

<!-- MCP:END -->

## Related Skills

- [development-workflow](../development-workflow/SKILL.md): Use it when the workflow also needs planning, quality gates, and delivery tracking.
- [code-quality](../code-quality/SKILL.md): Use it when the workflow also needs two-stage review (spec compliance first, then code quality), maintainability, and refactoring guidance.
- [systematic-debugging](../systematic-debugging/SKILL.md): Use it when the workflow also needs root-cause debugging before proposing fixes.
- [test-driven-development](../test-driven-development/SKILL.md): Use it when the workflow also needs test-first implementation and regression safety.
