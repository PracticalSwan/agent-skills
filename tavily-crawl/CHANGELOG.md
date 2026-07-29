# Changelog

All notable changes to the `tavily-crawl` skill are documented here.

## [2026-07-30] - Initial Catalog Import

### Added

- Imported the official Tavily CLI crawl workflow from `tavily-ai/skills`.
- Added catalog metadata, cross-client portability, Tavily MCP fallback, verification, and related-skill routing.

### Changed

- Replaced the default pipe-to-shell setup with reviewable CLI installation and authentication checks.
- Clarified conservative depth, page, domain, path, timeout, and output-directory limits.

### Fixed

- Added private-target, prompt-injection, overwrite, credential, and partial-result safeguards.
