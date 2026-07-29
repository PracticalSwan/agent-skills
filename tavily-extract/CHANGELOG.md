# Changelog

All notable changes to the `tavily-extract` skill are documented here.

## [2026-07-30] - Initial Catalog Import

### Added

- Imported the official Tavily CLI extraction workflow from `tavily-ai/skills`.
- Added catalog metadata, cross-client portability, Tavily MCP fallback, verification, and related-skill routing.

### Changed

- Replaced the default pipe-to-shell setup with reviewable CLI installation and authentication checks.
- Clarified bounded batches, focused chunks, and JavaScript-heavy page handling.

### Fixed

- Added private-URL, prompt-injection, failed-result, and credential safeguards.
