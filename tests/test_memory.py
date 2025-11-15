"""Test memory management and stress testing for TreeMap."""

import gc
import sys
from blart import TreeMap


def test_large_treemap_memory():
    """Test TreeMap with large number of entries."""
    tree = TreeMap()
    n = 50000

    # Insert many entries
    for i in range(n):
        tree[f"key_{i:06d}"] = i

    assert len(tree) == n

    # Verify some random accesses
    assert tree["key_000000"] == 0
    assert tree["key_025000"] == 25000
    assert tree["key_049999"] == 49999

    # Clean up
    tree.clear()
    assert len(tree) == 0


def test_repeated_insert_delete():
    """Test repeated insertion and deletion cycles."""
    tree = TreeMap()

    # Multiple cycles of insert and delete
    for cycle in range(5):
        # Insert 1000 items
        for i in range(1000):
            tree[f"cycle_{cycle}_key_{i:04d}"] = i

        # Delete half of them
        for i in range(0, 1000, 2):
            del tree[f"cycle_{cycle}_key_{i:04d}"]

        # Verify state
        assert len(tree) == 500 + (cycle * 500)

    # Clean up
    tree.clear()
    gc.collect()


def test_large_values():
    """Test TreeMap with large values."""
    tree = TreeMap()

    # Create large values (1MB strings)
    large_value = "x" * (1024 * 1024)

    # Insert several large values
    for i in range(10):
        tree[f"large_key_{i}"] = large_value

    assert len(tree) == 10

    # Verify values are correct
    for i in range(10):
        assert len(tree[f"large_key_{i}"]) == 1024 * 1024

    # Delete them
    for i in range(10):
        del tree[f"large_key_{i}"]

    assert len(tree) == 0
    gc.collect()


def test_many_iterations():
    """Test multiple iterations over the same TreeMap."""
    tree = TreeMap()

    # Insert data
    for i in range(1000):
        tree[f"key_{i:04d}"] = i

    # Perform many iterations
    for _ in range(100):
        count = 0
        for key in tree:
            count += 1
        assert count == 1000

    # Also test other iterators
    for _ in range(100):
        keys = list(tree.keys())
        assert len(keys) == 1000

    for _ in range(100):
        values = list(tree.values())
        assert len(values) == 1000

    for _ in range(100):
        items = list(tree.items())
        assert len(items) == 1000


def test_reference_counting():
    """Test that Python objects are properly reference counted."""
    tree = TreeMap()

    # Create a list and get its refcount
    test_list = [1, 2, 3, 4, 5]
    initial_refcount = sys.getrefcount(test_list)

    # Insert the list
    tree["key1"] = test_list
    after_insert_refcount = sys.getrefcount(test_list)

    # Refcount should increase by at least 1 (tree holds a reference)
    assert after_insert_refcount > initial_refcount

    # Get the value back
    retrieved = tree["key1"]
    assert retrieved is test_list

    # Remove from tree
    del tree["key1"]
    after_delete_refcount = sys.getrefcount(test_list)

    # Refcount should decrease back (within 1 due to temporary refs)
    assert abs(after_delete_refcount - initial_refcount) <= 1


def test_circular_reference_handling():
    """Test that circular references don't cause issues."""
    tree = TreeMap()

    # Create a circular reference
    obj = {"tree": tree}
    tree["self_ref"] = obj

    # Should be able to access it
    assert tree["self_ref"]["tree"] is tree

    # Clean up
    del tree["self_ref"]
    del obj


def test_treemap_garbage_collection():
    """Test that TreeMaps can be garbage collected."""
    # Note: PyO3 classes don't support weak references by default
    # This test verifies that deletion and GC work without crashes

    # Create a tree
    tree = TreeMap()
    for i in range(1000):
        tree[f"key_{i:04d}"] = i

    assert len(tree) == 1000

    # Delete the tree and force garbage collection
    del tree
    gc.collect()

    # If we reach here without crashing, GC worked
    assert True


def test_nested_treemaps():
    """Test TreeMaps containing other TreeMaps."""
    outer = TreeMap()

    # Create nested TreeMaps
    for i in range(10):
        inner = TreeMap()
        for j in range(10):
            inner[f"inner_key_{j}"] = j
        outer[f"outer_key_{i}"] = inner

    # Verify structure
    assert len(outer) == 10
    for i in range(10):
        inner = outer[f"outer_key_{i}"]
        assert len(inner) == 10
        assert inner["inner_key_5"] == 5


def test_unicode_value_memory():
    """Test memory handling with Unicode values."""
    tree = TreeMap()

    # Various Unicode strings
    unicode_values = [
        "Hello 世界",
        "🚀🌟✨",
        "Привет мир",
        "مرحبا بالعالم",
        "こんにちは世界",
        "안녕하세요 세계",
    ]

    # Insert many Unicode values
    for i in range(1000):
        for j, uval in enumerate(unicode_values):
            tree[f"key_{i}_{j}"] = uval

    assert len(tree) == 1000 * len(unicode_values)

    # Verify some values
    assert tree["key_500_0"] == unicode_values[0]
    assert tree["key_500_1"] == unicode_values[1]

    # Clean up
    tree.clear()
    gc.collect()


def test_stress_prefix_operations():
    """Stress test prefix operations."""
    tree = TreeMap()

    # Insert many keys with common prefixes
    prefixes = ["app", "apple", "application", "banana", "band", "bandana"]
    for prefix in prefixes:
        for i in range(100):
            tree[f"{prefix}_{i:03d}"] = i

    # Perform many prefix queries
    for _ in range(100):
        results = list(tree.prefix_iter("app"))
        assert len(results) == 300  # app, apple, application * 100

    for _ in range(100):
        results = list(tree.prefix_iter("ban"))
        assert len(results) == 300  # banana, band, bandana * 100


def test_stress_fuzzy_search():
    """Stress test fuzzy search operations."""
    tree = TreeMap()

    # Insert test data
    words = ["hello", "world", "python", "rust", "code", "test"]
    for word in words:
        tree[word] = len(word)

    # Perform many fuzzy searches
    for _ in range(100):
        results = list(tree.fuzzy_search("hello", 2))
        assert len(results) >= 1  # At least "hello" itself

    for _ in range(100):
        results = list(tree.fuzzy_search("wrld", 2))
        # Should find "world" (distance 1)
        assert any(key == "world" for key, _, _ in results)


def test_clear_and_reuse():
    """Test clearing and reusing the same TreeMap."""
    tree = TreeMap()

    for cycle in range(10):
        # Fill the tree with keys that don't have prefix conflicts
        for i in range(1000):
            tree[f"key_{i:04d}"] = i

        assert len(tree) == 1000

        # Clear it
        tree.clear()
        assert len(tree) == 0

        # Verify it's truly empty
        assert list(tree.keys()) == []


def test_memory_efficiency_vs_dict():
    """Compare memory usage with dict (informational test)."""
    import sys

    # Create TreeMap
    tree = TreeMap()
    for i in range(10000):
        tree[f"key_{i:05d}"] = i

    # Create equivalent dict
    d = {}
    for i in range(10000):
        d[f"key_{i:05d}"] = i

    # Get sizes (this is informational, not a strict assertion)
    tree_size = sys.getsizeof(tree)
    dict_size = sys.getsizeof(d)

    # Just verify both work
    assert len(tree) == 10000
    assert len(d) == 10000

    # Print for information (will only show in verbose mode)
    print(f"\nTreeMap size: {tree_size} bytes")
    print(f"Dict size: {dict_size} bytes")
