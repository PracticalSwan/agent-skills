# Changelog

All notable changes to the `nextjs-development` skill will be documented in this file.

## [2026-04-24] - Current Version Refresh

### Changed
- Updated the active Next.js version guidance from 16.1.6 to 16.2.4 after checking the current npm package version.
- Removed the redundant standalone Skill Paths section; the generated portability section remains the authoritative cross-client path guidance.

### Tested
- Verified the latest published package version with `npm view next version`.

## [2026-04-04] - Gemini Path Clarification

### Changed
- Expanded the explicit global path example so it documents both the Codex global skill path and the current Gemini Antigravity global skill path.

## [2026-04-04] - Cross-Client Portability Refresh

### Changed
- Added a standard portability note covering GitHub Copilot, Claude Code, Codex, and Gemini CLI.
- Documented the preferred MCP server surface for this skill and a local no-MCP fallback workflow.

### Tested
- Validated `SKILL.md` frontmatter, portability sections, and Gemini export readiness with `python scripts/validate-skills.py`.
## [2026-03-10] — Initial Release

### Added

- Full Next.js 15/16 (v16.1.6) skill covering App Router, Server/Client Components, and routing
- `use cache` directive patterns with `cacheTag()`, `cacheLife()`, and named profiles
- Async Request APIs section (v15 breaking change): `await cookies()`, `await headers()`, `await params`, `await searchParams`
- Server Actions with `"use server"`, `<Form>` component, optimistic updates
- `after()` and `connection()` utility functions for post-response side effects and dynamic rendering
- Next.js MCP dev tools section (`next-devtools-mcp`) with `.mcp.json` setup and tool reference table
- Turbopack defaults, `turbopackFileSystemCache`, `serverComponentsHmrCache`
- React Compiler (`reactCompiler: true`) stable config
- Auth interrupts: `forbidden()`, `unauthorized()` with `forbidden.tsx`, `unauthorized.tsx` file conventions
- `instrumentation.ts` (stable) and `instrumentation-client.ts` (v16) usage patterns
- Middleware template with `matcher` config
- Metadata API: static and dynamic `generateMetadata`
- v15 upgrade breaking changes table and codemod commands
- `references/app-router-reference.md`: complete file conventions and routing patterns quick reference
- `references/nextjs-mcp-server.md`: detailed MCP devtools setup and troubleshooting
- `examples/data-fetching-patterns.md`: `use cache`, ISR, `fetch`, CSR patterns with TypeScript
- `examples/server-client-components.md`: RSC/RCC composition patterns and decision guide
- `scripts/page-generator.ps1`: PowerShell scaffold for App Router page, loading, error files
