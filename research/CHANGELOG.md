# Changelog

All notable changes to the `research` skill are documented here.

## [2026-08-14] - Catalog Freshness And Source Sync

### Added

- Refreshed the catalog metadata and retained-client portability baseline.

### Changed

- Updated the catalog metadata and last-updated state for the 2026-08-14 maintenance pass.
- Kept the retained-client portability, MCP fallback, Anti-Patterns, Verification Protocol, and Related Skills sections aligned.

### Fixed

- Preserved explicit no-MCP fallbacks and the catalog's safety, approval, and source-boundary guidance.

## [2026-08-08] - Workspace Fit And Catalog Import

### Added

- Added the MIT-licensed upstream skill from `mattpocock/skills` at commit `84fdeffd12f2ee307994d1eb6feb48173b6e0502`.

### Changed

- Added the catalog metadata, cross-client portability, MCP fallback, and verification baseline.
- Added a same-session fallback for hosts without bounded background delegation.

### Fixed

- Prevented the workflow from claiming background-agent execution when the active host does not expose it.

## [2026-07-29] - Version 2.0 Client Support Reset

### Added

- Added the current GitHub Copilot, Claude Code, and Codex portability baseline.

### Changed

- **BREAKING:** Removed Gemini CLI and Antigravity as supported clients.
- Refreshed catalog metadata and last-updated state for the 2026-07-29 maintenance pass.
- Kept the retained-client portability, MCP fallback, Anti-Patterns, Verification Protocol, and Related Skills sections aligned.

### Fixed

- Prevented catalog modernization from reintroducing removed Gemini or Antigravity guidance.
