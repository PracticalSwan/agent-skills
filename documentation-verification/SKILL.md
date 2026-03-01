---
name: documentation-verification
description: Validate documentation before merging — check completeness, broken links, code example accuracy, and factual correctness. Use when reviewing docs for quality gates or running pre-merge doc validation.
license: Complete terms in LICENSE.txt
---

# Documentation Verification

## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.agents/skills/`

## Activation Conditions

Use this skill when:
- Reviewing documentation before merging
- Checking documentation completeness
- Validating code examples
- Ensuring no broken links
- Verifying configuration accuracy

## Before Applying Changes

**Check documentation completeness:**

1. All new public APIs are documented
2. Code examples compile and run
3. Links in documentation are valid
4. Configuration examples are accurate
5. Installation steps are current
6. README.md reflects current state

## Documentation Testing

See [Validation Procedures](./references/validation.md) for:
- Verifying code examples compile/run
- Checking for broken internal/external links
- Validating configuration examples against schemas
- Ensuring API examples match current implementation

## Validation Commands

```bash
# Example validation commands
npm run docs:check         # Verify docs build
npm run docs:test-examples # Test code examples
npm run docs:lint         # Check for issues
```

## Review Checklist

- [ ] All new public APIs are documented
- [ ] Code examples compile and run
- [ ] Links in documentation are valid
- [ ] Configuration examples are accurate
- [ ] Installation steps are current
- [ ] README.md reflects current state
- [ ] No broken internal links
- [ ] No broken external references


---

## Related Skills

| Skill | Relationship |
|-------|-------------|
| [documentation-quality](../documentation-quality/SKILL.md) | Quality standards to verify against |
| [documentation-authoring](../documentation-authoring/SKILL.md) | Verify authored docs before publishing |
| [code-examples-sync](../code-examples-sync/SKILL.md) | Validate code examples are current and working |

---

## Related Skills

| Skill | Relationship |
|-------|-------------|
| [documentation-quality](../documentation-quality/SKILL.md) | Quality standards to verify against |
| [documentation-authoring](../documentation-authoring/SKILL.md) | Verify authored docs before publishing |
| [code-examples-sync](../code-examples-sync/SKILL.md) | Validate code examples are current and working |
