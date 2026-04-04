---
name: documentation-verification
description: Validate documentation before merging - check completeness, broken links, code example accuracy, and factual correctness. Use when reviewing docs for quality gates or running pre-merge doc validation.
license: Complete terms in LICENSE.txt
---
# Documentation Verification

Use this skill when a docs change needs evidence, not just a writing pass.

## Activation Conditions

- Reviewing docs before merge or release
- Checking README, setup, or config accuracy
- Verifying local links, commands, and code samples
- Confirming docs changed alongside user-facing behavior

## Verification Workflow

1. Confirm the docs cover the changed behavior.
2. Check relative links and referenced files.
3. Validate commands and snippets where feasible.
4. Report missing coverage and stale claims explicitly.

## Review Checklist

- [ ] Public behavior changes are documented
- [ ] Local links resolve
- [ ] Examples and commands still make sense
- [ ] Setup steps reflect current tool versions
- [ ] README and CHANGELOG were updated when required

## References & Resources

### Documentation
- [Validation Procedures](./references/validation.md) - Practical checks for links, examples, config, and coverage

### Scripts
- [Doc Link Check](./scripts/doc-link-check.py) - Validate relative Markdown links across one file or an entire docs tree

<!-- PORTABILITY:START -->
## Cross-Client Portability

This skill is written to stay usable across GitHub Copilot, Claude Code, Codex, and Gemini CLI.

- GitHub Copilot: keep the folder in a Copilot-visible skill or plugin path, or wrap the workflow as project instructions if the host does not support portable skill folders directly.
- Claude Code: keep the folder in a local skills directory or a compatible plugin or marketplace source.
- Codex: install or sync the folder into `$CODEX_HOME/skills/<skill-name>` and restart Codex after major changes.
- Gemini CLI: this repository generates a project command named `/skills:documentation-verification` from this skill. Rebuild commands with `python scripts/export-gemini-skill.py documentation-verification` and then run `/commands reload` inside Gemini CLI.

<!-- PORTABILITY:END -->

<!-- MCP:START -->
## MCP Availability And Fallback

No dedicated MCP server is required for the normal workflow in this skill.

- If the current host lacks an equivalent tool surface, use the bundled scripts, standard shell or editor tooling, and the manual workflow already described in this skill.
- Treat local verification as the fallback evidence path before closing the task.

<!-- MCP:END -->

## Related Skills
| Skill | Relationship |
|-------|-------------|
| [documentation-quality](../documentation-quality/SKILL.md) | Quality standards to verify against |
| [documentation-authoring](../documentation-authoring/SKILL.md) | Verify authored docs before publishing |
| [code-examples-sync](../code-examples-sync/SKILL.md) | Validate code examples are current and working |
