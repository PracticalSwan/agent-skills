#!/usr/bin/env python3
"""
NotebookLM MCP Helper Script

Utility script for common NotebookLM MCP operations.
Provides helper functions for library management, queries, and maintenance.
"""

import json
import sys
from datetime import datetime
from typing import List, Dict, Optional


class NotebookLMHelper:
    """Helper class for NotebookLM MCP operations"""
    
    def __init__(self):
        """Initialize helper"""
        self.cached_notebooks = None
        self.cache_timestamp = None
        self.cache_ttl = 300  # 5 minutes
    
    def list_notebooks_with_details(self) -> List[Dict]:
        """
        List all notebooks with enhanced details.
        
        Returns:
            List of notebook dictionaries with full metadata
        """
        from mcp import list_notebooks
        
        # Check cache
        if (self.cached_notebooks and 
            self.cache_timestamp and 
            (datetime.now() - self.cache_timestamp).seconds < self.cache_ttl):
            print("Using cached notebook list")
            return self.cached_notebooks
        
        notebooks = list_notebooks()
        self.cached_notebooks = notebooks
        self.cache_timestamp = datetime.now()
        
        return notebooks
    
    def find_notebook_by_name(self, name: str) -> Optional[Dict]:
        """
        Find a notebook by exact name match.
        
        Args:
            name: Exact notebook name to search for
            
        Returns:
            Notebook dictionary or None if not found
        """
        notebooks = self.list_notebooks_with_details()
        
        for notebook in notebooks:
            if notebook.name.lower() == name.lower():
                return notebook
        
        return None
    
    def find_notebooks_by_topic(self, topic: str) -> List[Dict]:
        """
        Find all notebooks containing a specific topic.
        
        Args:
            topic: Topic to search for
            
        Returns:
            List of matching notebooks
        """
        notebooks = self.list_notebooks_with_details()
        
        matching = []
        topic_lower = topic.lower()
        
        for notebook in notebooks:
            if any(t.lower() == topic_lower for t in notebook.topics):
                matching.append(notebook)
        
        return matching
    
    def search_notebooks_fuzzy(self, query: str) -> List[Dict]:
        """
        Fuzzy search across name, description, and topics.
        
        Args:
            query: Search query string
            
        Returns:
            List of matching notebooks with match score
        """
        from mcp import search_notebooks
        
        # Use MCP search
        notebooks = search_notebooks(query=query)
        
        # Score matches based on name, description, topic overlap
        scored = []
        query_lower = query.lower()
        query_parts = query_lower.split()
        
        for notebook in notebooks:
            score = 0
            
            # Name match (highest weight)
            if query_lower in notebook.name.lower():
                score += 50
            
            # Topic matches
            topic_matches = sum(
                1 for t in notebook.topics 
                if any(part in t.lower() for part in query_parts)
            )
            if topic_matches > 0:
                score += 30 * topic_matches
            
            # Description matches
            desc_matches = sum(
                1 for part in query_parts 
                if part in notebook.description.lower()
            )
            if desc_matches > 0:
                score += 20 * desc_matches
            
            if score > 0:
                scored.append({
                    'notebook': notebook,
                    'score': score
                })
        
        # Sort by score (descending)
        scored.sort(key=lambda x: x['score'], reverse=True)
        
        return [item['notebook'] for item in scored]
    
    def analyze_library_quality(self) -> Dict[str, List]:
        """
        Analyze notebook library for quality issues.
        
        Returns:
            Dictionary with lists of notebook IDs by issue type
        """
        notebooks = self.list_notebooks_with_details()
        
        issues = {
            'short_descriptions': [],
            'missing_topics': [],
            'few_topics': [],
            'no_use_cases': [],
            'missing_tags': [],
            'duplicate_names': {}
        }
        
        name_to_ids = {}
        
        for notebook in notebooks:
            # Check description length
            if len(notebook.description) < 30:
                issues['short_descriptions'].append({
                    'id': notebook.id,
                    'name': notebook.name,
                    'length': len(notebook.description)
                })
            
            # Check for missing topics
            if not notebook.topics or len(notebook.topics) == 0:
                issues['missing_topics'].append({
                    'id': notebook.id,
                    'name': notebook.name
                })
            # Check for few topics
            elif len(notebook.topics) < 3:
                issues['few_topics'].append({
                    'id': notebook.id,
                    'name': notebook.name,
                    'topic_count': len(notebook.topics)
                })
            
            # Check use cases
            if not hasattr(notebook, 'use_cases') or not notebook.use_cases:
                issues['no_use_cases'].append({
                    'id': notebook.id,
                    'name': notebook.name
                })
            
            # Check tags
            if not hasattr(notebook, 'tags') or not notebook.tags:
                issues['missing_tags'].append({
                    'id': notebook.id,
                    'name': notebook.name
                })
            
            # Track duplicate names
            if notebook.name in name_to_ids:
                name_to_ids[notebook.name].append(notebook.id)
            else:
                name_to_ids[notebook.name] = [notebook.id]
        
        # Filter duplicates with more than one ID
        for name, ids in name_to_ids.items():
            if len(ids) > 1:
                issues['duplicate_names'][name] = ids
        
        return issues
    
    def generate_library_report(self) -> str:
        """
        Generate a comprehensive library report.
        
        Returns:
            Formatted report string
        """
        issues = self.analyze_library_quality()
        notebooks = self.list_notebooks_with_details()
        
        report = ["=" * 60]
        report.append("NotebookLM Library Report")
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Total Notebooks: {len(notebooks)}")
        report.append("=" * 60)
        
        # Summary
        total_issues = sum(len(v) if isinstance(v, list) else len(v) 
                        for v in issues.values())
        
        report.append(f"\n📊 Summary")
        report.append(f"   Total Issues Found: {total_issues}")
        
        # Detailed issues
        if any(issues.values()):
            report.append("\n🔍 Issues Found\n")
            
            for issue_type, affected in issues.items():
                if not affected:
                    continue
                
                if not isinstance(affected, list):
                    # Dictionary (duplicates)
                    for name, ids in affected.items():
                        report.append(f"  ⚠ Duplicate Name: '{name}'")
                        for nb_id in ids:
                            report.append(f"     - {nb_id}")
                else:
                    # List
                    type_name = issue_type.replace('_', ' ').title()
                    report.append(f"  ⚠ {type_name}: {len(affected)} notebook(s)")
                    
                    for item in affected[:5]:  # Show first 5
                        if isinstance(item, dict):
                            report.append(f"     - {item.get('name', item.get('id'))}")
                    
                    if len(affected) > 5:
                        report.append(f"     ... and {len(affected) - 5} more")
        else:
            report.append("\n✓ No issues found!")
        
        # Statistics
        report.append("\n📈 Statistics")
        report.append(f"   Avg Description Length: {sum(len(nb.description) for nb in notebooks) / len(notebooks):.1f} chars")
        report.append(f"   Avg Topics per Notebook: {sum(len(nb.topics) for nb in notebooks) / len(notebooks):.1f}")
        
        with_tags = [nb for nb in notebooks if hasattr(nb, 'tags') and nb.tags]
        report.append(f"   Notebooks with Tags: {len(with_tags) / len(notebooks) * 100:.1f}%")
        
        with_use_cases = [nb for nb in notebooks if hasattr(nb, 'use_cases') and nb.use_cases]
        report.append(f"   Notebooks with Use Cases: {len(with_use_cases) / len(notebooks) * 100:.1f}%")
        
        report.append("\n" + "=" * 60)
        
        return "\n".join(report)
    
    def suggest_notebook_updates(self, notebook_id: str) -> List[str]:
        """
        Suggest updates for a specific notebook.
        
        Args:
            notebook_id: ID of notebook to analyze
            
        Returns:
            List of update suggestions
        """
        notebooks = self.list_notebooks_with_details()
        notebook = next((nb for nb in notebooks if nb.id == notebook_id), None)
        
        if not notebook:
            raise ValueError(f"Notebook not found: {notebook_id}")
        
        suggestions = []
        
        # Description suggestions
        if len(notebook.description) < 30:
            suggestions.append(
                "Consider expanding description to 30+ characters "
                "for better discoverability"
            )
        
        # Topic suggestions
        if len(notebook.topics) < 3:
            suggestions.append(
                "Add more topics (aim for 3-5) to improve searchability"
            )
        
        # Use cases
        if not hasattr(notebook, 'use_cases') or not notebook.use_cases:
            suggestions.append(
                "Add use cases to describe when this notebook is helpful"
            )
        
        # Tags
        if not hasattr(notebook, 'tags') or not notebook.tags:
            suggestions.append(
                "Add organizational tags for better library management"
            )
        
        return suggestions
    
    def export_library(self, filename: str = "notebook-library-export.json"):
        """
        Export library to JSON file.
        
        Args:
            filename: Output filename
        """
        notebooks = self.list_notebooks_with_details()
        
        export_data = {
            'exported_at': datetime.now().isoformat(),
            'total_notebooks': len(notebooks),
            'notebooks': []
        }
        
        for notebook in notebooks:
            nb_data = {
                'id': notebook.id,
                'name': notebook.name,
                'description': notebook.description,
                'topics': notebook.topics,
                'url': notebook.url
            }
            
            if hasattr(notebook, 'tags') and notebook.tags:
                nb_data['tags'] = notebook.tags
            
            if hasattr(notebook, 'use_cases') and notebook.use_cases:
                nb_data['use_cases'] = notebook.use_cases
            
            if hasattr(notebook, 'content_types') and notebook.content_types:
                nb_data['content_types'] = notebook.content_types
            
            export_data['notebooks'].append(nb_data)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Library exported to {filename}")
        print(f"  Total notebooks: {len(notebooks)}")
        
        return filename


def main():
    """Main entry point for CLI usage"""
    helper = NotebookLMHelper()
    
    import argparse
    
    parser = argparse.ArgumentParser(
        description="NotebookLM MCP Helper Utility"
    )
    parser.add_argument(
        'action',
        choices=['list', 'search', 'report', 'export', 'analyze'],
        help="Action to perform"
    )
    parser.add_argument(
        '--query', '-q',
        help="Search query"
    )
    parser.add_argument(
        '--output', '-o',
        help="Output filename (for export)"
    )
    parser.add_argument(
        '--notebook-id', '-n',
        help="Notebook ID (for specific actions)"
    )
    
    args = parser.parse_args()
    
    try:
        if args.action == 'list':
            notebooks = helper.list_notebooks_with_details()
            print(f"\nTotal Notebooks: {len(notebooks)}\n")
            
            for nb in notebooks:
                print(f"📚 {nb.name}")
                print(f"   Topics: {', '.join(nb.topics)}")
                print(f"   ID: {nb.id}")
                print()
        
        elif args.action == 'search':
            if not args.query:
                print("Error: --query required for search")
                sys.exit(1)
            
            results = helper.search_notebooks_fuzzy(args.query)
            
            print(f"\nSearch Results for '{args.query}':\n")
            
            if results:
                for i, nb in enumerate(results, 1):
                    print(f"{i}. {nb.name}")
                    print(f"   {', '.join(nb.topics)}")
                    print(f"   {nb.description}")
                    print(f"   ID: {nb.id}")
                    print()
            else:
                print("No matching notebooks found.")
        
        elif args.action == 'report':
            report = helper.generate_library_report()
            print(report)
        
        elif args.action == 'export':
            filename = args.output or "notebook-library-export.json"
            helper.export_library(filename)
        
        elif args.action == 'analyze':
            if not args.notebook_id:
                print("Error: --notebook-id required for analyze")
                sys.exit(1)
            
            suggestions = helper.suggest_notebook_updates(args.notebook_id)
            
            print(f"\nSuggestions for notebook {args.notebook_id}:\n")
            
            if suggestions:
                for i, suggestion in enumerate(suggestions, 1):
                    print(f"{i}. {suggestion}")
            else:
                print("✓ No suggestions - notebook looks great!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
