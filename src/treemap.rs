use pyo3::prelude::*;
use pyo3::exceptions::PyKeyError;
use pyo3::types::{PyDict, PyList};
use blart::TreeMap;
use crate::iterators::{PyTreeMapIter, PyTreeMapKeys, PyTreeMapValues, PyTreeMapItems, PyPrefixIter, PyFuzzyIter};

/// Calculate Levenshtein distance between two strings
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
            let cost = if s1_chars[i - 1] == s2_chars[j - 1] { 0 } else { 1 };
            matrix[i][j] = std::cmp::min(
                std::cmp::min(
                    matrix[i - 1][j] + 1,      // deletion
                    matrix[i][j - 1] + 1       // insertion
                ),
                matrix[i - 1][j - 1] + cost    // substitution
            );
        }
    }

    matrix[len1][len2]
}

/// Adaptive radix tree implementation
#[pyclass(name = "PyTreeMap")]
pub struct PyTreeMap {
    inner: TreeMap<Box<[u8]>, PyObject>,
}

#[pymethods]
impl PyTreeMap {
    /// Create a new empty TreeMap or from initial data
    #[new]
    #[pyo3(signature = (data=None))]
    fn new(py: Python, data: Option<&Bound<'_, PyAny>>) -> PyResult<Self> {
        let mut tree = Self {
            inner: TreeMap::new(),
        };

        if let Some(data) = data {
            // Try to interpret as dict
            if let Ok(dict) = data.downcast::<PyDict>() {
                for (key, value) in dict.iter() {
                    let key_str: String = key.extract()?;
                    tree.insert(py, key_str, value.to_object(py))?;
                }
            }
            // Try to interpret as list of tuples
            else if let Ok(list) = data.downcast::<PyList>() {
                for item in list.iter() {
                    let tuple = item.downcast::<pyo3::types::PyTuple>()?;
                    if tuple.len() != 2 {
                        return Err(PyErr::new::<pyo3::exceptions::PyValueError, _>(
                            "Items must be (key, value) tuples"
                        ));
                    }
                    let key_str: String = tuple.get_item(0)?.extract()?;
                    let value = tuple.get_item(1)?.to_object(py);
                    tree.insert(py, key_str, value)?;
                }
            }
        }

        Ok(tree)
    }

    /// Insert a key-value pair
    ///
    /// Uses force_insert which removes any conflicting prefix keys
    /// to ensure insertion always succeeds.
    fn insert(&mut self, _py: Python, key: String, value: PyObject) -> PyResult<()> {
        let key_bytes = key.into_bytes().into_boxed_slice();
        self.inner.force_insert(key_bytes, value);
        Ok(())
    }

    /// Get a value by key with optional default
    #[pyo3(signature = (key, default=None))]
    fn get(&self, py: Python, key: String, default: Option<PyObject>) -> PyResult<Option<PyObject>> {
        let key_bytes = key.as_bytes();
        match self.inner.get(key_bytes) {
            Some(value) => Ok(Some(value.clone_ref(py))),
            None => Ok(default.or_else(|| Some(py.None()))),
        }
    }

    /// Remove a key and return its value
    fn remove(&mut self, _py: Python, key: String) -> PyResult<PyObject> {
        let key_bytes = key.as_bytes();
        match self.inner.remove(key_bytes) {
            Some(value) => Ok(value),
            None => Err(PyErr::new::<PyKeyError, _>(format!("'{}'", key))),
        }
    }

    /// Clear all entries
    fn clear(&mut self) -> PyResult<()> {
        self.inner.clear();
        Ok(())
    }

    /// Check if TreeMap is empty
    fn is_empty(&self) -> PyResult<bool> {
        Ok(self.inner.is_empty())
    }

    /// Get item using [] syntax
    fn __getitem__(&self, py: Python, key: String) -> PyResult<PyObject> {
        let key_bytes = key.as_bytes();
        match self.inner.get(key_bytes) {
            Some(value) => Ok(value.clone_ref(py)),
            None => Err(PyErr::new::<PyKeyError, _>(format!("'{}'", key))),
        }
    }

    /// Set item using [] syntax
    fn __setitem__(&mut self, py: Python, key: String, value: PyObject) -> PyResult<()> {
        self.insert(py, key, value)
    }

    /// Delete item using del
    fn __delitem__(&mut self, py: Python, key: String) -> PyResult<()> {
        self.remove(py, key)?;
        Ok(())
    }

    /// Check if key exists using 'in' operator
    fn __contains__(&self, key: String) -> PyResult<bool> {
        let key_bytes = key.as_bytes();
        Ok(self.inner.contains_key(key_bytes))
    }

    /// Get length of TreeMap
    fn __len__(&self) -> PyResult<usize> {
        Ok(self.inner.len())
    }

    /// String representation for debugging
    fn __repr__(&self) -> PyResult<String> {
        Ok(format!("TreeMap(len={})", self.inner.len()))
    }

    /// String representation for display
    fn __str__(&self) -> PyResult<String> {
        Ok(format!("TreeMap with {} entries", self.inner.len()))
    }

    /// Iterator support - iterate over keys
    fn __iter__(&self, _py: Python) -> PyResult<PyTreeMapIter> {
        let keys: Vec<String> = self.inner
            .iter()
            .map(|(k, _)| String::from_utf8_lossy(k).into_owned())
            .collect();
        Ok(PyTreeMapIter::new(keys))
    }

    /// Get an iterator over keys
    fn keys(&self, _py: Python) -> PyResult<PyTreeMapKeys> {
        let keys: Vec<String> = self.inner
            .iter()
            .map(|(k, _)| String::from_utf8_lossy(k).into_owned())
            .collect();
        Ok(PyTreeMapKeys::new(keys))
    }

    /// Get an iterator over values
    fn values(&self, py: Python) -> PyResult<PyTreeMapValues> {
        let values: Vec<PyObject> = self.inner
            .iter()
            .map(|(_, v)| v.clone_ref(py))
            .collect();
        Ok(PyTreeMapValues::new(values))
    }

    /// Get an iterator over (key, value) pairs
    fn items(&self, py: Python) -> PyResult<PyTreeMapItems> {
        let items: Vec<(String, PyObject)> = self.inner
            .iter()
            .map(|(k, v)| (String::from_utf8_lossy(k).into_owned(), v.clone_ref(py)))
            .collect();
        Ok(PyTreeMapItems::new(items))
    }

    /// Get the first key-value pair matching a prefix
    ///
    /// Returns None if no keys match the prefix, otherwise returns
    /// a tuple of (key, value) for the first matching entry.
    fn get_prefix(&self, py: Python, prefix: String) -> PyResult<Option<(String, PyObject)>> {
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

    /// Get an iterator over all key-value pairs with a given prefix
    ///
    /// Returns an iterator that yields (key, value) tuples for all keys
    /// that start with the given prefix, in lexicographic order.
    fn prefix_iter(&self, py: Python, prefix: String) -> PyResult<PyPrefixIter> {
        let prefix_bytes = prefix.as_bytes();
        let items: Vec<(String, PyObject)> = self.inner
            .prefix(prefix_bytes)
            .map(|(k, v)| (String::from_utf8_lossy(k).into_owned(), v.clone_ref(py)))
            .collect();
        Ok(PyPrefixIter::new(items))
    }

    /// Get the first (minimum) key-value pair
    ///
    /// Returns the first key-value pair in lexicographic order,
    /// or None if the tree is empty.
    fn first(&self, py: Python) -> PyResult<Option<(String, PyObject)>> {
        match self.inner.first_key_value() {
            Some((key, value)) => {
                let key_str = String::from_utf8_lossy(key).into_owned();
                Ok(Some((key_str, value.clone_ref(py))))
            }
            None => Ok(None),
        }
    }

    /// Get the last (maximum) key-value pair
    ///
    /// Returns the last key-value pair in lexicographic order,
    /// or None if the tree is empty.
    fn last(&self, py: Python) -> PyResult<Option<(String, PyObject)>> {
        match self.inner.last_key_value() {
            Some((key, value)) => {
                let key_str = String::from_utf8_lossy(key).into_owned();
                Ok(Some((key_str, value.clone_ref(py))))
            }
            None => Ok(None),
        }
    }

    /// Remove and return the first (minimum) key-value pair
    ///
    /// Returns and removes the first key-value pair in lexicographic order,
    /// or None if the tree is empty.
    fn pop_first(&mut self, _py: Python) -> PyResult<Option<(String, PyObject)>> {
        match self.inner.pop_first() {
            Some((key, value)) => {
                let key_str = String::from_utf8_lossy(&key).into_owned();
                Ok(Some((key_str, value)))
            }
            None => Ok(None),
        }
    }

    /// Remove and return the last (maximum) key-value pair
    ///
    /// Returns and removes the last key-value pair in lexicographic order,
    /// or None if the tree is empty.
    fn pop_last(&mut self, _py: Python) -> PyResult<Option<(String, PyObject)>> {
        match self.inner.pop_last() {
            Some((key, value)) => {
                let key_str = String::from_utf8_lossy(&key).into_owned();
                Ok(Some((key_str, value)))
            }
            None => Ok(None),
        }
    }

    /// Fuzzy search for keys within a Levenshtein distance threshold
    ///
    /// Returns an iterator that yields (key, value, distance) tuples for all keys
    /// within the specified Levenshtein distance from the search key.
    ///
    /// # Arguments
    /// * `key` - The search key to match against
    /// * `max_distance` - Maximum Levenshtein distance (edit distance) allowed
    fn fuzzy_search(&self, py: Python, key: String, max_distance: usize) -> PyResult<PyFuzzyIter> {
        let key_bytes = key.as_bytes();
        let items: Vec<(String, PyObject, usize)> = self.inner
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
