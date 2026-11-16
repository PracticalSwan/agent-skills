# Changelog

## 2026-11-16 Catalog maintenance

### Added

- Added a generated skill catalog index from Git-visible skill folders.
- Imported the current Tavily SDK, entity, list, and monitor workflows; refreshed
  search and research; retired six superseded operation-specific entrypoints.

### Changed

- Refreshed 40 existing mapped skill workflows from their audited upstream
  paths, including Anthropic document/MCP skills, Java, Figma, Gemini, Matt
  Pocock, MongoDB, Netlify, Vercel, Xquik, Humanizer, Avoid AI Writing, Tavily,
  and Playwright CLI.
- Updated exact source pins and provenance to the 2026-11-16 source snapshot.
- Refreshed `rag-perf` to upstream v2.6.0 from NVIDIA's RAG Blueprint repository,
  corrected its source record, and linked repository-only code and docs explicitly.
- Reviewed current Codex plugin skills and imported no additional workflow
  because the candidates overlap maintained skills or require host-specific
  tools.
- Reworked the README and maintenance docs for shorter navigation and current sync behavior.
- Generated provenance from Git-visible catalog content and removed personal workspace paths from maintained metadata.
- Preserved existing third-party license and notice files when refreshed upstream skill paths no longer ship those files.
- Added refresh regression coverage for preserving existing third-party license and notice files.
- Replaced catalog-owned copyright notices with neutral contributor attribution
  while preserving third-party license text.
- Repaired skill references to excluded statistical, literature-review, and
  Figma 3D companion skills; kept those workflows explicit about their availability.
- Repaired relative links in curated support docs and the generated React view
  transitions guide; external repository assets now point to their pinned sources.
- Replaced hard-coded personal Windows profile paths in the custom-agent workflow
  with portable user-profile environment variables.
- Refreshed the protected Codex-only Blender overlay through its owner updater;
  kept it outside parent promotion and shared-agent/Claude sync.
- Documented automatic commit-and-push criteria for requested publication,
  recommended delivery, and substantial validated workspace changes.

### Fixed

- Made global sync roots profile-derived while retaining the three-root allowlist.
- Kept local overlays out of tracked provenance and generated catalog documentation.
- Corrected source records for current official PDF, Humanizer v4.0.0,
  Playwright CLI 0.1.24, Playwright 1.65.1, and Tavily paths.
- Curated Avoid AI Writing's default test command to the self-contained suites
  shipped in this cross-client catalog copy.
