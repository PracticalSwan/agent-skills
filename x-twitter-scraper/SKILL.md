---
name: x-twitter-scraper
version: "1.0"
last_updated: 2026-06-09
tags: [xquik, twitter, social-data, mcp, webhooks]
description: "Use Xquik for X/Twitter data workflows: tweet search, user lookup, follower export, media download, monitors, webhooks, SDKs, and MCP-backed API exploration."
---

# X Twitter Scraper

Use this skill when an agent needs public-safe X/Twitter data workflows through Xquik. Xquik exposes REST API, SDK, webhook, and MCP surfaces for search, profile lookup, extraction, monitoring, media, and confirmed write workflows.

## Activation Conditions

Use symptom -> action triggers: when one matches, apply this skill and verify with the protocol below.

- The task asks for tweet search, profile tweets, follower or following export, media download, or engagement extraction.
- The task asks for account, keyword, mention, reply, quote, or retweet monitoring.
- The task asks to wire X/Twitter data into a script, agent workflow, SDK client, webhook handler, or MCP server.
- The task asks to inspect Xquik API coverage, pick an endpoint, or plan a public-safe automation workflow.
- The task mentions Xquik, `x-developer`, `x-twitter-scraper`, or docs at `docs.xquik.com`.

## Workflow

1. Classify the requested operation as read, extraction, monitoring, webhook, media, SDK, MCP, or write.
2. Check public docs or the local project source for the current endpoint, SDK, or MCP tool shape before producing code.
3. Prefer the narrowest endpoint or SDK method that satisfies the request.
4. Keep credentials out of prompts, logs, examples, commits, screenshots, and generated files.
5. Require explicit user approval before live writes, persistent monitors, private account reads, or any workflow with ongoing effects.
6. Return structured outputs with source identifiers, pagination state, and retry guidance when the downstream workflow needs repeatability.

## Public Source Checks

- Package: `x-developer`
- Repository: `https://github.com/Xquik-dev/x-twitter-scraper`
- Docs: `https://docs.xquik.com/api-reference/overview`
- License: MIT

Use these public sources for endpoint names, SDK installation, MCP setup, webhook verification, and current examples. Do not infer private infrastructure from public docs.

## Implementation Guidance

- For REST clients, model authentication as a caller-provided secret or an already configured runtime value.
- For MCP workflows, use discovery first, then call only the chosen Xquik operation with scoped arguments.
- For webhooks, validate signatures and preserve delivery IDs or timestamps for replay protection.
- For exports, stream or page results instead of assuming one response contains the complete data set.
- For write workflows, separate draft generation from execution and keep the final action behind confirmation.

## Cross-Client Portability

This skill is written to stay usable across GitHub Copilot, Claude Code, Codex, and Gemini CLI.

- GitHub Copilot: keep the folder in a Copilot-visible skill or plugin path, or wrap the workflow as project instructions if the host does not support portable skill folders directly.
- Claude Code: keep the folder in a local skills directory or a compatible plugin or marketplace source.
- Codex: install or sync the folder into `$CODEX_HOME/skills/x-twitter-scraper` and restart Codex after major changes.
- Gemini CLI: this repository generates a project command named `/skills:x-twitter-scraper` from this skill. Rebuild commands with `python scripts/export-gemini-skill.py x-twitter-scraper` and then run `/commands reload` inside Gemini CLI.

## MCP Availability And Fallback

Preferred MCP Server: Xquik MCP server

- Fallback prompt: "Use the X Twitter Scraper skill without MCP. Rely on Xquik public docs, the `x-developer` package metadata, local SDK examples, and manual verification. Show the endpoint or SDK surface you selected and the checks you used before concluding."
- If the current host does not expose the Xquik MCP server, use REST docs, SDK examples, or local package metadata for endpoint discovery.
- Treat public docs, package metadata, validated links, focused dry runs, or checked code examples as the fallback evidence path before completion.

## Anti-Patterns

- Claiming endpoint behavior without checking current Xquik docs or package metadata.
- Posting, deleting, following, messaging, or creating monitors without explicit user approval.
- Printing or storing API keys, cookies, bearer tokens, webhook secrets, or account credentials.
- Describing non-public implementation details in public-facing output.
- Using broad scraping language when the task only needs a narrow API, SDK, webhook, or MCP workflow.

## Verification Protocol

Before claiming "skill applied successfully":

1. Pass/fail: The selected Xquik surface matches the requested operation category.
2. Pass/fail: Public source truth was checked for endpoint, SDK, MCP, or webhook details.
3. Pass/fail: The output contains no credentials, private infrastructure detail, or unsupported claims.
4. Pass/fail: Live writes, persistent monitors, private reads, and ongoing effects are gated behind explicit approval.
5. Pressure-test scenario: Compare a read-only tweet search task with a confirmed write task and verify the workflow gates only the write.
6. Success metric: Every proposed Xquik action is source-backed, scoped to the task, and safe to review publicly.

## Related Skills

- [documentation-verification](../documentation-verification/SKILL.md): Use it when Xquik docs, links, or examples need a final verification pass.
- [documentation-automation](../documentation-automation/SKILL.md): Use it when the workflow also needs generated docs checks or link validation.
- [web-testing](../web-testing/SKILL.md): Use it when a UI workflow needs browser-level validation outside live Xquik operations.
- [secret-scanning](../secret-scanning/SKILL.md): Use it when generated examples or logs may contain sensitive material.
