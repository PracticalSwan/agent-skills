# Changelog

All notable changes to the Copilot Skills repository will be documented in this
file.

## [2026-08-31] - Catalog Freshness And Corpus Refresh

### Added

- Added the current `avoid-ai-writing` corpus documentation and conversational
  seed entries with explicit under-sampling limits.

### Changed

- Refreshed `avoid-ai-writing/corpus/manifest.json`, `corpus/README.md`,
  `scripts/corpus.js`, and `scripts/corpus.test.js` from source commit
  `58a95fc9971d7af95f1f1324b8a6bc991eb8004d`.
- Updated the remaining source provenance pins and catalog baseline to
  `2026-08-31`; `awesome-copilot` and NVIDIA changed only outside installed
  mappings.

### Fixed

- Re-audited the three scoped child roots and confirmed no eligible child-only
  skills remain; protected and project-specific boundaries stayed intact.

## [2026-08-29] - Catalog Freshness And Mirror Repair

### Added

- Added current web-quality field/agentic-browsing references, React View
  Transitions troubleshooting guidance, and the latest Gemini model guidance
  for transcription, Omni video, and embeddings.

### Changed

- Refreshed exact mapped paths for `avoid-ai-writing` 3.28.0,
  `x-twitter-scraper`, `gemini-api-dev`, `gemini-interactions-api`,
  `react-view-transitions`, and the changed web-quality skills.
- Updated all 24 source pins and the catalog-wide maintenance baseline to
  `2026-08-29`; repository movement outside installed mappings was recorded
  without broad rewrites.
- Removed the stale preferred Xquik MCP mapping because the current source no
  longer documents an MCP setup surface; the normalized skill now exposes its
  REST/SDK fallback honestly.

### Fixed

- Repaired the missing top-level Codex `doc` mirror through the approved sync
  script while preserving `.system`, Blender/local-only, Superpowers, and
  project-specific boundaries.
- Re-audited `.codex`, `.agents`, and `.claude`; no eligible child-only skills
  remain to promote.

## [2026-08-24] - Catalog Freshness And Personal Child Promotion

### Added

- Promoted five eligible Codex Router-managed child skills into the parent
  catalog: `codex-app-threads`, `codex-computer-use`, `codex-in-app-browser`,
  `codex-router`, and `codex-router-media`.
- Added host-specific MCP/fallback routing and local tree-digest provenance for
  the promoted Codex Router skills without copying their `.codex-router-managed`
  marker files.

### Changed

- Refreshed the catalog-wide metadata and changelog baseline to `2026-08-24`.
- Compared recorded upstream heads with exact mapped paths and refreshed
  material changes in `avoid-ai-writing`, the eight selected Matt Pocock
  workflows, and `x-twitter-scraper` while leaving unrelated changed paths
  untouched.
- Updated source manifests and `REFERENCE_SOURCES.md` to current verified
  upstream heads, and retained the required 94 upstream Blender skills plus
  one separately protected local entry outside the parent and shared/Claude
  mirrors.

### Fixed

- Kept project-specific paths, Codex `.system`, copied official Superpowers,
  and the Blender overlay outside normal promotion and sync ownership.
- Preserved catalog changelog/provenance sidecars while applying upstream
  support-file deletions and additions.

## [2026-08-20] - VoltAgent Platform Skills And Catalog Maintenance

### Added

- Added 66 canonical vendor skills selected from the VoltAgent discovery index:
  Vercel, Netlify, MongoDB, Figma, Hugging Face, and the retained current
  Supabase import, with pinned source commits and per-skill provenance.
- Added `scripts/platform_skill_manifest.py` and
  `scripts/import-platform-skills.py` for repeatable, reviewed imports from
  pinned vendor clones.
- Added explicit CLI gating: Vercel, Netlify, and Supabase CLI guidance is
  enabled because those commands are installed locally; absent Hugging Face,
  MongoDB, and Figma CLIs were not imported.

### Changed

- Refreshed the generated registry/source report and root inventory to 232
  tracked folders (200 maintained) and 290 local folders (258 maintained).
- Ran the required Codex-only Blender refresh at upstream commit
  `8f778d2405a214b508d4c7d80742be8e43acdd52`; the 94-skill overlay remains
  outside the parent catalog and shared/Claude mirrors.
- Updated all root maintenance documentation with vendor provenance, CLI
  detection, importer usage, and the approved downstream sync boundary.

### Fixed

- Repaired imported nested Markdown references in MongoDB, Figma, and Hugging
  Face support files and replaced stale source-tree documentation links with
  stable official URLs.
- Corrected the catalog modernization heading check so headings such as
  `## Anti-Patterns to Avoid` are recognized without breaking validation.

## [2026-08-17] - Codex-Only Blender Skills Overlay

### Added

- Added guarded maintenance automation for the `arjun988/blender-skills` pack, installed only under the personal Codex skill root with a dedicated vendor checkout and ownership manifest.
- Added registry protection for the 94 current Blender skill names and dynamic upstream commit tracking.

### Changed

- Parent source-maintenance now refreshes the Blender pack through `scripts/update-codex-local-blender-skills.ps1` without treating those skills as shared-catalog imports.
- Child promotion, validation, and downstream sync now enforce the Codex-only ownership boundary.

### Fixed

- Prevented future maintenance runs from promoting Blender-local skill folders upstream or mirroring them into shared or Claude skill roots.

## [2026-08-16] - Related Skill Consolidation Audit

### Added

- Added explicit cross-skill routing links for the Supabase, Gemini, React, and
  web-quality groups so related workflows remain discoverable without merging
  distinct activation boundaries.

### Changed

- Reviewed the parent catalog against plugin-managed Supabase and React copies.
  The maintained parent versions remain canonical because they include catalog
  metadata, cross-client safeguards, explicit fallbacks, and maintained support
  trees; plugin-managed copies remain external.
- Documented why platform/Postgres, general/Interactions, implementation/
  performance, aggregate/focused web-quality, browser/general code quality, and
  language-specific security workflows remain separate.

### Fixed

- Removed ambiguity at the related-skill routing boundary without deleting or
  collapsing any skill whose evidence path or user-facing scope differs.

## [2026-08-16] - Promote Installed Platform And Web Skills

### Added

- Audited the eleven newly installed personal-Codex skill trees against the
  exact current upstream paths in Supabase, Google Gemini, Vercel, and
  web-quality repositories.
- Added `supabase`, `supabase-postgres-best-practices`, `gemini-api-dev`,
  `gemini-interactions-api`, `react-best-practices`, `web-quality-audit`,
  `performance`, `core-web-vitals`, `accessibility`, `seo`, and
  `best-practices` with catalog metadata, changelogs, provenance, and retained
  upstream license texts where available.

### Changed

- Updated the catalog inventory to `166` tracked folders and `134` maintained
  skills; the live parent workspace now contains `224` folders and `192`
  maintained skills including the existing local-only overlays.
- Kept `web-quality-audit` as an aggregate router over five focused leaves,
  kept broad `performance` separate from targeted Core Web Vitals, and kept
  browser `best-practices` separate from the general `code-quality` workflow.
- Kept Vercel `react-best-practices` separate from `react-development`,
  `nextjs-development`, and `frontend-design`; retained the source's detailed
  compiled rule files and support metadata.
- Added current Supabase/Gemini MCP mappings and explicit official-doc or CLI
  fallbacks, plus a Windows/manual fallback for the POSIX web-quality helper.
- Refreshed root documentation, the generated source report, and the
  normalization helper's maintenance date. Downstream routing remains limited
  to the three approved personal-global roots; no project-local path was used.

### Fixed

- Added explicit authorization gates before creating Supabase project MCP
  configuration or authenticating a server.
- Removed provider-specific managed-agent identifiers from the Gemini
  Interactions workflow and now require a current account/documentation lookup
  before selecting a managed agent.
- Narrowed the removed-client validator to reject retired Gemini CLI or
  Antigravity host support while allowing official Gemini API documentation and
  skills.

## [2026-08-14] - Catalog-Wide Freshness And Source Sync

### Added

- Added the current upstream support material for `avoid-ai-writing`, Stitch,
  Xquik, and the affected copied Superpowers workflows, including the new
  detector validation/style helpers, Angular-aware Stitch capture guidance,
  Xquik reference workflows, and bounded visual-brainstorming helpers.
- Recorded current source-head provenance for the audited external catalogs
  and refreshed the generated reference-source report.

### Changed

- Refreshed all `213` live skill entrypoints to the 2026-08-14 catalog
  metadata and documentation baseline while preserving `2.0` tracked
  versions and the upstream overlay version contract.
- Reconciled only the personal `.codex` and `.claude` child roots; no
  child-only skills required promotion, and no project-specific path was
  scanned or synchronized.
- Updated root maintenance documentation, per-skill changelogs, source
  selection notes, and the current downstream-sync guidance.

### Fixed

- Removed imported Gemini/Antigravity operational setup from refreshed Stitch,
  Xquik, and visual-companion guidance while retaining local no-MCP and secret
  handling fallbacks.
- Kept copied Superpowers and Codex system-managed routing distinct from the
  maintained catalog during normalization and downstream synchronization.

## [2026-08-08] - Selected Matt Pocock Skills Import

### Added

- Audited all `35` live skill entrypoints in `mattpocock/skills` at commit
  `84fdeffd12f2ee307994d1eb6feb48173b6e0502`.
- Added the eight selected MIT-licensed skills: `codebase-design`,
  `domain-modeling`, `improve-codebase-architecture`, `prototype`,
  `research`, `resolving-merge-conflicts`, `handoff`, and
  `writing-for-agents`.
- Added per-skill licenses, catalog changelogs, registry provenance, and
  cross-client fallback metadata.

### Changed

- Updated the live catalog to `155` skill folders and `123` maintained skills;
  the local workspace now contains `213` skill folders and `181` maintained
  skills including `58` local-only overlays.
- Retained the existing catalog equivalents for upstream TDD, debugging, code
  review, implementation, planning, and skill-authoring overlaps.
- Adapted the imported workflows for existing project conventions, concise
  clarification, Windows-first temporary paths, and explicit Git approval
  gates.
- Updated root instructions, client guidance, catalog lists, source registry,
  and reference-source documentation. Downstream sync remains limited to the
  three approved personal-global roots; no project-local skill path was used.

### Fixed

- Removed the imported architecture workflow's hard dependency on an absent
  `/grilling` skill by routing to the local `brainstorming` workflow or a
  bounded direct decision loop.
- Prevented imported merge/conflict and prototype workflows from implying
  unauthorized destructive, history-changing, or publication actions.

## [2026-08-02] - Canonical Frontend Design Consolidation

### Added

- Added a context-fit operating rubric and six-mode router to the canonical
  `frontend-design` skill, with accessibility and functional correctness as
  hard gates.
- Added canonical agent metadata, a corrected WCAG 2.2 accessibility
  reference, complete Apache-2.0 and GitHub MIT license texts, and provenance
  and modification notices.
- Added exact retired-name cleanup to the downstream sync for
  `frontend-skill` and `premium-frontend-ui` across only the three approved
  personal-global roots.

### Changed

- **BREAKING:** Consolidated the general creation and art-direction behavior
  of `frontend-skill` and `premium-frontend-ui` into `frontend-design` while
  retaining `web-design-reviewer` as post-implementation visual QA.
- Reduced the tracked catalog to `147` skill folders and `115` maintained
  skills; the live workspace contains `205` skill folders and `173` maintained
  skills including `58` local-only overlays.
- Migrated framework, Stitch, visual-tool, registry, import-script, and root
  documentation references to the canonical path while preserving the
  `#component-review-rubric` anchor used by React, Next.js, and Vite.
- Updated provenance to map `frontend-design` to the modified historical
  OpenAI source and preserved the reviewed Awesome Copilot source attribution.

### Fixed

- Removed broken JSX and contrast examples, corrupted text, universal
  60-30-10 and 44-pixel claims, and excessive generic framework tutorials.
- Replaced mandatory preloaders, smooth scrolling, custom cursors, pinned
  journeys, 3D, and animation dependencies with optional techniques bounded by
  accessibility, performance, and maintenance cost.
- Removed the inaccessible recipe-card example and duplicative Tailwind
  component catalog instead of preserving unsupported quality claims.

## [2026-07-30] - Official Tavily Agent Skills

### Added

- Imported all eight current skill folders from the official
  `tavily-ai/skills` repository at commit
  `ea5e8201b0d3ed9c10b70b71187589bd761fe2d2`: `tavily-best-practices`,
  `tavily-cli`, `tavily-crawl`, `tavily-dynamic-search`, `tavily-extract`,
  `tavily-map`, `tavily-research`, and `tavily-search`.
- Added self-contained MIT licenses, per-skill changelogs, provenance
  records, Tavily MCP mappings, no-MCP CLI/SDK fallbacks, and cross-client
  guidance for GitHub Copilot, GLM-backed Claude Code, and Codex.

### Changed

- Updated tracked catalog counts to `149` skill folders and `117` maintained
  skills; the live workspace now contains `207` skills including `58`
  local-only overlays.
- Replaced upstream pipe-to-shell defaults with reviewable `uv` and `pip`
  installation choices and documented that the skills do not install the
  Tavily CLI or store credentials.
- Updated root catalog, contribution, security, provenance, and client
  documentation for the Tavily suite.

### Fixed

- Removed the imported removed-client integration so the suite does not
  reintroduce removed-client support.
- Added explicit API-key, private-target, prompt-injection, crawl-scope,
  output-overwrite, job-state, cost, and citation-verification safeguards.

## [2026-07-29] - Version 2.0 Client Support Reset

### Added

- Added normalized parent copies of five Codex system-only skills:
  `openai-docs`, `plugin-creator`, `review-agent`, `skill-creator`, and
  `skill-installer`.
- Added `stitch-react-vite-dashboard` from the current Stitch source and
  refreshed `imagegen` from the personal Codex system bundle.
- Added `MIGRATION.md` with old/new behavior, migration steps, legacy mirror
  handling, and rollback guidance.

### Changed

- **BREAKING:** Removed Gemini CLI and Antigravity from the supported client
  matrix, retired command generation, and reduced downstream sync from five
  roots to the Codex, shared, and Claude roots.
- Updated all `199` live skills to the 2026-07-29 retained-client baseline;
  all `141` intended tracked skills now use catalog `version: "2.0"`, while
  the `58` local Google Workspace overlays retain upstream `version: "0.22.5"`.
- Limited child promotion to the personal `.codex` and `.claude` roots and
  left project-specific paths out of scope.
- Refreshed changed Anthropic document helpers, `avoid-ai-writing`, two NVIDIA
  workflows, Stitch workflows, and `x-twitter-scraper` from their current
  recorded sources.
- Added capability-based browser, plugin, docs, image, creator, and installer
  routing that preserves Codex behavior while giving GLM-backed Claude Code a
  safe external-MCP or manual fallback.

### Fixed

- Prevented top-level sync from overwriting six Codex-owned `.system` skills.
- Pruned stale catalog-owned top-level system shadows and copied Superpowers
  that no longer belong in retained-client mirror roots.
- Removed retired client names and paths from active skills, root guidance,
  imported Xquik setup notes, and the legacy Superpowers tool mapping.
- Kept authenticated LinkedIn publication confirmation-gated and prohibited
  search/reader tools from being treated as browser write surfaces.
- Removed two verified byte-identical retired skill mirrors, generated Python
  and Serena caches, and four empty local placeholder directories while
  preserving surrounding application state and intentional catalog copies.
- Removed a stale PowerPoint reference link whose untracked empty directory
  masked the missing support material in local link checks.

## [2026-07-29] - LinkedIn Chrome Publishing Skill

### Added

- Added the maintained `linkedin-create-post` skill for drafting, publishing,
  and verifying LinkedIn posts through a signed-in Chrome session.

### Changed

- Updated catalog counts, client guidance, the MCP registry, Gemini command
  generation, and five-root global sync coverage for the new skill.

### Fixed

- Defined action-time confirmation, public-safe media review, and live
  post-publication verification as required boundaries for LinkedIn writes.

## [2026-07-11] - Sync Path Policy: Locked Downstream Targets and Antigravity CLI

### Changed

- Locked downstream sync to exactly five personal-global roots: `C:\Users\LOQ\.agents\skills`, `C:\Users\LOQ\.codex\skills`, `C:\Users\LOQ\.claude\skills`, `C:\Users\LOQ\.gemini\antigravity\global_skills`, and the newly added `C:\Users\LOQ\.gemini\antigravity-cli\skills`.
- Removed workspace-local downstream sync from `scripts/sync-skills.ps1`, including the `-WorkspaceSearchRoot` and `-SkipWorkspaceRoots` parameters and the workspace target discovery. Workspace-local skill roots (`.agent\skills`, `.agents\skills`, `.claude\skills` under project trees) are now upstream promotion sources only.
- Added an allowlist guard to `scripts/sync-skills.ps1` that refuses to write to any path outside the five approved roots.
- Updated `README.md`, `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, and `LESSON.md` to document the locked sync targets, the new Antigravity CLI destination, and the upstream-only role of workspace-local roots.

## [2026-07-11] - Full Catalog Maintenance, Child Promotion, and Source Refresh

### Added

- Promoted `11` Codex-only and `12` workspace-local skills into the parent catalog, normalizing invalid child names to lowercase hyphen-case where required.
- Flattened `18` newly discovered official Superpowers from categorized child paths and added the current `using-skills` entrypoint while retaining `using-superpowers` for compatibility.
- Added `scripts/promote-child-skills.py` for safe explicit and recursive child-path promotion.
- Added `scripts/update-skill-registry.py` to refresh source commits, provenance mappings, copied-official classification, and `REFERENCE_SOURCES.md`.
- Added the upstream `avoid-ai-writing` detector resources and the expanded current Xquik reference set.

### Changed

- Refreshed all `192` live skills to the 2026-07-11 catalog baseline; all `134` tracked skills now use catalog `version: "1.3"`, while the `58` local-only Google Workspace overlays retain upstream `version: "0.22.5"`.
- Refreshed `avoid-ai-writing` from upstream `3.15.0`, the Stitch import from commit `3f64079d75d025bc5890c73669f27c26a2d80b31`, and `x-twitter-scraper` from upstream `2.4.17` while preserving stricter local safety and tool-availability boundaries.
- Updated the `13` overlapping copied Superpowers from `obra/superpowers-skills` and the legacy `using-superpowers` copy from `obra/superpowers`.
- Finalized canonical provenance for `docx`, `jupyter-notebook`, `pptx`, and `xlsx` and refreshed all source-commit snapshots after exact-path comparison.
- Updated `README.md`, `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `LESSON.md`, `CONTRIBUTING.md`, `SECURITY.md`, and `REFERENCE_SOURCES.md` for the new counts and workflows.

### Fixed

- Aligned validation with documented policy by requiring `Verification Protocol` immediately after `Anti-Patterns`, requiring final `Related Skills`, enforcing lowercase hyphen-case folders, and rejecting both `### Tested` and `### Verified` changelog headings.
- Migrated historical banned changelog headings without deleting their evidence and added missing verification protocols to the local overlay set.
- Repaired imported path assumptions, including flattened Superpowers category paths, the parent-installed image generation CLI path, and unavailable optional Figma companion links.

## [2026-06-24] - Xquik Skill Import, GitHub Guidelines, and PR Conflict Resolution

### Added

- Added the normalized `x-twitter-scraper` maintained skill and provenance mapping from `Xquik-dev/x-twitter-scraper` at commit `800893485c490eafeadec76624dcb6575d7a70d8`.
- Added `CONTRIBUTING.md` and `SECURITY.md` so GitHub contributors have explicit workflow and disclosure guidance.

### Changed

- Resolved PR `#2` against the current Stitch-expanded catalog by carrying the `x-twitter-scraper` README entries forward on top of the newer `main` layout.
- Updated `README.md`, `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `LESSON.md`, `REFERENCE_SOURCES.md`, and `scripts/skill-registry.json` for the new `93` tracked skill folders, `79` tracked maintained skills, `151` local skill folders, and `137` local maintained skills.

### Fixed

- Hardened the normalized Xquik skill against prompt-injection from X-authored content and clarified API-key-only credential handling and approval gates.

## [2026-06-15] - Stitch Skills Import, Overlap Consolidation, and Publish Rule

### Added

- Imported all `14` Google Stitch skills from `google-labs-code/stitch-skills` at commit `1544aa4a3be93e7515b0c27d32722f7ca5a2f691`, preserving relevant support assets and adding per-skill changelogs.
- Added `scripts/import-stitch-skills.py` to repeat the normalized Stitch import from an upstream clone.
- Added the required completion, sync, and publish rule to `AGENTS.md`, `CLAUDE.md`, `README.md`, `GEMINI.md`, and `LESSON.md`.

### Changed

- Converted `stitch-design` from a broad monolithic skill into a router that points to the narrower imported Stitch workflows.
- Documented the durable Stitch consolidation decisions in `README.md` and `REFERENCE_SOURCES.md` instead of keeping a transient audit file.
- Updated `README.md`, `REFERENCE_SOURCES.md`, `GEMINI.md`, `AGENTS.md`, `CLAUDE.md`, `LESSON.md`, and `scripts/skill-registry.json` for the new `92` tracked skill folders and `150` local skill folders.
- Updated Stitch MCP guidance to name the verified design-system tools and treat screen lookup, generation, editing, and variant tools as optional host-specific capabilities.

### Fixed

- Replaced stale Stitch support references that claimed unavailable MCP screen tools were generally available.
- Removed the obsolete `### Tested` heading from the `stitch-design` changelog history.
- Removed the standalone Stitch overlap audit file after preserving its decisions in root documentation.

## [2026-06-09] - Workspace Startup Rule for LESSON.md

### Added

- Added a tracked root `AGENTS.md` with workspace-specific guidance for shared-skill maintenance across GitHub Copilot, Claude Code, Codex, Gemini CLI, and Antigravity.

### Changed

- Updated `README.md`, `CLAUDE.md`, `GEMINI.md`, and `LESSON.md` to document the shared startup rule that requires reading `LESSON.md` at the start of each new session.
- Updated `.gitignore` so `AGENTS.md` is tracked as a real workspace instruction file instead of being silently ignored.

## [2026-06-09] - NVIDIA Imports, Upstream Audit Refresh, and Catalog Validation Recovery

### Added

- Imported the NVIDIA skills `accelerated-computing-cudf`, `deepstream-dev`, `deepstream-import-vision-model`, `nemo-retriever`, `rag-blueprint`, `rag-eval`, and `rag-perf`, including their provenance sidecars and per-skill changelogs.
- Added repo-standard metadata, required validation sections, and new per-skill changelogs for the previously raw tracked imports `docx`, `jupyter-notebook`, `pptx`, and `xlsx`.

### Changed

- Updated `README.md`, `CLAUDE.md`, `GEMINI.md`, `REFERENCE_SOURCES.md`, `LESSON.md`, and `scripts/skill-registry.json` to document the expanded catalog, current upstream audit commits, and the fact that the tracked document imports now match the maintained schema while still awaiting finalized provenance mapping.
- Refreshed the vendored `avoid-ai-writing` skill to upstream commit `4331560d02b2c86ffd1d889d4f688da699d360d9` while preserving the catalog's verification, portability, and no-MCP sections.
- Regenerated Gemini command exports for all `136` local skills after the catalog refresh.

### Fixed

- Updated `scripts/validate-skills.py` so Gemini command validation works on Python 3.10 hosts that do not provide `tomllib`.
- Removed validation blockers from legacy skill folders, including the banned `### Tested` changelog heading and replacement-character separators in `avoid-ai-writing`.

## [2026-05-05] - Documentation Refresh for Tracked Document Skill Imports

### Added

- Documented the tracked imported skills `docx`, `jupyter-notebook`, `pptx`, and `xlsx` in the maintained catalog and provenance notes.

### Changed

- Updated `README.md`, `CLAUDE.md`, and `GEMINI.md` to reflect the current `71` tracked skill folders, `57` tracked maintained skills, `129` local skill folders, and `115` local maintained skills.
- Clarified in the root docs that `docx`, `jupyter-notebook`, `pptx`, and `xlsx` are tracked imports that still need catalog normalization before they match the repo's full `version: "1.2"` maintained-skill schema.
- Updated `REFERENCE_SOURCES.md` and `LESSON.md` to record the current pending-provenance and pending-normalization state for those tracked imports.

### Fixed

- Corrected stale inventory and baseline claims that still described the pre-import catalog state.

## [2026-04-25] - Catalog 1.2 Verification Protocol Refresh and Full Sync

### Added

- Added per-skill changelog entries for the `version: "1.2"` verification protocol refresh across all `67` tracked skill folders.

### Changed

- Updated `README.md`, `CLAUDE.md`, `GEMINI.md`, `REFERENCE_SOURCES.md`, and `LESSON.md` to document the current `version: "1.2"` / `last_updated: 2026-04-25` catalog baseline.
- Documented `Verification Protocol` as part of the required skill structure while keeping validator descriptions aligned with the current script behavior.

### Fixed

- Replaced remaining directly related legacy review wording in skill support documentation with `two-stage review (spec compliance first, then code quality)`.

## [2026-04-24] - Catalog 1.1 Docs Refresh and Full Sync

### Changed

- Updated `README.md`, `CLAUDE.md`, and `GEMINI.md` to document the current git-tracked catalog baseline of `67` tracked skill folders aligned on `version: "1.1"` with `last_updated: 2026-04-24`.
- Updated `README.md` and `CLAUDE.md` to make validation, Gemini export, and downstream sync explicit requirements after a catalog-wide skill refresh, even when inventory counts do not change.
- Updated `LESSON.md` with new guidance for documenting repo-wide metadata refreshes and rerunning sync after doc-only catalog updates.

## [2026-04-24] - Catalog Schema Alignment, Validation Refresh, and Full Sync

### Changed

- Updated `scripts/skill-registry.json` to track the copied official superpower list explicitly.
- Updated `scripts/sync-skills.ps1` to classify maintained skills versus copied official superpowers from the registry instead of inferring that split from `CHANGELOG.md` presence.
- Updated `scripts/validate-skills.py` to accept the catalog frontmatter fields `version`, `last_updated`, and `tags`, require `CHANGELOG.md` for every skill folder, and validate the Anti-Patterns and Related Skills baseline.
- Updated `README.md`, `CLAUDE.md`, `GEMINI.md`, and `LESSON.md` to document the current skill schema, validator expectations, and the explicit superpower classification rule.

## [2026-04-24] - Validation Scope Fix, Provenance Alignment, and Full Sync

### Changed

- Updated `scripts/validate-skills.py` to ignore local environment folders (`.venv`, `venv`, `env`) and cache folders when scanning for stray `*.pyc` files, preventing false positives from local toolchains.
- Updated `README.md` and `CLAUDE.md` to show both git-tracked catalog counts and live local workspace counts, removing inventory ambiguity.
- Updated `GEMINI.md` to clarify that Gemini export and validation include all local `SKILL.md` folders, including local-only overlays.
- Reworked `REFERENCE_SOURCES.md` to align with `scripts/skill-registry.json`, including the `googleworkspace_cli` source commit and tracked-versus-local provenance coverage.
- Added new maintenance guidance in `LESSON.md` for dual inventory reporting and validator exclusion scope.

## [2026-04-24] - Skill Imports and Source Refresh

### Added

- Imported `avoid-ai-writing` from `https://github.com/conorbronsdon/avoid-ai-writing`.
- Imported `codebase-to-course` from `https://github.com/zarazhangrui/codebase-to-course` with its course-generation reference assets.
- Added provenance records and per-skill changelogs for both new maintained skills.

### Changed

- Updated public inventory counts to `67` tracked skill folders and `53` maintained skills.
- Refreshed upstream provenance for audited source repos in `scripts/skill-registry.json` and `REFERENCE_SOURCES.md`.
- Applied the current upstream `premium-frontend-ui` author metadata and Anthropic `mcp-builder` license notice.

## [2026-04-04] - Public Docs Cleanup for Ignored Local-Only Skills

### Changed

- Removed ignored local-only skill families from the public inventory, provenance notes, and lessons.
- Restored the tracked documentation counts to `65` total skill folders and `51` maintained skills.

## [2026-04-04] - Curated Skill Imports, AGENTS Upgrade, and Full Sync Refresh

### Added

- Imported and maintained these new skills after researching the reference catalogs in parallel:
  - `agentic-eval`
  - `cloud-design-patterns`
  - `context-map`
  - `mcp-builder`
  - `secret-scanning`
- Added local helper scripts so the imported skills are useful even without host-specific MCP or plugin support:
  - `agentic-eval/scripts/rubric-scorecard.py`
  - `cloud-design-patterns/scripts/pattern-shortlist.py`
  - `context-map/scripts/build-context-map.py`
  - `secret-scanning/scripts/precommit-secret-audit.py`
- Added per-skill changelogs for all newly maintained imports

### Changed

- Updated root documentation for the new `65` total skill / `51` maintained skill inventory
- Extended provenance tracking to record canonical upstream sources separately from discovery catalogs when the discovery repo was not the best maintained origin
- Rewrote the top-level imported skill instructions into the repo house style while preserving upstream references and helper assets where they added value
- Strengthened the global Codex `AGENTS.md` guidance to require safer skill import screening, canonical-source preference, import smoke tests, and repo-wide sync discipline

## [2026-04-04] - Main Workspace Policy Clarification

### Changed

- Clarified in root documentation that `C:\Users\LOQ\.copilot\skills` is the canonical main workspace for maintained skills and that new maintained skills must be added here first
- Documented downstream skill roots as synced branch mirrors rather than authoring locations
- Updated maintenance guidance so external skill imports are recorded and reviewed in this repo before outward sync

## [2026-04-04] - Codex Path Alignment and Sync Refresh

### Changed

- Realigned `scripts/sync-skills.ps1` so maintained skills now target `C:\Users\LOQ\.codex\skills` for Codex while keeping `C:\Users\LOQ\.agents\skills` as a shared mirror
- Updated root documentation to distinguish the primary Codex install root from the shared mirror path instead of treating them as the same destination
- Refreshed installed Codex skills from the current workspace catalog before the full sync pass

### Fixed

- Removed the stale assumption that `C:\Users\LOQ\.agents\skills` was the only Codex sync target

## [2026-04-04] - Gemini Antigravity Sync and Cleanup

### Changed

- Added `C:\Users\LOQ\.gemini\antigravity\global_skills` as a first-class sync target in `scripts/sync-skills.ps1`
- Updated root documentation to describe Gemini Antigravity global-skill syncing alongside generated Gemini CLI commands
- Refined high-impact meta-skill wording in `using-superpowers`, `writing-skills`, and `nextjs-development` so they read more cleanly across clients instead of assuming only Claude or Codex paths

### Fixed

- Removed the accidental `GEMINI.md` ignore rule from `.gitignore` so the Gemini-specific documentation can be tracked with the repo

## [2026-04-04] - Four-Client Portability and Workspace Skill Expansion

### Added

- Added `scripts/skill-registry.json` to track MCP-backed skills, no-MCP fallback guidance, reference sources, and imported-skill provenance
- Added `scripts/export-gemini-skill.py` to generate Gemini CLI `/skills:<skill-name>` commands from repo `SKILL.md` files
- Added `scripts/modernize-skills.py` to inject the standard cross-client portability section and MCP fallback section across skills
- Added `scripts/validate-skills.py` to verify skill frontmatter, required sections, and generated Gemini command validity
- Added the former `GEMINI.md` guide for Gemini CLI usage guidance
- Added [REFERENCE_SOURCES.md](c:\Users\LOQ\.copilot\skills\REFERENCE_SOURCES.md) documenting imported skill sources, commits, and selection rationale
- Imported and maintained these new skills after auditing `C:\Assumption University`:
  - `csharp-xunit`
  - `dotnet-best-practices`
  - `java-docs`
  - `java-junit`
  - `pdf`
  - `premium-frontend-ui`
  - `security-review`
  - `spreadsheet-formula-helper`

### Changed

- Updated every skill folder so the current catalog works across GitHub Copilot, Claude Code, Codex, and Gemini CLI instead of assuming a single host
- Added explicit no-MCP fallback guidance to MCP-aware skills so the workflows stay usable even when a client lacks the preferred MCP server
- Rewrote root docs for the new `60` total skill / `46` maintained skill inventory and the four-client support model
- Extended `scripts/sync-skills.ps1` to discover workspace-local skill roots under `.agent\skills`, `.agents\skills`, and `.claude\skills`
- Fixed `scripts/sync-skills.ps1` summary handling so source inventory and discovered workspace targets are tracked separately
- Reworked Gemini command export to use TOML-safe escaped strings instead of fragile raw multiline embedding
- Normalized imported skill descriptions and wording where they still assumed Copilot-only or host-specific placeholders

## [2026-03-28] - Cross-Client Sync and Lessons

### Added

- Added `LESSON.md` to capture maintenance lessons and recurring mistakes for
  the shared skill catalog
- Added `scripts/sync-skills.ps1` to sync maintained skills from the workspace
  to Codex and Claude target folders while keeping Codex superpowers in their
  nested `superpowers/` location

### Changed

- Updated `README.md` with the correct `38` maintained-skill count, current
  sync workflow, and the explicit source-of-truth policy for this workspace
- Updated `CLAUDE.md` to document Codex versus Claude sync targets, repo-wide
  lesson tracking, and the maintained skill structure in clean ASCII

### Fixed

- Removed the stale `nestjs` entry from the maintained skill catalog
- Removed mojibake from the root documentation set by normalizing headings and
  structure examples to ASCII

## [2026-03-10] - nextjs-development Skill Added

### Added

- New `nextjs-development` maintained skill folder covering Next.js 15/16
  (v16.1.6)
- `SKILL.md` with 12 parts: App Router routing, Server/Client Components,
  `use cache` directive, `cacheTag()` and `cacheLife()`, Server Actions,
  `<Form>` component, `after()`, `connection()`, Turbopack, metadata API,
  auth interrupts (`forbidden()` and `unauthorized()`), and upgrade codemods
- Async Request APIs section covering the v15 breaking change for `params`,
  `searchParams`, `cookies()`, and `headers()`
- Next.js MCP dev tools coverage (`next-devtools-mcp`) with `.mcp.json` setup,
  all 5 runtime tool descriptions, and example agent prompts
- `references/app-router-reference.md`: complete file conventions table,
  dynamic routes, route groups, parallel routes, intercepting routes, and OG
  image generation
- `references/nextjs-mcp-server.md`: full `next-devtools-mcp` setup guide and
  troubleshooting
- `examples/data-fetching-patterns.md`: 8 patterns from `use cache` to SWR
  with TypeScript
- `examples/server-client-components.md`: RSC/RCC decision guide and 9
  composition patterns
- `scripts/page-generator.ps1`: scaffold `page.tsx`, `loading.tsx`,
  `error.tsx` for any route, with automatic handling of dynamic segment params
- `CHANGELOG.md` and `LICENSE.txt` (MIT) for the skill folder

## [2026-03-10] - README MCP Inventory Refresh

### Changed

- Rewrote `README.md` in clean ASCII to remove the visible encoding corruption
  in the structure examples and formatting blocks
- Added a complete maintained-skill catalog so the README now covers all
  editable skills instead of a partial subset
- Added a verified MCP server inventory with current sources for Serena,
  Context7, Notion, Microsoft Learn Docs, Playwright, Power BI, Microsoft
  Agent 365 Office preview, and NotebookLM
- Added a per-skill MCP map to show which maintained skills are MCP-backed,
  host-specific, client-specific, or fully local

## [2026-03-09] - Custom Agent Discovery Alignment

### Changed

- Updated the `custom-agent-usage` skill, examples, and helper script to use
  the real custom-agent discovery directories on this machine:
  `C:\Users\LOQ\.claude\agents` and
  `C:\Users\LOQ\AppData\Roaming\Code - Insiders\User\prompts`
- Added repo-level guidance that the VS Code Insiders prompts folder contains
  mixed prompt file types and must be filtered to `*.agent.md` for subagent
  discovery

### Fixed

- Removed stale custom-agent discovery references to legacy
  `.copilot/agents` and `.github/copilot/agents` locations
- Removed the external `glob` dependency from
  `custom-agent-usage/scripts/agent-finder.js` so the helper runs in the
  current local Node environment

## [2026-03-09] - Workspace Skill Modernization

### Changed

- Modernized editable skill folders to align with the maintained structure of
  `SKILL.md`, `scripts/`, and `references/`
- Removed duplicated `## Related Skills` sections across the editable skill
  set
- Rewrote outdated MCP-heavy skills to reflect current 2026 behavior,
  especially for Notion, Microsoft Learn, NotebookLM, Power BI, and
  Office-document workflows
- Updated `README.md` to reflect the real workspace layout, current counts,
  loading order, and MCP guidance

### Added

- New runnable helper scripts for skills that previously had references only:
  - `breaking-changes-management/scripts/migration-guide-scaffold.py`
  - `code-examples-sync/scripts/example-sync-check.py`
  - `documentation-automation/scripts/docs-pipeline-scaffold.py`
  - `documentation-patterns/scripts/doc-template-picker.py`
  - `documentation-quality/scripts/doc-style-audit.py`
  - `documentation-verification/scripts/doc-link-check.py`
  - `web-design-reviewer/scripts/css-risk-audit.py`
- New current-reference notes:
  - `microsoft-development/references/microsoft-learn-mcp.md`
  - `notion-docs/references/notion-mcp-quickstart.md`
  - `notebooklm-management/scripts/README.md`
- Backfilled `CHANGELOG.md` into every editable skill folder and added a dated
  `2026-03-09` entry for each skill
- Normalized per-skill changelog headings so only `Added`, `Changed`, `Fixed`,
  and `Tested` are used

### Fixed

- Replaced broken PowerShell automation in:
  - `azure-integrations/scripts/deploy-appservice.ps1`
  - `microsoft-development/scripts/azure-health-check.ps1`
- Removed stale references to old global skill paths and legacy repo
  structure assumptions

## [2026-03-01] - Activation Testing and Fixes

### Fixed

- `javascript-development`: Added `TypeScript` to the description so
  TypeScript prompts without React context activate the right skill
- `frontend-design`: Added generic `CSS`, `wireframes`, and `writing CSS`
  keywords
- `web-testing`: Added `unit tests` to the description
- `web-design-reviewer`: Added clearer disambiguation against automated E2E
  testing

## [2026-02-28] - Description Rewrite and Cross-References

### Changed

- Rewrote all 37 non-superpower skill descriptions to concise
  activation-focused language
- Reduced overlap between related skills, especially JS vs React, DevOps vs
  Workflow, and the documentation skill cluster

### Added

- Added `## Related Skills` cross-reference tables across the editable skill
  set
