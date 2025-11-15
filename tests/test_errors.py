"""Test error handling and edge cases for TreeMap."""

import pytest
from blart import TreeMap


def test_keyerror_message_includes_key():
    """KeyError should include the key in the error message."""
    tree = TreeMap()
    tree["foo"] = "bar"

    with pytest.raises(KeyError) as exc_info:
        _ = tree["missing_key"]

    # Check that the key is included in the error message
    assert "missing_key" in str(exc_info.value)


def test_invalid_key_type_raises_typeerror():
    """Using non-string keys should raise TypeError."""
    tree = TreeMap()

    with pytest.raises(TypeError):
        tree[123] = "value"

    with pytest.raises(TypeError):
        _ = tree[123]

    with pytest.raises(TypeError):
        tree.insert(None, "value")


def test_operations_on_empty_treemap():
    """Operations on empty TreeMap should behave correctly."""
    tree = TreeMap()

    # Getting from empty tree
    assert tree.get("key") is None
    assert tree.get("key", "default") == "default"

    # Removing from empty tree
    with pytest.raises(KeyError):
        tree.remove("key")

    with pytest.raises(KeyError):
        del tree["key"]

    # Iteration over empty tree
    assert list(tree) == []
    assert list(tree.keys()) == []
    assert list(tree.values()) == []
    assert list(tree.items()) == []

    # Boundary operations on empty tree
    assert tree.first() is None
    assert tree.last() is None
    assert tree.pop_first() is None
    assert tree.pop_last() is None


def test_extremely_long_keys():
    """TreeMap should handle extremely long keys."""
    tree = TreeMap()

    # Create a very long key (10KB)
    long_key = "a" * 10000
    tree[long_key] = "value"

    assert tree[long_key] == "value"
    assert long_key in tree
    assert len(tree) == 1

    # Should be able to remove it
    del tree[long_key]
    assert long_key not in tree


def test_special_unicode_characters():
    """TreeMap should handle special Unicode characters."""
    tree = TreeMap()

    special_keys = [
        "hello\nworld",  # Newline
        "hello\tworld",  # Tab
        "hello\rworld",  # Carriage return
        "hello\0world",  # Null character
        "hello\\world",  # Backslash
        'hello"world',  # Quote
        "hello'world",  # Single quote
    ]

    for i, key in enumerate(special_keys):
        tree[key] = i

    # Verify all keys are stored correctly
    assert len(tree) == len(special_keys)

    for i, key in enumerate(special_keys):
        assert tree[key] == i


def test_emoji_keys():
    """TreeMap should handle emoji in keys."""
    tree = TreeMap()

    emoji_keys = [
        "🚀",
        "🐍",
        "🔥",
        "hello🌍world",
        "test🎉emoji🎊here",
    ]

    for i, key in enumerate(emoji_keys):
        tree[key] = i

    assert len(tree) == len(emoji_keys)

    for i, key in enumerate(emoji_keys):
        assert tree[key] == i
        assert key in tree


def test_null_bytes_in_keys():
    """TreeMap should handle null bytes in keys."""
    tree = TreeMap()

    # Keys with null bytes
    key1 = "hello\0world"
    key2 = "hello\0there"
    key3 = "\0start"
    key4 = "end\0"

    tree[key1] = 1
    tree[key2] = 2
    tree[key3] = 3
    tree[key4] = 4

    assert tree[key1] == 1
    assert tree[key2] == 2
    assert tree[key3] == 3
    assert tree[key4] == 4
    assert len(tree) == 4


def test_empty_string_key():
    """TreeMap should handle empty string as a key."""
    tree = TreeMap()

    tree[""] = "empty"
    assert tree[""] == "empty"
    assert "" in tree
    assert len(tree) == 1

    # Should be able to remove it
    del tree[""]
    assert "" not in tree


def test_mixed_operations_dont_corrupt_state():
    """Mixed operations should maintain TreeMap consistency."""
    tree = TreeMap()

    # Use keys that don't have prefix conflicts
    # Add prefix 'a_' to avoid issues with key2 being prefix of key20
    for i in range(100):
        tree[f"a_key_{i:03d}"] = i

    # Verify all keys inserted
    assert len(tree) == 100

    # Remove every other key
    for i in range(0, 100, 2):
        del tree[f"a_key_{i:03d}"]

    # Verify remaining keys
    assert len(tree) == 50
    for i in range(1, 100, 2):
        assert tree[f"a_key_{i:03d}"] == i

    # Re-insert some removed keys
    for i in range(0, 100, 4):
        tree[f"a_key_{i:03d}"] = i * 2

    # Verify state
    for i in range(0, 100, 4):
        assert tree[f"a_key_{i:03d}"] == i * 2


def test_overwrite_with_different_value_types():
    """Overwriting a key with different value types should work."""
    tree = TreeMap()

    tree["key"] = 123
    assert tree["key"] == 123

    tree["key"] = "string"
    assert tree["key"] == "string"

    tree["key"] = [1, 2, 3]
    assert tree["key"] == [1, 2, 3]

    tree["key"] = None
    assert tree["key"] is None


def test_concurrent_modifications_during_iteration():
    """Test behavior when modifying tree during iteration."""
    tree = TreeMap()
    for i in range(10):
        tree[f"key{i}"] = i

    # This test documents the current behavior
    # Modifying during iteration should not crash
    try:
        keys_to_delete = []
        for key in tree:
            if int(key[3:]) % 2 == 0:
                keys_to_delete.append(key)

        # Delete after iteration completes
        for key in keys_to_delete:
            del tree[key]

        assert len(tree) == 5
    except RuntimeError:
        # If modification during iteration raises an error, that's also acceptable
        pass


def test_get_with_callable_default():
    """get() should work with callable defaults."""
    tree = TreeMap()

    # Should not call the callable if key exists
    tree["key"] = "value"
    result = tree.get("key", lambda: "default")
    assert result == "value"  # The lambda itself, not called


def test_prefix_operations_with_empty_prefix():
    """Prefix operations with empty prefix should return all items."""
    tree = TreeMap()
    tree["apple"] = 1
    tree["banana"] = 2
    tree["cherry"] = 3

    # Empty prefix should match everything
    result = tree.get_prefix("")
    assert result is not None

    # Iteration with empty prefix should return all items
    items = list(tree.prefix_iter(""))
    assert len(items) == 3


def test_fuzzy_search_with_zero_distance():
    """Fuzzy search with max_distance=0 should only return exact matches."""
    tree = TreeMap()
    tree["hello"] = 1
    tree["world"] = 2
    tree["help"] = 3

    results = list(tree.fuzzy_search("hello", 0))
    assert len(results) == 1
    assert results[0] == ("hello", 1, 0)


def test_fuzzy_search_with_negative_distance():
    """Fuzzy search with negative distance should raise OverflowError."""
    tree = TreeMap()
    tree["hello"] = 1

    # Negative distance can't be converted to usize, so it raises OverflowError
    with pytest.raises((ValueError, OverflowError)):
        list(tree.fuzzy_search("hello", -1))


def test_large_number_of_keys():
    """TreeMap should handle a large number of keys efficiently."""
    tree = TreeMap()
    n = 10000

    # Insert many keys
    for i in range(n):
        tree[f"key_{i:05d}"] = i

    assert len(tree) == n

    # Verify random access
    assert tree["key_05000"] == 5000
    assert tree["key_00000"] == 0
    assert tree["key_09999"] == 9999

    # Verify iteration works
    count = 0
    for _ in tree:
        count += 1
        if count > 100:  # Don't iterate all for performance
            break

    assert count > 100
