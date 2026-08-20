# Changelog

All notable changes to the `huggingface-spaces` skill are documented here.

## [2026-08-20] - Vendor Skill Import

### Added

- Imported the canonical `skills/huggingface-spaces` workflow from `https://github.com/huggingface/skills` at commit `020194918dc4a27d5a5d9a154b6b56cc2bd21364`.
- Normalized catalog metadata, retained-client portability, MCP fallback, safety, verification, and related-skill routing.

### Changed

- Preserved the upstream workflow and support files while adding this catalog's cross-client wrapper.

### Fixed

- Added explicit fallback and approval boundaries so the skill does not assume unavailable host tools or credentials.
- Documented the absent local `hf` CLI and removed implicit runtime installation and token-paste guidance.
- Removed literal-token command examples from the Space secret and bucket guidance.
