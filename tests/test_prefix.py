"""Tests for prefix query functionality."""

from blart import TreeMap


def test_get_prefix_first_match():
    """Test getting the first key-value pair matching a prefix."""
    tree = TreeMap()
    tree["apple"] = 1
    tree["application"] = 2
    tree["apply"] = 3
    tree["banana"] = 4

    # Should return the first match in lexicographic order
    result = tree.get_prefix("app")
    assert result is not None
    key, value = result
    assert key == "apple"
    assert value == 1


def test_get_prefix_no_match():
    """Test get_prefix returns None when no keys match."""
    tree = TreeMap()
    tree["apple"] = 1
    tree["banana"] = 2

    result = tree.get_prefix("orange")
    assert result is None


def test_prefix_iter_multiple_matches():
    """Test iterating over multiple keys with a common prefix."""
    tree = TreeMap()
    tree["apple"] = 1
    tree["application"] = 2
    tree["apply"] = 3
    tree["banana"] = 4
    tree["band"] = 5

    # Collect all keys starting with "app"
    results = list(tree.prefix_iter("app"))

    assert len(results) == 3
    keys = [key for key, value in results]
    assert "apple" in keys
    assert "application" in keys
    assert "apply" in keys
    assert "banana" not in keys


def test_prefix_iter_preserves_order():
    """Test that prefix iteration returns results in lexicographic order."""
    tree = TreeMap()
    tree["apple"] = 1
    tree["apply"] = 2
    tree["application"] = 3

    results = list(tree.prefix_iter("app"))
    keys = [key for key, value in results]

    # Should be in lexicographic order
    assert keys == ["apple", "application", "apply"]


def test_prefix_iter_empty_result():
    """Test prefix iteration with no matches."""
    tree = TreeMap()
    tree["apple"] = 1
    tree["banana"] = 2

    results = list(tree.prefix_iter("orange"))
    assert results == []


def test_prefix_with_exact_match():
    """Test prefix matching when the prefix exactly matches a key.

    Note: Due to blart's adaptive radix tree design with prefix compression,
    when a key is a prefix of another key, force_insert will remove the
    shorter prefix key when inserting the longer key. This is expected behavior.
    """
    tree = TreeMap()
    tree["application"] = 3
    tree["apple"] = 2
    tree["app"] = 1  # Insert shortest last to keep all keys

    # Should include the exact match
    results = list(tree.prefix_iter("app"))
    keys = [key for key, value in results]

    assert "app" in keys
    assert len(keys) == 1  # Only "app" remains due to prefix removal


def test_prefix_with_unicode():
    """Test prefix queries work with unicode strings."""
    tree = TreeMap()
    tree["café"] = 1
    tree["cafeteria"] = 2
    tree["cake"] = 3

    results = list(tree.prefix_iter("caf"))
    keys = [key for key, value in results]

    assert "café" in keys
    assert "cafeteria" in keys
    assert "cake" not in keys


def test_prefix_empty_prefix():
    """Test that empty prefix matches all keys."""
    tree = TreeMap()
    tree["apple"] = 1
    tree["banana"] = 2
    tree["cherry"] = 3

    results = list(tree.prefix_iter(""))
    assert len(results) == 3


def test_prefix_iter_returns_tuples():
    """Test that prefix_iter returns (key, value) tuples."""
    tree = TreeMap()
    tree["apple"] = 100
    tree["application"] = 200

    results = list(tree.prefix_iter("app"))

    assert len(results) == 2
    for item in results:
        assert isinstance(item, tuple)
        assert len(item) == 2
        key, value = item
        assert isinstance(key, str)
        assert isinstance(value, int)


def test_get_prefix_on_empty_tree():
    """Test get_prefix on an empty tree."""
    tree = TreeMap()
    result = tree.get_prefix("anything")
    assert result is None


def test_prefix_iter_on_empty_tree():
    """Test prefix_iter on an empty tree."""
    tree = TreeMap()
    results = list(tree.prefix_iter("anything"))
    assert results == []


def test_prefix_with_various_value_types():
    """Test that prefix queries work with different value types."""
    tree = TreeMap()
    tree["app1"] = 42
    tree["app2"] = "string value"
    tree["app3"] = [1, 2, 3]
    tree["app4"] = {"nested": "dict"}
    tree["app5"] = None

    results = list(tree.prefix_iter("app"))
    assert len(results) == 5

    # Verify values are correctly returned
    values = [v for k, v in results]
    assert 42 in values
    assert "string value" in values
    assert [1, 2, 3] in values
    assert {"nested": "dict"} in values
    assert None in values
