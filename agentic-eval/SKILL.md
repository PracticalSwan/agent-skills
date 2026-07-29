---
name: agentic-eval
version: "2.0"
last_updated: 2026-07-29
tags: [agentic, eval, agents, delegation, workflow]
description: "Evaluate and improve AI-generated output with explicit rubrics, reflection loops, and stop conditions. Use when building self-critique workflows, evaluator-optimizer pipelines, or acceptance gates for code, docs, analysis, or plans."
---
# Agentic Eval

Use structured evaluation loops to improve important outputs before you call them done.

- Leverage native parallel subagent dispatch and 200k+ context windows where available.


## When to Use

Use symptom -> action triggers: when one matches, apply this skill and verify with the protocol below.

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

## Self-Verification Phase-Gate Questions

Before you claim the evaluation is complete, the evaluating agent must ask:

- Did I define the rubric, threshold, and evidence sources explicitly enough for another agent to rerun the check?
- Did every failing dimension produce a concrete improvement action instead of a vague critique?
- Did I stop because the result is acceptable, or only because I ran out of patience?
- Can I point to tests, logs, screenshots, or scorecards that support the final PASS or FAIL decision?

## Anti-Patterns

- Delegating or evaluating without a scoped success condition: The output becomes hard to review and easy to overbuild.
- Skipping the evidence step: A workflow that cannot be re-checked quickly is not ready for handoff.
- Bundling unrelated subtasks together: It creates noisy prompts, weaker ownership, and avoidable integration risk.

## Verification Protocol

Before claiming "skill applied successfully":

1. Pass/fail: The Agentic Eval workflow names the agent boundary, delegated scope, and expected return artifact.
2. Pass/fail: Context passed to helpers is minimal, task-local, and free of hidden expected answers.
3. Pass/fail: Results are integrated only after evidence, diffs, or citations are checked by the controller.
4. Pressure-test scenario: Run the workflow on two similar tasks that must not share assumptions or leaked context.
5. Success metric: Zero context leakage; every delegated output is independently reviewable.

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

<!-- MCP:START -->

<!-- PORTABILITY:START -->
## Cross-Client Portability

This skill is written to stay usable across GitHub Copilot, Claude Code, and Codex.

- GitHub Copilot: keep the folder in a Copilot-visible skill path or wrap the
  workflow in project instructions when folder discovery is unavailable.
- Claude Code: keep the folder in a local skills directory or a compatible plugin source.
- Codex: install or sync the folder into
  `$CODEX_HOME/skills/agentic-eval` and restart Codex after major changes.

<!-- PORTABILITY:END -->

## MCP Availability And Fallback

Preferred MCP Server: None required

- Fallback prompt: "Use the Agentic Eval skill without MCP. Rely on the local `SKILL.md`, bundled references or scripts, and manual verification. Show the exact commands, evidence, and final checks you used before concluding."
- If the current host does not expose a matching server, use the bundled references, scripts, native toolchain, and manual workflow already described in this skill.
- Treat direct local verification, rendered output, logs, tests, or screenshots as the fallback evidence path before completion.

<!-- MCP:END -->

## Related Skills

- [agent-task-mapping](../agent-task-mapping/SKILL.md): Use it when the workflow also needs task-to-agent routing decisions.
- [custom-agent-usage](../custom-agent-usage/SKILL.md): Use it when the workflow also needs loading and invoking custom agent definitions safely.
- [subagent-delegation](../subagent-delegation/SKILL.md): Use it when the workflow also needs safe, scoped delegation to helper agents.
- [subagent-driven-development](../subagent-driven-development/SKILL.md): Use it when the workflow also needs plan-driven implementation with reviewer loops.
