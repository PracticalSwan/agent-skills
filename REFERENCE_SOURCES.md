# Reference Sources

Reference catalogs used for discovery and selection during the 2026-04-04 workspace upgrades:

- `https://github.com/github/awesome-copilot`
- `https://awesome-copilot.github.com/skills`
- `https://github.com/travisvn/awesome-claude-skills`
- `https://github.com/ComposioHQ/awesome-codex-skills`
- `https://github.com/anthropics/skills`
- `https://github.com/conorbronsdon/avoid-ai-writing`
- `https://github.com/zarazhangrui/codebase-to-course`

## Source Commits

| Source | Commit |
|--------|--------|
| `awesome-copilot` | `63d08d51f792d53feec8c1c06897cee870e83c18` |
| `awesome-claude-skills` | `b05169af5448a3d8961aa0ed12c2934f94bfe52e` |
| `anthropics/skills` | `5128e1865d670f5d6c9cef000e6dfc4e951fb5b9` |
| `awesome-codex-skills` | `711ee69d724457093d52f685d729917f5389c686` |
| `avoid-ai-writing` | `cbf885e087e8ec1168bc58dc603606a6e4bfacbd` |
| `codebase-to-course` | `ff8837ecf8e9f6ce9874ffa42e42633394a52a00` |

## Installed Skills

| Skill | Source | Reason |
|-------|--------|--------|
| `avoid-ai-writing` | `https://github.com/conorbronsdon/avoid-ai-writing` | Portable writing cleanup skill for auditing and rewriting AI-generated phrasing. |
| `agentic-eval` | `awesome-copilot` | Reusable evaluator-optimizer and rubric workflows improve code, docs, and planning quality across many projects. |
| `cloud-design-patterns` | `awesome-copilot` | Distributed-system and cloud architecture trade-offs come up often enough to justify a portable shortlist skill. |
| `codebase-to-course` | `https://github.com/zarazhangrui/codebase-to-course` | Converts local or GitHub codebases into interactive course-style walkthroughs for onboarding and project understanding. |
| `context-map` | `awesome-copilot` | A dedicated pre-edit scoping skill is useful for safer multi-file changes and bug investigations across clients. |
| `csharp-xunit` | `awesome-copilot` | The workspace contains a top-level Visual Studio solution and .NET work. |
| `dotnet-best-practices` | `awesome-copilot` | The workspace contains a top-level Visual Studio solution and .NET work. |
| `java-docs` | `awesome-copilot` | The workspace contains multiple Java coursework directories. |
| `java-junit` | `awesome-copilot` | The workspace contains multiple Java coursework directories. |
| `mcp-builder` | `awesome-claude-skills` for discovery, canonical source `anthropics/skills` | MCP server creation is a durable cross-client workflow and the official Anthropic skill is stronger than the discovery index copy. |
| `pdf` | `awesome-claude-skills` -> official Anthropic `pdf` skill reference | The workspace contains many PDF course materials and deliverables. |
| `premium-frontend-ui` | `awesome-copilot` | The workspace contains React, Vite, Next.js, and Three.js frontends that benefit from stronger UI direction. |
| `secret-scanning` | `awesome-copilot` | Local pre-commit secret hygiene and GitHub alert workflows are broadly useful and safe to ship in a shared catalog. |
| `security-review` | `awesome-copilot` | The workspace contains multiple web apps and APIs that benefit from repeatable security review guidance. |
| `spreadsheet-formula-helper` | `awesome-codex-skills` | The workspace contains spreadsheet-heavy coursework and XLSX files. |

## Selection Notes

- The wider `C:\Assumption University` workspace was inventoried before adding skills.
- Installed skills were chosen to match real technologies found in that workspace, not just to maximize catalog size.
- Imported skills are installed into `C:\Users\LOQ\.copilot\skills` first because this repo is the canonical maintained source.
- Discovery lists are useful for finding candidates, but canonical upstream sources win when a discovery repo points to a stronger maintained original.
- Downstream skill folders such as `C:\Users\LOQ\.codex\skills`, `C:\Users\LOQ\.agents\skills`, `C:\Users\LOQ\.claude\skills`, and workspace-local skill roots are synced from this repo after import and review.
- Imported skills are modernized in this repo so they work as shared skills across GitHub Copilot, Claude Code, Codex, and Gemini CLI.
- MCP-aware skills are required to include a no-MCP fallback path before being treated as valid maintained skills.
- New helper scripts are smoke-tested locally before the repo-wide validation and sync pass.
- Unsafe, offensive, credential-heavy, or low-signal skills discovered during research are intentionally excluded from this maintained catalog.
- On 2026-04-24, source paths recorded in `scripts/skill-registry.json` were rechecked against current upstream heads. `premium-frontend-ui` received upstream author metadata, `mcp-builder` received the current upstream license notice, and unchanged audited paths had provenance bumped to the verified current source commit.
