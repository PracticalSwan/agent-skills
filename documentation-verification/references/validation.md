# Documentation Validation Procedures

## Code Example Validation

**Verify code examples in docs compile/run:**

1. Extract code blocks from documentation files
2. Execute each example in isolated environment
3. Compare output with documented expected output
4. Flag any failures or mismatches

**Tools:**
- JavaScript/TypeScript: `jest`, `vitest` with example runner
- Python: `pytest` with doctest
- Go: `go test -run=Doc`
- Rust: `cargo test --doc`

## Link Validation

**Check for broken links:**

1. Scan documentation for markdown, HTML, and auto-links
2. Resolve internal links (point to existing documentation files)
3. Test external links (HTTP HEAD requests)
4. Report broken or redirected links

**Tools:**
- `markdown-link-check`: Validates markdown links
- `lychee`: Fast link checker, supports HTML
- `linkchecker`: Advanced, supports recursion

## Configuration Validation

**Validate configuration examples:**

1. Compare examples against config schemas
2. Verify all documented options are valid
3. Check for typos in configuration keys
4. Validate default values match implementation

**Example Validation Command:**

```bash
npm run docs:check         # Verify docs build
npm run docs:test-examples # Test code examples
npm run docs:lint         # Check for issues
npm run docs:validate      # Run all documentation checks
```

## Automated Testing

### Pre-Commit Hooks

```json
{
  "husky": {
    "hooks": {
      "pre-commit": "npm run docs:validate",
      "pre-push": "npm run docs:links"
    }
  }
}
```

### CI Pipeline

```yaml
- name: Validate Documentation
  run: npm run docs:validate

- name: Test Examples
  run: npm run docs:test-examples

- name: Check Links
  run: npm run docs:links
```
