"""
Example: Simple Query to NotebookLM

This example demonstrates how to query a specific notebook
with a straightforward question.
"""

# Example 1: Query a specific notebook by ID
result = ask_question(
    question="What are the main features of the product?",
    notebook_id="notebook-abc-123"
)

# Example 2: Query without notebook ID (uses active session)
result = ask_question(
    question="Explain the authentication flow"
)

# Example 3: Query with follow-up using session_id
# First query
initial_response = ask_question(
    question="What are the API endpoints?",
    notebook_id="notebook-abc-123"
)
session_id = initial_response.session_id

# Follow-up query in same conversation
follow_up = ask_question(
    question="How do I authenticate to these endpoints?",
    notebook_id="notebook-abc-123",
    session_id=session_id
)
