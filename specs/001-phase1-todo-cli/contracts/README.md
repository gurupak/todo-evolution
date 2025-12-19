# Function Contracts: Phase I Todo CLI

**Feature**: Phase I - In-Memory Python Console Todo App  
**Date**: 2025-12-18  
**Status**: Complete

## Overview

This directory contains the function signature contracts for the Phase I Todo CLI application. Since this is a CLI application (not a web API), these contracts define the **public Python function interfaces** that form the application's internal API.

---

## Contract Files

- [models.md](./models.md) - Task and Priority data structures
- [storage.md](./storage.md) - InMemoryStorage service interface
- [commands.md](./commands.md) - Command handler functions
- [display.md](./display.md) - Display/formatting functions

---

## Design Principles

### 1. Dependency Injection
All command functions receive `storage: InMemoryStorage` as a parameter, enabling:
- Testability (can inject mock storage)
- No global state
- Clear dependencies

### 2. Type Safety
All functions use complete type hints:
- Parameter types
- Return types
- Union types (e.g., `Task | None`)
- Generic types (e.g., `list[Task]`)

### 3. Single Responsibility
Each function has one clear purpose:
- Command functions orchestrate user interaction
- Storage functions perform data operations
- Display functions handle output formatting

### 4. Void Returns for Commands
Command functions return `None` (side effects only):
- Simplifies control flow
- All output via display functions
- No complex return value handling

---

## Module Dependencies

```
main.py
  ├─> commands.py (uses all command functions)
  └─> display.py (uses show_banner)

commands.py
  ├─> storage.py (uses all storage methods)
  ├─> display.py (uses all display functions)
  └─> questionary (external library)

storage.py
  └─> models.py (uses Task, Priority)

display.py
  ├─> models.py (uses Task, Priority)
  └─> rich (external library)

models.py
  └─> (no dependencies - foundation)
```

**Dependency Rule**: Modules can only import from:
- Standard library
- External dependencies (questionary, rich)
- Modules below them in the dependency graph

---

## Testing Strategy

### Unit Tests
Test individual functions in isolation:
- `models.py` - Task creation, Priority enum
- `storage.py` - Each CRUD method independently

### Integration Tests
Test function interactions:
- `commands.py` - Mock questionary input, verify storage calls and display output
- End-to-end flows (add task → list tasks → mark complete)

### Contract Tests
Verify function signatures match contracts:
- Parameter types
- Return types
- Exception types

---

## Error Handling Contracts

All functions follow these error handling patterns:

### 1. Invalid Input
- **Storage methods**: Return `None` or `False` (not found)
- **Command functions**: Display error panel, return to menu
- **Display functions**: Never raise (graceful degradation)

### 2. Keyboard Interrupt
- **questionary prompts**: Return `None` on Ctrl+C
- **Command functions**: Check for `None`, show cancellation message
- **main loop**: Catch KeyboardInterrupt, continue loop

### 3. Unexpected Errors
- **All functions**: Let exceptions propagate to main loop
- **main loop**: Catch, log to console, display error panel, continue

---

## Versioning

Function contracts are versioned with the application:
- **Current Version**: 0.1.0 (Phase I)
- **Breaking Changes**: Require new major/minor version
- **Non-Breaking**: Can add optional parameters with defaults

---

## Next Steps

See individual contract files for detailed function signatures:
1. [models.md](./models.md) - Data structures
2. [storage.md](./storage.md) - Storage operations
3. [commands.md](./commands.md) - User interaction
4. [display.md](./display.md) - Output formatting
