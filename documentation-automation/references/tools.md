# Automated Documentation Tools

## Language-Specific Tools

| Language | Documentation Tool | Notes |
|----------|-------------------|--------|
| JavaScript | JSDoc | Standard for JS, adds type annotations |
| TypeScript | TSDoc | Native TS doc comments, generates types |
| Python | Sphinx | Full-featured, supports multiple formats |
| Python | pdoc | Simple, auto-generation from docstrings |
| Java | Javadoc | Java standard, HTML output |
| C# | xmldoc | XML-based documentation |
| Go | godoc | Go native, web-based output |
| Rust | rustdoc | Rust native, includes tests |

## Setup Examples

### JSDoc for JavaScript

```bash
npm install --save-dev jsdoc
```

```javascript
/**
 * Calculate sum of two numbers.
 * @param {number} a - First number
 * @param {number} b - Second number
 * @returns {number} Sum of a and b
 */
function add(a, b) {
  return a + b;
}
```

### TSDoc for TypeScript

```typescript
/**
 * Calculate sum of two numbers.
 * @param a - First number
 * @param b - Second number
 * @returns Sum of a and b
 */
function add(a: number, b: number): number {
  return a + b;
}
```

## Linting Tools

### Markdown Linting

```bash
npm install --save-dev markdownlint-cli
npx markdownlint "*.md"
```

### Link Checking

```bash
npm install --save-dev markdown-link-check
markdown-link-check *.md
```

### Spell Checking

```bash
npm install --save-dev cspell
cspell "**/*.md"
```
