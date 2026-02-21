# Custom React Hooks Gallery

Production-ready custom hooks with full TypeScript, usage examples, and test patterns.

---

## Table of Contents

- [useDebounce](#usedebounce)
- [useLocalStorage](#uselocalstorage)
- [useFetch](#usefetch)
- [useMediaQuery](#usemediaquery)
- [useOnClickOutside](#useonclickoutside)
- [useKeyPress](#usekeypress)
- [usePrevious](#useprevious)
- [useIntersectionObserver](#useintersectionobserver)
- [useClipboard](#useclipboard)
- [useToggle](#usetoggle)
- [useEventListener](#useeventlistener)
- [usePagination](#usepagination)

---

## useDebounce

Debounce a rapidly changing value. Useful for search inputs, resize handlers, and API calls.

### Implementation

```ts
import { useState, useEffect } from 'react';

export function useDebounce<T>(value: T, delay: number = 300): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value);

  useEffect(() => {
    const timer = setTimeout(() => setDebouncedValue(value), delay);
    return () => clearTimeout(timer);
  }, [value, delay]);

  return debouncedValue;
}
```

### Usage

```tsx
function SearchInput() {
  const [query, setQuery] = useState('');
  const debouncedQuery = useDebounce(query, 500);

  useEffect(() => {
    if (debouncedQuery) {
      searchApi(debouncedQuery).then(setResults);
    }
  }, [debouncedQuery]);

  return <input value={query} onChange={(e) => setQuery(e.target.value)} />;
}
```

### Test

```ts
import { renderHook, act } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import { useDebounce } from './useDebounce';

describe('useDebounce', () => {
  beforeEach(() => { vi.useFakeTimers(); });
  afterEach(() => { vi.useRealTimers(); });

  it('returns initial value immediately', () => {
    const { result } = renderHook(() => useDebounce('hello', 300));
    expect(result.current).toBe('hello');
  });

  it('debounces value changes', () => {
    const { result, rerender } = renderHook(
      ({ value }) => useDebounce(value, 300),
      { initialProps: { value: 'a' } }
    );

    rerender({ value: 'ab' });
    expect(result.current).toBe('a');

    act(() => { vi.advanceTimersByTime(300); });
    expect(result.current).toBe('ab');
  });

  it('resets timer on rapid changes', () => {
    const { result, rerender } = renderHook(
      ({ value }) => useDebounce(value, 300),
      { initialProps: { value: 'a' } }
    );

    rerender({ value: 'ab' });
    act(() => { vi.advanceTimersByTime(200); });
    rerender({ value: 'abc' });
    act(() => { vi.advanceTimersByTime(200); });
    expect(result.current).toBe('a');

    act(() => { vi.advanceTimersByTime(100); });
    expect(result.current).toBe('abc');
  });
});
```

---

## useLocalStorage

Persist state in `localStorage` with type safety and SSR compatibility.

### Types

```ts
type SetValue<T> = T | ((prevValue: T) => T);
```

### Implementation

```ts
import { useState, useCallback, useEffect } from 'react';

export function useLocalStorage<T>(
  key: string,
  initialValue: T
): [T, (value: SetValue<T>) => void, () => void] {
  const readValue = useCallback((): T => {
    if (typeof window === 'undefined') return initialValue;
    try {
      const item = window.localStorage.getItem(key);
      return item ? (JSON.parse(item) as T) : initialValue;
    } catch {
      return initialValue;
    }
  }, [key, initialValue]);

  const [storedValue, setStoredValue] = useState<T>(readValue);

  const setValue = useCallback(
    (value: SetValue<T>) => {
      try {
        const newValue = value instanceof Function ? value(storedValue) : value;
        window.localStorage.setItem(key, JSON.stringify(newValue));
        setStoredValue(newValue);
        window.dispatchEvent(new StorageEvent('storage', { key }));
      } catch (error) {
        console.warn(`Error setting localStorage key "${key}":`, error);
      }
    },
    [key, storedValue]
  );

  const removeValue = useCallback(() => {
    try {
      window.localStorage.removeItem(key);
      setStoredValue(initialValue);
    } catch (error) {
      console.warn(`Error removing localStorage key "${key}":`, error);
    }
  }, [key, initialValue]);

  // Sync across tabs
  useEffect(() => {
    function handleStorageChange(e: StorageEvent) {
      if (e.key === key) setStoredValue(readValue());
    }
    window.addEventListener('storage', handleStorageChange);
    return () => window.removeEventListener('storage', handleStorageChange);
  }, [key, readValue]);

  return [storedValue, setValue, removeValue];
}
```

### Usage

```tsx
function ThemeToggle() {
  const [theme, setTheme] = useLocalStorage<'light' | 'dark'>('theme', 'light');

  return (
    <button onClick={() => setTheme((prev) => (prev === 'light' ? 'dark' : 'light'))}>
      Current: {theme}
    </button>
  );
}
```

### Test

```ts
import { renderHook, act } from '@testing-library/react';
import { describe, it, expect, beforeEach } from 'vitest';
import { useLocalStorage } from './useLocalStorage';

describe('useLocalStorage', () => {
  beforeEach(() => { localStorage.clear(); });

  it('returns initial value when key does not exist', () => {
    const { result } = renderHook(() => useLocalStorage('test', 'default'));
    expect(result.current[0]).toBe('default');
  });

  it('persists value to localStorage', () => {
    const { result } = renderHook(() => useLocalStorage('test', 'default'));
    act(() => { result.current[1]('updated'); });
    expect(result.current[0]).toBe('updated');
    expect(JSON.parse(localStorage.getItem('test')!)).toBe('updated');
  });

  it('supports functional updates', () => {
    const { result } = renderHook(() => useLocalStorage('count', 0));
    act(() => { result.current[1]((prev) => prev + 1); });
    expect(result.current[0]).toBe(1);
  });

  it('removes value', () => {
    const { result } = renderHook(() => useLocalStorage('test', 'default'));
    act(() => { result.current[1]('value'); });
    act(() => { result.current[2](); });
    expect(result.current[0]).toBe('default');
    expect(localStorage.getItem('test')).toBeNull();
  });
});
```

---

## useFetch

Data fetching with AbortController, loading/error states, and refetch capability.

### Types

```ts
interface FetchState<T> {
  data: T | null;
  error: Error | null;
  isLoading: boolean;
}

interface UseFetchReturn<T> extends FetchState<T> {
  refetch: () => void;
}
```

### Implementation

```ts
import { useState, useEffect, useCallback, useRef } from 'react';

export function useFetch<T>(url: string | null, options?: RequestInit): UseFetchReturn<T> {
  const [state, setState] = useState<FetchState<T>>({
    data: null,
    error: null,
    isLoading: !!url,
  });
  const abortControllerRef = useRef<AbortController | null>(null);
  const [fetchCount, setFetchCount] = useState(0);

  const refetch = useCallback(() => setFetchCount((c) => c + 1), []);

  useEffect(() => {
    if (!url) {
      setState({ data: null, error: null, isLoading: false });
      return;
    }

    abortControllerRef.current?.abort();
    const controller = new AbortController();
    abortControllerRef.current = controller;

    setState((prev) => ({ ...prev, isLoading: true, error: null }));

    fetch(url, { ...options, signal: controller.signal })
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}: ${res.statusText}`);
        return res.json() as Promise<T>;
      })
      .then((data) => {
        if (!controller.signal.aborted) {
          setState({ data, error: null, isLoading: false });
        }
      })
      .catch((error) => {
        if (!controller.signal.aborted) {
          setState({ data: null, error: error as Error, isLoading: false });
        }
      });

    return () => controller.abort();
  }, [url, fetchCount]); // eslint-disable-line react-hooks/exhaustive-deps

  return { ...state, refetch };
}
```

### Usage

```tsx
function UserProfile({ userId }: { userId: string }) {
  const { data: user, isLoading, error, refetch } = useFetch<User>(
    `/api/users/${userId}`
  );

  if (isLoading) return <Spinner />;
  if (error) return <ErrorBanner message={error.message} onRetry={refetch} />;
  if (!user) return null;

  return <h1>{user.name}</h1>;
}
```

### Test

```ts
import { renderHook, waitFor } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { useFetch } from './useFetch';

describe('useFetch', () => {
  beforeEach(() => { vi.restoreAllMocks(); });

  it('fetches data successfully', async () => {
    vi.spyOn(global, 'fetch').mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve({ id: 1, name: 'Test' }),
    } as Response);

    const { result } = renderHook(() => useFetch<{ id: number; name: string }>('/api/test'));

    expect(result.current.isLoading).toBe(true);

    await waitFor(() => expect(result.current.isLoading).toBe(false));
    expect(result.current.data).toEqual({ id: 1, name: 'Test' });
    expect(result.current.error).toBeNull();
  });

  it('handles fetch errors', async () => {
    vi.spyOn(global, 'fetch').mockResolvedValueOnce({
      ok: false,
      status: 404,
      statusText: 'Not Found',
    } as Response);

    const { result } = renderHook(() => useFetch('/api/missing'));
    await waitFor(() => expect(result.current.isLoading).toBe(false));
    expect(result.current.error?.message).toContain('404');
  });

  it('returns idle state for null URL', () => {
    const { result } = renderHook(() => useFetch(null));
    expect(result.current.isLoading).toBe(false);
    expect(result.current.data).toBeNull();
  });
});
```

---

## useMediaQuery

Reactive CSS media query matching with SSR safety.

### Implementation

```ts
import { useState, useEffect } from 'react';

export function useMediaQuery(query: string): boolean {
  const [matches, setMatches] = useState<boolean>(() => {
    if (typeof window === 'undefined') return false;
    return window.matchMedia(query).matches;
  });

  useEffect(() => {
    const mediaQuery = window.matchMedia(query);
    setMatches(mediaQuery.matches);

    function handleChange(e: MediaQueryListEvent) {
      setMatches(e.matches);
    }

    mediaQuery.addEventListener('change', handleChange);
    return () => mediaQuery.removeEventListener('change', handleChange);
  }, [query]);

  return matches;
}
```

### Usage

```tsx
function ResponsiveLayout() {
  const isMobile = useMediaQuery('(max-width: 768px)');
  const prefersDark = useMediaQuery('(prefers-color-scheme: dark)');

  return (
    <div className={prefersDark ? 'dark' : ''}>
      {isMobile ? <MobileNav /> : <DesktopNav />}
    </div>
  );
}
```

### Test

```ts
import { renderHook, act } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import { useMediaQuery } from './useMediaQuery';

describe('useMediaQuery', () => {
  it('returns initial match state', () => {
    const listeners: Array<(e: { matches: boolean }) => void> = [];
    vi.spyOn(window, 'matchMedia').mockReturnValue({
      matches: true,
      addEventListener: (_: string, fn: any) => listeners.push(fn),
      removeEventListener: vi.fn(),
    } as any);

    const { result } = renderHook(() => useMediaQuery('(min-width: 768px)'));
    expect(result.current).toBe(true);
  });

  it('updates when media query changes', () => {
    const listeners: Array<(e: { matches: boolean }) => void> = [];
    vi.spyOn(window, 'matchMedia').mockReturnValue({
      matches: false,
      addEventListener: (_: string, fn: any) => listeners.push(fn),
      removeEventListener: vi.fn(),
    } as any);

    const { result } = renderHook(() => useMediaQuery('(min-width: 768px)'));
    expect(result.current).toBe(false);

    act(() => { listeners.forEach((fn) => fn({ matches: true })); });
    expect(result.current).toBe(true);
  });
});
```

---

## useOnClickOutside

Detect clicks outside a referenced element. Useful for dropdowns, popovers, and modals.

### Implementation

```ts
import { useEffect, type RefObject } from 'react';

type EventType = MouseEvent | TouchEvent;

export function useOnClickOutside<T extends HTMLElement>(
  ref: RefObject<T | null>,
  handler: (event: EventType) => void
): void {
  useEffect(() => {
    function listener(event: EventType) {
      const el = ref.current;
      if (!el || el.contains(event.target as Node)) return;
      handler(event);
    }

    document.addEventListener('mousedown', listener);
    document.addEventListener('touchstart', listener);

    return () => {
      document.removeEventListener('mousedown', listener);
      document.removeEventListener('touchstart', listener);
    };
  }, [ref, handler]);
}
```

### Usage

```tsx
function Dropdown() {
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  useOnClickOutside(dropdownRef, () => setIsOpen(false));

  return (
    <div ref={dropdownRef}>
      <button onClick={() => setIsOpen(!isOpen)}>Toggle</button>
      {isOpen && <div className="absolute mt-2 rounded border bg-white p-4 shadow">Menu</div>}
    </div>
  );
}
```

### Test

```ts
import { render, screen, fireEvent } from '@testing-library/react';
import { useRef, useState } from 'react';
import { describe, it, expect, vi } from 'vitest';
import { useOnClickOutside } from './useOnClickOutside';

function TestComponent({ onClickOutside }: { onClickOutside: () => void }) {
  const ref = useRef<HTMLDivElement>(null);
  useOnClickOutside(ref, onClickOutside);
  return (
    <div>
      <div ref={ref} data-testid="inside">Inside</div>
      <div data-testid="outside">Outside</div>
    </div>
  );
}

describe('useOnClickOutside', () => {
  it('calls handler on outside click', () => {
    const handler = vi.fn();
    render(<TestComponent onClickOutside={handler} />);
    fireEvent.mouseDown(screen.getByTestId('outside'));
    expect(handler).toHaveBeenCalledTimes(1);
  });

  it('does not call handler on inside click', () => {
    const handler = vi.fn();
    render(<TestComponent onClickOutside={handler} />);
    fireEvent.mouseDown(screen.getByTestId('inside'));
    expect(handler).not.toHaveBeenCalled();
  });
});
```

---

## useKeyPress

Detect specific key presses with modifier support.

### Implementation

```ts
import { useState, useEffect, useCallback } from 'react';

interface KeyPressOptions {
  target?: EventTarget;
  ctrlKey?: boolean;
  shiftKey?: boolean;
  altKey?: boolean;
  metaKey?: boolean;
}

export function useKeyPress(targetKey: string, options: KeyPressOptions = {}): boolean {
  const [isPressed, setIsPressed] = useState(false);
  const { target = window, ctrlKey, shiftKey, altKey, metaKey } = options;

  const matchesModifiers = useCallback(
    (event: KeyboardEvent): boolean => {
      if (ctrlKey !== undefined && event.ctrlKey !== ctrlKey) return false;
      if (shiftKey !== undefined && event.shiftKey !== shiftKey) return false;
      if (altKey !== undefined && event.altKey !== altKey) return false;
      if (metaKey !== undefined && event.metaKey !== metaKey) return false;
      return true;
    },
    [ctrlKey, shiftKey, altKey, metaKey]
  );

  useEffect(() => {
    function handleDown(e: Event) {
      const event = e as KeyboardEvent;
      if (event.key === targetKey && matchesModifiers(event)) {
        setIsPressed(true);
      }
    }

    function handleUp(e: Event) {
      const event = e as KeyboardEvent;
      if (event.key === targetKey) {
        setIsPressed(false);
      }
    }

    target.addEventListener('keydown', handleDown);
    target.addEventListener('keyup', handleUp);

    return () => {
      target.removeEventListener('keydown', handleDown);
      target.removeEventListener('keyup', handleUp);
    };
  }, [targetKey, target, matchesModifiers]);

  return isPressed;
}
```

### Usage

```tsx
function ShortcutDemo() {
  const isEscPressed = useKeyPress('Escape');
  const isSavePressed = useKeyPress('s', { ctrlKey: true });

  useEffect(() => {
    if (isSavePressed) {
      saveDocument();
    }
  }, [isSavePressed]);

  return <div>{isEscPressed && <p>Escape pressed!</p>}</div>;
}
```

### Test

```ts
import { renderHook, act } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { useKeyPress } from './useKeyPress';

describe('useKeyPress', () => {
  it('detects key press and release', () => {
    const { result } = renderHook(() => useKeyPress('Enter'));
    expect(result.current).toBe(false);

    act(() => {
      window.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter' }));
    });
    expect(result.current).toBe(true);

    act(() => {
      window.dispatchEvent(new KeyboardEvent('keyup', { key: 'Enter' }));
    });
    expect(result.current).toBe(false);
  });

  it('respects modifier keys', () => {
    const { result } = renderHook(() => useKeyPress('s', { ctrlKey: true }));

    act(() => {
      window.dispatchEvent(new KeyboardEvent('keydown', { key: 's', ctrlKey: false }));
    });
    expect(result.current).toBe(false);

    act(() => {
      window.dispatchEvent(new KeyboardEvent('keydown', { key: 's', ctrlKey: true }));
    });
    expect(result.current).toBe(true);
  });
});
```

---

## usePrevious

Track the previous value of a prop or state across renders.

### Implementation

```ts
import { useRef, useEffect } from 'react';

export function usePrevious<T>(value: T): T | undefined {
  const ref = useRef<T | undefined>(undefined);

  useEffect(() => {
    ref.current = value;
  }, [value]);

  return ref.current;
}
```

### Usage

```tsx
function Counter() {
  const [count, setCount] = useState(0);
  const prevCount = usePrevious(count);

  return (
    <div>
      <p>Current: {count}, Previous: {prevCount ?? 'N/A'}</p>
      <button onClick={() => setCount((c) => c + 1)}>Increment</button>
    </div>
  );
}
```

### Test

```ts
import { renderHook } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { usePrevious } from './usePrevious';

describe('usePrevious', () => {
  it('returns undefined on first render', () => {
    const { result } = renderHook(() => usePrevious(0));
    expect(result.current).toBeUndefined();
  });

  it('returns previous value after update', () => {
    const { result, rerender } = renderHook(({ value }) => usePrevious(value), {
      initialProps: { value: 1 },
    });

    expect(result.current).toBeUndefined();
    rerender({ value: 2 });
    expect(result.current).toBe(1);
    rerender({ value: 3 });
    expect(result.current).toBe(2);
  });
});
```

---

## useIntersectionObserver

Observe element visibility using the Intersection Observer API. Useful for lazy loading, infinite scroll, and animations.

### Types

```ts
interface UseIntersectionObserverOptions extends IntersectionObserverInit {
  freezeOnceVisible?: boolean;
}
```

### Implementation

```ts
import { useState, useEffect, useRef, type RefObject } from 'react';

export function useIntersectionObserver<T extends HTMLElement>(
  options: UseIntersectionObserverOptions = {}
): [RefObject<T | null>, IntersectionObserverEntry | null] {
  const { threshold = 0, root = null, rootMargin = '0px', freezeOnceVisible = false } = options;
  const ref = useRef<T | null>(null);
  const [entry, setEntry] = useState<IntersectionObserverEntry | null>(null);

  const frozen = entry?.isIntersecting && freezeOnceVisible;

  useEffect(() => {
    const node = ref.current;
    if (!node || frozen) return;

    const observer = new IntersectionObserver(
      ([entry]) => setEntry(entry),
      { threshold, root, rootMargin }
    );

    observer.observe(node);
    return () => observer.disconnect();
  }, [threshold, root, rootMargin, frozen]);

  return [ref, entry];
}
```

### Usage

```tsx
function LazyImage({ src, alt }: { src: string; alt: string }) {
  const [ref, entry] = useIntersectionObserver<HTMLDivElement>({
    threshold: 0.1,
    freezeOnceVisible: true,
  });

  const isVisible = entry?.isIntersecting ?? false;

  return (
    <div ref={ref} className="min-h-[200px]">
      {isVisible ? (
        <img src={src} alt={alt} className="h-auto w-full" />
      ) : (
        <div className="h-[200px] animate-pulse bg-gray-200" />
      )}
    </div>
  );
}

// Infinite scroll trigger
function InfiniteList({ loadMore }: { loadMore: () => void }) {
  const [ref, entry] = useIntersectionObserver<HTMLDivElement>();

  useEffect(() => {
    if (entry?.isIntersecting) loadMore();
  }, [entry?.isIntersecting, loadMore]);

  return <div ref={ref} className="h-4" />;
}
```

### Test

```ts
import { renderHook } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { useIntersectionObserver } from './useIntersectionObserver';

describe('useIntersectionObserver', () => {
  const observeMock = vi.fn();
  const disconnectMock = vi.fn();

  beforeEach(() => {
    vi.stubGlobal('IntersectionObserver', vi.fn((cb) => ({
      observe: observeMock,
      disconnect: disconnectMock,
      unobserve: vi.fn(),
    })));
  });

  it('returns a ref and null entry initially', () => {
    const { result } = renderHook(() => useIntersectionObserver());
    expect(result.current[0]).toBeDefined();
    expect(result.current[1]).toBeNull();
  });

  it('disconnects on unmount', () => {
    const { unmount } = renderHook(() => useIntersectionObserver());
    unmount();
    expect(disconnectMock).toHaveBeenCalled();
  });
});
```

---

## useClipboard

Copy text to clipboard with a temporary "copied" state.

### Types

```ts
interface UseClipboardReturn {
  copy: (text: string) => Promise<void>;
  isCopied: boolean;
  error: Error | null;
}
```

### Implementation

```ts
import { useState, useCallback, useRef } from 'react';

export function useClipboard(resetDelay: number = 2000): UseClipboardReturn {
  const [isCopied, setIsCopied] = useState(false);
  const [error, setError] = useState<Error | null>(null);
  const timeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  const copy = useCallback(
    async (text: string) => {
      try {
        await navigator.clipboard.writeText(text);
        setIsCopied(true);
        setError(null);

        if (timeoutRef.current) clearTimeout(timeoutRef.current);
        timeoutRef.current = setTimeout(() => setIsCopied(false), resetDelay);
      } catch (err) {
        setError(err instanceof Error ? err : new Error('Failed to copy'));
        setIsCopied(false);
      }
    },
    [resetDelay]
  );

  return { copy, isCopied, error };
}
```

### Usage

```tsx
function CopyButton({ text }: { text: string }) {
  const { copy, isCopied } = useClipboard();

  return (
    <button
      onClick={() => copy(text)}
      className="rounded border px-3 py-1 text-sm"
    >
      {isCopied ? 'Copied!' : 'Copy'}
    </button>
  );
}
```

### Test

```ts
import { renderHook, act } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { useClipboard } from './useClipboard';

describe('useClipboard', () => {
  beforeEach(() => {
    Object.assign(navigator, {
      clipboard: { writeText: vi.fn().mockResolvedValue(undefined) },
    });
    vi.useFakeTimers();
  });

  afterEach(() => { vi.useRealTimers(); });

  it('copies text and sets isCopied', async () => {
    const { result } = renderHook(() => useClipboard());
    await act(async () => { await result.current.copy('hello'); });
    expect(result.current.isCopied).toBe(true);
    expect(navigator.clipboard.writeText).toHaveBeenCalledWith('hello');
  });

  it('resets isCopied after delay', async () => {
    const { result } = renderHook(() => useClipboard(1000));
    await act(async () => { await result.current.copy('hello'); });
    expect(result.current.isCopied).toBe(true);
    act(() => { vi.advanceTimersByTime(1000); });
    expect(result.current.isCopied).toBe(false);
  });

  it('handles clipboard errors', async () => {
    (navigator.clipboard.writeText as any).mockRejectedValueOnce(new Error('Denied'));
    const { result } = renderHook(() => useClipboard());
    await act(async () => { await result.current.copy('fail'); });
    expect(result.current.isCopied).toBe(false);
    expect(result.current.error?.message).toBe('Denied');
  });
});
```

---

## useToggle

Boolean toggle state with explicit set/reset.

### Implementation

```ts
import { useState, useCallback } from 'react';

export function useToggle(
  initialValue: boolean = false
): [boolean, () => void, (value: boolean) => void] {
  const [value, setValue] = useState(initialValue);

  const toggle = useCallback(() => setValue((v) => !v), []);
  const set = useCallback((newValue: boolean) => setValue(newValue), []);

  return [value, toggle, set];
}
```

### Usage

```tsx
function Disclosure() {
  const [isOpen, toggle] = useToggle(false);

  return (
    <div>
      <button onClick={toggle} aria-expanded={isOpen}>
        {isOpen ? 'Hide' : 'Show'} Details
      </button>
      {isOpen && <p>Hidden content revealed.</p>}
    </div>
  );
}
```

### Test

```ts
import { renderHook, act } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { useToggle } from './useToggle';

describe('useToggle', () => {
  it('initializes with default value', () => {
    const { result } = renderHook(() => useToggle());
    expect(result.current[0]).toBe(false);
  });

  it('toggles value', () => {
    const { result } = renderHook(() => useToggle(false));
    act(() => { result.current[1](); });
    expect(result.current[0]).toBe(true);
    act(() => { result.current[1](); });
    expect(result.current[0]).toBe(false);
  });

  it('sets explicit value', () => {
    const { result } = renderHook(() => useToggle(false));
    act(() => { result.current[2](true); });
    expect(result.current[0]).toBe(true);
    act(() => { result.current[2](true); });
    expect(result.current[0]).toBe(true);
  });
});
```

---

## useEventListener

Type-safe wrapper for `addEventListener` with automatic cleanup.

### Implementation

```ts
import { useEffect, useRef } from 'react';

export function useEventListener<K extends keyof WindowEventMap>(
  eventName: K,
  handler: (event: WindowEventMap[K]) => void,
  element?: undefined,
  options?: boolean | AddEventListenerOptions
): void;
export function useEventListener<
  K extends keyof HTMLElementEventMap,
  T extends HTMLElement
>(
  eventName: K,
  handler: (event: HTMLElementEventMap[K]) => void,
  element: React.RefObject<T>,
  options?: boolean | AddEventListenerOptions
): void;
export function useEventListener(
  eventName: string,
  handler: (event: Event) => void,
  element?: React.RefObject<HTMLElement>,
  options?: boolean | AddEventListenerOptions
): void {
  const savedHandler = useRef(handler);

  useEffect(() => {
    savedHandler.current = handler;
  }, [handler]);

  useEffect(() => {
    const target = element?.current ?? window;

    function eventListener(event: Event) {
      savedHandler.current(event);
    }

    target.addEventListener(eventName, eventListener, options);
    return () => target.removeEventListener(eventName, eventListener, options);
  }, [eventName, element, options]);
}
```

### Usage

```tsx
function ScrollTracker() {
  const [scrollY, setScrollY] = useState(0);

  useEventListener('scroll', () => {
    setScrollY(window.scrollY);
  });

  return <div className="fixed top-0 right-0 p-2 text-xs">Scroll: {scrollY}px</div>;
}

// On a specific element
function HoverCard() {
  const cardRef = useRef<HTMLDivElement>(null);
  const [isHovered, setIsHovered] = useState(false);

  useEventListener('mouseenter', () => setIsHovered(true), cardRef);
  useEventListener('mouseleave', () => setIsHovered(false), cardRef);

  return (
    <div ref={cardRef} className={isHovered ? 'shadow-lg scale-105' : 'shadow'}>
      Hover me
    </div>
  );
}
```

### Test

```ts
import { renderHook } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import { useEventListener } from './useEventListener';

describe('useEventListener', () => {
  it('adds and removes window event listener', () => {
    const addSpy = vi.spyOn(window, 'addEventListener');
    const removeSpy = vi.spyOn(window, 'removeEventListener');
    const handler = vi.fn();

    const { unmount } = renderHook(() => useEventListener('resize', handler));
    expect(addSpy).toHaveBeenCalledWith('resize', expect.any(Function), undefined);

    unmount();
    expect(removeSpy).toHaveBeenCalledWith('resize', expect.any(Function), undefined);

    addSpy.mockRestore();
    removeSpy.mockRestore();
  });

  it('uses latest handler without re-attaching listener', () => {
    const addSpy = vi.spyOn(window, 'addEventListener');
    const handler1 = vi.fn();
    const handler2 = vi.fn();

    const { rerender } = renderHook(
      ({ handler }) => useEventListener('click', handler),
      { initialProps: { handler: handler1 } }
    );

    const callCount = addSpy.mock.calls.length;
    rerender({ handler: handler2 });

    // Listener should not be re-attached
    expect(addSpy.mock.calls.length).toBe(callCount);
    addSpy.mockRestore();
  });
});
```

---

## usePagination

Client-side pagination logic with page calculations and navigation helpers.

### Types

```ts
interface UsePaginationOptions {
  totalItems: number;
  itemsPerPage?: number;
  initialPage?: number;
  siblingCount?: number;
}

interface UsePaginationReturn {
  currentPage: number;
  totalPages: number;
  startIndex: number;
  endIndex: number;
  hasPrev: boolean;
  hasNext: boolean;
  pages: (number | 'ellipsis')[];
  goToPage: (page: number) => void;
  nextPage: () => void;
  prevPage: () => void;
}
```

### Implementation

```ts
import { useState, useMemo, useCallback } from 'react';

function generatePageRange(
  currentPage: number,
  totalPages: number,
  siblingCount: number
): (number | 'ellipsis')[] {
  const totalSlots = siblingCount * 2 + 5; // siblings + first + last + current + 2 ellipses

  if (totalPages <= totalSlots) {
    return Array.from({ length: totalPages }, (_, i) => i + 1);
  }

  const leftSiblingIndex = Math.max(currentPage - siblingCount, 1);
  const rightSiblingIndex = Math.min(currentPage + siblingCount, totalPages);

  const showLeftEllipsis = leftSiblingIndex > 2;
  const showRightEllipsis = rightSiblingIndex < totalPages - 1;

  if (!showLeftEllipsis && showRightEllipsis) {
    const leftRange = Array.from({ length: 3 + 2 * siblingCount }, (_, i) => i + 1);
    return [...leftRange, 'ellipsis', totalPages];
  }

  if (showLeftEllipsis && !showRightEllipsis) {
    const rightRange = Array.from(
      { length: 3 + 2 * siblingCount },
      (_, i) => totalPages - (3 + 2 * siblingCount) + i + 1
    );
    return [1, 'ellipsis', ...rightRange];
  }

  const middleRange = Array.from(
    { length: rightSiblingIndex - leftSiblingIndex + 1 },
    (_, i) => leftSiblingIndex + i
  );
  return [1, 'ellipsis', ...middleRange, 'ellipsis', totalPages];
}

export function usePagination({
  totalItems,
  itemsPerPage = 10,
  initialPage = 1,
  siblingCount = 1,
}: UsePaginationOptions): UsePaginationReturn {
  const [currentPage, setCurrentPage] = useState(initialPage);
  const totalPages = Math.max(1, Math.ceil(totalItems / itemsPerPage));

  const safePage = Math.min(Math.max(1, currentPage), totalPages);
  if (safePage !== currentPage) setCurrentPage(safePage);

  const goToPage = useCallback(
    (page: number) => setCurrentPage(Math.max(1, Math.min(page, totalPages))),
    [totalPages]
  );

  const nextPage = useCallback(
    () => setCurrentPage((p) => Math.min(p + 1, totalPages)),
    [totalPages]
  );

  const prevPage = useCallback(
    () => setCurrentPage((p) => Math.max(p - 1, 1)),
    []
  );

  const pages = useMemo(
    () => generatePageRange(safePage, totalPages, siblingCount),
    [safePage, totalPages, siblingCount]
  );

  return {
    currentPage: safePage,
    totalPages,
    startIndex: (safePage - 1) * itemsPerPage,
    endIndex: Math.min(safePage * itemsPerPage, totalItems),
    hasPrev: safePage > 1,
    hasNext: safePage < totalPages,
    pages,
    goToPage,
    nextPage,
    prevPage,
  };
}
```

### Usage

```tsx
function PaginatedList<T>({ items, renderItem }: { items: T[]; renderItem: (item: T) => ReactNode }) {
  const {
    currentPage, totalPages, startIndex, endIndex,
    hasPrev, hasNext, pages, goToPage, nextPage, prevPage,
  } = usePagination({ totalItems: items.length, itemsPerPage: 10 });

  const visibleItems = items.slice(startIndex, endIndex);

  return (
    <div>
      <ul>{visibleItems.map(renderItem)}</ul>

      <nav aria-label="Pagination" className="mt-4 flex items-center gap-1">
        <button onClick={prevPage} disabled={!hasPrev} className="rounded px-3 py-1 disabled:opacity-50">
          Prev
        </button>

        {pages.map((page, i) =>
          page === 'ellipsis' ? (
            <span key={`ellipsis-${i}`} className="px-2">...</span>
          ) : (
            <button
              key={page}
              onClick={() => goToPage(page)}
              className={`rounded px-3 py-1 ${page === currentPage ? 'bg-blue-600 text-white' : 'hover:bg-gray-100'}`}
              aria-current={page === currentPage ? 'page' : undefined}
            >
              {page}
            </button>
          )
        )}

        <button onClick={nextPage} disabled={!hasNext} className="rounded px-3 py-1 disabled:opacity-50">
          Next
        </button>
      </nav>

      <p className="mt-2 text-sm text-gray-500">
        Page {currentPage} of {totalPages}
      </p>
    </div>
  );
}
```

### Test

```ts
import { renderHook, act } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { usePagination } from './usePagination';

describe('usePagination', () => {
  it('calculates pages correctly', () => {
    const { result } = renderHook(() =>
      usePagination({ totalItems: 50, itemsPerPage: 10 })
    );
    expect(result.current.totalPages).toBe(5);
    expect(result.current.currentPage).toBe(1);
    expect(result.current.startIndex).toBe(0);
    expect(result.current.endIndex).toBe(10);
    expect(result.current.hasPrev).toBe(false);
    expect(result.current.hasNext).toBe(true);
  });

  it('navigates to next page', () => {
    const { result } = renderHook(() =>
      usePagination({ totalItems: 50, itemsPerPage: 10 })
    );
    act(() => { result.current.nextPage(); });
    expect(result.current.currentPage).toBe(2);
    expect(result.current.startIndex).toBe(10);
    expect(result.current.hasPrev).toBe(true);
  });

  it('does not go below page 1', () => {
    const { result } = renderHook(() =>
      usePagination({ totalItems: 50, itemsPerPage: 10 })
    );
    act(() => { result.current.prevPage(); });
    expect(result.current.currentPage).toBe(1);
  });

  it('does not go above total pages', () => {
    const { result } = renderHook(() =>
      usePagination({ totalItems: 50, itemsPerPage: 10, initialPage: 5 })
    );
    act(() => { result.current.nextPage(); });
    expect(result.current.currentPage).toBe(5);
  });

  it('navigates to arbitrary page', () => {
    const { result } = renderHook(() =>
      usePagination({ totalItems: 100, itemsPerPage: 10 })
    );
    act(() => { result.current.goToPage(7); });
    expect(result.current.currentPage).toBe(7);
    expect(result.current.startIndex).toBe(60);
    expect(result.current.endIndex).toBe(70);
  });

  it('generates ellipsis in page range', () => {
    const { result } = renderHook(() =>
      usePagination({ totalItems: 200, itemsPerPage: 10, initialPage: 10 })
    );
    expect(result.current.pages).toContain('ellipsis');
    expect(result.current.pages[0]).toBe(1);
    expect(result.current.pages[result.current.pages.length - 1]).toBe(20);
  });
});
```
