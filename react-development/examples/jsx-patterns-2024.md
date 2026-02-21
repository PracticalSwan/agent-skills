# React JSX Patterns with React 19+

Modern JSX patterns and component examples using React 19+ features, TypeScript, and ES6+ syntax.

## JSX Fundamentals

### Component Structure

```jsx
import { useState, useEffect } from 'react';

/**
 * RecipeCard component with proper typing and hooks usage
 * Displays recipe information with interactive elements
 */
export function RecipeCard({ recipe, onLike, onEdit }) {
    const [isLiked, setIsLiked] = useState(false);
    const [imageError, setImageError] = useState(false);

    useEffect(() => {
        // Check if recipe is already liked
        setIsLiked(checkIfLiked(recipe.id));
    }, [recipe.id]);

    const handleLike = () => {
        setIsLiked(!isLiked);
        onLike?.(recipe.id);
    };

    if (imageError) {
        return (
            <div className="recipe-card fallback">
                <h3>{recipe.title}</h3>
                <p>No image available</p>
            </div>
        );
    }

    return (
        <article className="recipe-card" data-recipe-id={recipe.id}>
            <div className="recipe-image">
                <img
                    src={recipe.imageUrl}
                    alt={recipe.title}
                    onError={() => setImageError(true)}
                    loading="lazy"
                />
            </div>

            <div className="recipe-content">
                <div className="recipe-header">
                    <h2 className="recipe-title">{recipe.title}</h2>
                    <span className={`badge ${recipe.difficulty}`}>
                        {recipe.difficulty}
                    </span>
                </div>

                <p className="recipe-description">
                    {recipe.description}
                </p>

                <div className="recipe-meta">
                    <span>⏱ {recipe.prepTime} min</span>
                    <span>⏰ {recipe.cookTime} min</span>
                    <span>👥 {recipe.servings} servings</span>
                </div>

                <div className="recipe-actions">
                    <button
                        className={`like-button ${isLiked ? 'liked' : ''}`}
                        onClick={handleLike}
                        aria-label="Like recipe"
                        aria-pressed={isLiked}
                    >
                        {isLiked ? '❤️' : '🤍'}
                    </button>

                    <button
                        className="edit-button"
                        onClick={() => onEdit?.(recipe.id)}
                        aria-label="Edit recipe"
                    >
                        ✏️ Edit
                    </button>
                </div>
            </div>
        </article>
    );
}
```

### Conditional Rendering

```jsx
// Multiple conditional patterns
function RecipeList({ recipes, loading, error }) {
    // Pattern 1: Loading state
    if (loading) {
        return <LoadingSpinner message="Loading recipes..." />;
    }

    // Pattern 2: Error state
    if (error) {
        return (
            <ErrorMessage
                title="Failed to load recipes"
                message={error.message}
                onRetry={() => window.location.reload()}
            />
        );
    }

    // Pattern 3: Empty state (guard clause)
    if (recipes.length === 0) {
        return (
            <EmptyState
                icon="🍳"
                title="No recipes found"
                description="Be the first to add a recipe!"
            />
        );
    }

    // Pattern 4: Render list
    return (
        <div className="recipe-list">
            {recipes.map((recipe) => (
                <RecipeCard key={recipe.id} recipe={recipe} />
            ))}
        </div>
    );
}

// Conditional rendering with ternary
function RecipeStatus({ status }) {
    return (
        <span className={`status-badge status-${status}`}>
            {status === 'published' && '✅ Published'}
            {status === 'pending' && '⏳ Pending'}
            {status === 'rejected' && '❌ Rejected'}
        </span>
    );
}

// Conditional rendering with logical &&
function FavoriteButton({ isFavorited, onToggle }) {
    return (
        <button
            className="favorite-button"
            onClick={onToggle}
            aria-label={isFavorited ? 'Remove from favorites' : 'Add to favorites'}
        >
            {isFavorited && <span className="fill">⭐</span>}
            {!isFavorited && <span className="outline">☆</span>}
        </button>
    );
}
```

### Lists & Keys

```jsx
// Correct key usage patterns
function IngredientList({ ingredients }) {
    // ✅ GOOD: Using unique IDs as keys
    return (
        <ul className="ingredient-list">
            {ingredients.map((ingredient) => (
                <li key={ingredient.id} className="ingredient-item">
                    <span className="name">{ingredient.name}</span>
                    <span className="quantity">
                        {ingredient.quantity} {ingredient.unit}
                    </span>
                </li>
            ))}
        </ul>
    );
}

// ✅ GOOD: Using index as key ONLY when list is static and filtered
function FilterableList({ items, filter }) {
    const filtered = items.filter(item =>
        item.name.toLowerCase().includes(filter.toLowerCase())
    );

    return (
        <ul>
            {filtered.map((item, index) => (
                <li key={`${item.id}-${index}`}>
                    {item.name}
                </li>
            ))}
        </ul>
    );
}

// ❌ BAD: Using index as key for dynamic lists
function IngredientListBAD({ ingredients }) {
    return (
        <ul>
            {ingredients.map((ingredient, index) => (
                <li key={index}> {/* DON'T DO THIS */}
                    {ingredient.name}
                </li>
            ))}
        </ul>
    );
}
```

## Advanced JSX Patterns

### Composition

```jsx
// Compound components for flexible composition
function RecipeCard({ children, featured = false }) {
    return (
        <article className={`recipe-card ${featured ? 'featured' : ''}`}>
            {children}
        </article>
    );
}

RecipeCard.Image = ({ src, alt }) => (
    <div className="recipe-card__image">
        <img src={src} alt={alt} loading="lazy" />
    </div>
);

RecipeCard.Header = ({ children }) => (
    <header className="recipe-card__header">
        {children}
    </header>
);

RecipeCard.Body = ({ children }) => (
    <div className="recipe-card__body">
        {children}
    </div>
);

RecipeCard.Footer = ({ children }) => (
    <footer className="recipe-card__footer">
        {children}
    </footer>
);

// Usage
function RecipeDisplay({ recipe }) {
    return (
        <RecipeCard featured={recipe.featured}>
            <RecipeCard.Image src={recipe.imageUrl} alt={recipe.title} />
            <RecipeCard.Header>
                <h2>{recipe.title}</h2>
                <RecipeDifficulty difficulty={recipe.difficulty} />
            </RecipeCard.Header>
            <RecipeCard.Body>
                <p>{recipe.description}</p>
                <RecipeTags tags={recipe.tags} />
            </RecipeCard.Body>
            <RecipeCard.Footer>
                <LikeButton recipeId={recipe.id} />
                <FavoriteButton recipeId={recipe.id} />
            </RecipeCard.Footer>
        </RecipeCard>
    );
}
```

### Render Props & Children

```jsx
// Render prop for conditional rendering
function RecipeList({ recipes, loading, renderEmpty }) {
    if (loading) return <LoadingSpinner />;

    return (
        <ul className="recipe-list">
            {recipes.length === 0 ? (
                renderEmpty?.()
            ) : (
                recipes.map((recipe) => (
                    <RecipeCard key={recipe.id} recipe={recipe} />
                ))
            )}
        </ul>
    );
}

// Usage
<RecipeList
    recipes={recipes}
    loading={loading}
    renderEmpty={() => (
        <EmptyState
            title="No recipes yet"
            description="Create your first recipe to get started!"
            icon="🍳"
        />
    )}
/>

// Children as render function
function DataList({ data, renderItem }) {
    return (
        <ul className="data-list">
            {data.map((item, index) => renderItem?.(item, index))}
        </ul>
    );
}

function UsersPage() {
    const users = useFetchUsers();

    return (
        <DataList
            data={users}
            renderItem={(user, index) => (
                <li key={user.id} className="user-item">
                    <span className="rank">#{index + 1}</span>
                    <span className="name">{user.name}</span>
                </li>
            )}
        />
    );
}
```

### Higher-Order Components (HOCs)

```jsx
// HOC for loading state
function withLoading(WrappedComponent) {
    return function LoadingHOC(props) {
        const [loading, setLoading] = useState(false);

        return (
            <>
                {loading && <GlobalLoader />}
                <WrappedComponent
                    {...props}
                    setLoading={setLoading}
                    isLoading={loading}
                />
            </>
        );
    };
}

// Usage
const RecipeFormWithLoading = withLoading(RecipeForm);

function CreateRecipe() {
    return (
        <RecipeFormWithLoading
            onSubmit={handleSubmit}
            onCancel={handleCancel}
        />
    );
}

// HOC for authentication check
function withAuth(WrappedComponent) {
    return function AuthenticatedComponent(props) {
        const user = useAuth();

        if (!user) {
            return <Navigate to="/login" replace />;
        }

        return <WrappedComponent user={user} {...props} />;
    };
}

// Usage
const UserProfile = withAuth(function Profile({ user }) {
    return (
        <div className="profile">
            <h1>{user.name}</h1>
            {/* Profile content */}
        </div>
    );
});
```

## Forms in JSX

### Controlled Components

```jsx
import { useState } from 'react';

/**
 * RecipeForm component with controlled inputs and validation
 */
export function RecipeForm({ initialData, onSubmit, onCancel }) {
    const [formData, setFormData] = useState({
        title: initialData?.title || '',
        description: initialData?.description || '',
        category: initialData?.category || 'Uncategorized',
        difficulty: initialData?.difficulty || 'Medium',
        prepTime: initialData?.prepTime || 0,
        cookTime: initialData?.cookTime || 0,
        servings: initialData?.servings || 1,
    });

    const [errors, setErrors] = useState({});
    const [isSubmitting, setIsSubmitting] = useState(false);

    const validateField = (name, value) => {
        const newErrors = { ...errors };

        switch (name) {
            case 'title':
                if (value.length < 3) {
                    newErrors.title = 'Title must be at least 3 characters';
                } else if (value.length > 200) {
                    newErrors.title = 'Title must be less than 200 characters';
                } else {
                    delete newErrors.title;
                }
                break;
            case 'description':
                if (value.length > 1000) {
                    newErrors.description = 'Description is too long';
                } else {
                    delete newErrors.description;
                }
                break;
            case 'prepTime':
            case 'cookTime':
                if (value < 0) {
                    newErrors[name] = 'Time must be positive';
                } else {
                    delete newErrors[name];
                }
                break;
            default:
                break;
        }

        setErrors(newErrors);
    };

    const handleChange = (event) => {
        const { name, value, type } = event.target;

        setFormData(prev => ({
            ...prev,
            [name]: type === 'number' ? parseInt(value) || 0 : value,
        }));

        validateField(name, value);
    };

    const handleSubmit = async (event) => {
        event.preventDefault();

        // Check for remaining errors
        if (Object.keys(errors).length > 0) {
            setIsSubmitting(true);
            try {
                await onSubmit(formData);
            } catch (error) {
                setErrors({ submit: error.message });
            } finally {
                setIsSubmitting(false);
            }
        }
    };

    return (
        <form onSubmit={handleSubmit} className="recipe-form" noValidate>
            <div className="form-group">
                <label htmlFor="title">
                    Recipe Title <span className="required">*</span>
                </label>
                <input
                    id="title"
                    name="title"
                    type="text"
                    value={formData.title}
                    onChange={handleChange}
                    className={errors.title ? 'error' : ''}
                    aria-invalid={!!errors.title}
                    aria-describedby="title-error"
                    required
                    maxLength={200}
                />
                {errors.title && (
                    <span id="title-error" className="error-message">
                        {errors.title}
                    </span>
                )}
            </div>

            <div className="form-group">
                <label htmlFor="description">Description</label>
                <textarea
                    id="description"
                    name="description"
                    value={formData.description}
                    onChange={handleChange}
                    className={errors.description ? 'error' : ''}
                    rows={4}
                    maxLength={1000}
                    aria-invalid={!!errors.description}
                    aria-describedby="description-error"
                />
                {errors.description && (
                    <span id="description-error" className="error-message">
                        {errors.description}
                    </span>
                )}
            </div>

            <div className="form-row">
                <div className="form-group">
                    <label htmlFor="category">Category</label>
                    <select
                        id="category"
                        name="category"
                        value={formData.category}
                        onChange={handleChange}
                    >
                        <option value="Uncategorized">Uncategorized</option>
                        <option value="Breakfast">Breakfast</option>
                        <option value="Lunch">Lunch</option>
                        <option value="Dinner">Dinner</option>
                        <option value="Dessert">Dessert</option>
                    </select>
                </div>

                <div className="form-group">
                    <label htmlFor="difficulty">Difficulty</label>
                    <select
                        id="difficulty"
                        name="difficulty"
                        value={formData.difficulty}
                        onChange={handleChange}
                    >
                        <option value="Easy">Easy</option>
                        <option value="Medium">Medium</option>
                        <option value="Hard">Hard</option>
                    </select>
                </div>
            </div>

            <div className="form-row">
                <div className="form-group">
                    <label htmlFor="prepTime">Prep Time (minutes)</label>
                    <input
                        id="prepTime"
                        name="prepTime"
                        type="number"
                        min="0"
                        value={formData.prepTime}
                        onChange={handleChange}
                        aria-invalid={!!errors.prepTime}
                        aria-describedby="prepTime-error"
                    />
                    {errors.prepTime && (
                        <span id="prepTime-error" className="error-message">
                            {errors.prepTime}
                        </span>
                    )}
                </div>

                <div className="form-group">
                    <label htmlFor="cookTime">Cook Time (minutes)</label>
                    <input
                        id="cookTime"
                        name="cookTime"
                        type="number"
                        min="0"
                        value={formData.cookTime}
                        onChange={handleChange}
                        aria-invalid={!!errors.cookTime}
                        aria-describedby="cookTime-error"
                    />
                    {errors.cookTime && (
                        <span id="cookTime-error" className="error-message">
                            {errors.cookTime}
                        </span>
                    )}
                </div>
            </div>

            {errors.submit && (
                <div className="form-error" role="alert">
                    {errors.submit}
                </div>
            )}

            <div className="form-actions">
                <button
                    type="button"
                    onClick={onCancel}
                    disabled={isSubmitting}
                    className="button secondary"
                >
                    Cancel
                </button>
                <button
                    type="submit"
                    disabled={isSubmitting || Object.keys(errors).length > 0}
                    className="button primary"
                >
                    {isSubmitting ? 'Saving...' : 'Save Recipe'}
                </button>
            </div>
        </form>
    );
}
```

### Dynamic Forms with Arrays

```jsx
import { useState } from 'react';

export function IngredientListForm({ ingredients, onChange }) {
    const [newIngredient, setNewIngredient] = useState({
        name: '',
        quantity: '',
        unit: '',
    });

    const handleAddIngredient = () => {
        if (newIngredient.name.trim()) {
            onChange?.([...ingredients, { ...newIngredient }]);
            setNewIngredient({ name: '', quantity: '', unit: '' });
        }
    };

    const handleRemoveIngredient = (index) => {
        onChange?.(ingredients.filter((_, i) => i !== index));
    };

    const handleIngredientChange = (index, field) => (event) => {
        const updated = ingredients.map((ingredient, i) =>
            i === index
                ? { ...ingredient, [field]: event.target.value }
                : ingredient
        );
        onChange?.(updated);
    };

    return (
        <div className="ingredient-list-form">
            <div className="ingredient-inputs">
                <input
                    type="text"
                    placeholder="Ingredient name"
                    value={newIngredient.name}
                    onChange={(e) => setNewIngredient({ ...newIngredient, name: e.target.value })}
                />
                <input
                    type="text"
                    placeholder="Quantity"
                    value={newIngredient.quantity}
                    onChange={(e) => setNewIngredient({ ...newIngredient, quantity: e.target.value })}
                />
                <input
                    type="text"
                    placeholder="Unit (e.g., cups, grams)"
                    value={newIngredient.unit}
                    onChange={(e) => setNewIngredient({ ...newIngredient, unit: e.target.value })}
                />
                <button
                    type="button"
                    onClick={handleAddIngredient}
                    disabled={!newIngredient.name.trim()}
                    className="button small"
                >
                    + Add
                </button>
            </div>

            {ingredients.map((ingredient, index) => (
                <div key={index} className="ingredient-row">
                    <input
                        type="text"
                        value={ingredient.name}
                        onChange={handleIngredientChange(index, 'name')}
                        placeholder="Ingredient name"
                    />
                    <input
                        type="text"
                        value={ingredient.quantity}
                        onChange={handleIngredientChange(index, 'quantity')}
                        placeholder="Quantity"
                    />
                    <input
                        type="text"
                        value={ingredient.unit}
                        onChange={handleIngredientChange(index, 'unit')}
                        placeholder="Unit"
                    />
                    <button
                        type="button"
                        onClick={() => handleRemoveIngredient(index)}
                        className="button danger small"
                        aria-label={`Remove ${ingredient.name}`}
                    >
                        ✕
                    </button>
                </div>
            ))}
        </div>
    );
}
```

## Performance JSX Patterns

### Avoiding Inline Functions

```jsx
// ❌ BAD: Creating new function on every render
function RecipeList({ recipes }) {
    return (
        <ul>
            {recipes.map((recipe) => (
                <RecipeCard
                    key={recipe.id}
                    recipe={recipe}
                    onLike={() => handleLike(recipe.id)} {/* Creates new function each render */}
                    onDelete={() => handleDelete(recipe.id)}
                />
            ))}
        </ul>
    );
}

// ✅ GOOD: Using data attributes or useCallback
function RecipeList({ recipes, onLike, onDelete }) {
    return (
        <ul>
            {recipes.map((recipe) => (
                <RecipeCard
                    key={recipe.id}
                    recipe={recipe}
                    onLike={() => onLike(recipe.id)}
                    onDelete={() => onDelete(recipe.id)}
                />
            ))}
        </ul>
    );
}

// ✅ EVEN BETTER: Event delegation
function RecipeList({ recipes }) {
    const handleAction = (event) => {
        const button = event.target.closest('[data-recipe-action]');
        if (!button) return;

        const { action, recipeId } = button.dataset;

        switch (action) {
            case 'like':
                handleLike(parseInt(recipeId));
                break;
            case 'delete':
                handleDelete(parseInt(recipeId));
                break;
        }
    };

    return (
        <ul onClick={handleAction}>
            {recipes.map((recipe) => (
                <li key={recipe.id} data-recipe-id={recipe.id}>
                    <h3>{recipe.title}</h3>
                    <button
                        data-recipe-action="like"
                        data-recipe-id={recipe.id}
                        type="button"
                    >
                        Like
                    </button>
                    <button
                        data-recipe-action="delete"
                        data-recipe-id={recipe.id}
                        type="button"
                    >
                        Delete
                    </button>
                </li>
            ))}
        </ul>
    );
}
```

### Lazy Loading Components

```jsx
import { lazy, Suspense } from 'react';

// Lazy load heavy components
const RecipeEditor = lazy(() => import('./RecipeEditor'));
const AdminDashboard = lazy(() => import('./AdminDashboard'));
const UserProfile = lazy(() => import('./UserProfile'));

// Loading fallback component
function ComponentLoader() {
    return (
        <div className="component-loader">
            <div className="loader-spinner"></div>
            <p>Loading component...</p>
        </div>
    );
}

// Usage with Suspense
function App() {
    return (
        <Suspense fallback={<ComponentLoader />}>
            <Routes>
                <Route path="/recipes/new" element={<RecipeEditor />} />
                <Route path="/admin" element={<AdminDashboard />} />
                <Route path="/profile" element={<UserProfile />} />
            </Routes>
        </Suspense>
    );
}
```

## Accessibility in JSX

### ARIA Attributes

```jsx
function RecipeCard({ recipe, onLike }) {
    const [isLiked, setIsLiked] = useState(false);
    const [isExpanded, setIsExpanded] = useState(false);

    return (
        <article
            className="recipe-card"
            aria-labelledby={`recipe-title-${recipe.id}`}
            aria-describedby={`recipe-desc-${recipe.id}`}
        >
            <img
                src={recipe.imageUrl}
                alt={recipe.title}
                loading="lazy"
                role="img"
            />

            <h2 id={`recipe-title-${recipe.id}`}>{recipe.title}</h2>

            <p id={`recipe-desc-${recipe.id}`} className="description">
                {recipe.description}
            </p>

            <button
                className="like-button"
                onClick={() => setIsLiked(!isLiked)}
                aria-label={isLiked ? 'Remove from likes' : 'Add to likes'}
                aria-pressed={isLiked}
            >
                {isLiked ? '❤️ Liked' : '🤍 Like'}
            </button>

            <button
                className="expand-button"
                onClick={() => setIsExpanded(!isExpanded)}
                aria-expanded={isExpanded}
                aria-controls={`details-${recipe.id}`}
            >
                {isExpanded ? 'Show Less' : 'Show More'}
            </button>

            {isExpanded && (
                <div id={`details-${recipe.id}`} className="recipe-details">
                    <RecipeIngredients ingredients={recipe.ingredients} />
                    <RecipeInstructions instructions={recipe.instructions} />
                </div>
            )}
        </article>
    );
}

// Accessible form with ARIA
function SearchForm({ onSearch }) {
    const [query, setQuery] = useState('');

    return (
        <form
            role="search"
            onSubmit={(e) => {
                e.preventDefault();
                onSearch(query);
            }}
            aria-label="Search recipes"
        >
            <label htmlFor="search-input" className="sr-only">
                Search recipes
            </label>
            <div className="search-input-wrapper">
                <input
                    id="search-input"
                    type="search"
                    placeholder="Search recipes..."
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    aria-describedby="search-hint"
                    autoComplete="off"
                />
                <button
                    type="submit"
                    aria-label="Submit search"
                    disabled={!query.trim()}
                >
                    🔍
                </button>
            </div>
            <p id="search-hint" className="hint-text">
                Type at least 2 characters to search
            </p>
        </form>
    );
}
```

### Keyboard Navigation

```jsx
import { useEffect, useRef } from 'react';

function Modal({ isOpen, onClose, title, children, ariaLabel }) {
    const modalRef = useRef(null);
    const closeButtonRef = useRef(null);

    // Focus trap
    useEffect(() => {
        if (isOpen && closeButtonRef.current) {
            closeButtonRef.current.focus();
        }

        const handleEscape = (event) => {
            if (event.key === 'Escape' && isOpen) {
                onClose();
            }
        };

        const trapFocus = (event) => {
            if (!isOpen) return;

            const focusableElements = modalRef.current?.querySelectorAll(
                'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
            );

            const firstElement = focusableElements[0];
            const lastElement = focusableElements[focusableElements.length - 1];

            if (event.key === 'Tab') {
                if (event.shiftKey) {
                    // Shift+Tab: Focus last element
                    if (document.activeElement === firstElement) {
                        event.preventDefault();
                        lastElement.focus();
                    }
                } else {
                    // Tab: Focus first element
                    if (document.activeElement === lastElement) {
                        event.preventDefault();
                        firstElement.focus();
                    }
                }
            }
        };

        document.addEventListener('keydown', handleEscape);
        document.addEventListener('keydown', trapFocus);

        return () => {
            document.removeEventListener('keydown', handleEscape);
            document.removeEventListener('keydown', trapFocus);
        };
    }, [isOpen, onClose]);

    // Body scroll lock
    useEffect(() => {
        if (isOpen) {
            document.body.style.overflow = 'hidden';
        } else {
            document.body.style.overflow = '';
        }
    }, [isOpen]);

    if (!isOpen) return null;

    return (
        <div
            className="modal-overlay"
            onClick={onClose}
            role="presentation"
        >
            <div
                ref={modalRef}
                className="modal-content"
                onClick={(e) => e.stopPropagation()}
                role="dialog"
                aria-modal="true"
                aria-labelledby={`modal-title-${title}`}
                aria-label={ariaLabel}
            >
                <div className="modal-header">
                    <h2 id={`modal-title-${title}`} className="modal-title">
                        {title}
                    </h2>
                    <button
                        ref={closeButtonRef}
                        className="modal-close"
                        onClick={onClose}
                        aria-label="Close modal"
                    >
                        ✕
                    </button>
                </div>

                <div className="modal-body">
                    {children}
                </div>
            </div>
        </div>
    );
}
```

## Summary

### Key React 19+ Features
- **Server Components** (if using Next.js)
- **useActionState** hook for form submissions
- **useOptimistic** hook for optimistic UI updates
- **Automatic batching** for multiple state updates
- **Improved TypeScript support** and type inference

### Best Practices
- Use functional components with hooks
- Keep components small and focused
- Implement proper error boundaries
- Add loading and error states
- Use TypeScript for type safety
- Test components with React Testing Library
- Follow accessibility guidelines (ARIA, keyboard nav)
- Optimize performance with React.memo and memoization
