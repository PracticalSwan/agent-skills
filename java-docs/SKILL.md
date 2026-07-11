---
name: java-docs
version: "1.3"
last_updated: 2026-07-11
tags: [java, docs, development, testing, quality]
description: "Java Javadoc best practices. Use when adding or reviewing documentation for Java types, methods, packages, and public APIs."
---
# Java Documentation (Javadoc) Best Practices

> Optimized for current Java LTS releases, JavaDoc doclint, Maven or Gradle builds, and module-aware API documentation.

- Public and protected members should be documented with Javadoc comments.
- It is encouraged to document package-private and private members as well, especially if they are complex or not self-explanatory.
- The first sentence of the Javadoc comment is the summary description. It should be a concise overview of what the method does and end with a period.
- Use `@param` for method parameters. The description starts with a lowercase letter and does not end with a period.
- Use `@return` for method return values.
- Use `@throws` or `@exception` to document exceptions thrown by methods.
- Use `@see` for references to other types or members.
- Use `{@inheritDoc}` to inherit documentation from base classes or interfaces.
  - Unless there is major behavior change, in which case you should document the differences.
- Use `@param <T>` for type parameters in generic types or methods.
- Use `{@code}` for inline code snippets.
- Use `<pre>{@code ... }</pre>` for code blocks.
- Use `@since` to indicate when the feature was introduced (e.g., version number).
- Use `@version` to specify the version of the member.
- Use `@author` to specify the author of the code.
- Use `@deprecated` to mark a member as deprecated and provide an alternative.

- Leverage native parallel subagent dispatch and 200k+ context windows where available.


## Documentation Stack Reference

Inherit the shared stack from [documentation-patterns](../documentation-patterns/SKILL.md#shared-documentation-stack): source-of-truth discovery, audience framing, structure selection, verification, and freshness checks. Keep this skill focused on Java API documentation specifics instead of restating the full stack.

## Anti-Patterns

- Repeating the method signature in prose: JavaDoc is most useful when it adds intent, constraints, and failure semantics.
- Leaving exceptions or side effects undocumented: Callers cannot use the API safely if the contract is only visible in code.
- Publishing examples that no longer compile: Broken snippets damage trust faster than missing snippets.

## Verification Protocol

Before claiming "skill applied successfully":

1. Pass/fail: The Java Docs output identifies audience, purpose, source of truth, and freshness requirements.
2. Pass/fail: Shared documentation-stack guidance is referenced instead of duplicating another documentation skill.
3. Pass/fail: Claims, links, commands, examples, and screenshots are verified or explicitly marked unverified.
4. Pressure-test scenario: Apply the skill to a doc request with a stale command, missing owner, and conflicting audience.
5. Success metric: Zero undocumented assumptions; every reader-facing claim is sourced or scoped.

## Before and After Example

```java
// Before
/** Gets a user. */
User getUser(String id);

// After
/**
 * Loads a user by identifier.
 *
 * @param id stable user identifier from the identity provider
 * @return persisted user record when found
 * @throws UserNotFoundException when the identifier does not resolve
 */
User getUser(String id);
```

Documents inputs, outputs, and failure conditions so the API contract is clear to callers and reviewers.

## Common Pitfalls

- Explaining what the method name already says: JavaDoc should capture intent, constraints, and side effects, not repeat the signature.
- Leaving exceptions undocumented: Callers cannot use the API safely if failure modes are only visible in implementation.
- Letting examples lag behind the code: Outdated snippets make the docs look trustworthy while teaching the wrong contract.

<!-- PORTABILITY:START -->
## Cross-Client Portability

This skill is written to stay usable across GitHub Copilot, Claude Code, Codex, and Gemini CLI.

- GitHub Copilot: keep the folder in a Copilot-visible skill or plugin path, or wrap the workflow as project instructions if the host does not support portable skill folders directly.
- Claude Code: keep the folder in a local skills directory or a compatible plugin or marketplace source.
- Codex: install or sync the folder into `$CODEX_HOME/skills/<skill-name>` and restart Codex after major changes.
- Gemini CLI: this repository generates a project command named `/skills:java-docs` from this skill. Rebuild commands with `python scripts/export-gemini-skill.py java-docs` and then run `/commands reload` inside Gemini CLI.

<!-- PORTABILITY:END -->

<!-- MCP:START -->
## MCP Availability And Fallback

Preferred MCP Server: None required

- Fallback prompt: "Use the Java Documentation (Javadoc) Best Practices skill without MCP. Rely on the local `SKILL.md`, bundled references or scripts, and manual verification. Show the exact commands, evidence, and final checks you used before concluding."
- If the current host does not expose a matching server, use the bundled references, scripts, native toolchain, and manual workflow already described in this skill.
- Treat direct local verification, rendered output, logs, tests, or screenshots as the fallback evidence path before completion.

<!-- MCP:END -->

## Related Skills

- [java-junit](../java-junit/SKILL.md): Use it when the workflow also needs JUnit 5 testing practices in Java.
- [documentation-authoring](../documentation-authoring/SKILL.md): Use it when the workflow also needs drafting structured technical or product documents.
- [documentation-quality](../documentation-quality/SKILL.md): Use it when the workflow also needs documentation review standards and quality gates.
- [code-quality](../code-quality/SKILL.md): Use it when the workflow also needs two-stage review (spec compliance first, then code quality), maintainability, and refactoring guidance.
