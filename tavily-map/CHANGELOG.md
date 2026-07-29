# Changelog

All notable changes to the `tavily-map` skill are documented here.

## [2026-07-30] - Initial Catalog Import

### Added

- Imported the official Tavily CLI URL-mapping workflow from `tavily-ai/skills`.
- Added catalog metadata, cross-client portability, Tavily MCP fallback, verification, and related-skill routing.

### Changed

- Replaced the default pipe-to-shell setup with reviewable CLI installation and authentication checks.
- Clarified path, domain, depth, breadth, and external-link boundaries.

### Fixed

- Distinguished URL discovery from content verification and added prompt-injection and credential safeguards.
