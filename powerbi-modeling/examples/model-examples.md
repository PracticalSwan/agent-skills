# Power BI Modeling Examples

## Example 1: Creating a Star Schema

When designing a new data model from scratch:

```python
# Step 1: Connect to the model
connection_operations(operation="Connect")

# Step 2: Create dimension table (Customers)
table_operations(
    operation="Create",
    name="Customer",
    columns=[
        {"name": "CustomerKey", "dataType": "Int64"},
        {"name": "FirstName", "dataType": "String"},
        {"name": "LastName", "dataType": "String"},
        {"name": "Email", "dataType": "String"},
        {"name": "City", "dataType": "String"},
        {"name": "Country", "dataType": "String"}
    ]
)

# Step 3: Create fact table (Sales)
table_operations(
    operation="Create",
    name="Sales",
    columns=[
        {"name": "SalesKey", "dataType": "Int64"},
        {"name": "CustomerKey", "dataType": "Int64"},
        {"name": "ProductKey", "dataType": "Int64"},
        {"name": "DateKey", "dataType": "Int64"},
        {"name": "Quantity", "dataType": "Int64"},
        {"name": "Amount", "dataType": "Decimal"},
        {"name": "Profit", "dataType": "Decimal"}
    ]
)

# Step 4: Create relationship (one-to-many, single direction)
relationship_operations(
    operation="Create",
    definitions=[{
        "fromTable": "Customer",
        "fromColumn": "CustomerKey",
        "toTable": "Sales",
        "toColumn": "CustomerKey",
        "crossFilteringBehavior": "OneDirection"
    }]
)
```

## Example 2: Adding DAX Measures

When adding business calculations to a model:

```python
# Add basic sum measure
measure_operations(
    operation="Create",
    definitions=[{
        "name": "Total Sales",
        "tableName": "Sales",
        "expression": "SUM(Sales[Amount])",
        "formatString": "$#,##0",
        "description": "Sum of all sales amounts"
    }]
)

# Add year-to-date measure
measure_operations(
    operation="Create",
    definitions=[{
        "name": "Total Sales YTD",
        "tableName": "Sales",
        "expression": "CALCULATE([Total Sales], DATESYTD('Date'[Date]))",
        "formatString": "$#,##0",
        "description": "Year-to-date sales"
    }]
)

# Add YoY growth measure
measure_operations(
    operation="Create",
    definitions=[{
        "name": "Sales YoY Growth %",
        "tableName": "Sales",
        "expression": "DIVIDE([Total Sales] - CALCULATE([Total Sales], SAMEPERIODLASTYEAR('Date'[Date])), CALCULATE([Total Sales], SAMEPERIODLASTYEAR('Date'[Date])))",
        "formatString": "0.00%",
        "description": "Year-over-year sales growth percentage"
    }]
)
```

## Example 3: Documenting a Model

When adding documentation to improve model usability:

```python
# Update table descriptions
table_operations(
    operation="Update",
    name="Customer",
    description="Customer dimension containing demographic and geographic information"
)

# Update column descriptions
column_operations(
    operation="Update",
    definitions=[{
        "tableName": "Customer",
        "name": "CustomerKey",
        "description": "Unique identifier for customer (surrogate key)",
        "isHidden": True
    }, {
        "tableName": "Customer",
        "name": "Email",
        "description": "Primary email address for customer communications"
    }]
)

# Update measure descriptions
measure_operations(
    operation="Update",
    definitions=[{
        "name": "Total Sales",
        "tableName": "Sales",
        "description": "Total revenue from all completed sales transactions"
    }]
)
```

## Example 4: Implementing Row-Level Security

When adding security roles to restrict data access:

```python
# Create sales manager role
security_role_operations(
    operation="Create",
    name="Sales Manager",
    # Restricts to their region's customers
    modelRole=[{
        "tableName": "Sales",
        "filterExpression": "USERNAME() = [ManagerEmail]"
    }]
)

# Create executive role (all data)
security_role_operations(
    operation="Create",
    name="Executive",
    modelRole=[{
        "tableName": "Sales",
        "filterExpression": "TRUE()"  # No filtering
    }]
)
```

## Example 5: Optimizing Model Performance

When improving performance of existing measures:

```python
# Before: Inefficient measure scanning entire table
measure_operations(
    operation="Update",
    definitions=[{
        "name": "Total Sales",
        "tableName": "Sales",
        "expression": "SUM(Sales[Amount])  # Scans all rows"
    }]
)

# After: Optimized with DIVIDE and error handling
measure_operations(
    operation="Update",
    definitions=[{
        "name": "Total Sales",
        "tableName": "Sales",
        "expression": "SUMX(RELATEDTABLE('Customer'), CALCULATE(SUM(Sales[Amount])))",
        "description": "Optimized: Uses SUMX with filtered context for better performance"
    }]
)

# Add hidden technical measures for calculations
measure_operations(
    operation="Create",
    definitions=[{
        "name": "_Total Sales Base",
        "tableName": "Sales",
        "expression": "SUM(Sales[Amount])",
        "isHidden": True,
        "description": "Base calculation used by other measures"
    }]
)
```
