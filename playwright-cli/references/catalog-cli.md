# Playwright CLI Reference

The current package is `@playwright/cli`. Prefer the verified global binary
when it is present; the wrapper falls back to the same package through `npx`:

```bash
export CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
export PWCLI="$CODEX_HOME/skills/playwright-cli/scripts/playwright_cli.sh"
"$PWCLI" --help
```

User-scoped skills install under `$CODEX_HOME/skills` (default: `~/.codex/skills`).

Check the package before a run:

```bash
playwright-cli --version
playwright-cli --help
```

Optional convenience alias:

```bash
alias pwcli="$PWCLI"
```

## Core

```bash
pwcli open https://example.com
pwcli close
pwcli snapshot
pwcli click e3
pwcli dblclick e7
pwcli type "search terms"
pwcli press Enter
pwcli fill e5 "user@example.com"
pwcli drag e2 e8
pwcli hover e4
pwcli select e9 "option-value"
pwcli upload ./document.pdf
pwcli check e12
pwcli uncheck e12
pwcli eval "document.title"
pwcli eval "el => el.textContent" e5
pwcli dialog-accept
pwcli dialog-accept "confirmation text"
pwcli dialog-dismiss
pwcli resize 1920 1080
```

## Navigation

```bash
pwcli go-back
pwcli go-forward
pwcli reload
```

## Keyboard

```bash
pwcli press Enter
pwcli press ArrowDown
pwcli keydown Shift
pwcli keyup Shift
```

## Mouse

```bash
pwcli mousemove 150 300
pwcli mousedown
pwcli mousedown right
pwcli mouseup
pwcli mouseup right
pwcli mousewheel 0 100
```

## Save as

```bash
pwcli screenshot
pwcli screenshot e5
pwcli pdf
```

## Tabs

```bash
pwcli tab-list
pwcli tab-new
pwcli tab-new https://example.com/page
pwcli tab-close
pwcli tab-close 2
pwcli tab-select 0
```

## DevTools

```bash
pwcli console
pwcli console warning
pwcli requests
pwcli request 0
pwcli run-code "await page.waitForTimeout(1000)"
pwcli tracing-start
pwcli tracing-stop
```

`requests` is the current network-inspection command. Use `request-headers`,
`request-body`, `response-headers`, or `response-body` when the individual
request needs a narrower view. `network` is not a current command.

## Sessions

Use a named session to isolate work:

```bash
pwcli -s=todo open https://demo.playwright.dev/todomvc
pwcli -s=todo snapshot
```

Or set an environment variable once:

```bash
export PLAYWRIGHT_CLI_SESSION=todo
pwcli open https://demo.playwright.dev/todomvc
```

The wrapper maps `PLAYWRIGHT_CLI_SESSION` to the CLI's session option. Close
named sessions explicitly and use `pwcli close-all` or `pwcli kill-all` only
when the exact stale-session scope is understood.

## Network state and structured output

```bash
pwcli network-state-set offline
pwcli network-state-set online
pwcli --json list
pwcli --raw snapshot
```

Use `--raw` when another command or a file needs only the result value and
`--json` when a machine-readable response wrapper is required.

## Installation and browser runtime

Install the CLI globally only with explicit user authorization:

```bash
npm install -g @playwright/cli@latest
playwright-cli --version
```

The CLI can install its own agent skill into either supported global agent
home:

```bash
playwright-cli install --skills=agents --global
playwright-cli install --skills=claude --global
```

Browser binaries are a separate decision. Inspect the available options first
with `playwright-cli install-browser --help`; do not download a browser as a
side effect of merely installing or loading a skill.
