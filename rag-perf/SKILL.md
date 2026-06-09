---
name: rag-perf
version: "1.2"
last_updated: 2026-06-09
tags: [nvidia, rag, performance, latency, throughput, profiling]
description: "NVIDIA RAG Blueprint performance-tuning guidance for profiling retrieval stacks, comparing bottlenecks, and validating latency or throughput improvements."
license: Apache-2.0
compatibility: "Guidance imported from the NVIDIA RAG Blueprint performance skill for current benchmark and profiling workflows."
metadata:
  author: "NVIDIA RAG"
  source_repo: "https://github.com/NVIDIA/skills"
  source_commit: "129a1087a1853f32a950e2f7bbc0fd7d57b9d422"
  source_path: "skills/rag-perf"
  upstream_repo: "https://github.com/NVIDIA-AI-Blueprints/rag"
---

# RAG-Perf — config-driven perf benchmark CLI

## Purpose

Drive a deployed NVIDIA RAG Blueprint server with a YAML config, run a server-side **profiling pass** (per-stage timing, citation quality, bottleneck inference) and an optional **aiperf load test** (TTFT / E2E / token & request throughput / error rate), and write a unified report. The CLI is intentionally minimal: `rag-perf -c <config>` plus `--help` / `--version`. Behaviour is *fully* config-driven; field variations belong in YAML.

## Scope

- **Accuracy / RAGAS** scoring of answer quality → use the **rag-eval** skill.
- **Deploying, repairing, or configuring services** (compose, helm, NIM env vars) → use the **rag-blueprint** skill.
- **Production monitoring / alerting** — rag-perf is a one-shot benchmark tool.
- **Runtime requirement:** a deployed RAG server reachable on the network.

## Prerequisites

- Repo cloned; **run commands from the repo root** (config paths in the presets are repo-root-relative).
- Python **3.11+** and **uv** on PATH.
- Install rag-perf into its own uv-managed venv: `uv sync --project scripts/rag-perf`.
- For unit tests: install dev extras as well — `uv sync --project scripts/rag-perf --extra dev` (otherwise `pytest-asyncio` is missing and async tests error out at collection time).
- A reachable RAG server (default `http://localhost:8081`). For the aiperf phase, the bundled `nvidia_rag` endpoint plugin must be installed — `pip install -e ./scripts/rag-perf` registers it via the `aiperf.plugins` entry point.
- For **synthetic** queries: an OpenAI-compatible chat-completions endpoint reachable at `synthetic.llm_url` (default `http://localhost:8999/v1/chat/completions`).
- rag-perf itself runs without `NVIDIA_API_KEY` (unlike rag-eval). The synthetic LLM endpoint may require its own auth — that's the deployment's concern.

## Instructions

1. **Pick a preset.** The three under [`scripts/rag-perf/configs/`](../../scripts/rag-perf/configs) are:
   - `quick_profile.yaml` — profile-only, ~30 s. Skips load test. For fast iteration on retrieval / reranker tuning.
   - `single_run.yaml` — one concurrency level, profiling + aiperf, ~2 min. Regression checks.
   - `sweep.yaml` — multi-axis sweep. `load.concurrency`, `rag.vdb_top_k`, `rag.reranker_top_k` are all `int | list[int]`; any of them as a list becomes a sweep axis (Cartesian product).

2. **Edit the preset.** **Required:** replace `rag.collection_names: ["<collection_name>"]` with a real collection on the deployed ingestor server. Verify the collection exists via `GET /v1/collections` on the ingestor. The placeholder `<collection_name>` validates fine but every request will fail at retrieval. Use a copied YAML preset for variants; the CLI surface is intentionally config-only.

3. **Run.** From repo root:
   ```bash
   uv run --project scripts/rag-perf rag-perf -c scripts/rag-perf/configs/single_run.yaml
   ```
   Same form for the other presets. The CLI accepts only `-c / --config` (required), `--help`, `--version`.

4. **Read stdout.** Every invocation prints, in order: a startup banner, a one-line summary, the **fully resolved config as YAML** (so the run is reproducible from terminal output), per-grid-point progress with the **shlex-joined aiperf command** in copy-pastable form, a **rich per-point summary table** (stage breakdown with bars, citation quality, bottleneck, load-test block), and finally a **side-by-side comparison table** auto-labelled by whichever axis varied. See [`references/output-and-analysis.md`](references/output-and-analysis.md).

5. **Inspect artifacts.** Layout depends on run shape — flat for single-point + `iterations=1`, nested under `iter_<i>/<point>/...` otherwise. See [`references/output-and-analysis.md`](references/output-and-analysis.md) for the full directory tree, file purposes, and how to parse `results.json` / `results.csv` / `report.md`.

6. **Summarise for the user.** When reporting back, follow the playbook in [`references/output-and-analysis.md#summarising-results-to-the-user`](references/output-and-analysis.md#summarising-results-to-the-user): pick the canonical result file for the run shape, build a headline table (concurrency × top-k axes × TTFT × throughput × bottleneck × citation quality), compute scaling efficiency on sweeps, **always flag** zero citations / non-zero error rate / suspect `llm_ttft_ms` / small-sample p99, and propose a concrete next-experiment YAML.

7. **Tune.** Schema is fully documented in [`docs/performance-benchmarking.md`](../../docs/performance-benchmarking.md) and the deeper-dive references below. Common knobs: turn `aiperf.enabled: false` for profile-only mode, increase `load.iterations` for variance estimation, set `load.sleep_between_points_s: 60` for overnight Cartesian sweeps.

## Examples

**Profile-only (quickest signal on retrieval / reranker tuning):**

```bash
uv run --project scripts/rag-perf rag-perf -c scripts/rag-perf/configs/quick_profile.yaml
```

Output: `rag-perf-results/quick_profile/run_<ts>/{profile_report.md, profile_results.json, profiling/}`. The `aiperf_rag_on/` directory is omitted. Filenames are `profile_*` because `aiperf.enabled: false`.

**Single benchmark point with full report:**

```bash
uv run --project scripts/rag-perf rag-perf -c scripts/rag-perf/configs/single_run.yaml
```

Output: flat `run_<ts>/{report.md, results.json, results.csv, profiling/, aiperf_rag_on/}`.

**Concurrency sweep:**

```bash
uv run --project scripts/rag-perf rag-perf -c scripts/rag-perf/configs/sweep.yaml
```

Output: nested `run_<ts>/iter_1/<CR:_VDB-K:_RERANKER-K:_…>/{profiling,aiperf_rag_on}/` per point, plus aggregate `report.md` / `results.json` / `results.csv` at the run root.

**Run unit tests:**

```bash
uv sync --project scripts/rag-perf --extra dev   # one-time, installs pytest-asyncio
uv run --project scripts/rag-perf python -m pytest tests/unit/test_rag_perf/
```

## Limitations

- The CLI is **config-only**: author or copy YAML to vary a parameter.
- `load.concurrency` / `rag.vdb_top_k` / `rag.reranker_top_k` accept `int | list[int]`; the validator requires unique list values because each value names a unique point dir.
- `input.file` and `input.synthetic` follow an XOR rule — both set fails validation. When neither is set, `synthetic` auto-fills with defaults so a bare config still validates.
- File-based input format is **inferred from extension only** (`.jsonl` or `.csv`); other extensions are rejected.
- Synthetic generation streams each query to disk as it completes (failure-resilient) but **fails fast on the first LLM error** — partial JSONL is preserved. Re-run after fixing the endpoint.
- Reasoning models (Nemotron Omni, Qwen-Reasoning) require `synthetic.disable_thinking: true` (the default). Without it the model exhausts the token budget on chain-of-thought and `content` returns empty — the generator now raises with a clear message instead of substituting `reasoning_content` for the answer.
- aiperf-specific knobs outside the YAML surface (request rate distribution, GPU telemetry config, etc.) require editing `AiperfRunner._base_aiperf_cmd` in `scripts/rag-perf/rag_perf/runner.py`.
- Procedural detail lives under **`references/`** to keep this file concise.

## Troubleshooting

| Error / signal | Likely cause | What to do |
|---|---|---|
| `Configuration errors in <yaml>:  •  input  —  ... XOR rule` | Both `input.file` and `input.synthetic` set | Pick one. The XOR validator runs at YAML load time. |
| `input.file must end in .jsonl or .csv` | Extension other than `.jsonl` / `.csv` | Rename or convert. |
| `load.concurrency has duplicate values` | e.g. `[2, 2, 4]` | Each concurrency maps to a unique point dir; dedupe. |
| `warmup_requests must be >= 1` | YAML had `warmup_requests: 0` | aiperf rejects warmup=0; minimum is 1. |
| `LLM returned empty content (reasoning_content was populated — model exhausted its budget on chain-of-thought; raise min_query_tokens or set synthetic.disable_thinking=true).` | Reasoning model used CoT and ran out of tokens | Set `synthetic.disable_thinking: true` (the default) or raise `min_query_tokens`. |
| `✗ All N profiling requests failed across M point(s).` + exit 1 | Bad URL, server down, wrong collection | Verify `target.url`, `rag.collection_names` (the `<collection_name>` placeholder will hit this). |
| Per-iteration `⚠ N profiling requests failed` warning, run continues | Some requests timed out / errored mid-run | Check rag-server logs, raise `target.timeout_s`, drop concurrency. |
| `RuntimeError: Random synthetic query generation failed at query N: ...` | LLM endpoint rejected a request mid-generation | Partial JSONL is at `synthetic.jsonl_output_path`; fix endpoint and re-run with reduced `num_queries`, or point `input.file` at the partial file. |
| `Citation count (mean): 0` and `Citation relevance score: N/A` for a non-empty deployment | Collection mismatch between `rag.collection_names` and what's actually ingested | Run `curl -s http://<ingestor>:8082/v1/collections` to list real collections. |
| Tests error with `ModuleNotFoundError: No module named 'pytest_asyncio'` | Dev extras missing | `uv sync --project scripts/rag-perf --extra dev`. |
| CI: `ModuleNotFoundError: No module named 'ruamel'` from `tests/unit/test_rag_perf/` | rag-perf package missing from CI venv | Add `uv pip install -e ./scripts/rag-perf` after the top-level install in the unit-tests job. |

## Gotchas

- **Run from repo root.** Preset configs reference `scripts/rag-perf/examples/queries.jsonl` and `scripts/rag-perf/prompts/default_prompts.yaml` with repo-root-relative paths. Running from inside `scripts/rag-perf/` will fail those file lookups.
- **CLI is config-only.** Edit the YAML or copy a preset for URL, concurrency, collection, and similar fields.
- **Always edit `rag.collection_names` before the first run.** The presets ship with `["<collection_name>"]` as a deliberate placeholder. Validation passes, retrieval fails silently for every request — manifests as `Citation count (mean): 0` everywhere.
- **`load.concurrency_list`, `rag.vdb_top_k_list`, `rag.reranker_top_k_list`** are read-only properties that normalise scalar-or-list to a list. Use them when reasoning about the grid; the underlying YAML field is whatever the user wrote.
- **`aiperf.enabled: false` changes filenames.** The top-level outputs become `profile_report.md` / `profile_results.json` / `profile_results.csv`. The aggregate sweep table also suppresses load-test rows and the "Optimal throughput" footer.
- **Resolved-config dump is verbose** (50+ lines) — expected. It's what makes terminal output a self-contained reproducer; don't filter it out in scripts.
- **The aiperf shell command is logged before each subprocess.** Look for `\n  $ python -m aiperf profile -m ... --endpoint-type nvidia_rag ...` in stdout — copy-paste runnable for reproducing a single point outside rag-perf.
- **`--endpoint-type nvidia_rag`** comes from the bundled plugin at `scripts/rag-perf/rag_perf/plugin/nvidia_rag.py`. It teaches aiperf about the RAG `/v1/generate` request shape and parses citations + per-stage `metrics` out of the SSE stream. If aiperf can't resolve `nvidia_rag`, rag-perf needs editable installation in the venv — re-run `uv sync --project scripts/rag-perf` (or `uv pip install -e ./scripts/rag-perf`).
- **Sweep-mode point-name collision.** When two points differ only in concurrency (e.g. `[1, 4]` × single `vdb_top_k`), the dir name encodes everything: `CR:1_ISL:50_OSL:512_VDB-K:20_RERANKER-K:4_Model:...`. Cluster / GPU / experiment_name (`output.cluster`, `output.gpu`, `output.experiment_name`) are appended too — useful for diff-friendly artifact paths across machines.
- **`load.iterations > 1` repeats the entire grid**. Each repetition writes to its own `iter_<i>/`. Aggregate CSV row count = `n_points × iterations`.

## Source of truth

| Piece | Location |
|---|---|
| Driver | [`scripts/rag-perf/rag_perf/cli.py`](../../scripts/rag-perf/rag_perf/cli.py) (`main` is the single Click command) |
| Schema | [`scripts/rag-perf/rag_perf/config.py`](../../scripts/rag-perf/rag_perf/config.py) (`RunConfig` and sub-models) |
| Orchestrator | [`scripts/rag-perf/rag_perf/runner.py`](../../scripts/rag-perf/rag_perf/runner.py) (`BenchmarkRunner.run`, `RagProfiler`, `AiperfRunner`) |
| aiperf plugin | [`scripts/rag-perf/rag_perf/plugin/nvidia_rag.py`](../../scripts/rag-perf/rag_perf/plugin/nvidia_rag.py) |
| User-facing doc | [`docs/performance-benchmarking.md`](../../docs/performance-benchmarking.md) |
| Presets | [`scripts/rag-perf/configs/{quick_profile,single_run,sweep}.yaml`](../../scripts/rag-perf/configs/) |
| Sample queries | [`scripts/rag-perf/examples/queries.jsonl`](../../scripts/rag-perf/examples/queries.jsonl) |
| Synthetic prompts | [`scripts/rag-perf/prompts/default_prompts.yaml`](../../scripts/rag-perf/prompts/default_prompts.yaml) |
| Config schema details | [`references/config-schema.md`](references/config-schema.md) |
| Synthetic-query generation | [`references/synthetic-generation.md`](references/synthetic-generation.md) |
| Output layout & metric semantics | [`references/output-and-analysis.md`](references/output-and-analysis.md) |

## Agent playbook

1. **Sync deps:** `uv sync --project scripts/rag-perf` (one-time per checkout).
2. **Pick & customise a preset:** copy `scripts/rag-perf/configs/<preset>.yaml` if you want a variant; always set `rag.collection_names` to a real collection.
3. **Run:** `uv run --project scripts/rag-perf rag-perf -c <config>` from repo root.
4. **Read the per-point + aggregate tables on stdout.** Bottleneck inference is in the per-point profiling section; comparison across points is the final aggregate table.
5. **Parse artifacts** under `output.dir/run_<ts>/` — see [`references/output-and-analysis.md`](references/output-and-analysis.md). For multi-point runs, `results.csv` has one row per (point × iteration).
6. **Summarise for the user** using the playbook in [`references/output-and-analysis.md#summarising-results-to-the-user`](references/output-and-analysis.md#summarising-results-to-the-user) — headline table, scaling-efficiency math for sweeps, mandatory flags for zero citations / non-zero errors / suspect `llm_ttft_ms` / low sample size, and a concrete next-experiment YAML.
7. **Tune retrieval / reranker:** flip to `quick_profile.yaml` or `aiperf.enabled: false` for fast iteration, then return to `single_run.yaml` / `sweep.yaml` when characterising under load.
8. **Triage failures:** see Troubleshooting above and [`references/output-and-analysis.md`](references/output-and-analysis.md) for empty-citation / bottleneck=N/A patterns.

## Anti-Patterns

- Optimizing before recording a baseline: Without a starting point, there is no trustworthy performance story.
- Using toy traffic to justify production tuning: Tiny prompts or empty corpora hide the real bottleneck.
- Accepting lower answer quality as an untracked side effect of a latency win.

## Verification Protocol

Before claiming "skill applied successfully":

1. Pass/fail: The performance investigation starts from a named baseline and a concrete bottleneck hypothesis.
2. Pass/fail: The workload shape, corpus size, and concurrency assumptions match the path being optimized.
3. Pass/fail: Any latency or throughput claim is paired with a correctness or quality guardrail.
4. Pressure-test scenario: Re-run the workflow on a retrieval stack that speeds up only because caching masked a stale index.
5. Success metric: The user gets a reproducible benchmark path and a tuning change that improves the intended metric without hidden regressions.

<!-- PORTABILITY:START -->
## Cross-Client Portability

This skill is written to stay usable across GitHub Copilot, Claude Code, Codex, and Gemini CLI.

- GitHub Copilot: keep the folder in a Copilot-visible skill or plugin path, or wrap the workflow as project instructions if the host does not support portable skill folders directly.
- Claude Code: keep the folder in a local skills directory or a compatible plugin or marketplace source.
- Codex: install or sync the folder into `$CODEX_HOME/skills/<skill-name>` and restart Codex after major changes.
- Gemini CLI: this repository generates a project command named `/skills:rag-perf` from this skill. Rebuild commands with `python scripts/export-gemini-skill.py rag-perf` and then run `/commands reload` inside Gemini CLI.

<!-- PORTABILITY:END -->

<!-- MCP:START -->
## MCP Availability And Fallback

Preferred MCP Server: None required

- Fallback prompt: "Use the rag-perf skill without MCP. Rely on the local `SKILL.md`, bundled references or scripts, and manual verification. Show the exact commands, evidence, and final checks you used before concluding."
- If the current host does not expose a matching server, use the bundled references, scripts, native toolchain, and manual workflow already described in this skill.
- Treat direct local verification, rendered output, logs, tests, or screenshots as the fallback evidence path before completion.

<!-- MCP:END -->

## Related Skills

- [devops-tooling](../devops-tooling/SKILL.md): Use it when the performance work also needs container, CI, or infrastructure diagnostics.
- [cloud-design-patterns](../cloud-design-patterns/SKILL.md): Use it when bottlenecks reveal larger scaling or architecture tradeoffs.
- [documentation-verification](../documentation-verification/SKILL.md): Use it when benchmark claims must be published or preserved in repo docs.
