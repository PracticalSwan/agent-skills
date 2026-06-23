# GEMINI.md

This repository exposes its skills to Gemini CLI through generated project commands.

## Required Session Start Rule

- Every new session in this workspace must begin by reading `LESSON.md`.
- Treat `LESSON.md` as required startup context before analysis, planning, edits, validation, reviews, or advisory work.
- If `LESSON.md` is missing or unreadable, stop and report that blocker before continuing.

## Source of Truth

- Edit skill content in `SKILL.md` files under `C:\Users\LOQ\.copilot\skills`
- Do not hand-edit files under `.gemini/commands/skills`
- The repo currently tracks `93` skill folders
- Most tracked maintained skills remain aligned on `version: "1.2"`; the imported Stitch skills remain normalized to `version: "1.2"` with `last_updated: 2026-06-15`, the new `x-twitter-scraper` skill is normalized to `version: "1.2"` with `last_updated: 2026-06-24`, and the NVIDIA skills plus refreshed tracked imports `docx`, `jupyter-notebook`, `pptx`, and `xlsx` remain normalized to `version: "1.2"`
- The tracked imports `docx`, `jupyter-notebook`, `pptx`, and `xlsx` now match that baseline, but they still need finalized provenance mapping in `scripts/skill-registry.json`

## Generated Commands

Each skill is exported as a Gemini CLI command:

- `/skills:<skill-name>`

Examples:

- `/skills:java-junit`
- `/skills:pdf`
- `/skills:security-review`
- `/skills:x-twitter-scraper`

Generated command files live in:

- `C:\Users\LOQ\.copilot\skills\.gemini\commands\skills`

Export and validation count every local folder that contains `SKILL.md`. If this workspace includes local-only overlays (for example `gws-*` or `recipe-*`), Gemini command totals can be higher than the git-tracked catalog totals.

The current shared skill folders also sync to the Gemini Antigravity global skill path:

- `C:\Users\LOQ\.gemini\antigravity\global_skills`

## Refresh Workflow

After changing, adding, or removing skills:

```powershell
python scripts/export-gemini-skill.py --all
```

Run that export after catalog-wide documentation refreshes too, not only after new skills or helper scripts land.

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
- `Anti-Patterns` and `Related Skills` sections
- `CHANGELOG.md` presence in every skill folder
- new changelog entries that use `Added`, `Changed`, and `Fixed` sections only; do not add a `### Tested` section
- Gemini command count
- TOML parseability of generated commands
- obsolete Skill Paths sections, stale removed-skill links, mojibake markers, and generated Python bytecode

Catalog policy also expects each `SKILL.md` to include `## Verification Protocol` immediately after `## Anti-Patterns`.
The tracked imports `docx`, `jupyter-notebook`, `pptx`, and `xlsx` now validate against the shared schema baseline. Their remaining gap is canonical upstream matching and finalized provenance metadata.

For externally imported skills, normalize the workspace copy and run any local smoke tests before exporting new Gemini command files. The generated command should only mirror maintained content that already passed the repo checks.

## Notes

- The Gemini command prompt tells Gemini to resolve relative paths against the source skill folder.
- MCP-aware skills still include no-MCP fallback guidance, so they remain usable even if Gemini CLI is running without the same MCP surface as another host.
