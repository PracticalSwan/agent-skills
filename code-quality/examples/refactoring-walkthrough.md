# Refactoring Walkthrough: React Component

A step-by-step refactoring of a realistic React component. We start with a messy component full of code smells and transform it into clean, maintainable code through incremental improvements.

---

## The Starting Point: `ProductPage.jsx`

This component displays a product, handles cart operations, manages reviews, and tracks analytics. It's 160+ lines with multiple code smells.

```jsx
import { useState, useEffect } from "react";

export default function ProductPage({ productId, user }) {
  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [reviews, setReviews] = useState([]);
  const [reviewText, setReviewText] = useState("");
  const [reviewRating, setReviewRating] = useState(5);
  const [cartCount, setCartCount] = useState(0);
  const [showSuccess, setShowSuccess] = useState(false);
  const [selectedSize, setSelectedSize] = useState(null);
  const [selectedColor, setSelectedColor] = useState(null);
  const [isFavorite, setIsFavorite] = useState(false);
  const [quantity, setQuantity] = useState(1);

  useEffect(() => {
    setLoading(true);
    fetch(`https://api.example.com/products/${productId}`)
      .then((res) => {
        if (!res.ok) throw new Error("Failed to fetch");
        return res.json();
      })
      .then((data) => {
        setProduct(data);
        setSelectedSize(data.sizes[0]);
        setSelectedColor(data.colors[0]);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, [productId]);

  useEffect(() => {
    fetch(`https://api.example.com/products/${productId}/reviews`)
      .then((res) => res.json())
      .then((data) => setReviews(data))
      .catch((err) => console.log(err));
  }, [productId]);

  useEffect(() => {
    if (user) {
      fetch(`https://api.example.com/users/${user.id}/favorites`)
        .then((res) => res.json())
        .then((favs) => {
          setIsFavorite(favs.some((f) => f.productId === productId));
        })
        .catch((err) => console.log(err));
    }
  }, [productId, user]);

  function handleAddToCart() {
    if (!selectedSize) {
      alert("Please select a size");
      return;
    }
    if (!selectedColor) {
      alert("Please select a color");
      return;
    }
    fetch("https://api.example.com/cart", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        productId: productId,
        size: selectedSize,
        color: selectedColor,
        quantity: quantity,
        price: product.price,
      }),
    })
      .then((res) => res.json())
      .then((data) => {
        setCartCount(data.totalItems);
        setShowSuccess(true);
        setTimeout(() => setShowSuccess(false), 3000);
        // analytics
        if (window.gtag) {
          window.gtag("event", "add_to_cart", {
            item_id: productId,
            item_name: product.name,
            price: product.price,
            quantity: quantity,
          });
        }
      })
      .catch((err) => {
        console.log(err);
        alert("Failed to add to cart");
      });
  }

  function handleSubmitReview() {
    if (reviewText.length < 10) {
      alert("Review must be at least 10 characters");
      return;
    }
    if (!user) {
      alert("Please log in to submit a review");
      return;
    }
    fetch(`https://api.example.com/products/${productId}/reviews`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        text: reviewText,
        rating: reviewRating,
        userId: user.id,
        userName: user.name,
      }),
    })
      .then((res) => res.json())
      .then((newReview) => {
        setReviews([newReview, ...reviews]);
        setReviewText("");
        setReviewRating(5);
      })
      .catch((err) => {
        console.log(err);
        alert("Failed to submit review");
      });
  }

  function handleToggleFavorite() {
    const method = isFavorite ? "DELETE" : "POST";
    fetch(`https://api.example.com/users/${user.id}/favorites/${productId}`, {
      method: method,
    })
      .then(() => setIsFavorite(!isFavorite))
      .catch((err) => console.log(err));
  }

  if (loading) return <div className="loading">Loading...</div>;
  if (error) return <div className="error">Error: {error}</div>;
  if (!product) return <div>Product not found</div>;

  // calculate average rating
  let totalRating = 0;
  for (let i = 0; i < reviews.length; i++) {
    totalRating += reviews[i].rating;
  }
  const avgRating = reviews.length > 0 ? totalRating / reviews.length : 0;

  // calculate discounted price
  let finalPrice = product.price;
  if (product.discount > 0) {
    finalPrice = product.price * (1 - product.discount / 100);
  }

  return (
    <div className="product-page">
      <div className="product-header">
        <img src={product.image} alt={product.name} className="product-image" />
        <div className="product-info">
          <h1>{product.name}</h1>
          <div className="rating">
            {[1, 2, 3, 4, 5].map((star) => (
              <span key={star} className={star <= Math.round(avgRating) ? "star filled" : "star"}>
                ★
              </span>
            ))}
            <span>({reviews.length} reviews)</span>
          </div>
          <div className="price">
            {product.discount > 0 && (
              <span className="original-price">${product.price.toFixed(2)}</span>
            )}
            <span className="final-price">${finalPrice.toFixed(2)}</span>
            {product.discount > 0 && (
              <span className="discount-badge">{product.discount}% OFF</span>
            )}
          </div>
          <p className="description">{product.description}</p>

          <div className="options">
            <div className="size-selector">
              <label>Size:</label>
              {product.sizes.map((size) => (
                <button
                  key={size}
                  className={size === selectedSize ? "option selected" : "option"}
                  onClick={() => setSelectedSize(size)}
                >
                  {size}
                </button>
              ))}
            </div>
            <div className="color-selector">
              <label>Color:</label>
              {product.colors.map((color) => (
                <button
                  key={color}
                  className={color === selectedColor ? "option selected" : "option"}
                  onClick={() => setSelectedColor(color)}
                >
                  {color}
                </button>
              ))}
            </div>
          </div>

          <div className="actions">
            <input
              type="number"
              min="1"
              max="10"
              value={quantity}
              onChange={(e) => setQuantity(Number(e.target.value))}
            />
            <button onClick={handleAddToCart} className="add-to-cart">
              Add to Cart ({cartCount})
            </button>
            <button onClick={handleToggleFavorite} className="favorite">
              {isFavorite ? "♥ Favorited" : "♡ Favorite"}
            </button>
          </div>
          {showSuccess && <div className="success-message">Added to cart!</div>}
        </div>
      </div>

      <div className="reviews-section">
        <h2>Reviews ({reviews.length})</h2>
        {user && (
          <div className="review-form">
            <select value={reviewRating} onChange={(e) => setReviewRating(Number(e.target.value))}>
              {[5, 4, 3, 2, 1].map((r) => (
                <option key={r} value={r}>{r} Stars</option>
              ))}
            </select>
            <textarea
              value={reviewText}
              onChange={(e) => setReviewText(e.target.value)}
              placeholder="Write your review (min 10 characters)..."
            />
            <button onClick={handleSubmitReview}>Submit Review</button>
          </div>
        )}
        <div className="review-list">
          {reviews.map((review) => (
            <div key={review.id} className="review-card">
              <div className="review-header">
                <strong>{review.userName}</strong>
                <span>{[1, 2, 3, 4, 5].map((s) => (
                  <span key={s} className={s <= review.rating ? "star filled" : "star"}>★</span>
                ))}</span>
              </div>
              <p>{review.text}</p>
              <span className="review-date">
                {new Date(review.createdAt).toLocaleDateString()}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
```

### Identified Code Smells

| # | Smell | Location |
|---|---|---|
| 1 | **Long Method** | Entire component is 160+ lines |
| 2 | **Large Class** | Component manages product, cart, reviews, favorites, analytics |
| 3 | **Feature Envy** | Inline API calls that belong in a service layer |
| 4 | **Magic Numbers** | `3000` (timeout), `10` (min review length), `100` (discount calc) |
| 5 | **Duplicated Code** | Star rating rendered twice (header + review cards) |
| 6 | **Poor Error Handling** | `console.log(err)` and `alert()` for errors |
| 7 | **Mixed Concerns** | Analytics tracking mixed into cart logic |
| 8 | **Primitive Obsession** | Review form state as separate primitives |

---

## Step 1: Extract API Service

Move all `fetch` calls into a dedicated module. This removes Feature Envy and separates concerns.

**Create `api/productApi.js`:**

```javascript
const API_BASE = "https://api.example.com";

export async function fetchProduct(productId) {
  const res = await fetch(`${API_BASE}/products/${productId}`);
  if (!res.ok) throw new Error(`Failed to fetch product: ${res.status}`);
  return res.json();
}

export async function fetchReviews(productId) {
  const res = await fetch(`${API_BASE}/products/${productId}/reviews`);
  if (!res.ok) throw new Error(`Failed to fetch reviews: ${res.status}`);
  return res.json();
}

export async function submitReview(productId, review) {
  const res = await fetch(`${API_BASE}/products/${productId}/reviews`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(review),
  });
  if (!res.ok) throw new Error(`Failed to submit review: ${res.status}`);
  return res.json();
}

export async function addToCart(item) {
  const res = await fetch(`${API_BASE}/cart`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(item),
  });
  if (!res.ok) throw new Error(`Failed to add to cart: ${res.status}`);
  return res.json();
}

export async function fetchFavorites(userId) {
  const res = await fetch(`${API_BASE}/users/${userId}/favorites`);
  if (!res.ok) throw new Error(`Failed to fetch favorites: ${res.status}`);
  return res.json();
}

export async function toggleFavorite(userId, productId, isFavorite) {
  const method = isFavorite ? "DELETE" : "POST";
  const res = await fetch(`${API_BASE}/users/${userId}/favorites/${productId}`, { method });
  if (!res.ok) throw new Error(`Failed to toggle favorite: ${res.status}`);
}
```

**Impact:** All 6 inline `fetch` calls removed from the component. API base URL defined once. Error handling is consistent.

---

## Step 2: Extract Custom Hook — `useProduct`

Extract the product-loading logic into a reusable hook. This addresses Long Method and separates data-fetching from rendering.

**Create `hooks/useProduct.js`:**

```javascript
import { useState, useEffect } from "react";
import { fetchProduct, fetchReviews, fetchFavorites } from "../api/productApi";

export function useProduct(productId, userId) {
  const [product, setProduct] = useState(null);
  const [reviews, setReviews] = useState([]);
  const [isFavorite, setIsFavorite] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let cancelled = false;

    async function load() {
      setLoading(true);
      setError(null);
      try {
        const [productData, reviewsData] = await Promise.all([
          fetchProduct(productId),
          fetchReviews(productId),
        ]);
        if (cancelled) return;
        setProduct(productData);
        setReviews(reviewsData);
      } catch (err) {
        if (!cancelled) setError(err.message);
      } finally {
        if (!cancelled) setLoading(false);
      }
    }

    load();
    return () => { cancelled = true; };
  }, [productId]);

  useEffect(() => {
    if (!userId) return;
    let cancelled = false;

    fetchFavorites(userId)
      .then((favs) => {
        if (!cancelled) {
          setIsFavorite(favs.some((f) => f.productId === productId));
        }
      })
      .catch(() => {}); // favorite status is non-critical

    return () => { cancelled = true; };
  }, [productId, userId]);

  function addReview(review) {
    setReviews((prev) => [review, ...prev]);
  }

  return { product, reviews, isFavorite, setIsFavorite, addReview, loading, error };
}
```

**What improved:**
- Race condition handled with `cancelled` flag
- Parallel data fetching with `Promise.all`
- Cleanup on unmount prevents state updates after unmount
- Review list update encapsulated in `addReview`

---

## Step 3: Extract Sub-Components

Break the monolithic render into focused components. This addresses Large Class and Duplicated Code.

**Create `components/StarRating.jsx`:**

```jsx
const STARS = [1, 2, 3, 4, 5];

export default function StarRating({ rating, count }) {
  const rounded = Math.round(rating);
  return (
    <div className="rating">
      {STARS.map((star) => (
        <span key={star} className={star <= rounded ? "star filled" : "star"}>
          ★
        </span>
      ))}
      {count != null && <span>({count} reviews)</span>}
    </div>
  );
}
```

> The duplicated star-rendering logic (header + review cards) is now a single component.

**Create `components/OptionSelector.jsx`:**

```jsx
export default function OptionSelector({ label, options, selected, onSelect }) {
  return (
    <div className="option-selector">
      <label>{label}:</label>
      {options.map((option) => (
        <button
          key={option}
          className={option === selected ? "option selected" : "option"}
          onClick={() => onSelect(option)}
        >
          {option}
        </button>
      ))}
    </div>
  );
}
```

> Eliminates duplication between size selector and color selector.

**Create `components/PriceDisplay.jsx`:**

```jsx
export default function PriceDisplay({ price, discountPercent }) {
  const finalPrice = discountPercent > 0 ? price * (1 - discountPercent / 100) : price;

  return (
    <div className="price">
      {discountPercent > 0 && (
        <span className="original-price">${price.toFixed(2)}</span>
      )}
      <span className="final-price">${finalPrice.toFixed(2)}</span>
      {discountPercent > 0 && (
        <span className="discount-badge">{discountPercent}% OFF</span>
      )}
    </div>
  );
}
```

> Price calculation logic is encapsulated. The magic number `100` is now contextually clear inside a `discountPercent` computation.

**Create `components/ReviewCard.jsx`:**

```jsx
import StarRating from "./StarRating";

export default function ReviewCard({ review }) {
  return (
    <div className="review-card">
      <div className="review-header">
        <strong>{review.userName}</strong>
        <StarRating rating={review.rating} />
      </div>
      <p>{review.text}</p>
      <time className="review-date">
        {new Date(review.createdAt).toLocaleDateString()}
      </time>
    </div>
  );
}
```

---

## Step 4: Extract Review Form with Proper Validation

Replace `alert()` with inline validation state and extract the form into its own component.

**Create `components/ReviewForm.jsx`:**

```jsx
import { useState } from "react";
import { submitReview } from "../api/productApi";

const MIN_REVIEW_LENGTH = 10;
const RATING_OPTIONS = [5, 4, 3, 2, 1];

export default function ReviewForm({ productId, user, onReviewAdded }) {
  const [text, setText] = useState("");
  const [rating, setRating] = useState(5);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState(null);

  const validationError =
    text.length > 0 && text.length < MIN_REVIEW_LENGTH
      ? `Review must be at least ${MIN_REVIEW_LENGTH} characters`
      : null;

  const canSubmit = text.length >= MIN_REVIEW_LENGTH && !submitting;

  async function handleSubmit(e) {
    e.preventDefault();
    setSubmitting(true);
    setError(null);

    try {
      const newReview = await submitReview(productId, {
        text,
        rating,
        userId: user.id,
        userName: user.name,
      });
      onReviewAdded(newReview);
      setText("");
      setRating(5);
    } catch (err) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <form className="review-form" onSubmit={handleSubmit}>
      <select value={rating} onChange={(e) => setRating(Number(e.target.value))}>
        {RATING_OPTIONS.map((r) => (
          <option key={r} value={r}>{r} Stars</option>
        ))}
      </select>
      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder={`Write your review (min ${MIN_REVIEW_LENGTH} characters)...`}
      />
      {validationError && <p className="validation-error">{validationError}</p>}
      {error && <p className="error-message">{error}</p>}
      <button type="submit" disabled={!canSubmit}>
        {submitting ? "Submitting..." : "Submit Review"}
      </button>
    </form>
  );
}
```

**What improved:**
- `alert()` replaced with inline validation messages
- Loading state during submission
- Error state displayed in UI instead of alert
- Magic number `10` replaced with named constant
- Uses `<form>` with `onSubmit` instead of button `onClick`

---

## Step 5: Extract Cart Logic with Analytics Separation

Separate analytics tracking from cart operations. Replace `alert()` and `console.log()`.

**Create `hooks/useCart.js`:**

```javascript
import { useState, useCallback } from "react";
import { addToCart as addToCartApi } from "../api/productApi";
import { trackAddToCart } from "../analytics";

const SUCCESS_MESSAGE_DURATION_MS = 3000;

export function useCart() {
  const [cartCount, setCartCount] = useState(0);
  const [showSuccess, setShowSuccess] = useState(false);
  const [error, setError] = useState(null);
  const [adding, setAdding] = useState(false);

  const addItem = useCallback(async (item, productMeta) => {
    setAdding(true);
    setError(null);

    try {
      const data = await addToCartApi(item);
      setCartCount(data.totalItems);
      setShowSuccess(true);
      setTimeout(() => setShowSuccess(false), SUCCESS_MESSAGE_DURATION_MS);
      trackAddToCart(productMeta);
    } catch (err) {
      setError(err.message);
    } finally {
      setAdding(false);
    }
  }, []);

  return { cartCount, showSuccess, error, adding, addItem };
}
```

**Create `analytics.js`:**

```javascript
export function trackAddToCart({ id, name, price, quantity }) {
  if (typeof window !== "undefined" && window.gtag) {
    window.gtag("event", "add_to_cart", {
      item_id: id,
      item_name: name,
      price,
      quantity,
    });
  }
}
```

**What improved:**
- Analytics is a separate module—testable and replaceable
- Magic number `3000` replaced with named constant
- `console.log` and `alert` replaced with proper error state
- Cart logic is reusable across pages

---

## Step 6: The Final Component

After all extractions, the `ProductPage` component is focused purely on composition and layout:

```jsx
import { useProduct } from "../hooks/useProduct";
import { useCart } from "../hooks/useCart";
import { toggleFavorite } from "../api/productApi";
import StarRating from "../components/StarRating";
import PriceDisplay from "../components/PriceDisplay";
import OptionSelector from "../components/OptionSelector";
import ReviewCard from "../components/ReviewCard";
import ReviewForm from "../components/ReviewForm";
import { useState } from "react";

export default function ProductPage({ productId, user }) {
  const {
    product, reviews, isFavorite, setIsFavorite, addReview, loading, error,
  } = useProduct(productId, user?.id);

  const cart = useCart();

  const [selectedSize, setSelectedSize] = useState(null);
  const [selectedColor, setSelectedColor] = useState(null);
  const [quantity, setQuantity] = useState(1);

  // set defaults once product loads
  if (product && !selectedSize) setSelectedSize(product.sizes[0]);
  if (product && !selectedColor) setSelectedColor(product.colors[0]);

  if (loading) return <div className="loading">Loading...</div>;
  if (error) return <div className="error">Error: {error}</div>;
  if (!product) return <div>Product not found</div>;

  const averageRating = reviews.length > 0
    ? reviews.reduce((sum, r) => sum + r.rating, 0) / reviews.length
    : 0;

  function handleAddToCart() {
    if (!selectedSize || !selectedColor) return;
    cart.addItem(
      { productId, size: selectedSize, color: selectedColor, quantity, price: product.price },
      { id: productId, name: product.name, price: product.price, quantity },
    );
  }

  async function handleToggleFavorite() {
    try {
      await toggleFavorite(user.id, productId, isFavorite);
      setIsFavorite(!isFavorite);
    } catch { /* favorite toggle is non-critical */ }
  }

  return (
    <div className="product-page">
      <div className="product-header">
        <img src={product.image} alt={product.name} className="product-image" />
        <div className="product-info">
          <h1>{product.name}</h1>
          <StarRating rating={averageRating} count={reviews.length} />
          <PriceDisplay price={product.price} discountPercent={product.discount} />
          <p className="description">{product.description}</p>

          <OptionSelector
            label="Size" options={product.sizes}
            selected={selectedSize} onSelect={setSelectedSize}
          />
          <OptionSelector
            label="Color" options={product.colors}
            selected={selectedColor} onSelect={setSelectedColor}
          />

          <div className="actions">
            <input
              type="number" min={1} max={10}
              value={quantity}
              onChange={(e) => setQuantity(Number(e.target.value))}
            />
            <button
              onClick={handleAddToCart}
              disabled={cart.adding || !selectedSize || !selectedColor}
              className="add-to-cart"
            >
              {cart.adding ? "Adding..." : `Add to Cart (${cart.cartCount})`}
            </button>
            {user && (
              <button onClick={handleToggleFavorite} className="favorite">
                {isFavorite ? "♥ Favorited" : "♡ Favorite"}
              </button>
            )}
          </div>
          {cart.showSuccess && <div className="success-message">Added to cart!</div>}
          {cart.error && <div className="error-message">{cart.error}</div>}
        </div>
      </div>

      <section className="reviews-section">
        <h2>Reviews ({reviews.length})</h2>
        {user && (
          <ReviewForm productId={productId} user={user} onReviewAdded={addReview} />
        )}
        <div className="review-list">
          {reviews.map((review) => (
            <ReviewCard key={review.id} review={review} />
          ))}
        </div>
      </section>
    </div>
  );
}
```

---

## Summary of Changes

| Step | Action | Smells Addressed | Lines Moved |
|---|---|---|---|
| 1 | Extract API service | Feature Envy, Duplicated fetch patterns | ~60 lines → `productApi.js` |
| 2 | Extract `useProduct` hook | Long Method, Mixed Concerns | ~45 lines → `useProduct.js` |
| 3 | Extract sub-components | Duplicated Code, Large Class | ~50 lines → 4 components |
| 4 | Extract `ReviewForm` | Poor Error Handling, Magic Numbers | ~30 lines → `ReviewForm.jsx` |
| 5 | Extract `useCart` + analytics | Mixed Concerns, Magic Numbers | ~25 lines → `useCart.js` + `analytics.js` |
| 6 | Compose final component | All of the above | 160+ → ~75 lines |

### Final File Structure

```
components/
  StarRating.jsx          — 15 lines, reusable
  OptionSelector.jsx      — 18 lines, reusable
  PriceDisplay.jsx        — 16 lines, reusable
  ReviewCard.jsx          — 16 lines, reusable
  ReviewForm.jsx          — 52 lines, self-contained
hooks/
  useProduct.js           — 48 lines, data management
  useCart.js              — 32 lines, cart operations
api/
  productApi.js           — 45 lines, API layer
analytics.js              — 10 lines, tracking
ProductPage.jsx           — 75 lines, composition only
```

### Key Principles Applied

1. **Single Responsibility** — Each file has one reason to change
2. **Separation of Concerns** — API, state, UI, and analytics are isolated
3. **DRY** — Star rating, option selectors, and fetch patterns defined once
4. **Error Handling** — No `alert()` or `console.log`; errors shown in UI with proper state
5. **Named Constants** — Magic numbers replaced with descriptive identifiers
6. **Composition over Complexity** — The main component assembles small, testable pieces
7. **Custom Hooks** — State logic extracted into reusable hooks with cleanup
