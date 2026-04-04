# Changelog

All notable changes to this skill will be documented in this file.

## [2026-04-04] - Cross-Client Portability Refresh

### Changed
- Added a standard portability note covering GitHub Copilot, Claude Code, Codex, and Gemini CLI.
- Clarified that the core workflow does not require a dedicated MCP server and can run with local tools alone.

### Tested
- Validated `SKILL.md` frontmatter, portability sections, and Gemini export readiness with `python scripts/validate-skills.py`.
## [2026-03-09] - Workspace Modernization

### Changed
- Rewrote the skill into a tighter breaking-change workflow focused on migration impact, replacement paths, and release notes

### Added
- `scripts/migration-guide-scaffold.py` to generate migration-guide templates for breaking releases

## [2026-02-28] — Description Rewrite & Cross-References

### Changed
- Rewrote skill description to ~200 characters with clear, specific activation keywords
- Improved keyword specificity to reduce overlap with related skills

### Added
- `## Related Skills` cross-reference table with 2-4 related skills and "Use When" guidance
