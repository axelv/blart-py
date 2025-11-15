"""Tests for advanced features: boundary operations and fuzzy search."""

from blart import TreeMap


# Boundary operation tests


def test_first():
    """Test getting the first key-value pair."""
    tree = TreeMap()
    tree["cherry"] = 3
    tree["apple"] = 1
    tree["banana"] = 2

    result = tree.first()
    assert result is not None
    key, value = result
    assert key == "apple"
    assert value == 1


def test_first_empty():
    """Test first() on an empty tree returns None."""
    tree = TreeMap()
    result = tree.first()
    assert result is None


def test_last():
    """Test getting the last key-value pair."""
    tree = TreeMap()
    tree["apple"] = 1
    tree["cherry"] = 3
    tree["banana"] = 2

    result = tree.last()
    assert result is not None
    key, value = result
    assert key == "cherry"
    assert value == 3


def test_last_empty():
    """Test last() on an empty tree returns None."""
    tree = TreeMap()
    result = tree.last()
    assert result is None


def test_pop_first():
    """Test removing and returning the first key-value pair."""
    tree = TreeMap()
    tree["cherry"] = 3
    tree["apple"] = 1
    tree["banana"] = 2

    result = tree.pop_first()
    assert result is not None
    key, value = result
    assert key == "apple"
    assert value == 1

    # Verify it was removed
    assert len(tree) == 2
    assert "apple" not in tree
    assert "banana" in tree
    assert "cherry" in tree


def test_pop_last():
    """Test removing and returning the last key-value pair."""
    tree = TreeMap()
    tree["apple"] = 1
    tree["cherry"] = 3
    tree["banana"] = 2

    result = tree.pop_last()
    assert result is not None
    key, value = result
    assert key == "cherry"
    assert value == 3

    # Verify it was removed
    assert len(tree) == 2
    assert "cherry" not in tree
    assert "apple" in tree
    assert "banana" in tree


def test_pop_first_empty_returns_none():
    """Test pop_first() on an empty tree returns None."""
    tree = TreeMap()
    result = tree.pop_first()
    assert result is None


def test_pop_last_empty_returns_none():
    """Test pop_last() on an empty tree returns None."""
    tree = TreeMap()
    result = tree.pop_last()
    assert result is None


def test_boundary_operations_single_item():
    """Test boundary operations with a single item."""
    tree = TreeMap()
    tree["only"] = 42

    # first and last should return the same item
    first_result = tree.first()
    last_result = tree.last()

    assert first_result == last_result
    assert first_result == ("only", 42)

    # Pop first should remove it
    pop_result = tree.pop_first()
    assert pop_result == ("only", 42)
    assert len(tree) == 0


def test_boundary_operations_with_unicode():
    """Test boundary operations work with unicode keys."""
    tree = TreeMap()
    tree["zebra"] = 1
    tree["café"] = 2
    tree["apple"] = 3

    first = tree.first()
    assert first is not None
    assert first[0] == "apple"

    last = tree.last()
    assert last is not None
    # Last should be "zebra" in lexicographic order
    assert last[0] == "zebra"


# Fuzzy search tests


def test_fuzzy_search_exact_match():
    """Test fuzzy search with exact match (distance 0)."""
    tree = TreeMap()
    tree["apple"] = 1
    tree["banana"] = 2

    results = list(tree.fuzzy_search("apple", 0))
    assert len(results) == 1
    key, value, distance = results[0]
    assert key == "apple"
    assert value == 1
    assert distance == 0


def test_fuzzy_search_one_char_diff():
    """Test fuzzy search with one character difference."""
    tree = TreeMap()
    tree["apple"] = 1
    tree["apply"] = 2
    tree["banana"] = 3

    # "aple" is 1 character away from "apple" (missing 'p')
    results = list(tree.fuzzy_search("aple", 1))

    # Should find "apple"
    keys = [key for key, value, distance in results]
    assert "apple" in keys


def test_fuzzy_search_returns_distance():
    """Test that fuzzy search returns the Levenshtein distance."""
    tree = TreeMap()
    tree["test"] = 1

    results = list(tree.fuzzy_search("test", 2))

    assert len(results) >= 1
    for key, value, distance in results:
        assert isinstance(distance, int)
        assert distance >= 0
        assert distance <= 2  # Should not exceed max_distance


def test_fuzzy_search_max_distance():
    """Test fuzzy search respects max_distance parameter."""
    tree = TreeMap()
    tree["hello"] = 1
    tree["world"] = 2

    # "hello" and "world" are far apart
    results_0 = list(tree.fuzzy_search("hello", 0))
    results_1 = list(tree.fuzzy_search("hello", 1))
    results_5 = list(tree.fuzzy_search("hello", 5))

    # Distance 0 should only find exact match
    assert len(results_0) == 1
    assert results_0[0][0] == "hello"

    # Higher distance should potentially find more matches
    assert len(results_5) >= len(results_1)


def test_fuzzy_search_no_matches():
    """Test fuzzy search with no matches within max_distance."""
    tree = TreeMap()
    tree["apple"] = 1

    # "xyz" is very different from "apple"
    results = list(tree.fuzzy_search("xyz", 1))

    # Should find no matches
    assert len(results) == 0


def test_fuzzy_search_empty_tree():
    """Test fuzzy search on an empty tree."""
    tree = TreeMap()
    results = list(tree.fuzzy_search("anything", 5))
    assert results == []


def test_fuzzy_search_with_unicode():
    """Test fuzzy search works with unicode strings."""
    tree = TreeMap()
    tree["café"] = 1
    tree["cafe"] = 2

    # Search for "café" with small distance
    results = list(tree.fuzzy_search("café", 1))

    keys = [key for key, value, distance in results]
    assert "café" in keys


def test_fuzzy_search_returns_tuples():
    """Test that fuzzy search returns (key, value, distance) tuples."""
    tree = TreeMap()
    tree["test"] = 100

    results = list(tree.fuzzy_search("test", 0))

    assert len(results) == 1
    assert isinstance(results[0], tuple)
    assert len(results[0]) == 3

    key, value, distance = results[0]
    assert key == "test"
    assert value == 100
    assert distance == 0


def test_fuzzy_search_multiple_results():
    """Test fuzzy search can return multiple results."""
    tree = TreeMap()
    tree["test"] = 1
    tree["text"] = 2
    tree["tent"] = 3
    tree["best"] = 4

    # "test" with distance 1 should find several words
    results = list(tree.fuzzy_search("test", 1))

    # Should find at least "test" itself
    keys = [key for key, value, distance in results]
    assert "test" in keys

    # All results should be within distance 1
    for key, value, distance in results:
        assert distance <= 1


def test_fuzzy_search_with_various_value_types():
    """Test fuzzy search works with different value types."""
    tree = TreeMap()
    tree["key1"] = 42
    tree["key2"] = "string"
    tree["key3"] = [1, 2, 3]
    tree["key4"] = None

    results = list(tree.fuzzy_search("key1", 1))

    # Should find matches and preserve value types
    for key, value, distance in results:
        if key == "key1":
            assert value == 42
        elif key == "key2":
            assert value == "string"
