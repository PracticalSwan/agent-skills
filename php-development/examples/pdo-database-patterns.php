<?php
/**
 * PDO Database Integration Patterns for PHP
 *
 * This file demonstrates secure database operations using PHP PDO,
 * following the Recipe Sharing System architecture.
 */

/**
 * Database Connection Class - Singleton Pattern
 * Ensures only one database connection exists throughout application lifetime
 */
class Database {
    private static ?PDO $instance = null;

    /**
     * Get PDO database instance
     * Creates new connection if doesn't exist
     *
     * @return PDO Database connection object
     * @throws RuntimeException If connection fails
     */
    public static function getInstance(): PDO {
        if (self::$instance === null) {
            try {
                $dsn = sprintf(
                    "mysql:host=%s;dbname=%s;charset=utf8mb4",
                    $_ENV['DB_HOST'] ?? 'localhost',
                    $_ENV['DB_NAME'] ?? 'recipe_sharing_system'
                );

                self::$instance = new PDO(
                    $dsn,
                    $_ENV['DB_USER'] ?? 'root',
                    $_ENV['DB_PASSWORD'] ?? '',
                    [
                        PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
                        PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
                        PDO::ATTR_EMULATE_PREPARES => false,
                        PDO::MYSQL_ATTR_INIT_COMMAND => "SET time_zone = '+00:00'",
                    ]
                );

            } catch (PDOException $e) {
                error_log("Database connection error: " . $e->getMessage());
                throw new RuntimeException("Failed to connect to database");
            }
        }

        return self::$instance;
    }

    /**
     * Close database connection
     */
    public static function closeConnection(): void {
        self::$instance = null;
    }
}

/**
 * Base Repository Pattern
 * Provides common database operations for all entities
 */
abstract class BaseRepository {
    protected PDO $db;
    protected string $table;

    /**
     * Constructor
     */
    public function __construct() {
        $this->db = Database::getInstance();
    }

    /**
     * Find record by ID
     *
     * @param int $id Record ID
     * @return array|null Record data or null if not found
     */
    public function findById(int $id): ?array {
        $stmt = $this->db->prepare(
            "SELECT * FROM {$this->table} WHERE id = :id LIMIT 1"
        );

        $stmt->bindParam(':id', $id, PDO::PARAM_INT);
        $stmt->execute();

        $record = $stmt->fetch();
        return $record ?: null;
    }

    /**
     * Find all records with optional pagination
     *
     * @param array $filters WHERE clause conditions
     * @param array $orderBy ORDER BY columns and direction
     * @param int|null $limit Maximum records to return
     * @param int|null $offset Records to skip
     * @return array Array of records
     */
    public function findAll(
        array $filters = [],
        array $orderBy = [],
        ?int $limit = null,
        ?int $offset = null
    ): array {
        $sql = "SELECT * FROM {$this->table}";
        $params = [];

        // Build WHERE clause
        if (!empty($filters)) {
            $conditions = [];
            foreach ($filters as $column => $value) {
                if ($value === null) {
                    $conditions[] = "$column IS NULL";
                } else {
                    $paramKey = ":$column";
                    $conditions[] = "$column = $paramKey";
                    $params[$paramKey] = $value;
                }
            }
            $sql .= " WHERE " . implode(" AND ", $conditions);
        }

        // Build ORDER BY clause
        if (!empty($orderBy)) {
            $orders = [];
            foreach ($orderBy as $column => $direction) {
                $direction = strtoupper($direction) === 'DESC' ? 'DESC' : 'ASC';
                $orders[] = "$column $direction";
            }
            $sql .= " ORDER BY " . implode(", ", $orders);
        }

        // Add pagination
        if ($limit !== null) {
            $sql .= " LIMIT :limit";
            $params[':limit'] = $limit;

            if ($offset !== null) {
                $sql .= " OFFSET :offset";
                $params[':offset'] = $offset;
            }
        }

        $stmt = $this->db->prepare($sql);
        $stmt->execute($params);

        return $stmt->fetchAll();
    }

    /**
     * Create a new record
     *
     * @param array $data Column-value pairs to insert
     * @return int Inserted record ID
     * @throws RuntimeException If insert fails
     */
    public function create(array $data): int {
        $columns = array_keys($data);
        $placeholders = array_map(fn(string $col): string => ":$col", $columns);

        $sql = sprintf(
            "INSERT INTO %s (%s) VALUES (%s)",
            $this->table,
            implode(", ", $columns),
            implode(", ", $placeholders)
        );

        $stmt = $this->db->prepare($sql);

        foreach ($data as $key => $value) {
            $paramType = is_int($value) ? PDO::PARAM_INT : PDO::PARAM_STR;
            $stmt->bindValue(":$key", $value, $paramType);
        }

        if (!$stmt->execute()) {
            error_log("Insert error: " . implode(", ", $stmt->errorInfo()));
            throw new RuntimeException("Failed to create record");
        }

        return (int) $this->db->lastInsertId();
    }

    /**
     * Update existing record
     *
     * @param int $id Record ID to update
     * @param array $data Column-value pairs to update
     * @return bool True if update successful
     * @throws RuntimeException If update fails
     */
    public function update(int $id, array $data): bool {
        $setParts = [];
        foreach (array_keys($data) as $column) {
            $setParts[] = "$column = :$column";
        }

        $sql = sprintf(
            "UPDATE %s SET %s WHERE id = :id",
            $this->table,
            implode(", ", $setParts)
        );

        $stmt = $this->db->prepare($sql);

        foreach ($data as $key => $value) {
            $paramType = is_int($value) ? PDO::PARAM_INT : PDO::PARAM_STR;
            $stmt->bindValue(":$key", $value, $paramType);
        }

        $stmt->bindValue(":id", $id, PDO::PARAM_INT);

        if (!$stmt->execute()) {
            error_log("Update error: " . implode(", ", $stmt->errorInfo()));
            throw new RuntimeException("Failed to update record");
        }

        return $stmt->rowCount() > 0;
    }

    /**
     * Delete record by ID
     *
     * @param int $id Record ID to delete
     * @return bool True if deletion successful
     * @throws RuntimeException If delete fails
     */
    public function delete(int $id): bool {
        $stmt = $this->db->prepare(
            "DELETE FROM {$this->table} WHERE id = :id"
        );

        $stmt->bindParam(':id', $id, PDO::PARAM_INT);

        if (!$stmt->execute()) {
            error_log("Delete error: " . implode(", ", $stmt->errorInfo()));
            throw new RuntimeException("Failed to delete record");
        }

        return $stmt->rowCount() > 0;
    }

    /**
     * Count records with optional filters
     *
     * @param array $filters WHERE clause conditions
     * @return int Number of matching records
     */
    public function count(array $filters = []): int {
        $sql = "SELECT COUNT(*) as count FROM {$this->table}";
        $params = [];

        if (!empty($filters)) {
            $conditions = [];
            foreach ($filters as $column => $value) {
                if ($value === null) {
                    $conditions[] = "$column IS NULL";
                } else {
                    $paramKey = ":$column";
                    $conditions[] = "$column = $paramKey";
                    $params[$paramKey] = $value;
                }
            }
            $sql .= " WHERE " . implode(" AND ", $conditions);
        }

        $stmt = $this->db->prepare($sql);
        $stmt->execute($params);

        $result = $stmt->fetch();
        return (int)($result['count'] ?? 0);
    }
}

/**
 * User Repository
 * Handles user-related database operations
 */
class UserRepository extends BaseRepository {
    protected string $table = 'user';

    /**
     * Find user by email address
     *
     * @param string $email User email
     * @return array|null User data or null
     */
    public function findByEmail(string $email): ?array {
        $stmt = $this->db->prepare(
            "SELECT * FROM user WHERE email = :email LIMIT 1"
        );

        $stmt->bindParam(':email', $email, PDO::PARAM_STR);
        $stmt->execute();

        $user = $stmt->fetch();
        return $user ?: null;
    }

    /**
     * Find user by username
     *
     * @param string $username Username
     * @return array|null User data or null
     */
    public function findByUsername(string $username): ?array {
        $stmt = $this->db->prepare(
            "SELECT * FROM user WHERE username = :username LIMIT 1"
        );

        $stmt->bindParam(':username', $username, PDO::PARAM_STR);
        $stmt->execute();

        $user = $stmt->fetch();
        return $user ?: null;
    }

    /**
     * Find users by role with pagination
     *
     * @param string $role User role (admin, user)
     * @param int $limit Records per page
     * @param int $offset Records to skip
     * @return array Array of users
     */
    public function findByRole(string $role, int $limit = 20, int $offset = 0): array {
        $stmt = $this->db->prepare(
            "SELECT * FROM user
             WHERE role = :role
             ORDER BY created_at DESC
             LIMIT :limit OFFSET :offset"
        );

        $stmt->bindParam(':role', $role, PDO::PARAM_STR);
        $stmt->bindParam(':limit', $limit, PDO::PARAM_INT);
        $stmt->bindParam(':offset', $offset, PDO::PARAM_INT);
        $stmt->execute();

        return $stmt->fetchAll();
    }

    /**
     * Verify user credentials and return user data
     *
     * @param string $email User email
     * @param string $password Plain text password
     * @return array|null User data without password hash if successful, null otherwise
     */
    public function verifyCredentials(string $email, string $password): ?array {
        $stmt = $this->db->prepare(
            "SELECT id, email, username, password_hash, first_name, last_name, role, status
             FROM user
             WHERE email = :email LIMIT 1"
        );

        $stmt->bindParam(':email', $email, PDO::PARAM_STR);
        $stmt->execute();

        $user = $stmt->fetch();

        if ($user === null) {
            return null;
        }

        if (!password_verify($password, $user['password_hash'])) {
            return null;
        }

        // Remove password hash before returning
        unset($user['password_hash']);

        return $user;
    }

    /**
     * Update user's last active timestamp
     *
     * @param int $userId User ID
     * @return bool True if update successful
     */
    public function updateLastActive(int $userId): bool {
        $stmt = $this->db->prepare(
            "UPDATE user SET last_active = NOW() WHERE id = :id"
        );

        $stmt->bindParam(':id', $userId, PDO::PARAM_INT);

        return $stmt->execute();
    }

    /**
     * Get user statistics
     *
     * @param int $userId User ID
     * @return array User statistics (recipe count, review count, etc.)
     */
    public function getUserStats(int $userId): array {
        $stmt = $this->db->prepare(
            "SELECT
                COUNT(DISTINCT r.id) as recipe_count,
                COUNT(DISTINCT rv.id) as review_count,
                COUNT(DISTINCT f.id) as favorite_count
             FROM user u
             LEFT JOIN recipe r ON u.id = r.author_id
             LEFT JOIN review rv ON u.id = rv.user_id
             LEFT JOIN favorite f ON u.id = f.user_id
             WHERE u.id = :userId
             GROUP BY u.id"
        );

        $stmt->bindParam(':userId', $userId, PDO::PARAM_INT);
        $stmt->execute();

        return $stmt->fetch() ?: [
            'recipe_count' => 0,
            'review_count' => 0,
            'favorite_count' => 0,
        ];
    }
}

/**
 * Recipe Repository
 * Handles recipe-related database operations with transactions
 */
class RecipeRepository extends BaseRepository {
    protected string $table = 'recipe';

    /**
     * Get published recipes with aggregated statistics
     *
     * @param array $filters Filter conditions
     * @param int $limit Records limit
     * @param int $offset Records offset
     * @return array Array of recipes with stats
     */
    public function findPublishedWithStats(
        array $filters = [],
        int $limit = 20,
        int $offset = 0
    ): array {
        $sql = "SELECT
                    r.*,
                    u.username as author_name,
                    COUNT(DISTINCT rv.id) as view_count,
                    COUNT(DISTINCT lr.id) as like_count,
                    AVG(rev.rating) as avg_rating
                 FROM recipe r
                 JOIN user u ON r.author_id = u.id
                 LEFT JOIN recipe_view rv ON r.id = rv.recipe_id
                 LEFT JOIN like_record lr ON r.id = lr.recipe_id
                 LEFT JOIN review rev ON r.id = rev.recipe_id
                 WHERE r.status = 'published'";

        $params = [];

        // Add filters
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
            $searchTerm = "%{$filters['search']}%";
            $params[':search'] = $searchTerm;
        }

        $sql .= " GROUP BY r.id
                  ORDER BY r.created_at DESC
                  LIMIT :limit OFFSET :offset";

        $stmt = $this->db->prepare($sql);

        foreach ($params as $key => $value) {
            $stmt->bindValue($key, $value, PDO::PARAM_STR);
        }

        $stmt->bindValue(':limit', $limit, PDO::PARAM_INT);
        $stmt->bindValue(':offset', $offset, PDO::PARAM_INT);

        $stmt->execute();

        return $stmt->fetchAll();
    }

    /**
     * Get recipe with full details including ingredients and instructions
     *
     * @param int $recipeId Recipe ID
     * @return array|null Recipe with nested details
     */
    public function findByIdWithDetails(int $recipeId): ?array {
        // Get main recipe data
        $stmt = $this->db->prepare(
            "SELECT r.*, u.username as author_name, u.email as author_email
             FROM recipe r
             JOIN user u ON r.author_id = u.id
             WHERE r.id = :id LIMIT 1"
        );

        $stmt->bindParam(':id', $recipeId, PDO::PARAM_INT);
        $stmt->execute();

        $recipe = $stmt->fetch();

        if ($recipe === false) {
            return null;
        }

        // Get ingredients
        $ingredientStmt = $this->db->prepare(
            "SELECT * FROM ingredient
             WHERE recipe_id = :recipe_id
             ORDER BY sort_order ASC"
        );

        $ingredientStmt->bindParam(':recipe_id', $recipeId, PDO::PARAM_INT);
        $ingredientStmt->execute();

        $recipe['ingredients'] = $ingredientStmt->fetchAll();

        // Get instructions
        $instructionStmt = $this->db->prepare(
            "SELECT * FROM instruction
             WHERE recipe_id = :recipe_id
             ORDER BY step_number ASC"
        );

        $instructionStmt->bindParam(':recipe_id', $recipeId, PDO::PARAM_INT);
        $instructionStmt->execute();

        $recipe['instructions'] = $instructionStmt->fetchAll();

        // Get images
        $imageStmt = $this->db->prepare(
            "SELECT * FROM recipe_image
             WHERE recipe_id = :recipe_id
             ORDER BY display_order ASC"
        );

        $imageStmt->bindParam(':recipe_id', $recipeId, PDO::PARAM_INT);
        $imageStmt->execute();

        $recipe['images'] = $imageStmt->fetchAll();

        return $recipe;
    }

    /**
     * Create recipe with nested ingredients and instructions (transactional)
     *
     * @param array $recipeData Recipe main data
     * @param array $ingredients Array of ingredient data
     * @param array $instructions Array of instruction data
     * @return int Created recipe ID
     * @throws RuntimeException If creation fails
     */
    public function createWithDetails(
        array $recipeData,
        array $ingredients = [],
        array $instructions = []
    ): int {
        try {
            $this->db->beginTransaction();

            // Insert main recipe
            $recipeSql = "INSERT INTO recipe (
                title, description, category, difficulty,
                prep_time, cook_time, servings, author_id,
                status, created_at, updated_at
            ) VALUES (
                :title, :description, :category, :difficulty,
                :prep_time, :cook_time, :servings, :author_id,
                :status, NOW(), NOW()
            )";

            $recipeStmt = $this->db->prepare($recipeSql);

            $recipeStmt->bindParam(':title', $recipeData['title'], PDO::PARAM_STR);
            $recipeStmt->bindParam(':description', $recipeData['description'], PDO::PARAM_STR);
            $recipeStmt->bindParam(':category', $recipeData['category'], PDO::PARAM_STR);
            $recipeStmt->bindParam(':difficulty', $recipeData['difficulty'], PDO::PARAM_STR);
            $recipeStmt->bindParam(':prep_time', $recipeData['prep_time'], PDO::PARAM_INT);
            $recipeStmt->bindParam(':cook_time', $recipeData['cook_time'], PDO::PARAM_INT);
            $recipeStmt->bindParam(':servings', $recipeData['servings'], PDO::PARAM_INT);
            $recipeStmt->bindParam(':author_id', $recipeData['author_id'], PDO::PARAM_INT);
            $recipeStmt->bindParam(':status', $recipeData['status'] ?? 'pending', PDO::PARAM_STR);

            $recipeStmt->execute();

            $recipeId = (int) $this->db->lastInsertId();

            // Insert ingredients
            if (!empty($ingredients)) {
                $ingredientStmt = $this->db->prepare(
                    "INSERT INTO ingredient (
                        recipe_id, name, quantity, unit, sort_order, created_at, updated_at
                    ) VALUES (
                        :recipe_id, :name, :quantity, :unit, :sort_order, NOW(), NOW()
                    )"
                );

                foreach ($ingredients as $index => $ingredient) {
                    $ingredientStmt->bindParam(':recipe_id', $recipeId, PDO::PARAM_INT);
                    $ingredientStmt->bindParam(':name', $ingredient['name'], PDO::PARAM_STR);
                    $ingredientStmt->bindParam(':quantity', $ingredient['quantity'], PDO::PARAM_STR);
                    $ingredientStmt->bindParam(':unit', $ingredient['unit'], PDO::PARAM_STR);
                    $ingredientStmt->bindParam(':sort_order', $index, PDO::PARAM_INT);

                    $ingredientStmt->execute();
                }
            }

            // Insert instructions
            if (!empty($instructions)) {
                $instructionStmt = $this->db->prepare(
                    "INSERT INTO instruction (
                        recipe_id, step_number, instruction_text, created_at, updated_at
                    ) VALUES (
                        :recipe_id, :step_number, :instruction_text, NOW(), NOW()
                    )"
                );

                foreach ($instructions as $index => $instruction) {
                    $instructionStmt->bindParam(':recipe_id', $recipeId, PDO::PARAM_INT);
                    $instructionStmt->bindParam(':step_number', $index + 1, PDO::PARAM_INT);
                    $instructionStmt->bindParam(':instruction_text', $instruction['text'], PDO::PARAM_STR);

                    $instructionStmt->execute();
                }
            }

            $this->db->commit();

            return $recipeId;

        } catch (Exception $e) {
            $this->db->rollBack();
            error_log("Recipe creation error: " . $e->getMessage());
            throw new RuntimeException("Failed to create recipe");
        }
    }
}

/**
 * Transaction Manager
 * Handles complex multi-step database operations
 */
class TransactionManager {
    private PDO $db;

    public function __construct() {
        $this->db = Database::getInstance();
    }

    /**
     * Execute a callback function within a transaction
     *
     * @param callable $callback Function to execute within transaction
     * @return mixed Result of callback
     * @throws Exception If callback fails, transaction is rolled back
     */
    public function execute(callable $callback): mixed {
        try {
            $this->db->beginTransaction();

            $result = $callback($this->db);

            $this->db->commit();

            return $result;

        } catch (Exception $e) {
            $this->db->rollBack();
            error_log("Transaction error: " . $e->getMessage());
            throw $e;
        }
    }
}

/**
 * Usage Examples
 */

// Example 1: Simple user lookup
function exampleFindUser(): void {
    $userRepo = new UserRepository();
    $user = $userRepo->findByEmail('user@example.com');

    if ($user !== null) {
        echo "Found user: " . $user['username'];
    }
}

// Example 2: Create user with password hashing
function exampleCreateUser(): void {
    $userRepo = new UserRepository();

    $userData = [
        'username' => 'newuser',
        'email' => 'newuser@example.com',
        'password_hash' => password_hash('securePassword123!', PASSWORD_DEFAULT),
        'first_name' => 'John',
        'last_name' => 'Doe',
        'role' => 'user',
        'status' => 'active',
    ];

    $userId = $userRepo->create($userData);
    echo "Created user with ID: " . $userId;
}

// Example 3: Transactional recipe creation
function exampleCreateRecipe(): void {
    $recipeRepo = new RecipeRepository();
    $transactionManager = new TransactionManager();

    $recipeData = [
        'title' => 'Delicious Pasta',
        'description' => 'A wonderful pasta recipe',
        'category' => 'Dinner',
        'difficulty' => 'Medium',
        'prep_time' => 15,
        'cook_time' => 30,
        'servings' => 4,
        'author_id' => 1,
        'status' => 'pending',
    ];

    $ingredients = [
        ['name' => 'Pasta', 'quantity' => '400g', 'unit' => ''],
        ['name' => 'Tomato Sauce', 'quantity' => '500ml', 'unit' => ''],
        ['name' => 'Parmesan', 'quantity' => '100g', 'unit' => 'grated'],
    ];

    $instructions = [
        ['text' => 'Boil the pasta in salted water'],
        ['text' => 'Heat the tomato sauce in a pan'],
        ['text' => 'Drain pasta and mix with sauce'],
        ['text' => 'Serve with parmesan on top'],
    ];

    try {
        $recipeId = $recipeRepo->createWithDetails(
            $recipeData,
            $ingredients,
            $instructions
        );

        echo "Recipe created with ID: " . $recipeId;

    } catch (RuntimeException $e) {
        echo "Failed to create recipe: " . $e->getMessage();
    }
}

// Example 4: Search recipes with filters
function exampleSearchRecipes(): void {
    $recipeRepo = new RecipeRepository();

    $recipes = $recipeRepo->findPublishedWithStats([
        'category' => 'Dinner',
        'difficulty' => 'Medium',
        'search' => 'pasta',
    ], limit: 10, offset: 0);

    foreach ($recipes as $recipe) {
        echo sprintf(
            "%s by %s (Rating: %.1f)\n",
            $recipe['title'],
            $recipe['author_name'],
            $recipe['avg_rating'] ?? 0
        );
    }
}
