# GEMINI.md

This repository exposes its skills to Gemini CLI through generated project commands.

## Source of Truth

- Edit skill content in `SKILL.md` files under `C:\Users\LOQ\.copilot\skills`
- Do not hand-edit files under `.gemini/commands/skills`

## Generated Commands

Each skill is exported as a Gemini CLI command:

- `/skills:<skill-name>`

Examples:

- `/skills:java-junit`
- `/skills:pdf`
- `/skills:security-review`

Generated command files live in:

- `C:\Users\LOQ\.copilot\skills\.gemini\commands\skills`

The current shared skill folders also sync to the Gemini Antigravity global skill path:

- `C:\Users\LOQ\.gemini\antigravity\global_skills`

## Refresh Workflow

After changing, adding, or removing skills:

```powershell
python scripts/export-gemini-skill.py --all
```

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

- `SKILL.md` frontmatter
- required portability and MCP sections
- Gemini command count
- TOML parseability of generated commands

For externally imported skills, normalize the workspace copy and run any local smoke tests before exporting new Gemini command files. The generated command should only mirror maintained content that already passed the repo checks.

## Notes

- The Gemini command prompt tells Gemini to resolve relative paths against the source skill folder.
- MCP-aware skills still include no-MCP fallback guidance, so they remain usable even if Gemini CLI is running without the same MCP surface as another host.
