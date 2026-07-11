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

## [2026-07-11] - Stitch Skill Router Refresh

### Added

- Refreshed route selection for the dedicated Stitch skills imported from `https://github.com/google-labs-code/stitch-skills` at `3f64079d75d025bc5890c73669f27c26a2d80b31`.

### Changed

- Kept the Stitch Design skill as a lightweight router so detailed workflow guidance remains in narrower `stitch-*` skills.
- Preserved the verified design-system MCP boundary while refreshing compatible upstream support material.

### Fixed

- Prevented upstream screen-tool assumptions from overriding the host-verified fallback guidance.

## [2026-06-15] - Stitch Skill Router Consolidation

### Added

- Added route selection for the dedicated Stitch skills imported from `https://github.com/google-labs-code/stitch-skills`.

### Changed

- Converted the old monolithic Stitch Design skill into a lightweight router so detailed workflow guidance lives in narrower `stitch-*` skills.
- Updated the Stitch MCP guidance to name the verified design-system tools and avoid claiming unavailable screen-generation tools.

### Fixed

- Removed duplicated long-form guidance for design-md, React conversion, stitch-loop, prompt enhancement, Remotion, and shadcn/ui from the entrypoint skill.

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

## [2026-04-24] - Skill Refresh

### Changed
- Standardized the SKILL frontmatter with version metadata, last-updated date, tags, and a concise catalog description.
- Reformatted the portability and MCP guidance with a preferred server line, a copy-paste fallback prompt, and consistent bullet lists.
- Added a catalog-standard Anti-Patterns section and refreshed the Related Skills links at the end of the skill.
## [2026-04-24] - Catalog Audit Cleanup

### Fixed
- Removed obsolete standalone Skill Paths guidance that duplicated the generated portability section.

All notable changes to this skill will be documented in this file.

## [2026-04-04] - Cross-Client Portability Refresh

### Changed
- Added a standard portability note covering GitHub Copilot, Claude Code, Codex, and Gemini CLI.
- Documented the preferred MCP server surface for this skill and a local no-MCP fallback workflow.

### Changed
- Validated `SKILL.md` frontmatter, portability sections, and Gemini export readiness with `python scripts/validate-skills.py`.
## [2026-03-09] - Workspace Modernization

### Added
- Added a 2026-03-09 maintenance entry after reviewing the skill; the existing structure and guidance remained suitable.

## [2026-02-28] — Description Rewrite & Cross-References

### Changed
- Rewrote skill description to ~200 characters with clear, specific activation keywords
- Improved keyword specificity to reduce overlap with related skills

### Added
- `## Related Skills` cross-reference table with 2-4 related skills and "Use When" guidance
