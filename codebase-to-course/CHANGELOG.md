# Changelog

All notable changes to the `codebase-to-course` skill will be documented in this file.

## [2026-04-24] - Initial Import and Portability Upgrade

### Added
- Imported the skill from `https://github.com/zarazhangrui/codebase-to-course` at `ff8837ecf8e9f6ce9874ffa42e42633394a52a00`.
- Imported the upstream `references/` course template assets used by the skill.
- Added cross-client portability guidance for GitHub Copilot, Claude Code, Codex, and Gemini CLI.
- Added the repo-standard no-MCP fallback guidance for this skill.

### Changed
- Clarified that parallel delegated-agent module writing depends on host support and user approval.

### Tested
- Validated `SKILL.md` frontmatter and Gemini command export readiness with `python scripts/validate-skills.py`.
