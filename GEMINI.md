# GEMINI.md

This repository exposes its skills to Gemini CLI through generated project commands.

## Required Session Start Rule

- Every new session in this workspace must begin by reading `LESSON.md`.
- Treat `LESSON.md` as required startup context before analysis, planning, edits, validation, reviews, or advisory work.
- If `LESSON.md` is missing or unreadable, stop and report that blocker before continuing.

## Source of Truth

- Edit skill content in `SKILL.md` files under `C:\Users\LOQ\.copilot\skills`
- Do not hand-edit files under `.gemini/commands/skills`
- The repo currently tracks `135` skill folders: `103` maintained skills and `32` copied official Superpowers
- All tracked skills use catalog `version: "1.3"`; `linkedin-create-post` is dated `2026-07-29`, while the prior tracked catalog baseline remains dated `2026-07-11`
- The live local catalog contains `193` skills when the `58` local-only Google Workspace overlays are present
- The tracked imports `docx`, `jupyter-notebook`, `pptx`, and `xlsx` have finalized canonical provenance in `scripts/skill-registry.json`

## Generated Commands

Each skill is exported as a Gemini CLI command:

- `/skills:<skill-name>`

Examples:

- `/skills:java-junit`
- `/skills:linkedin-create-post`
- `/skills:pdf`
- `/skills:security-review`
- `/skills:x-twitter-scraper`

Generated command files live in:

- `C:\Users\LOQ\.copilot\skills\.gemini\commands\skills`

Export and validation count every local folder that contains `SKILL.md`. If this workspace includes local-only overlays (for example `gws-*` or `recipe-*`), Gemini command totals can be higher than the git-tracked catalog totals.

The current shared skill folders also sync to the Gemini Antigravity global skill path and the Antigravity CLI skill path:

- `C:\Users\LOQ\.gemini\antigravity\global_skills`
- `C:\Users\LOQ\.gemini\antigravity-cli\skills`

## Refresh Workflow

After changing, adding, or removing skills:

```powershell
python scripts/export-gemini-skill.py --all
```

Run that export after catalog-wide documentation refreshes too, not only after new skills or helper scripts land.

When a child or categorized skill root has additional skills, promote them into the parent with `scripts/promote-child-skills.py`, normalize the full catalog with `scripts/modernize-skills.py`, and refresh provenance with `scripts/update-skill-registry.py` before exporting commands.

Then reload commands inside Gemini CLI:

```text
/commands reload
```

For mutation tasks in this workspace, follow the shared completion rule from
`AGENTS.md` and `CLAUDE.md`: after the task is complete, validate, export, sync
the skill folders, then commit and push when the result is satisfactory.

## Validation

Before relying on the exported commands:

```powershell
python scripts/validate-skills.py
```

That validation checks:

- catalog `SKILL.md` frontmatter (`name`, `version`, `last_updated`, `tags`, `description`)
- required portability and MCP sections
- `Preferred MCP Server:` and `Fallback prompt:` lines
- `Anti-Patterns`, immediately followed by `Verification Protocol`, and a final `Related Skills` section
- `CHANGELOG.md` presence in every skill folder
- changelog entries that use `Added`, `Changed`, and `Fixed` sections only; `### Tested` and `### Verified` are rejected
- Gemini command count
- TOML parseability of generated commands
- obsolete Skill Paths sections, stale removed-skill links, mojibake markers, and generated Python bytecode

Catalog policy and validation require each `SKILL.md` to include `## Verification Protocol` immediately after `## Anti-Patterns`.
The tracked imports `docx`, `jupyter-notebook`, `pptx`, and `xlsx` now validate against the shared schema baseline and have finalized provenance metadata.

For externally imported skills, normalize the workspace copy and run any local smoke tests before exporting new Gemini command files. The generated command should only mirror maintained content that already passed the repo checks.

## Notes

- The Gemini command prompt tells Gemini to resolve relative paths against the source skill folder.
- MCP-aware skills still include no-MCP fallback guidance, so they remain usable even if Gemini CLI is running without the same MCP surface as another host.
