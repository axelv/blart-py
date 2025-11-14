use pyo3::prelude::*;
use blart::TreeMap;

/// Adaptive radix tree implementation
#[pyclass(name = "PyTreeMap")]
pub struct PyTreeMap {
    inner: TreeMap<Box<[u8]>, PyObject>,
}

#[pymethods]
impl PyTreeMap {
    /// Create a new empty TreeMap
    #[new]
    fn new() -> Self {
        Self {
            inner: TreeMap::new(),
        }
    }
}
