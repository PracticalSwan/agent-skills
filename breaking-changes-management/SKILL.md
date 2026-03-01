---
name: breaking-changes-management
description: Manage breaking API changes, migration guides, deprecation notices, and semver versioning. Use when introducing breaking changes, writing migration paths, updating changelogs, or releasing major versions.
license: Complete terms in LICENSE.txt
---

# Breaking Changes Management

## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.agents/skills/`

## Activation Conditions

Use this skill when:
- Introducing breaking API changes
- Creating migration guides
- Deprecating features with timeline
- Updating CHANGELOG.md for major versions
- Managing version transitions

## Breaking Change Documentation

**When breaking API changes occur:**
- Document what changed
- Provide before/after examples
- Include step-by-step migration instructions
- Update CHANGELOG.md with BREAKING prefix

## Deprecation Process

See [Deprecation Procedures](./references/deprecation.md) for:
- marking deprecated features
- suggesting alternative approaches
- creating migration guides
- updating changelog with deprecation notice
- setting timeline for removal

## Migration Guides

**Create migration guides when:**

1. **Breaking API changes occur**: Document what changed, provide before/after examples, include step-by-step migration instructions

2. **Major version updates**: List all breaking changes, provide upgrade checklist, include common migration issues and solutions

3. **Deprecating features**: Mark deprecated features clearly, suggest alternative approaches, include timeline for removal

## Changelog Format

```markdown
## [Version] - YYYY-MM-DD

### Added
- New feature description with reference to PR/issue

### Changed
- **BREAKING**: Description of breaking change
- Other changes

### Fixed
- Bug fix description
```

## Review Checklist

- [ ] Breaking changes clearly documented
- [ ] Migration guide created if needed
- [ ] Deprecated features marked with alternative suggestions
- [ ] Removal timeline specified
- [ ] ChangeLog updated with BREAKING prefix
- [ ] Before/after examples provided


---

## Related Skills

| Skill | Relationship |
|-------|-------------|
| [documentation-patterns](../documentation-patterns/SKILL.md) | Templates for migration guides and breaking change docs |
| [code-examples-sync](../code-examples-sync/SKILL.md) | Update code examples after breaking API changes |
| [development-workflow](../development-workflow/SKILL.md) | Versioning and release lifecycle management |

---

## Related Skills

| Skill | Relationship |
|-------|-------------|
| [documentation-patterns](../documentation-patterns/SKILL.md) | Templates for migration guides and breaking change docs |
| [code-examples-sync](../code-examples-sync/SKILL.md) | Update code examples after breaking API changes |
| [development-workflow](../development-workflow/SKILL.md) | Versioning and release lifecycle management |
