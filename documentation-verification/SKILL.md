---
name: documentation-verification
description: Documentation verification, validation procedures, and quality checks. Use when reviewing documentation before merging, checking doc completeness, verifying code examples work, ensuring no broken links, and validating accuracy. Triggered by keywords like documentation review, verify documentation, doc validation, check broken links, validate code examples.
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
