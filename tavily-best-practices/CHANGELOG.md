# Changelog

All notable changes to the `tavily-best-practices` skill are documented here.

## [2026-08-14] - Catalog Freshness And Source Sync

### Added

- Refreshed the catalog metadata and retained-client portability baseline.

### Changed

- Updated the catalog metadata and last-updated state for the 2026-08-14 maintenance pass.
- Kept the retained-client portability, MCP fallback, Anti-Patterns, Verification Protocol, and Related Skills sections aligned.

### Fixed

- Preserved explicit no-MCP fallbacks and the catalog's safety, approval, and source-boundary guidance.

## [2026-07-30] - Initial Catalog Import

### Added

- Imported the official Tavily SDK and integration guidance from `tavily-ai/skills`.
- Added catalog metadata, cross-client portability, Tavily MCP fallback, verification, and related-skill routing.

### Changed

- Normalized credential handling around environment variables and approved secret stores.
- Removed the out-of-scope removed-client integration while retaining current Claude Code, Codex, GitHub Copilot, SDK, CLI, and MCP paths.

### Fixed

- Added explicit prompt-injection, API-usage, method-selection, and citation-verification boundaries.
