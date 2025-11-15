#![allow(clippy::useless_conversion)]

use crate::iterators::{
    PyFuzzyIter, PyPrefixIter, PyTreeMapItems, PyTreeMapIter, PyTreeMapKeys, PyTreeMapValues,
};
use blart::TreeMap;
use pyo3::exceptions::PyKeyError;
use pyo3::prelude::*;
use pyo3::types::{PyDict, PyList};

/// Calculate Levenshtein distance between two strings
#[allow(clippy::needless_range_loop)]
fn levenshtein_distance(s1: &str, s2: &str) -> usize {
    let len1 = s1.chars().count();
    let len2 = s2.chars().count();

    if len1 == 0 {
        return len2;
    }
    if len2 == 0 {
        return len1;
    }

    let mut matrix = vec![vec![0; len2 + 1]; len1 + 1];

    for i in 0..=len1 {
        matrix[i][0] = i;
    }
    for j in 0..=len2 {
        matrix[0][j] = j;
    }

    let s1_chars: Vec<char> = s1.chars().collect();
    let s2_chars: Vec<char> = s2.chars().collect();

    for i in 1..=len1 {
        for j in 1..=len2 {
            let cost = if s1_chars[i - 1] == s2_chars[j - 1] {
                0
            } else {
                1
            };
            matrix[i][j] = std::cmp::min(
                std::cmp::min(
                    matrix[i - 1][j] + 1, // deletion
                    matrix[i][j - 1] + 1, // insertion
                ),
                matrix[i - 1][j - 1] + cost, // substitution
            );
        }
    }

    matrix[len1][len2]
}

/// A high-performance adaptive radix tree (ART) implementation.
///
/// TreeMap is an ordered map data structure that stores key-value pairs.
/// It provides efficient operations for:
/// - Standard dictionary operations (insert, get, delete)
/// - Prefix queries (find all keys starting with a prefix)
/// - Fuzzy matching (find keys within edit distance)
/// - Ordered iteration
///
/// # Performance
/// - Insert: O(k) where k is key length
/// - Get: O(k) where k is key length
/// - Remove: O(k) where k is key length
/// - Prefix query: O(k + m) where m is number of matches
///
/// # Examples
/// ```python
/// from blart import TreeMap
///
/// # Create a new TreeMap
/// tree = TreeMap()
/// tree["hello"] = "world"
///
/// # Create from dict
/// tree = TreeMap({"apple": 1, "banana": 2})
///
/// # Prefix queries
/// for key, value in tree.prefix_iter("app"):
///     print(key, value)
/// ```
#[pyclass(name = "PyTreeMap")]
pub struct PyTreeMap {
    inner: TreeMap<Box<[u8]>, Py<PyAny>>,
}

#[pymethods]
impl PyTreeMap {
    /// Create a new TreeMap.
    ///
    /// Args:
    ///     data: Optional initial data. Can be:
    ///         - None: Creates an empty TreeMap
    ///         - dict: Creates TreeMap from dictionary
    ///         - list of tuples: Creates TreeMap from [(key, value), ...] pairs
    ///
    /// Returns:
    ///     A new TreeMap instance
    ///
    /// Raises:
    ///     ValueError: If data format is invalid
    ///     TypeError: If keys are not strings
    ///
    /// Examples:
    ///     >>> tree = TreeMap()
    ///     >>> tree = TreeMap({"a": 1, "b": 2})
    ///     >>> tree = TreeMap([("a", 1), ("b", 2)])
    #[new]
    #[pyo3(signature = (data=None))]
    fn new(py: Python, data: Option<&Bound<'_, PyAny>>) -> PyResult<Self> {
        let mut tree = Self {
            inner: TreeMap::new(),
        };

        if let Some(data) = data {
            // Try to interpret as dict
            if let Ok(dict) = data.cast_exact::<PyDict>() {
                for (key, value) in dict.iter() {
                    let key_str: String = key.extract()?;
                    tree.insert(py, key_str, value.clone().unbind())?;
                }
            }
            // Try to interpret as list of tuples
            else if let Ok(list) = data.cast_exact::<PyList>() {
                for item in list.iter() {
                    let tuple = item.cast_exact::<pyo3::types::PyTuple>()?;
                    if tuple.len() != 2 {
                        return Err(PyErr::new::<pyo3::exceptions::PyValueError, _>(
                            "Items must be (key, value) tuples",
                        ));
                    }
                    let key_str: String = tuple.get_item(0)?.extract()?;
                    let value = tuple.get_item(1)?.clone().unbind();
                    tree.insert(py, key_str, value)?;
                }
            }
        }

        Ok(tree)
    }

    /// Insert a key-value pair into the TreeMap.
    ///
    /// If the key already exists, its value is updated.
    /// Note: Due to the adaptive radix tree structure, inserting a key may
    /// remove existing keys that are prefixes of the new key.
    ///
    /// Args:
    ///     key: String key to insert
    ///     value: Python object to store
    ///
    /// Examples:
    ///     >>> tree = TreeMap()
    ///     >>> tree.insert("hello", "world")
    ///     >>> tree.insert("hello", "universe")  # Updates value
    fn insert(&mut self, _py: Python, key: String, value: Py<PyAny>) -> PyResult<()> {
        let key_bytes = key.into_bytes().into_boxed_slice();
        self.inner.force_insert(key_bytes, value);
        Ok(())
    }

    /// Get a value by key, with optional default.
    ///
    /// Args:
    ///     key: String key to look up
    ///     default: Value to return if key not found (defaults to None)
    ///
    /// Returns:
    ///     The value associated with the key, or default if not found
    ///
    /// Examples:
    ///     >>> tree = TreeMap({"hello": "world"})
    ///     >>> tree.get("hello")
    ///     'world'
    ///     >>> tree.get("missing")
    ///     None
    ///     >>> tree.get("missing", "default")
    ///     'default'
    #[pyo3(signature = (key, default=None))]
    fn get(
        &self,
        py: Python,
        key: String,
        default: Option<Py<PyAny>>,
    ) -> PyResult<Option<Py<PyAny>>> {
        let key_bytes = key.as_bytes();
        match self.inner.get(key_bytes) {
            Some(value) => Ok(Some(value.clone_ref(py))),
            None => Ok(default.or_else(|| Some(py.None()))),
        }
    }

    /// Remove a key and return its value.
    ///
    /// Args:
    ///     key: String key to remove
    ///
    /// Returns:
    ///     The value that was associated with the key
    ///
    /// Raises:
    ///     KeyError: If the key does not exist
    ///
    /// Examples:
    ///     >>> tree = TreeMap({"hello": "world"})
    ///     >>> tree.remove("hello")
    ///     'world'
    ///     >>> tree.remove("missing")  # Raises KeyError
    fn remove(&mut self, _py: Python, key: String) -> PyResult<Py<PyAny>> {
        let key_bytes = key.as_bytes();
        match self.inner.remove(key_bytes) {
            Some(value) => Ok(value),
            None => Err(PyErr::new::<PyKeyError, _>(format!("'{}'", key))),
        }
    }

    /// Remove all entries from the TreeMap.
    ///
    /// Examples:
    ///     >>> tree = TreeMap({"a": 1, "b": 2})
    ///     >>> tree.clear()
    ///     >>> len(tree)
    ///     0
    fn clear(&mut self) -> PyResult<()> {
        self.inner.clear();
        Ok(())
    }

    /// Check if the TreeMap contains no entries.
    ///
    /// Returns:
    ///     True if the TreeMap is empty, False otherwise
    ///
    /// Examples:
    ///     >>> tree = TreeMap()
    ///     >>> tree.is_empty()
    ///     True
    ///     >>> tree["key"] = "value"
    ///     >>> tree.is_empty()
    ///     False
    fn is_empty(&self) -> PyResult<bool> {
        Ok(self.inner.is_empty())
    }

    /// Get item using subscript notation (tree[key]).
    ///
    /// Args:
    ///     key: String key to look up
    ///
    /// Returns:
    ///     The value associated with the key
    ///
    /// Raises:
    ///     KeyError: If the key does not exist
    fn __getitem__(&self, py: Python, key: String) -> PyResult<Py<PyAny>> {
        let key_bytes = key.as_bytes();
        match self.inner.get(key_bytes) {
            Some(value) => Ok(value.clone_ref(py)),
            None => Err(PyErr::new::<PyKeyError, _>(format!("'{}'", key))),
        }
    }

    /// Set item using subscript notation (tree[key] = value).
    ///
    /// Args:
    ///     key: String key
    ///     value: Python object to store
    fn __setitem__(&mut self, py: Python, key: String, value: Py<PyAny>) -> PyResult<()> {
        self.insert(py, key, value)
    }

    /// Delete item using del statement (del tree[key]).
    ///
    /// Args:
    ///     key: String key to delete
    ///
    /// Raises:
    ///     KeyError: If the key does not exist
    fn __delitem__(&mut self, py: Python, key: String) -> PyResult<()> {
        self.remove(py, key)?;
        Ok(())
    }

    /// Check if key exists using 'in' operator (key in tree).
    ///
    /// Args:
    ///     key: String key to check
    ///
    /// Returns:
    ///     True if key exists, False otherwise
    fn __contains__(&self, key: String) -> PyResult<bool> {
        let key_bytes = key.as_bytes();
        Ok(self.inner.contains_key(key_bytes))
    }

    /// Get the number of entries in the TreeMap.
    ///
    /// Returns:
    ///     Number of key-value pairs
    fn __len__(&self) -> PyResult<usize> {
        Ok(self.inner.len())
    }

    /// Return a developer-friendly string representation.
    ///
    /// Returns:
    ///     String like "TreeMap(len=5)"
    fn __repr__(&self) -> PyResult<String> {
        Ok(format!("TreeMap(len={})", self.inner.len()))
    }

    /// Return a user-friendly string representation.
    ///
    /// Returns:
    ///     String like "TreeMap with 5 entries"
    fn __str__(&self) -> PyResult<String> {
        Ok(format!("TreeMap with {} entries", self.inner.len()))
    }

    /// Return an iterator over keys in lexicographic order.
    ///
    /// Returns:
    ///     Iterator that yields keys as strings
    ///
    /// Examples:
    ///     >>> tree = TreeMap({"c": 3, "a": 1, "b": 2})
    ///     >>> list(tree)
    ///     ['a', 'b', 'c']
    fn __iter__(&self, _py: Python) -> PyResult<PyTreeMapIter> {
        let keys: Vec<String> = self
            .inner
            .iter()
            .map(|(k, _)| String::from_utf8_lossy(k).into_owned())
            .collect();
        Ok(PyTreeMapIter::new(keys))
    }

    /// Return an iterator over all keys in lexicographic order.
    ///
    /// Returns:
    ///     Iterator that yields keys as strings
    ///
    /// Examples:
    ///     >>> tree = TreeMap({"c": 3, "a": 1, "b": 2})
    ///     >>> list(tree.keys())
    ///     ['a', 'b', 'c']
    fn keys(&self, _py: Python) -> PyResult<PyTreeMapKeys> {
        let keys: Vec<String> = self
            .inner
            .iter()
            .map(|(k, _)| String::from_utf8_lossy(k).into_owned())
            .collect();
        Ok(PyTreeMapKeys::new(keys))
    }

    /// Return an iterator over all values in key order.
    ///
    /// Returns:
    ///     Iterator that yields values
    ///
    /// Examples:
    ///     >>> tree = TreeMap({"c": 3, "a": 1, "b": 2})
    ///     >>> list(tree.values())
    ///     [1, 2, 3]
    fn values(&self, py: Python) -> PyResult<PyTreeMapValues> {
        let values: Vec<Py<PyAny>> = self.inner.iter().map(|(_, v)| v.clone_ref(py)).collect();
        Ok(PyTreeMapValues::new(values))
    }

    /// Return an iterator over all (key, value) pairs in lexicographic order.
    ///
    /// Returns:
    ///     Iterator that yields (key, value) tuples
    ///
    /// Examples:
    ///     >>> tree = TreeMap({"c": 3, "a": 1})
    ///     >>> list(tree.items())
    ///     [('a', 1), ('c', 3)]
    fn items(&self, py: Python) -> PyResult<PyTreeMapItems> {
        let items: Vec<(String, Py<PyAny>)> = self
            .inner
            .iter()
            .map(|(k, v)| (String::from_utf8_lossy(k).into_owned(), v.clone_ref(py)))
            .collect();
        Ok(PyTreeMapItems::new(items))
    }

    /// Get the first key-value pair matching a prefix.
    ///
    /// This is useful for quickly checking if any keys start with a given prefix,
    /// or for getting a representative value for a prefix.
    ///
    /// Args:
    ///     prefix: String prefix to search for
    ///
    /// Returns:
    ///     (key, value) tuple for first match, or None if no match
    ///
    /// Examples:
    ///     >>> tree = TreeMap({"apple": 1, "application": 2, "banana": 3})
    ///     >>> tree.get_prefix("app")
    ///     ('apple', 1)
    ///     >>> tree.get_prefix("ban")
    ///     ('banana', 3)
    ///     >>> tree.get_prefix("xyz")
    ///     None
    fn get_prefix(&self, py: Python, prefix: String) -> PyResult<Option<(String, Py<PyAny>)>> {
        let prefix_bytes = prefix.as_bytes();
        // Use prefix iterator to get the first matching key-value pair
        let mut iter = self.inner.prefix(prefix_bytes);
        match iter.next() {
            Some((key, val)) => {
                let key_str = String::from_utf8_lossy(key).into_owned();
                Ok(Some((key_str, val.clone_ref(py))))
            }
            None => Ok(None),
        }
    }

    /// Return an iterator over all key-value pairs with a given prefix.
    ///
    /// This is one of the key features of the adaptive radix tree - efficient
    /// prefix queries that don't require scanning all keys.
    ///
    /// Args:
    ///     prefix: String prefix to search for
    ///
    /// Returns:
    ///     Iterator yielding (key, value) tuples for matching keys
    ///
    /// Examples:
    ///     >>> tree = TreeMap({"apple": 1, "application": 2, "apply": 3, "banana": 4})
    ///     >>> list(tree.prefix_iter("app"))
    ///     [('apple', 1), ('application', 2), ('apply', 3)]
    ///     >>> list(tree.prefix_iter(""))  # Empty prefix matches all
    ///     [('apple', 1), ('application', 2), ('apply', 3), ('banana', 4)]
    fn prefix_iter(&self, py: Python, prefix: String) -> PyResult<PyPrefixIter> {
        let prefix_bytes = prefix.as_bytes();
        let items: Vec<(String, Py<PyAny>)> = self
            .inner
            .prefix(prefix_bytes)
            .map(|(k, v)| (String::from_utf8_lossy(k).into_owned(), v.clone_ref(py)))
            .collect();
        Ok(PyPrefixIter::new(items))
    }

    /// Get the first (lexicographically smallest) key-value pair.
    ///
    /// Args:
    ///     None
    ///
    /// Returns:
    ///     (key, value) tuple for the first entry, or None if empty
    ///
    /// Examples:
    ///     >>> tree = TreeMap({"c": 3, "a": 1, "b": 2})
    ///     >>> tree.first()
    ///     ('a', 1)
    ///     >>> TreeMap().first()
    ///     None
    fn first(&self, py: Python) -> PyResult<Option<(String, Py<PyAny>)>> {
        match self.inner.first_key_value() {
            Some((key, value)) => {
                let key_str = String::from_utf8_lossy(key).into_owned();
                Ok(Some((key_str, value.clone_ref(py))))
            }
            None => Ok(None),
        }
    }

    /// Get the last (lexicographically largest) key-value pair.
    ///
    /// Args:
    ///     None
    ///
    /// Returns:
    ///     (key, value) tuple for the last entry, or None if empty
    ///
    /// Examples:
    ///     >>> tree = TreeMap({"c": 3, "a": 1, "b": 2})
    ///     >>> tree.last()
    ///     ('c', 3)
    ///     >>> TreeMap().last()
    ///     None
    fn last(&self, py: Python) -> PyResult<Option<(String, Py<PyAny>)>> {
        match self.inner.last_key_value() {
            Some((key, value)) => {
                let key_str = String::from_utf8_lossy(key).into_owned();
                Ok(Some((key_str, value.clone_ref(py))))
            }
            None => Ok(None),
        }
    }

    /// Remove and return the first (lexicographically smallest) key-value pair.
    ///
    /// This is useful for implementing queue-like behavior or for iteratively
    /// processing elements in sorted order.
    ///
    /// Args:
    ///     None
    ///
    /// Returns:
    ///     (key, value) tuple for the first entry, or None if empty
    ///
    /// Examples:
    ///     >>> tree = TreeMap({"c": 3, "a": 1, "b": 2})
    ///     >>> tree.pop_first()
    ///     ('a', 1)
    ///     >>> tree.pop_first()
    ///     ('b', 2)
    ///     >>> len(tree)
    ///     1
    fn pop_first(&mut self, _py: Python) -> PyResult<Option<(String, Py<PyAny>)>> {
        match self.inner.pop_first() {
            Some((key, value)) => {
                let key_str = String::from_utf8_lossy(&key).into_owned();
                Ok(Some((key_str, value)))
            }
            None => Ok(None),
        }
    }

    /// Remove and return the last (lexicographically largest) key-value pair.
    ///
    /// This is useful for implementing stack-like behavior or for iteratively
    /// processing elements in reverse sorted order.
    ///
    /// Args:
    ///     None
    ///
    /// Returns:
    ///     (key, value) tuple for the last entry, or None if empty
    ///
    /// Examples:
    ///     >>> tree = TreeMap({"c": 3, "a": 1, "b": 2})
    ///     >>> tree.pop_last()
    ///     ('c', 3)
    ///     >>> tree.pop_last()
    ///     ('b', 2)
    ///     >>> len(tree)
    ///     1
    fn pop_last(&mut self, _py: Python) -> PyResult<Option<(String, Py<PyAny>)>> {
        match self.inner.pop_last() {
            Some((key, value)) => {
                let key_str = String::from_utf8_lossy(&key).into_owned();
                Ok(Some((key_str, value)))
            }
            None => Ok(None),
        }
    }

    /// Find keys within a specified edit distance (Levenshtein distance).
    ///
    /// This is useful for fuzzy matching, typo tolerance, and approximate
    /// string searching. The Levenshtein distance counts the minimum number
    /// of single-character edits (insertions, deletions, substitutions)
    /// needed to transform one string into another.
    ///
    /// Args:
    ///     key: String to search for
    ///     max_distance: Maximum edit distance allowed (must be non-negative)
    ///
    /// Returns:
    ///     Iterator yielding (key, value, distance) tuples for all matches
    ///
    /// Raises:
    ///     OverflowError: If max_distance is negative
    ///
    /// Examples:
    ///     >>> tree = TreeMap({"hello": 1, "hallo": 2, "world": 3})
    ///     >>> list(tree.fuzzy_search("hello", 0))
    ///     [('hello', 1, 0)]
    ///     >>> results = list(tree.fuzzy_search("hello", 1))
    ///     >>> # Returns both "hello" (distance 0) and "hallo" (distance 1)
    ///     >>> len(results)
    ///     2
    fn fuzzy_search(&self, py: Python, key: String, max_distance: usize) -> PyResult<PyFuzzyIter> {
        let key_bytes = key.as_bytes();
        let items: Vec<(String, Py<PyAny>, usize)> = self
            .inner
            .fuzzy(key_bytes, max_distance)
            .map(|(k, v)| {
                let key_str = String::from_utf8_lossy(k).into_owned();
                let distance = levenshtein_distance(&key, &key_str);
                (key_str, v.clone_ref(py), distance)
            })
            .collect();
        Ok(PyFuzzyIter::new(items))
    }
}
