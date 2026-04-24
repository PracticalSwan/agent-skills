# Changelog

## [2026-04-24] - Catalog Audit Cleanup

### Fixed
- Removed obsolete standalone Skill Paths guidance that duplicated the generated portability section.

All notable changes to this skill will be documented in this file.

## [2026-04-04] - Cross-Client Portability Refresh

### Changed
- Added a standard portability note covering GitHub Copilot, Claude Code, Codex, and Gemini CLI.
- Documented the preferred MCP server surface for this skill and a local no-MCP fallback workflow.

### Tested
- Validated `SKILL.md` frontmatter, portability sections, and Gemini export readiness with `python scripts/validate-skills.py`.
## [2026-03-09] - Workspace Modernization

### Added
- Added a 2026-03-09 maintenance entry after reviewing the skill; the earlier unit-test activation improvements remained the only content changes needed.

## [2026-03-01] — Activation Fix

### Fixed
- Added "unit tests" alongside E2E — previously only activated for Playwright/E2E testing prompts
- Changed "E2E tests" to "E2E/unit tests" in description

## [2026-02-28] — Description Rewrite & Cross-References

### Changed
- Rewrote skill description to ~200 characters with clear, specific activation keywords
- Improved keyword specificity to reduce overlap with related skills

### Added
- `## Related Skills` cross-reference table with 2-4 related skills and "Use When" guidance
