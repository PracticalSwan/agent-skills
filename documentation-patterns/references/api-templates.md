# API Documentation Templates

## Function Documentation Template

```markdown
### `functionName(param1, param2)`

Brief description of what the function does.

**Parameters:**
- `param1` (type): Description of parameter
- `param2` (type, optional): Description with default value

**Returns:**
- `type`: Description of return value

**Example:**
```javascript
const result = functionName('value', 42);
```

**Throws:**
- `ErrorType`: When and why error is thrown
```

## REST Endpoint Documentation Template

```markdown
### `HTTP_METHOD /api/endpoint`

Description of what the endpoint does.

**Request:**
```json
{
  "param": "value"
}
```

**Response:**
```json
{
  "result": "value"
}
```

**Status Codes:**
- 200: Success
- 400: Bad request
- 401: Unauthorized
```
