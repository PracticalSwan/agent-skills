# React Hooks Reference (React 19+)

Quick-reference for every built-in React hook. Each entry includes signature, when to use, patterns, gotchas, and examples.

---

## Table of Contents

- [State Hooks](#state-hooks)
  - [useState](#usestate)
  - [useReducer](#usereducer)
- [Context Hooks](#context-hooks)
  - [useContext](#usecontext)
- [Ref Hooks](#ref-hooks)
  - [useRef](#useref)
  - [useImperativeHandle](#useimperativehandle)
- [Effect Hooks](#effect-hooks)
  - [useEffect](#useeffect)
  - [useLayoutEffect](#uselayouteffect)
- [Performance Hooks](#performance-hooks)
  - [useMemo](#usememo)
  - [useCallback](#usecallback)
- [Transition Hooks](#transition-hooks)
  - [useTransition](#usetransition)
  - [useDeferredValue](#usedeferredvalue)
- [Identity Hooks](#identity-hooks)
  - [useId](#useid)
- [Debug Hooks](#debug-hooks)
  - [useDebugValue](#usedebugvalue)
- [External Store Hooks](#external-store-hooks)
  - [useSyncExternalStore](#usesyncexternalstore)
- [React 19 Hooks](#react-19-hooks)
  - [use](#use)
  - [useOptimistic](#useoptimistic)
  - [useActionState](#useactionstate)
  - [useFormStatus](#useformstatus)
- [React 19 Actions](#react-19-actions)

---

## State Hooks

### useState

```ts
const [state, setState] = useState<T>(initialValue: T | (() => T)): [T, Dispatch<SetStateAction<T>>]
```

**When to use:** Local component state for primitive values, objects, or arrays.

**Common patterns:**

```tsx
// Primitive
const [count, setCount] = useState(0);

// Lazy initialization (expensive computation runs once)
const [data, setData] = useState(() => expensiveComputation());

// Functional update (when new state depends on previous)
setCount(prev => prev + 1);

// Object state
const [form, setForm] = useState({ name: '', email: '' });
setForm(prev => ({ ...prev, name: 'Alice' }));
```

**Gotchas:**
- `setState` does NOT merge objects—always spread previous state for partial updates.
- State updates are batched in React 18+/19. Multiple `setState` calls in an event handler produce one re-render.
- Initializer function runs only on mount. Don't pass a function call: `useState(fn())` runs every render; use `useState(fn)` or `useState(() => fn())`.
- Setting state to the same reference (Object.is) skips re-render.

---

### useReducer

```ts
const [state, dispatch] = useReducer<R>(
  reducer: R,
  initialArg: ReducerStateWithoutAction<R>,
  init?: (arg: ReducerStateWithoutAction<R>) => ReducerState<R>
): [ReducerState<R>, Dispatch<ReducerAction<R>>]
```

**When to use:** Complex state logic with multiple sub-values, or when next state depends on previous state with defined action types.

**Common patterns:**

```tsx
type State = { count: number; step: number };
type Action =
  | { type: 'increment' }
  | { type: 'decrement' }
  | { type: 'setStep'; payload: number };

function reducer(state: State, action: Action): State {
  switch (action.type) {
    case 'increment': return { ...state, count: state.count + state.step };
    case 'decrement': return { ...state, count: state.count - state.step };
    case 'setStep':   return { ...state, step: action.payload };
  }
}

const [state, dispatch] = useReducer(reducer, { count: 0, step: 1 });
dispatch({ type: 'increment' });
```

**Gotchas:**
- Reducer must be pure—no side effects.
- If reducer returns the same reference, React skips re-render.
- Third `init` argument enables lazy initialization: `useReducer(reducer, initialArg, init)`.

---

## Context Hooks

### useContext

```ts
const value = useContext<T>(SomeContext: React.Context<T>): T
```

**When to use:** Consume values from a `React.createContext` provider without prop drilling.

**Common patterns:**

```tsx
// Define
const ThemeContext = createContext<'light' | 'dark'>('light');

// Provide
<ThemeContext.Provider value="dark">
  <App />
</ThemeContext.Provider>

// Consume
function Button() {
  const theme = useContext(ThemeContext);
  return <button className={theme === 'dark' ? 'bg-gray-800' : 'bg-white'}>Click</button>;
}
```

**Gotchas:**
- Every consumer re-renders when the context value changes (by reference).
- Split contexts (state vs dispatch) to minimize re-renders.
- Wrap provider value in `useMemo` if it's a computed object.

---

## Ref Hooks

### useRef

```ts
const ref = useRef<T>(initialValue: T): MutableRefObject<T>
const ref = useRef<T>(null): RefObject<T>  // DOM refs
```

**When to use:** Persist mutable values across renders without triggering re-renders. DOM element references.

**Common patterns:**

```tsx
// DOM ref
const inputRef = useRef<HTMLInputElement>(null);
useEffect(() => { inputRef.current?.focus(); }, []);
return <input ref={inputRef} />;

// Mutable value (previous value, interval ID, etc.)
const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null);
```

**Gotchas:**
- Mutating `.current` does NOT cause a re-render.
- Don't read/write `.current` during rendering (except initialization).
- For callback refs, use a function: `<div ref={(node) => { /* ... */ }} />`.

---

### useImperativeHandle

```ts
useImperativeHandle<T, R extends T>(
  ref: ForwardedRef<T>,
  createHandle: () => R,
  deps?: DependencyList
): void
```

**When to use:** Customize the instance value exposed to parent components when using `forwardRef`.

**Common patterns:**

```tsx
interface InputHandle {
  focus: () => void;
  scrollIntoView: () => void;
}

const FancyInput = forwardRef<InputHandle, Props>((props, ref) => {
  const inputRef = useRef<HTMLInputElement>(null);

  useImperativeHandle(ref, () => ({
    focus: () => inputRef.current?.focus(),
    scrollIntoView: () => inputRef.current?.scrollIntoView({ behavior: 'smooth' }),
  }));

  return <input ref={inputRef} {...props} />;
});
```

**Gotchas:**
- Avoid overusing—prefer declarative patterns.
- Must be used with `forwardRef` (or React 19's ref-as-prop).
- React 19: `ref` is available as a regular prop, reducing need for `forwardRef`.

---

## Effect Hooks

### useEffect

```ts
useEffect(setup: () => (void | (() => void)), deps?: DependencyList): void
```

**When to use:** Synchronize with external systems (APIs, subscriptions, DOM manipulation, timers).

**Common patterns:**

```tsx
// Fetch data
useEffect(() => {
  const controller = new AbortController();
  fetch('/api/data', { signal: controller.signal })
    .then(res => res.json())
    .then(setData)
    .catch(err => {
      if (err.name !== 'AbortError') setError(err);
    });
  return () => controller.abort();
}, []);

// Subscribe to external store
useEffect(() => {
  const unsubscribe = store.subscribe(handleChange);
  return () => unsubscribe();
}, []);

// Run once on mount
useEffect(() => { /* ... */ }, []);

// Run on every render (rare)
useEffect(() => { /* ... */ });
```

**Gotchas:**
- Missing dependencies cause stale closures. Use the exhaustive-deps lint rule.
- Cleanup function runs before each re-execution AND on unmount.
- Effects run after paint (not before)—use `useLayoutEffect` for DOM measurements.
- In React 18+ Strict Mode, effects mount → unmount → mount in dev to surface cleanup bugs.
- Don't use effects for data that can be computed during render (use `useMemo`).
- Don't use effects to respond to events (use event handlers instead).

---

### useLayoutEffect

```ts
useLayoutEffect(setup: () => (void | (() => void)), deps?: DependencyList): void
```

**When to use:** Same as `useEffect` but fires synchronously after DOM mutations, before the browser paints. For DOM measurements and synchronous visual updates.

**Common patterns:**

```tsx
// Measure DOM and adjust layout before paint
useLayoutEffect(() => {
  const { height } = ref.current!.getBoundingClientRect();
  setTooltipPosition(height);
}, []);
```

**Gotchas:**
- Blocks visual updates—keep logic minimal.
- Prefer `useEffect` unless you see visual flickering.
- Does NOT fire on the server (SSR). Use `useEffect` for SSR-safe code.

---

## Performance Hooks

### useMemo

```ts
const memoizedValue = useMemo<T>(factory: () => T, deps: DependencyList): T
```

**When to use:** Cache expensive computations. Prevent re-creating reference values (objects, arrays) that would cause child re-renders.

**Common patterns:**

```tsx
// Expensive computation
const sorted = useMemo(() => items.sort(compareFn), [items]);

// Stable object reference for context value
const contextValue = useMemo(() => ({ user, logout }), [user, logout]);
```

**Gotchas:**
- Not a semantic guarantee—React may discard cached values under memory pressure.
- Don't use for side effects—that's what `useEffect` is for.
- Profile before adding; premature memoization adds complexity.
- React Compiler (React 19) can auto-memoize, reducing manual `useMemo` needs.

---

### useCallback

```ts
const memoizedCallback = useCallback<T extends Function>(callback: T, deps: DependencyList): T
```

**When to use:** Stabilize function references passed to memoized children (`React.memo`) or used as effect dependencies.

**Common patterns:**

```tsx
const handleClick = useCallback((id: string) => {
  setItems(prev => prev.filter(item => item.id !== id));
}, []);

// Equivalent to:
const handleClick = useMemo(() => (id: string) => {
  setItems(prev => prev.filter(item => item.id !== id));
}, []);
```

**Gotchas:**
- Only useful when the consuming component is wrapped in `React.memo` or the function is in a dependency array.
- `useCallback(fn, deps)` is syntactic sugar for `useMemo(() => fn, deps)`.
- React Compiler (React 19) can auto-memoize callbacks.

---

## Transition Hooks

### useTransition

```ts
const [isPending, startTransition] = useTransition(): [boolean, (callback: () => void) => void]
```

**When to use:** Mark state updates as non-urgent (transitions). Keeps the UI responsive during expensive re-renders.

**Common patterns:**

```tsx
const [isPending, startTransition] = useTransition();
const [query, setQuery] = useState('');
const [results, setResults] = useState<Item[]>([]);

function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
  setQuery(e.target.value); // Urgent: update input immediately
  startTransition(() => {
    setResults(filterItems(e.target.value)); // Non-urgent: can be interrupted
  });
}

return (
  <>
    <input value={query} onChange={handleChange} />
    {isPending ? <Spinner /> : <ResultsList items={results} />}
  </>
);
```

**Gotchas:**
- The callback passed to `startTransition` must be synchronous.
- Transition updates can be interrupted by urgent updates.
- In React 19, `startTransition` supports async functions (Actions).

---

### useDeferredValue

```ts
const deferredValue = useDeferredValue<T>(value: T, initialValue?: T): T
```

**When to use:** Defer re-rendering of a non-urgent part of the UI. Alternative to `useTransition` when you don't control the state update.

**Common patterns:**

```tsx
function SearchResults({ query }: { query: string }) {
  const deferredQuery = useDeferredValue(query);
  const isStale = query !== deferredQuery;

  const results = useMemo(() => filterItems(deferredQuery), [deferredQuery]);

  return (
    <div style={{ opacity: isStale ? 0.7 : 1 }}>
      <ResultsList items={results} />
    </div>
  );
}
```

**Gotchas:**
- React 19 adds optional `initialValue` parameter for initial render.
- Returns the previous value during transitions, then updates.
- Combine with `useMemo` to avoid re-computing with stale value.

---

## Identity Hooks

### useId

```ts
const id = useId(): string
```

**When to use:** Generate unique IDs for accessibility attributes (`htmlFor`, `aria-describedby`). Safe for SSR hydration.

**Common patterns:**

```tsx
function FormField({ label }: { label: string }) {
  const id = useId();
  return (
    <>
      <label htmlFor={id}>{label}</label>
      <input id={id} />
    </>
  );
}

// Multiple related IDs
function PasswordField() {
  const id = useId();
  return (
    <>
      <label htmlFor={`${id}-password`}>Password</label>
      <input id={`${id}-password`} aria-describedby={`${id}-hint`} />
      <p id={`${id}-hint`}>Must be 8+ characters</p>
    </>
  );
}
```

**Gotchas:**
- Do NOT use for list keys—use data-based keys instead.
- IDs are opaque strings (e.g., `:r1:`)—don't parse or depend on format.
- Safe across server and client (hydration-stable).

---

## Debug Hooks

### useDebugValue

```ts
useDebugValue<T>(value: T, format?: (value: T) => any): void
```

**When to use:** Display a label for custom hooks in React DevTools.

**Common patterns:**

```tsx
function useOnlineStatus(): boolean {
  const isOnline = useSyncExternalStore(subscribe, getSnapshot);
  useDebugValue(isOnline ? '🟢 Online' : '🔴 Offline');
  return isOnline;
}

// Lazy formatting (expensive computations)
useDebugValue(date, d => d.toISOString());
```

**Gotchas:**
- Only visible in React DevTools—no runtime impact.
- Use the format function to defer expensive formatting.
- Only use in custom hooks, not regular components.

---

## External Store Hooks

### useSyncExternalStore

```ts
const snapshot = useSyncExternalStore<T>(
  subscribe: (onStoreChange: () => void) => () => void,
  getSnapshot: () => T,
  getServerSnapshot?: () => T
): T
```

**When to use:** Subscribe to external data stores (Redux, Zustand, browser APIs, third-party state).

**Common patterns:**

```tsx
// Browser online status
function useOnlineStatus() {
  return useSyncExternalStore(
    (callback) => {
      window.addEventListener('online', callback);
      window.addEventListener('offline', callback);
      return () => {
        window.removeEventListener('online', callback);
        window.removeEventListener('offline', callback);
      };
    },
    () => navigator.onLine,
    () => true // Server snapshot
  );
}

// External store
const snapshot = useSyncExternalStore(
  store.subscribe,
  store.getSnapshot,
  store.getServerSnapshot
);
```

**Gotchas:**
- `getSnapshot` must return a cached/immutable value. Returning a new object each call causes infinite re-renders.
- `getServerSnapshot` is required for SSR.
- Prefer this over `useEffect` + `useState` for external subscriptions.

---

## React 19 Hooks

### use

```ts
const value = use<T>(resource: Promise<T> | Context<T>): T
```

**When to use:** Read a Promise or Context value inside a component. Unlike other hooks, `use` can be called conditionally and inside loops.

**Common patterns:**

```tsx
// Read a promise (with Suspense)
function UserProfile({ userPromise }: { userPromise: Promise<User> }) {
  const user = use(userPromise);
  return <h1>{user.name}</h1>;
}

// Wrap in Suspense
<Suspense fallback={<Spinner />}>
  <UserProfile userPromise={fetchUser(id)} />
</Suspense>

// Read context conditionally
function StatusBar({ showTheme }: { showTheme: boolean }) {
  if (showTheme) {
    const theme = use(ThemeContext);
    return <span>{theme}</span>;
  }
  return null;
}
```

**Gotchas:**
- When reading a Promise, must be wrapped in a `<Suspense>` boundary.
- The Promise must be created outside the component (in a loader, server component, or parent). Creating it during render causes infinite suspension.
- Can replace `useContext` where conditional reads are needed.
- Unlike other hooks, does NOT need to follow the rules of hooks (can be inside if/loops).

---

### useOptimistic

```ts
const [optimisticState, addOptimistic] = useOptimistic<State, Update>(
  state: State,
  updateFn: (currentState: State, optimisticValue: Update) => State
): [State, (action: Update) => void]
```

**When to use:** Show optimistic UI updates while an async action (form submission, mutation) is in progress.

**Common patterns:**

```tsx
type Message = { text: string; sending?: boolean };

function Chat({ messages, sendMessage }: Props) {
  const [optimisticMessages, addOptimistic] = useOptimistic<Message[], string>(
    messages,
    (state, newMessage) => [
      ...state,
      { text: newMessage, sending: true },
    ]
  );

  async function handleSubmit(formData: FormData) {
    const text = formData.get('message') as string;
    addOptimistic(text);
    await sendMessage(text);
  }

  return (
    <form action={handleSubmit}>
      {optimisticMessages.map((msg, i) => (
        <p key={i} style={{ opacity: msg.sending ? 0.6 : 1 }}>{msg.text}</p>
      ))}
      <input name="message" />
      <button type="submit">Send</button>
    </form>
  );
}
```

**Gotchas:**
- Optimistic state reverts automatically when the async action completes.
- Best paired with `<form action={...}>` (React 19 Actions).
- The update function must be pure.

---

### useActionState

```ts
const [state, formAction, isPending] = useActionState<State, Payload>(
  action: (previousState: State, payload: Payload) => State | Promise<State>,
  initialState: State,
  permalink?: string
): [State, (payload: Payload) => void, boolean]
```

**When to use:** Manage form state with server or client actions. Replaces the `useFormState` hook (renamed in React 19).

**Common patterns:**

```tsx
interface FormState {
  error: string | null;
  success: boolean;
}

async function submitAction(prev: FormState, formData: FormData): Promise<FormState> {
  const email = formData.get('email') as string;
  try {
    await subscribe(email);
    return { error: null, success: true };
  } catch (e) {
    return { error: (e as Error).message, success: false };
  }
}

function Newsletter() {
  const [state, action, isPending] = useActionState(submitAction, {
    error: null,
    success: false,
  });

  return (
    <form action={action}>
      <input name="email" type="email" required />
      <button disabled={isPending}>
        {isPending ? 'Subscribing...' : 'Subscribe'}
      </button>
      {state.error && <p className="text-red-500">{state.error}</p>}
      {state.success && <p className="text-green-600">Subscribed!</p>}
    </form>
  );
}
```

**Gotchas:**
- Renamed from `useFormState` in React 19.
- The action receives the previous state as first argument—useful for accumulating errors.
- `isPending` (third return value) is unique to `useActionState`—no need for separate `useTransition`.
- `permalink` is optional, used for progressive enhancement with server actions.

---

### useFormStatus

```ts
const { pending, data, method, action } = useFormStatus(): {
  pending: boolean;
  data: FormData | null;
  method: string;
  action: string | ((formData: FormData) => void) | null;
}
```

**When to use:** Read the status of a parent `<form>` from within a child component. Must be rendered inside a `<form>`.

**Common patterns:**

```tsx
function SubmitButton() {
  const { pending } = useFormStatus();
  return (
    <button type="submit" disabled={pending} className="btn">
      {pending ? 'Saving...' : 'Save'}
    </button>
  );
}

function MyForm() {
  return (
    <form action={saveAction}>
      <input name="title" />
      <SubmitButton /> {/* Must be a child of <form> */}
    </form>
  );
}
```

**Gotchas:**
- Must be called from a component rendered inside a `<form>`—will not work if called in the same component that renders the `<form>`.
- Returns status of the nearest parent `<form>`.
- Only works with React 19's `<form action={...}>` pattern.

---

## React 19 Actions

Actions are a React 19 pattern (not a hook) that enable async functions in transitions.

```tsx
// Form actions
<form action={async (formData) => {
  await saveToServer(formData);
}}>
  <input name="title" />
  <button type="submit">Save</button>
</form>

// startTransition with async
const [isPending, startTransition] = useTransition();

function handleSave() {
  startTransition(async () => {
    await saveData();
    // React waits for the async function to finish
  });
}
```

**Key points:**
- `<form action={fn}>` calls `fn` with `FormData` on submit.
- `startTransition` now accepts async functions in React 19.
- Actions automatically handle pending states, errors, and optimistic updates.
- Pair with `useActionState` for form state and `useOptimistic` for optimistic UI.

---

## Quick Decision Guide

| Need | Hook |
|------|------|
| Simple local state | `useState` |
| Complex state machine | `useReducer` |
| Shared state (no prop drilling) | `useContext` |
| DOM reference or mutable container | `useRef` |
| Side effect / sync with external system | `useEffect` |
| DOM measurement before paint | `useLayoutEffect` |
| Cache expensive computation | `useMemo` |
| Stable function reference | `useCallback` |
| Non-urgent state update | `useTransition` |
| Defer re-render of a value | `useDeferredValue` |
| SSR-safe unique IDs | `useId` |
| External store subscription | `useSyncExternalStore` |
| Read Promise or Context (conditional) | `use` |
| Optimistic UI during async mutation | `useOptimistic` |
| Form action state management | `useActionState` |
| Parent form submission status | `useFormStatus` |
