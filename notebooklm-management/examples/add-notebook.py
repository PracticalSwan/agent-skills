"""
Example: Adding a New Notebook to Library

This example shows how to add a notebook from a Google share link
with proper metadata.
"""

# Example 1: Add documentation notebook
add_notebook(
    url="https://notebooklm.google/share/example-docs",
    name="Product Documentation",
    description="Complete API documentation and usage examples",
    topics=["API", "Documentation", "Reference"],
    content_types=["documentation", "examples"],
    use_cases=["API integration", "Troubleshooting", "Feature lookup"],
    tags=["official", "v2.0"]
)

# Example 2: Add research notebook
add_notebook(
    url="https://notebooklm.google/share/research-notes",
    name="ML Research Papers",
    description="Collection of key machine learning papers and summaries",
    topics=["Machine Learning", "Research", "Papers"],
    use_cases=["Literature review", "Model selection", "State-of-art"],
    tags=["academic", "research", "ml"]
)

# Example 3: Add tutorial notebook
add_notebook(
    url="https://notebooklm.google/share/tutorial-guide",
    name="React Tutorial Series",
    description="Step-by-step React development tutorials from beginner to advanced",
    topics=["React", "JavaScript", "Frontend"],
    content_types=["tutorials", "examples"],
    use_cases=["Learning React", "Best practices", "Quick reference"],
    tags=["tutorial", "react", "javascript"]
)
