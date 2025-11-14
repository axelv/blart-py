use pyo3::prelude::*;
use pyo3::exceptions::PyKeyError;
use pyo3::types::{PyDict, PyList};
use blart::TreeMap;

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
    fn insert(&mut self, _py: Python, key: String, value: PyObject) -> PyResult<()> {
        let key_bytes = key.into_bytes().into_boxed_slice();
        self.inner.try_insert(key_bytes, value)
            .map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(
                format!("Failed to insert key: {:?}", e)
            ))?;
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
}
