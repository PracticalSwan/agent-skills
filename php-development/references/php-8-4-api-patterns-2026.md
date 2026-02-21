# PHP 8.4 API Patterns (2026)

Up-to-date PHP patterns for building secure, maintainable REST APIs with PDO, authentication, validation, and XAMPP/MySQL integration.

## PHP Version Context

### Current Stable Baseline
- **PHP 8.4** (latest stable branch in 2026 context)
- Recommended minimum for new projects: **PHP 8.2+**
- For this project (XAMPP + MySQL + React frontend): **PHP 8.0+ required**, **8.2+ preferred**

## Core Language Features (PHP 8.x)

### Constructor Property Promotion

```php
<?php
class Recipe {
    public function __construct(
        public int $id,
        public string $title,
        public string $description,
        public string $difficulty = 'Medium'
    ) {}
}
```

### Union and Intersection Types

```php
<?php
declare(strict_types=1);

function normalizeValue(string|int|float|null $value): string {
    return (string)($value ?? '');
}

interface JsonSerializableEntity extends JsonSerializable {}

function toJson(JsonSerializable&ArrayAccess $entity): string {
    return json_encode($entity, JSON_THROW_ON_ERROR);
}
```

### Nullsafe Operator

```php
<?php
$email = $user?->profile?->contact?->email ?? 'no-email@example.com';
```

### Match Expression

```php
<?php
function mapStatusCodeToMessage(int $statusCode): string {
    return match ($statusCode) {
        200 => 'Success',
        201 => 'Created',
        400 => 'Bad Request',
        401 => 'Unauthorized',
        403 => 'Forbidden',
        404 => 'Not Found',
        500 => 'Internal Server Error',
        default => 'Unknown Status',
    };
}
```

### Readonly Properties

```php
<?php
class ApiConfig {
    public function __construct(
        public readonly string $baseUrl,
        public readonly string $apiVersion,
        public readonly int $timeout
    ) {}
}
```

## API Design Patterns

### Standard JSON Response Format

```php
<?php
class JsonResponse {
    public static function success(
        mixed $data = null,
        string $message = 'Success',
        int $statusCode = 200
    ): never {
        http_response_code($statusCode);
        header('Content-Type: application/json; charset=utf-8');

        echo json_encode([
            'success' => true,
            'message' => $message,
            'data' => $data,
            'timestamp' => date(DATE_ATOM),
        ], JSON_THROW_ON_ERROR | JSON_UNESCAPED_UNICODE);

        exit;
    }

    public static function error(
        string $message,
        int $statusCode = 400,
        array $errors = []
    ): never {
        http_response_code($statusCode);
        header('Content-Type: application/json; charset=utf-8');

        echo json_encode([
            'success' => false,
            'error' => $message,
            'errors' => $errors,
            'timestamp' => date(DATE_ATOM),
        ], JSON_THROW_ON_ERROR | JSON_UNESCAPED_UNICODE);

        exit;
    }
}
```

### RESTful Controller Structure

```php
<?php
declare(strict_types=1);

class RecipeController {
    public function __construct(
        private readonly RecipeService $recipeService,
        private readonly AuthService $authService
    ) {}

    // GET /api/recipes
    public function index(): never {
        try {
            $filters = [
                'category' => $_GET['category'] ?? null,
                'difficulty' => $_GET['difficulty'] ?? null,
                'search' => $_GET['search'] ?? null,
                'limit' => (int)($_GET['limit'] ?? 20),
                'offset' => (int)($_GET['offset'] ?? 0),
            ];

            $recipes = $this->recipeService->getPublishedRecipes($filters);

            JsonResponse::success($recipes);

        } catch (ValidationException $e) {
            JsonResponse::error($e->getMessage(), 422);
        } catch (Throwable $e) {
            error_log($e->getMessage());
            JsonResponse::error('Failed to fetch recipes', 500);
        }
    }

    // GET /api/recipes/{id}
    public function show(int $id): never {
        try {
            $recipe = $this->recipeService->getRecipeById($id);

            if ($recipe === null) {
                JsonResponse::error('Recipe not found', 404);
            }

            JsonResponse::success($recipe);

        } catch (Throwable $e) {
            error_log($e->getMessage());
            JsonResponse::error('Failed to fetch recipe', 500);
        }
    }

    // POST /api/recipes
    public function store(): never {
        try {
            $user = $this->authService->requireUser();
            $payload = $this->getJsonPayload();

            $recipeId = $this->recipeService->createRecipe(
                authorId: $user['id'],
                payload: $payload
            );

            JsonResponse::success([
                'id' => $recipeId,
            ], 'Recipe created successfully', 201);

        } catch (UnauthorizedException $e) {
            JsonResponse::error($e->getMessage(), 401);
        } catch (ValidationException $e) {
            JsonResponse::error($e->getMessage(), 422, $e->getErrors());
        } catch (Throwable $e) {
            error_log($e->getMessage());
            JsonResponse::error('Failed to create recipe', 500);
        }
    }

    // PUT /api/recipes/{id}
    public function update(int $id): never {
        try {
            $user = $this->authService->requireUser();
            $payload = $this->getJsonPayload();

            $updated = $this->recipeService->updateRecipe(
                recipeId: $id,
                userId: $user['id'],
                payload: $payload
            );

            if (!$updated) {
                JsonResponse::error('Recipe not found or no changes made', 404);
            }

            JsonResponse::success(null, 'Recipe updated successfully');

        } catch (ForbiddenException $e) {
            JsonResponse::error($e->getMessage(), 403);
        } catch (ValidationException $e) {
            JsonResponse::error($e->getMessage(), 422, $e->getErrors());
        } catch (Throwable $e) {
            error_log($e->getMessage());
            JsonResponse::error('Failed to update recipe', 500);
        }
    }

    // DELETE /api/recipes/{id}
    public function destroy(int $id): never {
        try {
            $user = $this->authService->requireUser();

            $deleted = $this->recipeService->deleteRecipe(
                recipeId: $id,
                userId: $user['id']
            );

            if (!$deleted) {
                JsonResponse::error('Recipe not found', 404);
            }

            JsonResponse::success(null, 'Recipe deleted successfully');

        } catch (ForbiddenException $e) {
            JsonResponse::error($e->getMessage(), 403);
        } catch (Throwable $e) {
            error_log($e->getMessage());
            JsonResponse::error('Failed to delete recipe', 500);
        }
    }

    private function getJsonPayload(): array {
        $rawInput = file_get_contents('php://input');

        if ($rawInput === false || $rawInput === '') {
            throw new ValidationException('Request body is required');
        }

        try {
            return json_decode($rawInput, true, 512, JSON_THROW_ON_ERROR);
        } catch (JsonException $e) {
            throw new ValidationException('Invalid JSON payload');
        }
    }
}
```

## PDO Patterns and Security

### Connection Factory

```php
<?php
class PdoFactory {
    public static function create(array $config): PDO {
        $dsn = sprintf(
            'mysql:host=%s;port=%d;dbname=%s;charset=utf8mb4',
            $config['host'],
            $config['port'] ?? 3306,
            $config['database']
        );

        return new PDO($dsn, $config['username'], $config['password'], [
            PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
            PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
            PDO::ATTR_EMULATE_PREPARES => false,
            PDO::ATTR_STRINGIFY_FETCHES => false,
        ]);
    }
}
```

### Safe Query Pattern

```php
<?php
class RecipeRepository {
    public function __construct(private readonly PDO $db) {}

    public function findPublished(array $filters, int $limit = 20, int $offset = 0): array {
        $sql = "
            SELECT
                r.id,
                r.title,
                r.description,
                r.category,
                r.difficulty,
                r.prep_time,
                r.cook_time,
                r.servings,
                r.created_at,
                u.username AS author_name,
                COUNT(DISTINCT rv.id) AS view_count,
                COUNT(DISTINCT lr.id) AS like_count,
                AVG(rev.rating) AS avg_rating
            FROM recipe r
            JOIN user u ON u.id = r.author_id
            LEFT JOIN recipe_view rv ON rv.recipe_id = r.id
            LEFT JOIN like_record lr ON lr.recipe_id = r.id
            LEFT JOIN review rev ON rev.recipe_id = r.id
            WHERE r.status = 'published'
        ";

        $params = [];

        if (!empty($filters['category'])) {
            $sql .= " AND r.category = :category";
            $params[':category'] = $filters['category'];
        }

        if (!empty($filters['difficulty'])) {
            $sql .= " AND r.difficulty = :difficulty";
            $params[':difficulty'] = $filters['difficulty'];
        }

        if (!empty($filters['search'])) {
            $sql .= " AND (r.title LIKE :search OR r.description LIKE :search)";
            $params[':search'] = '%' . $filters['search'] . '%';
        }

        $sql .= "
            GROUP BY r.id
            ORDER BY r.created_at DESC
            LIMIT :limit OFFSET :offset
        ";

        $stmt = $this->db->prepare($sql);

        foreach ($params as $key => $value) {
            $stmt->bindValue($key, $value, PDO::PARAM_STR);
        }

        $stmt->bindValue(':limit', $limit, PDO::PARAM_INT);
        $stmt->bindValue(':offset', $offset, PDO::PARAM_INT);

        $stmt->execute();

        return $stmt->fetchAll();
    }
}
```

### Transaction Pattern

```php
<?php
class RecipeService {
    public function __construct(private readonly PDO $db) {}

    public function createRecipeWithDetails(array $payload, int $authorId): int {
        try {
            $this->db->beginTransaction();

            // 1. Insert recipe
            $recipeStmt = $this->db->prepare(
                "
                INSERT INTO recipe (
                    title, description, category, difficulty,
                    prep_time, cook_time, servings,
                    author_id, status, created_at, updated_at
                ) VALUES (
                    :title, :description, :category, :difficulty,
                    :prep_time, :cook_time, :servings,
                    :author_id, 'pending', NOW(), NOW()
                )
                "
            );

            $recipeStmt->execute([
                ':title' => $payload['title'],
                ':description' => $payload['description'] ?? '',
                ':category' => $payload['category'] ?? 'Uncategorized',
                ':difficulty' => $payload['difficulty'] ?? 'Medium',
                ':prep_time' => (int)($payload['prep_time'] ?? 0),
                ':cook_time' => (int)($payload['cook_time'] ?? 0),
                ':servings' => (int)($payload['servings'] ?? 1),
                ':author_id' => $authorId,
            ]);

            $recipeId = (int)$this->db->lastInsertId();

            // 2. Insert ingredients
            if (!empty($payload['ingredients']) && is_array($payload['ingredients'])) {
                $ingredientStmt = $this->db->prepare(
                    "
                    INSERT INTO ingredient (
                        recipe_id, name, quantity, unit, sort_order, created_at, updated_at
                    ) VALUES (
                        :recipe_id, :name, :quantity, :unit, :sort_order, NOW(), NOW()
                    )
                    "
                );

                foreach ($payload['ingredients'] as $index => $ingredient) {
                    $ingredientStmt->execute([
                        ':recipe_id' => $recipeId,
                        ':name' => $ingredient['name'],
                        ':quantity' => $ingredient['quantity'] ?? '',
                        ':unit' => $ingredient['unit'] ?? '',
                        ':sort_order' => $index,
                    ]);
                }
            }

            // 3. Insert instructions
            if (!empty($payload['instructions']) && is_array($payload['instructions'])) {
                $instructionStmt = $this->db->prepare(
                    "
                    INSERT INTO instruction (
                        recipe_id, step_number, instruction_text, created_at, updated_at
                    ) VALUES (
                        :recipe_id, :step_number, :instruction_text, NOW(), NOW()
                    )
                    "
                );

                foreach ($payload['instructions'] as $index => $instruction) {
                    $instructionStmt->execute([
                        ':recipe_id' => $recipeId,
                        ':step_number' => $index + 1,
                        ':instruction_text' => $instruction['instruction_text'] ?? '',
                    ]);
                }
            }

            $this->db->commit();

            return $recipeId;

        } catch (Throwable $e) {
            $this->db->rollBack();
            throw $e;
        }
    }
}
```

## Authentication Patterns

### Password Hashing

```php
<?php
class PasswordService {
    public function hash(string $plainPassword): string {
        return password_hash($plainPassword, PASSWORD_DEFAULT);
    }

    public function verify(string $plainPassword, string $hash): bool {
        return password_verify($plainPassword, $hash);
    }

    public function needsRehash(string $hash): bool {
        return password_needs_rehash($hash, PASSWORD_DEFAULT);
    }
}
```

### Token-Based Auth (JWT-style pattern)

```php
<?php
class AuthService {
    public function __construct(
        private readonly UserRepository $userRepository,
        private readonly PasswordService $passwordService
    ) {}

    public function login(string $email, string $password): array {
        $user = $this->userRepository->findByEmail($email);

        if ($user === null) {
            throw new UnauthorizedException('Invalid credentials');
        }

        if (!$this->passwordService->verify($password, $user['password_hash'])) {
            throw new UnauthorizedException('Invalid credentials');
        }

        if ($user['status'] !== 'active') {
            throw new UnauthorizedException('Account is not active');
        }

        // Replace with actual JWT implementation if used
        $token = base64_encode(json_encode([
            'sub' => $user['id'],
            'email' => $user['email'],
            'role' => $user['role'],
            'exp' => time() + (60 * 60 * 24),
        ]));

        return [
            'token' => $token,
            'user' => [
                'id' => $user['id'],
                'email' => $user['email'],
                'username' => $user['username'],
                'role' => $user['role'],
            ],
        ];
    }

    public function requireUser(): array {
        $header = $_SERVER['HTTP_AUTHORIZATION'] ?? '';

        if (!preg_match('/Bearer\s+(.+)$/i', $header, $matches)) {
            throw new UnauthorizedException('Missing bearer token');
        }

        $token = $matches[1];
        $payload = json_decode(base64_decode($token), true);

        if (!$payload || ($payload['exp'] ?? 0) < time()) {
            throw new UnauthorizedException('Invalid or expired token');
        }

        return [
            'id' => $payload['sub'],
            'email' => $payload['email'],
            'role' => $payload['role'],
        ];
    }

    public function requireAdmin(): array {
        $user = $this->requireUser();

        if ($user['role'] !== 'admin') {
            throw new ForbiddenException('Admin access required');
        }

        return $user;
    }
}
```

## Validation and Sanitization

### Request Validation

```php
<?php
class Validator {
    public static function validateRecipePayload(array $payload): array {
        $errors = [];

        if (empty(trim($payload['title'] ?? ''))) {
            $errors['title'][] = 'Title is required';
        } elseif (mb_strlen($payload['title']) > 200) {
            $errors['title'][] = 'Title must be at most 200 characters';
        }

        if (!empty($payload['difficulty'])) {
            $allowed = ['Easy', 'Medium', 'Hard'];
            if (!in_array($payload['difficulty'], $allowed, true)) {
                $errors['difficulty'][] = 'Invalid difficulty value';
            }
        }

        if (isset($payload['servings']) && ((int)$payload['servings'] < 1 || (int)$payload['servings'] > 100)) {
            $errors['servings'][] = 'Servings must be between 1 and 100';
        }

        return $errors;
    }

    public static function sanitizeString(string $value): string {
        return trim(filter_var($value, FILTER_SANITIZE_FULL_SPECIAL_CHARS));
    }

    public static function sanitizeEmail(string $value): string {
        return trim(filter_var($value, FILTER_SANITIZE_EMAIL));
    }
}
```

## CORS Middleware Pattern

```php
<?php
class CorsMiddleware {
    public static function handle(): void {
        $allowedOrigins = [
            'http://localhost:5173',
            'http://127.0.0.1:5173',
        ];

        $origin = $_SERVER['HTTP_ORIGIN'] ?? '';

        if (in_array($origin, $allowedOrigins, true)) {
            header("Access-Control-Allow-Origin: {$origin}");
        }

        header('Access-Control-Allow-Methods: GET, POST, PUT, PATCH, DELETE, OPTIONS');
        header('Access-Control-Allow-Headers: Content-Type, Authorization, X-Requested-With');
        header('Access-Control-Allow-Credentials: true');
        header('Vary: Origin');

        if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
            http_response_code(204);
            exit;
        }
    }
}
```

## Error Handling Strategy

### Global Exception Handler

```php
<?php
set_exception_handler(function (Throwable $e): void {
    error_log(sprintf(
        '[%s] %s in %s:%d',
        get_class($e),
        $e->getMessage(),
        $e->getFile(),
        $e->getLine()
    ));

    $statusCode = match (true) {
        $e instanceof ValidationException => 422,
        $e instanceof UnauthorizedException => 401,
        $e instanceof ForbiddenException => 403,
        $e instanceof NotFoundException => 404,
        default => 500,
    };

    $message = $statusCode >= 500
        ? 'Internal server error'
        : $e->getMessage();

    JsonResponse::error($message, $statusCode);
});
```

## XAMPP-Specific Notes

### Required PHP Extensions
- `pdo`
- `pdo_mysql`
- `openssl`
- `mbstring`
- `json`

### Recommended php.ini Settings (Development)
- `display_errors = On`
- `error_reporting = E_ALL`
- `log_errors = On`
- `date.timezone = Asia/Bangkok` (or your timezone)

### Apache Requirements
- `mod_rewrite` enabled
- `.htaccess` support enabled (`AllowOverride All`)

## References

### Official
- PHP Documentation: https://www.php.net/docs.php
- PHP Migration Guides: https://www.php.net/manual/en/appendices.php
- PDO Manual: https://www.php.net/manual/en/book.pdo.php

### Security
- OWASP PHP Security Cheat Sheet: https://cheatsheetseries.owasp.org/
- PHP Security Guide: https://www.php.net/manual/en/security.php

### Standards
- PSR Standards: https://www.php-fig.org/psr/
- PSR-12 Coding Style: https://www.php-fig.org/psr/psr-12/
