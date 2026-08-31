# Lessons

Lessons and maintenance mistakes for the shared Copilot, Claude Code, and
Codex skill catalog.

## Source of Truth

- Edit skills in `C:\Users\LOQ\.copilot\skills` first.
- Install or import new maintained skills in `C:\Users\LOQ\.copilot\skills` first.
- Treat only three personal-global roots as deployment targets:
  `C:\Users\LOQ\.codex\skills`, `C:\Users\LOQ\.agents\skills`, and
  `C:\Users\LOQ\.claude\skills`.
- Keep normal child promotion limited to personal `.codex`, `.agents`, and
  `.claude` roots. Do not scan or sync project-local skill roots unless the
  user explicitly scopes them.
- Preserve Codex `.system` skills as host-managed. Publish normalized catalog
  copies to shared and Claude roots without overwriting those system folders.
- Treat `arjun988/blender-skills` as a Codex-only exception: its skills remain in `C:\Users\LOQ\.codex\skills`, are never promoted into the parent, and never sync to `.agents` or `.claude`.
- Parent maintenance still owns freshness for that exception through `scripts/update-codex-local-blender-skills.ps1`, which must run during source-refresh or update-all-skills work.

## Inventory Lessons

- Count real skill folders by checking for `SKILL.md`, not by counting directories.
- Derive the maintained count by excluding the explicit copied official superpower list in `scripts/skill-registry.json`, not by whether a folder has `CHANGELOG.md`.
- Keep copied official superpowers separate from maintained skills so counts and maintenance expectations stay honest.
- Treat `gws-*` and `recipe-*` folders as local-only skills excluded from the public repo via `.gitignore`. Do not include them in public counts, catalogs, or GitHub-facing documentation.
- Keep two inventory views in root docs: git-tracked catalog counts and local workspace counts. Mixing them in one number creates avoidable drift and confusion.
- Child-path reconciliation must compare the parent only with the user-scoped
  personal roots. Promote portable extras into the parent, normalize invalid
  names to lowercase hyphen-case, and preserve source provenance.
- Categorized upstream catalogs can hide skills below an extra directory level. Discover by `SKILL.md`, flatten by the normalized skill name, and check for duplicate names before copying.
- An upstream installation page, repository README, and live skill tree can
  expose different counts. For `--all` imports, reconcile the live
  `SKILL.md` tree at a pinned commit and document any newer unlisted skill
  instead of silently omitting it.
- Exact duplicate files across separate skill folders are not automatically
  redundant. Preserve self-contained schemas, validators, licenses, and
  per-skill changelogs unless the deployment contract changes.
- An untracked empty directory can mask a broken tracked Markdown link. Verify
  links against files present in Git, not only against the live filesystem.

## Portability Lessons

- A portability footer alone is not enough; imported skills may still contain host-specific wording in frontmatter or body content.
- Every MCP-aware skill needs an explicit no-MCP fallback path or it will fail in at least one client.
- A portability footer does not grant host capabilities. Browser, image,
  plugin, and docs skills need explicit Codex, Claude Code, and fallback
  routes.
- Claude Code on a third-party endpoint such as the GLM Coding Plan must not
  assume Anthropic's native Chrome integration is available. Use an active
  external browser MCP or stop at a manual handoff.
- CLI-backed web skills remain portable when the skill separates capability
  routing from the host surface: use a configured MCP server when present,
  otherwise use the reviewed external CLI or official SDK.
- Discovery catalogs are not automatically the canonical source. If a discovery repo points to an official upstream skill, record both and import from the stronger maintained original.
- If you track a raw imported skill before normalizing it, update the root docs immediately so counts stay accurate and the schema exceptions are explicit.

## Skill Consolidation Lessons

- Keep one canonical general frontend creation and art-direction workflow at
  `frontend-design`. Route the retired `frontend-skill` and
  `premium-frontend-ui` names there instead of recreating style-specific
  skills.
- Keep `web-design-reviewer` separate because post-implementation browser QA
  has a different activation boundary and evidence path from design creation.
- Define frontend quality as fitness for context with accessibility and
  functional correctness as hard gates. Visual intensity, cards, motion,
  immersive effects, and animation dependencies are conditional techniques.
- Before deleting overlapping imported skills, inspect every source file and
  upstream license. Preserve applicable license texts, attribution, historical
  provenance, and modification notices with the canonical result.
- When external skills link to a canonical section anchor such as
  `#component-review-rubric`, verify the heading and every dependent link after
  the rewrite.

## Sync Lessons

- The workspace sync script should treat the repo inventory and discovered workspace targets as separate summary keys. Reusing the same key hides useful state.
- Downstream skill folders behave like branch mirrors: make changes in this repo first, then publish them outward with the sync script.
- After a catalog-wide doc-only refresh, still rerun validation and downstream
  sync so the mirrors do not lag the workspace copy.
- Keep the primary Codex root (`C:\Users\LOQ\.codex\skills`) distinct from the shared mirror (`C:\Users\LOQ\.agents\skills`) so documentation does not blur installation targets.
- The Codex root can keep extra local skills outside this catalog, so sync verification there should compare the expected maintained set rather than only the total folder count.
- Downstream sync is locked to three personal-global roots:
  `C:\Users\LOQ\.agents\skills`, `C:\Users\LOQ\.codex\skills`, and
  `C:\Users\LOQ\.claude\skills`. The sync script enforces this allowlist and
  refuses to write anywhere else.
- Project-local roots such as those under `C:\Assumption University` are out
  of scope for normal promotion and sync.
- Mirror copies should replace stale skill folders entirely so old
  `SKILL.md.bak` files or removed support files do not linger.
- When routing changes, prune only known catalog-owned copies that now conflict
  with policy. Preserve unknown personal skills and host-owned system folders.
- When refreshing copied official skills from a newly categorized upstream,
  replace stale support files in the parent while preserving catalog changelog
  history. Promote extracted support documents that became standalone skills
  instead of keeping duplicate embedded copies.
- After a user-requested mutation task in this workspace is complete and
  satisfactory, sync outward every time, then commit and push without asking
  for extra confirmation. Escalate before commit or push only when work is
  incomplete, validation/sync failed, a required command was rejected,
  security or privacy risk remains, or staging is unsafe.
- When a maintained skill is deliberately retired, add only its reviewed exact
  name to the sync cleanup and verify it is removed from all three approved
  personal-global roots. Never expand that cleanup into unknown personal or
  project-specific skill paths.

## Documentation Lessons

- Every new agent session in this workspace should begin by reading `LESSON.md` before any other task work so prior mistakes stay visible.
- Root docs drift quickly when counts are copied from memory. Recompute live counts before editing `README.md` or `CLAUDE.md`.
- Keep root docs aligned on supported clients and link a migration guide for
  breaking client-support changes.
- When a catalog-wide skill refresh bumps shared metadata or structure, document the new baseline explicitly in the root docs and root changelog even if the inventory counts do not change.
- When a catalog-wide skill refresh adds a required section such as
  `Verification Protocol`, update root docs, per-skill changelogs, and sync
  mirrors in the same pass.
- Keep documentation ASCII-first unless Unicode materially improves clarity.

## Verification Lessons

- Live social-post skills must distinguish drafting from publishing, require
  action-time confirmation before media upload or final submission, and find
  the new post in current activity before claiming success.
- Structural validation must also reject removed-client wording in active
  `SKILL.md` files and reject retired support surfaces in the repo.
- When the catalog frontmatter or required section schema changes, update the validator before relying on the next export or sync pass.
- Spot-check imported skills after bulk modernization. Source catalogs can include host-specific assumptions, placeholder variables, or formatting that does not match the rest of the repo.
- Audit imported reference files as well as `SKILL.md`. A removed-client
  integration can remain hidden in a support document even when the skill
  entrypoint is portable.
- Installing an agent skill does not authorize installing its runtime or
  collecting credentials. Keep runtime setup explicit, prefer reviewable
  package-manager commands, and leave authentication to an approved secret or
  login flow.
- Record source repo and commit metadata for imported skills so later updates can be traced safely.
- When a child source is not owned by git, record a `local-workspace://` source plus a SHA-256 tree digest instead of inventing a commit.
- Historical curated skills can disappear from upstream HEAD. Match the child copy byte-for-byte to the last canonical commit and record that historical commit rather than pretending the retired skill is still current.
- Keep official provenance sidecars from trusted imports when they add value. NVIDIA skill imports, for example, ship `skill-card.md`, `skill.oms.sig`, and benchmark evidence that should stay with the vendored copy unless removal is deliberate and documented.
- If an imported tracked skill is still missing catalog sections or `CHANGELOG.md`, document that exception plainly until the modernization pass is done.
- When a source repository has moved, compare the exact recorded source paths before changing maintained skill content; many upstream commits do not touch the vendored skill path.
- Smoke-test bundled helper scripts after import. A skill can look fine in Markdown while its local fallback tooling still behaves poorly.
- The verified Stitch MCP surface in this workspace is design-system oriented: `create_project`, `upload_design_md`, `create_design_system_from_design_md`, `list_design_systems`, and `apply_design_system`. Do not claim screen lookup, screen generation, screen editing, or variant tools exist unless the active host exposes them.
- Imported skills that broker third-party content need explicit prompt-injection boundaries and credential-collection limits in the normalized `SKILL.md`; do not assume upstream README safety notes survive a catalog rewrite.
- Local secret scans should ignore agent metadata and generated caches by
  default or they will drown in false positives.
- Do not commit Python bytecode or generated `__pycache__` artifacts. They are ignored and should be removed if a helper-script smoke test creates them.
- Validation scans should ignore local environment folders such as `.venv`, `venv`, and `env` when looking for stray `*.pyc` files, or they will produce false positives from toolchain internals.
- Keep validator behavior aligned with documented policy. If docs ban `### Tested` and require `Verification Protocol` immediately after `Anti-Patterns`, enforce both conditions and migrate historical headings without deleting their evidence.
- Partial clones can fail when a later checkout needs missing blobs. For source refreshes that require copying many support files, a shallow full checkout is more reliable than a filtered no-checkout clone on this Windows host.
- Run the final cache scan after helper-script smoke tests because imports and
  help commands can regenerate ignored `__pycache__` files.
- Before removing a retired external mirror, resolve the exact leaf path,
  compare inventories and digests, confirm that no configuration or process
  uses it, and preserve all surrounding application state.

## 2026-08-08 Matt Pocock Skill Import

- When importing from a categorized upstream catalog, audit every live
  `SKILL.md` entrypoint and its support files first; README indexes can omit
  beta, misc, or newly added entries.
- Select skills by real workspace gaps and preserve stronger local equivalents
  for overlapping TDD, debugging, review, implementation, planning, and skill
  authoring workflows.
- Normalize imported content before validation, retain the upstream license
  and pinned commit, and adapt host-specific or destructive-operation guidance
  to the catalog's cross-client and approval boundaries.
- Keep the parent catalog as the source of truth and sync only the approved
  personal-global roots. Project-local skill paths remain out of scope even
  when the workspace audit reads their project documentation.

## 2026-08-14 Catalog Freshness And Source Sync

- Compare each recorded source commit with the live upstream head, then
  inspect only the exact mapped paths before refreshing a normalized skill.
  Repository-wide head movement is not evidence that every imported skill
  changed.
- When an upstream refresh adds a client-specific setup path that the catalog
  intentionally retired, copy the current workflow but remove that setup
  surface and keep an honest no-MCP or manual fallback.
- Preserve the parent catalog's wrappers and changelogs when importing current
  support trees. Replacing a full upstream folder can silently drop local
  provenance, approval gates, or client-routing safeguards.
- A catalog-wide metadata refresh must update all root inventory snapshots and
  the generated source report in the same change, even when skill counts stay
  unchanged.
- Child reconciliation is a separate check from upstream refresh: compare only
  personal `.codex`, `.agents`, and `.claude` roots, report eligible extras
  explicitly, and do not scan project-specific paths.

## 2026-08-16 Installed Platform And Web Skills

- Compare each installed child tree with the exact upstream path at a pinned
  current commit before promotion; this distinguishes a verified source match
  from an unverified local copy.
- Keep an aggregate audit router and its focused leaves separate when their
  activation boundaries, evidence, or output shape differ. The same rule keeps
  Vercel React performance guidance separate from framework and art-direction
  skills.
- Keep official Gemini API terminology allowed in active skills and docs while
  rejecting retired command-line or provider-specific host support;
  managed-agent IDs must come from current account/documentation discovery.
- When a source skill is MCP-aware, name the optional server in the catalog
  registry and keep an official-doc or CLI fallback. Configuration and
  authentication remain explicit user-authorized actions.
- Shell-based helpers need a truthful Windows/manual fallback. Do not claim a
  POSIX script ran when its shell or `jq` dependency is unavailable.
- Promote from the personal Codex root into the parent first, update registry
  provenance and root counts, then validate and sync only the three approved
  personal-global roots. Project-specific paths remain out of scope.

## 2026-08-16 Related Skill Consolidation Audit

- Compare parent skills with plugin-managed copies before merging. Plugin
  copies can be older or omit catalog safety, provenance, and cross-client
  sections; keep them external when the parent is the stronger maintained
  canonical copy.
- Keep related skills separate when their activation boundary, input/output
  shape, or evidence path differs. Add explicit `Related Skills` routes so
  discoverability improves without collapsing distinct workflows.
- For this audit, platform/Postgres, general/Interactions, React
  implementation/performance, and aggregate/focused web-quality workflows
  remained separate after review.

## 2026-08-20 VoltAgent Platform Import And Maintenance

- Treat `VoltAgent/awesome-agent-skills` as a discovery index, then pin and
  import from each canonical vendor repository; record the exact source commit
  and selected path in `scripts/platform_skill_manifest.py` and the generated
  `REFERENCE_SOURCES.md`.
- Gate CLI-specific imports on commands actually present on the host. This
  refresh found `vercel`, `netlify`, and `supabase`, but not `hf`,
  `huggingface-cli`, `mongosh`, `mongo`, or `figma`; omit absent CLI skills
  rather than documenting an uninstalled executable as available.
- Audit imported support-file links from their actual nested location. A
  source-relative `references/...` link can become broken after importing a
  file that is already inside `references/`; resolve it or replace it with the
  vendor's stable official documentation URL.
- Run `scripts/update-codex-local-blender-skills.ps1` during parent source
  maintenance. On this refresh it completed successfully at upstream commit
  `8f778d2405a214b508d4c7d80742be8e43acdd52` with 94 upstream skills plus one
  separately protected local entry and no promotion to the parent, shared, or
  Claude roots.
- Keep the approved sync boundary explicit: only
  `C:\Users\LOQ\.codex\skills`, `C:\Users\LOQ\.agents\skills`, and
  `C:\Users\LOQ\.claude\skills` may receive downstream catalog writes.

## 2026-08-24 Catalog Freshness And Personal Child Promotion

- Compare every recorded upstream head with the exact mapped skill path before
  rewriting content. This pass found material changes in `avoid-ai-writing`,
  the eight selected Matt Pocock workflows, and `x-twitter-scraper`; unrelated
  repository movement was recorded in provenance without broad rewrites.
- A personal Codex root can contain plugin-managed skills that are not in the
  parent catalog. Promote only the eligible five Codex Router skills, omit
  their host marker files, and retain package plus tree-digest provenance.
- Keep `.codex`, `.agents`, and `.claude` child reconciliation separate from
  project-specific paths. Codex `.system`, Blender, copied Superpowers, and
  unknown personal skills remain protected from parent ownership and sync.
- When an upstream skill deletes a reference file, apply that deletion while
  preserving catalog changelogs and reviewed provenance sidecars. Run the
  complete validator after the catalog-wide modernization pass.

## 2026-08-31 Catalog Freshness And Corpus Refresh

- Recheck live source heads at each continuation. This pass found one new
  installed-path delta in `avoid-ai-writing` corpus support; repository head
  movement alone was not evidence that the other mapped skills changed.
- Preserve corpus lineage when adding public seeds: record register, selector,
  rights status, hash, and sample-size limits in the manifest and README.
- Smoke-test source helpers after a support refresh. The selector-aware corpus
  extractor now has regression coverage for authored semantic elements and
  page chrome outside the selected container.
- Keep child reconciliation limited to `.codex`, `.agents`, and `.claude` and
  keep protected Blender, `.system`, Superpowers, and project paths outside
  promotion and sync ownership.

## 2026-08-29 Catalog Freshness And Mirror Repair

- Recheck live source heads on every continuation. A clean published parent can
  still have stale pins within days, while most repository movement remains
  outside the installed mappings.
- Compare exact mapped paths before copying current source content. This pass
  refreshed `avoid-ai-writing`, `x-twitter-scraper`, Gemini, React View
  Transitions, and web-quality references while leaving unrelated paths alone.
- A downstream mirror can drift independently after publication. Compare the
  expected maintained set against each target and restore only evidence-backed
  missing skills such as the Codex `doc` copy.
- Treat source removals as current behavior: when Xquik dropped MCP setup files,
  remove the stale registry mapping and regenerate the normalized no-MCP tail.
- The current protected set is 94 upstream Blender skills plus one explicitly
  configured local entry. Keep that distinction in generated documentation.

## Update Checklist

1. Edit the workspace copy.
2. If the change is a new skill, install or import it into this repo before touching downstream targets.
3. Update per-skill `CHANGELOG.md` files for every touched skill folder.
4. Update root docs if counts, support matrix, sync behavior, client guidance, or startup rules changed.
5. Run `python scripts/validate-skills.py`.
6. Sync outward with `powershell -ExecutionPolicy Bypass -File .\scripts\sync-skills.ps1`.
7. If the work is satisfactory, commit and push to GitHub.
8. Record any new gotchas here before closing the task.
