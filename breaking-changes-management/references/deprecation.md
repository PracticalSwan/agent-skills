# Deprecation Procedures

## Deprecation Process

**When deprecating features:**

1. **Add deprecation notice** to documentation
2. **Update examples** to use recommended alternatives
3. **Create migration guide** if alternative is non-trivial
4. **Update CHANGELOG** with deprecation notice
5. **Set timeline** for removal (e.g., "Will be removed in v3.0")
6. **In next major version**, remove deprecated feature and docs

## Deprecation Notice Format

```markdown
> **⚠️ Deprecated**
>
> This feature is deprecated and will be removed in version X.Y.Z.
> Please use [Alternative Feature](link-to-alt) instead.
```

## Migration Guide Template

```markdown
## Migration Guide: Change Name

Change introduced in v2.0.0. This guide helps you migrate from v1.x to v2.x.

### What Changed

[Description of what changed and why]

### Before vs After

**Before (v1.x):**
\`\`\`language
oldFunctionCall();
\`\`\`

**After (v2.x):**
\`\`\`language
newFunctionCall();
\`\`\`

### Migration Steps

1. Step one: Description
2. Step two: Description
3. Step three: Description

### Common Issues

**Issue:** Description
**Solution:** How to fix it

### Additional Resources

- [Link to full documentation](url)
- [Link to discussion](url)
```

## Version Management

**Deprecation Timeline:**
- **Announce**: Document in minor version (e.g., v2.1.0 - "Will be removed in v3.0")
- **Feature Freeze**: In next minor version (e.g., v2.2.0 - stop recommending, encourage migration)
- **Removal**: In major version (e.g., v3.0.0 - remove feature and docs)

**Semver Rules:**
- PATCH (x.Y.Z): Bug fixes, no deprecations
- MINOR (x.Y.Z): New features, deprecations allowed
- MAJOR (X.Y.Z): Breaking changes, removal of deprecated features
