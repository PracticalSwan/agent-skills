# App Router Quick Reference

Complete file conventions and routing patterns for Next.js App Router (v15/v16).

> Official docs: https://nextjs.org/docs/app/api-reference/file-conventions

---

## Table of Contents

1. [Special Files](#special-files)
2. [Dynamic Routes](#dynamic-routes)
3. [Route Groups](#route-groups)
4. [Parallel Routes](#parallel-routes)
5. [Intercepting Routes](#intercepting-routes)
6. [Route Segment Config](#route-segment-config)
7. [Metadata Files](#metadata-files)

---

## Special Files

### Core Layout & Page Files

| File | Extension | Description |
|------|-----------|-------------|
| `layout` | `.js` `.jsx` `.tsx` | Root or segment layout; wraps children; persists across navigations |
| `page` | `.js` `.jsx` `.tsx` | Unique UI for a route; makes it publicly accessible |
| `template` | `.js` `.jsx` `.tsx` | Like layout but re-mounts on navigation; resets state |
| `loading` | `.js` `.jsx` `.tsx` | Suspense wrapper shown while page/layout loads |
| `error` | `.js` `.jsx` `.tsx` | Error boundary for the segment; **must be a Client Component** |
| `global-error` | `.js` `.jsx` `.tsx` | Catches errors in root layout; wraps entire app |
| `not-found` | `.js` `.jsx` `.tsx` | Rendered by `notFound()` or unmatched routes |
| `forbidden` | `.js` `.jsx` `.tsx` | Rendered by `forbidden()` — HTTP 403 (v16) |
| `unauthorized` | `.js` `.jsx` `.tsx` | Rendered by `unauthorized()` — HTTP 401 (v16) |
| `default` | `.js` `.jsx` `.tsx` | Fallback for parallel routes when slot has no active match |

### API & Infra Files

| File | Extension | Description |
|------|-----------|-------------|
| `route` | `.js` `.ts` | API endpoint; exports HTTP verbs (`GET`, `POST`, etc.) |
| `proxy` | `.js` `.ts` | Lightweight HTTP proxy for the segment (v16) |
| `middleware` | `.js` `.ts` | Runs before request completes; place at project root |
| `instrumentation` | `.js` `.ts` | Server lifecycle hooks, OpenTelemetry init (stable v15) |
| `instrumentation-client` | `.js` `.ts` | Client-side performance + error monitoring (v16) |

---

## Dynamic Routes

### Segment Types

| Syntax | Example | Matches |
|--------|---------|---------|
| `[slug]` | `app/blog/[slug]/page.tsx` | `/blog/hello-world` |
| `[...slug]` | `app/docs/[...slug]/page.tsx` | `/docs/a`, `/docs/a/b`, `/docs/a/b/c` |
| `[[...slug]]` | `app/shop/[[...slug]]/page.tsx` | `/shop`, `/shop/a`, `/shop/a/b` |

### Async Params Pattern (v15+ Required)

```typescript
// app/blog/[slug]/page.tsx
interface Props {
  params: Promise<{ slug: string }>
  searchParams: Promise<{ page?: string; sort?: string }>
}

export default async function BlogPost({ params, searchParams }: Props) {
  // Both params and searchParams are now async
  const { slug } = await params
  const { page = '1', sort = 'date' } = await searchParams

  const post = await getPost(slug)
  return <Article post={post} page={Number(page)} sort={sort} />
}

export async function generateStaticParams() {
  const posts = await getAllPosts()
  return posts.map((post) => ({ slug: post.slug }))
}
```

---

## Route Groups

Use `(groupName)` to organize routes without affecting the URL structure.

```
app/
├── (marketing)/
│   ├── layout.tsx        # Layout shared only for marketing pages
│   ├── page.tsx          # → /
│   ├── about/page.tsx    # → /about
│   └── pricing/page.tsx  # → /pricing
├── (app)/
│   ├── layout.tsx        # Layout shared only for app pages (requires auth)
│   ├── dashboard/page.tsx # → /dashboard
│   └── settings/page.tsx  # → /settings
└── layout.tsx            # Root layout
```

**Use cases:**
- Different layouts for different sections without URL nesting
- Opt segments in/out of a shared layout
- Split large apps into logical sections

---

## Parallel Routes

Render multiple pages simultaneously in the same layout using **slots** (`@folderName`).

```
app/
├── layout.tsx            # Receives { children, modal } props
├── page.tsx              # → / (main content)
└── @modal/               # Parallel slot
    ├── default.tsx       # Fallback when no modal is active
    └── photo/
        └── [id]/
            └── page.tsx  # → renders as modal alongside main page
```

```typescript
// app/layout.tsx
export default function Layout({
  children,
  modal,
}: {
  children: React.ReactNode
  modal: React.ReactNode  // @modal slot
}) {
  return (
    <>
      {children}
      {modal}
    </>
  )
}
```

**Use cases:**
- Modals with shareable URLs (soft navigation)
- Split views (e.g., sidebar + main content)
- Tab navigation that preserves page state

---

## Intercepting Routes

Intercept a route in a different context (e.g., show a modal instead of full page navigation).

| Convention | Intercepts |
|-----------|-----------|
| `(.)folder` | Same level |
| `(..)folder` | One level up |
| `(..)(..)folder` | Two levels up |
| `(...)folder` | From root `app/` |

```
app/
├── photos/
│   └── [id]/
│       └── page.tsx         # Full page: /photos/123
├── @modal/
│   ├── default.tsx          # null (no modal by default)
│   └── (.)photos/           # Intercept same-level /photos
│       └── [id]/
│           └── page.tsx     # Modal: shown when navigating from feed
└── layout.tsx               # Renders both children + @modal
```

**Pattern:** On soft navigation from within the app → modal. On hard navigation (new tab, direct URL) → full page.

---

## Route Segment Config

Export these from `page.tsx`, `layout.tsx`, or `route.ts` to control rendering behavior.

```typescript
// Rendering mode
export const dynamic = 'auto'           // default: auto-detect
export const dynamic = 'force-dynamic'  // always SSR
export const dynamic = 'error'          // error if dynamic
export const dynamic = 'force-static'   // always static

// Revalidation (ISR)
export const revalidate = false         // cache forever
export const revalidate = 0            // no cache (same as force-dynamic)
export const revalidate = 3600         // revalidate every hour

// Runtime
export const runtime = 'nodejs'        // default
export const runtime = 'edge'          // Edge Runtime

// Fetch cache
export const fetchCache = 'auto'       // default
export const fetchCache = 'force-no-store'
export const fetchCache = 'force-cache'

// Generate static paths at build
export async function generateStaticParams() { ... }
```

---

## Metadata Files

These files are auto-detected in any route segment and handle SEO/social metadata.

| File | Content Type | Description |
|------|-------------|-------------|
| `favicon.ico` | Image | Browser favicon |
| `icon.png` / `icon.svg` | Image | App icon |
| `apple-icon.png` | Image | iOS home screen icon |
| `opengraph-image.png` | Image | OG image for social sharing |
| `twitter-image.png` | Image | Twitter card image |
| `opengraph-image.tsx` | Dynamic | Auto-generated OG image with `ImageResponse` |
| `sitemap.xml` / `sitemap.ts` | XML | Crawlable sitemap |
| `robots.txt` / `robots.ts` | Text | Crawl directives |
| `manifest.json` | JSON | PWA web app manifest |

### Dynamic OG Image Example

```typescript
// app/blog/[slug]/opengraph-image.tsx
import { ImageResponse } from 'next/og'

export const runtime = 'edge'
export const size = { width: 1200, height: 630 }
export const contentType = 'image/png'

export default async function OGImage({
  params,
}: {
  params: Promise<{ slug: string }>
}) {
  const { slug } = await params
  const post = await getPost(slug)

  return new ImageResponse(
    <div style={{ display: 'flex', background: '#fff', width: '100%', height: '100%' }}>
      <h1 style={{ fontSize: 60 }}>{post.title}</h1>
    </div>,
    { ...size }
  )
}
```
