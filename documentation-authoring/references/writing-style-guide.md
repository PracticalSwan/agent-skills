# Technical Writing Style Guide

Practical rules and patterns for clear, consistent, and inclusive technical documentation.

---

## Voice and Tone

### Active vs Passive Voice

**Prefer active voice.** It is shorter, clearer, and identifies who does what.

| Passive (avoid) | Active (prefer) |
|-----------------|-----------------|
| "The configuration file is loaded by the server." | "The server loads the configuration file." |
| "An error will be returned if the input is invalid." | "The function returns an error if the input is invalid." |
| "Tests should be run before merging." | "Run tests before merging." |

**Acceptable passive uses:**
- When the actor is unknown or irrelevant: "The bug was first reported in v2.1."
- When emphasizing the object: "All user data is encrypted at rest."
- Error messages where the system is the actor: "Your session has expired."

### Imperative Mood for Instructions

Use direct commands in procedural content:

- **Yes:** "Install the dependencies." / "Open the configuration file."
- **No:** "You should install the dependencies." / "The user needs to open the configuration file."

### Consistent Perspective

- **Guides and tutorials:** Use "you" to address the reader directly.
- **Reference docs:** Use third person ("the function returns...").
- **Avoid "we"** unless genuinely collaborative ("In this tutorial, we will build...").

---

## Sentence Structure

### Sentence Length

- **Target:** 15–25 words per sentence.
- **Maximum:** 40 words. If longer, split.
- **One idea per sentence.** Compound sentences with multiple clauses slow comprehension.

| Too long | Better |
|----------|--------|
| "When the user clicks the submit button, the form data is validated on the client side, and if validation passes, the data is sent to the server, which processes it and returns a response." | "When the user clicks Submit, the client validates the form data. If validation passes, the client sends the data to the server. The server processes the request and returns a response." |

### Front-Load Key Information

Put the most important content at the beginning of the sentence:

- **Yes:** "To deploy, run `npm run build` first."
- **No:** "Before you can deploy your application to the production server, you need to first run `npm run build`."

### Parallel Structure

Keep list items and related clauses grammatically parallel:

- **Yes:** "The API supports creating, reading, updating, and deleting records."
- **No:** "The API supports creation of records, to read records, record updates, and you can delete them."

---

## Paragraph Organization

### One Topic Per Paragraph

Each paragraph should convey a single idea. Start with a topic sentence, then support it.

### Paragraph Length

- **Target:** 3–5 sentences.
- **Maximum:** 7 sentences. Break longer paragraphs.
- Single-sentence paragraphs are acceptable for emphasis or transitions.

### Transitional Flow

Connect paragraphs logically:
- **Sequence:** "Next," "Then," "After completing this step,"
- **Contrast:** "However," "Unlike," "In contrast,"
- **Cause/Effect:** "As a result," "Because of this," "Therefore,"
- **Addition:** "Additionally," "Also," "Furthermore,"

---

## Jargon and Terminology

### Define Terms on First Use

Introduce jargon or acronyms with a definition the first time they appear in a document:

> "The API uses JWT (JSON Web Token) for authentication. Each JWT contains..."

### Use Consistent Terminology

Pick one term and stick with it throughout a document:

| Inconsistent | Consistent |
|-------------|------------|
| "endpoint" / "route" / "path" / "URL" interchangeably | Pick "endpoint" and use it everywhere |
| "click" / "tap" / "press" / "select" | Use "select" for all UI interactions, or platform-specific terms consistently |

### Avoid Unnecessary Jargon

| Jargon-heavy | Clearer |
|-------------|---------|
| "Leverage the SDK to instantiate a client" | "Use the SDK to create a client" |
| "Utilize the endpoint to facilitate data retrieval" | "Call the endpoint to get data" |

### Glossary

For documents with heavy domain terminology, include a glossary section or link to a shared glossary.

---

## Progressive Disclosure

Structure content so readers get the level of detail they need without wading through information they do not.

### The Inverted Pyramid

```
┌─────────────────────────────┐
│     Essential / Summary      │  ← Everyone reads this
├─────────────────────────────┤
│    Important Details         │  ← Most readers need this
├─────────────────────────────┤
│  Background / Deep Dive      │  ← Advanced readers explore this
└─────────────────────────────┘
```

### Techniques

1. **TL;DR at the top** — Start documents with a summary.
2. **Expandable sections** — Use `<details>` for advanced content.
3. **Layered headings** — Top-level for overview, sub-headings for depth.
4. **Cross-links** — Reference deep-dive docs instead of inlining everything.
5. **Quick-start vs Full guide** — Provide both paths.

---

## Inclusive Language

### Avoid Gendered Terms

| Avoid | Use |
|-------|-----|
| "he/she", "his/her" | "they/their" (singular they) |
| "manpower" | "workforce", "staffing" |
| "master/slave" | "primary/replica", "leader/follower" |
| "whitelist/blacklist" | "allowlist/denylist" |
| "sanity check" | "confidence check", "smoke test" |

### Avoid Ableist Language

| Avoid | Use |
|-------|-----|
| "blind to" | "unaware of" |
| "cripple" | "disable", "degrade" |
| "dumb" (component) | "silent", "passive" |

### Avoid Assumptions About Reader Expertise

- Do not write "simply", "just", "obviously", "of course". These words imply the content is trivial and alienate readers who struggle with it.
- Do not assume prior tooling knowledge without stating prerequisites.

---

## Visual Aids: Tables vs Lists vs Diagrams

### When to Use Tables

- Comparing multiple items across the same attributes
- Reference data (API parameters, config options, status codes)
- Anything with a clear row-column structure

```markdown
| Parameter | Type   | Required | Default | Description          |
|-----------|--------|----------|---------|----------------------|
| `page`    | number | No       | 1       | Page number          |
| `limit`   | number | No       | 20      | Results per page     |
```

### When to Use Lists

- Sequential steps (ordered list)
- Non-comparative collections (unordered list)
- Feature highlights or key points
- Fewer than 4 attributes per item

### When to Use Diagrams

- System architecture and component relationships
- Request/response flows or sequences
- State machines and decision trees
- Anything spatial or relational

**Diagram guidelines:**
- Use Mermaid for text-based diagrams in markdown
- Label all components and connections
- Keep diagrams focused — one concept per diagram
- Provide alt text or a text description for accessibility

---

## Formatting Conventions

### Headings

- **H1 (`#`):** Document title only — one per document
- **H2 (`##`):** Major sections
- **H3 (`###`):** Subsections
- **H4 (`####`):** Use sparingly for deeply nested content
- Never skip levels (e.g., H2 → H4 without H3)
- Use sentence case: "Configure the database" not "Configure The Database"

### Code Blocks

Always specify the language for syntax highlighting:

````markdown
```javascript
const result = await fetchData(url);
```
````

- **Inline code** (`` ` ``) for: variable names, function names, file paths, CLI commands, config values
- **Code blocks** for: multi-line code, command output, file contents, API payloads

### Callouts and Admonitions

Use consistent callout patterns:

```markdown
> **Note:** Supplementary information that adds context.

> **Tip:** Helpful suggestion that improves the experience.

> **Warning:** Important caveat that could cause issues if ignored.

> **Caution:** Action that could result in data loss or security risk.
```

### Links

- Use descriptive link text: "[Configure the database](./db-setup.md)" not "[click here](./db-setup.md)"
- Prefer relative links for internal docs
- external links should open concepts, not duplicate content

### Numbers

- Spell out one through nine; use numerals for 10 and above
- Always use numerals with units: "5 MB", "3 seconds"
- Use numerals in technical contexts: "Set `retries` to 3"

---

## Common Mistakes in Technical Writing

### 1. Wall of Text
**Problem:** Large unbroken paragraphs with no visual structure.
**Fix:** Break into paragraphs, add headings, use lists and code blocks.

### 2. Missing Context
**Problem:** Jumping into steps without explaining prerequisites or goals.
**Fix:** Always include a "Prerequisites" section and a brief overview of what the reader will accomplish.

### 3. Ambiguous Pronouns
**Problem:** "It returns the value after it processes it."
**Fix:** "The `parse()` function returns the value after the validator processes the input."

### 4. Outdated Examples
**Problem:** Code examples that no longer match the current API.
**Fix:** Test examples regularly. Include version numbers. Automate example validation.

### 5. Undocumented Error Cases
**Problem:** Only documenting the happy path.
**Fix:** Document at least the most common error scenarios with causes and solutions.

### 6. Inconsistent Formatting
**Problem:** Mixing formatting conventions within a document (some code in backticks, some in quotes).
**Fix:** Establish and follow a style guide (this document). Review before publishing.

### 7. Too Much Detail Too Soon
**Problem:** Explaining every edge case before the reader understands the basics.
**Fix:** Use progressive disclosure. Basic usage first, advanced topics later.

### 8. No Verification Step
**Problem:** Instructions that end without confirming success.
**Fix:** Always include a "Verify" or "Expected result" step after procedures.

---

## Readability Scoring

### Flesch-Kincaid Grade Level

**Target:** Grade 8–10 for general technical docs, Grade 10–12 for advanced engineering docs.

**Formula simplified:** Longer sentences and longer words raise the grade level.

**How to improve readability:**
- Shorten sentences
- Replace long words with shorter synonyms
- Break complex ideas into multiple sentences
- Use concrete examples instead of abstract explanations

### Quick Self-Check

Before publishing, read your document and ask:
1. Can a new team member follow this without asking questions?
2. Is every step actionable and verifiable?
3. Are all terms defined or linked to definitions?
4. Does the structure help scanning (headings, lists, bold key terms)?
5. Have I removed every word that does not add value?

---

## Checklist: Before Publishing

- [ ] Title clearly describes the document's purpose
- [ ] Summary/TL;DR at the top
- [ ] Prerequisites listed
- [ ] Headings follow hierarchy (no skipped levels)
- [ ] Code blocks have language tags
- [ ] All links are valid and descriptive
- [ ] No TODO/TBD/FIXME markers remain
- [ ] Examples are tested and current
- [ ] Inclusive language review complete
- [ ] Spellcheck and grammar check passed
