# Changelog

## [2026-07-11] - Catalog Maintenance Refresh

### Added

- Added the current catalog verification baseline where it was missing.

### Changed

- Refreshed catalog metadata and last-updated state for the 2026-07-11 maintenance pass.
- Kept the cross-client, MCP fallback, Anti-Patterns, Verification Protocol, and Related Skills sections aligned.
- Reclassified historical `Tested` or `Verified` changelog headings under the allowed changelog vocabulary without dropping their evidence.

### Fixed

- Closed validator and documentation drift so the enforced schema matches the documented skill baseline.

## [2026-04-25] - Version 1.2 Verification Protocol Refresh

### Added
- Added a `Verification Protocol` section with skill-specific pass/fail checks, one pressure-test scenario, and a measurable success metric.
- Added guidance to leverage native parallel subagent dispatch and 200k+ context windows where available.

### Changed
- Updated `SKILL.md` frontmatter to `version: "1.2"` and `last_updated: 2026-04-25`.
- Reframed activation guidance toward symptom -> action triggers and standardized two-stage review wording where applicable.

## [2026-04-24] - Version 1.1 Refresh

### Changed
- Updated the SKILL frontmatter version to `1.1` for the 2026-04-24 catalog refresh.

## [2026-04-24] - Post-Refresh Cleanup

### Fixed
- Split the operational guidance into explicit Security, Observability, Auth Handling, Logging, and Versioning subsections for clearer MCP server hardening guidance.

## [2026-04-24] - Skill Refresh

### Changed
- Standardized the SKILL frontmatter with version metadata, last-updated date, tags, and a concise catalog description.
- Reformatted the portability and MCP guidance with a preferred server line, a copy-paste fallback prompt, and consistent bullet lists.
- Added a catalog-standard Anti-Patterns section and refreshed the Related Skills links at the end of the skill.
- Added a glossary, before-and-after shared-infrastructure examples, and new guidance covering security, observability, auth handling, logging, and server versioning.
## [2026-04-24] - Upstream License Refresh

### Changed

- Updated `LICENSE.txt` from the official Anthropic source at commit `5128e1865d670f5d6c9cef000e6dfc4e951fb5b9` to include the current copyright holder.

### Changed
- Confirmed the current upstream change for `skills/mcp-builder` is limited to `LICENSE.txt`.

## [2026-04-04] - Initial Import and Catalog Upgrade

### Added

- Imported `mcp-builder` from the `awesome-claude-skills` discovery catalog using the official Anthropic skill as the canonical source
- Rewrote the top-level skill into the repo house style while preserving the upstream reference library and helper scripts
- Added a maintained `CHANGELOG.md` so the skill is tracked like the rest of the editable catalog

### Changed
- Ran `python -m py_compile mcp-builder/scripts/connections.py mcp-builder/scripts/evaluation.py`
- Planned validation through `python scripts/validate-skills.py`
