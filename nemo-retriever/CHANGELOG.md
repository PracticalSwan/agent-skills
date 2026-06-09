# Changelog

All notable changes to the `nemo-retriever` skill will be documented in this file.

## [2026-06-09] - Initial Import and Catalog Normalization

### Added

- Imported `nemo-retriever` from `https://github.com/NVIDIA/skills` at `skills/nemo-retriever` pinned to `129a1087a1853f32a950e2f7bbc0fd7d57b9d422`.
- Added repo-standard `Anti-Patterns`, `Verification Protocol`, portability, MCP fallback, and related-skills sections.
- Preserved the upstream benchmark, signature, skill card, and bundled references or scripts for provenance and later refreshes.

### Changed

- Normalized `SKILL.md` frontmatter to the shared catalog schema with `version: "1.2"` and `last_updated: 2026-06-09`.
- Moved upstream-only top-level metadata into the nested `metadata` block so validation, export, and downstream sync stay consistent.

### Fixed

- Aligned the imported skill with this repository's maintained-skill requirements and downstream sync workflow.
