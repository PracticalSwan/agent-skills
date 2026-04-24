# Changelog

## [2026-04-25] - Version 1.2 Verification Protocol Refresh

### Added
- Added a `Verification Protocol` section with skill-specific pass/fail checks, one pressure-test scenario, and a measurable success metric.
- Added guidance to leverage native parallel subagent dispatch and 200k+ context windows where available.
- Added the shared `MCP Fallback ? Native Automation` section for Office-style workflows.

### Changed
- Updated `SKILL.md` frontmatter to `version: "1.2"` and `last_updated: 2026-04-25`.
- Reframed activation guidance toward symptom -> action triggers and standardized two-stage review wording where applicable.

## [2026-04-24] - Version 1.1 Refresh

### Changed
- Updated the SKILL frontmatter version to `1.1` for the 2026-04-24 catalog refresh.

All notable changes to this skill will be documented in this file.

## [2026-04-24] - Skill Refresh

### Changed
- Standardized the SKILL frontmatter with version metadata, last-updated date, tags, and a concise catalog description.
- Reformatted the portability and MCP guidance with a preferred server line, a copy-paste fallback prompt, and consistent bullet lists.
- Added a catalog-standard Anti-Patterns section and refreshed the Related Skills links at the end of the skill.
- Added a Tech Stack Target / Version note so deck-generation guidance is tied to the current slide tooling surface.
## [2026-04-04] - Cross-Client Portability Refresh

### Changed
- Added a standard portability note covering GitHub Copilot, Claude Code, Codex, and Gemini CLI.
- Documented the preferred MCP server surface for this skill and a local no-MCP fallback workflow.

### Tested
- Validated `SKILL.md` frontmatter, portability sections, and Gemini export readiness with `python scripts/validate-skills.py`.
## [2026-03-09] - Workspace Modernization

### Changed
- Rewrote the skill to describe presentation MCP access as host-specific instead of assuming stable wrapper tool names
- Repositioned the local automation script as the fallback path when MCP presentation tools are unavailable

## [2026-02-28] - Description Rewrite and Cross-References

### Changed
- Rewrote the skill description to concise activation-focused wording
- Improved keyword specificity to reduce overlap with related skills

### Added
- Added the related-skills cross-reference table

## [2026-02-19] - PowerPoint MCP Extraction

### Changed
- Split presentation workflow guidance out of the former shared office-documents skill into a PowerPoint-specific skill
- Replaced library-first guidance with MCP-oriented presentation workflows
- Updated activation triggers around presentations, slide decks, `.pptx`, and PowerPoint MCP use cases

### Added
- Added PowerPoint-specific references and local automation support
- Added coverage for slide management, text, templates, images, and presentation extraction workflows

### Fixed
- Reduced ambiguity between generic office-document handling and PowerPoint-specific presentation tasks
