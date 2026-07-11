---
name: nemo-retriever
version: "1.3"
last_updated: 2026-07-11
tags: [nvidia, nemo, retriever, rag, indexing, qa]
description: "NVIDIA NeMo Retriever deployment and usage guidance for local retrieval services, corpus ingestion, and grounded question-answering workflows."
license: "CC-BY-4.0 AND Apache-2.0"
compatibility: "Guidance imported from the NVIDIA NeMo Retriever skill for local retriever deployment and corpus-backed QA workflows."
---
# nemo-retriever

The `retriever` CLI indexes a folder of PDFs into LanceDB (`retriever ingest`) and serves vector search over it (`retriever query`). For any task about searching/answering questions across a folder of PDFs, use this CLI — do not write a custom RAG.

**Beyond PDFs and beyond semantic search.** `retriever ingest` also handles images, Office, HTML, TXT, audio, and video — see `references/setup.md` for the per-format recipe and `references/install.md` for the install extras (`[multimedia]`, libreoffice, ffmpeg). For non-semantic operations — page filter, verbatim quote with citation, corpus-level aggregate, chart/image caption hits — see `references/query.md`. Don't fall back to native Read/Grep/Python on non-PDF inputs.

## Install (if `retriever` is missing)

If `command -v retriever` returns nothing, follow `references/install.md` to install the NeMo Retriever Library before proceeding. It prints `RETRIEVER_VENV=<path>`; substitute that path for `<RETRIEVER_VENV>` in every example in this skill (setup, query, troubleshooting, and the CLI references).

## Workflow — read the reference for the current phase, then execute

| Turn type | Read this once | Then execute |
| :--- | :--- | :--- |
| **Setup turn** (first turn — `./lancedb/nv-ingest.lance` doesn't exist) | `references/setup.md` | Build the index |
| **Query turn** (every subsequent turn — user asks a question) | `references/query.md` | One `retriever query` call |
| Anything errored or returned empty | `references/troubleshooting.md` | Apply the named recovery; do not improvise |

For the full `retriever ingest` / `retriever query` CLI specs, see `references/cli/ingest.md` and `references/cli/query.md`. You do not need these for routine turns — `<RETRIEVER_VENV>/bin/retriever <subcommand> --help` is faster.

Before ingesting a mixed folder, inventory extensions (`find <dir> -name '*.*' | sed 's/.*\.//' | sort -u`) — `--input-type=auto` silently drops anything outside the supported set. See `references/troubleshooting.md` "Unsupported file types".

## Hard limits (apply to every turn)

- **Setup turn**: build the index in one shell command (see `references/setup.md`). STOP after the index lands.
- **Query turn**: at most **2 Bash calls** — 1 `retriever query`, +1 optional targeted text-extract per `references/query.md`. Reply and then STOP.
- **No narration between tool calls.** Tokens you emit between calls become input + cached input for every later turn — quadratic cost. Go straight from reading the summary to writing the JSON file.
- **Banned**: `TodoWrite`, Glob, Grep, `Read` of whole PDFs, re-running setup, spawning subagents, speculative "confirmation" calls.

Long query turns (5+ tool calls, 1M+ cache-read tokens) cost ~5× a disciplined turn and almost always still produce the wrong answer. **Answering partially beats timing out.**

## Anti-Patterns

- Indexing content before clarifying corpus boundaries, freshness, or ownership: Retrieval quality collapses when the source of truth is unstable.
- Treating embedding, chunking, and backend choices as invisible defaults: They change recall, latency, and storage cost in user-visible ways.
- Claiming grounded answers without checking the retrieved passages that supported them.

## Verification Protocol

Before claiming "skill applied successfully":

1. Pass/fail: The workflow names the corpus, index or backend choice, and the query path before answering deployment or QA questions.
2. Pass/fail: Retrieval checks include at least one real query and inspection of the supporting passages or scores.
3. Pass/fail: Ingestion or indexing advice keeps corpus freshness and reindex cost visible instead of implicit.
4. Pressure-test scenario: Apply the workflow to a retriever that answers quickly but returns stale passages after a corpus update.
5. Success metric: The user gets a reproducible retriever setup or debugging path with live retrieval evidence.

<!-- PORTABILITY:START -->

## Cross-Client Portability

This skill is written to stay usable across GitHub Copilot, Claude Code, Codex, and Gemini CLI.

- GitHub Copilot: keep the folder in a Copilot-visible skill or plugin path, or wrap the workflow as project instructions if the host does not support portable skill folders directly.
- Claude Code: keep the folder in a local skills directory or a compatible plugin or marketplace source.
- Codex: install or sync the folder into `$CODEX_HOME/skills/<skill-name>` and restart Codex after major changes.
- Gemini CLI: this repository generates a project command named `/skills:nemo-retriever` from this skill. Rebuild commands with `python scripts/export-gemini-skill.py nemo-retriever` and then run `/commands reload` inside Gemini CLI.

<!-- PORTABILITY:END -->

<!-- MCP:START -->
## MCP Availability And Fallback

Preferred MCP Server: None required

- Fallback prompt: "Use the nemo-retriever skill without MCP. Rely on the local `SKILL.md`, bundled references or scripts, and manual verification. Show the exact commands, evidence, and final checks you used before concluding."
- If the current host does not expose a matching server, use the bundled references, scripts, native toolchain, and manual workflow already described in this skill.
- Treat direct local verification, rendered output, logs, tests, or screenshots as the fallback evidence path before completion.

<!-- MCP:END -->

## Related Skills

- [notebooklm-management](../notebooklm-management/SKILL.md): Use it when retrieval-backed research needs a notebook-style grounding workflow.
- [development-workflow](../development-workflow/SKILL.md): Use it when the retriever work also needs scoped implementation and validation checkpoints.
- [cloud-design-patterns](../cloud-design-patterns/SKILL.md): Use it when the retriever deployment choice also needs storage, scaling, or service-boundary analysis.
