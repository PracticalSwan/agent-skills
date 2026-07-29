# Changelog

All notable changes to the `tavily-search` skill are documented here.

## [2026-07-30] - Initial Catalog Import

### Added

- Imported the official Tavily CLI search workflow from `tavily-ai/skills`.
- Added catalog metadata, cross-client portability, Tavily MCP fallback, verification, and related-skill routing.

### Changed

- Replaced the default pipe-to-shell setup with reviewable CLI installation and authentication checks.
- Clarified query, domain, date, and result-count scoping.

### Fixed

- Added prompt-injection, source-opening, freshness, citation, and credential boundaries.
