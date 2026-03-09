# Next.js MCP Server Reference

Setup, capabilities, and usage patterns for `next-devtools-mcp` with Next.js 16+.

> Official guide: https://nextjs.org/docs/app/guides/mcp
> Package: https://www.npmjs.com/package/next-devtools-mcp
> Repository: https://github.com/vercel/next-devtools-mcp

---

## Requirements

- Next.js **16.0.0** or above
- A running development server (`npm run dev`)
- A coding agent that supports MCP (e.g. GitHub Copilot, Claude)

---

## Setup

### 1. Add `.mcp.json` to Project Root

```json
{
  "mcpServers": {
    "next-devtools": {
      "command": "npx",
      "args": ["-y", "next-devtools-mcp@latest"]
    }
  }
}
```

### 2. Start the Dev Server

```bash
npm run dev
# or
pnpm dev
```

`next-devtools-mcp` automatically discovers all running Next.js 16+ instances on your machine and connects to them via the built-in `/_next/mcp` endpoint.

### 3. Agent Auto-Discovery

Once your agent loads the `.mcp.json` config, it connects automatically. No additional setup needed.

---

## How It Works

Next.js 16+ includes a built-in MCP endpoint at `/_next/mcp` inside the development server. This endpoint exposes runtime state, errors, and project metadata over the Model Context Protocol.

`next-devtools-mcp` acts as a *proxy* that:
- Discovers all running Next.js instances (scanning local ports)
- Forwards tool calls to the appropriate dev server
- Returns structured results to the agent

This means agents work seamlessly with multi-app setups (e.g., monorepos with multiple ports).

---

## Available Tools

### `get_errors`
Retrieve current errors from the running development server.

**Returns:**
- Build errors (TypeScript, ESLint, module resolution)
- Runtime errors (unhandled exceptions)
- Type errors from the TypeScript language server

**Use when:** App shows an error overlay, build fails, or you need to check the current error state.

---

### `get_logs`
Get the path to the development log file.

**Returns:** File path containing:
- Browser console logs (errors, warnings, info)
- Server-side console output
- HMR events

**Use when:** Debugging rendering behavior, tracing data flow, finding silent failures.

---

### `get_page_metadata`
Get detailed metadata about a specific page in the application.

**Parameters:** `route` (string) — e.g. `/dashboard`, `/blog/[slug]`

**Returns:**
- Rendering type (static, dynamic, ISR)
- Component tree (Server Components, Client Components)
- Route segment config (`dynamic`, `revalidate`, `runtime`)
- Applied layouts and templates

**Use when:** Diagnosing unexpected static/dynamic rendering, understanding component boundaries.

---

### `get_project_metadata`
Retrieve high-level project information.

**Returns:**
- Next.js version and `next.config` options
- Dev server URL and running port
- Directory structure overview
- All registered routes and their types

**Use when:** Starting work in an unfamiliar project, checking config before suggesting patterns.

---

### `get_server_action_by_id`
Look up a Server Action by its Next.js-generated ID.

**Parameters:** `id` (string) — the opaque action ID from client-side code

**Returns:**
- Source file path
- Function name
- Module location

**Use when:** Tracing Server Action calls in client components, debugging action routing.

---

### `nextjs_docs` (Knowledge Base Query)
Query the comprehensive Next.js documentation and best practices knowledge base.

**Use when:**
- Answering "when should I use X?" questions about Next.js APIs
- Validating patterns against official guidance
- Getting context on specific APIs before generating code

---

### `nextjs_runtime`
Interact directly with the running Next.js instance.

**Use when:**
- Live state queries during development
- Checking current configuration and middleware
- Understanding the active routing state

---

### `upgrade_nextjs_16`
Automated guide and tooling for upgrading a project to Next.js 16.

**What it does:**
1. Analyzes current version and config
2. Runs applicable `@next/codemod` transforms
3. Identifies manual changes needed (breaking changes)
4. Guides through `next.config` renames and API changes

**Use when:** User asks to upgrade to v16, migrating from v14/v15.

---

### `enable_cache_components`
Setup and configuration assistance for the Cache Components feature (v16).

**What it does:**
- Enables `cacheComponents` in `next.config.ts`
- Explains `"use cache"`, `cacheTag()`, `cacheLife()` setup
- Configures `cacheHandlers` if needed
- Shows conversion patterns from old ISR/`fetch` approaches

**Use when:** User wants to adopt the `use cache` directive feature.

---

## Troubleshooting

### MCP Server Not Connecting

1. Ensure Next.js version is **16.0.0 or above**: `node -e "require('next/package.json').version"`
2. Verify `.mcp.json` is at the **project root** (same level as `package.json`)
3. Check that the dev server is **actively running**: `npm run dev`
4. **Restart the dev server** if it was already running when you added `.mcp.json`
5. Verify your coding agent has **loaded the MCP config** (check agent settings)

### Multiple Projects / Monorepo

`next-devtools-mcp` discovers all running Next.js instances automatically. Place the `.mcp.json` at each app's root if needed, or at the monorepo root to configure once.

### Older Next.js (v13/v14)

The built-in `/_next/mcp` endpoint does not exist below v16. You cannot use `next-devtools-mcp` with older versions. Use the [upgrade tool](#upgrade_nextjs_16) to migrate first.

---

## Example Prompts

```
# Debugging
"What errors are currently in my app?"
"Why is /products/[id] rendering statically?"
"Show me all Server Actions in the project"

# Understanding structure  
"What does the component tree look like for /checkout?"
"Which routes are dynamic vs static?"
"What's in my next.config.ts?"

# Upgrading & migration
"Help me upgrade this app from Next.js 14 to 16"
"Convert my getServerSideProps pages to App Router"
"Enable Cache Components in this project"

# Best practices
"When should I use 'use cache' vs ISR revalidate?"
"Should this component be a Server or Client Component?"
"How do I add OpenTelemetry to this Next.js 16 app?"
```
