# Modern JavaScript 2026 Reference

Up-to-date JavaScript language features, APIs, and best practices relevant for React + Vite + API-driven applications.

## Language Version Support

### ES2024 Features (Current)

#### `Object.groupBy` and `Map.groupBy`

```javascript
const users = [
    { name: 'Alice', role: 'admin' },
    { name: 'Bob', role: 'user' },
    { name: 'Charlie', role: 'admin' },
];

// Group by role using Object.groupBy
const groupedByRole = Object.groupBy(users, ({ role }) => role);
// {
//   admin: [{name: 'Alice', role: 'admin'}, {name: 'Charlie', role: 'admin'}],
//   user: [{name: 'Bob', role: 'user'}]
// }

// Group by role using Map.groupBy
const groupedMap = Map.groupBy(users, ({ role }) => role);
// Map(2) { 'admin' => [...], 'user' => [...] }
```

#### Promise.withResolvers

```javascript
// Create promise with explicit resolve/reject functions
const { promise, resolve, reject } = Promise.withResolvers();

setTimeout(() => resolve('Done!'), 1000);

promise.then(result => console.log(result)); // "Done!"
```

### ES2023 Features

#### Non-mutating Array Methods

```javascript
const numbers = [3, 1, 4, 1, 5];

// New methods that don't mutate original array
const sorted = numbers.toSorted();
const reversed = numbers.toReversed();
const spliced = numbers.toSpliced(2, 1, 99); // remove 1 item at index 2, insert 99
const updated = numbers.with(0, 100); // replace item at index 0

console.log(numbers);  // [3, 1, 4, 1, 5] (unchanged)
console.log(sorted);   // [1, 1, 3, 4, 5]
console.log(reversed); // [5, 1, 4, 1, 3]
console.log(spliced);  // [3, 1, 99, 1, 5]
console.log(updated);  // [100, 1, 4, 1, 5]
```

### ES2022 Features

#### Top-level await

```javascript
// In ES modules (.mjs or with "type": "module")
const config = await fetch('/api/config').then(res => res.json());

export const apiBaseUrl = config.apiBaseUrl;
```

#### Class Fields and Private Methods

```javascript
class RecipeService {
    #apiBaseUrl = '/api';
    #cache = new Map();

    async getRecipe(id) {
        if (this.#cache.has(id)) {
            return this.#cache.get(id);
        }

        const response = await fetch(`${this.#apiBaseUrl}/recipes/${id}`);
        const recipe = await response.json();

        this.#cache.set(id, recipe);
        return recipe;
    }

    #validateId(id) {
        if (!Number.isInteger(id) || id <= 0) {
            throw new Error('Invalid recipe ID');
        }
    }
}
```

## Asynchronous JavaScript Patterns

### Promise Composition

```javascript
// Promise.all - all must succeed
const [users, recipes, stats] = await Promise.all([
    fetch('/api/users').then(r => r.json()),
    fetch('/api/recipes').then(r => r.json()),
    fetch('/api/stats').then(r => r.json()),
]);

// Promise.allSettled - handle partial failures
const results = await Promise.allSettled([
    fetch('/api/users').then(r => r.json()),
    fetch('/api/recipes').then(r => r.json()),
    fetch('/api/notifications').then(r => r.json()),
]);

results.forEach((result, index) => {
    if (result.status === 'fulfilled') {
        console.log(`Request ${index} succeeded:`, result.value);
    } else {
        console.error(`Request ${index} failed:`, result.reason);
    }
});

// Promise.any - first successful one wins
const firstResponse = await Promise.any([
    fetch('/api-mirror1/data').then(r => r.json()),
    fetch('/api-mirror2/data').then(r => r.json()),
    fetch('/api-mirror3/data').then(r => r.json()),
]);
```

### AbortController for Request Cancellation

```javascript
const controller = new AbortController();
const signal = controller.signal;

try {
    const response = await fetch('/api/recipes', { signal });
    const data = await response.json();
    console.log(data);
} catch (error) {
    if (error.name === 'AbortError') {
        console.log('Request was cancelled');
    } else {
        console.error('Request failed:', error);
    }
}

// Cancel request
controller.abort();
```

## Web Platform APIs (2026)

### URL and URLSearchParams

```javascript
// Parse URL
const url = new URL('https://example.com/recipes?category=dinner&difficulty=easy');
console.log(url.pathname); // '/recipes'

// Build query params safely
const params = new URLSearchParams();
params.append('category', 'dinner');
params.append('difficulty', 'easy');
params.append('page', '1');

const apiUrl = `/api/recipes?${params.toString()}`;
// '/api/recipes?category=dinner&difficulty=easy&page=1'
```

### Intl APIs for Formatting

```javascript
// Number formatting
const formatter = new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
});
console.log(formatter.format(1234.56)); // '$1,234.56'

// Date formatting
const dateFormatter = new Intl.DateTimeFormat('en-US', {
    dateStyle: 'medium',
    timeStyle: 'short',
});
console.log(dateFormatter.format(new Date()));

// Relative time
const relativeFormatter = new Intl.RelativeTimeFormat('en', { numeric: 'auto' });
console.log(relativeFormatter.format(-2, 'day')); // '2 days ago'

// List formatting
const listFormatter = new Intl.ListFormat('en', {
    style: 'long',
    type: 'conjunction',
});
console.log(listFormatter.format(['salt', 'pepper', 'olive oil']));
// 'salt, pepper, and olive oil'
```

### Structured Clone

```javascript
const original = {
    id: 1,
    name: 'Recipe',
    ingredients: ['salt', 'pepper'],
    metadata: { difficulty: 'easy' },
};

// Deep clone
const clone = structuredClone(original);
clone.metadata.difficulty = 'hard';

console.log(original.metadata.difficulty); // 'easy' (unchanged)
console.log(clone.metadata.difficulty);    // 'hard'
```

## Error Handling Patterns

### Custom Error Classes

```javascript
class ApiError extends Error {
    constructor(message, status, data = null) {
        super(message);
        this.name = 'ApiError';
        this.status = status;
        this.data = data;
    }
}

class ValidationError extends Error {
    constructor(message, fieldErrors = {}) {
        super(message);
        this.name = 'ValidationError';
        this.fieldErrors = fieldErrors;
    }
}

async function fetchRecipe(id) {
    const response = await fetch(`/api/recipes/${id}`);

    if (!response.ok) {
        const errorData = await response.json().catch(() => null);

        if (response.status === 404) {
            throw new ApiError('Recipe not found', 404, errorData);
        }

        if (response.status === 422) {
            throw new ValidationError(
                'Validation failed',
                errorData?.errors || {}
            );
        }

        throw new ApiError(
            `Request failed with status ${response.status}`,
            response.status,
            errorData
        );
    }

    return response.json();
}
```

### Error Boundary Pattern (for React)

```javascript
function handleAsyncError(error, context = '') {
    console.error(`Error in ${context}:`, error);

    // Log to monitoring service in production
    if (import.meta.env.PROD) {
        // Example: sendToMonitoring(error, context);
    }

    // Return user-friendly message
    if (error instanceof ValidationError) {
        return {
            type: 'validation',
            message: error.message,
            fieldErrors: error.fieldErrors,
        };
    }

    if (error instanceof ApiError) {
        switch (error.status) {
            case 401:
                return { type: 'auth', message: 'Please sign in again.' };
            case 403:
                return { type: 'permission', message: 'Access denied.' };
            case 404:
                return { type: 'not-found', message: 'Resource not found.' };
            default:
                return { type: 'api', message: 'Server error. Please try again.' };
        }
    }

    return { type: 'unknown', message: 'Something went wrong.' };
}
```

## Performance Optimizations

### Debounce and Throttle

```javascript
// Debounce: execute after user stops triggering
function debounce(fn, delay = 300) {
    let timeoutId;

    return function debounced(...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => fn.apply(this, args), delay);
    };
}

// Throttle: execute at most once per interval
function throttle(fn, interval = 300) {
    let lastCall = 0;

    return function throttled(...args) {
        const now = Date.now();

        if (now - lastCall >= interval) {
            lastCall = now;
            fn.apply(this, args);
        }
    };
}

// Usage examples
const debouncedSearch = debounce((query) => {
    fetch(`/api/search?q=${encodeURIComponent(query)}`);
}, 500);

const throttledScroll = throttle(() => {
    console.log('Scroll position:', window.scrollY);
}, 100);
```

### Request Deduplication

```javascript
const pendingRequests = new Map();

async function deduplicatedFetch(url, options = {}) {
    const key = `${url}:${JSON.stringify(options)}`;

    if (pendingRequests.has(key)) {
        return pendingRequests.get(key);
    }

    const promise = fetch(url, options)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }
            return response.json();
        })
        .finally(() => {
            pendingRequests.delete(key);
        });

    pendingRequests.set(key, promise);
    return promise;
}
```

## Security Best Practices

### Input Sanitization

```javascript
function sanitizeHtml(input) {
    const div = document.createElement('div');
    div.textContent = input;
    return div.innerHTML;
}

function validateEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function validatePassword(password) {
    return {
        isValid: password.length >= 8,
        hasUppercase: /[A-Z]/.test(password),
        hasLowercase: /[a-z]/.test(password),
        hasNumber: /\d/.test(password),
        hasSpecial: /[!@#$%^&*]/.test(password),
    };
}
```

### Safe Local Storage

```javascript
class SafeStorage {
    static set(key, value) {
        try {
            localStorage.setItem(key, JSON.stringify(value));
            return true;
        } catch (error) {
            console.error(`Failed to save ${key}:`, error);
            return false;
        }
    }

    static get(key, defaultValue = null) {
        try {
            const item = localStorage.getItem(key);
            return item ? JSON.parse(item) : defaultValue;
        } catch (error) {
            console.error(`Failed to read ${key}:`, error);
            return defaultValue;
        }
    }

    static remove(key) {
        localStorage.removeItem(key);
    }

    static clear() {
        localStorage.clear();
    }
}
```

## Tooling Recommendations (2026)

### Essential Tools
- **Runtime**: Node.js 20+ (LTS)
- **Package Manager**: npm, pnpm, or yarn
- **Bundler**: Vite 6+
- **Linter**: ESLint 9+
- **Formatter**: Prettier 3+
- **Type Checking**: TypeScript 5.7+ (even for JS with JSDoc)
- **Testing**: Vitest + Playwright

### Recommended `package.json` scripts

```json
{
    "scripts": {
        "dev": "vite",
        "build": "vite build",
        "preview": "vite preview",
        "lint": "eslint .",
        "format": "prettier --write .",
        "type-check": "tsc --noEmit",
        "test": "vitest",
        "test:e2e": "playwright test"
    }
}
```

## References

### Official Documentation
- MDN JavaScript Guide: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide
- ECMAScript Specification: https://tc39.es/ecma262/
- JavaScript Compatibility: https://caniuse.com/

### Key Proposals & Features
- TC39 Proposals: https://github.com/tc39/proposals
- V8 Blog (language updates): https://v8.dev/blog

### Best Practices
- Web.dev JavaScript: https://web.dev/learn/javascript/
- JavaScript Info: https://javascript.info/
