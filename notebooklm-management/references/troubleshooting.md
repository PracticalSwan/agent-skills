# NotebookLM Troubleshooting Guide

Complete guide for diagnosing and resolving common NotebookLM MCP issues.

## Authentication Issues

### Problem: "Authentication Required" or "Login Required"

**Symptoms**:
- Error messages about requiring login
- unable to access notebooks
- Queries fail with auth errors

**Diagnosis Steps**:
1. Check if this is first-time use → see [Initial Setup](#initial-setup)
2. Check if session recently expired → see [Session Recovery](#session-recovery)
3. Check if Google account changed → see [Account Switch](#account-switch)

#### Initial Setup

First time using NotebookLM MCP:

```python
# Run authentication setup
notebooklm.auth-setup()

# This will:
# 1. Open browser for OAuth flow
# 2. Request Google account login
# 3. Request NotebookLM permissions
# 4. Save session credentials locally

# After setup, verify with health check
get_health()
```

**Expected Behavior**:
- Browser opens to Google login
- Request for NotebookLM access permissions
- Session saved automatically
- Health check returns success

**If Still Fails**:
1. Check browser is allowing popups
2. Verify Google account has NotebookLM access
3. Check network connectivity
4. Try incognito/private browser mode

#### Session Recovery

Previously authenticated but now getting auth errors:

```python
# Clear old session data
notebooklm.auth-repair()

# Re-authenticate
notebooklm.auth-setup()

# Verify
get_health()
```

**When to Use**:
- Seeing authentication required for first time in a while
- Just upgraded MCP server version
- Changed Google account
- Session corrupted

#### Account Switch

Using different Google account than initial setup:

```python
# Clear existing session
notebooklm.auth-repair()

# Start fresh
notebooklm.auth-setup()

# Login with desired account
```

### Problem: Authentication Stuck in Browser

**Symptoms**:
- OAuth window opens but doesn't complete
- Infinite loading during authentication
- Window closes without success

**Solutions**:

```python
# Clear all session data and retry
notebooklm.auth-repair()
notebooklm.auth-setup()

# If still stuck, check:
# 1. Browser extensions blocking OAuth
# 2. Pop-up blocker enabled
# 3. Network/firewall issues
# 4. Google service outage
```

**Browser-Specific Fixes**:

**Chrome**:
1. Disable ad blockers temporarily
2. Check `chrome://settings/cookies` for blocked cookies
3. Try in incognito mode

**Firefox**:
1. Check privacy settings
2. Allow cookies for accounts.google.com
3. Try in private window

## Query Issues

### Problem: Query Returns Wrong Information

**Symptoms**:
- Answer doesn't match question
- Information from different notebook
- Completely unrelated response

**Diagnosis**:

```python
# 1. Verify you're querying correct notebook
notebooks = list_notebooks()
print([nb.name for nb in notebooks])

# 2. Check if using the right notebook_id
response = ask_question(
    question="test query",
    notebook_id="your-notebook-id"
)

# 3. If using session_id, check if context is preserved
# Old session_id might have wrong context
```

**Solutions**:

```python
# Solution 1: Explicitly specify notebook_id
response = ask_question(
    question="Your specific question",
    notebook_id="correct-notebook-id"
)

# Solution 2: Reset session if context confused
reset_session(session_id="old-session-id")

# Solution 3: Start new conversation without session_id
response = ask_question(
    question="Your specific question",
    notebook_id="correct-notebook-id"
    # No session_id = new context
)
```

### Problem: Query Timeout or Slow Response

**Symptoms**:
- Query takes 30+ seconds
- Response never comes
- Timeout errors

**Diagnosis**:

```python
# Try with browser visibility to debug
response = ask_question(
    question="test query",
    notebook_id="your-notebook-id",
    show_browser=True
)
```

**Solutions**:

```python
# Solution 1: Optimize query
# Too broad → narrow down
response = ask_question(
    question="Specific focused question",  # Better than "tell me about X"
    notebook_id="your-notebook-id"
)

# Solution 2: Increase timeout via browser_options
response =ask_question(
    question="Your question",
    notebook_id="your-notebook-id",
    browser_options={
        "timeout": 60000  # 60 seconds
    }
)

# Solution 3: Break into smaller queries
# Instead of one complex question, ask multiple simple ones
```

### Problem: Query Returns Empty or Minimal Response

**Symptoms**:
- Response is very short
- "I don't know" type answers
- No sources cited

**Diagnosis**:

```python
# 1. Check if notebook has relevant content
list_notebooks()  # Verify notebook exists

# 2. Test with simple question
response = ask_question(
    question="What topics are covered?",
    notebook_id="your-notebook-id"
)

# 3. Check if notebook was properly added
# Verify it's not empty or corrupted
```

**Solutions**:

```python
# Solution 1: Re-add notebook if corrupted
add_notebook(
    url="original-share-url",
    name="Notebook Name",
    description="Description",
    topics=["Topic 1", "Topic 2"]
)

# Solution 2: Reformulate question
# Be more specific
response = ask_question(
    question="Specific question about specific topic",
    notebook_id="your-notebook-id"
)

# Solution 3: Query different notebook
search_notebooks(query="relevant-topic")
```

## Notebook Management Issues

### Problem: Notebook Not Found in Library

**Symptoms**:
- `list_notebooks()` doesn't show expected notebook
- Search returns no results
- Query fails with "notebook not found"

**Diagnosis**:

```python
# Check all notebooks
all_notebooks = list_notebooks()
for nb in all_notebooks:
    print(f"{nb.id}: {nb.name}")

# Search by partial name
results = search_notebooks(query="partial-name")
```

**Solutions**:

```python
# Solution 1: Re-add notebook
add_notebook(
    url="share-url",
    name="Notebook Name",
    description="Description",
    topics=["Topic"]
)

# Solution 2: Check different terms in search
search_notebooks(query="different-keyword")
search_notebooks(query="tag-name")

# Solution 3: Verify notebook ID from previous interactions
# If you have session_id, check context
```

### Problem: Can't Update Notebook Metadata

**Symptoms**:
- `update_notebook()` fails
- Changes not reflected
- Invalid field errors

**Diagnosis**:

```python
# Verify notebook exists and get correct ID
notebooks = list_notebooks()
for nb in notebooks:
    if nb.name == "Target Name":
        correct_id = nb.id
        print(f"Correct ID: {correct_id}")
```

**Solutions**:

```python
# Solution 1: Use correct notebook_id
update_notebook(
    id="correct-id-from-list",  # Must match exactly
    name="New Name"
)

# Solution 2: Update one field at a time
update_notebook(
    id="notebook-id",
    name="New Name"  # Just name
)
update_notebook(
    id="notebook-id",
    description="New Description"  # Then description
)

# Solution 3: Check for valid enum values
# content_types, tags should be strings
# topics should be list of strings
```

## Session Management Issues

### Problem: Session Context Confusing or Incorrect

**Symptoms**:
- Follow-up questions don't make sense
- Context from previous queries affects new ones
- Contradictory answers

**Diagnosis**:

```python
# Check if using old session_id
# Old sessions maintain context from previous questions
```

**Solutions**:

```python
# Solution 1: Reset session for fresh context
reset_session(session_id="old-session-id")

# Now start fresh context in same notebook
response = ask_question(
    question="Completely different topic",
    notebook_id="notebook-id",
    session_id="reset-session-id"  # Same ID, fresh context
)

# Solution 2: Start completely new session
# Don't provide session_id at all
response = ask_question(
    question="New topic",
    notebook_id="notebook-id"
    # No session_id = automatically new
)
```

### Problem: Lost Session ID

**Symptoms**:
- Can't continue multi-turn conversation
- Don't have session_id from previous query

**Solutions**:

```python
# Solution 1: Start fresh conversation
response = ask_question(
    question="Your question",
    notebook_id="notebook-id"
    # New session_id will be in response
)
new_session_id = response.session_id

# Solution 2: Re-ask initial question
# If you remember what the first question was
response = ask_question(
    question="Initial question from before",
    notebook_id="notebook-id"
)
# Get session_id and continue

# Solution 3: Check if session_id is needed
# For simple one-off questions, don't use session_id
response = ask_question(
    question="Independent question",
    notebook_id="notebook-id"
)
```

## Rate Limit Issues

### Problem: "Too Many Queries" or Rate Limit Errors

**Symptoms**:
- Rate limit error messages
- Queries suddenly start failing
- Error after many successful queries

**Diagnosis**:

```python
# Check NotebookLM account tier
# Free tier: 50 daily queries
# Paid tiers: Higher limits

# Monitor query count
# Keep track of how many queries you've made
```

**Solutions**:

```python
# Solution 1: Wait for cooldown
# Free tier resets daily
# Wait until next day for more queries

# Solution 2: Upgrade account tier
# Visit NotebookLM to upgrade for higher limits

# Solution 3: Optimize query strategy
# Batch related questions in multi-turn conversations
# Instead of 10 separate queries, use 1 with follow-ups
response1 = ask_question(
    question="Overview of topic",
    notebook_id="notebook-id"
)
session_id = response1.session_id

# Follow-ups count differently or use less quota
response2 = ask_question(
    question="Detail point A",
    notebook_id="notebook-id",
    session_id=session_id
)
```

### Problem: Frequent Rate Limiting

**Symptoms**:
- Always hitting limits
- Can't work efficiently

**Long-Term Solutions**:

```python
# Solution 1: Cache results locally
# Store common answers to avoid re-querying
cache = {}

def cached_query(question, notebook_id):
    key = f"{notebook_id}:{question}"
    if key in cache:
        return cache[key]
    
    response = ask_question(question=question, notebook_id=notebook_id)
    cache[key] = response
    return response

# Solution 2: Use notebooks with comprehensive content
# Better notebooks = fewer queries needed
# Add comprehensive documentation notebooks instead of many small ones

# Solution 3: Batch questions intelligently
# Use multi-turn conversations for related topics
```

## Network and Connectivity Issues

### Problem: Connection Errors

**Symptoms**:
- Network timeout errors
- Connection refused
- Unable to reach NotebookLM

**Diagnosis**:

```python
# Check network connectivity
# Can you reach other MCP servers?
# Test in browser: notebooklm.google
```

**Solutions**:

```python
# Solution 1: Check internet connection
# Verify you can access notebooklm.google in browser

# Solution 2: Check firewall/proxy settings
# Ensure NotebookLM domains not blocked

# Solution 3: Try with browser to debug
response = ask_question(
    question="test",
    notebook_id="notebook-id",
    show_browser=True,
    browser_options={
        "timeout": 60000
    }
)
```

## Getting Help

### When to Seek Additional Help

- Issues persist after trying all solutions
- Error messages not covered in this guide
- Unexpected behavior not documented

### Information to Gather

Before seeking help, collect:

```python
# 1. MCP server version
# From MCP server configuration

# 2. Error messages (exact text)
# Copy full error stack trace

# 3. Steps to reproduce
# What you did, in what order

# 4. Expected vs actual behavior
# What you expected to happen vs what did

# 5. Environment info
# OS, browser, Node.js version (if applicable)
```

### Where to Get Help

- [NotebookLM Documentation](https://notebooklm.google)
- [MCP Server Repository Issues](https://github.com/example/notebooklm-mcp/issues)
- [Agent Skills Documentation](https://agentskills.io/)
