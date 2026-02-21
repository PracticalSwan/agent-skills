# NotebookLM Detailed Workflows

Comprehensive step-by-step workflows for all NotebookLM operations.

## Workflow 1: Adding a New Notebook

Complete process for adding a notebook from a share link to your library.

### Phase 1: Information Gathering

**Step 1.1**: Acquire the NotebookLM Share URL
```python
# Ask user for the share link
user_url = input("Enter NotebookLM share URL: ")
# Example: https://notebooklm.google/share/abc123def456
```

**Step 1.2**: Gather Notebook Content Information
```python
# Ask: What knowledge is inside this notebook?
description = input("What content/knowledge is in this notebook? (1-2 sentences): ")
# Example: "Complete API documentation for React hooks with examples and best practices"
```

**Step 1.3**: Identify Topics
```python
# Ask: Which topics does it cover?
topics_input = input("List 3-5 topics covered (comma-separated): ")
# Example: "React, Hooks, State Management, Performance, Documentation"

topics = [t.strip() for t in topics_input.split(",")]
```

**Step 1.4**: Define Use Cases
```python
# Ask: When should we consult this notebook?
use_cases_input = input("List use cases (comma-separated): ")
# Example: "Learning hooks, Troubleshooting state issues, Performance optimization"

use_cases = [uc.strip() for uc in use_cases_input.split(",")]
```

**Step 1.5**: Capture Additional Metadata (Optional)
```python
# Ask for content types if relevant
content_types_input = input("Content types (documentation, tutorial, examples, etc.): ") or None
# Example: ["documentation", "examples"]

# Ask for tags for organization
tags_input = input("Organizational tags (optional, comma-separated): ") or None
# Example: ["official", "v2.0", "core"]
```

### Phase 2: Propose and Confirm

**Step 2.1**: Generate Metadata Summary
```python
summary = f"""
Notebook Addition Summary:

URL: {user_url}
Name: [Proposed Name]
Description: {description}
Topics: {', '.join(topics)}
Use Cases: {', '.join(use_cases)}
"""

print(summary)
```

**Step 2.2**: Propose Name Based on Topics
```python
# Suggest a concise, descriptive name
primary_topic = topics[0]
suggested_name = f"{primary_topic} Documentation"

# Or combine top 2 topics
suggested_name = f"{topics[0]} {topics[1]} Guide"

print(f"Suggested name: {suggested_name}")
```

**Step 2.3**: Confirm with User
```python
confirmation = input("Add this notebook to your library? (yes/no): ").lower()

if confirmation == "yes":
    add_notebook(
        url=user_url,
        name=suggested_name,
        description=description,
        topics=topics,
        content_types=content_types,
        use_cases=use_cases,
        tags=tags
    )
    print("Notebook added successfully!")
else:
    print("Notebook not added.")
```

### Full Example

```python
def add_notebook_workflow():
    """Complete workflow for adding a notebook"""
    
    print("=== Add New Notebook to Library ===\n")
    
    # Phase 1: Gather information
    url = input("Enter NotebookLM share URL: ")
    
    description = input(
        "What content/knowledge is in this notebook? (1-2 sentences): "
    )
    
    topics_input = input("List 3-5 topics covered (comma-separated): ")
    topics = [t.strip() for t in topics_input.split(",")]
    
    use_cases_input = input("List use cases (comma-separated): ")
    use_cases = [uc.strip() for uc in use_cases_input.split(",")]
    
    content_types_input = input(
        "Content types (optional, comma-separated): "
    ) or ""
    content_types = [ct.strip() for ct in content_types_input.split(",")] if content_types_input else []
    
    tags_input = input("Organizational tags (optional, comma-separated): ") or ""
    tags = [t.strip() for t in tags_input.split(",")] if tags_input else []
    
    # Phase 2: Propose and confirm
    suggested_name = f"{topics[0]} Documentation"
    
    print(f"\n=== Notebook Summary ===")
    print(f"URL: {url}")
    print(f"Name: {suggested_name}")
    print(f"Description: {description}")
    print(f"Topics: {', '.join(topics)}")
    print(f"Use Cases: {', '.join(use_cases)}")
    if content_types:
        print(f"Content Types: {', '.join(content_types)}")
    if tags:
        print(f"Tags: {', '.join(tags)}")
    
    confirmation = input("\nAdd this notebook to your library? (yes/no): ").lower()
    
    if confirmation == "yes":
        add_notebook(
            url=url,
            name=suggested_name,
            description=description,
            topics=topics,
            content_types=content_types,
            use_cases=use_cases,
            tags=tags
        )
        print("\n✓ Notebook added successfully!")
        return True
    else:
        print("\n✗ Notebook not added.")
        return False
```

## Workflow 2: Querying Notebooks

Complete process for asking questions and getting answers from notebooks.

### Phase 1: Notebook Selection

**Step 2.1**: Check for Active Session
```python
# If continuing a conversation
existing_session_id = check_existing_session()
if existing_session_id:
    print(f"Continuing session: {existing_session_id}")
    use_session = True
```

**Step 2.2**: Select Notebook if No Active Session
```python
if not use_session:
    # List available notebooks
    notebooks = list_notebooks()
    
    print("\nAvailable Notebooks:")
    for i, nb in enumerate(notebooks, 1):
        print(f"{i}. {nb.name}")
        print(f"   Topics: {', '.join(nb.topics)}")
        print(f"   Description: {nb.description}\n")
    
    # User selects
    selection = input("Enter notebook number: ")
    selected_notebook = notebooks[int(selection) - 1]
```

### Phase 2: Formulate Question

**Step 2.3**: Guide User to Ask Good Question
```python
print("\n=== Formulate Your Question ===")
print("Tips for good questions:")
print("• Be specific and focused")
print("• Include context if needed")
print("• Ask about one topic at a time")
print("• Reference notebook content specifically if possible")

question = input("\nEnter your question: ")
```

**Step 2.4**: Validate Question
```python
# Check if question is too vague
vague_indicators = ["tell me about", "explain", "what is", "give me"]

if any(question.lower().startswith(indicator) for indicator in vague_indicators):
    print("\n⚠ Your question might be too general.")
    print("Try to be more specific:")
    print(f"  Instead of: '{question}'")
    print(f"  Consider: 'How does [specific aspect] work in [context]?'")
    
    refine = input("Refine your question? (yes/no): ").lower()
    if refine == "yes":
        question = input("Enter refined question: ")
```

### Phase 3: Execute Query

**Step 2.5**: Query with Appropriate Parameters
```python
if use_session:
    # Continue existing conversation
    response = ask_question(
        question=question,
        notebook_id=selected_notebook.id,
        session_id=existing_session_id
    )
else:
    # New query
    response = ask_question(
        question=question,
        notebook_id=selected_notebook.id
    )
    
    # Save session_id for follow-ups
    session_id = response.session_id if response.session_id else None
```

### Phase 4: Present Results

**Step 2.6**: Display Answer with Context
```python
print(f"\n=== Answer ===")
print(f"{response.answer}")

if hasattr(response, 'sources') and response.sources:
    print(f"\n=== Sources ===")
    for i, source in enumerate(response.sources, 1):
        print(f"{i}. {source}")

if hasattr(response, 'confidence'):
    confidence_pct = response.confidence * 100
    print(f"\nConfidence: {confidence_pct:.1f}%")
```

**Step 2.7**: Offer Follow-up Questions
```python
print(f"\n=== Continue Conversation? ===")
print(f"Session ID: {session_id}")

continue_conv = input("Ask another question? (yes/no): ").lower()

if continue_conv == "yes" and session_id:
    # Continue in workflow from Phase 2
    # with existing session_id
    ...
```

### Full Example

```python
def query_notebook_workflow():
    """Complete workflow for querying a notebook"""
    
    print("=== Query Notebook ===\n")
    
    # Phase 1: Notebook selection
    session_id = None
    
    # Check for existing session
    existing_id = input("Continue existing session? (yes/no): ").lower()
    if existing_id == "yes":
        session_id = input("Enter session ID: ")
        notebook_id = input("Enter notebook ID: ")
    else:
        # Select notebook
        notebooks = list_notebooks()
        
        print("\nAvailable Notebooks:")
        for i, nb in enumerate(notebooks, 1):
            print(f"{i}. {nb.name}")
            print(f"   {', '.join(nb.topics)}")
        
        selection = int(input("\nSelect notebook number: "))
        selected_notebook = notebooks[selection - 1]
        notebook_id = selected_notebook.id
    
    # Phase 2: Formulate question
    print("\nFormulate your question:")
    print("• Be specific and focused")
    print("• Include context if needed")
    
    question = input("\nYour question: ")
    
    # Phase 3: Execute
    response = ask_question(
        question=question,
        notebook_id=notebook_id,
        session_id=session_id
    )
    
    if not session_id:
        session_id = response.session_id
    
    # Phase 4: Present results
    print(f"\n=== Answer ===")
    print(f"{response.answer}")
    
    if hasattr(response, 'sources'):
        print(f"\n=== Sources ===")
        for source in response.sources:
            print(f"• {source}")
    
    print(f"\nSession ID: {session_id}")
    
    # Offer follow-up
    while True:
        continue_query = input("\nAsk another? (yes/no): ").lower()
        if continue_query != "yes":
            break
        
        question = input("\nYour question: ")
        response = ask_question(
            question=question,
            notebook_id=notebook_id,
            session_id=session_id
        )
        print(f"\n{response.answer}")
    
    return session_id
```

## Workflow 3: Managing Notebook Library

Complete processes for organizing and maintaining notebook library.

### Phase 1: Library Audit

**Step 3.1**: List All Notebooks
```python
notebooks = list_notebooks()

print(f"\n=== Notebook Library Audit ===")
print(f"Total notebooks: {len(notebooks)}\n")

for i, nb in enumerate(notebooks, 1):
    print(f"{i}. {nb.name}")
    print(f"   ID: {nb.id}")
    print(f"   Topics: {', '.join(nb.topics)}")
    print(f"   Description: {nb.description}")
    
    if hasattr(nb, 'tags') and nb.tags:
        print(f"   Tags: {', '.join(nb.tags)}")
    
    if hasattr(nb, 'use_cases') and nb.use_cases:
        print(f"   Use Cases: {', '.join(nb.use_cases)}")
    
    print()
```

**Step 3.2**: Identify Issues
```python
issues = {
    "short_descriptions": [],
    "missing_topics": [],
    "no_use_cases": [],
    "duplicate_names": {}
}

for nb in notebooks:
    # Check description length
    if len(nb.description) < 30:
        issues["short_descriptions"].append(nb.id)
    
    # Check topic count
    if len(nb.topics) < 2:
        issues["missing_topics"].append(nb.id)
    
    # Check use cases
    if not nb.use_cases or len(nb.use_cases) == 0:
        issues["no_use_cases"].append(nb.id)
    
    # Check for duplicates
    if nb.name in issues["duplicate_names"]:
        issues["duplicate_names"][nb.name].append(nb.id)
    else:
        issues["duplicate_names"][nb.name] = [nb.id]

# Report issues
print("\n=== Issues Found ===")
for issue_type, affected in issues.items():
    if affected:
        print(f"\n{issue_type.replace('_', ' ').title()}: {len(affected)}")
        for item in affected:
            print(f"  - {item}")
```

### Phase 2: Organization

**Step 3.3**: Search for Related Notebooks
```python
print("\n=== Search and Group ===")

# Find notebooks by topic
search_query = input("Enter topic to search for: ")
matching_notebooks = search_notebooks(query=search_query)

print(f"\nNotebooks matching '{search_query}':")
for nb in matching_notebooks:
    print(f"• {nb.name} ({', '.join(nb.topics)})")
```

**Step 3.4**: Update Metadata
```python
print("\n=== Update Metadata ===")
notebook_id = input("Enter notebook ID to update: ")

# Get current notebook
notebook = next(nb for nb in notebooks if nb.id == notebook_id)
print(f"\nCurrent Name: {notebook.name}")
print(f"Current Description: {notebook.description}")
print(f"Current Topics: {', '.join(notebook.topics)}")

# Ask what to update
print("\nWhat to update?")
print("1. Name")
print("2. Description")
print("3. Topics")
print("4. All")
choice = input("Enter choice (1-4): ")

if choice == "1":
    new_name = input(f"New name for {notebook.name}: ")
    update_notebook(id=notebook_id, name=new_name)
elif choice == "2":
    new_desc = input(f"New description: ")
    update_notebook(id=notebook_id, description=new_desc)
elif choice == "3":
    new_topics = input("New topics (comma-separated): ")
    topics = [t.strip() for t in new_topics.split(",")]
    update_notebook(id=notebook_id, topics=topics)
elif choice == "4":
    new_name = input("New name: ")
    new_desc = input("New description: ")
    new_topics = input("New topics (comma-separated): ")
    topics = [t.strip() for t in new_topics.split(",")]
    update_notebook(id=notebook_id, name=new_name, description=new_desc, topics=topics)

print("✓ Updated successfully!")
```

### Full Example

```python
def manage_library_workflow():
    """Complete library management workflow"""
    
    while True:
        print("\n=== Notebook Library Management ===")
        print("1. List all notebooks")
        print("2. Search notebooks")
        print("3. Update metadata")
        print("4. Run audit")
        print("5. Exit")
        
        choice = input("\nSelect option (1-5): ")
        
        if choice == "1":
            notebooks = list_notebooks()
            for nb in notebooks:
                print(f"\n{nb.name}")
                print(f"  Topics: {', '.join(nb.topics)}")
                print(f"  Description: {nb.description}")
        
        elif choice == "2":
            query = input("\nSearch term: ")
            results = search_notebooks(query=query)
            
            if results:
                for nb in results:
                    print(f"\n{nb.name}")
                    print(f"  {', '.join(nb.topics)}")
            else:
                print("No matching notebooks found.")
        
        elif choice == "3":
            notebooks = list_notebooks()
            print("\nSelect notebook:")
            for i, nb in enumerate(notebooks, 1):
                print(f"{i}. {nb.name}")
            
            selection = int(input("\nEnter number: "))
            notebook = notebooks[selection - 1]
            
            field = input(f"\nUpdate field for '{notebook.name}' (name/description/topics): ")
            
            if field == "name":
                new_value = input("New name: ")
                update_notebook(id=notebook.id, name=new_value)
            elif field == "description":
                new_value = input("New description: ")
                update_notebook(id=notebook.id, description=new_value)
            elif field == "topics":
                new_value = input("New topics (comma-separated): ")
                topics = [t.strip() for t in new_value.split(",")]
                update_notebook(id=notebook.id, topics=topics)
            
            print("✓ Updated!")
        
        elif choice == "4":
            notebooks = list_notebooks()
            
            issues = 0
            for nb in notebooks:
                if len(nb.description) < 30:
                    print(f"⚠ Short description: {nb.name}")
                    issues += 1
                if len(nb.topics) < 2:
                    print(f"⚠ Few topics: {nb.name}")
                    issues += 1
            
            if issues == 0:
                print("✓ No issues found!")
        
        elif choice == "5":
            break
```

## Workflow 4: Troubleshooting Authentication

Complete process for resolving authentication issues.

### Scenario 1: First-Time Setup

```python
def initial_authentication_setup():
    """Complete first-time authentication setup"""
    
    print("=== NotebookLM Authentication Setup ===")
    print("This will open a browser window for Google OAuth.")
    print("\nRequirements:")
    print("• Google account with NotebookLM access")
    print("• Browser window permission")
    print("• Internet connection\n")
    
    proceed = input("Proceed? (yes/no): ").lower()
    if proceed != "yes":
        print("Setup cancelled.")
        return False
    
    print("\nOpening browser for authentication...")
    notebooklm.auth-setup()
    
    print("\n✓ Authentication complete!")
    print("\nVerifying health...")
    health_status = get_health()
    
    if health_status.get("status") == "authenticated":
        print("✓ Successfully authenticated!")
        return True
    else:
        print("✗ Authentication may have failed.")
        print("Please run authentication again or check troubleshoot guide.")
        return False
```

### Scenario 2: Session Recovery

```python
def recover_expired_session():
    """Recover from expired session"""
    
    print("=== Session Recovery ===")
    print("Your session may have expired.")
    print("Common causes:")
    print("• Long period of inactivity")
    print("• MCP server upgrade")
    print("• Account changes\n")
    
    action = input("Recover session? (yes/no): ").lower()
    if action != "yes":
        print("Recovery cancelled.")
        return False
    
    print("\nClearing old session data...")
    notebooklm.auth-repair()
    
    print("Opening browser for re-authentication...")
    notebooklm.auth-setup()
    
    print("\n✓ Session recovered!")
    return True
```

### Scenario 3: Account Switch

```python
def switch_google_account():
    """Switch to different Google account"""
    
    print("=== Switch Google Account ===")
    print("This will clear your current session.")
    print("You'll need to authenticate with the new account.\n")
    
    confirm = input("Switch account? (yes/no): ").lower()
    if confirm != "yes":
        print("Cancelled.")
        return False
    
    print("\nClearing current session...")
    notebooklm.auth-repair()
    
    print("Opening browser for new account authentication...")
    notebooklm.auth-setup()
    
    print("\n✓ Account switched!")
    return True
```

## Workflow 5: Multi-Turn Conversations

Advanced workflow for maintaining context across multiple questions.

### Complete Conversation Pattern

```python
def multi_turn_conversation(notebook_id):
    """Structured multi-turn conversation"""
    
    print("=== Multi-Turn Conversation ===")
    print("Topic exploration mode. Enter 'exit' to finish.\n")
    
    # Initial question
    question = input("Starting question: ")
    response = ask_question(
        question=question,
        notebook_id=notebook_id
    )
    
    session_id = response.session_id
    print(f"\n{response.answer}")
    
    turn_count = 1
    
    while True:
        turn_count += 1
        print(f"\n--- Turn {turn_count} ---")
        
        # Provide context hints
        print(f"Session: {session_id}")
        print("Context preserved from previous turns.")
        
        question = input("\nYour follow-up question (or 'exit'): ")
        
        if question.lower() == "exit":
            print("\n=== Conversation Summary ===")
            print(f"Total turns: {turn_count}")
            print(f"Session ID: {session_id}")
            break
        
        # Ask follow-up question
        response = ask_question(
            question=question,
            notebook_id=notebook_id,
            session_id=session_id
        )
        
        print(f"\n{response.answer}")
        
        # Show sources if available
        if hasattr(response, 'sources') and response.sources:
            print(f"\nSources:")
            for source in response.sources:
                print(f"  • {source}")
    
    return session_id
```

### Topic Exploration Pattern

```python
def explore_topic_depth(notebook_id, topic):
    """Explore a topic progressively deeper"""
    
    print(f"\n=== Exploring: {topic} ===\n")
    
    # Level 1: Overview
    print("Level 1: Overview")
    response = ask_question(
        question=f"What is {topic} at a high level?",
        notebook_id=notebook_id
    )
    print(f"{response.answer}\n")
    session_id = response.session_id
    
    # Level 2: Components
    print("Level 2: Components")
    response = ask_question(
        question="What are the main components or aspects?",
        notebook_id=notebook_id,
        session_id=session_id
    )
    print(f"{response.answer}\n")
    
    # Level 3: Deep dive
    print("Level 3: Deep Dive")
    component = input("\nWhich component to explore deeper? ")
    response = ask_question(
        question=f"Tell me more about {component}",
        notebook_id=notebook_id,
        session_id=session_id
    )
    print(f"{response.answer}\n")
    
    # Level 4: Use cases
    print("Level 4: Practical Application")
    response = ask_question(
        question="What are practical use cases or applications?",
        notebook_id=notebook_id,
        session_id=session_id
    )
    print(f"{response.answer}\n")
    
    return session_id
```
