---
name: code-examples-sync
description: Synchronize and verify code examples in documentation. Use when function signatures change, API interfaces update, imports shift, or documentation snippets become outdated and need correction.
license: Complete terms in LICENSE.txt
---

# Code Example Synchronization

Maintain code examples in documentation that stay synchronized with actual code.

## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.agents/skills/`

## Activation Conditions

Use this skill when:
- Function signatures or parameters change
- API interfaces are modified
- Best practices evolve (deprecated patterns emerge)
- Code examples become outdated
- Imports or dependencies change

## Verification Checks

See [Code Example Verification](./references/verification.md) for:
- Checking examples compile/run correctly
- Verifying imports are up to date
- Testing example output matches documentation
- Ensuring consistent syntax across examples

## Update Patterns

When code changes affect examples:

1. **Function signature changes**: Update all snippets using the function, verify examples compile, update imports if needed

2. **API interface changes**: Update request/response examples, revise client code examples, update SDK usage examples

3. **Best practice evolution**: Replace outdated patterns, update to current recommended approaches, add deprecation notices for old patterns

## Quality Checklist

- [ ] All code examples compile/run successfully
- [ ] Imports and dependencies are current
- [ ] Output matches documented results
- [ ] Syntax is consistent across language
- [ ] Error handling is demonstrated where applicable


---

## Related Skills

| Skill | Relationship |
|-------|-------------|
| [documentation-verification](../documentation-verification/SKILL.md) | Validate code examples before merging docs |
| [documentation-authoring](../documentation-authoring/SKILL.md) | Keep authored docs in sync with code changes |
| [breaking-changes-management](../breaking-changes-management/SKILL.md) | Update examples after breaking API changes |

---

## Related Skills

| Skill | Relationship |
|-------|-------------|
| [documentation-verification](../documentation-verification/SKILL.md) | Validate code examples before merging docs |
| [documentation-authoring](../documentation-authoring/SKILL.md) | Keep authored docs in sync with code changes |
| [breaking-changes-management](../breaking-changes-management/SKILL.md) | Update examples after breaking API changes |
