"""Comprehensive tests for TreeMap iteration support."""

import pytest
from blart import TreeMap


# Basic iteration
def test_iter_keys():
    """Test basic iteration over keys."""
    tree = TreeMap({"apple": 1, "banana": 2, "cherry": 3})
    keys = list(tree)
    assert len(keys) == 3
    assert "apple" in keys
    assert "banana" in keys
    assert "cherry" in keys


def test_iter_empty_treemap():
    """Test iteration over empty TreeMap."""
    tree = TreeMap()
    keys = list(tree)
    assert keys == []


def test_iter_preserves_order():
    """Test that iteration preserves lexicographic order."""
    tree = TreeMap()
    tree["dog"] = 1
    tree["apple"] = 2
    tree["zebra"] = 3
    tree["banana"] = 4

    keys = list(tree)
    # Radix tree should preserve lexicographic order
    assert keys == sorted(keys)


# Specialized iterators
def test_keys_method():
    """Test keys() method returns iterable of keys."""
    tree = TreeMap({"apple": 1, "banana": 2, "cherry": 3})
    keys = list(tree.keys())
    assert len(keys) == 3
    assert "apple" in keys
    assert "banana" in keys
    assert "cherry" in keys


def test_values_method():
    """Test values() method returns iterable of values."""
    tree = TreeMap({"apple": 1, "banana": 2, "cherry": 3})
    values = list(tree.values())
    assert len(values) == 3
    assert 1 in values
    assert 2 in values
    assert 3 in values


def test_items_method():
    """Test items() method returns iterable of (key, value) pairs."""
    tree = TreeMap({"apple": 1, "banana": 2, "cherry": 3})
    items = list(tree.items())
    assert len(items) == 3
    assert ("apple", 1) in items
    assert ("banana", 2) in items
    assert ("cherry", 3) in items


def test_items_returns_tuples():
    """Test that items() returns actual tuples."""
    tree = TreeMap({"apple": 1})
    items = list(tree.items())
    assert len(items) == 1
    item = items[0]
    assert isinstance(item, tuple)
    assert len(item) == 2
    assert item[0] == "apple"
    assert item[1] == 1


# Iterator behavior
def test_multiple_iterations():
    """Test that TreeMap can be iterated multiple times."""
    tree = TreeMap({"apple": 1, "banana": 2})
    keys1 = list(tree)
    keys2 = list(tree)
    assert keys1 == keys2


def test_iterator_exhaustion():
    """Test that iterator can be exhausted and recreated."""
    tree = TreeMap({"apple": 1, "banana": 2})
    iterator = iter(tree)

    # Exhaust the iterator
    keys = list(iterator)
    assert len(keys) == 2

    # Calling next on exhausted iterator should raise StopIteration
    with pytest.raises(StopIteration):
        next(iterator)

    # New iterator should work
    new_iterator = iter(tree)
    new_keys = list(new_iterator)
    assert len(new_keys) == 2


def test_modify_during_iteration():
    """Test behavior when modifying TreeMap during iteration."""
    tree = TreeMap({"apple": 1, "banana": 2, "cherry": 3})

    # This test documents the behavior - either:
    # 1. Iteration should work with a snapshot (no error)
    # 2. Should raise a clear error about modification during iteration

    # For now, we expect iteration to work with a snapshot
    # since we're cloning data in the iterator
    keys = []
    for key in tree:
        keys.append(key)
        if key == "banana":
            tree["new_key"] = 99  # Modify during iteration

    # Should have iterated over original 3 keys
    assert len(keys) == 3
    # New key should be present after iteration
    assert "new_key" in tree


# Edge cases
def test_iterate_large_treemap():
    """Test iteration over a large TreeMap."""
    tree = TreeMap()
    n = 1000
    for i in range(n):
        tree[f"key_{i:05d}"] = i

    keys = list(tree)
    assert len(keys) == n
    # Check ordering is preserved
    assert keys == sorted(keys)


def test_iterate_unicode_keys():
    """Test iteration with Unicode keys."""
    tree = TreeMap()
    tree["Ключ"] = "Russian"
    tree["键"] = "Chinese"
    tree["مفتاح"] = "Arabic"
    tree["🔑"] = "Emoji"

    keys = list(tree)
    assert len(keys) == 4
    assert "Ключ" in keys
    assert "键" in keys
    assert "مفتاح" in keys
    assert "🔑" in keys


def test_values_preserves_order():
    """Test that values() preserves order corresponding to keys."""
    tree = TreeMap()
    tree["apple"] = 1
    tree["banana"] = 2
    tree["cherry"] = 3

    keys = list(tree.keys())
    values = list(tree.values())
    items = list(tree.items())

    # Values should correspond to keys in same order
    for i, (key, value) in enumerate(items):
        assert keys[i] == key
        assert values[i] == value


def test_empty_iterations():
    """Test that all iteration methods work on empty TreeMap."""
    tree = TreeMap()
    assert list(tree) == []
    assert list(tree.keys()) == []
    assert list(tree.values()) == []
    assert list(tree.items()) == []


def test_single_item_iteration():
    """Test iteration with single item."""
    tree = TreeMap({"single": "value"})

    assert list(tree) == ["single"]
    assert list(tree.keys()) == ["single"]
    assert list(tree.values()) == ["value"]
    assert list(tree.items()) == [("single", "value")]


def test_iteration_with_none_values():
    """Test iteration when TreeMap contains None values."""
    tree = TreeMap({"key1": None, "key2": "value", "key3": None})

    keys = list(tree.keys())
    values = list(tree.values())
    items = list(tree.items())

    assert len(keys) == 3
    assert len(values) == 3
    assert len(items) == 3

    # None values should be preserved
    assert values.count(None) == 2
    assert ("key1", None) in items
    assert ("key3", None) in items
