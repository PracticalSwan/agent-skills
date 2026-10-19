# Changelog

All notable changes to the `paper-lookup` skill are documented here.

## [2026-10-19] - Catalog Freshness And Source Sync

### Added

- Added this skill from a reviewed upstream source and normalized it for the shared catalog.
- Refreshed the catalog metadata and retained-client portability baseline.

### Changed

- Updated the catalog metadata and last-updated state for the 2026-10-19 maintenance pass.
- Kept the retained-client portability, MCP fallback, Anti-Patterns, Verification Protocol, and Related Skills sections aligned.
- Routed related-work links through the retained `research` and `scientific-writing` skills instead of standalone literature-review and citation-management entries that were excluded after overlap review.

### Fixed

- Preserved explicit no-MCP fallbacks and the catalog's safety, approval, and source-boundary guidance.

## [2026-10-19] - Scientific Research Workflow Import

### Added

- Imported `skills/paper-lookup` from [K-Dense scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills) at commit `593377bb048752abb0152deab9fbb1083a6087df`.
- Preserved the applicable MIT license, documented API references, and bounded parser scripts.

### Changed

- Normalized catalog metadata and added cross-client portability, no-MCP fallback, verification, and related-skill routing.
- Documented Windows-safe `curl.exe`/PowerShell invocation and made JSON helper output ASCII-escaped while preserving parsed Unicode values.

### Fixed

- Restricted OpenCitations use to public unauthenticated endpoints; rate-limit failures must be reported without adding credentials.
- Kept console output reliable on Windows code pages by escaping non-ASCII characters in emitted JSON.
