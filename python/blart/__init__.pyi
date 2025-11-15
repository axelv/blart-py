"""Type stubs for blart package."""

from typing import Any, Dict, Iterable, Iterator, Optional, Tuple, overload

class TreeMap:
    """Adaptive radix tree implementation using an adaptive radix tree (ART).

    TreeMap provides a dictionary-like interface with efficient operations
    for string keys. It supports all standard dict operations plus advanced
    features like prefix queries.

    Examples:
        >>> tree = TreeMap()
        >>> tree["apple"] = 1
        >>> tree["banana"] = 2
        >>> print(tree["apple"])
        1
        >>> "banana" in tree
        True
        >>> len(tree)
        2
    """

    @overload
    def __init__(self) -> None:
        """Create an empty TreeMap."""
        ...

    @overload
    def __init__(self, data: Dict[str, Any]) -> None:
        """Create a TreeMap from a dictionary."""
        ...

    @overload
    def __init__(self, data: Iterable[Tuple[str, Any]]) -> None:
        """Create a TreeMap from an iterable of (key, value) tuples."""
        ...

    def insert(self, key: str, value: Any) -> None:
        """Insert or update a key-value pair.

        Args:
            key: The key to insert (must be a string)
            value: The value to associate with the key
        """
        ...

    def get(self, key: str, default: Optional[Any] = None) -> Optional[Any]:
        """Get a value by key with optional default.

        Args:
            key: The key to look up
            default: Value to return if key is not found (default: None)

        Returns:
            The value associated with the key, or default if not found
        """
        ...

    def remove(self, key: str) -> Any:
        """Remove a key and return its value.

        Args:
            key: The key to remove

        Returns:
            The value that was associated with the key

        Raises:
            KeyError: If the key does not exist
        """
        ...

    def clear(self) -> None:
        """Remove all entries from the TreeMap."""
        ...

    def is_empty(self) -> bool:
        """Check if the TreeMap is empty.

        Returns:
            True if the TreeMap has no entries, False otherwise
        """
        ...

    def __getitem__(self, key: str) -> Any:
        """Get a value using square bracket notation.

        Args:
            key: The key to look up

        Returns:
            The value associated with the key

        Raises:
            KeyError: If the key does not exist
        """
        ...

    def __setitem__(self, key: str, value: Any) -> None:
        """Set a value using square bracket notation.

        Args:
            key: The key to set
            value: The value to associate with the key
        """
        ...

    def __delitem__(self, key: str) -> None:
        """Delete a key using del statement.

        Args:
            key: The key to delete

        Raises:
            KeyError: If the key does not exist
        """
        ...

    def __contains__(self, key: str) -> bool:
        """Check if a key exists using 'in' operator.

        Args:
            key: The key to check

        Returns:
            True if the key exists, False otherwise
        """
        ...

    def __len__(self) -> int:
        """Get the number of entries in the TreeMap.

        Returns:
            The number of key-value pairs
        """
        ...

    def __repr__(self) -> str:
        """Get a debug string representation."""
        ...

    def __str__(self) -> str:
        """Get a human-readable string representation."""
        ...

    def __iter__(self) -> Iterator[str]:
        """Iterate over keys in the TreeMap.

        Returns:
            An iterator over the keys in lexicographic order
        """
        ...

    def keys(self) -> Iterator[str]:
        """Get an iterator over keys.

        Returns:
            An iterator over the keys in lexicographic order
        """
        ...

    def values(self) -> Iterator[Any]:
        """Get an iterator over values.

        Returns:
            An iterator over the values in key order
        """
        ...

    def items(self) -> Iterator[Tuple[str, Any]]:
        """Get an iterator over (key, value) pairs.

        Returns:
            An iterator over (key, value) tuples in key order
        """
        ...

    def get_prefix(self, prefix: str) -> Optional[Tuple[str, Any]]:
        """Get the first key-value pair matching a prefix.

        Returns the first key-value pair where the key starts with the given prefix,
        in lexicographic order. Returns None if no keys match the prefix.

        Args:
            prefix: The prefix to search for

        Returns:
            A tuple of (key, value) for the first matching entry, or None if no match

        Examples:
            >>> tree = TreeMap()
            >>> tree["apple"] = 1
            >>> tree["application"] = 2
            >>> tree["banana"] = 3
            >>> tree.get_prefix("app")
            ('apple', 1)
            >>> tree.get_prefix("ban")
            ('banana', 3)
            >>> tree.get_prefix("orange")
            None

        Note:
            Due to blart's adaptive radix tree design with prefix compression,
            when a key is a prefix of another key, inserting the longer key will
            remove the shorter prefix key. This is expected behavior.
        """
        ...

    def prefix_iter(self, prefix: str) -> Iterator[Tuple[str, Any]]:
        """Get an iterator over all key-value pairs with a given prefix.

        Returns an iterator that yields (key, value) tuples for all keys
        that start with the given prefix, in lexicographic order.

        Args:
            prefix: The prefix to search for

        Returns:
            An iterator over (key, value) tuples matching the prefix

        Examples:
            >>> tree = TreeMap()
            >>> tree["apple"] = 1
            >>> tree["application"] = 2
            >>> tree["apply"] = 3
            >>> tree["banana"] = 4
            >>> for key, value in tree.prefix_iter("app"):
            ...     print(f"{key}: {value}")
            apple: 1
            application: 2
            apply: 3
            >>> list(tree.prefix_iter("ban"))
            [('banana', 4)]
            >>> list(tree.prefix_iter("orange"))
            []

        Note:
            An empty prefix ("") matches all keys in the tree.
        """
        ...

    def first(self) -> Optional[Tuple[str, Any]]:
        """Get the first (minimum) key-value pair.

        Returns the first key-value pair in lexicographic order,
        or None if the tree is empty.

        Returns:
            A tuple of (key, value) for the first entry, or None if empty

        Examples:
            >>> tree = TreeMap()
            >>> tree["cherry"] = 3
            >>> tree["apple"] = 1
            >>> tree["banana"] = 2
            >>> tree.first()
            ('apple', 1)
            >>> TreeMap().first()
            None
        """
        ...

    def last(self) -> Optional[Tuple[str, Any]]:
        """Get the last (maximum) key-value pair.

        Returns the last key-value pair in lexicographic order,
        or None if the tree is empty.

        Returns:
            A tuple of (key, value) for the last entry, or None if empty

        Examples:
            >>> tree = TreeMap()
            >>> tree["apple"] = 1
            >>> tree["cherry"] = 3
            >>> tree["banana"] = 2
            >>> tree.last()
            ('cherry', 3)
            >>> TreeMap().last()
            None
        """
        ...

    def pop_first(self) -> Optional[Tuple[str, Any]]:
        """Remove and return the first (minimum) key-value pair.

        Returns and removes the first key-value pair in lexicographic order,
        or None if the tree is empty.

        Returns:
            A tuple of (key, value) for the first entry that was removed,
            or None if empty

        Examples:
            >>> tree = TreeMap()
            >>> tree["cherry"] = 3
            >>> tree["apple"] = 1
            >>> tree["banana"] = 2
            >>> tree.pop_first()
            ('apple', 1)
            >>> len(tree)
            2
            >>> "apple" in tree
            False
        """
        ...

    def pop_last(self) -> Optional[Tuple[str, Any]]:
        """Remove and return the last (maximum) key-value pair.

        Returns and removes the last key-value pair in lexicographic order,
        or None if the tree is empty.

        Returns:
            A tuple of (key, value) for the last entry that was removed,
            or None if empty

        Examples:
            >>> tree = TreeMap()
            >>> tree["apple"] = 1
            >>> tree["cherry"] = 3
            >>> tree["banana"] = 2
            >>> tree.pop_last()
            ('cherry', 3)
            >>> len(tree)
            2
            >>> "cherry" in tree
            False
        """
        ...

    def fuzzy_search(
        self, key: str, max_distance: int
    ) -> Iterator[Tuple[str, Any, int]]:
        """Fuzzy search for keys within a Levenshtein distance threshold.

        Returns an iterator that yields (key, value, distance) tuples for all keys
        within the specified Levenshtein distance from the search key. The Levenshtein
        distance (also known as edit distance) is the minimum number of single-character
        edits (insertions, deletions, or substitutions) required to change one string
        into another.

        Args:
            key: The search key to match against
            max_distance: Maximum Levenshtein distance (edit distance) allowed

        Returns:
            An iterator over (key, value, distance) tuples where distance is the
            Levenshtein distance from the search key

        Examples:
            >>> tree = TreeMap()
            >>> tree["test"] = 1
            >>> tree["text"] = 2
            >>> tree["tent"] = 3
            >>> tree["best"] = 4
            >>> # Find all keys within distance 1 from "test"
            >>> results = list(tree.fuzzy_search("test", 1))
            >>> # Results include exact match (distance=0) and close matches
            >>> for key, value, distance in results:
            ...     print(f"{key}: {value} (distance={distance})")
            test: 1 (distance=0)
            text: 2 (distance=1)
            best: 4 (distance=1)
            >>> # Search for typo with distance 2
            >>> list(tree.fuzzy_search("tset", 2))
            [('test', 1, 2), ...]

        Note:
            The fuzzy search uses the Levenshtein distance algorithm to calculate
            string similarity. Higher max_distance values will find more matches
            but may be slower for large trees.
        """
        ...

__all__ = ["TreeMap"]
