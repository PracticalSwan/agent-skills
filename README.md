# Agent Skills

A cross-client catalog of reusable agent workflows for GitHub Copilot, Claude
Code, and Codex. Each skill is a focused `SKILL.md` with supporting references,
examples, or scripts where they improve the workflow.

## Browse the catalog

- [Skill catalog](docs/SKILL_CATALOG.md): searchable, alphabetized index with
  short descriptions.
- [Source and revision index](REFERENCE_SOURCES.md): upstream repositories,
  revisions, and mapped skill paths.
- [Security policy](SECURITY.md): reporting and safe handling expectations.

The active catalog currently contains **251 skills**: 219 maintained skills
and 32 copied official Superpowers workflows. Machine-local overlays are not
part of this public inventory. The generated index includes tracked and
non-ignored catalog folders so a reviewed new import appears before commit.

## Use a skill

1. Find the closest match in the [catalog](docs/SKILL_CATALOG.md).
2. Read the complete `SKILL.md` and any references it points to.
3. Confirm required tools, credentials, and client capabilities are available.
4. Follow the stated fallback and verification steps when a preferred tool is
   unavailable.

Skills are guidance for agent workflows. They do not install their own tools,
grant permissions, or prove that a connected service call succeeded.

## Contribute

Edit maintained skills in this repository, keep source and licensing details
accurate, validate the catalog, then sync only to approved user-global skill
roots. For a substantial completed change, inspect the scoped diff, then commit
and push it to the configured GitHub remote after checks pass. The full workflow
and safety boundaries are in
[CONTRIBUTING.md](CONTRIBUTING.md) and [AGENTS.md](AGENTS.md).

```powershell
py -3 scripts/validate-skills.py
py -3 scripts/build-skill-catalog.py
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\sync-skills.ps1
```

The sync script enforces the three user-global destinations and preserves
host-managed or unknown personal skills. Do not use it to deploy into a
project-specific skill directory.

## Documentation

- [Contributor workflow](CONTRIBUTING.md)
- [Agent instructions](AGENTS.md)
- [Claude Code notes](CLAUDE.md)
- [Migration notes](MIGRATION.md)
- [Maintenance lessons](LESSON.md)
- [Change history](CHANGELOG.md)
- [Source provenance](REFERENCE_SOURCES.md)
