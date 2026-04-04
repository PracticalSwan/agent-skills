# Reference Sources

Reference catalogs used for discovery and selection during the 2026-04-04 workspace upgrade:

- `https://github.com/github/awesome-copilot`
- `https://awesome-copilot.github.com/skills`
- `https://github.com/travisvn/awesome-claude-skills`
- `https://github.com/ComposioHQ/awesome-codex-skills`

## Source Commits

| Source | Commit |
|--------|--------|
| `awesome-copilot` | `0c3c5bbbfb2a7d57d36473a83fdbef1becc5053f` |
| `awesome-claude-skills` | `b05169af5448a3d8961aa0ed12c2934f94bfe52e` |
| `awesome-codex-skills` | `ccf6204f6a594fde4bf9e29119f5bdad7935a793` |

## Installed Skills

| Skill | Source | Reason |
|-------|--------|--------|
| `csharp-xunit` | `awesome-copilot` | The workspace contains a top-level Visual Studio solution and .NET work. |
| `dotnet-best-practices` | `awesome-copilot` | The workspace contains a top-level Visual Studio solution and .NET work. |
| `java-docs` | `awesome-copilot` | The workspace contains multiple Java coursework directories. |
| `java-junit` | `awesome-copilot` | The workspace contains multiple Java coursework directories. |
| `pdf` | `awesome-claude-skills` -> official Anthropic `pdf` skill reference | The workspace contains many PDF course materials and deliverables. |
| `premium-frontend-ui` | `awesome-copilot` | The workspace contains React, Vite, Next.js, and Three.js frontends that benefit from stronger UI direction. |
| `security-review` | `awesome-copilot` | The workspace contains multiple web apps and APIs that benefit from repeatable security review guidance. |
| `spreadsheet-formula-helper` | `awesome-codex-skills` | The workspace contains spreadsheet-heavy coursework and XLSX files. |

## Selection Notes

- The wider `C:\Assumption University` workspace was inventoried before adding skills.
- Installed skills were chosen to match real technologies found in that workspace, not just to maximize catalog size.
- Imported skills were then modernized in this repo so they work as shared skills across GitHub Copilot, Claude Code, Codex, and Gemini CLI.
- MCP-aware skills were required to include a no-MCP fallback path before being treated as valid maintained skills.
