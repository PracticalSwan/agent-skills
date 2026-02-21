"""
Example: Multi-Turn Conversation with NotebookLM

This example demonstrates how to maintain conversation context
across multiple queries using session_id.
"""

import uuid

# Start a new conversation about a topic
def explore_topic(notebook_id, topic):
    """Explore a topic through iterative questioning"""
    
    # Initial question
    response1 = ask_question(
        question=f"What is {topic}?",
        notebook_id=notebook_id
    )
    session_id = response1.session_id
    print(f"Session ID: {session_id}")
    
    # Drill down based on response
    response2 = ask_question(
        question="What are the key components?",
        notebook_id=notebook_id,
        session_id=session_id
    )
    
    # Explore relationships
    response3 = ask_question(
        question="How do these components work together?",
        notebook_id=notebook_id,
        session_id=session_id
    )
    
    # Ask about use cases
    response4 = ask_question(
        question="What are common use cases?",
        notebook_id=notebook_id,
        session_id=session_id
    )
    
    return session_id

# Example usage for exploring React concept
react_session = explore_topic(
    notebook_id="react-docs-123",
    topic="React Context API"
)

# Example usage for troubleshooting
def troubleshoot_issue(notebook_id, issue):
    """Troubleshoot an issue through iterative questioning"""
    
    response1 = ask_question(
        question=f"I'm experiencing: {issue}. What could be the causes?",
        notebook_id=notebook_id
    )
    session_id = response1.session_id
    
    response2 = ask_question(
        question="How do I diagnose which cause it is?",
        notebook_id=notebook_id,
        session_id=session_id
    )
    
    response3 = ask_question(
        question="What are the solutions for each cause?",
        notebook_id=notebook_id,
        session_id=session_id
    )
    
    return session_id

# Example: Troubleshoot API rate limit
troubleshoot_session = troubleshoot_issue(
    notebook_id="api-docs-456",
    issue="Getting rate limit errors on API calls"
)
