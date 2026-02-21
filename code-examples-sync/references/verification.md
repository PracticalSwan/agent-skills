# Code Example Verification

## Before Committing Examples

1. **Syntax Check**: Ensure all code examples follow correct syntax for the language

2. **Compilation**: Verify examples compile without errors

3. **Execution**: Test that examples produce expected output

4. **Imports**: Check that import statements reference existing modules

5. **Dependencies**: Verify referenced dependencies are current and available

## Common Issues

- **Import Errors**: Module paths change, packages renamed
- **Syntax Changes**: Language version updates or deprecated syntax
- **Output Mismatches**: Function behavior changes or updates
- **Deprecated Functions**: Using removed or phased-out APIs

## Testing Examples

```bash
# Example validation for various languages
npm run docs:test-examples  # JavaScript/TypeScript
python -m doctest docs/     # Python
cargo test --doc            # Rust
go test -run=Doc            # Go
```
