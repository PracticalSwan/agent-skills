# Changelog

All notable changes to the `humanizer` skill are documented here.

## [2026-09-14] - Humanizer 3.0.0 Catalog Import

### Added

- Imported the current root Humanizer skill from [blader/humanizer](https://github.com/blader/humanizer) at main revision `9862685f575c65a8247f90369951df1b3416e3d` (v3.0.0).

### Changed

- Normalized the upstream package to the shared catalog v2.0 structure while keeping the official 25-pattern workflow, fact-preservation rules, and voice controls.
- Added explicit routing relationships to `avoid-ai-writing` and `voice-preserving-rewriter` so this compact direct-rewrite workflow does not replace the broader detector and preservation suite.

### Fixed

- Kept the catalog copy self-contained and cross-client; Claude marketplace metadata, CI packaging, and package-install commands are not runtime requirements.
