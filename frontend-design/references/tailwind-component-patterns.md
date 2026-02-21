# Tailwind CSS Component Patterns

Production-ready component patterns with complete HTML + Tailwind CSS code. Copy, adapt, and compose.

---

## Table of Contents

1. [Responsive Containers](#responsive-containers)
2. [Card Layouts](#card-layouts)
3. [Form Patterns](#form-patterns)
4. [Navigation Patterns](#navigation-patterns)
5. [Modal / Dialog](#modal--dialog)
6. [Toast / Notification](#toast--notification)
7. [Table Patterns](#table-patterns)
8. [Skeleton Loading](#skeleton-loading)

---

## Responsive Containers

### Centered Container with Max Width

```html
<div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
  <!-- Content -->
</div>
```

### Responsive Padding Container

```html
<div class="px-4 py-6 sm:px-6 sm:py-8 lg:px-8 lg:py-12">
  <!-- Content adapts padding at each breakpoint -->
</div>
```

### Full-Bleed with Constrained Content

```html
<div class="bg-gray-50">
  <div class="mx-auto max-w-5xl px-4 py-12 sm:px-6 lg:px-8">
    <!-- Full-width background, centered content -->
  </div>
</div>
```

---

## Card Layouts

### Vertical Card

```html
<div class="overflow-hidden rounded-xl bg-white shadow-md transition-shadow hover:shadow-lg">
  <img
    src="/recipe.jpg"
    alt="Recipe thumbnail"
    class="h-48 w-full object-cover"
  />
  <div class="p-5">
    <h3 class="text-lg font-semibold text-gray-900">Card Title</h3>
    <p class="mt-1 text-sm text-gray-500">Short description goes here.</p>
    <div class="mt-4 flex items-center justify-between">
      <span class="text-sm font-medium text-indigo-600">$12.99</span>
      <button class="rounded-lg bg-indigo-600 px-3 py-1.5 text-sm font-medium text-white hover:bg-indigo-700">
        View
      </button>
    </div>
  </div>
</div>
```

### Horizontal Card

```html
<div class="flex overflow-hidden rounded-xl bg-white shadow-md transition-shadow hover:shadow-lg">
  <img
    src="/recipe.jpg"
    alt="Recipe thumbnail"
    class="h-auto w-40 flex-shrink-0 object-cover sm:w-48"
  />
  <div class="flex flex-1 flex-col justify-between p-5">
    <div>
      <h3 class="text-lg font-semibold text-gray-900">Card Title</h3>
      <p class="mt-1 text-sm text-gray-500">
        Description that wraps to multiple lines on smaller widths.
      </p>
    </div>
    <div class="mt-3 flex items-center gap-2">
      <span class="inline-flex items-center rounded-full bg-green-100 px-2.5 py-0.5 text-xs font-medium text-green-700">
        Easy
      </span>
      <span class="text-xs text-gray-400">25 min</span>
    </div>
  </div>
</div>
```

### Responsive Card Grid

```html
<div class="grid gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
  <!-- Card items -->
  <div class="overflow-hidden rounded-xl bg-white shadow-md">...</div>
  <div class="overflow-hidden rounded-xl bg-white shadow-md">...</div>
  <div class="overflow-hidden rounded-xl bg-white shadow-md">...</div>
  <div class="overflow-hidden rounded-xl bg-white shadow-md">...</div>
</div>
```

### Card with Overlay Badge

```html
<div class="group relative overflow-hidden rounded-xl bg-white shadow-md">
  <img src="/recipe.jpg" alt="Recipe" class="h-48 w-full object-cover transition-transform group-hover:scale-105" />
  <span class="absolute left-3 top-3 rounded-full bg-black/60 px-2.5 py-1 text-xs font-medium text-white">
    Featured
  </span>
  <div class="p-5">
    <h3 class="font-semibold text-gray-900">Recipe Name</h3>
    <p class="mt-1 text-sm text-gray-500">Quick weeknight dinner.</p>
  </div>
</div>
```

---

## Form Patterns

### Floating Label Input

```html
<div class="relative">
  <input
    id="email"
    type="email"
    placeholder=" "
    class="peer w-full rounded-lg border border-gray-300 px-3 pb-2 pt-5 text-sm text-gray-900 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
  />
  <label
    for="email"
    class="absolute left-3 top-1 text-xs text-gray-500 transition-all peer-placeholder-shown:top-3.5 peer-placeholder-shown:text-sm peer-focus:top-1 peer-focus:text-xs peer-focus:text-indigo-600"
  >
    Email Address
  </label>
</div>
```

### Inline Validation Input

```html
<!-- Success state -->
<div>
  <label for="username" class="block text-sm font-medium text-gray-700">Username</label>
  <div class="relative mt-1">
    <input
      id="username"
      type="text"
      value="johndoe"
      class="w-full rounded-lg border border-green-500 px-3 py-2 pr-10 text-sm text-gray-900 focus:outline-none focus:ring-1 focus:ring-green-500"
    />
    <span class="absolute inset-y-0 right-3 flex items-center text-green-500">
      <!-- Checkmark icon -->
      <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
        <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
      </svg>
    </span>
  </div>
  <p class="mt-1 text-xs text-green-600">Username is available.</p>
</div>

<!-- Error state -->
<div>
  <label for="email" class="block text-sm font-medium text-gray-700">Email</label>
  <div class="relative mt-1">
    <input
      id="email"
      type="email"
      value="invalid-email"
      class="w-full rounded-lg border border-red-500 px-3 py-2 pr-10 text-sm text-gray-900 focus:outline-none focus:ring-1 focus:ring-red-500"
    />
    <span class="absolute inset-y-0 right-3 flex items-center text-red-500">
      <!-- Exclamation icon -->
      <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
        <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/>
      </svg>
    </span>
  </div>
  <p class="mt-1 text-xs text-red-600">Please enter a valid email address.</p>
</div>
```

### Multi-Step Form

```html
<!-- Step indicator -->
<nav class="mb-8">
  <ol class="flex items-center">
    <!-- Completed step -->
    <li class="flex items-center">
      <span class="flex h-8 w-8 items-center justify-center rounded-full bg-indigo-600 text-sm font-medium text-white">
        <svg class="h-4 w-4" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg>
      </span>
      <span class="ml-2 text-sm font-medium text-indigo-600">Account</span>
    </li>
    <!-- Connector -->
    <li class="mx-4 h-0.5 w-12 bg-indigo-600 sm:w-20"></li>
    <!-- Current step -->
    <li class="flex items-center">
      <span class="flex h-8 w-8 items-center justify-center rounded-full border-2 border-indigo-600 text-sm font-medium text-indigo-600">
        2
      </span>
      <span class="ml-2 text-sm font-medium text-indigo-600">Details</span>
    </li>
    <!-- Connector -->
    <li class="mx-4 h-0.5 w-12 bg-gray-300 sm:w-20"></li>
    <!-- Upcoming step -->
    <li class="flex items-center">
      <span class="flex h-8 w-8 items-center justify-center rounded-full border-2 border-gray-300 text-sm font-medium text-gray-400">
        3
      </span>
      <span class="ml-2 text-sm font-medium text-gray-400">Confirm</span>
    </li>
  </ol>
</nav>

<!-- Form content area -->
<div class="rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
  <h2 class="text-lg font-semibold text-gray-900">Step 2: Your Details</h2>
  <div class="mt-4 space-y-4">
    <!-- Form fields for this step -->
  </div>
  <div class="mt-6 flex justify-between">
    <button class="rounded-lg border border-gray-300 px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50">
      Back
    </button>
    <button class="rounded-lg bg-indigo-600 px-4 py-2 text-sm font-medium text-white hover:bg-indigo-700">
      Continue
    </button>
  </div>
</div>
```

---

## Navigation Patterns

### Top Navbar with Mobile Hamburger

```html
<header class="border-b border-gray-200 bg-white">
  <div class="mx-auto flex max-w-7xl items-center justify-between px-4 py-3 sm:px-6 lg:px-8">
    <!-- Logo -->
    <a href="/" class="text-xl font-bold text-indigo-600">Kitchen Odyssey</a>

    <!-- Desktop nav -->
    <nav class="hidden items-center gap-6 md:flex">
      <a href="/" class="text-sm font-medium text-gray-700 hover:text-indigo-600">Home</a>
      <a href="/search" class="text-sm font-medium text-gray-700 hover:text-indigo-600">Search</a>
      <a href="/create" class="text-sm font-medium text-gray-700 hover:text-indigo-600">Create</a>
      <a href="/profile" class="rounded-lg bg-indigo-600 px-4 py-2 text-sm font-medium text-white hover:bg-indigo-700">
        Profile
      </a>
    </nav>

    <!-- Mobile hamburger button -->
    <button class="rounded-lg p-2 text-gray-500 hover:bg-gray-100 md:hidden" aria-label="Open menu">
      <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>
      </svg>
    </button>
  </div>

  <!-- Mobile menu (toggle visibility with JS) -->
  <nav class="border-t border-gray-200 bg-white px-4 py-3 md:hidden">
    <div class="flex flex-col gap-2">
      <a href="/" class="rounded-lg px-3 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50">Home</a>
      <a href="/search" class="rounded-lg px-3 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50">Search</a>
      <a href="/create" class="rounded-lg px-3 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50">Create</a>
      <a href="/profile" class="rounded-lg px-3 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50">Profile</a>
    </div>
  </nav>
</header>
```

### Sidebar Navigation

```html
<aside class="flex h-screen w-64 flex-col border-r border-gray-200 bg-white">
  <!-- Logo -->
  <div class="flex h-16 items-center border-b border-gray-200 px-6">
    <span class="text-lg font-bold text-indigo-600">Admin</span>
  </div>

  <!-- Nav links -->
  <nav class="flex-1 overflow-y-auto px-3 py-4">
    <ul class="space-y-1">
      <!-- Active item -->
      <li>
        <a href="/admin/stats" class="flex items-center gap-3 rounded-lg bg-indigo-50 px-3 py-2 text-sm font-medium text-indigo-700">
          <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-4 0h4"/></svg>
          Dashboard
        </a>
      </li>
      <!-- Inactive item -->
      <li>
        <a href="/admin/recipes" class="flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium text-gray-600 hover:bg-gray-50 hover:text-gray-900">
          <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
          Recipes
        </a>
      </li>
      <li>
        <a href="/admin/users" class="flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium text-gray-600 hover:bg-gray-50 hover:text-gray-900">
          <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"/></svg>
          Users
        </a>
      </li>
    </ul>
  </nav>

  <!-- Footer -->
  <div class="border-t border-gray-200 px-3 py-3">
    <a href="/logout" class="flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium text-gray-600 hover:bg-gray-50">
      <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/></svg>
      Logout
    </a>
  </div>
</aside>
```

### Breadcrumbs

```html
<nav class="flex" aria-label="Breadcrumb">
  <ol class="flex items-center gap-1.5 text-sm">
    <li>
      <a href="/" class="text-gray-500 hover:text-gray-700">Home</a>
    </li>
    <li class="text-gray-400">/</li>
    <li>
      <a href="/recipes" class="text-gray-500 hover:text-gray-700">Recipes</a>
    </li>
    <li class="text-gray-400">/</li>
    <li>
      <span class="font-medium text-gray-900" aria-current="page">Thai Green Curry</span>
    </li>
  </ol>
</nav>
```

---

## Modal / Dialog

### Centered Modal with Backdrop

```html
<!-- Backdrop -->
<div class="fixed inset-0 z-40 bg-black/50 backdrop-blur-sm" aria-hidden="true"></div>

<!-- Modal -->
<div class="fixed inset-0 z-50 flex items-center justify-center p-4" role="dialog" aria-modal="true" aria-labelledby="modal-title">
  <div class="w-full max-w-md rounded-2xl bg-white p-6 shadow-xl">
    <!-- Header -->
    <div class="flex items-start justify-between">
      <h2 id="modal-title" class="text-lg font-semibold text-gray-900">Delete Recipe?</h2>
      <button class="rounded-lg p-1 text-gray-400 hover:bg-gray-100 hover:text-gray-500" aria-label="Close">
        <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
        </svg>
      </button>
    </div>

    <!-- Body -->
    <p class="mt-3 text-sm text-gray-500">
      This action cannot be undone. The recipe and all associated data will be permanently removed.
    </p>

    <!-- Footer -->
    <div class="mt-6 flex justify-end gap-3">
      <button class="rounded-lg border border-gray-300 px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50">
        Cancel
      </button>
      <button class="rounded-lg bg-red-600 px-4 py-2 text-sm font-medium text-white hover:bg-red-700">
        Delete
      </button>
    </div>
  </div>
</div>
```

### Mobile Bottom Sheet

```html
<!-- Backdrop -->
<div class="fixed inset-0 z-40 bg-black/50"></div>

<!-- Bottom Sheet -->
<div class="fixed inset-x-0 bottom-0 z-50 rounded-t-2xl bg-white pb-safe">
  <!-- Drag handle -->
  <div class="flex justify-center pt-3">
    <div class="h-1.5 w-10 rounded-full bg-gray-300"></div>
  </div>

  <!-- Content -->
  <div class="max-h-[70vh] overflow-y-auto px-4 pb-6 pt-4">
    <h3 class="text-lg font-semibold text-gray-900">Filters</h3>
    <div class="mt-4 space-y-4">
      <!-- Filter content here -->
    </div>
    <button class="mt-6 w-full rounded-lg bg-indigo-600 py-3 text-sm font-medium text-white hover:bg-indigo-700">
      Apply Filters
    </button>
  </div>
</div>
```

---

## Toast / Notification

### Toast Stack (Bottom Right)

```html
<div class="fixed bottom-4 right-4 z-50 flex flex-col gap-3">
  <!-- Success toast -->
  <div class="flex w-80 items-start gap-3 rounded-lg border border-green-200 bg-green-50 p-4 shadow-lg" role="alert">
    <svg class="h-5 w-5 flex-shrink-0 text-green-500" fill="currentColor" viewBox="0 0 20 20">
      <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
    </svg>
    <div class="flex-1">
      <p class="text-sm font-medium text-green-800">Recipe saved!</p>
      <p class="mt-0.5 text-xs text-green-600">Your recipe has been published.</p>
    </div>
    <button class="text-green-400 hover:text-green-600" aria-label="Dismiss">
      <svg class="h-4 w-4" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"/></svg>
    </button>
  </div>

  <!-- Error toast -->
  <div class="flex w-80 items-start gap-3 rounded-lg border border-red-200 bg-red-50 p-4 shadow-lg" role="alert">
    <svg class="h-5 w-5 flex-shrink-0 text-red-500" fill="currentColor" viewBox="0 0 20 20">
      <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-13a1 1 0 10-2 0v4a1 1 0 102 0V5zm-1 8a1 1 0 100 2 1 1 0 000-2z" clip-rule="evenodd"/>
    </svg>
    <div class="flex-1">
      <p class="text-sm font-medium text-red-800">Failed to save</p>
      <p class="mt-0.5 text-xs text-red-600">Please check your connection and try again.</p>
    </div>
    <button class="text-red-400 hover:text-red-600" aria-label="Dismiss">
      <svg class="h-4 w-4" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"/></svg>
    </button>
  </div>
</div>
```

---

## Table Patterns

### Sortable, Filterable Table

```html
<div class="overflow-hidden rounded-xl border border-gray-200 bg-white">
  <!-- Table toolbar -->
  <div class="flex items-center justify-between border-b border-gray-200 px-4 py-3">
    <div class="relative">
      <input
        type="text"
        placeholder="Search recipes..."
        class="w-64 rounded-lg border border-gray-300 py-1.5 pl-9 pr-3 text-sm focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
      />
      <svg class="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
      </svg>
    </div>
    <select class="rounded-lg border border-gray-300 px-3 py-1.5 text-sm text-gray-700 focus:border-indigo-500 focus:outline-none">
      <option>All Categories</option>
      <option>Italian</option>
      <option>Thai</option>
      <option>Mexican</option>
    </select>
  </div>

  <!-- Table -->
  <div class="overflow-x-auto">
    <table class="w-full text-left text-sm">
      <thead class="bg-gray-50 text-xs uppercase text-gray-500">
        <tr>
          <th class="px-4 py-3">
            <button class="group inline-flex items-center gap-1 font-medium">
              Recipe
              <svg class="h-3 w-3 text-gray-400 group-hover:text-gray-600" fill="currentColor" viewBox="0 0 20 20"><path d="M5.23 7.21a.75.75 0 011.06.02L10 11.168l3.71-3.938a.75.75 0 111.08 1.04l-4.25 4.5a.75.75 0 01-1.08 0l-4.25-4.5a.75.75 0 01.02-1.06z"/></svg>
            </button>
          </th>
          <th class="px-4 py-3">Category</th>
          <th class="px-4 py-3">Time</th>
          <th class="px-4 py-3">Rating</th>
          <th class="px-4 py-3 text-right">Actions</th>
        </tr>
      </thead>
      <tbody class="divide-y divide-gray-200">
        <tr class="hover:bg-gray-50">
          <td class="px-4 py-3 font-medium text-gray-900">Thai Green Curry</td>
          <td class="px-4 py-3">
            <span class="inline-flex rounded-full bg-amber-100 px-2 py-0.5 text-xs font-medium text-amber-700">Thai</span>
          </td>
          <td class="px-4 py-3 text-gray-500">35 min</td>
          <td class="px-4 py-3 text-gray-500">4.8</td>
          <td class="px-4 py-3 text-right">
            <button class="text-indigo-600 hover:text-indigo-800">Edit</button>
          </td>
        </tr>
        <tr class="hover:bg-gray-50">
          <td class="px-4 py-3 font-medium text-gray-900">Margherita Pizza</td>
          <td class="px-4 py-3">
            <span class="inline-flex rounded-full bg-red-100 px-2 py-0.5 text-xs font-medium text-red-700">Italian</span>
          </td>
          <td class="px-4 py-3 text-gray-500">45 min</td>
          <td class="px-4 py-3 text-gray-500">4.6</td>
          <td class="px-4 py-3 text-right">
            <button class="text-indigo-600 hover:text-indigo-800">Edit</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>

  <!-- Pagination -->
  <div class="flex items-center justify-between border-t border-gray-200 px-4 py-3">
    <p class="text-sm text-gray-500">Showing <span class="font-medium">1</span> to <span class="font-medium">10</span> of <span class="font-medium">42</span></p>
    <div class="flex gap-1">
      <button class="rounded-lg border border-gray-300 px-3 py-1 text-sm text-gray-500 hover:bg-gray-50">Previous</button>
      <button class="rounded-lg bg-indigo-600 px-3 py-1 text-sm text-white">1</button>
      <button class="rounded-lg border border-gray-300 px-3 py-1 text-sm text-gray-500 hover:bg-gray-50">2</button>
      <button class="rounded-lg border border-gray-300 px-3 py-1 text-sm text-gray-500 hover:bg-gray-50">3</button>
      <button class="rounded-lg border border-gray-300 px-3 py-1 text-sm text-gray-500 hover:bg-gray-50">Next</button>
    </div>
  </div>
</div>
```

---

## Skeleton Loading

### Card Skeleton

```html
<div class="animate-pulse overflow-hidden rounded-xl bg-white shadow-md">
  <div class="h-48 bg-gray-200"></div>
  <div class="p-5 space-y-3">
    <div class="h-5 w-3/4 rounded bg-gray-200"></div>
    <div class="h-4 w-full rounded bg-gray-200"></div>
    <div class="h-4 w-1/2 rounded bg-gray-200"></div>
    <div class="flex items-center justify-between pt-2">
      <div class="h-4 w-16 rounded bg-gray-200"></div>
      <div class="h-8 w-16 rounded-lg bg-gray-200"></div>
    </div>
  </div>
</div>
```

### Table Row Skeleton

```html
<tr class="animate-pulse">
  <td class="px-4 py-3"><div class="h-4 w-32 rounded bg-gray-200"></div></td>
  <td class="px-4 py-3"><div class="h-5 w-16 rounded-full bg-gray-200"></div></td>
  <td class="px-4 py-3"><div class="h-4 w-14 rounded bg-gray-200"></div></td>
  <td class="px-4 py-3"><div class="h-4 w-8 rounded bg-gray-200"></div></td>
  <td class="px-4 py-3 text-right"><div class="ml-auto h-4 w-10 rounded bg-gray-200"></div></td>
</tr>
```

### Text Block Skeleton

```html
<div class="animate-pulse space-y-3">
  <div class="h-6 w-1/3 rounded bg-gray-200"></div>
  <div class="space-y-2">
    <div class="h-4 w-full rounded bg-gray-200"></div>
    <div class="h-4 w-full rounded bg-gray-200"></div>
    <div class="h-4 w-5/6 rounded bg-gray-200"></div>
    <div class="h-4 w-2/3 rounded bg-gray-200"></div>
  </div>
</div>
```

### Form Skeleton

```html
<div class="animate-pulse space-y-5">
  <div>
    <div class="h-4 w-20 rounded bg-gray-200"></div>
    <div class="mt-1.5 h-10 w-full rounded-lg bg-gray-200"></div>
  </div>
  <div>
    <div class="h-4 w-28 rounded bg-gray-200"></div>
    <div class="mt-1.5 h-10 w-full rounded-lg bg-gray-200"></div>
  </div>
  <div>
    <div class="h-4 w-24 rounded bg-gray-200"></div>
    <div class="mt-1.5 h-24 w-full rounded-lg bg-gray-200"></div>
  </div>
  <div class="h-10 w-28 rounded-lg bg-gray-200"></div>
</div>
```
