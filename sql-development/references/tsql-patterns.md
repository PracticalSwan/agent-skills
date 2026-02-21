# T-SQL Common Patterns Reference

## UPSERT with MERGE

Insert or update in a single atomic statement.

```sql
MERGE INTO dbo.Recipe AS target
USING (SELECT @RecipeId AS Id, @Title AS Title, @Description AS Description) AS source
ON target.Id = source.Id
WHEN MATCHED THEN
    UPDATE SET
        Title = source.Title,
        Description = source.Description,
        UpdatedAt = GETUTCDATE()
WHEN NOT MATCHED THEN
    INSERT (Id, Title, Description, CreatedAt)
    VALUES (source.Id, source.Title, source.Description, GETUTCDATE())
OUTPUT $action, inserted.Id;
```

## Pagination with OFFSET FETCH

Standard keyset-free pagination for sorted results.

```sql
SELECT r.Id, r.Title, r.CreatedAt
FROM dbo.Recipe r
WHERE r.IsPublished = 1
ORDER BY r.CreatedAt DESC
OFFSET @PageSize * (@PageNumber - 1) ROWS
FETCH NEXT @PageSize ROWS ONLY;
```

**With total count** (single query):

```sql
SELECT
    r.Id, r.Title, r.CreatedAt,
    COUNT(*) OVER() AS TotalCount
FROM dbo.Recipe r
WHERE r.IsPublished = 1
ORDER BY r.CreatedAt DESC
OFFSET @PageSize * (@PageNumber - 1) ROWS
FETCH NEXT @PageSize ROWS ONLY;
```

## CTE Patterns

### Simple CTE for Readability

```sql
WITH ActiveUsers AS (
    SELECT Id, UserName, Email
    FROM dbo.[User]
    WHERE IsActive = 1 AND LastLoginDate > DATEADD(DAY, -30, GETUTCDATE())
)
SELECT au.UserName, COUNT(r.Id) AS RecipeCount
FROM ActiveUsers au
JOIN dbo.Recipe r ON r.AuthorId = au.Id
GROUP BY au.UserName;
```

### Recursive CTE for Hierarchies

```sql
WITH CategoryTree AS (
    -- Anchor: top-level categories
    SELECT Id, Name, ParentId, 0 AS Level, CAST(Name AS NVARCHAR(500)) AS Path
    FROM dbo.Category
    WHERE ParentId IS NULL

    UNION ALL

    -- Recursive: child categories
    SELECT c.Id, c.Name, c.ParentId, ct.Level + 1,
           CAST(ct.Path + ' > ' + c.Name AS NVARCHAR(500))
    FROM dbo.Category c
    JOIN CategoryTree ct ON c.ParentId = ct.Id
    WHERE ct.Level < 10  -- safety limit
)
SELECT Id, Name, Level, Path
FROM CategoryTree
ORDER BY Path;
```

### Windowed Aggregation CTE

```sql
WITH MonthlyStats AS (
    SELECT
        YEAR(CreatedAt) AS Yr,
        MONTH(CreatedAt) AS Mo,
        COUNT(*) AS RecipeCount,
        SUM(COUNT(*)) OVER (ORDER BY YEAR(CreatedAt), MONTH(CreatedAt)) AS RunningTotal
    FROM dbo.Recipe
    GROUP BY YEAR(CreatedAt), MONTH(CreatedAt)
)
SELECT Yr, Mo, RecipeCount, RunningTotal
FROM MonthlyStats
ORDER BY Yr, Mo;
```

## PIVOT / UNPIVOT

### PIVOT — Rows to Columns

```sql
SELECT UserId, [1] AS Jan, [2] AS Feb, [3] AS Mar, [4] AS Apr
FROM (
    SELECT AuthorId AS UserId, MONTH(CreatedAt) AS Mo, Id
    FROM dbo.Recipe
    WHERE YEAR(CreatedAt) = 2026
) src
PIVOT (
    COUNT(Id) FOR Mo IN ([1], [2], [3], [4])
) pvt;
```

### UNPIVOT — Columns to Rows

```sql
SELECT UserId, MonthName, RecipeCount
FROM (
    SELECT UserId, Jan, Feb, Mar, Apr
    FROM dbo.MonthlyRecipeSummary
) src
UNPIVOT (
    RecipeCount FOR MonthName IN (Jan, Feb, Mar, Apr)
) unpvt;
```

## Dynamic SQL with sp_executesql

Safe parameterized dynamic SQL.

```sql
DECLARE @SQL NVARCHAR(MAX);
DECLARE @Params NVARCHAR(500);
DECLARE @WhereClause NVARCHAR(MAX) = N'WHERE 1=1';

IF @CategoryId IS NOT NULL
    SET @WhereClause += N' AND r.CategoryId = @pCategoryId';

IF @SearchTerm IS NOT NULL
    SET @WhereClause += N' AND r.Title LIKE @pSearchTerm';

SET @SQL = N'
    SELECT r.Id, r.Title, r.CreatedAt
    FROM dbo.Recipe r
    ' + @WhereClause + N'
    ORDER BY r.CreatedAt DESC
    OFFSET @pOffset ROWS FETCH NEXT @pPageSize ROWS ONLY';

SET @Params = N'@pCategoryId INT, @pSearchTerm NVARCHAR(200), @pOffset INT, @pPageSize INT';

EXEC sp_executesql @SQL, @Params,
    @pCategoryId = @CategoryId,
    @pSearchTerm = @SearchTerm,
    @pOffset = @Offset,
    @pPageSize = @PageSize;
```

## TRY/CATCH Error Handling

```sql
BEGIN TRY
    BEGIN TRANSACTION;

    INSERT INTO dbo.Recipe (Title, AuthorId, CategoryId, CreatedAt)
    VALUES (@Title, @AuthorId, @CategoryId, GETUTCDATE());

    DECLARE @NewId INT = SCOPE_IDENTITY();

    INSERT INTO dbo.RecipeTag (RecipeId, TagId)
    SELECT @NewId, t.Id
    FROM dbo.Tag t
    WHERE t.Name IN (SELECT value FROM STRING_SPLIT(@Tags, ','));

    COMMIT TRANSACTION;
END TRY
BEGIN CATCH
    IF @@TRANCOUNT > 0
        ROLLBACK TRANSACTION;

    DECLARE @ErrorMessage NVARCHAR(4000) = ERROR_MESSAGE();
    DECLARE @ErrorSeverity INT = ERROR_SEVERITY();
    DECLARE @ErrorState INT = ERROR_STATE();
    DECLARE @ErrorLine INT = ERROR_LINE();
    DECLARE @ErrorProc NVARCHAR(200) = ERROR_PROCEDURE();

    INSERT INTO dbo.ErrorLog (Message, Severity, State, Line, Procedure, LogDate)
    VALUES (@ErrorMessage, @ErrorSeverity, @ErrorState, @ErrorLine, @ErrorProc, GETUTCDATE());

    THROW;
END CATCH;
```

## Table-Valued Parameters

### Define the Type

```sql
CREATE TYPE dbo.IngredientTableType AS TABLE (
    Name        NVARCHAR(200)   NOT NULL,
    Quantity    DECIMAL(10, 2)  NOT NULL,
    Unit        NVARCHAR(50)    NOT NULL
);
```

### Use in a Stored Procedure

```sql
CREATE PROCEDURE dbo.usp_Recipe_AddIngredients
    @RecipeId INT,
    @Ingredients dbo.IngredientTableType READONLY
AS
BEGIN
    INSERT INTO dbo.RecipeIngredient (RecipeId, IngredientId, Quantity, Unit)
    SELECT @RecipeId, i.Id, tvp.Quantity, tvp.Unit
    FROM @Ingredients tvp
    JOIN dbo.Ingredient i ON i.Name = tvp.Name;
END;
```

## Temporal Tables

### Create with System Versioning

```sql
CREATE TABLE dbo.Recipe (
    Id              INT IDENTITY(1,1) PRIMARY KEY,
    Title           NVARCHAR(200) NOT NULL,
    Description     NVARCHAR(MAX),
    SysStartTime    DATETIME2 GENERATED ALWAYS AS ROW START NOT NULL,
    SysEndTime      DATETIME2 GENERATED ALWAYS AS ROW END NOT NULL,
    PERIOD FOR SYSTEM_TIME (SysStartTime, SysEndTime)
) WITH (SYSTEM_VERSIONING = ON (HISTORY_TABLE = dbo.RecipeHistory));
```

### Query Historical Data

```sql
-- State at a specific point in time
SELECT * FROM dbo.Recipe
FOR SYSTEM_TIME AS OF '2026-01-15T12:00:00';

-- All changes in a date range
SELECT * FROM dbo.Recipe
FOR SYSTEM_TIME BETWEEN '2026-01-01' AND '2026-02-01';
```

## JSON Operations

### FOR JSON — Rows to JSON

```sql
SELECT r.Id, r.Title,
    (SELECT t.Name FROM dbo.Tag t
     JOIN dbo.RecipeTag rt ON rt.TagId = t.Id
     WHERE rt.RecipeId = r.Id
     FOR JSON PATH) AS Tags
FROM dbo.Recipe r
WHERE r.Id = @RecipeId
FOR JSON PATH, WITHOUT_ARRAY_WRAPPER;
```

### OPENJSON — JSON to Rows

```sql
DECLARE @json NVARCHAR(MAX) = N'[
    {"name": "Flour", "quantity": 2.5, "unit": "cups"},
    {"name": "Sugar", "quantity": 1, "unit": "cup"}
]';

SELECT *
FROM OPENJSON(@json)
WITH (
    Name     NVARCHAR(200) '$.name',
    Quantity DECIMAL(10,2) '$.quantity',
    Unit     NVARCHAR(50)  '$.unit'
);
```

## STRING_AGG

Concatenate values from multiple rows into a single string.

```sql
SELECT
    r.Id,
    r.Title,
    STRING_AGG(t.Name, ', ') WITHIN GROUP (ORDER BY t.Name) AS Tags
FROM dbo.Recipe r
JOIN dbo.RecipeTag rt ON rt.RecipeId = r.Id
JOIN dbo.Tag t ON t.Id = rt.TagId
GROUP BY r.Id, r.Title;
```

## Window Functions

### ROW_NUMBER — Unique Sequential Ranking

```sql
SELECT
    ROW_NUMBER() OVER (PARTITION BY CategoryId ORDER BY CreatedAt DESC) AS RowNum,
    Id, Title, CategoryId
FROM dbo.Recipe;
```

### RANK and DENSE_RANK

```sql
SELECT
    RANK() OVER (ORDER BY AvgRating DESC) AS Rank,
    DENSE_RANK() OVER (ORDER BY AvgRating DESC) AS DenseRank,
    Id, Title, AvgRating
FROM dbo.Recipe;
```

### LAG and LEAD — Access Adjacent Rows

```sql
SELECT
    Id, Title, CreatedAt,
    LAG(Title, 1) OVER (ORDER BY CreatedAt) AS PreviousRecipe,
    LEAD(Title, 1) OVER (ORDER BY CreatedAt) AS NextRecipe,
    DATEDIFF(DAY,
        LAG(CreatedAt, 1) OVER (ORDER BY CreatedAt),
        CreatedAt
    ) AS DaysSincePrevious
FROM dbo.Recipe
WHERE AuthorId = @AuthorId;
```

### Running Total

```sql
SELECT
    Id, Title, CreatedAt,
    COUNT(*) OVER (ORDER BY CreatedAt ROWS UNBOUNDED PRECEDING) AS RunningCount,
    SUM(ViewCount) OVER (ORDER BY CreatedAt ROWS UNBOUNDED PRECEDING) AS RunningViews
FROM dbo.Recipe
WHERE AuthorId = @AuthorId
ORDER BY CreatedAt;
```
