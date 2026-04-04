# Changelog

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
