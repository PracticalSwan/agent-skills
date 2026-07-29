# Changelog

All notable changes to the `avoid-ai-writing` skill will be documented in this file.

## [2026-07-29] - Version 2.0 Client Support Reset

### Added

- Added the current GitHub Copilot, Claude Code, and Codex portability baseline.

### Changed

- **BREAKING:** Removed Gemini CLI and Antigravity as supported clients.
- Refreshed catalog metadata and last-updated state for the 2026-07-29 maintenance pass.
- Kept the retained-client portability, MCP fallback, Anti-Patterns, Verification Protocol, and Related Skills sections aligned.

### Fixed

- Prevented catalog modernization from reintroducing removed Gemini or Antigravity guidance.

## [2026-07-11] - Catalog Maintenance Refresh

### Added

- Added the current catalog verification baseline where it was missing.

### Changed

- Refreshed catalog metadata and last-updated state for the 2026-07-11 maintenance pass.
- Kept the cross-client, MCP fallback, Anti-Patterns, Verification Protocol, and Related Skills sections aligned.
- Reclassified historical `Tested` or `Verified` changelog headings under the allowed changelog vocabulary without dropping their evidence.

### Fixed

- Closed validator and documentation drift so the enforced schema matches the documented skill baseline.

## [2026-06-09] - Upstream Refresh and Catalog Validation Cleanup

### Added
- Brought in the latest upstream guidance for edit-in-place cleanup, voice and context profiles, and iterative rewrite convergence.
- Refreshed the bundled MIT license text from the upstream repository.

### Changed
- Updated the maintained `SKILL.md` from `https://github.com/conorbronsdon/avoid-ai-writing` to commit `4331560d02b2c86ffd1d889d4f688da699d360d9` while keeping the repo-standard verification, portability, and no-MCP sections.
- Refreshed the frontmatter description and `last_updated` date to match the expanded workflow.

### Fixed
- Removed the legacy `### Tested` changelog heading so repo validation rules stay satisfied.
- Replaced the older two-mode wording with the current upstream three-mode guidance.

## [2026-04-25] - Version 1.2 Verification Protocol Refresh

### Added
- Added a `Verification Protocol` section with skill-specific pass/fail checks, one pressure-test scenario, and a measurable success metric.
- Added guidance to leverage native parallel subagent dispatch and 200k+ context windows where available.

### Changed
- Updated `SKILL.md` frontmatter to `version: "1.2"` and `last_updated: 2026-04-25`.
- Reframed activation guidance toward symptom -> action triggers and standardized two-stage review wording where applicable.

### Fixed
- Preserved the earlier import cleanup while aligning the maintained copy with the v1.2 catalog structure.

## [2026-04-24] - Initial Import and Portability Upgrade

### Added
- Imported the skill from `https://github.com/conorbronsdon/avoid-ai-writing`.
- Added the upstream MIT license as `LICENSE.txt`.
- Added cross-client portability guidance for GitHub Copilot, Claude Code, Codex, and Gemini CLI.
- Added the repo-standard no-MCP fallback guidance for this skill.

### Changed
- Standardized the maintained copy into the shared catalog structure used in this repo.
- Pinned the initial vendored source commit to `cbf885e087e8ec1168bc58dc603606a6e4bfacbd`.

### Fixed
- Cleaned up imported mojibake or replacement-character separators so the maintained copy rendered cleanly.
