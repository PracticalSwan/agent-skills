# MySQL 8.4 Patterns (2026)

Up-to-date MySQL patterns for relational schema design, query optimization, stored procedures, triggers, and API-oriented workloads.

## Version Context
- **MySQL 8.4 LTS** is the current long-term baseline for modern production usage.
- For this project (XAMPP + MySQL/MariaDB), patterns remain compatible with MySQL 8.x and most MariaDB 10.6+ features.

## Schema Design Principles

### Naming & Structure
- Use singular table names: `user`, `recipe`, `review`.
- Use `id` as primary key (`INT AUTO_INCREMENT` for course scope).
- Include `created_at`, `updated_at` in operational tables.
- Add explicit foreign key names and cascading rules.

```sql
CREATE TABLE recipe (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    category VARCHAR(50),
    difficulty ENUM('Easy', 'Medium', 'Hard') NOT NULL DEFAULT 'Medium',
    prep_time INT NOT NULL DEFAULT 0,
    cook_time INT NOT NULL DEFAULT 0,
    servings INT NOT NULL DEFAULT 1,
    author_id INT NOT NULL,
    status ENUM('published', 'pending', 'rejected') NOT NULL DEFAULT 'pending',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_recipe_author
        FOREIGN KEY (author_id)
        REFERENCES user(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
```

## Query Patterns

### API List Endpoint Query

```sql
SELECT
    r.id,
    r.title,
    r.category,
    r.difficulty,
    r.prep_time,
    r.cook_time,
    r.servings,
    r.created_at,
    u.username AS author_name,
    COUNT(DISTINCT rv.id) AS view_count,
    COUNT(DISTINCT lr.id) AS like_count,
    ROUND(AVG(rev.rating), 2) AS avg_rating
FROM recipe r
JOIN user u ON u.id = r.author_id
LEFT JOIN recipe_view rv ON rv.recipe_id = r.id
LEFT JOIN like_record lr ON lr.recipe_id = r.id
LEFT JOIN review rev ON rev.recipe_id = r.id
WHERE r.status = 'published'
GROUP BY r.id, u.username
ORDER BY r.created_at DESC
LIMIT 20 OFFSET 0;
```

### Search Query Pattern

```sql
SELECT
    r.id,
    r.title,
    r.description,
    r.category,
    r.difficulty,
    u.username AS author_name
FROM recipe r
JOIN user u ON u.id = r.author_id
WHERE r.status = 'published'
  AND (
      r.title LIKE CONCAT('%', :search, '%')
      OR r.description LIKE CONCAT('%', :search, '%')
  )
ORDER BY r.created_at DESC
LIMIT :limit OFFSET :offset;
```

## Indexing Strategy

### Operational Indexes

```sql
CREATE INDEX idx_user_email ON user(email);
CREATE INDEX idx_recipe_author_status ON recipe(author_id, status);
CREATE INDEX idx_recipe_category_status ON recipe(category, status);
CREATE INDEX idx_review_recipe_user ON review(recipe_id, user_id);
CREATE INDEX idx_recipe_view_recipe_viewed ON recipe_view(recipe_id, viewed_at);
CREATE INDEX idx_daily_stat_date ON daily_stat(stat_date);
```

### Notes
- Index columns used in JOIN, WHERE, ORDER BY.
- Keep indexes minimal; each write pays index maintenance cost.
- Verify with `EXPLAIN ANALYZE`.

## Stored Procedure Pattern

```sql
DELIMITER $$

CREATE PROCEDURE usp_CreateRecipe (
    IN p_title VARCHAR(200),
    IN p_description TEXT,
    IN p_category VARCHAR(50),
    IN p_difficulty VARCHAR(10),
    IN p_prep_time INT,
    IN p_cook_time INT,
    IN p_servings INT,
    IN p_author_id INT
)
BEGIN
    DECLARE v_recipe_id INT;

    START TRANSACTION;

    INSERT INTO recipe (
        title, description, category, difficulty,
        prep_time, cook_time, servings, author_id,
        status, created_at, updated_at
    ) VALUES (
        p_title, p_description, p_category, p_difficulty,
        p_prep_time, p_cook_time, p_servings, p_author_id,
        'pending', NOW(), NOW()
    );

    SET v_recipe_id = LAST_INSERT_ID();

    COMMIT;

    SELECT v_recipe_id AS recipe_id;
END$$

DELIMITER ;
```

## Trigger Pattern

```sql
DELIMITER $$

CREATE TRIGGER trg_RecipeView_UpdateStat
AFTER INSERT ON recipe_view
FOR EACH ROW
BEGIN
    INSERT INTO daily_stat (
        stat_date,
        recipe_view_count,
        page_view_count,
        active_user_count,
        new_user_count,
        created_at,
        updated_at
    )
    VALUES (
        DATE(NEW.viewed_at),
        1,
        0,
        0,
        0,
        NOW(),
        NOW()
    )
    ON DUPLICATE KEY UPDATE
        recipe_view_count = recipe_view_count + 1,
        updated_at = NOW();
END$$

DELIMITER ;
```

## View Pattern

```sql
CREATE OR REPLACE VIEW vw_recipe_with_stat AS
SELECT
    r.id,
    r.title,
    r.category,
    r.difficulty,
    r.status,
    r.author_id,
    u.username AS author_name,
    COUNT(DISTINCT rv.id) AS view_count,
    COUNT(DISTINCT lr.id) AS like_count,
    ROUND(AVG(rev.rating), 2) AS avg_rating,
    r.created_at,
    r.updated_at
FROM recipe r
JOIN user u ON u.id = r.author_id
LEFT JOIN recipe_view rv ON rv.recipe_id = r.id
LEFT JOIN like_record lr ON lr.recipe_id = r.id
LEFT JOIN review rev ON rev.recipe_id = r.id
GROUP BY
    r.id, r.title, r.category, r.difficulty, r.status,
    r.author_id, u.username, r.created_at, r.updated_at;
```

## Performance Workflow

### Use `EXPLAIN ANALYZE`

```sql
EXPLAIN ANALYZE
SELECT r.id, r.title, u.username
FROM recipe r
JOIN user u ON u.id = r.author_id
WHERE r.status = 'published'
ORDER BY r.created_at DESC
LIMIT 20;
```

### Check cardinality and selectivity
- High-selectivity columns are better index candidates.
- Composite index order matters: put most selective + most commonly filtered prefix first.

## Data Integrity Patterns
- Enforce one review per user/recipe: `UNIQUE (user_id, recipe_id)`
- Enforce one favorite per user/recipe: `UNIQUE (user_id, recipe_id)`
- Enforce one like per user/recipe: `UNIQUE (user_id, recipe_id)`

```sql
ALTER TABLE review
ADD CONSTRAINT uq_review_user_recipe UNIQUE (user_id, recipe_id);
```

## Backup & Restore Basics

```bash
# Backup
mysqldump -u root -p recipe_sharing_system > backup.sql

# Restore
mysql -u root -p recipe_sharing_system < backup.sql
```

## References
- MySQL 8.4 Reference Manual: https://dev.mysql.com/doc/refman/8.4/en/
- MySQL Performance Schema: https://dev.mysql.com/doc/refman/8.4/en/performance-schema.html
- EXPLAIN Statement: https://dev.mysql.com/doc/refman/8.4/en/explain.html
- InnoDB Locking: https://dev.mysql.com/doc/refman/8.4/en/innodb-locking.html
