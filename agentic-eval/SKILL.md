---
name: agentic-eval
description: Evaluate and improve AI-generated output with explicit rubrics, reflection loops, and stop conditions. Use when building self-critique workflows, evaluator-optimizer pipelines, or acceptance gates for code, docs, analysis, or plans.
---
# Agentic Eval

Use structured evaluation loops to improve important outputs before you call them done.

## When to Use

- A task is quality-critical and a single pass is too risky.
- You need repeatable acceptance criteria for code, docs, analysis, or plans.
- You want a reviewer or judge step that is separate from generation.
- You need to compare multiple candidate outputs against the same rubric.

## Core Loop

1. Define the artifact being judged.
2. Define a rubric with weighted dimensions.
3. Generate or collect the candidate output.
4. Evaluate it against the rubric.
5. Convert the feedback into concrete changes.
6. Re-run until the score crosses the threshold or the iteration budget is exhausted.

## Evaluation Patterns

### 1. Self-Reflection

Use the same agent to critique its own work when the task is moderate risk and the rubric is precise.

Best for:

- formatting checks
- completeness checks
- first-pass code or doc refinement

### 2. Evaluator-Optimizer Split

Separate generation from evaluation when you want clearer responsibilities.

Best for:

- high-value outputs
- rubric-based acceptance checks
- comparing multiple candidates fairly

### 3. Evidence-Based Evaluation

Back the score with tests, logs, benchmarks, or direct verification.

Best for:

- code generation
- migration plans
- architecture recommendations
- security or compliance review

## Rubric Design Rules

- Keep dimensions few and concrete.
- Weight the business-critical dimension highest.
- Define what a passing score means before evaluation starts.
- Require written evidence for any failing dimension.
- Stop when you are no longer learning new fixes.

Suggested dimensions:

- correctness
- completeness
- clarity
- maintainability
- risk management
- evidence quality

## Stop Conditions

Stop the loop when one of these becomes true:

- the overall threshold is met
- the failing dimensions are now low-impact only
- tests or verification evidence already prove the output is acceptable
- the score has stopped improving and more iterations are likely noise

## Output Format

Use a structure like this when reporting an evaluation:

```markdown
## Evaluation Summary

### Artifact
- Short description of what was evaluated

### Rubric Results
| Dimension | Weight | Score | Notes |
|-----------|--------|-------|-------|
| correctness | 0.40 | 4/5 | Main logic is sound |

### Overall
- Weighted score: 0.84
- Threshold: 0.80
- Result: PASS

### Required Improvements
- Tighten edge-case handling around ...
- Add verification evidence for ...
```

## Scripts And References

- [Rubric Template](./references/rubric-template.json)
- [Example Scores](./references/example-scores.json)
- [Rubric Scorecard Helper](./scripts/rubric-scorecard.py)

## Best Practices

- Keep the rubric stable across iterations so the score means something.
- Prefer evidence-backed criteria over taste-based criteria.
- Store the final rubric and score with the task when the output matters later.
- Pair with tests or direct verification whenever the artifact can be executed.
- If you use an LLM judge, constrain the output format so it can be parsed and compared.

## Cross-Client Portability

This skill is written to stay usable across GitHub Copilot, Claude Code, Codex, and Gemini CLI.

- GitHub Copilot: keep the folder in a Copilot-visible skill or plugin path, or wrap the workflow as project instructions if the host does not support portable skill folders directly.
- Claude Code: keep the folder in a local skills directory or a compatible plugin or marketplace source.
- Codex: install or sync the folder into `$CODEX_HOME/skills/<skill-name>` and restart Codex after major changes.
- Gemini CLI: this repository generates a project command named `/skills:agentic-eval` from this skill. Rebuild commands with `python scripts/export-gemini-skill.py agentic-eval` and then run `/commands reload` inside Gemini CLI.

## MCP Availability And Fallback

No dedicated MCP server is required for the normal workflow in this skill.

- If the current host lacks structured evaluation tooling, use the bundled rubric helper, local tests, and explicit Markdown scorecards.
- Treat direct verification evidence such as tests, logs, benchmarks, or rendered output as the fallback acceptance signal before closing the task.

## Related Skills

| Skill | Relationship |
|-------|--------------|
| [test-driven-development](../test-driven-development/SKILL.md) | Provides executable evidence for code-focused evaluation loops |
| [verification-before-completion](../verification-before-completion/SKILL.md) | Final evidence gate after the evaluation loop stabilizes |
| [code-quality](../code-quality/SKILL.md) | Use when rubric feedback points to maintainability or readability issues |
