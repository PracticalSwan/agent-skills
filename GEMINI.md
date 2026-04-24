# GEMINI.md

This repository exposes its skills to Gemini CLI through generated project commands.

## Source of Truth

- Edit skill content in `SKILL.md` files under `C:\Users\LOQ\.copilot\skills`
- Do not hand-edit files under `.gemini/commands/skills`
- The current git-tracked catalog baseline is `version: "1.1"` with `last_updated: 2026-04-24` across all `67` tracked skill folders

## Generated Commands

Each skill is exported as a Gemini CLI command:

- `/skills:<skill-name>`

Examples:

- `/skills:java-junit`
- `/skills:pdf`
- `/skills:security-review`

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
- changelog entries that use `Added`, `Changed`, and `Fixed` sections only; do not add a `### Tested` section
- Gemini command count
- TOML parseability of generated commands
- obsolete Skill Paths sections, stale removed-skill links, mojibake markers, and generated Python bytecode

For externally imported skills, normalize the workspace copy and run any local smoke tests before exporting new Gemini command files. The generated command should only mirror maintained content that already passed the repo checks.

## Notes

- The Gemini command prompt tells Gemini to resolve relative paths against the source skill folder.
- MCP-aware skills still include no-MCP fallback guidance, so they remain usable even if Gemini CLI is running without the same MCP surface as another host.
