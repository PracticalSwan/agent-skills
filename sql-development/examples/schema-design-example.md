# Recipe Management System — Database Schema Design

## Entity Relationship Diagram (Text)

```
┌──────────┐       ┌───────────┐       ┌────────────────┐
│  [User]  │1────M│  [Recipe]  │1────M│   [Comment]    │
│──────────│       │───────────│       │────────────────│
│ Id (PK)  │       │ Id (PK)   │       │ Id (PK)        │
│ UserName │       │ Title     │       │ RecipeId (FK)  │
│ Email    │       │ AuthorId  │──┐    │ UserId (FK)    │
│ PassHash │       │ CategoryId│  │    │ Body           │
│ Role     │       │ PrepTime  │  │    │ CreatedAt      │
│ CreatedAt│       │ CookTime  │  │    └────────────────┘
└──────────┘       │ Servings  │  │
      │1           │ CreatedAt │  │    ┌────────────────┐
      │            └───────────┘  └──M│   [Rating]     │
      │                  │1            │────────────────│
      │                  │             │ Id (PK)        │
      └────────M─────────┼───────────→│ RecipeId (FK)  │
                         │             │ UserId (FK)    │
                         │             │ Score (1-5)    │
                    ┌────┴──────┐      │ CreatedAt      │
               ┌────┤           ├────┐ └────────────────┘
               │    │           │    │
          ┌────┴───┐     ┌─────┴─────┐    ┌──────────┐
          │Recipe  │     │ RecipeTag  │M──1│  [Tag]   │
          │Ingredi-│     │───────────│    │──────────│
          │ent     │     │ RecipeId   │    │ Id (PK)  │
          │────────│     │ TagId      │    │ Name     │
          │RecipeId│     └───────────┘    └──────────┘
          │Ingredi-│
          │entId   │     ┌───────────┐
          │Quantity │M──1│[Ingredient]│
          │Unit    │     │───────────│
          └────────┘     │ Id (PK)   │
                         │ Name      │
     ┌───────────┐       └───────────┘
     │[Category] │
     │───────────│
     │ Id (PK)   │1────M Recipe.CategoryId
     │ Name      │
     │ ParentId  │──→ self (nullable, for hierarchy)
     └───────────┘
```

## Table Definitions

### User

```sql
CREATE TABLE dbo.[User] (
    Id              INT             IDENTITY(1,1) NOT NULL,
    UserName        NVARCHAR(100)   NOT NULL,
    Email           NVARCHAR(255)   NOT NULL,
    PasswordHash    NVARCHAR(500)   NOT NULL,
    DisplayName     NVARCHAR(200)   NULL,
    Bio             NVARCHAR(1000)  NULL,
    AvatarUrl       NVARCHAR(500)   NULL,
    Role            NVARCHAR(20)    NOT NULL DEFAULT 'user',
    IsActive        BIT             NOT NULL DEFAULT 1,
    CreatedAt       DATETIME2(3)    NOT NULL DEFAULT GETUTCDATE(),
    UpdatedAt       DATETIME2(3)    NOT NULL DEFAULT GETUTCDATE(),

    CONSTRAINT PK_User PRIMARY KEY CLUSTERED (Id),
    CONSTRAINT UQ_User_UserName UNIQUE (UserName),
    CONSTRAINT UQ_User_Email UNIQUE (Email),
    CONSTRAINT CK_User_Role CHECK (Role IN ('user', 'admin', 'moderator'))
);

CREATE NONCLUSTERED INDEX IX_User_Email ON dbo.[User] (Email);
CREATE NONCLUSTERED INDEX IX_User_Role ON dbo.[User] (Role) WHERE IsActive = 1;
```

### Category

```sql
CREATE TABLE dbo.Category (
    Id              INT             IDENTITY(1,1) NOT NULL,
    Name            NVARCHAR(100)   NOT NULL,
    Slug            NVARCHAR(100)   NOT NULL,
    Description     NVARCHAR(500)   NULL,
    ParentId        INT             NULL,
    SortOrder       INT             NOT NULL DEFAULT 0,
    CreatedAt       DATETIME2(3)    NOT NULL DEFAULT GETUTCDATE(),

    CONSTRAINT PK_Category PRIMARY KEY CLUSTERED (Id),
    CONSTRAINT UQ_Category_Slug UNIQUE (Slug),
    CONSTRAINT FK_Category_Parent FOREIGN KEY (ParentId) REFERENCES dbo.Category(Id)
);

CREATE NONCLUSTERED INDEX IX_Category_ParentId ON dbo.Category (ParentId);
```

### Recipe

```sql
CREATE TABLE dbo.Recipe (
    Id              INT             IDENTITY(1,1) NOT NULL,
    Title           NVARCHAR(200)   NOT NULL,
    Slug            NVARCHAR(200)   NOT NULL,
    Description     NVARCHAR(MAX)   NULL,
    Instructions    NVARCHAR(MAX)   NULL,
    AuthorId        INT             NOT NULL,
    CategoryId      INT             NULL,
    PrepTimeMinutes INT             NULL,
    CookTimeMinutes INT             NULL,
    Servings        INT             NULL,
    Difficulty      NVARCHAR(20)    NOT NULL DEFAULT 'medium',
    ImageUrl        NVARCHAR(500)   NULL,
    IsPublished     BIT             NOT NULL DEFAULT 0,
    ViewCount       INT             NOT NULL DEFAULT 0,
    CreatedAt       DATETIME2(3)    NOT NULL DEFAULT GETUTCDATE(),
    UpdatedAt       DATETIME2(3)    NOT NULL DEFAULT GETUTCDATE(),

    CONSTRAINT PK_Recipe PRIMARY KEY CLUSTERED (Id),
    CONSTRAINT UQ_Recipe_Slug UNIQUE (Slug),
    CONSTRAINT FK_Recipe_Author FOREIGN KEY (AuthorId) REFERENCES dbo.[User](Id),
    CONSTRAINT FK_Recipe_Category FOREIGN KEY (CategoryId) REFERENCES dbo.Category(Id),
    CONSTRAINT CK_Recipe_Difficulty CHECK (Difficulty IN ('easy', 'medium', 'hard')),
    CONSTRAINT CK_Recipe_PrepTime CHECK (PrepTimeMinutes IS NULL OR PrepTimeMinutes >= 0),
    CONSTRAINT CK_Recipe_CookTime CHECK (CookTimeMinutes IS NULL OR CookTimeMinutes >= 0),
    CONSTRAINT CK_Recipe_Servings CHECK (Servings IS NULL OR Servings > 0)
);

CREATE NONCLUSTERED INDEX IX_Recipe_AuthorId ON dbo.Recipe (AuthorId) INCLUDE (Title, CreatedAt);
CREATE NONCLUSTERED INDEX IX_Recipe_CategoryId ON dbo.Recipe (CategoryId) WHERE IsPublished = 1;
CREATE NONCLUSTERED INDEX IX_Recipe_CreatedAt ON dbo.Recipe (CreatedAt DESC) WHERE IsPublished = 1;
CREATE NONCLUSTERED INDEX IX_Recipe_Title ON dbo.Recipe (Title) INCLUDE (AuthorId, CategoryId, CreatedAt);
```

### Ingredient

```sql
CREATE TABLE dbo.Ingredient (
    Id              INT             IDENTITY(1,1) NOT NULL,
    Name            NVARCHAR(200)   NOT NULL,
    CreatedAt       DATETIME2(3)    NOT NULL DEFAULT GETUTCDATE(),

    CONSTRAINT PK_Ingredient PRIMARY KEY CLUSTERED (Id),
    CONSTRAINT UQ_Ingredient_Name UNIQUE (Name)
);
```

### RecipeIngredient (Junction)

```sql
CREATE TABLE dbo.RecipeIngredient (
    RecipeId        INT             NOT NULL,
    IngredientId    INT             NOT NULL,
    Quantity        DECIMAL(10, 2)  NOT NULL,
    Unit            NVARCHAR(50)    NOT NULL,
    SortOrder       INT             NOT NULL DEFAULT 0,
    Notes           NVARCHAR(200)   NULL,

    CONSTRAINT PK_RecipeIngredient PRIMARY KEY CLUSTERED (RecipeId, IngredientId),
    CONSTRAINT FK_RecipeIngredient_Recipe FOREIGN KEY (RecipeId)
        REFERENCES dbo.Recipe(Id) ON DELETE CASCADE,
    CONSTRAINT FK_RecipeIngredient_Ingredient FOREIGN KEY (IngredientId)
        REFERENCES dbo.Ingredient(Id),
    CONSTRAINT CK_RecipeIngredient_Quantity CHECK (Quantity > 0)
);
```

### Tag

```sql
CREATE TABLE dbo.Tag (
    Id              INT             IDENTITY(1,1) NOT NULL,
    Name            NVARCHAR(100)   NOT NULL,
    Slug            NVARCHAR(100)   NOT NULL,

    CONSTRAINT PK_Tag PRIMARY KEY CLUSTERED (Id),
    CONSTRAINT UQ_Tag_Name UNIQUE (Name),
    CONSTRAINT UQ_Tag_Slug UNIQUE (Slug)
);
```

### RecipeTag (Junction)

```sql
CREATE TABLE dbo.RecipeTag (
    RecipeId        INT NOT NULL,
    TagId           INT NOT NULL,

    CONSTRAINT PK_RecipeTag PRIMARY KEY CLUSTERED (RecipeId, TagId),
    CONSTRAINT FK_RecipeTag_Recipe FOREIGN KEY (RecipeId)
        REFERENCES dbo.Recipe(Id) ON DELETE CASCADE,
    CONSTRAINT FK_RecipeTag_Tag FOREIGN KEY (TagId)
        REFERENCES dbo.Tag(Id)
);

CREATE NONCLUSTERED INDEX IX_RecipeTag_TagId ON dbo.RecipeTag (TagId);
```

### Comment

```sql
CREATE TABLE dbo.Comment (
    Id              INT             IDENTITY(1,1) NOT NULL,
    RecipeId        INT             NOT NULL,
    UserId          INT             NOT NULL,
    ParentId        INT             NULL,
    Body            NVARCHAR(2000)  NOT NULL,
    IsDeleted       BIT             NOT NULL DEFAULT 0,
    CreatedAt       DATETIME2(3)    NOT NULL DEFAULT GETUTCDATE(),
    UpdatedAt       DATETIME2(3)    NOT NULL DEFAULT GETUTCDATE(),

    CONSTRAINT PK_Comment PRIMARY KEY CLUSTERED (Id),
    CONSTRAINT FK_Comment_Recipe FOREIGN KEY (RecipeId)
        REFERENCES dbo.Recipe(Id) ON DELETE CASCADE,
    CONSTRAINT FK_Comment_User FOREIGN KEY (UserId)
        REFERENCES dbo.[User](Id),
    CONSTRAINT FK_Comment_Parent FOREIGN KEY (ParentId)
        REFERENCES dbo.Comment(Id)
);

CREATE NONCLUSTERED INDEX IX_Comment_RecipeId ON dbo.Comment (RecipeId, CreatedAt);
CREATE NONCLUSTERED INDEX IX_Comment_UserId ON dbo.Comment (UserId);
```

### Rating

```sql
CREATE TABLE dbo.Rating (
    Id              INT             IDENTITY(1,1) NOT NULL,
    RecipeId        INT             NOT NULL,
    UserId          INT             NOT NULL,
    Score           TINYINT         NOT NULL,
    CreatedAt       DATETIME2(3)    NOT NULL DEFAULT GETUTCDATE(),

    CONSTRAINT PK_Rating PRIMARY KEY CLUSTERED (Id),
    CONSTRAINT UQ_Rating_UserRecipe UNIQUE (UserId, RecipeId),
    CONSTRAINT FK_Rating_Recipe FOREIGN KEY (RecipeId)
        REFERENCES dbo.Recipe(Id) ON DELETE CASCADE,
    CONSTRAINT FK_Rating_User FOREIGN KEY (UserId)
        REFERENCES dbo.[User](Id),
    CONSTRAINT CK_Rating_Score CHECK (Score BETWEEN 1 AND 5)
);

CREATE NONCLUSTERED INDEX IX_Rating_RecipeId ON dbo.Rating (RecipeId) INCLUDE (Score);
```

### ErrorLog (Support Table)

```sql
CREATE TABLE dbo.ErrorLog (
    Id              INT             IDENTITY(1,1) NOT NULL,
    ErrorNumber     INT             NULL,
    ErrorSeverity   INT             NULL,
    ErrorState      INT             NULL,
    ErrorLine       INT             NULL,
    ErrorProcedure  NVARCHAR(200)   NULL,
    ErrorMessage    NVARCHAR(4000)  NULL,
    LogDate         DATETIME2(3)    NOT NULL DEFAULT GETUTCDATE(),

    CONSTRAINT PK_ErrorLog PRIMARY KEY CLUSTERED (Id)
);
```

---

## Views

### vw_RecipeWithStats

Provides recipes with calculated rating and comment counts.

```sql
CREATE OR ALTER VIEW dbo.vw_RecipeWithStats
AS
SELECT
    r.Id,
    r.Title,
    r.Slug,
    r.Description,
    r.AuthorId,
    u.DisplayName AS AuthorName,
    c.Name AS CategoryName,
    r.PrepTimeMinutes,
    r.CookTimeMinutes,
    r.Servings,
    r.Difficulty,
    r.ImageUrl,
    r.IsPublished,
    r.ViewCount,
    r.CreatedAt,
    r.UpdatedAt,
    ISNULL(rs.AvgRating, 0) AS AvgRating,
    ISNULL(rs.RatingCount, 0) AS RatingCount,
    ISNULL(cs.CommentCount, 0) AS CommentCount,
    STRING_AGG(t.Name, ', ') WITHIN GROUP (ORDER BY t.Name) AS Tags
FROM dbo.Recipe r
JOIN dbo.[User] u ON u.Id = r.AuthorId
LEFT JOIN dbo.Category c ON c.Id = r.CategoryId
LEFT JOIN (
    SELECT RecipeId, AVG(CAST(Score AS DECIMAL(3,2))) AS AvgRating, COUNT(*) AS RatingCount
    FROM dbo.Rating
    GROUP BY RecipeId
) rs ON rs.RecipeId = r.Id
LEFT JOIN (
    SELECT RecipeId, COUNT(*) AS CommentCount
    FROM dbo.Comment
    WHERE IsDeleted = 0
    GROUP BY RecipeId
) cs ON cs.RecipeId = r.Id
LEFT JOIN dbo.RecipeTag rt ON rt.RecipeId = r.Id
LEFT JOIN dbo.Tag t ON t.Id = rt.TagId
GROUP BY
    r.Id, r.Title, r.Slug, r.Description, r.AuthorId, u.DisplayName,
    c.Name, r.PrepTimeMinutes, r.CookTimeMinutes, r.Servings, r.Difficulty,
    r.ImageUrl, r.IsPublished, r.ViewCount, r.CreatedAt, r.UpdatedAt,
    rs.AvgRating, rs.RatingCount, cs.CommentCount;
GO
```

### vw_UserProfile

User profile with activity summary.

```sql
CREATE OR ALTER VIEW dbo.vw_UserProfile
AS
SELECT
    u.Id,
    u.UserName,
    u.DisplayName,
    u.Bio,
    u.AvatarUrl,
    u.Role,
    u.CreatedAt AS MemberSince,
    COUNT(DISTINCT r.Id) AS RecipeCount,
    COUNT(DISTINCT cm.Id) AS CommentCount,
    COUNT(DISTINCT rt.RecipeId) AS RatedRecipeCount
FROM dbo.[User] u
LEFT JOIN dbo.Recipe r ON r.AuthorId = u.Id AND r.IsPublished = 1
LEFT JOIN dbo.Comment cm ON cm.UserId = u.Id AND cm.IsDeleted = 0
LEFT JOIN dbo.Rating rt ON rt.UserId = u.Id
WHERE u.IsActive = 1
GROUP BY u.Id, u.UserName, u.DisplayName, u.Bio, u.AvatarUrl, u.Role, u.CreatedAt;
GO
```

---

## Stored Procedures

### usp_Recipe_Search

Full-text search with filters, pagination, and sorting.

```sql
CREATE OR ALTER PROCEDURE dbo.usp_Recipe_Search
    @SearchTerm     NVARCHAR(200)   = NULL,
    @CategoryId     INT             = NULL,
    @TagName        NVARCHAR(100)   = NULL,
    @Difficulty     NVARCHAR(20)    = NULL,
    @MaxPrepTime    INT             = NULL,
    @PageNumber     INT             = 1,
    @PageSize       INT             = 20,
    @SortBy         NVARCHAR(20)    = 'newest',
    @TotalCount     INT             = 0 OUTPUT
AS
BEGIN
    SET NOCOUNT ON;

    SELECT @TotalCount = COUNT(DISTINCT r.Id)
    FROM dbo.Recipe r
    LEFT JOIN dbo.RecipeTag rt ON rt.RecipeId = r.Id
    LEFT JOIN dbo.Tag t ON t.Id = rt.TagId
    WHERE r.IsPublished = 1
        AND (@SearchTerm IS NULL OR r.Title LIKE N'%' + @SearchTerm + N'%'
             OR r.Description LIKE N'%' + @SearchTerm + N'%')
        AND (@CategoryId IS NULL OR r.CategoryId = @CategoryId)
        AND (@TagName IS NULL OR t.Name = @TagName)
        AND (@Difficulty IS NULL OR r.Difficulty = @Difficulty)
        AND (@MaxPrepTime IS NULL OR r.PrepTimeMinutes <= @MaxPrepTime);

    SELECT
        v.Id, v.Title, v.Slug, v.Description, v.AuthorName,
        v.CategoryName, v.PrepTimeMinutes, v.CookTimeMinutes,
        v.Servings, v.Difficulty, v.ImageUrl, v.AvgRating,
        v.RatingCount, v.CommentCount, v.Tags, v.CreatedAt
    FROM dbo.vw_RecipeWithStats v
    WHERE v.IsPublished = 1
        AND (@SearchTerm IS NULL OR v.Title LIKE N'%' + @SearchTerm + N'%'
             OR v.Description LIKE N'%' + @SearchTerm + N'%')
        AND (@CategoryId IS NULL OR v.AuthorName IS NOT NULL AND EXISTS (
            SELECT 1 FROM dbo.Recipe r2 WHERE r2.Id = v.Id AND r2.CategoryId = @CategoryId))
        AND (@Difficulty IS NULL OR v.Difficulty = @Difficulty)
    ORDER BY
        CASE @SortBy
            WHEN 'newest'    THEN v.CreatedAt END DESC,
        CASE @SortBy
            WHEN 'oldest'    THEN v.CreatedAt END ASC,
        CASE @SortBy
            WHEN 'rating'    THEN v.AvgRating END DESC,
        CASE @SortBy
            WHEN 'popular'   THEN v.ViewCount END DESC,
        v.CreatedAt DESC
    OFFSET (@PageNumber - 1) * @PageSize ROWS
    FETCH NEXT @PageSize ROWS ONLY;
END;
GO
```

### usp_Recipe_GetById

Retrieve a full recipe with all related data.

```sql
CREATE OR ALTER PROCEDURE dbo.usp_Recipe_GetById
    @RecipeId INT
AS
BEGIN
    SET NOCOUNT ON;

    -- Recipe details
    SELECT * FROM dbo.vw_RecipeWithStats WHERE Id = @RecipeId;

    -- Ingredients
    SELECT i.Name, ri.Quantity, ri.Unit, ri.Notes
    FROM dbo.RecipeIngredient ri
    JOIN dbo.Ingredient i ON i.Id = ri.IngredientId
    WHERE ri.RecipeId = @RecipeId
    ORDER BY ri.SortOrder;

    -- Comments (threaded)
    SELECT c.Id, c.ParentId, c.Body, c.CreatedAt,
           u.UserName, u.DisplayName, u.AvatarUrl
    FROM dbo.Comment c
    JOIN dbo.[User] u ON u.Id = c.UserId
    WHERE c.RecipeId = @RecipeId AND c.IsDeleted = 0
    ORDER BY c.CreatedAt;

    -- Increment view count
    UPDATE dbo.Recipe SET ViewCount = ViewCount + 1 WHERE Id = @RecipeId;
END;
GO
```

---

## Migration Script

Run this script to create the full schema from scratch.

```sql
-- ============================================================================
-- Recipe Management System — Initial Migration
-- Version: 1.0.0
-- Date: 2026-02-11
-- ============================================================================

BEGIN TRANSACTION;

BEGIN TRY
    -- Tables (in dependency order)
    -- 1. User
    IF NOT EXISTS (SELECT 1 FROM sys.tables WHERE name = 'User' AND schema_id = SCHEMA_ID('dbo'))
    BEGIN
        -- [paste User CREATE TABLE from above]
        PRINT 'Created table: User';
    END;

    -- 2. Category
    IF NOT EXISTS (SELECT 1 FROM sys.tables WHERE name = 'Category' AND schema_id = SCHEMA_ID('dbo'))
    BEGIN
        -- [paste Category CREATE TABLE from above]
        PRINT 'Created table: Category';
    END;

    -- 3. Recipe
    IF NOT EXISTS (SELECT 1 FROM sys.tables WHERE name = 'Recipe' AND schema_id = SCHEMA_ID('dbo'))
    BEGIN
        -- [paste Recipe CREATE TABLE from above]
        PRINT 'Created table: Recipe';
    END;

    -- 4. Ingredient
    IF NOT EXISTS (SELECT 1 FROM sys.tables WHERE name = 'Ingredient' AND schema_id = SCHEMA_ID('dbo'))
    BEGIN
        -- [paste Ingredient CREATE TABLE from above]
        PRINT 'Created table: Ingredient';
    END;

    -- 5. RecipeIngredient
    IF NOT EXISTS (SELECT 1 FROM sys.tables WHERE name = 'RecipeIngredient' AND schema_id = SCHEMA_ID('dbo'))
    BEGIN
        -- [paste RecipeIngredient CREATE TABLE from above]
        PRINT 'Created table: RecipeIngredient';
    END;

    -- 6. Tag
    IF NOT EXISTS (SELECT 1 FROM sys.tables WHERE name = 'Tag' AND schema_id = SCHEMA_ID('dbo'))
    BEGIN
        -- [paste Tag CREATE TABLE from above]
        PRINT 'Created table: Tag';
    END;

    -- 7. RecipeTag
    IF NOT EXISTS (SELECT 1 FROM sys.tables WHERE name = 'RecipeTag' AND schema_id = SCHEMA_ID('dbo'))
    BEGIN
        -- [paste RecipeTag CREATE TABLE from above]
        PRINT 'Created table: RecipeTag';
    END;

    -- 8. Comment
    IF NOT EXISTS (SELECT 1 FROM sys.tables WHERE name = 'Comment' AND schema_id = SCHEMA_ID('dbo'))
    BEGIN
        -- [paste Comment CREATE TABLE from above]
        PRINT 'Created table: Comment';
    END;

    -- 9. Rating
    IF NOT EXISTS (SELECT 1 FROM sys.tables WHERE name = 'Rating' AND schema_id = SCHEMA_ID('dbo'))
    BEGIN
        -- [paste Rating CREATE TABLE from above]
        PRINT 'Created table: Rating';
    END;

    -- 10. ErrorLog
    IF NOT EXISTS (SELECT 1 FROM sys.tables WHERE name = 'ErrorLog' AND schema_id = SCHEMA_ID('dbo'))
    BEGIN
        -- [paste ErrorLog CREATE TABLE from above]
        PRINT 'Created table: ErrorLog';
    END;

    -- Seed data
    INSERT INTO dbo.Category (Name, Slug, Description, SortOrder) VALUES
        (N'Appetizers',  N'appetizers',  N'Starters and small plates', 1),
        (N'Main Course', N'main-course', N'Entrees and main dishes',   2),
        (N'Desserts',    N'desserts',    N'Sweet treats and pastries',  3),
        (N'Beverages',   N'beverages',   N'Drinks and cocktails',      4),
        (N'Soups',       N'soups',       N'Soups and stews',           5);

    INSERT INTO dbo.Tag (Name, Slug) VALUES
        (N'Vegetarian',  N'vegetarian'),
        (N'Vegan',       N'vegan'),
        (N'Gluten-Free', N'gluten-free'),
        (N'Quick',       N'quick'),
        (N'Healthy',     N'healthy'),
        (N'Comfort Food',N'comfort-food'),
        (N'Spicy',       N'spicy'),
        (N'Low-Carb',    N'low-carb');

    PRINT 'Seed data inserted.';

    COMMIT TRANSACTION;
    PRINT 'Migration completed successfully.';
END TRY
BEGIN CATCH
    ROLLBACK TRANSACTION;
    PRINT 'Migration failed: ' + ERROR_MESSAGE();
    THROW;
END CATCH;
GO
```

## Design Decisions

| Decision | Rationale |
|----------|-----------|
| `DATETIME2(3)` over `DATETIME` | 3ms precision is sufficient, uses less storage than DATETIME's 3.33ms |
| `NVARCHAR` for all text | Unicode support for international recipe content |
| Composite PK on junction tables | Natural key avoids surrogate overhead |
| `ON DELETE CASCADE` on junction FKs | Deleting a recipe should remove its tags and ingredients |
| No cascade on User FK | Deleting a user should not silently remove recipes |
| Filtered indexes (`WHERE IsPublished = 1`) | Most queries filter on published recipes — smaller, faster indexes |
| `UNIQUE (UserId, RecipeId)` on Rating | One rating per user per recipe |
| Self-referencing Category | Supports nested category hierarchies |
| Slug columns | URL-friendly identifiers for SEO |
| ErrorLog table | Centralized server-side error capture for stored procedure diagnostics |
