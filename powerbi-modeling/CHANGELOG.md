# Changelog

All notable changes to this skill will be documented in this file.

## [2026-04-24] - Skill Refresh

### Changed
- Standardized the SKILL frontmatter with version metadata, last-updated date, tags, and a concise catalog description.
- Reformatted the portability and MCP guidance with a preferred server line, a copy-paste fallback prompt, and consistent bullet lists.
- Added a catalog-standard Anti-Patterns section and refreshed the Related Skills links at the end of the skill.
- Added a Tech Stack Target / Version note so the modeling guidance is anchored to current Power BI and DAX tooling.
## [2026-04-04] - Cross-Client Portability Refresh

### Changed
- Added a standard portability note covering GitHub Copilot, Claude Code, Codex, and Gemini CLI.
- Documented the preferred MCP server surface for this skill and a local no-MCP fallback workflow.

### Tested
- Validated `SKILL.md` frontmatter, portability sections, and Gemini export readiness with `python scripts/validate-skills.py`.
## [2026-03-09] - Workspace Modernization

### Changed
- Rewrote the skill to treat Power BI modeling MCP access as host-specific and to pair it explicitly with Microsoft Learn documentation lookups

## [2026-02-28] — Description Rewrite & Cross-References

### Changed
- Rewrote skill description to ~200 characters with clear, specific activation keywords
- Improved keyword specificity to reduce overlap with related skills

### Added
- `## Related Skills` cross-reference table with 2-4 related skills and "Use When" guidance
