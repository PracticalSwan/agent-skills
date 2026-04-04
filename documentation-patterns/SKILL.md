---
name: documentation-patterns
description: Templates and structural patterns for API docs, feature docs, config guides, and REST endpoint documentation. Use when structuring docs, applying Markdown templates, or standardizing doc formats.
license: Complete terms in LICENSE.txt
---
# Documentation Patterns

Use this skill when the main problem is document shape and consistency rather than writing quality alone.

## Activation Conditions

- Creating a new API, feature, or config guide
- Standardizing Markdown sections across repositories
- Writing migration or runbook documents
- Picking the right template for a doc request

## Pattern Selection

- API docs: endpoints, auth, request and response schema, errors
- Feature docs: purpose, UX, dependencies, rollout, support
- Config docs: env vars, defaults, examples, failure modes
- Migration docs: changed behavior, upgrade path, verification

## References & Resources

### Documentation
- [API Documentation Templates](./references/api-templates.md) - Endpoint, SDK, and function documentation patterns
- [Feature Documentation Templates](./references/feature-templates.md) - Feature overview, rollout, and troubleshooting patterns
- [Configuration Documentation Templates](./references/config-templates.md) - Config and environment variable templates

### Scripts
- [Doc Template Picker](./scripts/doc-template-picker.py) - Print a starter Markdown template for `api`, `feature`, `config`, or `migration`

<!-- PORTABILITY:START -->
## Cross-Client Portability

This skill is written to stay usable across GitHub Copilot, Claude Code, Codex, and Gemini CLI.

- GitHub Copilot: keep the folder in a Copilot-visible skill or plugin path, or wrap the workflow as project instructions if the host does not support portable skill folders directly.
- Claude Code: keep the folder in a local skills directory or a compatible plugin or marketplace source.
- Codex: install or sync the folder into `$CODEX_HOME/skills/<skill-name>` and restart Codex after major changes.
- Gemini CLI: this repository generates a project command named `/skills:documentation-patterns` from this skill. Rebuild commands with `python scripts/export-gemini-skill.py documentation-patterns` and then run `/commands reload` inside Gemini CLI.

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
| [documentation-authoring](../documentation-authoring/SKILL.md) | Use patterns when creating new documents |
| [documentation-quality](../documentation-quality/SKILL.md) | Quality standards that patterns should follow |
| [breaking-changes-management](../breaking-changes-management/SKILL.md) | Templates for migration guides and changelogs |
