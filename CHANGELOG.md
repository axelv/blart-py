# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2024-11-14

### Added

- Initial release of blart-py
- Core TreeMap implementation with dictionary-like interface
- Full iteration support (keys, values, items)
- Prefix query functionality
- Fuzzy search with Levenshtein distance
- Boundary operations (first, last, pop_first, pop_last)
- Comprehensive error handling with custom exceptions
- Type stubs for IDE support
- Complete documentation and examples
- Performance benchmarks
- CI/CD pipeline with GitHub Actions
- Multi-platform wheel building (Linux, macOS, Windows)
- Support for Python 3.8-3.12

### Features

#### Basic Operations
- `TreeMap()` - Create new tree
- `tree[key] = value` - Insert/update items
- `tree[key]` - Get items
- `del tree[key]` - Remove items
- `key in tree` - Membership testing
- `len(tree)` - Get size
- `tree.clear()` - Clear all items

#### Iteration
- `for key in tree` - Iterate over keys
- `tree.keys()` - Get keys iterator
- `tree.values()` - Get values iterator
- `tree.items()` - Get (key, value) pairs iterator

#### Advanced Features
- `tree.prefix_iter(prefix)` - Iterate over keys with prefix
- `tree.get_prefix(prefix)` - Get first key with prefix
- `tree.fuzzy_search(key, max_distance)` - Fuzzy matching with Levenshtein distance
- `tree.first()` - Get first (key, value) pair
- `tree.last()` - Get last (key, value) pair
- `tree.pop_first()` - Remove and return first pair
- `tree.pop_last()` - Remove and return last pair

### Performance

- Competitive with Python dict for basic operations
- Significantly faster than linear search for prefix queries
- Memory efficient with adaptive radix tree structure
- Optimized Rust implementation using blart library

### Documentation

- Comprehensive README with examples
- API documentation with docstrings
- Example scripts demonstrating all features
- Performance benchmarks and results

### Development

- TDD approach with 50+ tests
- >90% test coverage
- Full type hints and .pyi stub files
- Makefile for common development tasks
- CI/CD with automated testing and wheel building

[Unreleased]: https://github.com/axelv/blart-py/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/axelv/blart-py/releases/tag/v0.1.0
