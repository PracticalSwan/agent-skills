-- ============================================================================
-- Stored Procedure Template
-- ============================================================================
-- Description : [Brief description of what this procedure does]
-- Parameters  : @Id          INT           - Record identifier (NULL for insert)
--               @Title       NVARCHAR(200) - Record title
--               @PageNumber  INT           - Page number for pagination (default 1)
--               @PageSize    INT           - Page size for pagination (default 20)
--               @SortColumn  NVARCHAR(50)  - Column to sort by
--               @SortDir     NVARCHAR(4)   - Sort direction (ASC/DESC)
-- Returns     : @StatusCode  INT           - 0 = Success, 1 = Validation Error,
--                                            2 = Not Found, -1 = System Error
--               @StatusMsg   NVARCHAR(500) - Human-readable status message
--               @TotalCount  INT           - Total matching records (for pagination)
-- ============================================================================
-- Changelog:
--   2026-02-11  [Author]  Initial creation
--   YYYY-MM-DD  [Author]  [Change description]
-- ============================================================================

CREATE OR ALTER PROCEDURE dbo.usp_Entity_Operation
    -- Input parameters
    @Id             INT             = NULL,
    @Title          NVARCHAR(200)   = NULL,
    @Description    NVARCHAR(MAX)   = NULL,
    @CategoryId     INT             = NULL,
    @IsActive       BIT             = 1,

    -- Pagination parameters
    @PageNumber     INT             = 1,
    @PageSize       INT             = 20,

    -- Sorting parameters
    @SortColumn     NVARCHAR(50)    = N'CreatedAt',
    @SortDir        NVARCHAR(4)     = N'DESC',

    -- Output parameters
    @StatusCode     INT             = 0     OUTPUT,
    @StatusMsg      NVARCHAR(500)   = N''   OUTPUT,
    @TotalCount     INT             = 0     OUTPUT
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;

    -- ========================================================================
    -- Parameter Validation
    -- ========================================================================

    IF @PageNumber < 1 SET @PageNumber = 1;
    IF @PageSize < 1 OR @PageSize > 100 SET @PageSize = 20;

    IF @SortDir NOT IN (N'ASC', N'DESC')
        SET @SortDir = N'DESC';

    IF @SortColumn NOT IN (N'CreatedAt', N'Title', N'Id', N'UpdatedAt')
    BEGIN
        SET @StatusCode = 1;
        SET @StatusMsg = N'Invalid sort column. Allowed: CreatedAt, Title, Id, UpdatedAt.';
        RETURN;
    END;

    IF @Title IS NOT NULL AND LEN(TRIM(@Title)) = 0
    BEGIN
        SET @StatusCode = 1;
        SET @StatusMsg = N'Title cannot be empty when provided.';
        RETURN;
    END;

    IF @Title IS NOT NULL AND LEN(@Title) > 200
    BEGIN
        SET @StatusCode = 1;
        SET @StatusMsg = N'Title cannot exceed 200 characters.';
        RETURN;
    END;

    -- ========================================================================
    -- Main Logic
    -- ========================================================================

    BEGIN TRY
        BEGIN TRANSACTION;

        -- ====================================================================
        -- INSERT (when @Id is NULL)
        -- ====================================================================
        IF @Id IS NULL
        BEGIN
            IF @Title IS NULL
            BEGIN
                SET @StatusCode = 1;
                SET @StatusMsg = N'Title is required for insert.';
                ROLLBACK TRANSACTION;
                RETURN;
            END;

            INSERT INTO dbo.Entity (Title, Description, CategoryId, IsActive, CreatedAt, UpdatedAt)
            VALUES (@Title, @Description, @CategoryId, @IsActive, GETUTCDATE(), GETUTCDATE());

            SET @Id = SCOPE_IDENTITY();
            SET @StatusCode = 0;
            SET @StatusMsg = N'Record created successfully. Id: ' + CAST(@Id AS NVARCHAR(20));
        END

        -- ====================================================================
        -- UPDATE (when @Id is provided)
        -- ====================================================================
        ELSE
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM dbo.Entity WHERE Id = @Id)
            BEGIN
                SET @StatusCode = 2;
                SET @StatusMsg = N'Record not found with Id: ' + CAST(@Id AS NVARCHAR(20));
                ROLLBACK TRANSACTION;
                RETURN;
            END;

            UPDATE dbo.Entity
            SET
                Title       = ISNULL(@Title, Title),
                Description = ISNULL(@Description, Description),
                CategoryId  = ISNULL(@CategoryId, CategoryId),
                IsActive    = @IsActive,
                UpdatedAt   = GETUTCDATE()
            WHERE Id = @Id;

            SET @StatusCode = 0;
            SET @StatusMsg = N'Record updated successfully. Id: ' + CAST(@Id AS NVARCHAR(20));
        END;

        COMMIT TRANSACTION;

        -- ====================================================================
        -- Return the affected record
        -- ====================================================================
        SELECT Id, Title, Description, CategoryId, IsActive, CreatedAt, UpdatedAt
        FROM dbo.Entity
        WHERE Id = @Id;

    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0
            ROLLBACK TRANSACTION;

        SET @StatusCode = -1;
        SET @StatusMsg = N'Error: ' + ERROR_MESSAGE();

        -- Log the error for diagnostics
        INSERT INTO dbo.ErrorLog (
            ErrorNumber, ErrorSeverity, ErrorState, ErrorLine,
            ErrorProcedure, ErrorMessage, LogDate
        )
        VALUES (
            ERROR_NUMBER(), ERROR_SEVERITY(), ERROR_STATE(), ERROR_LINE(),
            ERROR_PROCEDURE(), ERROR_MESSAGE(), GETUTCDATE()
        );
    END CATCH;
END;
GO

-- ============================================================================
-- Companion: Paginated List Procedure
-- ============================================================================

CREATE OR ALTER PROCEDURE dbo.usp_Entity_List
    @SearchTerm     NVARCHAR(200)   = NULL,
    @CategoryId     INT             = NULL,
    @IsActive       BIT             = NULL,
    @PageNumber     INT             = 1,
    @PageSize       INT             = 20,
    @SortColumn     NVARCHAR(50)    = N'CreatedAt',
    @SortDir        NVARCHAR(4)     = N'DESC',
    @TotalCount     INT             = 0     OUTPUT
AS
BEGIN
    SET NOCOUNT ON;

    IF @PageNumber < 1 SET @PageNumber = 1;
    IF @PageSize < 1 OR @PageSize > 100 SET @PageSize = 20;
    IF @SortDir NOT IN (N'ASC', N'DESC') SET @SortDir = N'DESC';
    IF @SortColumn NOT IN (N'CreatedAt', N'Title', N'Id') SET @SortColumn = N'CreatedAt';

    -- Get total count
    SELECT @TotalCount = COUNT(*)
    FROM dbo.Entity
    WHERE (@SearchTerm IS NULL OR Title LIKE N'%' + @SearchTerm + N'%')
        AND (@CategoryId IS NULL OR CategoryId = @CategoryId)
        AND (@IsActive IS NULL OR IsActive = @IsActive);

    -- Dynamic sorting with validated column names
    DECLARE @SQL NVARCHAR(MAX);
    DECLARE @Params NVARCHAR(500);

    SET @SQL = N'
        SELECT Id, Title, Description, CategoryId, IsActive, CreatedAt, UpdatedAt
        FROM dbo.Entity
        WHERE (@pSearchTerm IS NULL OR Title LIKE N''%'' + @pSearchTerm + N''%'')
            AND (@pCategoryId IS NULL OR CategoryId = @pCategoryId)
            AND (@pIsActive IS NULL OR IsActive = @pIsActive)
        ORDER BY ' + QUOTENAME(@SortColumn) + N' ' + @SortDir + N'
        OFFSET @pOffset ROWS FETCH NEXT @pPageSize ROWS ONLY';

    SET @Params = N'@pSearchTerm NVARCHAR(200), @pCategoryId INT, @pIsActive BIT, @pOffset INT, @pPageSize INT';

    EXEC sp_executesql @SQL, @Params,
        @pSearchTerm = @SearchTerm,
        @pCategoryId = @CategoryId,
        @pIsActive = @IsActive,
        @pOffset = (@PageNumber - 1) * @PageSize,
        @pPageSize = @PageSize;
END;
GO
