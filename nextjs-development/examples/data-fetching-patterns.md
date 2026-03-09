# Data Fetching Patterns

Concrete TypeScript examples for every data fetching approach in Next.js 15/16.

---

## 1. `use cache` Directive (Preferred in v15+)

### Cache a Server Component

```typescript
// app/products/page.tsx
import { cacheTag, cacheLife } from 'next/cache'

async function ProductList() {
  'use cache'
  cacheLife('hours')           // stale: 1h, revalidate: 1h, expire: 24h
  cacheTag('products')         // tag for targeted invalidation

  const products = await db.products.findMany({
    where: { active: true },
    orderBy: { createdAt: 'desc' },
  })

  return (
    <ul>
      {products.map((p) => (
        <li key={p.id}>{p.name} — ${p.price}</li>
      ))}
    </ul>
  )
}

export default function Page() {
  return <ProductList />
}
```

### Cache a Data-Fetching Function

```typescript
// lib/products.ts
import { cacheTag, cacheLife } from 'next/cache'

export async function getProduct(id: string) {
  'use cache'
  cacheLife('days')
  cacheTag('products', `product-${id}`)

  return db.products.findUnique({ where: { id } })
}

// app/products/[id]/page.tsx
export default async function ProductPage({
  params,
}: {
  params: Promise<{ id: string }>
}) {
  const { id } = await params
  const product = await getProduct(id)   // cached per id

  if (!product) notFound()
  return <ProductDetail product={product} />
}
```

### Revalidate on Mutation

```typescript
// app/actions.ts
'use server'
import { revalidateTag } from 'next/cache'

export async function updateProduct(id: string, formData: FormData) {
  await db.products.update({
    where: { id },
    data: {
      name: formData.get('name') as string,
      price: Number(formData.get('price')),
    },
  })

  revalidateTag(`product-${id}`)  // invalidate specific product cache
  revalidateTag('products')       // invalidate product list cache
}
```

---

## 2. ISR with `revalidate` (Still Valid)

```typescript
// app/blog/page.tsx
// Revalidate the entire segment every 60 seconds (ISR)
export const revalidate = 60

export default async function BlogPage() {
  const posts = await fetch('https://cms.example.com/posts').then(r => r.json())
  return <PostList posts={posts} />
}
```

```typescript
// app/blog/[slug]/page.tsx
export async function generateStaticParams() {
  const posts = await getPosts()
  return posts.map((p) => ({ slug: p.slug }))
}

// Set per-page revalidation
export const revalidate = 3600  // 1 hour

export default async function BlogPost({
  params,
}: {
  params: Promise<{ slug: string }>
}) {
  const { slug } = await params
  const post = await getPost(slug)
  return <Article post={post} />
}
```

---

## 3. `fetch` with Cache Control

```typescript
// Server Component: fine-grained fetch caching
export default async function Dashboard() {
  // Cached and tagged (ISR-style)
  const stats = await fetch('https://api.example.com/stats', {
    next: { revalidate: 300, tags: ['stats'] },
  }).then(r => r.json())

  // Never cached (always fresh)
  const alerts = await fetch('https://api.example.com/alerts', {
    cache: 'no-store',
  }).then(r => r.json())

  return <DashboardView stats={stats} alerts={alerts} />
}
```

> **Note:** `fetch` caching is deduplicated per request in Next.js. Multiple components calling the same URL within one render get the same cached result (request memoization).

---

## 4. Parallel Data Fetching

```typescript
// ✅ Fetch in parallel — don't await sequentially
export default async function ProductPage({
  params,
}: {
  params: Promise<{ id: string }>
}) {
  const { id } = await params

  // Start all fetches simultaneously
  const [product, reviews, related] = await Promise.all([
    getProduct(id),
    getReviews(id),
    getRelatedProducts(id),
  ])

  return (
    <>
      <ProductDetail product={product} />
      <ReviewList reviews={reviews} />
      <RelatedProducts products={related} />
    </>
  )
}
```

---

## 5. Streaming with Suspense

```typescript
// app/products/[id]/page.tsx
import { Suspense } from 'react'
import { ReviewSkeleton } from '@/components/skeletons'

export default async function ProductPage({
  params,
}: {
  params: Promise<{ id: string }>
}) {
  const { id } = await params
  const product = await getProduct(id)  // blocks render until resolved

  return (
    <>
      <ProductDetail product={product} />
      {/* Reviews load independently without blocking the product */}
      <Suspense fallback={<ReviewSkeleton />}>
        <ReviewList productId={id} />
      </Suspense>
    </>
  )
}

// ReviewList is a separate async Server Component
async function ReviewList({ productId }: { productId: string }) {
  const reviews = await getReviews(productId)  // streamed in
  return <ul>{reviews.map(r => <li key={r.id}>{r.body}</li>)}</ul>
}
```

---

## 6. Client-Side Fetching (SWR / React Query)

For data that requires interactivity, user-specific state, or real-time updates:

```typescript
// components/UserDashboard.tsx
'use client'
import useSWR from 'swr'

const fetcher = (url: string) => fetch(url).then(r => r.json())

export function UserDashboard({ userId }: { userId: string }) {
  const { data, error, isLoading, mutate } = useSWR(
    `/api/users/${userId}/dashboard`,
    fetcher,
    { refreshInterval: 30000 }  // poll every 30s
  )

  if (isLoading) return <Skeleton />
  if (error) return <ErrorMessage />

  return (
    <div>
      <h2>Welcome, {data.name}</h2>
      <button onClick={() => mutate()}>Refresh</button>
    </div>
  )
}
```

---

## 7. Route Handler (API Endpoint)

```typescript
// app/api/products/route.ts
import { NextRequest, NextResponse } from 'next/server'
import { after } from 'next/server'

// GET is NOT cached by default in v15+
export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url)
  const category = searchParams.get('category') ?? undefined

  const products = await db.products.findMany({
    where: category ? { category } : undefined,
    take: 50,
  })

  after(() => {
    // Log analytics after response is sent
    logApiCall({ endpoint: '/api/products', category })
  })

  return NextResponse.json(products)
}

// To opt-in to caching for this route handler:
// export const revalidate = 3600
// export const dynamic = 'force-static'

export async function POST(request: NextRequest) {
  const body = await request.json()

  // Validate input at API boundary
  const { name, price, category } = body
  if (!name || !price) {
    return NextResponse.json({ error: 'name and price required' }, { status: 400 })
  }

  const product = await db.products.create({ data: { name, price, category } })
  return NextResponse.json(product, { status: 201 })
}
```

---

## 8. `after()` for Post-Response Work

```typescript
// Server Action with post-response analytics
'use server'
import { after } from 'next/server'

export async function purchaseProduct(productId: string) {
  const order = await db.orders.create({ data: { productId } })

  // Fires after the action response is sent; won't delay the user
  after(async () => {
    await sendOrderConfirmationEmail(order.id)
    await updateInventory(productId)
    await logPurchaseEvent(order.id)
  })

  return { orderId: order.id }
}
```

---

## Pattern Comparison

| Pattern | When to Use | Cached? | Revalidated? |
|---------|------------|---------|-------------|
| `use cache` directive | Preferred for RSC data | Yes | Via `revalidateTag` |
| `export const revalidate` | Segment-level ISR | Yes | On interval |
| `fetch` with `next.revalidate` | Fine-grained ISR | Yes | On interval |
| `fetch` with `no-store` | Always-fresh data | No | N/A |
| SWR / React Query | Client-side, interactive | Client cache | On mutation/interval |
| Route Handler + `force-static` | Static API outputs | Yes | On interval |
