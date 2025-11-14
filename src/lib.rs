use pyo3::prelude::*;

mod treemap;

#[pymodule]
fn _blart(_py: Python, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<treemap::PyTreeMap>()?;
    Ok(())
}
