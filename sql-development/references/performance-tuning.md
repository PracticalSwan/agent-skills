# SQL Server Performance Tuning Guide

## Execution Plan Reading

### Requesting Plans

```sql
-- Estimated plan (no execution)
SET SHOWPLAN_XML ON;
GO
SELECT ... FROM dbo.Recipe WHERE ...;
GO
SET SHOWPLAN_XML OFF;

-- Actual plan (with execution)
SET STATISTICS XML ON;
SELECT ... FROM dbo.Recipe WHERE ...;
SET STATISTICS XML OFF;
```

### Key Operators to Watch

| Operator | Meaning | Action |
|----------|---------|--------|
| **Table Scan** | Full table read, no useful index | Add appropriate index |
| **Clustered Index Scan** | Full scan of clustered index | Consider covering index or filter |
| **Index Seek** | Targeted index lookup | Good — this is the goal |
| **Key Lookup** | Extra lookup to clustered index for non-covered columns | Add INCLUDE columns to index |
| **Hash Match** | Hash-based join (memory-intensive) | Check join predicates and statistics |
| **Nested Loops** | Good for small outer sets | Verify outer set is actually small |
| **Sort** | Explicit sort operation | Check if an index can provide order |
| **Spool (Eager/Lazy)** | Materializes intermediate results | May indicate missing index |
| **Parallelism** | Query using multiple threads | Fine for large queries, problematic for OLTP |

### Cost Analysis

- **Estimated vs Actual Rows**: Large discrepancy signals stale statistics
- **Estimated Subtree Cost**: Relative cost within the plan (not wall-clock time)
- **Actual Executions**: How many times an operator ran (watch for nested loop inflation)
- **Memory Grant**: Check for excessive grants or spills to tempdb

## Index Tuning

### Missing Index DMVs

```sql
SELECT
    CONVERT(DECIMAL(18,2), migs.avg_total_user_cost * migs.avg_user_impact *
        (migs.user_seeks + migs.user_scans)) AS ImprovementScore,
    mid.statement AS TableName,
    mid.equality_columns,
    mid.inequality_columns,
    mid.included_columns,
    migs.user_seeks,
    migs.user_scans
FROM sys.dm_db_missing_index_group_stats migs
JOIN sys.dm_db_missing_index_groups mig ON migs.group_handle = mig.index_group_handle
JOIN sys.dm_db_missing_index_details mid ON mig.index_handle = mid.index_handle
WHERE mid.database_id = DB_ID()
ORDER BY ImprovementScore DESC;
```

### Index Usage Statistics

Find unused indexes consuming write overhead.

```sql
SELECT
    OBJECT_NAME(ius.object_id) AS TableName,
    i.name AS IndexName,
    i.type_desc,
    ius.user_seeks,
    ius.user_scans,
    ius.user_lookups,
    ius.user_updates,
    ius.last_user_seek,
    ius.last_user_scan
FROM sys.dm_db_index_usage_stats ius
JOIN sys.indexes i ON i.object_id = ius.object_id AND i.index_id = ius.index_id
WHERE ius.database_id = DB_ID()
    AND OBJECTPROPERTY(ius.object_id, 'IsUserTable') = 1
ORDER BY ius.user_seeks + ius.user_scans + ius.user_lookups ASC;
```

### Index Fragmentation

```sql
SELECT
    OBJECT_NAME(ips.object_id) AS TableName,
    i.name AS IndexName,
    ips.avg_fragmentation_in_percent,
    ips.page_count,
    ips.avg_page_space_used_in_percent
FROM sys.dm_db_index_physical_stats(DB_ID(), NULL, NULL, NULL, 'LIMITED') ips
JOIN sys.indexes i ON i.object_id = ips.object_id AND i.index_id = ips.index_id
WHERE ips.avg_fragmentation_in_percent > 10
    AND ips.page_count > 1000
ORDER BY ips.avg_fragmentation_in_percent DESC;
```

**Maintenance thresholds**:
- 10-30% fragmentation → `ALTER INDEX REORGANIZE`
- \>30% fragmentation → `ALTER INDEX REBUILD`
- <1000 pages → fragmentation is irrelevant

## Query Optimization

### Parameter Sniffing

**Problem**: First execution compiles a plan optimized for initial parameter values; subsequent calls with different data distributions get a suboptimal plan.

**Solutions**:

```sql
-- Option 1: OPTIMIZE FOR UNKNOWN
SELECT * FROM dbo.Recipe
WHERE CategoryId = @CategoryId
OPTION (OPTIMIZE FOR (@CategoryId UNKNOWN));

-- Option 2: RECOMPILE for volatile parameters
SELECT * FROM dbo.Recipe
WHERE CreatedAt > @StartDate
OPTION (RECOMPILE);

-- Option 3: Local variable assignment (breaks sniffing)
DECLARE @LocalCategoryId INT = @CategoryId;
SELECT * FROM dbo.Recipe
WHERE CategoryId = @LocalCategoryId;
```

### Statistics Management

```sql
-- Check statistics freshness
SELECT
    OBJECT_NAME(s.object_id) AS TableName,
    s.name AS StatName,
    sp.last_updated,
    sp.rows,
    sp.rows_sampled,
    sp.modification_counter
FROM sys.stats s
CROSS APPLY sys.dm_db_stats_properties(s.object_id, s.stats_id) sp
WHERE s.object_id = OBJECT_ID('dbo.Recipe')
ORDER BY sp.last_updated;

-- Manual update with full scan
UPDATE STATISTICS dbo.Recipe WITH FULLSCAN;

-- Update specific statistic
UPDATE STATISTICS dbo.Recipe IX_Recipe_CategoryId WITH FULLSCAN;
```

### Cardinality Estimation

When the optimizer misestimates row counts:

```sql
-- Force legacy CE for a specific query
SELECT * FROM dbo.Recipe
WHERE CategoryId = @Id AND IsPublished = 1
OPTION (USE HINT('FORCE_LEGACY_CARDINALITY_ESTIMATION'));

-- Check CE version in use
SELECT name, value
FROM sys.database_scoped_configurations
WHERE name = 'LEGACY_CARDINALITY_ESTIMATION';
```

## Wait Statistics Analysis

### Top Waits

```sql
WITH WaitStats AS (
    SELECT
        wait_type,
        wait_time_ms / 1000.0 AS wait_time_sec,
        signal_wait_time_ms / 1000.0 AS signal_wait_sec,
        (wait_time_ms - signal_wait_time_ms) / 1000.0 AS resource_wait_sec,
        waiting_tasks_count,
        100.0 * wait_time_ms / SUM(wait_time_ms) OVER() AS pct
    FROM sys.dm_os_wait_stats
    WHERE wait_type NOT IN (
        'CLR_SEMAPHORE','LAZYWRITER_SLEEP','RESOURCE_QUEUE',
        'SLEEP_TASK','SLEEP_SYSTEMTASK','SQLTRACE_BUFFER_FLUSH',
        'WAITFOR','LOGMGR_QUEUE','CHECKPOINT_QUEUE',
        'REQUEST_FOR_DEADLOCK_SEARCH','XE_TIMER_EVENT',
        'BROKER_TO_FLUSH','BROKER_TASK_STOP','CLR_MANUAL_EVENT',
        'DISPATCHER_QUEUE_SEMAPHORE','FT_IFTS_SCHEDULER_IDLE_WAIT',
        'XE_DISPATCHER_WAIT','HADR_FILESTREAM_IOMGR_IOCOMPLETION'
    )
)
SELECT TOP 20
    wait_type,
    wait_time_sec,
    resource_wait_sec,
    signal_wait_sec,
    waiting_tasks_count,
    CAST(pct AS DECIMAL(5,2)) AS pct
FROM WaitStats
ORDER BY wait_time_sec DESC;
```

### Common Wait Types and Actions

| Wait Type | Cause | Fix |
|-----------|-------|-----|
| `CXPACKET` / `CXCONSUMER` | Parallelism skew | Check MAXDOP, cost threshold |
| `PAGEIOLATCH_*` | Disk I/O waits | Add memory, faster storage, better indexes |
| `SOS_SCHEDULER_YIELD` | CPU pressure | Optimize queries, add CPU |
| `LCK_M_*` | Lock contention | Reduce transaction scope, add indexes |
| `WRITELOG` | Transaction log writes | Faster log disk, batch commits |
| `ASYNC_NETWORK_IO` | Client not consuming results fast enough | Check application code |

## TempDB Optimization

```sql
-- Check tempdb contention
SELECT
    session_id, wait_type, wait_duration_ms, resource_description
FROM sys.dm_os_waiting_tasks
WHERE wait_type LIKE 'PAGELATCH%'
    AND resource_description LIKE '2:%';  -- database_id 2 = tempdb

-- Best practices:
-- 1. Multiple data files (1 per logical CPU, up to 8)
-- 2. Equal size for proportional fill
-- 3. Trace flag 1118 (SQL 2014 and earlier) for uniform extent allocation
-- 4. Pre-size files to avoid auto-growth during load
```

## Memory Pressure Indicators

```sql
-- Buffer pool usage
SELECT
    (total_physical_memory_kb / 1024) AS TotalPhysicalMemoryMB,
    (available_physical_memory_kb / 1024) AS AvailableMemoryMB,
    (total_page_file_kb / 1024) AS TotalPageFileMB,
    (available_page_file_kb / 1024) AS AvailablePageFileMB,
    system_memory_state_desc
FROM sys.dm_os_sys_memory;

-- Page life expectancy (higher is better, <300 is concerning)
SELECT
    object_name, counter_name, cntr_value AS PageLifeExpectancy
FROM sys.dm_os_performance_counters
WHERE counter_name = 'Page life expectancy'
    AND object_name LIKE '%Buffer Manager%';

-- Memory grants pending
SELECT
    object_name, counter_name, cntr_value
FROM sys.dm_os_performance_counters
WHERE counter_name = 'Memory Grants Pending';
```

## Query Store

### Enable and Configure

```sql
ALTER DATABASE [RecipeDB] SET QUERY_STORE = ON (
    OPERATION_MODE = READ_WRITE,
    DATA_FLUSH_INTERVAL_SECONDS = 900,
    INTERVAL_LENGTH_MINUTES = 30,
    MAX_STORAGE_SIZE_MB = 1024,
    QUERY_CAPTURE_MODE = AUTO,
    SIZE_BASED_CLEANUP_MODE = AUTO,
    MAX_PLANS_PER_QUERY = 200
);
```

### Find Regressed Queries

```sql
SELECT TOP 20
    qsq.query_id,
    qsp.plan_id,
    qsqt.query_sql_text,
    rs.avg_duration / 1000.0 AS avg_duration_ms,
    rs.avg_cpu_time / 1000.0 AS avg_cpu_ms,
    rs.avg_logical_io_reads,
    rs.count_executions,
    qsp.is_forced_plan
FROM sys.query_store_query qsq
JOIN sys.query_store_query_text qsqt ON qsq.query_text_id = qsqt.query_text_id
JOIN sys.query_store_plan qsp ON qsq.query_id = qsp.query_id
JOIN sys.query_store_runtime_stats rs ON qsp.plan_id = rs.plan_id
JOIN sys.query_store_runtime_stats_interval rsi ON rs.runtime_stats_interval_id = rsi.runtime_stats_interval_id
WHERE rsi.start_time > DATEADD(HOUR, -24, GETUTCDATE())
ORDER BY rs.avg_duration DESC;
```

### Force a Known-Good Plan

```sql
EXEC sp_query_store_force_plan @query_id = 42, @plan_id = 7;
```

## Common Anti-Patterns and Fixes

| Anti-Pattern | Problem | Fix |
|---|---|---|
| `SELECT *` | Returns unnecessary data, blocks covering indexes | List only needed columns |
| Functions on indexed columns (`WHERE YEAR(Date) = 2026`) | Prevents index seek | Use range: `WHERE Date >= '2026-01-01' AND Date < '2027-01-01'` |
| Implicit conversions | Type mismatch prevents seek | Match parameter types to column types |
| Cursor loops for set operations | Row-by-row processing | Rewrite as set-based query |
| `NOLOCK` everywhere | Dirty reads, incorrect results | Use `READ COMMITTED SNAPSHOT` instead |
| Missing `SET NOCOUNT ON` | Extra round trips for row counts | Always set in stored procedures |
| Large transactions | Lock escalation, long rollbacks | Keep transactions short and focused |
| `OR` in WHERE with different columns | Often causes scans | Rewrite as `UNION ALL` of two seeks |
