---
name: tavily-research
version: "2.0"
last_updated: 2026-08-14
tags: [tavily, research, citations, synthesis, cli]
description: "Run Tavily's multi-source research workflow for comparisons, market analysis, literature-oriented exploration, or detailed cited reports. Use only when bounded search and extraction are insufficient."
license: "MIT"
compatibility: "Requires the official Tavily CLI and authenticated Tavily access, or an active Tavily research surface; research jobs may consume additional time and API credits."
---
# tavily research

AI-powered deep research that gathers sources, analyzes them, and produces a cited report. Takes 30-120 seconds.

## Before running any command

Check `tvly --version` and `tvly --status` first. If the CLI is missing, use a
reviewed installation method:

```bash
uv tool install tavily-cli
# or: python -m pip install --user tavily-cli
```

Authenticate with `tvly login` or an approved environment secret. Never expose
a real API key in commands, logs, files, or chat.

See [tavily-cli](../tavily-cli/SKILL.md) for alternative install methods and auth options.

## When to use

- You need comprehensive, multi-source analysis
- The user wants a comparison, market report, or literature review
- Quick searches aren't enough — you need synthesis with citations
- Step 5 in the [workflow](../tavily-cli/SKILL.md): search → extract → map → crawl → **research**

## Quick start

```bash
# Basic research (waits for completion)
tvly research "competitive landscape of AI code assistants"

# Pro model for comprehensive analysis
tvly research "electric vehicle market analysis" --model pro

# Stream results in real-time
tvly research "AI agent frameworks comparison" --stream

# Save report to file
tvly research "fintech trends 2025" --model pro -o fintech-report.md

# JSON output for agents
tvly research "quantum computing breakthroughs" --json
```

## Options

| Option | Description |
|--------|-------------|
| `--model` | `mini`, `pro`, or `auto` (default) |
| `--stream` | Stream results in real-time |
| `--no-wait` | Return request_id immediately (async) |
| `--output-schema` | Path to JSON schema for structured output |
| `--citation-format` | `numbered`, `mla`, `apa`, `chicago` |
| `--poll-interval` | Seconds between checks (default: 10) |
| `--timeout` | Max wait seconds (default: 600) |
| `-o, --output` | Save output to file |
| `--json` | Structured JSON output |

## Model selection

| Model | Use for | Speed |
|-------|---------|-------|
| `mini` | Single-topic, targeted research | ~30s |
| `pro` | Comprehensive multi-angle analysis | ~60-120s |
| `auto` | API chooses based on complexity | Varies |

**Rule of thumb:** "What does X do?" → mini. "X vs Y vs Z" or "best way to..." → pro.

## Async workflow

For long-running research, you can start and poll separately:

```bash
# Start without waiting
tvly research "topic" --no-wait --json    # returns request_id

# Check status
tvly research status <request_id> --json

# Wait for completion
tvly research poll <request_id> --json -o result.json
```

## Tips

- **Research takes 30-120 seconds** — use `--stream` to see progress in real-time.
- **Use `--model pro`** for complex comparisons or multi-faceted topics.
- **Use `--output-schema`** to get structured JSON output matching a custom schema.
- **For quick facts**, use `tvly search` instead — research is for deep synthesis.
- Read from stdin: `echo "query" | tvly research - --json`

## See also

- [tavily-search](../tavily-search/SKILL.md) — quick web search for simple lookups
- [tavily-crawl](../tavily-crawl/SKILL.md) — bulk extract from a site for your own analysis

## Anti-Patterns

- Starting a long or higher-cost research job for a fact that bounded search can answer.
- Using an underspecified topic that invites uncontrolled scope or irrelevant synthesis.
- Treating the generated report as authoritative without checking its cited sources.
- Claiming completion from a request identifier before the job reaches a terminal success state.

## Verification Protocol

Before claiming Tavily research succeeded:

1. Pass/fail: The research question, scope, model, citation format, and output destination are explicit.
2. Pass/fail: The user-requested depth justifies research rather than search or extraction.
3. Pass/fail: The job reaches a completed state and the final output is preserved when requested.
4. Pass/fail: Material claims and citations are spot-checked against the linked sources.
5. Pressure test: Handle timeout, failed status, contradictory sources, or incomplete citations without fabricating a conclusion.
6. Success metric: Report job state, selected model, saved artifact if any, checked sources, and remaining uncertainty.

<!-- MCP:START -->

<!-- PORTABILITY:START -->

## Cross-Client Portability

This skill is written to stay usable across GitHub Copilot, Claude Code, and Codex.

- GitHub Copilot: keep the folder in a Copilot-visible skill path or wrap the
  workflow in project instructions when folder discovery is unavailable.
- Claude Code: keep the folder in a local skills directory or a compatible plugin source.
- Codex: install or sync the folder into
  `$CODEX_HOME/skills/tavily-research` and restart Codex after major changes.

<!-- PORTABILITY:END -->

## MCP Availability And Fallback

Preferred MCP Server: Tavily MCP Server

- Fallback prompt: "Use the Tavily Research skill without MCP. Run a scoped `tvly research` job, poll it to a terminal state, keep secrets out of output, verify important citations, and report the job and artifact evidence."
- If the MCP server does not expose research, use the official CLI or SDK. If no authenticated surface exists, report the blocker.
- Do not claim completion from a non-terminal request identifier.

<!-- MCP:END -->

## Related Skills

- [tavily-search](../tavily-search/SKILL.md): Answer smaller current-information questions before escalating.
- [tavily-dynamic-search](../tavily-dynamic-search/SKILL.md): Perform agent-controlled multi-step source triage and extraction.
- [documentation-verification](../documentation-verification/SKILL.md): Check report citations and source links.
