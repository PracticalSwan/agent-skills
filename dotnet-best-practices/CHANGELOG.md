# Changelog

All notable changes to the `dotnet-best-practices` skill will be documented in this file.

## [2026-04-04] - Initial Import and Portability Upgrade

### Added
- Imported this skill from `https://github.com/github/awesome-copilot` at `skills/dotnet-best-practices`.
- Added cross-client portability guidance for GitHub Copilot, Claude Code, Codex, and Gemini CLI.
- Added the repo-standard MCP or no-MCP fallback guidance for this skill.

### Changed
- Rewrote the description and scope wording so the guidance applies cleanly across clients and no longer depends on a host-specific `${selection}` placeholder.

### Tested
- Validated `SKILL.md` frontmatter and Gemini command export readiness with `python scripts/validate-skills.py`.
