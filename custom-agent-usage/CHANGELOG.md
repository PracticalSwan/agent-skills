# Changelog

## [2026-04-25] - Version 1.2 Verification Protocol Refresh

### Added
- Added a `Verification Protocol` section with skill-specific pass/fail checks, one pressure-test scenario, and a measurable success metric.
- Added guidance to leverage native parallel subagent dispatch and 200k+ context windows where available.

### Changed
- Updated `SKILL.md` frontmatter to `version: "1.2"` and `last_updated: 2026-04-25`.
- Reframed activation guidance toward symptom -> action triggers and standardized two-stage review wording where applicable.

## [2026-04-24] - Version 1.1 Refresh

### Changed
- Updated the SKILL frontmatter version to `1.1` for the 2026-04-24 catalog refresh.

## [2026-04-24] - Skill Refresh

### Changed
- Standardized the SKILL frontmatter with version metadata, last-updated date, tags, and a concise catalog description.
- Reformatted the portability and MCP guidance with a preferred server line, a copy-paste fallback prompt, and consistent bullet lists.
- Added a catalog-standard Anti-Patterns section and refreshed the Related Skills links at the end of the skill.
## [2026-04-24] - Catalog Audit Cleanup

### Fixed
- Removed obsolete standalone Skill Paths guidance that duplicated the generated portability section.

All notable changes to this skill will be documented in this file.

## [2026-04-04] - Cross-Client Portability Refresh

### Changed
- Added a standard portability note covering GitHub Copilot, Claude Code, Codex, and Gemini CLI.
- Clarified that the core workflow does not require a dedicated MCP server and can run with local tools alone.

### Tested
- Validated `SKILL.md` frontmatter, portability sections, and Gemini export readiness with `python scripts/validate-skills.py`.
## [2026-03-09] - Custom Agent Discovery Correction

### Changed
- Repointed custom-agent discovery guidance to the real local agent directories: `C:\Users\LOQ\.claude\agents` and `C:\Users\LOQ\AppData\Roaming\Code - Insiders\User\prompts`
- Updated the examples to search those directories directly instead of treating repo-local Copilot paths as the primary discovery roots

### Fixed
- Removed the stale `.copilot/agents` and `.github/copilot/agents` discovery guidance
- Clarified that the VS Code Insiders prompts directory also contains `.prompt.md` and `.instructions.md`, so discovery must filter to `*.agent.md`
- Removed the external `glob` dependency from the helper script so it runs in the plain local Node environment used in this workspace

### Tested
- Checked the real local directories on this machine and confirmed both exist
- Verified the correction against the files currently present in the Claude and VS Code Insiders agent directories

## [2026-03-09] - Workspace Modernization

### Changed
- Updated the workspace and global skill path guidance to match the current `C:/Users/LOQ/.agents/skills/` fallback path
- Removed duplicate related-skill content so the skill reads cleanly

## [2026-02-28] - Description Rewrite & Cross-References

### Changed
- Rewrote skill description to ~200 characters with clear, specific activation keywords
- Improved keyword specificity to reduce overlap with related skills

### Added
- `## Related Skills` cross-reference table with 2-4 related skills and "Use When" guidance
