---
name: documentation-automation
version: "1.3"
last_updated: 2026-07-11
tags: [documentation, automation, docs, writing, quality]
description: "Automate doc generation with JSDoc/TSDoc, linters, and pre-commit hooks. Use when setting up markdownlint, configuring doc linting pipelines, integrating JSDoc/TSDoc, or building automated documentation workflows."
---
# Documentation Automation

Use this skill when documentation quality should be enforced by scripts, CI, or local hooks instead of manual review alone.

- Leverage native parallel subagent dispatch and 200k+ context windows where available.


## Activation Conditions

Use symptom -> action triggers: when one matches, apply this skill and verify with the protocol below.

- Adding `docs:*` scripts to a project
- Setting up markdownlint, cspell, lychee, or remark-lint
- Generating API docs from source comments
- Adding pre-commit or CI validation for docs
- Standardizing documentation checks across repositories

## Automation Targets

- Build generated API docs
- Lint Markdown structure and style
- Check internal and external links
- Validate code examples and commands
- Enforce changelog or README updates when behavior changes

## Recommended Pipeline

1. Add local commands that can run without CI.
2. Make CI call the same commands.
3. Keep failure output actionable and fast.
4. Prefer incremental checks in pre-commit and fuller checks in CI.

## Documentation Stack Reference

Inherit the shared stack from [documentation-patterns](../documentation-patterns/SKILL.md#shared-documentation-stack): source-of-truth discovery, audience framing, structure selection, verification, and freshness checks. Keep this skill focused on automation pipelines instead of restating the full stack.

## Anti-Patterns

- Writing for the author instead of the reader: It bakes in unstated context and leaves the actual audience unsure what to do next.
- Skipping concrete examples or commands: Abstract guidance is easy to approve and hard to apply correctly.
- Letting links, screenshots, or versions drift: Polished formatting does not help if the instructions are no longer true.

## Verification Protocol

Before claiming "skill applied successfully":

1. Pass/fail: The Documentation Automation output identifies audience, purpose, source of truth, and freshness requirements.
2. Pass/fail: Shared documentation-stack guidance is referenced instead of duplicating another documentation skill.
3. Pass/fail: Claims, links, commands, examples, and screenshots are verified or explicitly marked unverified.
4. Pressure-test scenario: Apply the skill to a doc request with a stale command, missing owner, and conflicting audience.
5. Success metric: Zero undocumented assumptions; every reader-facing claim is sourced or scoped.

## References & Resources

### Documentation
- [Automated Tools](./references/tools.md) - Current doc tooling options by language and validation task

### Scripts
- [Docs Pipeline Scaffold](./scripts/docs-pipeline-scaffold.py) - Print starter `docs:*` scripts and a CI checklist for Node or Python projects

<!-- PORTABILITY:START -->
## Cross-Client Portability

This skill is written to stay usable across GitHub Copilot, Claude Code, Codex, and Gemini CLI.

- GitHub Copilot: keep the folder in a Copilot-visible skill or plugin path, or wrap the workflow as project instructions if the host does not support portable skill folders directly.
- Claude Code: keep the folder in a local skills directory or a compatible plugin or marketplace source.
- Codex: install or sync the folder into `$CODEX_HOME/skills/<skill-name>` and restart Codex after major changes.
- Gemini CLI: this repository generates a project command named `/skills:documentation-automation` from this skill. Rebuild commands with `python scripts/export-gemini-skill.py documentation-automation` and then run `/commands reload` inside Gemini CLI.

<!-- PORTABILITY:END -->

<!-- MCP:START -->
## MCP Availability And Fallback

Preferred MCP Server: None required

- Fallback prompt: "Use the Documentation Automation skill without MCP. Rely on the local `SKILL.md`, bundled references or scripts, and manual verification. Show the exact commands, evidence, and final checks you used before concluding."
- If the current host does not expose a matching server, use the bundled references, scripts, native toolchain, and manual workflow already described in this skill.
- Treat direct local verification, rendered output, logs, tests, or screenshots as the fallback evidence path before completion.

<!-- MCP:END -->

## Related Skills

- [documentation-authoring](../documentation-authoring/SKILL.md): Use it when the workflow also needs drafting structured technical or product documents.
- [documentation-patterns](../documentation-patterns/SKILL.md): Use it when the workflow also needs reusable documentation structures and templates.
- [documentation-quality](../documentation-quality/SKILL.md): Use it when the workflow also needs documentation review standards and quality gates.
- [documentation-verification](../documentation-verification/SKILL.md): Use it when the workflow also needs final documentation validation before publishing.
