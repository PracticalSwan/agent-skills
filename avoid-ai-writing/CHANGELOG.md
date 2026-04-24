# Changelog

All notable changes to the `avoid-ai-writing` skill will be documented in this file.

## [2026-04-24] - Initial Import and Portability Upgrade

### Added
- Imported the skill from `https://github.com/conorbronsdon/avoid-ai-writing` at `cbf885e087e8ec1168bc58dc603606a6e4bfacbd`.
- Added the upstream MIT license as `LICENSE.txt`.
- Added cross-client portability guidance for GitHub Copilot, Claude Code, Codex, and Gemini CLI.
- Added the repo-standard no-MCP fallback guidance for this skill.

### Changed
- Kept the upstream `SKILL.md` guidance intact while appending catalog-required generated sections.

### Tested
- Validated `SKILL.md` frontmatter and Gemini command export readiness with `python scripts/validate-skills.py`.
