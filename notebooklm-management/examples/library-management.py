"""
Example: Notebook Library Management

This example shows common library management operations.
"""

# Example 1: List all notebooks
notebooks = list_notebooks()
for notebook in notebooks:
    print(f"{notebook.name}")
    print(f"  Topics: {', '.join(notebook.topics)}")
    print(f"  Description: {notebook.description}")
    print()

# Example 2: Search for specific notebooks
# Find all React-related notebooks
react_notebooks = search_notebooks(query="react")

# Find notebooks about authentication
auth_notebooks = search_notebooks(query="authentication")

# Find notebooks with specific content type
tutorial_notebooks = search_notebooks(query="tutorial")

# Example 3: Update notebook metadata
# Rename a notebook
update_notebook(
    id="notebook-old-id",
    name="Updated: React Best Practices"
)

# Add more topics to a notebook
update_notebook(
    id="notebook-xyz",
    topics=["React", "Hooks", "Performance", "Optimization"]
)

# Update description and use cases
update_notebook(
    id="notebook-abc",
    description="Comprehensive guide to React hooks with real-world examples",
    use_cases=["Learning hooks", "Optimizing performance", "Best practices"],
    tags=["react", "hooks", "tutorial"]
)

# Example 4: Organize library workflow
def organize_library():
    """Find and update outdated notebook metadata"""
    
    # List all notebooks
    notebooks = list_notebooks()
    
    for notebook in notebooks:
        # Check for outdated descriptions (example logic)
        if "FIXME" in notebook.description or len(notebook.description) < 20:
            print(f"Needs update: {notebook.name}")
            
            # You would update with new metadata here
            # update_notebook(...)
    
    # Search for duplicates or similar notebooks
    docs_results = search_notebooks(query="documentation")
    print(f"Found {len(docs_results)} documentation notebooks")

# Example 5: Library audit
def audit_library():
    """Audit notebook library for quality"""
    
    notebooks = list_notebooks()
    
    missing_topics = []
    short_descriptions = []
    incomplete_metadata = []
    
    for nb in notebooks:
        if not nb.topics or len(nb.topics) < 2:
            missing_topics.append(nb.id)
        
        if len(nb.description) < 30:
            short_descriptions.append(nb.id)
        
        if not nb.use_cases:
            incomplete_metadata.append(nb.id)
    
    print(f"Notebooks missing topics: {len(missing_topics)}")
    print(f"Notebooks with short descriptions: {len(short_descriptions)}")
    print(f"Notebooks with incomplete metadata: {len(incomplete_metadata)}")
    
    return {
        "missing_topics": missing_topics,
        "short_descriptions": short_descriptions,
        "incomplete_metadata": incomplete_metadata
    }
