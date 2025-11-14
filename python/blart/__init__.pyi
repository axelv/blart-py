"""Type stubs for blart package."""

from typing import Any, Dict, Iterable, Iterator, List, Optional, Tuple, Union, overload

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

__all__ = ["TreeMap"]
