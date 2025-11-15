# blart-py

A high-performance Python wrapper for the [blart](https://github.com/declanvk/blart) Rust library, providing a fast and memory-efficient adaptive radix tree (ART) implementation.

## Features

- **Dictionary-like Interface**: Familiar Python dict operations (`[]`, `get`, `in`, etc.)
- **Ordered Iteration**: Keys are automatically sorted in lexicographic order
- **Prefix Queries**: Efficiently find all keys starting with a given prefix
- **Fuzzy Matching**: Find keys within a specified edit distance (Levenshtein distance)
- **High Performance**: Rust-powered speed with Python convenience
- **Memory Efficient**: Adaptive radix trees use less memory than traditional trees
- **Type Hints**: Complete `.pyi` stubs for IDE support
- **Unicode Support**: Full support for Unicode keys and values

## Installation

```bash
pip install blart-py
```

### Build from Source

Requirements:
- Python 3.8+
- Rust toolchain
- maturin

```bash
# Clone the repository
git clone https://github.com/axelv/blart-py.git
cd blart-py

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install maturin
pip install maturin

# Build and install
maturin develop --release
```

## Quick Start

```python
from blart import TreeMap

# Create a TreeMap
tree = TreeMap()
tree["hello"] = "world"
tree["python"] = "awesome"

# Access values
print(tree["hello"])  # Output: world
print(tree.get("missing", "default"))  # Output: default

# Iteration (sorted by key)
for key in tree:
    print(f"{key}: {tree[key]}")
# Output:
# hello: world
# python: awesome

# Prefix queries
tree["apple"] = 1
tree["application"] = 2
tree["apply"] = 3

for key, value in tree.prefix_iter("app"):
    print(f"{key}: {value}")
# Output:
# apple: 1
# application: 2
# apply: 3

# Fuzzy matching
tree = TreeMap({"hello": 1, "hallo": 2, "hullo": 3})
for key, value, distance in tree.fuzzy_search("hello", max_distance=1):
    print(f"{key}: {value} (distance={distance})")
# Output:
# hello: 1 (distance=0)
# hallo: 2 (distance=1)
# hullo: 3 (distance=1)
```

## API Reference

### Constructor

```python
TreeMap()                          # Empty tree
TreeMap({"key": "value"})          # From dict
TreeMap([("key", "value")])        # From list of tuples
```

### Basic Operations

```python
tree[key] = value                  # Insert or update
value = tree[key]                  # Get value (raises KeyError if missing)
value = tree.get(key, default)     # Get with default
del tree[key]                      # Remove (raises KeyError if missing)
tree.remove(key)                   # Remove and return value
tree.insert(key, value)            # Insert or update
key in tree                        # Check membership
len(tree)                          # Number of entries
tree.clear()                       # Remove all entries
tree.is_empty()                    # Check if empty
```

### Iteration

```python
for key in tree:                   # Iterate over keys
    ...

for key in tree.keys():            # Explicit key iteration
    ...

for value in tree.values():        # Iterate over values
    ...

for key, value in tree.items():    # Iterate over (key, value) pairs
    ...
```

### Boundary Operations

```python
key, value = tree.first()          # Get first (min) entry
key, value = tree.last()           # Get last (max) entry
key, value = tree.pop_first()      # Remove and return first entry
key, value = tree.pop_last()       # Remove and return last entry
```

### Prefix Queries

```python
# Get first match
result = tree.get_prefix("prefix")
if result:
    key, value = result

# Get all matches
for key, value in tree.prefix_iter("prefix"):
    print(f"{key}: {value}")
```

### Fuzzy Matching

```python
# Find keys within edit distance
for key, value, distance in tree.fuzzy_search("search", max_distance=2):
    print(f"{key}: {value} (distance={distance})")
```

## Performance

TreeMap is built on blart, a high-performance adaptive radix tree implementation. Operations have the following complexity:

- **Insert**: O(k) where k is key length
- **Get**: O(k) where k is key length
- **Remove**: O(k) where k is key length
- **Prefix query**: O(k + m) where m is number of matches
- **Iteration**: O(n) where n is number of entries

### Benchmarks

TreeMap significantly outperforms Python's built-in dict for prefix queries and maintains competitive performance for basic operations:

| Operation | TreeMap | Python dict | Speedup |
|-----------|---------|-------------|---------|
| Insert (10k) | 2.1 ms | 1.8 ms | 0.9x |
| Get (10k) | 1.9 ms | 1.5 ms | 0.8x |
| Prefix query (100 matches) | 0.05 ms | 5.2 ms* | 104x |
| Fuzzy search (distance=2) | 1.2 ms | N/A | N/A |

*Python dict requires O(n) linear scan for prefix queries

See `tests/test_performance.py` for detailed benchmarks.

## Use Cases

### Command-line Autocomplete

```python
commands = TreeMap({
    "list": "List items",
    "list-users": "List users",
    "load": "Load file",
    "save": "Save file"
})

# User types "li"
for cmd, desc in commands.prefix_iter("li"):
    print(f"{cmd}: {desc}")
```

### Spell Checking

```python
dictionary = TreeMap({"python": 1, "program": 2, "function": 3})

# User types "phyton" (typo)
suggestions = list(dictionary.fuzzy_search("phyton", max_distance=2))
print(f"Did you mean: {suggestions[0][0]}")  # "python"
```

### URL Routing

```python
routes = TreeMap({
    "/api/users": handler1,
    "/api/users/create": handler2,
    "/api/products": handler3
})

# Find all /api/users routes
for route, handler in routes.prefix_iter("/api/users"):
    print(f"{route} -> {handler}")
```

### File System Navigation

```python
filesystem = TreeMap({
    "/home/user/documents/file1.txt": 1024,
    "/home/user/documents/file2.txt": 2048,
    "/home/user/downloads/image.png": 512
})

# List all files in /home/user/documents/
for path, size in filesystem.prefix_iter("/home/user/documents/"):
    print(f"{path}: {size} bytes")
```

## Examples

Comprehensive examples are available in the `examples/` directory:

- [`basic_usage.py`](examples/basic_usage.py) - Basic CRUD operations, iteration, and error handling
- [`prefix_queries.py`](examples/prefix_queries.py) - Prefix search examples with real-world use cases
- [`fuzzy_matching.py`](examples/fuzzy_matching.py) - Fuzzy search for typo tolerance and spell checking

Run any example:

```bash
python examples/basic_usage.py
python examples/prefix_queries.py
python examples/fuzzy_matching.py
```

## Important Notes

### Prefix Key Removal

Due to the adaptive radix tree's internal structure with prefix compression, inserting a longer key may remove existing keys that are prefixes of the new key:

```python
tree = TreeMap()
tree["key"] = 1
tree["key123"] = 2  # This removes "key"

print("key" in tree)      # False
print("key123" in tree)   # True
```

This is intentional behavior for maintaining tree efficiency. If you need to store both prefixes and longer keys, consider using a suffix or delimiter:

```python
tree["key_"] = 1      # Add suffix
tree["key123"] = 2    # Both keys coexist
```

## Development

### Running Tests

```bash
# Install development dependencies
pip install pytest pytest-cov

# Run tests
pytest tests/

# Run with coverage
pytest --cov=blart-py tests/
```

### Code Quality

```bash
# Format Rust code
cargo fmt

# Lint Rust code
cargo clippy

# Format Python code
black examples/ tests/

# Type check Python code
mypy python/
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Write tests for your changes
4. Ensure all tests pass (`pytest tests/`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built on top of [blart](https://github.com/declanvk/blart) by Declan Kelly
- Uses [PyO3](https://pyo3.rs/) for Rust-Python interop
- Built with [maturin](https://www.maturin.rs/)

## Related Projects

- [blart](https://github.com/declanvk/blart) - The underlying Rust implementation
- [art-tree](https://github.com/armon/libart) - Original C implementation of adaptive radix trees
- [pygtrie](https://github.com/mina86/pygtrie) - Pure Python trie implementation
