---
name: notion-docs
version: "1.2"
last_updated: 2026-04-25
tags: [notion, docs, writing, quality, templates]
description: "Notion workspace management via MCP - create databases, pages, comments, and knowledge bases. Use when building Notion documentation, organizing project wikis, or managing Notion content."
---

# Notion Documentation

> Tech Stack Target / Version: Notion API current version, Markdown-to-Notion transforms, and local template scripts.

Use this skill when Notion is the system of record for specs, runbooks, project tracking, or knowledge management.

- Leverage native parallel subagent dispatch and 200k+ context windows where available.


## Current MCP Reality

As of March 2026, Notion documents two supported ways to use its MCP server:

- Hosted remote MCP endpoint: `https://mcp.notion.com/mcp`
- Local stdio server package: `@notionhq/notion-mcp-server`

Hosted mode uses OAuth. Local mode uses an internal integration token. Official docs also list supported tools for searching content, reading pages, comments, users, and working with pages and databases.

## Activation Conditions

Use symptom -> action triggers: when one matches, apply this skill and verify with the protocol below.

- Creating or updating Notion pages
- Building project trackers or engineering knowledge bases
- Organizing specs, ADRs, and onboarding docs in Notion
- Adding review comments or using database-backed workflows

## Practical Workflow

1. Confirm whether the client exposes the hosted Notion MCP server or a local stdio connection.
2. Read or search existing pages before creating duplicates.
3. Use databases for tracked work and pages for long-form documents.
4. Keep properties simple: owner, status, last reviewed, tags.
5. If MCP is unavailable in the current client, fall back to local content prep using the included script and templates.

## Operational Notes

- Official Notion guidance currently documents an average rate limit of 20 requests per second for integrations.
- Tool names can vary slightly by MCP host, but the supported capabilities are stable: search, fetch page content, create or update pages, create or update databases, manage comments, and read user context.

## Documentation Stack Reference

Inherit the shared stack from [documentation-patterns](../documentation-patterns/SKILL.md#shared-documentation-stack): source-of-truth discovery, audience framing, structure selection, verification, and freshness checks. Keep this skill focused on Notion conversion and workspace behavior instead of restating the full stack.

## Anti-Patterns

- Writing for the author instead of the reader: It bakes in unstated context and leaves the actual audience unsure what to do next.
- Skipping concrete examples or commands: Abstract guidance is easy to approve and hard to apply correctly.
- Letting links, screenshots, or versions drift: Polished formatting does not help if the instructions are no longer true.

## Verification Protocol

Before claiming "skill applied successfully":

1. Pass/fail: The Notion Docs output identifies audience, purpose, source of truth, and freshness requirements.
2. Pass/fail: Shared documentation-stack guidance is referenced instead of duplicating another documentation skill.
3. Pass/fail: Claims, links, commands, examples, and screenshots are verified or explicitly marked unverified.
4. Pressure-test scenario: Apply the skill to a doc request with a stale command, missing owner, and conflicting audience.
5. Success metric: Zero undocumented assumptions; every reader-facing claim is sourced or scoped.


## References & Resources

### Documentation
- [Notion Markdown Spec](./references/notion-markdown-spec.md) - Notion-flavored Markdown constraints and conversion notes
- [Database Properties](./references/database-properties.md) - Practical property patterns for docs and project trackers
- [Notion MCP Quickstart](./references/notion-mcp-quickstart.md) - Hosted endpoint, local package, auth options, and usage notes

### Scripts
- [Notion Templates](./scripts/notion-templates.js) - Local page and database template helpers for environments without Notion MCP access

### Examples
- [Workspace Setup Example](./examples/workspace-setup-example.md) - Example team workspace structure using pages, databases, and review comments

<!-- PORTABILITY:START -->
## Cross-Client Portability

This skill is written to stay usable across GitHub Copilot, Claude Code, Codex, and Gemini CLI.

- GitHub Copilot: keep the folder in a Copilot-visible skill or plugin path, or wrap the workflow as project instructions if the host does not support portable skill folders directly.
- Claude Code: keep the folder in a local skills directory or a compatible plugin or marketplace source.
- Codex: install or sync the folder into `$CODEX_HOME/skills/<skill-name>` and restart Codex after major changes.
- Gemini CLI: this repository generates a project command named `/skills:notion-docs` from this skill. Rebuild commands with `python scripts/export-gemini-skill.py notion-docs` and then run `/commands reload` inside Gemini CLI.

<!-- PORTABILITY:END -->

<!-- MCP:START -->
## MCP Availability And Fallback

Preferred MCP Server: Notion MCP

- Fallback prompt: "Use the Notion Documentation skill without MCP. Rely on the local `SKILL.md`, bundled references or scripts, and manual verification. Show the exact commands, evidence, and final checks you used before concluding."
- Draft content locally in Markdown or JSON, then use `scripts/notion-templates.js` and the Notion web UI for final publishing.
- Prefer page and database templates from this skill to avoid duplicate structures when working without MCP.

<!-- MCP:END -->

## Related Skills

- [documentation-authoring](../documentation-authoring/SKILL.md): Use it when the workflow also needs drafting structured technical or product documents.
- [documentation-patterns](../documentation-patterns/SKILL.md): Use it when the workflow also needs reusable documentation structures and templates.
- [documentation-quality](../documentation-quality/SKILL.md): Use it when the workflow also needs documentation review standards and quality gates.
- [documentation-verification](../documentation-verification/SKILL.md): Use it when the workflow also needs final documentation validation before publishing.
