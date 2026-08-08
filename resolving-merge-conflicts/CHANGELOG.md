# Changelog

All notable changes to the `resolving-merge-conflicts` skill are documented here.

## [2026-08-08] - Workspace Fit And Catalog Import

### Added

- Added the MIT-licensed upstream skill from `mattpocock/skills` at commit `84fdeffd12f2ee307994d1eb6feb48173b6e0502`.

### Changed

- Added the catalog metadata, cross-client portability, MCP fallback, and verification baseline.
- Added explicit approval gates around abort, reset, clean, history rewrite, staging, and completion.

### Fixed

- Prevented conflict resolution from silently performing destructive or history-changing Git operations.

## [2026-07-29] - Version 2.0 Client Support Reset

### Added

- Added the current GitHub Copilot, Claude Code, and Codex portability baseline.

### Changed

- **BREAKING:** Removed Gemini CLI and Antigravity as supported clients.
- Refreshed catalog metadata and last-updated state for the 2026-07-29 maintenance pass.
- Kept the retained-client portability, MCP fallback, Anti-Patterns, Verification Protocol, and Related Skills sections aligned.

### Fixed

- Prevented catalog modernization from reintroducing removed Gemini or Antigravity guidance.
