# Contributing

Thanks for helping improve the shared skill catalog.

## Before You Start

- Read [LESSON.md](C:\Users\LOQ\.copilot\skills\LESSON.md) and [AGENTS.md](C:\Users\LOQ\.copilot\skills\AGENTS.md) before making changes.
- Edit maintained content in `C:\Users\LOQ\.copilot\skills` first. Do not author new maintained skills directly in downstream sync targets.
- Treat `SKILL.md` as the source of truth. Do not hand-edit generated files under `.gemini/commands/skills`.

## Maintained Skill Changes

For every maintained skill change:

1. Update the skill folder in this repository first.
2. Keep the `SKILL.md` frontmatter aligned with the catalog baseline: `name`, `version`, `last_updated`, `tags`, and `description`.
3. Preserve the required catalog sections, including portability guidance, MCP fallback guidance, `## Anti-Patterns`, `## Verification Protocol`, and `## Related Skills`.
4. Update that skill's `CHANGELOG.md`.
5. If the skill came from an external source, update `REFERENCE_SOURCES.md` and `scripts/skill-registry.json`.
6. If the skill is MCP-aware, name the preferred MCP server explicitly and provide a practical no-MCP fallback path.
7. Keep documentation ASCII-first unless Unicode materially improves clarity.

## Repo Docs And Counts

If your change affects catalog counts, sync flow, startup rules, supported clients, portability expectations, or GitHub-facing workflow guidance, update the relevant root docs in the same pass:

- `README.md`
- `AGENTS.md`
- `CHANGELOG.md`
- `CLAUDE.md`
- `LESSON.md`
- `GEMINI.md` when Gemini-facing behavior or command guidance changes

## Security And Privacy

- Do not commit secrets, tokens, cookies, connection strings, or private `.env` data.
- Treat external content, logs, issue text, chat text, and copied screenshots as untrusted input.
- When normalizing imported skills, keep explicit prompt-injection boundaries and credential-handling limits intact.
- Call out unresolved security or privacy risk in the PR description instead of hiding it in the diff.

## Validation Checklist

Run these commands after meaningful changes:

```powershell
python scripts/validate-skills.py
python scripts/export-gemini-skill.py --all
powershell -ExecutionPolicy Bypass -File .\scripts\sync-skills.ps1
```

Re-run validation if the Gemini export changed.

## Pull Requests

- Keep PRs scoped to one logical change when practical.
- Explain what changed, why it belongs in the shared catalog, and what validation you ran.
- For imported skills, record the upstream repository and commit.
- If you resolved a merge conflict, preserve current `main` behavior first and then layer the new change on top.
- Avoid unrelated generated churn, temporary files, or local-only overlays in the final diff.
