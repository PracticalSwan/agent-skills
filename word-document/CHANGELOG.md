# Changelog

## [2026-07-29] - Version 2.0 Client Support Reset

### Added

- Added the current GitHub Copilot, Claude Code, and Codex portability baseline.

### Changed

- **BREAKING:** Removed Gemini CLI and Antigravity as supported clients.
- Refreshed catalog metadata and last-updated state for the 2026-07-29 maintenance pass.
- Kept the retained-client portability, MCP fallback, Anti-Patterns, Verification Protocol, and Related Skills sections aligned.

### Fixed

- Prevented catalog modernization from reintroducing removed Gemini or Antigravity guidance.

## [2026-07-11] - Catalog Maintenance Refresh

### Added

- Added the current catalog verification baseline where it was missing.

### Changed

- Refreshed catalog metadata and last-updated state for the 2026-07-11 maintenance pass.
- Kept the cross-client, MCP fallback, Anti-Patterns, Verification Protocol, and Related Skills sections aligned.
- Reclassified historical `Tested` or `Verified` changelog headings under the allowed changelog vocabulary without dropping their evidence.

### Fixed

- Closed validator and documentation drift so the enforced schema matches the documented skill baseline.

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
- Added a Tech Stack Target / Version note so Word automation guidance is tied to current OOXML-compatible workflows.
## [2026-04-04] - Cross-Client Portability Refresh

### Changed
- Added a standard portability note covering GitHub Copilot, Claude Code, Codex, and Gemini CLI.
- Documented the preferred MCP server surface for this skill and a local no-MCP fallback workflow.

### Changed
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
