# Contributing

This catalog serves GitHub Copilot, Claude Code, and Codex. Keep additions
useful across clients and easy to verify.

## Before editing

- Read [LESSON.md](LESSON.md) and [AGENTS.md](AGENTS.md).
- Inspect Git status and preserve unrelated work.
- Treat `SKILL.md` as the source of truth for a skill's behavior.
- Keep tracked content free of credentials, personal identifiers, and
  machine-specific or project-specific paths.

## Add or refresh a skill

1. Confirm the task is not already covered by a maintained skill.
2. Prefer a canonical upstream source over discovery catalogs or plugin
   snapshots. For child-only skills, inspect only the user's global `.codex`,
   `.agents`, and `.claude` skill roots.
3. Review the exact upstream skill path and its supporting files at a pinned
   revision. Import or refresh only material changes relevant to that mapping.
4. Preserve applicable licenses, provenance, security safeguards, and
   cross-client fallbacks. Do not copy host metadata or credentials.
5. Keep the folder name aligned with frontmatter `name`. Include `CHANGELOG.md`
   for maintained skills and follow the required sections described in
   [AGENTS.md](AGENTS.md).
6. Update `scripts/skill-registry.json` and
   [REFERENCE_SOURCES.md](REFERENCE_SOURCES.md) for external provenance.
7. Generate the public catalog index and update the relevant root
   documentation.

Codex plugin skills are candidates only when they are self-contained,
portable, materially useful, and distinct from existing catalog workflows.
Avoid importing whole plugin bundles or skills that depend on unverified host
tools.

The 2026-11-16 plugin review selected no additional imports: available Codex
engineering and security workflows either depend on host-specific facilities
or overlap maintained review, security, and plugin-authoring skills. Recheck
the catalog before importing a future candidate.

## Validate and sync

Run the focused checks after edits:

```powershell
py -3 scripts/validate-skills.py
py -3 scripts/test_validate_skills.py
py -3 scripts/test-promote-child-skills.py
py -3 scripts/build-skill-catalog.py --check
git diff --check
```

For an approved mutation, sync only to the three user-global skill roots using
the allowlisted script:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\sync-skills.ps1
```

Compare the parent inventory with the downstream mirrors and verify hashes for
maintained skill content. Preserve unknown personal skills and host-managed
folders. Never sync to project-specific skill roots.

During parent source maintenance, run
`scripts/update-codex-local-blender-skills.ps1`. Its protected Codex-only
overlay remains outside this catalog and all shared mirrors.

## Documentation and publication

Update the README, agent instructions, Claude notes, lessons, contributor
guide, changelog, and source index when their content changes. Update
`MIGRATION.md` when compatibility or sync behavior changes.

Do not publish a change while validation fails, privacy or provenance issues
remain, or the final diff includes unrelated files. Do not rewrite published
Git history without explicit authorization.

## Commit and push

Treat publication as the normal completion step when the user requests it, the
task or release workflow recommends it, or a substantial coherent change is
ready. Substantial changes include multi-file implementations or refactors,
catalog refreshes, and coordinated workflow or documentation updates; a
scratch experiment or isolated trivial typo alone does not qualify. After the
required checks and catalog sync/hash verification pass, inspect the branch and
diff, stage only task files, commit on the intended current branch, and push to
its configured GitHub remote without asking for a second confirmation. Keep
unrelated user work unstaged. Stop and report if validation fails, unrelated
changes cannot be separated, the branch has diverged, or the GitHub remote is
unavailable. Never force-push or rewrite published history.
