# React Component Patterns Catalog

Comprehensive catalog of React component design patterns with TypeScript examples, trade-offs, and guidance for React 19+.

---

## Table of Contents

- [Compound Components](#compound-components)
- [Render Props](#render-props)
- [Higher-Order Components (HOC)](#higher-order-components-hoc)
- [Custom Hook Pattern](#custom-hook-pattern)
- [Provider Pattern](#provider-pattern)
- [Container / Presentational](#container--presentational)
- [Controlled / Uncontrolled](#controlled--uncontrolled)
- [Polymorphic Components](#polymorphic-components)
- [Slot Pattern](#slot-pattern)
- [Forwarding Refs](#forwarding-refs)
- [Error Boundaries](#error-boundaries)
- [Server / Client Component Patterns (React 19)](#server--client-component-patterns-react-19)

---

## Compound Components

**When to use:** Components that share implicit state and work together as a cohesive unit (tabs, accordions, select menus, dropdown groups).

```tsx
import { createContext, useContext, useState, ReactNode } from 'react';

// --- Context ---
interface TabsContextValue {
  activeTab: string;
  setActiveTab: (tab: string) => void;
}

const TabsContext = createContext<TabsContextValue | null>(null);

function useTabsContext() {
  const ctx = useContext(TabsContext);
  if (!ctx) throw new Error('Tab components must be used within <Tabs>');
  return ctx;
}

// --- Root ---
interface TabsProps {
  defaultTab: string;
  children: ReactNode;
}

function Tabs({ defaultTab, children }: TabsProps) {
  const [activeTab, setActiveTab] = useState(defaultTab);
  return (
    <TabsContext.Provider value={{ activeTab, setActiveTab }}>
      <div role="tablist">{children}</div>
    </TabsContext.Provider>
  );
}

// --- Sub-components ---
function TabTrigger({ value, children }: { value: string; children: ReactNode }) {
  const { activeTab, setActiveTab } = useTabsContext();
  return (
    <button
      role="tab"
      aria-selected={activeTab === value}
      onClick={() => setActiveTab(value)}
      className={activeTab === value ? 'border-b-2 border-blue-500 font-semibold' : ''}
    >
      {children}
    </button>
  );
}

function TabContent({ value, children }: { value: string; children: ReactNode }) {
  const { activeTab } = useTabsContext();
  if (activeTab !== value) return null;
  return <div role="tabpanel">{children}</div>;
}

// Attach sub-components
Tabs.Trigger = TabTrigger;
Tabs.Content = TabContent;

// --- Usage ---
<Tabs defaultTab="profile">
  <Tabs.Trigger value="profile">Profile</Tabs.Trigger>
  <Tabs.Trigger value="settings">Settings</Tabs.Trigger>
  <Tabs.Content value="profile"><ProfilePanel /></Tabs.Content>
  <Tabs.Content value="settings"><SettingsPanel /></Tabs.Content>
</Tabs>
```

**Pros:** Clean API, implicit state sharing, declarative composition, enforces valid combinations.
**Cons:** Context overhead, children must be direct descendants (or use context), harder to tree-shake.

---

## Render Props

**When to use:** Share behavior/logic between components when the consumer needs control over rendering.

```tsx
interface MousePosition {
  x: number;
  y: number;
}

interface MouseTrackerProps {
  children: (pos: MousePosition) => ReactNode;
}

function MouseTracker({ children }: MouseTrackerProps) {
  const [pos, setPos] = useState<MousePosition>({ x: 0, y: 0 });

  return (
    <div
      onMouseMove={(e) => setPos({ x: e.clientX, y: e.clientY })}
      className="relative h-64 w-full border"
    >
      {children(pos)}
    </div>
  );
}

// Usage
<MouseTracker>
  {({ x, y }) => (
    <div className="absolute" style={{ left: x, top: y }}>
      🎯 ({x}, {y})
    </div>
  )}
</MouseTracker>
```

**Pros:** Maximum flexibility, no naming collisions, composable.
**Cons:** Deeply nested JSX ("callback hell"), harder to read. Largely superseded by custom hooks.

---

## Higher-Order Components (HOC)

**When to use:** Cross-cutting concerns that need to wrap many components (auth guards, logging, feature flags). Less common in modern React—prefer hooks.

```tsx
import { ComponentType, useEffect } from 'react';

interface WithAuthProps {
  user: User;
}

function withAuth<P extends WithAuthProps>(WrappedComponent: ComponentType<P>) {
  function AuthGuard(props: Omit<P, keyof WithAuthProps>) {
    const user = useAuth();

    if (!user) return <Navigate to="/login" />;

    return <WrappedComponent {...(props as P)} user={user} />;
  }

  AuthGuard.displayName = `withAuth(${WrappedComponent.displayName || WrappedComponent.name})`;
  return AuthGuard;
}

// Usage
const ProtectedDashboard = withAuth(Dashboard);
<ProtectedDashboard />
```

**Pros:** Reuse logic across many components, separation of concerns.
**Cons:** Prop collision risk, wrapper hell (multiple HOCs), harder to type in TypeScript, obscures component tree in DevTools. Prefer custom hooks.

---

## Custom Hook Pattern

**When to use:** Extract and reuse stateful logic across components. The modern replacement for render props and most HOCs.

```tsx
interface UsePaginationOptions {
  totalItems: number;
  itemsPerPage: number;
  initialPage?: number;
}

interface UsePaginationReturn {
  currentPage: number;
  totalPages: number;
  nextPage: () => void;
  prevPage: () => void;
  goToPage: (page: number) => void;
  startIndex: number;
  endIndex: number;
}

function usePagination({
  totalItems,
  itemsPerPage,
  initialPage = 1,
}: UsePaginationOptions): UsePaginationReturn {
  const [currentPage, setCurrentPage] = useState(initialPage);
  const totalPages = Math.ceil(totalItems / itemsPerPage);

  const nextPage = useCallback(
    () => setCurrentPage((p) => Math.min(p + 1, totalPages)),
    [totalPages]
  );

  const prevPage = useCallback(
    () => setCurrentPage((p) => Math.max(p - 1, 1)),
    []
  );

  const goToPage = useCallback(
    (page: number) => setCurrentPage(Math.max(1, Math.min(page, totalPages))),
    [totalPages]
  );

  return {
    currentPage,
    totalPages,
    nextPage,
    prevPage,
    goToPage,
    startIndex: (currentPage - 1) * itemsPerPage,
    endIndex: currentPage * itemsPerPage,
  };
}

// Usage
function UserList({ users }: { users: User[] }) {
  const { currentPage, totalPages, nextPage, prevPage, startIndex, endIndex } =
    usePagination({ totalItems: users.length, itemsPerPage: 10 });

  const visibleUsers = users.slice(startIndex, endIndex);
  // render...
}
```

**Pros:** Composable, testable, no wrapper components, clean TypeScript types.
**Cons:** Cannot render JSX (use compound components for that), can be over-abstracted.

---

## Provider Pattern

**When to use:** Share global or semi-global state (theme, auth, locale, feature flags) across a tree without prop drilling.

```tsx
interface AuthContextValue {
  user: User | null;
  login: (creds: Credentials) => Promise<void>;
  logout: () => void;
  isLoading: boolean;
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used within AuthProvider');
  return ctx;
}

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    checkSession().then(setUser).finally(() => setIsLoading(false));
  }, []);

  const login = useCallback(async (creds: Credentials) => {
    const user = await authenticate(creds);
    setUser(user);
  }, []);

  const logout = useCallback(() => {
    clearSession();
    setUser(null);
  }, []);

  const value = useMemo(
    () => ({ user, login, logout, isLoading }),
    [user, login, logout, isLoading]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

// Usage
<AuthProvider>
  <App />
</AuthProvider>
```

**Pros:** Clean API, eliminates prop drilling, easy to test (wrap in mock provider).
**Cons:** All consumers re-render on any value change—split into multiple contexts for performance. Deeply nested providers ("provider hell").

---

## Container / Presentational

**When to use:** Separate data-fetching/logic (container) from UI rendering (presentational). In React 19, this maps naturally to Server Components (container) and Client Components (presentational).

```tsx
// Presentational: pure UI, receives data via props
interface UserCardProps {
  name: string;
  email: string;
  avatarUrl: string;
  onFollow: () => void;
}

function UserCard({ name, email, avatarUrl, onFollow }: UserCardProps) {
  return (
    <div className="flex items-center gap-4 rounded-lg border p-4">
      <img src={avatarUrl} alt={name} className="h-12 w-12 rounded-full" />
      <div>
        <h3 className="font-semibold">{name}</h3>
        <p className="text-sm text-gray-500">{email}</p>
      </div>
      <button onClick={onFollow} className="ml-auto rounded bg-blue-500 px-3 py-1 text-white">
        Follow
      </button>
    </div>
  );
}

// Container: handles data fetching and state
function UserCardContainer({ userId }: { userId: string }) {
  const { data: user, isLoading } = useFetch<User>(`/api/users/${userId}`);
  const [isFollowing, setIsFollowing] = useState(false);

  const handleFollow = useCallback(async () => {
    await followUser(userId);
    setIsFollowing(true);
  }, [userId]);

  if (isLoading) return <Skeleton />;
  if (!user) return null;

  return (
    <UserCard
      name={user.name}
      email={user.email}
      avatarUrl={user.avatarUrl}
      onFollow={handleFollow}
    />
  );
}
```

**Pros:** Clear separation of concerns, presentational components are easy to test/reuse/storybook.
**Cons:** Can lead to many wrapper components. In React 19, Server Components provide this separation naturally.

---

## Controlled / Uncontrolled

**When to use:** Form inputs and any component where the parent may or may not want to own the state.

```tsx
interface InputProps {
  value?: string;                              // Controlled
  defaultValue?: string;                       // Uncontrolled
  onChange?: (value: string) => void;
  placeholder?: string;
}

function Input({ value, defaultValue, onChange, placeholder }: InputProps) {
  // Internal state for uncontrolled mode
  const [internalValue, setInternalValue] = useState(defaultValue ?? '');
  const isControlled = value !== undefined;
  const currentValue = isControlled ? value : internalValue;

  function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
    const newValue = e.target.value;
    if (!isControlled) setInternalValue(newValue);
    onChange?.(newValue);
  }

  return (
    <input
      value={currentValue}
      onChange={handleChange}
      placeholder={placeholder}
      className="rounded border px-3 py-2"
    />
  );
}

// Controlled usage
const [name, setName] = useState('');
<Input value={name} onChange={setName} />

// Uncontrolled usage
<Input defaultValue="initial" onChange={(v) => console.log(v)} />
```

**Pros:** Flexible—supports both usage modes, familiar pattern (mirrors native HTML behavior).
**Cons:** Complexity managing both modes, must handle controlled/uncontrolled switching warnings.

---

## Polymorphic Components

**When to use:** A component that can render as different HTML elements or other components (e.g., a `<Button>` that can also be an `<a>` or `<Link>`).

```tsx
import { ElementType, ComponentPropsWithoutRef, ReactNode } from 'react';

type PolymorphicProps<E extends ElementType> = {
  as?: E;
  children: ReactNode;
  className?: string;
} & ComponentPropsWithoutRef<E>;

function Text<E extends ElementType = 'p'>({
  as,
  children,
  className = '',
  ...props
}: PolymorphicProps<E>) {
  const Component = as || 'p';
  return (
    <Component className={`text-base ${className}`} {...props}>
      {children}
    </Component>
  );
}

// Usage
<Text>Default paragraph</Text>
<Text as="h1" className="text-3xl font-bold">Heading</Text>
<Text as="span" className="text-sm text-gray-400">Small span</Text>
<Text as="a" href="/about">Link text</Text>
<Text as={Link} to="/about">Router link</Text>
```

**Pros:** One component, many renderings; DRY; type-safe props that adapt to the `as` element.
**Cons:** Complex TypeScript generics, can be confusing for consumers unfamiliar with the pattern.

---

## Slot Pattern

**When to use:** Components with named insertion points (header, footer, icon, action area) instead of a single `children` prop.

```tsx
interface CardProps {
  header?: ReactNode;
  footer?: ReactNode;
  icon?: ReactNode;
  children: ReactNode;
}

function Card({ header, footer, icon, children }: CardProps) {
  return (
    <div className="rounded-lg border shadow-sm">
      {header && (
        <div className="flex items-center gap-2 border-b p-4">
          {icon && <span className="text-xl">{icon}</span>}
          <div className="font-semibold">{header}</div>
        </div>
      )}
      <div className="p-4">{children}</div>
      {footer && <div className="border-t bg-gray-50 p-3">{footer}</div>}
    </div>
  );
}

// Usage
<Card
  icon={<UserIcon />}
  header="User Profile"
  footer={<button className="text-blue-500">Edit</button>}
>
  <p>Main content goes here</p>
</Card>
```

**Pros:** Clear API for layout composition, avoids children-type checking, easily documented.
**Cons:** Props list grows with slots—consider compound components for many slots.

---

## Forwarding Refs

**When to use:** Library/design-system components that need to expose the underlying DOM element to consumers.

```tsx
import { forwardRef, ComponentPropsWithoutRef } from 'react';

interface ButtonProps extends ComponentPropsWithoutRef<'button'> {
  variant?: 'primary' | 'secondary' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
}

const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ variant = 'primary', size = 'md', className = '', children, ...props }, ref) => {
    const variants = {
      primary: 'bg-blue-600 text-white hover:bg-blue-700',
      secondary: 'bg-gray-200 text-gray-800 hover:bg-gray-300',
      ghost: 'bg-transparent hover:bg-gray-100',
    };
    const sizes = {
      sm: 'px-2 py-1 text-sm',
      md: 'px-4 py-2',
      lg: 'px-6 py-3 text-lg',
    };

    return (
      <button
        ref={ref}
        className={`rounded font-medium transition-colors ${variants[variant]} ${sizes[size]} ${className}`}
        {...props}
      >
        {children}
      </button>
    );
  }
);

Button.displayName = 'Button';

// Usage
const btnRef = useRef<HTMLButtonElement>(null);
<Button ref={btnRef} variant="primary" onClick={() => {}}>Click</Button>
```

**React 19 note:** `ref` is available as a regular prop—`forwardRef` becomes optional:

```tsx
// React 19: ref as a prop (no forwardRef needed)
function Button({ ref, variant = 'primary', ...props }: ButtonProps & { ref?: Ref<HTMLButtonElement> }) {
  return <button ref={ref} {...props} />;
}
```

**Pros:** Full DOM access for consumers, required for some third-party libs (e.g., Framer Motion, Radix).
**Cons:** Extra wrapping boilerplate (less in React 19).

---

## Error Boundaries

**When to use:** Catch JavaScript errors in a component subtree and display a fallback UI instead of crashing the app.

```tsx
import { Component, ErrorInfo, ReactNode } from 'react';

interface ErrorBoundaryProps {
  fallback: ReactNode | ((error: Error, reset: () => void) => ReactNode);
  children: ReactNode;
  onError?: (error: Error, errorInfo: ErrorInfo) => void;
}

interface ErrorBoundaryState {
  hasError: boolean;
  error: Error | null;
}

class ErrorBoundary extends Component<ErrorBoundaryProps, ErrorBoundaryState> {
  state: ErrorBoundaryState = { hasError: false, error: null };

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    this.props.onError?.(error, errorInfo);
  }

  resetError = () => {
    this.setState({ hasError: false, error: null });
  };

  render() {
    if (this.state.hasError && this.state.error) {
      const { fallback } = this.props;
      if (typeof fallback === 'function') {
        return fallback(this.state.error, this.resetError);
      }
      return fallback;
    }
    return this.props.children;
  }
}

// Usage
<ErrorBoundary
  fallback={(error, reset) => (
    <div className="rounded border border-red-300 bg-red-50 p-4">
      <h2 className="text-red-800">Something went wrong</h2>
      <p className="text-red-600">{error.message}</p>
      <button onClick={reset} className="mt-2 text-blue-600 underline">Try again</button>
    </div>
  )}
  onError={(error) => logToService(error)}
>
  <Dashboard />
</ErrorBoundary>
```

**Pros:** Prevents full-app crashes, graceful degradation, per-section error handling.
**Cons:** Must be a class component (no hook API), doesn't catch event handler errors or async errors.

---

## Server / Client Component Patterns (React 19)

### Server Components (default)

Server Components run on the server. They can directly access databases, file systems, and secrets. They send zero JavaScript to the client.

```tsx
// app/users/page.tsx — Server Component (default)
import { db } from '@/lib/db';
import { UserList } from './user-list'; // Client Component

export default async function UsersPage() {
  const users = await db.user.findMany(); // Direct DB access

  return (
    <main className="p-8">
      <h1 className="text-2xl font-bold">Users</h1>
      <UserList initialUsers={users} />
    </main>
  );
}
```

### Client Components

Client Components run in the browser. Use `'use client'` directive for interactivity, hooks, browser APIs.

```tsx
// app/users/user-list.tsx
'use client';

import { useState } from 'react';
import type { User } from '@/types';

export function UserList({ initialUsers }: { initialUsers: User[] }) {
  const [users, setUsers] = useState(initialUsers);
  const [search, setSearch] = useState('');

  const filtered = users.filter((u) =>
    u.name.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div>
      <input
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        placeholder="Search users..."
        className="mb-4 rounded border px-3 py-2"
      />
      <ul>
        {filtered.map((user) => (
          <li key={user.id} className="border-b py-2">{user.name}</li>
        ))}
      </ul>
    </div>
  );
}
```

### Composition Pattern: Server → Client

```
Server Component (data fetching, no JS)
  └── Client Component (interactivity, hooks)
        └── Server Component (can be passed as children)
```

```tsx
// Server Component passes server-rendered children into a Client Component
export default async function Layout() {
  const nav = await getNavItems();
  
  return (
    <InteractiveShell>        {/* Client Component */}
      <NavList items={nav} /> {/* Server Component rendered on server, passed as children */}
    </InteractiveShell>
  );
}
```

**Key rules:**
- Server Components cannot use hooks, event handlers, or browser APIs.
- Client Components cannot directly `import` Server Components (pass as `children` or props instead).
- Shared components (no `'use client'`) default to Server Components.
- Move `'use client'` boundary as low in the tree as possible to minimize client JS.

**Pros:** Zero client JS for static content, direct data access, smaller bundles, better performance.
**Cons:** New mental model, serialization constraints (props must be serializable across the server-client boundary), can't mix hooks into server code.

---

## Pattern Selection Guide

| Scenario | Recommended Pattern |
|----------|-------------------|
| Reusable stateful logic | Custom Hook |
| Component group with shared state | Compound Components |
| Global/app-wide state | Provider Pattern |
| Different element rendering | Polymorphic Component |
| Named layout sections | Slot Pattern |
| Exposing DOM refs | Forwarding Refs |
| Graceful error handling | Error Boundary |
| Cross-cutting wrapper logic | HOC (or custom hook) |
| Consumer-controlled rendering | Render Props (or custom hook) |
| Data vs. presentation split | Container/Presentational or Server/Client |
| Two-way binding for inputs | Controlled/Uncontrolled |
| Server-side data, client interactivity | Server → Client composition |
