# Changelog

All notable changes to this skill will be documented in this file.

## [2026-04-04] - Cross-Client Portability Refresh

### Changed
- Added a standard portability note covering GitHub Copilot, Claude Code, Codex, and Gemini CLI.
- Documented the preferred MCP server surface for this skill and a local no-MCP fallback workflow.

### Tested
- Validated `SKILL.md` frontmatter, portability sections, and Gemini export readiness with `python scripts/validate-skills.py`.
## [2026-03-09] - Workspace Modernization

### Changed
- Rewrote the skill to describe Word MCP access as host-specific instead of assuming stable wrapper commands
- Repositioned the local document generator as the fallback path when Word MCP tools are unavailable

## [2026-02-28] - Description Rewrite and Cross-References

### Changed
- Rewrote the skill description to concise activation-focused wording
- Improved keyword specificity to reduce overlap with related skills

### Added
- Added the related-skills cross-reference table

## [2026-02-19] - Word MCP Extraction

### Changed
- Split Word workflow guidance out of the former shared office-documents skill into a Word-specific skill
- Replaced library-first guidance with MCP-oriented document workflows
- Updated activation triggers around `.docx`, Word documents, and Word MCP use cases

### Added
- Added Word-specific references, examples, and local document-generation support
- Added coverage for document structure, formatting, tables, and review-oriented workflows

### Fixed
- Reduced ambiguity between generic office-document handling and Word-specific document tasks
