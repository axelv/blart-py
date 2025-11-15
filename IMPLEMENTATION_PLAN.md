# Python Wrapper for Blart using PyO3 - Implementation Plan

## Overview
Create a high-performance Python wrapper for the blart Rust library (adaptive radix tree) using PyO3. The wrapper will expose blart's TreeMap as a Python class with dictionary-like interface and advanced features like prefix queries and fuzzy matching.

## Background

### About Blart
Blart is a high-performance adaptive radix tree implementation that serves as a drop-in replacement for BTreeMap. It provides:
- Space-efficient ordered map storage
- Excellent performance for byte-string keys
- Memory-efficient prefix compression
- Advanced features like fuzzy matching (Levenshtein distance) and prefix queries

### About PyO3
PyO3 provides Rust bindings for Python, enabling the creation of native Python extension modules. It allows seamless integration between Rust and Python with automatic type conversions and memory management.

## Implementation Phases

**Development Approach**: Test-Driven Development (TDD)

Each phase follows the TDD cycle:
1. **Write tests first** - Define expected behavior through tests
2. **Implement minimal interfaces** - Create stubs that compile but fail tests
3. **Make tests pass** - Implement functionality incrementally
4. **Refactor** - Clean up code while keeping tests green
5. **Commit** - Commit working milestone with meaningful message

**Key TDD Principles**:
- Tests are written before implementation code
- Each commit represents a working milestone (tests pass)
- Commit messages follow conventional commit format (feat/test/docs/fix/chore)
- Never commit broken tests or failing builds
- Total expected commits: 35+ across all phases

**Phase Summary**:
- **Phase 1**: Project setup (2 commits)
- **Phase 2**: Basic operations (8 commits)
- **Phase 3**: Iteration (4 commits)
- **Phase 4**: Prefix queries (4 commits)
- **Phase 5**: Advanced features (5 commits)
- **Phase 6**: Error handling (6 commits)
- **Phase 7**: Documentation (4 commits)
- **Phase 8**: Build/distribution (5 commits)

### Phase 1: Project Setup & Scaffolding
**Goal**: Establish project structure, build infrastructure, and minimal stub implementation

**TDD Steps**:

1. **Setup project structure** (no tests yet):
   - Create `Cargo.toml` with dependencies:
     - `pyo3 = { version = "0.22", features = ["extension-module"] }`
     - `blart = "0.4"`
   - Create `pyproject.toml` with maturin configuration
   - Create `.gitignore` for Rust/Python hybrid project
   - Create Python package structure:
     - `python/blart/__init__.py`
     - `python/blart/__init__.pyi`
     - `python/blart/py.typed`
   - Create Rust source structure:
     - `src/lib.rs` - Minimal `#[pymodule]` definition
     - `src/treemap.rs` - Empty `PyTreeMap` struct stub
   - **Commit**: `"chore: initial project setup with build configuration"`

2. **Verify build works**:
   - Run `maturin develop` to ensure project compiles
   - Create `tests/conftest.py` with pytest configuration
   - Create minimal smoke test in `tests/test_import.py`:
     ```python
     def test_can_import():
         import blart
         assert blart is not None
     ```
   - **Commit**: `"test: add smoke test for package import"`

**Deliverables**:
- Compilable Rust project with PyO3
- Python package structure
- Development environment working
- Initial git repository with commits

---

### Phase 2: Core TreeMap - Constructor & Basic Operations
**Goal**: Implement basic TreeMap functionality with dictionary-like interface

**TDD Steps**:

1. **Write comprehensive tests** (`tests/test_basic.py`):
   ```python
   # Constructor tests
   def test_treemap_constructor_empty()
   def test_treemap_constructor_from_dict()
   def test_treemap_constructor_from_items()

   # Basic operations
   def test_insert_and_get()
   def test_get_with_default()
   def test_get_missing_key_returns_none()
   def test_remove_existing_key()
   def test_remove_missing_key_raises_keyerror()
   def test_clear()
   def test_len()
   def test_is_empty()

   # Dict-like interface
   def test_setitem_and_getitem()
   def test_getitem_missing_raises_keyerror()
   def test_delitem()
   def test_delitem_missing_raises_keyerror()
   def test_contains()

   # String representation
   def test_repr()
   def test_str()

   # Edge cases
   def test_unicode_keys()
   def test_none_values()
   def test_various_value_types()
   ```
   - **Commit**: `"test: add comprehensive tests for basic TreeMap operations"`

2. **Create minimal interface stubs** (in `src/treemap.rs`):
   - Define `PyTreeMap` struct wrapping `TreeMap<Box<[u8]>, PyObject>`
   - Implement `#[new]` returning empty TreeMap
   - Add stub methods that raise `NotImplementedError` or return dummy values
   - Update `src/lib.rs` to export `PyTreeMap` as `TreeMap`
   - Update `python/blart/__init__.py` to re-export
   - Build with `maturin develop` - tests should fail
   - **Commit**: `"feat: add TreeMap stub interface"`

3. **Implement constructor**:
   - Implement empty constructor
   - Make constructor tests pass
   - **Commit**: `"feat: implement TreeMap constructor"`

4. **Implement insert & get operations**:
   - Implement `insert()` method with key conversion
   - Implement `get()` method with optional default
   - Implement `__contains__()` for membership testing
   - Make related tests pass
   - **Commit**: `"feat: implement insert and get operations"`

5. **Implement removal operations**:
   - Implement `remove()` with KeyError handling
   - Implement `__delitem__()` with KeyError handling
   - Implement `clear()`
   - Make removal tests pass
   - **Commit**: `"feat: implement remove and clear operations"`

6. **Implement dict-like interface**:
   - Implement `__getitem__()` and `__setitem__()`
   - Implement `__len__()`
   - Implement `is_empty()`
   - Make dict interface tests pass
   - **Commit**: `"feat: implement dictionary-like interface"`

7. **Implement string representation**:
   - Implement `__repr__()` and `__str__()`
   - Make representation tests pass
   - **Commit**: `"feat: implement string representation"`

8. **Add type stubs** (`python/blart/__init__.pyi`):
   - Add type hints for all implemented methods
   - **Commit**: `"docs: add type stubs for basic operations"`

**Deliverables**:
- Full test suite for basic operations (20+ tests)
- Working TreeMap with CRUD operations
- All basic operation tests passing
- Type stubs for IDE support
- 8+ git commits documenting progress

---

### Phase 3: Iteration Support
**Goal**: Enable Python iteration over TreeMap contents

**TDD Steps**:

1. **Write iteration tests** (`tests/test_iteration.py`):
   ```python
   # Basic iteration
   def test_iter_keys()
   def test_iter_empty_treemap()
   def test_iter_preserves_order()

   # Specialized iterators
   def test_keys_method()
   def test_values_method()
   def test_items_method()
   def test_items_returns_tuples()

   # Iterator behavior
   def test_multiple_iterations()
   def test_iterator_exhaustion()
   def test_modify_during_iteration()  # should work or raise clear error

   # Edge cases
   def test_iterate_large_treemap()
   def test_iterate_unicode_keys()
   ```
   - **Commit**: `"test: add comprehensive iteration tests"`

2. **Implement basic key iteration**:
   - Create `PyTreeMapIter` struct in `src/iterators.rs`
   - Implement `__iter__()` on `PyTreeMap` returning `PyTreeMapIter`
   - Implement `__next__()` on `PyTreeMapIter`
   - Make basic iteration tests pass
   - **Commit**: `"feat: implement basic key iteration"`

3. **Implement specialized iterators**:
   - Create `PyTreeMapKeys`, `PyTreeMapValues`, `PyTreeMapItems` structs
   - Implement `.keys()`, `.values()`, `.items()` methods
   - Make specialized iterator tests pass
   - **Commit**: `"feat: implement keys(), values(), and items() iterators"`

4. **Update type stubs**:
   - Add iterator type hints to `.pyi` file
   - **Commit**: `"docs: add type stubs for iteration support"`

**Deliverables**:
- Full iteration test suite (10+ tests)
- All iterator types working
- All iteration tests passing
- 4 git commits

---

### Phase 4: Advanced Features - Prefix Queries
**Goal**: Implement prefix query functionality (blart's killer feature)

**TDD Steps**:

1. **Write prefix query tests** (`tests/test_prefix.py`):
   ```python
   def test_get_prefix_first_match()
   def test_get_prefix_no_match()
   def test_prefix_iter_multiple_matches()
   def test_prefix_iter_preserves_order()
   def test_prefix_iter_empty_result()
   def test_prefix_with_exact_match()
   def test_prefix_with_unicode()
   ```
   - **Commit**: `"test: add prefix query tests"`

2. **Implement get_prefix()**:
   - Add `get_prefix(prefix: str)` method to `PyTreeMap`
   - Make get_prefix tests pass
   - **Commit**: `"feat: implement get_prefix() method"`

3. **Implement prefix_iter()**:
   - Create `PyPrefixIter` in `src/iterators.rs`
   - Add `prefix_iter(prefix: str)` method
   - Make prefix iteration tests pass
   - **Commit**: `"feat: implement prefix_iter() method"`

4. **Update type stubs**:
   - Add prefix query type hints
   - **Commit**: `"docs: add type stubs for prefix queries"`

**Deliverables**:
- Prefix query test suite (7+ tests)
- Working prefix queries
- 4 git commits

---

### Phase 5: Advanced Features - Boundary & Fuzzy Operations
**Goal**: Implement remaining advanced features

**TDD Steps**:

1. **Write boundary operation tests** (`tests/test_advanced.py`):
   ```python
   def test_first()
   def test_first_empty()
   def test_last()
   def test_last_empty()
   def test_pop_first()
   def test_pop_last()
   def test_pop_empty_returns_none()
   ```
   - **Commit**: `"test: add boundary operation tests"`

2. **Implement boundary operations**:
   - Implement `first()`, `last()`, `pop_first()`, `pop_last()`
   - Make boundary tests pass
   - **Commit**: `"feat: implement boundary operations (first/last/pop)"`

3. **Write fuzzy search tests** (add to `tests/test_advanced.py`):
   ```python
   def test_fuzzy_search_exact_match()
   def test_fuzzy_search_one_char_diff()
   def test_fuzzy_search_returns_distance()
   def test_fuzzy_search_max_distance()
   def test_fuzzy_search_no_matches()
   ```
   - **Commit**: `"test: add fuzzy search tests"`

4. **Implement fuzzy_search()**:
   - Create `PyFuzzyIter` in `src/iterators.rs`
   - Implement `fuzzy_search(key, max_distance)` method
   - Make fuzzy search tests pass
   - **Commit**: `"feat: implement fuzzy_search() with Levenshtein distance"`

5. **Update type stubs**:
   - Add type hints for all advanced features
   - **Commit**: `"docs: add type stubs for advanced features"`

**Deliverables**:
- Advanced features test suite (12+ tests)
- All advanced features working
- 5 git commits

---

### Phase 6: Error Handling & Edge Cases
**Goal**: Robust error handling and production-ready code

**TDD Steps**:

1. **Write error handling tests** (`tests/test_errors.py`):
   ```python
   def test_keyerror_message_includes_key()
   def test_custom_exception_for_prefix_conflict()
   def test_invalid_key_type_raises_typeerror()
   def test_operations_on_empty_treemap()
   def test_extremely_long_keys()
   def test_special_unicode_characters()
   def test_emoji_keys()
   def test_null_bytes_in_keys()
   ```
   - **Commit**: `"test: add error handling and edge case tests"`

2. **Implement custom exceptions**:
   - Create `src/errors.rs` with custom exception types
   - Implement `From<T> for PyErr` conversions
   - Make error tests pass
   - **Commit**: `"feat: add custom exceptions and error handling"`

3. **Write memory/stress tests** (`tests/test_memory.py`):
   ```python
   def test_large_treemap_memory()
   def test_repeated_insert_delete()
   def test_large_values()
   def test_many_iterations()
   ```
   - **Commit**: `"test: add memory and stress tests"`

4. **Fix any memory issues**:
   - Ensure proper reference counting
   - Fix any leaks discovered
   - Make memory tests pass
   - **Commit**: `"fix: ensure proper memory management"`

5. **Add comprehensive docstrings**:
   - Add docstrings to all Rust `#[pymethods]`
   - Include examples in docstrings
   - **Commit**: `"docs: add comprehensive docstrings to all methods"`

6. **Finalize type stubs**:
   - Complete `.pyi` file with all methods
   - Add generic type support where applicable
   - **Commit**: `"docs: finalize type stubs with complete API"`

**Deliverables**:
- Error handling test suite (8+ tests)
- Memory/stress test suite (4+ tests)
- Custom exceptions working
- All tests passing
- Complete docstrings and type hints
- 6 git commits

---

### Phase 7: Documentation & Examples
**Goal**: User-facing documentation and examples

**Steps** (not strictly TDD):

1. **Create example scripts**:
   - `examples/basic_usage.py` - CRUD operations demo
   - `examples/prefix_queries.py` - Prefix search demo
   - `examples/fuzzy_matching.py` - Fuzzy search demo
   - Test all examples work correctly
   - **Commit**: `"docs: add example scripts"`

2. **Write comprehensive README.md**:
   - Installation instructions
   - Quick start guide
   - API reference (link to docstrings)
   - Performance characteristics
   - Usage examples from examples/
   - **Commit**: `"docs: add comprehensive README"`

3. **Create performance benchmarks** (`tests/test_performance.py`):
   ```python
   def benchmark_insert_vs_dict()
   def benchmark_get_vs_dict()
   def benchmark_prefix_search()
   def benchmark_fuzzy_search()
   def benchmark_iteration()
   ```
   - Run benchmarks and document results in README
   - **Commit**: `"test: add performance benchmarks"`

4. **Test coverage report**:
   - Run `pytest --cov=blart-py tests/`
   - Ensure >90% coverage
   - Add coverage badge to README if desired
   - **Commit**: `"test: verify >90% test coverage"`

**Deliverables**:
- Working example scripts (3+)
- Comprehensive README
- Performance benchmarks
- >90% test coverage verified
- 4 git commits

---

### Phase 8: Build & Distribution
**Goal**: Prepare for release and distribution

**Steps**:

1. **Create CI/CD configuration** (`.github/workflows/ci.yml`):
   - Test job: Run pytest on multiple Python versions (3.8-3.12)
   - Test job: Run on multiple OS (Linux, macOS, Windows)
   - Lint job: cargo clippy, ruff
   - Format check: cargo fmt, black
   - **Commit**: `"ci: add GitHub Actions CI pipeline"`

2. **Create build workflow** (`.github/workflows/build.yml`):
   - Configure maturin for multi-platform wheel building
   - Build for Python 3.8-3.12
   - Build for Linux, macOS, Windows
   - Upload wheels as artifacts
   - **Commit**: `"ci: add wheel building workflow"`

3. **Add development tooling**:
   - Create `Makefile` or `justfile` with common commands:
     - `make dev` - Run maturin develop
     - `make test` - Run pytest
     - `make lint` - Run all linters
     - `make format` - Format all code
   - Optional: Create pre-commit hooks configuration
   - **Commit**: `"chore: add development tooling and scripts"`

4. **Test release build**:
   - Run `maturin build --release`
   - Test wheel installation locally
   - Verify all features work in installed wheel
   - **Commit**: `"build: verify release build works"`

5. **Prepare for distribution** (optional):
   - Add LICENSE file
   - Add CHANGELOG.md
   - Update pyproject.toml with complete metadata (author, license, URLs)
   - Create release checklist document
   - **Commit**: `"chore: prepare for distribution"`

**Deliverables**:
- Working CI/CD pipeline
- Multi-platform wheel building
- Development tooling
- Release-ready package
- 5 git commits

---

## Key Technical Decisions

### Architecture Decisions

**Key Type**: String keys only (UTF-8)
- Rationale: Simplest and most common use case, matches Python dict behavior
- Keys converted to UTF-8 bytes internally via `Box<[u8]>`
- Future: Could extend to support bytes keys

**Value Type**: PyObject for maximum flexibility
- Rationale: Allows any Python object as values
- Handles reference counting automatically
- No conversion overhead for Python objects

**PREFIX_LEN Constant**: Use default (16)
- Rationale: Good balance for most use cases
- Simplifies implementation (no runtime configuration)
- Future: Could expose as creation parameter if needed

**Allocator**: Use default Global allocator
- Rationale: Simpler integration, good enough performance
- Avoid nightly Rust features
- Future: Could optimize with custom allocator

**Module naming**: Use nested module pattern (`blart._blart`)
- Rationale: Avoids double-import confusion (prevents `from blart import blart`)
- Cleaner API: `from blart import TreeMap` instead of `from blart import blart`
- Encapsulates Rust implementation details as private submodule
- Follows maturin best practices for mixed Rust/Python projects

### Error Handling Strategy

- Map Rust `Result` types to Python exceptions via `PyResult`
- Create custom exception types for domain-specific errors
- Use `?` operator for automatic error propagation
- Provide detailed error messages with context

### Iteration Strategy

- Return cloned data initially for simplicity
- Avoid lifetime complexity in first version
- Consider zero-copy iteration in future optimization
- Use `Option<T>` return from `__next__` (simpler than PyStopIteration)

### Build System

- **Tool**: maturin (standard for PyO3 projects)
- **Rationale**:
  - Built specifically for PyO3
  - Handles wheel building and PyPI uploads
  - Supports PEP 517/518
  - Active development and community

---

## File Structure

```
blart-py/
├── Cargo.toml              # Rust package configuration
├── pyproject.toml          # Python package config (maturin)
├── README.md               # Project documentation
├── IMPLEMENTATION_PLAN.md  # This file
├── CLAUDE.md               # Claude development guidelines
├── .gitignore              # Git ignore patterns
├── LICENSE                 # Project license (Phase 8)
├── CHANGELOG.md            # Version history (Phase 8)
├── Makefile                # Development commands (Phase 8)
├── .github/
│   └── workflows/
│       ├── ci.yml          # CI/CD pipeline (Phase 8)
│       └── build.yml       # Wheel building (Phase 8)
├── src/
│   ├── lib.rs             # PyO3 module definition (#[pymodule])
│   ├── treemap.rs         # PyTreeMap wrapper implementation
│   ├── iterators.rs       # Iterator wrapper implementations
│   ├── errors.rs          # Error type conversions
│   └── utils.rs           # Helper functions (if needed)
├── python/
│   └── blart/
│       ├── __init__.py    # Python package initialization
│       ├── __init__.pyi   # Type stubs for IDE support
│       └── py.typed       # PEP 561 marker file
├── tests/                 # ⚠️ Created BEFORE implementation (TDD)
│   ├── conftest.py        # Pytest configuration (Phase 1)
│   ├── test_import.py     # Smoke tests (Phase 1)
│   ├── test_basic.py      # Basic operations tests (Phase 2)
│   ├── test_iteration.py  # Iterator tests (Phase 3)
│   ├── test_prefix.py     # Prefix query tests (Phase 4)
│   ├── test_advanced.py   # Advanced features tests (Phase 5)
│   ├── test_errors.py     # Error handling tests (Phase 6)
│   ├── test_memory.py     # Memory/stress tests (Phase 6)
│   └── test_performance.py # Benchmarks (Phase 7)
├── examples/              # Created in Phase 7
│   ├── basic_usage.py
│   ├── prefix_queries.py
│   └── fuzzy_matching.py
└── benches/               # Optional Rust benchmarks
    └── benchmark.rs
```

**TDD File Creation Order**:
1. Project structure files (Cargo.toml, pyproject.toml, etc.)
2. Test files (tests/*.py) - **CREATED FIRST**
3. Implementation files (src/*.rs) - Created after tests
4. Documentation files (examples/, README.md) - Created last

---

## Development Workflow

### Initial Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install maturin
pip install maturin

# Install development dependencies
pip install pytest pytest-cov black ruff mypy hypothesis
```

### TDD Development Cycle

**For each feature:**

1. **Write tests first**:
   ```bash
   # Edit test file (e.g., tests/test_basic.py)
   # Write tests defining expected behavior
   ```

2. **Run tests (they should fail)**:
   ```bash
   pytest tests/test_basic.py -v
   # Tests fail because implementation doesn't exist yet
   ```

3. **Create minimal interface**:
   ```bash
   # Edit Rust source files
   # Add method stubs that compile but don't work yet
   maturin develop  # Build and install
   pytest tests/test_basic.py -v
   # Tests should still fail, but with better error messages
   ```

4. **Implement functionality**:
   ```bash
   # Edit Rust source files
   # Implement actual functionality
   maturin develop  # Rebuild
   pytest tests/test_basic.py -v
   # Tests should pass now
   ```

5. **Refactor if needed**:
   ```bash
   # Clean up code, improve structure
   cargo fmt  # Format Rust code
   cargo clippy  # Check for issues
   maturin develop  # Rebuild
   pytest tests/test_basic.py -v
   # Tests still pass
   ```

6. **Commit the milestone**:
   ```bash
   git add .
   git commit -m "feat: implement insert and get operations"
   ```

### Running Tests
```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_basic.py -v

# Run tests with coverage
pytest --cov=blart-py tests/

# Run tests matching pattern
pytest tests/ -k "test_insert"
```

### Code Quality
```bash
# Format code
cargo fmt
black python/ tests/ examples/

# Lint code
cargo clippy
ruff check python/ tests/ examples/

# Type check
mypy python/
```

### Building Release
```bash
# Build release wheels
maturin build --release

# Build for specific Python version
maturin build --release --interpreter python3.11

# Build for all supported versions
maturin build --release --compatibility manylinux2014
```

### Testing Locally
```bash
# Install from wheel
pip install target/wheels/blart-*.whl

# Run examples
python examples/basic_usage.py
```

---

## Dependencies

### Rust (Cargo.toml)
```toml
[package]
name = "blart-py"
version = "0.1.0"
edition = "2021"

[dependencies]
pyo3 = { version = "0.22", features = ["extension-module"] }
blart = "0.4"

[lib]
name = "_blart"
crate-type = ["cdylib"]
```

### Python (pyproject.toml)
```toml
[build-system]
requires = ["maturin>=1.0,<2.0"]
build-backend = "maturin"

[project]
name = "blart"
version = "0.1.0"
description = "Python wrapper for blart adaptive radix tree"
requires-python = ">=3.8"
classifiers = [
    "Programming Language :: Rust",
    "Programming Language :: Python :: Implementation :: CPython",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
]

[tool.maturin]
features = ["pyo3/extension-module"]
python-source = "python"
module-name = "blart._blart"
```

---

## Success Criteria

### Phase Completion
- [ ] All 8 phases completed in order
- [ ] All tests passing on all supported platforms
- [ ] 35+ git commits with meaningful messages
- [ ] Documentation complete and accurate
- [ ] Performance benchmarks meet expectations

### TDD Compliance
- [ ] Every feature has tests written before implementation
- [ ] No commits with failing tests (except initial test commits)
- [ ] All test files created before implementation files
- [ ] Commit messages follow conventional commit format

### Test Suite Quality
- [ ] 50+ tests covering all functionality
- [ ] Test coverage >90%
- [ ] All edge cases covered (Unicode, empty, large data, etc.)
- [ ] Memory leak tests passing
- [ ] Performance benchmarks documented

### Code Quality
- [ ] All clippy warnings resolved
- [ ] Code formatted with cargo fmt and black
- [ ] Type hints complete and verified (.pyi files)
- [ ] Comprehensive docstrings on all public methods
- [ ] No memory leaks detected

### Performance Goals
- [ ] Faster than Python dict for large datasets
- [ ] Prefix queries significantly faster than linear search
- [ ] Memory usage competitive with BTreeMap
- [ ] Iteration performance acceptable

### User Experience
- [ ] Installation via `pip install blart-py` works
- [ ] API intuitive for Python developers
- [ ] Error messages clear and actionable
- [ ] Examples run without modification
- [ ] Type hints work in IDEs (VSCode, PyCharm)

---

## Future Enhancements

### Short-term
- Support for bytes keys in addition to str
- Range query support with inclusive/exclusive bounds
- Entry API for efficient upsert patterns
- Parallel iteration support

### Medium-term
- Async/await support for IO-bound operations
- Serialization/deserialization (pickle, JSON)
- Memory-mapped file backend
- Custom key types via protocol

### Long-term
- Multi-version concurrency control (MVCC)
- Persistent tree with transaction support
- Distributed variant with network sync
- GPU-accelerated fuzzy search

---

## Risk Mitigation

### Technical Risks
- **Lifetime complexity**: Start simple, optimize later
- **Memory leaks**: Extensive testing with valgrind/ASAN
- **Thread safety**: Document limitations, add tests
- **Performance regression**: Continuous benchmarking

### Project Risks
- **Scope creep**: Stick to phases, defer enhancements
- **PyO3 API changes**: Pin versions, test upgrades
- **Platform compatibility**: CI/CD on all platforms
- **Documentation drift**: Keep code and docs together

---

## References

### Documentation
- PyO3 Guide: https://pyo3.rs/
- Blart crate: https://docs.rs/blart/
- Maturin Guide: https://www.maturin.rs/
- Python C API: https://docs.python.org/3/c-api/

### Related Projects
- polars (PyO3 success story)
- cryptography (Rust+Python)
- pydantic-core (performance-critical PyO3)

---

## Appendix: Code Examples

### Minimal PyTreeMap Skeleton (Rust)
```rust
use pyo3::prelude::*;
use blart::TreeMap;

#[pyclass]
struct PyTreeMap {
    inner: TreeMap<Box<[u8]>, PyObject>,
}

#[pymethods]
impl PyTreeMap {
    #[new]
    fn new() -> Self {
        Self {
            inner: TreeMap::new(),
        }
    }

    fn insert(&mut self, py: Python, key: String, value: PyObject) -> PyResult<()> {
        let key_bytes = key.into_bytes().into_boxed_slice();
        self.inner.try_insert(key_bytes, value)
            .map_err(|_| PyErr::new::<pyo3::exceptions::PyKeyError, _>("Key exists"))?;
        Ok(())
    }

    fn get(&self, py: Python, key: String) -> PyResult<Option<PyObject>> {
        let key_bytes = key.as_bytes();
        Ok(self.inner.get(key_bytes).map(|v| v.clone()))
    }
}

#[pymodule]
fn _blart(_py: Python, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<PyTreeMap>()?;
    Ok(())
}
```

### Python Package Initialization
```python
# python/blart/__init__.py
"""High-performance adaptive radix tree for Python."""

from blart._blart import PyTreeMap as TreeMap

__all__ = ["TreeMap"]
```

### Expected Python API
```python
from blart import TreeMap

# Basic usage
tree = TreeMap()
tree["hello"] = "world"
print(tree["hello"])  # "world"

# Iteration
for key in tree:
    print(key, tree[key])

# Prefix queries
tree["apple"] = 1
tree["application"] = 2
tree["apply"] = 3
for key, value in tree.prefix_iter("app"):
    print(key, value)  # application, apple, apply

# Fuzzy matching
for key, value, distance in tree.fuzzy_search("aple", max_distance=1):
    print(f"{key}: {value} (distance: {distance})")
```
