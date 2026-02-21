# JavaScript API Integration Patterns

Modern patterns for API integration in JavaScript using Fetch API and Axios, with error handling, retry logic, and authentication.

## Fetch API Patterns

### Basic GET Request

```javascript
/**
 * Fetch all published recipes from the API
 * @param {Object} filters - Query parameters for filtering
 * @param {string} filters.category - Filter by recipe category
 * @param {string} filters.difficulty - Filter by difficulty level
 * @param {number} filters.limit - Maximum number of results
 * @param {number} filters.offset - Offset for pagination
 * @returns {Promise<Array>} Array of recipe objects
 */
async function getRecipes(filters = {}) {
    // Build query parameters
    const queryParams = new URLSearchParams();

    if (filters.category) queryParams.append('category', filters.category);
    if (filters.difficulty) queryParams.append('difficulty', filters.difficulty);
    if (filters.limit) queryParams.append('limit', filters.limit);
    if (filters.offset) queryParams.append('offset', filters.offset);
    if (filters.search) queryParams.append('search', filters.search);

    const queryString = queryParams.toString();
    const url = `/api/recipes${queryString ? `?${queryString}` : ''}`;

    try {
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            },
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.message || `HTTP ${response.status}: ${response.statusText}`);
        }

        const data = await response.json();

        if (!data.success) {
            throw new Error(data.error || 'Request failed');
        }

        return data.data;

    } catch (error) {
        console.error('Failed to fetch recipes:', error);
        throw error;
    }
}
```

### POST Request

```javascript
/**
 * Create a new recipe
 * @param {Object} recipeData - Recipe data to create
 * @param {string} recipeData.title - Recipe title (required)
 * @param {string} recipeData.description - Recipe description
 * @param {string} recipeData.category - Recipe category
 * @param {string} recipeData.difficulty - Recipe difficulty
 * @param {Array} recipeData.ingredients - Array of ingredients
 * @param {Array} recipeData.instructions - Array of instructions
 * @param {string} token - Authentication token
 * @returns {Promise<Object>} Created recipe object
 */
async function createRecipe(recipeData, token) {
    // Validate required fields
    if (!recipeData.title || recipeData.title.trim().length < 3) {
        throw new Error('Title is required and must be at least 3 characters');
    }

    try {
        const response = await fetch('/api/recipes', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Authorization': `Bearer ${token}`,
            },
            body: JSON.stringify({
                title: recipeData.title.trim(),
                description: recipeData.description?.trim() || '',
                category: recipeData.category || 'Uncategorized',
                difficulty: recipeData.difficulty || 'Medium',
                prep_time: parseInt(recipeData.prepTime) || 0,
                cook_time: parseInt(recipeData.cookTime) || 0,
                servings: parseInt(recipeData.servings) || 1,
                ingredients: recipeData.ingredients || [],
                instructions: recipeData.instructions || [],
            }),
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || `Failed to create recipe: ${response.status}`);
        }

        return data.data;

    } catch (error) {
        console.error('Error creating recipe:', error);
        throw error;
    }
}
```

### PUT/PATCH Request

```javascript
/**
 * Update an existing recipe
 * @param {number} recipeId - ID of the recipe to update
 * @param {Object} updates - Fields to update
 * @param {string} token - Authentication token
 * @returns {Promise<Object>} Updated recipe object
 */
async function updateRecipe(recipeId, updates, token) {
    try {
        const response = await fetch(`/api/recipes/${recipeId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Authorization': `Bearer ${token}`,
            },
            body: JSON.stringify(updates),
        });

        if (response.status === 404) {
            throw new Error('Recipe not found');
        }

        if (response.status === 403) {
            throw new Error('You do not have permission to update this recipe');
        }

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Failed to update recipe');
        }

        return data.data;

    } catch (error) {
        console.error('Error updating recipe:', error);
        throw error;
    }
}
```

### DELETE Request

```javascript
/**
 * Delete a recipe
 * @param {number} recipeId - ID of the recipe to delete
 * @param {string} token - Authentication token
 * @returns {Promise<boolean>} True if successful
 */
async function deleteRecipe(recipeId, token) {
    try {
        const response = await fetch(`/api/recipes/${recipeId}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`,
            },
        });

        if (response.status === 404) {
            throw new Error('Recipe not found');
        }

        if (response.status === 403) {
            throw new Error('You do not have permission to delete this recipe');
        }

        if (!response.ok) {
            const data = await response.json().catch(() => ({}));
            throw new Error(data.error || 'Failed to delete recipe');
        }

        return true;

    } catch (error) {
        console.error('Error deleting recipe:', error);
        throw error;
    }
}
```

## Axios Integration

### Creating an Axios Instance

```javascript
import axios from 'axios';

// Create base axios instance with configuration
const apiClient = axios.create({
    baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8080/api',
    timeout: 10000, // 10 second timeout
    headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    },
});

// Request interceptor - Add authentication
apiClient.interceptors.request.use(
    (config) => {
        // Get token from localStorage
        const token = localStorage.getItem('auth_token');

        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }

        // Add request timestamp
        config.metadata = { startTime: new Date() };

        return config;
    },
    (error) => {
        // Handle request error
        console.error('Request interceptor error:', error);
        return Promise.reject(error);
    }
);

// Response interceptor - Handle errors and logging
apiClient.interceptors.response.use(
    (response) => {
        const { config } = response;

        // Calculate request duration
        const duration = new Date() - config.metadata.startTime;
        console.log(`API ${config.method?.toUpperCase()} ${config.url} - ${response.status} (${duration}ms)`);

        return response;
    },
    (error) => {
        // Handle network errors
        if (!error.response) {
            console.error('Network error:', error.message);
            return Promise.reject(new Error('Network error. Please check your connection.'));
        }

        const { response } = error;

        // Handle 401 Unauthorized - Redirect to login
        if (response?.status === 401) {
            console.log('Unauthorized - Logging out...');
            localStorage.removeItem('auth_token');
            localStorage.removeItem('user_data');
            // Only redirect if not already on login page
            if (window.location.pathname !== '/login') {
                window.location.href = '/login';
            }
        }

        // Handle 403 Forbidden
        if (response?.status === 403) {
            console.error('Access forbidden:', response.data);
            return Promise.reject(new Error('You do not have permission to access this resource.'));
        }

        // Handle 404 Not Found
        if (response?.status === 404) {
            return Promise.reject(new Error('Resource not found.'));
        }

        // Handle 500 Server Error
        if (response?.status >= 500) {
            return Promise.reject(new Error('Server error. Please try again later.'));
        }

        // Return other errors with message from server
        const errorMessage = response?.data?.error || response?.data?.message || error.message;
        return Promise.reject(new Error(errorMessage));
    }
);

export default apiClient;
```

### API Service Methods

```javascript
/**
 * Recipe API Service
 * Provides methods for all recipe-related API calls
 */
export const recipeApi = {
    /**
     * Get all published recipes with optional filters
     * @param {Object} filters - Query parameters
     * @returns {Promise<Object>} Response with data and pagination info
     */
    getAll(filters = {}) {
        const params = {};

        if (filters.category) params.category = filters.category;
        if (filters.difficulty) params.difficulty = filters.difficulty;
        if (filters.search) params.search = filters.search;
        if (filters.limit) params.limit = filters.limit;
        if (filters.offset) params.offset = filters.offset;
        if (filters.sort) params.sort = filters.sort;

        return apiClient.get('/recipes', { params });
    },

    /**
     * Get a specific recipe by ID
     * @param {number} recipeId - Recipe ID
     * @returns {Promise<Object>} Recipe object with full details
     */
    getById(recipeId) {
        return apiClient.get(`/recipes/${recipeId}`);
    },

    /**
     * Create a new recipe
     * @param {Object} recipeData - Recipe data
     * @returns {Promise<Object>} Created recipe
     */
    create(recipeData) {
        return apiClient.post('/recipes', recipeData);
    },

    /**
     * Update a recipe
     * @param {number} recipeId - Recipe ID
     * @param {Object} updates - Fields to update
     * @returns {Promise<Object>} Updated recipe
     */
    update(recipeId, updates) {
        return apiClient.put(`/recipes/${recipeId}`, updates);
    },

    /**
     * Delete a recipe
     * @param {number} recipeId - Recipe ID
     * @returns {Promise<Object>} Deletion confirmation
     */
    delete(recipeId) {
        return apiClient.delete(`/recipes/${recipeId}`);
    },

    /**
     * Like/unlike a recipe
     * @param {number} recipeId - Recipe ID
     * @returns {Promise<Object>} Updated like status
     */
    toggleLike(recipeId) {
        return apiClient.post(`/recipes/${recipeId}/like`);
    },

    /**
     * Favorite/unfavorite a recipe
     * @param {number} recipeId - Recipe ID
     * @returns {Promise<Object>} Updated favorite status
     */
    toggleFavorite(recipeId) {
        return apiClient.post(`/recipes/${recipeId}/favorite`);
    },

    /**
     * Record a view for a recipe
     * @param {number} recipeId - Recipe ID
     * @returns {Promise<Object>} View record confirmation
     */
    recordView(recipeId) {
        return apiClient.post(`/recipes/${recipeId}/view`);
    },
};

/**
 * Authentication API Service
 */
export const authApi = {
    /**
     * Register a new user
     * @param {Object} userData - User registration data
     * @returns {Promise<Object>} User data and token
     */
    register(userData) {
        return apiClient.post('/auth/register', userData);
    },

    /**
     * Login with email and password
     * @param {Object} credentials - Login credentials
     * @returns {Promise<Object>} User data and token
     */
    login(credentials) {
        return apiClient.post('/auth/login', credentials);
    },

    /**
     * Logout current user
     * @returns {Promise<Object>} Logout confirmation
     */
    logout() {
        return apiClient.post('/auth/logout');
    },

    /**
     * Get current authenticated user
     * @returns {Promise<Object>} Current user data
     */
    getCurrentUser() {
        return apiClient.get('/auth/me');
    },
};

/**
 * User API Service
 */
export const userApi = {
    /**
     * Get all users (admin only)
     * @param {Object} filters - Query parameters
     * @returns {Promise<Object>} Users list
     */
    getAll(filters = {}) {
        return apiClient.get('/users', { params: filters });
    },

    /**
     * Get user by ID
     * @param {number} userId - User ID
     * @returns {Promise<Object>} User data
     */
    getById(userId) {
        return apiClient.get(`/users/${userId}`);
    },

    /**
     * Update user profile
     * @param {number} userId - User ID
     * @param {Object} updates - Fields to update
     * @returns {Promise<Object>} Updated user data
     */
    update(userId, updates) {
        return apiClient.put(`/users/${userId}`, updates);
    },

    /**
     * Delete user (admin only)
     * @param {number} userId - User ID
     * @returns {Promise<Object>} Deletion confirmation
     */
    delete(userId) {
        return apiClient.delete(`/users/${userId}`);
    },

    /**
     * Update user status (admin only)
     * @param {number} userId - User ID
     * @param {string} status - New status (active, inactive, suspended)
     * @returns {Promise<Object>} Updated user data
     */
    updateStatus(userId, status) {
        return apiClient.put(`/users/${userId}/status`, { status });
    },
};

/**
 * Review API Service
 */
export const reviewApi = {
    /**
     * Get reviews for a recipe
     * @param {number} recipeId - Recipe ID
     * @returns {Promise<Object>} Reviews array
     */
    getByRecipe(recipeId) {
        return apiClient.get(`/recipes/${recipeId}/reviews`);
    },

    /**
     * Create a review for a recipe
     * @param {number} recipeId - Recipe ID
     * @param {Object} reviewData - Review data
     * @returns {Promise<Object>} Created review
     */
    create(recipeId, reviewData) {
        return apiClient.post(`/recipes/${recipeId}/reviews`, reviewData);
    },

    /**
     * Update a review
     * @param {number} reviewId - Review ID
     * @param {Object} updates - Fields to update
     * @returns {Promise<Object>} Updated review
     */
    update(reviewId, updates) {
        return apiClient.put(`/reviews/${reviewId}`, updates);
    },

    /**
     * Delete a review
     * @param {number} reviewId - Review ID
     * @returns {Promise<Object>} Deletion confirmation
     */
    delete(reviewId) {
        return apiClient.delete(`/reviews/${reviewId}`);
    },
};
```

## Error Handling Patterns

### Centralized Error Handler

```javascript
/**
 * API Error Handler - Centralized error handling for all API calls
 * @param {Error} error - The error object
 * @param {Object} options - Additional options
 * @returns {Object} Error response object
 */
export function handleApiError(error, options = {}) {
    const {
        showToast = true,
        logError = true,
        defaultMessage = 'An error occurred. Please try again.',
    } = options;

    // Log error to console
    if (logError) {
        console.error('API Error:', error);
    }

    // Determine error message
    let errorMessage = defaultMessage;
    let errorType = 'error';

    if (error.isAxiosError) {
        // Axios-specific errors
        if (!error.response) {
            errorMessage = 'Network error. Please check your connection.';
            errorType = 'network';
        } else {
            const { status, data } = error.response;

            switch (status) {
                case 400:
                    errorMessage = data.error || 'Invalid request. Please check your input.';
                    break;
                case 401:
                    errorMessage = 'Session expired. Please login again.';
                    errorType = 'auth';
                    break;
                case 403:
                    errorMessage = 'Access denied.';
                    break;
                case 404:
                    errorMessage = 'Resource not found.';
                    break;
                case 422:
                    errorMessage = data.error || 'Validation error.';
                    break;
                case 429:
                    errorMessage = 'Too many requests. Please wait.';
                    errorType = 'rate-limit';
                    break;
                case 500:
                case 502:
                case 503:
                    errorMessage = 'Server error. Please try again later.';
                    errorType = 'server';
                    break;
                default:
                    errorMessage = data.error || defaultMessage;
            }
        }
    } else if (error.message) {
        errorMessage = error.message;
    }

    // Show toast notification
    if (showToast) {
        // Assuming a toast notification library
        showToastNotification(errorMessage, errorType);
    }

    return {
        message: errorMessage,
        type: errorType,
        originalError: error,
    };
}
```

### Wrapper for API Calls with Error Handling

```javascript
/**
 * Safe API wrapper with automatic error handling
 * @param {Function} apiCall - The API function to call
 * @param {Object} options - Options for error handling
 * @returns {Promise<Object>} API response or error object
 */
export async function safeApiCall(apiCall, options = {}) {
    const {
        showLoading = true,
        errorMessage = 'Request failed',
        onSuccess = null,
        onError = null,
    } = options;

    // Show loading state (assuming a global loading state)
    let loadingId;
    if (showLoading) {
        loadingId = showGlobalLoading();
    }

    try {
        const response = await apiCall();

        if (onSuccess) {
            onSuccess(response.data);
        }

        return {
            success: true,
            data: response.data,
        };

    } catch (error) {
        const handledError = handleApiError(error, {
            showToast: true,
            defaultMessage: errorMessage,
        });

        if (onError) {
            onError(handledError);
        }

        return {
            success: false,
            error: handledError,
        };

    } finally {
        if (showLoading && loadingId) {
            hideGlobalLoading(loadingId);
        }
    }
}
```

### Using the Safe API Wrapper

```javascript
// Example: Loading recipes with error handling
async function loadRecipes(filters) {
    const result = await safeApiCall(
        () => recipeApi.getAll(filters),
        {
            errorMessage: 'Failed to load recipes',
            onSuccess: (data) => {
                console.log('Recipes loaded:', data.length);
            },
        }
    );

    if (result.success) {
        setRecipes(result.data);
    } else {
        // Error already handled by safeApiCall
        console.error('Error:', result.error);
    }
}

// Example: Creating a recipe with validation
async function handleCreateRecipe(recipeData) {
    const result = await safeApiCall(
        () => recipeApi.create(recipeData),
        {
            errorMessage: 'Failed to create recipe',
            onSuccess: (data) => {
                console.log('Recipe created:', data);
                navigate(`/recipes/${data.id}`);
            },
            onError: (error) => {
                console.error('Form submission error:', error);
                if (error.type === 'validation') {
                    setFormErrors(error.originalError.response.data.errors);
                }
            },
        }
    );

    return result.success;
}
```

## Retry Logic

### Exponential Backoff Retry

```javascript
/**
 * Retry a failed request with exponential backoff
 * @param {Function} requestFn - Function to call
 * @param {Object} options - Retry options
 * @returns {Promise<Object>} Response data
 */
export async function retryWithBackoff(requestFn, options = {}) {
    const {
        maxRetries = 3,
        initialDelay = 1000,
        backoffMultiplier = 2,
        retryIf = (error) => {
            // Retry on network errors and 5xx status codes
            if (!error.response) return true;
            if (error.response.status >= 500) return true;
            return false;
        },
    } = options;

    let lastError;

    for (let attempt = 0; attempt <= maxRetries; attempt++) {
        try {
            const response = await requestFn();
            return response.data; // Return data on success

        } catch (error) {
            lastError = error;

            // Don't retry if error doesn't meet retry condition
            if (!retryIf?.(error)) {
                throw error;
            }

            // Don't retry on last attempt
            if (attempt >= maxRetries) {
                throw error;
            }

            // Calculate delay with exponential backoff
            const delay = initialDelay * Math.pow(backoffMultiplier, attempt);
            console.log(`Attempt ${attempt + 1} failed, retrying in ${delay}ms...`);

            // Wait before retrying
            await new Promise(resolve => setTimeout(resolve, delay));
        }
    }

    throw lastError;
}
```

### Using Retry with API Calls

```javascript
// Example: Retry recipe fetching on failure
async function fetchRecipesWithRetry(filters) {
    try {
        const data = await retryWithBackoff(
            () => recipeApi.getAll(filters),
            {
                maxRetries: 3,
                initialDelay: 1000, // Start with 1 second
                backoffMultiplier: 2, // 1s, 2s, 4s
            }
        );

        return data;

    } catch (error) {
        handleApiError(error, {
            errorMessage: 'Failed to load recipes after multiple attempts',
        });
        throw error;
    }
}
```

## Request Cancellation

### Using AbortController

```javascript
/**
 * Fetch function with cancellation support
 * @param {Function} apiCall - API function to call
 * @returns {Object} Object with promise and cancel function
 */
export function cancellableRequest(apiCall) {
    const abortController = new AbortController();

    const promise = apiCall({ signal: abortController.signal });

    return {
        promise,
        cancel: () => abortController.abort(),
    };
}

// Example: Cancelable search
function useRecipeSearch() {
    const [results, setResults] = useState([]);
    const [searching, setSearching] = useState(false);
    const abortControllerRef = useRef(null);

    const searchRecipes = useCallback(async (query) => {
        // Cancel previous request
        if (abortControllerRef.current) {
            abortControllerRef.current.abort();
        }

        // Create new abort controller for this request
        abortControllerRef.current = new AbortController();

        setSearching(true);

        try {
            const data = await recipeApi.getAll({ search: query }, {
                signal: abortControllerRef.current.signal,
            });

            setResults(data);

        } catch (error) {
            if (error.name !== 'AbortError') {
                console.error('Search error:', error);
                handleApiError(error);
            }
        } finally {
            setSearching(false);
        }
    }, []);

    // Cleanup on unmount
    useEffect(() => {
        return () => {
            if (abortControllerRef.current) {
                abortControllerRef.current.abort();
            }
        };
    }, []);

    return { results, searching, searchRecipes };
}
```

## Summary of Patterns

### Fetch API
- ✅ Simple with just a function call
- ✅ No additional dependencies
- ✅ Built into all modern browsers
- ❌ No automatic request/response interception
- ❌ No automatic JSON parse for errors

### Axios
- ✅ Powerful with interceptors
- ✅ Automatic JSON parsing
- ✅ Request cancellation via cancel tokens
- ✅ Better error handling
- ✅ Automatic XSRF protection
- ❌ Additional bundle size (~13KB)

### When to Use Each
- Use **Fetch** for simple projects or when minimizing bundle size
- Use **Axios** for complex projects with authentication, error handling, and retry logic needs
