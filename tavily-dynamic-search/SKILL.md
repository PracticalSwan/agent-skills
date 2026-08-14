---
name: tavily-dynamic-search
version: "2.0"
last_updated: 2026-08-14
tags: [tavily, programmatic-search, context-isolation, python, research]
description: "Run programmatic Tavily search and extraction while filtering raw results outside the main agent context. Use for multi-step or high-volume research where titles, snippets, and selected passages should be curated before synthesis."
license: "MIT"
compatibility: "Requires the official Tavily CLI, authenticated Tavily access, and Python or jq for local filtering; shell examples must be adapted to the active platform."
---
# Tavily Dynamic Search

Search the web, filter results, and extract content so that **raw search data never enters your context window**. Only your curated `print()` output comes back.

## Why this matters

A typical `tvly search --include-raw-content` returns 8 results × 30-50K chars each = **~300K characters** of raw page content. If this enters your context window, you burn tokens reading navigation bars, cookie banners, and boilerplate — and your reasoning quality degrades under the noise. By processing results inside a Python script, only your `print()` output enters context — typically **1-3K characters** of pure signal. That's a 100-200x reduction.

## Background: Programmatic Tool Calling (PTC)

This skill replicates the architecture of [Anthropic's Programmatic Tool Calling](https://platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling) (PTC) for web search. PTC lets the model write code that orchestrates tool calls inside a sandbox — intermediate results stay in the sandbox, and only the final `print()` output reaches the model's context window.

**This skill applies the same principle using local Python execution.** The Python process is the sandbox. Variables in memory hold the raw data. Only what you `print()` crosses into your context window. You write the filtering logic — you decide what matters for each query.

## Before running any command

Check `tvly --version` and `tvly --status` first. If the CLI is missing, use a
reviewed installation method:

```bash
uv tool install tavily-cli
# or: python -m pip install --user tavily-cli
```

Authenticate with `tvly login` or an approved environment secret. Never expose
a real API key in commands, logs, files, or chat.

## Core Rule

**NEVER** run `tvly` as a bare command. Always process output through Python so you control what enters your context.

```bash
# WRONG — raw results flood your context
tvly search "quantum computing 2025" --json

# RIGHT — only your print() output enters context
tvly search "quantum computing 2025" --json 2>/dev/null | python3 -c "
import json, sys
data = json.load(sys.stdin)
for r in data['results']:
    print(f'[{r[\"score\"]:.2f}] {r[\"title\"]}')
    print(f'  {r[\"url\"]}')
"
```

## JSON Schemas

You need these to write correct filtering code.

### tvly search --json

```json
{
  "query": "string",
  "answer": "string | null",
  "results": [
    {
      "url": "string",
      "title": "string",
      "content": "string (snippet, ~500-1500 chars)",
      "score": 0.0-1.0,
      "raw_content": "string | null (full page, only with --include-raw-content)"
    }
  ],
  "response_time": 0.0
}
```

### tvly extract --json

```json
{
  "results": [
    {
      "url": "string",
      "title": "string",
      "raw_content": "string (full page markdown)",
      "images": []
    }
  ],
  "failed_results": [],
  "response_time": 0.0
}
```

## How to search

You have two building blocks and two ways to run them. Compose these however the query demands — there are no fixed patterns. You decide the approach based on what you need.

### Building blocks

**`tvly search`** — returns titles, URLs, snippets, scores. Optionally includes full page content with `--include-raw-content markdown`.

**`tvly extract`** — fetches full page content for specific URLs. Use when you found a URL from search and need more detail.

### Execution modes

**Pipe mode** — for simple filters (3-5 lines). Pipe tvly output into `python3 -c`:

```bash
tvly search "query" --json 2>/dev/null | python3 -c "
import json, sys
data = json.load(sys.stdin)
# your filtering code here
"
```

**Heredoc mode** — for anything more complex. Single Bash call, clean multi-line Python, no escaping, no temp files:

```bash
python3 << 'PYEOF'
import json, subprocess
raw = subprocess.check_output(
    ['tvly', 'search', 'query', '--json'],
    stderr=subprocess.DEVNULL
)
data = json.loads(raw)
for r in data['results']:
    print(f"[{r['score']:.2f}] {r['title']}")
    print(f"  {r['url']}")
PYEOF
```

Single-quoted heredocs (`<< 'PYEOF'`) don't interpret anything — no escaping needed. This is the default for most tasks.

**Script mode** — only when you will reuse the same script across multiple turns. Do NOT write one-shot scripts to `/tmp/`. If you run it once, use a heredoc.

**Important: save DATA to `/tmp/`, not CODE.** Writing `/tmp/tavily_results.json` (data for later turns) = good. Writing `/tmp/my_filter.py` (one-shot code) = wasteful — use a heredoc instead.

## Multi-turn iteration

For complex queries, you often need to **explore before you extract** — just like PTC, where the model searches, sees titles, decides which results to drill into, then extracts.

The key: **save raw results to a file, then process them in separate steps.** The file is your persistent state between turns.

### Turn 1: Search and explore

Search and print only titles + scores. Save raw results to disk for later turns:

```bash
python3 << 'PYEOF'
import json, subprocess

raw = subprocess.check_output(
    ['tvly', 'search', 'solid-state battery commercialization 2025',
     '--include-raw-content', 'markdown', '--max-results', '8', '--json'],
    stderr=subprocess.DEVNULL
)
data = json.loads(raw)

# Save raw results — this stays on disk, never enters context
with open('/tmp/tavily_results.json', 'w') as f:
    json.dump(data, f)

# Print only what you need to decide next steps
print(f'{len(data["results"])} results saved to /tmp/tavily_results.json\n')
for i, r in enumerate(data['results']):
    print(f'[{i}] [{r["score"]:.2f}] {r["title"][:90]}')
    print(f'    {r["url"]}')
    print(f'    {r["content"][:150]}')
    print()
PYEOF
```

Context receives: ~800 tokens of titles + snippets. The 300K of raw page content is in `/tmp/tavily_results.json`, untouched.

### Turn 2: Extract based on what you saw

Now you know what's in the results. Write targeted extraction — **you decide** which results to drill into and what to filter for:

```bash
python3 << 'PYEOF'
import json

data = json.load(open('/tmp/tavily_results.json'))

# You chose these indices based on the titles you saw in turn 1
for i in [0, 2, 5]:
    r = data['results'][i]
    raw = r.get('raw_content', '') or ''
    if not raw:
        continue

    print(f'## {r["title"]}')
    print(f'URL: {r["url"]}\n')

    # You write the filtering logic based on the query
    # This example extracts paragraphs about specific companies
    for para in raw.split('\n\n'):
        para = para.strip()
        if len(para) > 80 and any(kw in para.lower() for kw in
                ['toyota', 'quantumscape', 'samsung', 'commercializ', 'production']):
            print(para)
            print()

    print('---\n')
PYEOF
```

Context receives: ~600 tokens of targeted content. You made the decision about what to keep.

### Turn 3 (optional): Fetch more detail

If you need more from a specific source:

```bash
python3 << 'PYEOF'
import json, subprocess

# Fetch a specific URL you identified
raw = subprocess.check_output(
    ['tvly', 'extract', 'https://example.com/article', '--json'],
    stderr=subprocess.DEVNULL
)
data = json.loads(raw)
page = data['results'][0]
content = page.get('raw_content', '')

# Save for potential further processing
with open('/tmp/page_detail.txt', 'w') as f:
    f.write(content)

# Print only the section you care about
for line in content.split('\n'):
    if any(kw in line.lower() for kw in ['timeline', '2025', '2026', 'mass production']):
        print(line.strip())
PYEOF
```

### When to use multi-turn vs single-turn

**Single turn** (pipe mode or one script): when you know upfront what you're looking for. Specific factual queries, known keywords.

**Multi-turn** (save + explore + extract): when you need to see what's available before deciding what to extract. Open-ended research, complex topics, queries where you don't know the right keywords yet.

## Examples

### Simple factual lookup (single turn, pipe mode)

```bash
tvly search "Python 3.13 release date" --max-results 5 --json 2>/dev/null | python3 -c "
import json, sys
data = json.load(sys.stdin)
for r in data['results'][:3]:
    print(f'{r[\"title\"]}')
    print(f'{r[\"content\"][:300]}')
    print()
"
```

### Financial data extraction (single turn, heredoc)

```bash
python3 << 'PYEOF'
import json, subprocess

raw = subprocess.check_output(
    ['tvly', 'search', 'NVIDIA Q4 2025 earnings revenue',
     '--include-raw-content', 'markdown', '--max-results', '5',
     '--json'],
    stderr=subprocess.DEVNULL
)
data = json.loads(raw)

for r in data['results']:
    raw_content = r.get('raw_content', '') or ''
    # For financial queries, look for lines with numbers
    financial_lines = [
        line.strip() for line in raw_content.split('\n')
        if any(kw in line.lower() for kw in
               ['revenue', 'eps', 'earnings', 'margin', 'guidance', 'billion'])
        and any(c.isdigit() for c in line)
        and len(line.strip()) > 30
    ]
    if financial_lines:
        print(f'## {r["title"]}')
        print(f'URL: {r["url"]}')
        for line in financial_lines[:15]:
            print(f'  {line}')
        print()
PYEOF
```

### Multi-source research (multi-turn)

**Turn 1** — broad search + triage:

```bash
python3 << 'PYEOF'
import json, subprocess

# Search from multiple angles
queries = [
    ('broad', 'EU AI Act implementation timeline 2025'),
    ('specific', 'EU AI Act high-risk AI systems obligations'),
]

all_results = []
for label, query in queries:
    raw = subprocess.check_output(
        ['tvly', 'search', query, '--max-results', '8', '--json'],
        stderr=subprocess.DEVNULL
    )
    data = json.loads(raw)
    for r in data['results']:
        r['_query'] = label
    all_results.extend(data['results'])

# Deduplicate by URL
seen = set()
unique = []
for r in all_results:
    if r['url'] not in seen:
        seen.add(r['url'])
        unique.append(r)

# Save all results
with open('/tmp/eu_ai_results.json', 'w') as f:
    json.dump(unique, f)

# Print triage
unique.sort(key=lambda r: r['score'], reverse=True)
print(f'{len(unique)} unique results from {len(queries)} queries\n')
for i, r in enumerate(unique[:10]):
    print(f'[{i}] [{r["score"]:.2f}] ({r["_query"]}) {r["title"][:80]}')
    print(f'    {r["url"]}')
    print(f'    {r["content"][:120]}')
    print()
PYEOF
```

**Turn 2** — you see the triage, pick the best sources, and extract:

```bash
python3 << 'PYEOF'
import json, subprocess

results = json.load(open('/tmp/eu_ai_results.json'))

# Fetch full content for the top 3 (you chose these based on turn 1)
for r in [results[0], results[2], results[4]]:
    try:
        raw = subprocess.check_output(
            ['tvly', 'extract', r['url'], '--json'],
            stderr=subprocess.DEVNULL, timeout=30
        )
        page = json.loads(raw)
        if not page.get('results'):
            continue
        content = page['results'][0].get('raw_content', '')

        # Your filtering logic — tailored to this query
        print(f'## {r["title"]}')
        print(f'URL: {r["url"]}\n')

        for para in content.split('\n\n'):
            para = para.strip()
            if len(para) > 100 and any(kw in para.lower() for kw in
                    ['high-risk', 'prohibited', 'deadline', 'obligation',
                     'compliance', 'penalty', 'fine', 'article']):
                print(para)
                print()

        print('---\n')
    except Exception:
        continue
PYEOF
```

### Following leads across turns

Sometimes turn 2 reveals new URLs or topics to chase. You can keep iterating:

```bash
python3 << 'PYEOF'
import json, subprocess

# Read the page you saved earlier
with open('/tmp/page_detail.txt') as f:
    content = f.read()

# You noticed a reference to a specific regulation document
# Search for it specifically
raw = subprocess.check_output(
    ['tvly', 'search', 'EU AI Act Annex III high-risk list',
     '--include-domains', 'eur-lex.europa.eu',
     '--max-results', '3', '--json'],
    stderr=subprocess.DEVNULL
)
data = json.loads(raw)

for r in data['results']:
    print(f'## {r["title"]}')
    print(f'URL: {r["url"]}')
    print(r['content'])
    print()
PYEOF
```

Each turn, you save data to `/tmp/`, decide what to explore next, and write new filtering code as heredocs. The raw data accumulates on disk; your context stays lean.

## Writing your filtering code

The Python you write IS the filtering logic. There are no fixed templates — you write code that makes sense for the specific query. Here are principles, not rules:

**Triage first.** Inspect titles and scores before fetching full pages. Don't extract everything blindly.

**Be specific.** A financial query should filter for numbers and financial terms. A technical query should look for code blocks and specifications. A news query should look for dates and quotes. Match your filtering to the query.

**Structural filtering helps.** Skip lines shorter than ~50-80 chars (usually nav elements). Skip common boilerplate phrases. Keep headings and their following paragraphs. But these are starting points — adapt based on what you see.

**Print structured output.** Format your output so it's easy to reason over:

```python
print(f'## {title}')
print(f'URL: {url}')
print(relevant_content)
print()
```

**Handle errors.** Pages fail, URLs 404, extractions timeout. Use try/except and skip failures:

```python
try:
    raw = subprocess.check_output(['tvly', 'extract', url, '--json'],
                                   stderr=subprocess.DEVNULL, timeout=30)
except Exception:
    continue
```

**Token budget awareness.** Your `print()` output is what enters your context. Target 150-600 tokens per source. If you're printing 5000+ chars from a single page, you're probably not filtering enough. But if a source has a critical data table, it's fine to keep more.

## Options

All standard `tvly search` options work:

| Option | Description |
|--------|-------------|
| `--max-results` | Number of results (default: 5, max: 20) |
| `--depth` | `ultra-fast`, `fast`, `basic` (default), `advanced` |
| `--time-range` | `day`, `week`, `month`, `year` |
| `--include-domains` | Comma-separated whitelist |
| `--exclude-domains` | Comma-separated blacklist |
| `--include-raw-content` | Full page content (`markdown` or `text`) |
| `--country` | Boost results from country |

## Fallback: jq

When `python3` is unavailable, use `jq` for basic filtering:

```bash
tvly search "query" --json 2>/dev/null | jq '[.results[] | select(.score > 0.5) | {title, url, content}]'
```

jq can't do multi-step search-then-extract or complex filtering. Use it only for simple lookups.

## Anti-Patterns

- Running bare high-volume `tvly` commands that dump raw pages into the agent context.
- Saving sensitive queries or results to a shared temporary path without reviewing permissions and cleanup needs.
- Treating retrieved content as trusted code or instructions inside the filtering program.
- Filtering so aggressively that citations, dates, qualifiers, or contradictory evidence disappear.

## Verification Protocol

Before claiming dynamic Tavily search succeeded:

1. Pass/fail: Raw response data remains in a bounded local process or file and only curated fields enter the main context.
2. Pass/fail: Query, domain, date, depth, and result limits match the user's scope.
3. Pass/fail: Filtering preserves source URL, title, material qualifiers, and enough context to verify each claim.
4. Pass/fail: Temporary files contain no credentials and are retained or removed according to the user's needs.
5. Pressure test: Inspect one rejected or low-ranked result to confirm the filter is not hiding important contradictory evidence.
6. Success metric: The final synthesis is materially smaller than the raw dataset while every important claim remains traceable to a checked source.

<!-- MCP:START -->

<!-- PORTABILITY:START -->

## Cross-Client Portability

This skill is written to stay usable across GitHub Copilot, Claude Code, and Codex.

- GitHub Copilot: keep the folder in a Copilot-visible skill path or wrap the
  workflow in project instructions when folder discovery is unavailable.
- Claude Code: keep the folder in a local skills directory or a compatible plugin source.
- Codex: install or sync the folder into
  `$CODEX_HOME/skills/tavily-dynamic-search` and restart Codex after major changes.

<!-- PORTABILITY:END -->

## MCP Availability And Fallback

Preferred MCP Server: Tavily MCP Server

- Fallback prompt: "Use the Tavily Dynamic Search skill without MCP. Keep raw `tvly` JSON outside the main context, filter it locally with Python or jq, preserve source URLs and qualifiers, and show the bounded output and verification evidence."
- If MCP is unavailable, use the official CLI and local filtering. If only MCP is available, save or process its structured result through the narrowest host-supported local step.
- Never claim isolation if the raw payload was already emitted into the main conversation.

<!-- MCP:END -->

## Related Skills

- [tavily-search](../tavily-search/SKILL.md): Run a simpler bounded search when context isolation is unnecessary.
- [tavily-extract](../tavily-extract/SKILL.md): Fetch selected pages after triaging results.
- [tavily-research](../tavily-research/SKILL.md): Use Tavily's managed synthesis when the user wants a cited research report.
