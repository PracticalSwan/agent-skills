# Changelog

All notable changes to the `tavily-dynamic-search` skill are documented here.

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

- Imported the official Tavily programmatic search and context-isolation workflow from `tavily-ai/skills`.
- Added catalog metadata, cross-client portability, Tavily MCP fallback, verification, and related-skill routing.

### Changed

- Replaced the default pipe-to-shell setup with reviewable CLI installation and authentication checks.
- Documented Windows PowerShell, local temporary-path, and GLM-backed Claude Code adaptations.

### Fixed

- Added prompt-injection, temporary-data, filter-bias, credential, and source-traceability safeguards.
