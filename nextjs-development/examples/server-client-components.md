# Server & Client Component Patterns

Practical TypeScript patterns for composing Server Components (RSC) and Client Components (RCC) in Next.js App Router.

---

## Decision Guide

```
Does the component need any of these?
  ✓ onClick, onChange, onSubmit or any event handler
  ✓ useState, useReducer, useEffect, useLayoutEffect
  ✓ useRouter, useParams, useSearchParams, usePathname
  ✓ window, document, localStorage, navigator
  ✓ Third-party libraries that use browser APIs
  ✓ Real-time subscriptions (WebSocket, SSE)
    → Add "use client" directive

Otherwise (default — no directive needed):
  ✓ Fetch data directly from DB or internal API
  ✓ Access cookies(), headers(), auth tokens
  ✓ Use large server-only dependencies (sharp, pdf-lib)
  ✓ Keep sensitive logic/credentials out of the JS bundle
  ✓ Top-level await in component body
    → Server Component (RSC)
```

---

## 1. Basic Server Component

```typescript
// app/products/page.tsx — Server Component (default, no directive)
import { db } from '@/lib/db'

export default async function ProductsPage() {
  // Direct DB access — no API call needed, zero client-side JS
  const products = await db.products.findMany({ where: { active: true } })

  return (
    <main>
      <h1>Products</h1>
      <ul>
        {products.map((p) => (
          <li key={p.id}>
            {p.name} — ${p.price}
          </li>
        ))}
      </ul>
    </main>
  )
}
```

---

## 2. Basic Client Component

```typescript
// components/Counter.tsx
'use client'
import { useState } from 'react'

export function Counter({ initialCount = 0 }: { initialCount?: number }) {
  const [count, setCount] = useState(initialCount)

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(c => c + 1)}>Increment</button>
      <button onClick={() => setCount(c => c - 1)}>Decrement</button>
    </div>
  )
}
```

---

## 3. Composition: Server Data → Client Component

The most common pattern: fetch data in a Server Component, pass it as props to a Client Component.

```typescript
// app/dashboard/page.tsx (Server Component)
import { getUser, getStats } from '@/lib/data'
import { StatsChart } from '@/components/StatsChart'

export default async function DashboardPage() {
  const [user, stats] = await Promise.all([getUser(), getStats()])

  return (
    <div>
      <h1>Welcome, {user.name}</h1>
      {/* StatsChart is "use client" — receives plain data as props */}
      <StatsChart data={stats} />
    </div>
  )
}

// components/StatsChart.tsx (Client Component)
'use client'
import { LineChart } from 'recharts'

export function StatsChart({ data }: { data: StatsData[] }) {
  // data is already fetched; this component only handles rendering
  return <LineChart data={data} width={600} height={300} />
}
```

---

## 4. Pass Server Component as Child to Client Component

```typescript
// ✅ This works — children passes through the "use client" boundary
// app/page.tsx (Server Component)
import { Modal } from '@/components/Modal'
import { UserProfile } from '@/components/UserProfile'

export default async function Page() {
  const user = await getUser()

  return (
    <Modal>
      {/* UserProfile is a Server Component — allowed as children prop */}
      <UserProfile user={user} />
    </Modal>
  )
}

// components/Modal.tsx (Client Component)
'use client'
import { useState } from 'react'

export function Modal({ children }: { children: React.ReactNode }) {
  const [open, setOpen] = useState(false)
  return (
    <div>
      <button onClick={() => setOpen(true)}>Open</button>
      {open && <div className="modal">{children}</div>}
    </div>
  )
}
```

---

## 5. Server Component as Leaf Inside Client Component Tree

```typescript
// ❌ WRONG: Importing a Server Component inside a Client Component
// components/ClientParent.tsx
'use client'
import { ServerChild } from './ServerChild'  // ERROR: can't import RSC in RCC

// ✅ CORRECT: Pass Server Component via props/children
// app/page.tsx (Server Component — the composition boundary)
import { ClientParent } from '@/components/ClientParent'
import { ServerChild } from '@/components/ServerChild'

export default function Page() {
  return (
    <ClientParent>
      <ServerChild />  {/* injected as children, not imported */}
    </ClientParent>
  )
}
```

---

## 6. Context Providers (Must Be Client Components)

```typescript
// components/providers/ThemeProvider.tsx
'use client'
import { createContext, useContext, useState } from 'react'

const ThemeContext = createContext<{ dark: boolean; toggle: () => void } | null>(null)

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [dark, setDark] = useState(false)
  return (
    <ThemeContext.Provider value={{ dark, toggle: () => setDark(d => !d) }}>
      {children}
    </ThemeContext.Provider>
  )
}

export function useTheme() {
  const ctx = useContext(ThemeContext)
  if (!ctx) throw new Error('useTheme must be used inside ThemeProvider')
  return ctx
}

// app/layout.tsx (Server Component)
import { ThemeProvider } from '@/components/providers/ThemeProvider'

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html>
      <body>
        <ThemeProvider>
          {children}  {/* Server Components can be children of Client providers */}
        </ThemeProvider>
      </body>
    </html>
  )
}
```

---

## 7. Server Actions from Client Components

```typescript
// app/actions.ts
'use server'
import { revalidatePath } from 'next/cache'
import { z } from 'zod'

const schema = z.object({ message: z.string().min(1) })

export async function submitComment(
  prevState: { error?: string } | null,
  formData: FormData
) {
  const result = schema.safeParse({ message: formData.get('message') })

  if (!result.success) {
    return { error: result.error.flatten().fieldErrors.message?.[0] }
  }

  await db.comments.create({ data: result.data })
  revalidatePath('/comments')
  return null
}

// components/CommentForm.tsx
'use client'
import { useActionState } from 'react'
import { submitComment } from '@/app/actions'

export function CommentForm() {
  const [state, action, isPending] = useActionState(submitComment, null)

  return (
    <form action={action}>
      <textarea name="message" required />
      {state?.error && <p className="error">{state.error}</p>}
      <button type="submit" disabled={isPending}>
        {isPending ? 'Posting…' : 'Post Comment'}
      </button>
    </form>
  )
}
```

---

## 8. `useLinkStatus` Hook (v16)

```typescript
// components/NavLink.tsx — shows pending state during navigation
'use client'
import Link from 'next/link'
import { useLinkStatus } from 'next/link'

function PendingIndicator() {
  const { pending } = useLinkStatus()
  return pending ? <Spinner /> : null
}

export function NavLink({ href, children }: { href: string; children: React.ReactNode }) {
  return (
    <Link href={href}>
      {children}
      <PendingIndicator />
    </Link>
  )
}
```

---

## 9. Server-Only and Client-Only Modules

```typescript
// lib/server-auth.ts
import 'server-only'  // throws if imported in Client Component

export async function getSession() {
  const cookieStore = await cookies()
  // ... decode JWT
}

// lib/analytics.ts
import 'client-only'  // throws if imported in Server Component

export function trackEvent(name: string) {
  window.gtag('event', name)
}
```

---

## Key Rules Summary

| Scenario | Solution |
|---------|---------|
| Need interactivity (click, state) | Add `"use client"` |
| Need server data in a Client Component | Fetch in RSC, pass as props |
| Need Server Component inside Client Component | Pass as `children` prop |
| Need context state (theme, auth session) | Wrap with a Client Provider in layout |
| Want to protect server-only code | Use `import 'server-only'` |
| Server Action from Client form | `useActionState` with `action` prop on `<form>` |
| Navigation pending state (v16) | `useLinkStatus()` inside `<Link>` scope |
