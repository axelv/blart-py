"""Comprehensive tests for basic TreeMap operations."""

import pytest
from blart import TreeMap


# Constructor tests
def test_treemap_constructor_empty():
    """Test creating an empty TreeMap."""
    tree = TreeMap()
    assert tree is not None
    assert len(tree) == 0
    assert tree.is_empty()


def test_treemap_constructor_from_dict():
    """Test creating TreeMap from a dictionary."""
    tree = TreeMap({"apple": 1, "banana": 2, "cherry": 3})
    assert len(tree) == 3
    assert tree["apple"] == 1
    assert tree["banana"] == 2
    assert tree["cherry"] == 3


def test_treemap_constructor_from_items():
    """Test creating TreeMap from items (list of tuples)."""
    tree = TreeMap([("apple", 1), ("banana", 2), ("cherry", 3)])
    assert len(tree) == 3
    assert tree["apple"] == 1
    assert tree["banana"] == 2
    assert tree["cherry"] == 3


# Basic operations
def test_insert_and_get():
    """Test inserting and retrieving values."""
    tree = TreeMap()
    tree.insert("key1", "value1")
    tree.insert("key2", "value2")
    assert tree.get("key1") == "value1"
    assert tree.get("key2") == "value2"


def test_get_with_default():
    """Test get with default value."""
    tree = TreeMap()
    tree.insert("key1", "value1")
    assert tree.get("key1", "default") == "value1"
    assert tree.get("missing", "default") == "default"


def test_get_missing_key_returns_none():
    """Test that get returns None for missing keys."""
    tree = TreeMap()
    assert tree.get("missing") is None


def test_remove_existing_key():
    """Test removing an existing key."""
    tree = TreeMap()
    tree.insert("key1", "value1")
    tree.insert("key2", "value2")
    result = tree.remove("key1")
    assert result == "value1"
    assert tree.get("key1") is None
    assert tree.get("key2") == "value2"


def test_remove_missing_key_raises_keyerror():
    """Test that remove raises KeyError for missing keys."""
    tree = TreeMap()
    with pytest.raises(KeyError):
        tree.remove("missing")


def test_clear():
    """Test clearing all entries from TreeMap."""
    tree = TreeMap({"key1": "value1", "key2": "value2", "key3": "value3"})
    assert len(tree) == 3
    tree.clear()
    assert len(tree) == 0
    assert tree.is_empty()


def test_len():
    """Test len() function with TreeMap."""
    tree = TreeMap()
    assert len(tree) == 0
    tree.insert("key1", "value1")
    assert len(tree) == 1
    tree.insert("key2", "value2")
    assert len(tree) == 2
    tree.remove("key1")
    assert len(tree) == 1


def test_is_empty():
    """Test is_empty method."""
    tree = TreeMap()
    assert tree.is_empty()
    tree.insert("key1", "value1")
    assert not tree.is_empty()
    tree.remove("key1")
    assert tree.is_empty()


# Dict-like interface
def test_setitem_and_getitem():
    """Test dict-like item access."""
    tree = TreeMap()
    tree["key1"] = "value1"
    tree["key2"] = "value2"
    assert tree["key1"] == "value1"
    assert tree["key2"] == "value2"


def test_getitem_missing_raises_keyerror():
    """Test that accessing missing key raises KeyError."""
    tree = TreeMap()
    with pytest.raises(KeyError):
        _ = tree["missing"]


def test_delitem():
    """Test deleting items using del."""
    tree = TreeMap({"key1": "value1", "key2": "value2"})
    del tree["key1"]
    assert tree.get("key1") is None
    assert tree["key2"] == "value2"


def test_delitem_missing_raises_keyerror():
    """Test that deleting missing key raises KeyError."""
    tree = TreeMap()
    with pytest.raises(KeyError):
        del tree["missing"]


def test_contains():
    """Test 'in' operator for membership testing."""
    tree = TreeMap({"key1": "value1", "key2": "value2"})
    assert "key1" in tree
    assert "key2" in tree
    assert "missing" not in tree


# String representation
def test_repr():
    """Test __repr__ returns valid representation."""
    tree = TreeMap({"apple": 1, "banana": 2})
    repr_str = repr(tree)
    assert "TreeMap" in repr_str or "PyTreeMap" in repr_str


def test_str():
    """Test __str__ returns readable representation."""
    tree = TreeMap({"apple": 1, "banana": 2})
    str_repr = str(tree)
    assert isinstance(str_repr, str)
    assert len(str_repr) > 0


# Edge cases
def test_unicode_keys():
    """Test Unicode keys work correctly."""
    tree = TreeMap()
    tree["Ключ"] = "Russian"
    tree["键"] = "Chinese"
    tree["مفتاح"] = "Arabic"
    assert tree["Ключ"] == "Russian"
    assert tree["键"] == "Chinese"
    assert tree["مفتاح"] == "Arabic"


def test_none_values():
    """Test that None can be stored as a value."""
    tree = TreeMap()
    tree["key1"] = None
    assert tree["key1"] is None
    assert "key1" in tree


def test_various_value_types():
    """Test storing various Python types as values."""
    tree = TreeMap()
    tree["int"] = 42
    tree["float"] = 3.14
    tree["str"] = "hello"
    tree["list"] = [1, 2, 3]
    tree["dict"] = {"nested": "value"}
    tree["tuple"] = (1, 2)

    assert tree["int"] == 42
    assert tree["float"] == 3.14
    assert tree["str"] == "hello"
    assert tree["list"] == [1, 2, 3]
    assert tree["dict"] == {"nested": "value"}
    assert tree["tuple"] == (1, 2)


def test_overwrite_existing_key():
    """Test that inserting same key overwrites the value."""
    tree = TreeMap()
    tree["key"] = "value1"
    assert tree["key"] == "value1"
    tree["key"] = "value2"
    assert tree["key"] == "value2"
    assert len(tree) == 1


def test_empty_string_key():
    """Test that empty string can be used as a key."""
    tree = TreeMap()
    tree[""] = "empty"
    assert tree[""] == "empty"
    assert "" in tree
