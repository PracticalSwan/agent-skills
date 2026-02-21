# React 19 JSX and API Updates (2026)

Up-to-date React 19 guidance relevant to JSX-heavy Vite apps.

## Core React 19 Patterns

### Declarative Components
- Prefer pure rendering logic in components.
- Keep side effects inside hooks (`useEffect`, `useLayoutEffect`) only when needed.
- Derive UI state from props/store where possible to reduce sync bugs.

### Form Actions and Async Flows
- Use action-oriented handlers for submit/update/delete flows.
- Keep optimistic UI updates local and reversible.
- Surface validation errors as field-level messages and general API errors separately.

### Suspense-friendly data loading
- Use route-level or boundary-level loading fallbacks.
- Split heavy subtrees with `React.lazy`.
- Avoid over-wrapping tiny components in `Suspense`.

## JSX Composition Patterns

```jsx
function RecipeSection({ title, children }) {
    return (
        <section className="space-y-3">
            <h2 className="text-lg font-semibold">{title}</h2>
            <div>{children}</div>
        </section>
    );
}

function RecipeMeta({ prepTime, cookTime, servings }) {
    return (
        <dl className="grid grid-cols-3 gap-2 text-sm">
            <div><dt>Prep</dt><dd>{prepTime} min</dd></div>
            <div><dt>Cook</dt><dd>{cookTime} min</dd></div>
            <div><dt>Servings</dt><dd>{servings}</dd></div>
        </dl>
    );
}
```

## Performance Notes
- Use stable keys from database IDs.
- Avoid unnecessary derived arrays in render; memoize expensive transforms.
- Prefer coarse memoization at list/section boundaries.
- Keep callback identity stable only when it prevents real rerenders.

## Accessibility Notes
- Ensure interactive controls are real `button`/`a` elements.
- Provide labels/`aria-label` for icon-only buttons.
- Use semantic headings and landmark regions.
- Ensure modal/dialog focus management and escape handling.

## References
- React docs: https://react.dev/
- React API reference: https://react.dev/reference/react
- Accessibility: https://react.dev/learn/accessibility
