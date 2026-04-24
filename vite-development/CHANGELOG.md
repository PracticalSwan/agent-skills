# Changelog

All notable changes to this skill will be documented in this file.

## [2026-04-24] - Current Version Refresh

### Changed
- Updated the active Vite guidance from Vite 6+ to Vite 8.0.10 after checking the current npm package version.

### Tested
- Verified current published package versions with `npm view vite version` and `npm view @vitejs/plugin-react version`.

## [2026-04-04] - Cross-Client Portability Refresh

### Changed
- Added a standard portability note covering GitHub Copilot, Claude Code, Codex, and Gemini CLI.
- Clarified that the core workflow does not require a dedicated MCP server and can run with local tools alone.

### Tested
- Validated `SKILL.md` frontmatter, portability sections, and Gemini export readiness with `python scripts/validate-skills.py`.
## [2026-03-09] - Workspace Modernization

### Added
- Added a 2026-03-09 maintenance entry after reviewing the skill; the existing structure and guidance remained suitable.

## [2026-02-28] — Description Rewrite & Cross-References

### Changed
- Rewrote skill description to ~200 characters with clear, specific activation keywords
- Improved keyword specificity to reduce overlap with related skills

### Added
- `## Related Skills` cross-reference table with 2-4 related skills and "Use When" guidance
