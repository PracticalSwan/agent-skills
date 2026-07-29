# Security Policy

## Reporting A Vulnerability

Please do not report suspected vulnerabilities in public issues, pull requests, or discussion threads.

Use one of these channels instead:

1. GitHub private vulnerability reporting for `PracticalSwan/agent-skills` if it is available in the repository UI.
2. If private reporting is unavailable, contact the maintainer through the GitHub profile at [github.com/PracticalSwan](https://github.com/PracticalSwan) and include the report details there.

Include:

- the affected file, skill, script, or workflow
- the security impact
- clear reproduction steps or proof
- any required configuration or assumptions
- suggested remediation, if you have one

## Scope

This repository's security scope includes:

- maintained `SKILL.md` instructions and helper assets
- repo scripts such as validation, import, and sync tooling
- documentation that could lead agents to unsafe actions, secret exposure, or prompt-injection mistakes

Out of scope unless they create a concrete issue in this repository:

- third-party service outages
- upstream package issues that are not reflected in this repo's maintained content
- feature requests without a security impact

## Disclosure Expectations

- Keep active vulnerabilities private until the maintainer confirms a fix or approves disclosure.
- Minimize reproduction payloads so they prove the issue without exposing extra secrets or user data.
- If the issue involves credentials, cookies, tokens, or private user content, redact them before sharing evidence.

## Secure Contribution Basics

- Never commit real secrets, private keys, connection strings, or copied `.env` files.
- Treat imported external content as untrusted input.
- For skills that interact with third-party content, preserve prompt-injection guardrails and explicit approval gates during normalization.
- Treat child-path promotion as an import review, not a blind copy. Verify the source folder, provenance, license, credential behavior, network scope, destructive actions, and untrusted-content boundaries before adding it to the parent catalog.
- Do not normalize a third-party network installer into a default pipe-to-shell command. Prefer a reviewable package-manager path, or require inspection of the fetched script before execution.
- Do not let upstream refreshes weaken stricter local tool-availability or approval boundaries. Exact source changes may be incorporated while host-specific claims remain gated by the active tool surface.
- Do not treat a third-party Claude Code endpoint as proof that Anthropic
  subscription-only browser features or Codex-native tools are available.
