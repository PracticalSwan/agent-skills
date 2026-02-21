# MySQL Query Patterns (from MySQL 9.4 Documentation)

Excerpted from official MySQL 9.4 documentation https://dev.mysql.com/doc/refman/9.4/en/.

## SELECT JOIN optimization

When optimizing SELECT statements with joins, ensure indexes exist on join columns and foreign keys. This improves performance by allowing MySQL to use indexes instead of table scans.

```sql
SELECT t1.col1, t2.col2
FROM table1 t1
JOIN table2 t2 ON t1.id = t2.fk_id
WHERE t1.filter_col = 'value';
```

## EXPLAIN SELECT for query analysis

Use `EXPLAIN SELECT` to understand how MySQL executes your query and which indexes it uses.

```sql
EXPLAIN SELECT * FROM your_table;
```

## SHOW CREATE PROCEDURE

View the exact definition of a stored procedure.

```sql
SHOW CREATE PROCEDURE procedure_name;
```

## SHOW PROCEDURE STATUS

List all stored procedures and their status.

```sql
SHOW PROCEDURE STATUS;
```

## SHOW PROCEDURE CODE

Get the source code of a stored procedure for debugging or documentation.

```sql
SHOW PROCEDURE CODE FOR 'procedure_name';
```

## ALTER VIEW

Modify an existing view's SELECT statement.

```sql
ALTER VIEW view_name AS
    new_select_statement;
```

## Stored procedure with conditional logic

```sql
IF name IS NULL then
  CALL p1();
ELSE
  CALL p2();
END IF;
```

## UPDATE view with join

```sql
UPDATE vjoin SET c=c+1;
```

## Source

- MySQL 9.4 Reference: https://dev.mysql.com/doc/refman/9.4/en/
- SELECT optimization: https://dev.mysql.com/doc/refman/9.4/en/select-optimization
- Stored programs: https://dev.mysql.com/doc/refman/9.4/en/stored-programs-defining.html
