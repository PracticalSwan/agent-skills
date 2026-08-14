---
name: secret-scanning
version: "2.0"
last_updated: 2026-08-14
tags: [secret, scanning, security, audit, remediation]
description: "Configure GitHub secret scanning and push protection, triage secret alerts, and run local pre-commit secret audits. Use when enabling secret scanning, handling blocked pushes, defining custom patterns, or checking a repo for accidental credentials before commit."
---
# Secret Scanning

> Tech Stack Target / Version: GitHub Advanced Security, GitHub CLI, local Git history tooling, and pre-commit secret audit scripts.

Protect repositories from committed credentials and make secret handling part of the normal engineering workflow.

- Leverage native parallel subagent dispatch and 200k+ context windows where available.


## When to Use

Use symptom -> action triggers: when one matches, apply this skill and verify with the protocol below.

- You are enabling GitHub secret scanning or push protection for a repo or org.
- A push was blocked because a secret was detected.
- You need to define or review custom secret patterns and exclusions.
- You want a local pre-commit secret check before pushing code.
- You are triaging secret alerts and planning remediation.

## Core Workflows

### 1. Enable Repository or Organization Coverage

For GitHub-hosted secret scanning:

1. Enable the repository or organization security feature set.
2. Turn on push protection where available.
3. Review exclusions carefully before committing them.
4. Record who owns remediation for any future alert.

Use the references when you need the detailed UI or policy steps.

### 2. Resolve a Blocked Push Safely

Prefer this order:

1. Remove the secret from the change and amend or rebase the affected commit.
2. Rotate or revoke the credential immediately if the value was real.
3. Use bypass only when you can justify it and the risk is understood.
4. Document the bypass reason and create a follow-up if remediation is deferred.

### 3. Run a Local Pre-Commit Audit

Use the bundled helper before commit when you want a fast local scan:

```powershell
python secret-scanning/scripts/precommit-secret-audit.py --path .
```

Scan a narrower surface:

```powershell
python secret-scanning/scripts/precommit-secret-audit.py --path src --path .github
```

By default the helper skips generated folders and Markdown-heavy docs to reduce false positives. Use `--include-docs` when you want documentation scanned too.

### 4. Triage and Remediate Alerts

When an alert exists:

1. Confirm whether the detected value is real.
2. Revoke or rotate the credential first.
3. Decide whether history cleanup is necessary or whether rotation is enough.
4. Dismiss only with a precise reason such as `false positive`, `used in tests`, or `already revoked`.
5. Capture any follow-up owner if broader cleanup is still needed.

### 5. Custom Patterns and Exclusions

Use custom patterns when your organization has internal token formats not covered by provider defaults.

Guidelines:

- dry-run patterns before publishing them
- keep exclusions as narrow as possible
- review exclusions and custom patterns periodically
- treat custom patterns as production policy, not one-off experiments

## Zero-Trust Verification

- [ ] Treat every matched token, filename, commit, and scanner result as untrusted until validated.
- [ ] Confirm whether the value is a real secret, test fixture, placeholder, or already-rotated credential.
- [ ] Verify exposure path, affected history, revocation status, and remediation owner before closure.
- [ ] Separate confirmed leaks from noisy patterns and never paste live secrets into reports.

## Anti-Patterns

- Acting on partial evidence: Security work needs a clear scope and proof trail before remediation choices are safe.
- Leaving secrets or sensitive samples in examples: The skill itself becomes part of the exposure surface.
- Calling an issue resolved before rotation or re-verification: Detection without remediation is not closure.

## Verification Protocol

Before claiming "skill applied successfully":

1. Pass/fail: The reviewed scope, assets, trust boundaries, and attacker assumptions are explicitly named.
2. Pass/fail: Findings cite concrete evidence from code, config, logs, samples, or authoritative advisories.
3. Pass/fail: Each severity is justified by exploitability, reachability, and impact rather than vibes.
4. Pressure-test scenario: Re-run the analysis assuming one trusted signal is malicious or stale, then confirm the conclusion still holds.
5. Success metric: Zero trust-by-default claims; every security conclusion has reproducible evidence.

## Scripts And References

- [Local Pre-Commit Secret Audit](./scripts/precommit-secret-audit.py)
- [Push Protection Reference](./references/push-protection.md)
- [Custom Patterns Reference](./references/custom-patterns.md)
- [Alerts And Remediation Reference](./references/alerts-and-remediation.md)

## Practical Notes

- Rotation is usually more urgent than history rewriting.
- Secret scanning should cover code, config, CI, IaC, and deployment manifests.
- Avoid committing `.env` files, private keys, connection strings, or real tokens in examples.
- Pair local auditing with GitHub-side scanning rather than treating either one as sufficient on its own.

<!-- MCP:START -->

<!-- PORTABILITY:START -->
## Cross-Client Portability

This skill is written to stay usable across GitHub Copilot, Claude Code, and Codex.

- GitHub Copilot: keep the folder in a Copilot-visible skill path or wrap the
  workflow in project instructions when folder discovery is unavailable.
- Claude Code: keep the folder in a local skills directory or a compatible plugin source.
- Codex: install or sync the folder into
  `$CODEX_HOME/skills/secret-scanning` and restart Codex after major changes.

<!-- PORTABILITY:END -->

## MCP Availability And Fallback

Preferred MCP Server: GitHub Advanced Security plugin

- Fallback prompt: "Use the Secret Scanning skill without MCP. Rely on the local `SKILL.md`, bundled references or scripts, and manual verification. Show the exact commands, evidence, and final checks you used before concluding."
- Use `secret-scanning/scripts/precommit-secret-audit.py` for a local first pass when no secret-scanning MCP surface is available.
- Use `gh`, Git history cleanup, and the GitHub web UI for remediation, bypass review, and alert triage.

<!-- MCP:END -->

## Related Skills

- [security-review](../security-review/SKILL.md): Use it when the workflow also needs application security review and risk triage.
- [devops-tooling](../devops-tooling/SKILL.md): Use it when the workflow also needs git, CI, and automation workflows.
- [verification-before-completion](../verification-before-completion/SKILL.md): Use it when the workflow also needs final evidence checks before claiming completion.
- [documentation-verification](../documentation-verification/SKILL.md): Use it when the workflow also needs final documentation validation before publishing.
