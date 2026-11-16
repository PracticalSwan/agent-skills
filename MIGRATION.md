# Migration Guide

This guide covers current catalog compatibility and the supported folder
layout. Detailed release history belongs in [CHANGELOG.md](CHANGELOG.md).

## Catalog version 2.0

Version 2.0 standardized skill metadata, portability guidance, fallbacks, and
verification. For each maintained skill:

1. Keep the skill folder name equal to the YAML `name`.
2. Include `version`, `last_updated`, `tags`, and an activation-focused
   `description` in frontmatter.
3. Provide cross-client portability guidance and an MCP or no-MCP fallback.
4. Put `## Verification Protocol` immediately after `## Anti-Patterns`.
5. Keep `## Related Skills` as the final level-two section.
6. Maintain a `CHANGELOG.md` in the skill folder.

Run `py -3 scripts/validate-skills.py` after migrating a skill. Preserve
source licenses and attribution when content is moved.

## Catalog name changes

- Use `frontend-design` for general interface creation and art direction.
  Framework, Figma, and Stitch workflows remain separate when they have a
  narrower tool contract. Use `web-design-reviewer` for post-implementation
  visual review.
- Browser CLI workflows use `playwright-cli`. Component testing and trace
  inspection use `playwright-component-testing` and `playwright-trace`.
- Use the current Gemini API skill family for supported Google API workflows.
  Retired standalone client integrations are not part of this catalog.
- Tavily's current set is `tavily-search`, `tavily-sdk`, `tavily-entity`,
  `tavily-list`, `tavily-monitor`, and `tavily-research`. The former
  `tavily-best-practices`, `tavily-cli`, `tavily-crawl`,
  `tavily-dynamic-search`, `tavily-extract`, and `tavily-map` entrypoints were
  retired and consolidated into the current six workflows. Read their local
  cross-links instead of reinstalling individual upstream skills.
- Similar research and writing skills remain separate when they have distinct
  activation boundaries or evidence requirements. Check the catalog index
  before merging or renaming them.

When retiring a catalog name, migrate useful content and licensing first,
update cross-references and source records, and add only the exact retired
folder to the sync cleanup list.

## Sync compatibility

The parent catalog is authoritative. Sync only to the three approved
user-global skill roots through `scripts/sync-skills.ps1`. Project-specific
skill directories are not downstream targets. The script preserves unknown
personal skills and host-managed content while pruning only reviewed retired
catalog folders.

Codex system-managed skills and protected Codex-only overlays stay outside the
shared catalog. Copied official Superpowers are routed separately according to
the registry and must not be treated as maintained imports.

## Rollback

Review the exact diff and restore only the affected files from the last known
good repository revision. Prefer a normal revert commit for published changes.
Do not rewrite published history without explicit authorization. After a
rollback, rerun catalog validation and verify the approved mirrors before
claiming the rollback is complete.
