---
name: documentation-quality
description: Documentation quality standards and writing principles. Use when establishing formatting rules, reviewing doc quality metrics, creating writing guidelines, or enforcing consistent documentation style across a project.
license: Complete terms in LICENSE.txt
---

# Documentation Quality Standards

## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.agents/skills/`

## Activation Conditions

Use this skill when:
- Writing new documentation
- Reviewing documentation for quality
- Establishing documentation standards
- Creating style guides for docs
- Checking documentation formatting

## Writing Guidelines

See [Writing Standards](./references/writing-standards.md) for:
- Clear, concise language principles
- Code example formatting
- Consistent terminology usage
- Error handling documentation
- Edge case documentation

## Code Example Format

```markdown
### Example: [Clear description of what example demonstrates]

\`\`\`language
// Include necessary imports/setup
import { function } from 'package';

// Complete, runnable example
const result = function(parameter);
console.log(result);
\`\`\`

**Output:**
\`\`\`
expected output
\`\`\`
```

## Quality Checklist

- [ ] Language is clear and concise
- [ ] Code examples are complete and runnable
- [ ] Both basic and advanced examples included
- [ ] Terminology is consistent
- [ ] Error handling documented
- [ ] Edge cases and limitations covered


---

## Related Skills

| Skill | Relationship |
|-------|-------------|
| [documentation-authoring](../documentation-authoring/SKILL.md) | Apply quality standards during doc creation |
| [documentation-verification](../documentation-verification/SKILL.md) | Verify quality metrics before merging docs |
| [documentation-patterns](../documentation-patterns/SKILL.md) | Patterns that enforce quality consistency |

---

## Related Skills

| Skill | Relationship |
|-------|-------------|
| [documentation-authoring](../documentation-authoring/SKILL.md) | Apply quality standards during doc creation |
| [documentation-verification](../documentation-verification/SKILL.md) | Verify quality metrics before merging docs |
| [documentation-patterns](../documentation-patterns/SKILL.md) | Patterns that enforce quality consistency |
