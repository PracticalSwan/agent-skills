# Changelog

All notable changes to the `peer-review` skill are documented here.

## [2026-10-19] - Catalog Freshness And Source Sync

### Added

- Added this skill from a reviewed upstream source and normalized it for the shared catalog.
- Refreshed the catalog metadata and retained-client portability baseline.

### Changed

- Updated the catalog metadata and last-updated state for the 2026-10-19 maintenance pass.
- Kept the retained-client portability, MCP fallback, Anti-Patterns, Verification Protocol, and Related Skills sections aligned.
- Routed evidence-coverage guidance to the retained `research` skill after excluding the overlapping standalone literature-review candidate.

### Fixed

- Preserved explicit no-MCP fallbacks and the catalog's safety, approval, and source-boundary guidance.

## [2026-10-19] - Scientific Research Workflow Import

### Added

- Imported `skills/peer-review` from [K-Dense scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills) at commit `593377bb048752abb0152deab9fbb1083a6087df`.
- Preserved the applicable MIT license, reviewer resources, and offline validation helpers.

### Changed

- Normalized catalog metadata and added cross-client portability, no-MCP fallback, verification, and related-skill routing.

### Fixed

- Made authorization, venue policy, and local-only handling mandatory before any confidential manuscript review.
