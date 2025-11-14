use pyo3::prelude::*;

/// Iterator for TreeMap keys
#[pyclass]
pub struct PyTreeMapIter {
    keys: Vec<String>,
    index: usize,
}

impl PyTreeMapIter {
    pub fn new(keys: Vec<String>) -> Self {
        Self { keys, index: 0 }
    }
}

#[pymethods]
impl PyTreeMapIter {
    fn __iter__(slf: PyRef<'_, Self>) -> PyRef<'_, Self> {
        slf
    }

    fn __next__(mut slf: PyRefMut<'_, Self>) -> Option<String> {
        if slf.index < slf.keys.len() {
            let key = slf.keys[slf.index].clone();
            slf.index += 1;
            Some(key)
        } else {
            None
        }
    }
}

/// Iterator for TreeMap keys (returned by .keys() method)
#[pyclass]
pub struct PyTreeMapKeys {
    keys: Vec<String>,
    index: usize,
}

impl PyTreeMapKeys {
    pub fn new(keys: Vec<String>) -> Self {
        Self { keys, index: 0 }
    }
}

#[pymethods]
impl PyTreeMapKeys {
    fn __iter__(slf: PyRef<'_, Self>) -> PyRef<'_, Self> {
        slf
    }

    fn __next__(mut slf: PyRefMut<'_, Self>) -> Option<String> {
        if slf.index < slf.keys.len() {
            let key = slf.keys[slf.index].clone();
            slf.index += 1;
            Some(key)
        } else {
            None
        }
    }
}

/// Iterator for TreeMap values
#[pyclass]
pub struct PyTreeMapValues {
    values: Vec<PyObject>,
    index: usize,
}

impl PyTreeMapValues {
    pub fn new(values: Vec<PyObject>) -> Self {
        Self { values, index: 0 }
    }
}

#[pymethods]
impl PyTreeMapValues {
    fn __iter__(slf: PyRef<'_, Self>) -> PyRef<'_, Self> {
        slf
    }

    fn __next__(mut slf: PyRefMut<'_, Self>, py: Python) -> Option<PyObject> {
        if slf.index < slf.values.len() {
            let value = slf.values[slf.index].clone_ref(py);
            slf.index += 1;
            Some(value)
        } else {
            None
        }
    }
}

/// Iterator for TreeMap items (key-value pairs)
#[pyclass]
pub struct PyTreeMapItems {
    items: Vec<(String, PyObject)>,
    index: usize,
}

impl PyTreeMapItems {
    pub fn new(items: Vec<(String, PyObject)>) -> Self {
        Self { items, index: 0 }
    }
}

#[pymethods]
impl PyTreeMapItems {
    fn __iter__(slf: PyRef<'_, Self>) -> PyRef<'_, Self> {
        slf
    }

    fn __next__(mut slf: PyRefMut<'_, Self>, py: Python) -> Option<(String, PyObject)> {
        if slf.index < slf.items.len() {
            let (key, value) = &slf.items[slf.index];
            let result = (key.clone(), value.clone_ref(py));
            slf.index += 1;
            Some(result)
        } else {
            None
        }
    }
}

/// Iterator for prefix queries - returns (key, value) tuples
#[pyclass]
pub struct PyPrefixIter {
    items: Vec<(String, PyObject)>,
    index: usize,
}

impl PyPrefixIter {
    pub fn new(items: Vec<(String, PyObject)>) -> Self {
        Self { items, index: 0 }
    }
}

#[pymethods]
impl PyPrefixIter {
    fn __iter__(slf: PyRef<'_, Self>) -> PyRef<'_, Self> {
        slf
    }

    fn __next__(mut slf: PyRefMut<'_, Self>, py: Python) -> Option<(String, PyObject)> {
        if slf.index < slf.items.len() {
            let (key, value) = &slf.items[slf.index];
            let result = (key.clone(), value.clone_ref(py));
            slf.index += 1;
            Some(result)
        } else {
            None
        }
    }
}
