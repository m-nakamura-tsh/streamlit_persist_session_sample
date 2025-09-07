# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a proof-of-concept Streamlit application for managing long-running business processes with flexible session state persistence. The system demonstrates how Streamlit can handle long-term state management across multiple concurrent processes using a simple key-value storage approach.

### Key Requirements
- Single-user local environment (no multi-user considerations)
- Process state must persist beyond Streamlit session state
- Flexible data structure using `dict[str, Any]` instead of rigid models
- Only keys with `persist_` prefix are automatically persisted
- Storage backend must be swappable (JSON → SQLite) without interface changes

## Architecture

### Monorepo Structure with uv
- **packages/persistence**: Protocol-based persistence layer using duck typing (not ABC inheritance)
- **apps/main**: Main Streamlit application with automatic session state persistence
- **apps/sample**: Test application demonstrating flexible data storage
- **data/**: JSON file storage for process data (`processes.json`)

### Storage Layer Design
The persistence layer uses **Protocol (PEP 544)** for duck typing:
- `StorageInterface` is a Protocol, not an ABC
- `SimpleStorage` doesn't inherit from StorageInterface but conforms to it
- Any class implementing the required methods can be used as storage
- Currently JSON-based with single `processes.json` file

### Data Model Philosophy
- **No rigid models**: Removed `ProcessState`, `ProcessStep` classes
- **Flexible structure**: Uses `dict[str, Any]` for all process data
- **Type hints**: `JsonSerializable` and `ProcessData` type aliases for clarity
- **Validation**: Automatic JSON serializable checking on save

### Session State Persistence Rules
```python
# Keys with "persist_" prefix are automatically saved
st.text_input("Name", key="persist_name")  # Saved
st.checkbox("Show", key="show_details")    # Not saved
```

## Development Commands

### Setup & Installation
```bash
make setup       # Initial setup (creates directories, installs deps)
make install     # Install/sync dependencies with uv
uv sync --all-packages  # Sync all workspace packages
```

### Running Applications
```bash
make run-main    # Run main app on port 8501
make run-sample  # Run sample app on port 8502
./run_main.sh    # Alternative: run main app directly
./run_sample.sh  # Alternative: run sample app directly
```

### Development Tasks
```bash
make format      # Format code with ruff
make lint        # Lint code with ruff
make test        # Run tests with pytest
make clean       # Clean generated files

# Run specific tests
uv run pytest packages/persistence/tests/test_simple_storage.py -v

# Type checking
uv run mypy packages/persistence/src/
```

## Important Implementation Notes

### Process Selection Flow
1. App starts → Lists available processes from `data/processes.json`
2. User selects process → `load_process_data()` loads into session state
3. User modifies fields with `persist_` prefix → Auto-saved via `save_process_data()`
4. User switches process → Current state saved, new state loaded

### Data Storage Format
```json
{
  "process_name": {
    "session_data": {
      "persist_key1": "value1",
      "persist_key2": 123
    },
    "created": "ISO_DATE",
    "last_updated": "ISO_DATE"
  }
}
```

### Adding New Persistent Fields
Simply use `persist_` prefix:
```python
# Automatically persisted
st.number_input("Budget", key="persist_budget")
st.selectbox("Priority", ["Low", "High"], key="persist_priority")
```

### Storage Implementation Checklist
Any storage implementation must have these methods:
- `save_process(process_name: str, session_data: dict) -> None`
- `load_process(process_name: str) -> dict | None`
- `list_processes() -> List[str]`
- `delete_process(process_name: str) -> bool`
- `process_exists(process_name: str) -> bool`
- `get_process_info(process_name: str) -> dict | None`

## Testing Guidelines

### Test Coverage Areas
- Basic data types (str, int, float, bool, None)
- Complex structures (nested dicts, lists)
- Data validation (non-serializable objects)
- Process management (create, read, update, delete)
- Persistence across storage instances

### Running Tests
```bash
# All persistence tests
uv run pytest packages/persistence/tests/ -v

# With coverage
uv run pytest packages/persistence/tests/ --cov=persistence
```

## Common Issues & Solutions

### Issue: Module not found errors
**Solution**: Ensure `uv sync --all-packages` has been run

### Issue: Data not persisting
**Solution**: Check that keys have `persist_` prefix

### Issue: Non-serializable data error
**Solution**: Only use JSON-compatible types (no functions, classes, etc.)

## Future Extensions

### Adding SQLite Storage
1. Create `SqliteStorage` class in `packages/persistence/src/persistence/`
2. Implement all methods from `StorageInterface` protocol
3. No need to inherit or register - just implement the methods
4. Update app to use: `storage = SqliteStorage(db_path)`

### Adding Redis Storage
Same approach - implement the protocol methods, no inheritance needed.