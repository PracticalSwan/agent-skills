# Changelog

All notable changes to the `skill-creator` skill are documented here.

## [2026-08-14] - Catalog Freshness And Source Sync

### Added

- Refreshed the catalog metadata and retained-client portability baseline.

### Changed

- Updated the catalog metadata and last-updated state for the 2026-08-14 maintenance pass.
- Kept the retained-client portability, MCP fallback, Anti-Patterns, Verification Protocol, and Related Skills sections aligned.

### Fixed

- Preserved explicit no-MCP fallbacks and the catalog's safety, approval, and source-boundary guidance.

## [2026-07-29] - Version 2.0 Client Support Reset

### Added

- Promoted this skill from a verified `.codex` or `.claude` child path into the parent catalog.
- Added the current GitHub Copilot, Claude Code, and Codex portability baseline.

### Changed

- **BREAKING:** Removed Gemini CLI and Antigravity as supported clients.
- Added target-host selection for Codex, Claude Code, and shared-catalog skill
  roots.
- Refreshed catalog metadata and last-updated state for the 2026-07-29 maintenance pass.
- Kept the retained-client portability, MCP fallback, Anti-Patterns, Verification Protocol, and Related Skills sections aligned.

### Fixed

- Prevented catalog modernization from reintroducing removed Gemini or Antigravity guidance.
- Updated `quick_validate.py` to accept the catalog's version, date, tags, and
  compatibility metadata while retaining upstream name and description checks.
