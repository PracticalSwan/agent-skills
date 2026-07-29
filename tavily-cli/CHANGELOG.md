# Changelog

All notable changes to the `tavily-cli` skill are documented here.

## [2026-07-30] - Initial Catalog Import

### Added

- Imported the official Tavily CLI routing workflow from `tavily-ai/skills`.
- Added catalog metadata, cross-client portability, Tavily MCP fallback, verification, and related-skill routing.

### Changed

- Replaced the default pipe-to-shell setup with reviewable `uv` and `pip` installation choices.
- Documented PowerShell adaptation and GLM-backed Claude Code operation without assumed native browser tooling.

### Fixed

- Added secret-handling, external-content, bounded-scope, and execution-evidence safeguards.
