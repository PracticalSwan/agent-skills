# Context Map Template

Use this template when a request needs a concrete pre-edit map of the codebase.

```markdown
## Context Map

### Task
- One-sentence restatement of the requested outcome.

### Likely Edit Targets
| File | Why it matters | Expected change |
|------|----------------|-----------------|
| path/to/file | Main logic or entry point | Update implementation |

### Nearby Dependencies
| File | Relationship |
|------|--------------|
| path/to/file | Imported by or configures the main target |

### Verification Files
| File | Coverage |
|------|----------|
| path/to/test | Existing verification path |

### Reference Patterns
| File | Pattern to reuse |
|------|------------------|
| path/to/example | Similar implementation |

### Risks
- Public API or contract may change
- Config, env vars, or generated files may need updates
- Docs or changelog may need to move with the code

### Open Questions
- Anything still uncertain after discovery
```

Guidance:

- Keep the map short enough to act on quickly.
- Split by subsystem if the request spans backend, frontend, infra, or docs.
- Revise the map if discovery shows the scope is materially different from the initial assumption.
