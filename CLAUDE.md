# Blart-Py Development Guidelines

## Project Overview

This project creates a Python wrapper for the blart Rust library using PyO3. Blart is a high-performance adaptive radix tree implementation.

## Implementation Plan

The detailed implementation plan is documented in [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md). This plan covers:

- 7 development phases from project setup to distribution
- Key technical decisions and architecture
- File structure and dependencies
- Development workflow and tooling
- Success criteria and risk mitigation

**Please refer to IMPLEMENTATION_PLAN.md before making any changes to understand the overall architecture and phased approach.**

## Development Guidelines

### General Principles

Follow the guidelines from the global CLAUDE.md:
- Adhere to [DEV_GUIDELINES.md](~/.claude/DEV_GUIDELINES.md) for general development practices
- Follow [PYTHON_GUIDELINES.md](~/.claude/PYTHON_GUIDELINES.md) for Python code
- Use TodoWrite tool to track development tasks
- Prefer editing existing files over creating new ones

### Project-Specific Guidelines

#### Rust Code Standards

1. **Follow Rust best practices**:
   - Use `cargo fmt` for formatting
   - Resolve all `cargo clippy` warnings
   - Use `#[must_use]` where appropriate
   - Document public APIs with `///` doc comments

2. **PyO3 patterns**:
   - Use `#[pyclass]` for Python-visible types
   - Use `#[pymethods]` for Python methods
   - Return `PyResult<T>` for fallible operations
   - Use `Bound<'py, T>` for Python object references
   - Handle Python GIL correctly

3. **Error handling**:
   - Convert Rust errors to Python exceptions via `From<E> for PyErr`
   - Provide descriptive error messages
   - Use custom exception types for domain errors

4. **Memory safety**:
   - Ensure proper PyObject reference counting
   - Test for memory leaks with large datasets
   - Use `Py::clone_ref` when needed

#### Python Code Standards

1. **Type hints**:
   - Provide complete `.pyi` stub files
   - Use `typing` module for generic types
   - Document all parameters and return types

2. **Testing**:
   - Use pytest for all tests
   - Aim for >90% coverage
   - Include edge cases and error conditions
   - Test memory safety

3. **Documentation**:
   - Write comprehensive docstrings
   - Include usage examples in docstrings
   - Keep README.md up to date

#### Build and Development

1. **Use maturin for building**:
   ```bash
   maturin develop      # Development build
   maturin build        # Release build
   ```

2. **Testing workflow**:
   ```bash
   cargo test           # Rust tests
   pytest tests/        # Python tests
   ```

3. **Code quality**:
   ```bash
   cargo fmt            # Format Rust code
   cargo clippy         # Lint Rust code
   black python/ tests/ # Format Python code
   ruff check python/   # Lint Python code
   ```

## Key Technical Decisions

- **Key Type**: String keys (UTF-8) only for simplicity
- **Value Type**: PyObject for maximum flexibility
- **Build Tool**: maturin (standard for PyO3 projects)
- **Error Strategy**: Map Rust errors to Python exceptions
- **Iteration**: Clone data initially, optimize later if needed

## Development Phases

The project follows a 7-phase approach (see IMPLEMENTATION_PLAN.md):

1. **Project Setup** - Infrastructure and build configuration
2. **Core TreeMap** - Basic operations and dict-like interface
3. **Iteration Support** - Python iteration protocol
4. **Advanced Features** - Prefix queries and fuzzy matching
5. **Error Handling & Polish** - Production-ready code
6. **Testing & Documentation** - Comprehensive tests and docs
7. **Build & Distribution** - CI/CD and release process

## Important Notes

- Always check IMPLEMENTATION_PLAN.md before starting work on a phase
- Use TodoWrite to track progress within each phase
- Test on multiple Python versions (3.8+)
- Ensure backwards compatibility with PyO3 API changes
- Document any deviations from the plan with rationale
