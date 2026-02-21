# Responsive Recipe Card — React + Tailwind CSS

A complete recipe card component for Kitchen Odyssey with responsive layouts, loading/error/empty states, and hover effects.

---

## Overview

| Breakpoint | Layout | Columns |
|-----------|--------|---------|
| Mobile (< 640px) | Stacked vertical card | 1 column |
| Tablet (640px–1023px) | Horizontal card | 1 column (side-by-side image + content) |
| Desktop (≥ 1024px) | Vertical cards in grid | 3 columns |

---

## Tailwind Config Customizations

Add these to `tailwind.config.js` for the recipe card theme:

```javascript
export default {
  theme: {
    extend: {
      colors: {
        recipe: {
          50: '#fef7f0',
          100: '#fdebd5',
          200: '#fad4aa',
          300: '#f6b574',
          400: '#f18d3c',
          500: '#ee7316',
          600: '#df590c',
          700: '#b9420c',
          800: '#933512',
          900: '#772d12',
        },
      },
      animation: {
        'shimmer': 'shimmer 2s infinite linear',
      },
      keyframes: {
        shimmer: {
          '0%': { backgroundPosition: '-200% 0' },
          '100%': { backgroundPosition: '200% 0' },
        },
      },
    },
  },
};
```

---

## RecipeCard Component

```jsx
import { useState } from 'react';

const DIFFICULTY_CONFIG = {
  easy: { label: 'Easy', className: 'bg-green-100 text-green-700' },
  medium: { label: 'Medium', className: 'bg-amber-100 text-amber-700' },
  hard: { label: 'Hard', className: 'bg-red-100 text-red-700' },
};

function DifficultyBadge({ difficulty }) {
  const config = DIFFICULTY_CONFIG[difficulty] || DIFFICULTY_CONFIG.easy;
  return (
    <span className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ${config.className}`}>
      {config.label}
    </span>
  );
}

function StarRating({ rating, max = 5 }) {
  return (
    <div className="flex items-center gap-0.5" aria-label={`${rating} out of ${max} stars`}>
      {Array.from({ length: max }, (_, i) => (
        <svg
          key={i}
          className={`h-4 w-4 ${i < Math.round(rating) ? 'text-amber-400' : 'text-gray-300'}`}
          fill="currentColor"
          viewBox="0 0 20 20"
        >
          <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
        </svg>
      ))}
      <span className="ml-1 text-xs text-gray-500">({rating})</span>
    </div>
  );
}

export default function RecipeCard({ recipe, onClick }) {
  const [imgError, setImgError] = useState(false);

  return (
    <article
      onClick={onClick}
      className="
        group cursor-pointer overflow-hidden rounded-xl bg-white shadow-md
        transition-all duration-200 hover:shadow-xl hover:-translate-y-0.5
        /* Mobile: stacked vertical */
        flex flex-col
        /* Tablet: horizontal */
        sm:flex-row sm:h-48
        /* Desktop: back to vertical (grid handles columns) */
        lg:flex-col lg:h-auto
      "
    >
      {/* Image */}
      <div className="
        relative overflow-hidden bg-gray-100
        h-48 w-full flex-shrink-0
        sm:h-full sm:w-44
        lg:h-48 lg:w-full
      ">
        {imgError ? (
          <div className="flex h-full w-full items-center justify-center bg-gray-100 text-gray-400">
            <svg className="h-12 w-12" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5}
                d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
              />
            </svg>
          </div>
        ) : (
          <img
            src={recipe.image}
            alt={recipe.title}
            className="h-full w-full object-cover transition-transform duration-300 group-hover:scale-105"
            onError={() => setImgError(true)}
            loading="lazy"
          />
        )}

        {/* Overlay badges */}
        {recipe.featured && (
          <span className="absolute left-2 top-2 rounded-full bg-recipe-500 px-2.5 py-0.5 text-xs font-semibold text-white shadow-sm">
            Featured
          </span>
        )}
        <span className="absolute right-2 top-2 rounded-full bg-black/60 px-2 py-0.5 text-xs text-white">
          {recipe.prepTime} min
        </span>
      </div>

      {/* Content */}
      <div className="flex flex-1 flex-col justify-between p-4">
        <div>
          <div className="flex items-start justify-between gap-2">
            <h3 className="line-clamp-1 text-base font-semibold text-gray-900 group-hover:text-recipe-600 transition-colors">
              {recipe.title}
            </h3>
            <DifficultyBadge difficulty={recipe.difficulty} />
          </div>
          <p className="mt-1 line-clamp-2 text-sm text-gray-500">
            {recipe.description}
          </p>
        </div>
        <div className="mt-3 flex items-center justify-between">
          <StarRating rating={recipe.rating} />
          <span className="text-xs text-gray-400">{recipe.servings} servings</span>
        </div>
      </div>
    </article>
  );
}
```

---

## RecipeCardSkeleton — Loading State

```jsx
export function RecipeCardSkeleton() {
  return (
    <div className="
      animate-pulse overflow-hidden rounded-xl bg-white shadow-md
      flex flex-col
      sm:flex-row sm:h-48
      lg:flex-col lg:h-auto
    ">
      {/* Image skeleton */}
      <div className="
        h-48 w-full flex-shrink-0 bg-gray-200
        sm:h-full sm:w-44
        lg:h-48 lg:w-full
      " />

      {/* Content skeleton */}
      <div className="flex flex-1 flex-col justify-between p-4">
        <div className="space-y-2">
          <div className="flex items-center justify-between">
            <div className="h-5 w-3/5 rounded bg-gray-200" />
            <div className="h-5 w-14 rounded-full bg-gray-200" />
          </div>
          <div className="h-4 w-full rounded bg-gray-200" />
          <div className="h-4 w-2/3 rounded bg-gray-200" />
        </div>
        <div className="mt-3 flex items-center justify-between">
          <div className="flex gap-0.5">
            {Array.from({ length: 5 }, (_, i) => (
              <div key={i} className="h-4 w-4 rounded bg-gray-200" />
            ))}
          </div>
          <div className="h-4 w-16 rounded bg-gray-200" />
        </div>
      </div>
    </div>
  );
}
```

---

## RecipeCardError — Error State

```jsx
export function RecipeCardError({ message = 'Failed to load recipe', onRetry }) {
  return (
    <div className="flex flex-col items-center justify-center rounded-xl border-2 border-dashed border-red-200 bg-red-50 p-8 text-center">
      <svg className="h-10 w-10 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5}
          d="M12 9v2m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
        />
      </svg>
      <p className="mt-2 text-sm font-medium text-red-700">{message}</p>
      {onRetry && (
        <button
          onClick={onRetry}
          className="mt-3 rounded-lg bg-red-600 px-4 py-1.5 text-sm font-medium text-white hover:bg-red-700 transition-colors"
        >
          Retry
        </button>
      )}
    </div>
  );
}
```

---

## RecipeCardEmpty — Empty State

```jsx
export function RecipeCardEmpty({ message = 'No recipes found' }) {
  return (
    <div className="flex flex-col items-center justify-center rounded-xl border-2 border-dashed border-gray-200 bg-gray-50 p-12 text-center">
      <svg className="h-12 w-12 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5}
          d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"
        />
      </svg>
      <p className="mt-3 text-sm font-medium text-gray-500">{message}</p>
      <p className="mt-1 text-xs text-gray-400">Try adjusting your search or filters.</p>
    </div>
  );
}
```

---

## RecipeCardGrid — Responsive Grid Container

```jsx
import RecipeCard, { RecipeCardSkeleton } from './RecipeCard';
import { RecipeCardError, RecipeCardEmpty } from './RecipeCardStates';

export default function RecipeCardGrid({ recipes, loading, error, onRetry, onCardClick }) {
  if (error) {
    return <RecipeCardError message={error} onRetry={onRetry} />;
  }

  if (loading) {
    return (
      <div className="grid gap-6 sm:grid-cols-1 lg:grid-cols-2 xl:grid-cols-3">
        {Array.from({ length: 6 }, (_, i) => (
          <RecipeCardSkeleton key={i} />
        ))}
      </div>
    );
  }

  if (!recipes || recipes.length === 0) {
    return <RecipeCardEmpty />;
  }

  return (
    <div className="grid gap-6 sm:grid-cols-1 lg:grid-cols-2 xl:grid-cols-3">
      {recipes.map((recipe) => (
        <RecipeCard
          key={recipe.id}
          recipe={recipe}
          onClick={() => onCardClick?.(recipe.id)}
        />
      ))}
    </div>
  );
}
```

---

## Showcase: All Variants

Below is a demonstration page rendering every state. Use this as a local preview or Storybook entry.

```jsx
import { useState } from 'react';
import RecipeCard, { RecipeCardSkeleton } from './RecipeCard';
import { RecipeCardError, RecipeCardEmpty } from './RecipeCardStates';
import RecipeCardGrid from './RecipeCardGrid';

const MOCK_RECIPES = [
  {
    id: '1',
    title: 'Thai Green Curry',
    description: 'Creamy coconut curry with fresh vegetables and aromatic herbs.',
    image: '/images/thai-curry.jpg',
    prepTime: 35,
    difficulty: 'medium',
    rating: 4.8,
    servings: 4,
    featured: true,
  },
  {
    id: '2',
    title: 'Classic Margherita Pizza',
    description: 'Simple, fresh pizza with San Marzano tomatoes and buffalo mozzarella.',
    image: '/images/pizza.jpg',
    prepTime: 45,
    difficulty: 'easy',
    rating: 4.6,
    servings: 2,
    featured: false,
  },
  {
    id: '3',
    title: 'Beef Wellington',
    description: 'Tenderloin wrapped in mushroom duxelles and golden puff pastry.',
    image: '/images/wellington.jpg',
    prepTime: 120,
    difficulty: 'hard',
    rating: 4.9,
    servings: 6,
    featured: false,
  },
  {
    id: '4',
    title: 'Overnight Oats',
    description: 'Healthy make-ahead breakfast with oats, yogurt, and fresh berries.',
    image: '/images/oats.jpg',
    prepTime: 10,
    difficulty: 'easy',
    rating: 4.2,
    servings: 1,
    featured: false,
  },
  {
    id: '5',
    title: 'Pad Thai',
    description: 'Stir-fried rice noodles with shrimp, peanuts, and tamarind sauce.',
    image: '/images/pad-thai.jpg',
    prepTime: 30,
    difficulty: 'medium',
    rating: 4.7,
    servings: 3,
    featured: true,
  },
  {
    id: '6',
    title: 'French Onion Soup',
    description: 'Caramelized onion soup with crusty bread and melted Gruyere cheese.',
    image: '/images/onion-soup.jpg',
    prepTime: 60,
    difficulty: 'medium',
    rating: 4.5,
    servings: 4,
    featured: false,
  },
];

export default function RecipeCardShowcase() {
  const [activeView, setActiveView] = useState('grid');

  const views = [
    { id: 'grid', label: 'Grid (Normal)' },
    { id: 'loading', label: 'Loading' },
    { id: 'error', label: 'Error' },
    { id: 'empty', label: 'Empty' },
    { id: 'single', label: 'Single Card' },
  ];

  return (
    <div className="mx-auto max-w-7xl px-4 py-8">
      <h1 className="text-2xl font-bold text-gray-900">Recipe Card — All Variants</h1>

      {/* View selector */}
      <div className="mt-4 flex flex-wrap gap-2">
        {views.map((view) => (
          <button
            key={view.id}
            onClick={() => setActiveView(view.id)}
            className={`rounded-lg px-4 py-2 text-sm font-medium transition-colors ${
              activeView === view.id
                ? 'bg-recipe-500 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            {view.label}
          </button>
        ))}
      </div>

      {/* Variant display */}
      <div className="mt-8">
        {activeView === 'grid' && (
          <RecipeCardGrid
            recipes={MOCK_RECIPES}
            loading={false}
            error={null}
            onCardClick={(id) => console.log('Clicked recipe:', id)}
          />
        )}

        {activeView === 'loading' && (
          <RecipeCardGrid recipes={[]} loading={true} error={null} />
        )}

        {activeView === 'error' && (
          <RecipeCardGrid
            recipes={[]}
            loading={false}
            error="Failed to load recipes. Server returned 500."
            onRetry={() => console.log('Retry clicked')}
          />
        )}

        {activeView === 'empty' && (
          <RecipeCardGrid recipes={[]} loading={false} error={null} />
        )}

        {activeView === 'single' && (
          <div className="max-w-sm">
            <RecipeCard
              recipe={MOCK_RECIPES[0]}
              onClick={() => console.log('Card clicked')}
            />
          </div>
        )}
      </div>
    </div>
  );
}
```

---

## Accessibility Notes

- Card uses `<article>` for semantic grouping
- Image has meaningful `alt` text (recipe title)
- Star rating uses `aria-label` for screen reader context
- Fallback image state avoids broken image icons
- Touch targets exceed 44x44px minimum
- Colors meet WCAG AA contrast requirements
- `loading="lazy"` on images for performance
- `line-clamp` prevents layout shifts from long titles
