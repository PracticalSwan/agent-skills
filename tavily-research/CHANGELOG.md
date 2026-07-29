# Changelog

All notable changes to the `tavily-research` skill are documented here.

## [2026-07-30] - Initial Catalog Import

### Added

- Imported the official Tavily CLI research workflow from `tavily-ai/skills`.
- Added catalog metadata, cross-client portability, research fallback, verification, and related-skill routing.

### Changed

- Replaced the default pipe-to-shell setup with reviewable CLI installation and authentication checks.
- Clarified model choice, bounded polling, terminal job state, and saved-artifact handling.

### Fixed

- Added cost-awareness, citation spot-checking, failed-job, credential, and uncertainty safeguards.
