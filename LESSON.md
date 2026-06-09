# Lessons

Lessons and maintenance mistakes for the shared Copilot, Claude Code, Codex, and Gemini CLI skill catalog.

## Source of Truth

- Edit skills in `C:\Users\LOQ\.copilot\skills` first.
- Install or import new maintained skills in `C:\Users\LOQ\.copilot\skills` first.
- Treat `C:\Users\LOQ\.codex\skills`, `C:\Users\LOQ\.agents\skills`, `C:\Users\LOQ\.claude\skills`, and workspace-local skill roots as deployment targets.
- Rebuild Gemini commands after changing `SKILL.md` content.
- Keep `GEMINI.md` tracked in the repo; only the generated `.gemini/` directory should stay ignored.

## Inventory Lessons

- Count real skill folders by checking for `SKILL.md`, not by counting directories.
- Derive the maintained count by excluding the explicit copied official superpower list in `scripts/skill-registry.json`, not by whether a folder has `CHANGELOG.md`.
- Keep copied official superpowers separate from maintained skills so counts and maintenance expectations stay honest.
- Treat `gws-*` and `recipe-*` folders as local-only skills excluded from the public repo via `.gitignore`. Do not include them in public counts, catalogs, or GitHub-facing documentation.
- Keep two inventory views in root docs: git-tracked catalog counts and local workspace counts. Mixing them in one number creates avoidable drift and confusion.

## Portability Lessons

- A portability footer alone is not enough; imported skills may still contain host-specific wording in frontmatter or body content.
- Every MCP-aware skill needs an explicit no-MCP fallback path or it will fail in at least one client.
- Gemini CLI command files must be generated with safely escaped TOML strings. Raw multiline embedding breaks on Windows paths, Markdown code fences, and backslashes.
- Discovery catalogs are not automatically the canonical source. If a discovery repo points to an official upstream skill, record both and import from the stronger maintained original.
- If you track a raw imported skill before normalizing it, update the root docs immediately so counts stay accurate and the schema exceptions are explicit.

## Sync Lessons

- The workspace sync script should treat the repo inventory and discovered workspace targets as separate summary keys. Reusing the same key hides useful state.
- Downstream skill folders behave like branch mirrors: make changes in this repo first, then publish them outward with the sync script.
- After a catalog-wide doc-only refresh, still rerun Gemini export and downstream sync so the mirrors do not lag the workspace copy.
- Keep the primary Codex root (`C:\Users\LOQ\.codex\skills`) distinct from the shared mirror (`C:\Users\LOQ\.agents\skills`) so documentation does not blur installation targets.
- The Codex root can keep extra local skills outside this catalog, so sync verification there should compare the expected maintained set rather than only the total folder count.
- Workspace-local skill roots under `.agent\skills`, `.agents\skills`, and `.claude\skills` are worth syncing when the broader workspace depends on shared skills.
- Gemini Antigravity can consume the full current skill catalog from `C:\Users\LOQ\.gemini\antigravity\global_skills`, so it should be treated as a first-class sync target rather than a manual copy.
- Mirror copies should replace stale skill folders entirely so old `SKILL.md.bak` files or removed support files do not linger.

## Documentation Lessons

- Root docs drift quickly when counts are copied from memory. Recompute live counts before editing `README.md` or `CLAUDE.md`.
- Keep root docs aligned on supported clients. If Gemini CLI support changes, update `README.md`, `CLAUDE.md`, and `GEMINI.md` together.
- When a catalog-wide skill refresh bumps shared metadata or structure, document the new baseline explicitly in the root docs and root changelog even if the inventory counts do not change.
- When a catalog-wide skill refresh adds a required section such as `Verification Protocol`, update root docs, per-skill changelogs, Gemini guidance, and sync mirrors in the same pass.
- Keep documentation ASCII-first unless Unicode materially improves clarity.

## Verification Lessons

- Structural validation is not enough for Gemini support; export and parse the generated TOML files too.
- When the catalog frontmatter or required section schema changes, update the validator before relying on the next export or sync pass.
- Spot-check imported skills after bulk modernization. Source catalogs can include host-specific assumptions, placeholder variables, or formatting that does not match the rest of the repo.
- Record source repo and commit metadata for imported skills so later updates can be traced safely.
- Keep official provenance sidecars from trusted imports when they add value. NVIDIA skill imports, for example, ship `skill-card.md`, `skill.oms.sig`, and benchmark evidence that should stay with the vendored copy unless removal is deliberate and documented.
- If an imported tracked skill is still missing catalog sections or `CHANGELOG.md`, document that exception plainly until the modernization pass is done.
- When a source repository has moved, compare the exact recorded source paths before changing maintained skill content; many upstream commits do not touch the vendored skill path.
- Smoke-test bundled helper scripts after import. A skill can look fine in Markdown while its local fallback tooling still behaves poorly.
- Local secret scans should ignore generated command folders and agent metadata by default or they will drown in false positives.
- Do not commit Python bytecode or generated `__pycache__` artifacts. They are ignored and should be removed if a helper-script smoke test creates them.
- Validation scans should ignore local environment folders such as `.venv`, `venv`, and `env` when looking for stray `*.pyc` files, or they will produce false positives from toolchain internals.

## Update Checklist

1. Edit the workspace copy.
2. If the change is a new skill, install or import it into this repo before touching downstream targets.
3. Update per-skill `CHANGELOG.md` files for every touched skill folder.
4. Update root docs if counts, support matrix, sync behavior, or client guidance changed.
5. Run `python scripts/validate-skills.py`.
6. Run `python scripts/export-gemini-skill.py --all`.
7. Sync outward with `powershell -ExecutionPolicy Bypass -File .\scripts\sync-skills.ps1`.
8. Record any new gotchas here before closing the task.
