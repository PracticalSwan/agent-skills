# Lessons

Lessons and maintenance mistakes for the shared Copilot/Codex/Claude skill catalog.

## Source of Truth

- Edit skills in `C:\Users\LOQ\.copilot\skills` first.
- Treat `C:\Users\LOQ\.agents\skills` and `C:\Users\LOQ\.claude\skills` as deploy targets, not authoring locations.
- Sync maintained skills outward after every structural or content update.

## Layout Lessons

- Count actual skill folders with `SKILL.md` instead of counting top-level directories. The workspace also contains `.serena`, which is metadata and not a skill.
- Derive the maintained-skill count from folders that contain both `SKILL.md` and `CHANGELOG.md`. That avoids silently drifting counts when copied official skills are present.
- Keep copied official superpowers distinct from maintained skills. They are tracked locally for discovery, but they do not follow the same maintenance contract.

## Host-Specific Lessons

- Codex stores copied official superpowers under `C:\Users\LOQ\.agents\skills\superpowers`, not as top-level skill folders.
- Claude already ships plugin-managed superpowers outside `C:\Users\LOQ\.claude\skills`. Do not mirror copied official superpowers into that folder unless you intentionally want local overrides.
- A one-way sync from the workspace avoids conflicting edits across clients.

## Documentation Mistakes Fixed

- The root README had drifted to `39` maintained skills and still listed a non-existent `nestjs` skill. Use live inventory, not memory, when updating catalog counts.
- `CLAUDE.md` and the root changelog had visible mojibake from copied box-drawing and punctuation characters. Keep repository docs ASCII-first unless Unicode is truly needed.
- Old target folders had leftover `SKILL.md.bak` files and placeholder `references/README.md` and `scripts/README.md` files that no longer existed in the workspace. Mirror copies should remove those stale artifacts.

## Update Checklist

1. Edit the workspace copy.
2. Update `README.md`, `CLAUDE.md`, and `CHANGELOG.md` if repo structure, counts, or sync behavior changed.
3. Run `powershell -ExecutionPolicy Bypass -File .\scripts\sync-skills.ps1`.
4. Re-run the inventory diff to confirm the workspace and target folders match where they are supposed to.
5. Record any new maintenance gotchas here before closing the task.
