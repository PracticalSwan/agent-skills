"""
Example: Ad-Hoc Notebook Queries

This example demonstrates querying notebooks without adding
them to your library using notebook_url parameter.
"""

# Example 1: Query a shared notebook directly
# Useful for one-time queries without adding to library
response = ask_question(
    question="What are the main architecture principles discussed?",
    notebook_url="https://notebooklm.google/share/some-shared-notebook"
)

# Example 2: Compare two notebooks
# Query notebook 1
response1 = ask_question(
    question="What is the approach to error handling?",
    notebook_url="https://notebooklm.google/share/notebook-1"
)

# Query notebook 2
response2 = ask_question(
    question="What is the approach to error handling?",
    notebook_url="https://notebooklm.google/share/notebook-2"
)

# Compare results and provide analysis

# Example 3: Quick question about public resource
def quick_fact_check(question, notebook_url):
    """
    Quickly check a fact or get information from a public notebook
    without adding it to your library.
    
    Useful for: 
    - One-time lookups
    - Evaluating if notebook is worth adding
    - Quick fact verification
    """
    response = ask_question(
        question=question,
        notebook_url=notebook_url
    )
    return response

# Usage: Check if a notebook is relevant
test_response = quick_fact_check(
    question="Does this notebook cover Node.js development?",
    notebook_url="https://notebooklm.google/share/some-public-docs"
)

# If relevant, then add to library
if "Node.js" in test_response.answer:
    add_notebook(
        url="https://notebooklm.google/share/some-public-docs",
        name="Node.js Development Guide",
        description="Complete Node.js development documentation",
        topics=["Node.js", "Backend", "JavaScript"]
    )

# Example 4: Evaluate notebook before adding
def evaluate_notebook(notebook_url):
    """
    Ask multiple questions to evaluate if a notebook is worth
    adding to your library.
    """
    
    questions = [
        "What topics does this notebook cover?",
        "What is the target audience?",
        "What level of detail is provided?",
        "What are the main use cases?"
    ]
    
    evaluation = {}
    for q in questions:
        response = ask_question(question=q, notebook_url=notebook_url)
        evaluation[q] = response.answer
    
    return evaluation

# Evaluate before adding
evaluation_result = evaluate_notebook(
    "https://notebooklm.google/share/candidate-notebook"
)

# Review and decide based on evaluation
