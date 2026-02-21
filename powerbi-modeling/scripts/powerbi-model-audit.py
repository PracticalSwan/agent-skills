"""
Power BI Model Audit Script

This script audits a Power BI semantic model for best practices violations
and provides recommendations for improvement.

Prerequisites: Power BI Modeling MCP Server must be running

Usage: python scripts/powerbi-model-audit.py
"""

from typing import Dict, List, Any


class ModelAuditor:
    """Audits Power BI semantic models against best practices."""

    def __init__(self):
        self.issues = []
        self.warnings = []
        self.passed = []

    def audit_model(self, model_data: Dict[str, Any]) -> Dict[str, List[str]]:
        """
        Perform comprehensive model audit.

        Args:
            model_data: Model data from Power BI MCP operations

        Returns:
            Dictionary with issues, warnings, and passed checks
        """
        self._audit_tables(model_data.get('tables', []))
        self._audit_relationships(model_data.get('relationships', []))
        self._audit_measures(model_data.get('measures', []))

        return {
            'issues': self.issues,
            'warnings': self.warnings,
            'passed': self.passed
        }

    def _audit_tables(self, tables: List[Dict]):
        """Audit table structure and documentation."""
        if not tables:
            self.issues.append("No tables found in model")
            return

        dimension_count = 0
        fact_count = 0

        for table in tables:
            # Check for table description
            if not table.get('description'):
                self.warnings.append(f"Table '{table['name']}' is missing description")

            # Check if marked as dimension or fact
            if table.get('isHidden'):
                self.passed.append(f"Table '{table['name']}' is hidden (appropriate for technical tables)")

            # Check for hidden technical keys
            for column in table.get('columns', []):
                if 'Key' in column['name'] and not column.get('isHidden'):
                    self.warnings.append(f"Technical key '{column['name']}' in '{table['name']}' should be hidden")

    def _audit_relationships(self, relationships: List[Dict]):
        """Audit relationship configuration."""
        if not relationships:
            self.issues.append("No relationships found - model may not be properly connected")
            return

        bidirectional_count = 0

        for rel in relationships:
            # Check for bidirectional filters
            if rel.get('crossFilteringBehavior') == 'BothDirections':
                bidirectional_count += 1
                self.warnings.append(
                    f"Relationship '{rel['fromTable']}.{rel['fromColumn']}' → "
                    f"'{rel['toTable']}.{rel['toColumn']}' uses bidirectional filtering"
                )

            # Check for many-to-many relationships
            if rel.get('fromCardinality') == 'many' and rel.get('toCardinality') == 'many':
                self.issues.append(
                    f"Many-to-many relationship between '{rel['fromTable']}' and '{rel['toTable']}' "
                    "should be avoided - use bridging table instead"
                )

            # Check for active relationships
            if not rel.get('isActive'):
                self.warnings.append(
                    f"Relationship '{rel['fromTable']}' → '{rel['toTable']}' is inactive"
                )

        if bidirectional_count > 2:
            self.issues.append(
                f"Found {bidirectional_count} bidirectional relationships. "
                "Limit to 1-2 for performance."
            )

    def _audit_measures(self, measures: List[Dict]):
        """Audit measure definitions."""
        if not measures:
            self.warnings.append("No measures found in model")
            return

        for measure in measures:
            # Check for measure description
            if not measure.get('description'):
                self.warnings.append(f"Measure '{measure['name']}' in '{measure['tableName']}' is missing description")

            # Check for format string
            if not measure.get('formatString'):
                self.warnings.append(f"Measure '{measure['name']}' has no format string")

            # Check for common anti-patterns
            expression = measure.get('expression', '')
            if 'CALCULATE' not in expression and 'SUM' in expression and '*' in expression:
                self.issues.append(
                    f"Measure '{measure['name']}' may have calculation issues - "
                    "use CALCULATE with proper filter context"
                )


def print_audit_report(audit_results: Dict[str, List[str]]):
    """Print formatted audit report."""
    print("=" * 80)
    print("POWER BI MODEL AUDIT REPORT")
    print("=" * 80)

    print("\n✓ PASSED CHECKS:")
    for item in audit_results['passed']:
        print(f"  ✓ {item}")

    if not audit_results['passed']:
        print("  None")

    print("\n⚠ WARNINGS:")
    for item in audit_results['warnings']:
        print(f"  ⚠ {item}")

    if not audit_results['warnings']:
        print("  None")

    print("\n✗ ISSUES:")
    for item in audit_results['issues']:
        print(f"  ✗ {item}")

    if not audit_results['issues']:
        print("  None")

    print("\n" + "=" * 80)
    print(f"Total: {len(audit_results['passed'])} passed, {len(audit_results['warnings'])} warnings, {len(audit_results['issues'])} issues")
    print("=" * 80)


# MCP Integration Example
def audit_via_mcp():
    """
    Example of using this with Power BI MCP tools.

    In actual usage, you would call MCP operations to get model data:
    - model_operations(operation="Get")
    - table_operations(operation="List")
    - measure_operations(operation="List")
    - relationship_operations(operation="List")
    """
    auditor = ModelAuditor()

    # Mock data for demonstration
    mock_model_data = {
        'tables': [
            {
                'name': 'Sales',
                'description': 'Sales transactions',
                'columns': [
                    {'name': 'SalesKey', 'isHidden': True},
                    {'name': 'Amount', 'isHidden': False}
                ]
            }
        ],
        'relationships': [
            {
                'fromTable': 'Customer',
                'toTable': 'Sales',
                'crossFilteringBehavior': 'OneDirection',
                'isActive': True
            }
        ],
        'measures': [
            {
                'name': 'Total Sales',
                'tableName': 'Sales',
                'expression': 'SUM(Sales[Amount])',
                'formatString': '$#,##0',
                'description': 'Total sales amount'
            }
        ]
    }

    results = auditor.audit_model(mock_model_data)
    print_audit_report(results)


if __name__ == '__main__':
    audit_via_mcp()
